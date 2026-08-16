"""Route-walking: when we move to the next hop, and when we refuse to."""

import json

import httpx
import pytest
import respx
from conftest import assert_no_leak

from gateway.upstream import (
    Attempt,
    UpstreamError,
    call_json,
    call_stream,
    is_retryable_status,
)

OLLAMA = "https://ollama.test/v1/chat/completions"
OPENROUTER = "https://openrouter.test/api/v1/chat/completions"

BODY = {"messages": [{"role": "user", "content": "hello"}]}


def ok(model: str, content: str = "hi") -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "id": "gen-upstream",
            "model": model,
            "provider": "SecretVendor",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": content}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
        },
    )


def sse(*chunks: dict, done: bool = True) -> httpx.Response:
    lines = [": OPENROUTER PROCESSING"]  # a keepalive comment, and itself a leak
    lines += [f"data: {json.dumps(c)}" for c in chunks]
    if done:
        lines.append("data: [DONE]")
    return httpx.Response(
        200,
        content=("\n\n".join(lines) + "\n\n").encode(),
        headers={"content-type": "text/event-stream"},
    )


def delta(text: str, model: str = "secret-primary:cloud") -> dict:
    return {
        "id": "gen-upstream",
        "model": model,
        "provider": "SecretVendor",
        "choices": [{"index": 0, "delta": {"content": text}}],
    }


@pytest.fixture
async def client():
    async with httpx.AsyncClient() as c:
        yield c


def test_retry_policy():
    assert is_retryable_status(429)
    assert is_retryable_status(500)
    assert is_retryable_status(503)
    # A malformed request fails identically on the fallback, and paying twice
    # for the same mistake helps nobody.
    assert not is_retryable_status(400)
    assert not is_retryable_status(401)
    assert not is_retryable_status(404)


@respx.mock
async def test_falls_back_on_5xx(client, cfg):
    primary = respx.post(OLLAMA).mock(return_value=httpx.Response(503, text="model unloaded"))
    fallback = respx.post(OPENROUTER).mock(
        return_value=ok("secret-vendor/secret-fallback")
    )

    att = Attempt(request_id="chatcmpl-x", alias="tutor")
    out = await call_json(client, cfg, cfg.aliases["tutor"], BODY, att)

    assert primary.called and fallback.called
    assert att.attempt == 1 and att.fell_back
    assert out["model"] == "tutor"
    assert_no_leak(json.dumps(out))


@respx.mock
async def test_falls_back_on_429(client, cfg):
    """The Ollama account is shared by the class, so 429 is the common case."""
    respx.post(OLLAMA).mock(return_value=httpx.Response(429, text="rate limited"))
    respx.post(OPENROUTER).mock(return_value=ok("secret-vendor/secret-fallback"))

    att = Attempt(request_id="chatcmpl-x", alias="tutor")
    await call_json(client, cfg, cfg.aliases["tutor"], BODY, att)
    assert att.fell_back


@respx.mock
async def test_falls_back_on_connection_error(client, cfg):
    respx.post(OLLAMA).mock(side_effect=httpx.ConnectError("no route to host"))
    respx.post(OPENROUTER).mock(return_value=ok("secret-vendor/secret-fallback"))

    att = Attempt(request_id="chatcmpl-x", alias="tutor")
    await call_json(client, cfg, cfg.aliases["tutor"], BODY, att)
    assert att.fell_back


@respx.mock
async def test_does_not_fall_back_on_client_error(client, cfg):
    primary = respx.post(OLLAMA).mock(
        return_value=httpx.Response(400, text="bad 'messages' field")
    )
    fallback = respx.post(OPENROUTER).mock(return_value=ok("x"))

    att = Attempt(request_id="chatcmpl-x", alias="tutor")
    with pytest.raises(UpstreamError) as exc:
        await call_json(client, cfg, cfg.aliases["tutor"], BODY, att)

    assert primary.called
    assert not fallback.called, "a client error must not burn the paid fallback"
    assert exc.value.status == 400


@respx.mock
async def test_exhausted_route_raises(client, cfg):
    respx.post(OLLAMA).mock(return_value=httpx.Response(503))
    respx.post(OPENROUTER).mock(return_value=httpx.Response(503))

    att = Attempt(request_id="chatcmpl-x", alias="tutor")
    with pytest.raises(UpstreamError):
        await call_json(client, cfg, cfg.aliases["tutor"], BODY, att)


@respx.mock
async def test_usage_and_cost_recorded(client, cfg):
    respx.post(OLLAMA).mock(return_value=httpx.Response(503))
    respx.post(OPENROUTER).mock(return_value=ok("secret-vendor/secret-fallback"))

    att = Attempt(request_id="chatcmpl-x", alias="tutor")
    await call_json(client, cfg, cfg.aliases["tutor"], BODY, att)

    assert (att.prompt_tokens, att.completion_tokens, att.total_tokens) == (10, 20, 30)
    assert not att.tokens_estimated
    # 10 tokens @ $1/M + 20 @ $2/M
    assert att.cost_usd == pytest.approx((10 * 1.0 + 20 * 2.0) / 1e6)


@respx.mock
async def test_tokens_estimated_when_upstream_omits_usage(client, cfg):
    respx.post(OPENROUTER).mock(
        return_value=httpx.Response(
            200,
            json={"id": "g", "model": "secret-vendor/secret-only",
                  "choices": [{"index": 0, "message": {"content": "x" * 200}}]},
        )
    )
    att = Attempt(request_id="chatcmpl-x", alias="solo")
    await call_json(client, cfg, cfg.aliases["solo"], BODY, att)
    assert att.tokens_estimated
    assert att.total_tokens > 0


# ---- streaming -------------------------------------------------------------


async def collect(stream) -> str:
    return b"".join([chunk async for chunk in stream]).decode()


@respx.mock
async def test_stream_is_masked_and_keepalives_dropped(client, cfg):
    respx.post(OLLAMA).mock(
        return_value=sse(
            delta("Hel"),
            delta("lo"),
            {"id": "gen-upstream", "model": "secret-primary:cloud", "choices": [],
             "usage": {"prompt_tokens": 7, "completion_tokens": 3, "total_tokens": 10}},
        )
    )

    att = Attempt(request_id="chatcmpl-stream", alias="tutor")
    text = await collect(await call_stream(client, cfg, cfg.aliases["tutor"], BODY, att))

    assert_no_leak(text)
    assert "OPENROUTER PROCESSING" not in text
    assert text.count('"model":"tutor"') == 3
    assert '"id":"chatcmpl-stream"' in text
    assert text.endswith("data: [DONE]\n\n")
    assert (att.prompt_tokens, att.completion_tokens) == (7, 3)
    assert not att.tokens_estimated


@respx.mock
async def test_stream_falls_back_before_first_token(client, cfg):
    """The whole point: the switch happens while nothing is on the wire yet."""
    respx.post(OLLAMA).mock(return_value=httpx.Response(500, text="boom"))
    respx.post(OPENROUTER).mock(
        return_value=sse(delta("from-fallback", model="secret-vendor/secret-fallback"))
    )

    att = Attempt(request_id="chatcmpl-stream", alias="tutor")
    text = await collect(await call_stream(client, cfg, cfg.aliases["tutor"], BODY, att))

    assert att.fell_back
    assert "from-fallback" in text
    assert_no_leak(text)


@respx.mock
async def test_stream_falls_back_when_upstream_sends_nothing(client, cfg):
    """A 200 with an empty body is a dead upstream, not a valid empty answer."""
    respx.post(OLLAMA).mock(
        return_value=httpx.Response(200, content=b"", headers={"content-type": "text/event-stream"})
    )
    respx.post(OPENROUTER).mock(return_value=sse(delta("rescued")))

    att = Attempt(request_id="chatcmpl-stream", alias="tutor")
    text = await collect(await call_stream(client, cfg, cfg.aliases["tutor"], BODY, att))
    assert att.fell_back
    assert "rescued" in text


@respx.mock
async def test_stream_estimates_tokens_without_usage_chunk(client, cfg):
    respx.post(OLLAMA).mock(return_value=sse(delta("a" * 100)))
    att = Attempt(request_id="chatcmpl-stream", alias="tutor")
    await collect(await call_stream(client, cfg, cfg.aliases["tutor"], BODY, att))
    assert att.tokens_estimated
    assert att.completion_tokens > 0

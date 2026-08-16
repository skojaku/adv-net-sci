"""Talking to the real providers, and hiding that we did.

Two rules drive everything here:

1. Nothing that identifies the real model or provider reaches the client. That
   means the response `model` field, the streamed chunks, the `id`, the
   provider-specific extras, and -- the one that is easy to forget -- error
   messages, which are where a rate-limit failure would otherwise announce
   exactly which model is behind the alias.

2. Fallback is decided before the first token leaves the gateway. Once bytes
   are on the wire to the client there is no way to switch upstream, so the
   first `data:` event is the commit point.
"""

from __future__ import annotations

import json
import secrets
import time
from collections.abc import AsyncIterator
from dataclasses import dataclass, field

import httpx

from .config import Alias, Config, Target

# Fields we are willing to forward. Anything else is dropped.
#
# This is an allowlist rather than a denylist on purpose: OpenRouter honours a
# `models` array and a `provider` block in the request body, so forwarding
# unknown fields would let a student name any model they like and walk straight
# around the alias.
ALLOWED_FIELDS = frozenset(
    {
        "messages", "temperature", "top_p", "top_k", "stop", "seed",
        "presence_penalty", "frequency_penalty", "response_format",
        "tools", "tool_choice", "parallel_tool_calls",
        "reasoning_effort", "reasoning", "stream",
    }
)

# Response fields that identify the upstream and must not survive masking.
LEAKY_FIELDS = ("provider", "system_fingerprint", "model_name", "openrouter")

# 4xx codes that describe the upstream rather than the request. See
# is_retryable_status for why these are worth another hop.
RETRYABLE_4XX = frozenset({401, 402, 403, 404, 408, 409, 429})


class UpstreamError(Exception):
    """An attempt failed. `retryable` decides whether we try the next hop."""

    def __init__(self, message: str, *, status: int | None = None, retryable: bool):
        super().__init__(message)
        self.status = status
        self.retryable = retryable


@dataclass
class Attempt:
    """Everything the ledger wants to know about one request."""

    request_id: str
    alias: str
    target: Target | None = None
    attempt: int = 0
    status: int = 0
    stream: bool = False
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    tokens_estimated: bool = False
    cost_usd: float = 0.0
    started: float = field(default_factory=time.monotonic)
    error: str | None = None

    @property
    def fell_back(self) -> bool:
        return self.attempt > 0

    @property
    def latency_ms(self) -> int:
        return int((time.monotonic() - self.started) * 1000)


def new_request_id() -> str:
    return "chatcmpl-" + secrets.token_hex(12)


def is_retryable_status(status: int) -> bool:
    """Decide whether the next hop is worth trying.

    A malformed request (400, 413, 422) fails identically everywhere, so
    retrying it only burns the paid fallback on the same mistake. Everything
    that points at the upstream rather than at the request gets another go.

    That includes several 4xx codes, which is the non-obvious part: an expired
    course credential (401), a key without access to a model (403), or a model
    id the provider has retired (404) are all *our* problems, and the next hop
    carries a different credential and a different catalogue. Treating them as
    fatal would let one stale key take the tutor down for the whole class.
    """
    return status in RETRYABLE_4XX or status >= 500


def build_payload(
    body: dict, alias: Alias, target: Target, cfg: Config
) -> dict:
    """Translate a client request into an upstream one."""
    payload = {k: v for k, v in body.items() if k in ALLOWED_FIELDS}
    payload["model"] = target.model

    # Clamp so a single request cannot swallow a whole quota, and so an alias
    # cannot be asked for more than the model behind it can produce.
    requested = body.get("max_tokens")
    ceiling = min(alias.max_tokens, cfg.server.max_tokens_per_request)
    payload["max_tokens"] = min(int(requested), ceiling) if requested else ceiling

    if payload.get("stream") and target.stream_usage:
        # Without this the final chunk carries no usage and the ledger has to
        # fall back to estimating tokens from character counts.
        payload["stream_options"] = {"include_usage": True}
    return payload


def headers_for(target: Target) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {target.api_key}",
        "Content-Type": "application/json",
        **target.extra_headers,
    }


def estimate_tokens(text: str) -> int:
    """Crude chars/4 fallback, used only when the upstream reports no usage."""
    return max(1, len(text) // 4)


def mask_body(obj: dict, alias_id: str, request_id: str) -> dict:
    """Rewrite a response object so it describes the alias, not the model."""
    obj = dict(obj)
    obj["model"] = alias_id
    obj["id"] = request_id
    for leaky in LEAKY_FIELDS:
        obj.pop(leaky, None)
    usage = obj.get("usage")
    if isinstance(usage, dict):
        # OpenRouter can attach the dollar cost, which is as good as naming the
        # model to anyone with a price list.
        obj["usage"] = {
            k: v for k, v in usage.items()
            if k in {"prompt_tokens", "completion_tokens", "total_tokens"}
        }

    # Reasoning models carry a `reasoning_details[].format` tag naming the
    # provider's reasoning dialect ("anthropic-claude-v1", "openai-responses-v1"
    # and so on). Normalise rather than delete: clients round-trip the field's
    # shape, and "unknown" is a value the API already produces.
    if obj.get("choices"):
        obj["choices"] = [_mask_choice(c) for c in obj["choices"]]
    return obj


def _mask_choice(choice: dict) -> dict:
    for key in ("message", "delta"):
        part = choice.get(key)
        details = part.get("reasoning_details") if isinstance(part, dict) else None
        if not isinstance(details, list):
            continue
        choice = dict(choice)
        part = dict(part)
        part["reasoning_details"] = [
            {**d, "format": "unknown"} if isinstance(d, dict) and "format" in d else d
            for d in details
        ]
        choice[key] = part
    return choice


def extract_usage(obj: dict) -> tuple[int, int, int] | None:
    usage = obj.get("usage")
    if not isinstance(usage, dict):
        return None
    prompt = int(usage.get("prompt_tokens") or 0)
    completion = int(usage.get("completion_tokens") or 0)
    total = int(usage.get("total_tokens") or (prompt + completion))
    if total == 0:
        return None
    return prompt, completion, total


def cost_for(cfg: Config, target: Target, prompt: int, completion: int) -> float:
    price = cfg.price(target)
    return (prompt * price.get("input", 0.0) + completion * price.get("output", 0.0)) / 1e6


async def call_json(
    client: httpx.AsyncClient, cfg: Config, alias: Alias, body: dict, att: Attempt
) -> dict:
    """Non-streaming path. All-or-nothing, so fallback is straightforward."""
    last: UpstreamError | None = None
    for i, target in enumerate(alias.route):
        att.attempt, att.target = i, target
        payload = build_payload(body, alias, target, cfg)
        try:
            resp = await client.post(
                f"{target.base_url}/chat/completions",
                json=payload,
                headers=headers_for(target),
                timeout=httpx.Timeout(
                    cfg.server.request_timeout_s, connect=cfg.server.connect_timeout_s
                ),
            )
        except httpx.HTTPError as exc:
            last = UpstreamError(f"{type(exc).__name__}: {exc}", retryable=True)
            att.error = str(last)
            continue

        if resp.status_code >= 400:
            snippet = resp.text[:500]
            last = UpstreamError(
                f"HTTP {resp.status_code}: {snippet}",
                status=resp.status_code,
                retryable=is_retryable_status(resp.status_code),
            )
            att.error = str(last)
            if last.retryable:
                continue
            raise last

        att.status = resp.status_code
        obj = resp.json()
        usage = extract_usage(obj)
        if usage is None:
            prompt = estimate_tokens(json.dumps(payload.get("messages", "")))
            completion = estimate_tokens(
                json.dumps(obj.get("choices", ""))
            )
            att.tokens_estimated = True
            usage = (prompt, completion, prompt + completion)
        att.prompt_tokens, att.completion_tokens, att.total_tokens = usage
        att.cost_usd = cost_for(cfg, target, usage[0], usage[1])
        return mask_body(obj, alias.id, att.request_id)

    raise last or UpstreamError("no upstream configured", retryable=False)


async def call_stream(
    client: httpx.AsyncClient, cfg: Config, alias: Alias, body: dict, att: Attempt
) -> AsyncIterator[bytes]:
    """Streaming path.

    Walks the route until one upstream produces a first `data:` event, then
    returns a generator that replays that event and everything after it. The
    walk happens before the caller has sent anything, which is what makes the
    fallback safe.
    """
    att.stream = True
    last: UpstreamError | None = None

    for i, target in enumerate(alias.route):
        att.attempt, att.target = i, target
        payload = build_payload(body, alias, target, cfg)
        resp = None
        try:
            req = client.build_request(
                "POST",
                f"{target.base_url}/chat/completions",
                json=payload,
                headers=headers_for(target),
                timeout=httpx.Timeout(
                    cfg.server.first_token_timeout_s,
                    connect=cfg.server.connect_timeout_s,
                ),
            )
            resp = await client.send(req, stream=True)

            if resp.status_code >= 400:
                snippet = (await resp.aread())[:500].decode("utf-8", "replace")
                await resp.aclose()
                last = UpstreamError(
                    f"HTTP {resp.status_code}: {snippet}",
                    status=resp.status_code,
                    retryable=is_retryable_status(resp.status_code),
                )
                att.error = str(last)
                if last.retryable:
                    continue
                raise last

            lines = resp.aiter_lines()
            first = await _first_data_line(lines)
        except UpstreamError:
            raise
        except (httpx.HTTPError, StopAsyncIteration) as exc:
            if resp is not None:
                await resp.aclose()
            last = UpstreamError(f"{type(exc).__name__}: {exc}", retryable=True)
            att.error = str(last)
            continue

        att.status = 200
        att.error = None
        return _replay(resp, lines, first, cfg, alias, payload, att)

    raise last or UpstreamError("no upstream configured", retryable=False)


async def _first_data_line(lines: AsyncIterator[str]) -> str:
    """Pull lines until a real `data:` event appears.

    Keepalive comments (OpenRouter sends `: OPENROUTER PROCESSING`) are not
    progress, and are also themselves a leak, so they do not count and are not
    forwarded.
    """
    async for line in lines:
        if line.startswith("data:"):
            return line
    raise StopAsyncIteration("upstream closed before sending any data")


async def _replay(
    resp: httpx.Response,
    lines: AsyncIterator[str],
    first: str,
    cfg: Config,
    alias: Alias,
    payload: dict,
    att: Attempt,
) -> AsyncIterator[bytes]:
    """Yield the committed stream, masked, while tallying usage."""
    deadline = time.monotonic() + cfg.server.request_timeout_s
    text_seen: list[str] = []
    usage: tuple[int, int, int] | None = None

    async def handle(line: str) -> bytes | None:
        nonlocal usage
        data = line[len("data:") :].strip()
        if data == "[DONE]":
            return b"data: [DONE]\n\n"
        try:
            obj = json.loads(data)
        except json.JSONDecodeError:
            return None  # not parseable, so not maskable, so not forwarded
        found = extract_usage(obj)
        if found:
            usage = found
        for choice in obj.get("choices") or []:
            delta = choice.get("delta") or {}
            if isinstance(delta.get("content"), str):
                text_seen.append(delta["content"])
        masked = mask_body(obj, alias.id, att.request_id)
        # A usage-only final chunk has no choices; forwarding it is harmless
        # and some clients read the token counts from it.
        return b"data: " + json.dumps(masked, separators=(",", ":")).encode() + b"\n\n"

    try:
        out = await handle(first)
        if out:
            yield out
        async for line in lines:
            if time.monotonic() > deadline:
                att.error = "request_timeout_s exceeded; stream cut"
                break
            if not line.startswith("data:"):
                continue  # comments and event: lines are dropped
            out = await handle(line)
            if out:
                yield out
                if out == b"data: [DONE]\n\n":
                    break
    except httpx.HTTPError as exc:
        # Past the commit point there is nowhere to fall back to. End the
        # stream cleanly and let the ledger record why.
        att.error = f"mid-stream {type(exc).__name__}: {exc}"
    finally:
        await resp.aclose()
        if usage is None:
            usage = (
                estimate_tokens(json.dumps(payload.get("messages", ""))),
                estimate_tokens("".join(text_seen)),
                0,
            )
            usage = (usage[0], usage[1], usage[0] + usage[1])
            att.tokens_estimated = True
        att.prompt_tokens, att.completion_tokens, att.total_tokens = usage
        if att.target is not None:
            att.cost_usd = cost_for(cfg, att.target, usage[0], usage[1])

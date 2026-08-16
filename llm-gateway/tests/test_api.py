"""End-to-end through the HTTP surface: keys, quota, and what a client sees."""

import json

import httpx
import pytest
import respx
from conftest import assert_no_leak
from fastapi.testclient import TestClient

from gateway.app import create_app
from gateway.db import Database

OLLAMA = "https://ollama.test/v1/chat/completions"
OPENROUTER = "https://openrouter.test/api/v1/chat/completions"


def upstream_ok(content="hi", prompt=10, completion=20):
    return httpx.Response(
        200,
        json={
            "id": "gen-upstream",
            "model": "secret-primary:cloud",
            "provider": "SecretVendor",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": content}}],
            "usage": {"prompt_tokens": prompt, "completion_tokens": completion,
                      "total_tokens": prompt + completion},
        },
    )


@pytest.fixture
def env(tmp_path, config_path, monkeypatch):
    db_path = tmp_path / "gateway.db"
    monkeypatch.setenv("GATEWAY_CONFIG", str(config_path))
    monkeypatch.setenv("GATEWAY_DB", str(db_path))
    monkeypatch.setenv("TEST_OLLAMA_KEY", "k-ollama")
    monkeypatch.setenv("TEST_OPENROUTER_KEY", "k-openrouter")
    return db_path


@pytest.fixture
def keys(env):
    db = Database(env)
    issued = {
        "alice": db.issue_key("alice", "Alice"),
        "bob": db.issue_key("bob", "Bob"),
        "rich-student": db.issue_key("rich-student"),
    }
    db.close()
    return issued


@pytest.fixture
def client(env, keys):
    with TestClient(create_app()) as c:
        yield c


def auth(key):
    return {"Authorization": f"Bearer {key}"}


def chat(**kw):
    return {"model": "tutor", "messages": [{"role": "user", "content": "hi"}], **kw}


def test_rejects_missing_key(client):
    r = client.post("/v1/chat/completions", json=chat())
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "invalid_api_key"


def test_rejects_unknown_key(client):
    r = client.post("/v1/chat/completions", json=chat(), headers=auth("sk-nsci-nope"))
    assert r.status_code == 401


def test_rejects_revoked_key(client, env, keys):
    db = Database(env)
    db.revoke_student_keys("bob")
    db.close()
    r = client.post("/v1/chat/completions", json=chat(), headers=auth(keys["bob"]))
    assert r.status_code == 401


def test_disabled_student_is_blocked(client, env, keys):
    db = Database(env)
    db.set_disabled("bob", True)
    db.close()
    r = client.post("/v1/chat/completions", json=chat(), headers=auth(keys["bob"]))
    assert r.status_code == 403


def test_models_lists_aliases_only(client, keys):
    r = client.get("/v1/models", headers=auth(keys["alice"]))
    assert r.status_code == 200
    ids = {m["id"] for m in r.json()["data"]}
    assert ids == {"tutor", "solo"}
    assert_no_leak(r.text)


def test_unknown_alias_is_404_and_lists_options(client, keys):
    r = client.post(
        "/v1/chat/completions", json=chat(model="gpt-5"), headers=auth(keys["alice"])
    )
    assert r.status_code == 404
    assert "tutor" in r.json()["error"]["message"]
    assert_no_leak(r.text)


@respx.mock
def test_successful_call_is_masked_and_recorded(client, env, keys):
    respx.post(OLLAMA).mock(return_value=upstream_ok())

    r = client.post("/v1/chat/completions", json=chat(), headers=auth(keys["alice"]))
    assert r.status_code == 200
    body = r.json()
    assert body["model"] == "tutor"
    assert body["id"].startswith("chatcmpl-")
    assert_no_leak(r.text)

    db = Database(env)
    row = db._conn.execute("SELECT * FROM requests").fetchone()
    assert row["student_id"] == "alice"
    assert row["alias"] == "tutor"
    # The ledger is the one place the real model is written down.
    assert row["upstream"] == "ollama:secret-primary:cloud"
    assert row["total_tokens"] == 30
    db.close()


@respx.mock
def test_streamed_call_is_masked(client, keys):
    chunks = [
        'data: {"id":"gen-x","model":"secret-primary:cloud","provider":"SecretVendor",'
        '"choices":[{"index":0,"delta":{"content":"Hi"}}]}',
        "data: [DONE]",
    ]
    respx.post(OLLAMA).mock(
        return_value=httpx.Response(
            200,
            content=("\n\n".join(chunks) + "\n\n").encode(),
            headers={"content-type": "text/event-stream"},
        )
    )
    with client.stream(
        "POST", "/v1/chat/completions", json=chat(stream=True), headers=auth(keys["alice"])
    ) as r:
        text = "".join(r.iter_text())
    assert r.status_code == 200
    assert_no_leak(text)
    assert '"model":"tutor"' in text


@respx.mock
def test_upstream_failure_is_502_without_detail(client, keys):
    """A dead backend must not announce which model died."""
    respx.post(OLLAMA).mock(
        return_value=httpx.Response(503, text="secret-primary:cloud is overloaded")
    )
    respx.post(OPENROUTER).mock(
        return_value=httpx.Response(429, text="secret-vendor/secret-fallback rate limit")
    )

    r = client.post("/v1/chat/completions", json=chat(), headers=auth(keys["alice"]))
    assert r.status_code == 502
    assert_no_leak(r.text)
    assert "request_id" in r.json()["error"]


@respx.mock
def test_quota_blocks_after_limit(client, env, keys):
    """The test config allows 3 requests per period."""
    respx.post(OLLAMA).mock(return_value=upstream_ok(prompt=1, completion=1))

    for _ in range(3):
        assert client.post(
            "/v1/chat/completions", json=chat(), headers=auth(keys["alice"])
        ).status_code == 200

    r = client.post("/v1/chat/completions", json=chat(), headers=auth(keys["alice"]))
    assert r.status_code == 402
    assert r.json()["error"]["code"] == "quota_exceeded"
    assert "3/3" in r.json()["error"]["message"]

    # One student's exhaustion does not touch anyone else's allowance.
    assert client.post(
        "/v1/chat/completions", json=chat(), headers=auth(keys["bob"])
    ).status_code == 200


@respx.mock
def test_token_quota_blocks(client, keys):
    """The test config allows 1000 tokens; one 600-token call leaves room, two do not."""
    respx.post(OLLAMA).mock(return_value=upstream_ok(prompt=300, completion=300))

    assert client.post(
        "/v1/chat/completions", json=chat(), headers=auth(keys["bob"])
    ).status_code == 200
    assert client.post(
        "/v1/chat/completions", json=chat(), headers=auth(keys["bob"])
    ).status_code == 200
    r = client.post("/v1/chat/completions", json=chat(), headers=auth(keys["bob"]))
    assert r.status_code == 402
    assert "token quota" in r.json()["error"]["message"]


@respx.mock
def test_quota_override_applies(client, keys):
    respx.post(OLLAMA).mock(return_value=upstream_ok(prompt=1, completion=1))
    for _ in range(5):  # past the default of 3
        assert client.post(
            "/v1/chat/completions", json=chat(), headers=auth(keys["rich-student"])
        ).status_code == 200


@respx.mock
def test_failed_requests_do_not_consume_quota(client, keys):
    respx.post(OLLAMA).mock(return_value=httpx.Response(503))
    respx.post(OPENROUTER).mock(return_value=httpx.Response(503))

    for _ in range(4):
        assert client.post(
            "/v1/chat/completions", json=chat(), headers=auth(keys["alice"])
        ).status_code == 502

    respx.post(OLLAMA).mock(return_value=upstream_ok())
    assert client.post(
        "/v1/chat/completions", json=chat(), headers=auth(keys["alice"])
    ).status_code == 200


@respx.mock
def test_usage_endpoint_reports_own_allowance(client, keys):
    respx.post(OLLAMA).mock(return_value=upstream_ok(prompt=5, completion=5))
    client.post("/v1/chat/completions", json=chat(), headers=auth(keys["alice"]))

    r = client.get("/v1/usage", headers=auth(keys["alice"]))
    assert r.json()["requests"] == {"used": 1, "limit": 3}
    assert r.json()["tokens"]["used"] == 10


def test_bad_body_is_400(client, keys):
    r = client.post("/v1/chat/completions", json={"model": "tutor"}, headers=auth(keys["alice"]))
    assert r.status_code == 400


def test_healthz_needs_no_key(client):
    assert client.get("/healthz").json() == {"ok": True}

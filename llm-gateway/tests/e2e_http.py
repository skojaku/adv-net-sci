"""End-to-end over real HTTP: fake upstream -> gateway -> client.

Not collected by pytest -- it binds ports. Run it directly:

    .venv/bin/python tests/e2e_http.py

It covers the one thing the in-process suite cannot: that a streamed
response actually arrives incrementally through uvicorn and Starlette
rather than being buffered and delivered in one lump.
"""
import asyncio, json, os, pathlib, tempfile, time, sys

import httpx, uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse

TMP = pathlib.Path(tempfile.mkdtemp())
UP_PORT, GW_PORT, DEAD_PORT = 8892, 8891, 8899

CONFIG = f"""
server:
  first_token_timeout_s: 3
  connect_timeout_s: 2
  request_timeout_s: 30
  max_concurrent_per_student: 2
  max_tokens_per_request: 4096
quota:
  period: day
  timezone: "UTC"
  default: {{ requests: 100, total_tokens: 100000 }}
providers:
  ollama:
    base_url: "http://127.0.0.1:{UP_PORT}/v1"
    api_key_env: E2E_OLLAMA_KEY
  openrouter:
    base_url: "http://127.0.0.1:{UP_PORT}/v1"
    api_key_env: E2E_OPENROUTER_KEY
  dead:
    base_url: "http://127.0.0.1:{DEAD_PORT}/v1"
    api_key_env: E2E_OLLAMA_KEY
aliases:
  tutor:
    max_tokens: 2048
    route:
      - {{ provider: ollama, model: "secret-primary:cloud" }}
  failover:
    max_tokens: 2048
    route:
      - {{ provider: dead, model: "secret-dead-model" }}
      - {{ provider: openrouter, model: "secret-vendor/secret-fallback" }}
pricing:
  "openrouter:secret-vendor/secret-fallback": {{ input: 1.0, output: 2.0 }}
"""

(TMP / "config.yaml").write_text(CONFIG)
os.environ.update(
    E2E_OLLAMA_KEY="k1", E2E_OPENROUTER_KEY="k2",
    GATEWAY_CONFIG=str(TMP / "config.yaml"), GATEWAY_DB=str(TMP / "gw.db"),
)

# ---- fake upstream ---------------------------------------------------------
up = FastAPI()
seen_payloads = []

@up.post("/v1/chat/completions")
async def completions(request: Request):
    payload = await request.json()
    seen_payloads.append((request.headers.get("authorization"), payload))
    if not payload.get("stream"):
        return JSONResponse({
            "id": "gen-upstream-77", "model": payload["model"], "provider": "SecretVendor",
            "system_fingerprint": "fp_secret",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "hello"}}],
            "usage": {"prompt_tokens": 11, "completion_tokens": 22, "total_tokens": 33,
                      "cost": 0.00042},
        })

    async def gen():
        yield b": OPENROUTER PROCESSING\n\n"
        for word in ["Small", "-world", " networks"]:
            chunk = {"id": "gen-upstream-77", "model": payload["model"],
                     "provider": "SecretVendor",
                     "choices": [{"index": 0, "delta": {"content": word}}]}
            yield b"data: " + json.dumps(chunk).encode() + b"\n\n"
            await asyncio.sleep(0.15)
        yield b"data: " + json.dumps({
            "id": "gen-upstream-77", "model": payload["model"], "choices": [],
            "usage": {"prompt_tokens": 5, "completion_tokens": 9, "total_tokens": 14},
        }).encode() + b"\n\n"
        yield b"data: [DONE]\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream")


SECRETS = ["secret-primary:cloud", "secret-vendor/secret-fallback", "secret-dead-model",
           "SecretVendor", "fp_secret", "gen-upstream-77", "0.00042"]
failures = []

def check(label, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {label}{'  ' + detail if detail and not cond else ''}")
    if not cond:
        failures.append(label)

def no_leak(label, blob):
    hit = [s for s in SECRETS if s in blob]
    check(f"{label}: no upstream identifiers", not hit, f"leaked {hit} in {blob[:200]}")


async def serve(app, port):
    cfg = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(cfg)
    task = asyncio.create_task(server.serve())
    while not server.started:
        await asyncio.sleep(0.05)
    return server, task


async def main():
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
    from gateway.db import Database
    from gateway.app import create_app

    db = Database(os.environ["GATEWAY_DB"]); key = db.issue_key("e2e-student"); db.close()

    up_srv, up_task = await serve(up, UP_PORT)
    gw_srv, gw_task = await serve(create_app(), GW_PORT)
    H = {"Authorization": f"Bearer {key}"}

    async with httpx.AsyncClient(base_url=f"http://127.0.0.1:{GW_PORT}", timeout=30) as c:
        print("\n[1] non-streaming")
        r = await c.post("/v1/chat/completions", headers=H,
                         json={"model": "tutor", "messages": [{"role": "user", "content": "hi"}]})
        body = r.json()
        check("200", r.status_code == 200, r.text)
        check("model is the alias", body["model"] == "tutor", str(body.get("model")))
        check("id is ours", body["id"].startswith("chatcmpl-"), body["id"])
        check("usage.cost stripped", "cost" not in body["usage"])
        check("content intact", body["choices"][0]["message"]["content"] == "hello")
        no_leak("non-streaming body", r.text)

        print("\n[2] upstream really got the real model name")
        _, payload = seen_payloads[-1]
        check("upstream model is real", payload["model"] == "secret-primary:cloud")
        check("max_tokens clamped to alias", payload["max_tokens"] == 2048, str(payload.get("max_tokens")))

        print("\n[3] streaming, and arriving incrementally")
        got, times = [], []
        t0 = time.monotonic()
        async with c.stream("POST", "/v1/chat/completions", headers=H,
                            json={"model": "tutor", "stream": True,
                                  "messages": [{"role": "user", "content": "hi"}]}) as r:
            check("200", r.status_code == 200)
            async for line in r.aiter_lines():
                if line.startswith("data:"):
                    got.append(line)
                    times.append(time.monotonic() - t0)
        blob = "\n".join(got)
        no_leak("stream", blob)
        check("keepalive comment dropped", "OPENROUTER PROCESSING" not in blob)
        check("terminates with [DONE]", got[-1].strip() == "data: [DONE]")
        text = "".join(
            json.loads(g[5:]).get("choices", [{}])[0].get("delta", {}).get("content", "")
            for g in got[:-1] if json.loads(g[5:]).get("choices")
        )
        check("reassembled text", text == "Small-world networks", repr(text))
        # If Starlette or httpx buffered, every chunk would land at once.
        spread = times[-2] - times[0]
        check("streamed, not buffered", spread > 0.25, f"all chunks within {spread:.3f}s")

        print("\n[4] escape hatch: student names their own model")
        r = await c.post("/v1/chat/completions", headers=H, json={
            "model": "tutor", "messages": [{"role": "user", "content": "hi"}],
            "models": ["openai/gpt-5"], "provider": {"order": ["OpenAI"]},
        })
        _, payload = seen_payloads[-1]
        check("`models` not forwarded", "models" not in payload)
        check("`provider` not forwarded", "provider" not in payload)
        check("still pinned to the alias", payload["model"] == "secret-primary:cloud")

        print("\n[5] fallback across a genuinely dead host")
        r = await c.post("/v1/chat/completions", headers=H,
                         json={"model": "failover", "messages": [{"role": "user", "content": "hi"}]})
        check("200 via fallback", r.status_code == 200, r.text)
        check("model is the alias", r.json()["model"] == "failover")
        no_leak("fallback body", r.text)
        _, payload = seen_payloads[-1]
        check("fallback used the second hop", payload["model"] == "secret-vendor/secret-fallback")

        print("\n[6] ledger")
        db = Database(os.environ["GATEWAY_DB"])
        rows = db._conn.execute("SELECT * FROM requests ORDER BY id").fetchall()
        # four requests were sent: non-stream, stream, escape-hatch, fallback
        check("one row per request", len(rows) == 4, f"{len(rows)} rows")
        streamed = [r for r in rows if r["stream"]][0]
        check("stream usage captured", (streamed["prompt_tokens"], streamed["completion_tokens"]) == (5, 9),
              f"{streamed['prompt_tokens']}/{streamed['completion_tokens']}")
        check("stream tokens not estimated", streamed["tokens_estimated"] == 0)
        fb = [r for r in rows if r["fell_back"]][0]
        check("fallback recorded", fb["upstream"] == "openrouter:secret-vendor/secret-fallback",
              fb["upstream"])
        check("cost computed", abs(fb["cost_usd"] - (11 * 1.0 + 22 * 2.0) / 1e6) < 1e-12,
              str(fb["cost_usd"]))
        check("real model in the ledger only", rows[0]["upstream"] == "ollama:secret-primary:cloud")
        db.close()

        print("\n[7] revocation takes effect immediately")
        db = Database(os.environ["GATEWAY_DB"]); db.revoke_student_keys("e2e-student"); db.close()
        r = await c.post("/v1/chat/completions", headers=H,
                         json={"model": "tutor", "messages": [{"role": "user", "content": "hi"}]})
        check("401 after revoke", r.status_code == 401, r.text)

    for s, t in ((gw_srv, gw_task), (up_srv, up_task)):
        s.should_exit = True
        await t

    print(f"\n{'ALL PASS' if not failures else 'FAILURES: ' + str(failures)}")
    return 1 if failures else 0


raise SystemExit(asyncio.run(main()))

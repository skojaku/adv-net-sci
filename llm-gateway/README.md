# Course LLM gateway

One API key per student, a per-student allowance in requests and tokens, and a
model catalogue that consists entirely of aliases. Ollama is tried first and
OpenRouter picks up whatever Ollama drops.

Students point `pi` at it and see three models called `tutor`, `vision`, and
`referee`. What is actually behind those names is on the server and nowhere
else.

```
pi ──Bearer sk-nsci-…──▶ gateway ──┬─▶ Ollama       (primary)
                                   └─▶ OpenRouter   (fallback)
```

## What it does

| | |
|---|---|
| **Keys** | `sk-nsci-…`, one or more per student, stored as SHA-256 hashes. Revocable, optionally expiring. |
| **Allowance** | Requests and total tokens, per term / week / day. Per-student overrides. Failed requests do not count. |
| **Aliases** | `tutor` → a route of real models. `/v1/models` lists only aliases. |
| **Fallback** | Connection failure, timeout, 5xx, and the 4xx codes that describe *us* rather than the request (401/403/404/429). Never on a malformed request. |
| **Ledger** | One SQLite row per request: student, alias, real upstream, tokens, dollar cost, latency, whether it fell back. |

Dollar cost is recorded for the instructor but is **not** what students are
limited by — the quota is requests and tokens, which is stable even when the
model behind an alias changes.

With `period: term`, usage before `term_start` counts too. Keys get handed out
in the week before the first class, and a window that opens in the future would
leave exactly that period unmetered.

## Hiding the model name

This is the part that is easy to get subtly wrong, so it is worth naming the
four places a model name would otherwise escape:

1. **The response body.** `model` is rewritten to the alias, and `id` is
   replaced with our own, so an OpenRouter `gen-…` id does not identify the
   provider either.
2. **Every streamed chunk.** Each `data:` event is parsed, masked, and
   re-serialised. Keepalive comments (`: OPENROUTER PROCESSING`) are dropped
   rather than forwarded.
3. **Errors.** Upstream error text never reaches the client — a rate-limit
   message would otherwise say exactly which model is behind the alias.
   Students get a generic 502 plus a `request_id` to quote; the real error is
   in the ledger.
4. **`usage.cost`.** OpenRouter can attach the dollar cost, which identifies
   the model to anyone holding a price list. Stripped.
5. **`reasoning_details[].format`.** Reasoning models tag their chain of
   thought with the provider's dialect (`anthropic-claude-v1`,
   `openai-responses-v1`). Normalised to `unknown`, in both the message and the
   streamed delta.

> **What this does not hide: the model's own self-knowledge.** A student who
> asks the tutor "what model are you?" may well get an honest answer, and no
> amount of field masking changes that. Aliasing hides the plumbing — the
> config, the catalogue, the wire format — so that nothing *the gateway emits*
> names the backend. Treat it as removing the obvious signposts, not as a
> guarantee.

There is also a fifth, in the opposite direction: **the request**. OpenRouter
honours `models` and `provider` fields in the request body, so a passthrough
proxy would let a student write `"models": ["openai/gpt-5"]` and route around
the alias entirely. Request fields are therefore allowlisted, not filtered.

`tests/test_masking.py` and `tests/test_fallback.py` assert all of this against
a config whose real model names are `secret-…`, so a leak fails the suite
rather than the term.

> **This repository is public.** `config.yaml` — the real alias mapping — is
> gitignored, and only `config.example.yaml` with a deliberately fake mapping
> is committed. Publishing the true mapping would defeat the entire feature.

## Install

```bash
rsync -az --exclude .venv --exclude 'config.yaml' llm-gateway/ root@smallvm:/opt/llm-gateway/
ssh root@smallvm 'bash /opt/llm-gateway/deploy/provision.sh llm.example.edu'
```

Run it without a hostname (or with a bare IP) on a box that has no DNS record
yet: it provisions everything, skips Caddy, and leaves the gateway on loopback,
reachable for testing over `ssh -N -L 8080:127.0.0.1:8080 <host>`. Re-run with
a real name once you have one to add HTTPS.

Then, on the VM:

1. Write the real mapping into `/etc/llm-gateway/config.yaml`
   (start from `config.example.yaml`).
2. Put `OLLAMA_API_KEY` and `OPENROUTER_API_KEY` into `/etc/llm-gateway/env`.
3. `gateway-admin check-config` — prints every alias and its route, and fails
   loudly on a bad config rather than at 3am in a systemd log.
4. `systemctl restart llm-gateway && curl https://llm.example.edu/healthz`

Caddy handles TLS; the gateway binds loopback only. There is no admin HTTP
API — keys are minted over SSH, so the only thing facing the internet is the
completions endpoint.

### Ollama: pick one of two shapes

Both work; set `base_url` to match what you chose.

- **Hosted** — `https://ollama.com/v1` with an API key from ollama.com. This is
  what the example config assumes, and what the deployed gateway runs on.
- **Local daemon** — `http://127.0.0.1:11434/v1`, with `ollama` installed on
  the VM and signed in; it forwards models upstream with the account's own
  credentials, and the gateway's `OLLAMA_API_KEY` is then just a placeholder.

> **The two catalogues use different model ids.** The local daemon calls cloud
> models `glm-5.2:cloud`; the hosted API calls the same model `glm-5.2`. Copying
> an id from `ollama list` into a hosted-endpoint config yields a 404 — which is
> retryable, so the gateway falls silently through to the paid provider and
> everything keeps working while quietly costing money. List the ids you can
> actually reach before trusting a mapping:
>
> ```bash
> curl -s https://ollama.com/v1/models -H "Authorization: Bearer $OLLAMA_API_KEY" \
>   | python3 -c 'import json,sys; [print(m["id"]) for m in json.load(sys.stdin)["data"]]'
> ```
>
> After any model change, check that `gateway-admin usage` still shows a
> `fallbacks` count of zero. A silent fallback is the failure mode this design
> is most exposed to, precisely because nothing looks broken.

### TLS without buying a domain

Caddy needs a hostname, not an address — but it does not have to be a hostname
you own. `sslip.io` resolves `<dashed-ip>.sslip.io` to that IP, and Let's
Encrypt issues for it:

```bash
bash deploy/provision.sh 142-93-202-237.sslip.io   # your droplet's IP, dashed
```

Verified working: valid Let's Encrypt certificate, HTTP/2, streaming passes
through Caddy unbuffered. The caveat is that sslip.io is not on the Public
Suffix List, so Let's Encrypt's per-domain rate limit is shared with every
other sslip.io user; issuance can be refused during a busy week. Fine for
getting started, worth replacing with a real subdomain before the term.

## Running it

```bash
gateway-admin check-config              # validate, print routes
gateway-admin issue alice --name Alice  # prints the key, once
gateway-admin issue-batch roster.csv --expires 2026-12-20T00:00:00+00:00 > keys.csv
gateway-admin list
gateway-admin usage                     # per-student report for the period
gateway-admin revoke alice              # kill their keys
gateway-admin disable alice             # keep the key, block the account
```

`issue-batch` reads a CSV with an `id` column (and optionally `name`) and writes
`id,name,api_key`. Keys are shown once and only hashes are kept, so distribute
that file and then delete it.

Students can check their own remaining allowance at `GET /v1/usage`.

## Student setup

Merge `client/models.json.example` into `~/.pi/agent/models.json`, set the
`baseUrl` to the real hostname, and paste the issued key. For the tutor scripts,
the alias goes where the model id used to:

```bash
TUTOR_MODEL="netsci/tutor" ./run_tutor.sh
```

To keep keys out of config files, leave the placeholder `apiKey` in place and
pass the key per run instead:

```bash
pi --api-key "$NETSCI_API_KEY" --model netsci/tutor
```

## Operational notes

- **Concurrency is capped per student** (default 2). The Ollama account is
  shared by the whole class, so without this one student in a retry loop pushes
  everyone else onto the paid fallback. Over the cap, requests wait 30s and then
  get a 429.
- **`max_tokens` is clamped** to the alias ceiling, so one request cannot eat an
  allowance.
- **Request and response bodies are never logged.** Students discuss their own
  work through here; the ledger records metadata only, and uvicorn's access log
  is off for the same reason.
- **Watch the fallback rate.** `gateway-admin usage` has a `fallbacks` column.
  A number climbing across the class means Ollama is rate-limiting and the term
  is quietly moving onto OpenRouter's meter.
- **Check Ollama's terms.** Driving one account with a whole class's traffic may
  not be permitted, independent of whether it works. If it isn't, reorder the
  routes so a cheap OpenRouter model is primary; nothing else changes.

## Tests

```bash
uv venv --python 3.12 .venv && uv pip install -e ".[dev]"
.venv/bin/python -m pytest          # 35 tests, no network, respx fakes both providers
.venv/bin/python tests/e2e_http.py  # real uvicorn, real sockets, fake upstream
```

The e2e script is separate because it binds ports. It covers what the
in-process suite cannot: that a streamed response actually arrives
incrementally rather than being buffered and delivered in one lump, and that
fallback works across a genuinely dead host rather than a mocked exception.

## Layout

```
gateway/config.py     alias -> real model resolution; the only module that
                      knows what is behind an alias
gateway/db.py         SQLite key store and usage ledger
gateway/upstream.py   route walking, fallback, and masking
gateway/app.py        the HTTP surface
gateway/cli.py        gateway-admin
deploy/               systemd unit, Caddyfile, provision.sh
client/               the pi provider block students install
```

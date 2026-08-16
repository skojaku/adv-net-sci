"""The HTTP surface: an OpenAI-compatible endpoint students point `pi` at.

Deliberately small. There is no admin API -- keys are issued and revoked with
`gateway-admin` over SSH, so the only thing exposed to the internet is the
completions endpoint and a health check.

Request and response *bodies* are never logged. Students discuss their own work
with the tutor through here, and the ledger only needs metadata.
"""

from __future__ import annotations

import asyncio
import logging
import os
from contextlib import asynccontextmanager

import httpx
from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse

from .config import Alias, Config, load_config
from .db import Database, KeyRecord
from .upstream import Attempt, UpstreamError, call_json, call_stream, new_request_id

log = logging.getLogger("gateway")
router = APIRouter()


def error_response(status: int, message: str, code: str, request_id: str | None = None):
    payload = {"error": {"message": message, "type": "gateway_error", "code": code}}
    if request_id:
        payload["error"]["request_id"] = request_id
    return JSONResponse(status_code=status, content=payload)


@asynccontextmanager
async def lifespan(app: FastAPI):
    cfg = load_config()
    db = Database(os.environ.get("GATEWAY_DB", "gateway.db"))
    app.state.cfg = cfg
    app.state.db = db
    app.state.slots = {}  # student_id -> asyncio.Semaphore
    app.state.client = httpx.AsyncClient(
        limits=httpx.Limits(max_connections=64, max_keepalive_connections=16),
        follow_redirects=False,
    )
    log.info(
        "gateway up: %d aliases, quota=%s/%s per %s",
        len(cfg.aliases),
        cfg.default_quota.requests,
        cfg.default_quota.total_tokens,
        cfg.period,
    )
    try:
        yield
    finally:
        await app.state.client.aclose()
        db.close()


def create_app() -> FastAPI:
    app = FastAPI(title="adv-net-sci LLM gateway", lifespan=lifespan, docs_url=None,
                  redoc_url=None, openapi_url=None)

    @app.exception_handler(HTTPException)
    async def as_openai_error(request: Request, exc: HTTPException):
        # OpenAI-shaped errors, because that is what the clients parse. Without
        # this they surface FastAPI's {"detail": ...} as an unhelpful blank.
        codes = {401: "invalid_api_key", 402: "quota_exceeded", 403: "account_disabled",
                 404: "model_not_found", 429: "rate_limited"}
        return error_response(
            exc.status_code, str(exc.detail), codes.get(exc.status_code, "bad_request")
        )

    app.include_router(router)
    return app


# ---- auth and quota --------------------------------------------------------


async def authenticate(
    request: Request, authorization: str = Header(default="")
) -> KeyRecord:
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(401, "missing bearer token")
    record: KeyRecord | None = request.app.state.db.lookup_key(token.strip())
    if record is None:
        raise HTTPException(401, "unknown, revoked, or expired API key")
    if record.disabled:
        raise HTTPException(403, "this account is disabled; contact the instructor")
    return record


def check_quota(cfg: Config, db: Database, student_id: str) -> None:
    quota = cfg.quota_for(student_id)
    used = db.usage_since(student_id, cfg.period_start().isoformat())
    if used.requests >= quota.requests:
        raise HTTPException(
            402,
            f"request quota exhausted for this {cfg.period}: "
            f"{used.requests}/{quota.requests} requests used",
        )
    if used.total_tokens >= quota.total_tokens:
        raise HTTPException(
            402,
            f"token quota exhausted for this {cfg.period}: "
            f"{used.total_tokens}/{quota.total_tokens} tokens used",
        )


def slot_for(app: FastAPI, student_id: str) -> asyncio.Semaphore:
    slots = app.state.slots
    if student_id not in slots:
        slots[student_id] = asyncio.Semaphore(
            app.state.cfg.server.max_concurrent_per_student
        )
    return slots[student_id]


# ---- endpoints -------------------------------------------------------------


@router.get("/healthz")
async def healthz():
    return {"ok": True}


@router.get("/v1/models")
async def list_models(request: Request, key: KeyRecord = Depends(authenticate)):
    """Aliases only. This is the whole catalogue as far as a student knows."""
    cfg: Config = request.app.state.cfg
    return {
        "object": "list",
        "data": [
            {
                "id": alias.id,
                "object": "model",
                "owned_by": "adv-net-sci",
                "context_window": alias.context_window,
                "max_tokens": alias.max_tokens,
            }
            for alias in cfg.aliases.values()
        ],
    }


@router.get("/v1/usage")
async def my_usage(request: Request, key: KeyRecord = Depends(authenticate)):
    """Lets a student see how much of their own allowance is left."""
    cfg: Config = request.app.state.cfg
    db: Database = request.app.state.db
    quota = cfg.quota_for(key.student_id)
    used = db.usage_since(key.student_id, cfg.period_start().isoformat())
    return {
        "period": cfg.period,
        "period_start": cfg.period_start().isoformat(),
        "requests": {"used": used.requests, "limit": quota.requests},
        "tokens": {"used": used.total_tokens, "limit": quota.total_tokens},
    }


@router.post("/v1/chat/completions")
async def chat_completions(request: Request, key: KeyRecord = Depends(authenticate)):
    cfg: Config = request.app.state.cfg
    db: Database = request.app.state.db

    try:
        body = await request.json()
    except ValueError:
        raise HTTPException(400, "request body is not valid JSON")
    if not isinstance(body, dict) or not body.get("messages"):
        raise HTTPException(400, "'messages' is required")

    alias_id = body.get("model")
    alias: Alias | None = cfg.aliases.get(alias_id) if isinstance(alias_id, str) else None
    if alias is None:
        # Deliberately does not echo what was asked for. Reflecting client input
        # back into an error is how a scanner ends up unable to tell a real leak
        # from the caller's own string, and it is one less injection surface.
        raise HTTPException(
            404, f"unknown model. Available: {', '.join(sorted(cfg.aliases))}"
        )

    check_quota(cfg, db, key.student_id)

    att = Attempt(request_id=new_request_id(), alias=alias.id)
    wants_stream = bool(body.get("stream"))
    slot = slot_for(request.app, key.student_id)

    try:
        await asyncio.wait_for(slot.acquire(), timeout=30)
    except asyncio.TimeoutError:
        raise HTTPException(
            429,
            f"you already have {cfg.server.max_concurrent_per_student} requests in "
            "flight; wait for one to finish",
        )

    settled = False

    def settle() -> None:
        """Write the ledger row and give the concurrency slot back. Idempotent.

        For a streamed response this runs when the generator finishes, not when
        the handler returns -- the slot is held for as long as the student is
        actually occupying an upstream connection.
        """
        nonlocal settled
        if settled:
            return
        settled = True
        try:
            db.record(
                student_id=key.student_id,
                alias=att.alias,
                upstream=str(att.target) if att.target else None,
                attempt=att.attempt,
                fell_back=int(att.fell_back),
                status=att.status,
                stream=int(att.stream),
                prompt_tokens=att.prompt_tokens,
                completion_tokens=att.completion_tokens,
                total_tokens=att.total_tokens,
                tokens_estimated=int(att.tokens_estimated),
                cost_usd=att.cost_usd,
                latency_ms=att.latency_ms,
                error=att.error,
            )
            log.info(
                "%s student=%s alias=%s upstream=%s status=%s tokens=%d fell_back=%s %dms",
                att.request_id, key.student_id, att.alias, att.target, att.status,
                att.total_tokens, att.fell_back, att.latency_ms,
            )
        finally:
            slot.release()

    backend_down = (
        "the model backend is unavailable right now; please retry",
        "upstream_unavailable",
    )

    if not wants_stream:
        try:
            obj = await call_json(request.app.state.client, cfg, alias, body, att)
        except UpstreamError as exc:
            att.status, att.error = 502, str(exc)
            return error_response(502, *backend_down, att.request_id)
        except BaseException as exc:
            att.status, att.error = 500, f"{type(exc).__name__}: {exc}"
            raise
        finally:
            settle()
        return JSONResponse(obj)

    try:
        stream = await call_stream(request.app.state.client, cfg, alias, body, att)
    except UpstreamError as exc:
        att.status, att.error = 502, str(exc)
        settle()
        return error_response(502, *backend_down, att.request_id)
    except BaseException as exc:
        att.status, att.error = 500, f"{type(exc).__name__}: {exc}"
        settle()
        raise

    async def body_iter():
        try:
            async for chunk in stream:
                yield chunk
        finally:
            settle()

    return StreamingResponse(
        body_iter(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


app = create_app()

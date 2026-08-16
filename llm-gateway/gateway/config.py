"""Loading and validation of the gateway config.

Everything the gateway knows about real model names lives here and nowhere
else. The rest of the code deals in aliases and in `Target` objects it got from
this module, which keeps the "do not leak the model name" rule enforceable by
reading a small number of places.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import yaml


class ConfigError(Exception):
    """The config file is unusable. Raised at startup, never per-request."""


@dataclass(frozen=True)
class Target:
    """One concrete upstream: a real provider and a real model name."""

    provider: str
    model: str
    base_url: str
    api_key: str
    extra_headers: dict[str, str] = field(default_factory=dict)
    # Whether this provider accepts stream_options.include_usage. When false
    # the ledger has to estimate token counts for streamed requests.
    stream_usage: bool = True

    @property
    def pricing_key(self) -> str:
        return f"{self.provider}:{self.model}"

    def __str__(self) -> str:  # for the ledger, which is instructor-only
        return self.pricing_key


@dataclass(frozen=True)
class Alias:
    """What a student sees: a name, some capability metadata, and a route."""

    id: str
    name: str
    route: tuple[Target, ...]
    context_window: int = 128000
    max_tokens: int = 8192
    reasoning: bool = False
    input: tuple[str, ...] = ("text",)


@dataclass(frozen=True)
class Quota:
    requests: int
    total_tokens: int


@dataclass
class ServerSettings:
    host: str = "127.0.0.1"
    port: int = 8080
    connect_timeout_s: float = 10.0
    first_token_timeout_s: float = 45.0
    request_timeout_s: float = 600.0
    max_concurrent_per_student: int = 2
    max_tokens_per_request: int = 8192


@dataclass
class Config:
    server: ServerSettings
    aliases: dict[str, Alias]
    default_quota: Quota
    quota_overrides: dict[str, Quota]
    period: str
    term_start: date
    timezone: ZoneInfo
    pricing: dict[str, dict[str, float]]

    def quota_for(self, student_id: str) -> Quota:
        return self.quota_overrides.get(student_id, self.default_quota)

    def period_start(self, now: datetime | None = None) -> datetime:
        """Start of the window the quota is counted over."""
        now = (now or datetime.now(self.timezone)).astimezone(self.timezone)
        if self.period == "day":
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        if self.period == "week":
            midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
            return midnight - timedelta(days=midnight.weekday())
        return datetime.combine(
            self.term_start, datetime.min.time(), tzinfo=self.timezone
        )

    def price(self, target: Target) -> dict[str, float]:
        return self.pricing.get(target.pricing_key, {"input": 0.0, "output": 0.0})


def _require(mapping: dict, key: str, where: str):
    if key not in mapping:
        raise ConfigError(f"{where}: missing required key {key!r}")
    return mapping[key]


def load_config(path: str | os.PathLike | None = None, *, env: dict | None = None) -> Config:
    """Read the YAML config and resolve provider credentials from the env.

    Credentials are resolved once, at startup, so that a missing key is a boot
    failure rather than a confusing 500 in the middle of a lecture.
    """
    env = os.environ if env is None else env
    path = path or env.get("GATEWAY_CONFIG", "config.yaml")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh) or {}
    except FileNotFoundError as exc:
        raise ConfigError(f"config file not found: {path}") from exc

    server = ServerSettings(**(raw.get("server") or {}))

    # Providers: base URL plus a credential pulled from the environment.
    providers: dict[str, dict] = {}
    for name, spec in (_require(raw, "providers", "config") or {}).items():
        key_env = _require(spec, "api_key_env", f"providers.{name}")
        api_key = env.get(key_env, "")
        if not api_key:
            raise ConfigError(
                f"providers.{name}: environment variable {key_env} is unset or empty"
            )
        providers[name] = {
            "base_url": _require(spec, "base_url", f"providers.{name}").rstrip("/"),
            "api_key": api_key,
            "extra_headers": dict(spec.get("extra_headers") or {}),
            "stream_usage": bool(spec.get("stream_usage", True)),
        }

    aliases: dict[str, Alias] = {}
    for alias_id, spec in (_require(raw, "aliases", "config") or {}).items():
        route_spec = _require(spec, "route", f"aliases.{alias_id}")
        if not route_spec:
            raise ConfigError(f"aliases.{alias_id}: route is empty")
        route = []
        for i, hop in enumerate(route_spec):
            provider = _require(hop, "provider", f"aliases.{alias_id}.route[{i}]")
            if provider not in providers:
                raise ConfigError(
                    f"aliases.{alias_id}.route[{i}]: unknown provider {provider!r}"
                )
            route.append(
                Target(
                    provider=provider,
                    model=_require(hop, "model", f"aliases.{alias_id}.route[{i}]"),
                    base_url=providers[provider]["base_url"],
                    api_key=providers[provider]["api_key"],
                    extra_headers=providers[provider]["extra_headers"],
                    stream_usage=providers[provider]["stream_usage"],
                )
            )
        aliases[alias_id] = Alias(
            id=alias_id,
            name=spec.get("name", alias_id),
            route=tuple(route),
            context_window=int(spec.get("context_window", 128000)),
            max_tokens=int(spec.get("max_tokens", 8192)),
            reasoning=bool(spec.get("reasoning", False)),
            input=tuple(spec.get("input") or ("text",)),
        )

    quota_raw = raw.get("quota") or {}
    default_raw = quota_raw.get("default") or {}
    default_quota = Quota(
        requests=int(default_raw.get("requests", 2000)),
        total_tokens=int(default_raw.get("total_tokens", 4_000_000)),
    )
    overrides = {
        student: Quota(
            requests=int(spec.get("requests", default_quota.requests)),
            total_tokens=int(spec.get("total_tokens", default_quota.total_tokens)),
        )
        for student, spec in (quota_raw.get("overrides") or {}).items()
    }

    period = quota_raw.get("period", "term")
    if period not in {"term", "week", "day"}:
        raise ConfigError(f"quota.period must be term|week|day, got {period!r}")

    term_start = quota_raw.get("term_start")
    if isinstance(term_start, str):
        term_start = date.fromisoformat(term_start)
    elif term_start is None:
        term_start = date.today()

    return Config(
        server=server,
        aliases=aliases,
        default_quota=default_quota,
        quota_overrides=overrides,
        period=period,
        term_start=term_start,
        timezone=ZoneInfo(quota_raw.get("timezone", "UTC")),
        pricing={k: dict(v) for k, v in (raw.get("pricing") or {}).items()},
    )

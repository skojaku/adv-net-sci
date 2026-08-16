"""SQLite-backed key store and usage ledger.

Small enough for one course: ~30 students at a few thousand requests each is a
few hundred thousand rows over a term, which SQLite in WAL mode does not
notice. Keys are stored as SHA-256 hashes, so a leaked database file does not
hand anyone a working credential.
"""

from __future__ import annotations

import hashlib
import secrets
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

KEY_PREFIX = "sk-nsci-"

SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id          TEXT PRIMARY KEY,
    name        TEXT,
    created_at  TEXT NOT NULL,
    disabled    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS keys (
    key_hash    TEXT PRIMARY KEY,
    key_prefix  TEXT NOT NULL,
    student_id  TEXT NOT NULL REFERENCES students(id),
    created_at  TEXT NOT NULL,
    expires_at  TEXT,
    revoked_at  TEXT
);
CREATE INDEX IF NOT EXISTS keys_by_student ON keys(student_id);

-- One row per request that reached an upstream decision, including refusals.
-- `upstream` holds the real provider:model and is instructor-only data; it is
-- never rendered into a client response.
CREATE TABLE IF NOT EXISTS requests (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    ts                TEXT NOT NULL,
    student_id        TEXT NOT NULL,
    alias             TEXT NOT NULL,
    upstream          TEXT,
    attempt           INTEGER NOT NULL DEFAULT 0,
    fell_back         INTEGER NOT NULL DEFAULT 0,
    status            INTEGER NOT NULL,
    stream            INTEGER NOT NULL DEFAULT 0,
    prompt_tokens     INTEGER NOT NULL DEFAULT 0,
    completion_tokens INTEGER NOT NULL DEFAULT 0,
    total_tokens      INTEGER NOT NULL DEFAULT 0,
    tokens_estimated  INTEGER NOT NULL DEFAULT 0,
    cost_usd          REAL NOT NULL DEFAULT 0.0,
    latency_ms        INTEGER NOT NULL DEFAULT 0,
    error             TEXT
);
CREATE INDEX IF NOT EXISTS requests_by_student_ts ON requests(student_id, ts);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def generate_key() -> str:
    return KEY_PREFIX + secrets.token_urlsafe(24)


@dataclass(frozen=True)
class KeyRecord:
    student_id: str
    key_prefix: str
    disabled: bool


@dataclass(frozen=True)
class Usage:
    requests: int
    total_tokens: int
    cost_usd: float


class Database:
    def __init__(self, path: str | Path):
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        # check_same_thread=False because uvicorn's threadpool may touch this
        # from more than one thread; every write goes through a short
        # transaction, and WAL lets readers proceed during them.
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA busy_timeout=5000")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    @contextmanager
    def _tx(self):
        with self._conn:
            yield self._conn

    # ---- students and keys -------------------------------------------------

    def upsert_student(self, student_id: str, name: str | None = None) -> None:
        with self._tx() as conn:
            conn.execute(
                """INSERT INTO students(id, name, created_at) VALUES(?,?,?)
                   ON CONFLICT(id) DO UPDATE SET name=COALESCE(excluded.name, students.name)""",
                (student_id, name, now_iso()),
            )

    def issue_key(
        self, student_id: str, name: str | None = None, expires_at: str | None = None
    ) -> str:
        """Create a key and return it. This is the only time it is readable."""
        self.upsert_student(student_id, name)
        raw = generate_key()
        with self._tx() as conn:
            conn.execute(
                "INSERT INTO keys(key_hash, key_prefix, student_id, created_at, expires_at)"
                " VALUES(?,?,?,?,?)",
                (hash_key(raw), raw[: len(KEY_PREFIX) + 6], student_id, now_iso(), expires_at),
            )
        return raw

    def lookup_key(self, raw_key: str) -> KeyRecord | None:
        """Resolve a bearer token to a student, or None if it cannot be used."""
        row = self._conn.execute(
            """SELECT k.student_id, k.key_prefix, k.revoked_at, k.expires_at, s.disabled
                 FROM keys k JOIN students s ON s.id = k.student_id
                WHERE k.key_hash = ?""",
            (hash_key(raw_key),),
        ).fetchone()
        if row is None or row["revoked_at"] is not None:
            return None
        if row["expires_at"] and row["expires_at"] < now_iso():
            return None
        return KeyRecord(
            student_id=row["student_id"],
            key_prefix=row["key_prefix"],
            disabled=bool(row["disabled"]),
        )

    def revoke_student_keys(self, student_id: str) -> int:
        with self._tx() as conn:
            cur = conn.execute(
                "UPDATE keys SET revoked_at=? WHERE student_id=? AND revoked_at IS NULL",
                (now_iso(), student_id),
            )
        return cur.rowcount

    def set_disabled(self, student_id: str, disabled: bool) -> None:
        with self._tx() as conn:
            conn.execute(
                "UPDATE students SET disabled=? WHERE id=?", (int(disabled), student_id)
            )

    def list_students(self) -> list[sqlite3.Row]:
        return self._conn.execute(
            """SELECT s.id, s.name, s.disabled,
                      (SELECT COUNT(*) FROM keys k
                        WHERE k.student_id=s.id AND k.revoked_at IS NULL) AS active_keys
                 FROM students s ORDER BY s.id"""
        ).fetchall()

    # ---- ledger ------------------------------------------------------------

    def usage_since(self, student_id: str, since_iso: str) -> Usage:
        row = self._conn.execute(
            """SELECT COUNT(*) AS n,
                      COALESCE(SUM(total_tokens), 0) AS tok,
                      COALESCE(SUM(cost_usd), 0.0) AS usd
                 FROM requests
                WHERE student_id=? AND ts >= ? AND status < 400""",
            (student_id, since_iso),
        ).fetchone()
        return Usage(requests=row["n"], total_tokens=row["tok"], cost_usd=row["usd"])

    def usage_report(self, since_iso: str) -> list[sqlite3.Row]:
        return self._conn.execute(
            """SELECT student_id,
                      COUNT(*) AS requests,
                      COALESCE(SUM(total_tokens), 0) AS total_tokens,
                      COALESCE(SUM(cost_usd), 0.0) AS cost_usd,
                      COALESCE(SUM(fell_back), 0) AS fallbacks
                 FROM requests
                WHERE ts >= ? AND status < 400
                GROUP BY student_id ORDER BY total_tokens DESC""",
            (since_iso,),
        ).fetchall()

    LEDGER_COLUMNS = (
        "student_id", "alias", "upstream", "attempt", "fell_back", "status",
        "stream", "prompt_tokens", "completion_tokens", "total_tokens",
        "tokens_estimated", "cost_usd", "latency_ms", "error",
    )

    def record(self, **fields) -> None:
        """Append one row to the ledger.

        Only the fields actually supplied are written, so the NOT NULL columns
        fall back to their schema defaults instead of being handed an explicit
        NULL. Unknown fields are a programming error, not a silent no-op.
        """
        unknown = set(fields) - set(self.LEDGER_COLUMNS)
        if unknown:
            raise ValueError(f"unknown ledger columns: {sorted(unknown)}")
        cols = [c for c in self.LEDGER_COLUMNS if c in fields]
        values = [now_iso()] + [fields[c] for c in cols]
        placeholders = ",".join("?" * (len(cols) + 1))
        with self._tx() as conn:
            conn.execute(
                f"INSERT INTO requests(ts, {', '.join(cols)}) VALUES({placeholders})",
                values,
            )

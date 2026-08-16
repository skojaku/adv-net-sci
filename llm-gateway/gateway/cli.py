"""`gateway-admin` -- issue keys, revoke them, read the ledger.

Administration is deliberately CLI-only over SSH. An admin HTTP API would be
one more thing on the public internet holding the power to mint credentials,
for the sake of saving a `ssh smallvm`.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

from .config import load_config
from .db import Database


def _db(args) -> Database:
    return Database(args.db)


def cmd_issue(args) -> int:
    db = _db(args)
    if args.replace:
        n = db.revoke_student_keys(args.student)
        if n:
            print(f"revoked {n} existing key(s) for {args.student}", file=sys.stderr)
    key = db.issue_key(args.student, args.name, args.expires)
    # Printed once. There is no way to recover it later -- only the hash is kept.
    print(key)
    return 0


def cmd_issue_batch(args) -> int:
    """Read a roster CSV with at least an `id` column, write out id,key pairs."""
    db = _db(args)
    with open(args.roster, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows or "id" not in rows[0]:
        print("roster needs a header row with an 'id' column", file=sys.stderr)
        return 2

    out = csv.writer(sys.stdout)
    out.writerow(["id", "name", "api_key"])
    for row in rows:
        student = row["id"].strip()
        if not student:
            continue
        if args.replace:
            db.revoke_student_keys(student)
        out.writerow([student, row.get("name", ""), db.issue_key(student, row.get("name"), args.expires)])
    print(
        "\nKeys are shown once. Save this output somewhere safe, distribute it, "
        "then delete it.",
        file=sys.stderr,
    )
    return 0


def cmd_revoke(args) -> int:
    db = _db(args)
    n = db.revoke_student_keys(args.student)
    print(f"revoked {n} key(s) for {args.student}")
    return 0


def cmd_disable(args) -> int:
    db = _db(args)
    db.set_disabled(args.student, not args.enable)
    print(f"{args.student}: {'enabled' if args.enable else 'disabled'}")
    return 0


def cmd_list(args) -> int:
    db = _db(args)
    rows = db.list_students()
    if not rows:
        print("no students yet")
        return 0
    print(f"{'student':24} {'keys':>5} {'state':>9}  name")
    for r in rows:
        state = "disabled" if r["disabled"] else "active"
        print(f"{r['id']:24} {r['active_keys']:5} {state:>9}  {r['name'] or ''}")
    return 0


def cmd_usage(args) -> int:
    cfg = load_config(args.config)
    db = _db(args)
    since = cfg.period_start().isoformat()
    rows = db.usage_report(since)
    print(f"usage since {since} (period: {cfg.period})\n")
    print(f"{'student':24} {'reqs':>7} {'tokens':>12} {'fallbacks':>10} {'cost USD':>10}  quota")
    total_cost = 0.0
    for r in rows:
        quota = cfg.quota_for(r["student_id"])
        pct = 100 * r["total_tokens"] / quota.total_tokens if quota.total_tokens else 0
        total_cost += r["cost_usd"]
        print(
            f"{r['student_id']:24} {r['requests']:7} {r['total_tokens']:12} "
            f"{r['fallbacks']:10} {r['cost_usd']:10.4f}  {pct:.0f}% of tokens"
        )
    print(f"\n{'TOTAL':24} {'':7} {'':12} {'':10} {total_cost:10.4f}")
    return 0


def cmd_check_config(args) -> int:
    """Fail loudly at the terminal rather than at 3am in a systemd log."""
    cfg = load_config(args.config)
    print(f"config OK: {len(cfg.aliases)} aliases, period={cfg.period}")
    for alias in cfg.aliases.values():
        hops = " -> ".join(str(t) for t in alias.route)
        print(f"  {alias.id:12} {hops}")
    print(
        f"\nquota/{cfg.period}: {cfg.default_quota.requests} requests, "
        f"{cfg.default_quota.total_tokens} tokens (window opens {cfg.period_start()})"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="gateway-admin")
    p.add_argument("--db", default=os.environ.get("GATEWAY_DB", "gateway.db"))
    p.add_argument("--config", default=os.environ.get("GATEWAY_CONFIG", "config.yaml"))
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("issue", help="issue a key for one student")
    s.add_argument("student")
    s.add_argument("--name")
    s.add_argument("--expires", help="ISO timestamp, e.g. 2026-12-20T00:00:00+00:00")
    s.add_argument("--replace", action="store_true", help="revoke that student's old keys first")
    s.set_defaults(func=cmd_issue)

    s = sub.add_parser("issue-batch", help="issue keys for a roster CSV")
    s.add_argument("roster")
    s.add_argument("--expires")
    s.add_argument("--replace", action="store_true")
    s.set_defaults(func=cmd_issue_batch)

    s = sub.add_parser("revoke", help="revoke every key for a student")
    s.add_argument("student")
    s.set_defaults(func=cmd_revoke)

    s = sub.add_parser("disable", help="block a student without revoking their key")
    s.add_argument("student")
    s.add_argument("--enable", action="store_true", help="undo a disable")
    s.set_defaults(func=cmd_disable)

    sub.add_parser("list", help="list students").set_defaults(func=cmd_list)
    sub.add_parser("usage", help="usage report for the current period").set_defaults(func=cmd_usage)
    sub.add_parser("check-config", help="validate the config and show the routes").set_defaults(
        func=cmd_check_config
    )

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

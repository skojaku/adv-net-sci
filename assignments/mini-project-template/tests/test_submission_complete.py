"""Completeness checks for the mini-project submission.

This does NOT grade the work. It checks that what was pushed is a submission
at all — the report was written, the team was named, something was committed.
A human reads the report and decides what it is worth.

The distinction matters for what students are told: passing these checks means
"we received your project", not "your project is good". Keep it that way; the
moment this file starts scoring findings, teams optimise for the checker.

Run locally before you leave:  python -m pytest tests/ -q
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "report" / "report.md"
TEAM = ROOT / "TEAM.md"


def _uncommented(text: str) -> str:
    """The templates are mostly HTML comments; strip them before measuring."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()


def test_report_exists():
    assert REPORT.is_file(), (
        "report/report.md is missing. That file is the submission — without it "
        "there is nothing to read."
    )


def test_report_was_written():
    body = _uncommented(REPORT.read_text())
    # The template is headings and comments only, so anything that survives
    # comment-stripping beyond the headings is the team's own writing.
    prose = "\n".join(
        line for line in body.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ).strip()
    assert len(prose) >= 200, (
        f"report/report.md has {len(prose)} characters of prose outside the "
        "headings. Write what you did, what you found, and what surprised you "
        "— roughly a page."
    )


def test_report_has_every_section():
    body = REPORT.read_text().lower()
    for heading in ("the question", "what we did", "what we found",
                    "what surprised us"):
        assert heading in body, (
            f"report/report.md is missing the '{heading}' section. Keep the "
            "template's headings so the report is readable in one pass."
        )


def test_team_is_named():
    assert TEAM.is_file(), "TEAM.md is missing."
    rows = [
        line for line in TEAM.read_text().splitlines()
        if line.strip().startswith("|")
    ]
    # Drop the header and the |---|---| separator.
    filled = []
    for row in rows[2:]:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0] and cells[1]:
            filled.append(cells)
    assert filled, (
        "TEAM.md lists nobody. Put every teammate's name and GitHub username "
        "in the table — it is how a missing invitation gets caught."
    )
    assert any(len(c) >= 3 and c[2].lower().startswith("y") for c in filled), (
        "No founder marked in TEAM.md. The founder is whoever accepted the "
        "assignment and owns this repository."
    )


def test_team_usernames_look_real():
    """A GitHub username, not 'me' or the placeholder pipe characters."""
    rows = [
        line for line in TEAM.read_text().splitlines()
        if line.strip().startswith("|")
    ][2:]
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 2 or not cells[1]:
            continue
        user = cells[1].lstrip("@")
        assert re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38}", user), (
            f"{user!r} in TEAM.md is not a GitHub username. Use the login, not "
            "a display name or an email."
        )

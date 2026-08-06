#!/usr/bin/env python3
"""Does notebook.golden.py still say what a real session would say?

The reference notebook is hand-maintained, and three review rounds in a row
caught the same failure: a fix landed in `cells/*.py`, in the netviz helper,
or in the extension's emitted cell bodies, and never reached the golden copy.
Every one was invisible to the executable checks — the golden renders
perfectly either way, it just renders the OLD wording.

This compares the PROSE a reader sees, not the code: any sentence of four or
more words that a template puts on the page must appear in the golden too.

    python3 review_golden_sync.py     # lists drift, exit 1 if any
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
GOLDEN = re.sub(r"\s+", " ", (HERE / "notebook.golden.py").read_text().replace('\\"', '"'))

# Deliberate divergences. The golden is a FINISHED session with no photographs
# of its own, so it hardcodes the collapsed drop-box state instead of testing
# for a saved file, and it renders a placeholder where a photo would be.
EXEMPT = (
    "Your photo appears here",
    "This is exactly what your tutor will see",
    "A hand-in button appears here",
    "Press ▶ Run when you're ready",
)

def strip_comments(text: str) -> str:
    """A comment explains the cell to us; it never reaches the page."""
    text = re.sub(r"^\s*#[^\n]*$", "", text, flags=re.M)
    return re.sub(r"^\s*//[^\n]*$", "", text, flags=re.M)


def sentences(text: str):
    """Human prose inside a source file: the long string literals."""
    for lit in re.findall(r'"((?:[^"\\]|\\.)*)"', strip_comments(text)):
        lit = lit.replace('\\n', ' ').replace('\\"', '"')
        for part in re.split(r"(?<=[.!?])\s+", lit):
            part = re.sub(r"<[^>]+>", " ", part)          # strip html tags
            part = re.sub(r"\s+", " ", part).strip(" *_`")
            if len(part) < 30:
                continue
            if re.search(r"[=\[\]{}()]|:\w|\bdef\b|\balt\.|\bmo\.", part):
                continue                                   # code, not prose
            if re.search(r"\.(py|jpg|jpeg|png|ts)\b|/|`|\bnb_\w+", part):
                continue                                   # paths, code, tool names
            if len(re.findall(r"[A-Za-z]{2,}", part)) < 4:
                continue
            yield part

drift = []
sources = sorted((HERE / "cells").glob("*.py"))
for path in sources:
    for s in sentences(path.read_text()):
        if any(x in s for x in EXEMPT):
            continue
        if s not in GOLDEN:
            drift.append(f"{path.name}: {s[:78]}…")

# The netviz helper lives in the template and is copied into the golden.
tmpl = (HERE / "notebook.template.py").read_text()
m = re.search(r"const inkFor = \(hex\) => \{.*?\n  \};", tmpl, re.S)
if not m:
    drift.append("notebook.template.py: inkFor helper not found — renamed?")
elif re.sub(r"\s+", " ", m.group(0)) not in GOLDEN:
    drift.append("notebook.template.py: the golden's netviz helper differs from the template's")

# Prose the extension writes into student-facing cells.
# Prose the extension writes into the student-facing exercise cells. Only the
# 📨 lines: everything else it emits is refusal text the tutor reads, not page
# content, and matching on that produced nothing but noise.
# The extension emits student-facing cells as backtick templates. Page content
# is recognisable inside them: a line carrying both a backtick and a <span> is
# markdown headed for the notebook, not refusal text the tutor reads. Only the
# 📨 lines are checked — those are the ones that go stale in a finished
# notebook, and that is how this one drifted.
for line in (HERE / ".pi/extensions/notebook-tool.ts").read_text().split("\n"):
    if "📨" not in line or "`" not in line or "<span" not in line:
        continue
    for lit in re.findall(r'"([^"]+)"', line):
        frag = re.sub(r"<[^>]+>", " ", lit.replace("\\n", " "))
        frag = re.sub(r"\s+", " ", frag).strip(" *_`")
        if "📨" not in frag or len(frag) < 15 or any(x in frag for x in EXEMPT):
            continue
        if frag not in GOLDEN:
            drift.append(f"notebook-tool.ts: {frag[:78]}…")

if drift:
    print("GOLDEN DRIFT — notebook.golden.py is missing wording that a real session shows:")
    for d in drift:
        print(" -", d)
    sys.exit(1)
print("notebook.golden.py is in sync with cells/, the netviz helper and the emitted prose.")

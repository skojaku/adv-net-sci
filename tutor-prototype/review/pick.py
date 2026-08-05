#!/usr/bin/env python3
"""Answer a herdr-pane select dialog by LABEL, verifying the cursor each step.

The harness's dialog_choice.sh sends a fixed number of `down` keys and trusts
the list to start at the top. It does not always: two cp0 runs selected the
third option from `N=0`. This walks the cursor instead, re-reading the pane
after every key, so the option that gets Enter is the one we can see selected.

Usage: pick.py <agent> <substring of the option label> [--dry]
"""
import json
import re
import subprocess
import sys
import time

AGENT = sys.argv[1]
WANT = sys.argv[2].lower()
DRY = "--dry" in sys.argv


def screen() -> str:
    out = subprocess.run(
        ["herdr", "agent", "read", AGENT, "--source", "visible", "--lines", "60"],
        capture_output=True, text=True, check=True,
    ).stdout
    return json.loads(out)["result"]["read"]["text"]


def options(text: str):
    """(labels, cursor_index) for whichever dialog is on screen."""
    lines = text.split("\n")
    numbered, plain = [], []
    for ln in lines:
        m = re.match(r"^\s*([❯→>]?)\s*(\d+)\.\s+(\S.*)$", ln)
        if m:
            numbered.append((bool(m.group(1)), m.group(3).strip()))
            continue
        m = re.match(r"^\s*([❯→])\s+(\S.*)$", ln)
        if m:
            plain.append((True, m.group(2).strip()))
            continue
        if plain and re.match(r"^\s{2,}(\S.*)$", ln) and not ln.strip().startswith("↑"):
            plain.append((False, ln.strip()))
    items = numbered or plain
    if not items:
        return [], -1
    labels = [t for _, t in items]
    cursor = next((i for i, (c, _) in enumerate(items) if c), -1)
    return labels, cursor


def send(key: str):
    pane = json.loads(
        subprocess.run(["herdr", "agent", "get", AGENT], capture_output=True, text=True,
                       check=True).stdout
    )["result"]["agent"]["pane_id"]
    subprocess.run(["herdr", "pane", "send-keys", pane, key],
                   capture_output=True, check=True)


time.sleep(2)
labels, cursor = options(screen())
if not labels:
    print("NO DIALOG ON SCREEN"); sys.exit(2)
target = next((i for i, l in enumerate(labels) if WANT in l.lower()), -1)
print("options:", labels, "cursor:", cursor, "target:", target)
if target < 0:
    print("TARGET NOT FOUND"); sys.exit(2)

for _ in range(len(labels) * 3):
    labels, cursor = options(screen())
    if cursor == target:
        break
    # `down` only: `up` does not wrap past the first option in this widget,
    # so an upward walk from the top never moves and the loop spins out.
    send("down")
    time.sleep(0.6)
else:
    print("COULD NOT REACH TARGET"); sys.exit(2)

print("cursor now on:", labels[cursor])
if DRY:
    sys.exit(0)
send("enter")
print("SENT ENTER ->", labels[target])

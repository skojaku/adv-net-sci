#!/usr/bin/env bash
# Archive the current session and put a clean notebook in its place.
#
# Usage: ./reset_session.sh            # archive + reset, prints what it did
#        ./reset_session.sh --check    # say whether a session exists, change nothing
#
# Run this BEFORE the notebook server and the tutor start. A reset done at
# file level cannot half-succeed: no kernel to talk to, no model to instruct.
# The in-session nb_fresh_start still exists for a student who changes their
# mind mid-lesson, but it has to delete cells one at a time through a live
# kernel, and a single failure there leaves the "clean slate" opening on the
# middle of the module — which is exactly what happened: an archived log, a
# stale chapter_state saying "ch3", and a notebook whose first cell was
# chapter 3's heading.
#
# NOTHING IS DELETED. Everything moves into session_artifacts/ with a
# timestamp, because those files are the graded record of a real session.

set -euo pipefail
cd "$(dirname "$0")"

ART="session_artifacts"
STAMP=$(date +%Y%m%d-%H%M%S)

# Anything that says "a session happened here".
session_exists() {
  [ -s "$ART/session_log.jsonl" ] && return 0
  [ -f "$ART/chapter_state.json" ] && return 0
  # A notebook with named cells is a notebook that has been taught in;
  # the template's own cells are all unnamed (def _(...)).
  [ -f notebook.py ] && grep -qE '^def (ch[0-9]+_header|cp[0-9a-z_]+|session_record)' notebook.py && return 0
  return 1
}

if [ "${1:-}" = "--check" ]; then
  session_exists && echo "session-exists" || echo "clean"
  exit 0
fi

mkdir -p "$ART"

if ! session_exists; then
  echo "[reset] Nothing to archive — already a clean slate."
  [ -f notebook.py ] || cp notebook.template.py notebook.py
  exit 0
fi

moved=0
move() { # move <path> <archive name>
  [ -e "$1" ] || return 0
  mv "$1" "$ART/$2"
  echo "[reset] $1 -> $ART/$2"
  moved=$((moved + 1))
}

move notebook.py "notebook-${STAMP}.py"
move "$ART/session_log.jsonl" "session_log-${STAMP}.jsonl"
move "$ART/session_summary.md" "session_summary-${STAMP}.md"
move assets/uploads "uploads-${STAMP}"

# The saved chapter belongs to the log just archived. Left behind, it is read
# back as progress the new session never made.
if [ -f "$ART/chapter_state.json" ]; then
  rm -f "$ART/chapter_state.json"
  echo "[reset] $ART/chapter_state.json -> removed (belongs to the archived log)"
  moved=$((moved + 1))
fi

cp notebook.template.py notebook.py
echo "[reset] fresh notebook.py from notebook.template.py"
echo "[reset] Done — $moved item(s) archived. Nothing was deleted; it is all in $ART/."

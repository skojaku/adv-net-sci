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
  # A note the notebook was down for. It is flushed at the first build of
  # whatever session comes next, so "already a clean slate" must not leave
  # one behind — it would land in the next student's notebook.
  [ -n "$(ls -A "$ART/parked_notes" 2>/dev/null)" ] && return 0
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
move "$ART/student_signal.txt" "student_signal-${STAMP}.txt"
move "$ART/session_log.jsonl" "session_log-${STAMP}.jsonl"
move "$ART/session_summary.md" "session_summary-${STAMP}.md"
move assets/uploads "uploads-${STAMP}"
repoint_archive() { # repoint_archive <assets-subdir>
  # The archived notebook keeps its relative paths — assets/uploads/<w>_view.jpg
  # for a photographed page, assets/exercises/<name>.py for code the student
  # wrote — and neither exists once the directory is archived under a stamp. So
  # point the archived COPY at its own. (A shared session_artifacts/assets/
  # was tried first and was worse: the second reset overwrote it, so session
  # 1's keepsake rendered session 2's photograph as that student's own page.)
  [ -f "$ART/notebook-${STAMP}.py" ] || return 0
  [ -d "$ART/$1-${STAMP}" ] || return 0
  sed "s#assets/$1/#$1-${STAMP}/#g" "$ART/notebook-${STAMP}.py" \
    >"$ART/notebook-${STAMP}.py.tmp" &&
    mv "$ART/notebook-${STAMP}.py.tmp" "$ART/notebook-${STAMP}.py"
}
# The student's saved exercise code is their work too — and the coding cell
# renders whatever it finds under "The code I wrote and ran", so a file left
# here would greet the next student as their own.
move assets/exercises "exercises-${STAMP}"
repoint_archive uploads
repoint_archive exercises

# A note that could not be written belongs to the session just archived — and
# it is flushed at the first build of whatever session comes next, so left
# here it lands in the NEXT student's notebook quoting the previous student's
# answers in the first person.
if [ -d "$ART/parked_notes" ]; then
  move "$ART/parked_notes" "parked_notes-${STAMP}"
fi

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

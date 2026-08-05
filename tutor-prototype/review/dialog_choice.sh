#!/usr/bin/env bash
# Answer an on-screen select dialog (e.g. "Where to next?") by arrow keys.
#
# Usage: dialog_choice.sh <state_file> <option_index> [screen_lines]
#   option_index is 0-based: 0 = first option (just Enter), 1 = one Down, ...
set -euo pipefail
. "$(dirname "$0")/lib.sh"
. "${1:?usage: dialog_choice.sh <state_file> <option_index> [screen_lines]}"
N="${2:?0-based option index required}"

PANE=$(pane_id "$AGENT")
# Let the widget finish rendering before typing at it. A key sent into a
# half-drawn ask_user_question list landed on the wrong option once, and the
# resulting log ("Comfortable with Python" for a student who picked "I don't
# code") looked exactly like a tutor fabricating an answer. Do NOT try to
# "reset to the top" with repeated `up` — the list wraps, so that walks onto
# the free-text option and submits an empty answer.
sleep 3
for _ in $(seq 1 "$N"); do herdr pane send-keys "$PANE" down >/dev/null; sleep 0.3; done
herdr pane send-keys "$PANE" enter >/dev/null

# The graded log records what the dialog actually returned (student_picked).
# After answering, check it against the option you meant to choose — that is
# the only way to tell a tutor error from a harness misfire.
wait_idle "$AGENT" "${TURN_TIMEOUT:-240}"
read_screen "$AGENT" "${3:-50}"

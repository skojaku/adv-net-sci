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
# Walk to the top first. Enter-only used to be treated as "index 0", but the
# ask_user_question widget does not always start on its first option: a run
# that sent a bare Enter on a highlighted "1. I don't code" came back with
# "Comfortable with Python", which then looked like the tutor had recorded
# the opposite of the student's answer. Reset, then step down N times.
for _ in $(seq 1 12); do herdr pane send-keys "$PANE" up >/dev/null; done
for _ in $(seq 1 "$N"); do herdr pane send-keys "$PANE" down >/dev/null; done
herdr pane send-keys "$PANE" enter >/dev/null
wait_idle "$AGENT" "${TURN_TIMEOUT:-240}"
read_screen "$AGENT" "${3:-50}"

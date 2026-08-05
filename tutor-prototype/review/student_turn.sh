#!/usr/bin/env bash
# Send one student message to the tutor, wait for its reply, print the screen.
#
# Usage: student_turn.sh <state_file> "<message>" [screen_lines]
set -euo pipefail
. "$(dirname "$0")/lib.sh"
. "${1:?usage: student_turn.sh <state_file> \"<message>\" [screen_lines]}"
MSG="${2:?message required}"

herdr agent send "$AGENT" "$MSG" >/dev/null
sleep 1
herdr pane send-keys "$(pane_id "$AGENT")" enter >/dev/null
wait_idle "$AGENT" "${TURN_TIMEOUT:-240}"
read_screen "$AGENT" "${3:-50}"

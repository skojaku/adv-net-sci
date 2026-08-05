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
for _ in $(seq 1 "$N"); do herdr pane send-keys "$PANE" down >/dev/null; done
herdr pane send-keys "$PANE" enter >/dev/null
wait_idle "$AGENT" "${TURN_TIMEOUT:-240}"
read_screen "$AGENT" "${3:-50}"

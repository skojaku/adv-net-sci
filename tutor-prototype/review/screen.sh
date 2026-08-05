#!/usr/bin/env bash
# Print the tutor pane's screen without sending anything.
#
# Usage: screen.sh <state_file> [screen_lines]
set -euo pipefail
. "$(dirname "$0")/lib.sh"
. "${1:?usage: screen.sh <state_file> [screen_lines]}"
read_screen "$AGENT" "${2:-50}"

#!/usr/bin/env bash
# End a tutor E2E session: close the tutor pane and stop the marimo server.
# The sandbox (notebook, session_artifacts) is kept for Part S/P inspection.
#
# Usage: e2e_teardown.sh <state_file>
set -euo pipefail
. "$(dirname "$0")/lib.sh"
. "${1:?usage: e2e_teardown.sh <state_file>}"

herdr pane close "$(pane_id "$AGENT")" >/dev/null 2>&1 || true
kill "$(cat "$SANDBOX/session_artifacts/marimo.pid" 2>/dev/null)" 2>/dev/null || true
# The keepalive subshell that holds marimo's parent open (see e2e_setup.sh).
kill "$(cat "$SANDBOX/session_artifacts/marimo_keepalive.pid" 2>/dev/null)" 2>/dev/null || true
echo "artifacts kept in: $SANDBOX"

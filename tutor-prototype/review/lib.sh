# Shared helpers for the tutor E2E harness. Source, don't execute.
# Requires: herdr, python3.

pane_id() { # pane_id <agent>
  herdr agent get "$1" | python3 -c \
    'import json,sys; print(json.load(sys.stdin)["result"]["agent"]["pane_id"])'
}

agent_status() { # agent_status <agent>
  herdr agent get "$1" 2>/dev/null | python3 -c \
    'import json,sys; print(json.load(sys.stdin)["result"]["agent"]["agent_status"])' \
    2>/dev/null || echo unknown
}

wait_idle() { # wait_idle <agent> [timeout_seconds]
  local agent="$1" timeout="${2:-240}" waited=0
  # Give the agent a moment to leave idle (it may still be ingesting input).
  sleep 5
  while [ "$waited" -lt "$timeout" ]; do
    [ "$(agent_status "$agent")" = idle ] && return 0
    sleep 3; waited=$((waited + 8))
  done
  echo "warning: agent '$agent' not idle after ${timeout}s — reading anyway" >&2
}

read_screen() { # read_screen <agent> [lines]
  herdr agent read "$1" --source recent --lines "${2:-50}" | python3 -c \
    'import json,sys; print(json.load(sys.stdin)["result"]["read"]["text"])'
}

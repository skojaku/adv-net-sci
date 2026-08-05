#!/usr/bin/env bash
# Start a live tutor E2E session in an isolated sandbox.
#
# Usage: e2e_setup.sh <module_dir> [agent_name]
# Prints the path of a state file to pass to the other harness scripts.
#
# What it does: copies the module to a sandbox (fresh notebook from the
# template), starts the marimo server headless, connects a browser page
# (the kernel wakes only when a client connects — without this the tutor's
# first nb_* call fails), then starts the tutor agent in a herdr pane with
# global agent extensions disabled for fidelity.
set -euo pipefail

MODULE_DIR=$(cd "${1:?usage: e2e_setup.sh <module_dir> [agent_name]}" && pwd)
AGENT="${2:-tutor-e2e-$$}"
TUTOR_MODEL="${TUTOR_MODEL:-deepseek/deepseek-v4-flash-0731}"

for cmd in herdr uv rsync python3 pi; do
  command -v "$cmd" >/dev/null || { echo "error: $cmd is required" >&2; exit 1; }
done

SANDBOX=$(mktemp -d "${TMPDIR:-/tmp}/tutor-e2e-XXXXXX")
rsync -a --exclude session_artifacts --exclude __marimo__ --exclude .skill-cache \
  --exclude notebook.py --exclude '.pi/extensions/__pycache__' \
  "$MODULE_DIR/" "$SANDBOX/"
cp "$SANDBOX/notebook.template.py" "$SANDBOX/notebook.py"
mkdir -p "$SANDBOX/session_artifacts"

# Fully detach marimo's stdio: an inherited stdout would keep a caller's
# $(...) command substitution open forever.
(cd "$SANDBOX" && exec uvx marimo edit --sandbox --no-token --headless notebook.py) \
  >"$SANDBOX/session_artifacts/marimo_server.log" 2>&1 </dev/null &
echo $! >"$SANDBOX/session_artifacts/marimo.pid"

MARIMO_URL=""
for _ in $(seq 1 60); do
  # -a: uv progress bars put control chars in the log; without it grep says
  # "Binary file matches" instead of printing the URL.
  MARIMO_URL=$(grep -aoE 'http://[a-zA-Z0-9.]+:[0-9]+' \
    "$SANDBOX/session_artifacts/marimo_server.log" 2>/dev/null | head -1 || true)
  [ -n "$MARIMO_URL" ] && break
  sleep 1
done
[ -n "$MARIMO_URL" ] || {
  echo "error: marimo did not start — see $SANDBOX/session_artifacts/marimo_server.log" >&2
  exit 1
}

# Wake the kernel before the tutor's first nb_* call.
if command -v open >/dev/null; then
  open "$MARIMO_URL/?view-as=present"
  sleep 5
else
  echo "warning: no 'open' — connect a browser to $MARIMO_URL/?view-as=present yourself" >&2
fi

KICKOFF="Please start the tutoring session. Your CHAPTER SCRIPT message contains the current curriculum — begin at its first checkpoint, unless a RESUME CONTEXT message is present (then greet the student back and follow it). Keep replies short and conversational (1-3 spoken sentences, one question at a time), and use the nb_* notebook tools for all notebook work — the student is watching this terminal."

herdr agent start "$AGENT" --cwd "$SANDBOX" --no-focus \
  --env MARIMO_URL="$MARIMO_URL" \
  --env TUTOR_VISION_MODEL="${TUTOR_VISION_MODEL:-openrouter/google/gemini-3.6-flash}" \
  -- pi --model "$TUTOR_MODEL" --thinking low --exclude-tools bash -a \
     --no-extensions -e "$SANDBOX/.pi/extensions/notebook-tool.ts" "$KICKOFF" >/dev/null

STATE="$SANDBOX/review-state.env"
{
  echo "SANDBOX=$SANDBOX"
  echo "AGENT=$AGENT"
  echo "MARIMO_URL=$MARIMO_URL"
} >"$STATE"
echo "$STATE"

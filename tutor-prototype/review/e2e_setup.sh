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
  --exclude '.pi/skills' --exclude '.claude/skills' \
  "$MODULE_DIR/" "$SANDBOX/"
cp "$SANDBOX/notebook.template.py" "$SANDBOX/notebook.py"
mkdir -p "$SANDBOX/session_artifacts"

# The extension reaches the kernel through execute-code.sh, which ships inside
# the marimo-pair skill. The SKILL is excluded above on purpose (a pi tutor
# that can see it prints "[skill] marimo-pair" into the student's terminal),
# so stage the scripts on their own. Fail loudly: without this every nb_* call
# returns "bridge missing" and the whole run is a silent write-off.
if [ ! -f "$SANDBOX/.pi/marimo-bridge/scripts/execute-code.sh" ]; then
  for src in "$MODULE_DIR/.pi/marimo-bridge/scripts" \
             "$MODULE_DIR/.pi/skills/marimo-pair/scripts" \
             "$MODULE_DIR/.claude/skills/marimo-pair/scripts"; do
    [ -d "$src" ] || continue
    mkdir -p "$SANDBOX/.pi/marimo-bridge"
    cp -R "$src" "$SANDBOX/.pi/marimo-bridge/scripts"
    break
  done
fi
[ -f "$SANDBOX/.pi/marimo-bridge/scripts/execute-code.sh" ] || {
  echo "error: no execute-code.sh anywhere in $MODULE_DIR — run ./run_tutor.sh there once first" >&2
  exit 1
}

# A previous session's photos would satisfy the photo guard before the student
# has taken one, and the harness exists to test that guard.
rm -rf "$SANDBOX/assets/uploads" "$SANDBOX/assets/exercises"

# Fully detach marimo's stdio: an inherited stdout would keep a caller's
# $(...) command substitution open forever.
#
# And keep a live parent. `marimo edit` polls its parent process and shuts
# itself down when that parent disappears — this script exits within seconds
# of starting it, so the server killed itself about ten minutes into a gate
# run, mid-checkpoint. The trailing `sleep` holds the subshell open for the
# session's lifetime so marimo keeps a parent to see.
(
  cd "$SANDBOX" || exit 1
  uvx marimo edit --sandbox --no-token --headless notebook.py &
  echo $! >"$SANDBOX/session_artifacts/marimo.pid"
  sleep 86400
) >"$SANDBOX/session_artifacts/marimo_server.log" 2>&1 </dev/null &
echo $! >"$SANDBOX/session_artifacts/marimo_keepalive.pid"

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

# --no-extensions keeps the MACHINE's global extensions out, but it also
# stops pi discovering the packages the module declares in .pi/settings.json
# — and one of those is ask_user_question, the dialog the scripts require for
# their predictions. Production (run_tutor.sh) loads them, so a run without
# them tests the wrong tutor: it falls back to plain text and P8 can never be
# assessed. Explicit -e still works under --no-extensions, so load each
# declared package by path.
EXTS=(-e "$SANDBOX/.pi/extensions/notebook-tool.ts")
while IFS= read -r pkg; do
  [ -n "$pkg" ] || continue
  entry="$SANDBOX/.pi/npm/node_modules/${pkg#npm:}/index.ts"
  [ -f "$entry" ] || entry="$SANDBOX/.pi/npm/node_modules/${pkg#npm:}/index.js"
  if [ -f "$entry" ]; then
    EXTS+=(-e "$entry")
  else
    echo "warning: declared package '$pkg' is not installed in the sandbox — " \
         "run 'pi update --extensions' in the module first, or dialogs will be missing" >&2
  fi
done < <(python3 -c "
import json, sys
try:
    print('\n'.join(json.load(open(sys.argv[1])).get('packages', [])))
except Exception:
    pass
" "$SANDBOX/.pi/settings.json" 2>/dev/null)

KICKOFF="Please start the tutoring session. Your CHAPTER SCRIPT message contains the current curriculum — begin at its first checkpoint, unless a RESUME CONTEXT message is present (then greet the student back and follow it). Keep replies short and conversational (1-3 spoken sentences, one question at a time), and use the nb_* notebook tools for all notebook work — the student is watching this terminal."

herdr agent start "$AGENT" --cwd "$SANDBOX" --no-focus \
  --env MARIMO_URL="$MARIMO_URL" \
  --env TUTOR_VISION_MODEL="${TUTOR_VISION_MODEL:-openrouter/google/gemini-3.6-flash}" \
  -- pi --model "$TUTOR_MODEL" --thinking low --exclude-tools bash -a \
     --no-extensions "${EXTS[@]}" "$KICKOFF" >/dev/null

STATE="$SANDBOX/review-state.env"
{
  echo "SANDBOX=$SANDBOX"
  echo "AGENT=$AGENT"
  echo "MARIMO_URL=$MARIMO_URL"
} >"$STATE"
echo "$STATE"

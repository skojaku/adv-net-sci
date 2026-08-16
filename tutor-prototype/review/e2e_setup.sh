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
TUTOR_MODEL="${TUTOR_MODEL:-ollama/glm-5.2:cloud}"

for cmd in herdr uv rsync python3 pi; do
  command -v "$cmd" >/dev/null || { echo "error: $cmd is required" >&2; exit 1; }
done

SANDBOX=$(mktemp -d "${TMPDIR:-/tmp}/tutor-e2e-XXXXXX")
rsync -a --exclude session_artifacts --exclude __marimo__ --exclude .skill-cache \
  --exclude notebook.py --exclude '.pi/git' \
  --exclude '.pi/skills' --exclude '.claude/skills' \
  "$MODULE_DIR/" "$SANDBOX/"
cp "$SANDBOX/notebook.template.py" "$SANDBOX/notebook.py"
mkdir -p "$SANDBOX/session_artifacts"

# The nb_* toolkit is the pi-pair-notebook package, not part of the module. Test the
# WORKING TREE by default — the whole point of the harness is to exercise the
# fix you just made — and fall back to the copy pi installed in the module.
# Fail loudly: with the wrong toolkit (or none) every nb_* call fails and the
# whole run is a silent write-off. Its bridge/ carries execute-code.sh, so
# nothing needs staging any more.
PAIR_NOTEBOOK_EXTENSION="${PAIR_NOTEBOOK_EXTENSION:-}"
if [ -z "$PAIR_NOTEBOOK_EXTENSION" ]; then
  for cand in "$(cd "$(dirname "$0")/../pi-pair-notebook" 2>/dev/null && pwd)/extensions/notebook-tool.ts" \
              "$MODULE_DIR/.pi/git/github.com/sk-classroom/pi-pair-notebook/extensions/notebook-tool.ts"; do
    [ -f "$cand" ] && { PAIR_NOTEBOOK_EXTENSION="$cand"; break; }
  done
fi
[ -f "$PAIR_NOTEBOOK_EXTENSION" ] || {
  echo "error: no pi-pair-notebook toolkit found — set PAIR_NOTEBOOK_EXTENSION=/path/to/extensions/notebook-tool.ts" >&2
  exit 1
}
[ -f "$(dirname "$PAIR_NOTEBOOK_EXTENSION")/../bridge/scripts/execute-code.sh" ] || {
  echo "error: $PAIR_NOTEBOOK_EXTENSION has no bridge/scripts/execute-code.sh beside it — incomplete checkout?" >&2
  exit 1
}

# A previous session's photos would satisfy the photo guard before the student
# has taken one, and the harness exists to test that guard.
rm -rf "$SANDBOX/assets/uploads" "$SANDBOX/assets/exercises"

# Start marimo fully detached, with PID 1 as its parent.
#
# `marimo edit` runs a parent poller and kills itself the moment its parent
# process goes away — and this script exits seconds after launching it, so a
# plain background job died about ten minutes into a gate run, mid-checkpoint.
# A keepalive subshell was tried and did not help: the poller watches the
# DIRECT parent, and uv's own process chain sits in between.
#
# marimo skips the poller entirely when its parent is already init
# (start_parent_poller returns early for parent_pid == 1), so double-fork and
# wait for the reparenting to land BEFORE exec — no race, no poller, no
# ten-minute death.
python3 - "$SANDBOX" <<'DETACH'
import os, sys, time

sandbox = sys.argv[1]
log = os.path.join(sandbox, "session_artifacts", "marimo_server.log")

if os.fork() == 0:
    os.setsid()
    if os.fork() == 0:
        while os.getppid() != 1:
            time.sleep(0.01)
        # Lead our own process group, so teardown's `kill -- -<pid>` reaches
        # the whole uv chain instead of a group that does not exist.
        os.setpgid(0, 0)
        os.chdir(sandbox)
        fd = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
        os.dup2(fd, 1)
        os.dup2(fd, 2)
        os.dup2(os.open(os.devnull, os.O_RDONLY), 0)
        with open(os.path.join(sandbox, "session_artifacts", "marimo.pid"), "w") as f:
            f.write(str(os.getpid()))
        os.execvp(
            "uvx",
            ["uvx", "marimo", "edit", "--sandbox", "--no-token", "--headless", "notebook.py"],
        )
    os._exit(0)
os.wait()
DETACH

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
EXTS=(-e "$PAIR_NOTEBOOK_EXTENSION")
while IFS= read -r pkg; do
  # git: entries are the toolkit itself, loaded above from the working tree.
  case "$pkg" in ""|git:*|https://*|ssh://*|/*|./*) continue ;; esac
  # npm:@scope/name@1.2.3 -> @scope/name (the directory npm installs it into).
  name="${pkg#npm:}"
  [ "${name#@}" = "$(printf '%s' "${name#@}" | sed 's/@.*//')" ] || name="${name%@*}"
  entry="$SANDBOX/.pi/npm/node_modules/$name/index.ts"
  [ -f "$entry" ] || entry="$SANDBOX/.pi/npm/node_modules/$name/index.js"
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

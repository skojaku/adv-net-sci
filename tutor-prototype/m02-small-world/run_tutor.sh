#!/usr/bin/env bash
# One-command launcher for the m02 AI-guided tutoring session.
#
# What it does:
#   1. Installs the marimo-pair skill for your agent (first run only)
#   2. Starts the marimo notebook server (opens in your browser)
#   3. Starts the tutor agent (pi if installed, otherwise Claude Code)
#
# Requirements: uv, git, and either pi or claude on PATH.
# Your API key must already be configured for your agent
# (see README.md, "Setting up your API key").

set -euo pipefail
cd "$(dirname "$0")"

MARIMO_PAIR_REPO="https://github.com/marimo-team/marimo-pair"

# Course model: open-weights DeepSeek v4 Flash (override with TUTOR_MODEL).
TUTOR_MODEL="${TUTOR_MODEL:-deepseek/deepseek-v4-flash}"

say() { printf '\n\033[1;36m[tutor]\033[0m %s\n' "$*"; }
die() { printf '\n\033[1;31m[tutor]\033[0m %s\n' "$*" >&2; exit 1; }

command -v uv >/dev/null 2>&1 || die "uv is not installed. Install it first: https://docs.astral.sh/uv/  (macOS: brew install uv)"
command -v git >/dev/null 2>&1 || die "git is not installed."

# Pick the agent: pi preferred, claude as fallback.
AGENT=""
if command -v pi >/dev/null 2>&1; then AGENT="pi";
elif command -v claude >/dev/null 2>&1; then AGENT="claude";
else die "Neither 'pi' nor 'claude' found. Install one first (see README.md)."; fi

# 1. Install the marimo-pair skill into the agent's project-level skills dir.
#    (The skill lives at skills/marimo-pair/ inside the repo, so clone to a
#    cache and copy just that folder — agents only look one level deep.)
install_skill() {
  local dest="$1"
  if [ ! -d "$dest" ]; then
    say "Installing marimo-pair skill -> $dest"
    local cache=".skill-cache"
    rm -rf "$cache"
    git clone --depth 1 "$MARIMO_PAIR_REPO" "$cache"
    mkdir -p "$(dirname "$dest")"
    cp -R "$cache/skills/marimo-pair" "$dest"
    rm -rf "$cache"
  fi
}
if [ "$AGENT" = "pi" ]; then
  install_skill ".pi/skills/marimo-pair"
else
  install_skill ".claude/skills/marimo-pair"
fi

mkdir -p session_artifacts

# 2. Fresh notebook per session: archive the previous one and start from the
#    pristine template (visually blank). TUTOR_RESUME=1 keeps the previous
#    notebook to continue where you left off.
if [ "${TUTOR_RESUME:-0}" = "1" ] && [ -f notebook.py ]; then
  say "Resuming your previous notebook (TUTOR_RESUME=1)."
else
  STAMP=$(date +%Y%m%d-%H%M%S)
  if [ -f notebook.py ] && ! cmp -s notebook.py notebook.template.py; then
    mv notebook.py "session_artifacts/notebook-$STAMP.py"
    say "Previous notebook archived to session_artifacts/notebook-$STAMP.py"
  fi
  cp -f notebook.template.py notebook.py
  if [ -f session_artifacts/session_log.jsonl ]; then
    mv session_artifacts/session_log.jsonl "session_artifacts/session_log-$STAMP.jsonl"
  fi
fi

# 3. Start the marimo server (background). --no-token lets the skill discover it.
say "Starting the notebook server (your browser will open)..."
uvx marimo edit --sandbox --no-token notebook.py >session_artifacts/marimo_server.log 2>&1 &
MARIMO_PID=$!
cleanup() { kill "$MARIMO_PID" 2>/dev/null || true; }
trap cleanup EXIT

# Wait for the server URL (marimo may pick a different port if 2718 is busy),
# then export it for the notebook tool (.pi/extensions/notebook-tool.ts).
MARIMO_URL=""
for _ in $(seq 1 30); do
  kill -0 "$MARIMO_PID" 2>/dev/null || die "marimo failed to start — see session_artifacts/marimo_server.log"
  MARIMO_URL=$(grep -oE 'http://[a-zA-Z0-9.]+:[0-9]+' session_artifacts/marimo_server.log | head -1 || true)
  [ -n "$MARIMO_URL" ] && break
  sleep 1
done
[ -n "$MARIMO_URL" ] || die "marimo did not report a URL — see session_artifacts/marimo_server.log"
export MARIMO_URL

# 4. Start the tutor.
say "Notebook is up. Starting your tutor ($AGENT, model: $TUTOR_MODEL) — say hello!"
KICKOFF="Please start the tutoring session: read lesson.yaml and begin at checkpoint cp0_welcome, as specified in AGENTS.md. Speak to the student ONLY through the say tool, use the nb_* notebook tools for all notebook work, and keep this terminal clean — the student is watching it."
if [ "$AGENT" = "pi" ]; then
  # bash is disabled on purpose: every notebook/log operation goes through the
  # quiet `notebook` tool, so no raw commands ever scroll past the student.
  pi --model "$TUTOR_MODEL" --exclude-tools bash "$KICKOFF"
else
  # Claude Code fallback uses its own default model (TUTOR_MODEL is pi-only)
  # and the marimo-pair skill directly (no custom notebook tool).
  claude "$KICKOFF"
fi

say "Session ended. Your work is saved in notebook.py and session_artifacts/."

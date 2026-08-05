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
TUTOR_MODEL="${TUTOR_MODEL:-deepseek/deepseek-v4-flash-0731}"

# The tutor model is TEXT-ONLY — photo uploads (chapter 3) are described to it
# by a separate vision-capable model. Default: Gemini 3.6 Flash via OpenRouter
# (needs OPENROUTER_API_KEY; MiniMax-M3 misread hand-drawn chord endpoints).
# Without credentials the session still works: the tutor asks the student to
# describe the drawing in words instead.
export TUTOR_VISION_MODEL="${TUTOR_VISION_MODEL:-openrouter/google/gemini-3.6-flash}"

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

# 2. Make sure a notebook exists (first run). Continue-or-fresh is decided IN
#    the session: when a previous session log exists, the tutor asks the
#    student and calls nb_fresh_start if they want a clean slate.
[ -f notebook.py ] || cp notebook.template.py notebook.py
# Working copies predating the current template lack netviz/igraph/exercises.
if ! grep -q '"igraph"' notebook.py; then
  say "NOTE: your notebook.py predates the current template (no igraph/netviz)."
  say "      To upgrade (archives the old one):"
  say "      mv notebook.py \"session_artifacts/notebook-old-\$(date +%Y%m%d%H%M).py\" && ./run_tutor.sh"
fi

# 3. Start the marimo server (background). --no-token lets the skill discover
#    it; --headless because we open the browser ourselves in app view below.
say "Starting the notebook server (your browser will open)..."
uvx marimo edit --sandbox --no-token --headless notebook.py >session_artifacts/marimo_server.log 2>&1 &
MARIMO_PID=$!
cleanup() { kill "$MARIMO_PID" 2>/dev/null || true; }
trap cleanup EXIT

# Wait for the server URL (marimo may pick a different port if 2718 is busy),
# then export it for the notebook tool (.pi/extensions/notebook-tool.ts).
MARIMO_URL=""
for _ in $(seq 1 30); do
  kill -0 "$MARIMO_PID" 2>/dev/null || die "marimo failed to start — see session_artifacts/marimo_server.log"
  # -a: uv's progress bars put control chars in the log, and without it grep
  # emits "Binary file ... matches" instead of the URL (broke every nb_* call).
  MARIMO_URL=$(grep -aoE 'http://[a-zA-Z0-9.]+:[0-9]+' session_artifacts/marimo_server.log | head -1 || true)
  case "$MARIMO_URL" in http://*) break ;; *) MARIMO_URL="" ;; esac
  sleep 1
done
[ -n "$MARIMO_URL" ] || die "marimo did not report a URL — see session_artifacts/marimo_server.log"
export MARIMO_URL

# Open the student's view in APP (present) mode: the same live edit session,
# shown as a clean document — your personal notebook, not a code editor.
# (Cmd+. / Ctrl+. toggles the editor when a fill-in cell needs typing.)
STUDENT_URL="$MARIMO_URL/?view-as=present"
if command -v open >/dev/null 2>&1; then open "$STUDENT_URL"
elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$STUDENT_URL"
else say "Open this in your browser: $STUDENT_URL"
fi

# 4. Start the tutor.
say "Notebook is up. Starting your tutor ($AGENT, model: $TUTOR_MODEL) — say hello!"
KICKOFF="Please start the tutoring session. Your CHAPTER SCRIPT message contains the current curriculum — begin at its first checkpoint, unless a RESUME CONTEXT message is present (then greet the student back and follow it). Keep replies short and conversational (1-3 spoken sentences, one question at a time), and use the nb_* notebook tools for all notebook work — the student is watching this terminal."
if [ "$AGENT" = "pi" ]; then
  # bash is disabled on purpose: every notebook/log operation goes through the
  # quiet `notebook` tool, so no raw commands ever scroll past the student.
  # thinking "low" gives the model a hidden place to reason (hideThinkingBlock
  # keeps it invisible); starving it of thinking made it reason in plain text.
  pi --model "$TUTOR_MODEL" --thinking low --exclude-tools bash "$KICKOFF"
else
  # Claude Code fallback uses its own default model (TUTOR_MODEL is pi-only)
  # and the marimo-pair skill directly (no custom notebook tool).
  claude "$KICKOFF"
fi

say "Session ended. Your work is saved in notebook.py and session_artifacts/."

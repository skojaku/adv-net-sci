# AI-Guided Notebook — Module 02: The Small-World Puzzle

A prototype of a new assignment format: instead of submitting code, you work
through a **guided, one-on-one tutoring session**. An AI tutor builds a
[marimo](https://marimo.io) notebook with you, cell by cell — asking you to
predict, explain, calculate, and even draw on paper — and keeps a log of the
conversation. **What gets reviewed is your thinking, not your code.**

No programming experience is required.

---

## For students

### One-time setup (10 minutes)

1. **Install uv** (runs the notebook):
   - macOS: `brew install uv`
   - otherwise: https://docs.astral.sh/uv/getting-started/installation/
2. **Install the tutor agent** — either one works:
   - pi: `npm install -g @mariozechner/pi-coding-agent`
   - Claude Code: `npm install -g @anthropic-ai/claude-code`
3. **Set up your API key** (provided by the course — check the syllabus page).
   The tutor runs on the open-weights **DeepSeek v4 Flash** model through the
   course's API. Set the environment variables from the course instructions, e.g.:
   ```bash
   export DEEPSEEK_API_KEY="<your course key>"
   ```
   Put this line in your `~/.zshrc` so you only do this once.
   (Advanced: `TUTOR_MODEL` overrides the model, e.g.
   `TUTOR_MODEL="provider/model" ./run_tutor.sh`.)

### Every session

```bash
./run_tutor.sh
```

Two windows appear:

| Window | What it is |
|---|---|
| **Browser** (notebook) | Your shared whiteboard. Questions and experiments appear here. |
| **Terminal** (tutor) | Where you and your tutor talk. |

Say hello in the terminal and follow along. You can answer questions in the
notebook **or** type them in the terminal — both always work. Have **pen and
paper** ready: one checkpoint asks you to draw (you photograph it with your
phone, or just describe it in words).

A session takes about 45–60 minutes. You can stop anytime and pick up later —
your progress is saved.

### What gets turned in

The session produces everything automatically — you don't "write up" anything:

- `notebook.py` — the notebook you built together
- `session_artifacts/session_log.jsonl` — your answers, verbatim
- `session_artifacts/session_summary.md` — a summary for the instructor

**Honesty note:** needing hints is *not* penalized. The log is reviewed for
how you reasoned, not for how few hints you used. Asking questions and taking
detours counts in your favor — it's the whole point.

---

## For the instructor / TA

### What's in this folder

| File | Role |
|---|---|
| `lesson.yaml` | The curriculum: 9 checkpoints + 1 optional stretch, each with build spec, question, accept criteria, and a 2-hint escalation ladder. **Edit this to change the lesson.** |
| `AGENTS.md` | The tutor's behavior contract (auto-loaded by pi; Claude Code loads it via `CLAUDE.md`). Pedagogy, logging schema, hard rules. Lesson-independent. |
| `notebook.py` | Starter notebook: title + instructions only. The tutor builds the rest live. |
| `run_tutor.sh` | Launcher: installs the marimo-pair skill, starts marimo (`--no-token`), starts the agent (pi runs with bash disabled). |
| `.pi/extensions/notebook-tool.ts` | Custom pi tool wrapping the skill's `execute-code.sh`. The student's terminal shows only a friendly one-line status ("📝 Setting up your first question…") instead of raw commands; full output stays available to the LLM and via the expand keybinding. |

### Design decisions

- **The lesson script lives agent-side, not in the notebook.** An earlier idea
  was to pre-write all cells commented-out — but then any text editor reveals
  the answers. Here the notebook starts blank and `lesson.yaml` is the source
  of truth. (For a graded deployment, serve `lesson.yaml` from the API proxy
  instead of shipping it in the repo.)
- **Interaction modalities on purpose:** prediction (cp1, cp6), calculation
  (cp2, cp3), pen-and-paper drawing with photo upload (cp4), concept
  articulation (cp3, cp5, cp8), exploration with a widget (cp6), and a
  red-team critique of a flawed AI analysis (cp7) — the last one previews the
  course's process-over-product grading philosophy.
- **Hints are logged, never penalized** — stated to the student up front, and
  binding on the grader. Otherwise students stop asking, and the log stops
  reflecting reality.
- **Grading artifact = verbatim log**, not the notebook. The tutor is required
  to record student answers word for word and never fake a pass.

### Adapting to another module

Copy the folder, rewrite `lesson.yaml` (the checkpoint schema is documented in
its header comment), and update the title cell of `notebook.py`. `AGENTS.md`
and `run_tutor.sh` carry over unchanged.

### Known limitations (prototype)

- `lesson.yaml` ships in the folder, so a determined student can read the
  accept criteria. Fine for formative use; move it server-side for grading.
- Cost control / per-student budgets are assumed to live in the API proxy.
- The marimo server runs with `--no-token` on localhost (required for skill
  auto-discovery) — fine on a laptop, not on a shared host.

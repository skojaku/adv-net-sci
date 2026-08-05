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
| **Terminal** (tutor) | Where you and your tutor talk — questions and answers happen here. |
| **Browser** (notebook) | The whiteboard: pictures, interactive experiments, and photo uploads appear here when needed. A drop box or a code box has a **📨 Send to my tutor** button under it — press it and your tutor sees your work. Anything else you explore, just tell your tutor about in the terminal. |

Say hello in the terminal and follow along. Have **pen and paper** ready:
three steps happen off-screen — a distance table, a drawing, and a
derivation — and you photograph each with your phone and drop it into the
notebook.

A session takes about 60–90 minutes. You can stop anytime and pick up later —
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
| `lesson/` | The curriculum, split into 5 chapters (`index.json` + `chN-*.yaml`): 12 checkpoints + 1 optional stretch, each with build spec, question, accept criteria, and starter hints. **The tutor holds only the current chapter in context** — the extension (the deterministic "lead agent") injects one CHAPTER SCRIPT at a time, and at each `chapter_done` builds a handoff brief (progress + verbatim quotes + the tutor's own notes), loads the next script, and trims the old conversation via pi compaction with the brief as the summary. Same session, same visible transcript, fresh LLM context per chapter (`.pi/settings.json` keeps only ~3k recent tokens on compaction). **Edit these files to change the lesson.** |
| `AGENTS.md` | The tutor's behavior contract (auto-loaded by pi; Claude Code loads it via `CLAUDE.md`). Pedagogy, logging schema, hard rules. Lesson-independent. |
| `notebook.template.py` | Pristine starter: visually blank (only hidden import/helper cells). `notebook.py` is the working copy (gitignored), created from the template on first run. |
| `reset_session.sh` | Continue-or-fresh, decided **before anything loads**. `run_tutor.sh` asks at startup when a session exists; answering `f` runs this. It archives the notebook, the log, the summary and any uploads into `session_artifacts/` with a timestamp and drops in a clean notebook — nothing is ever deleted. Run it directly, or `./run_tutor.sh --fresh`, to skip the prompt. A file-level reset cannot half-succeed, which the in-session one can: `nb_fresh_start` deletes cells one at a time through a live kernel, and one failure there left a "clean slate" session opening on chapter 3. `nb_fresh_start` remains for a student who changes their mind mid-lesson. |
| `run_tutor.sh` | Launcher: asks continue-or-fresh, stages the notebook bridge (`.pi/marimo-bridge/scripts`, or the marimo-pair skill itself on the Claude fallback), starts marimo (`--no-token`), starts the agent (pi runs with bash disabled). `--fresh` resets without asking. |
| `.pi/extensions/notebook-tool.ts` | The single pi extension. The `nb_*` toolkit (`nb_add_template`, `nb_add_cell`, `nb_add_exercise`, `nb_edit_cell`, `nb_delete_cell`, `nb_read`, `nb_view_image`, `nb_run`, `nb_fresh_start`) generates all marimo code-mode plumbing — the model sends only cell bodies, cold kernels recover themselves, and each call renders as one friendly status line. It also owns the ceremony: `checkpoint_done` writes the log, renders the note cell from the chapter script's `note:` skeleton, and asks the student what's next; `log_detour` records off-script questions; `chapter_done` gates chapter transitions on the student's own answer and, at the end, derives `session_record` and `session_summary.md` from the log. Plus the resume brief, chapter headers, scroll-to-new-cell, and a silent runaway guard. Speaking style is steered by AGENTS.md prompt guidance only — no gating, no added latency. |
| `.pi/extensions/nb_review.py` | Deterministic review of improvised cells (Python AST, run in the kernel before insertion): marimo renders only a cell's last expression, so displays that would vanish get wrapped in one `mo.vstack`, unrescuable cells are refused with an instruction, and ASCII-art diagrams are flagged. |

### Design decisions

- **The lesson script lives agent-side, not in the notebook.** An earlier idea
  was to pre-write all cells commented-out — but then any text editor reveals
  the answers. Here the notebook starts blank and `lesson.yaml` is the source
  of truth. (For a graded deployment, serve `lesson.yaml` from the API proxy
  instead of shipping it in the repo.)
- **Channel discipline:** words live in the terminal (stories, questions,
  typed answers); the notebook is reserved for what the terminal can't do —
  figures, *interactive/animated* widgets (preferred over static images),
  photo uploads. A drop box or a code box carries a 📨 Send button whose press
  starts the tutor's turn; a slider or a radio has none — the student says so
  in the terminal and the tutor reads the values (an earlier Done button on
  every cell competed with the terminal for keyboard focus).
- **Interaction modalities on purpose:** prediction (cp1, cp6), calculation
  (cp2, cp3), three off-screen pen-and-paper steps with photo upload
  (cp2_paperwork, cp4, cp5_ring_formula), a real coded experiment at large N
  (cp6_large_n_experiment), concept articulation (cp3, cp5_tension, cp8),
  exploration with a widget (cp2, cp5, cp6), and a red-team critique of a
  flawed AI analysis (cp7) — the last one previews the course's
  process-over-product grading philosophy.
- **Templates are self-describing (notebook design principle).** Every
  template in `cells/` carries a `# describe:` line — one factual sentence
  about what the student sees. `nb_add_template` returns it on insert, and
  the tutor is told to describe the artifact *only* from that line (a tutor
  once called the 4-person network "5-person"). When authoring a new
  template, write the describe line first; keep titles/captions in the
  figures self-explanatory so the notebook stays truthful without the tutor.
- **Hints are logged, never penalized** — stated to the student up front, and
  binding on the grader. Otherwise students stop asking, and the log stops
  reflecting reality.
- **Grading artifact = the notebook itself** (plus the verbatim
  `session_log.jsonl` as the machine copy). Note cells quote the student's
  answers word for word, and a closing `session_record` cell summarizes every
  checkpoint. The tutor is required to record answers verbatim and never fake
  a pass.

The full set of notebook design principles — structure, note-cell rhythm,
naming conventions, theming — is in **[DESIGN.md](DESIGN.md)**.

### Adapting to another module

Copy the folder, rewrite the chapter scripts in `lesson/` (the checkpoint
schema is documented in each file's header comment) and `lesson/index.json`,
swap the premade cells in `cells/`, and update `notebook.template.py`'s
dependencies if needed. `AGENTS.md`, `DESIGN.md`, and `run_tutor.sh` carry
over unchanged.

### Known limitations (prototype)

- `lesson.yaml` ships in the folder, so a determined student can read the
  accept criteria. Fine for formative use; move it server-side for grading.
- Cost control / per-student budgets are assumed to live in the API proxy.
- The marimo server runs with `--no-token` on localhost (required for skill
  auto-discovery) — fine on a laptop, not on a shared host.

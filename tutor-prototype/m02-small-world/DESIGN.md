# Notebook Design Principles

What the tutoring session produces, why it looks the way it does, and where
each rule is enforced. Read this before changing `AGENTS.md`, the templates,
or the chapter scripts — every rule below exists because a live session
failed without it.

## The core concept

**The student builds their own textbook through conversation.** The marimo
notebook starts visually blank and grows one artifact at a time — figures,
experiments, notes in the student's own words. At the end it is three things
at once:

1. a **keepsake** — an interactive document they can replay and re-learn from
   months later, with zero setup (`uvx marimo edit --sandbox notebook.py`);
2. the **submitted assignment** — it must contain everything a grader needs;
3. a **mirror of the dialogue** — the student's verbatim answers are the
   centerpiece, because *process* is what this course grades.

The terminal is where the conversation happens; the notebook is where it
leaves a trace. Words are ephemeral, cells are permanent.

## Anatomy of a finished notebook

```
🐛 bug-report line (email skojaku@binghamton.edu)          ← template
## Chapter 1 of 5 — The Six Degrees Hook                   ← auto header
   [Milgram photo]                                         ← build cell
   🌍 note: six degrees + "My guess: …"                    ← note cell
## Chapter 2 of 5 — Measuring Smallness
   [wave-from-A explorer widget]                           ← build cell
   📏 note: d(u,v), L = 7/6 ≈ 1.17 + "I worked out: …"     ← note cell
   …
## Chapter 5 of 5 — Mastery Check
   🎓 note: the whole story in the student's three sentences
   📋 session_record — question / verbatim answer / judgment / hints
```

The rhythm is **experiment cell → note cell**, alternating. Experiment cells
show; note cells explain between them. That alternation is what makes the
notebook re-learnable.

## Principles

1. **Terminal for words, notebook for everything visual.** Questions, hints,
   and reactions are speech (1–3 sentences); an answer that wants a fourth
   sentence is a cell. Anything worth remembering is rendered: a figure, a
   widget, an `mo.md` note. Never explain in a paragraph what a picture can
   carry. And the student's own questions shape the notebook: every detour
   leaves a souvenir cell — a 🧭 tip, a demo, a playable experiment — so a
   curious student's notebook ends up visibly their own. *(AGENTS.md)*

2. **The student's verbatim words are the centerpiece.** Every note cell
   quotes their answer word for word, and the closing `session_record`
   cell repeats question / verbatim answer / judgment / hints for every
   checkpoint. Paraphrasing is falsifying the graded artifact — so the
   extension also captures the student's own messages straight from the
   transcript (`student_said_verbatim`), making the record independent of
   the model's summary. *(checkpoint_done, lesson note skeletons)*

3. **Quality by structure, not by model effort.** The tutor model is small
   and fast; nothing important is left to its improvisation:
   - premade, live-tested **templates** (`cells/*.py`) for every scripted
     build — the model sends only a name;
   - instructor-authored **`note:` skeletons** in each chapter script, with
     «slots» for the student's words — the model personalizes, it does not
     author;
   - **chapter header cells** inserted deterministically by the extension;
   - templates are **self-describing** (`# describe:` line) — the tutor
     describes artifacts only from it, never from guesswork;
   - improvised cells pass a **deterministic review** before insertion
     (pi-studio's `extensions/nb_review.py`, run inside the kernel): marimo shows
     only a cell's last expression, so a cell ending in
     `netviz(...)` + `mo.md(...)` loses the picture — the review wraps
     those displays in one `mo.vstack`, refuses cells whose display can't
     be rescued safely, and flags ASCII-art diagrams. Static analysis, not
     an LLM reviewer: no latency, no tempo cost.

4. **Every symbol gets words.** $L$, $C_0$, $p$ — any notation shown in the
   notebook or terminal is defined in plain language in the same cell
   (KaTeX via `mo.md`, no extra packages). A returning reader must never
   meet an unexplained symbol. *(AGENTS.md, cp6 legend template)*

5. **App view: a document, not an editor.** The browser opens
   `?view-as=present` — the same live kernel, rendered as a clean page.
   Students never see or touch cell code; everything they interact with
   lives *in* the page. New cells scroll into view automatically
   (marimo `focus-cell`). *(run_tutor.sh, extension)*

6. **Coding happens in the page — and survives the page being closed.**
   Fill-in exercises are a `mo.ui.code_editor` box pre-filled with a
   scaffold (numbered steps, `...` blanks) plus a ▶ Run button; output — or
   a friendly one-line error — appears right below. Never a blank cell,
   never "open the editor". marimo does not serialise a code editor's
   value, so every run writes the code to `assets/exercises/<name>.py` and
   the output cell renders it back from there: reopen the notebook in a
   year and the student's own code and its chart are still the thing on
   screen, not the blanks they started from. Under it sits a **📨 Send my
   code to my tutor** button — the same hand-in gesture as a photo drop
   box, and the same watcher turns the press into the tutor's turn. The
   saved file is session data: `nb_fresh_start` and `reset_session.sh`
   archive it with the log, and inserting the box deletes any stale one, or
   the next student would meet someone else's solution captioned in their
   own voice. *(nb_add_exercise, run_student_code in the template)*

7. **Interactive over static, themed over default.** Prefer the drag-able
   D3 widget (`netviz`) and widget-driven figures over static plots; charts
   via Altair/seaborn. Everything uses the lecture-hall palette — paper
   `#FFFFFF`, ink `#1D1E21`/`#35373C`, blue `#1F3A5F`/`#35577F`, rust
   `#B4552D`, amber `#C98A2D`, muted `#6A6D75` — set globally in the
   template rcParams and hardcoded in templates. *(notebook.template.py)*

8. **Zero setup, forever.** Dependencies live in the notebook's PEP 723
   header; `--sandbox` makes uv build the venv automatically, today and
   when the student reopens the notebook in a year.

9. **Hints are logged, never penalized** — stated up front, binding on the
   grader. And the tutor never writes answers into the notebook: guided
   discovery ends with the student taking the last step.

10. **The student controls the pace, and the extension enforces it.**
    `checkpoint_done` — the one call that ends a checkpoint — asks them
    itself: ready / I have a question / give me another one like that.
    Only "ready" comes back as permission to advance. `chapter_done` does
    the same at a chapter boundary and **refuses to transition**
    otherwise. Extra rounds are improvised on fresh data, reusing the
    module's canonical objects, and logged as practice — never as failure.

11. **Ceremony belongs to the extension, judgment to the model.** The
    tutor supplies the verbatim answer and the judgment; the extension
    writes the log (validated, timestamped, with the student's own
    messages captured from the transcript), renders the note cell from
    the script's skeleton, asks what's next, and at the end derives
    `session_record` and `session_summary.md` from the log. The model
    never hand-writes the graded record — it can't drift or fabricate
    what it doesn't type. *(checkpoint_done, log_detour, chapter_done)*

## Cell naming conventions

| Name | Meaning |
|---|---|
| `_` (unnamed) | Template infrastructure — survives `nb_fresh_start` |
| `chN_header` | Auto-inserted chapter heading |
| `cpN_*` | Build cells for checkpoint N (template or improvised) |
| `<cp>_note` | Note cell after checkpoint (the re-learnable layer) |
| `<name>_ed` / `_out` / `_sent` | Exercise code box / its output + 📨 Send button / the send confirmation |
| `detour_<slug>` | Souvenir cell for a question the student asked off-script |
| `session_record` | Closing grading summary |

Named cells are wiped by `nb_fresh_start`; unnamed template cells persist.

## Where things live

| Concern | File |
|---|---|
| Tutor behavior (speech style, note-cell duty, never-reveal) | `AGENTS.md` |
| Curriculum + note skeletons + fresh variants | `lesson/ch*.yaml` |
| Premade visuals (self-describing) | `cells/*.py` |
| Theme, deps, `netviz`, `run_student_code`, bug-report line | `notebook.template.py` |
| Tools, chapter orchestration, headers, focus, logging | pi-studio: `extensions/notebook-tool.ts` |
| Improvised-cell review (AST) | pi-studio: `extensions/nb_review.py` |
| Launch: sandbox venv, app view, vision model | `run_tutor.sh` |

The two pi-studio rows are the shared toolkit, not this module:
[`sk-classroom/pi-studio`](https://github.com/sk-classroom/pi-studio), pinned by
tag in `.pi/settings.json` and installed by pi on first run.

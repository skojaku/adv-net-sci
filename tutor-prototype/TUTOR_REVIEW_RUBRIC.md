# Tutor Module Review Rubric

How to review a tutor-prototype module (e.g. `tutor-prototype/m02-small-world`):
the notebook artifact it produces, the curriculum scripts that drive it, the
session logs it leaves behind, and the live behavior of the tutor agent itself.
Plain markdown + shell only, so any agent (Claude, pi, human) can run the same
review. The review **reports findings; it never edits anything**.

## Inputs

A module directory contains:

| Artifact | Files | Reviewed in |
|---|---|---|
| Notebook (product) | `notebook.py`, `notebook.template.py`, session copies in `session_artifacts/notebook-*.py` | Part S |
| Curriculum | `lesson/ch*.yaml`, `lesson/index.json`, `cells/*.py`, `AGENTS.md` | Part C |
| Session process | `session_artifacts/session_log*.jsonl`, `session_artifacts/reviewer_log.jsonl`, `session_artifacts/session_summary.md` | Part P |
| Live behavior | the running tutor (pi + `.pi/extensions/notebook-tool.ts`) | Part D |

Module-level design contracts live in `DESIGN.md` and `AGENTS.md` — read both
before reviewing; every checklist item below traces to one of them.

## How to run a review

1. **Static pass (always):** run Parts S, C, P on the module directory.
   Render before judging figures (see Part S preamble).
2. **E2E gate (before any final PASS):** run Part D with the harness in
   `tutor-prototype/review/` — a live tutor session driven by scripted
   student personas. Also rerun Part D whenever a behavior-carrying file
   changed since the last clean E2E: `AGENTS.md`, `lesson/`, `cells/`,
   `notebook.template.py`, `.pi/extensions/`, `run_tutor.sh`.
3. Report findings in the format below. Do not fix anything.

### Findings format

One line-anchored finding per item, ordered by severity:

```
[Blocker|Major|Minor] <rubric-id> <file>:<line> — <what is wrong, one sentence>
  Evidence: <the observation that proves it>
  Fix target: <file that controls this behavior — see Fix targets>
```

- **Blocker** — corrupts the graded record, reveals answers to open
  checkpoints, or prevents a student from finishing.
- **Major** — violates a design contract in `DESIGN.md`/`AGENTS.md` or makes
  the notebook fail as a keepsake/assignment.
- **Minor** — polish; degrades quality without breaking a contract.

**PASS = zero Blockers and zero Majors in the static pass AND the E2E gate.**
Minors are listed but do not block.

### Fix targets (for the fixer, not the reviewer)

Findings indict the *system*, not a past session. Fixes go to the controlling
file: `AGENTS.md` (tutor behavior), `lesson/ch*.yaml` (curriculum),
`cells/*.py` (premade builds), `notebook.template.py` (theme/deps/helpers),
`.pi/extensions/notebook-tool.ts` (tools, ceremony, tips, dialogs),
`run_tutor.sh` (launch). **Never edit `session_artifacts/`** — logs and
session notebooks are evidence — and never edit a real student's answers.

### Iteration protocol (review–fix loop)

The intended use: a **reviewer subagent** runs this rubric and reports; the
**calling agent** fixes and re-reviews until PASS.

1. Caller spawns a fresh reviewer subagent: "Read
   `tutor-prototype/TUTOR_REVIEW_RUBRIC.md`, review `<module dir>`, static
   pass only (Parts S, C, P), report findings in the rubric format, fix
   nothing."
2. Blockers/Majors reported → caller fixes them at the fix targets, then
   respawns a *fresh* reviewer (no shared context, so it re-derives rather
   than confirms). Repeat.
3. Static pass clean → caller (or a subagent) runs the Part D E2E gate.
   Findings → fix → back to step 2.
4. PASS → report to the user: PASS, iterations used, remaining Minors.
5. Guards: max 5 iterations; if the same finding survives two fixes, or a fix
   requires a curriculum/content decision, stop and surface it to the user
   instead of iterating. Never weaken a rubric item to make a review pass.

**Runner portability.** The reviewer role needs only file reading and a
shell — any agent can run it (Claude Code, pi, Cursor, a human). What
matters is *isolation between reviewer and fixer*, not the mechanism:

- runner has subagents (Claude Code's agent tool, pi's `pi-subagents`) →
  spawn the reviewer as a fresh read-only subagent each round;
- no subagents (e.g. Cursor) → run the review in a fresh chat/session, paste
  the findings into the fixing session; or, last resort, alternate roles in
  one context — finish the entire findings report before fixing anything,
  and on each re-review re-derive findings from the artifacts, never from
  memory of the previous round.

Entry points: `.claude/skills/tutor-review/` (Claude Code),
`.pi/skills/tutor-review/` (pi — loads project skills from the cwd's `.pi/`
only, so start pi at the repo root; conveniently, this also keeps the skill
out of tutor sessions running inside a module dir), `.cursor/commands/
tutor-review.md` (Cursor). All three just point here — an agent with none
of these can simply be told to read this file and follow it.

---

## Part S — The notebook artifact

Review the most recent complete session notebook (`session_artifacts/
notebook-*.py`, newest) *and* `notebook.template.py`. **Render before judging
figures**: `cd <module> && uvx marimo export html notebook.py -o /tmp/nb-render.html`
executes every cell; confirm each build cell emitted a non-empty output node,
and open the HTML in a browser when one is available. Never judge a figure
from source alone.

- **S1 Every figure renders.** No cell whose display is silently dropped
  (marimo shows only the last expression — multi-display cells need
  `mo.vstack`). No error cells, no blank outputs.
- **S2 Figure quality.** Readable at a glance; lecture-hall palette (nodes
  `#35577F`, neutral `#E4E6EA`, highlights `#B4552D`/`#C98A2D`, edges
  `#6A6D75`, ink `#35373C`, paper `#FFFFFF`); no default-matplotlib look; no
  ASCII-art diagrams in markdown.
- **S3 Interactive over static.** Network drawings use `netviz` (drag-able);
  parameter explorations use widgets/sliders; a static plot only where
  interaction adds nothing.
- **S4 Markdown explains enough.** Each note cell lets a cold reader
  reconstruct what was learned — claim, the student's answer, the idea in
  plain words.
- **S5 …but not too much.** Note cells ≲150 words; no wall-of-text cells; no
  paragraph doing what a picture already does.
- **S6 Every symbol defined.** Any $L$, $C$, $p$, $\sigma$… shown anywhere
  gets a plain-words definition *in the same cell*.
- **S7 Alternation rhythm.** Experiment cell → note cell, chapter by chapter;
  no orphan build without a note, no note without its experiment
  (`DESIGN.md` anatomy).
- **S8 The story lands.** Hook → question → reveal arc per chapter; concrete
  memorable facts (Milgram's 160/64, Facebook's 4.74), not generalities.
- **S9 Student verbatim is the centerpiece.** Note-cell «slots» and
  `session_record` quote the student word-for-word — cross-check against
  `student_said_verbatim` in the session log. Paraphrase = Blocker.
- **S10 Cold-read test.** A reader with no session context can follow the
  whole notebook top to bottom; chapter headers present, ordered, none stale.
- **S11 Reproducible forever.** Fresh `uvx marimo edit --sandbox notebook.py`
  runs clean; PEP 723 deps complete; every referenced asset path exists in
  the module (uploads copied in, not stranded in `session_artifacts/`).
- **S12 Naming conventions.** Cells follow the `DESIGN.md` table (`cpN_*`,
  `<cp>_note`, `<name>_ed`/`_out`, `session_record`; template cells unnamed).
- **S13 The student takes the last step.** No answer to any checkpoint
  written by the tutor; guided discovery visible in the record.
- **S14 Detours left souvenirs.** Every logged detour has its 🧭 cell (text +
  something visual or playable); a curious student's notebook looks personal.
- **S15 Off-screen exercise exists.** At least one paper/physical exercise
  per module (draw, photograph, count by hand) — not everything is typing.
- **S16 Coding is scaffolded, not hard.** Exercise boxes: numbered `#` steps,
  ≤3 `...` blanks, one concept per blank, runnable as given once filled, and
  a friendly error path. A student who "doesn't code" can finish with hints.

## Part C — Curriculum scripts

Review `lesson/ch*.yaml`, `lesson/index.json`, `cells/*.py` against
`AGENTS.md` and the lecture notes (`lecture-note/`, repo root) if present.

- **C1 Checkpoint completeness.** Every checkpoint: `goal`, `ask`, `accept`,
  ≥2 `hints` (each a smaller question, never the answer), `reveal_after`,
  and a `note:` skeleton with «slots».
- **C2 Fresh variants.** Any checkpoint whose answer could leak (spoken,
  spoiled, or revealed by UI) lists `fresh_variants` on new data.
- **C3 Accept is judgeable by meaning.** A gold answer plus what counts as
  equivalent; no wording-dependent criteria.
- **C4 Facts and math check out.** Verify every number and formula in `ask`/
  `reveal_after`/`note` against the lecture notes; students can't catch an
  error, so the reviewer must.
- **C5 Objectives covered.** The module's learning objectives in the repo
  `curriculum.yml` all map to at least one checkpoint.
- **C6 Length and ramp.** Difficulty rises monotonically; estimated session
  time (timestamp span of past `session_log*.jsonl`) fits 60–90 minutes.
- **C7 The red-team checkpoint tests taught knowledge.** The flawed claim is
  catchable *using only what earlier chapters built* (e.g. the p=0 ring as
  counterexample); it is a transfer test, not trivia, and not solvable by
  generic skepticism ("check the data") without the concept.
- **C8 Practice variants exist.** "Give me another one like that" is
  satisfiable from `fresh_variants` or an obvious recipe on the module's
  canonical objects.
- **C9 Templates are self-describing and honest.** Every `cells/*.py` has a
  `# describe:` line matching what it actually renders.
- **C10 No unexplained jargon.** Every technical term in `ask`/`reveal_after`
  is defined at first use, in plain words.

## Part P — Session process

Review the newest complete `session_log*.jsonl` + `reviewer_log.jsonl` +
the matching session notebook. These findings indict prompts/extension, not
the student or the past session (see Fix targets).

- **P1 Log ↔ notebook ↔ summary agree.** Every checkpoint logged has its
  note cell and its `session_record` row; judgments match what the
  transcript shows actually happened.
- **P2 Verbatim integrity.** `student_response` and note «slots» match
  `student_said_verbatim`.
- **P3 Speech discipline.** Tutor turns are 1–3 short sentences, one
  question at a time, no process narration ("Let me check the log…").
- **P4 No answer leakage while a checkpoint is open** — including the
  extension's own UI: working-message tips, status lines, and dialog text
  must not state facts the current or a future checkpoint asks for.
- **P5 Hint ladders shrink.** Each successive hint is a smaller question;
  the student's final step is always left to them; warm at every rung.
- **P6 Re-anchoring.** After any detour/hint, the live question is restated
  in full — never a bare "so, what do you think?", never silence.
- **P7 Detours logged.** Student questions → answer + souvenir cell +
  `log_detour`; curiosity recorded as engagement.
- **P8 Dialogs only where scripted.** `ask_user_question` used exactly for
  script-marked predictions and resume — and those *do* use it (a marked
  prediction asked as plain text is a finding); never doubled with a typed
  question in the same turn.
- **P9 Grading integrity.** `hints_used` truthful; no fake `pass`;
  predictions never judged wrong; extra practice logged as `_extra`, not
  failure.
- **P10 Failures stay backstage.** nb_* errors handled via their RECOVERY
  line; no infrastructure debugging, cell talk, or error jargon shown to
  the student.

## Part D — Dynamic E2E gate

Drive a **live tutor session** with the harness in `tutor-prototype/review/`
(herdr-based; see `review/README.md` for the exact commands). The reviewer
plays the student. Fidelity requirements: course model
(`TUTOR_MODEL`, default `deepseek/deepseek-v4-flash-0731`), global agent
extensions disabled (`--no-extensions -e <module>/.pi/extensions/notebook-tool.ts`),
a browser page connected **before** the tutor's first nb_* call (the marimo
kernel wakes only when a client connects), sandbox copy of the module (never
the real working dir).

Run at minimum the **novice run** plus the three probes; log every Part P
violation observed live as a finding too.

- **D1 Novice run.** Persona: zero programming, a little nervous, answers
  honestly, one wrong guess somewhere. Must reach the end of chapter 2 with
  every checkpoint logged, note cells rendered, no stall, no unhandled
  dialog.
- **D2 Pace gating works.** "Where to next?" dialog after every checkpoint;
  only "Ready" advances; "Give me another one like that" yields a fresh
  problem on new data, logged `_extra`.
- **D3 Stuck probe.** Answer wrong 3+ times on one checkpoint: hints shrink,
  tone stays warm, the answer is never stated, `guided` logged truthfully.
- **D4 Shortcut probe.** "Just tell me the answer": warm decline + smallest
  next step; never the answer.
- **D5 Detour probe.** Ask one genuine question mid-checkpoint: correct
  answer, souvenir cell, `log_detour`, then the live question restated in
  full.
- **D6 Resume works.** Kill the tutor mid-chapter, restart: continue path
  recaps and lands on the right checkpoint; fresh path calls
  `nb_fresh_start` and starts at cp0.
- **D7 Notebook-down mode.** Start the tutor without the browser connected:
  it must follow the RECOVERY line (ask to open the page), not debug in
  front of the student, and proceed once connected.
- **D8 Tool discipline.** Transcript shows scripted builds via
  `nb_add_template` (with `checkpoint`), exercises via `nb_add_exercise`, no
  bash, no hand-written log JSON, `checkpoint_done` closing every checkpoint.

After the run, feed the sandbox's `session_artifacts/` and notebook back
through Parts S and P — the E2E gate passes only if that pass is also clean.

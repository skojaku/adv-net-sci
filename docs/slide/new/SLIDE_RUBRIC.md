# Slide Validation Rubric

Standards and review procedure for lecture decks in this course (Marp decks under
`docs/slide/new/`). Written to be executable by **any** reviewer — a human, or any
coding agent (Claude, pi, …). It uses only shell commands and file paths; no
agent-specific tooling.

The bar is deliberately high, especially for figures. A slide that merely "works"
but is not simple, clear, and easy to see does **not** pass. The reviewer's job is
to report findings, not to fix them — fixing is a separate task.

## Core principles

1. **One slide, one point.** Every slide teaches exactly one thing, stateable in one sentence.
2. **Dense, but progressive.** Slides should be substantive, never thin — but density
   must accumulate one component at a time (progressive disclosure), not land all at once.
3. **Teach visually.** The figure carries the explanation; text supports the figure.
4. **Conversational.** Slides talk *with* students. Questions come before answers.
5. **One complexity at a time.** Never introduce two unfamiliar ideas in the same step.
6. **Interactive demo at every milestone.** Milestones are roughly the sections (parts) of the deck.

## How to run a review

### 1. Render — always

```sh
cd <module dir>   # e.g. docs/slide/new/m01
marp <deck>.md --theme network-science.css --allow-local-files \
     --images png -o review/slide.png        # emits review/slide.001.png … one per slide
```

Never judge figures or layout from the markdown source alone — visibility, edge
crossings, label sizes, and balance are only assessable on rendered slides.
PNG export shows each slide's **final** state; progressive disclosure
(fragmented `*` lists, build sequences) must be verified in the source.

### 2. Student pass

View every slide in order, at reading speed. For each slide, write down its point
in one sentence. If you cannot — or you need two sentences joined by "and" — that
is a P1 finding. Note every place your eye hesitates or wanders: that hesitation
is usually a figure or layout finding.

### 3. Checklist pass

Go slide by slide against every criterion below. For dense slides, open the
markdown source and confirm a disclosure mechanism exists (`*` fragment lists, or
a build sequence of consecutive slides adding one element to the same figure).

### 4. Structure pass

At deck level:

- List the parts (section dividers) and map them onto the four-act arc (S1–S4).
- List the milestones (≈ part boundaries) and check each has an interactive
  demo or student activity (S5). The report must include this milestone list.

### 5. Report

Use the report format at the bottom. Order findings by severity, then slide number.

## Severity and verdict

- **BLOCKER** — violates a core principle; the slide fails its teaching job.
  Must be fixed before the deck is used.
- **MAJOR** — noticeably hurts clarity or engagement; fix before lecture.
- **MINOR** — polish; fix when touching the slide anyway.

**Verdict:** `FAIL` if any Blocker · `NEEDS WORK` if any Major · `PASS` otherwise
(Minors alone still pass).

## Criteria

### P — One point per slide

- **P1 · Blocker — Single point.** A slide introduces at most **one** new concept.
  Two or more new definitions, claims, or mechanisms on one slide is a Blocker
  (e.g. defining a term *and* introducing a special case of it).
  *Check:* the one-sentence test from the student pass.
- **P2 · Major — Progressive disclosure.** A dense slide (final state has more than
  a title + one figure + one short text block) must build one component at a time:
  fragmented lists (`*` markers in Marp, not `-`), or a build sequence of
  consecutive slides that add one element to the same figure. Dense-and-static is a Major.
- **P3 · Minor — No thin slides.** Slides must be dense in substance. A slide whose
  final state is nearly empty, or that restates the previous slide without adding
  anything, is a Minor.

### F — Figures (high standard — this is where most decks fail)

- **F1 · Blocker — No unexplained encodings.** Any visual variation must mean
  something stated on the slide. Node sizes differ → the size must encode a named
  quantity. Same for node color, edge thickness, edge style, layout position.
  Otherwise all nodes are the same size, all edges the same weight. Unexplained
  complexity invites confusion.
- **F2 · Major — Minimize edge crossings.** Network figures must be laid out to
  avoid edge crossings. If the graph is planar, draw it planar. A crossing is
  acceptable only when topologically unavoidable — and a Blocker if crossings make
  the structure hard to trace at all.
- **F3 · Major — Legible from the back row.** Labels, strokes, and contrast must
  read at rendered slide size. Thin lines, small fonts, gray-on-gray fail.
  Concretely: in-figure text must land at least **body size on the rendered slide**
  (30px type ≈ 15px x-height). The page number is *not* the floor — that standard was
  tried and rejected by the lecturer. `check_render.py` measures this; a failing run
  is a Major on every named slide.
- **F4 · Major — The figure carries the point.** The figure must show the slide's
  single point, not a multi-panel dump. Multi-panel figures are acceptable only as
  a build (one panel per step). Decorative elements that encode nothing get cut.
- **F5 · Minor — Palette discipline.** Use the theme tokens (accent `#3959A6`,
  accent-2 `#B14434`, accent-3 `#DAB167`, annotation gray `#6b6b6b`). The palette
  is already good; off-palette colors are a Minor unless they collide with an
  existing encoding (then Major).

### L — Layout and format

- **L1 · Blocker — At most one text column.** Two-column layouts are fine — the
  house pattern is text + figure. Two or more columns of *text* (including
  three-way `cols3` text layouts) are a Blocker.
- **L2 · Blocker — No tables.** Tables are the worst presentation format. Convert
  every table to an annotated figure, or to a build that reveals one row-equivalent
  at a time as marked-up text/graphics.
- **L3 · Blocker — No code.** No code blocks, no inline code teaching syntax.
  A single plain-prose pointer ("hands-on in the Module 01 notebook") is allowed.
- **L4 · Minor — Bullets in moderation.** Bullets are practical but easy to overuse:
  more than 4 items, nested bullets, or more than one list per slide is a Minor.
  A bullet list standing in where a figure should teach the idea is a Major (F4).
- **L5 · Major — No paragraph below a fragmented list.** The room reads it before the
  bullets reveal, which defeats the build. Move it above the list, fold it into the
  last fragment, or make it a fragment itself.
- **L6 · Minor — Centre shallow slides.** A slide whose content does not fill the frame
  hangs from the rule with all the slack below; it takes `<!-- _class: mid -->`, which
  centres the body block only (headings stay at their fixed y so titles line up
  deck-wide). Most question slides qualify.

### N — Narrative and tone

- **N1 · Major — One complexity at a time, in order.** A slide may rely only on
  concepts already introduced. If understanding a slide needs an idea that arrives
  later (or never), that is a Major.
- **N2 · Major — Teach visually.** Every concept slide has a visual that does the
  explaining. Exceptions: question/prompt slides, part dividers, the roadmap.
- **N3 · Major — Conversational voice.** The deck addresses students directly
  ("Can you…?", "Your turn", "What breaks if…?"). A whole part with no direct
  address or question is a Major; individual textbook-monologue slides are Minors.
- **N4 · Major — Question before answer.** Key results are set up as a question,
  a beat for thinking (turn to your neighbor / take 30 seconds), then the answer.
  Revealing the punchline in the same breath as the question is a Major. The answer
  must not appear *anywhere* on the question slide — a gray `note` has leaked the
  puzzle's answer twice; check the notes, not just the body.

### S — Deck structure (four-act arc + milestones)

- **S1 · Blocker — Act 1: story.** The deck opens with a concrete story or
  historical example — real names, dates, places. Opening with definitions is a Blocker.
- **S2 · Major — Act 2: math of the story.** The second movement mathematically
  analyzes *that same* opening example — not a fresh toy example.
- **S3 · Major — Act 3: generalization.** The third movement extends the math from
  the historical case to general graphs/networks.
- **S4 · Major — Act 4: edge cases as prompts.** The final movement probes edge
  cases, each posed **as a question to students** before any resolution
  (self-loops? disconnected? a single node? directed?).
- **S5 · Major — Demo at every milestone.** Each milestone (≈ each part) contains
  an interactive element: a demo, worksheet, trace-it-yourself activity, poll, or
  live widget. A milestone without one is a Major per milestone.

## Report format

```markdown
# Slide review — <deck path> — <date>

**Verdict:** FAIL | NEEDS WORK | PASS
**Slides:** <N> · **Blockers:** <n> · **Majors:** <n> · **Minors:** <n>

**Milestones:** (structure pass, S5)
- Part 1 <title> — demo: <yes: what / MISSING>
- …

## Blockers
1. Slide 12 "<title>" — L2 — <evidence: what the rendered slide shows> — Fix: <concrete change>.

## Majors
…

## Minors
…
```

Every finding names the slide (number + title), the criterion ID, the evidence as
seen on the **rendered** slide, and a concrete fix. Deck-level findings (S-criteria)
use "deck" in place of a slide number.

## Calibration examples (from m01, 2026-08)

- **F1 Blocker.** "Coming up in Module 02" (`abstraction.png`): left-panel landmass
  blobs differ in size for no stated reason; right-panel multi-edges curve and
  nearly cross. Nothing on the slide explains either. Fix: uniform shapes,
  straight or gently-curved non-crossing edges.
- **L2 Blocker.** "The Königsberg verdict": a 4-row degree/parity table. Fix: put
  the degree numbers directly on the network figure, color odd-degree nodes
  accent-2, and reveal one landmass at a time.
- **L3 Blocker.** "Degree, three ways": a Python code block plus a table. Fix: cut;
  leave one prose pointer to the notebook.
- **P1 Blocker.** "A graph, written down": introduces $G=(V,E)$, multigraphs, and
  self-loops on one slide — three points. Fix: split into a build.
- **Pass.** "The Königsberg bridge problem": one point (the puzzle), a story with
  place and date, a question in a formula panel, a map figure, conversational note.

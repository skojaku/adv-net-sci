# Slide Validation Rubric

Standards and review procedure for Marp slide decks. Tuned for technical/didactic
decks — lectures, technical talks, workshops — not generic business decks. Written
to be executable by **any** reviewer — a human, or any coding agent. It uses only
shell commands and file paths; no agent-specific tooling.

For the lecturer's decks, `HOUSE_STYLE.md` (section 7 is its checklist) refines these criteria and wins
where they disagree. Criteria marked *lectures* do not apply to a talk, whose story criteria are
`HOUSE_STYLE.md` section 10.

The bar is deliberately high, especially for figures. A slide that merely "works"
but is not simple, clear, and easy to see does **not** pass. The reviewer's job is
to report findings, not to fix them — fixing is a separate task.

## Core principles

1. **One slide, one point.** Every slide teaches exactly one thing, stateable in one sentence.
2. **Dense, but progressive.** A run of slides should be substantive, never thin — but density
   must accumulate one component at a time (progressive disclosure), not land all at once. A
   single slide may be one sentence or one picture when that is its beat.
3. **Teach visually.** The figure carries the explanation; text supports the figure.
4. **Conversational.** Slides talk *with* the audience. Questions come before answers.
5. **One complexity at a time.** Never introduce two unfamiliar ideas in the same step.
6. **Interactive demo at every milestone** (lectures). Milestones are roughly the sections (parts)
   of the deck. A talk asks the room at least once (CompleNet: three A-or-B tests).
7. **Direct wording** (the lecturer, 2026-10-31: 「もっと端的に、シンプルに、直接的かつ簡潔に、飾らずに」).
   Every title, sub, take, cue, label and bullet says what the slide shows, in literal words: no
   figure of speech, no cleverness, no thematic label. See N9. This applies from the first
   wireframe, not only to the finished deck.

## How to run a review

### 1. Render — always

```sh
cd <deck dir>
marp <deck>.md --theme ~/.claude/skills/slide/theme.css --allow-local-files \
     --images png -o review/slide.png --no-stdin   # emits review/slide.001.png … one per slide
```

Use `--theme <your-theme>.css` if the deck has its own theme instead of the bundled
default. Never judge figures or layout from the markdown source alone — visibility,
edge crossings, label sizes, and balance are only assessable on rendered slides. PNG
export shows each slide's **final** state; progressive disclosure (fragmented `*`
lists, build sequences) must be verified in the source.

### 2. Student pass

View every slide in order, at reading speed. For each slide, write down its point
in one sentence. If you cannot — or you need two sentences joined by "and" — that
is a P1 finding. Note every place your eye hesitates or wanders: that hesitation
is usually a figure or layout finding.

### 3. Checklist pass

Read the wording first (N9): every title, sub, take, cue, bullet and label, one by one, against the
test in N9. Do this before the figures; a figurative title is a finding even when the figure is good.

Go slide by slide against every criterion below. For dense slides, open the
markdown source and confirm a disclosure mechanism exists (`*` fragment lists, or
a build sequence of consecutive slides adding one element to the same figure).

### 3b. Numbers pass

Verify every concrete number on the slides against the experiment's data tables and
notes (NOTE.md or equivalent) before shipping — spawn a verification agent if the deck
is data-backed. Classify each: OK / STALE / UNSUPPORTED / MISMATCH. One results deck
shipped four bad numbers at once: a "0–11 %" range the data put at 0.4–17.8 %, a
"six times the information" with no defensible denominator, a title crediting the call
count to fewer models than produced it, and a temperature claim its own resample arm
exceeded. All four read as precise and all four were wrong; only recomputation finds
this class.

### 4. Structure pass

At deck level:

- List the parts (section dividers) and map them onto the four-act arc (S1–S4; for a talk, the
  arc of `HOUSE_STYLE.md` section 10.1), and read the F slides alone (the spine test).
- Lectures: list the milestones (≈ part boundaries) and check each has an interactive
  demo or audience activity (S5). The report must include this milestone list.

### 5. Report

Use the report format at the bottom. Order findings by severity, then slide number.

## Severity and verdict

- **BLOCKER** — violates a core principle; the slide fails its teaching job.
  Must be fixed before the deck is used.
- **MAJOR** — noticeably hurts clarity or engagement; fix before delivery.
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
- **P3 · Minor — No thin slides.** A slide that restates the previous slide without adding
  anything is a Minor. A nearly empty slide is not thin when emptiness is its beat: a
  statement (F), a picture in a narrated run (G), a part opener.

### F — Figures (high standard — this is where most decks fail)

- **F1 · Blocker — No unexplained encodings.** Any visual variation must mean
  something stated on the slide. Node/marker sizes differ → the size must encode a
  named quantity. Same for node color, edge/line thickness, edge style, layout
  position. Otherwise all nodes are the same size, all edges the same weight.
  Unexplained complexity invites confusion.
- **F2 · Major — Minimize edge crossings.** Node-link diagrams must be laid out to
  avoid edge crossings. If the diagram is planar, draw it planar. A crossing is
  acceptable only when topologically unavoidable — and a Blocker if crossings make
  the structure hard to trace at all.
- **F3 · Major — Legible from the back row.** Labels, strokes, and contrast must
  read at rendered slide size. Thin lines, small fonts, gray-on-gray fail.
  Concretely: in-figure text must land at least **body size on the rendered slide**
  (30px type ≈ 15px x-height, for the bundled default theme). The page number is
  *not* the floor — that standard has been tried and rejected. `check_render.py`
  measures this; a failing run is a Major on every named slide.
- **F4 · Major — The figure carries the point.** The figure must show the slide's
  single point, not a multi-panel dump. Multi-panel figures are acceptable only as
  a build (one panel per step) or as small multiples (the same plot per category, shared
  axes, category colours). Decorative elements that encode nothing get cut.
- **F6 · Major — No shared figures with different explanations.** If two slides
  reference the same figure file but explain it differently (different captions,
  different narrative roles), one slide gets content the other hasn't introduced.
  Emit two files. `check_deck.py` flags this automatically.
- **F7 · Major — A bullet cites only what its figure shows.** Every number in a
  figure slide's text must be visible on, or directly readable from, that figure.
  A range computed from a stdout table that the figure never plots reads as
  authoritative and is unverifiable by the room ("changes its answer 0–11 % of the
  time" under a figure with no change rates on it — and the range was wrong too).
- **F8 · Major — Every plotted quantity is named.** Each marker series, reference
  line, and annotation column carries the symbol or name the deck defined for it
  ($\beta_q$, $J_q$), in the legend or a column header. A square labelled only
  "checked by X" under a y axis that says "rate" severs the link to the slide that
  defined the rate; a grey column of "+0.65 [+0.58, +0.71]" with no header is
  unexplained digits. Both happened on the same deck in one round.
- **F5 · Minor — Palette discipline.** Use the theme's tokens: for house decks the palette of
  `HOUSE_STYLE.md` section 3; for the bundled theme accent `#3959A6`, accent-2 `#B14434`,
  accent-3 `#DAB167`, annotation gray `#6b6b6b`. Off-palette colors are a Minor unless they
  collide with an existing encoding (then Major).

### L — Layout and format

- **L1 · Blocker — At most one text column.** Two-column layouts are fine — the
  house pattern is text + figure. Two or more columns of *text* (including
  three-way `cols3` text layouts) are a Blocker.
- **L2 · Blocker — No tables.** Tables are the worst presentation format. Convert
  every table to an annotated figure, or to a build that reveals one row-equivalent
  at a time as marked-up text/graphics (CompleNet's query / key table, drawn and built
  row by row, is that build).
- **L3 · Blocker — No code.** No code blocks, no inline code teaching syntax.
  A single plain-prose pointer ("hands-on in the companion notebook") is allowed.
- **L4 · Minor — Bullets in moderation.** Bullets are practical but easy to overuse:
  more than 3 items, more than one list per slide, or nesting other than one level of at most
  two sub-items under a bold claim is a Minor. A bullet list standing in where a figure should
  teach the idea is a Major (F4).
- **L5 · Major — No paragraph below a fragmented list.** The room reads it before the
  bullets reveal, which defeats the build. Move it above the list, fold it into the
  last fragment, or make it a fragment itself.
- **L6 · Minor — Centre shallow slides.** A slide whose content does not fill the frame
  hangs from the title with all the slack below; it takes a layout that centres itself (F, C,
  G in the house theme) or `<!-- _class: mid -->`, which centres the body block only
  (headings stay at their fixed y so titles line up deck-wide).

### N — Narrative and tone

- **N1 · Major — One complexity at a time, in order.** A slide may rely only on
  concepts already introduced. If understanding a slide needs an idea that arrives
  later (or never), that is a Major.
- **N2 · Major — Teach visually.** Every concept slide has a visual that does the
  explaining. Exceptions: question/prompt slides, statements (F), quotations (Q), part
  dividers, the roadmap.
- **N3 · Major — Conversational voice.** The deck addresses the audience directly
  ("Can you…?", "Which one wins?", "What breaks if…?"). A whole part with no direct
  address or question is a Major; individual textbook-monologue slides are Minors.
- **N4a · Blocker — No answer leak on question slides.** The answer must not
  appear *anywhere* on the question slide — body, notes, gray text, or figcaption.
  A gray `note` leaking a puzzle's answer is a real, repeated failure mode.
  `check_deck.py` flags question slides with substantive notes (>15 words).
- **N4 · Major — Question before answer.** Key results are set up as a question,
  a beat for thinking (a near-white cue such as *Take a minute.*), then the answer.
  Revealing the punchline in the same breath as the question is a Major. The answer
  must not appear *anywhere* on the question slide — check the notes, not just the body.

- **N5 · Major — One storyline, serialized.** Never run two experimental threads in
  parallel. A setup slide that introduces two measurement pipelines at once ("Phase A
  … Phase B …") launches two storylines and the reader tracks neither. Present the
  first experiment plainly (without calling it "phase 1"), close it with a findings
  summary slide, then open the next as a follow-up question. Check the whole deck for
  parallel threads and serialize every one.
- **N6 · Major — The naive-reader test.** A reader who knows nothing of the project
  must be able to follow from slide 1. Internal context — a sibling experiment, a
  prior run, a framing the team studies — is either introduced on its own slide
  (a failed prior run often makes the best opening story) or cut. "Why does this
  experiment exist" must be answered before any theory or setup slide, and the
  why must visibly translate into the how ("everything a vote or a reviewer can do
  is a function of three per-question rates" is a bridge; a pipeline diagram is not).
- **N7 · Major — Plain academic language.** No software-engineering jargon on slides
  or figures: "arm", "cell", "probed items", "screened" become "condition",
  "model × benchmark", "the questions the author ever got wrong", "reviewed". No
  rhetorical metaphor doing load-bearing work: "the taller spike swaps ends",
  "ladder", "waves through", "only downhill", "borrowed ability" all lose to the
  direct sentence ("the tall spike is at 1 for weak models, at 0 for strong ones").
  Prefer "questions" to "items". Isolated instances are Minors; a deck written in
  this register is a Major.
- **N9 · Major — Direct wording (a titled rule; check it on every slide).** The lecturer's
  instruction of 2026-10-31, after a wireframe titled "One walk, three worlds" and "Which circle
  dies last?": write plainly, directly and briefly, with no ornament. A title is the claim or the
  question in literal words, naming things by their technical term. N7 and N8 cover the
  vocabulary and the sentence; N9 is the check that a reviewer runs on **every** title, sub, take,
  cue, bullet and figure label, and a figurative **title or F statement is a Major by itself**.
  - **No thematic or poetic titles.** "One walk, three worlds" → "Random walks appear in many
    fields". "A man leaves the pub" → "Where is the walker after 100 steps?". "Two rooms, one
    door" → "Two communities joined by one edge". "Look near where he started" → "Most likely
    near the start". A title that could be the name of a chapter in a novel is wrong.
  - **No verbs of life, war or commerce for mathematical objects.** *dies, survives, forgets,
    remembers, wins, buys, outvotes, collapses, refuses, sets the clock*. "Which circle dies
    last?" → "Which term stays the longest?". "The slowest circle sets the clock" → "The mixing
    time follows from λ₂". "Forgetting is a distance that shrinks" → "The distance to π
    decreases". "Small gap, long memory" → "Small gap, long mixing time".
  - **No metaphorical nouns for plain things.** "rooms" for communities, "world" for field,
    "door" for an edge, "clock" for a time scale, "blind walker" for a random walker.
  - **No commands as titles.** "Measure it", "Expand it" → "Pen & Paper, Part 1", with the
    subject on the `.sub`.
  - **No flourish at the end of a statement.** "…degree, and nothing else" → "…proportional to
    degree".
  - **One literal sentence per idea.** If a title needs an explanation to be understood, the
    explanation is the title.
  - **Test:** read each title aloud to someone who has not seen the figure. If they would
    answer "what do you mean?", it is figurative. Report every hit as an exact old/new pair.
    `gatelib` (`check_deck.py`, "figurative wording") lists likely hits; it is a prompt for the
    reviewer, not a replacement for reading every slide.
- **N8 · Major — Sentence-level diction.** N7 rules out the wrong vocabulary; this
  rules out the wrong sentence. Every clause below was cut from a shipped deck.
  - **One idea per sentence,** and at most two short lines per text block. A clause
    that carries no fact, cause, number or instruction is deleted rather than
    shortened — that is the filler pass (`FILLER_PASS.md`), run first.
  - **No "A, not B" antithesis.** "Not kilometres. Not people. Edges." · "the worst
    case, not the average" · "Not a sample — the whole graph" · "Not sixty." Rewrite
    each as the positive statement alone. The construction is a tic: by its third
    appearance it has stopped carrying emphasis and started sounding like a house
    style. A genuine disambiguation between two defined quantities ("the C-bar here
    is the average local clustering, not the transitivity") is a different thing and
    stays.
  - **No metaphorical or colloquial verbs.** Banned from Module 02 in one pass:
    shortcuts *buy* short routes · randomness *hands you* short paths · the average
    *collapses* · real networks *refuse to choose* · ten nodes *outvote* the hub ·
    clustering *wins* the ratio · the far pairs *moved* · the longer route *does not
    count*. Literal enumeration ("the diagonal entry counts closed walks of length
    three") is correct and stays. The test is whether the verb is doing arithmetic or
    doing colour.
  - **No em-dash, anywhere in the deck.** Beside a formula it reads as a minus sign.
    Use a colon, a semicolon, or a full stop. `check_render` fails the build on it,
    and a deck can carry sixty of them for months without anyone reading the failure.
  - **Vary the construction.** The three rules above push every sentence toward the
    same shape, and forty slides of "X is Y. Z is W." is its own kind of unreadable.
    Check consecutive slides against each other, not only each slide against the rules.

  Run this as its own top-to-bottom sweep. Splitting the deck across parallel
  reviewers by slide range works well — the violations are local, and one reviewer
  per range returns exact old/new pairs the lead applies in order.

### S — Deck structure (four-act arc + milestones; lectures)

A talk's structure is `HOUSE_STYLE.md` section 10 instead: the arc per part, the spine test,
the close that answers the opening picture. S1 (open on a concrete story) holds for both.

- **S1 · Blocker — Act 1: story.** The deck opens with a concrete story or
  historical example — real names, dates, places. Opening with definitions is a Blocker.
- **S2 · Major — Act 2: depth on the story.** The second movement analyzes *that
  same* opening example in depth — not a fresh toy example.
- **S3 · Major — Act 3: generalization.** The third movement extends the analysis
  from the concrete opening case to the general case.
- **S4 · Major — Act 4: edge cases as prompts.** The final movement probes edge
  cases, each posed **as a question to the audience** before any resolution
  (what if it's empty? disconnected? a single item? reversed?).
- **S5a · Major — A demo the presenter cannot launch is not a demo.** If a milestone
  slide points at a live tool, the link must be **on the slide** and clickable in the
  HTML export. A demo link that lives only in the speaker note, without a scheme, means
  the presenter has to retype it mid-talk. Check the export, not the markdown:
  `grep -o 'href="http[^"]*"' out.html`.
- **S5 · Major — Demo at every milestone.** Each milestone (≈ each part) contains
  an interactive element: a demo, worksheet, trace-it-yourself activity, poll, or
  live widget. A milestone without one is a Major per milestone.
- **S6 · Major — Do not re-ask what the worksheet asks.** When the module ships a
  pen-and-paper exercise or a lab notebook, read it before writing or reviewing the
  deck, and treat its questions as spent. After the exercise the deck's job is to
  **name and formalise** what the audience computed — the term, the symbol, the
  general formula — and then to go where paper cannot reach. Module 02 lost about
  twenty slides to this rule in one pass: counting one distance by hand, "what single
  number would you report?", counting the six pairs around a node, the 150-friend
  fan-out table, and two worksheets with their answer slides were all already on the
  sheet. A slide that repeats an exercise question is a Major even when it is well
  made. The exception is a question the exercise *depends* on: Module 02 keeps "write
  down your guess now", because the sheet's last question asks the audience to compare
  against it.

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

## Calibration examples

Before the first review round of a new deck, build a small calibration set from
what that round actually finds — 2–3 concrete findings in the exact report format
above, so later rounds (and other reviewers) read findings the same way. The three
worked examples below are generic placeholders to show the format; replace them
with real findings from your own deck's first round as soon as you have one.

- **F1 Blocker (worked example).** A diagram has three elements filled in two
  different colors with no legend or label explaining what the colors mean, and
  two connector lines are curved so closely they nearly touch. Nothing on the
  slide explains either choice. Fix: pick one color per meaning and state it in
  the caption; separate the near-touching lines or merge them if they carry the
  same information.
- **L2 Blocker (worked example).** A slide presents a 4-row, 3-column data table
  summarizing categories and counts. Fix: put the counts directly on an annotated
  figure (e.g. a bar-free dot plot or the objects themselves), instead of a table.
- **Pass (worked example).** An opening slide poses a concrete, dated real-world
  scenario as a question, includes a labeled figure grounding it, and closes with
  a conversational prompt ("What would you guess happens next?") rather than
  answering immediately.

## Keeping this current

Same contract as the other guides in this skill family, all alongside this file —
`DECK_BUILD_GUIDE.md` and `FIGURE_GUIDE.md` (authoring), `REVIEW_PLAYBOOK.md` (the
review loop) — when a review teaches something new
about *what good looks like*, add it here; loop-process lessons go to
`REVIEW_PLAYBOOK.md`, authoring lessons go to `DECK_BUILD_GUIDE.md`/`FIGURE_GUIDE.md`.

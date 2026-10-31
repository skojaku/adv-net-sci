# Deck build guide

How to build a **new** slide deck from scratch. The other guides bundled alongside this one
cover judgment and review — `SLIDE_RUBRIC.md` (what good is), `FIGURE_GUIDE.md` (how to
draw), `REVIEW_PLAYBOOK.md` (how to run the review loop) — this one covers authoring: what
the slides are for, the order of work that succeeded, and the Marp/theme facts that were
established the hard way. Written, like the others, to be executable by any agent.

Everything here was learned rebuilding an early deck from scratch — 30 slides grew to 78
across thirteen rounds, including two full slide-by-slide passes. Where a rule states a
preference rather than a measured fact, treat it as decided, not as an invitation to
relitigate.

**Read `HOUSE_STYLE.md` first; it wins where the two disagree.** This guide predates the house
style: its measurements of the bundled "network-science" theme (heading, rule, fit budgets)
and its GIF and slider advice are kept for decks built on that theme. A house deck is built from
`house/`, steps its builds as runs of slides (no GIF, no slider), and plans its story before
its slides (`HOUSE_STYLE.md` section 10.6).

## What these slides are for — the use model

The framing that changes what "good" means on every slide:

> These are not slides for the audience to read. They are an aid for teaching *through
> dialogue with the room*. Keep the text short, highlight what matters, lower the
> complexity of each individual slide — and get the density back by animating instead.

What follows from it:

- **Telegraphic is fine.** "Read the row, then read the column — two lookups per cell."
  Fragments, no verb, no article: all acceptable where the presenter will say the sentence
  aloud. Keep full sentences only where the audience must reconstruct the argument later —
  theorem statements, definitions.
- **Density comes from builds, not text.** A build (a run of slides, each adding one element
  to the same figure) beats a paragraph. Live widgets belong in a notebook or app follow-up.
- **Bold marks key terms and nothing else.** `strong` renders hot orange with a brush
  underline. Bold the terms themselves (**the terms you are defining**…); unbold anything
  bolded for mere stress, or the colour loses its meaning. A coloured keyword in a title is a
  `.hot` span, not bold.
- **A question slide carries no answer — anywhere on the slide.** A gray `note` leaked a
  puzzle's answer twice in one deck. The answer goes on the *next* slide.
- **Never put a paragraph below a fragmented list.** The room reads it before the bullets
  reveal, which defeats the build. Move it above, fold it into the last fragment, or make
  it a fragment.
- **Interaction prompts must earn their place.** "Turn to your neighbor — 30 seconds" and
  two open-ended "your turn" slides were cut outright in review. Keep an activity only when
  it teaches a mechanism; drop ritual prompts.
- **The interaction worth strengthening: concrete first, then predict.** Have the room
  compute one small case by hand, then *predict* the general one without computing. Two
  slides, not one.
- **State the restriction on the slide *before* the number that depends on it.** A number
  is only as honest as the rule it was computed under, and the room can only check it if it
  has the rule first. One deck does this twice well and once backwards, and the contrast is
  the lesson: one slide fixes the denominator ("seven people make 21 pairs") one slide
  before a rate is defined from it, and another marks a subset as "the only ones that carry
  data" one slide before the next slide quotes their median. But a computed ratio shipped
  in an early part of the deck while the convention it rests on — that a zero-degree case
  counts as zero, say — was introduced as *new* forty slides later, in a much later part,
  on a slide that then asked the room to think about it. A convention spent before it is
  stated turns a later question into a formality.

  Quoting someone else's published number under an unstated convention is a *different*
  case and is fine — nothing on the slide computes it, so there is no arithmetic for the
  reader to fail. Pay it back later: one deck names the underlying convention in a later
  part and ties it explicitly back to the number quoted earlier.
- **When figure + text do not fit side by side, stack two rows** — figure full width,
  text on its own line — rather than shrinking both into `cols`.

## Deck directory

Scaffold a new deck from the bundled template — do not reinvent:

    <deck-slug>/
      <deck-slug>.md         the deck (marp front matter, math: katex)
      theme.css               house/theme-house.css, copied under this name (the gate
                               renders with <deck dir>/theme.css only)
      figures/                make_figures.py, figlib.py and figs_ui.py from house/,
                               emitted PNGs, frames/ for builds
      check_render.py         copy from `~/.claude/skills/slide/template/`, adjust
                               the deck filename — the build gate
      review/                 DECK_SPEC.md, FIGURE_SPEC.md, FIXES_Rn.md, rendered slide.NNN.png
      README.md               build commands (copy the template's and adjust)

See `~/.claude/skills/slide/template/` for a ready-to-copy starting point.

`check_render.py` is not optional. A deck that skips it gets the gatelib line
`(no check_render.py in module)` and every pixel-level check — overflow, text size,
container mismatch — silently does not run. One results deck went through several review
rounds that way; its bullet overflow and clipped legends were all found by eye, late.
Copy the template's file when the deck directory is created, not "later".

Gather your source material before writing DECK_SPEC.md — an outline, existing notes, a
script, a curriculum entry, whatever you are starting from. The four-act arc (below) is
often nearly written already in a good outline; find it before inventing one.

## Order of work

For a **talk** (conference, seminar) the order is different: story, then a wireframe of every slide with dashed figure boxes,
then red-pen rounds, then real figures, then animation. Follow `TALK_PLAYBOOK.md`; the list below is for lecture modules.

What thirteen rounds settled into; skipping a step reliably cost a round.

1. **DECK_SPEC.md first.** A slide-by-slide outline in `review/`: every slide named, its
   one point, its figure, its question/answer beat. Restate the rubric's non-negotiables
   at the top (fragments use `*`; no tables; no code; `cols` is text + figure only;
   question and answer on separate slides; every concept slide has a figure). Verify
   every number and claim in the spec before writing it down — two arithmetic errors once
   reached shipped slides *through* specs.
2. **FIGURE_SPEC.md, then the generator.** All figures from one `make_figures.py` on
   `house/figlib.py`, with assertions per `FIGURE_GUIDE.md`. A build's frames come from the
   same code (`figlib.emit_frames`), so the steps and the still cannot drift.
3. **Write the deck to the spec.**
4. **Gate before any review:** render and run both checkers; both must exit 0.

       python3 figures/make_figures.py
       cd ~/.claude/skills/slide && python3 -m gatelib review <deck_dir>   # render + all checks

   `check_render.py` measures what the audience sees — in-figure x-height ≥ 15px, drawing
   ≥ 150px, per-axis margin ≤ 30%, no ink below the pagination row (plus node discs
   26–52px, opt-in, for decks with circular node-diagrams — see `FIGURE_GUIDE.md`). It
   reproduces a human reviewer's measurements to the pixel; a green run is the completion
   criterion for figure work, not a matter of taste.
5. **Then the tiered review loop** — `/slide` in review mode, run per `REVIEW_PLAYBOOK.md`:
   - **Tier 0** every round: `check_render.py` + `check_deck.py` (zero tokens)
   - **Tier 1** per round: LLM review of only changed slides, judgment criteria only
   - **Tier 2** once before shipping: full-deck LLM review, all criteria
   Expect the Blocker count to bounce as the deck grows; what must fall is the severity
   class (structure → polish).
6. **Commit every gate pass, not just every round.** A commit is the checkpoint that
   survives a session-limit crash. Write `review/CHECKPOINT.md` after each round with
   the round number, gate status, and pending fixes.
7. **Last, the filler pass** — `FILLER_PASS.md`. A separate top-to-bottom sweep whose
   only job is deleting padding: restatements, emphasis that carries no fact, retellings
   of what the audience already did. It runs **after** the deck is complete and green,
   never during drafting — while writing you cannot tell scaffolding from load-bearing
   wall, and cutting early costs content. Re-render and re-gate when it is done.

## Marp and theme facts (verified in the render, not assumed)

These numbers describe the skill's bundled default `theme.css`. A deck using a different
theme must re-measure them the same way — render a probe slide, measure the PNG — rather
than assume they carry over.

- **Fragments:** only `*` list markers fragment. `-` does not. A list that reveals an
  argument uses `*`; a caption-like aside stays `-`.
- **The `w:` directive is inert** under this theme (`section .fig img { width: auto
  !important }` beats Marp's inline style). What actually bounds a figure: content area
  **1120px**, a `cols` column **537px**, display height cap **380px**. Author figures at
  final size (one unit = one slide pixel) and the numbers reconcile.
- Grid tracks are `minmax(0, 1fr)` — a `1fr` track lets an unbreakable formula in one
  column steal width from the other.
- **PNG, not SVG:** an `<img>` pointing at `.svg` tends to render blank inside Marp's
  `foreignObject`. **GIF animates** (referenced by relative path); inline `<svg>` is
  stripped by the sanitizer, and so are `style` attributes — style lives in the theme.
- **Scripting works, in the `--html` export.** A `<script>` runs and an
  `<input type="range">` fires its listener — tested in a real browser, not read off the
  HTML source. So a slider the presenter can drag while talking is a real option, not a
  closed door.

  Two conditions. It needs `--html` (or `html: true` in the front matter), and **that flag
  matters for the whole deck**: without it the HTML export escapes *all* raw HTML to
  literal text, including the existing `<div class="cols">` layout. And the `--images png`
  path parses raw HTML either way, so `check_render.py` never exercises the export the
  deck is actually given from — if you add scripted content, open the HTML and check it,
  because nothing in the pipeline will.

  A caution worth carrying, since it cost a round once: "Marp restricts scripting" was an
  over-generalisation of an SVG-specific finding, repeated in three briefs before anyone
  tested `<script>` separately. **One negative result about one tag is not a result about
  the sanitizer.** Test the thing you are about to rule out.

  Built and shipped once on a slide teaching a sparse data-structure layout: a slider that
  steps through rows while the row's contiguous slice of the underlying arrays highlights.
  Verified by driving the real slider in the bundled Chromium — inject a small harness that
  dispatches an `input` event and writes the outcome into the DOM, then read it with
  `--dump-dom`, since `--dump-dom` cannot interact on its own. Checking that the `<script>`
  tag survived the export is not the same as checking that it runs.

  Two gotchas that cost time here:

  - **`--no-stdin`, always.** Without it marp waits on stdin and never returns when it is
    not attached to a terminal — which is every background or scripted invocation. It looks
    exactly like a slow render.
  - **Widget styling lives in the theme, and the selectors must match what the JS builds.**
    Cells appended into a `<span>` are not children of the row, so `.row > i` silently
    matches nothing; and `<i>` is inline, so box properties need `inline-block` or every
    cell collapses into one run-on number. Both looked fine in the HTML source and wrong on
    the slide.
- KaTeX does not process `<figcaption>` — **nor any other raw HTML block**, including
  `steps-list`. One deck shipped nine captions and a roadmap item that printed a formula's
  raw LaTeX source to the room as literal text. `check_render.py` fails the build on it
  now; write the symbol as a word instead.
- **A figure is authored for one container.** Put a full-width figure inside a `cols` column
  and it renders at 48% — 19px node discs against 39px on the identical figure laid out full
  width, invisible in the source. The gate compares the authored width against the container
  it is used in; keep the generator's declaration and the deck's markup in step.
- `## Title` + `<hr>` stay on the same slide as their content; `---` after a title
  splits the slide.
- Classes of the bundled theme: `lead` (title), `part` (divider with `band` markup), `mid`
  (shallow slide — centres the body block only; the heading stays at its fixed y so titles
  line up deck-wide), `cols`, `fig` + `figcaption`, `formula`, `note`, `steps-list`. The house
  theme keeps them and adds the layouts and pieces of `HOUSE_STYLE.md` sections 8 and 9
  (markup: `house/layouts.md`).
- Type floors (already in the theme): body 30px, notes 27px, formula panels and
  figcaptions 30px. In-figure text must land at least body-size **on the slide** — raised
  repeatedly in early review; it is now an assertion in the figure generator and a
  `check_render.py` failure, not a review finding.

## Write the deck before you commission the figures

One deck dispatched three figure-generation tasks in parallel while the deck was still
being written, with the container for each figure taken from the *spec*. Two of the three
authored most of their figures at full width for slides that ended up two-column, and
`check_render.py` failed them all: a figure authored for 1080 px and used in a 537 px
column renders at 50% of its intended scale.

Halving a figure's width is a **re-composition, not a re-declaration** — a wide slope
chart, a large matrix, or two side-by-side panels do not survive it — so the cost of
getting this wrong is a second authoring pass, not a one-line edit. Write the slide first,
or at minimum fix the container per figure before dispatching, and put the list in the
brief.

## What fits on a slide with a wide figure, measured

For the bundled theme, on a slide with heading, rule, one line of body text, a full-width
figure and a figcaption: the heading's ink ends at y=85, the rule sits at y=139, and a
349 bp figure plus caption ends at **y=606** against a page number at 617–629. Two lines of
body text still fit. That is the budget; anything more and `check_render.py`'s
CONTENT_BOTTOM check fires.

If a figure cannot be beside its text — a wide map or diagram whose labels do not fit at
537 px, say — then stack: one short line above, figure full width below. A deck where
*every* slide does that is monotonous, so keep the two-column pattern wherever the figure
is small enough to take it.

## What actually fits on a slide

Arithmetic worth doing once, because ten of one deck's thirteen first-run gate failures
were the same mistake. The theme reserves nothing below **y = 660** in a 720px frame, a
title with its rule takes about **110px**, and a full-width figure may be **380px** tall
(`fig tight` 320, `fig stack` 190). So:

> a ~350px figure leaves room for **one** short line of text, and only above it.

(Measured on the bundled theme. The house theme has no rule under the title, so its layout A
holds a `.sub` above and a `.take` below a `fig tight` figure, 320 px.)

On the bundled theme a line above *and* a line below does not fit. Move the second one into the `figcaption` —
which is where prose belongs anyway — or shorten the drawing. Never shrink the type, and
do not reach for `fig tight` to buy 60px: the generator asserts the figure fits the cap the
deck's class declares, so a 349bp drawing in a `tight` container is a build failure, not a
saving.

Same arithmetic, different component: **`steps-list` gives eight rows** before the
pagination row. A ninth does not fit and shortening the text does not help, because the row
height is fixed. Merge two items.

## Density from motion, not from more text

The core framing: the slides are an aid for teaching through dialogue, so a slide should
carry one point and the *build* should carry the rest. Where a static figure would need a
legend or three panels, animate it instead — one deck's vocabulary slides draw a sequence
one step at a time, and another slide constructs a data structure's internal arrays row by
row.

Two things that make an animation teach rather than decorate:

- **Loop back to what the deck shows next.** One such animation settles on the exact frame
  its neighbouring static figure uses, so the loop hands off instead of resting somewhere
  arbitrary.
- **Generate it from the same data as the static figure, and assert they agree.** Duplicating
  geometry between an animation and its still is how the two drift; compute both from the
  one source and check.

- **Magic move between two slides** (the same object slides, resizes or recolours) is a
  different mechanism from a build inside one slide: matching `view-transition-name`s, HTML
  boxes rather than SVG shapes, Chrome HTML output only. Procedure and pitfalls:
  `MAGIC_MOVE.md`.

## A figcaption says what nothing else on the slide says — and survives the figure changing

Two failure modes, and the second one is the interesting one.

**The caption restates the drawing.** By one deck's fourth round this was the single most
common Minor in the deck: a figure printing a percentage under a caption restating the same
percentage in words, the same sentence twice, 120px apart. The division of labour is
**numbers in the drawing, prose in the caption** — and the test is not "does the caption
describe the figure" but "does the caption say something nothing else on the slide says".

Run it as a **criterion over every captioned slide**, not as a list of slides. One deck
fixed this class four times from four lists and it kept coming back, because each list was
the slides someone had happened to look at. When it was finally run as a criterion it
turned up a slide neither of two prior passes had caught, and cleared seven suspects that
did not hold up once the render was actually opened.

**The caption is orphaned by a fix to the figure it describes.** A caption written
truthfully in one round described a grouping that a later round changed to fix a different
defect. The caption did not change; the drawing moved under it, and a sentence that had
been correct became false without anybody editing it.

That one is not caught by reading captions, because nothing about the caption looks wrong.
Two defences:

- After changing a figure, **re-read the caption of every slide that uses it** — the same
  rule as "check every slide that uses the figure", extended to the words underneath.
- Prefer captions a regrouping cannot stale. Describe the *shape* of the finding ("most of
  the mass sits at the low end") rather than the specific grouping that produced it.

## When the module also has a worksheet or a lab

Read the exercise sheet and the notebook **before** the deck spec, and divide the work
explicitly. The division that survived Module 02:

- **Deck, before the exercise** — the story, the evidence, and the one question the
  exercise turns on. It ends on a hand-out slide that states the exercise's premise in two
  lines and stops.
- **The exercise** — every quantity the audience can work out with a pencil.
- **Deck, after the exercise** — the term, the symbol and the general formula for each
  thing they just computed, then the material paper cannot reach.
- **The lab** — sweeps, large-*n* behaviour, and anything that needs a slider.

The criterion is `SLIDE_RUBRIC.md` S6, and it is worth a lot of slides: Module 02 went from
95 to 47 mostly by deleting questions the sheet already asks. Budget the live-taught part
generously (Module 02: the first thirteen slides get half the half-hour) and let the
post-exercise naming pass run fast.

Three failures that only appear once you start cutting:

- **A figure can leak an answer.** `ring-lattice.png` draws the worksheet's own town and
  prints C-bar = 0.50 on it, which is the answer to the sheet's clustering question. The
  hand-out slide needed a new, unannotated build of the same geometry. Check every figure
  on and before the hand-out slide against the sheet's answer key, not just the slide text.
- **Cutting a build strands the figures downstream of it.** Module 02 deleted the two
  slides that introduced a chord and a long edge; the diameter figure two slides later
  still drew both, so the room would have met a graph it had never been shown. After
  deleting a build, re-read every later figure that was drawn on top of it.
- **Deleting a slide can orphan a figure into being wrong.** A caption written for the old
  neighbouring slide survives the deletion and now describes nothing. Same defence as the
  figcaption section above: re-read the caption, not just the image.

## Ship the artifact the deck is read from

If the deck is distributed as a PDF (the house convention for results decks is a
compiled PDF committed next to the markdown), recompile and commit that PDF with **every**
content commit — deck edits and figure regenerations both. One experiment's committed
`results.pdf` was four days and one full rewrite behind its `results.md`: readers of the
PR were reviewing conclusions the run had already retracted. The render gate does not
check this; make it part of the commit, not a separate step someone remembers.

## Keeping this current

Same contract as the other guides bundled with this skill: when building a deck teaches
something new about *authoring*, add it here; drawing lessons go to `FIGURE_GUIDE.md`, loop
lessons to `REVIEW_PLAYBOOK.md`, defect definitions to `SLIDE_RUBRIC.md`.

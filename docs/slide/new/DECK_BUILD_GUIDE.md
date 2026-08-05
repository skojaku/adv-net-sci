# Deck build guide

How to build a **new** module deck from scratch. The other three files cover judgment and
review — `SLIDE_RUBRIC.md` (what good is), `FIGURE_GUIDE.md` (how to draw),
`REVIEW_PLAYBOOK.md` (how to run the review loop) — this one covers authoring: what the
slides are for, the order of work that succeeded, and the Marp/theme facts that were
established the hard way. Written, like the others, to be executable by any agent.

Everything here was learned rebuilding the Module 01 deck (30 slides → 78, thirteen
rounds, two slide-by-slide passes by the lecturer himself). Where a rule quotes him, treat
it as decided.

## What these slides are for — the use model

The lecturer's own framing, which changes what "good" means on every slide:

> These are not slides for the audience to read. They are an aid for me to teach *through
> dialogue with students*. Keep the text short, highlight what matters, lower the
> complexity of each individual slide — and get the density back by animating instead.

What follows from it:

- **Telegraphic is fine.** "Arrive by one edge, leave by another — two edges per visit."
  Fragments, no verb, no article: all acceptable where the lecturer will say the sentence
  aloud. Keep full sentences only where a student must reconstruct the argument later —
  theorem statements, definitions.
- **Density comes from motion, not text.** A build that animates (GIF) beats a paragraph.
  Sliders and scripting are restricted in Marp — animation is the reachable interactivity;
  treat live widgets as a notebook follow-up.
- **Bold marks key terms and nothing else.** `strong` renders accent-2 red. Bold the terms
  themselves (**graph**, **degree**, **path**…); unbold anything bolded for mere stress,
  or the red loses its meaning.
- **A question slide carries no answer — anywhere on the slide.** A gray `note` leaked the
  puzzle's answer twice in m01. The answer goes on the *next* slide.
- **Never put a paragraph below a fragmented list.** The room reads it before the bullets
  reveal, which defeats the build. Move it above, fold it into the last fragment, or make
  it a fragment.
- **Interaction prompts must earn their place.** The lecturer cut "Turn to your neighbor —
  30 seconds" and two "Your turn" slides outright. Keep an activity only when it teaches a
  mechanism; drop ritual prompts.
- **The interaction he asked to strengthen: concrete first, then predict.** Have students
  compute one small case by hand ($A^2$, one entry), then *predict* the general one
  ($A^3$, $A^4$) without computing. Two slides, not one.
- **When figure + text do not fit side by side, stack two rows** — figure full width,
  text on its own line — rather than shrinking both into `cols`.

## Module directory

Scaffold a new module from m01 — do not reinvent:

    docs/slide/new/m0N/
      m0N-<slug>.md         the deck (marp front matter, math: katex)
      network-science.css   copy from m01 — the theme carries the lecturer-set type sizes
      figures/              make_figures.py (+ make_animations.py), emitted PNG/GIF
      check_render.py       copy from m01, adjust the deck filename — the build gate
      review/               DECK_SPEC.md, FIGURE_SPEC.md, FIXES_Rn.md, rendered slide.NNN.png
      README.md             build commands (copy m01's and adjust)

Content sources: the module's entry in `curriculum.yml` (big_question, hook, the concept
list with prereqs — the four-act arc is nearly written there already) and
`docs/lecture-note/<module-slug>/`.

## Order of work

What thirteen rounds settled into; skipping a step reliably cost a round.

1. **DECK_SPEC.md first.** A slide-by-slide outline in `review/`: every slide named, its
   one point, its figure, its question/answer beat. Restate the rubric's non-negotiables
   at the top (fragments use `*`; no tables; no code; `cols` is text + figure only;
   question and answer on separate slides; every concept slide has a figure). Verify
   every number and claim in the spec before writing it down — two arithmetic errors
   reached m01 slides *through* specs.
2. **FIGURE_SPEC.md, then the generator.** All figures from one `make_figures.py` with
   assertions per `FIGURE_GUIDE.md`. Animations in `make_animations.py`, importing
   geometry and palette **from** `make_figures.py` so the two cannot drift.
3. **Write the deck to the spec.**
4. **Gate before any review:** render and run the checker; it must exit 0.

       python3 figures/make_figures.py
       python3 figures/make_animations.py
       marp m0N-<slug>.md --theme network-science.css --allow-local-files \
            --images png -o review/slide.png
       python3 check_render.py

   `check_render.py` measures what a student sees — in-figure x-height ≥ 15px, node
   discs 26–52px, drawing ≥ 150px, per-axis margin ≤ 30%, no ink below the pagination
   row. It reproduced the human reviewers' measurements to the pixel; a green run is the
   completion criterion for figure work (the lecturer's most-repeated complaint, stated
   as a build failure).
5. **Then the review loop** — `/slide-review`, run per `REVIEW_PLAYBOOK.md`, until PASS.
   Expect the Blocker count to bounce as the deck grows; what must fall is the severity
   class (structure → polish).
6. **Commit every round**, with the round's lesson in the message.

## Marp and theme facts (verified in the render, not assumed)

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
- KaTeX does not process `<figcaption>` — no math there.
- `## Title` + `<hr>` stay on the same slide as their content; `---` after a title
  splits the slide.
- House classes: `lead` (title), `part` (divider with `band` markup), `mid` (shallow
  slide — centres the body block only; the heading stays at its fixed y so titles line
  up deck-wide), `cols`, `fig` + `figcaption`, `formula`, `note`, `steps-list`.
- Type floors (lecturer-set, already in the theme): body 30px, notes 27px, formula
  panels and figcaptions 30px. In-figure text must land at least body-size **on the
  slide** — he raised this four times on m01; it is now an assertion in the figure
  generator and a `check_render.py` failure, not a review finding.

## Keeping this current

Same contract as the other three files: when building a deck teaches something new about
*authoring*, add it here; drawing lessons go to `FIGURE_GUIDE.md`, loop lessons to
`REVIEW_PLAYBOOK.md`, defect definitions to `SLIDE_RUBRIC.md`.

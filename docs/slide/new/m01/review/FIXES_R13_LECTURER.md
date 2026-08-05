# Round-13 — the lecturer's slide-by-slide pass

Sadamori went through the rendered deck slide by slide. Slides are named by heading below,
since numbers shift.

## The thing he has now said four times

**In-figure text is too small.** His words this round: *"この指摘を何度も食らっているので
なるべくフォントをあげるように本当に直してください"* — I keep getting this same note, so
please actually raise the fonts. He named fourteen slides individually.

He also gave a concrete floor for the worst of them: **at least double the current size**
("少なくともフォントを2倍にする"), and for slide 016's "k = 4", *"フォントは最大限上げる"* —
raise it as far as it will go.

`check_render.py` now fails on this: it measures glyph x-height on every figure against a
15px floor (body type is 30px, which renders ~15px x-height) and currently fails 27 slides.
**That check passing is the completion criterion.** Do not fix this per label — it has
regressed twice that way. Derive the on-slide size and assert it:

    scale       = min(container / src_w, 380 / src_h, 1.0)    # container 537 or 1120
    on_slide_px = pt * (dpi / 72) * scale

Named slides, in his order: **013, 014, 016, 018, 020, 021, 023, 024, 026, 027, 030, 038,
039, 072, 073, 078**. Effectively the whole deck, which is why it is one rule.

## Already fixed

`section.mid` centred the whole slide, so the title moved down the frame and no longer lined
up with its neighbours. He flagged this twice. The theme now centres only the body block and
leaves the heading where it always sits.

## Cuts — remove these slides

- **"Your turn: abstract a transit line"** (012) — *"いらない"*.
- **"You are mid-walk. How many edges do you use?"** (017) — *"いらないわ"*.
- **"Your turn: run the sweep"** (040) — *"要らないかな"*, tentative.
- **"Three sweeps, three components"** (041) — *"要らないかな"*, tentative. He also could not
  read its right-hand figure: *"右の図が散布図になってグラフではなくて何が言いたいのかよく
  わからない"* — it reads as a scatter plot rather than a graph, and its point does not come
  across.

Treat 012 and 017 as decided. For 040/041, cut them unless doing so leaves the component
sweep untaught — if it does, say so and propose the smaller change instead.

## Text to delete

- **"The Königsberg bridge problem"** (004) — the gray note **gives the answer away**. Delete it.
- **"Your turn"** (005) — delete the gray note.
- **"What can you throw away?"** (007) — drop "Turn to your neighbor — 30 seconds".

## Per-slide

- **013 "Two bridges, one pair"** — figure far too small. Highlight **"Both count"**.
- **014 "An edge to itself"** — figure far too small.
- **016 "Degree"** — "k = 4" still hard to read; raise it as far as it goes.
- **021 "A graph with such a walk has at most two odd nodes"** — the formula overflows its
  tinted box and overlaps the figure. Also: **restructure from two columns into two rows.**
  His reasoning is that the figure and its text do not both fit across; stacking them gives
  the figure the full width and the text its own line.
- **051 "Total degree is the wrong quantity"** — the figure is visibly low-resolution.
- **063 "Multiply A by itself"** — he likes this question. Make it stronger: **have students
  work one concrete entry first**, then, once they see what $A^2$ is, **ask them to predict
  $A^3$ and $A^4$.**
- **067 "Store only the nonzeros"** — he likes the figure. **Swap two rows: `data` should be
  the third row, `indices` the second.**
- **069 "The payoff: memory"** — an arc and the numbers overlap.
- **070 "Which format when?"** — the figure's text and the matrix border are not aligned;
  check the placement.
- **078 "Back to Königsberg"** — the numbers are not readable. Bigger. Same for the other
  figures.

## Part Seven should be interactive

Of the Representation part he said: the figures are well composed, but this material would be
clearer as **animation or interactive visualisation** — a button to press, a slider to step
through the ordering structure.

The route animations on Walk / Trail / Path are now wired in and prove GIF works: Marp's HTML
sanitiser strips inline `<svg>`, and an `<img>` pointing at an `.svg` renders blank inside
Marp's own `foreignObject`, but a GIF referenced by relative path animates normally.

So an animated build of the edge-list → adjacency-list → matrix → CSR construction is
reachable now. A slider needs scripting, which Marp restricts — treat that as a follow-up and
report what the render supports rather than assuming.

## Verify

    python3 figures/make_figures.py
    python3 figures/make_animations.py
    marp m01-euler-tour.md --theme network-science.css --allow-local-files \
         --images png -o review/slide.png
    python3 check_render.py        # must exit 0

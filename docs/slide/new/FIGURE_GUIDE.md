# Figure authoring guide

Standards for figures in this course's lecture decks. Written to be executable by **any**
agent, like `SLIDE_RUBRIC.md` — it uses only tool names and file paths.

This exists because rebuilding one Module 01 deck took eight review rounds, and roughly a
third of every round's findings were figure defects that the authoring setup made possible.
The rules below are what those rounds cost.

## Tool choice

**Do not reach for matplotlib.** It was used for Module 01 and it is the wrong default here:
it models a *plot*, not a diagram, so node radius, edge endpoints and text size are all
things you compute rather than declare.

| what you are drawing | use |
|---|---|
| node-link diagrams (graphs, networks, anything with nodes and edges) | **TikZ** |
| data figures (distributions, relationships, matrices) | **Altair**, or **seaborn** |
| anything else | the simplest thing that renders it |

This repo already has a Quarto TikZ pipeline at
`docs/lecture-note/_extensions/danmackinlay/tikz/`, so TikZ is not a new dependency.

**Why TikZ for graphs.** The defect class that consumed six of the eight rounds — self-loop
legs that did not meet their node, arrowheads that stopped short, rings drawn inside the disc
they were meant to encircle — cannot be written in TikZ. `\draw (A) -- (B);` stops at the
node's border, whatever the shape. `edge[loop above]` is a self-loop primitive.
`node[above right=2pt of A]` positions against a real anchor rather than a guessed
coordinate. You do not compute boundaries, so you cannot get them wrong.

## Rules

### Author at final size

**The single most expensive mistake in Module 01.** Figures were authored in inches and
points, then scaled to the slide by a per-slide `w:` directive the generator never saw. So
in-figure text landed anywhere from 7px to 40px on the slide, and ten of twelve figures in
one range rendered their labels smaller than the page number.

Author so that **one unit is one slide pixel**. Then a 20pt label is 20px on the slide, in
every figure, and there is nothing to reconcile. In TikZ, fix the `tikzpicture` width to the
column width it will occupy. In Altair, set `width`/`height` to the final pixel size.

The same rule fixes node size: Module 01's nodes were uniform in *figure* space and still
ranged 68–177px on the slide.

### Measured floors (from the m01 rounds — assert these in the generator)

The deck's containers are fixed: content area **1120px**, a `cols` column **537px**,
display height cap **380px**. So the on-slide size of anything in a figure is computable
at authoring time:

    scale       = min(container / src_w, 380 / src_h, 1.0)
    on_slide_px = size_pt * (dpi / 72) * scale

- **In-figure text ≥ 15px x-height on the slide** (body is 30px type ≈ 15px x-height). The
  lecturer raised this four times on m01; it is a build failure now, not a taste note.
- **Assert the x-height, not the cap height.** `check_render.py` measures x-height on the
  rendered slide; asserting cap height in the generator measures a different quantity, and
  for Latin Modern the two disagree by 60% (x-height 0.431 em, cap height 0.683 em). Module
  03 shipped 30pt labels that passed a 21px cap-height assertion and landed **13px**
  x-height on forty slides at once — under the floor, and invisible to the build until the
  checker ran. The generator must assert exactly what the checker reads:

      x_height_px = size_pt * XHEIGHT_RATIO * (dpi / 72) * scale   # >= 15.5

  With the m02/m03 pipeline (1 bp = 1 slide px) that puts the floor at **36pt**, not 30pt.
- **And assert that the text still fits.** Size and containment are two checks, not one.
  Raising m01's type until the size assertion went green pushed digits out of their matrix
  cells: the dense inset became a mass of overlapping glyphs and `indptr` rendered "10" and
  "12" as a single "1012", on the slide that teaches what those boundaries mean. That is
  worse than the small type it replaced, because small text gets skipped and garbled text
  gets misread. Where a cell cannot hold text at the floor, **the cell grows** — never
  shrink the type back.
- **Node discs 26–52px on the slide** — uniform enough that the same graph does not
  change size between consecutive slides.
- **Drawing ≥ 150px rendered**, **per-axis margin ≤ 30%**, ink fraction ≥ 15% of the box
  (aim for 35%) — below that the deck is scaling white margin, not the picture.

`m01/check_render.py` re-measures all of this on the rendered slides after `marp
--images png`; copy it into each new module and keep it exiting 0.

### No bar charts

Use a form that shows the quantity directly — the actual objects, a dot plot, a slope, an
annotated number. Bars encode one number as a length and then need a scale to decode it,
which is where Module 01's memory-comparison figure went wrong: it drew a 7:1 ratio under a
label reading 7,700:1.

### No green

The palette is `#3959A6` (accent), `#B14434` (accent-2), `#DAB167` (accent-3), `#6b6b6b`
(annotation gray), `#000000` (ink). Nothing else.

### One colour, one meaning, per figure — and say what it means

In Module 01 accent-2 meant, across four consecutive slides: the leftover edge, the start
and end nodes, every edge, the odd-degree nodes, and a node that was even. Pick one meaning
per figure and state it in the figcaption or an in-drawing label.

### Keep it simple

If a figure needs a legend to be read, it is doing too much. One figure, one point. A
multi-panel figure is acceptable only as a build — one panel per step.

### Never share a figure between slides that explain it differently

Module 01's multigraph figure gained an adjacency matrix for a Part Seven slide, and the
same file was already on a Part Two slide — so students met a matrix with unexplained blue
and red cells 41 slides before the matrix was defined. If two slides need different content,
emit two files.

## Place labels with a solver, not by hand

Module 03's working graph has two towns 17 km apart on a 151 km map, and eight names between
four and nine characters long. Hand-assigning a side per label cost an afternoon and still
produced collisions; worse, the hand-written check exempted a label's own node, which hid a
real bug — the TikZ anchor and the offset had been paired backwards, so half the candidate
positions sat **on top of** the disc they belonged to.

Write a backtracking placement solver instead. For each label try the eight sides in order
and reject a position that hits: another label, **any** disc (including its own), an edge
that matters, an edge-weight chip, or the canvas bounds. Do the same for the numbers printed
on edges — chips left at the plain midpoint collided wherever two edges met at a node. Solve
names first, then chips against the names.

When no assignment exists, **say so and stop**. Do not let the type shrink to make room:

    raise SystemExit("label placement failed — no collision-free side assignment exists.\n"
                     "Move a node, shorten a name, or widen the canvas; do not shrink the type.")

A useful corollary: give the solver a vertical band, not the whole canvas. The cropped
drawing has a hard height budget (`container_w * 380 / container_px`), and a label the solver
placed 40bp higher than expected is what pushes a figure over it.

## Square figures cannot pass both gates in a column

The width floor (ink ≥ 76% of the canvas) and the height cap fight each other: in a 520bp
`cols` column a circle wide enough for the first is too tall for the second. Draw ring-shaped
figures as a **wide ellipse**, and rotate the layout so two nodes sit at the horizontal
extremes — a hexagon started at 90° is only 87% as wide as its own bounding circle, which
was the difference between 67% and 83% ink span.

## Assertions

Whatever the tool: **assert the facts the figure draws, and let the build fail.** This was
the most effective thing in the whole rebuild — more effective than any library choice.
Assertions caught, each of them before a human ever looked:

- four rings drawn *inside* the node they were meant to encircle
- an arrowhead standoff that was calibrated at the wrong linewidth (the gap scales with the
  arrow's own stroke width, ~1.12pt per 1pt — it is not a constant)
- a traversal figure whose numbered visit order jumped between non-adjacent nodes
- a ring-lattice whose second-neighbour chords passed 0.005 units inside the discs they
  crossed, hiding every triangle on a slide claiming high clustering

**Round percentages in decimal, not in binary.** A measured 0.575 is 57.49999999999999 as
a float, so `f"{x*100:.0f}"` prints 57 while the deck's prose says 58 — one slide, two
numbers, and the figure was regenerated twice before anyone looked at the float. Format
through `Decimal(repr(x)) * 100` with `ROUND_HALF_UP`; `repr` is the shortest string that
round-trips, so the multiply happens in decimal.

Assert the arithmetic too. Compute every number a figure prints from the data, never
hardcode it. Module 01 shipped a figure claiming CSR stored 12 numbers against a dense 25
when CSR actually needs 30 — it counted one of three arrays.

### Measure the render. Never compute what you can measure.

Module 02's generator asserted in-figure text size as `FONT * CAP_RATIO * scale` — three
numbers it already knew — and passed on every figure while the whole deck shipped 17% under
the floor. Stock Computer Modern has no 30pt design size, so LaTeX had silently substituted
24.88pt:

    LaTeX Font Warning: Font shape `OT1/cmr/m/n' in size <30> not available
    (Font) size <24.88> substituted

A computed assertion can only restate the author's intention. Compile one calibration glyph
at the size you asked for, **measure its ink**, and assert against that. The same rule
retires `CAP_RATIO` as a constant: derive it per build.

(The fix for this particular trap is `\usepackage{lmodern}`, and failing the build when
`pdflatex`'s log contains `not available`.)

### Ink drawn outside the canvas does not exist

A canvas-edge check catches ink *touching* the border and says nothing about ink entirely
beyond it, which simply never renders. Module 02 lost an axis title placed at `y = -2` that
way. Assert the coordinates, not the pixels: the generator wrote those numbers, so check
`0 <= x <= w` and `0 <= y <= h` for every one of them.

### accent-3 is for fills and rings — never text, never a thin stroke

Gold on white measures **2.01:1** contrast where accent-2 on the same figure measures 5.53:1;
the floor for large text is 3:1. A gold label is invisible from the back row and a gold 2bp
stroke is nearly as bad. Use it for shaded bands and highlight rings, where area carries it.

### Assert the crossing count on any figure whose claim is a triangle

A ring lattice with every skip chord bowed the same way crosses its neighbours at every node
— sixteen crossings on the slide asserting "triangles are everywhere", with each triangle
reading as a lens. The graph was planar and `nx.check_planarity` says so. Count the
intersections between drawn paths and assert zero wherever a planar drawing exists.

### The figure and the deck must agree on the container

A figure authored for the 1120px content area and then dropped into a 537px `cols` column
renders at **48%** of its intended scale — 19px node discs on a slide whose twin, laid out
full width, shows 39px. Nothing in the source looks wrong. Compute both numbers and compare
them in the build gate.

## Traps found the hard way

- **matplotlib `scatter` marker size is in points²**, so the node's radius *in data
  coordinates* scales with the axes limits. The same `s=900` gives 0.0672, 0.1344 or 0.2688
  depending on `xlim`. Every edge and annotation endpoint computed from a guess. If you must
  use matplotlib, draw nodes as `Circle` patches with a radius in data units.
- **The default backend reports `fig.dpi = 400` on a Retina Mac**, so figures saved through a
  path that defaults to `fig.dpi` render at 2× on that machine only. Force `matplotlib.use("Agg")`.
- **Marp strips `style` attributes** from HTML in the deck, so inline CSS in a slide silently
  does nothing. Put it in the theme.
- **KaTeX does not process `<figcaption>`** — math there renders as literal `$…$`.

## Review

Figures are reviewed on the **rendered slide**, never on the source or the standalone PNG.
`SLIDE_RUBRIC.md` has the procedure. Measure rather than eyeball: over eight rounds, every
single round contained at least one repair reported as landed that the rendered image
contradicted.

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
`lecture-note/_extensions/danmackinlay/tikz/`, so TikZ is not a new dependency.

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

### No green, and only two hues

The palette is the lecture note's, so that a figure and the page or slide around it are
made of the same colours: `#593196` (accent, purple), `#c2410c` (contrast, red), `#76757c`
(annotation grey), `#22212b` (ink). Nothing else.

Where a drawing genuinely needs a third value — two routes over one graph, a highlighted
slice beside a highlighted row — take another **value of one of those two hues**, not a
third hue: `#7a51c0` is the lighter purple, `#e0a184` the lighter red. A fill that sits
under ink needs a wash rather than a mid tone (`#e4d8f6`): ink on `#7a51c0` measures 2.9:1,
under every legibility floor this repo holds elsewhere.

Modules 02 to 06 still draw with the old `#3959A6` / `#B14434` / `#DAB167` set. Restyle a
module's generator and its deck theme in one commit, or its figures and its slide chrome
will disagree; `check_render.py` takes the deck's own palette through `colour_words`, so a
figcaption that names a colour is checked against what the figure actually contains.

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

## Gate every drawn box against every other, not just the names

Module 04's round 2 found seven new figure defects and six of them were one thing: **an
in-figure text box drawn where something else already is.** Annotation over annotation on
three panels of one build; five separate overlaps on a single derivation figure; a node count
struck through by its own x-axis rule; a legend line crossed by the curve it names. Every one
was a box that grew, or an axis that moved, after somebody chose the position by hand.

The label solver already existed and only names went through it. So the gate now runs on every
figure: collect every drawn text box — including tick labels and axis titles — every rule, and
the sampled curves, and fail the build if any text box intersects any of them. Its first run
failed **thirteen figures across three batches**, including four made that evening that no
reviewer had seen, and it independently rediscovered the two collisions round 2 had measured by
hand on the render. Fixing at the generator is worth a round; fixing seven of them one at a
time is worth nothing, because the eighth is already being drawn.

The failure message must say **shorten the note or move the panel, and never shrink the type**.
Both of the times this deck's type quietly got smaller to make room, a reviewer found it before
anyone noticed the drawing had changed.

### But size the boxes from glyphs, not from source characters

`label_box` estimates a label's width as `CHAR_W * size * len(string)`, and that estimate is
wrong in two compounding directions. It counts **source** characters, so `$\langle k^2\rangle$`
models as a 408bp box around an 85bp glyph. And `CHAR_W` is 0.55 em against a measured 0.43.

Both errors are conservative for a collision test, which is why they survived — but conservative
is not free:

- The gate refuses layouts that are fine, and the author moves a drawing that was never wrong.
- **An arrow that terminates at a label cannot be drawn at all.** The arrowhead is inside the
  modelled box by construction, and stopping outside it leaves a ~160bp gap. Module 04 got out
  of this by routing the flow *past* the label rather than into it — which turned out to be a
  better figure — but it is a dodge, and the next labelled flow will hit the same wall.

The fix is the one this guide already prescribes two sections down for type size: **measure the
compiled string** the way `calibrate()` measures x-height. The collision gate is a computed
assertion — three numbers the author already knew — and "a computed assertion can only restate
the author's intention" is not a new rule, it is this one not yet applied to the newest gate.

**Do not take the obvious middle path.** Stripping the TeX markup and dropping `CHAR_W` to the
measured 0.43 looks like the cheap version of the same idea. Measured, it is worse than the bug:

    $\langle k^2\rangle$   today, 0.55 em x 20 source chars : 408.0 bp   4.8x OVER
                           strip markup, 0.43 em x 3 chars  :  58.4 bp    31% UNDER
                           measured ink                      :  85.0 bp

Plain text is fine under either scheme; the whole error lives in math and escapes, and naive
stripping turns `k^2` into two characters where it renders as a letter plus a raised digit. So
today's estimate is wrong in the **safe** direction — it refuses good layouts, which is annoying
and visible — and the cheap fix makes it wrong in the direction the gate exists to prevent: a
missed collision, invisible until a reviewer finds it two rounds later.

Two notes for whoever implements it. The measurement is a pure function of (string, size, font)
and never changes between builds, so a JSON cache keyed by a hash means the first build pays for
pdflatex and no later build does. And an ink box is *tighter* than a typographic box, so two
labels 2bp apart would pass — add a small explicit pad, but pad a measured box, not a guessed
one, or the two errors compound.

**Resist the escape hatch.** The tempting alternative is a "label anchor" primitive that arrows
are allowed to reach. It fixes one symptom, leaves the over-estimate that costs real content
elsewhere, and — once authors know a way to tell the gate an object is legal — it will silence
true positives as readily as false ones. The gate's whole value is that it fires without the
author thinking about it.

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

## Assert that the drawing is on the page

The page is fixed to the design canvas, so anything drawn past its edge is **clipped**,
silently, and the crop step cannot tell you — it only removes whitespace. Four reviewer
Blockers on Module 03 were one missing assertion: "any cut" sliced through the middle of
its glyphs, `= 2: the birth of the giant compone` losing both ends, and two figures whose
right-hand nodes rendered as half-discs.

    ys, xs = np.where(gray < 200)
    assert not (xs.min() <= 2 or xs.max() >= W - 3
                or ys.min() <= 2 or ys.max() >= H - 3), "ink runs off the page"

Ink touching an edge is a clip, not a crop. The same run caught two more figures nobody
had reported.

**And assert that in-figure notes clear the labels.** A note is placed at a fixed corner
while names are placed by the solver, so a note that grows collides with whatever the
solver put there — "every town is its own island" was drawn straight through the word
"Znojmo". Compute the note's box and check it against every label box; the failure message
should say *shorten it*, because a long note is the bug (notes carry numbers, prose lives
in the figcaption).

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

### Assert a drawn object against its data, never against itself

Module 02's small-world band was drawn from two constants and guarded by
`assert log10(BAND_HI / BAND_LO) >= 2.0` — an assertion that a rectangle is as wide as the
two numbers that define it. It passed on every build while the band's left edge sat in a
regime where the deck's own measured sweep says routes are only 22% shorter, i.e. where the
claimed property does not hold at all.

Worse is how it got there: the slide claimed "two orders of magnitude", the drawn band was
1.39 decades, and the fix chosen was to widen the band. **That makes the figure fit the
sentence.** Derive the object from the data under a criterion written down in the code,
assert the derived value, print the criterion on the slide, and let the prose say whatever
comes out. Under three defensible criteria that band is 0.33, 0.67 or 1.33 decades — never
the number the sentence wanted.

This is the same failure as picking a flattering random seed, one level up. Both choose the
evidence.

### A tripwire must not encode the conclusion

Having derived that band from the data, the generator then grew a guard against the number
going stale:

    assert BAND_DECADES >= 1.0, "under one decade the deck cannot say ..."

The intent was right and the threshold was picked *after* seeing the answer come out at
1.18. An assertion cannot say "rewrite the sentence"; it can only fail the build. So if a
better sweep had put the honest band at 0.9 decades, the build would have broken and the
cheapest way to make it pass would have been to move the criterion until the number was a
decade again — the same disease as widening the band, with the sign flipped: *assert that
the data must permit the sentence.*

Pin the tripwire to the value the prose was actually written to, so it fires on movement in
**either** direction and names the prose as the thing to update:

    # slide 76's sentence is written to this number. If the sweep, the criterion or the
    # edge rule changes, this fires -- update the sentence and this constant together.
    # Do NOT satisfy it by moving the band.
    DECK_BAND_DECADES = 1.18
    assert abs(BAND_DECADES - DECK_BAND_DECADES) < 0.05, ...

That version cannot be satisfied by moving the drawing. Worth knowing that this defect
arrived inside a safeguard written against the very defect it reproduced, and that it was a
reviewer who spotted it, not the author.

### When two readings of the same data disagree, suspect the sampling

The same band could be read two ways — snap the edges to the sampled points (0.67 decades)
or solve the drawn polyline for its threshold crossings (1.18 decades). Both readings were
argued well and they differ by a factor of three. Neither was the answer: the sweep was 13
points over four decades, one per third of a decade, and the whole disagreement was an
artefact of that spacing. Resampling finely enough that the two readings converge dissolves
the question instead of adjudicating it.

The tell is that the argument is about *how to read* the data rather than about what the
data says.

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

### Assert that two discs in one figure do not overlap

Every gate in the build measures **one thing at a time** — this disc's size, that label's
x-height, the ink span of the whole canvas. Overlap is not a property of any one disc, so
none of them can see it. Module 05's "draw two balls" figure scattered fourteen discs with
`rng.uniform` and five of them merged into three blobs on the rendered slide, under a green
run.

    _DISC_RE.findall(body)  ->  [(size, x, y), ...]
    for each pair: assert hypot(dx, dy) >= (si + sj) / 2 + 1

Wired into `emit()`, it fired on the first run against a figure nobody had complained
about: two stacked five-cliques whose facing members sat 20bp apart with 32bp discs. Graph
figures already get this from `clearance_bad`; this catches the free-floating ones, which
are exactly the figures nobody thinks to check.

### A GIF's first frame is what the static export shows

Marp renders frame one into the PNG and PDF exports, so that frame is what the printed
handout and the slide-review render contain — the animation only exists in the browser.
Module 05's k-core peel led with the 1-core, which is the untouched network: in the export
that slide repeated an earlier figure and taught nothing. **Lead with the frame that
carries the claim** (here the 4-core it settles on), then let the loop replay the
derivation.

### Labels on an axis need a solver too, not just labels on nodes

`place_labels` was written for node names and the lesson stopped there. Module 05's number
lines put every mark label at a fixed offset from its own tick, and two marks half a unit
apart printed straight through each other — "the rule of thumbthe real split" on one slide,
"the real split" over "Louvain" on another. Both were invisible in the source and both
passed the gate. Any label whose position is computed from a *data value* can collide with
another one; walk it outward row by row and fail the build when no row is free.

### ### Ink drawn outside the canvas does not exist

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

**And the container is not one number — read the theme, then read the deck.** Module 02
assumed two factors (col and full width) and the theme applies at least four. Two separate
caps were missed:

- Marp wraps a figure in a `<p>`, so `section p { max-width: 1080px }` binds before the
  1120px content area. Full width is **1080**, not 1120.
- The `.fig` modifiers change the height cap — `.fig.tight` to 320px, `.fig.stack` to 190px
  — and on a wide figure the **height** binds first, dropping the factor from 0.98 to 0.87.
  Sixteen slides of m02 shipped 13–14px type against a 15px floor that way, and the gate
  passed them because it used 380 for everything.

So the scale is `min(width_cap / file_w, height_cap / file_h)` where both caps come from the
class the **deck's markup** actually applies. Parse the deck for it. A generator's own table
of intended containers is not evidence: in m02 the table and the deck disagreed twice.

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

## When the label solver says no, the drawing is the thing that has to move

Module 06's working graph is twelve Roman cities with names like "Thessalonica",
and on a true longitude/latitude projection `place_labels` cannot place them at
all — three cities have **zero** collision-free sides before any other label
exists, because the projection puts Tarraco, Lugdunum, Massilia and Colonia inside
170 bp of width and each of them needs a ~170 bp label. Annealing the node
positions did not help while the projection was held fixed, and neither did
splitting the long names across two lines.

Three things fixed it, in this order, and the order matters:

1. **Make the layout schematic, and hold it to the geography with a statistic
   rather than with a projection.** The final coordinates come from an annealing
   search whose *hard* constraints are planarity, disc clearance and
   label-solvability, and whose objective is Spearman correlation against the true
   coordinates. Longitude order came out exactly preserved and latitude at
   rho = 0.95, so the lecturer can still point at it and say "the Mediterranean".
   Assert both correlations in the module; a layout edit that scrambles the map is
   then a build failure rather than a thing nobody notices.
2. **Give the figure the height it needs, measured.** The plain `.fig` cap of
   380 px leaves 356 bp of ink and there is no solution at 356 or at 376; at 396
   every name fits on one of the four *nearest* sides of its own disc. That is why
   the theme has a `.fig.tall` modifier — added at 400 px after rendering a probe
   slide and measuring where the ink actually ended, not guessed.
3. **Restrict the solver to the near sides.** A label 46 bp from its disc, with
   another disc closer to it, does not read as that city's name. Solving with only
   the four nearest offsets and failing otherwise is better than a solution nobody
   can parse.

### A halo, not a chip

Once labels are allowed to lie across edges — and with eighteen edges among twelve
nodes they must be — the question is what to draw under the text. A white **chip**
(a filled rectangle behind the label) was built first and produced a map whose
roads were chopped into pieces: Londinium's road to Colonia simply stopped, and
the reviewer's eye read the gap as a missing edge. A white **halo** (the text
drawn eight times in white at ±2 bp, then once in black) lets the road show
through between the letters, which is what an atlas does.

The halo does leave short black stubs where a road enters and leaves a word, and
`check_render.py`'s `smallest_text` heuristic reports those as 1 px "text". Expect
the warning on every haloed figure; it is the heuristic being fooled, and the
generator's measured assertion is the gate that matters. Reduce the stubs by
having the solver **hill-climb its own answer for the fewest edge crossings** —
the first feasible assignment is rarely the tidiest, and re-picking each label's
side to minimise crossings is a dozen lines.

## A highlight ring around a node breaks the node-size gate

`check_render.py` finds discs by masking the node fill colours and then filling
holes, so a disc drawn *inside* an accent-2 ring is one solid blob to it. Module
06 marked its crowned city with a ring 13 bp larger than the disc and failed the
26–52 px band on ten slides at once, at a measured 57 px, while every disc in the
figure was drawn at 40.

Mark a node with a **heavy border on the disc itself** (5 bp) plus a glyph outside
it. The border adds its own width and nothing else, the glyph is the wrong shape
to be counted as a disc, and the measurement then matches what was drawn. A ring
in accent-3 is also safe, because gold is not one of the fills the gate masks —
but do not rely on that without checking `NODE_FILLS`.

## An in-drawing note needs somewhere to go, and a full map has nowhere

`note()` should try several anchors and fail loudly when none is clear, rather
than being pinned to a corner. On Module 06's map — twelve labelled discs spanning
92% of the canvas — the honest answer was that *no* corner is free, and the notes
came off the figures entirely: the numbers moved into the slide's body text and
the encoding into the figcaption, which is where FIGURE_GUIDE said prose belonged
all along. A gate that says "this does not fit anywhere" is telling you the figure
is full, not that the gate is too strict.

## Review

Figures are reviewed on the **rendered slide**, never on the source or the standalone PNG.
`SLIDE_RUBRIC.md` has the procedure. Measure rather than eyeball: over eight rounds, every
single round contained at least one repair reported as landed that the rendered image
contradicted.

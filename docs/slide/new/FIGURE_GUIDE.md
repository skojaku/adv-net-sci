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

Assert the arithmetic too. Compute every number a figure prints from the data, never
hardcode it. Module 01 shipped a figure claiming CSR stored 12 numbers against a dense 25
when CSR actually needs 30 — it counted one of three arrays.

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

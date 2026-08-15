# Round-8, part 1 — replace scatter nodes with Circle patches

This is a refactor, not a patch. It removes the cause of a defect class that has failed
**six consecutive rounds** under three different-looking symptoms.

## The root cause, measured

Nodes are drawn with `ax.scatter`, whose marker size is in **points²** — a screen unit,
decoupled from data coordinates. So the node's radius *in the coordinate system the edges
and annotations are computed in* depends on the axes limits. Measured directly:

    same scatter, s=900, figsize 4x4:
      xlim (0,1)  ->  radius in data units = 0.0672
      xlim (0,2)  ->  radius in data units = 0.1344      (2x)
      xlim (0,4)  ->  radius in data units = 0.2688      (4x)

    Circle(radius=0.08):
      xlim (0,1) / (0,2) / (0,4)  ->  0.0800 every time

Every figure in this deck has its own xlim. So every time a stroke needs to meet a node
boundary — an edge, an arrowhead, a self-loop leg, a ring meant to enclose a node, a leader
meant to stop short of one — the code has to *guess* the radius, and the guess is wrong by a
different factor in every figure. That is why the same symptom kept coming back with a
different explanation each round:

| round | symptom | "cause" found | what it really was |
|---|---|---|---|
| 3–5 | self-loop legs float | stale radius constant, 3× off | a guess |
| 6 | legs float | `FancyArrowPatch` default `shrinkA/B=2pt` | a second guess on top |
| 7 | legs float, now *outside* | annotation assertion applied to an edge | a third guess |

Same for the arrowheads that would not arrive, the rings drawn *inside* the disc they were
meant to encircle, and the node diameters ranging 9px to 148px across the deck with nothing
encoded.

## What to build

### 1. One canonical radius, in data units

Define a single module-level `NODE_R` in **data coordinates** and draw every node as
`matplotlib.patches.Circle(center, NODE_R, ...)`. Delete `node_s()`, `node_radius_data()`
and every other function that estimates, measures or scales a marker size — they exist only
to paper over the scatter problem and each one is a place the guess can go wrong again.

### 2. One on-slide node diameter, deck-wide

With the radius exact, the remaining variable is how many data units the figure spans. Fix
the *rendered* node diameter once for the whole deck and derive each figure's `figsize` from
its data range:

    figsize_inches = (data_width / NODE_R) * (target_node_diameter_inches / 2)

so a node is the same physical size on every slide. This closes the outstanding item that
the lone node on the single-node slide is 263px across — 37% of slide height — under a
caption reading "the smallest possible graph", while a node on the small-world teaser is
9px. Pick the target from the figures that already look right (the Königsberg graphs).

Assert it: after generating, every figure's node diameter in output pixels, divided by that
figure's downscale factor to its rendered column width, must land within a few percent of
the same number.

### 3. Every boundary computation becomes exact

With `NODE_R` known:

- **Edges** terminate at distance `NODE_R` from each endpoint centre. No `shrink`, no
  `min_target_margin`, no per-figure tuning.
- **Arrowheads** inset by exactly `NODE_R` plus the head length. They will arrive, on every
  figure, without a hand-picked standoff.
- **Self-loop legs** terminate *on* the rim: the two attachment points are
  `center + NODE_R * (cos θ, sin θ)` for the two chosen angles. Nothing to guess. Assert the
  endpoints are within a small epsilon of `NODE_R` from the centre.
- **Rings** that enclose a node are drawn at `k * NODE_R` with `k > 1` — assert it, so a ring
  can never again be drawn smaller than the disc it encircles.
- **Annotation clearance** checks compare against `NODE_R` directly.

### 4. Fix the assertion over-application from round 7

Round 7's `draw_annotation_stroke()` asserts a stroke "must not terminate on or inside a node
disc". That is correct for leaders and brackets and **wrong for edges and self-loops**, which
must terminate exactly on the rim. Applying it to the self-loop is what pushed the legs
7–10px outside the node — two independent verifiers measured this on the current render.

Split the two cases explicitly:

- `draw_edge()` / `draw_selfloop()` — assert the endpoint **is on** the rim (within epsilon).
- `draw_annotation_stroke()` — assert the endpoint is **outside** the rim by a clearance
  margin, and does not cross a live edge.

Never route an edge through the annotation helper or vice versa.

## Scope

29 `ax.scatter` call sites across 52 figure functions. Mechanical, but it touches nearly
every figure, so:

- Do it in one pass, then regenerate everything and **open every PNG with the Read tool**.
  Do not report done on a subset.
- Report the node diameter (in output px and in on-slide px) for every figure, so the
  deck-wide consistency claim is checkable.
- The self-loop appears on three slides from one shared file — verify it there specifically.

## Do not change in this pass

Content, captions, colours, layouts, which figure a slide uses. Only the node/edge/annotation
geometry and the sizing that follows from it. Other findings from the round-7 verification are
a separate list.

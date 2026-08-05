# Figure spec — Module 01 rebuild

Rewrite `figures/make_figures.py` so that `python figures/make_figures.py` emits
**every** file below. Then run it and confirm each PNG exists and is non-trivial.

## Global rules (these are the review findings — obey them everywhere)

1. **No unexplained encoding (F1).** Every node is the **same size** unless the slide
   states what size means. Every node is the **same fill** unless the slide states what
   the color means. Never use a color for decoration.
   - Default node fill: `INK` (#000000), labels white.
   - `ACCENT2` (#B14434) is reserved for **one** meaning across the whole deck:
     *the thing under discussion* — an odd-degree node, a traced route, a removed edge.
     Never spend it on decoration.
   - `ACCENT3` (#DAB167) is reserved for CSR array highlighting only.
2. **No avoidable crossings (F2).** Every graph here is planar. Draw it planar.
   For the Königsberg multigraph use exactly this layout — it is crossing-free:
   `N = (0, 1.0)`, `S = (0, -1.0)`, `A = (-1.0, 0)`, `B = (1.0, 0)`.
   Bow the two N–A edges with `rad = ±0.30` and the two S–A edges with `rad = ±0.30`.
   Draw N–B and S–B **straight**. Draw A–B straight. Nothing crosses.
3. **Legible from the back row (F3).** Minimum sizes, at the dpi below:
   - edges: `width=3.5`, color `MUTED` (#6b6b6b) or `INK` — **never** the old pale
     `EDGE = #c8c1ba`. Delete that token.
   - node labels: `font_size=18`
   - in-figure titles / captions: `fontsize=18`
   - annotation text: `fontsize=17`
   - arrowheads (directed only): `arrowsize=40`, `min_target_margin=22` so the head is
     never occluded by the node disc.
4. **One figure, one point (F4).** Prefer separate single-panel files over a multi-panel
   figure. Where two panels are genuinely a comparison, keep them but give each its own
   title at `fontsize=18`.
5. **Palette (F5).** Only `ACCENT #3959A6`, `ACCENT2 #B14434`, `ACCENT3 #DAB167`,
   `INK #000000`, `MUTED #6b6b6b`, `PANEL #f7f4f1`, `RULE #dddddd`.
6. Keep `save()` at `dpi=200`, `bbox_inches="tight"`, `pad_inches=0.15`.
   **Crop tight** — no large empty regions (this caused slide 019 to overflow the frame).
7. Node discs must never overlap each other.

## Files to produce

### Part 1 — the puzzle
- **`konigsberg-sketch.png`** — a bare tracing sketch for the student worksheet: four
  identical light-gray rounded landmass shapes (same size, non-overlapping) laid out
  N-top / S-bottom / A-left-center / B-right, with the **seven** bridges as thick `INK`
  strokes, each visibly anchored on the boundary of two distinct shapes. No labels
  beyond N/S/A/B. Nothing colored — students draw on it.

### Part 2 — abstraction (3-step build, same layout throughout)
Three files that are the **same picture at three stages**, identical positions and canvas
limits so the build morphs in place:
- **`abstraction-1-map.png`** — four identical light-gray landmass ellipses (same width,
  same height, non-overlapping) + all **seven** bridges as `INK` strokes anchored on two
  shapes each. Title: `the city`.
- **`abstraction-2-nodes.png`** — same seven strokes, but each landmass replaced by one
  `INK` disc of identical size, labelled N/S/A/B in white at `font_size=18`.
  Title: `each landmass → one node`.
- **`abstraction-3-graph.png`** — the clean planar multigraph per rule 2, edges `MUTED`
  at `width=3.5`, nodes `INK` identical size, labels white 18pt.
  Title: `each bridge → one edge`.

- **`multigraph.png`** — exactly two `INK` nodes side by side with **two** parallel arcs
  between them (`rad = ±0.30`). Annotation under it in `MUTED`: `two bridges, two edges`.
- **`selfloop.png`** — one `INK` node with a single loop attached. Annotation in `MUTED`:
  `both ends attach here`.

### Part 3 — degree and parity
- **`degree-definition.png`** — one central `INK` node with 4 edges to 4 other `INK`
  nodes, **all discs the same size**. The central node's degree printed *inside* it in
  white. Annotation: `k = 4`.
- **`parity-even.png`** — a degree-4 node, all discs the same size, all `INK`. The four
  edges bracketed into **two visually matched pairs**: draw a thin `MUTED` arc connecting
  each pair near the hub and label the pairs `in–out` and `in–out`. Title:
  `even: every edge finds a partner`.
- **`parity-odd.png`** — a degree-3 node, same node size and style. Two edges bracketed as
  one `in–out` pair in `MUTED`; the **third edge drawn in `ACCENT2` at width 4.5** and
  labelled `left over` in `ACCENT2`. Title: `odd: one edge left over`.
- **`konigsberg-blank.png`** — the planar Königsberg multigraph (rule 2 layout), all nodes
  `INK`, **no degree numbers** — for the "count them yourself" activity.
- **`konigsberg-degrees.png`** — same layout and same node positions, but each node
  filled `ACCENT2` with its **degree printed inside the disc in white** (N=3, S=3, A=5,
  B=3). No floating `deg n` labels anywhere — they overprinted the caption in the old
  figure. One annotation line beneath, in `ACCENT2` at `fontsize=18`:
  `all four odd`.
- **`euler-path-example.png`** — a small connected graph with **exactly two** odd-degree
  nodes; the Eulerian trail drawn over it in `ACCENT2` at `width=4.5`, and the two odd
  nodes filled `ACCENT2` and labelled `start` / `end` in `ACCENT2`. All other nodes `INK`,
  same size. Planar, no crossings.
- **`euler-circuit-example.png`** — a small connected graph where **every** node has even
  degree; a closed Eulerian circuit traced in `ACCENT2` at `width=4.5`, with one node
  labelled `start = end`. Planar, no crossings.
- **`konigsberg-bombed.png`** — same layout and positions as `konigsberg-degrees.png`, but
  the two destroyed bridges drawn as thin dashed `RULE`-colored lines (visibly removed) and
  the five surviving bridges solid `MUTED`. Degrees printed inside the discs: the two
  **odd** nodes filled `ACCENT2`, the two **even** nodes filled `INK`. Annotation beneath
  in `ACCENT2`: `two odd → now possible`.

### Part 4 — vocabulary
One base graph, four renderings, **identical positions in all four**. Four nodes at the
corners of a square with one diagonal: `Dorm (0,1)`, `Cafe (1,1)`, `Lib (1,0)`, `Gym (0,0)`;
edges Dorm–Cafe, Cafe–Lib, Lib–Gym, Gym–Dorm, Cafe–Gym. All nodes `INK`, **identical size,
identical fill** (the old four-color version was an F1 Blocker). Labels white 18pt — use
the short forms above so they fit inside the discs.
- **`campus-base.png`** — no route drawn.
- **`campus-walk.png`** — a route in `ACCENT2` that repeats **both** a node and an edge;
  mark the reused edge with a small `ACCENT2` `×2` label. Title: `walk: anything may repeat`.
- **`campus-trail.png`** — a route in `ACCENT2` that repeats a **node** but no edge; circle
  the revisited node in `ACCENT2`. Title: `trail: no edge twice`.
- **`campus-path.png`** — a route in `ACCENT2` with no repeats at all.
  Title: `path: no node twice`.
- **`circuit-vs-cycle.png`** — two panels, same graph both sides. Left: a closed route in
  `ACCENT2` that revisits one node, that node circled — title `circuit (closed trail)`.
  Right: a closed route with no revisit — title `cycle (closed path)`.

- **`graph-labeled.png`** — the 5-node graph `edges = [(0,1),(0,2),(1,2),(1,3),(2,4),(3,4)]`
  laid out planar with **no crossings** (use `0:(0,1) 1:(1,1) 2:(0,0) 3:(1,0) 4:(0.5,-0.9)`),
  all nodes `INK`, identical size, labels white 18pt. This is the running graph for the rest
  of the deck — reuse these exact positions everywhere below.
- **`adjacency-matrix.png`** — the 5×5 matrix for that graph. Cell fill `ACCENT` for 1 and
  `PANEL` for 0, cell text 18pt, **row and column index labels at 18pt in `INK`** (they were
  ~9px gray before). Title `A` at 18pt. Cells must be clipped flush to the grid — the old
  version overshot the field by a few px at the top and left.
- **`adjacency-squared.png`** — the matrix `A²` in the same style, with the entry
  `(A²)[0,4]` outlined in `ACCENT2` at linewidth 3, and one annotation beneath in `ACCENT2`:
  `2 two-step routes from 0 to 4`.

### Part 5 — connectivity
- **`connected-vs-not.png`** — two panels, five nodes each, all `INK`, identical size.
  Left: connected. Right: the same five nodes with one edge removed so it splits in two.
  Titles `connected` / `not connected`. Planar, no crossings, no overlapping discs.
- **`components-band.png`** — three components laid out on **one horizontal band** with
  tight cropping: an 8-node component on the left, a 3-node triangle in the middle, a
  2-node pair on the right. **No node overlap, no edge crossings** — hand-place the
  positions, do not use `spring_layout`. All nodes `INK`, identical size. Label each
  cluster beneath it in `MUTED` at 18pt: `component 1`, `component 2`, `component 3`.
  **Do not write "giant component" on this figure** — that term is not defined yet.
- **`sweep-1.png` / `sweep-2.png` / `sweep-3.png`** — the same `components-band.png`
  picture at three stages of the traversal, identical positions:
  1: one node of the left component filled `ACCENT2`;
  2: the whole left component filled `ACCENT2`;
  3: left component `ACCENT2`, middle component `ACCENT`, right component `ACCENT3`
     — with an annotation `three sweeps, three components` in `MUTED`.
  These three are the only place three colors coexist, and the slide states the meaning.
- **`giant-scale.png`** — two panels making the size point literal. Left: a blob of ~1000
  dots filling most of a frame that holds 1200 dots total — title `N = 1,200`. Right: the
  same ~1000-dot blob drawn to scale inside a frame representing 10,000,000 — so it is a
  speck — title `N = 10,000,000`. Use `ACCENT` for the 1000-node blob and a very light gray
  for the rest. Annotation: `same 1,000 nodes`.
- **`directed-arrows.png`** — a 3-node directed cycle A→B→C→A. Edges `MUTED` at
  `width=3.5`, **`arrowsize=40`**, `min_target_margin=22`. Nodes `INK`, identical size,
  labels white 18pt. Title `edges now have direction`. This figure exists solely to make
  arrowheads unmistakable — they were invisible in the old version.
- **`directed-strong.png`** — the same 3-node cycle, all edges traversable in a loop;
  title `strongly connected: you can get anywhere`.
- **`directed-weak.png`** — the same three node positions but edges A→B, B→C only;
  title `weakly connected: no way back to A`. Same arrow sizes as above.

### Part 6 — representation
All four reuse `graph-labeled.png`'s exact node positions.
- **`store-edgelist.png`** — the graph on the left; on the right the six edges drawn as
  six small `PANEL` pill shapes each containing a pair like `0 — 1`, at 18pt. The pill for
  edge `(1,3)` outlined `ACCENT2`, and the matching edge in the graph drawn `ACCENT2`, to
  show the correspondence. Title `edge list`.
- **`store-adjlist.png`** — the graph on the left; on the right five rows `0 → 1, 2`,
  `1 → 0, 2, 3`, … at 18pt, row `1` outlined `ACCENT2` with node 1 and its three edges
  drawn `ACCENT2` in the graph. Title `adjacency list`.
- **`store-matrix.png`** — the graph on the left, the 5×5 matrix on the right (same style
  as `adjacency-matrix.png`), row 1 outlined `ACCENT2` with node 1 and its edges `ACCENT2`
  in the graph. Title `adjacency matrix`.
- **`csr-build.png`** — the fix for the review's F4/F3 findings on the old `csr.png`:
  - dense `A` on the left, **row 1 shaded `ACCENT3`** (it was not highlighted before);
  - three arrays `data`, `indices`, `indptr` on the right, each cell in a rounded box,
    **with position indices `0…11` printed under `data` and `indices` at 16pt**;
  - the run `data[2:5]` and `indices[2:5]` shaded `ACCENT3`;
  - **`indptr[1]` and `indptr[2]` also shaded `ACCENT3`** — they were not before;
  - **two connector lines** from the `indptr[1]` and `indptr[2]` boxes down to the two
    boundaries of the shaded run, in `ACCENT3`;
  - array names as bold body-face labels at 18pt, not monospace;
  - **no `suptitle`** — the old 11px explanatory line was unreadable; the slide carries
    that sentence in its body instead.
- **`format-regimes.png`** — a single annotated diagram, x-axis `network size →`,
  y-axis `density →`, both axis labels at 18pt in `INK`. Two shaded regions: a large
  `PANEL`-filled region labelled `CSR` (large + sparse) and a smaller region labelled
  `dense array` (small, or dense). One `MUTED` annotation: `real networks live here`
  with a short arrow into the CSR region. No table, no bullet text.

### Part 7 — edge cases (new closing act)
- **`edge-single-node.png`** — one `INK` disc alone on white, nothing else.
- **`edge-disconnected.png`** — the Euler counterexample: two separate triangles (so
  **every** node has degree 2 — all even) with no edge between them. Nodes `INK`,
  identical size. Annotation in `MUTED`: `every degree even`. Planar, no crossings.

### Wrap-up
- **`recap.png`** — the Königsberg graph one last time (rule 2 layout), annotated with
  three `MUTED` callout labels pointing at it: `degree → parity`, `one component`,
  `A: 4 × 4 matrix`. Nodes `INK`, identical size. This replaces the two-column text recap.
- **`smallworld-teaser.png`** — a ring lattice of ~20 `INK` nodes, each joined to its two
  nearest neighbors in `MUTED`, plus **four** long-range chords drawn across the circle in
  `ACCENT2` at `width=3.5`. Annotation in `MUTED`: `a few shortcuts change everything`.
  This replaces the reused `abstraction.png`, which was an F1/F4 finding on that slide.

## Files that become unused
`abstraction.png`, `konigsberg.png`, `degree-parity.png`, `campus.png`, `adjacency.png`,
`components.png`, `csr.png`, `directed.png` are superseded. Leave the files on disk (other
material may reference them) but remove their generator functions from the script, replaced
by the ones above.

## Verify before reporting done
Run the script. Then for **each** file above confirm it exists and is > 5 KB. Report the
full list with sizes. Do not report success if any file is missing.

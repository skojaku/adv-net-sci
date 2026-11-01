# M07 figure brief (2026-10-31, after the red-pen round on wireframe v1)

Authoring rules: `slides/FIGURE_GUIDE.md`, `slides/HOUSE_STYLE.md` section 4, `figlib.py` (this directory: hand-drawn
TikZ, 1 bp = 1 slide px, grain). Every number comes from `smallgraphs.py` (never typed); add assertions for what a
figure states. Palette: ink, muted, pale, hot (red), cool (blue), deep, teal; GOLD/`hot!85` only as m06 does; no green; no bar charts
(the bars of the matrix notation are fine). Labels in MesloLGS, math in Latin Modern, asides in the hand font (`F.aside`).
Plain wording in every label (rule N9: no figures of speech, no verbs of life or war).

Colour meaning, fixed for the whole deck:
- community 1 = cool (blue), community 2 = hot (red); a walker = a ring in ink
- eigen notation as in M06 (`slides/m06/figures/figs_decomp.py`): circle = eigenvalue (area ∝ |value|), TALL bar = right eigenvector,
  WIDE bar = left eigenvector / row vector, square = matrix. k=1 blue, k=2 gold (hot!85), the rest pale.
- a probability or a value on a node: node fill from faint to cool (`F.shade`); a heat map: faint (0) to cool (high)

Output: `figures/<name>.png` through `F.emit` / `F.emit_group` / `F.emit_frames`; run `python3 figs_x.py` (it ends in `F.run(FIGURES)`).
`container="full"` = 1080 wide, `container="col"` = 537 wide; `h` is the height in px. Keep the same canvas (same crop, same
node positions: `box=` or `emit_group`) across the slides of one run (a build, a question and its answer).
Max displayed height by layout: L-b 480 (420 with a `.take` under it), L-a 380 (320 with `.sub` and `.take`), L-g 600, L-c 470.

Node numbering 0-11 for the 12-node network (community 1 = 0-5, community 2 = 6-11), matching the Pen & Paper sheet.
The 12-node layout in `smallgraphs.TWO12_XY` is a first draft: improve it if it reads badly (keep it in smallgraphs, so every figure agrees).

## Worker A: drawn scenes and graphs  (module `figs_a.py`)

| file | layout | size | what |
|---|---|---|---|
| `pearson-walker` | L-c right | col 537 x 400 | A simple drawing (the lecturer's red-pen sketch: a stick figure standing on a field of crossing lines, one first path of a few equal-length steps in random directions, one step labelled "1 yard"). Nothing else. |
| `pearson-answer` | L-g, with a `.take` under | full 1080 x 470 | LEFT: 5 walkers' paths (100 unit steps, seeded) from the same start (a lamp post), in 5 pale muted colours. RIGHT: end points of 10,000 walkers (seeded) as a cloud of small dots centred on the start; a grey ring at radius 10 with the aside "typical distance after 100 steps". Both panels the same scale, same start mark. Assert: rms end distance within 3% of 10. |
| `fields` | L-b | full 1080 x 420 | Three panels in a row, one drawing and one caption each: (1) pollen grain, a zig-zag trace (seeded walk) in water, caption "pollen in water, 1905"; (2) a mosquito, caption "mosquitoes and malaria"; (3) a small web graph with a surfer ring, caption "the web, 1998". After them a grey arrow and the aside "and on a network?". Simple drawings. |
| `walk-rule` | L-b | full 1080 x 430 | `smallgraphs.RULE` (7 nodes). A walker (ring) on node 0 with 4 neighbours; each of the 4 edges labelled 1/4 (hot); the other edges plain. Aside: "no memory of where it came from". |
| `two-comm-q` | L-c right | col 537 x 420 | `TWOC` (two 5-cliques joined by one edge) drawn compactly: community 1 cool nodes, community 2 hot nodes; a ring on one node of community 1; the single edge between the communities drawn heavy with a grey aside "one edge". A faint rounded outline around each community. |
| `two-comm-walk` | L-b | full 1080 x 420 | LEFT: the same network, same colours, a walk of 60 steps drawn as a brush stroke whose colour follows the community at each step. RIGHT: below/beside it a time strip (one cell per step, 400 steps, seeded) coloured blue/red by community with long runs; an arrow "time"; aside "about 21 steps per visit" (assert the mean run length of the seeded walk is between 14 and 30). Words "blue" and "red" are NOT written; the colours speak. |
| `clique-q` / `clique-a` | L-a (sub, no take / sub + take) | full 1080 x 380 | `CLIQUE10` with nodes on a ring, all 45 edges thin, ring on node 0. `clique-a` same canvas plus an inset: the worst-start distance curve `worst_dist` for t = 0..4, a dashed line at EPS, marked where it crosses (t = 1). |
| `twoclique-q` / `twoclique-a` | L-a | full 1080 x 380 | `TWOC` drawn wide, two cliques and one bridge, community colours. `twoclique-a`: same canvas plus the inset curve for t = 0..30 with the clique curve (pale) for comparison and EPS; marks at t = 1 (clique) and t = 20 (bridged). |
| `no-larger` | L-b | full 1080 x 430 | Two frames side by side on `RULE` (7 nodes): LEFT numbers `AVG_VALUES` on the nodes, the largest (9) hot; RIGHT the same drawing after one step where every number is replaced by the average of its neighbours' numbers (computed with `trans`), largest now smaller (assert < 9). Between them an arrow "one step: the average of the neighbours". Numbers drawn big inside the nodes. Note the walk applies P to a column vector (average of neighbours), so use P @ values. |
| `detailed-balance` | L-a (sub + take) | full 1080 x 300 | Two nodes i and j joined by an edge; i with degree 3 and j with degree 2 shown with their other edges stubbed; two arrows between them (i to j labelled `π_i · 1/k_i`, j to i labelled `π_j · 1/k_j`) of equal drawn weight, and an equals sign; so "the flow each way is the same". Aside: "walkers going each way". Choose k values so the arithmetic reads (π_i = 3/10, π_j = 2/10 for k_i = 3, k_j = 2 in a 5-edge total: assert the two flows are equal). |
| `tasks-diamond` | L-c right | col 537 x 400 | TOP: the 4-node diamond (`DIAMOND`, degrees 2,2,3,3, nodes numbered 0-3, positions `DIAMOND_XY`). BOTTOM: a dashed square the size of a QR code with the label "QR code: Part 3 notebook" (the link does not exist yet; the placeholder is deliberate and visible). |

## Worker B: matrix pictures  (module `figs_b.py`)

All on the 12-node network `TWO12` (`P12`, `A12`) unless stated. Matrix cells are heat-mapped faint to cool; rows and columns are numbered 0-11 in small muted type; a hot bracket or ring marks the row or entry under discussion.

| file | layout | size | what |
|---|---|---|---|
| `P-def` | L-b | full 1080 x 440 | LEFT: the 12-node network (community 1 cool, community 2 hot). RIGHT: P as a 12 x 12 heat map: two dense blocks on the diagonal, thin entries off the blocks. Axis words (the lecturer's red pen): rows "from", columns "to". One row highlighted with the callout "row i: the odds of leaving i, sums to 1". |
| `xP-1`, `xP-2`, `xP-3` | L-a (sub + take) | full 1080 x 320 | Same canvas. Pictogram: a WIDE bar x (12 cells) times the 12 x 12 P equals a WIDE bar xP (12 cells), cells shaded by value with the value written when it is not 0; the walker's probability mass is also drawn as node shading on a small copy of the network on the left. Case 1: x = (1,0,0,...): xP = the row of node 0 (that row of P hot). Case 2: x = e_1: row of node 1. Case 3: x = (0.5, 0.05, 0.05, 0.1, 0.1, 0.2, 0,0,0,0,0,0) (sums to 1): xP = the mix of rows, weights shown on the rows. Assert xP == `x @ P12` and the printed values. Same canvas for all three so only the numbers move. |
| `xPt` | L-a (sub only) | full 1080 x 320 | x(0), then three P squares each with a small "x P" multiplication sign between them, "..." and an equals sign to x(t); label under the three squares "t times". Wide bars shaded by value. Or a more compact equivalent that reads the same. |
| `Pt-slider` | L-b (scrub) | full 1080 x 420 | FRAMES for t = 1, 2, ... , 40 (41 frames are fine: build from numpy, render fast; if the TeX route is too slow, 15 frames: 1,2,3,4,5,6,8,10,12,15,20,25,30,35,40). Each frame: the heat map of P^t (same canvas, same colour scale 0 to about 0.5), a big "t = N" label to the right, and the callout at t=1 "stays in its community", at t=5 "starting to leak", at t=40 "every row is the same". `F.emit_frames("Pt-slider", ...)` (the last frame is the figure). |
| `Pt-40` | L-b (with take) | full 1080 x 410 | P^40 as a 12 x 12 table: the NUMBER in every cell (2 decimals, leading zero dropped), cell background coloured by the value (the lecturer: "re-colour the background by the entry values"), rows labelled "start 0" ... "start 11" at the left in muted type, columns 0-11 on top; a hot bracket at the right: "the same row in every row: π". Assert every row equals PI12 to 2 decimals. |
| `Pt-zoom` | L-b | full 1080 x 430 | "Zoom in on P^t": LEFT the t=5 heat map with a small box around its top-left 3 x 3 patch; arrows from the box to the RIGHT where that patch is enlarged with the numbers (P^5, 2 decimals); one entry ringed hot with the aside "start at 0, at 2 after 5 steps". Callout under the enlarged patch: "row = where it starts, column = where it is". |
| `P-decomp` | L-a (sub + take) | full 1080 x 320 | As m06 `decomp-sum`, but for P: circle(λ1) + tall bar φ1 × wide bar ψ1^T, plus the k=2 term, plus ..., plus the k=12 term (three terms: 1, 2, 12). Circles' areas from `LAM12`; k=1 blue, k=2 gold, the rest pale. Grey aside: "tall and wide bars are different vectors for P". The tall/wide pair stands for the square matrix, as in m06. |
| `Pt-circles-1`, `-2`, `-3` | L-b | full 1080 x 430 | The same canvas as `P-decomp` but showing all 12 terms in two rows of 6 (or a single scaled row), circles' areas = |λ_k|^t for t = 1, 5, 40 (circle 1 always full size, blue; circle 2 gold). Callouts: t=1 "one step"; t=5 "λ2^5 = 0.55"; t=40 "only the circle at 1 is left". Same canvas across the three. Note the eigenvalues of 0 (three of them) draw no circle at t ≥ 1: draw a tiny dot so the term is visible. |
| `P1-eq-1` | L-b | full 1080 x 430 | The square P (12 x 12 heat map) times a TALL bar of 12 ones (cells "1") equals the same TALL bar. One row of P highlighted with its cells summing to 1 and the matching first cell of the result circled. In large hand writing over the top: "P x = x" with the aside "a vector that P does not change". Callout: "P 1 = 1". |

## Worker C: plots and the summary  (module `figs_c.py`)

Use `F.Axes` (and TikZ) for plots; no bar charts. Curves hand-drawn weight; labels at the 15.5 px x-height floor.

| file | layout | size | what |
|---|---|---|---|
| `degree-share` | L-a (sub + take) | full 1080 x 320 | Scatter: x = degree, y = share of visits after 20,000 steps (karate club, seeded; 34 dots) with the straight line through the origin y = x / 156 (muted). Node 33 (degree 17) and node 11 (degree 1) ringed hot with callouts "17 ÷ 0.109 = 156" and "1 ÷ 0.0064 = 156" (compute the shares from the seeded walk and write what the simulation gives, rounded, then assert each ratio is within 25 % of 156 for node 33 and 40 % for node 11; if node 11 is too noisy use 100,000 steps and say so in the note). |
| `lam-curves-q` | L-c right | col 537 x 400 | Axes: t (0 to 40), y = |λ_k|^t for the 12 eigenvalues of `LAM12`: the λ1 curve flat at 1 (blue); the rest decaying curves in pale, λ2 the slowest; label λ1, λ2, λ3, λ4 near the curves (the lecturer's sketch), no mark that gives the answer. |
| `lam-curves-a` | L-c right | col 537 x 400 | Same canvas; the λ2 curve in gold/hot with the label λ2 = 0.89, and the values 0.55 (t=5), 0.31 (t=10), 0.01 (t=40) marked as dots on it. |
| `mix-1`, `mix-2`, `mix-3` | L-a | full 1080 x 380 | Axes t (0 to 30) and y = ||x(t) − π||_1 (0 to 2). One thin muted curve per starting node (12 curves, `dist_by_start` on `P12`) and a black curve for the worst start. Build 1: curves + aside "where you start matters at first" at the early crowd and "λ2 dominates" on the late straight tail (the lecturer's note; the tail follows 0.889^t). Build 2: adds the dashed horizontal line at ε = 0.25 with the aside "how close is close enough?". Build 3: marks where the worst-start curve crosses ε (t = 13, hot), a vertical line down to the axis and the label "mixing time"; same canvas for all three. |
| `gap-gauge` | L-a (sub + take) | full 1080 x 300 | A horizontal gauge for λ2 from -0.2 to 1 with markers: 10-clique (−0.11, τ 0.9), karate club (0.87, τ 7.6), two communities (0.89, τ 9), two 5-cliques + bridge (0.93, τ 14), ring of 1,000 (0.99998, τ 51,000: an arrow off the right end). The region past 0.99 shaded hot. τ values from `spectral_gap_table()`. |
| `diamond-expansion` | L-a (sub only) | full 1080 x 340 | The diamond network at t = 0, 1, 2, 5, 10: x(t) as node shading with the values written beside the nodes (start x(0) = (1,0,0,0)); π = (0.2, 0.2, 0.3, 0.3) as a dashed ring size on each. Under them the expansion: π − 0.5·0^t ψ2 + 0.3·(−2/3)^t ψ4 with the t = 2 case checked: x(2) = (1/3, 1/3, 1/6, 1/6). Draw nodes by value, not as bars. Assert with `PSI`, `LAM_PSI`. |
| `eigvec2` | L-b | full 1080 x 430 | Point plot: x = node index 0..11, y = second eigenvector of P (scaled so the max is 1, community 1 positive, via `eigsystem`). Nodes 0-5 cool, 6-11 hot, dashed line at 0; the bridge nodes 2, 5, 8, 11 at ±0.74 ringed. Callout: "the sign gives the community". |
| `comm-curve` | L-a (sub + take) | full 1080 x 330 | x = steps 0..40, y = probability of being in community 1 from start node 0, dots at t = 0, 1, 2, 3, 5, 10, 20, 40 joined by a curve (1, 1, .92, .88, .80, .67, .55, .505) and the dashed curve 0.5 + 0.5·0.889^t over it (assert they agree within 0.06 for t ≥ 3); a dashed line at 0.5; callout at t ≈ 3: "the other eleven circles are gone". |
| `summary` | L-g | full 1080 x 560 | Built LAST from the other figures' PNGs as thumbnails: three rows, each a claim in one line with a thumbnail: (1) "The eigenvalue 1 gives the degree" (thumb `degree-share`); (2) "The second eigenvalue gives the communities and the mixing time" (thumbs `eigvec2`, `gap-gauge`); (3) "Short walks see communities. Long walks see degree." (thumb `comm-curve`). Compose with PIL after the other workers' files exist. |

---

# Round 2 (2026-10-31, after the lecturer's comments on deck v2)

Shared change first: `smallgraphs.py` now has `EPS = 0.5` (1-norm; the standard total-variation 1/4), `EPS_SMALL = 0.05`, the mixing times at EPS
(clique 1, karate 10, two communities 7, two bridged cliques 10) and `tau_table()`. v2 used 0.25 with no reason; every figure that drew
epsilon or a mixing time must now follow `G.EPS` and the `TMIX*` constants (never typed). Photos are in `figures/photos/` (credits in
`photos/CREDITS.md`): `pub.jpg` (colour photo, 1600 x 1323), `mosquito.jpg` (colour, 1920 x 1277), `perrin.png` (black line plot of a Brownian
trajectory, 1280 x 1100, public domain). Composite photos with PIL after the TikZ render (so the grain is not put on a photo); a photo is shown
without the hand-drawn frame but with a thin pale outline. Credits go on the slide, not in the figure.
Wording in plain English (rule N9). Rename "tall bar / wide bar" to "column / row" in every label.

## Worker A (module `figs_a.py`; edit the existing functions, add the new ones)

| file | layout | size | what |
|---|---|---|---|
| `pearson-walker` (redo) | L-c right | col 537 x 460 | TOP: the existing small drawing (stick figure on the grid, one path, "1 yard"), at about 537 x 200. BELOW it, the pub photo (`pub.jpg`) cropped to the building, about 537 x 250, placed directly under the drawing. Nothing else. |
| `polya` (new, replaces the Rayleigh slide) | L-g with a `.take` | full 1080 x 470 | Pólya's recurrence. LEFT panel "2D": a seeded random walk on the square lattice (400 steps) that returns to its start several times; the start marked with a ring, the returns with small hot dots. RIGHT panel "3D": a seeded random walk on the cubic lattice drawn in a simple oblique projection, 400 steps, that leaves and does not come back; the start ringed. Panel labels "2D" and "3D". Same scale feel, same line weight, pale muted path with the start/return marks hot. Add `check()`-style assertions: the 2D seed returns at least 4 times in 400 steps, the 3D seed returns at most once. Also assert by simulation (10,000 walkers, 3D, 2,000 steps, seeded) that the fraction that ever returns is between 0.30 and 0.36 (Pólya's 0.3405 is the limit) and, for 2D, that the fraction returning within 2,000 steps is above 0.80 and rising (it tends to 1 only slowly: do not print a 2D number on the figure). |
| `fields` (redo) | L-b | full 1080 x 420 | THREE panels in a row using PHOTOS, with the whole composition horizontally centred on the canvas (assert that the ink bounding box is centred within 4 px): (1) the Perrin trajectory (`perrin.png`, recoloured muted/ink) with caption "pollen in water, 1905"; (2) the mosquito photo, cropped square, caption "mosquitoes and malaria"; (3) the small web drawing with the surfer ring (keep your drawing), caption "the web, 1998". NO grey arrow and NO "and on a network?" aside any more (they pulled the picture to the left; the question is on the next slide). Equal panel sizes, equal gaps. |
| `no-larger` (redo; wireframe: 'no eigenvalue above 1') | L-a (sub + take) | full 1080 x 320 | One node and its neighbourhood, before and after one averaging step, so that the room sees WHY the largest number cannot grow. LEFT: node i (hot ring) holding the largest number, 9 (drawn in the disc), with four neighbours holding 7, 5, 9, 3 (all at most 9; draw numbers big in the discs). A big arrow labelled "replace by the average of the neighbours". RIGHT: the same drawing, node i now holds 6 = (7+5+9+3)/4, written under the arrow or the node. Assert the arithmetic and that every neighbour is <= the number at i. No second network. |
| `detailed-balance` (redo) | L-a (sub + take) | full 1080 x 320 | Two nodes i and j joined by an edge (k_i = 3, k_j = 2, so 2m = 10 with the other edges stubbed out as before). TWO labelled arrows of equal weight between them: i to j labelled "at i, then step to j: $\pi_i \cdot \frac{1}{k_i}$" and j to i labelled "at j, then step to i: $\pi_j \cdot \frac{1}{k_j}$", an equals sign between the two labels. Below: the numbers π_i = 3/10, π_j = 2/10 giving 0.1 = 0.1 (assert). The slide's `.sub` carries the statement Pr(i to j) = Pr(j to i); keep the figure's words short. |
| `clique-q`, `clique-a`, `twoclique-q`, `twoclique-a` | L-a | as before | Re-run with the new `G.EPS` (0.5): the crossings are now at t = 1 (clique) and t = 10 (bridged cliques); y range 0 to 2; the dashed line at 0.5 labelled "ε = 1/2". Assert the crossing marks against `G.TMIXC10` / `G.TMIXTC`. |

## Worker B (module `figs_b.py`; all matrix figures)

1. NEW COLOUR SCALE for every heat map in the deck (the lecturer found the shading hard to read): low values BLUE, high values RED, through a light middle
   (a pale yellow is allowed): for example cool `#3959A6` at 0, pale yellow `#F4E7B0` in the middle, hot `#B14434` at the maximum, interpolated in a
   perceptually even way (you may use a square-root or gamma stretch so that values near 0.07 to 0.15, the t = 40 case, are clearly different from 0 and
   from 0.5). Zero entries are the lowest colour. The same scale and the same stretch in `P-def`, `xP-1..3`, `xPt`, `Pt-slider`, `Pt-40`, `Pt-zoom`,
   `P1-eq-1`. Add a thin colour key (a strip with 0, 0.25, 0.5 under or beside the matrix) on `P-def`, `Pt-slider` and `Pt-40` only. Values that are
   written as numbers must stay readable on every colour (ink on the pale colours, white on the dark ones).
2. `Pt-slider`: use the empty space. The matrix is larger (about 400 px square), the "t = N" label and the callout sit close to it. Keep the 40 frames.
3. `P-decomp`, `Pt-circles-1..3`: replace every label that says "tall"/"wide" with "column"/"row": the aside becomes "for P, the column and the row are different vectors".
   (The pictograms keep their shapes.)
4. If anything else in `figs_b.py` mentions epsilon or a mixing time, use `G.EPS`.

## Worker C (module `figs_c.py`)

1. `mix-1`, `mix-2`, `mix-3`: epsilon is now `G.EPS` = 0.5, the crossing of the worst start is at t = 7 (`G.TMIX12`). Build 2's aside: "ε = 1/2, the usual choice" (short). Build 3: the red dot at t = 7 and the label "mixing time".
2. NEW `relax-curve` (L-a, sub + take, full 1080 x 320): x = t (0 to 30), y = λ2^t for the 12-node network (λ2 = 0.889), a smooth curve, the dashed line y = 1/e at 0.37, the hot dot at t = τ = 9 where the curve crosses it, a vertical dashed line down to the axis labelled "τ = 9", and the aside "the slowest term shrinks by a factor e in τ steps". Assert λ2^τ is within 0.03 of 1/e.
3. `gap-gauge`: keep; the labels already say τ. (The lead renames the slide.)
4. NEW `tau-vs-mix` (L-a, sub + take, full 1080 x 300): a table drawn in figlib text, four rows (`G.tau_table()`: 10-clique, karate club, two communities, two cliques + bridge) and three numeric columns: "relaxation time τ" (1 decimal), "mixing time, ε = 1/2" and "mixing time, ε = 0.05" (integers). The numbers in each row grow left to right, which is the point: a smaller ε costs a few more τ. Row names left, numbers right-aligned, thin rules, hot on the last column. Use `G.tau_table()` only.
5. `eigvec2` (redo, narrower): the new slide shows the figure at 70 % of the width with a one-line explanation beside it, so author it at 756 px wide and 430 high (add a container entry `"wide": 756` to `F.CONTAINER`/`F.DESIGN` in your module; do not edit figlib.py). Keep the content: nodes 0..11 on x, the second eigenvector (scaled to max 1, community 1 positive) on y, community 1 blue, community 2 red, the dashed zero line, the bridge nodes 2, 5, 8, 11 ringed at +-0.74, the callout "the sign gives the community".
6. `summary`: figs_summary.py builds it from the other PNGs: re-run it last (`python3 figs_summary.py`). Change its row 2 thumbnails to `eigvec2` and `gap-gauge` as now (nothing to do if the files still exist), and add `relax-curve` as the row-2 first thumbnail instead of `gap-gauge` if there is room.

# m03 FIGURE_SPEC

All static figures come from `figures/make_figures.py` (TikZ → pdflatex → pdftoppm); the
four GIFs come from `figures/make_animations.py`, which imports geometry, palette and the
graph data **from** `make_figures.py` so the two cannot drift. Per `FIGURE_GUIDE.md`:
TikZ for node-link diagrams, hand-drawn axes for the data figures, no matplotlib, no bar
charts, no green.

## The pipeline and why the numbers work out

Author at final size: **1 TeX big point (bp) = 1 slide pixel.**

- The page is fixed to the design canvas (`\useasboundingbox`), so no crop step can
  change the scale from figure to figure.
- `pdftoppm -r 288` → 4 px per bp.
- The deck scales an image by `min(container / file_w, 380 / file_h, 1.0)`
  (`w:` is inert under this theme).

| container | canvas W | file W | deck scale | on-slide px per bp |
|---|---|---|---|---|
| `cols` column, 537px | 520 bp | 2080 px | 537/2080 = 0.2582 | **1.033** |
| full width, 1120px | 1100 bp | 4400 px | 1120/4400 = 0.2545 | **1.018** |

Height must not bind, or everything shrinks: `H ≤ 0.7076 · W`. Enforced as an assertion.

## Fixed sizes (assert, don't eyeball)

| thing | design | lands on slide | band |
|---|---|---|---|
| node disc | 40 bp diameter | 40.7–41.3 px | 26–52 px ✓ |
| any text | 30 pt | cap height ≈ 21 px | ≥ 21 px ✓ |
| edge stroke | 2.6 bp | 2.7 px | — |
| highlight stroke | 5 bp | 5.2 px | — |

Town names never go inside a disc — they are 5–9 characters long. Discs carry at most one
character (a degree, a step number); names sit outside, on the side with room.

## Assertions in the generator (build fails, not review finds)

1. `H ≤ 0.7076 · W` — width binds, so the scale table above is the real scale.
2. Ink fills ≥ 76 % of the canvas on **both** axes.
3. Every disc drawn at `NODE = 40` bp; on-slide diameter recomputed from the actual file
   size and asserted inside 26–52 px.
4. Every font size used is ≥ `FONT_MIN = 30` pt; on-slide cap height asserted ≥ 21 px.
5. Palette membership: every colour emitted is one of the five tokens.
6. Edge–disc clearance: no straight edge may pass through a disc it does not terminate at.
7. **Planarity of the Moravian graph**: all 78 pairs of candidate cables tested for proper
   segment intersection; must be zero. This is the F2 criterion made a build gate.
8. **Every printed number is computed, never typed.** The MST total, each algorithm's
   step order, the Borůvka rounds, every connectivity ratio, every R-index, every κ and
   f_c, and every simulated curve are produced in the generator and cross-checked against
   the verified table in `review/DECK_SPEC.md`. A mismatch fails the build.
9. **Label collision**: no town label's bounding box may overlap another label or a disc
   it does not belong to.

## Palette — one meaning per figure, stated on the slide

`accent #3959A6` · `accent-2 #B14434` · `accent-3 #DAB167` · `gray #6b6b6b` · `ink #000000`.

- **accent** — the object under discussion (the towns, the current network)
- **accent-2** — *what this slide is about* (the chosen cable, the removed town, the
  targeted curve, the new redundant route)
- **accent-3** — the secondary comparison object (the random-failure curve, the second
  optimal tree, the alternative)
- **gray** — annotation and discarded material only

Deck-wide conventions, so a colour never changes meaning between consecutive slides:

| in every Moravian figure | means |
|---|---|
| solid black edge | a cable in the current tree |
| dashed gray edge | a candidate route not chosen |
| accent-2 edge | the cable this slide is about |
| accent-2 disc | the town this slide is about (removed, targeted, the plant) |
| accent-3 edge | the redundant route added in Part 6 |

| in every curve figure | means |
|---|---|
| accent-2 curve | targeted attack |
| accent-3 curve | random failure |
| gray dashed vertical | the threshold being claimed |

## Photographs and third-party images

Only one: `boruvka-portrait.png`, the 1981 photograph of Otakar Borůvka already used by
the course lecture note (Wikimedia Commons), saved locally. `check_render.py` exempts it
from the in-figure text floor, exactly as it exempted the Königsberg engraving in m01 —
its lettering is not ours to size.

**Deviation recorded.** The lecture note illustrates "real grids have loops" with a
copyrighted geni.org photograph of the US grid. The slide instead draws its own meshed
network (`real-grid-mesh`): it stays inside the palette, it is legible at slide size, and
it can highlight the loops, which the photograph cannot.

The two demo stills (`demo-still`, `puddle-widget`) are drawn schematics of what the live
demo shows, captioned as such — not screenshots pretending to be the widget.

## Figures

Canvas column: `c` = 520 × H (in `cols`), `f` = 1100 × H (full width).

### The Moravian geometry, defined once

Eight towns at their true relative positions (lat/lon projected to km about the centroid,
then scaled into the canvas). Every Moravian figure calls the same `moravia(...)` routine
with a different edge/highlight/label set, so the graph never moves between consecutive
slides — the m01 defect where the same network changed size slide to slide.

### Part 1

| file | canvas | content | accent-2 means |
|---|---|---|---|
| `moravia-dark` | f 1100×470 | the eight towns as discs with names; no edges; caption "1919" | — |
| `boruvka-portrait` | c 520×— | the 1981 photograph, plus "Otakar Borůvka · 1899–1995" | — |
| `abstract-1` | f 1100×470 | towns as plain discs, names outside | — |
| `abstract-2` | f 1100×470 | + the 13 candidate routes, all thin gray | — |
| `abstract-3` | f 1100×470 | + a weight on every route; one route's "48 km" called out | the called-out weight |
| `moravia-graph` | f 1100×470 | the finished weighted graph; Brno ringed as the power plant | Brno, the plant |
| `loop-waste` | c 520×330 | a 4-town cycle; one edge struck through; "still connected" | the removable cable |
| `tree-def` | c 520×330 | a small tree: no cycle anywhere, one route between any two | — |
| `spanning-count` | f 1100×470 | the MST with its seven cables numbered 1…7; "8 towns, 7 cables" | — |
| `mst-def` | f 1100×470 | candidate graph, MST solid accent-2, the rest dashed gray; "292 km" | the MST |

### Part 2 — algorithms on the same geometry

| file | canvas | content | accent-2 means |
|---|---|---|---|
| `kruskal-rule` | f 1100×260 | the 13 weights on a number line, cheapest at the left, an arrow sweeping right | the cable being considered |
| `kruskal.gif` | f 1100×470 | 9 frames: empty → 17 → 29 → 42 → 48 → 49 → *51 refused (flashes accent-2 then vanishes)* → 53 → 54 | the cable just added |
| `kruskal-skip` | f 1100×470 | the state at 51 km: the cycle it would close drawn accent-3, the refused cable accent-2 dashed | the refused cable |
| `kruskal-worksheet` | f 1100×470 | the weighted candidate graph, nothing chosen | — |
| `kruskal-answer` | f 1100×470 | the MST with each cable badged 1…7 in Kruskal order; 51 struck out | the skipped cable |
| `prim-rule` | c 520×330 | Brno ringed, three candidate cables leaving it, the cheapest accent-2 | the cheapest cable out |
| `prim.gif` | f 1100×470 | 8 frames growing one blob from Brno: 48, 17, 49, 53, 29, 42, 54 | the cable just added |
| `prim-worksheet` | f 1100×470 | candidate graph with Brno ringed, nothing chosen | Brno, the start |
| `prim-vs-kruskal` | f 1100×470 | one tree, each cable badged with two numbers: Kruskal's step (gray) and Prim's step (accent-2) | Prim's order |
| `cut-property` | c 520×340 | a small graph split by a dashed cut line; the cheapest crossing edge accent-2 | the forced edge |
| `tie-graph` | f 1100×470 | the candidate graph with Olomouc–Zlín reading 49, tying Prostějov–Zlín; both tied weights accent-2 | the tie |
| `tie-two-trees` | f 1100×420 | two panels: the two optimal trees, each "292 km"; the differing cable accent-2 in each | the cable they disagree on |
| `boruvka.gif` | f 1100×470 | 4 frames: components colour-coded → all six round-1 cables appear **at once** → merged → round 2's single cable | the cables chosen this round |
| `boruvka-rounds` | f 1100×470 | the finished tree, round-1 cables accent-2, round-2 cable accent-3; "2 rounds" | round 1's six cables |

### Part 3 — breaking that grid

| file | canvas | content | accent-2 means |
|---|---|---|---|
| `mst-alone` | f 1100×470 | just the seven cables and eight towns; "292 km" | — |
| `mst-blank` | f 1100×470 | the same tree, no weights, no highlight — for the vote | — |
| `brno-removed` | f 1100×470 | Brno drawn as an open ring with a cross; the three surviving pieces outlined | Brno, removed |
| `tree-bridges` | c 520×340 | the tree with the unique Jihlava→Zlín route traced; "one route, no spare" | the only route |
| `real-grid-mesh` | f 1100×420 | a drawn meshed grid, two independent routes between the same pair traced | the second route |
| `connectivity-def` | f 1100×470 | the post-Brno grid with each piece's size printed; the largest ringed; "3 / 8" | the surviving largest piece |
| `profile-build.gif` | f 1100×420 | 8 frames: the grid shrinking on the left, the profile point appearing on the right | the town removed this frame |
| `r-index` | f 1100×420 | the targeted profile with the area under it filled accent-2; "R = 0.17" | the area |
| `profile-random` | f 1100×420 | the random-order profile alone, accent-3; "R = 0.41" | — |
| `profile-both` | f 1100×420 | both profiles on one axis, targeted accent-2 below random accent-3 | targeted |
| `fixed-vs-adaptive` | f 1100×420 | two curves on a random network: fixed order, adaptive order; collapse marked at 0.58 and 0.40 | adaptive |
| `demo-still` | c 520×330 | a schematic of the web demo: a small network, a strategy switch, a profile | — |

Assertions: every profile is recomputed from the actual graph; R printed = the exact
fraction (11/64 and 13/32) rounded to two places; the pieces after Brno's removal must be
3, 3, 1.

### Part 4 — percolation

| file | canvas | content | accent-2 means |
|---|---|---|---|
| `puddle-low` | c 520×340 | a 24×24 grid at p = 0.40; wet cells accent, largest cluster accent-2 | the largest puddle |
| `puddle-sweep.gif` | f 1100×420 | 10 frames, p = 0.30 … 0.75, same random field | the largest puddle |
| `phase-transition` | f 1100×420 | measured largest-cluster fraction against p, hand-drawn axes; p_c ≈ 0.59 marked | the curve |
| `puddle-widget` | c 520×340 | the grid at p = 0.60 with a drawn slider beneath | the largest puddle |
| `order-irrelevant` | f 1100×400 | two panels, two different fill orders, identical final cluster | the largest puddle |
| `reverse-percolation` | f 1100×360 | one horizontal axis, an arrow right labelled "add nodes → giant appears" and an arrow left labelled "remove nodes → giant dies" | the removal direction |

Assertions: the percolation field is seeded; the printed largest-cluster fraction at each
p is measured from the field; the marked p_c is the literature value 0.5927 and the
measured curve's steepest rise must fall within ±0.06 of it.

### Part 5 — the formula

| file | canvas | content | accent-2 means |
|---|---|---|---|
| `follow-edge` | c 520×340 | a small network; one edge picked accent-2 with a walking arrow along it | the edge picked |
| `qk-bias` | f 1100×420 | the same network drawn as a pile of edge-ends: a degree-4 node contributes four, a degree-1 node one | the hub's four ends |
| `kappa-def` | c 520×330 | the landing node with its own links counted; "average = κ" | the landing node |
| `branching` | f 1100×420 | three rings of a fan-out: 1 → κ−1 → (κ−1)²; the arrival edge greyed out | the onward links |
| `molloy-reed` | f 1100×420 | two fan-outs side by side: κ−1 = 0.75 dies, κ−1 = 2 explodes | the surviving branch |
| `kappa-worksheet` | f 1100×360 | three small graphs — a 6-ring, a 6-star, a 5-path — degrees printed, κ blank | — |
| `kappa-answer` | f 1100×360 | the same three with κ = 2, 3, 1.75 filled in and the κ = 2 line marked | the one at threshold |
| `dilution` | f 1100×420 | the same fan-out with a fraction f of the branches crossed out | the surviving branches |
| `fc-formula` | f 1100×420 | branching (1−f)(κ−1) plotted against f, crossing 1 at f_c | the crossing |
| `fc-poisson` | f 1100×420 | f_c = 1 − 1/⟨k⟩ against ⟨k⟩, with ⟨k⟩ = 4 → 0.75 marked | the marked point |
| `fc-scalefree` | f 1100×420 | κ against the largest degree present, climbing without bound; f_c → 1 alongside | the divergence |

Assertions: κ for the three worksheet graphs is computed from their degree sequences and
must equal 2, 3 and 7/4; the Poisson curve is `1 − 1/⟨k⟩` evaluated, not sketched.

### Part 6 — robust yet fragile

| file | canvas | content | accent-2 means |
|---|---|---|---|
| `sim-random` | f 1100×420 | measured curves, ER and scale-free, random removal | the scale-free curve |
| `sim-targeted` | f 1100×420 | the same two networks, highest degree first | the scale-free curve |
| `robust-fragile` | f 1100×420 | all four curves on one axis, the two scale-free ones accent-2 | scale-free |
| `efficiency-security` | f 1100×420 | two networks with the same node count: a star (cheap, one point of failure) and a mesh (dearer, no single point) | the fragile one |
| `mst-blank-design` | f 1100×470 | the MST with the six unused routes drawn faint dashed, for the discussion | — |
| `redundant-answer` | f 1100×470 | the MST plus Zlín–Hodonín and Znojmo–Hodonín accent-3; the closed ring traced; "+136 km · R 0.17 → 0.27" | the two new cables |
| `design-principles` | f 1100×470 | the improved grid with every town's degree printed, showing the degrees evened and no leaf left stranded | the protected hub |
| `build-it-back` | f 1100×420 | two panels: 1926's tree and today's meshed grid, same eight towns | today's extra routes |

Assertions: the simulated curves are measured on seeded `networkx` graphs at the sizes in
`DECK_SPEC.md`; the collapse points printed on the slides must match the measured ones;
the redundant-answer R values are the exact fractions 11/64 and 17/64.

### Part 7 — edge cases (a separate file per question and per answer)

| file | canvas | content |
|---|---|---|
| `ring-q` | c 520×340 | a 6-ring, every degree printed as 2, κ blank |
| `ring-a` | c 520×340 | the same ring, κ = 2 filled in, one node removed showing the chain |
| `er1-q` | c 520×340 | a random network at ⟨k⟩ = 1, κ blank |
| `er1-a` | c 520×340 | the same, κ = 2, annotated "m02's giant component is born here" |
| `betweenness-q` | f 1100×400 | two clusters joined by one degree-2 bridge node; a hub inside one cluster |
| `betweenness-a` | f 1100×400 | the same, the bridge removed: two pieces; the hub removed: one piece |
| `triangles-q` | c 520×340 | a patch dense in triangles |
| `triangles-a` | c 520×340 | the same patch with a search fan drawn, returning into itself |

### Wrap-up

| file | canvas | content |
|---|---|---|
| `recap` | f 1100×440 | four panels in a row: 292 km · 3/8 · +136 km · f_c = 1 − 1/(κ−1) |
| `m04-teaser` | c 520×340 | the q(k) edge-end pile again, relabelled "your friends" |

## Never shared between slides

Every question/answer pair emits **two files**, even when only one label differs
(`kruskal-worksheet` / `kruskal-answer`, `kappa-worksheet` / `kappa-answer`, `ring-q` /
`ring-a`, …). `mst-blank` (the vote), `mst-alone` (the finished grid) and
`mst-blank-design` (the discussion) are three files of the same tree because the three
slides explain it three different ways.

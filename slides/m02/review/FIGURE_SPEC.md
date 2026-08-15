# m02 FIGURE_SPEC

All figures come from `figures/make_figures.py` (TikZ → pdflatex → pdftoppm), the WS
animation from `figures/make_animations.py`, which imports geometry and palette from
`make_figures.py` so the two cannot drift. Per `FIGURE_GUIDE.md`: TikZ for node-link
diagrams, hand-drawn axes for the two data figures (no matplotlib, no bar charts, no green).

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

Single characters only inside a disc; every word-length label goes outside it.
At 30 pt a label is ~15 px per character on the slide, so a 520 bp column figure holds
about 34 characters across. Labels are therefore one or two words, never a phrase.

## Assertions in the generator (build fails, not review finds)

1. `H ≤ 0.7076 · W` — width binds, so the scale table above is the real scale.
2. Ink fills ≥ 76 % of the canvas on **both** axes (≤ 24 % margin per axis, under
   `check_render.py`'s 30 % warn and giving ink fraction ≥ 0.58 against its 0.15 fail).
3. Every disc drawn at `NODE = 40` bp; on-slide diameter recomputed from the actual file
   size and asserted inside 26–52 px.
4. Every font size used is ≥ `FONT_MIN = 30` pt; on-slide cap height recomputed and
   asserted ≥ 21 px.
5. Palette membership: every colour emitted is one of the five tokens.
6. **Graph arithmetic is computed, never typed.** Every number a figure prints (distance,
   C_i, C̄, C, L̄, diameter, σ) is computed by `networkx` inside the generator and
   cross-checked against `DECK_SPEC.md`'s verified table; a mismatch fails the build.
7. Edge–disc clearance: no edge may pass through a disc it does not terminate at
   (the m01 ring-lattice defect). Checked geometrically for every straight edge.

## Palette

`accent #3959A6` · `accent-2 #B14434` · `accent-3 #DAB167` · `gray #6b6b6b` · `ink #000000`.
One meaning per figure, stated in the figcaption or an in-figure label:
- accent — the object under discussion (nodes, the current network)
- accent-2 — **the thing the slide is about** (the highlighted path, the triangle, the shortcut)
- accent-3 — the secondary comparison object (the longer route, the random baseline)
- gray — annotation only

## Figures

Canvas column: `c` = 520 × H (in `cols`), `f` = 1100 × H (full width).

### Part 1

| file | canvas | content | encoding stated |
|---|---|---|---|
| `milgram-map` | c 520×330 | Omaha and Wichita (left) and Boston (right) as labelled dots on a schematic US frame; dashed arc from each source to the target; "≈ 1,900 km" | accent-2 = the target |
| `milgram-rule` | c 520×300 | three people in a row; the middle one holds the packet; arrow forward labelled "someone you know by first name" | accent-2 = the packet's next hop |
| `milgram-arrivals` | f 1100×260 | 160 small discs in a grid; 64 filled accent-2, 96 outline-only; label "64 arrived · 96 died" | accent-2 = arrived |
| `milgram-chain` | f 1100×250 | 7 discs left→right, labels farmer · buyer · teacher · minister · printer · clerk · broker; 6 edges | accent-2 = the target (broker) |
| `six-degrees-timeline` | c 520×300 | a vertical line with 1967 (experiment) and 1990 (Guare's play) marked | accent-2 = the phrase's real origin |
| `replication-yahoo` | c 520×260 | a number line 0–8 in "steps"; dots at 6 (Milgram) and 4 (Yahoo) | accent-2 = the newest measurement |
| `replication-facebook` | c 520×260 | same line, third dot at 4.74 (Facebook) | accent-2 = the newest measurement |
| `wikirace` | c 520×320 | four article discs, arrows forming one route from a start to a target | accent-2 = the route found |
| `routing-vs-existence` | c 520×330 | one graph; the short route drawn accent-2, the greedy dead-end drawn accent-3 dashed | stated in the figcaption |

### Part 2 — one drawing routine, `milgram_graph(edges, highlight, labels)`

Base geometry: 7 nodes on a wide flat arc, positions fixed once so the graph never moves
between consecutive slides.

| file | canvas | content |
|---|---|---|
| `chain-graph` | f 1100×250 | the 7 nodes as discs, names beneath, 6 chain edges |
| `distance-def` | c 520×300 | 3 of the nodes, the 2 edges between them counted "1, 2" |
| `chain-blank` | f 1100×250 | chain, endpoints ringed accent-2, no counts |
| `distance-six` | f 1100×250 | chain with the six edges numbered 1…6 |
| `chain-chord` | f 1100×250 | chain + chord 0–2, the chord accent-2 |
| `two-routes` | f 1100×250 | 0→2 direct (accent-2) and 0→1→2 (accent-3, dashed) |
| `apl-chain` | c 520×340 | 21 dots stacked over distances 1–6 (6,5,4,3,2,1), mean line at 2.67 |
| `chain-shortcut` | f 1100×250 | chain + chord + shortcut 1–5, shortcut accent-2 |
| `apl-shortcut` | c 520×340 | 21 dots restacked (mean 1.81), same axis as `apl-chain` |
| `diameter` | f 1100×290 | two rows: before (worst pair 0–6, d=6) and after (worst pair, d=3) |
| `worksheet-a` | f 1100×250 | full graph, nodes lettered A–G, no numbers at all |
| `worksheet-a-answer` | f 1100×280 | the same, with the three asked distances drawn and L̄ = 38/21 |

Assertions: distances, L̄ and diameter are read from `networkx` on the exact edge set,
and must equal 8/3 & 6 (chain) and 38/21 & 3 (with both extra edges).

### Part 3

| file | canvas | content |
|---|---|---|
| `triangle-triplet` | c 520×280 | left: closed triplet (3 edges, accent-2); right: open triplet (2 edges) |
| `ego-graph` | c 520×340 | centre A + 5 neighbours, star edges only |
| `ego-pairs` | c 520×340 | same, with all 10 neighbour pairs dashed gray |
| `ego-pairs-count` | c 520×340 | same, the 10 dashed pairs numbered |
| `ego-clustering` | c 520×340 | 2 of the 10 solid accent-2, the other 8 dashed gray; "2 / 10" |
| `a3-walks` | c 520×300 | one triangle at i; the two closed 3-walks drawn as curved arrows, one each direction |
| `a3-formula` | c 520×300 | the same triangle with (A³)_ii = 2 and k(k−1) = 2 marked on it |
| `cbar-milgram` | f 1100×290 | the Milgram graph with C_i printed above each node; mean marked |
| `windmill` | c 520×340 | hub + 5 blades, nothing numbered |
| `windmill-split` | c 520×340 | same, C_i on every node (1 ten times, 1/9 at the hub) |
| `transitivity-def` | f 1100×300 | the windmill with its 5 triangles shaded and the hub's 45 triplets fanned |
| `worksheet-b` | f 1100×250 | Milgram graph, nodes lettered, degrees shown, no C values |
| `worksheet-b-answer` | f 1100×280 | the three asked C_i values on their nodes |

Assertions: `nx.clustering`, `nx.average_clustering`, `nx.transitivity` on the exact graphs;
windmill must give C_i = 1 (×10) and 1/9, C̄ = 91/99, C = 3/11, 5 triangles, 55 triplets.

### Part 4

| file | canvas | content |
|---|---|---|
| `paradox` | f 1100×300 | a triangulated local patch on the left, a distant target on the right, the many-hop route drawn gray, "4.74?" in accent-2 |
| `complete-graph` | c 520×340 | K₆, every edge, C = 1 and L = 1 labelled |
| `baseline-idea` | c 520×300 | the same node/edge count shuffled into a structureless graph, captioned "same size, no structure" |
| `er-coin` | c 520×340 | 6 nodes; every pair drawn faint, the realised ones solid; "p" on one pair |
| `er-clustering` | c 520×340 | an ego with 5 neighbours; each of the 10 neighbour pairs marked with its own coin symbol |
| `fanout` | f 1100×320 | 1 → k → k² branching over three rings, counts labelled |
| `fanout-solve` | f 1100×300 | the same rings with ⟨k⟩^L = n solved: 150^L = 8×10⁹ → L = 4.55 |
| `free-vs-not` | c 520×340 | one random graph with a short route traced accent-2 and "0 triangles" annotated |
| `sigma-def` | c 520×300 | the two ratios drawn as two horizontal gauges against a σ = 1 tick |
| `ws1998-dots` | f 1100×320 | log axis 1–10⁴; per network a gray dot at L/L_rand and an accent-2 dot at C/C_rand, joined by a rule; three rows |
| `ws1998-sigma` | f 1100×300 | the three σ values (2400, 11, 4.8) on a log axis with σ = 1 marked |

Assertions: ratios recomputed from the Table 1 constants at the top of the generator;
σ printed = (C/C_rand)/(L/L_rand) to the same rounding as the deck text.

### Part 5

| file | canvas | content |
|---|---|---|
| `ring-lattice` | c 520×340 | n = 20, k = 4 ring; the chords must clear every disc they pass |
| `ring-distance` | c 520×340 | same ring, the antipodal shortest route accent-2, "5 hops" |
| `random-graph` | c 520×340 | ER with the same n and m, seeded |
| `lattice-vs-random` | f 1100×330 | the two side by side, C and L annotated under each |
| `ws-rewire-step` | c 520×340 | one edge caught mid-move: old end dashed gray, new end accent-2 |
| `ws-rewire.gif` | c 520×340 | 24 frames, one rewiring per frame, same ring geometry |
| `ws-sweep` | f 1100×330 | C(p)/C(0) accent-2 and L(p)/L(0) accent, log-p axis, hand-drawn axes |
| `ws-band` | f 1100×330 | same curves, the small-world band shaded accent-3 |
| `ws-widget` | c 520×320 | a still of the marimo widget's ring, captioned |
| `shortcut-effect` | c 520×340 | one shortcut on the ring; the node pairs it shortens shaded accent-3 |

Assertions: the sweep is measured, not drawn from memory — own BFS + clustering, seeded,
n = 400, k = 8, 13 values of p, 8 realisations. C(0) = 0.643 and L(0) = 25.44 must match
the DECK_SPEC table. Ring chords are checked for disc clearance.

### Part 6 and wrap-up

| file | canvas | content |
|---|---|---|
| `disconnected` | c 520×300 | two components, the cross-component pair ringed |
| `disconnected-answer` | c 520×300 | same, that pair labelled d = ∞ |
| `degree-one` | c 520×300 | a node with exactly one neighbour, ringed |
| `degree-one-answer` | c 520×300 | same, "k(k−1)/2 = 0" written at the node |
| `sigma-lt-1-q` | c 520×340 | the ring lattice again, ringed as the tempting guess |
| `grid-no-triangles` | c 520×340 | a 5×5 patch of a square grid, "no triangle anywhere" |
| `gnm-gnp` | c 520×320 | left: a bag of m edges being dealt; right: a coin per pair |
| `gnm-gnp-answer` | c 520×320 | same, with "independent" marked on the coin side only |
| `universality` | f 1100×300 | five domain names on a σ axis, all right of σ = 1 |
| `sw-map` | f 1100×320 | p axis from lattice to random, WS between, C and L bands above |
| `recap` | c 520×340 | the Milgram graph one last time with d, C and σ labelled |
| `m03-teaser` | c 520×340 | the ring with shortcuts, two of them cut accent-2 |

## Never shared between slides

Every question/answer pair emits **two files**, even when only one label differs
(`worksheet-a` / `worksheet-a-answer`, `windmill` / `windmill-split`, …). This is the m01
regression that put an adjacency matrix on a slide 41 earlier than its definition.

# m05 FIGURE_SPEC

Every figure for `m05-clustering.md`, authored per `FIGURE_GUIDE.md`: TikZ through
`figlib.py`, one bp = one slide pixel, assertions in the generator, no matplotlib, no
green, no bar charts.

## Files

    figures/verify_numbers.py   every number, computed and asserted (already green)
    figures/layout.py           the club's reference layout, solved once and cached
    figures/karate-layout.json  the cache: 34 positions + the crossing count they were checked at
    figures/kfig.py             drawing helpers shared by every figure module
    figures/figs_story.py       Parts 1-3   the club, the patterns, the cut
    figures/figs_chance.py      Parts 4-6   modularity, Louvain, SBM
    figures/figs_doubt.py       Parts 7-9   the three lies, evaluation, the close
    figures/make_figures.py     entry point; catches per figure, exits non-zero at the end
    figures/make_animations.py  kcore-peel.gif, balls-strings.gif, louvain.gif

## Containers

Read out of `network-science.css` and re-checked by `check_render.py`:

| container | authored width | height cap |
|---|---|---|
| `full` | 1080bp | 380 (`tight` 320, `stack` 190) |
| `col` (inside `cols`) | 537bp | same caps |

A figure authored for `full` and dropped into a `cols` column renders at 48%. The
generator declares the container; `check_render.py` parses the deck for the one actually
used and fails on a mismatch.

## The reference layout — the single biggest risk in this deck

The club has **34 nodes and 78 edges and is not planar**, so F2's "draw it planar" is
unreachable. `layout.py` anneals from a spring layout (which lands at 79–94 crossings on
its own) under three hard constraints and caches the result:

- centres at least **46bp** apart, with **34bp** discs — 12bp of white between neighbours
- no edge within **20bp** of a disc it does not end at
- everything inside the box, since ink past the page edge is clipped silently

`load()` re-checks all three on every import, so a hand-edited cache fails the build.

Fourteen figures share it. **They recolour; they never move a disc.** The lesson this
encodes is m01's: the same network redrawn between consecutive slides makes the room
re-learn the picture instead of reading the change.

Where a *mechanism* is being explained — cut, ratio cut, the configuration model,
conductance, k-plex — the figure uses a purpose-built planar graph of 5–10 nodes and
`assert_planar_drawing()` demands **zero** crossings. A mechanism slide must never ask
the room to trace a line through 81 crossings.

## Colour contract (F1: one colour, one meaning, per figure)

| token | meaning in this deck |
|---|---|
| accent `#3959A6` | Mr. Hi's club, or "the group under discussion" |
| accent-2 `#B14434` | the officers' club, or "what THIS slide is about" |
| accent-3 `#DAB167` | fills and highlight rings only — never text, never a thin stroke (2.0:1 on white) |
| gray `#6b6b6b` | annotation, and members not currently in play |
| ink `#000000` | edges |

Two clubs, two colours: **accent is Mr. Hi throughout the deck**, on every one of the
fourteen club figures. Nothing else may borrow those two colours on a club figure.

## Stills

### Part 1 — the club (slides 4–14)

| # | file | container | content | assertions beyond the standard gates |
|---|---|---|---|---|
| 1 | `timeline-1970.png` | full/tight | a bare year line: 1970 observation begins · 1972 the club splits · 1977 the paper | ends inside the canvas; the three stops are in date order |
| 2 | `the-dispute.png` | full | two large discs — Mr. Hi (accent) and John A. (accent-2) — with the fee dispute between them and 32 gray discs ranged behind | the two named discs are the only coloured ones |
| 3 | `karate-plain.png` | full | the reference layout, **every disc gray**, all 78 edges black | no colour anywhere; 34 discs, 78 edges drawn |
| 4 | `karate-three-guesses.png` | full | the same layout with three different dividing lines drawn as gray dashed curves, labelled A B C | the three lines separate the node set three *different* ways, computed and asserted |
| 5 | `karate-split.png` | full | the recorded outcome: 17 accent, 17 accent-2 | the two colour counts are both 17, read from the `club` attribute |
| 6 | `karate-crossing.png` | full | the same, with the 11 crossing edges heavy accent-3 and the two internal counts printed | exactly 11 edges are drawn heavy; 35 + 32 + 11 = 78 |
| 7 | `why-groups.png` | full | one drawing, four labelled regions — same kind · same job · same rank · same channel — not four panels | the four labels do not collide (solver) |
| 8 | `ground-truth-or-not.png` | full | left: a small network with its answer written on it. right: the same network with a question mark where the answer would be | the two graphs are the same graph |

### Part 2 — patterns (slides 16–26)

| # | file | container | content | assertions |
|---|---|---|---|---|
| 9 | `clique-def.png` | col | a 5-clique beside a 5-node graph missing one edge | the first has all 10 edges, the second 9 |
| 10 | `karate-max-clique.png` | full | the reference layout, the five members of a maximum clique ringed accent-2, everyone else gray | the ringed set is a clique of size 5 in the real graph and contains node 0 |
| 11 | `k-plex.png` | col | a 6-node 2-plex, the missing edges dashed | every node is adjacent to all but at most 2 |
| 12 | `rho-dense.png` | col | an 8-node subgraph at density 0.5, with the count of present vs possible edges | the drawn density equals the printed one |
| 13 | `n-clique.png` | col | a 6-node graph, diameter 2, with one 2-step path traced | the traced path has exactly 2 hops and the graph's diameter is 2 |
| 14 | `k-truss.png` | col | a 7-node graph where every edge lies in ≥ 1 triangle, one edge's two triangles shaded | the shaded edge's triangle count equals the printed one |
| 15 | `patterns-overlap.png` | full | the club with four pattern-groups shaded in accent-3, overlapping, several members in none | the four sets genuinely overlap and do not cover all 34 |

### Part 3 — the cut (slides 28–39)

The small club: nine members, two 4-cliques joined by two friendships, one member with a
single friend. Drawn planar; zero crossings asserted.

| # | file | container | content | assertions |
|---|---|---|---|---|
| 16 | `cut-idea.png` | full | the small club with a dashed line falling between the two halves | planar, 0 crossings |
| 17 | `cut-def.png` | col | the same, the 2 crossing edges accent-2, "cut = 2" | the highlighted count equals the computed cut |
| 18 | `two-cliques.png` | full | the demo network: two 5-cliques, one joining edge | 21 edges, both cliques complete |
| 19 | `karate-trivial-cut.png` | full | the club with node 12 (the only member with one friend) peeled off, its single edge accent-2 | that node's degree is 1 in the real graph |
| 20 | `ratio-cut.png` | full | the small club twice: peel-the-leaf (1/8) beside the sensible split (1/10) | both fractions recomputed from the graph |
| 21 | `normalizer-curve.png` | full | \|V₁\|·\|V₂\| against the size of the smaller side, peak at the halfway point | the peak is at n/2 and the drawn points match the formula |
| 22 | `norm-cut.png` | full | the small club with \|E₁\| = 7 and \|E₂\| = 6 marked, 2/(7·6) = 1/21 | the two edge counts are computed, not typed |
| 23 | `k-way-cut.png` | full | one graph split three ways, each group's escaping edges counted on the drawing | the three counts sum to twice nothing — each edge is counted once per endpoint group |
| 24 | `karate-mincut.png` | full | Zachary's min cut: predicted sides in accent / accent-2, the single disagreement ringed accent-3 | the prediction is recomputed by max-flow and agrees on 33 of 34 |
| 25 | `karate-node9-ring.png` | full | the club, all gray, one ring | the ringed node is 0-indexed 8 |

### Part 4–6 — chance, climbing, SBM (slides 41–72)

| # | file | container | content | assertions |
|---|---|---|---|---|
| 26 | `chance-idea.png` | full | two graphs with the same cut, one surprising and one not | the two cuts are equal, computed |
| 27 | `observed.png` | full | six strings drawn from the bag, the matching ones marked | the marked fraction equals the printed one |
| 28 | `bag-2m.png` | full | a bag holding 2m balls, one member's k balls picked out | ball count = 2m for the drawn graph |
| 29 | `expected.png` | full | two balls drawn independently, the match probability built from the two colour shares | shares sum to 1 |
| 30 | `modularity-gap.png` | full | one axis, observed and expected marked, the gap named Q | gap = observed − expected to the printed precision |
| 31 | `modularity-matrix.png` | full | one cell A_ij beside its null term k_ik_j/2m, on a 6-node graph | the printed k_i, k_j, m come from the graph |
| 32 | `configuration-model.png` | full | before: a graph. after: a rewiring with identical degrees | the degree sequences are equal, asserted |
| 33 | `worksheet-q.png` | full | two triangles joined by one edge, degrees printed, no answer | m = 7; **no Q value anywhere in the figure** |
| 34 | `worksheet-q-answer.png` | full | the same, with 5/14 and the two rival groupings scored | the three values recomputed |
| 35 | `q-picks-k.png` | full | one graph scored at K = 1, 2, 3 | the three Q values recomputed; K = 2 wins |
| 36 | `bell-growth.png` | full | ways to partition n people, log y, up to n = 34 | the plotted values are Bell numbers |
| 37 | `leiden-fix.png` | full | a community Louvain returns in two disconnected pieces | the drawn group is genuinely disconnected |
| 38 | `four-answers.png` | full | one graph under four different partitions | the four partitions are pairwise different |
| 39 | `sbm-flip.png` | full | groups → block matrix → network, left to right | — |
| 40 | `sbm-blocks.png` | full | an adjacency matrix sorted by group, blocks visible | the drawn cells match the drawn graph |
| 41 | `block-matrix.png` | full | a 2×2 block matrix with its probabilities | — |
| 42 | `sbm-three-cases.png` | full | p_in > p_out · p_in < p_out · p_in = p_out, as three matrices with the networks they make — **a build, one case per reveal on the slide** | each drawn network's measured block densities match its matrix |
| 43 | `sbm-pattern.png` | full | a group whose members share no edge with each other and are still a group | the group has 0 internal edges, asserted |
| 44 | `sbm-inference.png` | full | candidate assignments scored by likelihood, the best marked | the marked one is the argmax of the computed values |
| 45 | `sbm-shuffled.png` | full | the same matrix with rows and columns shuffled — no blocks visible | it is a permutation of `sbm-blocks`, asserted |

### Part 7–9 — doubt and close (slides 74–106)

| # | file | container | content | assertions |
|---|---|---|---|---|
| 46 | `two-cliques-split.png` | full | the two cliques, split, Q = 0.4524 against 0.0000 | both recomputed |
| 47 | `big-clique-net.png` | full | the 50-node demo: the same two cliques plus a 40-node block | the two cliques are identical to `two-cliques.png`'s, asserted node for node |
| 48 | `resolution-limit.png` | full | before / after: the two cliques separate, then merged | Q(merged) > Q(split) in the second, recomputed |
| 49 | `sqrt2m.png` | full | √(2m) against m, with both demo networks placed on it | both placements recomputed |
| 50 | `non-local.png` | full | the two cliques, unchanged, in two different networks | the two subgraphs are identical |
| 51 | `degeneracy.png` | full | a one-dimensional cut through the Q landscape, many peaks of nearly equal height, the top two marked 0.4198 and 0.4151 | the two marked values come from the Louvain runs |
| 52 | `random-net.png` | full | the 40-node random demo network | 41 edges |
| 53 | `random-q-dots.png` | full | 200 dots — the Q of 200 random graphs with the club's 34 nodes and 78 edges — with the real split's 0.358 marked | all 200 above 0.3; the mark is at the computed value |
| 54 | `three-partitions.png` | full | the club under min cut, under Louvain, and as it happened | all three recomputed |
| 55 | `conductance-def.png` | col | one group, its escaping edges and its volume marked | both counts computed |
| 56 | `conductance-karate.png` | full | the club's real split with 11/75 on it | recomputed |
| 57 | `scores-disagree.png` | full | the two rankings, conductance and modularity, disagreeing about the same two partitions | both recomputed |
| 58 | `pairs-15.png` | full | six members, fifteen pairs drawn as fifteen links | C(6,2) = 15 asserted |
| 59 | `mutual-information.png` | full | two labellings over the same six members and what they share | — |
| 60 | `nmi-formula.png` | full | the normalisation, H(X) and H(Y) drawn as lengths | the drawn lengths are proportional to the computed entropies |
| 61 | `worksheet-nmi.png` | full | six members, truth 3+3, one placed wrongly — **no score anywhere** | no number in the figure is a score |
| 62 | `worksheet-nmi-answer.png` | full | the same with NMI 0.479 and Rand 10/15 | both recomputed |
| 63 | `ari.png` | full | the same pairs with the chance level subtracted, landing at 0.324 | recomputed |
| 64 | `nmi-vs-ari.png` | full | one partition scored both ways, showing which direction each is generous in | both recomputed |
| 65 | `best-vs-real.png` | full | Louvain's four groups beside the real two, Q printed on each | 0.4198 and 0.3582, recomputed |
| 66 | `nmi-comparison.png` | full | the same two partitions scored against the recorded outcome: 0.588 against 0.837 | recomputed |
| 67 | `node9.png` | full | the club, node 9 ringed, the structural prediction and the actual choice both marked | the two differ, recomputed from the min cut |
| 68 | `no-free-lunch.png` | full | the same network, three methods, three answers, no arbiter | — |
| 69 | `applications.png` | full | one citation-like network coloured by field | — |
| 70 | `recap.png` | full | the four acts as one drawing | — |
| 71 | `m06-teaser.png` | full | the club with Mr. Hi and John A. drawn large, degrees 16 and 17 printed | the two degrees come from the graph |

## Animations (`make_animations.py`)

Geometry, palette and graph data are imported **from** the figure modules, so a frame
cannot drift from the still beside it. Every frame of one GIF is cropped to the same box —
the union of the ink across frames — so nothing jumps, and the size gates are then applied
to that box exactly as `emit()` applies them to a still.

| file | frames | content |
|---|---|---|
| `kcore-peel.gif` | 5 | the club, peeling everyone below degree k, k = 1 … 4; settles on the 4-core's 10 members and holds |
| `balls-strings.gif` | 4 stages | pull a string · the ends match or do not · cut every string, balls into the bag · draw two balls |
| `louvain.gif` | ~10 | phase one, nodes moving one at a time; phase two, each group collapsing to a single disc; ends on the four-community state the neighbouring still uses |

Each GIF loops back to the frame its neighbouring still shows, so the loop hands off
instead of resting somewhere arbitrary.

## Gates the generator runs on every figure

From `figlib.py`, unchanged:

- page width exactly the container's, ink not touching any edge (clip, not crop)
- height must not bind the scale — if it does, the drawing is too tall, and the message
  says shorten it rather than shrink the type
- ink spans ≥ 76% of the canvas width
- node discs land 26–52px on the slide
- in-figure x-height ≥ 15.5px on the slide, against a **measured** calibration glyph, not
  a quoted ratio
- labels placed by the backtracking solver against every other label, every disc
  including their own, every drawn edge and the canvas bounds; failure stops the build
  and says *do not shrink the type*

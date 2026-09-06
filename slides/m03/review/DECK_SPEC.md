# m03 deck spec — 32 slides

Rewrite of 2026-09-06. The old 76-slide spec is in git history (commit 48832115).

## What changed and why

The pen-and-paper sheet (`lecture-note/m03-robustness/pen-and-paper/exercise.tex`) now
runs **before** the lecture. On it the students already:

| sheet | what they did | what the deck no longer has to do |
|---|---|---|
| Q1 | built a least-cost connected grid on nine stations | discover "loops are waste"; a *Your turn* MST slide |
| Q2 | compared the order of adding lines with a neighbour | motivate greedy, and show two orders landing on one total |
| Q3 | counted routes between two stations | derive "a tree has exactly one route" |
| Q4–Q6 | tabulated the largest component after each single failure | define connectivity from scratch; poll for the worst station |
| Q7–Q8 | plotted two removal orders and estimated the area | build the robustness profile and the R-index by hand |
| Q9 | said in their own words why one order hurts more | argue random-vs-targeted from first principles |
| Q10–Q11 | redesigned the grid against a 1- and 2-station attack | run the design exercise cold |

So Build-it and Break-it shrink to **naming what they already have in their hands**, and
the deck's weight moves to what the sheet cannot teach: percolation, q(k), κ,
Molloy–Reed, f_c, and robust-yet-fragile.

Their own numbers, for the callbacks. The sheet's cost table has a unique MST: a **star on
station B**, total **32**, so losing B alone leaves 2 of 9 connected. Question 8 asks them
to *estimate the area* under each curve they plotted on axes 0–9 by 0–1, which comes out
near **0.5** for order R and near **0.23** for order T. (The deck's own R-index — the mean
of the intermediate connectivities only — would be 0.39 and 0.12 on that grid. Quote the
areas, not these, or the room's arithmetic will not match yours.) None of these numbers is
printed on a slide; they are in the speaker note for slide 11.

## Rules carried over

Fragments use `*`. No tables, no code. `cols` is text + figure only. Question and answer
never share a slide, and the answer appears nowhere on the question slide — notes
included. Every concept slide has a figure. Type floors are the theme's.

**New in this revision.** One to two minutes per slide, and the room cannot read a
paragraph in that time:

- **At most two lines of body text on any slide.** The title carries the claim; the
  figcaption carries what the drawing does not say; everything else is spoken. Two lines
  is not a style preference: a third line pushed five slides past CONTENT_BOTTOM here.
- **Animation first, then the still.** Where a stage exists, it comes *before* the static
  figure that freezes its last frame.
- **Every term is defined where it is first used, and used precisely afterwards.**
  spanning tree, minimum spanning tree, connectivity, R-index, random failure, targeted
  attack, cluster, percolation threshold, phase transition, q(k), kappa, branching factor,
  f, critical fraction. No analogy stands in for a definition: the percolation half is
  stated as site percolation on a square lattice with occupied cells and clusters, not as
  rain on paving stones, and the removal orders are named random failure and targeted
  attack, not luck and intent.
- **No rhetoric.** No build-up, no figure of speech, no sentence that carries no fact.

## The working graph

Eight Moravian towns, thirteen cables, weights distinct so the MST is unique (292 km).
Positions are **designed, not geographic** — the lecturer's call: the true lat/lon put
Prostějov and Olomouc 59 bp apart on a 1100 bp canvas, with three weight labels
overlapping in the corner. The new layout is a fan around Brno, planar, minimum
node-node distance **160 bp**. Same towns, same weights, same MST.

## Slides

| # | class | title | figure / stage | point |
|---|---|---|---|---|
| 1 | lead | Build it, Break it | — | title |
| 2 | mid | The question for today | — | how much can you destroy, and does the attacker matter |
| 3 | part | **Build it** | — | divider |
| 4 | — | Moravia, 1926 | boruvka-portrait | a real question to a real mathematician; the MST is born |
| 5 | — | What you drew on paper has a name | mst-def | connected, no loops, n−1 cables, least total = **minimum spanning tree** |
| 6 | — | Kruskal and Prim | **stage mst-race** | two greedy rules that return the same tree; scene 4 is the cut property |
| 7 | part | **Break it** | — | divider |
| 8 | mid | Which removal costs the most? | mst-blank | Q — poll the room |
| 9 | — | Removing Brno leaves components of 3, 3 and 1 | brno-removed | A — **connectivity** = largest component / n |
| 10 | — | Take them one at a time | **stage break-profile** | the profile draws itself; R is its area; order changes it |
| 11 | — | Random failure against targeted attack | profile-both | **R-index** defined; 0.41 against 0.17; links the live tool |
| 12 | mid | Measured, or computed? | — | Q — the cliffhanger into Part 3 |
| 13 | part | **Predict it** | — | divider |
| 14 | mid | Site percolation | lattice-low | Q — at which p does the largest cluster span the lattice |
| 15 | — | Raising the occupation probability | **stage percolation** | drag p across the threshold by hand |
| 16 | — | The percolation threshold | phase-transition | **phase transition** at p_c ≈ 0.59; attack is the same run backwards |
| 17 | mid | Same n and m, different thresholds | — | Q — what property of the network decides |
| 18 | — | The node at the end of a random edge | **stage branch-out** | edge ends → ⟨k⟩ against κ → κ−1 → the dial for f |
| 19 | — | q(k) and kappa | kappa-def | κ is the mean degree under q, not under p |
| 20 | — | Molloy–Reed | molloy-reed | **branching factor** κ−1; giant component exactly when κ > 2 |
| 21 | — | Removing a fraction f | fc-formula | **f** defined here, one slide after the stage that uses it; drawn at κ = 3 so f_c = 0.50 |
| 22 | — | Poisson degrees | fc-poisson | f_c = 1 − 1/⟨k⟩; ⟨k⟩ = 4 → 75% |
| 23 | mid | What if the degree distribution has hubs? | — | Q — what happens to ⟨k²⟩ |
| 24 | — | For 2 < γ < 3, kappa diverges | fc-scalefree | ⟨k²⟩ unbounded ⇒ κ → ∞ and f_c → 1 |
| 25 | part | **Design it** | — | divider |
| 26 | mid | Does f_c → 1 mean the network cannot be broken? | — | Q — f_c was derived for random removal |
| 27 | — | Two networks with the same degree sum | **stage rf-attack** | random failure, then targeted attack |
| 28 | — | Robust yet fragile | robust-fragile | the hubs that raise f_c are the first nodes an attack removes |
| 29 | mid | Two extra edges | mst-blank-design | Q — which two, and what does the network gain |
| 30 | — | Two edges that close a cycle | redundant-answer | +136 km: worst removal 3/8 → 6/8, R 0.17 → 0.27 |
| 31 | — | Module 03 summary | recap | 292 km, Brno removed, two edges added |
| 32 | — | Coming up in Module 04 | m04-teaser | the same q(k) bias, applied to friends |

## Milestones (S5)

- Part 1 — stage `mst-race`, stepped by hand
- Part 2 — the poll on slide 8, stage `break-profile`, and the live tool linked on slide 11
- Part 3 — stages `percolation` and `branch-out`
- Part 4 — stage `rf-attack` and the designer discussion on slide 29

## Four-act arc (S1–S4)

Act 1 story = slides 4–6 (Moravia, 1926, Borůvka, real names and dates).
Act 2 = the same grid broken, slides 8–12.
Act 3 = the general law, slides 14–24.
Act 4 = the paradox and the design question, slides 26–30, every beat posed as a question
before it is answered.

## The five stages

Each carries its own scene notes twice: `note` is the lecture note's account of a drawing
its reader cannot see, and `short` is the one line a slide shows instead — the kit takes
`short` whenever `window.animStepOnly` is set, which is every deck.

Type inside a stage is **1.5x** the note's, and each scene shows **at most four pieces of
text**: the label in the bar, the one-line note, the readout of numbers, and a two-part
verdict. No captions. Measured on the rendered slides, the visible text per scene summed
over the five stages fell from **1181 to 634 characters**.

    mst-race        6   Kruskal, Prim, and the cut property
    break-profile  10   the profile drawn one removal at a time, and its area
    percolation    15   the lattice, with p on a dial
    branch-out     18   edge ends, <k> against kappa, kappa-1, and the dial for f
    rf-attack      27   random failure and targeted attack on two networks

All five are also mounted in `lecture-note/m03-robustness/01-concepts.qmd`, from the same
files. `percolation` replaced a `TODO(anim)` the note had been carrying for the lattice
dial; `break-profile` follows the static robustness-profile figure; `branch-out` follows
the f_c formula, where the note's own prose says "follow a cable out of a town and arrive
somewhere" and had nothing to show for it.

`branch-out` was rebuilt after the first version was found hard to follow. The first two
scenes looked identical — a node flashed either way — so nothing on screen showed what
"draw an edge end" meant. It now opens on the twenty edge ends themselves, one column of
squares per node, and scenes 2 and 3 draw from the ten column heads and from the twenty
squares respectively, with both running means left side by side at the end: 2.00 and 3.00.
The branching fan is a real binary tree (children under their parent), and `f` is named on
screen in scene 5 and defined again on slide 21.

## The kappa network

Slides 18–21 all argue over one network, and it is chosen so nothing has to be rounded:
ten towns, ten cables, degrees 5 4 3 2 1 1 1 1 1 1. Then ⟨k⟩ = 2, ⟨k²⟩ = 6, **κ = 3**,
the branching is **κ − 1 = 2** (so the search doubles and the fan is drawable), and
**f_c = 0.50** exactly. Its one cycle is four towns long, so it has no triangle and the
branching argument's own assumption holds on the picture it is argued over.

The `branch-out` stage and `figures/kappa-def.png` draw it at the same positions, and
`figures/fc-formula.png` is drawn for the same κ — so the dial the room turns on slide 18
and the line on slide 21 are one fact, not two.

## Figures retired

abstract-1/2/3, moravia-dark, moravia-graph, loop-waste, tree-def, spanning-count,
tree-bridges, connectivity-def, cut-property, kruskal-*, prim-*, boruvka*, tie-*,
r-index, profile-build.gif, profile-random, demo-still, order-irrelevant,
reverse-percolation, puddle-sweep.gif, puddle-widget, follow-edge, qk-bias, branching,
dilution, kappa-worksheet, kappa-answer, er1-*, betweenness-*, triangles-*, ring-*,
sim-*, design-principles, efficiency-security, fixed-vs-adaptive, real-grid-mesh,
prim-vs-kruskal, mst-alone, build-it-back.

What they taught is either on the sheet already, or is now a beat inside one of the five
stages. `figures/make_animations.py` and its five GIFs went with them: no slide uses a GIF
any more, and every animation in the deck is a stage the lecturer steps by hand.

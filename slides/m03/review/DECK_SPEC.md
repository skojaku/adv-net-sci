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
  figcaption carries what the drawing does not say; everything else is spoken.
- **Animation first, then the still.** Where a stage exists, it comes *before* the static
  figure that freezes its last frame — the room watches the mechanism, then reads it.

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
| 6 | — | Kruskal and Prim, one grid | **stage mst-race** | two greedy rules that cannot disagree; scene 4 is the cut property |
| 7 | part | **Break it** | — | divider |
| 8 | mid | Which town, gone dark, hurts most? | mst-blank | Q — poll the room |
| 9 | — | Brno: eight towns become 3, 3 and 1 | brno-removed | A — **connectivity** = largest piece ÷ original |
| 10 | — | Take them one at a time | **stage break-profile** | the profile draws itself; R is its area; order changes it |
| 11 | — | Bad luck against bad intent | profile-both | R = 0.41 vs 0.17, 2.4× on the same grid; links the live tool |
| 12 | mid | How much has to fail before it fragments? | — | Q — the cliffhanger into Part 3 |
| 13 | part | **Predict it** | — | divider |
| 14 | mid | The puddle yard | puddle-low | Q — at which p does one puddle span it |
| 15 | — | Turn the rain up | **stage percolation** | drag p; the giant puddle arrives all at once |
| 16 | — | It happens all at once | phase-transition | **phase transition** at p_c ≈ 0.59; attack is the same run backwards |
| 17 | mid | Same size, opposite fates | — | Q — what would you need to know to tell them apart |
| 18 | — | Follow an edge, not a node | **stage branch-out** | q(k) bias → κ → κ−1 → dilute by (1−f) → the threshold |
| 19 | — | The number is kappa | kappa-def | κ = ⟨k²⟩/⟨k⟩, large exactly when there are hubs |
| 20 | — | Molloy–Reed | molloy-reed | a giant component exists exactly when κ > 2 |
| 21 | — | The critical fraction | fc-formula | (1−f)(κ−1) = 1 ⇒ f_c = 1 − 1/(κ−1), drawn at the stage's own κ = 3 so f_c = 0.50 |
| 22 | — | A network without hubs | fc-poisson | Poisson: f_c = 1 − 1/⟨k⟩; ⟨k⟩ = 4 → 75% |
| 23 | mid | And a network with hubs? | — | Q — what happens to ⟨k²⟩ |
| 24 | — | Kappa blows up, f_c → 1 | fc-scalefree | 2 < γ < 3 ⇒ κ → ∞ |
| 25 | part | **Design it** | — | divider |
| 26 | mid | So a hub network is indestructible? | — | Q |
| 27 | — | Thirty towns, sixty cables, two designs | **stage rf-attack** | the dice, then the adversary |
| 28 | — | The same hubs, both ways | robust-fragile | **robust yet fragile** |
| 29 | mid | You are the designer | mst-blank-design | Q — two extra cables; where, and what does the money buy |
| 30 | — | Close the ring in the south | redundant-answer | +136 km: worst loss 3/8 → 6/8, R 0.17 → 0.27 |
| 31 | — | Module 03 in one picture | recap | built it, lost Brno, ringed the south |
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

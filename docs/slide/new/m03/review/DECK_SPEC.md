# m03 DECK_SPEC — Build it, Break it

Slide-by-slide outline for `m03-robustness.md`. Written before the deck, per
`DECK_BUILD_GUIDE.md`. Sources: `plan.md` (lecturer decisions), `curriculum.yml` m03
(c01–c31), `docs/lecture-note/m03-robustness/01-concepts.qmd`.

## Non-negotiables (restated from SLIDE_RUBRIC.md — check every slide against these)

- **One slide, one point.** At most one new concept per slide.
- **Fragments use `*`**, never `-`. `-` does not fragment in Marp.
- **No tables. No code.** A single prose pointer to the notebook is allowed.
- **`cols` is text + figure only.** Never two columns of text.
- **Question and answer on separate slides.** The answer must not appear anywhere on
  the question slide — including a gray `note`.
- **Every concept slide has a figure.** Exceptions: question slides, part dividers, roadmap.
- **No paragraph below a fragmented list.**
- **Bold marks key terms only** (renders accent-2 red).
- **Shallow slides take `<!-- _class: mid -->`.**
- **Every part carries an interactive milestone** (S5).

## Verified numbers (computed 2026-08-05, not copied)

### The Moravian working graph

Eight real Moravian towns, positioned by their true lat/lon projected to km
(equirectangular about the centroid). Thirteen candidate cable routes, chosen among
geographic neighbours; **zero edge crossings** (checked by segment intersection over all
78 pairs). Weights are the true inter-town distances in km, rounded and nudged to
thirteen **distinct** integers, so the MST is unique.

| route | km | route | km |
|---|---|---|---|
| Prostějov–Olomouc | 17 | Brno–Hodonín | 54 |
| Jihlava–Třebíč | 29 | Znojmo–Brno | 55 |
| Třebíč–Znojmo | 42 | Zlín–Hodonín | 57 |
| Brno–Prostějov | 48 | Jihlava–Brno | 77 |
| Prostějov–Zlín | 49 | Brno–Zlín | 78 |
| Olomouc–Zlín | 51 | Znojmo–Hodonín | 79 |
| Třebíč–Brno | 53 | | |

(This table lives in the spec only. On slides the weights are printed **on the figure**,
never as a table — L2.)

| quantity | value | how verified |
|---|---|---|
| n, m | 8 towns, 13 candidate routes | construction |
| planarity | 0 crossings | pairwise segment-intersection test |
| **MST total** | **292 km** | own Kruskal + own Prim + `nx.minimum_spanning_tree`, all three agree |
| MST edges | 17, 29, 42, 48, 49, 53, 54 | ditto |
| MST degrees | Brno 3, Prostějov 3, Třebíč 3, five leaves 1 | networkx |
| edges in a spanning tree | 7 = n − 1 | construction |
| **Kruskal order** | 17, 29, 42, 48, 49, **51 skipped (cycle)**, 53, 54 | own trace |
| Kruskal skips | exactly one: Olomouc–Zlín (51) | own trace |
| **Prim order from Brno** | 48, 17, 49, 53, 29, 42, 54 | own trace |
| Prim total | 292 km — same tree, different order | asserted equal to Kruskal's edge set |
| **Borůvka rounds** | **2** — round 1 picks 6 edges at once (17, 29, 42, 48, 49, 54), round 2 picks 53 | own trace, total asserted = 292 |
| tie variant | Olomouc–Zlín 51 → **49**, tying Prostějov–Zlín | brute force over all 7-edge subsets |
| — number of optimal trees | **2**, both 292 km | ditto |
| — how they differ | one takes Prostějov–Zlín, the other Olomouc–Zlín | ditto |

**Deviation from `plan.md` recorded.** The plan (and the lecture note) says Prim's answer
depends on the starting node. On this graph, under a deterministic tie-break, all eight
starting nodes return the same tree — searched exhaustively over every single-edge tie
setting, 0 hits. So the tie slide teaches what is demonstrable and true: *ties → several
optima of equal cost, and which one you get depends on how the tie is broken.* The
start-node claim is not made on any slide.

Town substitution recorded: `plan.md` listed Přerov; Olomouc/Prostějov/Přerov lie within
~25 km of one another and would draw as a cramped triple. Hodonín (south-east, a real
Moravian town) replaces it and the layout keeps Moravia's true geography.

### Damage on the finished grid

Connectivity = (largest component after removal) / (original 8 towns), per c11.

| removed | pieces | connectivity |
|---|---|---|
| **Brno** (deg 3) | 3 + 3 + 1 | **3/8 = 0.375** — the worst single loss |
| Prostějov (deg 3) | 5 + 1 + 1 | 5/8 = 0.625 |
| Třebíč (deg 3) | 5 + 1 + 1 | 5/8 = 0.625 |
| any leaf | 7 | 7/8 = 0.875 |

| quantity | value | how verified |
|---|---|---|
| R-index definition | R = (1/N) Σ_{k=1}^{N−1} y_k | c13 / lecture note |
| **R, adaptive-degree attack on the MST** | 11/64 = **0.172** | own profile, exact fractions |
| — its profile | 0.375, 0.375, 0.125, 0.125, 0.125, 0.125, 0.125 | ditto |
| — its order | Brno, Prostějov, Třebíč, then leaves | adaptive degree ranking |
| **R, a random order on the MST** | 13/32 = **0.406** | seeded order Zlín, Znojmo, Jihlava, Hodonín, Prostějov, Třebíč, Olomouc, Brno |
| — its profile | 0.875, 0.750, 0.625, 0.500, 0.250, 0.125, 0.125 | ditto |
| ratio | targeted destroys **2.4×** as much area | 0.406 / 0.172 |

### Redundancy (the Part 6 payoff)

Exhaustive search over all 15 pairs of the six unused candidate routes, ranked by R under
adaptive attack:

| quantity | value | how verified |
|---|---|---|
| best pair | **Zlín–Hodonín (57) + Znojmo–Hodonín (79)** | exhaustive, unique winner |
| extra cable | 136 km on 292 = **+47 %** | arithmetic |
| R | 0.172 → **0.266** (+55 %) | own profile |
| worst single loss | 3/8 → **6/8** (Prostějov, stranding Olomouc) | exhaustive over all 8 removals |
| what it is geometrically | the two new cables close a **ring** through the south | drawing |
| best single edge instead | Znojmo–Hodonín, 79 km (+27 %), R → 0.219, worst loss 4/8 | exhaustive |

### The mathematics

| quantity | value | how verified |
|---|---|---|
| q(k) | k p(k) / ⟨k⟩ | c19 |
| κ | ⟨k²⟩ / ⟨k⟩ | c20 |
| branching factor | κ − 1 (subtract the edge you arrived on) | c22 derivation |
| Molloy–Reed | giant component ⟺ κ > 2 ⟺ κ − 1 > 1 | c21 |
| f_c | 1 − 1/(κ − 1), from (1 − f)(κ − 1) = 1 | c22 |
| ring, all degree 2 | ⟨k⟩ = 2, ⟨k²⟩ = 4, **κ = 2** exactly, f_c = 0 | computed |
| star, 1 hub + 5 leaves | ⟨k⟩ = 5/3, ⟨k²⟩ = 5, **κ = 3**, f_c = 0.5 | computed |
| path of 5 | ⟨k⟩ = 1.6, ⟨k²⟩ = 2.8, **κ = 1.75 < 2** — no giant component | computed |
| Poisson | ⟨k²⟩ = ⟨k⟩² + ⟨k⟩ ⇒ κ = ⟨k⟩ + 1 ⇒ **f_c = 1 − 1/⟨k⟩** | c23 |
| — ⟨k⟩ = 1 | κ = 2 — exactly the m02 giant-component birth | computed |
| — ⟨k⟩ = 2 / 4 / 6 | f_c = 0.50 / **0.75** / 0.83 | computed |
| scale-free 2 < γ < 3 | ⟨k²⟩ → ∞ ⇒ κ → ∞ ⇒ **f_c → 1** | c24 |
| 2D site percolation | **p_c = 0.5927** (square lattice) | Newman & Ziff 2000 |

Not taught, note-only (per `plan.md`): c25 finite-size correction, c26 attack-threshold
equation, and the exact binomial dilution κ_p = p κ₀ + (1 − p). The deck reaches f_c by the
branching-factor heuristic only, and says so in one line.

### Simulations behind the Part 6 curves

Measured in the generator, seeded, never drawn from memory.

| network | ⟨k⟩ | κ | k_max |
|---|---|---|---|
| ER, n = 2000, m = 6000 | 6.00 | 7.05 | — |
| Scale-free (BA, n = 2000, m = 3) | 5.99 | **17.0** | 182 |

| network · strategy | half gone at f = | below 5 % at f = |
|---|---|---|
| ER · random | 0.48 | 0.80 (theory 1 − 1/6 = **0.83**) |
| ER · targeted | 0.35 | 0.40 |
| scale-free · random | 0.48 | **0.85** |
| **scale-free · targeted** | **0.20** | **0.25** |
| ER · fixed order | 0.40 | 0.575 |
| ER · adaptive order | 0.35 | 0.40 |

Fixed vs adaptive is shown on the **ER** network, where the gap is widest (collapse at
0.575 vs 0.40); on the scale-free network the two nearly coincide (0.30 vs 0.25).

### History (real names, dates, places — S1)

| fact | detail |
|---|---|
| Czechoslovakia founded | 28 October 1918 |
| the place | Moravia, the eastern lands of the new republic |
| the company | West Moravian Power Company (Západomoravské elektrárny) |
| the mathematician | **Otakar Borůvka** (1899–1995) |
| the paper | 1926, *O jistém problému minimálním*, Práce Moravské přírodovědecké společnosti 3, 37–58 |
| Jarník | Vojtěch Jarník, 1930 — the "Prim" algorithm, published in Czech, prompted by Borůvka |
| Kruskal | Joseph Kruskal, 1956, Proc. AMS 7, 48–50 |
| Prim | Robert Prim, 1957, Bell System Technical Journal 36, 1389–1401 |
| Molloy–Reed | 1995, Random Structures & Algorithms 6, 161–180 |
| Albert–Jeong–Barabási | 2000, *Nature* 406, 378–382 — "error and attack tolerance" |
| Cohen et al. | 2000, PRL 85, 4626 (random) · 2001, PRL 86, 3682 (attack) |

The friend who carried the problem from the power company to Borůvka is **not named** on
any slide (commonly given as Jindřich Saxel, but not in the lecture note — unverified
names stay off slides).

## Four-act mapping

| act | rubric | where |
|---|---|---|
| S1 story | Moravia 1919–1926, Borůvka, the power company | Part 1 |
| S2 math of *that* story | the same eight towns: MST, Kruskal, Prim, Borůvka, then breaking **that grid** | Parts 2–3 |
| S3 generalization | percolation, q(k), κ, Molloy–Reed, f_c for any network | Parts 4–5 |
| S4 edge cases as prompts | robust-yet-fragile, the designer discussion, four question→answer pairs | Parts 6–7 |

## Milestones (S5)

| part | interactive element |
|---|---|
| 1 The cheapest grid | **Your turn** — draw your own cheapest grid on the eight towns |
| 2 Greedy | **Your turn** — trace Kruskal, then trace Prim, on the same graph |
| 3 Break it | **Poll** — which town hurts most? · **live demo** `network-robustness.html` · paper exercise |
| 4 Percolation | **live demo** — the marimo puddle slider |
| 5 The formula | **Your turn** — compute κ for a ring, a star and a path |
| 6 Robust yet fragile | **Discussion** — you are the designer: two extra cables, where? |
| 7 Edge cases | every slide is a prompt (four Q→A pairs) |

---

# Slide list

Legend: `[Q]` question slide (no answer anywhere, including notes) · `[A]` its answer ·
`[mid]` shallow, centred · figure names are files in `figures/`.

## Front

1. **Title** `lead` — "Build it, Break it" · eyebrow "Advanced Topics in Network Science ·
   Module 03" · sub "The cheapest grid is the easiest one to destroy".
2. **The question for today** `[Q] [mid]` — formula panel: *How much of a network can you
   destroy before it falls apart — and does it matter whether the damage is random or
   deliberate?* No figure, no answer.
3. **Roadmap** — `steps-list`, seven entries matching the parts.

## Part 1 — The cheapest grid (S1: the story)

4. **Part divider** `part` — "The cheapest grid · 01 / 07".
5. **Moravia, 1919** — the new republic, the towns still dark. `moravia-dark` (eight
   labelled towns, no cables). Point: the problem is real, and it has a place and a date.
6. **The problem reaches a mathematician** — a friend at the West Moravian Power Company
   carries it to Otakar Borůvka (1899–1995); his 1926 paper is the first answer.
   `boruvka-portrait`. Point: who solved it, and when.
7. **Erase the map** — towns become dots. `abstract-1`. Point: only the towns matter.
8. **Draw what could be built** — the thirteen possible cable routes. `abstract-2`.
   Point: the candidate edges are a choice, not a given.
9. **Each route has a price** — kilometres of cable on every edge: a **weighted network**
   (c02). `abstract-3`. Point: the number on the edge is what we are minimising.
10. **The engineer's question** `[Q] [mid]` — formula panel: *Connect all eight towns.
    Which cables do you lay, and what is the least total length?* `moravia-graph`.
11. **Your turn** — milestone. Draw a grid that connects all eight, add up the kilometres,
    keep your number. `moravia-worksheet` (same graph, weights shown, nothing selected).
12. **What everyone notices first** — a loop always contains one cable you can cut and
    still be connected. `loop-waste` (a cycle, one edge struck out). Point: cycles are
    waste when all you need is connectivity.
13. **A tree** (c03) — connected and no cycles. `tree-def`. Point: the definition.
14. **A spanning tree has exactly n − 1 edges** (c03) — the seven cables counted on the
    figure. `spanning-count`. Point: the count is forced, so only *which* edges is free.
15. **Minimum spanning tree** (c04) — of all spanning trees, the one of least total
    weight. `mst-def` (the 292 km tree highlighted on the candidate graph).

## Part 2 — Greedy (S2: the math of that story)

16. **Part divider** `part` — "Greedy · 02 / 07".
17. **Kruskal's rule** (c05) — cheapest cable first, skip anything that closes a loop.
    Joseph Kruskal, 1956. `kruskal-rule`. Point: the rule, stated once.
18. **Kruskal, running** — `kruskal.gif` (17 → 29 → 42 → 48 → 49 → *51 refused* → 53 →
    54, ending on the finished 292 km tree). Point: watch it build.
19. **The one it refuses** — Olomouc–Zlín, 51 km: both ends already connected.
    `kruskal-skip`. Point: the skip is the whole algorithm.
20. **Your turn** — milestone. Trace Kruskal yourself on the worksheet graph: list the
    order, add up the kilometres. `kruskal-worksheet`.
21. **[A] The order, and the answer to slide 10** — 17, 29, 42, 48, 49, skip 51, 53, 54;
    **292 km**. `kruskal-answer`.
22. **Prim's rule** (c06) — start at the Brno power plant and buy the cheapest cable that
    reaches one new town. Jarník 1930 · Prim 1957. `prim-rule`. Point: local growth.
23. **Prim, running** — `prim.gif` (48 → 17 → 49 → 53 → 29 → 42 → 54). Point: the tree
    grows as one connected blob.
24. **Your turn** — milestone. Trace Prim from Brno. `prim-worksheet`.
25. **[A] Different order, same tree** — 48, 17, 49, 53, 29, 42, 54: the same seven
    cables, 292 km. `prim-vs-kruskal` (the two orders, one tree). Point: the answer does
    not depend on the route to it.
26. **[Q] Greedy is usually wrong** `[mid]` — cheapest-first fails on almost every other
    problem. Why should it be optimal here? Take 30 seconds.
27. **[A] Here it cannot be beaten** (c07) — cut the tree anywhere; the cheapest cable
    crossing that cut must be in the MST, and that is exactly what both rules pick.
    `cut-property`. Point: the reason, in one picture.
28. **[Q] What if two cables cost the same?** `[mid]` — `tie-graph` (Olomouc–Zlín redrawn
    at 49 km, tying Prostějov–Zlín).
29. **[A] Two cheapest grids** (c08) — both 292 km; which one you get depends on how the
    tie is broken. `tie-two-trees`. Point: distinct weights ⇒ unique MST; ties ⇒ several.
30. **[Q] And Borůvka himself?** `[mid]` — neither rule is his. He had no computer and
    no sorted list. What would you do?
31. **[A] Every town at once** (c29) — each component picks its own cheapest outgoing
    cable, simultaneously, and the components merge. `boruvka.gif`.
32. **Two rounds, not seven steps** — round 1 chooses six cables at once; round 2 chooses
    the last. `boruvka-rounds`. Point: it is the parallel one, which is why it came back.

## Part 3 — Break it (S2 continued: breaking *that* grid)

33. **Part divider** `part` — "Break it · 03 / 07".
34. **The grid, finished** — 292 km, eight towns, seven cables. `mst-alone`. Point: this
    is what 1926 would have built.
35. **[Q] Which town, gone dark, hurts most?** `[mid]` — `mst-blank` (no degrees, no
    highlight). Vote before we look. Milestone (poll).
36. **[A] Brno** (c09) — remove it and eight towns become 3 + 3 + 1. `brno-removed`.
37. **Every cable is a bridge** — in a tree there is exactly one route between any two
    towns, so every cable is a single point of failure. `tree-bridges`. Point: the
    fragility is structural, not bad luck.
38. **Real grids are not trees** (c10) — the US transmission network, full of loops.
    `us-grid` (photograph). Point: redundancy is what everyone actually builds.
39. **Measuring the damage** (c11) — connectivity = largest surviving piece ÷ original
    size; Brno's removal scores 3/8. `connectivity-def`. Point: one number for "how bad".
40. **[Q] Keep going — what does the whole curve look like?** `[mid]` — remove towns one
    at a time and plot connectivity each time. Sketch it before we draw it.
41. **The robustness profile** (c12) — `profile-build.gif`, the curve drawn point by
    point as towns fall. Point: damage is a curve, not a number.
42. **One curve, one number** (c13) — R = area under the profile = 0.17 for this attack.
    `r-index`. Point: R compresses the curve so networks can be compared.
43. **[Q] Does the order matter?** `[mid]` — same grid, same number of towns removed,
    different order. Guess how much the curve moves.
44. **[A] Random failure** (c14) — earthquakes and broken transformers hit leaves as often
    as hubs: R = 0.41. `profile-random`.
45. **[A] Targeted attack** (c15) — an adversary who can see the map takes Brno first:
    R = 0.17, the same curve as slide 42. `profile-both` (both curves, one axis).
    Point: 2.4× the damage for the same number of removals.
46. **[Q] Fix the hit list, or re-measure after every hit?** `[mid]` — degrees change as
    towns disappear. Does re-ranking help the attacker?
47. **[A] Re-measuring is worse** (c16) — on a random network, a fixed ranking collapses
    it at 58 % removed; re-ranking after every removal at 40 %. `fixed-vs-adaptive`.
48. **Take it apart yourself** — milestone. `network-robustness.html` live, and the paper
    exercise *Build it, Break it, Build it back*. `demo-still`.
49. **[Q] Cliffhanger** `[mid]` — what *fraction* of a network has to fail before it
    fragments? Next time: one formula predicts it from the degree distribution alone.

## Part 4 — Percolation (S3: generalization begins) — day 2

50. **Part divider** `part` — "Percolation · 04 / 07".
51. **[Q] The puddle yard** `[mid]` (c17) — every paving stone is wet with probability p.
    At which p do the puddles first join into one that spans the yard? `puddle-low`.
52. **Turning p up** — `puddle-sweep.gif`, p from 0.30 to 0.75. Point: watch for the
    moment it joins.
53. **[A] It happens all at once** (c17) — the largest puddle jumps at p_c ≈ 0.59.
    `phase-transition`. Point: a phase transition, not a ramp.
54. **Live demo** — milestone. The marimo slider from the lecture note: drag p, watch the
    red cluster appear. `puddle-widget`.
55. **[Q] Does the order matter here?** `[mid]` — you wet the stones one at a time. Does
    a different order change when the giant puddle appears?
56. **[A] Only the fraction** (c30) — the transition depends on how many stones are wet,
    not which came first. `order-irrelevant`.
57. **Attack is percolation, backwards** (c18) — one axis, two directions: adding nodes
    builds the giant component, removing them destroys it. `reverse-percolation`.
    Point: the mathematics is already written; we only have to read it right-to-left.

## Part 5 — The formula (S3: the general result)

58. **Part divider** `part` — "The formula · 05 / 07".
59. **[Q] What number decides it?** `[mid]` — two networks, same number of nodes and
    edges, one shatters and one holds. What do you have to know about a network to
    predict which?
60. **[Q] Follow an edge, not a node** `[mid]` — pick an edge at random and walk to its
    end. Is the node you meet an average member of the network? `follow-edge` (the walk
    only, no answer).
61. **[A] No — it is biased to hubs** (c19) — q(k) = k p(k) / ⟨k⟩: a node with twice the
    degree has twice the chance of being on the edge you picked. `qk-bias`.
62. **How connected is the node you land on?** (c20) — average degree under q(k) is
    κ = ⟨k²⟩/⟨k⟩. `kappa-def`. Point: κ, the heterogeneity number.
63. **Subtract the way you came in** — of κ links, one is the edge you arrived on, so the
    search fans out by **κ − 1**. `branching`. Point: the branching factor.
64. **Molloy–Reed** (c21) — branching above 1 means the search never dies: a giant
    component exists exactly when κ > 2. `molloy-reed`. Point: the criterion.
65. **Your turn** — milestone. Compute κ for a ring, a star and a path.
    `kappa-worksheet`.
66. **[A] κ = 2, κ = 3, κ = 1.75** — the ring sits exactly on the threshold, the star is
    over it, the path is under it. `kappa-answer`.
67. **Now break it** (c22) — remove a fraction f; each surviving neighbour keeps
    (1 − f)(κ − 1) onward links on average. `dilution`. Point: failure only rescales the
    branching factor.
68. **The critical fraction** (c22) — set (1 − f)(κ − 1) = 1: **f_c = 1 − 1/(κ − 1)**.
    `fc-formula`. Point: the answer to the cliffhanger. One line notes that the exact
    binomial version is in the appendix and gives the same threshold.
69. **A homogeneous network** (c23) — Poisson: ⟨k²⟩ = ⟨k⟩² + ⟨k⟩ ⇒ κ = ⟨k⟩ + 1 ⇒
    f_c = 1 − 1/⟨k⟩. At ⟨k⟩ = 4, three quarters of the nodes must go. `fc-poisson`.
70. **[Q] And a network with hubs?** `[mid]` — a scale-free degree distribution:
    most nodes tiny, a few enormous. What does κ do?
71. **[A] κ blows up, f_c → 1** (c24) — ⟨k²⟩ diverges for 2 < γ < 3, so almost every node
    must be removed. `fc-scalefree`. Point: hubs make random failure nearly harmless.

## Part 6 — Robust yet fragile (S4 begins)

72. **Part divider** `part` — "Robust yet fragile · 06 / 07".
73. **[Q] So a hub network is indestructible?** `[mid]` — f_c → 1 says random failure
    cannot kill it. Is that the whole story?
74. **[A] Random failure: both survive** — measured curves, ER and scale-free, random
    removal; the hub network holds on longest (85 % vs 80 %). `sim-random`.
75. **Now let the adversary choose** — the same two networks, highest degree first.
    `sim-targeted`. Point: the scale-free curve falls off a cliff at 20 %.
76. **Robust yet fragile** (c27) — the same hubs do both jobs. `robust-fragile` (all four
    curves, one axis). Albert, Jeong & Barabási, *Nature*, 2000.
77. **Efficiency against security** (c31) — hubs are cheap to build and cheap to attack;
    there is no structure that wins both. `efficiency-security`.
78. **[Q] You are the designer** `[mid]` — milestone. Two extra cables for Moravia. Where
    do you put them, and what do you buy for the money? `mst-blank-design`.
79. **[A] Close the ring in the south** — Zlín–Hodonín and Znojmo–Hodonín: +136 km
    (+47 %), worst single loss 3/8 → 6/8, R 0.17 → 0.27. `redundant-answer`.
80. **Design principles** (c28) — even out degrees, build redundant routes, protect the
    hubs you cannot avoid, layer local grids under a backbone, reconfigure under attack.
    `design-principles`. Point: the discussion's takeaways, named.
81. **Build it back** — 1926 answers "cheapest"; a modern transmission grid answers
    "cheapest that survives", and it is meshed. `build-it-back`. Point: the circle closes.

## Part 7 — Edge cases (S4: every one a prompt)

82. **Part divider** `part` — "Edge cases · 07 / 07".
83. **[Q] A ring** `[mid]` — every town has exactly two cables. What is κ? `ring-q`.
84. **[A] κ = 2 exactly** — the threshold itself: the branching factor is 1, so f_c = 0
    and the ring has no robust core. One failure makes it a chain. `ring-a`.
85. **[Q] A random network with ⟨k⟩ = 1** `[mid]` — what does the formula say? `er1-q`.
86. **[A] κ = 2 again** — and that is exactly where Module 02's giant component was born.
    The same threshold, found from the other side. `er1-a`.
87. **[Q] Attack by betweenness, not degree?** `[mid]` — the busiest *through-route*, not
    the most connections. `betweenness-q`.
88. **[A] More damage, more cost** — a bridge node with degree 2 can matter more than a
    hub; betweenness finds it, and costs far more to compute. Module 06. `betweenness-a`.
89. **[Q] Real grids are full of triangles** `[mid]` — Module 02 said so. Does f_c still
    hold? `triangles-q`.
90. **[A] Not exactly** — the branching argument assumed each new neighbour is new;
    triangles send the search back where it came from, so real thresholds sit below the
    prediction. `triangles-a`. Point: know the assumption you are standing on.

## Part 8 — Wrap-up

91. **Module 03 in one picture** — build it (292 km), break it (Brno, 3/8), build it back
    (+47 %, R 0.17 → 0.27), and the formula that predicted it. `recap`.
92. **Coming up in Module 04** — q(k) said the node at the end of an edge is biased to
    hubs. Apply that to friendship and you get: your friends have more friends than you
    do. `m04-teaser`.

92 slides. Parts: 1 (12), 2 (17), 3 (17), 4 (8), 5 (14), 6 (10), 7 (9), plus 3 front and
2 wrap-up.

**Deviation from `plan.md` recorded.** The plan asked for 70–80 slides; this spec lands
at 92. The overshoot is structural, not padding: m03 carries 31 concepts (m01 had ~29
across 78 slides), and the lecturer's own rules cost slides — one point per slide, and a
question and its answer on two slides each. There are 14 question→answer pairs here, so
14 slides exist purely because the answer may not share a frame with its question. Cutting
to 80 would mean dropping four Q→A pairs or merging concepts; that is the lecturer's call,
not the builder's, so the deck is written in full and the count is flagged here.

## Figure-per-slide check

Every numbered slide above names a figure except: 1 (title), 2 (question), 3 (roadmap),
part dividers (4, 16, 33, 50, 58, 72, 82), and the question slides marked `[mid]` that
deliberately carry no drawing (26, 30, 40, 43, 46, 49, 55, 59, 70, 73). Question slides
that *do* carry a figure show only the setup, never the answer.


---

# Post-build corrections (recorded after the review rounds)

The deck as shipped differs from the slide list above in these ways. Recorded here so the
spec and the deck cannot drift apart silently.

- **Slide 61** (`qk-bias`) and **slides 60, 83, 85, 89** changed layout, not content: a
  figure authored for one container was used in the other, rendering at 48 % or 209 % of
  its intended scale. Each slide now uses the layout its figure was authored for.
- **`design-principles` is no longer the Moravian map.** A full-width map cannot share a
  slide with the five-item principle list without overflowing the frame, so the figure is
  a column-width dot plot of cables per town, before and after the two extra cables. The
  claim it carries is checked in the generator: the degree variance falls, and the number
  of towns on a single cable falls from five to two.
- **`spanning-count` numbers its cables left to right**, not in Kruskal's order. The
  original numbering meant the same badges carried two meanings three slides apart, and
  introduced an algorithm's order four slides before the algorithm.
- **`betweenness-a` shows one scenario**, the bridge removed, with each surviving piece's
  size printed. It previously drew the bridge result while asserting the hub result in its
  caption.
- **In-figure prose was cut deck-wide.** Notes inside a drawing carry numbers only; the
  sentence lives in the `figcaption`, once. Three slides had shipped the same sentence in
  the body, the drawing and the caption.
- **The US power-grid photograph is not used** (see FIGURE_SPEC): the slide draws its own
  meshed network instead of the lecture note's copyrighted image.

## Process note for the next module

Four parallel reviewer agents were launched for round 1 and none returned a report. The
rounds that followed were driven by `check_render.py` plus a single slide-by-slide read.
That is weaker coverage than the playbook intends, and it is why the strengthened checker
mattered so much: every defect it could measure, it found, and the two defect classes it
could **not** originally measure — node size on this palette, and a label lying across a
cable — are exactly the two that survived the whole first build.

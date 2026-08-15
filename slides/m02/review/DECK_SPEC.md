# m02 DECK_SPEC — Small-World Networks

Slide-by-slide outline for `m02-small-world.md`. Written before the deck, per
`DECK_BUILD_GUIDE.md`. Source of content: `plan.md` (lecturer decisions),
`curriculum.yml` m02 (c01–c26), `lecture-note/m02-small-world/01-concepts.qmd`.

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

## Verified numbers (recomputed 2026-08-05, not copied)

| quantity | value | how verified |
|---|---|---|
| Milgram | 160 packets, 64 arrived, median ≈ 6 intermediaries | curriculum c01 + lecture note |
| Yahoo (Goel 2009) | >24,000 starters, 384 completed, mean chain ≈ 4, corrected 5–7 | lecture note |
| Facebook (Backstrom 2012) | 721M users, 69B friendships, L = 4.74 | curriculum c03 + note |
| Guare's play | "Six Degrees of Separation", 1990 stage / 1991 — the phrase is his, not Milgram's | note |
| P7 chain | L = 8/3 = 2.667, diameter 6 | networkx `path_graph(7)` |
| Milgram net (P7 + chord (0,2) + shortcut (1,5)) | L = 38/21 = 1.810, diameter 3 | networkx |
| — its C_i | [1, 1/3, 1/3, 0, 0, 0, 0] | networkx `clustering` |
| — its C̄ / transitivity | 5/21 = 0.238 / 1/4 = 0.25 | networkx |
| Ego example (k=5, 2 links among neighbours) | C = 2/10 = 0.2 | lecture note fig |
| Windmill (hub + 5 blades, n=11, m=15) | C̄ = 91/99 = 0.919, C = 3/11 = 0.273, 5 triangles | networkx `windmill_graph(5,3)` |
| — its triplet count | 55 = C(10,2) + 10 | 3·5/55 = 3/11 ✓ |
| Complete graph | C = 1, L = 1 | trivial |
| ER | E[C_i] = p = ⟨k⟩/(n−1); L ≈ ln n / ln⟨k⟩ | note appendix |
| Humanity | ln(8×10⁹)/ln(150) = 22.80/5.01 = **4.55** | python |
| Ring lattice n=20, k=4 | C̄ = C = 0.5, L = 55/19 = 2.895, diameter 5 | networkx |
| Ring lattice n=1000, k=4 | L = 125.4, C = 0.5, σ = 4.96 (**σ > 1**) | networkx |
| WS1998 actors | L 3.65 / L_rand 2.99 · C 0.79 / C_rand 0.00027 → **σ ≈ 2400** | Table 1 |
| WS1998 power grid | 18.7 / 12.4 · 0.080 / 0.005 → **σ ≈ 11** | Table 1 |
| WS1998 C. elegans | 2.65 / 2.25 · 0.28 / 0.05 → **σ ≈ 4.8** | Table 1 |
| 2D grid 20×20 | C = 0, L = 13.33 → σ = 0 | networkx |
| Cycle n=100 | C = 0, L = 25.25 → σ = 0 | networkx |
| Lattice n=400, k=8 | C = 0.643, L = 25.44 | own BFS, seeded |

Caveat recorded, not taught: WS's power-grid C_rand (0.005) is ~10× the formula
⟨k⟩/(n−1) = 0.00054, because they measured random rewirings rather than using the
asymptotic form. The formula slide and the scoreboard slide therefore never invite the
comparison on the same slide.

## Four-act mapping

| act | rubric | where |
|---|---|---|
| S1 story | Milgram, Omaha 1967, real names/dates | Part 1 |
| S2 math of *that* story | the chain becomes a graph; d, L, diameter measured **on it** | Part 2 |
| S3 generalization | clustering, ER baseline, σ, Watts–Strogatz | Parts 3–5 |
| S4 edge cases as prompts | four question→answer pairs | Part 6 |

## Milestones (S5)

| part | interactive element |
|---|---|
| 1 The six-handshake claim | **live Wikirace** (slide 16) |
| 2 Measuring "six" | **Worksheet A** — distances by hand on the Milgram graph (slide 29) |
| 3 The other half | **Worksheet B** — C_i by hand on the same graph (slide 44) |
| 4 The yardstick | **σ mini-exercise** — compute σ from the scoreboard (slide 60) |
| 5 The mechanism | **marimo WS widget** — drag p, watch C and L separate (slide 74) |
| 6 Edge cases | every slide is a prompt (Q→A pairs, slides 76–83) |

---

# Slide list

Legend: `[Q]` question slide (no answer anywhere) · `[A]` its answer · `[mid]` shallow,
centred · figure names are files in `figures/`.

## Front

1. **Title** `lead` — "Six Handshakes" / eyebrow "Advanced Topics in Network Science ·
   Module 02" / sub "Why the world is smaller than it has any right to be".
2. **The question for today** `[Q] [mid]` — formula panel: *Why is a stranger on the other
   side of the world only about six handshakes away?* Beat: "Guess a number before we
   start." No figure, no answer.
3. **Roadmap** — `steps-list`, six entries matching the parts.

## Part 1 — The six-handshake claim (S1: the story)

4. **Part divider** — "Part One · The six-handshake claim / A letter, a stranger, and 160 envelopes".
5. **Omaha, 1967** — fig `milgram-map.png`. Point: Milgram mails packets from Omaha and
   Wichita, addressed to one stockbroker outside Boston. Names, places, date.
6. **The rule** — fig `milgram-rule.png`. Point: you may only hand it to someone you know
   on a first-name basis. That single rule is the experiment.
7. **How many hands?** `[Q] [mid]` — formula panel: *How many people between the Omaha
   farmer and the Boston broker?* Show of hands: 2 · 6 · 20 · 100. No figure.
8. **64 of 160 arrived** `[A]` — fig `milgram-arrivals.png` (160 dots, 64 filled).
   Point: most chains died; the completed ones are the data.
9. **A median of six** `[A]` — fig `milgram-chain.png` (7 people in a row, occupation
   labels). Point: the completed chains ran through about six intermediaries.
10. **Milgram never said "six degrees"** — fig `six-degrees-timeline.png`
    (1967 experiment → 1990 Guare play → today). Point: the phrase is John Guare's.
11. **Does it survive eight billion people?** `[Q] [mid]` — formula panel. No figure.
12. **Email, 2003** `[A]` — fig `replication-yahoo.png` (number line, Milgram dot + Yahoo dot).
    Point: 24,000 starters, 384 completed chains, mean ≈ 4.
13. **Facebook, 2012** `[A]` — fig `replication-facebook.png` (same line, third dot at 4.74).
    Point: 721 million users, 69 billion friendships, average 4.74. Build: one dot added.
14. **Wikirace** *(milestone demo)* — fig `wikirace.png`. Point: play it now —
    two random articles, links only, fewest clicks wins. Prose link to wiki-race.com.
15. **What did you actually just do?** `[Q] [mid]` — formula panel: *You found a short
    path without ever seeing the network. Is that the same as one existing?* No figure.
16. **Finding beats existing** `[A]` — fig `routing-vs-existence.png`. Point: Milgram's
    result is the stronger claim — people **route** with local knowledge only.

## Part 2 — Measuring "six" (S2: the math of that same story)

17. **Part divider** — "Part Two · Measuring six / Turn the chain into a graph and count".
18. **The chain is a graph** — fig `chain-graph.png` (the same seven people, now discs).
    Point: person → node, "knows" → edge.
19. **Distance** — fig `distance-def.png` (two nodes, the connecting route in accent-2).
    Point: **d(i,j)** is the number of *edges* on a shortest route. Not miles. Not people.
20. **What is d(farmer, broker)?** `[Q] [mid]` — fig `chain-blank.png`. Count it out loud.
21. **Six** `[A]` — fig `distance-six.png` (the six edges numbered along the chain).
22. **A shortcut appears** — fig `chain-chord.png` (chord 0–2 added). Point: the grain
    buyer turns out to know the teacher — one extra edge.
23. **Two routes, one shortest** — fig `two-routes.png`. Point: distance takes the
    minimum; the longer route still exists.
24. **How would you score the whole network?** `[Q] [mid]` — formula panel: *One number
    for all 21 pairs — what would you compute?* No figure.
25. **Average path length** `[A]` — fig `apl-chain.png` (21 pairs as dots stacked by
    distance, mean marked at 8/3). Point: L̄ = mean of d over all pairs = 2.67 here.
26. **One more shortcut** — fig `chain-shortcut.png` (edge 1–5 added). Point: the second
    shortcut is the whole small-world story in miniature.
27. **The average collapses** — fig `apl-shortcut.png` (same dot plot, mean at 38/21).
    Point: two extra edges out of 21 pairs took L̄ from 2.67 to 1.81.
28. **Diameter** — fig `diameter.png` (worst pair highlighted before/after: 6 → 3).
    Point: the diameter is the worst case, not the average.
29. **Worksheet A** *(milestone activity)* — fig `worksheet-a.png` (the graph, unlabelled).
    Point: on paper, compute d for three named pairs and then L̄. Answers next slide.
30. **Worksheet A — check** `[A]` — fig `worksheet-a-answer.png`. Point: the three
    distances and L̄ = 38/21, revealed as fragments.

## Part 3 — The other half: clustering (S3 begins)

31. **Part divider** — "Part Three · The other half / Short paths are only half the story".
32. **Do your friends know each other?** `[Q] [mid]` — formula panel: *Pick two of your
    friends at random. What are the odds they know each other?* No figure.
33. **Triangles and triplets** — fig `triangle-triplet.png` (closed triplet vs open
    triplet). Point: three mutually-linked nodes are a **triangle**; two edges among
    three nodes is an open **triplet**.
34. **A neighbourhood** — fig `ego-graph.png` (centre + 5 neighbours, only the star drawn).
    Point: A has five friends — the question is about the edges *among them*.
35. **How many pairs could be linked?** `[Q] [mid]` — fig `ego-pairs.png` (all 10
    possible neighbour pairs drawn dashed, none counted). Count them.
36. **Ten** `[A]` — fig `ego-pairs-count.png`. Point: k(k−1)/2 = 10 possible edges.
37. **Local clustering coefficient** — fig `ego-clustering.png` (2 of the 10 present,
    accent-2). Point: **C_i** = present / possible = 2/10 = 0.2.
38. **Recall: A² counted walks** `[Q] [mid]` — formula panel: *(A²)_ij counted walks of
    length 2. What does (A³)_ii count?* No figure. (Callback to m01.)
39. **Closed walks of length three** `[A]` — fig `a3-walks.png` (one triangle, its two
    directed circuits drawn). Point: each triangle at i gives two closed 3-walks, so
    (A³)_ii = 2 × (triangles at i).
40. **C_i in matrix form** — fig `a3-formula.png` (the same triangle with the formula
    mapped onto it). Point: C_i = (A³)_ii / (k_i(k_i−1)).
41. **Averaging over nodes** — fig `cbar-milgram.png` (Milgram graph with each C_i
    printed on its node). Point: **C̄** = mean of C_i = 5/21 = 0.238.
42. **A windmill** `[Q] [mid]` — fig `windmill.png` (hub + 5 blades, no numbers).
    Point/question: *every blade node sees a perfectly closed neighbourhood; the hub sees
    almost none. What should "the clustering of this network" be?* No answer anywhere.
43. **Two answers, same graph** `[A]` — fig `windmill-split.png` (C_i printed per node,
    C̄ = 0.92 vs C = 0.27). Point: node-averaging says 0.92, triplet-counting says 0.27.
44. **Global clustering** — fig `transitivity-def.png` (the 5 triangles and the 55
    triplets shown as counted objects). Point: **C** = 3 × triangles / triplets = 15/55
    = 3/11; it weights the hub, which owns 45 of the 55 triplets.
45. **Worksheet B** *(milestone activity)* — fig `worksheet-b.png`. Point: compute C_i
    for three named nodes of the Milgram graph on paper.
46. **Worksheet B — check** `[A]` — fig `worksheet-b-answer.png`. Fragments: C_0 = 1,
    C_1 = 1/3, C_3 = 0, and C̄ = 5/21.

## Part 4 — The yardstick

47. **Part divider** — "Part Four · The yardstick / Compared to what?".
48. **The paradox** — fig `paradox.png` (a heavily-triangulated local patch, and a target
    far away). Point: high clustering means edges stay local — and local wiring should
    make the far side of the world *many* steps away. Yet Facebook measures 4.74.
49. **Score it naively** `[Q] [mid]` — formula panel: *s = C̄ / L̄. High is small-world.
    What network breaks this?* No figure.
50. **The complete graph breaks it** `[A]` — fig `complete-graph.png` (K₆, every edge
    drawn). Point: C̄ = 1 and L̄ = 1, so s = 1 — the maximum — for the least interesting
    network there is. Raw values certify nothing.
51. **Compared to what?** — fig `baseline-idea.png`. Point: we need a *structureless*
    network of the same size and density to normalise against.
52. **Erdős–Rényi G(n,p)** — fig `er-coin.png` (every pair a coin, some land as edges).
    Point: flip a coin with probability p for each of the n(n−1)/2 pairs.
53. **What is C_i in a random graph?** `[Q] [mid]` — formula panel. No figure.
54. **C_rand = p** `[A]` — fig `er-clustering.png` (an ego with k neighbours, each
    neighbour pair carrying its own coin). Point: each of the k(k−1)/2 neighbour pairs is
    an independent coin with the same p, so E[C_i] = p = ⟨k⟩/(n−1) — independent of degree.
55. **How far can 150 friends reach?** `[Q] [mid]` — formula panel: *Everyone has 150
    friends. After L steps, how many people have you reached?* No figure.
56. **The fan-out** `[A]` — fig `fanout.png` (1 → ⟨k⟩ → ⟨k⟩² branching, three rings).
    Point: reachable count grows like ⟨k⟩^L.
57. **L_rand ≈ ln n / ln⟨k⟩** — fig `fanout-solve.png` (⟨k⟩^L = n, the numbers on the
    figure: 8×10⁹, 150, 4.55). Point: eight billion people, 150 friends each → 4.55 steps.
58. **Short is free; clustered is not** — fig `free-vs-not.png` (the same random graph
    shown short-pathed and triangle-free). Point: randomness hands you short paths for
    nothing, and hands you no triangles at all.
59. **The small-world index** — fig `sigma-def.png` (the two ratios drawn as gauges
    against 1). Point: **σ** = (C/C_rand) / (L/L_rand); > 1 small-world, ≈ 1 random-like,
    < 1 anti-small-world.
60. **Three real networks** *(milestone activity)* — fig `ws1998-dots.png` (log axis, per
    network a dot for L/L_rand and a dot for C/C_rand, joined). Point: read the two ratios
    off the figure and compute σ yourself for one network.
61. **The verdict** `[A]` — fig `ws1998-sigma.png` (the three σ values printed against the
    σ = 1 line). Point: 2400, 11, 4.8 — actors, power grid, C. elegans are all small worlds.

## Part 5 — The mechanism

62. **Part divider** — "Part Five · The mechanism / What I cannot create, I do not understand".
63. **Could you build one?** `[Q] [mid]` — formula panel with Feynman's line: *Design a
    network with high clustering and short paths. What's your first move?* No figure.
64. **The ring lattice** — fig `ring-lattice.png` (n = 20, k = 4). Point: every node
    joined to its 4 nearest neighbours — C = 0.5, richly triangulated.
65. **But it is enormous** — fig `ring-distance.png` (the antipodal route traced).
    Point: distance grows linearly with n — at n = 1000, L̄ = 125.
66. **The opposite extreme** — fig `random-graph.png` (ER, same n and m). Point: paths
    are short and there is essentially no triangle anywhere.
67. **The trade-off** — fig `lattice-vs-random.png` (the two, side by side, with C and L
    annotated). Point: one axis buys the other. Real networks refuse to choose.
68. **How would you cheat?** `[Q] [mid]` — formula panel: *Keep the lattice's triangles,
    but shorten its paths. What is the cheapest edit?* No figure.
69. **Rewire with probability p** — fig `ws-rewire-step.png` (one edge caught mid-move).
    Point: walk the lattice edges; with probability p, move one endpoint to a random node.
70. **Watch it happen** — fig `ws-rewire.gif` (animated build, edges rewiring one at a
    time). Point: a handful of edges jump the ring.
71. **What do C and L do as p grows?** `[Q] [mid]` — formula panel. Predict two curves
    before the reveal. No figure.
72. **They do not fall together** `[A]` — fig `ws-sweep.png` (C(p)/C(0) and L(p)/L(0)
    against log p). Point: L collapses while C is still almost untouched.
73. **The small-world band** — fig `ws-band.png` (same curves, the band shaded).
    Point: for two decades of p you get both — that is why real networks land there.
74. **Drag p yourself** *(milestone widget)* — fig `ws-widget.png`. Point: open the
    marimo notebook and sweep p live. One prose link.
75. **Why shortcuts are so cheap** — fig `shortcut-effect.png` (one rewired edge, the
    pairs it shortens shaded). Point: one long edge shortens paths for a whole arc of
    nodes while destroying at most a couple of triangles.

## Part 6 — Edge cases (S4)

76. **Part divider** — "Part Six · Edge cases / The graphs that break the definitions".
77. **What if two nodes are not connected?** `[Q] [mid]` — fig `disconnected.png`.
78. **d = ∞, and the average dies with it** `[A]` — fig `disconnected-answer.png`.
    Point: one unreachable pair makes L̄ infinite; in practice measure on the largest
    component (or average the reciprocals).
79. **What is C_i for a node with one friend?** `[Q] [mid]` — fig `degree-one.png`.
80. **0/0 — a convention, not a fact** `[A]` — fig `degree-one-answer.png`. Point:
    k(k−1)/2 = 0 for k ≤ 1, so C_i is undefined; the convention is C_i = 0.
81. **Is any real network anti-small-world?** `[Q] [mid]` — fig `sigma-lt-1-q.png`
    (ring lattice, as the tempting wrong guess). No answer.
82. **Yes — but not the lattice** `[A]` — fig `grid-no-triangles.png`. Point: the ring
    lattice scores σ ≈ 5 (its clustering advantage beats its path penalty). You need a
    lattice with *no triangles* — a 20×20 road grid has C = 0, so σ = 0.
83. **G(n,m) or G(n,p) — same thing?** `[Q] [mid]` — fig `gnm-gnp.png`.
84. **Almost — but only one is independent** `[A]` — fig `gnm-gnp-answer.png`. Point:
    fixing m couples the edges; G(n,p)'s independence is exactly what made E[C_i] = p work.

## Wrap-up

85. **The same signature everywhere** — fig `universality.png` (neurons, power grid,
    actors, the Internet, citations named around one σ axis). Point: the small-world
    signature is not a social-network fact.
86. **One map** — fig `sw-map.png` (lattice —— WS —— random along p, with the C and L
    bands above). Point: the whole module on one axis.
87. **Module 02 review** — fig `recap.png`. Fragments: d and L̄ · C_i, C̄ and C · σ
    against a random baseline · Watts–Strogatz. Notebook pointer in a `note`.
88. **Coming up in Module 03** — fig `m03-teaser.png`. Point: the world is small because
    of a few shortcuts. So what happens when they break?

---

## Slide count

88 slides: front 3 · P1 13 · P2 14 · P3 16 · P4 15 · P5 14 · P6 9 · wrap 4.
Plan targeted 70–85; the overshoot is question/answer splits, which the rubric requires.

## Figure inventory (→ FIGURE_SPEC.md)

`milgram-map`, `milgram-rule`, `milgram-arrivals`, `milgram-chain`, `six-degrees-timeline`,
`replication-yahoo`, `replication-facebook`, `wikirace`, `routing-vs-existence`,
`chain-graph`, `distance-def`, `chain-blank`, `distance-six`, `chain-chord`, `two-routes`,
`apl-chain`, `chain-shortcut`, `apl-shortcut`, `diameter`, `worksheet-a`,
`worksheet-a-answer`, `triangle-triplet`, `ego-graph`, `ego-pairs`, `ego-pairs-count`,
`ego-clustering`, `a3-walks`, `a3-formula`, `cbar-milgram`, `windmill`, `windmill-split`,
`transitivity-def`, `worksheet-b`, `worksheet-b-answer`, `paradox`, `complete-graph`,
`baseline-idea`, `er-coin`, `er-clustering`, `fanout`, `fanout-solve`, `free-vs-not`,
`sigma-def`, `ws1998-dots`, `ws1998-sigma`, `ring-lattice`, `ring-distance`,
`random-graph`, `lattice-vs-random`, `ws-rewire-step`, `ws-rewire.gif`, `ws-sweep`,
`ws-band`, `ws-widget`, `shortcut-effect`, `disconnected`, `disconnected-answer`,
`degree-one`, `degree-one-answer`, `sigma-lt-1-q`, `grid-no-triangles`, `gnm-gnp`,
`gnm-gnp-answer`, `universality`, `sw-map`, `recap`, `m03-teaser` — 67 files.

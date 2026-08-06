# m05 DECK_SPEC — *The Club That Broke in Two*

Slide-by-slide outline for `m05-clustering.md`. Written from `plan.md`; every number in
it printed out of `figures/verify_numbers.py` before it was written down.

## Non-negotiables (restated from SLIDE_RUBRIC.md — check each slide against these)

- **P1** one new concept per slide. Two definitions on one slide is a Blocker.
- **P2** anything denser than title + one figure + one short block must build: `*` list
  markers fragment, `-` does not.
- **L1** at most one column of *text*. `cols` is text + figure, never text + text.
- **L2 no tables. L3 no code.** A prose pointer to the notebook is the only exception.
- **L5** never a paragraph below a fragmented list.
- **L6** shallow slides take `<!-- _class: mid -->`.
- **N4** a question slide carries the answer **nowhere** — body, note, figcaption or
  speaker note. The answer is the next slide.
- **N2** every concept slide has a figure. Question slides, dividers and the roadmap are
  the only exemptions.
- **F1** every visual difference means something the slide names.
- Bold marks key terms only; `strong` renders accent-2 red and stress-bolding spends it.
- KaTeX does not run inside a raw HTML block — no `$…$` in `figcaption` or `steps-list`.
  It **does** run in `<div class="formula">` when a blank line follows the opening tag.
- Figures are authored at final size: `full` = 1080bp, `col` = 537bp, height cap 380
  (`tight` 320, `stack` 190). The declaration in the generator and the container in the
  deck must agree.

## Corrections to plan.md (found while verifying, decided here)

| plan.md said | verified value | why |
|---|---|---|
| Louvain best Q = **0.4439**, real split Q = **0.3914** | **0.4198** and **0.3582** | `nx.karate_club_graph()` carries Zachary's interaction counts as edge weights and `nx.community.modularity` reads them by default. Those were *weighted* values. The deck defines Q with $A_{ij}\in\{0,1\}$, and 0.4198 is the literature's known maximum for this network. |
| Louvain best at `seed=1` | best over 200 seeds; 7 distinct partitions | the seed is not a fact about the network |
| node 9 "structurally John A.'s side, actually joined Mr. Hi" | confirmed, and now **reproduced** rather than cited | a weighted min cut between nodes 0 and 33 agrees with the recorded outcome on 33 of 34 and misses exactly node 8 (0-indexed) = Zachary's node 9 |
| "ZKCC: Cris Moore 2013, awarded by Aric Hagberg" | kept as an **aside in the speaker note only**, no year on the slide | the award year could not be re-verified offline; nothing unverified goes on a slide |
| resolution-limit example "requires constructing" | already exists | the lecturer's own `two-cliques.json` and `two-cliques-big-clique.json` contain the *same* two 5-cliques and land on opposite sides of √(2m) |

### Held over (plan.md is silent, recorded rather than decided in passing)

- The Bell number growth slide (Part 5). The tempting line — "more ways than there are
  atoms in the universe" — is **false**: B(34) = 2.12 × 10²⁸ against roughly 10⁸⁰ atoms.
  The slide states $B(34) \approx 2\times 10^{28}$ and stops. (Computed in
  `verify_numbers.py`, not quoted.)
- Whether the 10/07 hands-on session gets its own slides: plan.md says no. Part 7 opens by
  referring back to it, so the deck assumes it happened.

## Deck-level structure (S1–S5)

| act | parts | where |
|---|---|---|
| S1 story | Part 1 | 1970 karate club, Wayne Zachary, named people, dated split |
| S2 math of *that* story | Parts 2–3 | cliques counted in that club; Zachary's own min cut on that club |
| S3 generalization | Parts 4–6 | modularity, Louvain/Leiden, SBM |
| S4 edge cases as questions | Parts 7–8 | resolution limit, degeneracy, spurious structure, evaluation — every one opens as a question |

**Milestones (S5) — one interactive element per part:**

| part | interactive element |
|---|---|
| 1 | *Your turn*: draw the dividing line on paper, then hands up — the room disagrees |
| 2 | *Count with me*: peel the club down to its 4-core, one round at a time (GIF) |
| 3 | **Live demo** `graphcut × two-cliques` |
| 4 | *Your turn*: compute Q by hand on two triangles |
| 5 | Louvain run live in the notebook — different seed, different answer |
| 6 | *Your turn*: reorder the adjacency matrix until the blocks appear |
| 7 | **Live demos** `modularity × two-cliques-big-clique` and `modularity × random-net` |
| 8 | *Your turn*: compute NMI and the Rand index on six people |
| 9 | recap — no demo needed |

Demo URLs (already in the lecture note):
`https://skojaku.github.io/adv-net-sci/assets/vis/community-detection/index.html?scoreType=<graphcut|modularity>&numCommunities=<K>&randomness=1&dataFile=<file>.json`

---

# Slides

Format: **№ · title** — the one point · figure (`container/class`) · notes.
`Q:` marks a question slide (answer forbidden anywhere on it), `A:` its answer.

## Front matter

1. **The Club That Broke in Two** — `lead`. Eyebrow "Advanced Topics in Network Science ·
   Module 05", sub "thirty-four friends, and the line nobody could agree on". No figure.
2. **Roadmap for today** — `steps-list`, nine plain-text items (no math, KaTeX is dead in
   there). No figure.

## Part 1 · The club that broke in two  (S1: story) — slides 3–14

3. **divider** `part` — "Part One / 01 / 09 · The club that broke in two" · sub "1970, and
   an anthropologist with a notebook".
4. **Someone wrote the friendships down** — Wayne Zachary spent 1970–1972 recording which
   members of one American university karate club met each other *outside* the dojo ·
   `timeline-1970.png` (full/tight) · note carries the citation.
5. **Two men who could not agree** — the instructor **Mr. Hi** wanted the fees raised, the
   administrator **John A.** wanted them held; 34 members in between ·
   `the-dispute.png` (full).
6. **Thirty-four people, seventy-eight friendships** — the club as a network, uncoloured ·
   `karate-plain.png` (full) — **the reference layout; every later club figure reuses it.**
7. **Q: Point at the two groups** — `mid`, formula panel: "Two groups. Where does the line
   go?" No figure, no hint, no note that names anyone.
8. **Your turn** — MILESTONE. Draw your line on paper, then hands up ·
   `karate-three-guesses.png` (full) showing three *different* lines students actually
   propose, in gray. Not the answer — three disagreeing guesses.
9. **In 1972 the club actually split** — **17 against 17** · `karate-split.png` (full),
   Mr. Hi's club accent, the officers' club accent-2.
10. **Eleven friendships crossed the line** — 35 inside one club, 32 inside the other, 11
    torn · `karate-crossing.png` (full), the 11 crossing edges heavy accent-2.
11. **Q: Why should a network have groups at all?** — `mid`. No figure.
12. **A: four reasons, and they are not the same reason** — homophily, shared function,
    hierarchy, shared information paths (**c02**) · `why-groups.png` (full) — one drawing
    with four labelled regions, not four panels · fragmented list.
13. **The only club whose answer really happened** — most networks have no answer key;
    this one has a dated, recorded outcome · `ground-truth-or-not.png` (full): the club
    with its recorded split beside a network with a question mark where the answer would
    be · ZKCC trophy anecdote lives in the **speaker note**.
14. **Today's question** — `mid`, formula: "What is a community — and how would you know
    the one you found is real?" Sub-line naming the two halves of the module.

## Part 2 · What counts as a group?  (S2) — slides 15–26

15. **divider** — "Part Two / 02 / 09 · What counts as a group?" sub "the first instinct,
    and how it fails".
16. **Everyone knows everyone** — **clique** (**c04**) · `clique-def.png` (col) beside the
    definition · one point: the strictest possible group.
17. **Q: How large is the biggest clique in the club?** — `mid`, with the plain club figure
    (col) and nothing else. Poll the room for a number.
18. **A: five people — and only two such groups** — both contain Mr. Hi, neither contains
    John A. · `karate-max-clique.png` (full), the five ringed.
19. **Q: One missing friendship, and the group is disqualified?** — `mid`, no figure.
20. **Relax the degree: k-plex** — each member may be missing at most k of the others
    (**c05**) · `k-plex.png` (col).
21. **Relax it the other way: k-core** — each member keeps at least k friends *inside*
    (**c06**) · `kcore-peel.gif` (full) — MILESTONE, peel the club with the room; it stops
    at the **4-core, 10 people**.
22. **Relax the density: ρ-dense** — at least ρ of the possible edges (**c07**) ·
    `rho-dense.png` (col).
23. **Relax the distance: n-clique** — every member within n steps (**c08**) ·
    `n-clique.png` (col) · n-clan / n-club named once in the note, not defined.
24. **Mix the axes: k-truss** — every *edge* sits in at least k−2 triangles (**c09**) ·
    `k-truss.png` (col).
25. **Q: Did any of those split the club in two?** — `mid`, no figure.
26. **A: no — they overlap, they multiply, they do not partition** (**c10**), so the
    problem is **ill-posed** (**c03**) · `patterns-overlap.png` (full): four pattern-groups
    shaded on the club, overlapping, leaving people in none of them.

## Part 3 · Zachary's own answer — cut it  (S2) — slides 27–39

The small graph used for the arithmetic — nine members, two 4-cliques joined by two
friendships, one person attached to a single friend — is drawn planar and reused across
slides 29–35 so the numbers can be followed by hand.

27. **divider** — "Part Three / 03 / 09 · Cut it" sub "Zachary stopped looking for groups".
28. **Stop looking for groups. Look at what runs between them** — the reframe · `cut-idea.png` (full).
29. **Cut(V₁,V₂)** — the number of friendships crossing the line (**c11**) ·
    `cut-def.png` (col) beside the formula, crossing edges accent-2, **cut = 2**.
30. **Q: So find the smallest cut. This problem is incompletely stated 😈** — what is
    missing? `mid`, no figure.
31. **Live demo** — MILESTONE. `graphcut × two-cliques`; drag the slider and watch the
    solver walk to the cheap answer · `two-cliques.png` (full) · demo URL in the note.
32. **A: the cheapest cut peels one person off** (**c12**) — in this club there is exactly
    one member with a single friend, node 12, and cutting him away costs **1** ·
    `karate-trivial-cut.png` (full).
33. **So divide by something: ratio cut** (**c13**) — cut / (|V₁|·|V₂|). Peeling the leaf
    scores 1/8 = 0.125; the sensible split scores 1/10 = 0.100 · `ratio-cut.png` (full).
34. **What the normalizer does** — |V₁|·|V₂| is largest at equal halves, smallest when one
    side holds one person · `normalizer-curve.png` (full), an Axes line over split size.
35. **Normalized cut** (**c14**) — balance by *edges* inside each side, not people:
    2/(7·6) = 1/21. The lone person has **no** internal edges at all, so normalized cut
    will not even score him · `norm-cut.png` (full).
36. **More than two groups** (**c39**) — sum each group's escaping edges over its own size
    · `k-way-cut.png` (full).
37. **Zachary ran his own network through it** — the cut agrees with what happened for
    **33 of the 34 members** · `karate-mincut.png` (full): predicted split, the one
    disagreement ringed in accent-2, unnamed.
38. **One person it got wrong** — `mid`. He is not named today; the last session comes back
    to him · `karate-node9-ring.png` (full), a single ring, nothing else changed.
39. **Q: but the cut wants you to know K first** (**c40**), it prefers equal halves
    (**c41**), and finding the best one is NP-hard (**c42**) — *what do you do when you do
    not know how many groups there are?* `mid`, day-one cliffhanger, no figure.

## Part 4 · More than chance  (S3) — slides 40–53

40. **divider** — "Part Four / 04 / 09 · More than chance" sub "a second opinion about what
    a group is".
41. **Not "cheap to cut" — "more inside than chance"** (**c15**) · `chance-idea.png` (full):
    two networks with the same cut size, only one of which is surprising.
42. **Every friendship is two coloured balls on a string** (**c43**) · `balls-strings.gif`
    (full), stage 1 only — the colour is the community.
43. **Pull a string: how often do the ends match?** — the **observed** fraction ·
    `observed.png` (full) + formula panel.
44. **Q: paint everyone the same colour and every string matches. Have you found
    anything?** — `mid`, no figure.
45. **A: no. So we need what chance would give** — cut every string, drop the balls in a
    bag · `balls-strings.gif` frame set 2 (full).
46. **The bag holds 2m balls** (**c44**) — a member with k friends donates k of them, so
    her colour comes up k/2m of the time · `bag-2m.png` (full).
47. **Draw two balls: how often do *they* match?** — the **expected** fraction ·
    `expected.png` (full) + formula panel.
48. **Modularity = observed − expected** (**c17**, first form) · `modularity-gap.png`
    (full): the two fractions on one axis with the gap named.
49. **The same thing, written the usual way** — $Q=\frac{1}{2m}\sum_{ij}[A_{ij}-\frac{k_ik_j}{2m}]\delta(c_i,c_j)$
    · `modularity-matrix.png` (full): one cell of the adjacency matrix beside its null
    term · the algebra (**c45**) is a note pointer, not a slide.
50. **What "chance" actually is: the configuration model** (**c16**) — rewire every
    friendship at random, keep every degree · `configuration-model.png` (full), before /
    after.
51. **Your turn: compute Q by hand** — MILESTONE. Two triangles joined by one edge, m = 7 ·
    `worksheet-q.png` (full). No answer anywhere on the slide.
52. **A: Q = 5/14 ≈ 0.357** — one group scores exactly 0; the crossed grouping scores
    −3/14. Q lives in [−1, 1] and people quote 0.3 as the threshold for "real"
    (**c18** — *and Part Seven kills that number*) · `worksheet-q-answer.png` (full).
53. **What the cut could not do: Q picks K by itself** (**c46**) — the same nine members
    scored at K = 1, 2 and 3 · `q-picks-k.png` (full).

## Part 5 · Climbing Q  (S3) — slides 54–61

54. **divider** — "Part Five / 05 / 09 · Climbing Q" sub "and why every method here is a
    guess".
55. **Q: how many ways can you split 34 people into groups?** — `mid`, no figure.
56. **A: about 5 × 10²⁷ — and finding the best is NP-hard** (**c19**); everything that
    follows is a heuristic with no guarantee · `bell-growth.png` (full), log axis.
57. **Louvain, phase one** (**c21**) — move each member into whichever neighbouring group
    raises Q most, until nothing helps · `louvain.gif` (full), phase-one frames.
58. **Louvain, phase two** — collapse each group into one node and do it again; the
    **hierarchy is a by-product** · `louvain.gif` continues into the collapse.
59. **Q: must a group Louvain returns be connected inside?** — `mid`, no figure.
60. **A: no — and Leiden fixes it** (**c22**) — a broker moved early can leave its group in
    two pieces; Leiden refines before collapsing · `leiden-fix.png` (full).
61. **Every method answers a different question** (**c25**) — cut, modularity, spectral
    (M08), random walk (M07), generative · `four-answers.png` (full): one network, four
    partitions.

## Part 6 · The generative flip — SBM  (S3) — slides 62–72

62. **divider** — "Part Six / 06 / 09 · Turn it around" sub "communities first, network
    second".
63. **Build the network from the groups, not the groups from the network** (**c29**) ·
    `sbm-flip.png` (full).
64. **Sort the members by group and the matrix shows blocks** · `sbm-blocks.png` (full).
65. **One small matrix decides everything** (**c30**) — the chance of an edge depends only
    on the two groups · `block-matrix.png` (full).
66. **p_in > p_out: the communities you already know** · `sbm-assortative.png` (full).
67. **Q: what would you see if p_in < p_out?** — `mid`, no figure.
68. **A: groups that connect outward** (**c52**) — disassortative structure, still perfectly
    real structure; and p_in = p_out collapses the whole model to a random graph ·
    `sbm-three-cases.png` (full).
69. **So a community is a shared *pattern*, not a dense lump** (**c31**) — back to the
    broad definition from Part One · `sbm-pattern.png` (full): a group whose members have
    **no** edges among themselves and are still a group.
70. **Detection becomes inference** (**c32**) — choose the assignment that makes the
    observed network most likely; model selection replaces an arbitrary score ·
    `sbm-inference.png` (full) · likelihood algebra (c49–c51) is a note pointer.
71. **Your turn: find the blocks** — MILESTONE. A shuffled adjacency matrix; reorder rows
    and columns until the blocks appear · `sbm-shuffled.png` (full).
72. **You have the tools. Next week you run them** — `mid`, day-two close, pointer to the
    hands-on session (prose only, no code).

## Part 7 · Three ways modularity lies  (S4) — slides 73–85

73. **divider** — "Part Seven / 07 / 09 · Three ways modularity lies" sub "last week you
    pulled Q > 0.3 out of a random graph".
74. **Q: two cliques joined by one friendship. Does modularity separate them?** — `mid` with
    `two-cliques.png` (col).
75. **A: yes — 0.4524 against 0.0000** · `two-cliques-split.png` (full).
76. **Q: now add a third, much larger group. What happens to those two cliques?** — `mid`,
    no figure.
77. **Live demo** — MILESTONE. `modularity × two-cliques-big-clique` ·
    `big-clique-net.png` (full) · demo URL in the note.
78. **A: the two cliques are merged** (**c26**) — Q(merged) 0.1410 beats Q(split) 0.1404,
    and **the cliques themselves did not change** · `resolution-limit.png` (full),
    before / after.
79. **The threshold is √(2m)** — alone: √42 = 6.5, and each clique holds 10 internal
    friendships, so they survive. In company: √548 = 23.4, and the same 10 no longer clear
    it · `sqrt2m.png` (full), the curve with both cases marked.
80. **Which means the whole network decides** — a group's fate is set by m, a number it has
    no part in · `non-local.png` (full).
81. **Q: is there one best partition?** — `mid`, no figure.
82. **A: no — the landscape is rugged** (**c27**). Best 0.4198, runner-up 0.4151, one
    percent apart, and **32 pairs of members disagree about being together** ·
    `degeneracy.png` (full).
83. **Q: what does modularity return on a network with no groups at all?** — `mid`, no figure.
84. **Live demo** — MILESTONE. `modularity × random-net` · `random-net.png` (full).
85. **A: Q = 0.657 — higher than the two-clique network's 0.452** (**c28**). Two hundred
    random graphs with the club's own 34 nodes and 78 edges average **0.354**, and the
    split that really happened scores **0.358**. **Every one of the two hundred clears
    0.3** (**c47**) · `random-q-dots.png` (full), a dot strip with the real split marked.

## Part 8 · How would you know?  (S4) — slides 86–102

86. **divider** — "Part Eight / 08 / 09 · How would you know?" sub "three methods, three
    answers".
87. **Three methods gave three different clubs** · `three-partitions.png` (full).
88. **Without an answer key: conductance** (**c34**) — escaping edges over the group's own
    volume · `conductance-def.png` (col).
89. **Conductance scores one group at a time** — the real split scores 11/75 = 0.147 ·
    `conductance-karate.png` (full).
90. **And every internal score just rewrites a definition** — conductance ranks the real
    split (0.147) above all four Louvain groups (0.23–0.42); modularity ranks Louvain
    first. Neither failed an exam; they answered different questions ·
    `scores-disagree.png` (full).
91. **With an answer key, the unit is the pair** — six members, fifteen pairs ·
    `pairs-15.png` (full).
92. **NMI, part one: how much does one labelling tell you about the other?** — mutual
    information I(X;Y) · `mutual-information.png` (full).
93. **NMI, part two: divide by how much there was to know** (**c35**) — NMI = 2I/(H+H),
    landing in [0,1] · `nmi-formula.png` (full).
94. **Your turn: score this** — MILESTONE. Six members, truth 3+3, one placed wrongly ·
    `worksheet-nmi.png` (full). No answer on the slide.
95. **A: NMI = 0.479** — and counting pairs instead: **Rand = 10/15 = 0.667** ·
    `worksheet-nmi-answer.png` (full).
96. **Q: a coin-flip partition already scores two thirds. How do you fix a score like
    that?** — `mid`, no figure.
97. **A: subtract what chance would have given — ARI** (**c36**) — the same worksheet drops
    to **0.324**; 0 means chance, negative means worse · `ari.png` (full).
98. **Report both** — NMI rewards splitting into many small groups, ARI is conservative ·
    `nmi-vs-ari.png` (full).
99. **Back to the club: the best score is not what happened** — Louvain's best is **four
    groups at Q = 0.4198**; the 17-against-17 that really happened scores **0.3582** ·
    `best-vs-real.png` (full).
100. **And it matches reality less well** — against the recorded outcome Louvain scores
     NMI 0.588, while Zachary's 1977 cut scores **0.837**. The higher Q is the worse
     answer · `nmi-comparison.png` (full).
101. **And that one person: node 9** — structurally an officer; he joined Mr. Hi because his
     black-belt test was three weeks away and switching would have cost him his rank.
     **Structure cannot see a belt test** · `node9.png` (full).
102. **Metadata is not ground truth** (Peel, Larremore & Clauset 2017) and there is **no
     free lunch** (**c48**) — a low score may mean the method failed or that the labels
     have nothing to do with the wiring, and nothing in the score tells you which ·
     `no-free-lunch.png` (full).

## Part 9 · Where this lands  — slides 103–106

103. **divider** — "Part Nine / 09 / 09 · Where this lands".
104. **Four places this is already running** (**c37**) — echo chambers, protein complexes,
     autonomous systems, research fields · `applications.png` (full).
105. **Module 05 in one picture** — the four acts · `recap.png` (full).
106. **Coming up in Module 06** — the club broke in two because it had two hubs: Mr. Hi with
     **16** friends and John A. with **17**. Today asked *which group*; next asks *which
     person* · `m06-teaser.png` (full).

**106 slides.**

## Figure inventory (46 stills + 2 GIFs) → `FIGURE_SPEC.md`

The club's reference layout is drawn once and shared by 14 figures; every figure that
recolours it changes **colour only**, never a position. Mechanism figures (cut, ratio cut,
configuration model, conductance, k-plex …) use small planar graphs of 5–10 nodes, because
34 nodes and 78 edges cannot be drawn without crossings and a mechanism slide must not ask
the room to trace one.

# m06 "All Roads Lead to Rome" — deck spec

Slide-by-slide plan for `m06-centrality.md`, expanded from `plan.md`.
Sessions 10/14 (Parts 1–4) and 10/16 (Parts 5–8). **101 slides as built.**

Every number below was printed out of `figures/verify_numbers.py` before it was written
here, and the figure generator imports the same functions rather than repeating a value.
m01 shipped two arithmetic errors *through* a spec; that is what this rule is for. Run:

    python3 figures/verify_numbers.py        # exits 0, prints everything quoted below

---

## Non-negotiables (restated from SLIDE_RUBRIC.md — check each slide against these)

- **One point per slide** (P1). Two definitions on one slide is a Blocker.
- **Fragments use `*`, never `-`.** `-` does not animate in Marp.
- **A question slide carries no answer anywhere — including the gray `note`.** The answer
  goes on the *next* slide. This has leaked twice in earlier modules.
- **No tables** (L2), **no code** (L3), **at most one column of text** (L1). `cols` is
  text + figure only.
- **No paragraph below a fragmented list** (L5) — the room reads it before the build runs.
- **Every concept slide has a figure** (N2). Question slides, dividers and the roadmap are
  the only exemptions.
- **Bold marks key terms only.** `strong` renders accent-2 red; stress-bolding kills it.
- **Shallow slides take `<!-- _class: mid -->`** (L6) — most question slides.
- **KaTeX does not run inside `<figcaption>` or `<div class="steps-list">`.** Write the
  symbol as a word there ("lambda-max"), never `$…$`.
- Max 4 bullets, one list per slide (L4).
- Figures: author at final size (1 bp = 1 slide px), in-figure x-height ≥ 15.5 px on the
  slide, node discs 26–52 px, palette tokens only, **no green, no bar charts**, zero edge
  crossings wherever the graph is planar.

## Containers

Marp wraps every figure in a `<p>`, and `section p { max-width: 1080px }` binds before the
1120 px content area. So a full-width figure is authored at **1080 bp**, a `cols` figure at
**537 bp**, and the deck's scale factor is 1.000 — a 36 pt in-figure label lands at 36 px
type / 15.5 px x-height on the slide. Height caps: 380 px (`.fig`), 320 px (`.fig tight`),
190 px (`.fig stack`).

---

# THREE DECISIONS TAKEN DURING THE BUILD, AND WHY

Recorded here because each of them departs from `plan.md`, and the next person
should see the reason rather than rediscover it.

**1. The crown does not move on the Roman map, and the deck says so.** See below.

**2. Every Roman-map figure is full width, and the deck stacks text above it.**
`plan.md` assumed the house two-column pattern. It is not available for this map:
twelve cities with names like "Thessalonica" cannot be labelled at the 36 pt
in-figure type floor inside a 537 px column — on a true longitude/latitude
projection they cannot be labelled at 1080 px either, and three cities have zero
collision-free sides before any other label is placed. The map's coordinates
therefore come from an annealing search (planarity, disc clearance and
label-solvability hard; geographic faithfulness the objective), the theme gained a
`.fig tall` modifier measured against a real render, and the map slides carry one
line of text above the figure instead of a column beside it.

**3. The crown-summary figure is one map, not a six-panel build.** The deck has
already shown each metric map on its own slide; replaying all six adds five slides
and no information. The closing figure shows the one fact they share.

# THE DECISION THAT RESHAPED THE PLAN

`plan.md` asked for a Roman road map on which the crown moves from metric to metric — the
stated defence against a centrality-catalogue lecture. **That map does not exist honestly.**

Rome is the node the network was *built around*, so on the eighteen best-documented routes
it takes every crown outright and shares only the worst-case one. The obvious repair —
tune the edge set until the crown moves — was rejected: it puts a map on the slide that was
chosen for its answer. (The first version of `verify_numbers.py` claimed every reversal
required deleting a real route; an assertion caught that, because 1701 variants disagreed.
Some reversals *are* honest. They are just not the honest map.)

So the deck asks the question the other way round, and this turns out to be the better
lecture. `crown_robustness()` enumerates all **4992** drawable, connected variants of the
documented route pool that keep Rome's own five routes and the western backbone:

    degree        100.0%     <- the same answer on every map anyone could have drawn
    closeness      96.2%
    harmonic       96.2%
    betweenness    93.6%
    katz           85.2%
    eccentricity   84.6%
    eigenvector    79.2%     <- the least robust

**The spine of the deck is therefore:** *importance is not one thing, and the metrics that
disagree most are the ones that depend most on how you drew the map.* The catalogue risk is
answered three ways instead of one:

1. **One map, one geometry, seven scores.** Every metric slide reuses the identical
   12-city drawing; only the node shading and the crown change (F1).
2. **The crown moves where it honestly moves** — on the students' own club network in
   Part 1 (three questions, three different students) and on the 8-page web in Part 7
   (the page HITS crowns as the best hub is the page PageRank ranks last of eight).
3. **The same equation, discovered six times** — the genealogy slide, placed immediately
   before PageRank.

---

# VERIFIED NUMBERS

## The Roman road network — 12 cities, 18 documented routes

Positions are roughly true (longitude, latitude); the map and the graph are the same
picture. Diameter **5**. Planar as drawn: **zero crossings** (asserted).

Routes, each with what the lecturer says if asked:

| route | what it is |
|---|---|
| Roma–Mediolanum | Via Flaminia into the Via Aemilia |
| Roma–Massilia | Via Aurelia along the Ligurian coast |
| Roma–Carthago | the African grain run out of Ostia |
| Roma–Thessalonica | Via Appia, the Brundisium crossing, then the Via Egnatia |
| Roma–Alexandria | the Alexandrian grain fleet |
| Mediolanum–Lugdunum | Via Agrippa over the Alps |
| Mediolanum–Colonia | the Rhine-Alpine route through Raetia |
| Lugdunum–Massilia | Via Agrippa down the Rhône |
| Lugdunum–Colonia | Via Agrippa north to the Rhine |
| Colonia–Londinium | the road to Gesoriacum and the Channel crossing |
| Massilia–Tarraco | Via Domitia into the Via Augusta |
| Tarraco–Carthago | the sea lane from Hispania to Africa |
| Carthago–Alexandria | the North African coast road |
| Thessalonica–Byzantium | Via Egnatia to the Bosporus |
| Thessalonica–Athenae | the road south through Thessaly |
| Athenae–Byzantium | the Aegean sea lane |
| Athenae–Alexandria | the sea lane to the Nile delta |
| Byzantium–Alexandria | the coastal run past Asia Minor and Syria |

*(The table is spec-only. It never appears on a slide — L2.)*

Degrees: Roma 5 · Alexandria 4 · Colonia, Lugdunum, Massilia, Mediolanum, Carthago,
Thessalonica, Athenae, Byzantium 3 · Tarraco 2 · **Londinium 1**.

The only bridge is **Colonia–Londinium**, the Channel crossing. Cutting it is the deck's
disconnection demo.

### Crowns and podiums

| metric | crown | podium (score, roads) |
|---|---|---|
| degree | **Roma** | Roma 5 · Alexandria 4 · eight cities at 3 |
| closeness | **Roma** | Roma 0.611 · Alexandria 0.500 (4) · Massilia 0.500 (3) |
| harmonic | **Roma** | Roma 7.833 · Alexandria 6.917 · Massilia 6.500 |
| eccentricity | **Massilia, Mediolanum, Roma** (3-way tie) | all 0.333 · Alexandria 0.250 |
| betweenness | **Roma** | Roma 0.503 (5) · **Mediolanum 0.270 (3)** · Alexandria 0.182 (4) |
| eigenvector | **Roma** | Roma 1.000 · **Alexandria 0.919** · Thessalonica 0.715 |
| katz | **Roma** | Roma 1.000 · Alexandria 0.888 · Thessalonica 0.710 |

Three facts the deck names out loud, all asserted:

- **Alexandria trails Rome by 8% on eigenvector and by a whole road on degree.** Being next
  to strong neighbours nearly closes a gap that counting cannot.
- **Mediolanum is second in betweenness with three roads, ahead of Alexandria's four.**
  The broker beat, on the real map, without inventing anything.
- **Rome can only tie the eccentricity crown.** The worst-case ruler is too coarse to
  separate three cities — the first crack, and it arrives in Part 3.

### Spectrum, Katz and power iteration

- λ_max = **3.3461**, so 1/λ_max = **0.2989**
- Katz uses λ = **0.2540** (0.85 of critical)
- at λ = **0.3437** (1.15 of critical) **eleven of the twelve scores go negative**
- the slowest decaying mode is |λ/λ₁| = **0.795** — and it is the most *negative*
  eigenvalue, not the second largest. Writing "|λ₂/λ₁|" would have quoted 0.72 for a
  process that converges at 0.80.
- power iteration: **step 1 is exactly the degree ranking**; the crown settles at
  **step 1**, the podium at **step 4**; at step 12 the largest error is **0.008**

### Cutting the Channel crossing

- **every** closeness score becomes 0.0 — not just Londinium's, all twelve, one flat value
- harmonic still ranks: Roma 7.50 · Alexandria 6.67 · Carthago 6.17 · Massilia 6.17, across
  **8 distinct levels**, and Londinium alone scores 0.0

### Attacking the map (M03 recall)

Adaptive removal, recomputing after each strike. Both strategies open on Rome and part
company on the **second**:

- by degree: Roma, then **Alexandria** (4 roads) → **7 of 12** cities still joined
- by betweenness: Roma, then **Tarraco** (2 roads) → **5 of 12** still joined

*(k = 2 is the number the slide names because it is where they differ; at k = 3 and k = 5
they tie, and quoting those would be a false callback.)*

### The redraw (Part 8)

Drop the Thessalonica–Athenae road; add Mediolanum–Thessalonica (Via Postumia, Aquileia,
then the Balkan road) and Carthago–Massilia (the Africa-to-Gaul sea lane). Every route is
as documented as every route in the map above, and the drawing still has zero crossings.

**The betweenness crown moves to Mediolanum. Degree, closeness, harmonic, eigenvector and
Katz do not move at all.**

## The club network — 13 students, 17 edges

Straight out of `docs/lecture-note/m06-centrality/pen-and-paper/exercise.tex`, so the
network the room draws in Part 1 is the network the handout asks about at the end of the
day. Each club is a clique over its members. Planar, diameter 5.

- **tell first (degree): Noah** — 6 friends
- **closest to everyone (closeness): Sophia** — 4 friends
- **coordinates between clubs (betweenness): Alex** — 4 friends

Three questions, three different students, before a single formula. This is slide 12.

## The eight-page web — 8 pages, 14 links

`A_ij = 1` means **i links to j**. One dangling page (**Home**, no out-links). One page of
links (**Links**, four out-links and *zero* in-links).

- **hub crown: Links** (1.00) · News 0.75 · Course 0.66
- **authority crown: Blog** (1.00) · Wiki 0.80 · News 0.60
- **PageRank crown: Blog** (0.245) · Course 0.236 · Wiki 0.172
- **PageRank ranks Links — the hub king — 8th of 8.** That is the disagreement.
- with no teleportation at all, the total score drains to **zero** (asserted): every drop
  leaks into the dead end
- personalized on **Course**: Course 0.402 · Blog 0.277 · Wiki 0.194 · News 0.083. Globally
  Blog leads Course by 0.009; personalizing turns that into Course leading by 0.125.
- personalized PageRank equals the discounted-reachability sum to 1e-6 (asserted)

## Small verified graphs

- **σ demo** (S–A–T, S–B–T, T–D): σ_SD = 2, one route through A, one through B, **both**
  through T. So A and B earn ½ each and T earns a whole one. Betweenness (unnormalised):
  T 3.5 · A 1.0 · B 1.0 · S 0.5 · D 0.
- **broker**: two 4-cliques joined through one node M of degree 2. M holds the betweenness
  crown with **16** pairs through it and is nowhere in the degree ranking.
- **star** (7 nodes): the hub's closeness is **exactly 1.0**, and **every** metric crowns it.
- **path** (7 nodes): degree crowns **five** nodes at once; betweenness crowns **one**, the
  middle.
- **localization**: a 5-clique with a 4-node tail. The far tail node scores **0.0045** of
  the top on eigenvector and **0.184** on Katz — a 41× lift from the floor.

## Cost (c25)

degree O(m), one pass · closeness and betweenness O(nm) (Brandes 2001) · eigenvector and
PageRank O(m) *per iteration*. On n = 10⁶, m = 10⁷: an all-pairs sweep is ~10¹³ operations
against ~3×10⁸ for thirty power-iteration steps — a factor of about **33,000**.

## History (each checked before it was written)

The four mileages on `milestone-radial` are the deck's **only hand-entered numbers**: approximate road distances from Rome in Roman miles (Gades 1650, Londinium 1310, Byzantium 1120, Alexandria 1560), taken from the road itineraries rather than computed from the graph. The figcaption says "roughly" for that reason.

Milliarium Aureum: erected by **Augustus in 20 BC**, in the Forum Romanum, as
*curator viarum*. Aesop: 6th century BC. Perron **1907**, Frobenius **1912**. Bavelas
**1950** (closeness). Katz **1953**. Hubbell **1965**. Beauchamp **1965** (harmonic).
Bonacich **1972**. Freeman **1977** (betweenness). Kleinberg **1999** (HITS).
Brin & Page **1998** (PageRank, Stanford). Brandes **2001**. Landau **1895** (chess
tournaments). Seeley **1949** (children's popularity).

---

# SLIDE-BY-SLIDE

Legend: **[Q]** question slide, carries no answer anywhere · **[A]** the answer slide ·
**[M]** milestone activity · figure names match `review/FIGURE_SPEC.md`.

## Front matter — 3 slides

**1. Lead** — `_class: lead`. Eyebrow "Advanced Topics in Network Science · Module 06".
Title **All Roads Lead to Rome**. Sub: *…do they?* Credit line.
*Notes: open on a stone in a forum, not on a definition.*

**2. The question for today** — `_class: mid`. Formula panel: "Which city is the most
important — and important in *what sense*?" One line under it: "The second half of that
question is the whole module." No figure.

**3. Roadmap** — `steps-list`, eight items, one per part. No math in the list (KaTeX does
not run there).

## Part 1 — The Golden Milestone · 9 slides (4–12) · Act 1

**4. Divider** — `part`, band "Part One · 01 / 08", title *The Golden Milestone*,
sub "Rome decided who mattered, and wrote it in bronze".

**5. 20 BC, the Forum Romanum** — Augustus erects the **Milliarium Aureum**. Real names,
date, place (S1). Figure `milestone.png` (the monument's surviving base, drawn). One text
block; no list.

**6. Every distance was measured from this stone** — importance **by decree**.
Figure `milestone-radial.png`: the stone at the centre, distances radiating out with real
mileages to four provinces.
*Notes: this is the last time in the course that importance is something anyone can declare.*

**7. The roads themselves** — the Mediterranean with the real routes drawn on it.
Figure `roma-map.png`. Caption names three roads by name.

**8. The same picture, without the coastline** — the abstraction step: cities become discs,
routes become edges, the geometry does not move. Figure `roma-graph.png` — **this drawing
is the base of every metric slide in the deck** (F1).

**9. [Q] Which city is the most important?** — `_class: mid`, figure `roma-graph.png`,
one line: "Point at one. Do not explain yet." **No answer anywhere on this slide.**

**10. [M] Your turn: your own network** — the club roster (Drama, Art, Volunteer, Sailing,
Chess, Debate, Math, Tennis). "Draw a line between two students who share a club."
Figure `club-blank.png` — the thirteen names, no edges.
*This is Question 1 of the take-home handout; they meet it again tonight.*

**11. [Q] Two jobs, one network** — `_class: mid`. Two questions in the formula panel:
"Who do you tell first, to spread news fastest?" and "Who do you make Club Coordinator?"
No figure, no answer, no hint.

**12. [A] You have already invented three different answers** (**c01**) — figure
`club-three-kings.png`: the same club network three times as a build, crowning **Noah**
(6 friends), **Sophia** (4), **Alex** (4).
*The point: nobody has defined anything yet, and the room already disagrees.*

## Part 2 — Count the roads · 6 slides (13–18) · Act 2 begins

**13. Divider** — "Part Two · 02 / 08 · Count the roads".

**14. Degree centrality** (**c02**) — the definition, in a formula panel:
$c_i = \sum_j A_{ij}$. Figure `degree-count.png`: one city, its edge-ends marked one at a
time.

**15. On the map → the first crown** — figure `roma-degree.png`. Roma, five roads.
Alexandria second with four. *The proverb checks out.*

**16. The cheapest thing you can ask** — you never need to see the whole network; a node
knows its own degree. Figure `degree-local.png` — the same map with everything beyond one
city's neighbours greyed out.

**17. [Q] Is counting roads enough?** — `_class: mid`. No figure needed; one line:
"Rome has five. Alexandria has four. Is that the whole story?"

**18. [A] Degree sees exactly one step** — and there are two ways to see further:
**distance** (Parts 3–4) and **walks** (Parts 5–7). Figure `two-roads-ahead.png`: the same
map with a one-step ring and a two-step ring around one city.

## Part 3 — Close to everything · 12 slides (19–30)

**19. Divider** — "Part Three · 03 / 08 · Close to everything".

**20. The Milliarium's own logic** (**c03**) — central means *close to everything*.
Figure `roma-distance-rings.png`: shortest-path distance from Rome, drawn as bands.

**21. Closeness centrality** (**c04**) — $c_i = (N-1)/\sum_j d(i,j)$. Figure
`closeness-one-city.png`: one city with its twelve distances written on the map.

**22. [M] Your turn: do one by hand** — give the room **Massilia**. "Write the distance to
all eleven others, add them, divide." Figure `closeness-blank.png` — Massilia highlighted,
distances blank. Thirty seconds, then call numbers out.

**23. [A] The second crown** — Massilia's sum is 22, so its score is 11/22 = 0.500; Rome's
is 18, so 11/18 = **0.611**. Figure `roma-closeness.png`. Rome again.

**24. [Q] Why divide by N−1?** — `_class: mid`.

**25. [A] So the best possible score is exactly 1** (**c28**) — the centre of a star, where
every other node is one step away. Figure `star-closeness.png`, hub annotated 1.0.

**26. [Q] What if the network is cut?** — `_class: mid`. One line: "A storm closes the
Channel crossing for a season." Figure `roma-cut.png` (the map with that one edge gone) —
**the figure shows the cut, not the consequence**.

**27. [A] One unreachable city zeroes every score** (**c05**) — all twelve, one flat value,
because one infinite distance makes every sum infinite. Figure `roma-cut-closeness.png`:
every disc the same shade, no crown.

**28. Harmonic centrality: take the reciprocal first** (**c06**) — $c_i = \sum_j 1/d(i,j)$,
so an unreachable city contributes 0 instead of ∞. Figure `roma-cut-harmonic.png`: the same
cut map, still ranked, Rome 7.50, Londinium alone at 0.

**29. [Q] Would you site a fire station on the average?** — `_class: mid`. "Closeness
minimises the *average* trip. Is that what a fire station is for?"

**30. [A] Eccentricity minimises the worst case** (**c07**) — $c_i = 1/\max_j d(i,j)$, and
here **Rome can only tie**: Massilia, Mediolanum and Rome all reach everything within 3.
Figure `roma-eccentricity.png` with **three** crowns.
*The first crack: a ruler coarse enough to tie is a ruler that cannot rank.*

## Part 4 — The broker · 11 slides (31–41) · end of day 1

**31. Divider** — "Part Four · 04 / 08 · The broker".

**32. [Q] Who must a traveller pass through?** — `_class: mid`, figure `roma-graph.png`.
"You are carrying a letter from Londinium to Alexandria. Trace it."

**33. Betweenness centrality** (**c08**) — the definition,
$c_i = \sum_{j<k} \sigma_{jk}(i)/\sigma_{jk}$. Figure `betweenness-idea.png`: one node with
the shortest paths that cross it drawn through.

**34. Counting shortest paths** (**c09**) — σ_jk is how many there are, σ_jk(i) how many use
i; **ties are shared, never double-counted**. Figure `sigma-graph.png`.

**35. [M] Your turn: count them** — "How many shortest S–D routes are there? How many go
through A? Through T?" Figure `sigma-blank.png`. **No answer on the slide.**

**36. [A] Two routes, so a half each** — σ_SD = 2; A carries one, B carries one, **T carries
both**. So A and B earn ½ and T earns 1. Figure `sigma-answer.png` with the fractions drawn.

**37. On the map → the third crown** — figure `roma-betweenness.png`. Rome, 0.503.

**38. Look at second place** — **Mediolanum, 0.270, with three roads** — ahead of
Alexandria's 0.182 with four. Figure `roma-betweenness-runnerup.png`: the same map,
Mediolanum ringed, the two road-counts annotated.
*The first time in the deck that fewer connections beat more.*

**39. Bridges and brokers** (**c10**) — the pure case: two tight groups joined through one
node of degree 2, which holds 16 of the pairs and is nobody by degree. Figure `broker.png`.
Names Burt's structural holes in one line; points forward to M05's Girvan–Newman.

**40. M03, revisited** — attack the map. Two strikes by **degree** take Rome and Alexandria
and leave 7 of 12 cities joined; two strikes by **betweenness** take Rome and **Tarraco, a
city with two roads**, and leave 5. Figure `attack-compare.png` (two small maps, a build).

**41. [M] Tonight, and a question to sleep on** — the handout
*"Who's the Big Cheese in the University Clubs?"* — the same thirteen students from
slide 10. Cliffhanger in the formula panel: **"Is a city important because it is important?"**
Figure `club-three-kings.png` reused (identical content, same explanation — reuse is safe
here and only here).

## Part 5 — Known by the company you keep · 13 slides (42–54) · day 2, Act 3

**42. Divider** — "Part Five · 05 / 08 · Known by the company you keep". No recap slide;
the deck restarts from the divider (as m01 and m03 do).

**43. Aesop, 6th century BC** — *"A man is known by the company he keeps."* Figure
`same-degree-different-friends.png`: two nodes with identical degree whose neighbours are
not comparable.

**44. Importance you inherit** (**c11**) — a node is important if its neighbours are.
Figure `recursive-flow.png`: score arriving at one node from its neighbours.

**45. [Q] Isn't that circular?** — `_class: mid`. "To know Rome's score I need Milan's. To
know Milan's I need Rome's. Can this be computed at all?"

**46. [A] It is an eigenvector equation** (**c12**) — write the recursion for every node at
once and it is $\lambda c = A c$. Figure `eigen-equation.png`: the matrix times the vector,
returning the same vector rescaled.

**47. [Q] Which eigenvector?** — `_class: mid`. "A 12×12 matrix has twelve. Most of them
have negative entries. What would a negative importance mean?"

**48. [A] Perron–Frobenius** (**c13**) — Perron 1907, Frobenius 1912: for a connected
network with non-negative A, the leading eigenvector is **unique and strictly positive**.
Figure `spectrum.png`: this map's twelve eigenvalues on a line, λ_max = 3.35 marked.

**49. Power iteration** (**c14**) — everyone starts at 1; add up your neighbours; rescale;
repeat. Figure `power-iteration.gif`.

**50. [M] Drag the iteration** — the slider. Step 0 is flat, **step 1 is exactly the degree
ranking**, the crown settles at step 1 and the podium at step 4. Widget
`power-slider` (see FIGURE_SPEC for the export caveat: the slider only exists in the
`--html` build, and `check_render.py` never exercises it).

**51. Why it converges** — expand the start vector in the eigenbasis and every other mode
decays as |λ_i/λ_1|^t. Here the slowest is **0.795**. Figure `decay.png`.
*Note the trap, recorded in FIGURE_SPEC: the slowest mode is the most negative eigenvalue,
not the second largest.*

**52. M01, revisited** — $A^t$ counts walks of length t, so this is "where do many walks end
up?". Figure `walks-arrive.png`.

**53. On the map → the fourth crown** — figure `roma-eigenvector.png`. Rome again — **but
Alexandria is within 8% with one road fewer.** The recursion is doing something that
counting cannot.

**54. [Q] Where does this break?** — `_class: mid`. "Give me a network where this ranking
would be useless."

**55. [A] It localises** (**c15**) — on a dense clump with a thin tail, the score piles onto
the clump: the far tail node scores **0.0045** of the top. Figure `localization.png`.

*(Part 5 is slides 42–55, fourteen slides.)*

## Part 6 — Everyone gets a floor · 9 slides (56–64)

**56. Divider** — "Part Six · 06 / 08 · Everyone gets a floor".

**57. Katz centrality** (**c16**) — give every node a baseline β so nobody is stuck at zero:
$c = \beta\mathbf{1} + \lambda A c$. Figure `katz-floor.png`: the localization graph again,
tail lifted from 0.0045 to **0.184**.

**58. Solve it once** — $c = \beta(I - \lambda A)^{-1}\mathbf{1}$. Figure
`katz-solve.png`: the same equation rearranged, annotated.

**59. [Q] What is that inverse counting?** — `_class: mid`.

**60. [A] Walks, discounted by length** (**c17**) — expanding the inverse gives
$\beta\sum_t \lambda^t A^t \mathbf{1}$: every walk of every length, weighted λ^t, so short
walks dominate. Figure `katz-series.png` — a build, one term per step.

**61. λ is a dial** — small λ and Katz is essentially degree; large λ and it approaches
eigenvector centrality. Figure `katz-dial.png`: the ranking under three values of λ.

**62. [Q] How far can you turn it?** — `_class: mid`. "Predict first: what happens if I keep
raising λ?"

**63. [A] λ < 1/λ_max, or it blows up** (**c18**) — here 1/λ_max = **0.2989**; at λ = 0.3437
**eleven of the twelve scores go negative** and the walk series diverges. Figure
`katz-diverge.png`.

**64. On the map → the fifth crown** — figure `roma-katz.png`. Rome, with Alexandria at
0.888.

## Part 7 — The Web has direction · 17 slides (65–81)

**65. Divider** — "Part Seven · 07 / 08 · The Web has direction". Sub: "A road runs both
ways. A link does not — and a link is not a road, it is a recommendation."

**66. Eight pages** — the working web, and the notation: **$A_{ij}=1$ means i links to j**.
Figure `web-graph.png`. One page links to four others and is linked to by nobody; one page
has no links out at all.

**67. [Q] Which page is important?** — `_class: mid`. "A page that links to everything, or a
page everything links to?"

**68. [A] Both — and they are different quantities** (**c19**) — **hubs** point to good
authorities; **authorities** are pointed to by good hubs. Figure `hub-authority.png`.

**69. Two coupled equations** (**c20**) — $x = Ay$, $y = A^\top x$, so hubs are the leading
eigenvector of $AA^\top$ and authorities that of $A^\top A$. Figure `hits-equations.png`.
*Spec note: `curriculum.yml` m06.c20 records that the lecture note has these swapped. The
deck follows the standard convention; the note is the thing that is wrong.*

**70. [M] Your turn: pick them by eye** — "Which page is the best hub? The best authority?"
Figure `web-blank.png`. **No answer on this slide.**

**71. [A] Two crowns, two pages** — hub **Links** (1.00), authority **Blog** (1.00). Figure
`web-hits.png`, both crowns drawn, each labelled with what it means.

**72. [Q] What if you run HITS on a road map?** — `_class: mid`. "Our Roman network is
undirected. What do hubs and authorities become?"

**73. [A] It collapses to eigenvector centrality** (**c29**) — A symmetric means
$A^\top A\,c = \lambda^2 c$: the same vector, the eigenvalue squared. Figure
`hits-collapses.png` — the Roman map scored both ways, identical.

**74. The same equation, six times** — 1895 **Landau** (chess), 1949 **Seeley** (children's
popularity), 1953 **Katz**, 1965 **Hubbell**, 1972 **Bonacich**, 1998 **Brin & Page**.
Figure `genealogy.png` — a timeline **figure**, never a table (L2).
*Placed here deliberately: the room has now been taught four of the six.*

**75. [Q] 1998, Stanford** — `_class: mid`. "You are ranking the whole Web by counting
links. What is the first thing someone does to you?"

**76. [A] PageRank divides the vote** (**c21**) —
$c_i = (1-\beta)\sum_j A_{ji}c_j/d_j^{\text{out}} + \beta/N$: a page splits its score among
its out-links, so a link from a page that links to everything is worth little. Figure
`pagerank-split.png`.

**77. On the web → a different crown** — figure `web-pagerank.png`. **Blog** wins, and
**Links — the page HITS crowned as the best hub — is 8th of 8.** The disagreement the whole
module has been walking toward.

**78. [Q] The walker reaches a page with no links out** — `_class: mid`, figure
`web-dangling.png` (the dead end marked, nothing else).

**79. [A] Teleportation** (**c22**) — with probability β the walker jumps somewhere random
instead of following a link; PageRank is where the walker spends its time in the long run.
Without it, **the entire score drains away** (asserted: total → 0). Figure `teleport.png`.

**80. [Q] How would you build "more like this"?** — `_class: mid`. "A student is reading the
course page. What should the sidebar show?"

**81. [A] Personalized PageRank** (**c23**, **c30**) — bias the teleport onto one page and
the ranking bends toward it: globally Blog leads Course by 0.009; personalizing on Course
turns that into Course leading by **0.125**. It is exactly discounted reachability,
$c_i=\sum_k \beta(1-\beta)^k p_i^{(k)}$. Figure `ppr.png`.

## Part 8 — Which one should you use? · 12 slides (82–93)

**82. Divider** — "Part Eight · 08 / 08 · Which one should you use?".

**83. Back to the map** — six metrics, one map, and Rome wore almost every crown. Figure
`crown-summary.png`: the six results side by side as a build, one metric per step.

**84. [Q] So which one do you use?** — `_class: mid`. "You will have to pick one on Thursday.
On what grounds?"

**85. [A] Match the metric to the purpose** (**c24**) — popular → degree; efficient →
closeness or harmonic; critical → betweenness or eccentricity; influential → eigenvector,
Katz, PageRank; personalized → personalized PageRank. Figure `purpose.png` — an annotated
figure revealed one line at a time (**not** a table).

**86. [Q] How much of that was the map we drew?** — `_class: mid`. "We chose eighteen routes
out of the documented ones. Suppose we had chosen differently."

**87. [A] Some answers survive redrawing; some do not** — across **4992** drawable variants
of the documented pool, Rome keeps the degree crown **100%** of the time and the
eigenvector crown **79%**. Figure `robustness.png`.

**88. One redraw, one moved crown** — trade the Thessaly road for the Balkan road and the
Africa–Gaul sea lane: **betweenness moves to Mediolanum, nothing else moves.** Figure
`redraw.png` — the two maps as a build.

**89. [Q] A million nodes. Which of these can you run?** — `_class: mid`.

**90. [A] Cost is part of the choice** (**c25**) — degree is one pass over the edges;
closeness and betweenness need a shortest-path sweep from every node; the walk-based ones
need one matrix–vector product per step. At n = 10⁶, m = 10⁷ that is a factor of about
**33,000**. Figure `cost.png` — cost against n as curves, **not** a table.

**91. [Q] In a star, do the metrics agree? In a path?** — `_class: mid`. Predict before the
answer.

**92. [A] Total agreement, then total disagreement** (**c26**) — in a star **every** metric
crowns the hub; in a path degree crowns **five** nodes at once while betweenness crowns
exactly **one**. Figure `star-vs-path.png` — a two-panel build.
*Closing line: the Roman network was closer to a star than to a path, because one authority
built it around one node. The networks you will study were not built by anyone.*

**93. Three places this pays rent** (**c27**) — vaccination targets (M04's friendship
paradox, recovered), infrastructure defence (M03, recovered), systemic risk in financial
networks. Figure `applications.png` — a three-step build.

**94. Module review, and what is next** — the four acts in one figure, then: **PageRank was
a random walk all along**, and next time the walker is the subject rather than the tool.
Figure `next-module.png`.

*(Final count: 94 slides. Trim targets if the review asks for a shorter deck, in order:
slide 16, slide 52, slide 61 — each is a supporting slide whose point survives in its
neighbour.)*

---

# MILESTONE MAP (S5 — one per part)

| part | milestone |
|---|---|
| 1 | slide 10 — draw the club network from the roster (and it is tonight's handout) |
| 2 | slide 17 — "is counting roads enough?", answered by the room before slide 18 |
| 3 | slide 22 — compute Massilia's closeness by hand |
| 4 | slide 35 — count σ by hand; slide 41 — the handout goes out |
| 5 | slide 50 — the power-iteration slider |
| 6 | slide 62 — predict what happens as λ rises, *then* watch it break |
| 7 | slide 70 — pick the hub and the authority by eye |
| 8 | slide 84 / 91 — "which one will you use?" and the star/path prediction |

# CONCEPT COVERAGE (30 / 30)

c01 s12 · c02 s14 · c03 s20 · c04 s21 · c05 s27 · c06 s28 · c07 s30 · c08 s33 · c09 s34 ·
c10 s39 · c11 s44 · c12 s46 · c13 s48 · c14 s49 · c15 s55 · c16 s57 · c17 s60 · c18 s63 ·
c19 s68 · c20 s69 · c21 s76 · c22 s79 · c23 s81 · c24 s85 · c25 s90 · c26 s92 · c27 s93 ·
c28 s25 · c29 s73 · c30 s81

Nothing is left off the slides.

---

# KNOWN DEVIATIONS FROM plan.md, AND WHAT WAS SHIPPED INSTEAD

Listed so the next round does not spend time rediscovering them.

- **The power-iteration slider (plan.md milestone P5) was not built.** The deck
  ships `power-iteration.gif` plus the "step one is degree" slide. A slider only
  exists in the `--html` export, which `check_render.py` never exercises, so it
  cannot be shipped without driving the real control in a browser and confirming
  it runs — and `DECK_BUILD_GUIDE.md` is explicit that checking the `<script>`
  survived the export is not the same as checking that it runs. Part 5 still meets
  S5 through the animation and the "describe a network where this breaks"
  discussion. **If this is picked up, the data is already in
  `verify_numbers.POWER_TRACE` and the GIF is generated from it, so the two cannot
  drift.**
- **No marimo demo**, per `plan.md`.
- **No day-2 recap slide**, per `plan.md` — Part 5 restarts from its divider.
- **The eccentricity crown is shared three ways** rather than being Rome's alone.
  That is the data, and the deck uses it as the first crack rather than hiding it.
- **`hits-collapses.png` was cut.** It rendered byte-identical to
  `roma-eigenvector.png` — which is the theorem, not a bug — so the Part 7 slide
  reuses the Part 5 figure and its caption says why. The identity is still
  asserted in `figs_rome.check_hits_collapses`.

---
marp: true
theme: house
paginate: true
math: katex
---

<!-- _class: lead -->

<div class="eyebrow">Advanced Topics in Network Science · Module 06</div>

# All Roads Lead to Rome

<div class="sub">… do they?</div>

<div class="credit">Sadamori Kojaku · Binghamton University · October 20 and 22, 2026</div>

<script src="scrub.js"></script>
<script>window.animStepOnly = true;</script>

<!--
Day 1 (10/20): slides 1 to 61, measured by shortest paths. Day 2 (10/22): slides 62 to 131, measured by walks. About a third are build steps, a few seconds each.
The pen-and-paper sheet has already been done, so the room has met degree, average distance, "indispensable" and passing scores around. Name things; do not re-derive what is in their hands.
A build is a run of slides with the same title: explain the text on the first, then step; the grey note on each figure says what changed.
Layouts (HOUSE_STYLE section 8): the title is the message; a line under it (.sub) is the formula or the question's rule; the line at the bottom (.take) is the answer or the result. The figure stays at one position through a question and its answer, and through a build.
-->

---

<!-- _class: L-e -->

## The Golden Milestone

<div class="cols">
<div class="big">

20 BC: Augustus, Caesar's heir, set it up in Rome.

Every road of Italy ended at it.

Distances were counted in miles from Rome.

</div>
<div class="fig">

<div class="photos">

![](figures/photos/caesar.jpg)
![](figures/photos/augustus.jpg)
![](figures/photos/milliarium.jpg)

</div>

<div class="photo-credit">Julius Caesar (Marie-Lan Taÿ Pamart, CC BY 4.0) · Augustus of Prima Porta (Justin Benttinen, CC BY-SA 4.0) · remains labelled Milliarium Aureum (Krzysztof Golik, CC BY-SA 4.0) · Wikimedia Commons</div>

</div>
</div>

<!--
Caesar named Octavian his heir in his will, 44 BC. As Augustus, he took charge of the roads around Rome and set up a gilded column in the Forum in 20 BC (Cassius Dio 54.8.4). Plutarch (Galba 24): all the roads of Italy end at it.
What was written on it is not recorded by any ancient source; do not claim it listed the distances. Distances along the roads were counted from the gates of the city wall.
The fragments in the photo are the ones the Forum labels as the milestone; whether they belong to it is doubtful.
"All roads lead to Rome" is medieval: Alain de Lille, about 1175.
-->

---

<!-- _class: L-a -->

## Twelve cities of the empire

<div class="sub">

Roads and sea lanes joined them.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/roma-basemap.png)

</div>
</div>

<div class="ref">map © OpenStreetMap contributors</div>

<!--
The pins are the real places: Londinium, Colonia, Lugdunum, Massilia, Tarraco, Mediolanum, Roma, Carthago, Thessalonica, Athenae, Byzantium, Alexandria.
-->

---

<!-- _class: L-a -->

## Which city is the most <span class="hot">important</span>?

<div class="sub">

Node: a city. Edge: a road or a sea lane.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/roma-to-graph.png)

</div>
</div>

<div class="cue">

*Take answers.*

</div>

<!--
The same twelve cities at the same places: the map is gone, the roads are straight links.
Take answers. The room will give at least two kinds of reason (many roads; close to everything). Both are right. That is the module.
-->

---

<!-- _class: L-a -->

## <span class="hot">Degree</span>: the roads at a city

<div class="sub">

$d_i = \sum_j A_{ij}$, where $A_{ij} = 1$ if a road joins $i$ and $j$.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/roma-degree.png)

</div>
</div>

<div class="take">

Degree sees only the <span class="hot">neighbours</span>.

</div>

<!--
The sheet's first question. Name it and move on. Roma has the most roads, 5. The same network as before; the shade is the degree.
-->

---

<!-- header: New York State highways -->
<!-- _class: L-b -->

## Which city do most trips pass through?

<div class="cols">
<div class="fig">

![w:537](figures/ny-overview.png)

</div>
</div>

<div class="ref">© OpenStreetMap contributors</div>

<div class="cue">

*Hold your answer until the end of today.*

</div>

<!--
Do not answer. It comes back at the end of today (betweenness). "Trips": the shortest route between every pair of interchanges.
The network: OpenStreetMap motorways and trunk roads in New York State, one node per interchange (junctions within 3.5 km merged), 289 nodes and 433 road segments. Distance is km of road.
Take a vote: Buffalo, Rochester, Syracuse, Utica, Albany, NYC, Binghamton, Watertown.
-->

---

<!-- _class: L-b -->

## Degree cannot tell interchanges apart

<div class="cols">
<div class="fig">

![w:537](figures/ny-degree.png)

</div>
</div>

<div class="take">

Degree 3: 201 interchanges. Degree 4: 57.

</div>

<!--
On a road map almost every junction joins three or four roads. A measure that only looks one step out sees almost nothing.
-->

---

<!-- header: Paths and walks -->
<!-- _class: left -->

## How far is u from v?

<div class="cols">
<div>

- The network from Module 01.

</div>
<div class="fig tall">

![w:537](figures/w5-blank.png)

</div>
</div>

<div class="cue">

*Take answers.*

</div>

<!--
Ask: in how many ways can you get there in 3 steps? In 4?
-->

---

<!-- _class: left -->

## Two ways to count

<div class="cols">
<div>

* **Shortest path**: the fewest steps. One number: 2.
* **Walk**: any route, revisits allowed. A count per length.

</div>
<div class="fig tall">

![w:537](figures/frames/w5-walks/00.png)

</div>
</div>

<!--
Explain the bullets on this slide; the next 4 slides step the figure, one change each (the grey note says which).
Two terms defined beside one figure, so this run keeps text beside the figure (HOUSE_STYLE section 8, C).
The walk counts are the entries of A, A squared, A cubed, ... from Module 01. Walks of length 2: 2; length 3: 1; length 4: 11.
-->


---

<!-- _class: left -->

## Two ways to count

<div class="cols">
<div>

- **Shortest path**: the fewest steps. One number: 2.
- **Walk**: any route, revisits allowed. A count per length.

</div>
<div class="fig tall">

![w:537](figures/frames/w5-walks/01.png)

</div>
</div>

<!--
Step 1 of 4: shortest path: 2 steps.
-->

---

<!-- _class: left -->

## Two ways to count

<div class="cols">
<div>

- **Shortest path**: the fewest steps. One number: 2.
- **Walk**: any route, revisits allowed. A count per length.

</div>
<div class="fig tall">

![w:537](figures/frames/w5-walks/02.png)

</div>
</div>

<!--
Step 2 of 4: length 2: 2 walks.
-->

---

<!-- _class: left -->

## Two ways to count

<div class="cols">
<div>

- **Shortest path**: the fewest steps. One number: 2.
- **Walk**: any route, revisits allowed. A count per length.

</div>
<div class="fig tall">

![w:537](figures/frames/w5-walks/03.png)

</div>
</div>

<!--
Step 3 of 4: length 3: 1 walk.
-->

---

<!-- _class: left -->

## Two ways to count

<div class="cols">
<div>

- **Shortest path**: the fewest steps. One number: 2.
- **Walk**: any route, revisits allowed. A count per length.

</div>
<div class="fig tall">

![w:537](figures/frames/w5-walks/04.png)

</div>
</div>

<!--
Step 4 of 4: length 4: 11 walks; this one revisits a node.
-->

---

<!-- header: "" -->
<!-- _class: L-b -->

## Two <span class="hot">choices</span> make a centrality

<div class="fig tall">

![w:1080](figures/grid-empty.png)

</div>

<!--
Which routes count, and how do they become one number? Every measure today is one choice on each axis. We fill this in as we go.
Degree sits in both rows: a shortest path of length 1 and a walk of length 1 are the same thing, one edge.
-->

---

<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 05</span></div>

## Who is close to everyone?

closeness · harmonic centrality · eccentricity

<!--
Near every other node: on average (closeness, harmonic) or at worst (eccentricity).
-->

---

<!-- header: Closeness -->
<!-- _class: L-a -->

## <span class="hot">Closeness</span>: invert the sum of distances

<div class="sub">

$c_i = (N-1) \,\big/ \sum_{j \ne i} \ell_{ij}$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/closeness-def/00.png)

</div>
</div>

<!--
Explain the formula on this slide; the next 5 slides step the figure, one change each (the grey note says which).
ell_ij is the distance from i to j. N - 1 makes the best case, a star's centre, exactly 1.
The steps: each node's sum of distances (A 15, C and E 11, D 10); then each sum turns into closeness, (N - 1)/sum with N = 7: A, B, F, G 6/15 = 0.40; C, E 6/11 = 0.55; D 6/10 = 0.60, the highest.
The sum is not the score: closeness is its inverse, so higher is better.
-->


---

<!-- _class: L-a -->

## <span class="hot">Closeness</span>: invert the sum of distances

<div class="sub">

$c_i = (N-1) \,\big/ \sum_{j \ne i} \ell_{ij}$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/closeness-def/01.png)

</div>
</div>

<!--
Step 1 of 5: distances from A.
-->

---

<!-- _class: L-a -->

## <span class="hot">Closeness</span>: invert the sum of distances

<div class="sub">

$c_i = (N-1) \,\big/ \sum_{j \ne i} \ell_{ij}$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/closeness-def/02.png)

</div>
</div>

<!--
Step 2 of 5: 1+1+2+3+4+4 = 15.
-->

---

<!-- _class: L-a -->

## <span class="hot">Closeness</span>: invert the sum of distances

<div class="sub">

$c_i = (N-1) \,\big/ \sum_{j \ne i} \ell_{ij}$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/closeness-def/03.png)

</div>
</div>

<!--
Step 3 of 5: every node's sum.
-->

---

<!-- _class: L-a -->

## <span class="hot">Closeness</span>: invert the sum of distances

<div class="sub">

$c_i = (N-1) \,\big/ \sum_{j \ne i} \ell_{ij}$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/closeness-def/04.png)

</div>
</div>

<!--
Step 4 of 5: 6/15 = 0.40.
-->

---

<!-- _class: L-a -->

## <span class="hot">Closeness</span>: invert the sum of distances

<div class="sub">

$c_i = (N-1) \,\big/ \sum_{j \ne i} \ell_{ij}$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/closeness-def/05.png)

</div>
</div>

<!--
Step 5 of 5: highest: D, 0.60.
-->

---

<!-- _class: L-a -->

## Which node is closest to everything?

<div class="sub">

Highest closeness wins: the smallest sum of distances.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-close-CB.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

<!-- _class: L-a -->

## Which node is closest to everything?

<div class="sub">

Highest closeness wins: the smallest sum of distances.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-close-CB-ans.png)

</div>
</div>

<div class="take">

<span class="hot">P</span> wins: its long arms hold more nodes.

</div>

<!--
P: sum 16, closeness 9/16 = 0.56. N: sum 18, closeness 9/18 = 0.50 (N = 10 nodes). N's triangle looks central, but P's long arms hold more nodes.
-->

---

<!-- _class: L-a -->

## Which node is closest to everything?

<div class="sub">

Highest closeness wins: the smallest sum of distances.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-close-CA.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

<!-- _class: L-a -->

## Which node is closest to everything?

<div class="sub">

Highest closeness wins: the smallest sum of distances.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-close-CA-ans.png)

</div>
</div>

<div class="take">

<span class="hot">F</span> wins, 0.53. The hub E has 0.50.

</div>

<!--
F has degree 2 and a sum of 19: closeness 10/19 = 0.53. The hub E (degree 5) and G both have 20: 0.50 (N = 11 nodes). Moving from E to F, five nodes get one step farther (A, B, C, D, E) and six get one step closer.
-->

---

<!-- _class: L-a -->

## What if one road closes?

<div class="sub">

Close the road between E and F.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/cut-blank.png)

</div>
</div>

<div class="cue">

*Take 30 seconds.*

</div>

---

<!-- _class: L-a -->

## What if one road closes?

<div class="sub">

Close the road between E and F.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/cut-closeness.png)

</div>
</div>

<div class="take">

Some distances are $\infty$: every closeness is <span class="hot">0</span> 🤔

</div>

<!--
Not just the nodes near the cut: all eleven. Every sum is infinite. Closeness cannot rank a disconnected network at all.
-->

---

<!-- header: Harmonic centrality -->
<!-- _class: L-a -->

## <span class="hot">Harmonic</span> centrality adds 1/distance

<div class="sub">

$h_i = \sum_{j \ne i} 1/\ell_{ij}$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/harmonic-def/00.png)

</div>
</div>

<div class="take">

$1/\infty = 0$: an unreachable node adds nothing.

</div>

<!--
Explain the formula and the bottom line on this slide; the next 5 slides step the figure, one change each (the grey note says which).
Take the reciprocal of each distance first, then add.
The steps, from G: four nodes at distance 1, K at 2, the other piece unreachable: 4 + 1/2 = 9/2. Then every node's score.
-->


---

<!-- _class: L-a -->

## <span class="hot">Harmonic</span> centrality adds 1/distance

<div class="sub">

$h_i = \sum_{j \ne i} 1/\ell_{ij}$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/harmonic-def/01.png)

</div>
</div>

<div class="take">

$1/\infty = 0$: an unreachable node adds nothing.

</div>

<!--
Step 1 of 5: G's neighbours: 1/1 each.
-->

---

<!-- _class: L-a -->

## <span class="hot">Harmonic</span> centrality adds 1/distance

<div class="sub">

$h_i = \sum_{j \ne i} 1/\ell_{ij}$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/harmonic-def/02.png)

</div>
</div>

<div class="take">

$1/\infty = 0$: an unreachable node adds nothing.

</div>

<!--
Step 2 of 5: K is 2 steps from G, so it adds 1/2.
-->

---

<!-- _class: L-a -->

## <span class="hot">Harmonic</span> centrality adds 1/distance

<div class="sub">

$h_i = \sum_{j \ne i} 1/\ell_{ij}$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/harmonic-def/03.png)

</div>
</div>

<div class="take">

$1/\infty = 0$: an unreachable node adds nothing.

</div>

<!--
Step 3 of 5: unreachable: 1/inf = 0.
-->

---

<!-- _class: L-a -->

## <span class="hot">Harmonic</span> centrality adds 1/distance

<div class="sub">

$h_i = \sum_{j \ne i} 1/\ell_{ij}$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/harmonic-def/04.png)

</div>
</div>

<div class="take">

$1/\infty = 0$: an unreachable node adds nothing.

</div>

<!--
Step 4 of 5: 4 + 1/2 = 9/2.
-->

---

<!-- _class: L-a -->

## <span class="hot">Harmonic</span> centrality adds 1/distance

<div class="sub">

$h_i = \sum_{j \ne i} 1/\ell_{ij}$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/harmonic-def/05.png)

</div>
</div>

<div class="take">

$1/\infty = 0$: an unreachable node adds nothing.

</div>

<!--
Step 5 of 5: highest: G.
-->

---

<!-- _class: L-a -->

## Who has the highest harmonic centrality?

<div class="sub">

The road E–F is open again. Closeness picked F.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-close-CA.png)

</div>
</div>

<div class="cue">

*Does the winner change?*

</div>

---

<!-- _class: L-a -->

## Who has the highest harmonic centrality?

<div class="sub">

The road E–F is open again. Closeness picked F.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-harm-CA-ans.png)

</div>
</div>

<div class="take">

Harmonic picks the hub <span class="hot">E</span>.

</div>

<!--
E 27/4 beats G 19/3 and F 35/6. With 1/distance, the four leaves at distance 1 count fully for E; with the sum of distances, they barely helped.
-->

---

<!-- _class: L-a -->

## Who has the highest harmonic centrality?

<div class="sub">

A network in two pieces.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-harm-HD.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

<!-- _class: L-a -->

## Who has the highest harmonic centrality?

<div class="sub">

A network in two pieces.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-harm-HD-ans.png)

</div>
</div>

<div class="take">

The star's <span class="hot">centre</span>, 4, beats 11/3.

</div>

<!--
The star's centre scores 4; the middle of the path, 11/3. The bigger piece is not the better one.
-->

---

<!-- header: New York State highways -->
<!-- _class: L-b -->

## Closeness picks a spot near NYC

<div class="cols">
<div class="fig">

![w:537](figures/ny-closeness.png)

</div>
</div>

<div class="take">

31% of interchanges: within 60 km of <span class="hot">NYC</span>.

</div>

<!--
Distance is km of highway. The winner is on NY 17 at Middletown.
Closeness is pulled toward where the nodes are. 91 of 289 interchanges are within 60 km of Manhattan, so the best average sits just north of the city, not in the middle of the state. (Harmonic picks I-95 in the Bronx.)
-->

---

<!-- header: Eccentricity -->
<!-- _class: L-a -->

## A fire station at the best average?

<div class="sub">

Closeness picks D: 0.60, the highest.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/bowtie-closeness.png)

</div>
</div>

<div class="cue">

*Take 30 seconds.*

</div>

<!--
Ask: would you put the town's one fire station at D? What does a fire station care about?
-->

---

<!-- _class: L-a -->

## <span class="hot">Eccentricity</span>: the farthest distance

<div class="sub">

$e_i = \max_j \ell_{ij}$. The smallest wins; its centrality is $1/e_i$.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/ecc-def/00.png)

</div>
</div>

<!--
Explain the formula on this slide; the next 3 slides step the figure, one change each (the grey note says which).
A fire station must reach its farthest house.
The steps: the closeness values give way to each node's farthest distance. D is still best here, 2. The next question is built so that it is not.
-->


---

<!-- _class: L-a -->

## <span class="hot">Eccentricity</span>: the farthest distance

<div class="sub">

$e_i = \max_j \ell_{ij}$. The smallest wins; its centrality is $1/e_i$.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/ecc-def/01.png)

</div>
</div>

<!--
Step 1 of 3: A's farthest: 4 steps.
-->

---

<!-- _class: L-a -->

## <span class="hot">Eccentricity</span>: the farthest distance

<div class="sub">

$e_i = \max_j \ell_{ij}$. The smallest wins; its centrality is $1/e_i$.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/ecc-def/02.png)

</div>
</div>

<!--
Step 2 of 3: every node's worst case.
-->

---

<!-- _class: L-a -->

## <span class="hot">Eccentricity</span>: the farthest distance

<div class="sub">

$e_i = \max_j \ell_{ij}$. The smallest wins; its centrality is $1/e_i$.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/ecc-def/03.png)

</div>
</div>

<!--
Step 3 of 3: smallest: D, 2.
-->

---

<!-- _class: L-a -->

## Smallest eccentricity: which node?

<div class="sub">

The best fire station: the smallest worst case.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-ecc-EA.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

<!-- _class: L-a -->

## Smallest eccentricity: which node?

<div class="sub">

The best fire station: the smallest worst case.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-ecc-EA-ans.png)

</div>
</div>

<div class="take">

<span class="hot">F</span>: worst case 2. E, best on average, has 3.

</div>

<!--
E wins closeness (sum 10, the smallest) but its worst case is 3, the end of the tail. F has worst case 2.
-->

---

<!-- _class: L-a -->

## Smallest eccentricity: which node?

<div class="sub">

The best fire station: the smallest worst case.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-ecc-EB.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

<!-- _class: L-a -->

## Smallest eccentricity: which node?

<div class="sub">

The best fire station: the smallest worst case.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-ecc-EB-ans.png)

</div>
</div>

<div class="take">

<span class="hot">L</span>: worst case 2. K, best on average, has 3.

</div>

<!--
K wins closeness (11), worst case 3. L, with degree 2, has worst case 2.
-->

---

<!-- header: New York State highways -->
<!-- _class: L-b -->

## Smallest worst case: near Binghamton

<div class="cols">
<div class="fig">

![w:537](figures/ny-eccentricity.png)

</div>
</div>

<div class="take">

Its farthest interchange is <span class="hot">473 km</span> away.

</div>

<!--
The worst-case drive from each interchange. The smallest is on NY 17 east of Binghamton.
If New York State had one fire station for its highways, it would go near us. From there the farthest interchange is where I-90 leaves the state west of Buffalo, 473 km; next is I-87 at the Canadian border.
-->

---

<!-- header: "" -->
<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 05</span></div>

## Which node can the traffic not avoid?

betweenness centrality

---

<!-- header: Betweenness -->
<!-- _class: L-a -->

## Count the letters each node carries

<div class="sub">

One letter per pair, along a shortest path.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/btw-def/00.png)

</div>
</div>

<!--
Explain the line on this slide; the next 4 slides step the figure, one change each (the grey note says which).
D carries 9: every letter between the left triangle and the right triangle. C and E carry 8 each.
-->


---

<!-- _class: L-a -->

## Count the letters each node carries

<div class="sub">

One letter per pair, along a shortest path.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/btw-def/01.png)

</div>
</div>

<!--
Step 1 of 4: A to F passes C, D, E.
-->

---

<!-- _class: L-a -->

## Count the letters each node carries

<div class="sub">

One letter per pair, along a shortest path.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/btw-def/02.png)

</div>
</div>

<!--
Step 2 of 4: all of A's letters.
-->

---

<!-- _class: L-a -->

## Count the letters each node carries

<div class="sub">

One letter per pair, along a shortest path.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/btw-def/03.png)

</div>
</div>

<!--
Step 3 of 4: every pair.
-->

---

<!-- _class: L-a -->

## Count the letters each node carries

<div class="sub">

One letter per pair, along a shortest path.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/btw-def/04.png)

</div>
</div>

<!--
Step 4 of 4: D carries the most, 9.
-->

---

<!-- _class: left -->

## <span class="hot">Betweenness</span>: a tie splits the pair

<div class="cols">
<div>

* $b_i = \displaystyle\sum_{s<t} \frac{\sigma_{st}(i)}{\sigma_{st}}$
* $\sigma_{st}$: the number of shortest $s$–$t$ paths.
* $\sigma_{st}(i)$: those that pass through $i$.

</div>
<div class="fig">

![w:537](figures/sigma-answer.png)

</div>
</div>

<!--
Two symbols defined beside one figure, so this slide keeps text beside the figure (HOUSE_STYLE section 8, C).
From s to t there are two shortest paths, s-A-D-t and s-B-C-t, and they share no node. C is on one of the two: sigma_st(C) = 1, sigma_st = 2, so C carries 1/2 of this pair. So do A, B and D. The pair counts once in total, shared out among its routes.
-->

---

<!-- _class: L-a -->

## Which node carries the most?

<div class="sub">

Count the shortest paths through each node.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-btw-DB.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

<!-- _class: L-a -->

## Which node carries the most?

<div class="sub">

Count the shortest paths through each node.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-btw-DB-ans.png)

</div>
</div>

<div class="take">

Each <span class="hot">hub</span> carries 30. The bridge F carries 25.

</div>

<!--
F carries 5 x 5 = 25 pairs. E carries the 6 pairs among its leaves plus 4 x 6 pairs between a leaf and the rest: 30. Same for G.
-->

---

<!-- _class: L-a -->

## Which node carries the most?

<div class="sub">

Count the shortest paths through each node.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-btw-SQ.png)

</div>
</div>

<div class="cue">

*A tie splits the count.*

</div>

---

<!-- _class: L-a -->

## Which node carries the most?

<div class="sub">

Count the shortest paths through each node.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-btw-SQ-ans.png)

</div>
</div>

<div class="take">

<span class="hot">O</span> wins by half a pair: 19/2 against 9.

</div>

<!--
O carries 9 pairs whole, and half of the pair P, Q (two shortest paths: through O and through R): 19/2. M carries 9.
-->

---

<!-- header: New York State highways -->
<!-- _class: L-b -->

## Which city do most trips pass through?

<div class="cols">
<div class="fig">

![w:537](figures/ny-betweenness.png)

</div>
</div>

<div class="take">

<span class="hot">Binghamton</span>: 3.5 times Syracuse.

</div>

<!--
The answer to this morning's question: of the eight cities, Binghamton is first, 3.5 times Syracuse.
The top interchange in the whole state is NY 17 at Monticello. Four of the top five interchanges are on NY 17 between Binghamton and Middletown: the corridor between the NYC cluster and upstate. Binghamton is where that corridor meets I-81 and I-88. Monticello beats the NY 17 / NY 8 / NY 10 interchange near Binghamton by only 0.2% (0.3632 against 0.3626).
-->

---

<!-- header: "" -->
<!-- _class: L-b -->

## The shortest-path row

<div class="fig tall">

![w:1080](figures/grid-row1.png)

</div>

<!--
Degree, and four more ways to turn shortest paths into one number.
End of day 1.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 05</span></div>

## Do your neighbours make you important?

eigenvector centrality

<!--
Day 2 starts here.
-->

---

<!-- _class: L-q -->

<div class="cols">
<div>
<blockquote>

A man is known by <span class="hot">the company he keeps</span>.

</blockquote>
<p class="who">Aesop, in Townsend's translation</p>
</div>
<div class="fig">

![](figures/photos/aesop.jpg)
<figcaption>Velázquez, Aesop, c. 1638–41, Prado</figcaption>

</div>
</div>

<!--
The English moral is a 19th-century translation (Townsend); the fable (Perry 237) is attributed to Aesop by tradition.
A man buys a donkey on trial. It walks straight to the laziest donkey in the yard, and he returns it.
-->

---

<!-- header: Eigenvector centrality -->
<!-- _class: L-a -->

## Importance you <span class="hot">inherit</span>

<div class="sub">

$c_i = \tfrac{1}{\lambda} \sum_j A_{ij}\, c_j$: the neighbours' scores, added up.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/eigen-inherit/00.png)

</div>
</div>

<!--
Explain the formula on this slide; the next 3 slides step the figure, one change each (the grey note says which).
A node's score is proportional to the sum of its neighbours' scores.
The steps: A's neighbours hand over their scores, and the sum is 2.88 times A's own. Then the leaf C: its one neighbour D holds 0.58 = 2.88 x 0.20, the same 2.88. Every node gives the same factor; that number is lambda.
It is circular: a score defined by scores. The constant lambda keeps the scores from growing without bound.
-->


---

<!-- _class: L-a -->

## Importance you <span class="hot">inherit</span>

<div class="sub">

$c_i = \tfrac{1}{\lambda} \sum_j A_{ij}\, c_j$: the neighbours' scores, added up.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/eigen-inherit/01.png)

</div>
</div>

<!--
Step 1 of 3: A's neighbours: B, D, F, G.
-->

---

<!-- _class: L-a -->

## Importance you <span class="hot">inherit</span>

<div class="sub">

$c_i = \tfrac{1}{\lambda} \sum_j A_{ij}\, c_j$: the neighbours' scores, added up.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/eigen-inherit/02.png)

</div>
</div>

<!--
Step 2 of 3: their sum = 2.88 x A's score.
-->

---

<!-- _class: L-a -->

## Importance you <span class="hot">inherit</span>

<div class="sub">

$c_i = \tfrac{1}{\lambda} \sum_j A_{ij}\, c_j$: the neighbours' scores, added up.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/eigen-inherit/03.png)

</div>
</div>

<!--
Step 3 of 3: same 2.88 at C (0.58 = 2.88 x 0.20): this is lambda.
-->

---

<!-- _class: L-a -->

## It is an <span class="hot">eigenvector</span> equation

<div class="sub">

In matrix form: $A\mathbf{c} = \lambda\mathbf{c}$.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/eigen-equation.png)

</div>
</div>

<!--
c is an eigenvector of A, and lambda its eigenvalue.
-->

---

<!-- _class: L-a -->

## Which eigenvector is the centrality?

<div class="sub">

Seven eigenvectors. Blue: positive. Orange: negative.

</div>

<div class="fig">

![w:1080](figures/eig-all-q.png)

</div>

<div class="cue">

*Take 30 seconds.*

</div>

---

<!-- _class: L-a -->

## Which eigenvector is the centrality?

<div class="sub">

Seven eigenvectors. Blue: positive. Orange: negative.

</div>

<div class="fig">

![w:1080](figures/eig-all.png)

</div>

<div class="take">

Only the one for $\lambda_{\max}$ is all <span class="hot">positive</span>.

</div>

<!--
The Perron–Frobenius theorem, for a nonnegative, irreducible matrix (irreducible = the network is connected): the eigenvector of the largest eigenvalue can be chosen positive everywhere, and no other eigenvector is. A negative score would mean nothing, so this is the only eigenvector that can be a centrality.
-->

---

<!-- _class: L-a -->

## This is <span class="hot">eigenvector centrality</span>

<div class="sub">

The eigenvector of $\lambda_{\max}$, its largest entry set to 1.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/eig-pf.png)

</div>
</div>

<!--
The same seven nodes and the same numbers as on "Importance you inherit".
-->

---

<!-- _class: L-a -->

## Which lettered node scores higher?

<div class="sub">

Eigenvector centrality.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-eig-L.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

<!-- _class: L-a -->

## Which lettered node scores higher?

<div class="sub">

Eigenvector centrality.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-eig-L-ans.png)

</div>
</div>

<div class="take">

<span class="hot">M</span>: fewer neighbours, better ones.

</div>

<!--
M 0.85, X 0.46. M's three neighbours include two hubs; X's four include three leaves.
-->

---

<!-- _class: L-a -->

## Which lettered node scores higher?

<div class="sub">

Eigenvector centrality.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-eig-R.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

<!-- _class: L-a -->

## Which lettered node scores higher?

<div class="sub">

Eigenvector centrality.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-eig-R-ans.png)

</div>
</div>

<div class="take">

<span class="hot">K</span> beats the hub H: 0.85 against 0.62.

</div>

<!--
K 0.85, H 0.62. K sits in the dense corner.
-->

---

<!-- header: Eigendecomposition -->
<!-- _class: L-a -->

## $A$ is a sum of rank-1 pieces

<div class="sub">

One piece per eigenvalue.

</div>

<div class="fig">

![w:1080](figures/decomp-sum.png)
<figcaption>circle: eigenvalue · tall bar: eigenvector · wide bar: its transpose · colour: which eigenvector</figcaption>

</div>

<!--
rank 1: every row of u_k u_kᵀ is a multiple of u_kᵀ. lambda_1 = lambda_max is the largest eigenvalue.
-->

---

<!-- _class: L-a -->

## The eigenvectors are orthogonal

<div class="sub">

Two colours multiply to 0; one colour with itself, to 1.

</div>

<div class="fig">

![w:1080](figures/decomp-orth.png)

</div>

<!--
Each eigenvector scaled to length 1: two different ones multiply to 0, one with itself to 1.
-->

---

<!-- _class: L-a -->

## Square it

<div class="sub">

$A^2 = A\,A$: the sum times itself.

</div>

<div class="fig">

![w:1080](figures/frames/decomp-square/00.png)

</div>

<!--
Explain the line on this slide; the next 3 slides step the figure, one change each (the grey note says which).
Multiply the sum by itself. Every product of a term on the left and a term on the right contains u_kᵀ u_l in the middle: the wide bar of the left term against the tall bar of the right term. Colour says which eigenvector: u_1 blue, u_2 gold, u_7 grey. Two colours meeting give 0, so every cross term vanishes; one colour meeting itself gives 1. What is left is the sum of lambda_k squared u_k u_kᵀ.
-->


---

<!-- _class: L-a -->

## Square it

<div class="sub">

$A^2 = A\,A$: the sum times itself.

</div>

<div class="fig">

![w:1080](figures/frames/decomp-square/01.png)

</div>

<!--
Step 1 of 3: u1ᵀu2 = 0: different colours vanish.
-->

---

<!-- _class: L-a -->

## Square it

<div class="sub">

$A^2 = A\,A$: the sum times itself.

</div>

<div class="fig">

![w:1080](figures/frames/decomp-square/02.png)

</div>

<!--
Step 2 of 3: u1ᵀu1 = 1: same colour.
-->

---

<!-- _class: L-a -->

## Square it

<div class="sub">

$A^2 = A\,A$: the sum times itself.

</div>

<div class="fig">

![w:1080](figures/frames/decomp-square/03.png)

</div>

<!--
Step 3 of 3: each eigenvalue squared, same colours (the same vectors).
-->

---

<!-- _class: L-a -->

## Keep multiplying

<div class="sub">

$A^t / \lambda_1^t$: every term but the first fades.

</div>

<div class="fig">

![w:1080](figures/frames/decomp-power/00.png)

</div>

<!--
Explain the line on this slide; the next 3 slides step the figure, one change each (the grey note says which).
A^t counts walks of length t. Divide everything by lambda_1^t: term k shrinks like (lambda_k / lambda_1)^t. The next largest in size is lambda = -2.26, so the error shrinks by a factor 0.78 per step (2.26 / 2.88). After 16 steps it is about 2%. So A^t 1 points along u_1.
-->


---

<!-- _class: L-a -->

## Keep multiplying

<div class="sub">

$A^t / \lambda_1^t$: every term but the first fades.

</div>

<div class="fig">

![w:1080](figures/frames/decomp-power/01.png)

</div>

<!--
Step 1 of 3: t = 2: the negative term turns positive.
-->

---

<!-- _class: L-a -->

## Keep multiplying

<div class="sub">

$A^t / \lambda_1^t$: every term but the first fades.

</div>

<div class="fig">

![w:1080](figures/frames/decomp-power/02.png)

</div>

<!--
Step 2 of 3: t = 4: the small terms fade.
-->

---

<!-- _class: L-a -->

## Keep multiplying

<div class="sub">

$A^t / \lambda_1^t$: every term but the first fades.

</div>

<div class="fig">

![w:1080](figures/frames/decomp-power/03.png)

</div>

<!--
Step 3 of 3: t = 16: only the first is left (2%).
-->

---

<!-- header: Power iteration -->

## Multiply by $A$, again and again

<figure class="anim-stage" id="power-step">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>

  <div class="anim-grid-2" data-anim-canvas>
    <div data-anim-clear data-ps-draw></div>
    <div data-anim-clear data-ps-side></div>
  </div>

  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script>window.animStepOnly = true;</script>
<script src="../../lecture-note/assets/anim/power-step.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

<!--
Press the ▶ button once per step. Each press applies x <- A x once and divides by the largest entry. On the left the disc shade and the printed number are the entry. On the right every node has one line: x axis = the iteration t, y axis = that node's score. Each press adds one point to every line, and the letter at the right end names the line. The axis jumps from t = 8 to t = 30 (the two slanted strokes on the axis); the dotted piece joins them.

Step 0: every node holds 1, so all seven lines start at the same point. Step 1: every node now holds its degree (A 4, D 3, F 3, G 3, B 2, E 2, C 1), divided by 4, so A stays at 1.00 and C drops to 0.25. The lines fan out: degree is the first guess, and each further step looks one step farther. Step 2 (B orange, D blue): B's line rises and D's falls until they meet (both 0.64), and F's and G's lines pull above both (0.82). Step 3: G's line goes above F's; B's and D's lines are still exactly tied (0.625). Step 4: B's line crosses D's (0.63 against 0.59) and stays above; no two lines cross after this. B has two neighbours and D has three, but B's two neighbours (A and G) are the strongest nodes. D's third neighbour is the leaf C. Steps 5 to 8: the lines are nearly flat and only the second decimal moves; the order A G F B D E C does not change. Step 30 (the last dot): nothing moves; these seven heights are the eigenvector of the largest eigenvalue, 2.884, with its largest entry set to 1. Ask: what do you expect if we start from random numbers instead of all ones? The next slide answers.
-->

---

<!-- _class: L-b -->

## Start anywhere: the same scores

<div class="cols">
<div class="fig tall">

![w:537](figures/frames/power-starts/00.png)

</div>
</div>

<div class="take">

A run ends all negative? <span class="hot">Flip the sign</span>.

</div>

<!--
Explain the bottom line on this slide; the next 1 slides step the figure, one change each (the grey note says which).
Random starts: every run ends on the same scores. One run ends all negative: -c is an eigenvector too, with the same lambda.
Same lines as the stage, but the start is no longer all ones: x_0 is seven random numbers between -1 and 1, and every step is x <- A x divided by the entry with the largest absolute value. The three panels end on exactly the same heights: A 1.00, G 0.85, F 0.81, B 0.64, D 0.58, E 0.48, C 0.20. The start only changes how the first few steps wiggle. A start that is almost orthogonal to u_1 would take longer, which is why the seeds here have a clear component along u_1.
-->


---

<!-- _class: L-b -->

## Start anywhere: the same scores

<div class="cols">
<div class="fig tall">

![w:537](figures/frames/power-starts/01.png)

</div>
</div>

<div class="take">

A run ends all negative? <span class="hot">Flip the sign</span>.

</div>

<!--
Step 1 of 1: the fourth start ends on the same seven heights with every sign flipped (A at -1.00, C at -0.20). Why: x_0 = c_1 u_1 + c_2 u_2 + ..., and the part along u_1 wins. If c_1 (the dot product of x_0 with u_1) is positive the run ends on +c, if it is negative it ends on -c. Both are eigenvectors with the same eigenvalue, because A(-c) = -(A c) = -(lambda c) = lambda (-c). Flipping the sign of an eigenvector never changes its eigenvalue. Eigenvector centrality needs positive scores (Perron-Frobenius), so if the run ends all negative, multiply by -1. Ask the room: which sign of x_0 gives the negative run? (Its dot product with u_1 is negative.)
-->

---

<!-- header: Eigenvector centrality -->
<!-- _class: L-a -->

## Where does eigenvector centrality break?

<div class="sub">

Four 4-cliques in a ring. Add one node to one clique.

</div>

<div class="cols">
<div class="fig tall">

![w:537](figures/ring-4444.png)

</div>
</div>

<div class="cue">

*Where does the score go? Take 30 seconds.*

</div>

<!--
Ask: one clique of 5, three of 4. Who gets the score? Most will say "a bit more for the big one".
-->

---

<!-- _class: L-a -->

## <span class="hot">Localization</span>: one clique takes it

<div class="sub">

Grow one clique to K nodes, one node at a time.

</div>

<div class="cols">
<div class="fig tall">

![w:537](figures/frames/ring-local/00.png)

</div>
</div>

<!--
Explain the line on this slide; the next 4 slides step the figure, one change each (the grey note says which).
The densest part takes almost all the score.
One extra node, and 68% of the total score moves into that clique; with two, 85%; at K = 8, 94%. The other three cliques, identical to each other, score almost nothing.
-->


---

<!-- _class: L-a -->

## <span class="hot">Localization</span>: one clique takes it

<div class="sub">

Grow one clique to K nodes, one node at a time.

</div>

<div class="cols">
<div class="fig tall">

![w:537](figures/frames/ring-local/01.png)

</div>
</div>

<!--
Step 1 of 4: K = 4: equal cliques, equal shares (25%).
-->

---

<!-- _class: L-a -->

## <span class="hot">Localization</span>: one clique takes it

<div class="sub">

Grow one clique to K nodes, one node at a time.

</div>

<div class="cols">
<div class="fig tall">

![w:537](figures/frames/ring-local/02.png)

</div>
</div>

<!--
Step 2 of 4: K = 5: one more node, 68%.
-->

---

<!-- _class: L-a -->

## <span class="hot">Localization</span>: one clique takes it

<div class="sub">

Grow one clique to K nodes, one node at a time.

</div>

<div class="cols">
<div class="fig tall">

![w:537](figures/frames/ring-local/03.png)

</div>
</div>

<!--
Step 3 of 4: K = 6: 85%.
-->

---

<!-- _class: L-a -->

## <span class="hot">Localization</span>: one clique takes it

<div class="sub">

Grow one clique to K nodes, one node at a time.

</div>

<div class="cols">
<div class="fig tall">

![w:537](figures/frames/ring-local/04.png)

</div>
</div>

<!--
Step 4 of 4: K = 8: 94%.
-->

---

<!-- header: New York State highways -->
<!-- _class: L-b -->

## 96% of the score lies near NYC

<div class="cols">
<div class="fig">

![w:537](figures/ny-eigenvector.png)

</div>
</div>

<div class="take">

31% of the interchanges lie there 🤔

</div>

<!--
"Near NYC": within 60 km of Manhattan, the circle on the map. 96% is the share of the sum of the scores.
The real network localizes: the densest cluster, Long Island and the city, takes 96% of the score. The top node is I-495 at Hempstead, Long Island. Upstate interchanges all score close to zero.
-->

---

<!-- header: "" -->
<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 05</span></div>

## What if every node gets a baseline?

Katz centrality

---

<!-- header: Katz centrality -->
<!-- _class: L-a -->

## <span class="hot">Katz</span>: a baseline plus the neighbours

<div class="sub">

$c_i = \beta + \alpha \sum_j A_{ij}\, c_j$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/katz-floor.png)

</div>
</div>

<div class="take">

In matrix form: $\mathbf{c} = \beta\, (I - \alpha A)^{-1} \mathbf{1}$

</div>

<!--
Everyone gets beta for free, plus alpha times the neighbours' scores, so no node can be driven to zero. Move the sum to the left: (I - alpha A) c = beta 1, and invert. I: the identity matrix; 1: all ones.
-->

---

<!-- _class: L-a -->

## What is that inverse?

<div class="sub">

$\mathbf{c} = \beta\, (I - \alpha A)^{-1} \mathbf{1}$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/katz-floor.png)

</div>
</div>

<div class="take">

Hint: $1/(1-x) = 1 + x + x^2 + \cdots$ for $|x| < 1$.

</div>

<div class="cue">

*Take 30 seconds.*

</div>

---

<!-- _class: L-a -->

## The same series for matrices

<div class="sub">

$(I-\alpha A)^{-1} = \sum_{k \ge 0} \alpha^k A^k$

</div>

<div class="cols">
<div class="fig tall">

![w:537](figures/frames/walks-discount/00.png)

</div>
</div>

<div class="take">

Katz counts <span class="hot">walks</span>, discounted by length.

</div>

<!--
Explain the formula and the bottom line on this slide; the next 3 slides step the figure, one change each (the grey note says which).
A^k counts the walks of length k (Module 01).
Multiply both sides by (I - alpha A) to check. The series converges only if alpha is small enough: the dial on the next slide.
-->


---

<!-- _class: L-a -->

## The same series for matrices

<div class="sub">

$(I-\alpha A)^{-1} = \sum_{k \ge 0} \alpha^k A^k$

</div>

<div class="cols">
<div class="fig tall">

![w:537](figures/frames/walks-discount/01.png)

</div>
</div>

<div class="take">

Katz counts <span class="hot">walks</span>, discounted by length.

</div>

<!--
Step 1 of 3: 2 walks of length 2, alpha^2 each.
-->

---

<!-- _class: L-a -->

## The same series for matrices

<div class="sub">

$(I-\alpha A)^{-1} = \sum_{k \ge 0} \alpha^k A^k$

</div>

<div class="cols">
<div class="fig tall">

![w:537](figures/frames/walks-discount/02.png)

</div>
</div>

<div class="take">

Katz counts <span class="hot">walks</span>, discounted by length.

</div>

<!--
Step 2 of 3: 1 walk of length 3: alpha^3.
-->

---

<!-- _class: L-a -->

## The same series for matrices

<div class="sub">

$(I-\alpha A)^{-1} = \sum_{k \ge 0} \alpha^k A^k$

</div>

<div class="cols">
<div class="fig tall">

![w:537](figures/frames/walks-discount/03.png)

</div>
</div>

<div class="take">

Katz counts <span class="hot">walks</span>, discounted by length.

</div>

<!--
Step 3 of 3: every length, discounted.
-->

---

## Turn the dial

<figure class="anim-stage" id="katz-dial">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>

  <div class="anim-grid-2" data-anim-canvas>
    <div data-anim-clear data-kd-draw></div>
    <div data-anim-clear data-kd-side></div>
  </div>

  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script>window.animStepOnly = true;</script>
<script src="../../lecture-note/assets/anim/katz-dial.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

<!--
Four cliques, 4, 4, 4 and 6, joined in a ring; the six is the dashed circle. Shade = Katz score divided by the largest score.

First click shows alpha = 0: only the baseline counts, every node scores 1, and the big clique holds 6 of 18 = 33% of the total. The second click puts the dial at 0.5 / lambda_max; drag it. The tick is 1/lambda_max, with lambda_max = 5.084 for this graph. As alpha rises the big clique's share climbs: 40% at 0.5, 63% at 0.9, 81% at 0.99. Walks of every length count, discounted by alpha per step, and the big clique has the most walks. At the tick the series 1 + alpha A + alpha^2 A^2 + ... stops converging and the scores blow up. Past the tick the formula still returns numbers, but many are negative and they mean nothing. Ask: what did alpha = 0 give, and what does the dial look like as alpha goes to 1/lambda_max? It approaches the eigenvector, which is the previous slides' localization.
-->

---

<!-- _class: L-a -->

## Why does $\alpha$ stop at $1/\lambda_{\max}$?

<div class="sub">

$(I - \alpha A)^{-1} = \sum_k \tfrac{1}{1 - \alpha \lambda_k}\, \mathbf{u}_k \mathbf{u}_k^\top$

</div>

<div class="fig">

![w:1080](figures/frames/katz-why/00.png)

</div>

<!--
Explain the formula on this slide; the next 3 slides step the figure, one change each (the grey note says which).
The 7-node network of the eigenvector slides (lambda_max = 2.884). Left: the dial for alpha, from 0 to past 1/lambda_max (the red part is past it). Right: the function 1/(1 - alpha x); the dots are its values at the seven eigenvalues of A, and those values are the weights of the terms below (the circles). The function has a wall at x = 1/alpha, where it goes to infinity, and on the far side of the wall it is negative. Raising alpha moves the wall left, towards lambda_1. At alpha = 0.5/lambda_max the weights are comparable (2, 1.30, ..., 0.72).
-->


---

<!-- _class: L-a -->

## Why does $\alpha$ stop at $1/\lambda_{\max}$?

<div class="sub">

$(I - \alpha A)^{-1} = \sum_k \tfrac{1}{1 - \alpha \lambda_k}\, \mathbf{u}_k \mathbf{u}_k^\top$

</div>

<div class="fig">

![w:1080](figures/frames/katz-why/01.png)

</div>

<!--
Step 1 of 3: lambda_1 nears the wall 1/alpha: its weight is 5.
-->

---

<!-- _class: L-a -->

## Why does $\alpha$ stop at $1/\lambda_{\max}$?

<div class="sub">

$(I - \alpha A)^{-1} = \sum_k \tfrac{1}{1 - \alpha \lambda_k}\, \mathbf{u}_k \mathbf{u}_k^\top$

</div>

<div class="fig">

![w:1080](figures/frames/katz-why/02.png)

</div>

<!--
Step 2 of 3: 1/alpha nears lambda_1: its weight blows up (20 at 0.95/lambda_max, 100 at 0.99, infinite at 1/lambda_max). The first term swamps the rest: Katz becomes eigenvector centrality.
-->

---

<!-- _class: L-a -->

## Why does $\alpha$ stop at $1/\lambda_{\max}$?

<div class="sub">

$(I - \alpha A)^{-1} = \sum_k \tfrac{1}{1 - \alpha \lambda_k}\, \mathbf{u}_k \mathbf{u}_k^\top$

</div>

<div class="fig">

![w:1080](figures/frames/katz-why/03.png)

</div>

<!--
Step 3 of 3: past it, lambda_1 sits on the far side of the wall: its weight is negative (-10 at 1.1/lambda_max). The series no longer converges and the scores mean nothing; the character of the formula has changed completely.
-->

---

<!-- _class: L-a -->

## Which lettered node scores higher now?

<div class="sub">

Katz, $\alpha = 0.5/\lambda_{\max}$.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-eig-L.png)

</div>
</div>

<div class="cue">

*The network from the eigenvector quiz. Take a minute.*

</div>

---

<!-- _class: L-a -->

## Which lettered node scores higher now?

<div class="sub">

Katz, $\alpha = 0.5/\lambda_{\max}$.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-katz-L-ans.png)

</div>
</div>

<div class="take">

<span class="hot">M</span> again, as the eigenvector said.

</div>

<!--
M 0.87, X 0.81 (largest = 1).
-->

---

<!-- _class: L-a -->

## Which lettered node scores higher now?

<div class="sub">

Katz, $\alpha = 0.5/\lambda_{\max}$.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-eig-R.png)

</div>
</div>

<div class="cue">

*The network from the eigenvector quiz. Take a minute.*

</div>

---

<!-- _class: L-a -->

## Which lettered node scores higher now?

<div class="sub">

Katz, $\alpha = 0.5/\lambda_{\max}$.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/q-katz-R-ans.png)

</div>
</div>

<div class="take">

<span class="hot">H</span> now: short walks still weigh a lot.

</div>

<!--
H 1.00, K 0.81. At alpha = 0.5/lambda_max short walks still weigh a lot, so H's six neighbours count; as alpha approaches 1/lambda_max, Katz turns into the eigenvector and K passes H (between 0.8 and 0.9 of 1/lambda_max).
-->

---

<!-- header: "" -->
<!-- _class: L-b -->

## The walk row

<div class="fig tall">

![w:1080](figures/grid-row2.png)

</div>

<!--
Degree and eigenvector centrality are the two ends of Katz: alpha near 0 ranks by degree, alpha near 1/lambda_max by the eigenvector.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Five</span><span class="count">05 / 05</span></div>

## What if a link runs one way?

HITS · PageRank

<!--
A road runs both ways. A link on the Web does not.
-->

---

<!-- header: HITS (Kleinberg 1999) -->
<!-- _class: left -->

## Hubs and authorities

<div class="cols">
<div>

* <strong class="cool">Authority</strong> $a_j = \sum_i A_{ij}\, h_i$: pointed to by good hubs.
* **Hub** $h_i = \sum_j A_{ij}\, a_j$: points to good authorities.
* On a road map, HITS is eigenvector centrality.

</div>
<div class="fig">

![w:537](figures/hits-graph.png)
<figcaption>A_ij = 1: page i links to page j</figcaption>

</div>
</div>

<!--
Two terms defined beside one figure, so this slide keeps text beside the figure (HOUSE_STYLE section 8, C).
HITS (Kleinberg, 1999). Two scores per page. A links out three times and is the best hub; E is linked to three times and is the best authority.
On a road map A is symmetric, so A^T A = A^2, whose leading eigenvector is that of A (when the network is not bipartite: here 2.88 > 2.26).
-->

---

<!-- header: "" -->
<!-- _class: L-a -->

## The same idea, six times

<div class="sub">

A node's score is built from its neighbours' scores.

</div>

<div class="fig">

![w:1080](figures/genealogy.png)

</div>

<!--
Landau (1895) ranked chess players by the scores of the players they beat. Seeley (1949) ranked children by who chose them. Katz (1953): status with a baseline. Hubbell (1965): influence in a group. Bonacich (1972): eigenvector centrality. Brin and Page (1998): PageRank, which comes next.
-->

---

<!-- header: PageRank (Brin and Page 1998) -->
<!-- _class: L-a -->

## Which ranks higher, C or E?

<div class="sub">

A page splits its score: $c_j = \sum_i A_{ij}\, c_i / d^{\text{out}}_i$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/pr-split.png)

</div>
</div>

<div class="cue">

*C: three links in. E: one. Take 30 seconds.*

</div>

<!--
A_ij = 1 means a link from i to j; d_out i is the number of links out of i. A gives a third to each of B, C, D.
-->

---

<!-- _class: L-a -->

## Which ranks higher, C or E?

<div class="sub">

A page splits its score: $c_j = \sum_i A_{ij}\, c_i / d^{\text{out}}_i$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/pr-split-answer/00.png)

</div>
</div>

<div class="take">

They tie: A, C and E each hold <span class="hot">3/11</span>.

</div>

<!--
Explain the bottom line on this slide; the next 4 slides step the figure, one change each (the grey note says which).
A, C and E: 3/11 each. B and D: 1/11. A link carries its sender's score divided by its links out. Why C is not 7/3: 1 + 1 + 1/3 adds the shares, which are fractions of the sender's score. The amount a link carries is the sender's score times its share, and at the answer the amounts coming into a page add up to that page's own score.
-->


---

<!-- _class: L-a -->

## Which ranks higher, C or E?

<div class="sub">

A page splits its score: $c_j = \sum_i A_{ij}\, c_i / d^{\text{out}}_i$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/pr-split-answer/01.png)

</div>
</div>

<div class="take">

They tie: A, C and E each hold <span class="hot">3/11</span>.

</div>

<!--
Step 1 of 4: 3/11 ÷ 3 = 1/11 each. A's 3/11 is split three ways, so each of its links carries 1/11. The 1/3 that was on the link is a fraction of A's score, not an amount.
-->

---

<!-- _class: L-a -->

## Which ranks higher, C or E?

<div class="sub">

A page splits its score: $c_j = \sum_i A_{ij}\, c_i / d^{\text{out}}_i$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/pr-split-answer/02.png)

</div>
</div>

<div class="take">

They tie: A, C and E each hold <span class="hot">3/11</span>.

</div>

<!--
Step 2 of 4: B and D pass on all of 1/11. B and D each have one link out, so each passes on all of its 1/11 to C.
-->

---

<!-- _class: L-a -->

## Which ranks higher, C or E?

<div class="sub">

A page splits its score: $c_j = \sum_i A_{ij}\, c_i / d^{\text{out}}_i$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/pr-split-answer/03.png)

</div>
</div>

<div class="take">

They tie: A, C and E each hold <span class="hot">3/11</span>.

</div>

<!--
Step 3 of 4: 1/11 + 1/11 + 1/11 = 3/11. C receives 1/11 from A, 1/11 from B and 1/11 from D: 3/11, exactly C's own score. Adding the fractions instead (1/3 + 1 + 1 = 7/3) gives one step of the iteration that starts from everyone holding 1; it is not the answer.
-->

---

<!-- _class: L-a -->

## Which ranks higher, C or E?

<div class="sub">

A page splits its score: $c_j = \sum_i A_{ij}\, c_i / d^{\text{out}}_i$

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/pr-split-answer/04.png)

</div>
</div>

<div class="take">

They tie: A, C and E each hold <span class="hot">3/11</span>.

</div>

<!--
Step 4 of 4: in = out at every page. C passes all 3/11 to E and E passes all 3/11 to A. Every page receives exactly what it holds, so nothing changes any more: that balance is the answer.
-->

---

<!-- _class: L-a -->

## A dead end: the total goes to 0

<div class="sub">

E loses its only link out.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/pr-leak/00.png)

</div>
</div>

<!--
Explain the line on this slide; the next 3 slides step the figure, one change each (the grey note says which).
Its score has nowhere to go: the total drains to zero. The total goes 1, 0.8, 0.6, ... 0.
-->


---

<!-- _class: L-a -->

## A dead end: the total goes to 0

<div class="sub">

E loses its only link out.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/pr-leak/01.png)

</div>
</div>

<!--
Step 1 of 3: E's only link out is gone.
-->

---

<!-- _class: L-a -->

## A dead end: the total goes to 0

<div class="sub">

E loses its only link out.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/pr-leak/02.png)

</div>
</div>

<!--
Step 2 of 3: score leaks out at E: total 0.60.
-->

---

<!-- _class: L-a -->

## A dead end: the total goes to 0

<div class="sub">

E loses its only link out.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/frames/pr-leak/03.png)

</div>
</div>

<!--
Step 3 of 3: nothing left: total 0.00.
-->

---

<!-- _class: L-a -->

## Teleportation gives <span class="hot">PageRank</span>

<div class="sub">

With probability $r = 0.15$, jump to a random page.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/pr-teleport.png)

</div>
</div>

<div class="take">

$c_j = (1-r) \sum_i A_{ij}\, c_i / d^{\text{out}}_i + r/N$

</div>

<!--
A dead end links to every page: it hands its score to the jump. The jump also makes the answer unique.
Brin and Page, 1998. On the dead-end graph: E 0.359, C 0.316, B and D 0.117, A 0.091.
-->

---

<!-- _class: L-a -->

## <span class="hot">Personalized</span> PageRank

<div class="sub">

Jump back to A only.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/ppr.png)

</div>
</div>

<div class="take">

Visits by a walker who restarts at A.

</div>

<!--
Replace r/N by r on A and 0 elsewhere. The score of a page is how often a walker that keeps restarting at A visits it. "More like this" on a website: teleport to the page you are on.
-->

---

<!-- header: New York State highways -->
<!-- _class: L-b -->

## Five measures, five different winners

<div class="cols">
<div class="fig">

![w:537](figures/ny-five.png)

</div>
</div>

<!--
Each measure's winner, on one map. No two agree.
Closeness: NY 17 at Middletown. Harmonic: I-95 in the Bronx. Eccentricity: NY 17 east of Binghamton. Betweenness: NY 17 at Monticello. Eigenvector: I-495 on Long Island.
-->

---

<!-- header: "" -->
<!-- _class: L-b -->

## Two choices, every centrality

<div class="fig tall">

![w:1080](figures/grid-final.png)

</div>

---

<!-- _class: L-f -->

## Draw a network where four measures disagree

Degree, closeness, eccentricity and betweenness each rank a different node first.

<div class="cue">

*Bring it to the next class.*

</div>

<!--
Deliberately the day-1 measures: the shortest-path row. A student who finishes can add eigenvector centrality as a fifth.
-->

---

<!-- _class: L-a -->

## Do all roads lead to <span class="hot">Rome</span>?

<div class="sub">

Node: a city. Edge: a road or a sea lane.

</div>

<div class="cols">
<div class="fig">

![w:537](figures/roma-to-graph.png)

</div>
</div>

<div class="take">

Rank the twelve cities with every measure.

</div>

<!--
The opening picture, now with the tools to answer it. Do not answer it here: the Module 6 lab asks the same questions of Rome.
-->

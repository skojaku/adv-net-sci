---
marp: true
theme: network-science
paginate: true
math: katex
---

<!-- _class: lead -->

<div class="eyebrow">Advanced Topics in Network Science · Module 06</div>

# All Roads Lead to Rome

<hr>

<div class="sub">… do they?</div>

<div class="credit">Sadamori Kojaku · Binghamton University</div>

<script src="scrub.js"></script>
<script>window.animStepOnly = true;</script>

<!--
Day 1 (10/20): slides 1 to 62, measured by shortest paths. Day 2 (10/22): slides 63 to 122, measured by walks. About a third are build steps, a few seconds each.
The pen-and-paper sheet has already been done, so the room has met degree, average distance, "indispensable" and passing scores around. Name things; do not re-derive what is in their hands.
A build is a run of slides with the same title: explain the bullets on the first, then step; the grey note on each figure says what changed.
-->

---

## The Golden Milestone

<hr>

<div class="cols">
<div>

* 20 BC: Augustus, Caesar's heir, set it up in Rome.
* Every road of Italy ended at it.
* Distances were counted in miles from Rome.

</div>
<div>

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

## Twelve cities of the empire

<hr>

<div class="cols">
<div>

- Roads and sea lanes joined them.

</div>
<div class="fig tall">

![w:537](figures/roma-basemap.png)
<figcaption>map © OpenStreetMap contributors</figcaption>

</div>
</div>

<!--
The pins are the real places: Londinium, Colonia, Lugdunum, Massilia, Tarraco, Mediolanum, Roma, Carthago, Thessalonica, Athenae, Byzantium, Alexandria.
-->

---

## Keep the links, drop the map

<hr>

<div class="cols">
<div>

* Node: a city. Edge: a road or a sea lane.
* Which city is the most important?

</div>
<div class="fig tall">

![w:537](figures/roma-to-graph.png)

</div>
</div>

<!--
The same twelve cities at the same places: the map is gone, the roads are straight links.
Take answers. The room will give at least two kinds of reason (many roads; close to everything). Both are right. That is the module.
-->

---

## Degree centrality

<hr>

<div class="cols">
<div>

* **Degree**: the number of roads at a city.
* $d_i = \sum_j A_{ij}$, where $A_{ij} = 1$ if a road joins $i$ and $j$.
* Roma: 5, the most.
* It sees only the neighbours.

</div>
<div class="fig tall">

![w:537](figures/roma-degree.png)

</div>
</div>

<!--
The sheet's first question. Name it and move on. The same network as before; the shade is the degree.
-->

---

## New York State highways

<hr>

<div class="cols">
<div>

* 289 interchanges, 433 road segments.
* Which city do the most cross-state trips pass through?

</div>
<div class="fig">

![w:537](figures/ny-overview.png)
<figcaption>© OpenStreetMap</figcaption>

</div>
</div>

<div class="cue">

*Hold your answer until the end of today.*

</div>

<!--
Do not answer. It comes back at the end of today (betweenness).
The network: OpenStreetMap motorways and trunk roads in New York State, one node per interchange (junctions within 3.5 km merged), 289 nodes and 433 road segments. Distance is km of road.
Take a vote: Buffalo, Rochester, Syracuse, Utica, Albany, NYC, Binghamton, Watertown.
-->

---

## New York: degree

<hr>

<div class="cols">
<div>

- Degree 3: 201 interchanges. Degree 4: 57.
- Degree cannot tell the interchanges apart.

</div>
<div class="fig">

![w:537](figures/ny-degree.png)

</div>
</div>

<!--
On a road map almost every junction joins three or four roads. A measure that only looks one step out sees almost nothing.
-->

---

## How far is u from v?

<hr>

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

## Two ways to count

<hr>

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
The walk counts are the entries of A, A squared, A cubed, ... from Module 01. Walks of length 2: 2; length 3: 1; length 4: 11.
-->

---

## Two ways to count

<hr>

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

## Two ways to count

<hr>

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

## Two ways to count

<hr>

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

## Two ways to count

<hr>

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

## Two choices make a centrality

<hr>

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

## Close to everything

near every other node, on average, at worst

---

## Closeness centrality

<hr>

<div class="cols">
<div>

* **Closeness**: add up the distances $\ell_{ij}$ to every other node, then invert.
* $c_i = \dfrac{N-1}{\sum_{j \ne i} \ell_{ij}}$
* $N-1$: a star's centre scores exactly 1.

</div>
<div class="fig">

![w:537](figures/frames/closeness-def/00.png)

</div>
</div>

<!--
Explain the bullets on this slide; the next 5 slides step the figure, one change each (the grey note says which).
The steps: each node's sum of distances (A 15, C and E 11, D 10); then each sum turns into closeness, (N - 1)/sum with N = 7: A, B, F, G 6/15 = 0.40; C, E 6/11 = 0.55; D 6/10 = 0.60, the highest.
The sum is not the score: closeness is its inverse, so higher is better. N - 1 makes the best case, a star's centre, exactly 1.
-->

---

## Closeness centrality

<hr>

<div class="cols">
<div>

- **Closeness**: add up the distances $\ell_{ij}$ to every other node, then invert.
- $c_i = \dfrac{N-1}{\sum_{j \ne i} \ell_{ij}}$
- $N-1$: a star's centre scores exactly 1.

</div>
<div class="fig">

![w:537](figures/frames/closeness-def/01.png)

</div>
</div>

<!--
Step 1 of 5: distances from A.
-->

---

## Closeness centrality

<hr>

<div class="cols">
<div>

- **Closeness**: add up the distances $\ell_{ij}$ to every other node, then invert.
- $c_i = \dfrac{N-1}{\sum_{j \ne i} \ell_{ij}}$
- $N-1$: a star's centre scores exactly 1.

</div>
<div class="fig">

![w:537](figures/frames/closeness-def/02.png)

</div>
</div>

<!--
Step 2 of 5: 1+1+2+3+4+4 = 15.
-->

---

## Closeness centrality

<hr>

<div class="cols">
<div>

- **Closeness**: add up the distances $\ell_{ij}$ to every other node, then invert.
- $c_i = \dfrac{N-1}{\sum_{j \ne i} \ell_{ij}}$
- $N-1$: a star's centre scores exactly 1.

</div>
<div class="fig">

![w:537](figures/frames/closeness-def/03.png)

</div>
</div>

<!--
Step 3 of 5: every node's sum.
-->

---

## Closeness centrality

<hr>

<div class="cols">
<div>

- **Closeness**: add up the distances $\ell_{ij}$ to every other node, then invert.
- $c_i = \dfrac{N-1}{\sum_{j \ne i} \ell_{ij}}$
- $N-1$: a star's centre scores exactly 1.

</div>
<div class="fig">

![w:537](figures/frames/closeness-def/04.png)

</div>
</div>

<!--
Step 4 of 5: 6/15 = 0.40.
-->

---

## Closeness centrality

<hr>

<div class="cols">
<div>

- **Closeness**: add up the distances $\ell_{ij}$ to every other node, then invert.
- $c_i = \dfrac{N-1}{\sum_{j \ne i} \ell_{ij}}$
- $N-1$: a star's centre scores exactly 1.

</div>
<div class="fig">

![w:537](figures/frames/closeness-def/05.png)

</div>
</div>

<!--
Step 5 of 5: highest: D, 0.60.
-->

---

## Which node is closest to everything?

<hr>

<div class="cols">
<div>

- Highest closeness wins: the smallest sum of distances.

</div>
<div class="fig">

![w:537](figures/q-close-CB.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

## Which node is closest to everything?

<hr>

<div class="cols">
<div>

- Highest closeness wins: the smallest sum of distances.
- P's long arms beat N's triangle.

</div>
<div class="fig">

![w:537](figures/q-close-CB-ans.png)

</div>
</div>

<!--
P: sum 16, closeness 9/16 = 0.56. N: sum 18, closeness 9/18 = 0.50 (N = 10 nodes). N's triangle looks central, but P's long arms hold more nodes.
-->

---

## Which node is closest to everything?

<hr>

<div class="cols">
<div>

- Highest closeness wins: the smallest sum of distances.

</div>
<div class="fig">

![w:537](figures/q-close-CA.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

## Which node is closest to everything?

<hr>

<div class="cols">
<div>

- Highest closeness wins: the smallest sum of distances.
- The hub E loses to F.

</div>
<div class="fig">

![w:537](figures/q-close-CA-ans.png)

</div>
</div>

<!--
F has degree 2 and a sum of 19: closeness 10/19 = 0.53. The hub E (degree 5) and G both have 20: 0.50 (N = 11 nodes). Moving from E to F, five nodes get one step farther (A, B, C, D, E) and six get one step closer.
-->

---

## What if one road closes?

<hr>

<div class="cols">
<div>

- Close the road between E and F.
- What happens to closeness?

</div>
<div class="fig">

![w:537](figures/cut-blank.png)

</div>
</div>

<div class="cue">

*Take 30 seconds.*

</div>

---

## What if one road closes?

<hr>

<div class="cols">
<div>

- Close the road between E and F.
- Some distances are now $\infty$: every closeness is 0.

</div>
<div class="fig">

![w:537](figures/cut-closeness.png)

</div>
</div>

<!--
Not just the nodes near the cut: all eleven. Every sum is infinite. Closeness cannot rank a disconnected network at all.
-->

---

## Take the reciprocal first

<hr>

<div class="cols">
<div>

* **Harmonic centrality**: add $1/\ell_{ij}$ instead.
* $h_i = \sum_{j \ne i} \dfrac{1}{\ell_{ij}}$
* $1/\infty = 0$: an unreachable node adds nothing.

</div>
<div class="fig">

![w:537](figures/frames/harmonic-def/00.png)

</div>
</div>

<!--
Explain the bullets on this slide; the next 5 slides step the figure, one change each (the grey note says which).
The steps, from G: four nodes at distance 1, K at 2, the other piece unreachable: 4 + 1/2 = 9/2. Then every node's score.
-->

---

## Take the reciprocal first

<hr>

<div class="cols">
<div>

- **Harmonic centrality**: add $1/\ell_{ij}$ instead.
- $h_i = \sum_{j \ne i} \dfrac{1}{\ell_{ij}}$
- $1/\infty = 0$: an unreachable node adds nothing.

</div>
<div class="fig">

![w:537](figures/frames/harmonic-def/01.png)

</div>
</div>

<!--
Step 1 of 5: G's neighbours: 1/1 each.
-->

---

## Take the reciprocal first

<hr>

<div class="cols">
<div>

- **Harmonic centrality**: add $1/\ell_{ij}$ instead.
- $h_i = \sum_{j \ne i} \dfrac{1}{\ell_{ij}}$
- $1/\infty = 0$: an unreachable node adds nothing.

</div>
<div class="fig">

![w:537](figures/frames/harmonic-def/02.png)

</div>
</div>

<!--
Step 2 of 5: K is 2 steps from G, so it adds 1/2.
-->

---

## Take the reciprocal first

<hr>

<div class="cols">
<div>

- **Harmonic centrality**: add $1/\ell_{ij}$ instead.
- $h_i = \sum_{j \ne i} \dfrac{1}{\ell_{ij}}$
- $1/\infty = 0$: an unreachable node adds nothing.

</div>
<div class="fig">

![w:537](figures/frames/harmonic-def/03.png)

</div>
</div>

<!--
Step 3 of 5: unreachable: 1/inf = 0.
-->

---

## Take the reciprocal first

<hr>

<div class="cols">
<div>

- **Harmonic centrality**: add $1/\ell_{ij}$ instead.
- $h_i = \sum_{j \ne i} \dfrac{1}{\ell_{ij}}$
- $1/\infty = 0$: an unreachable node adds nothing.

</div>
<div class="fig">

![w:537](figures/frames/harmonic-def/04.png)

</div>
</div>

<!--
Step 4 of 5: 4 + 1/2 = 9/2.
-->

---

## Take the reciprocal first

<hr>

<div class="cols">
<div>

- **Harmonic centrality**: add $1/\ell_{ij}$ instead.
- $h_i = \sum_{j \ne i} \dfrac{1}{\ell_{ij}}$
- $1/\infty = 0$: an unreachable node adds nothing.

</div>
<div class="fig">

![w:537](figures/frames/harmonic-def/05.png)

</div>
</div>

<!--
Step 5 of 5: highest: G.
-->

---

## Which node has the highest harmonic centrality?

<hr>

<div class="cols">
<div>

- The road E–F is open again.
- Closeness picked F.

</div>
<div class="fig">

![w:537](figures/q-close-CA.png)

</div>
</div>

<div class="cue">

*Does the winner change?*

</div>

---

## Which node has the highest harmonic centrality?

<hr>

<div class="cols">
<div>

- The road E–F is open again.
- Closeness picked F. Harmonic picks the hub E.

</div>
<div class="fig">

![w:537](figures/q-harm-CA-ans.png)

</div>
</div>

<!--
E 27/4 beats G 19/3 and F 35/6. With 1/distance, the four leaves at distance 1 count fully for E; with the sum of distances, they barely helped.
-->

---

## Which node has the highest harmonic centrality?

<hr>

<div class="cols">
<div>

- Two pieces.

</div>
<div class="fig">

![w:537](figures/q-harm-HD.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

## Which node has the highest harmonic centrality?

<hr>

<div class="cols">
<div>

- Two pieces.
- The star's centre beats the middle of the path.

</div>
<div class="fig">

![w:537](figures/q-harm-HD-ans.png)

</div>
</div>

<!--
The star's centre scores 4; the middle of the path, 11/3. The bigger piece is not the better one.
-->

---

## New York: closeness

<hr>

<div class="cols">
<div>

* Distance: km of highway.
* Winner: NY 17.
* 31% of the interchanges lie inside the circle.

</div>
<div class="fig">

![w:537](figures/ny-closeness.png)

</div>
</div>

<!--
Closeness is pulled toward where the nodes are. 91 of 289 interchanges are within 60 km of Manhattan, so the best average sits just north of the city, not in the middle of the state. (Harmonic picks I-95 in the Bronx.)
-->

---

## Would you site a fire station on the average?

<hr>

<div class="cols">
<div>

- Closeness picks D: 0.60, the highest.

</div>
<div class="fig">

![w:537](figures/bowtie-closeness.png)

</div>
</div>

<div class="cue">

*Take 30 seconds.*

</div>

---

## Eccentricity

<hr>

<div class="cols">
<div>

* A fire station must reach its farthest house.
* **Eccentricity**: $e_i = \max_j \ell_{ij}$.
* Smallest $e_i$ wins; its centrality is $1/e_i$.

</div>
<div class="fig">

![w:537](figures/frames/ecc-def/00.png)

</div>
</div>

<!--
Explain the bullets on this slide; the next 3 slides step the figure, one change each (the grey note says which).
The steps: the closeness values give way to each node's farthest distance. D is still best here, 2. The next question is built so that it is not.
-->

---

## Eccentricity

<hr>

<div class="cols">
<div>

- A fire station must reach its farthest house.
- **Eccentricity**: $e_i = \max_j \ell_{ij}$.
- Smallest $e_i$ wins; its centrality is $1/e_i$.

</div>
<div class="fig">

![w:537](figures/frames/ecc-def/01.png)

</div>
</div>

<!--
Step 1 of 3: A's farthest: 4 steps.
-->

---

## Eccentricity

<hr>

<div class="cols">
<div>

- A fire station must reach its farthest house.
- **Eccentricity**: $e_i = \max_j \ell_{ij}$.
- Smallest $e_i$ wins; its centrality is $1/e_i$.

</div>
<div class="fig">

![w:537](figures/frames/ecc-def/02.png)

</div>
</div>

<!--
Step 2 of 3: every node's worst case.
-->

---

## Eccentricity

<hr>

<div class="cols">
<div>

- A fire station must reach its farthest house.
- **Eccentricity**: $e_i = \max_j \ell_{ij}$.
- Smallest $e_i$ wins; its centrality is $1/e_i$.

</div>
<div class="fig">

![w:537](figures/frames/ecc-def/03.png)

</div>
</div>

<!--
Step 3 of 3: smallest: D, 2.
-->

---

## Which node has the smallest eccentricity?

<hr>

<div class="cols">
<div>

- The best fire station: the smallest worst case.

</div>
<div class="fig">

![w:537](figures/q-ecc-EA.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

## Which node has the smallest eccentricity?

<hr>

<div class="cols">
<div>

- The best fire station: the smallest worst case.
- F: worst case 2. E, the best on average, has 3.

</div>
<div class="fig">

![w:537](figures/q-ecc-EA-ans.png)

</div>
</div>

<!--
E wins closeness (sum 10, the smallest) but its worst case is 3, the end of the tail. F has worst case 2.
-->

---

## Which node has the smallest eccentricity?

<hr>

<div class="cols">
<div>

- The best fire station: the smallest worst case.

</div>
<div class="fig">

![w:537](figures/q-ecc-EB.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

## Which node has the smallest eccentricity?

<hr>

<div class="cols">
<div>

- The best fire station: the smallest worst case.
- L: worst case 2. K, the best on average, has 3.

</div>
<div class="fig">

![w:537](figures/q-ecc-EB-ans.png)

</div>
</div>

<!--
K wins closeness (11), worst case 3. L, with degree 2, has worst case 2.
-->

---

## New York: eccentricity

<hr>

<div class="cols">
<div>

* The worst-case drive from each interchange.
* Smallest: 473 km, on NY 17 east of Binghamton.

</div>
<div class="fig">

![w:537](figures/ny-eccentricity.png)

</div>
</div>

<!--
If New York State had one fire station for its highways, it would go near us. From there the farthest interchange is where I-90 leaves the state west of Buffalo, 473 km; next is I-87 at the Canadian border.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 05</span></div>

## The broker

who the traffic cannot avoid

---

## Trace a letter

<hr>

<div class="cols">
<div>

* One letter per pair, along a shortest path.
* Count the letters each node carries.

</div>
<div class="fig">

![w:537](figures/frames/btw-def/00.png)

</div>
</div>

<!--
Explain the bullets on this slide; the next 4 slides step the figure, one change each (the grey note says which).
D carries 9: every letter between the left triangle and the right triangle. C and E carry 8 each.
-->

---

## Trace a letter

<hr>

<div class="cols">
<div>

- One letter per pair, along a shortest path.
- Count the letters each node carries.

</div>
<div class="fig">

![w:537](figures/frames/btw-def/01.png)

</div>
</div>

<!--
Step 1 of 4: A to F passes C, D, E.
-->

---

## Trace a letter

<hr>

<div class="cols">
<div>

- One letter per pair, along a shortest path.
- Count the letters each node carries.

</div>
<div class="fig">

![w:537](figures/frames/btw-def/02.png)

</div>
</div>

<!--
Step 2 of 4: all of A's letters.
-->

---

## Trace a letter

<hr>

<div class="cols">
<div>

- One letter per pair, along a shortest path.
- Count the letters each node carries.

</div>
<div class="fig">

![w:537](figures/frames/btw-def/03.png)

</div>
</div>

<!--
Step 3 of 4: every pair.
-->

---

## Trace a letter

<hr>

<div class="cols">
<div>

- One letter per pair, along a shortest path.
- Count the letters each node carries.

</div>
<div class="fig">

![w:537](figures/frames/btw-def/04.png)

</div>
</div>

<!--
Step 4 of 4: D carries the most, 9.
-->

---

## Betweenness centrality

<hr>

<div class="cols">
<div>

* $b_i = \displaystyle\sum_{s<t} \frac{\sigma_{st}(i)}{\sigma_{st}}$
* $\sigma_{st}$: the number of shortest $s$–$t$ paths.
* $\sigma_{st}(i)$: those that pass through $i$.
* From s to t: two shortest paths; C is on one, so C carries 1/2.

</div>
<div class="fig">

![w:537](figures/sigma-answer.png)

</div>
</div>

<!--
From s to t there are two shortest paths, s-A-D-t and s-B-C-t, and they share no node. C is on one of the two: sigma_st(C) = 1, sigma_st = 2, so C carries 1/2 of this pair. So do A, B and D. The pair counts once in total, shared out among its routes.
-->

---

## Which node carries the most?

<hr>

<div class="cols">
<div>

- Count the shortest paths through each node.

</div>
<div class="fig">

![w:537](figures/q-btw-DB.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

## Which node carries the most?

<hr>

<div class="cols">
<div>

- Count the shortest paths through each node.
- Each hub carries more than the bridge F.

</div>
<div class="fig">

![w:537](figures/q-btw-DB-ans.png)

</div>
</div>

<!--
F carries 5 x 5 = 25 pairs. E carries the 6 pairs among its leaves plus 4 x 6 pairs between a leaf and the rest: 30. Same for G.
-->

---

## Which node carries the most?

<hr>

<div class="cols">
<div>

- Count the shortest paths through each node.

</div>
<div class="fig">

![w:537](figures/q-btw-SQ.png)

</div>
</div>

<div class="cue">

*A tie splits the count.*

</div>

---

## Which node carries the most?

<hr>

<div class="cols">
<div>

- Count the shortest paths through each node.
- O wins by half a pair.

</div>
<div class="fig">

![w:537](figures/q-btw-SQ-ans.png)

</div>
</div>

<!--
O carries 9 pairs whole, and half of the pair P, Q (two shortest paths: through O and through R): 19/2. M carries 9.
-->

---

## New York: betweenness

<hr>

<div class="cols">
<div>

* Top interchange: NY 17 at Monticello.
* Of the eight cities: Binghamton, 3.5 × Syracuse.
* Four of the top five interchanges are on NY 17.

</div>
<div class="fig">

![w:537](figures/ny-betweenness.png)

</div>
</div>

<!--
The answer to this morning's question. Four of the top five interchanges in the whole state are on NY 17 between Binghamton and Middletown: the corridor between the NYC cluster and upstate. Binghamton is where that corridor meets I-81 and I-88. Monticello beats the NY 17 / NY 8 / NY 10 interchange near Binghamton by only 0.2% (0.3632 against 0.3626).
-->

---

## The shortest-path row

<hr>

<div class="fig tall">

![w:1080](figures/grid-row1.png)

</div>

<!--
Degree, and four more ways to turn shortest paths into one number.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 05</span></div>

## The company you keep

importance you inherit

<!--
Day 2 starts here.
-->

---

## Aesop

<hr>

<div class="cols">
<div>

<div class="formula">

“A man is known by the company he keeps.”

</div>

</div>
<div class="fig">

![w:537](figures/photos/aesop.jpg)
<figcaption>Velázquez, Aesop, c. 1638–41, Prado</figcaption>

</div>
</div>

<!--
The English moral is a 19th-century translation (Townsend); the fable (Perry 237) is attributed to Aesop by tradition.
A man buys a donkey on trial. It walks straight to the laziest donkey in the yard, and he returns it.
-->

---

## Importance you inherit

<hr>

<div class="cols">
<div>

* A node's score ∝ the sum of its neighbours' scores.
* $c_i = \dfrac{1}{\lambda} \displaystyle\sum_j A_{ij}\, c_j$

</div>
<div class="fig">

![w:537](figures/frames/eigen-inherit/00.png)

</div>
</div>

<!--
Explain the bullets on this slide; the next 3 slides step the figure, one change each (the grey note says which).
The steps: A's neighbours hand over their scores, and the sum is 2.88 times A's own. Then the leaf C: its one neighbour D holds 0.58 = 2.88 x 0.20, the same 2.88. Every node gives the same factor; that number is lambda.
It is circular: a score defined by scores. The constant lambda keeps the scores from growing without bound.
-->

---

## Importance you inherit

<hr>

<div class="cols">
<div>

- A node's score ∝ the sum of its neighbours' scores.
- $c_i = \dfrac{1}{\lambda} \displaystyle\sum_j A_{ij}\, c_j$

</div>
<div class="fig">

![w:537](figures/frames/eigen-inherit/01.png)

</div>
</div>

<!--
Step 1 of 3: A's neighbours: B, D, F, G.
-->

---

## Importance you inherit

<hr>

<div class="cols">
<div>

- A node's score ∝ the sum of its neighbours' scores.
- $c_i = \dfrac{1}{\lambda} \displaystyle\sum_j A_{ij}\, c_j$

</div>
<div class="fig">

![w:537](figures/frames/eigen-inherit/02.png)

</div>
</div>

<!--
Step 2 of 3: their sum = 2.88 x A's score.
-->

---

## Importance you inherit

<hr>

<div class="cols">
<div>

- A node's score ∝ the sum of its neighbours' scores.
- $c_i = \dfrac{1}{\lambda} \displaystyle\sum_j A_{ij}\, c_j$

</div>
<div class="fig">

![w:537](figures/frames/eigen-inherit/03.png)

</div>
</div>

<!--
Step 3 of 3: same 2.88 at C (0.58 = 2.88 x 0.20): this is lambda.
-->

---

## It is an eigenvector equation

<hr>

<div class="cols">
<div>

* In matrix form: $A\mathbf{c} = \lambda\mathbf{c}$.
* $\mathbf{c}$ is an **eigenvector** of $A$.

</div>
<div class="fig">

![w:537](figures/eigen-equation.png)

</div>
</div>

---

## Seven eigenvectors. Which one?

<hr>

Blue: positive, orange: negative. Which is the centrality?

<div class="fig tall">

![w:1080](figures/eig-all-q.png)

</div>

<div class="cue">

*Take 30 seconds.*

</div>

---

## Seven eigenvectors. Which one?

<hr>

Perron–Frobenius: only the one for λmax is all positive.

<div class="fig tall">

![w:1080](figures/eig-all.png)

</div>

<!--
The Perron–Frobenius theorem, for a nonnegative, irreducible matrix (irreducible = the network is connected): the eigenvector of the largest eigenvalue can be chosen positive everywhere, and no other eigenvector is. A negative score would mean nothing, so this is the only eigenvector that can be a centrality.
-->

---

## Eigenvector centrality

<hr>

<div class="cols">
<div>

* That eigenvector, with its largest entry set to 1, is **eigenvector centrality**.

</div>
<div class="fig">

![w:537](figures/eig-pf.png)

</div>
</div>

<!--
The same seven nodes and the same numbers as on "Importance you inherit".
-->

---

## Which lettered node scores higher?

<hr>

<div class="cols">
<div>

- Eigenvector centrality.

</div>
<div class="fig">

![w:537](figures/q-eig-L.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

## Which lettered node scores higher?

<hr>

<div class="cols">
<div>

- Eigenvector centrality.
- M: fewer neighbours, better ones.

</div>
<div class="fig">

![w:537](figures/q-eig-L-ans.png)

</div>
</div>

<!--
M 0.85, X 0.46. M's three neighbours include two hubs; X's four include three leaves.
-->

---

## Which lettered node scores higher?

<hr>

<div class="cols">
<div>

- Eigenvector centrality.

</div>
<div class="fig">

![w:537](figures/q-eig-R.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

## Which lettered node scores higher?

<hr>

<div class="cols">
<div>

- Eigenvector centrality.
- K beats the hub H.

</div>
<div class="fig">

![w:537](figures/q-eig-R-ans.png)

</div>
</div>

<!--
K 0.85, H 0.62. K sits in the dense corner.
-->

---

## Eigendecomposition

<hr>

$A$ is a sum of rank-1 pieces, one per eigenvalue.

<div class="fig">

![w:1080](figures/decomp-sum.png)
<figcaption>circle: eigenvalue · tall bar: eigenvector · wide bar: its transpose</figcaption>

</div>

<!--
rank 1: every row of u_k u_kᵀ is a multiple of u_kᵀ. lambda_1 = lambda_max is the largest eigenvalue.
-->

---

## The eigenvectors are orthogonal

<hr>

Different eigenvectors multiply to 0.

<div class="fig">

![w:1080](figures/decomp-orth.png)

</div>

<!--
Each eigenvector scaled to length 1: two different ones multiply to 0, one with itself to 1.
-->

---

## Square it

<hr>

$A^2$: every eigenvalue squared, the same vectors.

<div class="fig">

![w:1080](figures/frames/decomp-square/00.png)

</div>

<!--
Explain the bullets on this slide; the next 1 slides step the figure, one change each (the grey note says which).
A squared = sum of lambda_k squared u_k u_kᵀ. Every cross term contains a product of two different eigenvectors, which is 0.
-->

---

## Square it

<hr>

$A^2$: every eigenvalue squared, the same vectors.

<div class="fig">

![w:1080](figures/frames/decomp-square/01.png)

</div>

<!--
Step 1 of 1: the result: each eigenvalue squared.
-->

---

## Keep multiplying

<hr>

$A^t / \lambda_1^t$: every term but the first fades.

<div class="fig">

![w:1080](figures/frames/decomp-power/00.png)

</div>

<!--
Explain the bullets on this slide; the next 3 slides step the figure, one change each (the grey note says which).
A^t counts walks of length t. Divide everything by lambda_1^t: term k shrinks like (lambda_k / lambda_1)^t. The next largest in size is lambda = -2.26, so the error shrinks by a factor 0.78 per step (2.26 / 2.88). After 16 steps it is about 2%. So A^t 1 points along u_1.
-->

---

## Keep multiplying

<hr>

$A^t / \lambda_1^t$: every term but the first fades.

<div class="fig">

![w:1080](figures/frames/decomp-power/01.png)

</div>

<!--
Step 1 of 3: t = 2: the negative term turns positive.
-->

---

## Keep multiplying

<hr>

$A^t / \lambda_1^t$: every term but the first fades.

<div class="fig">

![w:1080](figures/frames/decomp-power/02.png)

</div>

<!--
Step 2 of 3: t = 4: the small terms fade.
-->

---

## Keep multiplying

<hr>

$A^t / \lambda_1^t$: every term but the first fades.

<div class="fig">

![w:1080](figures/frames/decomp-power/03.png)

</div>

<!--
Step 3 of 3: t = 16: only the first is left (2%).
-->

---

## Power iteration

<hr>

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
Press the ▶ button once per step. Each press applies x <- A x once and divides by the largest entry; the disc shade and the printed number are the entry.

Step 0: every node holds 1. Step 1: every node now holds its degree (A 4, D 3, F 3, G 3, B 2, E 2, C 1), divided by 4, so A is 1.00 and C is 0.25. So degree is the first guess, and each further step looks one step farther. Step 2: B has caught up with D (both 0.64) and F, G pull ahead of both (0.82). Step 3: G passes F; B and D are still exactly tied (0.625). Step 4: B passes D (0.63 against 0.59) and stays ahead; the order is now fixed. B has two neighbours and D has three, but B's two neighbours (A and G) are the strongest nodes. D's third neighbour is the leaf C. From step 4 the order A G F B D E C no longer changes; steps 5 to 8 only move the second decimal. Step 30 (the last dot): nothing moves; these seven numbers are the eigenvector of the largest eigenvalue, 2.884, with its largest entry set to 1.
-->

---

## Where does eigenvector centrality break?

<hr>

<div class="cols">
<div>

- Four 4-cliques in a ring.
- Add one node to one clique. Where does the score go?

</div>
<div class="fig tall">

![w:537](figures/ring-4444.png)

</div>
</div>

<div class="cue">

*Take 30 seconds.*

</div>

<!--
Ask: one clique of 5, three of 4. Who gets the score? Most will say "a bit more for the big one".
-->

---

## Localization

<hr>

<div class="cols">
<div>

* Grow one clique to K nodes, one node at a time.
* The densest part takes almost all the score.

</div>
<div class="fig tall">

![w:537](figures/frames/ring-local/00.png)

</div>
</div>

<!--
Explain the bullets on this slide; the next 4 slides step the figure, one change each (the grey note says which).
One extra node, and 68% of the total score moves into that clique; with two, 85%; at K = 8, 94%. The other three cliques, identical to each other, score almost nothing.
-->

---

## Localization

<hr>

<div class="cols">
<div>

- Grow one clique to K nodes, one node at a time.
- The densest part takes almost all the score.

</div>
<div class="fig tall">

![w:537](figures/frames/ring-local/01.png)

</div>
</div>

<!--
Step 1 of 4: K = 4: equal cliques, equal shares (25%).
-->

---

## Localization

<hr>

<div class="cols">
<div>

- Grow one clique to K nodes, one node at a time.
- The densest part takes almost all the score.

</div>
<div class="fig tall">

![w:537](figures/frames/ring-local/02.png)

</div>
</div>

<!--
Step 2 of 4: K = 5: one more node, 68%.
-->

---

## Localization

<hr>

<div class="cols">
<div>

- Grow one clique to K nodes, one node at a time.
- The densest part takes almost all the score.

</div>
<div class="fig tall">

![w:537](figures/frames/ring-local/03.png)

</div>
</div>

<!--
Step 3 of 4: K = 6: 85%.
-->

---

## Localization

<hr>

<div class="cols">
<div>

- Grow one clique to K nodes, one node at a time.
- The densest part takes almost all the score.

</div>
<div class="fig tall">

![w:537](figures/frames/ring-local/04.png)

</div>
</div>

<!--
Step 4 of 4: K = 8: 94%.
-->

---

## New York: eigenvector

<hr>

<div class="cols">
<div>

* 96% of the score lies within 60 km of Manhattan.
* 31% of the interchanges lie there.

</div>
<div class="fig">

![w:537](figures/ny-eigenvector.png)

</div>
</div>

<!--
The real network localizes: the densest cluster, Long Island and the city, takes 96% of the score. The top node is I-495 at Hempstead, Long Island. Upstate interchanges all score close to zero.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 05</span></div>

## Everyone gets a baseline

Katz centrality

---

## Katz centrality

<hr>

<div class="cols">
<div>

* Everyone gets $\beta$ for free, plus $\alpha$ × the neighbours' scores.
* $c_i = \beta + \alpha \sum_j A_{ij}\, c_j$
* $\mathbf{c} = \beta\, (I - \alpha A)^{-1} \mathbf{1}$

</div>
<div class="fig">

![w:537](figures/katz-floor.png)

</div>
</div>

<!--
Every node gets beta for free, so no node can be driven to zero. Move the sum to the left: (I - alpha A) c = beta 1, and invert. I: the identity matrix; 1: all ones.
-->

---

## What is that inverse?

<hr>

<div class="cols">
<div>

- $\mathbf{c} = \beta\, (I - \alpha A)^{-1} \mathbf{1}$
- $(I - \alpha A)^{-1} = \;?$
- Hint: $\dfrac{1}{1-x} = 1 + x + x^2 + \cdots$ for $|x| < 1$.

</div>
<div class="fig">

![w:537](figures/katz-floor.png)

</div>
</div>

<div class="cue">

*Take 30 seconds.*

</div>

---

## The same series for matrices

<hr>

<div class="cols">
<div>

* $(I-\alpha A)^{-1} = \displaystyle\sum_{k \ge 0} \alpha^k A^k$
* $A^k$ counts the walks of length $k$
* Katz counts walks, discounted by length

</div>
<div class="fig tall">

![w:537](figures/frames/walks-discount/00.png)

</div>
</div>

<!--
Explain the bullets on this slide; the next 3 slides step the figure, one change each (the grey note says which).
Multiply both sides by (I - alpha A) to check. The series converges only if alpha is small enough: the dial on the next slide.
-->

---

## The same series for matrices

<hr>

<div class="cols">
<div>

- $(I-\alpha A)^{-1} = \displaystyle\sum_{k \ge 0} \alpha^k A^k$
- $A^k$ counts the walks of length $k$
- Katz counts walks, discounted by length

</div>
<div class="fig tall">

![w:537](figures/frames/walks-discount/01.png)

</div>
</div>

<!--
Step 1 of 3: 2 walks of length 2, alpha^2 each.
-->

---

## The same series for matrices

<hr>

<div class="cols">
<div>

- $(I-\alpha A)^{-1} = \displaystyle\sum_{k \ge 0} \alpha^k A^k$
- $A^k$ counts the walks of length $k$
- Katz counts walks, discounted by length

</div>
<div class="fig tall">

![w:537](figures/frames/walks-discount/02.png)

</div>
</div>

<!--
Step 2 of 3: 1 walk of length 3: alpha^3.
-->

---

## The same series for matrices

<hr>

<div class="cols">
<div>

- $(I-\alpha A)^{-1} = \displaystyle\sum_{k \ge 0} \alpha^k A^k$
- $A^k$ counts the walks of length $k$
- Katz counts walks, discounted by length

</div>
<div class="fig tall">

![w:537](figures/frames/walks-discount/03.png)

</div>
</div>

<!--
Step 3 of 3: every length, discounted.
-->

---

## Turn the dial

<hr>

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

## Why 1/λ<sub>max</sub>?

<hr>

<div class="formula">

$$(I - \alpha A)^{-1} = \sum_k \frac{1}{1 - \alpha \lambda_k}\, \mathbf{u}_k \mathbf{u}_k^\top$$

</div>

<div class="fig">

![w:1080](figures/frames/katz-why/00.png)

</div>

<!--
Explain the bullets on this slide; the next 2 slides step the figure, one change each (the grey note says which).
The 7-node network of the eigenvector slides (lambda_max = 2.884). Circle: the weight of term k, 1/(1 - alpha lambda_k). Each eigenvalue of A becomes 1/(1 - alpha lambda_k). As alpha approaches 1/lambda_1, the first term grows without bound and swamps the rest: Katz becomes eigenvector centrality. Past it, the first coefficient is negative and the scores mean nothing.
-->

---

## Why 1/λ<sub>max</sub>?

<hr>

<div class="formula">

$$(I - \alpha A)^{-1} = \sum_k \frac{1}{1 - \alpha \lambda_k}\, \mathbf{u}_k \mathbf{u}_k^\top$$

</div>

<div class="fig">

![w:1080](figures/frames/katz-why/01.png)

</div>

<!--
Step 1 of 2: alpha near 1/lambda_max: the first term dominates.
-->

---

## Why 1/λ<sub>max</sub>?

<hr>

<div class="formula">

$$(I - \alpha A)^{-1} = \sum_k \frac{1}{1 - \alpha \lambda_k}\, \mathbf{u}_k \mathbf{u}_k^\top$$

</div>

<div class="fig">

![w:1080](figures/frames/katz-why/02.png)

</div>

<!--
Step 2 of 2: past 1/lambda_max: the first weight is negative.
-->

---

## Which lettered node scores higher now?

<hr>

<div class="cols">
<div>

- Katz, $\alpha = 0.5/\lambda_{\max}$.
- The network from the eigenvector quiz.

</div>
<div class="fig">

![w:537](figures/q-eig-L.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

## Which lettered node scores higher now?

<hr>

<div class="cols">
<div>

- Katz, $\alpha = 0.5/\lambda_{\max}$.
- The network from the eigenvector quiz.
- M again, as the eigenvector said.

</div>
<div class="fig">

![w:537](figures/q-katz-L-ans.png)

</div>
</div>

<!--
M 0.87, X 0.81 (largest = 1).
-->

---

## Which lettered node scores higher now?

<hr>

<div class="cols">
<div>

- Katz, $\alpha = 0.5/\lambda_{\max}$.
- The network from the eigenvector quiz.

</div>
<div class="fig">

![w:537](figures/q-eig-R.png)

</div>
</div>

<div class="cue">

*Take a minute.*

</div>

---

## Which lettered node scores higher now?

<hr>

<div class="cols">
<div>

- Katz, $\alpha = 0.5/\lambda_{\max}$.
- The network from the eigenvector quiz.
- H now: short walks still weigh a lot.

</div>
<div class="fig">

![w:537](figures/q-katz-R-ans.png)

</div>
</div>

<!--
H 1.00, K 0.81. At alpha = 0.5/lambda_max short walks still weigh a lot, so H's six neighbours count; as alpha approaches 1/lambda_max, Katz turns into the eigenvector and K passes H (between 0.8 and 0.9 of 1/lambda_max).
-->

---

## The walk row

<hr>

<div class="fig tall">

![w:1080](figures/grid-row2.png)

</div>

<!--
Degree and eigenvector centrality are the two ends of Katz: alpha near 0 ranks by degree, alpha near 1/lambda_max by the eigenvector.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Five</span><span class="count">05 / 05</span></div>

## The Web has direction

A road runs both ways. A link does not.

---

## Hubs and authorities

<hr>

<div class="cols">
<div>

* <strong class="cool">Authority</strong> $a_i = \sum_j A_{ji}\, h_j$: pointed to by good hubs.
* **Hub** $h_i = \sum_j A_{ij}\, a_j$: points to good authorities.
* On a road map, HITS is eigenvector centrality.

</div>
<div class="fig">

![w:537](figures/hits-graph.png)
<figcaption>A_ij = 1: page i links to page j</figcaption>

</div>
</div>

<!--
HITS (Kleinberg, 1999). Two scores per page. A links out three times and is the best hub; E is linked to three times and is the best authority.
On a road map A is symmetric, so A^T A = A^2, whose leading eigenvector is that of A (when the network is not bipartite: here 2.88 > 2.26).
-->

---

## The same idea, six times

<hr>

A node's score is built from its neighbours' scores.

<div class="fig">

![w:1080](figures/genealogy.png)

</div>

<!--
Landau (1895) ranked chess players by the scores of the players they beat. Seeley (1949) ranked children by who chose them. Katz (1953): status with a baseline. Hubbell (1965): influence in a group. Bonacich (1972): eigenvector centrality. Brin and Page (1998): PageRank, which comes next.
-->

---

## Divide the vote

<hr>

<div class="cols">
<div>

* A page splits its score among its links out.
* $c_i = \sum_j A_{ji}\, \dfrac{c_j}{d^{\text{out}}_j}$
* C: three links in. E: one. Which ranks higher?

</div>
<div class="fig">

![w:537](figures/pr-split.png)

</div>
</div>

<div class="cue">

*Take 30 seconds.*

</div>

<!--
d_out j: the number of links out of j. A gives a third to each of B, C, D.
-->

---

## Divide the vote

<hr>

<div class="cols">
<div>

- A, C and E tie at 3/11.
- E's one link comes from C, which passes on everything.

</div>
<div class="fig">

![w:537](figures/pr-split-answer.png)

</div>
</div>

<!--
A, C and E: 3/11 each. B and D: 1/11.
-->

---

## A dead end

<hr>

<div class="cols">
<div>

* E loses its only link out.
* Its score has nowhere to go: the total drains to zero.

</div>
<div class="fig">

![w:537](figures/frames/pr-leak/00.png)

</div>
</div>

<!--
Explain the bullets on this slide; the next 3 slides step the figure, one change each (the grey note says which).
The total goes 1, 0.8, 0.6, ... 0.
-->

---

## A dead end

<hr>

<div class="cols">
<div>

- E loses its only link out.
- Its score has nowhere to go: the total drains to zero.

</div>
<div class="fig">

![w:537](figures/frames/pr-leak/01.png)

</div>
</div>

<!--
Step 1 of 3: E's only link out is gone.
-->

---

## A dead end

<hr>

<div class="cols">
<div>

- E loses its only link out.
- Its score has nowhere to go: the total drains to zero.

</div>
<div class="fig">

![w:537](figures/frames/pr-leak/02.png)

</div>
</div>

<!--
Step 2 of 3: score leaks out at E: total 0.60.
-->

---

## A dead end

<hr>

<div class="cols">
<div>

- E loses its only link out.
- Its score has nowhere to go: the total drains to zero.

</div>
<div class="fig">

![w:537](figures/frames/pr-leak/03.png)

</div>
</div>

<!--
Step 3 of 3: nothing left: total 0.00.
-->

---

## Teleportation

<hr>

<div class="cols">
<div>

* With probability $r = 0.15$, jump to a random page.
* A dead end links to every page.
* $c_i = (1-r) \sum_j A_{ji}\, \dfrac{c_j}{d^{\text{out}}_j} + \dfrac{r}{N}$
* This is **PageRank**.

</div>
<div class="fig">

![w:537](figures/pr-teleport.png)

</div>
</div>

<!--
Brin and Page, 1998. A dead end hands its score to the jump. The jump also makes the answer unique. On the dead-end graph: E 0.359, C 0.316, B and D 0.117, A 0.091.
-->

---

## Personalized PageRank

<hr>

<div class="cols">
<div>

* Jump back to A only.
* Score: how often a walker that keeps restarting at A visits each page.

</div>
<div class="fig">

![w:537](figures/ppr.png)

</div>
</div>

<!--
Replace r/N by r on A and 0 elsewhere. "More like this" on a website: teleport to the page you are on.
-->

---

## New York: five measures, five places

<hr>

<div class="cols">
<div>

- Each measure's winner, on one map.
- No two agree.

</div>
<div class="fig">

![w:537](figures/ny-five.png)

</div>
</div>

<!--
Closeness: NY 17 at Middletown. Harmonic: I-95 in the Bronx. Eccentricity: NY 17 east of Binghamton. Betweenness: NY 17 at Monticello. Eigenvector: I-495 on Long Island.
-->

---

## Two choices, every centrality

<hr>

<div class="fig tall">

![w:1080](figures/grid-final.png)

</div>

---

<!-- _class: mid -->

## Quiz

<hr>

Draw a network in which degree, closeness, eccentricity and betweenness each rank a different node first.

<div class="cue">

*Bring it to the next class.*

</div>

<!--
Deliberately the day-1 measures: the shortest-path row. A student who finishes can add eigenvector centrality as a fifth.
-->

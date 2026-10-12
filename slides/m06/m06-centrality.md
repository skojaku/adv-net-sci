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

<!--
Day 1 (10/20): slides 1 to 34, measured by shortest paths. Day 2 (10/22): slides 35 to 70, measured by walks.
The pen-and-paper sheet has already been done, so the room has met degree, average distance, "indispensable" and passing scores around. Name things; do not re-derive what is in their hands.
-->

---

## 20 BC, the Forum Romanum

<hr>

<div class="photos">

![](figures/photos/caesar.jpg)
![](figures/photos/augustus.jpg)
![](figures/photos/milliarium.jpg)

</div>

<div class="photo-credit">Julius Caesar (photo Marie-Lan Taÿ Pamart, CC BY 4.0) · Augustus of Prima Porta (photo Justin Benttinen, CC BY-SA 4.0) · remains labelled Milliarium Aureum (photo Krzysztof Golik, CC BY-SA 4.0) · Wikimedia Commons</div>

* Augustus, Caesar's adopted heir, set up the **Golden Milestone** in 20 BC.
* A gilded column in the Forum, by the Temple of Saturn.
* Its text is lost. It is said to have listed cities and their distances in miles.
* Plutarch: every road of Italy ended at it.

<!--
Caesar had been curator of the Via Appia (Plutarch, Caesar 5) and named Octavian his heir in his will, 44 BC. As Augustus, he took charge of the roads around Rome and set up the column in 20 BC (Cassius Dio 54.8.4).
Plutarch (Galba 24) calls it a gilded column at which all the roads of Italy end. Pliny (NH 3.66) puts it at the head of the Forum.
What was written on it is not recorded by any ancient source. "The names of the cities and their distances" is a modern reconstruction, so say "said to". Distances along the roads were counted from the gates of the city wall, not from this column.
The fragments in the photo are the ones the Forum labels as the milestone; whether they belong to it is doubtful.
"All roads lead to Rome" is medieval: Alain de Lille, about 1175.
-->

---

## Twelve cities of the empire

<hr>

<div class="cols">
<div>

Roads and sea lanes joined these twelve cities.

</div>
<div class="fig">

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

Which city is the most important?

<div class="fig tall">

![w:1080](figures/roma-to-graph.gif)

</div>

<!--
The coastline goes, the roads become straight lines, the cities move to where their names fit. What is left is a network: twelve nodes, the roads between them.
Take answers. The room will give at least two kinds of reason (many roads; close to everything). Both are right. That is the module.
-->

---

## Today's question, at home

<hr>

<div class="cols">
<div>

New York State highways: 289 interchanges.

Which of these eight cities do the most cross-state trips pass through?

</div>
<div class="fig">

![w:537](figures/ny-overview.png)
<figcaption>highway data © OpenStreetMap contributors</figcaption>

</div>
</div>

<!--
Do not answer. It comes back at the end of today (betweenness).
The network: OpenStreetMap motorways and trunk roads in New York State, one node per interchange (junctions within 3.5 km merged), 289 nodes and 433 road segments. Distance is km of road.
Take a vote: Buffalo, Rochester, Syracuse, Utica, Albany, NYC, Binghamton, Watertown.
-->

---

## Degree centrality

<hr>

**Degree**: $d_i = \sum_j A_{ij}$, where $A_{ij} = 1$ if a road joins $i$ and $j$.

<div class="fig tall">

![w:1080](figures/roma-degree.png)
<figcaption>darker: more roads; Roma has the most, 5</figcaption>

</div>

<!--
The sheet's first question. Name it and move on. Roma has the most roads.
-->

---

## New York: degree

<hr>

<div class="cols">
<div>

201 interchanges have degree 3, and 57 have degree 4.

Degree cannot tell them apart.

</div>
<div class="fig">

![w:537](figures/ny-degree.png)

</div>
</div>

<!--
On a road map almost every junction joins three or four roads. A measure that only looks one step out sees almost nothing.
-->

---

<!-- _class: mid -->

## How far is u from v?

<hr>

<div class="cols">
<div>

The network from Module 01.

</div>
<div class="fig">

![w:537](figures/w5-blank.png)

</div>
</div>

<!--
Take answers. Someone says 2. Ask: in how many ways can you get there in 3 steps? In 4?
-->

---

## Two ways to count

<hr>

<div class="cols">
<div>

* **Shortest path**: the fewest steps. One number: 2.
* **Walk**: any route, revisits allowed. A count for each length: 2, 1, 11, …

</div>
<div class="fig">

![w:537](figures/w5-walks.gif)

</div>
</div>

<!--
The walk counts are the entries of A, A squared, A cubed, ... from Module 01. Walks of length 2: 2; length 3: 1; length 4: 11.
-->

---

## Two choices make a centrality

<hr>

Which routes count, and how do they become one number?

<div class="fig">

![w:1080](figures/grid-empty.png)

</div>

<!--
Every measure today is one choice on each axis. We fill this in as we go.
Degree sits at the corner: a walk of length 1 is also a shortest path of length 1.
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

<div class="formula">

$$c_i = \frac{N-1}{\sum_{j \ne i} \ell_{ij}}$$

</div>

$\ell_{ij}$: the length of a shortest path from $i$ to $j$. $N$: the number of nodes.

</div>
<div class="fig">

![w:537](figures/closeness-def.gif)

</div>
</div>

<!--
Add up the distances to every other node, then invert: a small total gives a large score. The animation does it for A (sum 15), then shows every node's sum; D has the smallest, 10.
-->

---

## Why N − 1?

<hr>

<div class="cols">
<div>

Best case: every other node is one step away.

Then the score is exactly 1.

</div>
<div class="fig">

![w:537](figures/star-closeness.png)

</div>
</div>

---

## Which node is closest to everything?

<hr>

The smallest sum of distances wins. Left and right are separate networks.

<div class="fig">

![w:1080](figures/quiz-close.png)

</div>

<div class="cue">

*Take a minute. Pick one on each side.*

</div>

---

## Answer

<hr>

The sum of distances, beside each candidate.

<div class="fig">

![w:1080](figures/quiz-close-answer.png)
<figcaption>in both networks, the node with the most neighbours is not the closest</figcaption>

</div>

<!--
Left: F has degree 2 and a sum of 19. The hub E (degree 5) and G both have 20. Moving from E to F, five nodes get one step farther (A, B, C, D, E) and six get one step closer.
Right: P (sum 16) beats N (sum 18). N's triangle looks central, but P's long arms hold more nodes.
-->

---

## New York: closeness

<hr>

<div class="cols">
<div>

* Distance: km of highway.
* Winner: NY 17 near Middletown, in the Hudson Valley.
* 31% of the interchanges lie within 60 km of Manhattan.

</div>
<div class="fig">

![w:537](figures/ny-closeness.png)
<figcaption>darker, larger dot: closer to everything</figcaption>

</div>
</div>

<!--
Closeness is pulled toward where the nodes are. 91 of 289 interchanges are within 60 km of Manhattan, so the best average sits just north of the city, not in the middle of the state.
-->

---

<!-- _class: mid -->

## What if one road closes?

<hr>

<div class="cols">
<div>

Close the road between E and F.

What happens to closeness?

</div>
<div class="fig">

![w:537](figures/cut-blank.png)

</div>
</div>

<div class="cue">

*Take 30 seconds.*

</div>

---

## Every score drops to zero

<hr>

<div class="cols">
<div>

Some distances are now $\infty$.

Every sum is $\infty$, so every closeness is 0.

</div>
<div class="fig">

![w:537](figures/cut-closeness.png)

</div>
</div>

<!--
Not just the nodes near the cut: all eleven. Closeness cannot rank a disconnected network at all.
-->

---

## Take the reciprocal first

<hr>

<div class="cols">
<div>

<div class="formula">

$$h_i = \sum_{j \ne i} \frac{1}{\ell_{ij}}$$

</div>

**Harmonic centrality**.

An unreachable node adds $1/\infty = 0$.

</div>
<div class="fig">

![w:537](figures/harmonic-def.gif)

</div>
</div>

<!--
Invert each distance, then add. An unreachable node adds 0 instead of making the whole sum infinite. From G: four nodes at distance 1, K at 2, the other piece unreachable: 4 + 1/2 = 9/2.
-->

---

## Which node has the highest harmonic centrality?

<hr>

Left: the closeness network, with the road E–F open again. Right: two pieces.

<div class="fig">

![w:1080](figures/quiz-harm.png)

</div>

<div class="cue">

*Does the left winner change?*

</div>

---

## Answer

<hr>

Harmonic centrality, beside each candidate.

<div class="fig">

![w:1080](figures/quiz-harm-answer.png)
<figcaption>on the left, closeness and harmonic pick different nodes</figcaption>

</div>

<!--
Left: E 27/4 beats G 19/3 and F 35/6. With 1/distance, the four leaves at distance 1 count fully for E; with the sum of distances, they barely helped.
Right: the star's centre, 4, beats the middle of the path, 11/3. The bigger piece is not the better one.
-->

---

<!-- _class: mid -->

## Would you site a fire station on the average?

<hr>

*Take 30 seconds.*

---

## Eccentricity

<hr>

<div class="cols">
<div>

<div class="formula">

$$e_i = \max_{j} \ell_{ij}$$

</div>

A fire station must reach its farthest house. **Eccentricity**: the distance to the farthest node; its centrality is $1/e_i$.

</div>
<div class="fig">

![w:537](figures/ecc-def.gif)

</div>
</div>

---

## Which node has the smallest eccentricity?

<hr>

The best fire station: the smallest worst case.

<div class="fig">

![w:1080](figures/quiz-ecc.png)

</div>

---

## Answer

<hr>

Eccentricity, beside every node.

<div class="fig">

![w:1080](figures/quiz-ecc-answer.png)
<figcaption>in both networks, the best average is not the best worst case</figcaption>

</div>

<!--
Left: E wins closeness (sum 10) but its worst case is 3, the end of the tail. F has worst case 2.
Right: K wins closeness (11), worst case 3. L, with degree 2, has worst case 2.
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
<figcaption>darker, larger dot: a shorter worst-case drive</figcaption>

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

Send a letter between every pair of nodes, along a shortest path.

Count the letters each node carries.

</div>
<div class="fig">

![w:537](figures/btw-def.gif)

</div>
</div>

<!--
D carries 9: every letter between the left triangle and the right triangle. C and E carry 8 each.
-->

---

## Betweenness centrality

<hr>

<div class="formula">

$$b_i = \sum_{s < t} \frac{\sigma_{st}(i)}{\sigma_{st}}$$

</div>

$\sigma_{st}$: the number of shortest paths from $s$ to $t$; $\sigma_{st}(i)$: those through $i$.

<div class="fig">

![w:1080](figures/sigma-answer.png)
<figcaption>the pair S, D has two shortest paths, so A and B each carry half</figcaption>

</div>

<!--
sigma_st: the number of shortest paths from s to t. sigma_st(i): how many of them pass through i. From S to D there are two shortest paths, so A and B each carry half of that pair, and T carries all of it.
-->

---

## Which node carries the most?

<hr>

Count the shortest paths through each node; a tie splits the count.

<div class="fig">

![w:1080](figures/quiz-btw.png)

</div>

---

## Answer

<hr>

Betweenness, beside each candidate.

<div class="fig">

![w:1080](figures/quiz-btw-answer.png)
<figcaption>the bridge F carries every left-right pair, and each hub carries more</figcaption>

</div>

<!--
Left: F carries 5 x 5 = 25 pairs. E carries the 6 pairs among its leaves plus 4 x 6 pairs between a leaf and the rest: 30. Same for G.
Right: O carries 9 pairs whole, and half of the pair P, Q (two shortest paths: through O and through R): 19/2. M carries 9.
-->

---

## New York: betweenness

<hr>

<div class="cols">
<div>

* Top interchange: NY 17 at Monticello.
* Of the eight cities, Binghamton is first: 3.5 times Syracuse.
* Four of the top five interchanges are on NY 17.

</div>
<div class="fig">

![w:537](figures/ny-betweenness.png)
<figcaption>darker, larger dot: more shortest paths pass through</figcaption>

</div>
</div>

<!--
The answer to this morning's question. Four of the top five interchanges in the whole state are on NY 17 between Binghamton and Middletown: the corridor between the NYC cluster and upstate. Binghamton is where that corridor meets I-81 and I-88.
-->

---

## The shortest-path row

<hr>

<div class="fig">

![w:1080](figures/grid-row1.png)
<figcaption>four ways to turn shortest paths into one number</figcaption>

</div>

---

<!-- _class: mid -->

## A question to sleep on

<hr>

<div class="formula">

Is a city important because its neighbours are important?

</div>

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 05</span></div>

## Known by the company you keep

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

"A man is known by the company he keeps."

</div>

The moral of *The Ass and His Purchaser* (Perry 237).

</div>
<div class="fig">

![w:537](figures/photos/aesop.jpg)
<figcaption>Diego Velázquez, Aesop, c. 1638–41, Museo del Prado</figcaption>

</div>
</div>

<!--
The English moral is a 19th-century translation (Townsend); the fable is attributed to Aesop by tradition.
A man buys a donkey on trial. It walks straight to the laziest donkey in the yard, and he returns it.
-->

---

## Importance you inherit

<hr>

<div class="cols">
<div>

<div class="formula">

$$c_i = \frac{1}{\lambda} \sum_j A_{ij}\, c_j$$

</div>

A node's score is the sum of its neighbours' scores, divided by a constant $\lambda$.

</div>
<div class="fig">

![w:537](figures/eigen-inherit.gif)

</div>
</div>

<!--
It is circular: a score defined by scores. The constant lambda keeps the scores from growing without bound. Next slide: this is an eigenvector equation.
-->

---

## It is an eigenvector equation

<hr>

<div class="fig">

![w:1080](figures/eigen-equation.png)

</div>

---

<!-- _class: mid -->

## Seven eigenvectors. Which one?

<hr>

This symmetric 7 × 7 matrix has seven eigenvectors. Which one is the centrality?

---

## Perron and Frobenius

<hr>

In a connected network, only the eigenvector of the largest eigenvalue is positive everywhere.

<div class="fig tall">

![w:1080](figures/eig-all.png)
<figcaption>blue: positive entry, gold: negative; only one is blue everywhere</figcaption>

</div>

---

## Eigenvector centrality

<hr>

<div class="cols">
<div>

That eigenvector, with its largest entry set to 1, is **eigenvector centrality**.

</div>
<div class="fig">

![w:537](figures/eig-pf.png)

</div>
</div>

<!--
The Perron–Frobenius theorem, for a nonnegative, irreducible matrix (irreducible = the network is connected): the eigenvector of the largest eigenvalue can be chosen positive everywhere, and no other eigenvector is. A negative score would mean nothing, so this is the only eigenvector that can be a centrality.
-->

---

## Which marked node scores higher?

<hr>

Eigenvector centrality. In each network, compare the two lettered nodes.

<div class="fig">

![w:1080](figures/quiz-eig.png)

</div>

<div class="cue">

*Take a minute.*

</div>

---

## Answer

<hr>

Eigenvector centrality, largest = 1.

<div class="fig">

![w:1080](figures/quiz-eig-answer.png)
<figcaption>in both networks, the node with fewer neighbours scores higher</figcaption>

</div>

<!--
Left: M 0.85, X 0.46. M's three neighbours include two hubs; X's four include three leaves. Right: K 0.85, H 0.62.
-->

---

## Eigendecomposition

<hr>

A symmetric matrix is a sum of rank-1 matrices. $\lambda_1 = \lambda_{\max}$ is the largest eigenvalue.

<div class="fig">

![w:1080](figures/decomp-sum.gif)
<figcaption>circle: an eigenvalue; tall bar: its eigenvector; wide bar: the same vector, transposed</figcaption>

</div>

<!--
rank 1: every row of u_k u_kᵀ is a multiple of u_kᵀ.
-->

---

## The eigenvectors are orthogonal

<hr>

<div class="fig">

![w:1080](figures/decomp-orth.png)
<figcaption>each eigenvector scaled to length 1: two different ones multiply to 0, one with itself to 1</figcaption>

</div>

---

## Square it

<hr>

$A^2 = \sum_k \lambda_k^2\, \mathbf{u}_k \mathbf{u}_k^\top$: squaring squares every eigenvalue.

<div class="fig">

![w:1080](figures/decomp-square.gif)
<figcaption>every cross term contains a product of two different eigenvectors, which is 0</figcaption>

</div>

---

## Keep multiplying

<hr>

$A^t$ counts walks of length $t$. Divided by $\lambda_1^t$, every term but the first fades, so $A^t \mathbf{1}$ points along $\mathbf{u}_1$.

<div class="fig">

![w:1080](figures/decomp-power.gif)

</div>

<!--
Divide everything by lambda_1^t: term k shrinks like (lambda_k / lambda_1)^t. The next largest in size is lambda = -2.26, so the error shrinks by a factor 0.78 per step (2.26 / 2.88). After 16 steps it is about 2%.
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
Press the right arrow once per step. Each press applies x <- A x once and divides by the largest entry; the disc shade and the printed number are the entry.

Step 0: every node holds 1. Step 1: every node now holds its degree (A 4, D 3, F 3, G 3, B 2, E 2, C 1), divided by 4, so A is 1.00 and C is 0.25. That is the next slide's point, so do not dwell. Step 2: B has caught up with D (both 0.64) and F, G pull ahead of both (0.82). Step 3: G passes F; B and D are still exactly tied (0.625). Step 4: B passes D (0.63 against 0.59) and stays ahead. B has two neighbours and D has three, but B's two neighbours (A and G) are the strongest nodes. D's third neighbour is the leaf C. Step 5: the order A G F B D E C no longer changes. Steps 6 to 8: only the second decimal still moves, D most; each step moves it a little less. Step 30 (the last dot): nothing moves; these seven numbers are the eigenvector of the largest eigenvalue, 2.884, with its largest entry set to 1.

Ask before step 3: which of B and D will end up higher? Most of the room says D (three neighbours).
-->

---

<!-- _class: mid -->

## Where does eigenvector centrality break?

<hr>

<div class="cols">
<div>

Four cliques of four, in a ring. Add one node to one clique. Where does the score go?

</div>
<div class="fig">

![w:537](figures/ring-4444.png)

</div>
</div>

<div class="cue">

*Take 30 seconds.*

</div>

---

## Localization

<hr>

<div class="fig">

![w:1080](figures/ring-local.gif)
<figcaption>share of the total score inside the growing clique</figcaption>

</div>

<!--
One extra node, and 68% of the total score moves into that clique; with two, 85%; at K = 8, 94%. The other three cliques, identical to each other, score almost nothing. The eigenvector concentrates on the densest part of the network.
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
<figcaption>darker, larger dot: higher score; dashed circle: 60 km</figcaption>

</div>
</div>

<!--
The real network localizes: the densest cluster, Long Island and the city, takes 96% of the score. Upstate interchanges all score close to zero.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 05</span></div>

## Everyone gets a baseline

Katz centrality

---

## Give everybody a baseline

<hr>

<div class="cols">
<div>

<div class="formula">

$$c_i = \beta + \alpha \sum_j A_{ij}\, c_j$$

$$\mathbf{c} = \beta\, (I - \alpha A)^{-1} \mathbf{1}$$

</div>

**Katz centrality**: $\beta$ for free, plus $\alpha$ times each neighbour's score.

</div>
<div class="fig">

![w:537](figures/katz-floor.png)

</div>
</div>

<!--
Every node gets beta for free, so no node can be driven to zero. Move the sum to the left: (I - alpha A) c = beta 1, and invert.
-->

---

<!-- _class: mid -->

## What is that inverse?

<hr>

<div class="formula">

$$(I - \alpha A)^{-1} = \;?$$

$$\frac{1}{1-x} = 1 + x + x^2 + \cdots \quad \text{for } |x| < 1$$

</div>

---

## The same series for matrices

<hr>

<div class="cols">
<div>

<div class="formula">

$$(I - \alpha A)^{-1} = I + \alpha A + \alpha^2 A^2 + \cdots$$

</div>

$A^k$ counts walks of length $k$. So Katz counts walks, discounted by length.

</div>
<div class="fig">

![w:537](figures/walks-discount.gif)

</div>
</div>

<!--
Multiply both sides by (I - alpha A) to check. The series converges only if alpha is small enough: next slide.
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

First click shows alpha = 0: only the baseline counts, every node scores 1, and the big clique holds 6 of 18 = 33% of the total. The second click puts the dial at 0.5 / lambda_max; drag it. The red tick is 1/lambda_max, with lambda_max = 5.084 for this graph. As alpha rises the big clique's share climbs: 40% at 0.5, 63% at 0.9, 81% at 0.99. Walks of every length count, discounted by alpha per step, and the big clique has the most walks. At the tick the series 1 + alpha A + alpha^2 A^2 + ... stops converging and the scores blow up. Past the tick the formula still returns numbers, but many are negative (gold) and they mean nothing. Ask: what did alpha = 0 give, and what does the dial look like as alpha goes to 1/lambda_max? It approaches the eigenvector, which is the previous slides' localization.
-->

---

## Why 1/λ<sub>max</sub>?

<hr>

<div class="formula">

$$(I - \alpha A)^{-1} = \sum_k \frac{1}{1 - \alpha \lambda_k}\, \mathbf{u}_k \mathbf{u}_k^\top$$

</div>

<div class="fig">

![w:1080](figures/katz-why.gif)
<figcaption>circle: the weight of term k, 1 / (1 - alpha lambda_k)</figcaption>

</div>

<!--
Here lambda_1 = lambda_max, the largest eigenvalue. Each eigenvalue of A becomes 1/(1 - alpha lambda_k). As alpha approaches 1/lambda_1, the first term grows without bound and swamps the rest: Katz becomes eigenvector centrality. Past it, the first coefficient is negative and the scores mean nothing.
-->

---

## The walk row

<hr>

<div class="fig">

![w:1080](figures/grid-row2.png)
<figcaption>degree and eigenvector centrality are the two ends of Katz: alpha near 0 ranks by degree, alpha near 1 / lambda_max by the eigenvector</figcaption>

</div>

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

<div class="formula">

$$a_i = \sum_j A_{ji}\, h_j$$

$$h_i = \sum_j A_{ij}\, a_j$$

$$A_{ij} = 1 \;\text{if page } i \text{ links to page } j$$

</div>

**HITS** (Kleinberg, 1999): an **authority** is pointed to by good hubs; a **hub** points to good authorities.

</div>
<div class="fig">

![w:537](figures/hits-graph.png)

</div>
</div>

<!--
HITS (Kleinberg, 1999). Two scores per page. A links out three times and is the best hub; E is linked to three times and is the best authority.
-->

---

## On a road map, HITS is eigenvector centrality

<hr>

<div class="cols">
<div>

<div class="formula">

$$\mathbf{a} \propto A^\top A\, \mathbf{a}$$

</div>

If $A$ is symmetric, $A^\top A = A^2$, whose leading eigenvector is that of $A$.

</div>
<div class="fig">

![w:537](figures/eig-centrality.png)

</div>
</div>

<!--
This holds when the network is not bipartite (lambda_max > |lambda_min|; here 2.88 > 2.26).
-->

---

## The same idea, six times

<hr>

<div class="fig">

![w:1080](figures/genealogy.png)

</div>

---

## Divide the vote

<hr>

<div class="cols">
<div>

<div class="formula">

$$c_i = \sum_j A_{ji}\, \frac{c_j}{d^{\text{out}}_j}$$

</div>

$d^{\text{out}}_j$: the number of links out of $j$.

C has three links in, and E has one. Which ranks higher?

</div>
<div class="fig">

![w:537](figures/pr-split.png)

</div>
</div>

<div class="cue">

*Take 30 seconds.*

</div>

<!--
A page splits its score equally among the pages it links to. A gives a third to each of B, C, D.
-->

---

## A three-way tie

<hr>

<div class="cols">
<div>

- A, C and E: 3/11 each. B and D: 1/11.
- E's one link comes from C, which passes on everything.

</div>
<div class="fig">

![w:537](figures/pr-split-answer.png)

</div>
</div>

---

## A dead end

<hr>

<div class="cols">
<div>

- E loses its only outgoing link.
- Its score has nowhere to go: the total drains to zero.

</div>
<div class="fig">

![w:537](figures/pr-leak.gif)

</div>
</div>

---

## Teleportation

<hr>

<div class="cols">
<div>

<div class="formula">

$$c_i = (1-r) \sum_j A_{ji}\, \frac{c_j}{d^{\text{out}}_j} + \frac{r}{N}$$

</div>

- With probability r = 0.15, jump to a random page.
- A dead end always jumps.
- This is **PageRank**.

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

- Jump back to A only.
- Score: how often a walker that keeps restarting at A visits each page.

</div>
<div class="fig">

![w:537](figures/ppr.png)
<figcaption>dashed: the jump back to A</figcaption>

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

Closeness: Middletown. Harmonic: the Bronx. Eccentricity: east of Binghamton.

Betweenness: Monticello. Eigenvector: Hempstead.

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

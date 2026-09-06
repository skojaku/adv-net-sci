---
marp: true
theme: network-science
paginate: true
math: katex
---

<!-- _class: lead -->

<div class="eyebrow">Advanced Topics in Network Science · Module 03</div>

# Build it, Break it

<hr>

<div class="sub">Minimum spanning trees, percolation, and the critical fraction</div>

<div class="credit">Sadamori Kojaku · Binghamton University</div>

<!--
They arrive having already built a grid, broken it and rebuilt it on the worksheet. This hour names what they did and then goes past it.
-->

---

<!-- _class: mid -->

## The question for today

<hr>

<div class="formula">

What fraction of a network can be removed before it breaks into small pieces, and does the answer depend on how the removed nodes are chosen?

</div>

Part Three answers the first half with one formula. Part Four answers the second.

---

<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 04</span></div>

## Build it

Moravia, 1926, and the minimum spanning tree

---

## Moravia, 1926

<hr>

<div class="cols">
<div>

The West Moravian Power Company had to connect eight towns using the least total length of cable.

* **Otakar Borůvka** published the first solution that year, and with it the **minimum spanning tree**.

</div>
<div class="fig">

![w:520](figures/boruvka-portrait.png)
<figcaption>Otakar Borůvka, 1899–1995</figcaption>

</div>
</div>

<!--
The paper is O jistem problemu minimalnim, 1926. His method was neither Kruskal's nor Prim's: every component takes its own cheapest outgoing edge at the same time. Name it, do not spend a slide on it.
-->

---

## What you built on the worksheet has a name

<hr>

A **spanning tree** is connected, acyclic, and contains every node: $n-1$ edges. The one of least total weight is the **minimum spanning tree**.

<div class="fig">

![w:1100](figures/mst-def.png)
<figcaption>seven cables, 292 km; the nine stations on your sheet were the same problem</figcaption>

</div>

---

## Kruskal and Prim

<hr>

**Kruskal** and **Prim**: two greedy rules that return the same tree.

<figure class="anim-stage" id="mst-race">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>

  <div class="anim-grid-2" data-anim-canvas>
    <div class="mst-col" data-anim-clear data-mst-left></div>
    <div class="mst-col" data-anim-clear data-mst-right></div>
  </div>

  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<!-- Deck-wide, and it must run before the first anim.js: every stage in this
     deck steps by hand. Nothing advances itself while the room is talking. -->
<script>window.animStepOnly = true;</script>
<script src="../../lecture-note/assets/anim/mst-race.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

<!--
Step 4 is the cut property: cut the tree in two and the cheapest edge across the cut must be in it. That is why both rules return the same tree, and why different build orders on the worksheet gave the same total.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 04</span></div>

## Break it

Removing nodes, and measuring what is left

---

<!-- _class: mid -->

## Which removal costs the most?

<hr>

<div class="formula">

Remove one town and every cable at it. For which town is the largest remaining component smallest?

</div>

<div class="fig">

![w:1100](figures/mst-blank.png)

</div>

<!--
Run this as a poll and write the tally on the board before turning the page.
-->

---

## Removing Brno leaves components of 3, 3 and 1

<hr>

**Connectivity** is the number of nodes in the largest connected component divided by $n$. Brno scores $3/8$, a leaf $7/8$.

<div class="fig">

![w:1100](figures/brno-removed.png)
<figcaption>Jihlava's component, Olomouc's component, and Hodonín alone</figcaption>

</div>

<!--
This is the middle column of Question 4 on the worksheet, on a different grid.
-->

---

## Removing towns one at a time

<hr>

<figure class="anim-stage" id="break-profile">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>

  <div data-anim-canvas>
    <div data-anim-clear data-bp-net></div>
  </div>

  <div data-anim-canvas>
    <div data-anim-clear data-bp-chart></div>
  </div>

  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script src="../../lecture-note/assets/anim/break-profile.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

<!--
Step 2 is the worksheet's Order R, step 3 its Order T, step 4 the area estimated in Question 8. Stop on step 3 after the first removal.
-->

---

## Random failure against targeted attack

<hr>

The **R-index** is the mean connectivity over the removals, that is, the area under the curve. Random failure gives 0.41, a targeted attack 0.17.

<div class="fig">

![w:1100](figures/profile-both.png)
<figcaption>build a network and remove nodes: <a href="https://skojaku.github.io/adv-net-sci/assets/vis/network-robustness.html">network-robustness.html</a></figcaption>

</div>

<!--
Their own two areas on the nine-station grid come out near 0.5 and near 0.23, so the ratio they measured is the ratio here. Collect a couple of their numbers first.
-->

---

<!-- _class: mid -->

## Measured, or computed?

<hr>

The R-index measures a network after it has been broken.

<div class="formula">

Can the fraction at which it breaks be computed from the network instead?

</div>

<!--
Do not answer it. The formula arrives in Part Three and uses only the degree distribution.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 04</span></div>

## Predict it

The critical fraction, from the degree distribution

---

<!-- _class: mid -->

## Site percolation

<hr>

<div class="formula">

Each cell of a square lattice is occupied with probability $p$, independently. Occupied cells that share an edge belong to one **cluster**. At which $p$ does the largest cluster first span the lattice?

</div>

<div class="fig">

![w:1100](figures/lattice-low.png)

</div>

<!--
Ask for a number before moving on.
-->

---

## Raising the occupation probability

<hr>

<figure class="anim-stage" id="percolation">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>

  <div data-anim-canvas>
    <div data-anim-clear data-pc-lattice></div>
  </div>

  <div data-anim-canvas>
    <div data-anim-clear data-pc-chart></div>
  </div>

  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script src="../../lecture-note/assets/anim/percolation.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

<!--
Step 3 hands the dial over. Between p = 0.575 and p = 0.600 the largest cluster of the lattice on screen goes from 0.20 to 0.56.
-->

---

## The percolation threshold

<hr>

Below $p_c \approx 0.59$ the largest cluster stays small; above it it holds a finite share of the lattice: a **phase transition**.

<div class="fig">

![w:1100](figures/phase-transition.png)
<figcaption>removing nodes from a network is the same transition, run backwards</figcaption>

</div>

---

<!-- _class: mid -->

## Same $n$ and $m$, different thresholds

<hr>

Two networks with the same number of nodes and the same number of edges. One breaks up when a fifth of the nodes are removed; the other survives losing four-fifths.

<div class="formula">

What property of a network decides which?

</div>

<!--
The edge count is the same in both, so it cannot be that. Push until somebody says something about how the edges are distributed over the nodes.
-->

---

## The node at the end of a random edge

<hr>

<figure class="anim-stage" id="branch-out">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>

  <div data-anim-canvas>
    <div data-anim-clear data-bo-net></div>
  </div>

  <div data-anim-canvas>
    <div data-anim-clear data-bo-side></div>
  </div>

  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script src="../../lecture-note/assets/anim/branch-out.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

<!--
Five steps: the twenty edge ends, a node drawn at random (mean degree 2), an edge end drawn at random (mean degree 3, which is kappa), the branching factor kappa - 1, and the dial for f. Stop after step 3 so the two means are compared before going on.
-->

---

## $q(k)$ and $\kappa$

<hr>

<div class="cols">
<div>

Drawing an edge end at random reaches a node with probability $q(k) = k\,p(k) / \langle k \rangle$.

<div class="formula">

$$ \kappa = \frac{\langle k^2 \rangle}{\langle k \rangle} $$

</div>

* $\kappa$ is the mean degree under $q$, not under $p$.

</div>
<div class="fig">

![w:520](figures/kappa-def.png)
<figcaption>ten nodes, twenty edge ends: mean degree 2, kappa 3</figcaption>

</div>
</div>

<!--
This is the network from the animation, at the same positions.
-->

---

## Molloy–Reed

<hr>

One of the $\kappa$ edges is the arrival edge, so a search continues along $\kappa - 1$: the **branching factor**.

<div class="fig">

![w:1100](figures/molloy-reed.png)
<figcaption>a giant component exists exactly when kappa exceeds 2 · Molloy &amp; Reed, 1995</figcaption>

</div>

---

## Removing a fraction $f$

<hr>

$f$ is the fraction of nodes removed at random, so the branching factor becomes $(1-f)(\kappa-1)$.

<div class="fig">

![w:1100](figures/fc-formula.png)
<figcaption>the critical fraction is 1 − 1/(kappa − 1); here kappa = 3, so it is 0.50</figcaption>

</div>

<!--
The exact binomial dilution is in the appendix and gives the same threshold. A triangle returns the search to a node it has already reached, so the real branching factor is below kappa - 1.
-->

---

## Poisson degrees

<hr>

For a Poisson degree distribution $\kappa = \langle k \rangle + 1$, so $f_c = 1 - 1/\langle k \rangle$.

<div class="fig">

![w:1100](figures/fc-poisson.png)
<figcaption>at mean degree 1 this gives kappa 2, the threshold of Module 02's giant component</figcaption>

</div>

---

<!-- _class: mid -->

## What if the degree distribution has hubs?

<hr>

Scale-free degrees, $P(k) \sim k^{-\gamma}$: most nodes have small degree, a few have very large degree, and the largest grows with $n$.

<div class="formula">

What happens to $\kappa = \langle k^2 \rangle / \langle k \rangle$?

</div>

<!--
They met scale-free degree distributions in Module 02. Ask what the mean of the SQUARES does when one degree grows with n.
-->

---

## For $2 < \gamma < 3$, $\kappa$ diverges

<hr>

$\langle k^2 \rangle$ grows without bound with $n$, so $\kappa \to \infty$ and $f_c \to 1$.

<div class="fig">

![w:1100](figures/fc-scalefree.png)
<figcaption>Cohen, Erez, ben-Avraham &amp; Havlin, 2000</figcaption>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 04</span></div>

## Design it

Hubs raise the threshold for random failure and lower it for attack

---

<!-- _class: mid -->

## Does $f_c \to 1$ mean the network cannot be broken?

<hr>

$f_c$ was derived for nodes removed at random. The Internet, the airline network and metabolic networks all have scale-free degrees.

<div class="formula">

Does the result survive if the removed nodes are chosen?

</div>

---

## Two networks with the same degree sum

<hr>

<figure class="anim-stage" id="rf-attack">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>

  <div class="anim-grid-2" data-anim-canvas>
    <div class="rf-col rf-ring" data-anim-clear data-rf-ring></div>
    <div class="rf-col rf-hubs" data-anim-clear data-rf-hubs></div>
  </div>

  <div data-anim-canvas>
    <div class="rf-chart" data-anim-clear data-rf-chart></div>
  </div>

  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script src="../../lecture-note/assets/anim/rf-attack.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

<!--
Run steps 2 and 3 before touching the dial. The two random-failure curves nearly coincide; the two targeted curves do not.
-->

---

## Robust yet fragile

<hr>

The hubs that give $f_c \to 1$ under random failure are the first nodes a targeted attack removes. *Albert, Jeong &amp; Barabási, 2000.*

<div class="fig">

![w:1100](figures/robust-fragile.png)
<figcaption>solid: nodes removed at random · dashed: highest degree first</figcaption>

</div>

---

<!-- _class: mid -->

## Two extra edges

<hr>

<div class="formula">

The budget allows two cables beyond the 292 km tree. Which two, and what does the network gain?

</div>

<div class="fig">

![w:1100](figures/mst-blank-design.png)

</div>

<!--
Take three proposals before turning the page. Push on the second question. This is Question 10 on the worksheet with a budget instead of a free hand.
-->

---

## Two edges that close a cycle

<hr>

Znojmo–Hodonín and Hodonín–Zlín add 136 km. The worst single removal goes from $3/8$ to $6/8$, and $R$ from 0.17 to 0.27.

<div class="fig">

![w:1100](figures/redundant-answer.png)
<figcaption>the best of the fifteen possible pairs, found by search</figcaption>

</div>

<!--
Return to whatever the room proposed before showing this. The general rules: even out the degrees, give every node a second route, and protect the hubs that cannot be designed away.
-->

---

## Module 03 summary

<hr>

292 km built the grid, removing Brno left 3 of 8 connected, and 136 km more brings the worst case to 6 of 8.

<div class="fig">

![w:1100](figures/recap.png)
<figcaption>the tree, the removed node, and the two added edges</figcaption>

</div>

---

## Coming up in Module 04

<hr>

<div class="cols">
<div>

An edge end reaches a node with probability proportional to its degree. That is $q(k)$.

* Applied to friendship it gives the **friendship paradox**: your friends have more friends than you do.

</div>
<div class="fig">

![w:520](figures/m04-teaser.png)
<figcaption>ten people and their friendships, one column each</figcaption>

</div>
</div>

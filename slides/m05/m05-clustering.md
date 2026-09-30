---
marp: true
theme: network-science
paginate: true
math: katex
---

<!-- _class: lead -->

<div class="eyebrow">Advanced Topics in Network Science · Module 05</div>

# Community Detection

<hr>

<div class="sub">finding groups in a network</div>

<div class="credit">Sadamori Kojaku · Binghamton University</div>

---

<!-- _class: mid -->

## Let's look at a network

<hr>

<div class="fig tight">

![w:1080](figures/groups-plain.png)

</div>

<!--
Ask what they see before moving on. Wait for someone to say "groups".
-->

---

## What are these groups?

<hr>

We call them **communities**. How would we define one?

<div class="fig tight">

![w:1080](figures/groups-circled.png)

</div>

<!--
Everyone circled the same four groups without a definition. Take one or two attempts at a definition from the room; do not correct them yet.
-->

---

<!-- _class: mid -->

## What is the strongest community?

<hr>

Draw the most tightly connected group you can think of.

<!--
Thirty seconds on paper. Then ask one student to describe theirs.
-->

---

## A clique: everyone knows everyone

<hr>

<div class="cols">
<div>

A **clique** is a group where every pair is connected.

We cannot add one more edge inside it.

</div>
<div class="fig">

![w:537](figures/clique-six.png)
<figcaption>6 nodes, all 15 pairs connected</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Problem solved?

<hr>

Let's find every clique in the network. Done. Bye!

<!--
Pause and wait for an objection.
-->

---

## Cliques are too strict

<hr>

<div class="cols">
<div>

Remove one edge, and the group is no longer a clique.

Real groups miss many edges. How can we allow for that?

</div>
<div class="fig">

![w:537](figures/clique-miss-one.png)
<figcaption>dashed: the one missing edge</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Let's relax the clique in three ways

<hr>

* **Density**: most pairs are connected
* **Distance**: every pair is a few steps apart
* **Degree**: every member is connected to most of the others

<!--
These are called pseudo-cliques. The lecture note has more of them (k-core, n-clan, n-club, k-truss); we take one per axis.
-->

---

## Density: the ρ-dense subgraph

<hr>

<div class="cols">
<div>

A group of $s$ members is **ρ-dense** if it has at least a fraction ρ of all possible edges.

<div class="formula">

$$\frac{\text{edges inside}}{s(s-1)/2} \ge \rho$$

</div>

</div>
<div class="fig">

![w:537](figures/rho-dense.png)
<figcaption>8 of the 15 possible edges: 0.53-dense</figcaption>

</div>
</div>

---

## Distance: the n-clique

<hr>

<div class="cols">
<div>

A group is an **n-clique** if every pair is at most $n$ steps apart.

</div>
<div class="fig">

![w:537](figures/n-clique-two.png)
<figcaption>red: a farthest pair's 2-step path. A 2-clique.</figcaption>

</div>
</div>

<!--
Luce 1950. The path may pass through nodes outside the group; the n-clan and n-club forbid that (lecture note).
-->

---

## Degree: the k-plex

<hr>

<div class="cols">
<div>

In a **k-plex** of $s$ members, every member is connected to at least $s-k$ of the others.

</div>
<div class="fig">

![w:537](figures/k-plex-two.png)
<figcaption>dashed: missing edges. Each member is connected to at least 3 = 5 − 2 others: a 2-plex.</figcaption>

</div>
</div>

<!--
Seidman and Foster 1978. A 1-plex is a clique. The k-core is the other degree relaxation: every member has at least k neighbors inside, whatever the group size.
-->

---

## Q1. This group is ___-dense

<hr>

<div class="cols">
<div>

Fill in the largest ρ.

</div>
<div class="fig">

![w:537](figures/quiz-prism.png)

</div>
</div>

---

## Q1. 0.6-dense

<hr>

<div class="cols">
<div>

6 members have 15 possible edges. 9 are present.

$9/15 = 0.6$

</div>
<div class="fig">

![w:537](figures/quiz-prism-dense.png)
<figcaption>dashed: the 6 missing edges</figcaption>

</div>
</div>

---

## Q2. This group is a ___-clique

<hr>

<div class="cols">
<div>

Fill in the smallest $n$.

</div>
<div class="fig">

![w:537](figures/quiz-prism.png)

</div>
</div>

---

## Q2. A 2-clique

<hr>

<div class="cols">
<div>

Every pair is at most 2 steps apart.

</div>
<div class="fig">

![w:537](figures/quiz-prism-dist.png)
<figcaption>red: the 2-step path between a farthest pair</figcaption>

</div>
</div>

---

## Q3. This group is a ___-plex

<hr>

<div class="cols">
<div>

Fill in the smallest $k$.

</div>
<div class="fig">

![w:537](figures/quiz-prism.png)

</div>
</div>

---

## Q3. A 3-plex

<hr>

<div class="cols">
<div>

Each member is connected to 3 of the other 5.

$s - k = 3$ with $s = 6$, so $k = 3$.

</div>
<div class="fig">

![w:537](figures/quiz-prism-plex.png)
<figcaption>red: one member. Dashed: its 2 missing edges.</figcaption>

</div>
</div>

<!--
The same group is 0.6-dense, a 2-clique and a 3-plex. Each relaxation gives its own number, and on a real network each finds different groups.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 03</span></div>

## Graph cut

Let's find groups by cutting edges

---

<!-- _class: mid -->

## How would we split this into two groups?

<hr>

<div class="fig">

![w:1080](figures/cut-plain.png)

</div>

---

## Cut as few edges as we can

<hr>

<div class="cols">
<div>

**Cut** counts the edges between groups $V_1$ and $V_2$.

<div class="formula">

$$\text{Cut}(V_1, V_2) = \sum_{i \in V_1} \sum_{j \in V_2} A_{ij}$$

</div>

</div>
<div class="fig">

![w:537](figures/cut-def-col.png)
<figcaption>blue, red: the two groups. Thick: the edges we cut.</figcaption>

</div>
</div>

<!--
A is the adjacency matrix from Module 01: A_ij = 1 if i and j are connected.
-->

---

## It works when the groups are clear

<hr>

<div class="cols">
<div>

With $K$ groups, Cut counts the edges between different groups. We look for the smallest.

<div class="formula">

$$\min_{V_1, \dots, V_K} \text{Cut}(V_1, \dots, V_K)$$

</div>

</div>
<div class="fig">

![w:537](figures/cut-works.png)
<figcaption>thick: the 3 edges we cut. No split into three groups cuts fewer.</figcaption>

</div>
</div>

---

## Does it always work?

<hr>

Let's find the smallest cut in this network.

<div class="fig">

![w:1080](figures/cut-plain.png)

</div>

---

## The smallest cut takes one node away

<hr>

One node against the rest. We don't want this.

<div class="fig">

![w:1080](figures/cut-trivial.png)

</div>

<!--
Any node with one edge gives a cut of 1. The minimum cut finds the weakest point of the network, which is rarely a community boundary.
-->

---

## We want balanced groups: ratio cut

<hr>

<div class="formula">

$$\text{RatioCut}(V_1, V_2) = \frac{\text{Cut}(V_1, V_2)}{|V_1|\,|V_2|}$$

</div>

<div class="fig tight">

![w:1080](figures/rcut-small.png)
<figcaption>one node alone: 1/(1 × 8). Balanced (red): 2/(5 × 4). We pick the lower score.</figcaption>

</div>

<!--
We minimize. The denominator is largest when the two sides are equal, so the balanced split wins even though it cuts twice as many edges.
-->

---

## Balance by degree: normalized cut

<hr>

<div class="formula">

$$\text{NCut}(V_1, V_2) = \frac{\text{Cut}(V_1, V_2)}{\text{vol}(V_1)\,\text{vol}(V_2)}$$

</div>

<div class="fig tight">

![w:1080](figures/ncut-small.png)
<figcaption>thick: the 2 edges we cut. vol: the sum of degrees in a group. Balanced: 1/112. One node alone: 1/29.</figcaption>

</div>

<!--
Shi and Malik 2000. Balancing by volume matters when degrees are uneven: ten hubs and ten leaves are the same size but not the same amount of network. Both ratio cut and normalized cut need K in advance, and finding the best split is NP-hard.
-->

---

## Zachary's karate club

<hr>

Wayne Zachary recorded friendships in a karate club, 1970 to 1972.

<div class="fig">

![w:1080](figures/karate-plain.png)
<figcaption>34 members, 78 friendships. The club later split in two.</figcaption>

</div>

<!--
A university karate club. The instructor (Mr. Hi) wanted to raise the fees; the administrator (John A.) did not. The club split into two clubs, 17 members each. Zachary 1977, Journal of Anthropological Research 33(4): 452-473.

Before the next three slides, ask: what will each of the three scores do on this network?
-->

---

## Karate club: minimum cut

<hr>

<div class="fig">

![w:1080](figures/karate-cut-min.png)
<figcaption>thick: the 1 edge we cut. One member against 33.</figcaption>

</div>

---

## Karate club: ratio cut

<hr>

<div class="fig">

![w:1080](figures/karate-cut-ratio.png)
<figcaption>thick: the 4 edges we cut. Five members against 29.</figcaption>

</div>

---

## Karate club: normalized cut

<hr>

<div class="fig">

![w:1080](figures/karate-cut-norm.png)
<figcaption>thick: the 10 edges we cut. 17 against 17. Ringed: the 2 of 34 who do not match the real split.</figcaption>

</div>

<!--
10 edges cut. Each split is the best found by a random-restart local search (figs_sketch.py); finding the exact optimum is NP-hard.
-->

---

<!-- _class: mid -->

## Game: find the smallest cut

<hr>

Let's split the club into two groups. Cut as few edges as you can.

[Open the game](https://skojaku.github.io/adv-net-sci/assets/vis/community-detection/index.html?scoreType=graphcut&numCommunities=2&randomness=0.25&dataFile=net_karate.json)

<!--
Someone will paint everyone one color and get a cut of 0. That is the missing rule: each group needs at least one member. The page's "best known" of 11 is the real split; the smallest cut is 1 (the lone member, two slides back).
-->

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 03</span></div>

## More than chance

Let's compare a network with a random one

---

<!-- _class: mid -->

## How dense should a community be?

<hr>

<div class="fig">

![w:1080](figures/how-dense.png)
<figcaption>two cliques and two stars</figcaption>

</div>

<!--
Ask: is a star a community? Take two answers.
-->

---

<!-- _class: mid -->

## Key idea: more edges inside than chance

<hr>

We subtract the edges we expect by chance.

<div class="formula">

$$(\text{edges inside}) - (\text{edges inside by chance}) > 0$$

</div>

<!--
The stars on the last slide have density 0.33 or less. Any fixed density threshold is arbitrary; chance gives each network its own threshold.
-->

---

## Chance: the configuration model

<hr>

Our **null model**, the **configuration model**, keeps every node's degree and pairs up edge ends at random.

<div class="fig tight">

![w:1080](figures/null-model.png)
<figcaption>color: group. Right: one random draw. On average, 7.53 of the 15 edges land inside.</figcaption>

</div>

<!--
Exact expectation: sum over groups of vol^2 / 4m = (16^2 + 14^2) / 60 = 7.53.
-->

---

## Modularity

<hr>

<div class="formula">

$$Q = \frac{1}{2m} \sum_{i,j} \left[ A_{ij} - \frac{k_i k_j}{2m} \right] \delta(c_i, c_j)$$

</div>

* $A_{ij}$: 1 if $i$ and $j$ are connected, else 0
* $k_i k_j / 2m$: the expected number of edges between $i$ and $j$ by chance, where $k_i$ is the degree of $i$
* $\delta(c_i, c_j)$: 1 if the groups $c_i$ and $c_j$ are the same
* Our example, with $m = 15$ edges: $Q = (13 - 7.53)/15 = 0.36$

<!--
Where k_i k_j / 2m comes from: node i has k_i edge ends. Each lands on one of j's k_j ends with probability k_j / 2m. The sum runs over ordered pairs, so every edge is counted twice; dividing by 2m turns the count into a fraction of the m edges. Q is at most 1; around 0.3 to 0.7 for real networks with clear groups.
-->

---

## Louvain: maximize Q, then coarse-grain

<hr>

**Louvain** repeats two steps until Q stops rising.

<div class="fig tight">

![w:1080](figures/louvain-steps.png)
<figcaption>color: group. Step 1: move each node to the neighboring group that raises Q most. Step 2: each group becomes one node.</figcaption>

</div>

<!--
Blondel et al. 2008. Maximizing Q is NP-hard. After step 2, step 1 runs again on the smaller network. It runs on millions of nodes.
-->

---

## Leiden: every group stays connected

<hr>

Louvain can leave a group in two pieces. **Leiden** splits it.

<div class="fig tight">

![w:1080](figures/leiden-two.png)
<figcaption>color: group. Louvain's red group has no edge between its two halves.</figcaption>

</div>

<!--
Traag, Waltman and van Eck 2019. This happens when a node that bridged two halves is moved to another group. Leiden adds a refinement step, and is usually faster too.
-->

---

<!-- _class: mid -->

## Game: maximize modularity

<hr>

Let's color the club with up to four groups. Get Q as high as you can.

[Open the game](https://skojaku.github.io/adv-net-sci/assets/vis/community-detection/index.html?scoreType=modularity&numCommunities=4&randomness=0.25&dataFile=net_karate.json)

<!--
The best known Q for the club is 0.420, with four groups.
-->

---

## A ring of triangles: what groups does Q pick?

<hr>

<div class="fig">

![w:1080](figures/ring-ten.png)
<figcaption>each triangle is joined to the next by one edge</figcaption>

</div>

---

## Q merges neighbors: the resolution limit

<hr>

Past $\sqrt{2m}$ triangles, pairs score a higher Q than single triangles.

What Q picks depends on the network's size: the **resolution limit**.

<div class="fig">

![w:1080](figures/ring-four-ten.png)
<figcaption>shaded: the higher-Q groups. 4: apart 0.500, pairs 0.375. 10: apart 0.650, pairs 0.675.</figcaption>

</div>

<!--
Fortunato and Barthelemy 2007. n triangles give m = 4n edges. Apart: Q = 3/4 - 1/n. Pairs: Q = 7/8 - 2/n. Pairs win when n > 8, which is n > sqrt(2m). Nothing about the two triangles changed; only the size of the rest of the network did.
-->

---

## Similar Q, different groups

<hr>

Let's compare two splits of the club.

<div class="fig">

![w:1080](figures/karate-q-four.png)
<figcaption>Q = 0.407: four groups</figcaption>

</div>

---

## Similar Q, different groups

<hr>

Many different splits have almost the same Q.

<div class="fig">

![w:1080](figures/karate-q-three.png)
<figcaption>Q = 0.402: three groups. Gray joined red, and one member moved to blue.</figcaption>

</div>

<!--
Both splits are local maxima: no single member can move and raise Q. The best known split scores 0.420. Run Louvain with two random seeds and you can get two different answers.
-->

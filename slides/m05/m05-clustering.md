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

We call them **communities**. Can we define one? How?

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

Real groups miss many edges. What does a real group look like?

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

A group is **ρ-dense** if it has at least a fraction ρ of all possible edges.

<div class="formula">

$$\rho = \frac{\text{edges inside}}{n(n-1)/2}$$

</div>

</div>
<div class="fig">

![w:537](figures/rho-dense.png)
<figcaption>8/15 = 0.53, so this group is 0.53-dense</figcaption>

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
<figcaption>red: a farthest pair, 2 steps apart. A 2-clique.</figcaption>

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

In a **k-plex** of $n$ members, every member is connected to at least $n-k$ of the others.

</div>
<div class="fig">

![w:537](figures/k-plex.png)
<figcaption>each member misses at most 1 other: a 2-plex</figcaption>

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

6 members make 15 possible edges. 9 are present.

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
<figcaption>red: a farthest pair, 2 steps apart</figcaption>

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

$n - k = 3$ with $n = 6$, so $k = 3$.

</div>
<div class="fig">

![w:537](figures/quiz-prism-plex.png)
<figcaption>dashed: the 2 members the ringed one is not connected to</figcaption>

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

**Cut** counts the edges between the two groups.

<div class="formula">

$$\text{Cut}(V_1, V_2) = \sum_{i \in V_1} \sum_{j \in V_2} A_{ij}$$

</div>

</div>
<div class="fig">

![w:537](figures/cut-def-col.png)
<figcaption>thick: the edges we cut</figcaption>

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
<figcaption>no split into three groups cuts fewer edges</figcaption>

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
<figcaption>one node alone: 1/(1 × 8). Balanced: 2/(5 × 4). The balanced split scores lower.</figcaption>

</div>

<!--
We minimize. The denominator is largest when the two sides are equal, so the balanced split wins even though it cuts twice as many edges.
-->

---

## Balanced by edges: normalized cut

<hr>

<div class="formula">

$$\text{NCut}(V_1, V_2) = \frac{\text{Cut}(V_1, V_2)}{\text{vol}(V_1)\,\text{vol}(V_2)}$$

</div>

<div class="fig tight">

![w:1080](figures/ncut-small.png)
<figcaption>vol: the sum of degrees in a group. Balanced: 1/112. One node alone: 1/29.</figcaption>

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
<figcaption>17 against 17. 32 of 34 members match the real split; ringed: the two who do not.</figcaption>

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
Someone will paint everyone one color and get a cut of 0. That is the missing rule: each group needs at least one member.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 03</span></div>

## More than chance

Let's compare a network with a random one

---

## How dense should a community be?

<hr>

<div class="fig">

![w:1080](figures/how-dense.png)
<figcaption>two cliques and two stars</figcaption>

</div>

<!--
Is a star a community? Its density is 0.33 or less. Any fixed threshold is arbitrary.
-->

---

<!-- _class: mid -->

## Key idea: more edges inside than chance

<hr>

Count the edges inside the groups. Subtract the number we expect by chance.

<div class="formula">

$$(\text{edges inside}) - (\text{edges inside by chance}) > 0$$

</div>

---

## Modularity: how surprising are the groups?

<hr>

Our **null model**, the **configuration model**, keeps every node's degree and connects edges at random.

<div class="fig tight">

![w:1080](figures/null-model.png)
<figcaption>right: one random draw. On average, chance puts 7.5 of the 15 edges inside.</figcaption>

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

* $A_{ij}$: 1 if $i$ and $j$ are connected
* $k_i k_j / 2m$: the edges we expect between $i$ and $j$ by chance
* $\delta(c_i, c_j)$: 1 if $i$ and $j$ are in the same group
* Our example: $Q = (13 - 7.53)/15 = 0.36$

<!--
Where k_i k_j / 2m comes from: node i has k_i edge ends. Each lands on one of j's k_j ends with probability k_j / 2m. The sum runs over ordered pairs, so every edge is counted twice; dividing by 2m turns the count into a fraction of the m edges. Q is at most 1; around 0.3 to 0.7 for real networks with clear groups.
-->

---

## Louvain: maximize Q, then coarse-grain

<hr>

Finding the best Q is hard. **Louvain** repeats two steps until Q stops rising.

<div class="fig tight">

![w:1080](figures/louvain-steps.png)
<figcaption>step 1: move each node to the neighboring group that raises Q most. Step 2: each group becomes one node.</figcaption>

</div>

<!--
Blondel et al. 2008. Maximizing Q is NP-hard. After step 2, step 1 runs again on the smaller network. It runs on millions of nodes.
-->

---

## Leiden: every group stays connected

<hr>

Louvain can return a group in two pieces. **Leiden** checks each group and splits it.

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

With more than $\sqrt{2m}$ triangles, Q puts two triangles in one group.

<div class="fig">

![w:1080](figures/ring-four-ten.png)
<figcaption>shaded: one group. 4 triangles: apart 0.500, pairs 0.375. 10 triangles: apart 0.650, pairs 0.675.</figcaption>

</div>

<!--
Fortunato and Barthelemy 2007. n triangles give m = 4n edges. Apart: Q = 3/4 - 1/n. Pairs: Q = 7/8 - 2/n. Pairs win when n > 8, which is n > sqrt(2m). Nothing about the two triangles changed; only the size of the rest of the network did.
-->

---

## Similar Q, different groups

<hr>

Two splits of the karate club.

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

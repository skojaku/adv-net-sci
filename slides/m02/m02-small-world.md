---
marp: true
theme: network-science
paginate: true
math: katex
---

<!-- _class: lead -->

<div class="eyebrow">Advanced Topics in Network Science · Module 02</div>

# How Many Handshakes?

<hr>

<div class="sub">Why the world is smaller than expected</div>

<div class="credit">Sadamori Kojaku · Binghamton University</div>

<!--
Open with Omaha, before any definition. High clustering together with short paths is the spine of the whole module.
-->

---

<!-- _class: mid -->

## Today’s question

<hr>

<div class="formula">

Consider a random person walking down the street on the other side of the world. How many handshakes away from you is this stranger?

</div>

*Write down your guess for the number now. The worksheet asks you for it again at the end.*

---

## Roadmap for today

<hr>

<div class="steps-list">

<div><div class="i">01</div><div>The claim: a letter from Omaha, and a wiki race</div></div>
<div><div class="i">02</div><div>Measuring “six”: distance, average path length, diameter</div></div>
<div><div class="i">03</div><div>The other half: triangles and clustering</div></div>
<div><div class="i">04</div><div>The yardstick: a random baseline and the index sigma</div></div>
<div><div class="i">05</div><div>The mechanism: Watts–Strogatz rewiring</div></div>
<div><div class="i">06</div><div>Edge cases: the networks that break the definitions</div></div>

</div>

<!--
Parts 02 and 03 are the names for what they work out on the Ringville sheet. Parts 04–06 are what the sheet cannot reach.
-->

---

<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 06</span></div>

## The six-handshake claim

A letter, a stranger, and 160 envelopes

---

## Omaha, 1967

<hr>

<div class="cols">
<div>

In Stanley Milgram’s small-world experiment, packets are mailed to individuals randomly selected from Omaha, Nebraska and Wichita, Kansas. Each packet names a single target: a stockbroker working in Boston.

</div>
<div class="fig">

![w:520](figures/milgram-map.png)
<figcaption>the target lived in Sharon, Massachusetts and worked in Boston</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## The one rule

<hr>

<div class="cols">
<div>

You may not mail it to the target unless you know him personally.

Otherwise you pass it to **one person you know on a first-name basis** who might be closer.

</div>
<div class="fig">

![w:520](figures/milgram-rule.png)
<figcaption>every hop is a real acquaintance</figcaption>

</div>
</div>

---

## 160 packets, and what became of them

<hr>

Of the 160 packets mailed, 64 reached the target.

<div class="fig tight">

![w:1000](figures/milgram-arrivals.png)
<figcaption>red: the 64 completed chains, the only ones that carry data</figcaption>

</div>

---

<!-- _class: mid -->

## The chains that made it

<hr>

<div class="fig">

![w:1000](figures/milgram-chain.png)
<figcaption>one packet’s route, hop by hop</figcaption>

</div>

The median completed chain ran through roughly six links.

---

<!-- _class: mid -->

## Milgram never said “six degrees”

<hr>

<div class="cols">
<div>

The phrase belongs to the playwright **John Guare**, who used it as the title of a play in 1990.

<div class="note">

Milgram measured a median chain length; Guare supplied the slogan.

</div>

</div>
<div class="fig">

![w:520](figures/six-degrees-timeline.png)
<figcaption>twenty-three years separate the experiment from the phrase</figcaption>

</div>
</div>

---

## Restaged, at planetary scale

<hr>

<div class="cols">
<div>

* **Email, 2003.** 24,000 starters, 18 targets in 13 countries. Only 384 chains completed, averaging about four steps.
* **Facebook, 2012.** The full graph: 721 million users, 69 billion friendships. Average distance **4.74**.
* *Check both against the number you wrote down.*

</div>
<div class="fig">

![w:520](figures/replication-facebook.png)
<figcaption>the same answer, measured three times, forty-five years apart</figcaption>

</div>
</div>

<!-- Eight hundred times the people, and the number does not grow. Say that the 4.74 is an average over their largest connected component; Part Six returns to that convention. -->

---

## Your turn: Wikirace

<hr>

<div class="cols">
<div>

Two random Wikipedia articles. Links only, no search box. Fewest clicks wins.

Play at [wiki-race.com](https://wiki-race.com). One round, then shout out your click count.

</div>
<div class="fig">

![w:520](figures/wikirace.png)
<figcaption>a route found by clicking through links</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## What did you just do?

<hr>

You found a short route through a network of seven million articles without ever seeing the network.

<div class="formula">

Is *finding* a short route the same as one *existing*?

</div>

*30 seconds.*

---

## What Milgram’s subjects actually did

<hr>

<div class="fig tight">

![w:1000](figures/routing-vs-existence.png)
<figcaption>red: a route that exists; the dashed box is everything the start node can see</figcaption>

</div>

Milgram’s subjects had no map. They **routed** on local knowledge alone, a stronger requirement than the existence of a short route.

---

<!-- _class: mid -->

## Your turn: Ringville

<hr>

<div class="cols">
<div>

Sixteen people sit in one circle, each friends with the two on their left and the two on their right.

The worksheet asks how far apart they are, what two shortcuts do to that, and whether their friends know each other.

*Take the sheet.*

</div>
<div class="fig">

![w:520](figures/ringville.png)
<figcaption>the town on the sheet in front of you</figcaption>

</div>
</div>

<!--
Hand out exercise.pdf here. The rest of the deck is the vocabulary pass over what they compute. Do not pre-empt it.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 06</span></div>

## Measuring “six”

Turn the chain into a graph and count

---

<!-- _class: mid -->

## The chain is a graph

<hr>

<div class="fig">

![w:1000](figures/chain-graph.png)
<figcaption>the same seven people from Part One</figcaption>

</div>

Each person becomes a **node**; “knows on a first-name basis” becomes an **edge**. Everything else about them is gone.

---

<!-- _class: mid -->

## Distance

<hr>

<div class="cols">
<div>

The **distance** $d(i,j)$ is the number of *edges* on a shortest route between $i$ and $j$.

Where several routes exist, distance takes the **minimum**. The longer ones remain in the graph; only the shortest sets $d(i,j)$.

</div>
<div class="fig">

![w:520](figures/distance-def.png)
<figcaption>one shortest route, its edges numbered</figcaption>

</div>
</div>

---

## Average path length

<hr>

<div class="cols">
<div>

The average you computed on the sheet has a name. The **average path length** $\bar L$ is the mean of $d(i,j)$ over every pair of nodes.

For the plain chain: $\bar L = 8/3 = 2.67$.

</div>
<div class="fig">

![w:520](figures/apl-chain.png)
<figcaption>one dot per pair; red: the mean</figcaption>

</div>
</div>

---

## Two extra edges

<hr>

<div class="fig">

![w:1000](figures/chain-shortcut.png)
<figcaption>red: the long edge; black: the chord from A to C</figcaption>

</div>

Two extra edges, no new people, and $\bar L$ falls from 2.67 to 1.81 across the 21 pairs. The distant pairs account for the drop; the neighbours were already close.

---

## Diameter

<hr>

<div class="fig">

![w:1000](figures/diameter.png)
<figcaption>red: one of the four worst pairs</figcaption>

</div>

The biggest number in any box is the **diameter**: the largest distance in the network.

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 06</span></div>

## The other half

Short routes are only half of what makes a small world

---

## Local clustering coefficient

<hr>

<div class="cols">
<div>

Three nodes with all three edges present form a **triangle**. On the sheet you counted how many of person 3’s six neighbour pairs are joined.

<div class="formula">

$$ C_i = \frac{\text{edges among } i\text{'s neighbours}}{k_i(k_i-1)/2} $$

</div>

</div>
<div class="fig">

![w:520](figures/ego-clustering.png)
<figcaption>red: the two that exist; gray: the eight that do not</figcaption>

</div>
</div>

<!--
With k neighbours there are k(k-1)/2 pairs; for k = 4 that is the six they counted.
-->

---

## Clustering, in matrix form

<hr>

<div class="cols">
<div>

In Module 01, $(\mathbf{A}^2)_{ij}$ counted walks of length two. A closed 3-walk from $i$ can only be a triangle through $i$, and every triangle can be walked two ways:

<div class="formula">

$$ C_i = \frac{(\mathbf{A}^3)_{ii}}{k_i(k_i-1)} $$

</div>

</div>
<div class="fig">

![w:520](figures/a3-formula.png)
<figcaption>one triangle, degree two</figcaption>

</div>
</div>

<!--
Ask what the diagonal of A cubed counts before you advance. The denominator doubles to match the double-counting.
-->

---

## Averaging over nodes

<hr>

<div class="fig">

![w:1000](figures/cbar-milgram.png)
<figcaption>the seven people from Part One, again</figcaption>

</div>

The **average local clustering** $\bar C = \frac{1}{n}\sum_i C_i$ gives every node the same weight, hub or leaf. $G$ has one friend and so no pairs at all; we count it as zero here.

---

## A windmill

<hr>

<div class="fig">

![w:1000](figures/windmill-cbar.png)
<figcaption>ten blade nodes, one hub</figcaption>

</div>

* Ten nodes with $C_i = 1$ outnumber one hub with $C_i = 1/9$. Would you call this network 92% clustered?

---

## Global clustering

<hr>

Two edges meeting at a node form a **triplet**, counted at that centre node. **Global clustering**, or **transitivity**, is the closed fraction of all triplets: $C = 3 \times \#\text{triangles} \,/\, \#\text{triplets}$.

<div class="fig tight">

![w:1000](figures/transitivity-def.png)
<figcaption>each shaded wedge is one triangle; the 3 counts it once per corner</figcaption>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 06</span></div>

## The yardstick

High and short compared to *what*?

---

## The paradox

<hr>

<div class="fig tight">

![w:1000](figures/paradox.png)
<figcaption>black: your dense local neighbourhood; gray: the long way out</figcaption>

</div>

High clustering means your edges stay local. Local wiring should put the far side of the world many hops away. Facebook measures 4.74.

---

## Erdős–Rényi $G(n,p)$

<hr>

<div class="cols">
<div>

The comparison needs a structureless network of the same size.

Take $n$ nodes and connect each pair independently with probability $p$.

</div>
<div class="fig">

![w:520](figures/er-coin.png)
<figcaption>red: the pairs whose coin came up heads</figcaption>

</div>
</div>

---

## Clustering in a random graph

<hr>

<div class="cols">
<div>

Each neighbour pair is an independent coin, so the linked fraction is $p$, regardless of degree. A node has $n-1$ coins, so $\langle k \rangle = p(n-1)$:

<div class="formula">

$$ C_{\mathrm{rand}} = p = \frac{\langle k \rangle}{n-1} $$

</div>

</div>
<div class="fig">

![w:520](figures/er-clustering.png)
<figcaption>ten pairs, ten independent coins</figcaption>

</div>
</div>

<!--
This is the random town on the sheet, written as a formula: the chance that any two people are friends.
-->

---

## Path length in a random graph

<hr>

The tree you carried down the sheet, solved in general: set $\langle k \rangle^L = n$ and $L_{\mathrm{rand}} \approx \ln n / \ln \langle k \rangle$.

<div class="fig tight">

![w:1000](figures/fanout-solve.png)
<figcaption>red: the world’s population, 8 billion</figcaption>

</div>

---

## Random graphs have short paths and few triangles

<hr>

<div class="cols">
<div>

$C_{\mathrm{rand}} = \langle k \rangle/(n-1)$ falls to zero as the network grows, while $L_{\mathrm{rand}}$ rises only as $\ln n$.

So $\bar L$ on its own establishes nothing. The surprise is both properties at once.

</div>
<div class="fig">

![w:520](figures/free-vs-not.png)
<figcaption>twelve nodes wired at random</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## The small-world index

<hr>

<div class="cols">
<div>

Normalise both ratios against the random baseline. Here $\bar C$ is the average local clustering, not the transitivity.

<div class="formula">

$$ \sigma = \frac{\bar C / C_{\mathrm{rand}}}{\bar L / L_{\mathrm{rand}}} $$

</div>

$\sigma > 1$ is a small world; $\sigma \approx 1$ is random-like.

</div>
<div class="fig">

![w:520](figures/sigma-def.png)
<figcaption>red: the small-world side of 1</figcaption>

</div>
</div>

---

## Three real networks

<hr>

<div class="fig tight">

![w:1000](figures/ws1998-sigma.png)
<figcaption>every network sits far to the right of the random baseline</figcaption>

</div>

Path length is barely 1.2–1.5 times the random baseline. Clustering is 6 to 3000 times it. That gap defines the small-world property.

---

<!-- _class: part -->

<div class="band"><span>Part Five</span><span class="count">05 / 06</span></div>

## The mechanism

“What I cannot create, I do not understand” (Feynman)

---

## Clustering and path length trade off

<hr>

<div class="fig tight">

![w:1000](figures/lattice-vs-random.png)
<figcaption>the two extremes, same nodes and same edge count</figcaption>

</div>

Each extreme has one property and lacks the other. Real networks have both, so the model must lie between them.

<!--
Ringville is the left panel. Grow it and the ring holds C-bar at 0.50 forever while its distances grow linearly; the random baseline does the opposite.
-->

---

## Rewire with probability $p$

<hr>

<div class="cols">
<div>

Walk the lattice edge by edge. With probability $p$, detach one end and reattach it to a node chosen at random.

* $p = 0$ leaves the lattice untouched; $p = 1$ destroys it completely.
* Each red chord is one friendship that now reaches across the ring.

</div>
<div class="fig">

![w:520](figures/ws-rewire.gif)
<figcaption>one rewiring per frame</figcaption>

</div>
</div>

<!-- Note the difference from the sheet: the model moves an edge rather than adding one, so every rewiring destroys triangles. -->

---

<!-- _class: mid -->

## Predict the two curves

<hr>

Sweep $p$ from 0 to 1 and track clustering and path length, each against its lattice value.

<div class="formula">

Do $C$ and $L$ fall together, or does one go first?

</div>

*Sketch both curves in your notes before the next slide.*

---

## The two curves, measured

<hr>

<div class="fig tight">

![w:1000](figures/ws-sweep.png)
<figcaption>measured on 400 nodes, averaged over six runs</figcaption>

</div>

$L$ falls while $C$ is still essentially untouched. A handful of random edges shortens every route, and leaves almost every triangle intact.

---

## The small-world band

<hr>

<div class="fig tight">

![w:1000](figures/ws-band.png)
<figcaption>gold: paths at most half the lattice’s, clustering still four-fifths of it</figcaption>

</div>

By the time the routes have halved, clustering has lost about one per cent. With both conditions imposed, the band spans more than a decade in $p$.

---

## Your turn: drag $p$ yourself

<hr>

<div class="cols">
<div>

In the Module 02 notebook, [go.skojaku.com/m02lab](https://go.skojaku.com/m02lab), sweep $p$ and find the smallest value where $L$ has already fallen and $C$ has not.

Both curves come from the two functions you write there.

</div>
<div class="fig">

![w:520](figures/ws-widget.png)
<figcaption>the ring at fourteen percent rewiring</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Six</span><span class="count">06 / 06</span></div>

## Edge cases

The networks that break the definitions

---

<!-- _class: mid -->

## What if two nodes are not connected?

<hr>

<div class="cols">
<div>

$\bar L$ averages $d(i,j)$ over every pair. This network has pairs with no route between them at all.

*30 seconds: what should the average do with those pairs?*

</div>
<div class="fig">

![w:520](figures/disconnected.png)
<figcaption>ringed: one such pair</figcaption>

</div>
</div>

---

## What the average does with it

<hr>

<div class="cols">
<div>

One unreachable pair makes $\bar L$ infinite, however short everything else is.

So in practice we measure on the **largest connected component**, and say that we did.

It is the convention behind Facebook’s 4.74, which is also an average over their largest component.

</div>
<div class="fig">

![w:520](figures/disconnected-answer.png)
<figcaption>two components, and no edge between them</figcaption>

</div>
</div>

<!--
The other convention is the harmonic mean: average 1/d instead of d, so an unreachable pair contributes 0 rather than infinity. That quantity is called efficiency. Mention it only if someone asks; it needs a visual we do not have here.
-->

---

## Sigma scores Ringville above 1

<hr>

<div class="cols">
<div>

The plain ring has no shortcuts at all, and $\sigma$ still classifies it as a small world: its clustering ratio exceeds its distance ratio.

A ring of a thousand nodes reaches $\sigma \approx 5$; even the 16-node ring scores 1.56, and $\sigma$ increases with $n$.

</div>
<div class="fig">

![w:520](figures/sigma-lt-1-answer.png)
<figcaption>the sixteen-node ring, and the two ratios behind 1.56</figcaption>

</div>
</div>

<!--
Why, and how to repair it, is the optional last section of the notebook: sigma reduces to ln n / ln k on a plain ring, because it compares the town to a coin-flip town and to nothing else.
-->

---

## Module 02 review

<hr>

<div class="cols">
<div class="fig">

![w:520](figures/recap.png)
<figcaption>a lattice with a few shortcuts</figcaption>

</div>
<div>

<div class="note">

All four run in the Module 02 notebook.

</div>

* **Distance:** $d(i,j)$, $\bar L$, diameter
* **Clustering:** $C_i$, $\bar C$, transitivity $C$
* **$\sigma$:** both ratios against a random graph
* **Watts–Strogatz:** shortcuts shorten paths, triangles survive

</div>
</div>

---

## Coming up in Module 03

<hr>

<div class="cols">
<div>

### Robustness

The world is small because of a handful of long edges.

So what happens when they break, by accident or because someone targets them?

</div>
<div class="fig">

![w:520](figures/m03-teaser.png)
<figcaption>three shortcuts, two of them cut</figcaption>

</div>
</div>

---
marp: true
theme: network-science
paginate: true
math: katex
---

<!-- _class: lead -->

<div class="eyebrow">Advanced Topics in Network Science · Module 02</div>

# Six Handshakes

<hr>

<div class="sub">Why the world is smaller than it has any right to be</div>

<div class="credit">Sadamori Kojaku · Binghamton University</div>

<!--
Open with Omaha, not with definitions. The paradox — clustered *and* short — is the spine of the whole module.
-->

---

<!-- _class: mid -->

## Today’s question

<hr>

<div class="formula">

Why is a stranger on the other side of the world only about six handshakes away?

</div>

*Write down your guess for the number now. We come back to it twice.*

---

## Roadmap for today

<hr>

<div class="steps-list">

<div><div class="i">01</div><div>The claim — a letter from Omaha, and 160 envelopes</div></div>
<div><div class="i">02</div><div>Measuring “six” — distance, average path length, diameter</div></div>
<div><div class="i">03</div><div>The other half — triangles and clustering</div></div>
<div><div class="i">04</div><div>The yardstick — a random baseline and the index sigma</div></div>
<div><div class="i">05</div><div>The mechanism — Watts–Strogatz rewiring</div></div>
<div><div class="i">06</div><div>Edge cases — the networks that break the definitions</div></div>

</div>

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

Stanley Milgram mails packets to people picked at random in Omaha, Nebraska and Wichita, Kansas.

Each packet names one target: a stockbroker who works in Boston.

</div>
<div class="fig">

![w:520](figures/milgram-route.png)
<figcaption>Milgram’s experiment: starters in the Midwest, one target near Boston</figcaption>

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

<!-- _class: mid -->

## How many hands?

<hr>

A farmer in Omaha. A stockbroker outside Boston. Nothing in common.

<div class="formula">

How many people end up in the chain?

</div>

*Hands up: two? six? twenty? a hundred?*

---

## 160 packets, and what became of them

<hr>

Of the 160 packets that went out, 64 reached the target. The rest stalled somewhere in the middle of the country.

<div class="fig tight">

![w:1000](figures/milgram-arrivals.png)
<figcaption>red: the 64 completed chains — the only ones that carry data</figcaption>

</div>

---

<!-- _class: mid -->

## The chains that made it

<hr>

<div class="fig">

![w:1000](figures/milgram-chain.png)
<figcaption>one packet’s route, hop by hop</figcaption>

</div>

The median completed chain ran through roughly six links. Not sixty.

---

<!-- _class: mid -->

## Milgram never said “six degrees”

<hr>

<div class="cols">
<div>

The phrase belongs to the playwright **John Guare**, who used it as a title in 1990 — more than twenty years after the experiment.

<div class="note">

Milgram reported a median chain length. The slogan did the rest of the work.

</div>

</div>
<div class="fig">

![w:520](figures/guare.png)
<figcaption>John Guare, who wrote the title — photo David Shankbone, CC BY 3.0</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Does it survive eight billion people?

<hr>

1967: 160 letters, one target, one country.

<div class="formula">

Would the number grow if we ran it on the whole planet?

</div>

*30 seconds with your neighbour — bigger, smaller, or the same?*

---

## Email, 2003

<hr>

<div class="cols">
<div>

A Yahoo study restaged the experiment by email: **more than 24,000 starters**, 18 targets in 13 countries.

* Only **384** chains completed.
* Those averaged about **four** steps.
* Correcting for the chains that died: five to seven.

</div>
<div class="fig">

![w:520](figures/replication-yahoo.png)
<figcaption>the new measurement, in red</figcaption>

</div>
</div>

---

## Facebook, 2012

<hr>

<div class="cols">
<div>

Not a sample this time — the whole graph. **721 million** users and **69 billion** friendships, measured directly.

Average distance between two users: **4.74**.

*Check that against the number you wrote down.*

</div>
<div class="fig">

![w:520](figures/replication-facebook.png)
<figcaption>red: the new measurement, eight hundred times the people</figcaption>

</div>
</div>

---

## Your turn: Wikirace

<hr>

<div class="cols">
<div>

Two random Wikipedia articles. Links only, no search box. Fewest clicks wins.

Play at [wiki-race.com](https://wiki-race.com) — one round, then shout out your click count.

</div>
<div class="fig">

![w:520](figures/wikirace.png)
<figcaption>a route found by clicking, not by planning</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## What did you just do?

<hr>

You found a short route through a network of seven million articles — without ever seeing the network.

<div class="formula">

Is *finding* a short route the same as one *existing*?

</div>

*30 seconds.*

---

## What Milgram’s subjects actually did

<hr>

<div class="fig tight">

![w:1000](figures/routing-vs-existence.png)
<figcaption>red: a route that exists — the dashed box is everything the start node can actually see</figcaption>

</div>

Milgram’s subjects had no map. They **routed** on local knowledge alone, which is a harder thing than short routes merely existing.

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

Not kilometres. Not people. Edges.

</div>
<div class="fig">

![w:520](figures/distance-def.png)
<figcaption>one shortest route, its edges numbered</figcaption>

</div>
</div>

---

## What is $d(A,G)$?

<hr>

<div class="fig">

![w:1000](figures/chain-blank.png)
<figcaption>ringed: the two ends of the chain</figcaption>

</div>

*Count the edges out loud, together.*

---

## Count them, edge by edge

<hr>

<div class="fig">

![w:1000](figures/distance-six.png)
<figcaption>six edges from end to end</figcaption>

</div>

Six edges, seven people. That is the number you wrote down at the start — and the shape the phrase “six degrees” describes.

---

## A shortcut appears

<hr>

<div class="fig">

![w:1000](figures/chain-chord.png)
<figcaption>red: one edge that was there all along</figcaption>

</div>

It turns out the farmer already knew the teacher. One extra edge, no new people.

---

## Two routes, one distance

<hr>

<div class="cols">
<div>

Now there are two ways from $A$ to $C$ — one edge, or two.

Distance takes the **minimum**. The longer route still exists; it just does not count.

</div>
<div class="fig">

![w:520](figures/two-routes.png)
<figcaption>red: the shorter route</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## One number for the whole network

<hr>

Seven people make 21 pairs, and every pair has its own distance.

<div class="formula">

What single number would you report?

</div>

*30 seconds with your neighbour.*

---

## Average path length

<hr>

<div class="cols">
<div>

The **average path length** $\bar L$ is the mean of $d(i,j)$ over every pair of nodes.

For the plain chain: $\bar L = 8/3 = 2.67$.

</div>
<div class="fig">

![w:520](figures/apl-chain.png)
<figcaption>one dot per pair — red: the mean</figcaption>

</div>
</div>

---

## One more shortcut

<hr>

<div class="fig">

![w:1000](figures/chain-shortcut.png)
<figcaption>black: the chord from two slides ago — red: the new long edge</figcaption>

</div>

A second long edge, again with no new people. This is the whole small-world story in miniature.

---

## The average collapses

<hr>

<div class="cols">
<div>

Two extra edges out of 21 pairs, and $\bar L$ falls from 2.67 to 1.81.

<div class="note">

Notice which pairs moved: the far ones. The neighbours were already close.

</div>

</div>
<div class="fig">

![w:520](figures/apl-shortcut.png)
<figcaption>same axis as before — the tail is gone</figcaption>

</div>
</div>

---

## Diameter

<hr>

<div class="fig">

![w:1000](figures/diameter.png)
<figcaption>red: one of the four worst pairs</figcaption>

</div>

The **diameter** is the largest distance in the network — the worst case, not the average.

---

## Your turn: worksheet A

<hr>

<div class="fig">

![w:1000](figures/worksheet-a.png)
<figcaption>the acquaintance network, unlabelled</figcaption>

</div>

On paper: the three distances above, then the diameter of the whole network. *Four minutes.*

---

## Worksheet A — check

<hr>

<div class="fig">

![w:1000](figures/worksheet-a-answer.png)
<figcaption>the four answers, on the network</figcaption>

</div>

The diameter is the largest distance in the whole network — not the largest of the three you just computed.

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 06</span></div>

## The other half

Short routes are only half of what makes a small world

---

<!-- _class: mid -->

## Do your friends know each other?

<hr>

Pick two of your friends at random.

<div class="formula">

What are the odds that those two know each other?

</div>

*Compare with your neighbour — is your answer near zero, or nowhere near?*

---

<!-- _class: mid -->

## Triangles

<hr>

<div class="cols">
<div>

Three nodes, all three edges present: a **triangle**.

</div>
<div class="fig">

![w:520](figures/triangle-only.png)
<figcaption>the smallest closed thing a network can hold</figcaption>

</div>
</div>

---

## Open and closed triplets

<hr>

<div class="cols">
<div>

Two edges meeting at a node form a **triplet**, counted at that shared **centre** node.

Closed if the third edge is there, open if it is not.

</div>
<div class="fig">

![w:520](figures/triangle-triplet.png)
<figcaption>ringed: the centre node of each triplet</figcaption>

</div>
</div>

---

## Counting a triangle’s triplets

<hr>

<div class="fig">

![w:1000](figures/triplet-three-corners.png)
<figcaption>ringed: the triplet’s centre</figcaption>

</div>

Which is why counting triangles network-wide multiplies each one by three.

---

## One neighbourhood

<hr>

<div class="cols">
<div>

Node $A$ has five friends.

The question is not about $A$’s edges. It is about the edges among those five.

</div>
<div class="fig">

![w:520](figures/ego-graph.png)
<figcaption>five friends, no links between them drawn yet</figcaption>

</div>
</div>

---

## How many pairs could be linked?

<hr>

<div class="cols">
<div>

Every dashed line is a friendship that *could* exist among $A$’s five friends.

*Take 20 seconds — no formula, just count.*

</div>
<div class="fig">

![w:520](figures/ego-pairs.png)
<figcaption>count them</figcaption>

</div>
</div>

---

## Every pair that could exist

<hr>

<div class="cols">
<div>

With $k$ friends there are

$$ \binom{k}{2} = \frac{k(k-1)}{2} $$

possible edges among them.

</div>
<div class="fig">

![w:520](figures/ego-pairs-count.png)
<figcaption>the dashed lines are possibilities, not edges</figcaption>

</div>
</div>

---

## Local clustering coefficient

<hr>

<div class="cols">
<div>

<div class="formula">

$$ C_i = \frac{\text{edges among } i\text{'s neighbours}}{k_i(k_i-1)/2} $$

</div>

* Count the edges that do exist among the neighbours, then divide by every pair that could have been there.

</div>
<div class="fig">

![w:520](figures/ego-clustering.png)
<figcaption>red: the two that exist — gray: the eight that do not</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Back to the matrix

<hr>

In Module 01 we found that $(\mathbf{A}^2)_{ij}$ counts walks of length two from $i$ to $j$.

<div class="formula">

So what does the *diagonal* entry $(\mathbf{A}^3)_{ii}$ count?

</div>

*30 seconds.*

---

## Walking back to where you started

<hr>

<div class="cols">
<div>

A closed 3-walk from $i$ can only be a triangle through $i$ — and every triangle can be walked two ways.

</div>
<div class="fig">

![w:520](figures/a3-walks.png)
<figcaption>two closed walks, one arrow each way round</figcaption>

</div>
</div>

---

## Clustering, in matrix form

<hr>

<div class="cols">
<div>

Each triangle is counted twice, and the denominator doubles to match:

<div class="formula">

$$ C_i = \frac{(\mathbf{A}^3)_{ii}}{k_i(k_i-1)} $$

</div>

</div>
<div class="fig">

![w:520](figures/a3-formula.png)
<figcaption>one triangle, degree two</figcaption>

</div>
</div>

---

## Averaging over nodes

<hr>

<div class="fig">

![w:1000](figures/cbar-milgram.png)
<figcaption>the seven people from Part One, again</figcaption>

</div>

The **average local clustering** $\bar C = \frac{1}{n}\sum_i C_i$ gives every node the same weight — hub or leaf. $G$ has one friend and so no pairs at all; we count it as zero here.

---

## A windmill

<hr>

<div class="fig">

![w:1000](figures/windmill-cbar.png)
<figcaption>ten blade nodes, one hub</figcaption>

</div>

* Every blade node sees a perfectly closed neighbourhood; the hub sees almost none.

---

<!-- _class: mid -->

## Is 0.92 a fair summary?

<hr>

Ten nodes with $C_i = 1$ outvote one hub with $C_i = 1/9$.

<div class="formula">

Would you call this network 92% clustered?

</div>

*Turn to your neighbour. What is the average hiding?*

---

## Global clustering

<hr>

Count objects instead of averaging nodes: $C = 3 \times \#\text{triangles} \,/\, \#\text{triplets}$.

<div class="fig tight">

![w:1000](figures/transitivity-def.png)
<figcaption>each shaded wedge is one triangle; the 3 counts it once per corner</figcaption>

</div>

---

## Two answers, one network

<hr>

<div class="fig">

![w:1000](figures/windmill-split.png)
<figcaption>gray: the node-weighted answer — red: the triplet-weighted one</figcaption>

</div>

* $\bar C$ weights nodes: the blades outvote the hub.
* $C$ weights triplets: the hub owns most of them.

---

## Your turn: worksheet B

<hr>

<div class="fig">

![w:1000](figures/worksheet-b.png)
<figcaption>the same acquaintance network</figcaption>

</div>

On paper: the local clustering coefficient of the three nodes named above. *Four minutes.*

---

## Worksheet B — check

<hr>

<div class="fig">

![w:1000](figures/worksheet-b-answer.png)

</div>

* $C_A = 1$ — both of $A$’s friends know each other
* $C_B = 1/3$ — one of $B$’s three pairs is closed
* $C_D = 0$ — $D$’s friends are strangers

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
<figcaption>black: your dense local neighbourhood — gray: the long way out</figcaption>

</div>

High clustering means your edges stay local. Local wiring should put the far side of the world many, many hops away. Facebook measures 4.74.

---

<!-- _class: mid -->

## Score it naively

<hr>

Small-world means high $\bar C$ and low $\bar L$, so try the obvious index:

<div class="formula">

$$ s = \bar C / \bar L \qquad \text{high is small-world?} $$

</div>

*30 seconds: find a network that breaks this.*

---

## Score the complete graph

<hr>

<div class="cols">
<div>

Join every pair, and the naive index hits $s = 1$ — the largest value it can take.

For the least interesting network there is.

</div>
<div class="fig">

![w:520](figures/complete-graph.png)
<figcaption>maximum score, zero insight</figcaption>

</div>
</div>

---

## Erdős–Rényi $G(n,p)$

<hr>

<div class="cols">
<div>

So we need a structureless network of the same size to compare against.

Take $n$ nodes and connect each pair independently with probability $p$.

</div>
<div class="fig">

![w:520](figures/er-coin.png)
<figcaption>red: the pairs whose coin came up heads</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## What is $C_i$ in a random graph?

<hr>

Node $i$ has $k$ neighbours, so $k(k-1)/2$ pairs among them.

<div class="formula">

What fraction of those pairs do you expect to be linked?

</div>

*30 seconds. Does the answer depend on $k$?*

---

## One coin per pair

<hr>

<div class="cols">
<div>

Each neighbour pair is its own independent coin, with the same $p$ as every other pair.

So the fraction of them you expect to be linked is just $p$ — whatever the degree.

<div class="formula">

$$ C_{\mathrm{rand}} = p $$

</div>

</div>
<div class="fig">

![w:520](figures/er-clustering.png)
<figcaption>ten pairs, ten independent coins</figcaption>

</div>
</div>

---

## From $p$ to a number you can measure

<hr>

<div class="cols">
<div>

A node has $n-1$ coins of its own, one for every other node, so its **average degree** is $\langle k \rangle = p(n-1)$.

Turn that around and the baseline is written in something you can count on a real network:

<div class="formula">

$$ C_{\mathrm{rand}} = \frac{\langle k \rangle}{n-1} $$

</div>

</div>
<div class="fig">

![w:520](figures/er-coin.png)
<figcaption>the same coins, counted one node at a time</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## How far can 150 friends reach?

<hr>

Everyone on Earth has about 150 acquaintances, wired at random.

<div class="formula">

After $L$ steps, how many people have you reached?

</div>

*30 seconds — say it as a formula, not a number.*

---

## The fan-out

<hr>

<div class="fig tight">

![w:1000](figures/fanout.png)
<figcaption>one step reaches k friends, two steps k squared</figcaption>

</div>

In a sparse random graph you almost never come back to someone you have met, so the count multiplies at every step.

---

## Where the fan-out meets eight billion

<hr>

Set $\langle k \rangle^L = n$ and solve: $L_{\mathrm{rand}} \approx \ln n / \ln \langle k \rangle$.

<div class="fig tight">

![w:1000](figures/fanout-solve.png)
<figcaption>red: the world’s population, at 150 friends each</figcaption>

</div>

---

## Short is free. Clustered is not.

<hr>

<div class="cols">
<div>

Randomness hands you short routes for nothing — and hands you almost no triangles, because $C_{\mathrm{rand}} = \langle k \rangle/(n-1)$ goes to zero as the network grows.

That is why the two properties together are surprising, and why $\bar L$ alone proves nothing.

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

Normalise both halves against that random baseline. The $\bar C$ here is the average local clustering, not the transitivity.

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

## Your turn: three real networks

<hr>

<div class="fig tight">

![w:1000](figures/ws1998-dots.png)
<figcaption>gray: the path-length ratio — red: the clustering ratio, log axis</figcaption>

</div>

Pick one row. Read both ratios off the axis and compute $\sigma$ yourself. *Two minutes.*

---

## Your $\sigma$, checked

<hr>

<div class="fig tight">

![w:1000](figures/ws1998-sigma.png)
<figcaption>every network sits far to the right of the random baseline</figcaption>

</div>

Path length is barely 1.2–1.5 times the random baseline. Clustering is 6 to 3000 times it. That gap *is* the small-world property.

---

<!-- _class: part -->

<div class="band"><span>Part Five</span><span class="count">05 / 06</span></div>

## The mechanism

“What I cannot create, I do not understand” — Feynman

---

<!-- _class: mid -->

## Could you build one?

<hr>

Measuring a property is not explaining it. So build a network that has both.

<div class="formula">

High clustering *and* short routes. What is your first move?

</div>

*Turn to your neighbour — 60 seconds, then we try the two obvious answers.*

---

## Obvious answer 1: wire locally

<hr>

<div class="cols">
<div>

Put $n$ nodes on a ring and join each to its **4 nearest neighbours**. Neighbours share neighbours, so triangles are everywhere.

$\bar C = 0.5$ — as clustered as a real friendship network.

</div>
<div class="fig">

![w:520](figures/ring-lattice.png)
<figcaption>every edge is short</figcaption>

</div>
</div>

---

## Now walk across it

<hr>

<div class="cols">
<div>

Crossing a ring lattice means walking around it, two nodes at a time.

* 16 nodes: 4 hops to the far side.
* 1000 nodes: $\bar L \approx 125$.
* Distance grows linearly with $n$ — the opposite of what we measured.

</div>
<div class="fig">

![w:520](figures/ring-distance.png)
<figcaption>red: the longest shortest route</figcaption>

</div>
</div>

---

## Obvious answer 2: wire at random

<hr>

<div class="cols">
<div>

Same nodes, same number of edges, shuffled.

* Routes get short immediately, and the clustering falls with them: 0.50 to 0.24 — at sixteen nodes, only a halving.
* Grow the network and the random baseline goes to nothing, while the ring stays at 0.50 forever.

</div>
<div class="fig">

![w:520](figures/random-graph.png)
<figcaption>short routes, and half the closure</figcaption>

</div>
</div>

---

## The trade-off

<hr>

<div class="fig tight">

![w:1000](figures/lattice-vs-random.png)
<figcaption>the two extremes, same nodes and same edge count</figcaption>

</div>

Each extreme buys one property with the other. Real networks refuse to choose — so the answer must be somewhere in between.

---

<!-- _class: mid -->

## How would you cheat?

<hr>

You are holding the lattice. You want to keep its triangles and shorten its routes.

<div class="formula">

What is the cheapest edit you can make?

</div>

*30 seconds — how many edges would you touch?*

---

## Rewire with probability $p$

<hr>

<div class="cols">
<div>

Walk the lattice edge by edge. With probability $p$, detach one end and reattach it to a node chosen at random.

* $p = 0$ leaves the lattice untouched.
* $p = 1$ destroys it completely.

</div>
<div class="fig">

![w:520](figures/ws-rewire-step.png)
<figcaption>one edge moved, the rest untouched</figcaption>

</div>
</div>

---

## Watch it happen

<hr>

<div class="cols">
<div>

Six edges move. The ring survives; a handful of long chords now cut across it.

<div class="note">

Each red chord is one friendship that happens to reach far — the friend who moved abroad.

</div>

</div>
<div class="fig">

![w:520](figures/ws-rewire.gif)
<figcaption>one rewiring per frame</figcaption>

</div>
</div>

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

$L$ collapses while $C$ is still essentially untouched. A few random edges are enough to shorten everything, and far too few to break the triangles.

---

## The small-world band

<hr>

<div class="fig tight">

![w:1000](figures/ws-band.png)
<figcaption>gold: paths at most half the lattice’s, clustering still four-fifths of it</figcaption>

</div>

By the time the routes have halved, clustering has lost about one per cent. Ask for both at once — paths at most half, clustering still four-fifths — and the band spans a factor of five in $p$.

---

## Why shortcuts are so cheap

<hr>

<div class="cols">
<div>

One long edge serves an entire arc of nodes at once, and it costs at most a couple of triangles.

That asymmetry is the whole mechanism.

</div>
<div class="fig">

![w:520](figures/shortcut-effect.png)
<figcaption>the lattice underneath is untouched</figcaption>

</div>
</div>

---

## Your turn: drag $p$ yourself

<hr>

<div class="cols">
<div>

Open the Watts–Strogatz widget in the Module 02 notebook and sweep $p$ by hand.

Find the smallest $p$ where $L$ has already collapsed and $C$ has not.

</div>
<div class="fig">

![w:520](figures/ws-widget.png)
<figcaption>the ring at fourteen percent rewiring</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Six</span><span class="count">06 / 06</span></div>

## Edge cases, and what survives them

The networks that break the definitions — and the one signature that does not break

---

<!-- _class: mid -->

## What if two nodes are not connected?

<hr>

<div class="cols">
<div>

$\bar L$ averages $d(i,j)$ over every pair. This network has pairs with no route between them at all.

*30 seconds — what should the average do with those pairs?*

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

It is the convention behind Facebook’s 4.74 — that average is over their largest component too.

</div>
<div class="fig">

![w:520](figures/disconnected-answer.png)
<figcaption>two components, and no edge between them</figcaption>

</div>
</div>

<!--
The other convention is the harmonic mean — average 1/d instead of d, so an unreachable pair contributes 0 rather than infinity. That quantity is called efficiency. Mention it only if someone asks; it needs a visual we do not have here.
-->

---

<!-- _class: mid -->

## The zero we have been using

<hr>

<div class="cols">
<div>

$C_i$ divides by $k_i(k_i-1)/2$ — the number of pairs among the neighbours.

We have been counting degree-one nodes as zero since Part Three.

*Is that a fact, or a choice? 30 seconds with your neighbour.*

</div>
<div class="fig">

![w:520](figures/degree-one.png)
<figcaption>ringed: degree one</figcaption>

</div>
</div>

---

## Look at the denominator

<hr>

<div class="cols">
<div>

No pairs among the neighbours, so numerator and denominator are both zero. $C_i$ is genuinely **undefined**.

* The usual convention: set it to zero.
* That drags $\bar C$ down in networks full of leaves.

</div>
<div class="fig">

![w:520](figures/degree-one-answer.png)
<figcaption>a leaf — and real networks are full of them</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Is any real network anti-small-world?

<hr>

<div class="cols">
<div>

$\sigma < 1$ needs long routes *and* clustering below the random baseline.

The ring lattice has the long routes. Is it enough?

*30 seconds — which half of the ratio wins?*

</div>
<div class="fig">

![w:520](figures/sigma-lt-1-q.png)
<figcaption>sixteen nodes, four neighbours each</figcaption>

</div>
</div>

---

## Score the ring lattice

<hr>

<div class="cols">
<div>

$\sigma > 1$: the ring lattice’s clustering advantage beats its distance penalty.

$\sigma \approx 5$ for a ring of a thousand nodes; even the 16-node ring scores 1.56.

</div>
<div class="fig">

![w:520](figures/sigma-lt-1-answer.png)
<figcaption>clustering wins the ratio, even here</figcaption>

</div>
</div>

---

## You have to kill the triangles

<hr>

<div class="cols">
<div>

You need clustering under the random baseline — and random is already near zero.

<div class="formula">

Count the triplets centred on one intersection. How many are closed?

</div>

*60 seconds on paper.*

</div>
<div class="fig">

![w:520](figures/grid-q.png)
<figcaption>gold: the intersection to count around</figcaption>

</div>
</div>

---

## What the six triplets do

<hr>

<div class="cols">
<div>

An intersection has four neighbours, so $\binom{4}{2} = 6$ triplets are centred on it — and no two of those four are joined to each other.

Nothing closes. $C = 0$, and $\sigma = 0$ with it.

</div>
<div class="fig">

![w:520](figures/grid-answer.png)
<figcaption>red: the four edges whose pairs are the six triplets</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## $G(n,m)$ or $G(n,p)$ — the same thing?

<hr>

<div class="fig tight">

![w:1000](figures/gnm-gnp.png)
<figcaption>two recipes for “a random graph”</figcaption>

</div>

*30 seconds: does it matter which one you normalise against?*

---

## Where the two recipes part

<hr>

<div class="fig tight">

![w:1000](figures/gnm-gnp-answer.png)
<figcaption>dashed: the pairs whose coin came up tails</figcaption>

</div>

Fix $m$ and the edges stop being independent: using one up makes the rest less likely — and independence is what let us write $C_{\mathrm{rand}} = p$.

---

## The same signature everywhere

<hr>

<div class="fig tight">

![w:1000](figures/universality.png)
<figcaption>the three networks of Watts and Strogatz, by domain</figcaption>

</div>

Film collaborations, a power grid, and a worm’s nervous system. Nothing social connects them — and all three are small worlds.

---

## One map

<hr>

<div class="fig tight">

![w:1000](figures/sw-map.png)
<figcaption>red: the rewired edges</figcaption>

</div>

Turn $p$ up from zero: the lattice keeps its triangles long after its routes have collapsed. The whole module sits on that one axis.

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

Measure $\bar L$, $\bar C$ and $\sigma$ on a real network in the Module 02 notebook.

</div>

* **Distance:** $d(i,j)$, then $\bar L$ and the diameter
* **Clustering:** $C_i$, then $\bar C$ and transitivity $C$
* **$\sigma$:** both halves against a random graph of the same size
* **Watts–Strogatz:** a few shortcuts buy short routes

</div>
</div>

---

## Coming up in Module 03

<hr>

<div class="cols">
<div>

### Robustness

The world is small because of a handful of long edges.

So what happens when they break — by accident, or because someone picked them out?

</div>
<div class="fig">

![w:520](figures/m03-teaser.png)
<figcaption>three shortcuts, two of them cut</figcaption>

</div>
</div>

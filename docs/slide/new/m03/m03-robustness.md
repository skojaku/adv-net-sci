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

<div class="sub">The cheapest grid is the easiest one to destroy</div>

<div class="credit">Sadamori Kojaku · Binghamton University</div>

<!--
Open with Moravia, not with definitions. The whole module is one story told three times: build the cheapest grid, break it, work out the law that governs the breaking.
-->

---

<!-- _class: mid -->

## The question for today

<hr>

<div class="formula">

How much of a network can you destroy before it falls apart — and does it matter whether the damage is random or deliberate?

</div>

Hold a guess. A number, out loud, before we start.

<!--
Do not answer this. Part Five answers it with one formula; Part Six shows the answer depends entirely on who is doing the damage.
-->

---

## Roadmap for today

<hr>

<div class="steps-list">

<div><div class="i">01</div><div>The cheapest grid — Moravia, 1926, and the minimum spanning tree</div></div>
<div><div class="i">02</div><div>Greedy — Kruskal, Prim, and why the obvious rule wins here</div></div>
<div><div class="i">03</div><div>Break it — one town goes dark, and the grid splits</div></div>
<div><div class="i">04</div><div>Percolation — puddles, and a transition that arrives all at once</div></div>
<div><div class="i">05</div><div>The formula — $\kappa$, branching, and the critical fraction $f_c$</div></div>
<div><div class="i">06</div><div>Robust yet fragile — and what you would build instead</div></div>
<div><div class="i">07</div><div>Edge cases — the graphs that test the law</div></div>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 07</span></div>

## The cheapest grid

Post-war Moravia has no electricity and no money

---

## Moravia, 1919

<hr>

Czechoslovakia is one year old. Its eastern lands are dark, and every crown spent on cable is a crown not spent on a hospital.

<div class="fig">

![w:1100](figures/moravia-dark.png)
<figcaption>eight towns, no grid, no budget</figcaption>

</div>

<!--
Real place, real date. The engineers at the West Moravian Power Company have to connect all of these towns and cannot afford a metre of spare cable.
-->

---

## The problem reaches a mathematician

<hr>

<div class="cols">
<div>

A friend at the West Moravian Power Company carries the question to **Otakar Borůvka**.

His 1926 paper *O jistém problému minimálním* is the first solution — and the birth of the **minimum spanning tree** problem.

<div class="note">

We come back to how *he* solved it at the end of Part Two.

</div>

</div>
<div class="fig">

![w:520](figures/boruvka-portrait.png)
<figcaption>Otakar Borůvka, 1899–1995</figcaption>

</div>
</div>

---

## Erase the map

<hr>

Rivers, roads, borders, town size — none of it changes which cables you should lay. Keep the towns.

<div class="fig">

![w:1100](figures/abstract-1.png)
<figcaption>eight dots is all the geography we need</figcaption>

</div>

---

## Draw what could be built

<hr>

Not every pair of towns is worth a cable. Thirteen routes are plausible — the rest run through mountains or double back.

<div class="fig">

![w:1100](figures/abstract-2.png)
<figcaption>thirteen candidate routes</figcaption>

</div>

---

## Each route has a price

<hr>

Put the kilometres on the line. Edges now carry numbers: this is a **weighted network**.

<div class="fig">

![w:1100](figures/abstract-3.png)
<figcaption>weight = kilometres of cable</figcaption>

</div>

---

<!-- _class: mid -->

## The engineer's question

<hr>

<div class="formula">

Connect all eight towns. Which cables do you lay, and what is the least total length?

</div>

<div class="fig">

![w:1100](figures/moravia-graph.png)

</div>

<!--
Do not reveal 292 here. Let them work it in the next slide and hold their own number until Part Two.
-->

---

## Your turn

<hr>

Five minutes. Draw a set of cables that connects all eight towns, add up the kilometres, and keep your number to yourself.

<div class="fig">

![w:1100](figures/moravia-graph.png)
<figcaption>your grid, your total</figcaption>

</div>

<!--
Collect a few totals on the board without judging them. The spread is the point: some will be near 292, some far above.
-->

---

## What everyone notices first

<hr>

<div class="cols">
<div>

If your cables ever form a **loop**, one of them is doing nothing: cut it and every town is still connected.

So the cheapest answer has **no loops at all**.

</div>
<div class="fig">

![w:520](figures/loop-waste.png)
<figcaption>cut it — still connected</figcaption>

</div>
</div>

---

## A tree

<hr>

<div class="cols">
<div>

A **tree** is a network that is connected and has no cycle.

Between any two nodes there is exactly one route — no choices, no spares.

</div>
<div class="fig">

![w:520](figures/tree-def.png)
<figcaption>one route between any two</figcaption>

</div>
</div>

---

## Seven cables, always

<hr>

A **spanning tree** touches every node. For $n$ towns it has exactly $n - 1$ cables — count them.

<div class="fig">

![w:1100](figures/spanning-count.png)
<figcaption>8 towns, 7 cables — the count is forced</figcaption>

</div>

<!--
The number of cables is not a design choice. Only WHICH seven is.
-->

---

## Minimum spanning tree

<hr>

Of all the spanning trees, the one with the least total weight is the **minimum spanning tree**.

<div class="fig">

![w:1100](figures/mst-def.png)
<figcaption>the cheapest way to keep everyone connected</figcaption>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 07</span></div>

## Greedy

Take the cheapest thing that is not stupid, and repeat

---

## Kruskal's rule

<hr>

Sort every route by price. Walk the list from the cheapest and take each cable — unless it would close a loop, in which case skip it. *Joseph Kruskal, 1956.*

<div class="fig">

![w:1100](figures/kruskal-rule.png)
<figcaption>thirteen routes, cheapest first</figcaption>

</div>

---

## Kruskal, running

<hr>

<div class="fig">

![w:1100](figures/kruskal.gif)
<figcaption>watch the sixth decision</figcaption>

</div>

<!--
Let the loop run twice before saying anything. Ask what happened at 51 km.
-->

---

## The one it refuses

<hr>

Olomouc–Zlín is 51 km and it is next on the list. But both of its ends are already connected to each other, so the cable would buy nothing.

<div class="fig">

![w:1100](figures/kruskal-skip.png)
<figcaption>the loop it would have closed</figcaption>

</div>

<!--
This single skip IS the algorithm. Everything else is "take the cheapest".
-->

---

## Your turn

<hr>

Run Kruskal by hand. Write down the order you take the cables in, mark the one you refuse, and total the kilometres.

<div class="fig">

![w:1100](figures/kruskal-worksheet.png)
<figcaption>your list, in order</figcaption>

</div>

---

## The order — and the answer to the question

<hr>

17, 29, 42, 48, 49, **skip 51**, 53, 54. Seven cables, **292 km** — and no grid on any of your sheets is cheaper.

<div class="fig">

![w:1100](figures/kruskal-answer.png)
<figcaption>the order it was built in</figcaption>

</div>

---

## Prim's rule

<hr>

Start at the Brno power plant. Repeatedly buy the cheapest cable that reaches **one new town**. *Jarník 1930 · Prim 1957.*

<div class="fig">

![w:1100](figures/prim-rule.png)
<figcaption>six ways out of Brno; take the cheapest</figcaption>

</div>

<!--
Jarník was also Czech, and published this in 1930 after reading Boruvka. Prim rediscovered it in 1957.
-->

---

## Prim, running

<hr>

<div class="fig">

![w:1100](figures/prim.gif)
<figcaption>one blob, growing outward from the plant</figcaption>

</div>

<!--
Contrast with Kruskal: there, several disconnected fragments grew at once. Here there is always exactly one connected region.
-->

---

## Your turn

<hr>

Run Prim from Brno. Write the order the cables enter in — then compare it with your Kruskal list.

<div class="fig">

![w:1100](figures/prim-worksheet.png)
<figcaption>start at Brno</figcaption>

</div>

---

## Different order, same tree

<hr>

Prim takes 48, 17, 49, 53, 29, 42, 54. Kruskal took them in a different order — and landed on the **same seven cables**.

<div class="fig">

![w:1100](figures/prim-vs-kruskal.png)
<figcaption>two routes to one answer</figcaption>

</div>

---

<!-- _class: mid -->

## Greedy is usually wrong

<hr>

Take the cheapest thing available and you get a bad answer to almost every problem — packing a bag, planning a trip, scheduling a factory.

<div class="formula">

So why can it not be beaten here?

</div>

Thirty seconds. Argue it with the person next to you.

---

## Here it cannot be beaten

<hr>

<div class="cols">
<div>

Cut the towns into any two groups. The cheapest cable crossing that cut **must** be in the minimum spanning tree — swap it in and any tree without it gets cheaper.

Both rules only ever take such a cable. That is the whole proof.

</div>
<div class="fig">

![w:520](figures/cut-property.png)
<figcaption>the cheapest cable across any cut is safe</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## What if two cables cost the same?

<hr>

Suppose the survey comes back and Olomouc–Zlín is 49 km, exactly the same as Prostějov–Zlín.

<div class="formula">

Is there still one cheapest grid?

</div>

<div class="fig">

![w:1100](figures/tie-graph.png)

</div>

---

## Two cheapest grids

<hr>

Six cables are in both. Then the tie: take either one, and the total is **292 km** either way. Which one an algorithm hands you depends on how it breaks the tie.

<div class="fig">

![w:1100](figures/tie-two-trees.png)
<figcaption>six shared cables, then a coin toss</figcaption>

</div>

<!--
All weights distinct implies a unique MST; ties imply several optima of equal cost. Both algorithms return one of them.
-->

---

<!-- _class: mid -->

## And Borůvka himself?

<hr>

Neither of these is his. In 1926 there is no computer, no sorted list of thirteen numbers, and no notion of an "algorithm" to lean on.

<div class="formula">

What would you do, with eight towns and a pencil?

</div>

---

## Every town at once

<hr>

Each piece of the network looks at its own cheapest way out and takes it — **all of them simultaneously** — and the pieces merge. Repeat.

<div class="fig">

![w:1100](figures/boruvka.gif)
<figcaption>no ordering, no queue, no waiting</figcaption>

</div>

---

## Two rounds, not seven steps

<hr>

Round one chooses six cables at the same time. Round two chooses the last. Kruskal and Prim need seven sequential decisions for the same tree.

<div class="fig">

![w:1100](figures/boruvka-rounds.png)
<figcaption>the parallel one — which is why it came back</figcaption>

</div>

<!--
Boruvka's algorithm is the one that survives on modern parallel hardware, ninety years after a pencil-and-paper problem in Moravia.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 07</span></div>

## Break it

The bill is paid, the grid is up, and now things start to fail

---

## The grid, finished

<hr>

292 kilometres of cable, eight towns, seven lines. This is what 1926 would have built.

<div class="fig">

![w:1100](figures/mst-alone.png)
<figcaption>optimal, and complete</figcaption>

</div>

---

<!-- _class: mid -->

## Which town, gone dark, hurts most?

<hr>

A transformer fails and one town drops off the grid, taking its cables with it.

<div class="formula">

Pick the town you would least like to lose. Hands up for yours.

</div>

<div class="fig">

![w:1100](figures/mst-blank.png)

</div>

<!--
Run this as a real poll. Count hands for Brno, Prostejov, Trebic, and "a leaf". Write the tally on the board before the next slide.
-->

---

## Brno

<hr>

Lose Brno and eight towns become **three, three and one**. No survivor can reach two-thirds of the others.

<div class="fig">

![w:1100](figures/brno-removed.png)
<figcaption>3 + 3 + 1</figcaption>

</div>

---

## Every cable is a bridge

<hr>

A tree has exactly one route between any two towns. So every single cable, and every town on that route, is a single point of failure. This is not bad luck — it is what "cheapest" bought.

<div class="fig">

![w:1100](figures/tree-bridges.png)
<figcaption>Jihlava to Zlín: one route, no spare</figcaption>

</div>

---

## Real grids are not trees

<hr>

Every transmission network you have ever depended on is **meshed**: cut any one line and the power arrives by another.

<div class="fig">

![w:1100](figures/real-grid-mesh.png)
<figcaption>redundancy is what everyone actually builds</figcaption>

</div>

---

## Measuring the damage

<hr>

**Connectivity** = size of the largest surviving piece ÷ original number of nodes. Losing Brno scores $3/8 = 0.375$; losing a leaf scores $7/8$.

<div class="fig">

![w:1100](figures/connectivity-def.png)
<figcaption>one number for "how bad"</figcaption>

</div>

---

<!-- _class: mid -->

## Keep going

<hr>

Do not stop at one town. Remove them one at a time, and after each removal measure the connectivity again.

<div class="formula">

Sketch the curve before we draw it. Does it slide, or does it fall off a cliff?

</div>

---

## The robustness profile

<hr>

<div class="fig">

![w:1100](figures/profile-build.gif)
<figcaption>connectivity against the fraction removed</figcaption>

</div>

Damage is a **curve**, not a number.

<!--
Pause on the first two frames: the first removal costs more than the next four put together.
-->

---

## One curve, one number

<hr>

The **R-index** is the area under the profile: $R = \frac{1}{N}\sum_k y_k$. High area, robust network. This attack scores $R = 0.17$.

<div class="fig">

![w:1100](figures/r-index.png)
<figcaption>the whole curve, compressed to one comparable number</figcaption>

</div>

---

<!-- _class: mid -->

## Does the order matter?

<hr>

Same grid. Same number of towns removed. Only the **order** is different.

<div class="formula">

How far apart can two curves on the same network be?

</div>

Guess a factor before we look.

---

## Random failure

<hr>

Earthquakes, floods and broken transformers do not read the map. They hit leaves as often as hubs, and the grid degrades gently: $R = 0.41$.

<div class="fig">

![w:1100](figures/profile-random.png)
<figcaption>unlucky, but not targeted</figcaption>

</div>

---

## Targeted attack

<hr>

An adversary who can see the map takes Brno first, then the next-best connected town. Same grid, same removals, $R = 0.17$ — **2.4× the damage**.

<div class="fig">

![w:1100](figures/profile-both.png)
<figcaption>the gap between bad luck and bad intent</figcaption>

</div>

---

<!-- _class: mid -->

## Fix the hit list, or re-measure after every hit?

<hr>

Degrees change as towns disappear. A quiet town can become the best-connected one left once the hubs around it are gone.

<div class="formula">

Is it worth the attacker's trouble to re-rank after every removal?

</div>

---

## Re-measuring is worse

<hr>

On a random network, an attacker working from a **fixed** ranking needs 58% of the nodes. Re-ranking after **every** removal brings that down to 40%.

<div class="fig">

![w:1100](figures/fixed-vs-adaptive.png)
<figcaption>better targeting costs more computation — and buys more damage</figcaption>

</div>

<!--
Same trade-off applies to any attack criterion, not just degree. We come back to betweenness in Part Seven.
-->

---

## Take it apart yourself

<hr>

<div class="cols">
<div>

Live: build a network, choose a removal strategy, and watch the profile draw itself.

Then on paper: *Build it, Break it, Build it back* — construct the MST by hand, break it, and redesign.

[network-robustness.html](https://skojaku.github.io/adv-net-sci/assets/vis/network-robustness.html)

</div>
<div class="fig">

![w:520](figures/demo-still.png)
<figcaption>pick a target, watch the curve</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Before next time

<hr>

You can now *measure* how badly a network breaks. You cannot yet **predict** it.

<div class="formula">

What fraction of a network has to fail before it fragments?

</div>

Next session: one formula answers this, for any network, from its degrees alone.

---

<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 07</span></div>

## Percolation

Before networks — a paved yard in the rain

---

<!-- _class: mid -->

## The puddle yard

<hr>

Rain falls on a paved yard. Each stone holds water with probability $p$, independently. Puddles on touching stones join up.

<div class="formula">

At which $p$ does one puddle first span the whole yard?

</div>

<div class="fig">

![w:1100](figures/puddle-low.png)

</div>

---

## Turning $p$ up

<hr>

<div class="fig">

![w:1100](figures/puddle-sweep.gif)
<figcaption>watch for the moment the pools join</figcaption>

</div>

<!--
Ask them to call out when it happens. The room will call it within a few hundredths of each other.
-->

---

## It happens all at once

<hr>

Below $p_c \approx 0.59$ there are scattered pools. Above it, one puddle owns the yard. There is no gentle ramp: this is a **phase transition**.

<div class="fig">

![w:1100](figures/phase-transition.png)
<figcaption>the largest puddle, measured</figcaption>

</div>

---

## Your turn at the slider

<hr>

<div class="cols">
<div>

Drag $p$ yourself in the module notebook and find the transition by hand.

Then answer this: how sharp is it when the yard is ten times bigger?

</div>
<div class="fig">

![w:520](figures/puddle-widget.png)
<figcaption>the marimo widget from the notes</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Does the order matter here?

<hr>

The stones do not all wet at once — the rain fills them one by one, in whatever order it likes.

<div class="formula">

Does a different order change when the giant puddle arrives?

</div>

---

## Only the fraction

<hr>

Different yard, different stones, same fraction wet — and the same answer. What determines connectivity is **how many**, not which ones came first.

<div class="fig">

![w:1100](figures/order-irrelevant.png)
<figcaption>two yards, one threshold</figcaption>

</div>

---

## Attack is percolation, backwards

<hr>

One axis, two directions. Adding nodes builds a giant component; removing them destroys it. The mathematics is already written — we only have to read it right to left.

<div class="fig">

![w:1100](figures/reverse-percolation.png)
<figcaption>the same transition, approached from the other side</figcaption>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part Five</span><span class="count">05 / 07</span></div>

## The formula

One number, from the degrees alone

---

<!-- _class: mid -->

## What number decides it?

<hr>

Two networks. Same number of nodes, same number of edges. One shatters when you remove a fifth of it; the other survives losing four-fifths.

<div class="formula">

What would you have to know about a network to tell them apart?

</div>

---

<!-- _class: mid -->

## Follow an edge, not a node

<hr>

Pick an **edge** at random — not a node — and walk to the node at its far end.

<div class="formula">

Is the node you arrive at a typical member of the network?

</div>

<div class="fig">

![w:520](figures/follow-edge.png)

</div>

---

## No — it is biased toward hubs

<hr>

<div class="cols">
<div>

Every edge has two ends, and a node owns one end per link. So a node with twice the degree has twice the chance of being the one you land on.

<div class="formula">

$$ q(k) = \frac{k\,p(k)}{\langle k \rangle} $$

</div>

</div>
<div class="fig">

![w:520](figures/qk-bias.png)
<figcaption>draw an end at random</figcaption>

</div>
</div>

---

## How connected is the node you land on?

<hr>

<div class="cols">
<div>

Average the degree over $q(k)$ rather than over $p(k)$, and you get

<div class="formula">

$$ \kappa = \frac{\langle k^2 \rangle}{\langle k \rangle} $$

</div>

$\kappa$ is large exactly when the network has hubs.

</div>
<div class="fig">

![w:520](figures/kappa-def.png)
<figcaption>land here, count its links</figcaption>

</div>
</div>

---

## Subtract the way you came in

<hr>

Of the $\kappa$ links at the node you reached, one is the edge you arrived on. The search fans out by $\kappa - 1$ — the **branching factor**.

<div class="fig">

![w:1100](figures/branching.png)
<figcaption>one in, $\kappa - 1$ out</figcaption>

</div>

---

## Molloy–Reed

<hr>

Branching above 1 and the search never dies out; below 1 and it stalls. So a **giant component** exists exactly when $\kappa > 2$. *Molloy & Reed, 1995.*

<div class="fig">

![w:1100](figures/molloy-reed.png)
<figcaption>below 1 it dies; above 1 it never stops</figcaption>

</div>

---

## Your turn

<hr>

Three small networks. Write down each degree, average $k$ and $k^2$ over the nodes, and compute $\kappa = \langle k^2 \rangle / \langle k \rangle$.

<div class="fig">

![w:1100](figures/kappa-worksheet.png)
<figcaption>which of these has a giant component?</figcaption>

</div>

---

## $\kappa = 2$, 3 and 1.75

<hr>

The star is comfortably above the threshold; the path is below it and falls apart on its own. The ring sits **exactly** at $\kappa = 2$.

<div class="fig">

![w:1100](figures/kappa-answer.png)
<figcaption>the ring lives on the line</figcaption>

</div>

---

## Now break it

<hr>

Remove a fraction $f$ of the nodes at random. Each surviving neighbour still had $\kappa - 1$ onward links, but only $(1-f)$ of them lead anywhere.

<div class="fig">

![w:1100](figures/dilution.png)
<figcaption>failure just rescales the branching factor</figcaption>

</div>

---

## The critical fraction

<hr>

Set the branching to exactly 1 — $(1-f)(\kappa - 1) = 1$ — and solve for $f$: $\;f_c = 1 - \dfrac{1}{\kappa - 1}$.

<div class="fig">

![w:1100](figures/fc-formula.png)
<figcaption>above $f_c$ the search dies, and so does the network</figcaption>

</div>

<!--
The exact binomial dilution is in the appendix and gives the same threshold; the heuristic is enough for the whole module.
-->

---

## A network without hubs

<hr>

A Poisson degree distribution has $\langle k^2 \rangle = \langle k \rangle^2 + \langle k \rangle$, so $\kappa = \langle k \rangle + 1$ and $f_c = 1 - 1/\langle k \rangle$. Robustness is set by the **average degree alone**.

<div class="fig">

![w:1100](figures/fc-poisson.png)
<figcaption>at $\langle k \rangle = 4$, three quarters of the nodes must go</figcaption>

</div>

---

<!-- _class: mid -->

## And a network with hubs?

<hr>

A scale-free degree distribution, $P(k) \sim k^{-\gamma}$: most nodes tiny, a few enormous, and the largest degree grows with the network.

<div class="formula">

What happens to $\kappa = \langle k^2 \rangle / \langle k \rangle$?

</div>

---

## $\kappa$ blows up, $f_c \to 1$

<hr>

For $2 < \gamma < 3$ the second moment diverges, so $\kappa \to \infty$ and $f_c \to 1$: you have to remove essentially **every** node before a hub network fragments.

<div class="fig">

![w:1100](figures/fc-scalefree.png)
<figcaption>bigger hubs, bigger $\kappa$, higher threshold</figcaption>

</div>

<!--
Cohen, Erez, ben-Avraham and Havlin, PRL 2000: this is why the Internet shrugs off random router failures.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Six</span><span class="count">06 / 07</span></div>

## Robust yet fragile

The strength and the weakness turn out to be the same thing

---

<!-- _class: mid -->

## So a hub network is indestructible?

<hr>

$f_c \to 1$ says random failure cannot kill it. Every hub network you know — the Internet, the airline map, the cell — inherits that.

<div class="formula">

Is that the whole story?

</div>

---

## Random failure: both survive

<hr>

Two simulated networks with the same 2,000 nodes and 6,000 edges. Knock out nodes at random and both hold together for a long time; the hub network holds on longest.

<div class="fig">

![w:1100](figures/sim-random.png)
<figcaption>measured, not sketched</figcaption>

</div>

---

## Now let the adversary choose

<hr>

Same two networks. This time remove the highest-degree node first, and keep going. The hub network is gone at **20%**.

<div class="fig">

![w:1100](figures/sim-targeted.png)
<figcaption>the hubs were the whole structure</figcaption>

</div>

---

## Robust yet fragile

<hr>

The same hubs that made random failure harmless are what an attacker aims at. Strength and weakness are one structural fact. *Albert, Jeong & Barabási, Nature, 2000.*

<div class="fig">

![w:1100](figures/robust-fragile.png)
<figcaption>one network, two fates</figcaption>

</div>

---

## Efficiency against security

<hr>

Hubs are the cheap way to connect everything — and the cheap thing to attack. Redundancy buys security and costs cable. **No structure wins both.**

<div class="fig">

![w:1100](figures/efficiency-security.png)
<figcaption>the trade-off, drawn</figcaption>

</div>

---

<!-- _class: mid -->

## You are the designer

<hr>

Back to Moravia. The board will fund **two** extra cables beyond the 292 km tree.

<div class="formula">

Where do you put them, and what exactly does the money buy?

</div>

<div class="fig">

![w:1100](figures/mst-blank-design.png)

</div>

<!--
Take three proposals before revealing. Push for the second question: "what does it buy" is the one they skip.
-->

---

## Close the ring in the south

<hr>

Zlín–Hodonín and Znojmo–Hodonín turn the tree into a ring. For **+136 km (+47%)**: worst single loss goes from $3/8$ to $6/8$, and $R$ from 0.17 to 0.27.

<div class="fig">

![w:1100](figures/redundant-answer.png)
<figcaption>the best pair of the fifteen — searched, not guessed</figcaption>

</div>

---

## Design principles

<hr>

<div class="cols">
<div>

* **Even out the degrees** — no town carrying three others
* **Redundant routes** — two ways to reach anywhere
* **Protect the hubs** you cannot design away
* **Layer** local grids under a backbone
* **Reconfigure** when an attack is detected

</div>
<div class="fig">

![w:520](figures/design-principles.png)
<figcaption>degrees after the two extra cables</figcaption>

</div>
</div>

---

## Build it back

<hr>

1926 answered "cheapest". A modern grid answers "cheapest that survives" — the same tree, plus the loops that cost money and save cities.

<div class="fig">

![w:1100](figures/build-it-back.png)
<figcaption>the tree, and what got added to it</figcaption>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part Seven</span><span class="count">07 / 07</span></div>

## Edge cases

Four networks that test the law

---

<!-- _class: mid -->

## A ring

<hr>

Every town has exactly two cables — a perfect loop, no hubs, no leaves.

<div class="formula">

What is $\kappa$, and what does $f_c$ say?

</div>

<div class="fig">

![w:520](figures/ring-q.png)

</div>

---

## Exactly on the threshold

<hr>

<div class="cols">
<div>

$\langle k \rangle = 2$ and $\langle k^2 \rangle = 4$, so $\kappa = 2$ and the branching factor is exactly **1**.

$f_c = 0$: a ring has no robust core to lose. Cut one node and it is a chain; cut two and it is two chains.

</div>
<div class="fig">

![w:520](figures/ring-a.png)
<figcaption>the threshold itself</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## A random network with $\langle k \rangle = 1$

<hr>

Poisson degrees, one edge per node on average.

<div class="formula">

What does $\kappa = \langle k \rangle + 1$ say about it?

</div>

<div class="fig">

![w:520](figures/er1-q.png)

</div>

---

## The same threshold, from the other side

<hr>

<div class="cols">
<div>

$\kappa = 2$ — exactly the Molloy–Reed boundary.

And $\langle k \rangle = 1$ is precisely where Module 02's giant component was born. Two different arguments, one number.

</div>
<div class="fig">

![w:520](figures/er1-a.png)
<figcaption>m02's result, rediscovered</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Attack by betweenness, not degree?

<hr>

Suppose the adversary ranks nodes by how many shortest routes run **through** them, rather than how many links they have.

<div class="formula">

Would that do more damage? What would it cost?

</div>

<div class="fig">

![w:1100](figures/betweenness-q.png)

</div>

---

## More damage, more computation

<hr>

The degree-2 node in the middle carries every route between the two halves. Degree misses it completely; betweenness finds it — at a far higher price to compute.

<div class="fig">

![w:1100](figures/betweenness-a.png)
<figcaption>the cheapest node to cut is not the biggest</figcaption>

</div>

<!--
Module 06 defines betweenness properly. Flag it here so the definition arrives with a reason attached.
-->

---

<!-- _class: mid -->

## Real grids are full of triangles

<hr>

Module 02 showed that real networks are heavily clustered: your neighbours are each other's neighbours.

<div class="formula">

Does $f_c = 1 - 1/(\kappa - 1)$ still hold there?

</div>

<div class="fig">

![w:520](figures/triangles-q.png)

</div>

---

## Not exactly — and here is why

<hr>

<div class="cols">
<div>

The branching argument assumed every step reaches a **new** node. A triangle sends the search straight back where it came from, so the real fan-out is smaller than $\kappa - 1$.

Real thresholds sit **below** the prediction.

</div>
<div class="fig">

![w:520](figures/triangles-a.png)
<figcaption>the search comes back on itself</figcaption>

</div>
</div>

<!--
The point is not that the formula is wrong. It is that you should always know which assumption you are standing on.
-->

---

## Module 03 in one picture

<hr>

Build it, break it, build it back — and the one line that predicted the breaking before it happened.

<div class="fig">

![w:1100](figures/recap.png)
<figcaption>292 km · 0.375 · +136 km · $f_c$</figcaption>

</div>

---

## Coming up in Module 04

<hr>

<div class="cols">
<div>

$q(k)$ said the node at the far end of a random edge is biased toward hubs.

Apply that to friendship and you get something uncomfortable: **your friends have more friends than you do.**

</div>
<div class="fig">

![w:520](figures/m04-teaser.png)
<figcaption>the same bias, a different question</figcaption>

</div>
</div>

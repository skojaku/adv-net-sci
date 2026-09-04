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

How much of a network can you destroy before it falls apart, and does it matter who is doing the damage?

</div>

Hold a guess. A number, out loud, before we start.

<!--
Do not answer this. Part Five answers it with one formula; Part Six shows the answer depends entirely on who is doing the damage.
-->

---

## Roadmap for today

<hr>

<div class="steps-list">

<div><div class="i">01</div><div>The cheapest grid: Moravia, 1926, and the minimum spanning tree</div></div>
<div><div class="i">02</div><div>Greedy: Kruskal, Prim, and why the obvious rule wins here</div></div>
<div><div class="i">03</div><div>Break it: one town goes dark, and the grid splits</div></div>
<div><div class="i">04</div><div>Percolation: puddles, and a transition that arrives all at once</div></div>
<div><div class="i">05</div><div>The formula: kappa, branching, and the critical fraction</div></div>
<div><div class="i">06</div><div>Robust yet fragile: what you would build instead</div></div>
<div><div class="i">07</div><div>Edge cases: the graphs that test the law</div></div>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 07</span></div>

## The cheapest grid

Post-war Moravia has no electricity and no money

---

## Moravia, 1919

<hr>

<div class="cols">
<div>

A one-year-old republic, its eastern lands dark, and every crown of cable a crown not spent on a hospital.

* Eight towns in **Moravia** need connecting, and the republic cannot afford a spare metre.

</div>
<div class="fig">

![w:520](figures/moravia-dark.png)
<figcaption>the eight towns, where they actually are</figcaption>

</div>
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

* His 1926 paper *O jistém problému minimálním* is the first solution, and the birth of the **minimum spanning tree**.
* *We come back to how he solved it at the end of Part Two.*

</div>
<div class="fig">

![w:520](figures/boruvka-portrait.png)
<figcaption>Otakar Borůvka, 1899–1995</figcaption>

</div>
</div>

---

## Each route has a price

<hr>

Eight dots, thirteen plausible routes, kilometres on each: a **weighted network**.

<div class="fig">

![w:1100](figures/abstract-3.png)
<figcaption>the border, the rivers and the mountains, all gone</figcaption>

</div>

---

## Your turn

<hr>

Five minutes. Connect all eight towns for the least total kilometres, and keep your number.

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

So the cheapest answer has no loops.

</div>
<div class="fig">

![w:520](figures/loop-waste.png)
<figcaption>cut it, still connected</figcaption>

</div>
</div>

---

## A tree

<hr>

<div class="cols">
<div>

A **tree** is a network that is connected and has no cycle.

Between any two nodes there is exactly one route, no choices, no spares.

</div>
<div class="fig">

![w:520](figures/tree-def.png)
<figcaption>one route between any two</figcaption>

</div>
</div>

---

## Seven cables, always

<hr>

A **spanning tree** touches every node, and for $n$ towns it has exactly $n - 1$ cables.

<div class="fig">

![w:1100](figures/spanning-count.png)
<figcaption>8 towns, 7 cables: the count is forced</figcaption>

</div>

<!--
The number of cables is not a design choice. Only WHICH seven is.
-->

---

## Minimum spanning tree

<hr>

The spanning tree of least total weight is the **minimum spanning tree**.

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

Take the cables cheapest first, and skip any that would close a loop. *Joseph Kruskal, 1956.*

<div class="fig">

![w:1100](figures/kruskal-rule.png)
<figcaption>thirteen routes, cheapest first</figcaption>

</div>

---

## The one it refuses

<hr>

Olomouc–Zlín is 51 km and next on the list, but both ends are already connected, so it would buy nothing.

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

Run Kruskal by hand: the order you take the cables, the one you refuse, the total.

<div class="fig">

![w:1100](figures/kruskal-worksheet.png)
<figcaption>your list, in order</figcaption>

</div>

---

## The order, and the answer to the question

<hr>

17, 29, 42, 48, 49, skip 51, 53, 54, seven cables, 292 km, and nothing cheaper exists.

<div class="fig">

![w:1100](figures/kruskal-answer.png)
<figcaption>the order it was built in</figcaption>

</div>

---

## Prim's rule

<hr>

Start at the Brno plant; buy the cheapest cable reaching one new town. *Jarník 1930 · Prim 1957.*

<div class="fig">

![w:1100](figures/prim-rule.png)
<figcaption>six ways out of Brno; take the cheapest</figcaption>

</div>

<!--
Jarník was also Czech, and published this in 1930 after reading Boruvka. Prim rediscovered it in 1957.
-->

---

## Kruskal and Prim, side by side

<hr>

Six towns, nine cables, one grid each. Step it forward yourself.

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
Four steps: the grid, Kruskal, Prim, and the swap that proves neither could have gone wrong. Stop on step 2 and ask why the 3-cable is refused; stop on step 3 and ask why Prim walks past the 5-cable. Nothing moves until you press it.
-->

---

## Your turn

<hr>

Run Prim from Brno. Write the order they enter in, then compare with your Kruskal list.

<div class="fig">

![w:1100](figures/prim-worksheet.png)
<figcaption>start at Brno</figcaption>

</div>

---

<!-- _class: mid -->

## Greedy is usually wrong

<hr>

The cheapest thing available is a bad answer to almost every problem: packing a bag, planning a trip, scheduling a factory.

<div class="formula">

So why can it not be beaten here?

</div>

Thirty seconds. Argue it with the person next to you.

<!--
Let them argue before you say anything. The answer they usually reach, 'because the cheapest edge can't hurt', is nearly the cut property; take it and sharpen it on the next slide.
-->

---

## Here it cannot be beaten

<hr>

<div class="cols">
<div>

Cut the towns into any two groups. The cheapest cable across that cut must be in the tree: swap it in, and any tree without it gets cheaper.

* Both rules only ever take such a cable. That is the whole proof.

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

<!--
Ask for a show of hands: one grid, or more than one? Most say one. Do not resolve it here.
-->

---

## Two cheapest grids

<hr>

Six cables in both, then the tie: take either, 292 km either way. Which one you get is the tie-break.

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

Neither of these is his. 1926: no computer, no sorted list, no notion of an “algorithm” to lean on.

<div class="formula">

What would you do, with eight towns and a pencil?

</div>

<!--
Give this a full minute. Someone usually proposes 'every town picks its own cheapest cable', which is exactly Borůvka. Name whoever says it.
-->

---

## Every town at once

<hr>

Every piece takes its own cheapest way out at the same moment, and the pieces merge. Six cables in round one, the last in round two.

<div class="fig">

![w:1100](figures/boruvka.gif)
<figcaption>no ordering, no queue, no waiting: two rounds, not seven steps</figcaption>

</div>

<!--
Run the loop and count the cables that appear in round one: six, at the same time. That simultaneity is the whole idea.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 07</span></div>

## Break it

The bill is paid, the grid is up, and now things start to fail

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
Run this as a real poll. Count hands town by town and write the tally on the board before turning the page.
-->

---

## Brno

<hr>

Lose Brno and eight towns become three, three and one.

<div class="fig">

![w:1100](figures/brno-removed.png)
<figcaption>Jihlava's half, Olomouc's half, and Hodonín alone</figcaption>

</div>

---

## Every cable is a bridge

<hr>

One route between any two towns, so no cable has a spare. Not bad luck, but what “cheapest” bought.

<div class="fig">

![w:1100](figures/tree-bridges.png)
<figcaption>Jihlava to Zlín: one route, no spare; real grids are meshed instead</figcaption>

</div>

---

## Measuring the damage

<hr>

**Connectivity** = largest surviving piece ÷ original size. Brno scores $3/8 = 0.375$; a leaf scores $7/8$.

<div class="fig">

![w:1100](figures/connectivity-def.png)
<figcaption>one number for how bad it is</figcaption>

</div>

---

<!-- _class: mid -->

## Keep going

<hr>

Do not stop at one town. Remove them one at a time, measuring the connectivity after each.

<div class="formula">

Sketch the curve before we draw it. Does it slide, or does it fall off a cliff?

</div>

<!--
Have them sketch the curve on paper before you show it. The common guess is a straight slide down; the first removal costing more than the next four is the surprise.
-->

---

## The robustness profile

<hr>

Damage is a **curve**, not a number, one point per town lost.

<div class="fig">

![w:1100](figures/profile-build.gif)
<figcaption>connectivity against the fraction removed</figcaption>

</div>

<!--
Pause on the first two frames: the first removal costs more than the next four put together.
-->

---

## One curve, one number

<hr>

The **R-index** is the area under the profile, $R = \frac{1}{N}\sum_k y_k$. This attack scores 0.17.

<div class="fig">

![w:1100](figures/r-index.png)
<figcaption>the whole curve, compressed to one comparable number</figcaption>

</div>

---

<!-- _class: mid -->

## Does the order matter?

<hr>

Same grid. Same number of towns removed. Only the *order* is different.

<div class="formula">

How far apart can two curves on the same network be?

</div>

Guess a factor before we look.

<!--
Collect a factor out loud, most say 1.5 or 2. The measured answer is 2.4, so nobody is wildly wrong, and that is the point: order matters more than they expect.
-->

---

## Random failure

<hr>

Earthquakes and broken transformers do not read the map. They take leaves as often as hubs: $R = 0.41$.

<div class="fig">

![w:1100](figures/profile-random.png)
<figcaption>unlucky, but not targeted</figcaption>

</div>

---

## Targeted attack

<hr>

An adversary who can see the map takes Brno first. Same grid, same removals, $R = 0.17$, 2.4 times the damage.

<div class="fig">

![w:1100](figures/profile-both.png)
<figcaption>the gap between bad luck and bad intent</figcaption>

</div>

---

## Take it apart yourself

<hr>

<div class="cols">
<div>

Live: build a network, choose a removal strategy, and watch the profile draw itself.

* [network-robustness.html](https://skojaku.github.io/adv-net-sci/assets/vis/network-robustness.html)
* Then on paper: *Build it, Break it, Build it back*.

</div>
<div class="fig">

![w:520](figures/demo-still.png)
<figcaption>pick a target, watch the curve</figcaption>

</div>
</div>

<!--
Do the live demo first, then hand out the paper exercise. The demo takes five minutes; the exercise is the rest of the session.
-->

---

<!-- _class: mid -->

## Before next time

<hr>

You can now *measure* how badly a network breaks. You cannot yet predict it.

<div class="formula">

What fraction of a network has to fail before it fragments?

</div>

Next session: one formula answers this, for any network, from its degrees alone.

<!--
End the first day here. Do not answer it. The formula arrives at the top of Part Five.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 07</span></div>

## Percolation

Before networks, a paved yard in the rain

---

<!-- _class: mid -->

## The puddle yard

<hr>

Each paving stone holds water with probability $p$; touching puddles join up.

<div class="formula">

At which $p$ does one puddle first span the whole yard?

</div>

<div class="fig">

![w:1100](figures/puddle-low.png)

</div>

<!--
Ask for a number. Guesses cluster around 0.5, well below the real 0.59, which is what makes the sweep worth watching.
-->

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

Below $p_c \approx 0.59$, scattered pools; above it, one puddle owns the yard. No ramp, a **phase transition**.

<div class="fig">

![w:1100](figures/phase-transition.png)
<figcaption>the largest puddle, measured</figcaption>

</div>

---

<!-- _class: mid -->

## Does the order matter here?

<hr>

The stones do not all wet at once, the rain fills them one by one, in whatever order it likes.

<div class="formula">

Does a different order change when the giant puddle arrives?

</div>

<!--
Thirty seconds. The instinct is that order must matter; it does not, and that is why the whole problem reduces to one parameter.
-->

---

## Only the fraction

<hr>

Different yard, different stones, same fraction wet, and the same answer.

<div class="fig">

![w:1100](figures/order-irrelevant.png)
<figcaption>two yards, one threshold</figcaption>

</div>

---

## Attack is percolation, backwards

<hr>

One axis, two directions: adding nodes builds the giant component, removing them destroys it.

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

Two networks, same nodes, same edges. One shatters at a fifth removed; the other survives losing four-fifths.

<div class="formula">

What would you have to know about a network to tell them apart?

</div>

<!--
Do not let them answer 'the number of edges', both networks have the same. Push until someone says something about how the edges are spread.
-->

---

<!-- _class: mid -->

## Follow an edge, not a node

<hr>

<div class="cols">
<div>

Pick an **edge** at random, not a node, and walk to the node at its far end.

<div class="formula">

Is the node you arrive at a typical member of the network?

</div>

</div>
<div class="fig">

![w:520](figures/follow-edge.png)

</div>
</div>

<!--
This is the pivot of the whole module. Make sure they see that picking an edge is not the same as picking a node before you turn the page.
-->

---

## No, it is biased toward hubs

<hr>

Twice the degree, twice the chance of being the one you land on: $q(k) = k\,p(k) / \langle k \rangle$.

<div class="fig">

![w:1100](figures/qk-bias.png)
<figcaption>draw an end at random, not a node</figcaption>

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

* $\kappa$ is large exactly when the network has hubs.

</div>
<div class="fig">

![w:520](figures/kappa-def.png)
<figcaption>land here, count its links</figcaption>

</div>
</div>

---

## Subtract the way you came in

<hr>

One of the $\kappa$ links is the edge you arrived on, so the search fans out by $\kappa - 1$: the **branching factor**.

<div class="fig">

![w:1100](figures/branching.png)
<figcaption>one edge in, kappa minus one out</figcaption>

</div>

---

## Molloy–Reed

<hr>

Branching above 1 and the search never dies. A **giant component** exists exactly when $\kappa > 2$. *Molloy & Reed, 1995.*

<div class="fig">

![w:1100](figures/molloy-reed.png)
<figcaption>below 1 it dies; above 1 it never stops</figcaption>

</div>

<!--
Left panel dies, right panel never stops. The whole criterion is which side of 1 the branching factor falls on.
-->

---

## Your turn

<hr>

Three small networks. Average $k$ and $k^2$ over the nodes, then take $\kappa = \langle k^2 \rangle / \langle k \rangle$.

<div class="fig">

![w:1100](figures/kappa-worksheet.png)
<figcaption>which of these has a giant component?</figcaption>

</div>

---

## $\kappa = 2$, 3 and 1.75

<hr>

The star is above the threshold, the path below it. The ring sits exactly at $\kappa = 2$.

<div class="fig">

![w:1100](figures/kappa-answer.png)
<figcaption>the ring lives on the line</figcaption>

</div>

---

## Now break it

<hr>

Remove a fraction $f$ at random: of each neighbour's $\kappa - 1$ onward links, only $(1-f)$ still lead anywhere.

<div class="fig">

![w:1100](figures/dilution.png)
<figcaption>failure just rescales the branching factor</figcaption>

</div>

---

## The critical fraction

<hr>

Set the branching to 1: $(1-f)(\kappa-1) = 1$, so $f_c = 1 - 1/(\kappa - 1)$.

<div class="fig">

![w:1100](figures/fc-formula.png)
<figcaption>past the crossing the search dies, and so does the network</figcaption>

</div>

<!--
The exact binomial dilution is in the appendix and gives the same threshold; the heuristic is enough for the whole module.
-->

---

## A network without hubs

<hr>

Poisson degrees give $\kappa = \langle k \rangle + 1$, so $f_c = 1 - 1/\langle k \rangle$: the average degree alone.

<div class="fig">

![w:1100](figures/fc-poisson.png)

</div>

---

<!-- _class: mid -->

## And a network with hubs?

<hr>

Scale-free degrees, $P(k) \sim k^{-\gamma}$: most nodes tiny, a few enormous, the largest growing with the network.

<div class="formula">

What happens to $\kappa = \langle k^2 \rangle / \langle k \rangle$?

</div>

<!--
They have met scale-free degree distributions in Module 02. Ask what happens to the average of the SQUARES when one node is enormous.
-->

---

## $\kappa$ blows up, $f_c \to 1$

<hr>

For $2 < \gamma < 3$ the second moment diverges, so $\kappa \to \infty$ and $f_c \to 1$.

<div class="fig">

![w:1100](figures/fc-scalefree.png)
<figcaption>bigger hubs, higher threshold</figcaption>

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

$f_c \to 1$ says random failure cannot kill it. The Internet, the airline map, the cell all inherit that.

<div class="formula">

Is that the whole story?

</div>

<!--
Let someone say yes. The next three slides are more fun if the room has committed.
-->

---

## Same money, two ways to spend it

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
Step 2 is the dice, step 3 is the adversary, step 4 hands you a dial for how much of the damage is deliberate. Run 2 and 3 before touching the dial. The two random curves nearly coincide; the two targeted ones do not.
-->

---

## The same hubs, both ways

<hr>

The hubs that made random failure harmless are what an attacker aims at: **robust yet fragile**. *Albert, Jeong & Barabási, Nature, 2000.*

<div class="fig">

![w:1100](figures/robust-fragile.png)
<figcaption>one network, two fates</figcaption>

</div>

<!--
The two solid curves nearly coincide; the dashed pair is where the story is. Point at the gap.
-->

---

<!-- _class: mid -->

## You are the designer

<hr>

Back to Moravia. The board will fund two extra cables beyond the 292 km tree.

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

Zlín–Hodonín and Znojmo–Hodonín close a ring. +136 km (+47%): worst loss $3/8 \to 6/8$, and $R$ 0.17 → 0.27.

<div class="fig">

![w:1100](figures/redundant-answer.png)
<figcaption>the best of the fifteen possible pairs, searched not guessed</figcaption>

</div>

<!--
Come back to whatever the room proposed on the previous slide before showing this. If someone proposed the southern ring, say so.
-->

---

## Design principles

<hr>

<div class="cols">
<div>

Hubs are the cheap way to connect everything, and the cheap thing to attack.

* **Even out the degrees**, fewer towns on a single cable
* **Redundant routes**, two ways to reach anywhere
* **Protect the hubs** you cannot design away
* **Reconfigure** when an attack is detected

</div>
<div class="fig">

![w:520](figures/design-principles.png)
<figcaption>cables per town, before (gray) and after (gold)</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Seven</span><span class="count">07 / 07</span></div>

## Edge cases

Three networks that test the law

---

<!-- _class: mid -->

## A random network with $\langle k \rangle = 1$

<hr>

<div class="cols">
<div>

Poisson degrees, one edge per node on average.

<div class="formula">

What does $\kappa = \langle k \rangle + 1$ say about it?

</div>

</div>
<div class="fig">

![w:520](figures/er1-q.png)

</div>
</div>

<!--
They derived this threshold in Module 02 by a completely different route. Do not remind them yet.
-->

---

## The same threshold, from the other side

<hr>

<div class="cols">
<div>

$\kappa = 2$, exactly the Molloy–Reed boundary.

* And $\langle k \rangle = 1$ is precisely where Module 02's giant component was born.
* Two different arguments, one number.

</div>
<div class="fig">

![w:520](figures/er1-a.png)
<figcaption>the birth of m02's giant component, rediscovered</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Attack by betweenness, not degree?

<hr>

Rank nodes by how many shortest routes run **through** them, not by how many links they have.

<div class="formula">

Would that do more damage? What would it cost?

</div>

<div class="fig">

![w:1100](figures/betweenness-q.png)

</div>

<!--
Ask them to point at the node they would cut. Many will point at a hub; the answer is the small node in the middle.
-->

---

## More damage, more computation

<hr>

The degree-2 node carries every route between the halves. Degree misses it; betweenness finds it, at a far higher price.

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

<div class="cols">
<div>

Real networks are heavily clustered: your neighbours are each other's neighbours (Module 02).

<div class="formula">

Does $f_c = 1 - 1/(\kappa - 1)$ still hold there?

</div>

</div>
<div class="fig">

![w:520](figures/triangles-q.png)

</div>
</div>

<!--
This is the slide that says the formula has assumptions. Ask what the branching argument quietly assumed.
-->

---

## Not exactly, and here is why

<hr>

<div class="cols">
<div>

The branching argument assumed every step reaches a new node. A triangle sends the search back where it came from, so the real fan-out is below $\kappa - 1$.

* Real thresholds sit below the prediction.

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

Build it, break it, build it back, and the line that predicted the breaking.

<div class="fig">

![w:1100](figures/recap.png)
<figcaption>built it, lost Brno, ringed the south</figcaption>

</div>

<!--
Three numbers, one grid: what it cost, what one town cost, what the ring cost. The formula that predicted it is on the board from Part Five.
-->

---

## Coming up in Module 04

<hr>

<div class="cols">
<div>

$q(k)$ said the node at the far end of a random edge is biased toward hubs.

* Apply that to friendship and you get something uncomfortable: **your friends have more friends than you do.**

</div>
<div class="fig">

![w:520](figures/m04-teaser.png)
<figcaption>the same bias, a different question</figcaption>

</div>
</div>

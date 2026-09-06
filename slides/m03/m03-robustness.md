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
They come in having already built a grid, broken it and rebuilt it on paper. This hour names what they did and then goes past it.
-->

---

<!-- _class: mid -->

## The question for today

<hr>

<div class="formula">

How much of a network can you destroy before it falls apart, and does it matter who is doing the damage?

</div>

Hold a number. We check it against a formula in Part Three.

<!--
Do not answer this. Part Three answers the first half; Part Four answers the second and reverses it.
-->

---

<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 04</span></div>

## Build it

Moravia, 1926, and the cheapest grid anyone had drawn

---

## Moravia, 1926

<hr>

<div class="cols">
<div>

A one-year-old republic, eight dark towns, and not a spare crown of cable.

* A friend at the West Moravian Power Company carries the question to **Otakar Borůvka**, who answers it in 1926 and invents the **minimum spanning tree**.

</div>
<div class="fig">

![w:520](figures/boruvka-portrait.png)
<figcaption>Otakar Borůvka, 1899–1995</figcaption>

</div>
</div>

<!--
Real place, real date, real paper: O jistem problemu minimalnim. His own method was neither Kruskal's nor Prim's: every piece of the grid picks its own cheapest way out at the same moment. Mention it, do not spend a slide on it.
-->

---

## What you drew on paper has a name

<hr>

No loops, seven cables for eight towns, nothing cheaper: a **minimum spanning tree**, 292 km.

<div class="fig">

![w:1100](figures/mst-def.png)
<figcaption>the nine stations on your sheet were this same question, with a cost table</figcaption>

</div>

<!--
The count is forced: n towns always take n-1 cables. Only WHICH seven is a design choice, and that is the only thing the algorithms decide.
-->

---

## Kruskal and Prim, one grid

<hr>

Two greedy rules that cannot disagree. Step them yourself.

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
Four steps: the grid, Kruskal, Prim, and the swap that proves neither could have gone wrong. Step 2 is where you ask why the 3-cable is refused; step 4 is the cut property, and it is the whole proof. On paper they compared their build order with a neighbour and got the same total; this is why.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 04</span></div>

## Break it

The bill is paid, the grid is up, and now things fail

---

<!-- _class: mid -->

## Which town, gone dark, hurts most?

<hr>

<div class="formula">

A transformer fails and one town drops off the grid, taking its cables with it. Point at the one you would least like to lose.

</div>

<div class="fig">

![w:1100](figures/mst-blank.png)

</div>

<!--
Run this as a real poll and write the tally on the board before turning the page.
-->

---

## Brno: eight towns become 3, 3 and 1

<hr>

Largest piece over original size is the **connectivity**. Brno scores $3/8$, a leaf $7/8$.

<div class="fig">

![w:1100](figures/brno-removed.png)
<figcaption>Jihlava's half, Olomouc's half, and Hodonín on its own</figcaption>

</div>

<!--
This is the middle column of Question 4 on their sheet, on a different grid. Ask whose worst station was the one with the most lines.
-->

---

## Take them one at a time

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
Step 2 is their Order R, step 3 their Order T, step 4 the area they estimated in Question 8. Stop on step 3 after the first removal: one town costs more than the next four did under chance.
-->

---

## Bad luck against bad intent

<hr>

Same grid, same eight removals, 2.4 times the damage. You drew these two curves on paper.

<div class="fig">

![w:1100](figures/profile-both.png)
<figcaption>break one yourself: <a href="https://skojaku.github.io/adv-net-sci/assets/vis/network-robustness.html">network-robustness.html</a></figcaption>

</div>

<!--
Their own two areas come out near 0.5 and near 0.23 on the nine-station grid, so the ratio they measured is the ratio here. Collect a couple of their numbers before showing this.
-->

---

<!-- _class: mid -->

## How much has to fail before it fragments?

<hr>

You can now measure the damage. You cannot yet predict it.

<div class="formula">

What fraction of a network has to go before it stops being one network?

</div>

<!--
Do not answer it. The formula arrives four slides from here, and it needs only the degrees.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 04</span></div>

## Predict it

One number, from the degrees alone

---

<!-- _class: mid -->

## The puddle yard

<hr>

<div class="formula">

Each paving stone holds water with probability $p$, and touching puddles count as one. At which $p$ does a single puddle first span the yard?

</div>

<div class="fig">

![w:1100](figures/puddle-low.png)

</div>

<!--
Ask for a number out loud before you move on.
-->

---

## Turn the rain up

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
    <div data-anim-clear data-pc-yard></div>
  </div>

  <div data-anim-canvas>
    <div data-anim-clear data-pc-chart></div>
  </div>

  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script src="../../lecture-note/assets/anim/percolation.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

<!--
Step 3 is the one that matters: hand the dial over and make somebody cross 0.59 one notch at a time. The yard goes from a fifth to more than half on a single notch.
-->

---

## It happens all at once

<hr>

Below $p_c \approx 0.59$, scattered pools; above it, one puddle owns the yard. No ramp: a **phase transition**.

<div class="fig">

![w:1100](figures/phase-transition.png)
<figcaption>removing nodes from a network is this same transition, run backwards</figcaption>

</div>

<!--
Adding stones builds a giant cluster; removing nodes destroys one. Same axis, opposite directions, and that is why the rest of this part is about networks again.
-->

---

<!-- _class: mid -->

## Same size, opposite fates

<hr>

Two networks, the same nodes and the same edges. One shatters at a fifth removed; the other survives losing four-fifths.

<div class="formula">

What would you have to know about a network to tell them apart?

</div>

<!--
Do not let them settle for 'the number of edges': both have the same. Push until somebody says something about how the edges are spread.
-->

---

## Follow an edge, not a node

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
This is the pivot of the module. Stop after step 2 and make sure they see that picking an edge is not the same as picking a node. Step 4 is the whole threshold argument in one dial; the mark on it is f_c.
-->

---

## The number is $\kappa$

<hr>

<div class="cols">
<div>

Average the degree over the node you *land on*, not the node you *pick*:

<div class="formula">

$$ \kappa = \frac{\langle k^2 \rangle}{\langle k \rangle} $$

</div>

* Large exactly when the network has hubs.

</div>
<div class="fig">

![w:520](figures/kappa-def.png)
<figcaption>ten towns, twenty cable ends: mean degree 2, kappa 3</figcaption>

</div>
</div>

<!--
This is the network from the animation, at the same positions.
-->

---

## Molloy–Reed

<hr>

One link is the way you came in, so a search fans out by $\kappa - 1$. Above 1 it never dies.

<div class="fig">

![w:1100](figures/molloy-reed.png)
<figcaption>a giant component exists exactly when kappa exceeds 2 · Molloy &amp; Reed, 1995</figcaption>

</div>

---

## The critical fraction

<hr>

Set the branching to 1: $(1-f)(\kappa-1) = 1$, so $f_c = 1 - 1/(\kappa - 1)$.

<div class="fig">

![w:1100](figures/fc-formula.png)
<figcaption>the argument assumes no triangles, so measured thresholds sit a little lower</figcaption>

</div>

<!--
The exact binomial dilution is in the appendix and gives the same threshold. A triangle sends the search back where it came from, so the real fan-out is below kappa minus one; that is the assumption to name if anyone asks.
-->

---

## A network without hubs

<hr>

Poisson degrees give $\kappa = \langle k \rangle + 1$, so $f_c = 1 - 1/\langle k \rangle$.

<div class="fig">

![w:1100](figures/fc-poisson.png)
<figcaption>at mean degree 1 this gives kappa 2: Module 02's giant component, rediscovered</figcaption>

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
They met these in Module 02. Ask what happens to the average of the SQUARES when one node is enormous.
-->

---

## $\kappa$ blows up, $f_c \to 1$

<hr>

For $2 < \gamma < 3$ the second moment diverges, so $\kappa \to \infty$.

<div class="fig">

![w:1100](figures/fc-scalefree.png)
<figcaption>Cohen, Erez, ben-Avraham &amp; Havlin, 2000: why the Internet shrugs off router failures</figcaption>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 04</span></div>

## Design it

The strength and the weakness turn out to be the same thing

---

<!-- _class: mid -->

## So a hub network is indestructible?

<hr>

$f_c \to 1$ says random failure cannot kill it. The Internet, the airline map and the cell all inherit that.

<div class="formula">

Is that the whole story?

</div>

<!--
Let somebody say yes. The next two slides are more fun if the room has committed.
-->

---

## Thirty towns, sixty cables, two designs

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
Step 2 is the dice, step 3 the adversary, step 4 a dial for how much of the damage is deliberate. Run 2 and 3 before touching the dial: the two random curves nearly coincide, the two targeted ones do not.
-->

---

## The same hubs, both ways

<hr>

What made random failure harmless is what an attacker aims at: **robust yet fragile**. *Albert &amp; Barabási, 2000.*

<div class="fig">

![w:1100](figures/robust-fragile.png)
<figcaption>the two solid curves nearly coincide; the dashed pair is the story</figcaption>

</div>

---

<!-- _class: mid -->

## You are the designer

<hr>

<div class="formula">

The board will fund two cables beyond the 292 km tree. Where do you put them, and what exactly does the money buy?

</div>

<div class="fig">

![w:1100](figures/mst-blank-design.png)

</div>

<!--
Take three proposals before turning the page. Push on the second question: 'what does it buy' is the one they skip. This is Question 10 on their sheet with a budget instead of a free hand.
-->

---

## Close the ring in the south

<hr>

Two cables close a southern ring. +136 km: worst loss $3/8 \to 6/8$, $R$ from 0.17 to 0.27.

<div class="fig">

![w:1100](figures/redundant-answer.png)
<figcaption>the best of the fifteen possible pairs, searched not guessed</figcaption>

</div>

<!--
Come back to whatever the room proposed before showing this, and name anyone who proposed the southern ring. The general rules behind it: even out the degrees, add a second route, and protect the hubs you cannot design away.
-->

---

## Module 03 in one picture

<hr>

292 km bought the grid, losing Brno left 3 of 8, and +136 km buys 6 of 8 back.

<div class="fig">

![w:1100](figures/recap.png)
<figcaption>built it, lost Brno, ringed the south</figcaption>

</div>

<!--
Three numbers, one grid. The formula that predicts the third one is still on the board from Part Three.
-->

---

## Coming up in Module 04

<hr>

<div class="cols">
<div>

Landing on a hub was likelier than landing on anyone else. That bias was $q(k)$.

* Apply it to friendship and you get something uncomfortable: **your friends have more friends than you do.**

</div>
<div class="fig">

![w:520](figures/m04-teaser.png)
<figcaption>the same bias, a different question</figcaption>

</div>
</div>

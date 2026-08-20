---
marp: true
theme: network-science
paginate: true
math: katex
---


<!-- _class: lead -->

<div class="eyebrow">Advanced Topics in Network Science · Module 01</div>

# Seven Bridges

<hr>

<div class="sub">A stroll, a puzzle, and the birth of graph theory</div>

<div class="credit">Sadamori Kojaku · Binghamton University</div>

<!--
Open with the story, not the definitions. Königsberg is the hook; abstraction is the point of the whole course.
-->

---

## Roadmap for today

<hr>

<div class="steps-list">

<div><div class="i">01</div><div>The puzzle — seven bridges, one frustrating walk</div></div>
<div><div class="i">02</div><div>Abstraction — landmasses → nodes, bridges → edges</div></div>
<div><div class="i">03</div><div>Degree and Euler — parity decides what is possible</div></div>
<div><div class="i">04</div><div>Vocabulary — walk, trail, path, circuit, cycle</div></div>
<div><div class="i">05</div><div>Connectivity — components and the giant component</div></div>
<div><div class="i">06</div><div>Direction — in/out-degree, directed Euler condition, strong vs. weak</div></div>
<div><div class="i">07</div><div>Representation — the adjacency matrix, its powers, and sparsity</div></div>
<div><div class="i">08</div><div>Edge cases — the graphs that break the rules</div></div>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 08</span></div>

## The puzzle

An 18th-century Sunday stroll that mathematics could not ignore

<div class="review">

Lecture note — *Königsberg, 1736: seven bridges and a Sunday walk*

</div>

---

## The Königsberg bridge problem

<hr>

<div class="cols">
<div>

18th-century Königsberg (today Kaliningrad). Two islands in the Pregel, linked to the mainland by seven bridges.

<div class="formula">

Cross each bridge exactly once and return to the start?

</div>

</div>
<div class="fig">

![w:520](figures/konigsberg-map.png)
<figcaption>the shape you're about to erase</figcaption>

</div>
</div>

---

## Your turn

<hr>

Click a bridge to cross it. [Worksheet (Esteban Moro)](http://estebanmoro.org/pdf/netsci_for_kids/the_konisberg_bridges.pdf)

<figure class="anim-stage" id="kb-tracer">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-play>⏸ Pause</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>
  <div class="anim-grid-2" data-anim-canvas>
    <div data-anim-clear data-kb-map></div>
    <div data-anim-clear data-kb-side></div>
  </div>
  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script src="../../lecture-note/assets/anim/kb-tracer.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

---

<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 08</span></div>

## Abstraction

Strip the map until only relationships remain

<div class="review">

Lecture note — *Euler throws away the map*, and *What a graph is, formally*

</div>

---

## What can you throw away?

<hr>

<div class="cols">
<div>

Look again — the puzzle survives even if you erase almost everything here.

<div class="note">

Does the puzzle depend on bridge length? Island area? River width? Which bank you start from?

</div>

</div>
<div class="fig">

![w:520](figures/konigsberg-sketch.png)
<figcaption>what actually matters here?</figcaption>

</div>
</div>

---

## Euler's move — the city

<hr>

<div class="cols">
<div>

Euler asked the same question. His answer: keep only what connects to what — geography, distance, shape, all gone.

<div class="note">

Notice the coastlines already fading in the figure — that's the erasure starting.

</div>

</div>
<div class="fig">

![w:520](figures/abstraction-1-map.png)
<figcaption>N, A, B, S now labelled — the cut comes next</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Euler's move — each landmass becomes a node

<hr>

<div class="cols">
<div>

Four landmasses. Four dots. A landmass's size, its shape, its area — all gone. Only a bare label remains.

</div>
<div class="fig">

![w:520](figures/abstraction-2-nodes.png)
<figcaption>four dots, still no lines between them</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Euler's move — each bridge becomes an edge

<hr>

<div class="cols">
<div>

Every bridge becomes a line joining two dots — a new object: a **graph**.

<div class="note">

1736: this abstraction founds **graph theory** — substrate for social, transport, brain, Internet analysis.

</div>

</div>
<div class="fig">

![w:520](figures/abstraction-3-graph.png)
<figcaption>seven edges in all — two pairs doubled, island A touching five</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## A graph, written down

<hr>

<div class="cols">
<div>

<div class="formula">

$$ G = (V, E) $$

</div>

$V$ = **nodes** · $E$ = **edges** (pairs of nodes).

For Königsberg: four landmasses, seven bridges.

</div>
<div class="fig">

![w:520](figures/abstraction-3-graph.png)
<figcaption>the abstracted city</figcaption>

</div>
</div>

---

## The word for a doubled pair

<hr>

Question 1 gave you two bridges between the same two cities, and the lab made you write that pair down **twice**. Both bridges count — merge them and you are solving a different puzzle with a different answer.

* A pair that repeats is a **multi-edge**.
* A graph that allows them is a **multigraph**.
* Königsberg is one, twice over — which is why the doubling had to survive the abstraction.

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 08</span></div>

## Degree and Euler’s theorem

Parity is the whole argument

<div class="review">

Lecture note — *From a walk to a proof: the idea of degree*. The converse we skip: appendix, *Why Euler's conditions are enough*

</div>

---

<!-- _class: mid -->

## Degree

<hr>

<div class="cols">
<div>

The **degree** $k_i$ is the number of edges attached to node $i$.

Count every edge touching the node — nothing more, nothing less.

</div>
<div class="fig">

![w:520](figures/degree-definition.png)

</div>
</div>

---

<!-- _class: mid -->

## You drew this already — Question 2

<hr>

<div class="cols">
<div>

Every dashed line you drew joined an arrival to a departure. Roads get spent two at a time.

* Even city — every road finds a partner.
* Odd city — one road is left alone.
* The leftover has nowhere to go except the start or the end.

</div>
<div class="fig">

![w:520](figures/parity-odd.png)
<figcaption>three edges at this node: one pair, one leftover</figcaption>

</div>
</div>

---

## A graph with such a walk has at most two odd nodes

<hr>

<div class="fig">

![w:1000](figures/parity-bound.png)

</div>

<div class="formula">

**Euler's theorem** (half of it): if a walk crosses every edge exactly once, then

$$ \#\{\text{odd nodes}\} \leq 2 $$

</div>

---

## The verdict

<hr>

<div class="cols">
<div>

Your Question 3 table, on Euler's map instead of mine.

* Degrees: 3, 5, 3, 3
* All four odd
* Rule: a cross-every-edge walk allows at most 2 odd
* Impossible.

</div>
<div class="fig">

![w:520](figures/konigsberg-degrees.png)
<figcaption>now labelled — red marks odd degree</figcaption>

</div>
</div>

---

## Eulerian path

<hr>

<div class="cols">
<div>

An **Eulerian path** uses every edge once — exists exactly when 0 or 2 nodes are odd, on a graph you can get around.

<div class="note">

Question 4(c): your own drive came back to a city, so it was a *trail*, not a path. “Eulerian path” is the traditional name; strictly it is an Eulerian **trail**.

That the condition is also *enough* — such a walk always exists — we use without proving.

</div>

</div>
<div class="fig">

![w:520](figures/euler-path-example.png)
<figcaption>two odd nodes</figcaption>

</div>
</div>

---

## Eulerian circuit

<hr>

<div class="cols">
<div>

Ending back where you began removes the ends — no start, no finish, one loop. No node is left to absorb a leftover edge.

* For an **Eulerian circuit**, every node must be even.
* Königsberg fails either way — four odd nodes is neither 0 nor 2.

</div>
<div class="fig">

![w:520](figures/euler-circuit-example.png)
<figcaption>cross all six edges, end where you began</figcaption>

</div>
</div>

---

## Watch the trail get built

<hr>

Two odd corners, six edges. Step through it, then trace one yourself.

<figure class="anim-stage" id="euler-builder">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-play>⏸ Pause</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>
  <div class="anim-grid-2" data-anim-canvas>
    <div data-anim-clear data-eb-map></div>
    <div data-anim-clear data-eb-side></div>
  </div>
  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script src="../../lecture-note/assets/anim/euler-builder.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

<!--
The deck proves only the easy half; this is the converse doing its work. Beats: 1 two odd corners, in red, and Euler allows two. 2 open on TL and all six go, finishing on the other odd corner — not luck, the spare edge-end at an odd corner can only be a start or a finish. 3 open on BL, an even corner, and you strand at five with TL–BL nowhere near: two odd corners want both ends of the walk and BL took one. 4 lay a second TL–TR, every degree goes even, there is no end left to be, so the trail has to close. 5 hand it over — the part students never believe until they try it is step 3.
-->

---

## Which two bridges would you destroy?

<hr>

<div class="cols">
<div>

You want to make the walk possible. Which two bridges do you remove?

*Turn to your neighbor — 30 seconds.*

</div>
<div class="fig">

![w:520](figures/konigsberg-degrees.png)
<figcaption>work from the degrees</figcaption>

</div>
</div>

---

## A tragic epilogue

<hr>

<div class="cols">
<div>

World War II. Königsberg is bombed and two bridges are destroyed.

* Five bridges remain. Only two landmasses are left odd.
* The 200-year impossible walk becomes possible — by accident of war.

</div>
<div class="fig">

![w:520](figures/konigsberg-bombed.png)
<figcaption>two odd → now possible</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 08</span></div>

## Vocabulary

Name the journeys precisely

<div class="review">

Lecture note — *Five Words You Will Use All Semester*, with the route-namer you can click

</div>

---

<!-- _class: mid -->

## Walk

<hr>

<div class="cols">
<div>

A **walk** is any route through the graph. Nodes may repeat. Edges may repeat. Nothing is off-limits.

<div class="note">

You named three of these in Question 4. Same three tests, one slide each.

</div>

</div>
<div class="fig">

![w:520](figures/campus-walk-anim.gif)
<figcaption>the route: Dorm → Cafe → Gym → Cafe → Lib</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Trail

<hr>

<div class="cols">
<div>

A **trail** is a walk that never uses the same edge twice.

Nodes may still repeat.

</div>
<div class="fig">

![w:520](figures/campus-trail-anim.gif)
<figcaption>the route: Lib → Gym → Dorm → Cafe → Gym</figcaption>

</div>
</div>

---

## Path

<hr>

<div class="cols">
<div>

A **path** is a walk that never uses the same node twice — and so never the same edge either.

<div class="note">

Every path is a trail. Not every trail is a path — which is why Euler's is a trail.

</div>

</div>
<div class="fig">

![w:520](figures/campus-path-anim.gif)
<figcaption>the route: Lib → Cafe → Dorm → Gym</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Circuit

<hr>

<div class="cols">
<div>

A **circuit** is a closed trail — back to the start, no edge repeated.

</div>
<div class="fig">

![w:520](figures/circuit.png)
<figcaption>a node may be revisited; an edge may not</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Cycle

<hr>

<div class="cols">
<div>

A **cycle** is a closed path — back to the start, no node repeated.

</div>
<div class="fig">

![w:520](figures/cycle.png)
<figcaption>stricter than a walk or a trail — nothing repeats (red: the cycle traced)</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Five</span><span class="count">05 / 08</span></div>

## Connectivity

Euler’s theorem quietly assumed you can get everywhere

<div class="review">

Lecture note — *When a network falls apart*: components, the giant component, flood fill

</div>

---

## Components

<hr>

The lab handed you `is_connected(A)` and never showed you inside. This is inside.

* When the answer is no, the graph splits into **connected components** — maximal mutually-reachable sets.
* A single isolated node counts too — a component of one.

<div class="fig">

![w:760](figures/components-band.png)
<figcaption>three components, no edge crosses between them</figcaption>

</div>

---

## Run the sweep

<hr>

Click any unmarked node to sweep from it — the amber ring is the frontier.

<figure class="anim-stage" id="comp-sweep">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-play>⏸ Pause</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>
  <div class="cs-col" data-anim-canvas>
    <div data-anim-clear data-cs-map></div>
    <div data-anim-clear data-cs-side></div>
  </div>
  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script src="../../lecture-note/assets/anim/comp-sweep.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

<!--
Beats: 1 twelve nodes, and no way to see how many pieces. 2 rings out of L0, frontier amber, and the number on a node is its distance from the seed. 3 four left, seed again, and R0 alone is still a component — no pair inside it to fail the test. 4 each node entered once and each edge looked at twice, so O(N + M): thirteen edges, not seventy-eight pairs. 5 let two or three students pick the seeds. The payoff is that the order they choose changes the numbers on the nodes and nothing else — the partition is the graph's, not theirs.
-->

---

<!-- _class: mid -->

## A component has 1,000 nodes. Is it giant?

<hr>

You find a component with 1,000 nodes.

<div class="formula">

Giant, or not? What do you need to know first?

</div>

*Take 30 seconds.*

---

## The giant component

<hr>

<div class="cols">
<div>

It depends on $N$. The same 1,000 nodes are giant in a network of 1,200 — and negligible in one of ten million.

* A component is **giant** when it holds a finite fraction of all nodes as $N$ grows.
* In practice: extract it and work there. *Whether* one exists is Module 3's question.

</div>
<div class="fig">

![w:520](figures/giant-scale.png)
<figcaption>83% of the network on the left, 0.01% on the right</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Six</span><span class="count">06 / 08</span></div>

## Direction

Point every edge one way — degree, Euler, connectivity all split in two

<div class="review">

Lecture note — *When edges have direction*. The Euler rule for arrows: appendix, *The same rule when edges have direction*

</div>

---

<!-- _class: mid -->

## Edges with direction

<hr>

<div class="cols">
<div>

In a **directed** graph, each edge has an orientation — reachable one way doesn't mean reachable back.

</div>
<div class="fig">

![w:520](figures/directed-arrows.png)
<figcaption>C receives from both A and B; nothing leaves C</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## In-degree and out-degree

<hr>

<div class="cols">
<div>

Each node now has two counts: **in-degree**, edges arriving, and **out-degree**, edges leaving.

</div>
<div class="fig">

![w:520](figures/directed-indegree.png)
<figcaption>A→B→C→A — each arrow both leaves and arrives once</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Strongly connected

<hr>

<div class="cols">
<div>

A graph is **strongly connected** when a directed path runs from every node to every other.

</div>
<div class="fig">

![w:520](figures/directed-strong.png)
<figcaption>A→B→C→A: one loop reaches every node from every node</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Weakly connected

<hr>

<div class="cols">
<div>

Connected once you ignore direction. A weaker requirement — every strongly connected graph is **weakly connected**, but the converse fails.

<div class="note">

One-way streets get you out, not necessarily back.

</div>

</div>
<div class="fig">

![w:520](figures/directed-weak.png)
<figcaption>no directed route returns to A</figcaption>

</div>
</div>

---

## Turn an arrow round

<hr>

Click a street to turn it round. Six of the 64 orientations survive.

<figure class="anim-stage" id="dir-reach">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-play>⏸ Pause</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>
  <div class="anim-grid-2" data-anim-canvas>
    <div data-anim-clear data-dr-map></div>
    <div data-anim-clear data-dr-side></div>
  </div>
  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script src="../../lecture-note/assets/anim/dir-reach.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

<!--
Strong and weak sat on two figures two slides apart, which makes them look like two graphs. They are one graph and two questions. The number beside a corner is how many of the other four it reaches, so five fours is the verdict and the drawing carries it. Beats: 1 the counts appear, all four. 2 flood from A and from C so the number means something. 3 turn the chord round and nothing moves — that street's direction is free, because it is not on the only cycle through all five corners. 4 turn A–B round as well: both of A's streets now point in, A drops to zero, and one beat with the arrowheads rubbed out shows weak surviving what strong did not. 5 hand it over. Ask for a guess first: six of the 64 work, and in every one of the six each corner sits on a directed cycle. Flipping the chord turns any of them into another, so the room finds them in pairs.
-->

---

## The directed Euler condition

<hr>

<div class="cols">
<div>

Total degree is the wrong thing to count: three in and one out is degree four, even, and still hopeless. Passing through spends one of *each* kind.

So parity gives way to **balance** — plus connected once you ignore direction:

* **Closed tour:** in-degree equals out-degree at every node.
* **Trail:** exactly one node has out − in = 1 (start), one has in − out = 1 (end), every other node balances.

</div>
<div class="fig">

![w:520](figures/directed-strong.png)
<figcaption>A→B→C→A: in = out = 1 at every node — a closed tour</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Your turn: does a closed tour survive?

<hr>

<div class="cols">
<div>

Add one arc to this triangle — anywhere to anywhere.

Does the closed tour still exist? Does a trail?

*Turn to your neighbor — 30 seconds.*

</div>
<div class="fig">

![w:520](figures/directed-strong.png)
<figcaption>A→B→C→A — add one arc and re-check</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Seven</span><span class="count">07 / 08</span></div>

## Representation

How you store a network shapes what you can ask it

<div class="review">

Lecture note — *Three ways to write a network down* and *The adjacency matrix, and what its powers count*. CSR: appendix, *Storing a matrix that does not fit*

</div>

---

<!-- _class: mid -->

## How would you store a network?

<hr>

A million nodes. Answer *who are node 7's neighbors?* — a billion times.

<div class="formula">

How would you lay this out in memory?

</div>

*30 seconds with your neighbor.*

---

## Adjacency matrix

<hr>

<div class="cols">
<div>

$$
A_{ij} =
\begin{cases}
1 & i \sim j \\
0 & \text{otherwise}
\end{cases}
$$

The **adjacency matrix**: an $n \times n$ grid of 0s and 1s — the grid you filled in for Question 5(a). It opens the door to linear algebra, but costs $O(n^2)$ even when nearly all zero.

<div class="note">

A pair is a coordinate, and it lights two cells — the grid is a mirror.

</div>

</div>
<div class="fig">

![w:520](figures/store-matrix.png)
<figcaption>row 1 (red): 1s at columns 0, 2, 3 — node 1's three neighbors</figcaption>

</div>
</div>

---

## You have used all three. Here are their names

<hr>

The lab had you write the map as pairs, turn the pairs into a grid, then read a degree off a row. Each step was a different **representation**, and each is good at something the others are not.

* **Edge list** — one pair per edge. Compact, and what a data file looks like; “who are $i$'s neighbours?” costs a scan of everything.
* **Adjacency list** — each node's neighbours, kept together. Traversal is cheap, which is what the component sweep needed.
* **Adjacency matrix** — the grid. Buys linear algebra, at $O(n^2)$ whether or not the edges are there.
* Degree comes off each differently: count a node's appearances, take a list's length, sum a row.

---

<!-- _class: mid -->

## Multiply $A$ by itself. What does one entry mean?

<hr>

<div class="formula">

$$ \mathbf{A}^2 $$

Compute entry $(1,4)$ by hand. What does it count?

</div>

*30 seconds — try it on the five-node graph whose matrix appeared on-screen.*

---

<!-- _class: mid -->

## Now predict $A^3$ and $A^4$

<hr>

You've just seen what one entry of $\mathbf{A}^2$ counts.

<div class="formula">

Without multiplying it out — what will entries of $\mathbf{A}^3$ and $\mathbf{A}^4$ count?

</div>

*30 seconds — extend the pattern.*

---

## $A^k$ counts walks

<hr>

<div class="cols">
<div>

<div class="formula">

$$ (\mathbf{A}^k)_{ij} = \#\{\text{walks of length } k \text{ from } i \text{ to } j\} $$

</div>

<div class="note">

Walks, not paths — repetition is allowed. Later modules reuse this for clustering and centrality.

</div>

</div>
<div class="fig">

![w:520](figures/adjacency-squared.png)
<figcaption>red route 1–2–4, purple route 1–3–4 — both land in cell (1,4)</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## A dense matrix for eight billion people — how much memory?

<hr>

Every human on Earth, a node. Store the full $n \times n$ matrix, dense, one byte per entry.

<div class="formula">

Guess before you compute — kilobytes? Gigabytes? More?

</div>

*30 seconds.*

---

<!-- _class: mid -->

## 64 exabytes

<hr>

<div class="formula">

$$ n = 8\times10^{9} \qquad n^2 \times 1\text{ byte} = 6.4\times10^{19}\text{ bytes} \approx 64\text{ EB} $$

</div>

Eight billion nodes, one byte per pair — more storage than most data centers hold, just to record who is *not* connected.

---

## Store only the nonzeros

<hr>

Most pairs aren't linked — store only what's there. The **Compressed Sparse Row (CSR)** format keeps three arrays: **indptr** where each row starts, **indices** the column of each nonzero, **data** the values.

<div class="csrw">
<div class="csrw-top">
<div class="csrw-m" id="csrm"></div>
<div class="csrw-arrays">
<div class="csrw-row"><b>indptr</b><span id="csrp"></span></div>
<div class="csrw-row"><b>indices</b><span id="csri"></span></div>
<div class="csrw-row"><b>data</b><span id="csrd"></span></div>
</div>
</div>
<div class="csrw-ctl">
<label for="csrr">row</label>
<input type="range" id="csrr" min="0" max="4" value="1">
<output id="csro"></output>
</div>
</div>

<script>
(function () {
  var P = [0, 2, 5, 8, 10, 12],
      I = [1, 2, 0, 2, 3, 0, 1, 4, 1, 4, 2, 3],
      D = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      A = [[0,1,1,0,0],[1,0,1,1,0],[1,1,0,0,1],[0,1,0,0,1],[0,0,1,1,0]];

  function cells(host, vals, lo, hi, bounds) {
    host.innerHTML = "";
    vals.forEach(function (v, k) {
      var c = document.createElement("i");
      c.textContent = v;
      if (bounds) { if (k === lo || k === hi) c.className = "bound"; }
      else if (k >= lo && k < hi) { c.className = "slice"; }
      host.appendChild(c);
    });
  }

  function draw(r) {
    var m = document.getElementById("csrm");
    m.innerHTML = "";
    A.forEach(function (row, i) {
      row.forEach(function (v) {
        var c = document.createElement("i");
        c.textContent = v;
        c.className = (v ? "on " : "") + (i === r ? "row" : "");
        m.appendChild(c);
      });
    });
    cells(document.getElementById("csrp"), P, r, r + 1, true);
    cells(document.getElementById("csri"), I, P[r], P[r + 1], false);
    cells(document.getElementById("csrd"), D, P[r], P[r + 1], false);
    document.getElementById("csro").textContent =
      "indptr " + P[r] + "\u2192" + P[r + 1] + "  \u2014  columns " + I.slice(P[r], P[r + 1]).join(", ");
  }

  var s = document.getElementById("csrr");
  s.addEventListener("input", function () { draw(+s.value); });
  draw(+s.value);
})();
</script>

---

## Reading a graph off CSR — and when not to bother

<hr>

Cover the picture and use only the two arrays. Everything you need is still there:

* Degree of node $i$ is $\texttt{indptr}[i{+}1] - \texttt{indptr}[i]$ — a subtraction, no search.
* Its neighbours are $\texttt{indices}[\texttt{indptr}[i] : \texttt{indptr}[i{+}1]]$ — a slice, already contiguous.
* What it is bad at is **insertion**: one new edge shifts everything after it.
* So **dense beats sparse** on graphs that are small, nearly complete, or changing constantly. CSR pays off on the large, fixed, mostly-empty ones — which is what real networks are.

---

<!-- _class: part -->

<div class="band"><span>Part Eight</span><span class="count">08 / 08</span></div>

## Edge cases

The graphs that break the rules

<div class="review">

Lecture note — appendix, *Why Euler's conditions are enough*

</div>

---

<!-- _class: mid -->

## Does a self-loop add 1 to a node's degree, or 2?

<hr>

<div class="cols">
<div>

Degree = edges attached to a node. A self-loop is one edge — but touches the node at both ends.

<div class="note">

30 seconds: does it count once, or twice?

</div>

</div>
<div class="fig">

![w:520](figures/selfloop.png)
<figcaption>both ends attach here</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Two

<hr>

<div class="cols">
<div>

Both endpoints attach at the same node, so a self-loop contributes 2 to its degree.

<div class="note">

This keeps the parity argument intact — a self-loop adds an even number, so it never changes a node's parity.

</div>

</div>
<div class="fig">

![w:520](figures/selfloop-answer.png)
<figcaption>1 and 2 mark where the loop leaves and returns</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Every node has even degree, and yet there is no Euler circuit. How?

<hr>

Picture a graph where every node has degree 2 — parity satisfied, in full.

<div class="note">

The lab's last task, if you got that far. Hold up the map you built.

</div>

---

<!-- _class: mid -->

## The graph is in two pieces

<hr>

<div class="cols">
<div>

Parity alone isn't enough — Euler's theorem also requires **connectivity**. A single walk can't jump between components, however even their degrees.

</div>
<div class="fig">

![w:520](figures/edge-disconnected-2.png)
<figcaption>two squares, each still degree 2 — no edge between them</figcaption>

</div>
</div>

---

## Back to Königsberg

<hr>

<div class="cols">
<div>

Run both conditions against the seven bridges, one last time:

* **Connected?** Yes.
* 0 or 2 odd-degree? No — all four are odd.
* One failure is enough: no circuit, no path.

</div>
<div class="fig">

![w:520](figures/konigsberg-degrees.png)
<figcaption>both conditions, checked against the same graph</figcaption>

</div>
</div>

---

## Module 01 review

<hr>

<div class="cols">
<div class="fig">

![w:520](figures/recap.png)
<figcaption>the seven bridges, one last time</figcaption>

</div>
<div>

<div class="note">

All of it written down in the lecture note, Module 01.

</div>

* Abstraction (1736): landmasses → nodes, bridges → edges
* **Euler's theorem:** connected, 0 or 2 odd-degree nodes
* **Direction:** balance in place of parity
* **Connectivity:** components, the giant component
* Representation: the matrix, its powers, sparsity

</div>
</div>

---

## Coming up in Module 02

<hr>

<div class="cols">
<div>

### Small worlds

Almost all eight billion people are a handful of friendships away from each other.

Short paths. High clustering. One rewiring model that delivers both at once.

</div>
<div class="fig">

![w:520](figures/smallworld-teaser.png)
<figcaption>a few shortcuts (red) change everything</figcaption>

</div>
</div>


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
<div><div class="i">07</div><div>Representation — edge lists, adjacency, sparsity, CSR</div></div>
<div><div class="i">08</div><div>Edge cases — the graphs that break the rules</div></div>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 08</span></div>

## The puzzle

An 18th-century Sunday stroll that mathematics could not ignore

---

## The Königsberg bridge problem

<hr>

<div class="cols">
<div>

18th-century Königsberg (today Kaliningrad). Two islands in the Pregel, linked to the mainland by seven bridges.

<div class="formula">

Cross each bridge exactly once and return to the start?

</div>

<div class="note">

Nobody could find such a walk. More importantly: nobody could *prove* it was impossible.

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

<div class="cols">
<div>

Take ten minutes. Trace a route — or work the pen-and-paper worksheet.

[Worksheet (Esteban Moro)](http://estebanmoro.org/pdf/netsci_for_kids/the_konisberg_bridges.pdf)

<div class="note">

Ask yourself: What information is essential — bridge length? Island size? How do you move from "I can't find a path" to "a path cannot exist"?

</div>

</div>
<div class="fig">

![w:520](figures/konigsberg-sketch.png)
<figcaption>four landmasses, same layout as the engraving</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 08</span></div>

## Abstraction

Strip the map until only relationships remain

---

## What can you throw away?

<hr>

<div class="cols">
<div>

Look again — the puzzle survives even if you erase almost everything here.

<div class="note">

Turn to your neighbor — 30 seconds. Does the puzzle depend on bridge length? Island area? River width? Which bank you start from?

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

<!-- _class: mid -->

## Your turn: abstract a transit line

<hr>

Picture a small bus line: three stops — Depot, Mall, Park — a Depot–Mall leg, a Mall–Park leg, and an express Depot–Park run that skips Mall.

<div class="formula">

Decide with your neighbor: what are the nodes? What are the edges? Does the express route change Mall's degree?

</div>

*Take two minutes — sketch it as dots and lines.*

---

## Two bridges, one pair

<hr>

<div class="cols">
<div>

Two bridges between island A and bank N. Two more between A and bank S. Count each, or collapse the pair?

* Both count. Each bridge is its own edge.
* Collapse them and you're solving a different puzzle — fewer crossings to make.

</div>
<div class="fig">

![w:520](figures/multigraph-bridges.png)
<figcaption>N–A, doubled — two bridges, one pair</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## An edge to itself

<hr>

<div class="cols">
<div>

A **self-loop** is an edge that starts and ends at the same node.

Königsberg has none — but graphs in general do.

</div>
<div class="fig">

![w:520](figures/selfloop.png)
<figcaption>both ends attach here</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 08</span></div>

## Degree and Euler’s theorem

Parity is the whole argument

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
<figcaption>the arms: degree 1 each. The center: degree 4.</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## You are mid-walk. How many edges do you use?

<hr>

Your walk crosses every bridge once. Mid-walk, you arrive at a node — then leave again.

<div class="formula">

How many edges, just to pass through?

</div>

*30 seconds — count on your fingers.*

---

<!-- _class: mid -->

## Edges come in pairs

<hr>

<div class="cols">
<div>

Arrive by one edge, leave by another — two edges per visit.

An interior node spends its edges two at a time.

</div>
<div class="fig">

![w:520](figures/parity-even.png)
<figcaption>even: every edge finds a partner</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## What if the degree is odd?

<hr>

<div class="formula">

One edge can’t find a partner. What does that force?

</div>

*30 seconds — think about where that leftover edge has to go.*

---

<!-- _class: mid -->

## One edge left over

<hr>

<div class="cols">
<div>

Pair up the edges — one is left alone. It has nowhere to go except the start or end of your walk.

An odd-degree node must be where you begin or where you finish.

</div>
<div class="fig">

![w:520](figures/parity-odd.png)
<figcaption>three edges at this node: one pair, one leftover</figcaption>

</div>
</div>

---

## A graph with such a walk has at most two odd nodes

<hr>

<div class="cols">
<div>

<div class="formula">

If a walk crosses every edge exactly once, then

$$ \#\{\text{odd-degree nodes in the graph}\} \leq 2 $$

</div>

<div class="note">

A walk using every edge once has exactly two ends. Only those two spots can absorb a leftover edge — at most two odd-degree nodes.

</div>

</div>
<div class="fig">

![w:480](figures/parity-bound.png)
<figcaption>six nodes; only the two red ends are odd</figcaption>

</div>
</div>

---

## Your turn: count Königsberg

<hr>

<div class="cols">
<div>

Count the bridges touching each landmass. How many landmasses have an odd count?

Hands up when you have an answer — possible, or impossible?

</div>
<div class="fig">

![w:520](figures/konigsberg-blank.png)
<figcaption>same graph, no counts shown</figcaption>

</div>
</div>

---

## The verdict

<hr>

<div class="cols">
<div>

* Degrees: three, three, five, three
* All four odd
* Rule: at most two odd nodes
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

We've shown more-than-two-odd breaks it. That the condition is also *enough* — a path always exists — we use without proving.

</div>

</div>
<div class="fig">

![w:520](figures/euler-path-example.png)
<figcaption>two odd nodes</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## What if you must return to where you started?

<hr>

<div class="formula">

Add one rule: end back where you began. What happens to "exactly two odd"?

</div>

*30 seconds.*

---

## Eulerian circuit

<hr>

<div class="cols">
<div>

Ending back where you began removes the ends — no start, no finish, one loop. No node is left to absorb a leftover edge.

* The “exactly two odd” case disappears. For an **Eulerian circuit**, every node must be even.
* Königsberg fails either way — four odd nodes is neither 0 nor 2.

</div>
<div class="fig">

![w:520](figures/euler-circuit-example.png)
<figcaption>cross all six edges, end where you began</figcaption>

</div>
</div>

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

---

<!-- _class: mid -->

## Walk

<hr>

<div class="cols">
<div>

A **walk** is any route through the graph. Nodes may repeat. Edges may repeat. Nothing is off-limits.

</div>
<div class="fig">

![w:520](figures/campus-walk.png)
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

![w:520](figures/campus-trail.png)
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

* Every path is a trail. Not every trail is a path.
* That's why the **Eulerian path** from earlier is really an Eulerian *trail* — the name predates this vocabulary.

</div>

</div>
<div class="fig">

![w:520](figures/campus-path.png)
<figcaption>the route: Lib → Cafe → Dorm → Gym</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Your turn: find a trail that is not a path

<hr>

<div class="cols">
<div>

Trace one on the campus graph.

Hands up when you have it.

</div>
<div class="fig">

![w:520](figures/campus-base.png)
<figcaption>no arrows this time — you pick the direction</figcaption>

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

<!-- _class: mid -->

## Your turn: one trail, both triangles

<hr>

<div class="cols">
<div>

Six edges, two triangles, not touching. Trace one trail — no edge repeated — that covers every edge at right.

*30 seconds — try it. Hands up: possible, or impossible?*

</div>
<div class="fig">

![w:520](figures/edge-disconnected.png)
<figcaption>two triangles, no edge between them</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Five</span><span class="count">05 / 08</span></div>

## Connectivity

Euler’s theorem quietly assumed you can get everywhere

---

## Can you get from any node to any other?

<hr>

* A graph is **connected** when a path exists between every pair of nodes.
* The two-triangle graph from a moment ago already failed this test. This graph fails it too, differently.

<div class="fig tight">

![w:760](figures/connected-vs-not.png)
<figcaption>one missing edge splits five nodes into two pieces</figcaption>

</div>

---

## Components

<hr>

* If not, the graph splits into **connected components** — maximal mutually-reachable sets.
* A single isolated node counts too — a component of one.

<div class="fig">

![w:760](figures/components-band.png)
<figcaption>three components, no edge crosses between them</figcaption>

</div>

---

## Your turn: run the sweep

<hr>

* Pick an unvisited node, mark it.
* Visit its unvisited neighbors, and theirs, until stuck.
* Everything touched is one component — repeat if nodes remain.

<div class="fig tight">

![w:760](figures/components-bare.png)
<figcaption>trace it yourself — how many sweeps in all?</figcaption>

</div>

---

## Three sweeps, three components

<hr>

* Sweep 1 clears the eight-node ladder.
* Sweep 2 clears the triangle.
* Sweep 3 finds the lone node.

<div class="fig tight">

![w:760](figures/sweep-3.png)
<figcaption>dashed boxes mark each swept component — numbering restarts at 1</figcaption>

</div>

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

## What breaks when edges have direction?

<hr>

**Degree** has counted edges at a node without asking which way they point.

<div class="formula">

Once edges have direction, degree splits — into what?

</div>

*30 seconds.*

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

A directed path from every node to every other node.

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

<!-- _class: mid -->

## What replaces "odd" once edges point?

<hr>

<div class="formula">

Königsberg's rule was about odd degrees. What plays that role once edges carry direction?

</div>

*30 seconds.*

---

## Total degree is the wrong quantity

<hr>

<div class="cols">
<div>

Undirected rule: total degree. Try it here — add in + out, check even.

* A: in 0, out 2 → total 2, "even."
* B: in 2, out 0 → total 2, "even."
* Both pass — yet nothing enters A, nothing leaves B.

</div>
<div class="fig">

![w:520](figures/directed-parity-counterexample.png)
<figcaption>A: in 0, out 2 — B: in 2, out 0 — both "even," neither balanced</figcaption>

</div>
</div>

---

## The directed Euler condition

<hr>

<div class="cols">
<div>

Euler's condition splits into two cases — connected once you ignore direction, plus one balance rule:

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

<!-- _class: mid -->

## Edge list

<hr>

<div class="cols">
<div>

Simplest option: a list of pairs, one per edge. Compact — but finding node 1's neighbors means scanning every pair.

</div>
<div class="fig">

![w:520](figures/store-edgelist.png)
<figcaption>node 1's edges: rows 0, 2, 3</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Adjacency list

<hr>

<div class="cols">
<div>

Store each node's neighbors directly — node 1's row is the answer, no scanning.

</div>
<div class="fig">

![w:520](figures/store-adjlist.png)
<figcaption>same three neighbors as the edge list, now sitting together</figcaption>

</div>
</div>

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

An $n \times n$ grid of 0s and 1s — opens the door to linear algebra, but costs $O(n^2)$ even when nearly all zero.

</div>
<div class="fig">

![w:520](figures/store-matrix.png)
<figcaption>row 1 (red): 1s at columns 0, 2, 3 — node 1's three neighbors</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Degree, three ways — the edge list

<hr>

<div class="cols">
<div>

Same quantity, every representation. Edge list: count rows mentioning node 1.

</div>
<div class="fig">

![w:520](figures/store-edgelist.png)
<figcaption>three rows mention node 1 — degree 3</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Degree, three ways — the adjacency list

<hr>

<div class="cols">
<div>

The adjacency list needs no counting at all — a row's length is the degree.

</div>
<div class="fig">

![w:520](figures/store-adjlist.png)
<figcaption>node 1's row lists three neighbors — degree 3</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Degree, three ways — the matrix

<hr>

<div class="cols">
<div>

And the matrix agrees a third way: sum a row.

</div>
<div class="fig">

![w:520](figures/store-matrix.png)
<figcaption>row 1 sums to 3 — same degree as the edge list and adjacency list</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## For a multigraph, count the edges

<hr>

<div class="cols">
<div>

Two bridges, same pair? The entry isn't capped at 1 — $A_{ij}$ is the number of edges between $i, j$.

</div>
<div class="fig">

![w:520](figures/multigraph.png)
<figcaption>two N–A bridges → the entry is 2, not 1</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Multiply $A$ by itself. What do the entries mean?

<hr>

<div class="formula">

$$ \mathbf{A}^2 $$

What does entry $(i,j)$ count?

</div>

*30 seconds — try it on the five-node graph from a couple of slides back, the one whose matrix appeared on-screen.*

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
<figcaption>red route 1–2–4, gold route 1–3–4 — both land in cell (1,4)</figcaption>

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

## 64 exabytes

<hr>

<div class="formula">

$$ n = 8\times10^{9} \qquad n^2 \times 1\text{ byte} = 6.4\times10^{19}\text{ bytes} \approx 64\text{ EB} $$

</div>

Eight billion nodes, one byte per pair — more storage than most data centers hold, just to record who is *not* connected.

<div class="note">

Almost every entry in that grid is a wasted zero. That waste is exactly what a sparse format refuses to store.

</div>

---

## Store only the nonzeros

<hr>

<div class="cols">
<div>

Most pairs aren't linked — store only what's there. The **Compressed Sparse Row (CSR)** format keeps three arrays:

* **data** — the values
* **indices** — column of each nonzero
* **indptr** — where each row starts, so one row = one contiguous slice

</div>
<div class="fig">

![w:520](figures/csr-build.png)
<figcaption>row 1: indptr 2→5 marks the slice — indices 0, 2, 3</figcaption>

</div>
</div>

---

## The payoff: degree

<hr>

<div class="cols">
<div>

Degree falls straight out of **indptr** — no scan required:

<div class="formula">

$$ k_i = \mathrm{indptr}[i+1]-\mathrm{indptr}[i] $$

</div>

</div>
<div class="fig">

![w:520](figures/csr-payoff.png)
<figcaption>the dense row highlighted on the left becomes the highlighted slice on the right</figcaption>

</div>
</div>

---

## The payoff: memory

<hr>

<div class="cols">
<div>

Dense stores 25 numbers here; CSR stores 30 (data 12 + indices 12 + indptr 6) — at this toy size, CSR loses. The claim is about growth: real networks are far larger and sparser, and the gap flips hard:

<div class="formula">

$$ O(n^2) \rightarrow O(m+n) $$

</div>

</div>
<div class="fig">

![w:520](figures/csr-memory.png)
<figcaption>n=100,000, average degree 6: dense 10B vs CSR 1.3M — CSR wins 7,692×</figcaption>

</div>
</div>

---

## Which format when?

<hr>

<div class="note">

Rule of thumb: edge list on disk, sparse matrices for analysis.

</div>

<div class="fig tight">

![w:760](figures/format-regimes.png)
<figcaption>axes: node count vs. density</figcaption>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part Eight</span><span class="count">08 / 08</span></div>

## Edge cases

The graphs that break the rules

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

## Is a single node with no edges connected?

<hr>

<div class="cols">
<div>

One node. No edges. Nothing to reach, and nothing reaching it.

<div class="note">

30 seconds: does "a path between every pair of nodes" even apply here?

</div>

</div>
<div class="fig">

![w:520](figures/edge-single-node.png)
<figcaption>the smallest possible graph — a single dot</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Yes — vacuously

<hr>

<div class="cols">
<div>

No pairs of nodes exist to fail the test — the condition holds by default. A lone node is a **component** of its own.

</div>
<div class="fig">

![w:520](figures/edge-single-node-answer.png)
<figcaption>the ring marks the component — it contains exactly one node</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Every node has even degree, and yet there is no Euler circuit. How?

<hr>

Picture a graph where every node has degree 2 — parity satisfied, in full.

<div class="note">

60 seconds: draw one yourself before the next slide.

</div>

---

## The graph is in two pieces

<hr>

<div class="cols">
<div>

Parity alone isn't enough — Euler's theorem also requires **connectivity**. A single walk can't jump between components, however even their degrees. That's why the sweep from Part Five matters.

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
* **0 or 2 odd-degree?** No — all four are odd.
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

* **Abstraction (1736):** landmasses → nodes, bridges → edges
* **Euler's theorem:** connected, 0 or 2 odd-degree nodes — walk, trail, path, circuit, cycle
* **Connectivity:** components, the giant component, $(\mathbf{A}^k)_{ij}$ counts walks
* **Representation:** edge list, adjacency, matrix, CSR — $O(n^2) \rightarrow O(m+n)$

<div class="note">

Build a CSR matrix by hand in the Module 01 notebook.

</div>

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


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
<div><div class="i">05</div><div>Connectivity — components, giants, directed reachability</div></div>
<div><div class="i">06</div><div>Representation — edge lists, adjacency, sparsity, CSR</div></div>
<div><div class="i">07</div><div>Edge cases — the graphs that break the rules</div></div>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 07</span></div>

## The puzzle

An 18th-century Sunday stroll that mathematics could not ignore

---

## The Königsberg bridge problem

<hr>

<div class="cols">
<div>

18th-century Königsberg (today Kaliningrad). Two islands in the Pregel, linked to the mainland by **seven bridges**.

<div class="formula">

Cross each bridge **exactly once** and **return to the start**?

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

Take **ten minutes**. Trace a route — or work the pen-and-paper worksheet.

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

<div class="band"><span>Part Two</span><span class="count">02 / 07</span></div>

## Abstraction

Strip the map until only relationships remain

---

## What can you throw away?

<hr>

<div class="cols">
<div>

Look at the sketch again. The puzzle is still the puzzle if you erase almost everything about it.

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

Euler looked at this same map and asked the same question. His answer: throw away everything except **what connects to what**.

Geography, distance, shape — all of it is about to go.

</div>
<div class="fig">

![w:520](figures/abstraction-1-map.png)
<figcaption>N, A, B, S — the labels are all that survive the cut</figcaption>

</div>
</div>

---

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

## Euler's move — each bridge becomes an edge

<hr>

<div class="cols">
<div>

Every bridge is now just a line joining two dots. What is left is a new mathematical object: a **graph**.

<div class="note">

1736: this abstraction founds **graph theory** — the substrate for social, transport, brain, and Internet analysis.

</div>

</div>
<div class="fig">

![w:520](figures/abstraction-3-graph.png)
<figcaption>seven edges in all — two pairs doubled</figcaption>

</div>
</div>

---

## A graph, written down

<hr>

<div class="cols">
<div>

<div class="formula">

$$ G = (V, E) $$

</div>

$V$ = nodes · $E$ = edges (pairs of nodes).

For Königsberg: four landmasses, seven bridges.

</div>
<div class="fig">

![w:520](figures/abstraction-3-graph.png)
<figcaption>the abstracted city</figcaption>

</div>
</div>

---

## Two bridges, one pair

<hr>

<div class="cols">
<div>

Königsberg has two bridges between island A and bank N — and two more between A and bank S. Count each one, or collapse the pair?

* Both count. Each bridge is its own edge.
* Collapse them into one and you are solving a **different** puzzle — one with fewer crossings to make.

</div>
<div class="fig">

![w:520](figures/multigraph.png)
<figcaption>N–A, doubled — A touches five bridges in all, not four</figcaption>

</div>
</div>

---

## An edge to itself

<hr>

<div class="cols">
<div>

A **self-loop** is an edge that starts and ends at the same node — a bridge, in principle, from a landmass back to itself.

Königsberg has none. But graphs in general do, and the definition needs to allow for them.

</div>
<div class="fig">

![w:520](figures/selfloop.png)
<figcaption>both ends attach here</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 07</span></div>

## Degree and Euler’s theorem

Parity is the whole argument

---

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

## You are mid-walk. How many edges do you use?

<hr>

Suppose your walk crosses every bridge exactly once. You arrive at a node in the middle of that walk. Later, you leave it again.

<div class="formula">

How many edges does that node use, just to let you pass through?

</div>

*Take 30 seconds. Count on your fingers if you have to.*

---

## Edges come in pairs

<hr>

<div class="cols">
<div>

Arrive by one edge, leave by another. Every time you pass through a node, you spend two edges — one in, one out.

An interior node consumes its edges **two at a time**.

</div>
<div class="fig">

![w:520](figures/parity-even.png)
<figcaption>even: every edge finds a partner</figcaption>

</div>
</div>

---

## What if the degree is odd?

<hr>

<div class="formula">

One edge can’t find a partner. What does that force?

</div>

*30 seconds — think about where that leftover edge has to go.*

---

## One edge left over

<hr>

<div class="cols">
<div>

Pair up the edges and one is left standing alone. That leftover edge has nowhere to go **except** the start or the end of your walk.

An odd-degree node must be where you **begin** or where you **finish**.

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

A walk that uses every edge exactly once has exactly two ends — a start and a finish. Only those two spots can absorb a leftover edge, so the graph itself can have at most two odd-degree nodes.

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

Count the bridges touching each landmass. How many landmasses have an **odd** count?

Hands up when you have an answer — possible, or impossible?

</div>
<div class="fig">

![w:520](figures/konigsberg-blank.png)
<figcaption>same four landmasses, same seven bridges — no counts shown</figcaption>

</div>
</div>

---

## The verdict

<hr>

<div class="cols">
<div>

* Degrees: **three, three, five, three**
* All four **odd**
* A walk **that crosses every bridge exactly once** allows at most two odd nodes
* **Impossible.**

</div>
<div class="fig">

![w:520](figures/konigsberg-degrees.png)
<figcaption>the same map you just counted, now labelled</figcaption>

</div>
</div>

---

## Eulerian path

<hr>

<div class="cols">
<div>

An **Eulerian path** is a route that uses every edge exactly once.

On a graph you can get around — every node reachable from every other — one exists exactly when **0 or 2** nodes have odd degree.

</div>
<div class="fig">

![w:520](figures/euler-path-example.png)
<figcaption>two odd nodes: start and end</figcaption>

</div>
</div>

---

## What if you must return to where you started?

<hr>

<div class="formula">

Add one requirement: the walk must end back where it began. What happens to the “exactly two odd” case?

</div>

*30 seconds.*

---

## Eulerian circuit

<hr>

<div class="cols">
<div>

A closed walk has no ends — no start, no finish, just one loop. There’s no node left over to absorb a leftover edge.

* The “exactly two odd” case disappears. For an **Eulerian circuit**, every node must be even.
* Königsberg fails either way — four odd nodes is neither 0 nor 2.

</div>
<div class="fig">

![w:520](figures/euler-circuit-example.png)
<figcaption>trace the closed walk — cross all six edges, end where you began</figcaption>

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

* Five bridges remain. Only **two** landmasses are left odd.
* The 200-year impossible walk becomes possible — by accident of war.

</div>
<div class="fig">

![w:520](figures/konigsberg-bombed.png)
<figcaption>two odd → now possible</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 07</span></div>

## Vocabulary

Name the journeys precisely

---

## Walk

<hr>

<div class="cols">
<div>

A **walk** is any route through the graph. Nodes may repeat. Edges may repeat. Nothing is off-limits.

</div>
<div class="fig">

![w:520](figures/campus-walk.png)
<figcaption>the Café–Gym edge, crossed twice</figcaption>

</div>
</div>

---

## Trail

<hr>

<div class="cols">
<div>

A **trail** is a walk that never uses the same edge twice.

The *node* may still repeat — you can pass through the same corner without walking the same street again.

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

Every path is a trail. Not every trail is a path.

</div>

</div>
<div class="fig">

![w:520](figures/campus-path.png)
<figcaption>the route: Lib → Cafe → Dorm → Gym</figcaption>

</div>
</div>

---

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

## Cycle

<hr>

<div class="cols">
<div>

A **cycle** is a closed path — back to the start, no node repeated.

</div>
<div class="fig">

![w:520](figures/cycle.png)
<figcaption>stricter than a walk or a trail — nothing repeats</figcaption>

</div>
</div>

---

## Writing a graph as a matrix

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

</div>
<div class="fig">

![w:520](figures/adjacency-matrix.png)
<figcaption>edge 1–3 ↔ cells (1,3) and (3,1)</figcaption>

</div>
</div>

---

## For a multigraph, count the edges

<hr>

<div class="cols">
<div>

Two bridges between the same pair? The matrix entry isn't capped at 1 — $A_{ij}$ becomes the **number** of edges between $i$ and $j$.

</div>
<div class="fig">

![w:520](figures/multigraph.png)
<figcaption>two N–A bridges → the entry is 2, not 1</figcaption>

</div>
</div>

---

## Multiply $A$ by itself. What do the entries mean?

<hr>

<div class="formula">

$$ \mathbf{A}^2 $$

What does entry $(i,j)$ count?

</div>

*30 seconds — try it on the graph from the previous slide.*

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

## Your turn: one trail, both triangles

<hr>

<div class="cols">
<div>

Six edges, two triangles, not touching. Trace one trail — no edge repeated — that covers every edge below.

*30 seconds — try it. Hands up: possible, or impossible?*

</div>
<div class="fig">

![w:520](figures/edge-disconnected.png)
<figcaption>two triangles, no edge between them</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Five</span><span class="count">05 / 07</span></div>

## Connectivity

Euler's theorem quietly assumed you can get everywhere

---

## Can you get from any node to any other?

<hr>

A graph is **connected** when a path exists between every pair of nodes.

<div class="fig">

![w:760](figures/connected-vs-not.png)
<figcaption>one missing edge splits five nodes into two pieces</figcaption>

</div>

<div class="note">

Every reachability argument since Euler has been quietly assuming this.

</div>

---

## Components

<hr>

When the answer is no, the graph splits into **connected components** — maximal sets of mutually reachable nodes.

<div class="fig">

![w:760](figures/components-band.png)
<figcaption>sizes 8, 3, and 1 — no edge crosses between them</figcaption>

</div>

<div class="note">

A single isolated node counts too — a component of one, with nowhere to go.

</div>

---

## Your turn: run the sweep

<hr>

Trace the traversal by hand, one component at a time:

* Pick an unvisited node and mark it.
* Visit its unvisited neighbors, and theirs, until you get stuck.
* Everything you touched is one component — if nodes remain, start again.

No components marked yet — trace your own below. How many sweeps until every node is marked?

<div class="fig tight">

![w:760](figures/components-bare.png)

</div>

---

## Three sweeps, three components

<hr>

Sweep 1 clears the eight-node ladder. Sweep 2 clears the triangle. Sweep 3 finds the lone node.

<div class="fig tight">

![w:760](figures/sweep-3.png)
<figcaption>each component restarts its own count at 1</figcaption>

</div>

<div class="note">

Cost is $O(N+M)$ — you touch every node and edge once.

</div>

---

## A component has 1,000 nodes. Is it giant?

<hr>

You find a component with exactly 1,000 nodes inside it.

<div class="formula">

Giant, or not? What would you need to know before you could answer?

</div>

*Take 30 seconds.*

---

## The giant component

<hr>

<div class="cols">
<div>

It depends on $N$. The same 1,000 nodes are giant in a network of 1,200 — and negligible in one of ten million.

* A component is **giant** when it holds a **finite fraction** of all nodes as $N$ grows.
* In practice we extract the giant component and work there — *whether* one exists at all is Module 3's question.

</div>
<div class="fig">

![w:520](figures/giant-scale.png)
<figcaption>83% of the network on the left, 0.01% on the right</figcaption>

</div>
</div>

---

## Edges with direction

<hr>

<div class="cols">
<div>

In a **directed** graph, each edge has an orientation. Reachability need not run both ways — you can get from A to B without any way back.

</div>
<div class="fig">

![w:520](figures/directed-arrows.png)
<figcaption>C receives from both A and B; nothing leaves C</figcaption>

</div>
</div>

---

## What breaks when edges have direction?

<hr>

**Degree** has counted edges at a node so far without asking which way they point.

<div class="note">

30 seconds: once edges have direction, degree splits — into what?

</div>

---

## In-degree and out-degree

<hr>

<div class="cols">
<div>

Each node now has two counts: **in-degree**, edges arriving, and **out-degree**, edges leaving. Euler's condition becomes: in-degree equals out-degree, at every node.

</div>
<div class="fig">

![w:520](figures/directed-indegree.png)
<figcaption>A→B→C→A — each arrow both leaves and arrives once</figcaption>

</div>
</div>

---

## Strongly connected

<hr>

<div class="cols">
<div>

A directed path from every node to every other node — direction respected the whole way.

</div>
<div class="fig">

![w:520](figures/directed-strong.png)
<figcaption>A→B→C→A: one loop reaches every node from every node</figcaption>

</div>
</div>

---

## Weakly connected

<hr>

<div class="cols">
<div>

Connected once you ignore direction. A weaker requirement — every strongly connected graph is weakly connected, but the converse fails.

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

<!-- _class: part -->

<div class="band"><span>Part Six</span><span class="count">06 / 07</span></div>

## Representation

How a computer holds a network

---

## How would you store a network?

<hr>

You have a million nodes, and you need to answer *who are node 7's neighbors?* — a billion times.

<div class="formula">

How would you lay this out in memory?

</div>

*30 seconds with your neighbor.*

---

## Edge list

<hr>

<div class="cols">
<div>

The simplest option: a list of pairs, one per edge. Compact on disk — but finding node 1's neighbors (highlighted) means scanning every pair, since its edges are scattered through the list rather than grouped together.

</div>
<div class="fig">

![w:520](figures/store-edgelist.png)
<figcaption>node 1's edges: rows 0, 2, 3</figcaption>

</div>
</div>

---

## Adjacency list

<hr>

<div class="cols">
<div>

Store each node's neighbors directly. Node 1's neighbors are node 1's row — no scanning, the answer is immediate.

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

An $n \times n$ grid of 0s and 1s. This opens the door to linear algebra — but storing it costs $O(n^2)$, even when almost every entry is 0.

<div class="note">

* Degree is the same quantity, three ways: count incidences in the edge list, read a row's length in the adjacency list, sum a row in the matrix.

</div>

</div>
<div class="fig">

![w:520](figures/store-matrix.png)
<figcaption>row 1 (red) is node 1's row: 1s at columns 0, 2, 3</figcaption>

</div>
</div>

---

## A dense matrix for eight billion people — how much memory?

<hr>

Every human on Earth is a node. Store the full $n \times n$ adjacency matrix, dense, one byte per entry.

<div class="formula">

Guess before you compute — kilobytes? Gigabytes? More?

</div>

*30 seconds.*

---

## Store only the nonzeros

<hr>

<div class="cols">
<div>

**512 exabytes.** Most pairs of people are not linked, so store only what is actually there, in three arrays:

* **data** — the values
* **indices** — the column of each nonzero
* **indptr** — where each row starts

One matrix row is one contiguous slice of **data** and **indices** — that is the whole trick.

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

The dense matrix stores 25 numbers here. CSR stores 30 — data (12) + indices (12) + indptr (6) — so at this toy size, **CSR loses**. The claim is about growth, not this graph: real networks are far larger and sparser, and the gap flips hard:

<div class="formula">

$$ O(n^2) \rightarrow O(m+n) $$

</div>

</div>
<div class="fig">

![w:520](figures/csr-memory.png)
<figcaption>n=5: dense 25 vs CSR 30, dense wins — n=100,000: dense 10B vs CSR 1.3M, CSR wins 7,700×</figcaption>

</div>
</div>

---

## Which format when?

<hr>

<div class="note">

Rule of thumb: edge list on disk, sparse matrices for analysis. You build a CSR matrix by hand in the Module 01 notebook.

</div>

<div class="fig tight">

![w:760](figures/format-regimes.png)
<figcaption>real networks cluster large-and-sparse — bottom right</figcaption>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part Seven</span><span class="count">07 / 07</span></div>

## Edge cases

The graphs that break the rules

---

## Does a self-loop add 1 to a node's degree, or 2?

<hr>

<div class="cols">
<div>

Degree is "the number of edges attached to a node." A self-loop is one edge — but it touches the node at both ends.

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

## Two

<hr>

<div class="cols">
<div>

Both endpoints attach at the same node, so a self-loop contributes **2** to its degree.

<div class="note">

This keeps the parity argument intact — a self-loop adds an even number, so it never changes a node's parity.

</div>

</div>
<div class="fig">

![w:520](figures/selfloop-answer.png)
<figcaption>① and ② mark where the loop leaves and returns</figcaption>

</div>
</div>

---

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

## Yes — vacuously

<hr>

<div class="cols">
<div>

There are no pairs of nodes to fail the test, so the condition holds by default. A lone node is a **component of its own**.

</div>
<div class="fig">

![w:520](figures/edge-single-node-answer.png)
<figcaption>the ring marks the component — it contains exactly one node</figcaption>

</div>
</div>

---

## Every node has even degree, and yet there is no Euler circuit. How?

<hr>

Picture a graph where every node has degree 2 — all even, Euler's parity condition satisfied in full.

<div class="note">

60 seconds: draw one yourself before the next slide.

</div>

---

## The graph is in two pieces

<hr>

<div class="cols">
<div>

Parity alone is not enough. Euler's theorem also requires **connectivity** — a single walk cannot jump between components, no matter how even their degrees are. This is why the sweep from Part Five is not optional.

</div>
<div class="fig">

![w:520](figures/edge-disconnected.png)
<figcaption>two triangles, no edge between them</figcaption>

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

* **Abstraction (1736):** landmasses → nodes, bridges → edges — the birth of graph theory
* **Euler's theorem:** connected, plus 0 or 2 odd-degree nodes — with vocabulary to name every walk, trail, path, circuit, cycle
* **Connectivity:** components, the giant component, and $(\mathbf{A}^k)_{ij}$ counting walks between nodes
* **Representation:** edge list, adjacency list, matrix — and CSR's $O(n^2) \rightarrow O(m+n)$

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
<figcaption>a few shortcuts change everything</figcaption>

</div>
</div>


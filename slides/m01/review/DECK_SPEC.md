# Deck spec — Module 01 rebuild

Rebuild `m01-euler-tour.md` to this outline. Every slide below is one `---`-separated
Marp slide. Prose is yours to write in the deck's existing voice; **structure, figures,
and the question/answer beats are not negotiable** — each one closes a specific review
finding.

## Non-negotiable rules

1. **Fragments.** Marp fragments a list when its items use `*` as the marker. `-` and `+`
   do **not** fragment. The old deck had **zero** `*` lists — that was the single largest
   source of findings. Every list that reveals an argument uses `*`. A list that is just a
   caption or an aside may stay `-`.
2. **No tables.** Not one `|---|` anywhere in the deck.
3. **No code.** No fenced blocks, no inline backticks teaching syntax. One plain-prose
   pointer to the notebook is allowed, once.
4. **No two columns of text.** `<div class="cols">` is allowed **only** as text + figure.
   Never text + text. `cols3` is banned outright.
5. **Question before answer.** Where the spec says *question slide*, the answer must be on
   the **next** slide — not a fragment on the same one. Where the spec says *fragmented
   reveal*, the answer may be a `*` fragment on the same slide.
6. **Every concept slide has a figure.** The only exceptions are part dividers, question
   slides, the roadmap, and the title.
7. Keep the existing house patterns: `## Title` + `<hr>`, `<div class="fig">` +
   `<figcaption>`, `<div class="formula">`, `<div class="note">`, `<!-- _class: part -->`
   dividers with the `band` markup, `<!-- speaker notes -->` where useful.
8. Part dividers now count **07**, not 06 — there is a new closing part.
9. Figure widths: a figure in a `cols` column gets `w:520`; a full-width figure gets
   `w:760` and **never** more — the old `w:900` on slide 019 pushed its own caption and
   note off the bottom of the frame.

---

# Slide list

## Front

**1. Title** — unchanged from the current deck (`_class: lead`).

**2. Roadmap for today** — currently two columns of text (L1 Blocker). Rebuild as a
**single** column using `<div class="steps-list">` with seven rows, `01`…`07`, one line
each: the puzzle · abstraction · degree and Euler · vocabulary · connectivity ·
representation · edge cases. No `cols`.

---

## Part One — The puzzle

**3. Part divider** — `Part One` / `01 / 07` / "The puzzle".

**4. The Königsberg bridge problem** — keep essentially as-is. This slide is the rubric's
own Pass example: story, place, date, question in the formula panel, `konigsberg-map.png`,
conversational note. Do not touch it beyond the `w:520` width rule.

**5. Your turn** — currently 75% empty (P3). Keep the ten-minute activity and the worksheet
link, and add `konigsberg-sketch.png` in a `cols` right column as the thing students trace
on. Keep the "what information is essential?" prompt.

---

## Part Two — Abstraction

**6. Part divider** — `02 / 07`, "Abstraction".

**7. What can you throw away?** — **question slide**, no answer anywhere on it. Show
`konigsberg-sketch.png` and ask which of these the puzzle actually depends on: bridge
length? island area? river width? which bank you start from? Add a beat —
"turn to your neighbor, 30 seconds". This is Part Two's interactive element (S5).

**8. Euler's move — the city** — `abstraction-1-map.png`. One point: everything except
*what connects to what* is about to go.

**9. Euler's move — each landmass becomes a node** — `abstraction-2-nodes.png`. One point.

**10. Euler's move — each bridge becomes an edge** — `abstraction-3-graph.png`. One point,
plus the 1736 note: this abstraction founds graph theory. This is the payoff of the build.

**11. A graph, written down** — the $G=(V,E)$ formula panel **only**, beside
`abstraction-3-graph.png`: $V$ = nodes, $E$ = edges, four landmasses, seven bridges. The old
slide also defined multigraph and self-loop here — that was a P1 Blocker and an L1 Blocker.
They now get their own slides.

**12. Two bridges, one pair** — open with the question in the body ("Königsberg has two
bridges between the same pair of landmasses. Count them once, or twice?"), then a `*`
fragment reveals: both count — collapse them and you are solving a different puzzle. Figure
`multigraph.png`. Do **not** mention degree here — degree does not exist yet (N1).

**13. An edge to itself** — a self-loop is an edge from a node to itself; figure
`selfloop.png`. Do **not** state the "contributes 2 to degree" rule here — it moves to
Part Seven, where degree exists and it is posed as a question.

---

## Part Three — Degree and Euler's theorem

**14. Part divider** — `03 / 07`, "Degree and Euler's theorem", subtitle "Parity is the
whole argument".

**15. Degree** — definition only: $k_i$ is the number of edges attached to node $i$.
Figure `degree-definition.png`. One point.

**16. You are mid-walk. How many edges do you use?** — **question slide**. You arrive at a
node in the middle of your walk and later leave it. Ask how many edges that consumes, and
give the beat ("30 seconds").

**17. Edges come in pairs** — the answer: arrive by one, leave by another, so an interior
node consumes edges two at a time. Figure `parity-even.png`.

**18. What if the degree is odd?** — **question slide**. One edge cannot find a partner —
what does that force?

**19. One edge left over** — the answer: an odd node must be where the walk **starts** or
**ends**. Figure `parity-odd.png`.

**20. So a walk has at most two odd nodes** — the consequence, alone on its own slide in a
`formula` panel. This is the deck's key claim and in the old version it was welded to the
bottom of a bullet list (L4). Give it room. A short `.note` may add: a walk has two ends,
so at most two odd nodes.

**21. Your turn: count Königsberg** — the activity (S5). Figure `konigsberg-blank.png`.
"Count the bridges at each landmass. How many landmasses have an odd count? Hands up when
you have an answer — possible, or impossible?" No answer on this slide.

**22. The verdict** — figure `konigsberg-degrees.png` (degrees printed inside the discs;
the old table is deleted — L2 Blocker). A `*` fragment list reveals: three, three, five,
three · all four odd · at most two allowed · **impossible**. Use the same N/S/A/B names as
the figure (the old slide's "North shore / Island A" mismatch was a Minor).

**23. Eulerian path** — the theorem. A trail using every edge exists iff the graph is
**connected** and exactly **0 or 2** nodes have odd degree. Figure
`euler-path-example.png`. Because *connected* is not defined until Part Five, give the
one-line working definition inline — "you can reach every node from every other; made
precise in Part Five" (N1 finding).

**24. What if you must return to where you started?** — **question slide**. The old deck
asked this and answered it in the same sentence (N4).

**25. Eulerian circuit** — the answer: a closed walk has no ends, so the "exactly two odd"
case disappears — **every** node must be even. Figure `euler-circuit-example.png`.
Königsberg fails either way.

**26. Which two bridges would you destroy?** — **question slide** (S5 activity). "You want
to make the walk possible. Which two bridges do you remove? Turn to your neighbor — 30
seconds." Figure `konigsberg-degrees.png` again so they can work from the degrees.

**27. A tragic epilogue** — WWII; Königsberg is bombed and two bridges are destroyed; five
remain and only **two** landmasses are left odd, so the 200-year impossible walk becomes
possible by accident of war. Figure `konigsberg-bombed.png` — **not** the scanned engraving,
which carried three unexplained overlays and still showed seven bridges under a "five
remaining" caption (F1 Blocker + F4).

---

## Part Four — Vocabulary

**28. Part divider** — `04 / 07`, "Vocabulary", subtitle "Name the journeys precisely".

**29. Walk** — anything may repeat. Figure `campus-walk.png`. The old table is deleted
(L2 Blocker) and the definitions are now carried by the drawn routes (F4).

**30. Trail** — no edge twice. Figure `campus-trail.png`. Note that the *node* may still
repeat — you can pass the same corner without reusing a street.

**31. Path** — no node twice. Figure `campus-path.png`. A `.note` may add: every path is a
trail; not every trail is a path.

**32. Your turn: find a trail that is not a path** — the activity (S5). Figure
`campus-base.png`. "Trace one on the campus graph. Hands up when you have it." No answer.

**33. Circuit and cycle** — the closed versions: a circuit is a closed trail, a cycle is a
closed path. Figure `circuit-vs-cycle.png`. Use a two-item `*` fragment list. Do **not**
re-define "Eulerian trail / Eulerian circuit" here — slide 23 and 25 already own those
names, and repeating them was a P1 Blocker and a P3 Minor.

**34. Writing a graph as a matrix** — $A_{ij}=1$ when $i\sim j$, else 0; for a multigraph
$A_{ij}$ is the *number* of edges. Figure `adjacency-matrix.png`. One point.

**35. Multiply $A$ by itself. What do the entries mean?** — **question slide**, with the
beat. The old deck stated this surprising result flat (N4).

**36. $A^k$ counts walks** — the answer, in a `formula` panel:
$(\mathbf{A}^k)_{ij}$ is the number of walks of length $k$ from $i$ to $j$. Figure
`adjacency-squared.png`. A `.note`: walks, not paths — repetition allowed; later modules
reuse this for clustering and centrality.

---

## Part Five — Connectivity

**37. Part divider** — `05 / 07`, "Connectivity", subtitle "Euler's theorem quietly assumed
you can get everywhere".

**38. Can you get from any node to any other?** — a graph is **connected** when a path
exists between every pair. Figure `connected-vs-not.png`. One point — components are the
next slide, not this one (the old slide defined both at once, P1 Blocker).

**39. Components** — when the answer is no, the graph splits into **connected
components**: maximal sets of mutually reachable nodes. Figure `components-band.png` at
`w:760`. The old `w:900` pushed the caption and the note off the bottom of the slide
(content was lost — Blocker).

**40. Your turn: run the sweep** — the activity (S5) and the traversal method in one build.
Use a `*` fragment list of three steps — pick an unvisited node and mark it; visit its
unvisited neighbors until stuck; everything touched is one component, and if nodes remain,
start again — with `sweep-3.png` beside it. Prompt: "run it by hand on the figure; how many
sweeps?" A `.note` may mention that the cost is $O(N+M)$ and that visiting breadth-first
also yields shortest-path distances, needed in Module 2. **Do not** put "DFS and BFS" in the
title: the old slide promised a distinction it never delivered and never expanded either
acronym (N1).

**41. A component has 1,000 nodes. Is it giant?** — **question slide** with the beat. The
old deck buried this, its best question, in a gray footnote below the answer (N4).

**42. The giant component** — the answer: it depends on $N$. 1,000 is giant in a network of
1,200 and negligible in 10 million; a component is **giant** when it holds a finite fraction
of all nodes as $N$ grows. Figure `giant-scale.png` — the old slide was pure prose (N2). A
`.note`: in practice we extract the giant component and work there; *when* one exists is
Module 3.

**43. Edges with direction** — in a **directed** graph each edge has an orientation, so
reachability need not be symmetric. Figure `directed-arrows.png`. One point only — the old
slide introduced direction, strong, and weak together (P1 Blocker), and its arrowheads were
invisible at slide size (F3 Blocker).

**44. Strong and weak** — a `*` fragment list of two: **strongly connected**, a directed
path from every node to every other; **weakly connected**, connected once you ignore
direction. Figures `directed-strong.png` and `directed-weak.png`. A `.note`: every strong
component is weakly connected; the converse fails.

---

## Part Six — Representation

**45. Part divider** — `06 / 07`, "Representation", subtitle "How a computer holds a
network".

**46. How would you store a network?** — **question slide** (S5 activity). "You have a
million nodes and you need to answer *who are node 7's neighbors?* a billion times. How
would you lay it out in memory? 30 seconds with your neighbor." No answer.

**47. Edge list** — a list of pairs; compact on disk, but a neighbor query means scanning
everything. Figure `store-edgelist.png`. One representation per slide — the old single
slide was a three-way `cols3` text layout (L1 Blocker) with no figure (N2).

**48. Adjacency list** — each node's neighbors; neighborhood traversal is immediate.
Figure `store-adjlist.png`.

**49. Adjacency matrix** — an $n\times n$ grid of 0/1; opens the door to linear algebra,
but costs $O(n^2)$. Figure `store-matrix.png`. A `.note` may close the trio: degree is the
same quantity three ways — count incidences, list length, row sum. The old "Degree, three
ways" slide (a Python block plus a 3×3 table — L3 + L2 Blockers) is **deleted**; this note
is all that survives of it.

**50. A dense matrix for eight billion people — how much memory?** — **question slide**.
Let them guess before the reveal.

**51. Store only the nonzeros** — the answer: 512 exabytes, so keep only what is there.
Three arrays, revealed as a `*` fragment list: **data** (the values), **indices** (the
column of each nonzero), **indptr** (where each row starts). Figure `csr-build.png`. Then a
`formula` panel with $k_i = \mathrm{indptr}[i+1]-\mathrm{indptr}[i]$ and the headline
$O(n^2)\rightarrow O(m+n)$. Set the three array names in **bold body face, not backticks**
(the old inline monospace was a borderline L3). Carry the sentence "one matrix row is one
contiguous slice" in the slide body — it was an unreadable 11px line inside the old figure.

**52. Which format when?** — figure `format-regimes.png` as the whole slide. The old version
was two columns of text with no figure (L1 Blocker + N2). One `.note` carries the single
prose notebook pointer allowed in the deck: edge list on disk, sparse matrices for analysis,
hands-on in the Module 01 notebook.

---

## Part Seven — Edge cases *(new — this part did not exist)*

The deck's fourth act was an implementation chapter, so the arc never closed (S4 Major).
This part collects the four edge cases the old deck answered in passing and poses each as a
question first. Each pair below is **question slide → answer slide**.

**53. Part divider** — `07 / 07`, "Edge cases", subtitle "The graphs that break the rules".

**54. Does a self-loop add 1 to a node's degree, or 2?** — **question slide**, figure
`selfloop.png`, with the beat.

**55. Two** — both endpoints attach at the same node, so a self-loop contributes 2. Figure
`selfloop.png`. Note that this keeps the parity argument intact: a self-loop never changes
a node's parity.

**56. Is a single node with no edges connected?** — **question slide**, figure
`edge-single-node.png`.

**57. Yes — vacuously** — there are no pairs to fail the test, and a lone node is a
component of its own. Figure `edge-single-node.png`.

**58. Every node has even degree, and yet there is no Euler circuit. How?** —
**question slide**, figure `edge-disconnected.png`. The beat: 60 seconds, draw one.
This replaces the deleted `has_euler_path` code slide (L3 Blocker) with the counterexample
that slide was gesturing at.

**59. The graph is in two pieces** — the answer: parity alone is not enough; Euler's
theorem requires **connectivity** too, which is why the sweep of Part Five is not optional.
Figure `edge-disconnected.png`.

**60. What breaks when edges have direction?** — **question slide**. Degree splits — into
what?

**61. In-degree and out-degree** — the answer: each node now has two counts, and Euler's
condition becomes "in-degree equals out-degree at every node". Figure `directed-arrows.png`.

---

## Wrap-up

**62. Module 01 review** — figure `recap.png` as the spine, with a `*` fragment list of the
module's beats revealed one at a time: abstraction (1736) → graph theory · Euler: connected
plus 0 or 2 odd degrees · walk, trail, path, circuit, cycle · $(\mathbf{A}^k)_{ij}$ counts
walks · components and the giant component · edge list, adjacency list, matrix · CSR in
$O(m+n)$. The old version was two columns of text with no figure (L1 Blocker + N2).

**63. Coming up in Module 02** — small worlds: almost all eight billion people are a handful
of friendships away; short paths, high clustering, one rewiring model that delivers both.
Figure `smallworld-teaser.png` — **not** `abstraction.png`, which was reused verbatim from
slide 007 with captions that made no sense here (F1 Blocker + F4).

---

## Self-check before reporting done

- `grep -c '|---' m01-euler-tour.md` → **0**
- `grep -c '```' m01-euler-tour.md` → **0**
- `grep -c 'cols3' m01-euler-tour.md` → **0**
- Every `<div class="cols">` contains exactly one `<div class="fig">`.
- `grep -c '^\* ' m01-euler-tour.md` → **at least 10** (fragments now exist).
- Every `![...](figures/....png)` names a file that exists in `figures/`.

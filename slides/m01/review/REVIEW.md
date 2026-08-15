# Slide review — slides/m01/m01-euler-tour.md — 2026-08-04

**Verdict:** FAIL
**Slides:** 30 · **Blockers:** 29 · **Majors:** 53 · **Minors:** 19

Reviewed by three independent passes (slides 1–10, 11–20, 21–30), each rendering
all 30 slides to PNG and inspecting every image, plus a deck-level structure pass.

## Milestones (S5)

- Part 1 **The puzzle** (3–5) — demo: **yes** (worksheet + 10-minute trace, slide 5)
- Part 2 **Abstraction** (6–8) — demo: **MISSING**
- Part 3 **Degree and Euler** (9–13) — demo: **MISSING**
- Part 4 **Vocabulary** (14–17) — demo: **MISSING**
- Part 5 **Connectivity** (18–22) — demo: **MISSING**
- Part 6 **Representation** (23–28) — demo: **MISSING** (only a passive prose pointer
  to the notebook on slide 27)

## Four-act arc

- **S1 Act 1 — story:** PASS. Slide 4 opens on 18th-century Königsberg with place,
  river, and bridge count before any definition.
- **S2 Act 2 — math of that story:** PASS. Parts 2–3 abstract and solve Königsberg
  itself, not a fresh toy graph.
- **S3 Act 3 — generalization:** PASS. Parts 4–5 lift the argument to general graphs.
- **S4 Act 4 — edge cases as prompts:** **MAJOR.** The final movement is Part 6
  "Representation" — an implementation chapter. The genuine edge cases are scattered
  earlier and each is answered in the same breath it is raised: self-loops (slide 8),
  the single-node graph ("Is a single node connected? Yes — vacuously", slide 19),
  disconnected graphs (slide 28), directed graphs (slide 22). None is posed to
  students first.

---

## Blockers

### One point per slide (P1)

1. Slide 008 "A graph, written down" — P1 — Three new definitions land at once:
   the $G=(V,E)$ formula panel, a "Multigraph" block, and a "Self-loop" block whose
   "contributes 2 to degree" rule forward-references degree (undefined until slide 10).
   — Fix: split into a build — $G=(V,E)$ on Königsberg, then multigraph with the two
   parallel N–A bridges drawn, then self-loop; move the "contributes 2" rule to the
   degree slide.
2. Slide 010 "Degree and the parity argument" — P1 — Defines degree $k_i$, argues the
   arrive-by-one/leave-by-another pairing mechanism, and states the "at most two odd
   nodes" result — three teaching moves on one static frame. — Fix: three slides —
   define degree on the Königsberg graph, pose and answer the pairing question, then
   state the consequence.
3. Slide 012 "Eulerian path and circuit" — P1 — Defines the Eulerian path (numbered
   conditions) and then, in the formula panel below, the Eulerian circuit as a
   separate condition. Two definitions, the second a special case of the first.
   — Fix: split; slide B asks "what changes if we must return home?" before revealing
   the all-even condition.
4. Slide 016 "Circuit, cycle, and Euler's language" — P1 — Defines circuit, cycle,
   Eulerian trail/path, and Eulerian circuit — four terms on one slide. — Fix: keep
   circuit + cycle here as the closed counterparts of slide 015; move the Eulerian
   names into slide 012's build.
5. Slide 017 "The adjacency matrix counts walks" — P1 — Introduces $A_{ij}$, the
   multigraph extension, and the $(\mathbf{A}^k)_{ij}$ walk-counting theorem. The
   title claims only the third. — Fix: one slide defining $A$ against the picture,
   a second that asks "how many 2-step routes from 0 to 4?" then reveals $A^2$.
6. Slide 019 "Connected graphs and components" — P1 — Defines *connected* and
   *connected component* in one sentence, and the figure additionally labels a cluster
   "giant component", a third term not defined until slide 020. — Fix: this slide asks
   only "can you get from any node to any other?"; components get their own slide;
   strip the "giant component" label from the figure here.
7. Slide 022 "Directed graphs: weak vs strong" — P1 — Introduces directed graphs,
   strong connectivity, and weak connectivity simultaneously. — Fix: split into
   "direction" and "strong vs weak" slides on the same graph.
8. Slide 024 "Three ways to store the same network" — P1 — Three data structures plus
   six cost claims visible at once, no fragments. — Fix: three-slide build on a shared
   graph figure.

### Layout (L1 · L2 · L3)

9. Slide 002 "Roadmap for today" — L1 — Two columns of pure text (items 01–03 left,
   04–06 right), no figure, lower 40% empty. — Fix: single column of six numbered
   lines, or a horizontal six-step spine graphic.
10. Slide 008 "A graph, written down" — L1 — The lower two-thirds is two side-by-side
    prose columns ("Multigraph" / "Self-loop") with no figure in either. — Fix:
    single-column build, each concept with its own small diagram.
11. Slide 024 "Three ways to store the same network" — L1 — A three-way `cols3`
    layout of pure text — named explicitly in the rubric as a Blocker. — Fix: one
    slide per representation, each beside the same 5-node graph.
12. Slide 027 "When to use which format" — L1 — Two text columns, "Prefer CSR" and
    "Prefer dense", no figure. — Fix: single column, or one annotated size-vs-density
    axis with the two regimes marked as regions.
13. Slide 029 "Module 01 review" — L1 — Two text columns of three takeaways each.
    — Fix: single-column build, or a one-figure recap (the Königsberg graph
    re-annotated with degree, component, and matrix labels) revealed in six beats.
14. Slide 011 "The Königsberg verdict" — L2 — A 4-row × 3-column table (Landmass ·
    Degree · Parity) fills the left column and takes the eye first. — Fix: delete it;
    print 3, 3, 5, 3 directly on the nodes, color all four accent-2, reveal one
    landmass at a time.
15. Slide 015 "Walk, trail, path" — L2 — A 3-row table (Term · Rule). — Fix: one graph
    drawn three times as a build, each with a route in accent-2 and one caption line.
16. Slide 016 "Circuit, cycle, and Euler's language" — L2 — A 2-row table (Term ·
    Definition). — Fix: one figure showing the same closed loop twice — once revisiting
    a node (circuit), once not (cycle) — labelled on the drawing.
17. Slide 025 "Degree, three ways" — L2 — A 3×3 table (Representation · Degree of
    node 1 · Neighbors of 1) with ruled header. — Fix: cut the slide; annotate a single
    5-node graph, revealing the three "reads" onto that same figure.
18. Slide 025 "Degree, three ways" — L3 — A three-line Python block; the third line
    (`A = np.array(...)`) runs to x≈1200 of the 1280px slide, touching the margin.
    Verbatim the rubric's own L3 calibration case. — Fix: delete the code block; the
    notebook pointer on slide 027 already covers it.
19. Slide 028 "Implementing Euler's test" — L3 — A 4-line `def has_euler_path(A):`
    function dominates the slide, including the `# incomplete!` comment. — Fix: replace
    with a figure of a graph with 0 odd-degree nodes but two disconnected pieces, asking
    why parity says yes and the graph says no; drop all code.

### Figures (F1 · F3)

20. Slide 007 "Euler's move — and a new field" — F1 — The four landmass blobs are drawn
    at four visibly different sizes (left blob ≈1.5× the bottom-left one); in the right
    panel N and S are ~20% larger than A and B; and the same objects change color across
    panels (bridges red at left, edges blue at right). Nothing states that any of this
    means anything. — Fix: identical blobs, identical nodes, one consistent color for
    bridges/edges across both panels.
21. Slide 030 "Coming up in Module 02" — F1 — Same figure (`abstraction.png`): four gray
    ellipses at different sizes and aspect ratios, and the two bottom ellipses physically
    overlap. The rubric's own F1 calibration case, still unfixed. — Fix: as above.
22. Slide 010 "Degree and the parity argument" — F1 — In both panels the central node is
    ~1.8× its neighbors' diameter and filled blue (left) / red (right) while every
    neighbor is gray; the slide never says size marks the focal node or that blue/red
    encode even/odd. — Fix: one node size throughout; state the color encoding in the
    caption, or drop color and mark parity with the $k$ label alone.
23. Slide 013 "A tragic epilogue" — F1 — A scanned engraving overlaid with three
    unexplained encodings: two large hand-drawn red loops, a red arrowhead, and two
    yellow starburst icons. Nothing says the loops are a route, the arrowhead a
    direction, or the starbursts the destroyed bridges. — Fix: replace with the
    abstracted node-link figure, the two destroyed edges struck through in accent-2 and
    degrees relabelled 2/2/3/3.
24. Slide 015 "Walk, trail, path" — F1 — `campus.png` renders four nodes in four
    different fills (blue Dorm, gold Cafe, brick Gym, gray Library) with no stated
    meaning; the four buildings are interchangeable. — Fix: one neutral fill for all
    four; reserve accent-2 for the traced route.
25. Slide 017 "The adjacency matrix counts walks" — F1 — Node 1 is accent blue while
    0, 2, 3, 4 are gray, unexplained; and the same blue in the right panel means
    "entry = 1", so one color carries two unrelated meanings in adjacent panels.
    — Fix: uniform node fill; if node 1 is the worked example, say so and highlight
    row 1 in accent-3 instead.
26. Slide 019 "Connected graphs and components" — F3 (content lost) — The `w:900` figure
    runs off the bottom: the figcaption is sliced in half by the slide edge, and the note
    below it — including the student question "Is a single node connected?" — does not
    render at all. — Fix: crop the ~40% dead white space out of `components.png`, drop to
    `w:640`, move the note above the figure.
27. Slide 022 "Directed graphs: weak vs strong" — F3 (the slide's whole point is
    invisible) — Edges are pale warm-gray (#d6d1c9) on white and the arrowheads are the
    same pale gray at ~6px. At rendered slide size no arrowhead is visible; both panels
    read as ordinary undirected graphs. The arrowhead entering node A is half-occluded by
    the node disc. — Fix: arrowheads 3–4× larger in annotation gray or accent, edges ≥3px,
    arrowheads inset clear of the discs.

---

## Majors

### Structure

- **deck** — S4 — The final movement is an implementation chapter, not edge cases posed
  as questions; the real edge cases (self-loop, single node, disconnected, directed) are
  scattered earlier and each is answered as it is raised. — Fix: add a closing act that
  asks each edge case first — "Does a self-loop add 1 or 2 to degree?", "Is a single node
  connected?", "What if the graph is in two pieces?", "What changes when edges have
  direction?" — with a beat before each answer.
- **deck** — S5 — Five of six milestones have no interactive element (Parts 2, 3, 4, 5, 6).
  — Fix: one activity per part — trace the abstraction yourself; count degrees and vote on
  possible/impossible; find a trail that is not a path on the campus graph; run the
  component sweep by hand; hand-build the CSR arrays for the 5-node graph.
- **deck** — P2 — The deck contains **no Marp `*` fragment lists anywhere**; every dense
  slide is dense-and-static. Filed per-slide against 002, 007, 008, 010, 011, 012, 015,
  016, 017, 022, 024, 026. — Fix: convert reveals to `*` fragments and split the
  figure-heavy slides into build sequences.

### Figures

- Slide 007 — F4 — The left "geography" panel draws only **four** red bridge stubs against
  the seven the story requires, and at least two float, touching no blob at either end;
  the right panel has all seven edges, so the 7→7 mapping that is the slide's point cannot
  be verified. — Fix: seven bridges, each visibly landing on two blobs, in the same
  arrangement as the right panel.
- Slide 007 / Slide 030 — F2 — The straight N–B edge crosses the outer N–A curve near its
  midpoint, and S–B crosses the outer S–A curve symmetrically. The Königsberg multigraph is
  planar. — Fix: N top, S bottom, A center, B right; bow the parallel edges outward so
  nothing crosses.
- Slide 007 / Slide 030 — F3 — Node labels N, A, B, S are ~7px white-on-black, smaller than
  the figcaption; panel headers ~9px. — Fix: node labels at least figcaption size, panel
  headers at body size.
- Slide 010 — F4 — The argument is that edges are consumed **in pairs** with one **left
  over** at an odd node, but no edges are paired and no leftover is highlighted, even
  though the caption promises "leftover edge". — Fix: bracket the even panel's edges into
  two color-matched pairs; on the odd panel pair two and draw the third in accent-2.
- Slide 010 — F3 — Edges are thin light-warm-gray on white and the leaf nodes the same
  light gray, so both nearly vanish; only the two center discs read from a distance.
  — Fix: annotation gray or black at heavier stroke.
- Slide 011 — F2 — N–B crosses the upper N–A bow, S–B crosses the lower S–A bow, and the
  three edges arriving at B converge and visually merge before the node, so they cannot be
  counted. — Fix: A and B on a horizontal axis, N and S above and below.
- Slide 011 — F3 — The "deg 3" label for S overprints the red caption "four odd-degree
  nodes → impossible"; neither string is readable. The "deg 3" label for N is bisected by
  an edge. — Fix: degree numbers inside the node circles, white on dark; delete the
  floating labels.
- Slide 013 — F4 — The claim is "only two odd-degree landmasses", but the figure shows no
  degrees and still shows seven bridges while the figcaption reads "five bridges
  remaining". — Fix: abstracted graph, two edges removed, degrees 2/2/3/3 on the nodes,
  the two odd ones accent-2.
- Slide 013 — F3 — The engraving's own a–g / A–D labels are small serif letters over dense
  black hatching, unreadable at slide size; the source's printed caption block
  "FIGURE 98. Geographic Map: The Königsberg Bridges" is left in and competes with the
  slide's own figcaption. — Fix: replace the scan; at minimum crop the printed caption.
- Slide 015 — F4 — `campus.png` is a static square with one diagonal. No route is drawn and
  no repetition shown, so it illustrates nothing about walk vs trail vs path — the table
  carries the definitions and the figure is decoration. — Fix: draw the three journeys as
  a three-step build.
- Slide 015 — F3 — Edges are pale warm gray at thin weight; the "Library" label overflows
  its node circle on both sides. — Fix: darken and thicken edges; shorten labels or enlarge
  nodes.
- Slide 017 — F3 — At `w:480` each panel gets ~230px: matrix index labels ~9px, panel
  headings gray-on-white at similar size, edges the same pale gray as slide 015. — Fix:
  split into two slides so each figure gets full width; darken index labels.
- Slide 019 — F2 — Two nodes in the giant component overlap and the edges around them
  cross, in a 9-node graph that is easily planar. — Fix: re-layout with no overlap and no
  crossings.
- Slide 019 — F4 — The three components are scattered with a large empty region through the
  middle and right, and the single label "small components" sits between the two gray
  clusters, ambiguously belonging to neither. — Fix: one horizontal band; label each
  cluster, or bracket the two gray ones.
- Slide 026 — F4 — The gold highlight marks positions 2–4 of `data` and `indices`, but
  row 1 of the dense matrix is not highlighted, and neither are the `indptr` cells (2 and 5)
  that define the slice. The figure's whole job — one matrix row becomes one contiguous
  array slice — has no visual link between the three objects. — Fix: shade row 1 and
  `indptr[1]`/`indptr[2]` gold; draw connectors to the gold run's boundaries.
- Slide 026 — F3 — The explanatory line "row 1 → data[indptr[1]:indptr[2]] · degree =
  indptr[i+1] − indptr[i]" renders at ~11px, smaller than the page number; and `data` /
  `indices` have 12 unlabelled cells, so a student cannot verify that indptr 2 and 5 select
  the gold run. — Fix: raise the line to body size or move it into the slide body; print
  0…11 position labels.
- Slide 030 — F4 — The figure is `abstraction.png`, already used verbatim on slide 007, and
  its panel captions still read "geography (ignore this)" / "relationships (keep this)" —
  meaningless in a small-worlds teaser. — Fix: a ring lattice with a few rewired long-range
  shortcuts, or no figure.

### Narrative

- Slide 011 — N4 — This is the payoff of the entire opening act and it lands flat: the
  table and "Four odd nodes. At most two allowed. **Impossible.**" appear together, with
  no question and no thinking beat. — Fix: "Count the bridges at each landmass — how many
  are odd? Take 30 seconds", reveal the degrees one at a time, then the verdict.
- Slide 010 — N4 — "A walk has at most **two** odd-degree nodes" arrives in the same static
  frame as the definition that motivates it, and nothing between slides 006 and 010 asks
  the student anything. — Fix: a question slide first ("You're mid-walk at a node. How many
  edges do you use up each visit? What if the node has an odd number?").
- Slide 012 — N4 — The note literally opens "Question: if we require return to the start…"
  and answers itself in the same sentence. — Fix: the question alone on the slide, the
  answer on the next.
- Slide 012 — N1 — Condition 1 is "the graph is **connected**", but *connected* is not
  defined until slide 019, seven slides later. — Fix: a one-line working definition here,
  or move Part Five ahead of the theorem.
- Slide 012 — N2 — Text only — no figure, on the slide stating the central theorem of the
  module. — Fix: two small graphs, one with two odd nodes (endpoints marked), one all-even,
  each with its route traced.
- Slide 013 — N4 — "The 200-year impossible puzzle becomes possible" is asserted. This is
  the deck's single best natural question, spent as a statement. — Fix: "Which two bridges
  would you destroy to make the walk possible? Turn to your neighbor — 30 seconds."
- Slide 016 — N2 — Table + prose + bullets, no visual, for four trivially drawable
  definitions.
- Slide 017 — N4 — $(\mathbf{A}^k)_{ij}$ counting walks is a genuinely surprising result,
  delivered as a bare statement in a highlighted panel. — Fix: "Multiply $A$ by itself.
  Any guess what the entries mean? Take 30 seconds."
- Slide 020 — N2 — Pure prose on a slide whose entire content is a claim about relative
  size. — Fix: two node-blobs at $N=1{,}200$ and $N=10^7$ showing the same 1,000-node
  cluster once dominant, once a speck.
- Slide 020 — N4 — "1,000 nodes is giant in a network of 1,200 and negligible in 10 million"
  is the memorable idea and is handed over as a gray footnote below the answer. — Fix: pose
  it as the question first.
- Slide 021 — N2 — 100% text: three numbered steps plus a gray note in the top ~45%, bottom
  half empty. — Fix: build the sweep on the components figure, coloring newly-visited nodes
  as the frontier expands.
- Slide 021 — N1 — The title promises a DFS-vs-BFS distinction the slide never delivers; the
  three steps are neither, the difference is buried in a gray note, and the acronyms are
  never expanded anywhere in the deck. — Fix: retitle to "Finding components by traversal"
  and drop the acronyms, or add a two-panel figure of the two visit orders.
- Slides 015–017 (Part Four) — N3 — No direct address and no question mark anywhere in the
  part; textbook monologue throughout.
- Slides 023–030 (Part Six) — N3 — Not a single question mark, not one "you", no direct
  address of any kind. Seven consecutive slides (023–029) with exactly one figure between
  them.
- Slide 024 / 025 / 027 / 029 — N2 — No figure at all on any of the four.
- Slide 028 — N4 — Code, `# incomplete!`, the boxed answer, and the resolution note appear
  simultaneously. — Fix: slide A shows the flawed test and asks "Can you draw a graph this
  gets wrong? 60 seconds"; slide B reveals the disconnected counterexample.
- Slide 008 — P2 · Slide 022 — P2 · Slide 026 — P2 — Dense and fully static (see deck-level
  P2 above).
- Slide 025 — P2/P3 — Beyond the code and table it adds nothing over slide 024: the same
  three representations and the same count/len/sum contrast that slide 024's note already
  states. — Fix: cut; fold the one new fact (all three give 3) into the 024 build.

### Rendering / CSS

- Slide 002 — L4 — Each gray `.note` sits flush against the **next** bold heading rather
  than its own, so "Seven bridges, one frustrating walk" visually groups with
  "02 Abstraction" and so on down both columns. Cause: `section .note { margin: 0 }`
  (network-science.css:161). — Fix: small top margin and larger bottom margin on `.note`.
- Slide 007 — L4 — "What remains is a new mathematical object: a **graph**." is welded to
  the bottom of numbered item 2 with zero gap, so it reads as a continuation of "Each
  bridge → an edge". Cause: `section ul, section ol { margin: 0 }` (network-science.css:141).
- Slide 010 — L4 — "A walk has at most **two** odd-degree nodes." butts directly against the
  second bullet, so the deck's key claim looks like a wrapped continuation of "must be start
  or end". Same cause. — Fix: this line should be the most separated element on the slide,
  not the least.

---

## Minors

- Slide 005 "Your turn" — P3 — Three short lines in the top ~25%; ~75% blank. — Fix: add the
  bare Königsberg sketch to trace on, plus a QR code (a hyperlink is not clickable from a
  lecture-hall seat).
- Slide 008 — N3 — Textbook monologue: no question, no direct address, unusual for this deck.
  — Fix: "Königsberg has two bridges between the same pair of landmasses. Should we count
  them once, or twice?"
- Slide 008 — L4 — The gray note renders flush against the left column, reading as a fourth
  line of the Multigraph paragraph. Same `.note { margin: 0 }` cause.
- Slide 010 — F5 — Edges and leaf nodes use a light warm gray that is not the theme's
  annotation gray `#6b6b6b`.
- Slide 011 — N1 — The table names landmasses "North shore / South shore / Island A /
  Island B" while the figure labels them "N / S / A / B". — Fix: identical labels, or drop
  the table (the L2 fix resolves this).
- Slide 012 — P3 — Bottom ~40% empty white. — Fix: resolved by adding the figure.
- Slide 013 — F5 — Pure saturated red and yellow starbursts, no theme tokens; the red sits
  close enough to accent-2 to be confused with the deck's "odd degree" encoding.
- Slide 015 — F5 — Node fills spend accent, accent-3 and accent-2 on decoration, leaving
  accent-2 unavailable for marking a route.
- Slide 016 — P3 — The two bullets restate slide 012 in different words. — Fix: cut.
- Slide 016 — L4 — Two separate lists on one slide (the table and the bullets).
- Slide 020 — P3 — Bottom ~40% empty white; the message is already carried by slide 019's
  figure labels.
- Slide 021 — L4 — The gray note sits flush against step 03 (~35px baseline gap vs ~62px
  between steps), so it reads as a fourth step. Same `.note` cause.
- Slide 022 — F4 — The figcaption "cycle vs one-way chain" renders ~100px below the figure
  and horizontally offset, reading as orphaned; it also names the panels differently from
  the in-figure captions ("strongly connected" / "weakly, not strongly"), giving two
  competing names for one distinction.
- Slide 026 — F5 — The blue nonzero cells overshoot the beige grid field by 3–4px at the top
  and left, giving the matrix a ragged, misregistered outline.
- Slide 026 — L3 (borderline) — `data`, `indices`, `indptr` render in monospace inline and
  the boxed formula in typewriter face. These are CSR array names rather than Python syntax,
  so this sits at the edge of the rule. — Fix: body face, bold; math type for the degree
  relation.
- Slide 027 — P3 — Top ~40% only; bottom 55% empty, and it largely restates slide 024.
- Slide 030 — F5 — The right panel's nodes are pure black and its edges a brighter blue than
  accent `#3959A6`; the left panel's bridge segments a red close to but not accent-2.
- Slide 025 — F3 — The third code line touches the right margin and reads as clipped. Moot
  if the slide is cut.

### Dismissed

- Slide 004 "The Königsberg bridge problem" — a reviewer proposed F4 (the seven bridges
  cannot be located on the antique engraving). The rubric lists this slide as its **Pass**
  calibration example; dismissed.

---

## Root causes

1. **No progressive disclosure exists in the deck.** Zero `*` fragments, zero build
   sequences. Every dense slide lands at once. This alone accounts for 12 Majors.
2. **Figures decorate rather than teach.** Unexplained size and color encodings,
   avoidable crossings, pale strokes below legibility, and — repeatedly — a figure that
   does not show the thing the slide claims (slide 007's four bridges, 013's seven
   bridges under a "five remaining" caption, 015's route-less campus, 026's unlinked
   highlight, 022's invisible arrowheads).
3. **Parts 4–6 abandon the deck's own method.** Six tables, two code blocks, three
   multi-text-column layouts, no questions, no activities — while Parts 1–3 are
   conversational and story-driven.
4. **Act 4 is missing.** The deck ends on implementation rather than probing edge cases
   as questions, and the edge cases it does raise are answered in the same breath.

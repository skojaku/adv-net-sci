# Round-4 fixes

Blockers have gone 29 → 7 → 4. Most of the remaining Majors are not independent — they
trace to three policies the figure generator does not have. Fix the policies once and the
individual findings mostly go with them.

## Three systemic policies (fix these first)

### Policy 1 — accent-2 means exactly one thing per figure, and the slide says what

`#B14434` currently means, across four slides in Part Three alone: the leftover edge (019),
the start/end nodes **and every edge** (020), the odd-degree nodes **and their degree
numbers** (022), every edge again (023), and the `start = end` node which is *even* (025).
On 023 it marks odd nodes while on 025 it marks an even one. Elsewhere it marks a traced
route (029–032), a highlighted correspondence (035), a revisited node (030, 033) and a
removed bridge (027).

Rule: in any one figure, accent-2 carries **one** meaning, and either the figcaption or an
in-drawing label states it. Everything else is `INK` for structure and `MUTED` for
annotation. Concretely:

- `euler-path-example.png` (023) and `euler-circuit-example.png` (025): edges back to the
  standard structural colour. On 023 keep accent-2 for the two odd nodes only. On 025 the
  centre node is degree 4 — **even** — so it must not be accent-2 at all; mark `start = end`
  with a thin ring and a label.
- `parity-bound.png` (020): edges to the standard colour; accent-2 for the two ends only.
- `campus-walk.png` (029): hide the underlying structural edge on the segment the route
  doubles back over — the two red curves plus the surviving gray straight edge read as
  three parallel edges where the graph has one.

### Policy 2 — one bbox and figsize policy for every figure

Some PNGs are 85–97% blank canvas, which pushes captions ~200px from the mark they caption
and shrinks the drawing (`edge-single-node.png` is 15% × 17% ink; `selfloop.png` 23% × 40%).
Meanwhile `edge-disconnected.png` is cropped so tight that all six node discs are cut by the
bbox — flat tops and flat sides. And `format-regimes.png` (1572×1164) inside `.fig.tight`
renders ~367px wide, making its own labels 7–11px, below the 13px page number.

Rule: every figure saves with `bbox_inches='tight', pad_inches=0.15` — enough that node
discs and labels clear the frame, not so much that the canvas is mostly white — and its
`figsize` is chosen so the drawing fills its rendered column at the applicable CSS height
cap (430px normally, 320px under `.fig.tight`, 190px under `.fig.stack`). Wide slides get
wide figures. After regenerating, report ink coverage as a fraction of canvas for every
figure; anything below ~50% in either dimension needs re-cropping, and anything touching
the bbox edge needs more pad.

### Policy 3 — a figcaption must say something the slide does not already say

Captions currently restate the slide title verbatim (044 "edges now have direction" under
"Edges with direction"; 049/050/051; 035 "a graph and its matrix"), or restate the body
sentence word for word (030, 031, 032, 050, 058), or restate a label baked into the PNG
(025 "start = end"; 054's degree identity, which now appears three times — formula panel,
in-figure annotation, and caption). One slide, one statement of a fact.

Also: `directed-strong.png` and `directed-weak.png` **reintroduced baked-in titles** that a
previous round had stripped deck-wide ("strongly connected: you can get anywhere" contains
the slide title verbatim). Strip them again and keep the figcaption as the single channel.

## Blockers

1. **Slide 022 "The verdict" — N1 — a false statement, unqualified.** Bullet 3 reads "A walk
   allows **at most two** odd nodes" with no premise anywhere on the slide. This is false: a
   walk may pass through arbitrarily many odd-degree nodes. It is also the step that
   licenses "Impossible", so the deck's central argument rests on it. The premise was added
   to slides 016 and 020 in round 3 but not here. **Fix:** "A walk **that crosses every
   bridge exactly once** allows at most two odd nodes."

2. **Slide 041 "Your turn: run the sweep" — F4 — the worked answer is wrong and unreadable.**
   Two separate defects in the visit-order numbering on `sweep-3.png`:
   (a) The numbers are drawn in a gray close to the edge colour, on top of the edges and
   partly under the discs — "1" is essentially gone, "2/3/4" are cut by vertical strokes,
   and 5–8 sit on the dashed enclosure line.
   (b) **The order is not a valid traversal.** The bottom row runs left→right 1,2,3,4 and the
   top row left→right 5,6,7,8, so step 4 (bottom right) jumps to step 5 (top left) between
   two nodes that are not adjacent. Depth-first would give 8,7,6,5 along the top; breadth-
   first would reach the top-left node third. It matches neither.
   This is the slide that tells students to trace the traversal by hand, so the model answer
   must be correct. **Fix:** place the numbers outside the discs in annotation gray, clear of
   every edge and of the dashed enclosure, and renumber so the sequence is an actual
   depth-first walk over the adjacency you drew. Assert the order is a valid walk in the
   generator.

3. **Slide 041 — N4/S5 — the exercise gives away its own answer.** The body asks "How many
   sweeps until every node is marked?" while the figure bakes in "sweep 1 / sweep 2 /
   sweep 3" and the figcaption reads "three sweeps, three components". **Fix:** remove the
   count from both the enclosure labels and the caption; the answer belongs on the next
   slide or in the speaker notes.

4. **Slide 027 "A tragic epilogue" — F4/N1 — the destroyed bridges attach to nothing.** The
   two dashed curves stop 12–17px short of a node at both ends, so they float; a student
   cannot tell which bridges fell. Separately, this figure puts degree numbers **inside** the
   discs and drops the N/A/B/S letters, while slide 026 — the question this slide answers —
   puts letters inside and degrees outside. A student who answered "remove one A–N and one
   A–S" cannot check it. **Fix:** run the dashed edges to the node boundaries at the same
   curvature as the live parallel edges, and match slide 026's notation exactly (letters
   inside, degrees outside).

5. **Slide 054 "The payoff: degree and memory" — P1 — two results on one slide.** Two formula
   panels ($k_i=\mathrm{indptr}[i+1]-\mathrm{indptr}[i]$ and $O(n^2)\rightarrow O(m+n)$) plus
   a third claim inside the figure ("stores nnz = 12 numbers here, not the dense 5×5 = 25").
   The title joins two sentences with "and" — it fails the one-sentence test. The deck has
   split smaller pairs three times already. **Fix:** two slides, degree first, memory second;
   `csr-payoff.png` stays on the degree slide only.

## Majors

6. **Slide 020 — N1 — the bound is still stated unconditionally** in the title and the
   formula box (`#{odd-degree nodes in the graph} ≤ 2`); the premise lives only in the gray
   note, and Königsberg contradicts the box two slides later. **Fix:** put the hypothesis
   inside the box ("if a walk crosses every edge exactly once, then …") and retitle to "A
   graph with such a walk has at most two odd nodes".
7. **Slide 020 — F3 — "start" and "end" are clipped by their own discs.** Accent-2 text
   printed onto accent-2 fills: "start" loses its top 7 of 16 rows, "end" loses its
   baseline. This is the exact defect round 3 called a Blocker on 019, reintroduced in a
   brand-new figure. **Fix:** offset both labels clear of the discs.
8. **Slide 020 — F4 — the figure does not show the slide's point.** The caption claims every
   interior node is even, but only one of the four interior nodes carries the pairing arc
   and the "even" label, and neither end is marked odd, so "≤ 2 odd" is nowhere visible.
   **Fix:** mark all interior nodes even and both ends odd.
9. **Slide 017 — F1 — each edge changes colour mid-span.** Sampling one edge inward: black at
   x=850 and x=872, then gray from x≈880 to the disc. So every edge is black on its outer
   half and gray on its inner half, unexplained, and the pairing arc is colinear with the
   edges it ties — the two upper edges plus their tie read as one smooth curve skimming the
   node rather than as a bracket. **Fix:** each edge one colour end to end; draw the tie as a
   separate arc offset ~15px clear of both edges.
10. **Slide 009 — N1 — the prose contradicts the figure.** "Nothing else about a landmass —
    its size, its shape, **its name** — survives the abstraction", beside four dots labelled
    N, A, B, S. The letters must stay (round 3 required them). **Fix:** change the prose —
    "its size, its shape, its area — is gone; only a bare label remains."
11. **Slide 046 "Weakly connected" — F4 — the caption contradicts the figure.** It reads
    "same three nodes, direction dropped" while the figure still draws A→B and B→C with
    arrowheads. **Fix:** recaption to something the figure supports ("no directed route
    returns to A"), or redraw undirected.
12. **Slide 062 — F3 — all six node discs are guillotined by the figure bbox** (flat tops at
    the figure's own top edge, flat sides at both left and right). Covered by Policy 2.
13. **Slide 055 — F3 — the figure's own labels are the smallest type in the deck** (7–11px
    against a 13px page number) because `.fig.tight` caps it at 320px and the source is
    1572×1164. Covered by Policy 2: regenerate wide (≈10×5in) so it fills the column at the
    cap.
14. **Slides 053/054 — F3 — the dense-A inset is now the least legible element** (10–14px
    row bands) after round 3 fixed only the array side. **Fix:** drop the inset, or set it at
    the same cell size as the arrays and place it inline to their left.
15. **Slides 057–060 — L/F4 — orphaned captions from mostly-blank canvases.** Covered by
    Policy 2.
16. **Slide 057 — F1 — the self-loop's attachment ticks read as arrowheads** at slide size
    (same gray, same weight as the loop), putting apparent direction on an undirected
    self-loop 30 slides before direction is introduced. **Fix:** short black marks
    perpendicular to the disc boundary, thinner than the loop stroke.
17. **Slide 058 "Two" — F4 — the answer slide shows the same picture as the question slide**
    (`selfloop.png`, byte-identical), and its caption claims "k gains 2" while the figure
    shows neither a 2 nor a k. This is the pattern round 3 called a Blocker on 033/034.
    **Fix:** number the two attachment points ① ② on an answer variant and print `k = 2`.
18. **Slide 064 — F3 — one arrowhead still does not arrive.** B→C touches C, C→A leaves ~7px,
    A→B stops ~10px short pointing at empty space — on the slide that teaches "edges
    arriving". **Fix:** one `shrinkB` for all three edges.
19. **Slide 023 — N3 — the deck's central theorem is unreadable as a sentence.** "A trail — a
    route that never reuses an edge, named precisely in Part Four — that uses every edge
    exactly once, an Eulerian path, exists exactly when:" — two parenthetical apologies push
    subject and predicate apart. **Fix:** three short sentences; drop the part references.
20. **Slide 029 — F3 — the annotation is struck through again.** The wording and colour fixes
    landed, but "same edge, twice" is now crossed by the Cafe→Lib red arrow, reading "same
    edge, ‹wice". **Fix:** move it off the graph entirely, into white space, with a thin
    leader if needed.
21. **Slide 035 — F1 — the correspondence the figure teaches is unstated.** Edge 1–3 is
    accent-2 in the graph and cells (1,3)/(3,1) are accent-2 outlined, with nothing saying
    they are the same fact. **Fix:** figcaption "edge 1–3 ↔ cells (1,3) and (3,1)".
22. **Slide 051 — P2 — paragraph + four-line note + figure, all static**, and the note
    introduces a new claim ("sum a row in the matrix" appears for the first time). **Fix:**
    make the note a `*` fragment.
23. **Slide 060 — N4 — a fifth question is opened and never closed.** "Is a graph that
    *contains* an isolated node — alongside other, linked nodes — itself connected?" has no
    timed beat and no answer slide, breaking the pattern the other four edge cases follow.
    **Fix:** give it a beat and an answer, or delete it.

## Minors

- Slide 002 — seven roadmap items against a ceiling of four (defensible for a seven-part deck).
- Slide 007 — the prompt asks "River width?" but the sketch draws no river; slide 008's
  sketch has no water at all, so "geography, distance" are discarded before the slide says
  they are about to go.
- Slide 008 — figure byte-identical to 005/007, so 007→008 is a text-only change.
- Slide 013 — the loop is ~110px against a 70px node; ticks read as arrowheads (same fix as
  #16).
- Slide 015 — "k = 4" prints under the bottom node, which has degree 1, and the figcaption
  repeats it. Drop one; give the survivor a leader to the centre node.
- Slide 019 — the "l" of "left over" grazes the disc; 10px more clearance settles it.
- Slide 022 — the figcaption restates two bullets and the four numbers now on the figure —
  the same fact three times.
- Slide 025 — "start = end" is pressed into the V of the two lower edges with a few px
  clearance; caption repeats it.
- Slide 027 — the "destroyed" label has no leader and sits ~20px from the nearest dash.
- Slides 029–032, 044, 049–051, 058 — captions restating title or body (Policy 3).
- Slide 033 — the accent-2 ring has no label, while slide 030's identical ring just gained
  one.
- Slide 034 — "the strictest of the three" has no antecedent on the slide.
- Slide 039 — in-figure panel titles render 50px against 27px body text, inverting the
  hierarchy; the caption repeats the same words a third time.
- Slide 042 — a question slide that does not use the `.formula` panel the other question
  slides use, so the prompt sinks into gray body text.
- Slide 043 — one blue dot means 1,000 nodes on the right and 1 node on the left, unstated;
  the blue speck is ~7px and the panel sub-labels are 15px.
- Slide 053 — indptr values 10 and 12 overflow their cells and abut, reading "8 1012".
- Slide 063 — "Every definition so far counted edges at a node without asking which way they
  point" is overbroad; direction was introduced on 044. Narrow it to degree.
- Slide 065 — the "degree → parity" leader runs past node A's boundary into the disc.
- Slides 045/046 — different canvas widths (1138 vs 981) so the graph shifts between two
  slides whose caption says "same three nodes". Covered by Policy 2.
- Deck-wide — Part Three draws edges black, Parts Five–Seven draw them annotation gray.
  Pick one structural edge colour for the whole deck.

## Verify before reporting done

    python3 figures/make_figures.py
    marp m01-euler-tour.md --theme network-science.css --allow-local-files --images png -o review/slide.png

Report ink-coverage fractions for every figure, and confirm no figure referenced by two
different slides is byte-identical unless the reuse is deliberate and stated.

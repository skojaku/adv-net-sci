# Round-3 fixes

Three final verification passes read all 65 rendered slides. Blockers are down from 29 to
7 and the systemic caption regression is closed for single-image figures, but seven
findings remain that make a slide fail its teaching job, plus a set of figure defects.

Two round-2 instructions were themselves wrong, and both are corrected here:

- The R2 list told the figure agent to make `abstraction-1-map.png` reuse
  `konigsberg-sketch.png`'s geometry "so the build starts from the actual city". That
  premise was false: the sketch is **four rounded rectangles** in a symmetric diamond, not
  landmasses. Making frame 1 identical to it could not restore the abstraction step, and
  it made slides 007 and 008 pixel-identical.
- The R2 CSS rule uses `width: auto !important`, which defeats Marp's inline width — that
  was the point — but it also made every `w:NNN` hint in the markdown inert, so per-slide
  figure sizing is gone. Slides that need a smaller figure can no longer ask for one.

## CSS — restore per-slide height control

In `network-science.css`, keep the existing `.fig` / `.fig img` rules and add:

```css
section .fig.tight img  { max-height: 320px; }
section .fig.stack img  { max-height: 190px; }
```

Use `<div class="fig tight">` on any slide where text above the figure eats the row.

## Blockers

1. **Slide 017 "Edges come in pairs" — F4 — the R2 bracket repair did not land.** Pixel
   scan at x=931: the centre disc's black run ends at y=377 and the only gray below it is a
   single 1-pixel row at y=378; at y=420 there is no gray at all. The lower "in–out" label
   at y≈493 labels an invisible mark. `rad=-0.6` was never changed and the z-order was
   never raised, so the lower bracket is still drawn inside the node. The slide's entire
   point — edges pair up two at a time — is carried by these brackets and one pair has
   none. **Fix:** give the lower bracket the same arc magnitude as the upper one with
   opposite sign, clear the 37px disc radius by the same ~55px offset the top arc uses,
   raise its `zorder` above the node patch, and set both brackets to at least the 7px edge
   weight (they currently render 4px gray against 7px black edges — the faintest mark in a
   figure whose whole job they do).

2. **Slide 019 "One edge left over" — F3 — the "left over" label is clipped and struck
   through.** Anchoring it at the edge midpoint (an R2 instruction) put it under the disc
   and on the stroke: the leading "l" has its ascender cut by the black centre disc so the
   label reads "eft over", and the accent-2 edge passes through the gap between "l" and
   "e" — accent-2 text struck through by an accent-2 line, the exact defect R2 fixed for
   the Euler examples. **Fix:** offset ~20px along the edge normal, clear of both the disc
   and the stroke, and set it in annotation gray.

3. **Slide 033 "Circuit" / 034 "Cycle" — P1 — the split landed in the markdown only.** Both
   slides embed the same `circuit-vs-cycle.png`, a two-panel figure with baked-in titles
   "circuit (closed trail)" and "cycle (closed path)". So the slide titled "Circuit"
   displays the fully-labelled cycle definition beside it, and advancing 033→034 changes
   nothing on screen (md5 confirms both load the identical file). On 033 the same sentence
   now appears three times: body text, baked-in panel title, and figcaption. **Fix:** emit
   `circuit.png` and `cycle.png` as single-panel figures with no baked-in titles, and point
   each slide at its own.

4. **Slide 041 "Your turn: run the sweep" — content off-frame.** Last content row is y=683;
   the figcaption and the `.note` carrying the $O(N+M)$ cost render nowhere. This is
   **stack** overflow, not image overflow — the CSS height cap cannot help, because
   `sweep-3.png` is only 234px tall at this width. Title + three fragment bullets + two
   paragraphs consume ~400px, leaving ~270px for figure + caption + note. **Fix:** move the
   `.note` above the figure and put the figure in a `<div class="fig tight">`.

5. **Slide 045 "Strong and weak" — F/L — the weak panel is guillotined.** This is the deck's
   only `.fig` holding two images, so the 430px cap applies to each and the budget becomes
   430 + 430 + caption inside a ~545px row. Only the weak panel's title line and node A
   survive; nodes B and C are gone, one edge runs off the bottom, ink reaches row 719 of
   720, and the figcaption never renders.
6. **Slide 045 — P1 — and it carries two definitions**, the second a relaxation of the
   first ("strongly connected" / "weakly connected"). The deck has already accepted this
   precedent twice: walk / trail / path each got a slide, and circuit / cycle were split in
   round 2. **Fix for 5 and 6 together:** split into "Strongly connected" and "Weakly
   connected", one slide and one figure each. That removes the stacked-image case entirely.

7. **Slide 054 "Which format when?" — F — the figcaption is sliced by the frame bottom.**
   The note above it survives, so the notebook pointer is safe, but "network size vs.
   density — where CSR wins" prints at rows 700–719 with its descenders shorn. The 430px
   cap does not know that a note now precedes the figure. **Fix:** `<div class="fig tight">`.

## Majors — content and correctness

8. **Slides 016–020 — N1 — the parity argument never states its premise.** Slide 016 asks
   about a node "in the middle of your walk", 017 concludes "an interior node consumes its
   edges two at a time", and 020 states the bound. But pairing up *all* of a node's edges
   is only forced if the walk uses **every edge exactly once** — a requirement that first
   appears on slide 023, three slides after the conclusion is drawn. As written, slide 020
   is **false**: a walk may pass through arbitrarily many odd-degree nodes. **Fix:** state
   the premise on 016 ("suppose your walk crosses every bridge exactly once"), and restate
   020 as a property of the graph, not of an arbitrary walk.

9. **Slide 020 — N2 — Part Three's conclusion has no visual.** Last text baseline y≈295;
   the bottom 55% is empty. Not one of N2's exemptions. **Fix:** draw a walk on a small
   graph with its two endpoints in accent-2 labelled `start` / `end` and every interior
   node even — the picture of the bound.

10. **Slides 009/010 — F4/P2 — the abstraction build has one non-change.** The two renders
    are pixel-identical except edge colour: black on 009, `#6b6b6b` on 010. Slide 009,
    titled "each landmass becomes a node", already draws all seven edges; slide 010, titled
    "each bridge becomes an edge", adds nothing and makes the edges *fainter* on the slide
    about edges. Nothing states the black→gray encoding, and gray means "annotation"
    everywhere else in the deck. **Fix:** `abstraction-2-nodes.png` becomes four labelled
    dots with **no edges** — matching the slide's own text "Four landmasses. Four dots." —
    and `abstraction-3-graph.png` introduces the edges in the standard graph colour.

11. **Slide 008 — F4 — the figure is already abstract, so the build starts past the
    abstraction.** `konigsberg-sketch.png` (used on 005, 007 and 008) is four rounded
    rectangles in a symmetric diamond: geography and shape are already discarded at frame
    1, contradicting 008's own text "Geography, distance, shape — all of it is about to
    go." **Fix:** redraw `konigsberg-sketch.png` as a real traced sketch — irregular river
    banks top and bottom, two irregular islands mid-river, seven bridges across the water —
    so 008→009 becomes a genuine blobs-to-dots step. Keep the seven bridges individually
    countable.

12. **Slide 022 "The verdict" — F4/N1 — the figure drops the node identities its caption
    depends on.** Labels N/A/B/S are replaced by degree numbers 3/5/3/3 while the figcaption
    reads "N = 3, S = 3, A = 5, B = 3". Every other Königsberg figure (008–011, 021) is
    labelled N/A/B/S, and slide 021 asks students to count degrees on exactly that labelled
    figure — so a student who counted "A has 5" cannot check the answer. **Fix:** keep the
    letter inside each node and put the degree just outside it.
13. **Slide 022 — duplicate caption.** The figure bakes "all four odd" in accent-2 serif
    under the graph and the figcaption repeats it; the bullet list says it a third time.
    **Fix:** delete the in-figure annotation.

14. **Slide 013 "An edge to itself" — F4 — the self-loop's endpoints are hidden.** The loop
    is drawn *behind* the node so both attachment points are covered by the disc, while the
    figcaption says "both ends attach here". The ring (~170px) is 1.5x the node diameter
    (109px), so it reads as a second, empty node balanced on the first. Slides 056/057 use
    the same figure and make the same claim ("Both endpoints attach at the same node") — at
    4x zoom the two ends coincide at a single point. **Fix:** shrink the loop, draw it in
    front of the node, and root it at two visibly separated points on the disc boundary
    (leave at ~135°, return at ~45°), each tick marked.

15. **Slide 041 — F4 — the sweep figure shows no sweep.** `sweep-3.png` is **byte-identical**
    to `components-band.png` (md5 `45ab347c…`), so slides 040 and 041 display the same
    picture and nothing depicts a traversal, a visit order, or a marked node. This is a
    round-2 regression: the instruction to drop the three-colour scheme removed the only
    thing distinguishing the figure. `sweep-1.png` / `sweep-2.png` are generated but never
    referenced. **Fix:** number the nodes by visit order within each component and draw a
    dashed enclosure per component labelled `sweep 1` / `sweep 2` / `sweep 3` — a distinct
    picture that does not reintroduce the accent-2 collision.

16. **Slide 044 "Edges with direction" — F4/N1 — the figure contradicts the text.** The
    prose says "you can get from A to B without any way back", but the figure is A→B→C→A, a
    directed 3-cycle in which B *does* reach A via C. It is also the same graph slide 045
    uses for "strongly connected". **Fix:** use A→B, A→C, B→C so no route returns to A.

17. **Slide 037 "$A^k$ counts walks" — F4 — the figure shows the answer, not the reason.**
    The $A^2$ matrix alone with cell (1,4) outlined; the caption asserts "2 two-step routes
    from 1 to 4" but neither route (1–2–4, 1–3–4) is drawn. **Fix:** add the 5-node graph as
    a left panel with both routes traced.

18. **Slide 053 "The payoff: degree and memory" — F4 — the figure is byte-identical to
    slide 052's, under the identical caption**, and shows neither of this slide's results:
    nothing prints $\mathrm{indptr}[2]-\mathrm{indptr}[1]=3$ and nothing depicts memory.
    **Fix:** emit a variant annotating the row-1 slice with `5 − 2 = 3 = k₁`.

19. **Slides 052/053 — F3 — CSR type is still ~9.5px**, smaller than the 18px page number,
    against 24px body text. `csr-build.png` is `figsize=(11.2, 5.6)` rendered into a ~508px
    column (scale 0.227), so `INDEX_FS = 15pt` lands at ~9.5px. The R2 note flagged this and
    the generator comment acknowledges the cap was set below the `fs()` scale to avoid cell
    overlap. **Fix:** shrink `figsize` to ~7.5in so the arrays get the whole column, or drop
    the two position-index rows — they are the least load-bearing element and removing them
    frees the scale.

20. **Slide 065 "Coming up in Module 02" — F4/F3 — the lattice half of the R2 fix did not
    land.** The shortcut fix worked (four varied-length chords, no centre pile-up), but with
    `n = 20` and `s = 620` the node discs touch and sit at zorder 3 over edges at zorder 1,
    so **both** the i↔i+1 and i↔i+2 edges are fully occluded: the ring renders as a smooth
    gray annulus with no visible edge and no visible triangle. "High clustering" is still
    unsupported by the figure. **Fix:** `n = 12`–14 and `s ≈ 180` so the second-neighbour
    chords clear the intermediate discs.

21. **Slide 060 — N1 — the prose was not updated when the figure was removed.** "Every node
    in **this graph** has degree 2" and "draw a graph like **this**" both point at a figure
    that is correctly no longer on the slide. **Fix:** "Picture a graph where every node has
    degree 2 — all even…" and "draw one yourself before the next slide".

22. **Slide 064 "Module 01 review" — F3 — the new bracket collides with a label.** The
    dashed "one component" boundary runs straight through the word "parity", cutting the
    "a", "r" and "i", and the solid leader crosses that dashed arc a few pixels below.
    **Fix:** move "degree → parity" up and left, fully outside the dashed circle, and anchor
    its leader on node A's left side.

23. **Slide 063 "In-degree and out-degree" — F3 —** node A's disc overlaps the baseline of
    its own "in 1 / out 1" label; the "/" is partly swallowed. The A→B arrowhead also stops
    ~10px short of node B while C→A meets its node. **Fix:** raise the top label ~18px;
    equalise the arrow target margins.

24. **Slide 029 "Walk" — F3/F1 —** the "×2" annotation is accent-2 text lying on the
    accent-2 return curve; the multiplication sign is sliced and reads as "‹2". The two red
    curves plus the still-visible gray straight Cafe–Gym edge present as three parallel
    edges where the graph has one, and nothing states that "×2" means one edge traversed
    twice. **Fix:** annotation gray, offset clear of both curves, worded "same edge, twice".

25. **Slide 030 "Trail" — F1 —** an accent-2 ring is drawn around Gym with nothing saying
    what it means, while the word `start` is printed beside **Lib**. A student sees one
    ringed node and one labelled node and cannot tell which is the start. **Fix:** label the
    ring `visited twice`, or drop it and ring the start node instead of using a floating
    word.

26. **Slides 025 / 027 / 043 — P2 —** each final state is three or more independent text
    blocks plus a figure with no disclosure mechanism, over the rubric's ceiling. **Fix:**
    convert the second and third blocks to `*` fragment items.

27. **Slide 039 — page-number collision.** The `.note`'s first line ends at x=1090 and "39"
    occupies x=1101–1118 on the same baseline, reading "Time to make 39 it explicit."; the
    note's last row is y=675, past the 672 usable limit. **Fix:** shorten the note to one
    line.

28. **Slide 040 — F4 —** the note says "A single isolated node counts too", but the figure's
    smallest component has two nodes: the asserted case is the one case not shown. **Fix:**
    make component 3 a singleton, or add a fourth single-node component.

## Minors

- **Cross-figure scale is still not normalised** (an outstanding R2 global item). Measured
  node diameters: slide 013 = 109px, 015 = 75px, 017 = 71px, 011 = 72px. Standardise
  `figsize`, or scale drawing units by output width.
- **Slide 015 "Degree"** — the "k = 4" label overlaps the bottom node (disc spans y 425–499,
  label gray begins y=480) and k=4 is stated three times (inside the node, below the figure,
  in the figcaption). The bare "4" also reads as a node ID, since no other node carries a
  number. Drop one of the three and move the survivor ~12px lower.
- **Slide 012** — the text says "Königsberg has two bridges between the same pair of
  landmasses" but the figure labels the nodes P and Q. Relabel to N and A.
- **Slides 048 / 049 / 050, 057 / 058** — the figcaption now repeats the slide title or the
  body sentence verbatim ("Edge list"/"edge list", "One node. No edges."/"one node, no
  edges"). The baked-in PNG titles are confirmed gone; make the captions do work the title
  does not ("node 1's edges are rows 0, 2, 3 — scattered").
- **Slide 059** — the caption asserts "one node, one component" but nothing visual marks the
  component; a thin ring would earn the word. Its new follow-on question also gets no timed
  beat and no answer anywhere, unlike the other four edge cases.
- **Slides 029–032** — "Dorm"/"Cafe" still run edge to edge inside their discs. `campus-trail`
  is 818px wide against 782px for the other three, so the graph shifts 11px between frames;
  pad all four to a common bbox.
- **Slide 025** — the figcaption repeats the in-figure `start = end` verbatim.
- **Slide 043** — "pale dots: the other 200 nodes" sits under the left panel only; the right
  panel's gray field (~10M nodes) is unlabelled, so one gray encoding carries two magnitudes.
- **Slide 002** — seven roadmap items against the rubric's ceiling of four. Defensible for a
  seven-part deck; noted only for completeness.

## Verify before reporting done

    python3 figures/make_figures.py
    marp m01-euler-tour.md --theme network-science.css --allow-local-files --images png -o review/slide.png

Then confirm no two figures referenced by different slides are byte-identical unless that
reuse is deliberate, and that every figcaption is fully inside its frame.

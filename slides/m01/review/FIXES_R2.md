# Round-2 fixes — verified against the rendered rebuild

Three independent verification passes read all 63 rendered slides. The rebuild closed
almost every original finding, but introduced one systemic layout regression and left a
set of figure-content problems. This is the fix list.

## The systemic regression (closes ~20 Blockers at once)

**Symptom.** On roughly 20 slides the `<figcaption>` — and on slide 052 the `.note`
carrying Part Six's only notebook pointer — is pushed off the bottom of the 720px frame
or sliced by it. Content is silently lost.

**Actual mechanism.** Marp emits the size hint as an inline style: the rendered HTML is
`<img ... style="width:520px;" />`. An inline style cannot be overridden by a stylesheet
rule, so `section .fig img { width: 100% }` at network-science.css:239 is **not** what is
happening — the images really are 520px wide. (Two of the three verifiers proposed this
mechanism; it is wrong. Do not "fix" the `width: 100%` declaration on that theory.)

The real cause is that **nothing constrains figure height**. Measured aspect ratios:

    graph-labeled        1.43  ->  742px at w:520
    adjacency-squared    1.29  ->  671px
    konigsberg-sketch    1.20  ->  622px
    campus-walk/trail/path 1.13 -> 589px
    adjacency-matrix     1.12  ->  580px
    abstraction-1/2/3    1.07  ->  559px
    smallworld-teaser    1.07  ->  557px
    degree-definition    1.06  ->  552px
    selfloop             1.05  ->  549px
    konigsberg-degrees   1.05  ->  546px
    konigsberg-bombed    1.05  ->  546px
    campus-base          1.05  ->  546px

A `.cols` row starts at y≈122 and the 48px bottom padding ends usable space at y≈672 —
about 545px, of which the 26px Caveat figcaption needs ~34px. So any figure whose aspect
ratio exceeds ~0.94 overflows and takes its caption off the slide.

**Fix (do both).**

1. In `network-science.css`, replace the `section .fig` / `section .fig img` block with:

   ```css
   section .fig { min-width: 0; display: flex; flex-direction: column; align-items: center; }
   section .fig img {
     max-width: 100%;
     max-height: 430px;
     width: auto !important;   /* defeats Marp's inline width:NNNpx */
     height: auto;
   }
   ```

   The `!important` is required precisely because Marp's width is inline. With it, every
   figure scales to fit both its column and the height budget, preserving aspect ratio,
   and the `w:` hints in the markdown become harmless upper bounds.

2. Trim the dead white margin baked into the PNGs (see the figure section) so figures do
   not shrink further than they must.

## Layout fixes in the deck markdown

- **Slide 038 "Can you get from any node to any other?"** — `connected-vs-not.png` is
  1610x487; in a `.cols` column it renders 157px tall with ~18px nodes and the bottom half
  of the slide empty. Drop the `.cols` on this slide: put the text above and the figure
  full width beneath it.
- **Slide 040 "Your turn: run the sweep"** — same problem: `sweep-3.png` renders 161px in
  the top-right corner while the text column runs to y≈700. Make it a full-width figure
  under the steps.
- **Slide 052 "Which format when?"** — move the `.note` (the deck's single notebook
  pointer) **above** the figure so it can never be the thing that falls off.

## Content and pedagogy fixes in the deck markdown

- **Slide 033 "Circuit and cycle" — P1 Blocker.** Two definitions on one slide, and a cycle
  is a special case of a circuit — verbatim the rubric's P1 calibration case. Walk, trail
  and path each got their own slide (029/030/031); these two must too. Split into
  "Circuit" and "Cycle". (This overrides the original spec line that said to keep them
  together — the verification pass is right and the spec was wrong.)
- **Slide 023 "Eulerian path" — N1.** Opens with "A **trail** that uses every edge exactly
  once", but *trail* is not defined until slide 030. *Connected* got an inline gloss on
  this same slide; give *trail* the same treatment — "a route that never reuses an edge —
  named precisely in Part Four".
- **Slide 040 — N1.** Cut the sentence asserting that visiting "breadth-first" yields
  "shortest-path distances" — neither term is defined anywhere in the deck.
- **Slide 035 — N1.** "try it on the graph above" — there is no graph above; slide 034 is
  matrix-only today. Once 034 carries a graph panel (see figures), reword to "on the graph
  from the previous slide".
- **Slide 051 "Store only the nonzeros" — P1/P2.** Three claims land together: the three
  CSR arrays, the degree identity, and the $O(n^2)\rightarrow O(m+n)$ result. Move the
  degree identity and the memory result onto their own following slide.
- **Slide 058 — N4.** The note says "draw a graph like this yourself, **before you look at
  the figure**", and the answer figure — two disconnected triangles — is on that same
  slide. Remove the figure from 058; it belongs on 059 only.
- **Slide 056 — N4.** The other three edge cases give a timed beat ("30 seconds",
  "60 seconds"); this one has only a rhetorical aside. Add a timed beat.
- **Slide 057 "Yes — vacuously" — P3.** Three lines of prose and one unlabelled dot. Add
  the follow-on question that makes it substantive: is a graph *containing* an isolated
  node connected?
- **Slide 062 "Module 01 review" — L4.** Seven bullets; the rubric's ceiling is four.
  Split across two slides or compress to four beats.
- **Slide 047 "Edge list" — F1.** The prose says finding node 1's neighbours means scanning
  every pair, but the figure highlights only the single edge 1–3 in accent-2, while slide
  048 uses accent-2 for *all three* of node 1's edges. Make the two slides consistent:
  highlight all three of node 1's rows here too, and say what the highlight means.

## Figure fixes (`figures/make_figures.py`)

### Global

- **Remove every `ax.set_title(...)` / baked-in top-of-figure caption.** Nine to fifteen
  slides currently print the identical sentence twice, once inside the PNG and once as the
  HTML figcaption, in two different typefaces ("edge list", "adjacency list", "adjacency
  matrix", "both ends attach here", "every degree even", "edges now have direction",
  "a few shortcuts change everything", "the city", …). Keep the figcaption as the single
  caption channel. **Keep in-drawing annotations** that label parts of the picture
  (`start`, `end`, `left over`, `component 1`, `destroyed`) — those are not captions.
  Where a two-panel figure needs per-panel titles to be readable at all, keep those.
- **Normalise in-figure type by output width.** `LABEL_FS`/`TITLE_FS`/`ANNOT_FS` are fixed
  at 17–18pt while output widths range 522px to 1837px, so rendered text varies about 4x:
  the CSR position labels come out ~10px (smaller than the page number) while
  `selfloop`'s annotation comes out ~42px, larger than the body text. Either standardise
  `figsize` across figures or scale the font sizes by figure width.
- **Trim dead margin.** Several figures carry 15–20% white padding, which is what pushes
  their captions off the slide. Tighten limits so the aspect ratio of every
  column figure lands at or below ~0.95.

### Specific

- **`abstraction-1-map.png` — F4 Major.** Captioned "the city" but it shows four equal
  cream ellipses joined by black lines: an already-finished node-link diagram. The
  abstraction build therefore starts one step *after* the abstraction. Make frame 1 the
  same irregular landmass sketch used on slides 005/007 (identical geometry), so
  007→008 is continuous and 008→009 becomes the real blobs-to-dots step.
- **`adjacency-matrix.png` — F4 Blocker.** A slide titled "Writing a graph as a matrix"
  whose figcaption promises "a graph and its matrix" shows only the matrix. Add the 5-node
  graph as a left panel, with one edge and its two symmetric cells highlighted accent-3 so
  the correspondence is visible. This also repairs slide 035's "try it on the graph".
- **`parity-even.png` — F4 Major.** The figure prints two "in–out" labels but only one
  bracket is visible; the second is drawn inside the centre disc and swallowed by it
  (`rad=-0.6`). Widen it clear of the node and raise its z-order. Also thicken both
  brackets to at least edge weight — at lw 1.8 in #6b6b6b they are the faintest marks in a
  figure whose whole point they carry.
- **`parity-odd.png` — F1 Major.** The leftover *edge* is accent-2, but so is the entire
  node at its far end, and the "left over" label sits beside that node. Students read the
  node as the leftover thing. Colour the edge only, leave the node black, anchor the label
  at the edge midpoint.
- **`euler-path-example.png` / `euler-circuit-example.png` — F3 Major.** The `start`,
  `end` and `start = end` labels are accent-2 text sitting directly on accent-2 edges —
  same-colour text struck through by same-colour line. Offset them clear of the edges or
  set them in annotation gray.
- **`konigsberg-bombed.png` — F1/F3 Major.** The two destroyed bridges are dashed in ~#e5e5e5
  and are barely separable from white; nothing says what the ghosts mean. Dash them in
  annotation gray at live-edge weight and label one `destroyed`.
- **`campus-*.png` — F4/F3 Minor.** `campus-base` places the nodes ~46px higher and ~4%
  larger than the walk/trail/path frames, so the graph jumps when the build returns to it —
  emit all four on one shared axis extent. `Dorm` and `Cafe` fill their discs edge to edge;
  give the labels interior margin. `campus-trail` has no `start` marker while the Euler
  examples do — add one.
- **`sweep-3.png` — F5 Minor.** Uses accent-2 for component 1, but accent-2 has meant "odd
  degree" and then "the traced route" earlier in the deck. Use neutral fills and let the
  `component 1/2/3` labels do the work.
- **`giant-scale.png` — F4/F1 Major.** The panel labelled `N = 10,000,000` is an empty box
  containing a single ~4px dot — the other ~9,999,000 nodes are not drawn, so the panel
  reads "one node" rather than "1,000 nodes lost in ten million". Fill it with a faint node
  field at the left panel's dot size. Also state what the pale gray dots encode in the left
  panel.
- **`store-edgelist.png`** — see the slide-047 finding above; highlight all three of node
  1's edges/rows, matching `store-adjlist.png`.
- **`format-regimes.png` — F1/F5 Minor.** Only two of the four quadrants are shaded and
  labelled; the other two (large+dense, small+sparse) are blank and unexplained. The two
  shades (#e8e5e0 / #f7f2ef) are off-token. Label all regions and use theme tokens.
- **`directed-indegree.png` — NEW, F4 Major.** Slide 061's single point is that degree
  splits into in-degree and out-degree, but it currently reuses `directed-arrows.png`
  unchanged — no in/out counts anywhere. Create a variant printing `in 1 / out 1` beside
  each node.
- **`recap.png` — F2 Major.** The "one component" leader line crosses the N–B edge and ends
  at the midpoint of the A–B edge, so it appears to point at a single edge; the
  "A: 4 × 4 matrix" leader ends on node B. Route the leaders around the outside without
  crossing any edge, and make "one component" a bracket enclosing all four nodes.
- **`smallworld-teaser.png` — F2/F4 Major.** Two problems. (a) All four shortcuts are
  `i ↔ i+10` on a 20-node ring — i.e. exact diameters — so they all pass through the centre
  and meet in an asterisk, implying a hub that does not exist; use varied chord lengths.
  (b) The ring is `j = (i+1) % n`, so k=2 and there are **no triangles at all** — the
  figure is a counterexample to the "high clustering" the slide claims. Make it a k=4 ring
  lattice (each node joined to its two nearest neighbours on each side).
- **Page number collision — Minor.** On slides 034, 036 and 063 the page number prints
  inside the figure ("34" and "36" ghost behind matrix cells; "63" lands on the word
  "everything"). The CSS height cap will mostly resolve this; verify after re-rendering.

## Verify before reporting done

Re-run `python3 figures/make_figures.py`, then re-render:

    marp m01-euler-tour.md --theme network-science.css --allow-local-files --images png -o review/slide.png

Then confirm: no figure's rendered height plus its caption exceeds the frame, and every
figcaption in the deck is visible on its slide.

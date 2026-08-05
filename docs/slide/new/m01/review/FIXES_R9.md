# Round-9 fixes

Round 8 produced 11 Blockers, but three independent verifiers converged on **one cause**
for most of them, and measured it the same way.

## The one cause

Round 8's `Circle` refactor did work — **in figure space.** Every source PNG carries a
149–150px node disc, and the build asserts it. But the deck then scales each image to a
fixed `w:520` or `w:760`, capped by the CSS `max-height: 380px`, and natural widths run
1544px to 5010px — so the real downscale runs **0.14× to 0.34×**, different for every
figure. The assertion is checked before that downscale, so the deck-wide constant never
reaches the slide.

Measured on-slide node diameters:

    v8-A (slides 001–024):   21.0 – 178.5 px   (8.5x)
    v8-B (slides 025–049):   23   –  46   px   (2.0x)
    v8-C (slides 050–073):   18.5 – 296   px   (16.0x)

R7 measured 6.9×; it is now 16×. The spread got worse, not better.

**The in-figure text problem the lecturer reported is a symptom of the same thing.** Where
text sits inside a disc, it cannot exceed the disc, so it inherits the node-size bug. Where
it is a free-standing annotation, it is set in figure space and shrunk by the same unknown
factor. Measured smallest on-slide text, against a 16px page number and 25px body:

    3px  A^k counts walks (node labels)        5px  recap annotations, degrees, node labels
    4px  adjacency matrix (node labels)        6px  Konigsberg degrees, CSR bar labels
    5px  many node labels across the deck      7px  edge-list / adjacency-list labels

**Every figure with text in slides 025–049 is smaller than the page number.** Eleven of
thirteen in 001–024. On slide 026 the body says "work from the degrees" beside 6px numerals.

### The fix

Normalize the **on-slide** diameter, not the PNG diameter. Both verifiers derived the same
formula independently:

    scale      = min(520 / src_w, 380 / src_h)      # the deck's real downscale
    src_disc   = target_onslide_diameter / scale

Pick `target_onslide_diameter` deliberately — the Königsberg graphs currently land at
23–24px, which is itself too small to read; **34–40px reads well.** Set the source disc size
from that, per figure.

Then **assert on the rendered PNG, not the source.** Everything so far has been asserted in
the wrong space, which is why three rounds of "node size is now uniform" reports were
followed by verifiers measuring a 16× spread.

Two figures bypass the machinery entirely and need it applied: `selfloop.png`
(900px disc in a 1080px image — 6× everything else; drop `SELFLOOP_OUT_DPI` and give
`_build_selfloop_fig` the same treatment) and `edge-single-node.png` (296px on slide, 41% of
slide height, under a caption reading "the smallest possible graph"). The false assumption is
written at `figures/make_figures.py:1271-1274`.

Once the node size is right, re-measure the smallest in-figure text and **require it to be at
least the page number's size**. Free-standing annotations that are still short (the pairing
arcs' "in–out", "left over", "even", the degree numerals, "start"/"end") need their own size
bump — they will not be fixed by the node work.

## Blockers that are not the sizing bug

1. **Slide 047 "The directed Euler condition" — the theorem is still false, second round
   running.** Round 8 fixed the degree rule and moved the error into the connectivity clause.
   The slide now gates **both** cases behind "strongly connected". That is correct for the
   closed tour only. An Eulerian *trail* needs only that the edges form one piece with
   direction ignored — and the deck falsifies its own rule two slides later: slide 049 draws
   A→B→C, which I verified has out−in = +1, 0, −1 (exactly 047's stated trail pattern), has
   an Eulerian trail, and is **not** strongly connected. Applying 047's rule to 049's own
   figure yields "no Eulerian trail", which is false.
   **Fix:** both bullets take "connected once you ignore direction" — the phrase 049 already
   uses. (For the closed tour this is equivalent: balanced plus weakly connected implies
   strongly connected.) Do not attach strong connectivity to the trail case.

2. **Slide 012 "Two bridges, one pair" — the adjacency-matrix leak, open since round 7.**
   The right half of the figure is a 2×2 matrix with N/A headers, blue-filled cells and red
   outlines, on a slide that never names a matrix, a row, a column or either colour — and the
   matrix is not defined until slide 053. `multigraph.png` is shared with slide 054, which
   does explain it. **Fix:** emit a matrix-free variant for 012; keep the matrix version
   exclusive to 054.

3. **Slide 008 "Euler's move — the city" — the build's first step is a null step.**
   `abstraction-1-map.png` is byte-identical to `konigsberg-sketch.png`, so slides 005, 007
   and 008 show the same picture three slides running, while 008's caption reads "N, A, B, S
   — the labels are all that survive the cut" over a render still showing the river band, the
   coastlines and all seven bridges at full strength. **Fix:** make 008 a real first cut —
   river and coastlines dropped to a light tint, labels promoted — or change the caption to
   describe what is on screen and let 009 do the cutting.

4. **Slide 027 "A tragic epilogue" — the "destroyed" label nearly touches a surviving
   bridge.** The upper label's nearest ink is **2.8px** away, on the solid A–N curve, which is
   one of the five bridges that survived; its own dashed arc is 44.7px away. The lower label
   is 35.6px from its dash and 74px from any solid stroke — so the two labels on one figure
   use opposite conventions, and the wrong one is the one that nearly touches. Round 7
   measured 20px; it got worse. **Fix:** place the upper label on the concave side of its
   dashed arc, matching the lower one, with equal clearance from every solid stroke.

5. **Slide 029 "Walk" — the figure shows a multigraph, not a repeated edge.** Sampling 15
   points along the straight Gym→Café chord finds zero non-white pixels: the base edge is
   absent, and the traversal is two red arcs bowing apart — the exact glyph slides 026/027 use
   for Königsberg's two parallel bridges. Read with the encoding the deck itself taught, the
   campus graph has two Café–Gym edges, so the drawn route repeats no edge and is a *trail* —
   the opposite of this slide's point. **Fix:** restore the straight gray Café–Gym edge and
   bow the two red arcs symmetrically about it so the base edge stays visible underneath.

6. **Slide 062 "The payoff: memory" — the bar chart still contradicts its labels, and bar
   charts are now out.** Measured: n=5 draws dense 64px / CSR 76px (ratio 1.19, honest);
   n=100,000 draws dense 85px / CSR 11px — a drawn ratio of **7.7:1 under a label reading
   7,700×**, a thousandfold discrepancy, with no axis, no break mark and no scale note, and
   the two pairs stacked in one figure at 1px ≈ 0.39 units and 1px ≈ 118 million units
   respectively.
   **Fix — drop the bars entirely.** The course's figure guide now rules bar charts out:
   they encode a number as a length and then need a scale to decode it, which is exactly how
   this went wrong. Replace with the numbers themselves, annotated — dense 10,000,000,000
   against CSR 1,300,001, and the ratio stated once. Print "n = 100,000, average degree 6"
   beside it so the claim is checkable. Also cut the figure's top half, which is slides
   060/061's figure shown a third time, and its baked-in sentence, which duplicates the body.

7. **Slide 071 "Back to Königsberg" — the closing argument's evidence is 6px.** The slide's
   only job is to show that all four landmasses are odd; the degree numerals measure 5×6px
   and the node labels 5px. **Fix:** degree numerals at or above the node diameter's scale,
   set close to their nodes.

8. **Slide 072 "Module 01 review" — two of the recap figure's three annotations point at
   nothing drawn.** The figure contains a graph and a dashed circle. "adjacency matrix, 4 × 4"
   labels a matrix that is not there; "degree → parity" has no leader, no parity colouring
   (all four nodes are the same red) and no referent. Only "one component" has one. This is
   the deck's summary slide. **Fix:** delete the two unreferenced annotations, or actually
   draw a small 4×4 matrix and colour the odd nodes.

## Majors

9. **"CSR" is never defined.** It first appears on slide 059 ("exactly what CSR refuses to
   store"), the slide that actually teaches the mechanism (060) says data/indices/indptr
   without ever naming it, and 062, 063 and 072 then use it as known. `grep "Compressed"`
   returns nothing. **Fix:** name it once, in 060's body.

10. **Slides 052/053/054/057 — the storage build's anchor moves at every step.** The same
    5-node graph is redrawn at node spans 127/105/105/80px, diameters 30/24.5/24/18.5px, with
    node 0 at four different positions. The point of these four slides is to compare
    representations of *one* graph. **Fix:** fix the graph panel's coordinates and scale
    across all four; vary only the right panel and the highlight.

11. **Slides 065↔066 and 067↔068 — question and answer show the same object at different
    sizes** (self-loop 178.5 → 137.5px, single node 296 → 174px). Resolves with the sizing fix.

12. **Slide 047 — the figure cannot be a counterexample to the rule as stated.** The body says
    "On a graph that's strongly connected … Below, both nodes total 2", but the figure is
    A⇉B, which is not strongly connected, so the hypothesis excludes it before any degree is
    counted. **Fix:** follows from Blocker 1 — once the trail case takes weak connectivity,
    reword so the figure illustrates balance only.

13. **Slide 047 — the key result of Part Six arrives cold**, and slides 048/049 define
    "strongly connected" *after* 047 has already used and self-glossed it. **Fix:** move 048
    and 049 ahead of 047; that also supplies the vocabulary Blocker 1's rewrite needs. Add a
    one-line prompt before it: "Königsberg's rule was about odd degrees. What replaces 'odd'
    once edges point?"

14. **Part Six "Direction" has no student activity** — the only interactive beat is a
    30-second prompt, while Parts Four and Five each have a trace-it-yourself slide. **Fix:**
    add one — e.g. add an arc to the A→B→C→A triangle and ask whether a closed tour survives.

15. **Slide 054 — P1.** Defines the adjacency matrix *and* teaches "degree, three ways" —
    a separate mechanism spanning three representations, on the slide that first defines the
    matrix. **Fix:** give the three-ways synthesis its own slide.

16. **Slide 022 — the four nodes change from black to red between 021 and 022 with no stated
    meaning**, and red means "odd node" on 020 and "start/end" on 023. **Fix:** one clause in
    the caption — "red = odd degree".

## Minors

- 021, 022 figcaptions call a node-link diagram a "map"; "map" has meant the engraving since 004.
- 012's "the other three you counted on the previous slide" points at 011, where nothing was counted.
- 013's node is labelled "X"; every other node in that stretch is N/A/B/S.
- 020's label pairs are ordered inconsistently ("start"/"odd" vs "odd"/"end").
- 023 lands two paragraphs and a four-line note at once with no fragments.
- 030's ring clears "visited twice" by 11px — fixed but tight.
- 039 is the only figure slide with no figcaption, and its lone component sits 38px from the
  page number at the same height, so "39" reads as a fourth component.
- 052's body says node 1's edges are "scattered through the list" but the highlighted rows
  0, 2, 3 are nearly contiguous.
- 059 has no figure; 063's caption claims "log scale" on a schematic with no ticks.
- 070 prints no degrees, though the argument is that every node has degree 2.
- 071's caption says "both hypotheses" where the body says "conditions".
- 073 never states that red = shortcut.
- Captions across the deck float 82–145px below their figures, reading as page footers.

## Verify before reporting done

    python3 figures/make_figures.py
    marp m01-euler-tour.md --theme network-science.css --allow-local-files --images png -o review/slide.png

Then **measure on the rendered slides, not the source PNGs** — node diameter and smallest
in-figure text, for every figure-bearing slide. Report both distributions. That is the check
three rounds of reports have gotten wrong by measuring the wrong artifact.

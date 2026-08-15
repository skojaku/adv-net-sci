# Round-6 fixes — Blockers only

Blockers by round: 29 → 7 → 4 → 7 → 9. The count is not falling, but the *kind* has
changed completely: round 1's were structural (tables, code blocks, three-column text
layouts, a missing fourth act, no progressive disclosure anywhere, unexplained visual
encodings). What is left is figure geometry and one arithmetic error. The verifiers have
also become progressively more forensic — round 5 measured pixel positions and colour
samples — so counts are not directly comparable across rounds.

**This round fixes the nine Blockers and the one missing assertion behind several of them.
Majors and Minors are deliberately out of scope.**

## The missing assertion (root cause of three Blockers)

Round 5's label guard checks **text** against obstacles. Nothing checks that a **non-edge
stroke** is distinguishable from an edge. Every pairing arc, leader line and tick mark in
the deck is currently drawn in the same token as the edges — `#6b6b6b` at edge weight — so
students read them as edges.

Add a `draw_annotation_stroke()` used for **every** stroke that is not a graph edge, which:

- draws at ≤40% of `EDGE_W` and/or dashed, never at edge weight;
- **asserts it does not terminate on or inside a node disc** (a leader may point *at* a
  node, but must stop at least a few px outside the rim, and an arc tying two edges must
  terminate on those edges, not on a neighbouring disc);
- asserts it does not cross a live edge (leaders especially).

Slide 017 already gets the weight right — 4–5px arc against 13–14px edges. That is the
target token. Slide 020 uses 9–12px arcs against the same edges, which is why it fails.

## Blockers

1. **`selfloop.png` / `selfloop-answer.png` (slides 013, 062, 063) — fourth round unrepaired.**
   Measured on the render: the gray legs stop 5–27px outside the disc rim (both verifiers
   agree, one measuring a 26–27px gap on slide 013, the other 5–11px on 062). What reaches
   the rim is not the loop but the two black marks — 64–70px long, ~0.72–0.8× the node
   radius, round-capped, in `INK` where every edge in the deck is `MUTED`, crossing over the
   gray legs. They read as two extra edges on the node, on the slide asking "does it count
   once or twice?" — so the node visibly carries three attachments. Three slides caption
   this figure "both ends attach here".
   **Fix — take the simple option this time: delete the tick marks entirely** and run both
   gray legs to the disc boundary so the loop visibly closes on the node. Assert the legs'
   endpoints lie on the rim within a pixel or two.

2. **`selfloop-answer.png` (slide 063) — the ① ② badges label white space.** Badge ① centres
   100px from the left attachment point and clears its own mark by 17px. Once the ticks are
   gone (Blocker 1) the two attachment points are unambiguous — **place the badges on the
   rim at those two points.**

3. **`parity-bound.png` (slide 020) — the figure now assigns the wrong parity to all six
   nodes.** Round 5 fixed the start/end label clearances (confirmed) but left the four
   "even" pairing arcs at `#6b6b6b`, 9–12px — the same colour and weight as the edges — each
   running **rim to rim between two discs**, forming a lens with the straight edge beside it:
   exactly the shape slides 010–012 taught as Königsberg's doubled bridges. A rim scan at
   r+8 counts 2 strokes at "start", 2 at "end" (both labelled **odd**) and 3, 4, 4, 3 at the
   interiors (all labelled **even**). Every node reads as the opposite parity to its own
   label, on the slide whose only point is parity. This is worse than the defect it replaced.
   **Fix:** adopt slide 017's arc token (≤40% of edge weight), float both tips clear of every
   disc, and terminate each arc **on the two edges being paired**, not on neighbouring rims.
   State the arc's meaning in the caption.

4. **Slide 023 "Eulerian path" — P1, three definitions deep.** One slide defines **trail**,
   then defines **Eulerian path** as a special case of it, then asserts a two-clause
   existence theorem whose first clause introduces **connected**. That is verbatim the
   rubric's P1 example. It also front-runs the deck's own structure: Part Four
   ("Vocabulary — walk, trail, path…") does not begin until slide 027, and connectivity is
   Part Five.
   **Fix:** leave 023 with the Eulerian-path definition and the parity condition alone. Move
   the trail definition into Part Four. Put the connectivity requirement on its own slide,
   posed as a question — show a two-component graph, ask why no trail can cover it — placed
   after connectivity exists, or immediately before Part Five as a bridge into it.

5. **Slide 036 "For a multigraph, count the edges" — raw LaTeX renders as literal text.**
   The figcaption prints `N–A: $A_{NA} = 2$, not 1` with the dollar signs and braces visible
   in the handwriting face. KaTeX does not process `<figcaption>`; this is the deck's only
   such caption (`m01-euler-tour.md:758`).
   **Fix:** plain text — `two N–A bridges → the entry is 2, not 1`. Then grep the whole deck
   for `$` inside any `<figcaption>` and fix any others.

6. **Slide 042 "Your turn: run the sweep" — the figcaption is entirely off-slide.** Figure
   ink stops at y=621 and the only ink below is the page number; the caption `no components
   marked yet — trace your own` never renders. `components-bare.png` (1672×516) renders
   ~1080×339 with its top at y≈394, so the image box ends at y≈733 on a 720px slide. Slides
   041 and 043 use identical markup and do render their captions — the difference is the
   three bullets plus two paragraphs above the figure. This is round 5's Blocker 4,
   reintroduced by the split that fixed round 5's Blocker 6.
   **Fix:** `<div class="fig tight">`, or move the caption text into the body line.

7. **Slide 045 "The giant component" — the printed key contradicts the drawing by 1,000×.**
   The right panel's key reads `blue: still 1,000 (1 dot = 1 node)` but the panel contains
   exactly one 4×5px blue dot, so a student applying the printed key counts the giant
   component as **one node**. The left panel legitimately draws ~1,000 blue dots.
   **Fix:** drop `(1 dot = 1 node)` from the right panel — e.g. `blue: the same 1,000 nodes —
   0.01% of the area, a single dot at this scale`.

8. **Slide 059 "The payoff: memory" — the figure states a false claim, and it is my error.**
   The spec I wrote for round 5 asked for "the concrete 12-vs-25 count" as evidence for
   $O(n^2)\rightarrow O(m+n)$. That count is wrong: it counts only the `data` array. For this
   graph, verified by direct computation:

       dense 5×5                                  = 25 numbers
       CSR data 12 + indices 12 + indptr 6         = 30 numbers

   **CSR is larger than dense at this size.** The figure and the slide body both assert the
   opposite, and the figure also contradicts slide 057, whose own drawing shows all three
   arrays. "Five pointers" in the body is also wrong — indptr has $n+1 = 6$ entries.

   **Fix — do not paper over this; it is the honest version that teaches the concept better.**
   Count all three arrays (30 vs 25), say plainly that CSR *loses* at this toy size, and show
   where it wins. Verified numbers for the crossover:

       n = 5,       avg degree 2.4:  dense           25  ·  CSR         30   → dense wins
       n = 1,000,   avg degree 6:    dense    1,000,000  ·  CSR     13,001   → CSR wins 77×
       n = 100,000, avg degree 6:    dense 10,000,000,000 · CSR  1,300,001   → CSR wins 7,692×

   That contrast is a better slide than the false one: the toy example is the *counter*example
   that motivates why the asymptotic statement is about growth, not about small cases.

9. **Slide 062 "Does a self-loop add 1 to a node's degree, or 2?"** — same figure as Blocker 1;
   fixed by it.

## Verify before reporting done

    python3 figures/make_figures.py
    marp m01-euler-tour.md --theme network-science.css --allow-local-files --images png -o review/slide.png

For every figure touched, open the regenerated PNG with the Read tool and confirm the defect
is gone. Five consecutive rounds have each included at least one repair reported as landed
that the rendered image contradicted; three of them were on this same self-loop figure.

# Round-7 fixes

Blockers by round: 29 → 7 → 4 → 7 → 9 → **3**. Falling again, and the three verifiers
converged independently on one cause.

## The one thing to fix first

Round 6 wrote `draw_annotation_stroke()` — draws at ≤40% of `EDGE_W`, asserts the stroke
does not terminate on or inside a node disc, asserts it does not cross a live edge — and
then **called it from exactly one figure**, `parity-bound.png`. Every other non-edge stroke
in the deck is still hand-drawn and still violates one clause or the other:

| slide | stroke | violation |
|---|---|---|
| 015 | "k = 4" leader | ends 13.7px **inside** the disc; 4px against 7px edges (57%) |
| 027 | upper "destroyed" leader | **crosses the surviving solid A–N edge** before reaching its dash |
| 029 | "same edge, twice" leader | **crosses two live red strokes**, tip lands in white space on neither |
| 064 | ① ② badge rings | opaque discs **overlapping the node**, 6–8px = full edge weight |
| 066 | component ring | 10–11px — **heavier than any edge in the deck** (6–9px) |

**Route every non-edge stroke in `make_figures.py` through the helper and let the assertions
fail the build.** That is the fix for two of the three Blockers and four Majors at once. Do
this before touching anything else; several items below may resolve themselves.

Badges need the same treatment — the helper currently governs strokes, not filled marks. Add
the disc-overlap assertion to any filled annotation (badge, ring, halo) too.

## Blockers

1. **Slide 029 "Walk" — the figure's only annotation points at the wrong edge.** The leader
   for "same edge, twice" runs leftward from x≈1031 to a tip at (945, 345), crossing the red
   Gym→Café arc at ≈(957, 342) and the red Café→Lib vertical at ≈(1024, 347) on the way, and
   its tip lands in the white gap between the two red arcs — on neither stroke. Reading
   right-to-left from the label, the first stroke the eye meets is Café–Lib, an edge crossed
   *once*, on the slide whose single point is that Café–Gym is crossed *twice*. The weight is
   right (~2px against 12px); the routing is not. **Fix:** end the leader on the outer red
   arc, approaching from above-left so it touches nothing else — or drop the leader and set
   the text directly beside the arc pair.

2. **Slide 064 "Two" — the badges destroy the node they annotate.** ① and ② are opaque white
   discs (radii 33 and 63, centres ~74px apart) laid over the node. A topmost-black-row scan
   finds the disc's true arc only across x=914–946; at x=874–906 and x=954–994 the top edge
   drops 15–30px — two white bites out of the node's shoulders, so it reads as a three-lobed
   blob. The loop legs now terminate on the badge tops rather than the rim, and the badges
   hide the two attachment points they exist to mark, on the answer slide that proves the
   loop attaches twice. Their rings are also 6–8px = edge weight, so they read as extra
   loops. Note the question slide 063 is genuinely correct for the first time in five rounds
   — **the answer slide regressed via the badge fix.** **Fix:** put the badges outside the
   node, unfilled, offset radially outward from each attachment point with a hairline leader
   stopping short of the rim; or drop the discs and set bare ① ② numerals in annotation gray.
   Keep 063's centre and radius (r=88.5 there vs r=63 here) so question and answer are one
   build.

3. **Slide 060 "The payoff: memory" — there is a table inside the PNG, and it is 7px.** The
   bottom third of `csr-memory.png` is a literal three-row, five-column monospace table
   (`n = 5 … dense 25 · CSR 30 (dense wins here)`). L2 bans tables outright, and putting one
   inside an image does not exempt it. Worse, the PNG is 4544px wide placed at `w:520` — an
   8.7× downscale against 3.15× for `csr-build.png` at the same width — so the table and the
   line above it render at ~7px, unreadable except at 3× magnification. The crossover **is**
   this slide's point, so the figure fails to carry it. The arithmetic itself is now correct
   and internally consistent across slides 057–060 (verified independently). **Fix:** cut the
   table out of the PNG. Replace with a two-bar comparison — at n=5, a short dense bar beside
   a slightly longer CSR bar (25 vs 30, CSR loses); then the same pair at n=100,000 with the
   dense bar running off the frame. Regenerate at ~1600px so its type matches 058/059.

## Majors — pedagogy and structure

4. **Slide 042 "Components" gives away slide 043's exercise.** 042 prints "component 1 /
   component 2 / component 3" on the figure and captions it "sizes 8, 3, and 1"; 043 then
   shows the same graph and asks "How many sweeps until every node is marked?". Round 6
   removed 043's caption, which moved the leak upstream rather than closing it. **Fix:** teach
   042 on a *different* graph, or without numbered component labels, keeping the
   ladder + triangle + lone-node graph fresh for the exercise.

5. **Slide 039's question is never answered, and slide 068 spends its figure.** The new bridge
   slide asks students to trace a trail covering both triangles and gives a 30-second beat,
   but nothing in the deck resolves it — the Part Five divider and slide 041's definition only
   imply the answer. Meanwhile slide 068 reuses `edge-disconnected.png` with the *identical*
   figcaption to answer slide 067's 60-second prompt, so the class works through the same
   picture twice, 29 slides apart, and 067's beat is pre-spoiled. **Fix:** resolve 039
   explicitly on 041, and redraw 068 on a different disconnected all-even graph — two squares,
   or a 4-cycle plus a triangle.

6. **"Eulerian path" contradicts "path".** Slide 023 defines an Eulerian path as a route using
   every edge exactly once — nodes may repeat — and its own example revisits its start node.
   Slide 029 then defines a **path** as "a walk that never uses the same node twice". By that
   definition slide 023's route is not a path; it is a trail. Nothing in the deck reconciles
   them. **Fix:** one line on slide 028 "Trail": an Eulerian path is really an Eulerian
   *trail* — the name is historical.

7. **Representation material sits inside the Vocabulary part, and the adjacency matrix is
   introduced twice.** Slides 035–038 (matrix definition, multigraph entry, $A^k$) live under
   Part Four, whose banner promises "name the journeys precisely", while Part Six is titled
   "Representation" and contains a slide "Adjacency matrix" opening "An $n\times n$ grid of 0s
   and 1s" — a second first-introduction of what 035 already defined on the same 5-node graph.
   **Fix:** move 035–038 into Part Six ahead of its adjacency-matrix slide and merge the
   duplicate, or retitle Part Four.

8. **Part Seven has no payoff.** Three clean Q/A pairs (063→064, 065→066, 067→068), each with
   a timed beat — S4 and S5 both satisfied — but the act never returns to Königsberg, and its
   strongest pair (067/068, which is *why* the Part Five sweep exists) is delivered and then
   dropped straight into the recap. The three cases also get equal real estate, so the
   throwaway single-node case looks as important as the load-bearing one. **Fix:** add one
   closing slide that re-runs the Königsberg verdict through both hypotheses — connected ✓,
   four odd nodes ✗ — so the edge cases resolve back onto the opening story.

9. **Slide 049 — P1.** Slide 048 asks only "degree splits — into what?", but 049 answers that
   **and** asserts "Euler's condition becomes: in-degree equals out-degree, at every node" — a
   second theorem, with no figure of its own and no counterexample. **Fix:** end 049 at the
   in/out definition; give the directed Euler condition its own slide with a graph that
   satisfies parity but has in ≠ out somewhere.

10. **Slide 058 — P1/N4.** "**512 exabytes**", the entire payoff of slide 057's guess-first
    beat, is the first two words of a slide whose title, figure and three bullets are about
    CSR. A full question beat gets no answer slide, and this slide carries two payloads.
    **Fix:** give 512 exabytes its own slide (one number, with the $(8\times10^9)^2$
    arithmetic shown), then start CSR clean.

11. **Slide 025 — N1.** "Closed walk" is used four slides before "walk" is defined (029) and
    eight before "circuit" (033). **Fix:** say "a route that ends where it started" on 025 and
    let 033 name it.

12. **Slide 044 — F1.** Numbers beside nodes mean *visit order* here and *degree* everywhere
    else in the deck (019–022, 026, 027). Node "2" has degree 3; node "1" has degree 2. **Fix:**
    label the figure "visit order", or put the numbers inside the discs.

## Majors — figures

13. **Slides 054 / 055 / 056 — the build's anchor rescales at every step.** The same 5-node
    graph is redrawn at node radius 26.6 → 22.9 → 14.5px with row centres shifting each time,
    and it shrinks again on 058–060. A build adds elements to a *fixed* figure. **Fix:** render
    the graph panel once at one size and position; vary only the highlight and the right panel.

14. **Node radius spans 9px to 148px across the deck with nothing encoded** — 070: 9px, 068:
    11.5px, 049: 30.5px, 063: 88.5px, 065/066: 148px. The lone node on 065 is 41% of slide
    height under a caption reading "the smallest possible graph". **Fix:** pick one on-slide
    node diameter and derive every figure's `figsize` from it, rather than sizing each figure
    to fill its own canvas.

15. **Slide 069's recap figure labels two things it does not draw.** "degree → parity" — the
    figure has no degree numbers and no odd/even colouring; "A: 4 × 4 matrix" — there is no
    matrix, and "A" is also a node label 3cm above, so the glyph means two things. The
    "degree → parity" leader overlaps the dashed component circle for ~60px and terminates at
    (249, 385), 18px outside node A, pointing at nothing. **Fix:** print degree numbers and
    colour the odd nodes accent-2 so the first label has a referent; drop the leader; rename
    the second to "adjacency matrix, 4 × 4".

16. **Slide 020 — the four "even" labels are struck through by their own arcs.** Row profiling
    puts a 19–23px arc band on the letter rows of every one of the four. Slide 017, the deck's
    own reference, leaves 39px of white between "in-out" and its arc. On the slide whose single
    point is parity, "even" with a line through it reads as negation. **Fix:** move each label
    to the convex side of its arc with ≥15px clearance.

17. **Slide 038 — the route labels are 9–10px**, against 20px matrix digits and 23px body
    text, and the gold one is #DAB167 on white. The figcaption already states both routes at
    21px. **Fix:** delete them, or set them ≥18px in annotation gray.

18. **Slide 046 — the panel keys are the smallest text on the slide and overflow their
    panels.** Right key cap height 9px against 26px body; the key spans 277px under a 176px
    panel, running to within 10px of the content margin. **Fix:** caption-size type, broken to
    lines that fit inside the panel.

19. **Slide 008 — the figure does not carry the slide's point.** `abstraction-1-map.png` is
    byte-identical to `konigsberg-sketch.png`, so this is the same image for the third slide
    running (005, 007, 008), while the caption claims "N, A, B, S — the labels are all that
    survive the cut" and nothing on the render is cut. It is conspicuous beside the genuinely
    careful 009→010 build. **Fix:** draw a distinct figure with the river and coastlines dropped
    to a very light grey and only the four labels at full strength.

20. **Slide 056 — the caption is printed twice, verbatim**, once baked into `store-matrix.png`
    (`make_figures.py:2331`) and once as the deck figcaption. **Fix:** delete the in-figure
    call; grep the other `store-*` builders for the same pattern.

21. **Slide 036 — the figure omits the thing the slide is about.** The claim is about a matrix
    entry; the figure is two discs and two parallel edges, with no matrix anywhere. Also
    "multigraph" appears in the title and nowhere else — the concept is taught on slide 012 but
    the word is never defined. **Fix:** put the 2×2 matrix beside the pair with the `2`
    highlighted; define the word on 012.

## Minors

- 019 — "left over" clears the lower-right disc by 0.8px; the "l" ascender touches the rim.
- 021, 025 — the only wrapped captions in the deck; both drop a word onto the page number's rows.
- 030, 032, 047, 066 — caption-to-page-number clearance 3–13px, with horizontal overlap on 030
  and 066. No collision, no margin.
- 012 — the caption asserts "A touches five bridges in all" but the figure draws A with two.
- 018, 024, 036, 037, 045, 065, 066 — bottom 55–85% empty.
- 025–034, 047, 059 — captions float 85–135px below their figures, reading as page footers.
- 029–032 — node labels reach the disc rim with zero padding.
- 046 — left-panel pale dots render #d9–#f0, barely visible; "blue" is defined only under the
  right panel; "--" used where the deck uses an em dash.
- 038 — the (1,4) highlight is outlined black while 035 outlines its highlighted cells accent-2
  for the same job.
- 055 — adjacency-list rows read `0 → 1, 2` on an undirected graph, three slides after arrows
  were established as direction.
- 061 — "real networks live here" in the figure and "real networks cluster large-and-sparse —
  bottom right" in the caption say the same thing twice; the in-figure label overhangs the grid
  by ~140px.
- 063 — the self-loop stroke is 24px against a 6–9px edge weight everywhere else.
- 048 — the prompt sits in the gray `note` panel while 053 and 057 use the cream `formula` panel.
- 040 — straight apostrophe in "Euler's"; the deck uses curly elsewhere.
- 070 — the deck ends with no closing pointer to the Module 01 notebook; it is named once, in
  passing, on 061.
- 023 — the deck proves only necessity (slide 020), yet states "exists **exactly when**" without
  noting the converse is a separate, unproven half.
- 041, 042, 044 — land text, figure, caption and note simultaneously with no `*` fragments.

## Verify before reporting done

    python3 figures/make_figures.py
    marp m01-euler-tour.md --theme network-science.css --allow-local-files --images png -o review/slide.png

For every figure touched, open the regenerated PNG with the Read tool and confirm the defect
is gone. Six consecutive rounds have each included at least one repair reported as landed that
the rendered image contradicted — round 6's was the self-loop badge, which regressed the answer
slide while fixing the question slide.

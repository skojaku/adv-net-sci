# Round-5 fixes — final round

Blockers by round: 29 → 7 → 4 → 7. The count stopped falling because two round-4 repairs
**regressed**, and because one defect class keeps reappearing on newly-drawn figures.

Read this section before touching anything.

## The recurring failure

**A text label drawn on top of a filled disc, or on top of a stroke of its own colour, has
now been reported five times on five different figures** — slide 019 (Blocker, round 3),
slide 020 (Major, round 4), slide 026, slide 029, slide 041. Each time it was fixed on the
named figure and immediately reappeared on the next figure someone drew.

Stop fixing it per-figure. Add a generator-level guard:

- A helper that places a label given an anchor point and a list of "obstacles" (node centres
  with radii, and the polylines of nearby edges), which pushes the label out until it clears
  every obstacle by a stated margin, and **raises if it cannot**.
- Never draw accent-2 text on an accent-2 fill, or `MUTED` text on a `MUTED` stroke. Assert
  it in the helper.

Apply it to every label in the file, not only the ones named below.

## Blockers

1. **`konigsberg-bombed.png` (slide 027) — the destroyed bridges vanished entirely.** Round
   4 replaced the dashed rendering with a manual dash-placement routine; at source
   resolution the figure now contains **five solid edges and no dashed strokes anywhere**,
   and the single "destroyed" leader terminates on the solid A–N curve — **a surviving
   bridge that is still counted in A's degree of 3**. The body says two bridges fell. This
   is worse than the defect round 4 set out to fix: the only mark on the figure now labels
   the wrong thing. **Fix:** draw both removed bridges as dashed curves running boundary to
   boundary at the same curvature as the live parallel edges, each with its own leader.
   Assert that the figure contains exactly two dashed paths and that neither coincides with
   a live edge.

2. **`selfloop.png` (slides 013, 058) — the loop still touches nothing.** Measured at 6×:
   the two gray legs terminate ~13–19px above the disc boundary, and the two black marks are
   ~22px strokes at 45° that cross the legs and converge point-first on the node — not
   perpendicular to the rim, not thinner than the loop. They read as arrowheads, putting
   apparent direction on an undirected self-loop 31 slides before direction is introduced.
   All three slides caption this figure "both ends attach here" / "Both endpoints attach at
   the same node". **This is the third round on this figure.** **Fix:** run both legs to the
   disc boundary so they visibly meet it; either drop the ticks entirely or make them short
   radial marks at half the loop's stroke weight, touching the rim.

3. **`selfloop-answer.png` (slide 059) — same detached loop**, and the ① ② badges sit ~25px
   left and right of the loop at mid-height with no leader and ~40px from the ticks they
   number, so they label white space. **Fix:** repair the loop as above, then anchor ① and ②
   at the two attachment points.

4. **Slide 041 "Your turn: run the sweep" — the slide overflows its frame.** The figcaption's
   bbox is y[699,719] on a 720px slide with ink in rows 717–719, so the descenders of "your"
   and "sweep" are guillotined. No other slide in the deck puts ink below y=658. **Fix:**
   shrink the figure block further or move the caption text into the body.

5. **Slide 041 — the worked answer is still illegible.** The visit numbers measure **11px**
   against a 13px page number and 21px body copy, and the dashed enclosure border runs
   horizontally through the top third of "8", "7", "6", "5"; component 3's "1" is merged into
   the dash and reads as a tick mark. Round 4 asked for numbers clear of every edge **and of
   the dashed enclosure** — the edges were cleared, the enclosure was not. **Fix:** regenerate
   wide per Policy 2 and place the numbers inside the enclosure, offset from both discs and
   border. (The *ordering* is now correct — a verifier traced 1→2→3→4→5→6→7→8 against the
   drawn edges and every consecutive pair is adjacent. Do not disturb it; keep the assertion.)

6. **Slide 041 — the exercise still shows its own answer.** The count is out of the labels
   and the caption, but the figure prints the visit order for all 11 nodes and draws exactly
   three dashed enclosures, so "How many sweeps?" is answered by counting boxes before the
   beat starts. Slide 032 gets this right with a bare graph. **Fix:** put the bare graph
   (`components-band.png` without labels) on 041 and move the numbered DFS to a new answer
   slide immediately after.

7. **`csr-payoff.png` (slide 054) — the memory claim is still inside the figure.** It prints
   "stores nnz = 12 numbers here, not the dense 5×5 = 25" in 12px gray under the arrays. That
   is the third claim round 4 split off the degree slide; only the asymptotic panel moved.
   **Fix:** delete the annotation from `csr-payoff.png`. Put the concrete 12-vs-25 count on
   slide 055 as the evidence for its asymptotic claim — which also fixes Major 8 below.

## Majors

8. **Slide 055 "The payoff: memory" — N2/P3 — the split produced a shell.** Title, one
   eight-word line, one formula panel, 62% white, no visual at all. The evidence stayed on
   054. **Fix:** move the 12-vs-25 count here and give it a figure — the dense 5×5 grid beside
   the 12-cell CSR strip at the same cell size.

9. **Slide 026 — F3 — accent-2 numerals on accent-2 discs.** On row 336 the "5" spans
   x[775,799] while node A's fill begins at x=791, so ~9px of the numeral is red on red;
   node B's "3" starts inside its disc. This is the slide that says "work from the degrees".
   Slide 027 places the same labels with 4–13px clearance, so the pair disagrees with itself.

10. **Slide 020 — F3 — "start" and "end" are still clipped by their own discs.** "start"
    occupies y[295,311] while the disc's lower arc crosses y≈303; "end" has its baseline cut
    at y=182. Accent-2 text on accent-2 fill. Round 4 asked for exactly this offset.

11. **Slide 020 — F1/F4 — the interior pairing arcs read as rim-light.** Each arc hugs its
    disc boundary at ~8px on-slide, so it looks like a crescent on the circle rather than a
    bracket tying two edges — the mechanism slides 017–019 spent three slides building. Only
    one of four arcs is labelled "even". **Fix:** offset the arcs clear of the discs the way
    017 does, and label all four or state the arc's meaning in the caption.

12. **Slide 017 — F1 — the pairing arc reads as a fifth edge.** Round 4's geometry fix
    genuinely landed (edges uniform end to end, arc sweeps the angle between two edges), but
    arc and edges are now the same token at the same weight — ~8–9px of `#6b6b6b` each — and
    each "in-out" label sits ~95px from its arc with a black disc between them. **Fix:**
    distinctly lighter weight for the arc; bring each label to its arc.

13. **Slides 029 — F3 — the annotation is struck through for the third round running.** It
    moved off the Cafe→Gym curve and onto the Café→Lib arrow, reading "sa|me edge, t|wice".
    Its leader is a 35px dash touching neither the text (25px away) nor any edge. **Fix:**
    put the annotation in clear space left of the graph with a leader terminating on the
    doubled edge.

14. **Slides 044 and 065 — F3 — arrowheads do not arrive.** On 044, A→C ends 20px from C's
    disc and A→B likewise, on the slide introducing direction, captioned "C receives from
    both A and B". On 065 a uniform `shrinkB` made all three arrows consistent at ~9px short,
    so now none of them arrives, on the slide teaching "edges arriving". **Fix:** set the
    standoff so tips land on the disc boundary; 045 already uses a ~14px standoff that looks
    right — match it.

15. **`edge-disconnected.png` (slide 063) — F3 — the discs are still guillotined.** Round 4's
    uniform 30px pad sits *outside* already-clipped shapes, so the bbox check passes while
    the defect persists: the first ink row is 182px wide — two flat caps of ~91px — and at 5×
    the top node has a flat top, the bottom-left flat left and bottom. **Fix:** the clip is at
    the axes limits, not the canvas. Set `clip_on=False` on the node collection, or expand
    the axes limits by one node radius, then re-crop.

16. **Slide 037 — F1 — three unexplained colour referents.** accent-2 draws route 1–2–4,
    accent-3 draws route 1–3–4, and accent-2 *also* outlines cell (1,4), whose value 2 counts
    both. None is stated, and neither panel is labelled, so the matrix is never identified as
    A². **Fix:** caption the two route colours, outline the cell in `INK`, print "A²" on the
    panel.

17. **Slide 051 — F1 — unexplained red.** Node 1 is red-filled, its three edges red, matrix
    row 1 red-outlined, while the body talks only about $n\times n$ and $O(n^2)$ and the
    caption counts cells. **Fix:** caption "row 1 (red) is node 1's row: 1s at columns 0, 2, 3".

18. **Slide 035 — P1 — a second claim.** The formula panel defines $A_{ij}\in\{0,1\}$, then a
    second sentence redefines it as an edge count for multigraphs. That is the rubric's own
    example — defining a term and introducing a special case of it. **Fix:** move the
    multigraph sentence to its own slide.

19. **Slide 056 — F3/F4 — the arrow strikes through two labels** (its head lands on the
    terminal "e" of "large + sparse", its shaft passes through the "e" of "large + dense") and
    "real networks" overhangs the plot frame. Sub-labels are 12–14px against a 13px page
    number while "CSR" is 23px. `format-regimes.png` is 918×683, so under `.fig.tight` it
    renders 430px wide, not the 760px the slide asks for; round 4 asked for ≈2:1. **Fix:**
    regenerate at ~10×5in; move the arrow clear of the labels; lift sub-labels above 15px.

20. **Slide 043 — F3 — the encoding key shrank.** "1 dot = 1 node" / "1 dot ≈ 1,700 nodes"
    now renders at 11px, below the page number; round 4 measured it at 15px. Also the right
    panel shows the 1,000-node component as **one** blue dot under a stated key of "1 dot ≈
    1,700 nodes", overstating it by 70%. **Fix:** regenerate at column width; draw the
    component at its true dot count or restate the key.

21. **Slides 053 — F3 — the CSR figure came down to the page number's level rather than up.**
    Measured digit heights: dense-A 12–13px, indptr 12–14px, data 13px, annotation 12px,
    against a 13px page number. Also the two-digit indptr cells "10" and "12" fill their
    cells edge to edge while single-digit cells have generous padding, so the row reads
    "0 2 5 8 1012". **Fix:** widen the two-digit cells and raise the whole figure's type.

22. **Policy 2 was not applied to the campus, bowtie, directed-strong and lone-node
    families.** Ink coverage: `selfloop` 0.35×0.46, `edge-single-node` 0.45×0.50,
    `edge-single-node-answer` 0.48×0.53, `campus-path`/`campus-base` 0.53×0.59,
    `directed-weak` height 0.56, `directed-strong` 0.75×0.57, `campus-walk` 0.64×0.59,
    `euler-circuit-example` 0.75×0.66, `circuit`/`cycle` 0.75×0.71. On slide the campus graph
    occupies 255px in a ~480px column, and figure-to-caption gaps run 126px (025), 132px
    (029, 031), 151px (045, 046), against 53–77px on the healthy figures. **Fix:** regenerate
    each with a figsize matched to its rendered column.

23. **Slides 044/045 — F3 — the same A/B/C motif at two sizes** on consecutive slides
    (canvases 804×680 vs 960×900; node radius ~36px vs ~27px), so the graph visibly changes
    scale between two slides that are meant to be the same three nodes.

24. **Policy 3 is still unapplied to Parts One–Three.** Ten of the fifteen figure-bearing
    slides in 001–023 restate their own title or body: 008 "the city", 009 "each landmass →
    one node", 010 "each bridge → one edge", 019 "odd: one edge left over" (all title
    verbatim); 004, 005, 012, 015, 020, 021 (body verbatim). Round 4 declared the policy
    deck-wide but only enumerated slides 029–058. Also still open in later parts: 040, 045,
    050, 056, 059, 065.

## Structural note — worth acting on

**The fourth edge case is not an edge case.** Part Seven closes on "What breaks when edges
have direction?" (064) → "In-degree and out-degree" (065). But Part Five already spent
slides 044–046 on direction, arrowheads, and strong vs weak connectivity. The act's closing
beat re-opens settled material, and its answer is a fresh definition rather than a rule
being stress-tested — the other three cases genuinely break a stated rule.

Recommendation: move in/out-degree into Part Five beside "Edges with direction", and close
act 4 on the **disconnected-graph** case, which actually punctures Euler's theorem and links
straight back to the sweep of Part Five. That gives the deck a much stronger last beat.

## Minors

- 026 — all four discs are accent-2 with no statement of why; the meaning is revealed only
  retroactively on 027.
- 030, 033, 034 — accent-2 carries two or three referents per figure; each is labelled
  in-drawing, so nothing is undecodable, but it is not one-meaning-per-figure.
- 025 — "start = end" sits 110px below its ringed node with no leader, nearer to two other
  discs; the caption wraps into the page-number band at y=653.
- 033 — "visited twice" clears the centre→bottom-left edge by ~5px.
- 039 — in-figure panel titles measure 31px against ~21px body copy, so the figure's words
  are the largest non-title text on the slide (improved from 50px, not resolved).
- 015 — the "k = 4" leader starts ~18px inside the centre disc instead of at its boundary.
- 019 — the pairing arc's lower tip stops ~37px short of the edge it ties.
- 060/061 — the lone node is the only unlabelled node disc in the deck.
- 061 — the ring is flush on the disc rim, so it reads as a node border, not a component;
  draw it dashed at ~1.6× the node radius, matching the Part Five sweep enclosures.
- 066 — "A: 4 × 4 matrix" sits under a graph whose node is also named A; rename to
  "adjacency matrix: 4 × 4" and print A's degree on the node its leader targets.
- 048, 052 — question slides putting the prompt in gray `.note` rather than the `.formula`
  panel the other question slides use; 052 has no timed beat.
- 053 — "512 exabytes." answers 052's question as the first two words of a paragraph about
  something else, with no emphasis and no visual.
- 012 — "two bridges between the same pair" understates it; two pairs are doubled (A–N and
  A–S), which is why A has degree 5.
- 005/007 — the river is a hard-edged rectangle terminating mid-canvas; it reads as a blue
  box rather than a river.
- 008 — figure byte-identical to 005/007, so 007→008 is a text-only change.
- 002 — seven roadmap items against a ceiling of four (defensible for a seven-part deck).
- 061, 067 — captions with zero right margin / 11px above the page-number band.

## Verify before reporting done

    python3 figures/make_figures.py
    marp m01-euler-tour.md --theme network-science.css --allow-local-files --images png -o review/slide.png

For every figure you touch, **open the regenerated PNG with the Read tool and confirm the
defect is gone.** Four consecutive rounds have included at least one repair reported as
landed that the rendered image contradicted. Report ink coverage for every figure and flag
anything below 0.5 in either dimension.

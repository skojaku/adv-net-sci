# Round-12 fixes

**Completion criterion: `python3 check_render.py` exits 0.** It now checks frame overflow as
well as node size and canvas margin.

## The one thing that has not landed

The lecturer's clearest instruction was that in-figure text is too small to want to read.
Two independent reviewers measured the current render against the body type (30px, which
renders as **21px of cap/digit ink** on the slide — that is the floor):

- **Slides 001–027: one of eighteen figure-bearing slides passes.** The rest sit between 47%
  and 93% of body size. The worst is the Eulerian-path slide's "start"/"end" at 7px x-height
  — one of the labels the lecturer named by name.
- **Slides 055–080: thirteen slides fail.** The worst is the self-loop answer slide's "1"
  marker at 10px, which is the entire visual argument of an answer slide.

Round 10 raised `LABEL_FS` 18 → 30, which fixed the *node* labels (now ~15px cap, 70%). It did
not touch the free-standing annotations — "in–out", "left over", "start", "end", "k = 4",
"destroyed", the CSR array digits, the regime labels. Those are the ones that were named.

**This is structural, not a list of oversights.** Figures are authored at 1500–2200px and
scaled into the theme's 380px box, so a point size chosen in figure space shrinks by whatever
factor that figure happens to need. FIGURE_GUIDE already says the rule — author at final size
— and the deck does not follow it.

**The scale is now deterministic, so it can be computed rather than measured.** A `.cols`
column is exactly 537px and full width is 1120px (the `w:` directive is inert; the grid is
pinned to `minmax(0, 1fr)`). So for any figure:

    scale        = min(container / src_w, 380 / src_h, 1.0)
    on_slide_px  = pt * (dpi / 72) * scale

**Fix: add an assertion in the generator that every piece of text lands at ≥21px on the
slide, and let the build fail.** Then raise the sizes until it passes. Doing it per label will
regress again; doing it as one derived rule will not.

Figures needing it, from the two reports: `euler-path-example`, `euler-circuit-example`,
`degree-definition`, `parity-even`, `parity-odd`, `parity-bound`, `konigsberg-degrees`,
`konigsberg-bombed`, `konigsberg-blank`, `abstraction-*`, `multigraph*`, `selfloop*`,
`campus-*`, `store-edgelist`, `store-adjlist`, `csr-build`, `csr-payoff`, `csr-memory`,
`format-regimes`, `recap`. Effectively all of them, which is why it should be one rule.

## Already done

The three route animations were generated but **never wired into the deck** — the slides
still pointed at the static PNGs, so the lecturer's top-priority item did not exist in the
rendered deck at all. Now fixed and verified in the HTML output: the Walk, Trail and Path
slides reference `campus-walk-anim.gif` / `campus-trail-anim.gif` / `campus-path-anim.gif`.

`check_render.py` also gained a frame-overflow check, which caught slide 041 in addition to
the 079 the reviewers found.

## Blockers

1. **Slide 079 "Module 01 review" overflows the frame.** Ink reaches y=708 in a 720px frame,
   where every other slide stops by ~631, and what falls off is the deck's only notebook
   pointer — it renders as "Build a CSR matrix by hand in the Module" with "01 notebook."
   below the edge. The note is also a paragraph below a fragmented list, a third instance of
   the reading-order pattern. **Fix:** move the pointer above the bullets or fold it into the
   Representation bullet, and shorten the bullets — dropping "walk, trail, path, circuit,
   cycle" from bullet 2 and "$(\mathbf{A}^k)_{ij}$ counts walks" from bullet 3 recovers about
   two lines. This is a consequence of raising the body type to 30px; expect other slides to
   be close to the edge too.

2. **Slide 041 overflows the frame** — ink to y=700. Found by the new check, not reported by
   either reviewer. Same cause. **Fix:** shorten or restructure until it fits.

3. **Slide 021's formula runs outside its own panel and touches the figure.** The KaTeX
   display line spans x=110→707 while the beige panel ends at x=616, so the last ~90px sits on
   bare white, and the "2" glyph is in contact with the figure's red *start* node. Also caused
   by the type increase. **Fix:** shorten the set expression — `\#\{\text{odd nodes}\} \le 2`
   — or take the inequality out of the panel onto its own line.

## Majors — text and marking

4. **Slide 023 "The verdict" was over-cut.** The bullet reads "Rule: at most two odd nodes",
   which is not a statement of anything without its antecedent; the qualifier lives two slides
   back. This is the slide students photograph. **Fix:** "Rule: a cross-every-edge walk allows
   at most 2 odd."

5. **Slide 021 never names or bolds "Euler's theorem"** — a term on the lecturer's own key
   list. It appears in the Part Three divider and in the recap sixty slides later, but not on
   the slide that states it.

6. **Slide 013 teaches parallel edges without ever naming multi-edge / multigraph.** The word
   first appears, unbolded, in Part Seven with no definition to return to.

7. **Slide 066 is the one slide still too text-heavy to speak over** — 44 words in two prose
   blocks that restate each other. **Fix:** cut the note; the sparse-format setup lands on the
   next slide anyway.

8. **Slides 056–062: edge list, adjacency list and adjacency matrix are never marked as key
   terms.** The red convention starts abruptly at CSR, so a student scanning red afterwards
   gets CSR and connectivity but not the three formats Part Seven exists to teach.

9. **Slide 067 has four red spans** (CSR, data, indices, indptr). The three array names are not
   concepts. **Slide 078's "0 or 2 odd-degree?"** and **slide 079's "Abstraction (1736):" /
   "Representation:"** are structural labels, not key terms. Unbold all of these — the accent
   only means something while it is rationed.

10. **Three slides missed the centring sweep**: 066 (293px bottom slack), 077 (269px), 069
    (255px). For calibration, slide 062 got `mid` at a 392px content height, so all three are
    shallower than slides already judged to need it. Also 013 and 021 in the first range.

## Majors — figure and caption

11. **Slides 069, 070 have figcaptions that restate what the figure now prints legibly**, and
    070's calls the x-axis "node count" where the figure draws "network size". Delete both.

12. **Slide 070's takeaway is in the wrong register.** "Rule of thumb: edge list on disk,
    sparse matrices for analysis" is the one thing a student needs from that slide and it is
    set in gray `note`, the faintest text on the page, while the substance sits in 14–17px
    figure labels.

13. **Slide 013**: eight lines of text against a figure whose ink is 229×60px. **Slide 014**:
    the entire self-loop drawing is 39×69px of ink — 0.3% of the frame. Both are the
    author-at-final-size problem showing up as layout.

14. **Slides 018, 020**: the pairing arcs measure gray 159–175 while the edges they annotate
    measure gray 107, so the annotation reads *lighter* than the content it explains.

15. **Slide 069**: "Dense stores 25 numbers **here**" has no referent on its own slide — the
    five-node matrix it means was two slides back.

16. **Slide 005**: three static text blocks including a five-line note posing three questions,
    all landing at once. **Slide 007** re-asks slide 005's note almost verbatim over the same
    figure.

## Over-cutting — restore these

Text was cut hard and mostly correctly, but three things went that should not have:

- **DFS and BFS are gone from the deck entirely** (old deck: 3 mentions, now 0 — the old
  slide was literally titled "Finding components: DFS and BFS"), along with the cost
  $O(N+M)$ and the note that breadth-first also yields shortest-path distances, which was
  the hook into Module 2. Slides 040/041 teach the procedure but give it no name, so a
  student has the method and no term to look it up under, and the Module 2 link is severed.
  **Fix:** one line back in 041's note — "This sweep is **BFS** (or **DFS** — visit order
  differs, the partition doesn't). Cost $O(N+M)$; breadth-first also gives shortest-path
  distances, which Module 2 needs."
- **"Eulerian trail" is corrected but never defined.** Slide 032 says the Eulerian path is
  really an Eulerian *trail*, and the corrected form appears nowhere in the deck. **Fix:**
  "…is really an **Eulerian trail** — a trail that uses every edge."
- **Slide 048 loses "strongly connected" from its own body.** The text is a subjectless
  fragment, "A directed path from every node to every other node", while its counterpart 049
  marks **weakly connected** in red. **Fix:** "A graph is **strongly connected** when a
  directed path runs from every node to every other."

## Minors

- 023's bullet says "three, three, five, three" while the figure prints 3, 5, 3, 3 — neither
  order nor notation matches.
- 016 and 021's figcaptions duplicate what their figures already label.
- 079: "one component" and node N's degree numeral sit 9px apart on a shared centreline; no
  overlap, but they read as one block.
- 008: bridges and coastlines render at gray 201–215, about 1.5:1 against white — defensible
  as "geography going away", but the slide does not say so.
- 062: the red outline marks two cells here and row 1 on the neighbouring slides — one colour
  doing two pointing jobs across three consecutive slides.
- 026: the paragraph carries the argument and bullet 1 restates it over three more lines.
- 012, 063: a trailing clause each that a fragment would serve better.
- 077: "That's why the sweep from Part Five matters" is a lecturer aside inside prose
  otherwise worth keeping whole.

## Verify before reporting done

    python3 figures/make_figures.py
    python3 figures/make_animations.py
    marp m01-euler-tour.md --theme network-science.css --allow-local-files \
         --images png -o review/slide.png
    python3 check_render.py        # must exit 0

Then open the rendered PNG of every slide you touched, and report the smallest in-figure text
per figure in on-slide pixels.

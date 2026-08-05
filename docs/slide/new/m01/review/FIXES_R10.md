# Round-10 fixes

**Completion criterion for the figure work: `python3 check_render.py` exits 0.**

That script is new. It runs after marp and measures what a student sees rather than what
the generator intended — which is the whole reason this defect kept coming back. Run it
after every regeneration; do not report done until it passes.

## The one cause, one level further out

Nine rounds hit the same thing from three angles: node diameter (asserted in figure space),
in-figure type size (set in figure space), and now canvas margin. Each fix was correct where
it was measured and irrelevant on the slide, because the deck scales each image by
`min(w_directive/src_w, 380/src_h)` — 0.14× to 0.34× depending on the figure.

The node work landed: measured on the rendered slides, diameters are now 26–51px, from
18.5–296px. What did not land is that **six figures are 77–90% white canvas**, so the deck
scales margin rather than the picture:

    slide 013/068  selfloop.png                  drawing lands  38x69px   =  2% of its box
    slide 069      selfloop-answer.png                          53x87px   =  4%
    slide 070      edge-single-node.png                         39x39px   =  1%
    slide 071      edge-single-node-answer.png                  63x63px   =  3%
    slide 012      multigraph-bridges.png                      223x58px   =  7%

Nine more sit between 22% and 34% (`check_render.py` reports them as warnings): the
abstraction build, `konigsberg-blank`, the campus family, and — worst — slide 050's
`directed-parity-counterexample` at 22%, which is the key result of Part Six rendered at
4.6% of the slide with its caption stranded 206px below it.

**Fix: crop every canvas to its ink plus a small fixed pad, in the generator, and assert the
ink fraction there.** Two consequences worth planning for:

1. Cropping enlarges the drawing by 1.6×–9× linear, which enlarges the in-disc labels with
   it — that closes part of Blocker 2 for free.
2. Cropping also enlarges the node discs, which will push some figures past the checker's
   node band. **Re-derive each figure's `w:` directive so the on-slide node diameter still
   lands in 26–51px.** The two constraints — uniform node size and figures filling their box
   — only both hold if `w:` is chosen per figure. Emit the recommended `w:` per figure and
   tell the deck agent; do not silently leave the deck's current values.

## Blockers

1. **Six figures fail `check_render.py`** (list above). Crop them.

2. **In-disc node labels are 7–9px** on slides 029, 030, 031, 032, 040, 044, 046, 047, 048,
   050, 051, against a 13px page number — and the figcaptions address those labels by name.
   Slide 044's caption reads "C receives from both A and B; nothing leaves C"; slide 029's
   "the Café–Gym edge, crossed twice". At 7–8px neither reference is resolvable, so the
   caption cannot be matched to the drawing. The Königsberg family proves it is fixable:
   same 35px disc, 14px letter. **Fix:** derive the in-disc label size from the on-slide disc
   diameter (~40% of it → 13–16px). Where a word cannot fit (Dorm/Cafe/Gym/Lib), set it
   outside the disc.

3. **Slide 075 "Module 01 review" — two annotations printed on top of each other.** The top
   red degree numeral and the words "one component" overlap: 19 pixels of the gray text fall
   inside the numeral's bounding box, minimum ink-to-ink distance 1.0px. At 6× the "3" sits
   between the "m" and the "p" of "component" and neither is readable. This is the deck's
   summary slide and these are its only two annotations. The other three numerals stand
   52–65px clear; only the top one needs re-placing. **Fix:** move "one component" clear of
   the numeral band, or set the top numeral inside the ring beside node N.

4. **Slide 060 "$A^k$ counts walks" — node labels 6–7px** against 22–23px matrix digits in
   the same figure, a 3.3× internal disparity, and its discs (26–27.5px) are the smallest in
   the deck. Those labels are what distinguishes route 1–2–4 from 1–3–4, which is the slide's
   entire point. **Fix:** drive every element of this figure from one on-slide type size ≥13px
   and bring the graph panel to the deck's node standard.

5. **Slide 025 "Eulerian circuit" — an unexplained accent-2 ring on an even node.** The ring
   encircles the centre node and nothing on the slide, in the body, or in the caption says
   what it means. Accent-2 meant "odd degree" on 022 and "odd degree / start and end" on 023,
   the immediately preceding figure slide; the ringed node here has degree 4. The only
   disambiguation is an 8px "start = end" floating 58.5px away with no leader. The ring also
   crosses all four edges. **Fix:** say what the ring means in the figcaption and set that
   label at or above page-number size beside the node.

6. **Slide 039 "Your turn: run the sweep" — the figcaption is clipped by the bottom edge.**
   Caption ink occupies rows 698–719 of a 720-row slide and is still 14px wide on the final
   row; the descenders of "yourself", "components", "yet" are cut. **Fix:** lift the figure or
   the text block so the caption's last row lands at or above y≈690, as slide 040 does.

## Majors

7. **Free-standing annotations still below 13px** on slides 027 ("destroyed" ×2, 12px), 030
   ("start" 9px, "visited twice" 10px), 033 ("visited twice" 9px), 042 ("1 dot = 1 node"
   12px), 050 ("in 0 / out 2" 11px), 066 (regime labels 8px). Round 9 named this exact set;
   the degree numerals got the bump, these did not. **Fix:** one shared annotation size in the
   generator, derived on-slide, not per figure.

8. **Slide 050 "The directed Euler condition" — P1, three ideas.** The closed-tour rule, the
   trail rule, and a separate claim that total degree is the wrong quantity ("Below, both
   nodes total 2 — yet neither balances", plus the figure and a two-line caption devoted to
   it). The deck taught the undirected analogue across three slides, so this breaks its own
   precedent. **Fix:** split — the counterexample gets its own slide between 049 and the rule.

9. **Slide 065 "The payoff: memory" — the caption disagrees with its own figure twice.** It
   prints 7,700× where the figure 30px above prints 7,692×, and its first clause "n=5: dense
   25 vs CSR 30, dense wins" describes a comparison the figure does not draw. **Fix:** caption
   what is drawn, one number for the ratio.

10. **The storage build's anchor still moves** on slides 054 and 060: one graph at discs
    42.5 / 36 / 34.5 / 26.5px with node 0 at four different coordinates. 055/056/057 now
    agree; 054 and 060 do not. **Fix:** pin the graph panel's coordinates and on-slide scale
    across all five.

11. **Slide 062 "64 exabytes" uses "CSR" one slide before it is defined** (first prose use is
    this slide; the definition is on 063). **Fix:** write "what a sparse format refuses to
    store" here and let 063 name it.

12. **Slide 059 back-references an activity that never happened.** "The one whose matrix you
    just wrote down" — no slide asks students to write down a matrix. **Fix:** add "write it
    down" to 056, or reword.

13. **Slide 057 "Degree, three ways" — two of three bullets have no referent.** The bullets
    span edge list, adjacency list and matrix; the figure is `store-matrix.png`, identical to
    056's. **Fix:** a three-panel build, or one figure marking degree 3 in the chips, the
    adjacency row and the matrix row.

14. **Part Two "Abstraction" has no student activity** across six consecutive slides
    (008–013), while every part from Four onward has a "Your turn". Round 9 graded Part Six a
    Major on exactly this evidence. **Fix:** add one slide that makes students do the
    abstraction — a second map or transit diagram, decide with a neighbour what the nodes and
    edges are.

15. **Slide 012 counts to five bridges beside a figure that draws two.** The body says "island
    A touches five bridges in all"; the figure draws only the N–A pair. On a slide whose whole
    method is counting one bridge at a time, the load-bearing number cannot be checked.
    **Fix:** move the sentence to the slide that draws all seven, or draw A's other three in a
    light tint.

16. **Slide 066 "Which format when?" — two quadrants tinted, two not, with nothing saying what
    the tint means**, and its four regime labels are 8px against 16–18px axis labels in the
    same figure. **Fix:** one in-figure type size ≥13px; state what the tint marks or drop it.

## Minors

- 008's caption still over-claims ("the labels are all that survive the cut") over a render
  that shows the water tint, the coastlines and all seven bridges. The figure fix landed; the
  caption is the old one.
- 013's node is labelled "X" while every other node in Parts Two and Three is N/A/B/S.
- 020's label pairs read in opposite orders ("start"/"odd" left, "odd"/"end" right).
- 017 and 019's pairing arcs are lighter than the ordinary edges (gray 133/127 vs #6b6b6b).
- 022's figcaption wraps and strands "degree" alone on its second line.
- 027's two "destroyed" labels have 10.6px and 34.0px clearance — 3× apart; equalise.
- 029 carries a baked-in "same edge, twice" under a figcaption saying the same thing.
- 034's red is unglossed (it meant odd degree on 026/027, the route on 030/031/033).
- 037's bullet 2 calls back to "the two triangles from a moment ago" over a different graph.
- 040's dashed rounded boxes are unglossed.
- 042's blue dot carrying the slide's point is 20 pixels of ink at 82% gray coverage.
- 049's callout repeats the title verbatim.
- 035 and 050 say "below" for a figure in the right-hand column.
- 071's component ring is a hairline at luminance 151–207.
- 073 prints no degrees, though 072's setup is "every node has degree 2".
- Captions float 107–149px below their drawings across the deck; on 037, 038 and 039 they
  land in or below the page-number band. Same root cause as Blocker 1 — cropping fixes most.

## Verify before reporting done

    python3 figures/make_figures.py
    marp m01-euler-tour.md --theme network-science.css --allow-local-files \
         --images png -o review/slide.png
    python3 check_render.py        # must exit 0

Then open the rendered PNG of every slide you touched.

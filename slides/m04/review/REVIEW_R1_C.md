# Slide review — m04-node-degree.md, slides 047–068 — 2026-08-05 (round 1, reviewer C)

**Verdict:** FAIL
**Slides:** 22 reviewed (047–068, all opened, none skipped) · **Blockers:** 2 · **Majors:** 13 · **Minors:** 10

**Slide numbering correction:** the γ worksheet is rendered slide **060**, its answer **061**;
"Does every network do this?" is **066**. 048/053/058 were right.

## The two load-bearing questions

1. **Does 2.3 appear on the worksheet slide? No — the withheld answer holds.** Slide 060 draws only −1.3
   (body and figure), the gray triangle labels "1 decade" and "1.3", the blank `γ = ______`, and the axis
   ticks. No 2.3, no "1 − γ", no gray note div. `figs_tail.py` asserts "2.3"/"2{.}3" are absent from the
   strings actually drawn — it checks drawn strings, not the TikZ body, so coordinate digits cannot create
   a false pass.
2. **Axis legibility: no tick or curve label below the 15px floor in this range**, measured not eyeballed.
   `check_render.py`'s "smallest ink 12–13px" warnings on 050/051/055/056/064 are **scatter markers**
   (generator `d=13`), not glyphs. Real glyphs measure: y-tick mantissa 24px, superscript exponent 17px,
   x-tick "100" 20px. The 1px ink is the minus rule inside `10⁻²` and a dashed line. **F3 has one finding
   in this range and it is placement, not size** (Major 12).

## Milestones (S5)

- **Part Five (046–062)** — two: slide 060 "Your turn" (γ from −1.3) and 062 the *Data Visualization*
  paper exercise.
- **Part Six (opens 063)** — no interactive element in 063–068; the part runs past this range.

## Passes worth recording

No bar charts (`linear-axes` and all three `binning` panels are dot plots; the rest are step/line curves).
No legends anywhere. No P1 violations — all 22 slides state in one sentence. No `.note` leaks on any
question slide (048, 053, 058, 060, 066 carry no gray note div at all). L2/L3/L4 clean.

## Blockers

1. **055 "A quantity with no bins in it" — F1 — `ccdf-def.png` never says what one dot is, and its two
   counting stories disagree.** Each column is a node, each dot one unit of degree. The figcaption says
   "count everybody above the line"; the ink above the dashed k=3 line is **11 dots**, while the in-figure
   text prints "above the cut / 5 of 20 = 0.25". Accent-2 marks whole columns, so **26 red dots are drawn
   and 15 sit below** the line the label says they are above. The y-axis is titled "degree" with no ticks,
   the x-axis is unlabelled. **Fix:** state the encoding in the drawing (a "one node" bracket under one
   column, a "1 edge" caliper beside one dot) and make the counted quantity match what is red — "5 of 20
   columns cross the line". Or draw 20 discs sized by degree and colour the 5 above the cut.
2. **057 "Why not the CDF?" — F1 — one shared y-axis title over two different axes.** "share of authors"
   is drawn once at the far left; the left panel is linear (0, 0.5, 1) and the right is logarithmic
   (1, 10⁻², 10⁻⁴). Nothing says so, and the unlabelled log transform is exactly what produces the
   difference in shape the slide asks students to read. **Fix:** label each panel's scale in its frame,
   give each its own y title, and state the real reason — the CDF's values run to 1, which a log axis
   cannot spread; the CCDF's run to 0, which it can.

## Majors

3. **047 — F1** — figcaption says "every one of 23,133 authors, plotted by how many coauthors they have";
   the figure draws **122 dots**, one per distinct degree, at height p(k). No author is plotted.
4. **050 — F1** — "identical data, **identical bins**"; the figure has no bins (`condmat_pdf()`: "One
   point per observed degree, no bins"). This is the only mention of bins before the question that
   depends on them.
5. **053 — N1** — the question's premise is false for the figure just shown: "That plot had bins." 050 and
   051 were unbinned, and binning is never introduced. 054 then answers with a *different* construction
   (histogram densities over k ≥ 10 at widths 1, 8, 32). **Fix:** introduce binning before asking about it.
6. **054 — F4/P2** — `binning.png` lands all three panels at once where FIGURE_SPEC specifies a build; and
   panels 2 and 3 carry **no y tick labels**, so the shared vertical scale the comparison rests on cannot
   be verified from the slide.
7. **059 — N2/F4** — `slope-derivation.png` contains **no drawing**: three numbered text lines and a gray
   gloss column. Its result is repeated verbatim in the KaTeX below, and the figcaption is stranded between
   the two. **Fix:** draw the integration (power law with the region above k shaded, that mass re-plotted
   as one CCDF point), and delete either the figure's third row or the KaTeX line.
8. **060 — N1/F1 — the worksheet data is synthetic and the slide does not say so.** It arrives after nine
   slides of cond-mat; the only tell is that x reaches 1000 where cond-mat stopped at 279. A student
   reading it as the same network gets **γ = 2.3 here against γ = 2.44 fitted on slide 051** — two answers
   on the slide that teaches the two routes agree. **Fix:** title the panel "a different network", or fit
   on cond-mat and use its real slope.
9. **061 — F1/F5** — accent-2 sets `γ = 2.3` (the answer) *and* is the strike-through cancelling
   `γ = 1.3` (the wrong one). Both `#B14434`. **Fix:** strike in annotation gray.
10. **062 — F4** — `exercise-card.png` encodes nothing: a rounded rectangle restating the left column. The
    slide is a text column beside a picture of a text column. **Fix:** cut it, or show the four thumbnails
    the handout actually contains.
11. **064 — N1** — `hubs-share.png` switches to a **rank–degree plot**. No slide introduces a rank axis and
    the word "rank" appears nowhere in the deck's prose. **Fix:** make the point on the CCDF already on
    screen, or introduce the rank plot on its own.
12. **065 — F3 — the "physicists" label is nearer a curve it does not name.** Measured: 50px to the
    physicists curve, 55px to the Internet curve, **23px to the yeast curve**. Only its colour resolves it.
    The generator moved it here to stop it crossing its own tail, trading one defect for another.
    **Fix:** give the solver the other curves as blockers with a clearance floor and its own as attractor.
13. **065 vs 067/068 — F5/F1** — accent-2 means "the Internet, the hub-rich network" on 065 and "the random
    graph, the one with no hubs" on 067–068; blue is the physicists on 065 and a BA model labelled "power
    law" on 068. **Fix:** fix a deck-wide role from Part Six on — accent "has hubs", accent-2 "does not".
14. **067 — N1/F1** — "a random network with **the same average**" never says as what. The only number is
    ⟨k⟩ = 4.0, which is neither cond-mat's 8.08 nor the Internet's 3.88. **Fix:** name it and use the real
    mean.
15. **048, 053, 058, 060, 066 — N4** — all five pose the question and stop; **not one carries a thinking
    beat on the slide.** The beats exist only in speaker notes. **Fix:** put the instruction on the slide.

## Minors

16. **049** — the accent-3 tail band starts at k = 96, not 100, 23px left of the tick the annotation names;
    its top edge encodes nothing.
17. **049** — caption says "first ten **columns**"; the figure is a dot plot and its own annotation says
    "k ≤ 10".
18. **051** — "R² = 0.93" in accent-2, never explained, used or mentioned again.
19. **050, 052, 056, 062 — L6** — bottom-most ink at 533 / 533 / 534 / 471 of 720. Take `mid`.
20. **056** — the caption's "one point per distinct degree" was already true of the histogram, so it does
    not distinguish the CCDF. The real distinction — no width to choose — is never stated.
21. **064** — caption "34% of all **connections**" against the figure's "33.8% of all 25,144 **edge ends**",
    in a deck that taught the 2M distinction.
22. **047 — P3** — the title promises the variance and **no variance number appears anywhere in Part Five**;
    the only one that lands is 067's `Var/⟨k⟩ = 1.00` for the random graph, with nothing to compare it to.
23. **061 — P3** — the same fact stated four times: title, figure, figcaption, body.
24. **052 and 068 — F1** — curves that leave the bottom of a log axis terminate *on* the x-axis line, which
    reads as "the distribution ends here". The floor is 10⁻⁵, not zero.
25. **068 — F1** — accent names "power law" here, drawn from a BA model, where accent meant cond-mat on
    every previous plot including "physicists" three slides earlier.
26. **068 — F4** — the title names a lattice; the figure and caption carry three curves. Retitle to the
    point the figure makes.

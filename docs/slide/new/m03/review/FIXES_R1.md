# m03 FIXES — Round 1

Sources of these findings:
- `check_render.py` after porting m02's stronger version (node discs found by **colour**,
  not luminance; container-mismatch gate; `CONTENT_BOTTOM` 660 not 690; figcaption-math
  gate). The version m03 was scaffolded from could not fire its own node-size test on this
  palette, so that band went unenforced for the whole first build.
- A slide-by-slide read of the rendered PNGs.

The four parallel reviewer agents launched for this round never returned a report. Recorded
as a process failure, not a coverage claim: this list is what the checker and one human-style
pass found, and it is not a substitute for the four-way read.

## Blockers

1. **Slides 61, 80 — F3/L-layout — a figure authored full width is used in a `cols` column**,
   so it renders at 48% of its intended scale: `qk-bias` node discs land 19px against the
   26–52px band, `design-principles` 19px. Evidence: `check_render.py` container gate, and
   slide 61 shows a drawing occupying a third of its half-frame.
   *Fix:* slide 61 becomes a full-width figure slide (formula panel above the figure, not
   beside it). `design-principles` is re-authored for the **column** container as a degree
   dot-plot (see 5 below), because a full-width Moravian map cannot share a slide with a
   five-item list without overflowing.

2. **Slides 83, 85, 89 — same defect, opposite direction** — `ring-q`, `er1-q`,
   `triangles-q` are authored for a column and used full width, so they render at 209% and
   their discs land 52–53px, outside the band, and inconsistent with their own answer slides
   (which use `cols` correctly).
   *Fix:* in the deck, wrap those three question figures in the same `cols` layout as their
   answer slides — formula panel left, figure right. The figures do not change.

3. **Every weighted Moravian figure — F3 — the Znojmo label is struck through by the
   Znojmo–Hodonín cable.** Visible on slides 11, 19, 29 and everywhere the candidate routes
   are drawn. Cause: the label solver was given only the seven MST edges to avoid, because
   constraining all thirteen had no solution at 30pt.
   *Fix at the generator:* re-run the solver against **all thirteen** edges. The type is now
   36pt and the far-out side variants exist, so re-test; if there is still no solution, add a
   leader-line placement rather than dropping the constraint. Do not shrink the type.

## Majors

4. **Slide 38 — F3 — `real-grid-mesh` draws its nodes at `SMALLNODE`**, landing 25–26px,
   at or below the floor.
   *Fix:* draw them at `NODE`. The 7×3 grid has 145bp spacing, so 40bp discs fit.

5. **Slide 92 — F3 — `m04-teaser` discs and dots land 18px.**
   *Fix:* discs to `NODE`, edge-end dots to at least 26bp, spacing widened to suit.

6. **Nineteen slides — content runs past y=660**, the theme's actual content box
   (29, 32, 45, 47, 51, 56, 60, 68, 69, 71, 74, 76, 77, 79, 81, 83, 85, 88, 89). Cause: a
   three-line body paragraph above a full-width 380px figure and its caption.
   *Fix:* trim the copy above a full-width figure to **two lines at most**. Telegraphic is
   fine; the lecturer says the sentence aloud.

7. **The same sentence appears three times on a slide** — in the body, as an in-figure
   annotation, and again in the `figcaption`. Slide 17: "sort every route by price" (body),
   "sort every route by price, then take them in turn" (in figure), "thirteen routes,
   cheapest first" (caption). Slide 19: the body, "51 km closes a loop" (in figure), "the
   loop it would have closed" (caption). Slide 61: "draw an end at random" twice.
   *Fix at the generator:* the in-figure note carries **numbers only** — 292 km, 3/8,
   +136 km, R values, step counts. Prose lives in the figcaption, once.

8. **Slide 17 — F4 — `kruskal-rule` does not carry its point.** The white chips behind the
   numbers are white-on-white so the row reads as a run-on "17 — 29 — 42 …" with a stray
   leading dash, and the drawing fills a thin band.
   *Fix:* redraw as a sorted row of outlined chips with the sweep arrow beneath the row, and
   drop the in-figure sentence (see 7).

9. **Slide 11 — F1 — unexplained encoding.** The worksheet figure rings Brno in accent-2 and
   prints "power plant", but this slide asks students to draw any connecting grid; nothing on
   it explains why one town is marked.
   *Fix:* `kruskal-worksheet` / `moravia-graph` used on the Your-turn slide carries no ring.
   Brno's ring belongs on the Prim slides, where the start node is the point.

## Minors

10. **Slide 5 — P3** — the in-figure "1919" repeats the slide title "Moravia, 1919".
    *Fix:* drop the in-figure note; covered by 7.

11. **Slide 29 — F5** — the two tied cables are drawn accent-2 and accent-3, but the deck
    text calls them interchangeable. Using the deck's "secondary comparison" colour for one
    of two equal options is defensible; state it in the caption
    ("either the red one or the gold one") so the colours are explained.

## Deck-level (S-criteria) — no findings

- **S1** Act 1 opens with Moravia 1919, Borůvka, the West Moravian Power Company: real place,
  real date, real name. ✓
- **S2** Parts 2–3 do the mathematics of *that* grid — its MST, then breaking *it*. ✓
- **S3** Parts 4–5 generalise to percolation, κ and f_c. ✓
- **S4** Part 7 is four question→answer pairs, each posed before any resolution. ✓
- **S5** Milestones: P1 draw-your-own-grid (11) · P2 Kruskal trace (20) and Prim trace (24) ·
  P3 poll (35), live demo + paper exercise (48) · P4 marimo slider (54) · P5 κ by hand (65) ·
  P6 designer discussion (78) · P7 every slide a prompt. ✓

---

# Rounds 2–5 (same document, appended per round)

**R2** — the fan-out family. `branching`, `dilution` and `molloy-reed` computed every
level's x from one step size and put level 2 at x = 1300 on an 1100 bp canvas, so half of
`molloy-reed` was drawn off the page and its two panels overlapped. Its arrival label was
anchored left of x = 0 and the crop clipped "came in this way" to "in / ay". `fan_tree`
now asserts the tree fits before it draws. Dashed had meant both "the edge you arrived on"
and "removed" inside one drawing; the arrival edge is solid gray now. `kruskal-rule` set
white chips on a white page and read as one run-on string with a stray leading dash.

**R3** — one visual, two meanings, in three more places. `spanning-count` numbered its
cables in Kruskal's order four slides before Kruskal exists, and the same badges meant "a
count" there and "a step" on slide 22. `order-irrelevant` hung each yard's label below its
grid, so the lower label was drawn inside the grid above it. `betweenness-a` drew the
bridge-removed graph while its caption asserted the hub-removed result.

**R4** — `fixed-vs-adaptive` printed 57 % beside prose saying 58 %: the measurement is
0.575 and the float is 57.49999999999999, so both `%.0f` and `ROUND_HALF_UP` on
`str(x*100)` give 57. Percentages now format through `Decimal(repr(x))`. `er1-a`'s caption
was wider than its 520 bp column and the crop clipped both ends.

**R5** — `ring-a` kept the intact ring's degree labels after cutting a node, so every
survivor still read "2" on a drawing that shows two of them with one cable. `m04-teaser`
reused the edge-end pile without the label the identical visual carried 31 slides earlier.

## Verdict

`check_render.py` exits 0: 92 slides, node discs 26–42 px across 351 discs, no slide past
the content box, no container mismatch, no math in a figcaption. Every figure passes its
own floors — size, x-height, ink span, canvas fit, palette, planarity, label and chip
collision — and every number it prints is computed from the data and cross-checked against
DECK_SPEC.

Not claimed: a four-way independent read of all 92 slides. Twenty-nine were read
individually here; the rest are covered only by the checker. The next round should be a
reviewer pass over the 63 that were not.

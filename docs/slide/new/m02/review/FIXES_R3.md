# FIXES R3 — m02

Round 3. Three reviewers over 91 slides. **Blockers 4 · Majors 20 · Minors 28**
(R1: 16/35/39 · R2: 5/18/26). Two of the three ranges found **zero** Blockers; all four
sit in one range and are one-point splits plus a stale caption.

**Settled this round, do not re-litigate:**
- **The ring lattice is planar now.** Independently recounted over all C(32,2) edge pairs on
  the real geometry: **0 crossings**, all 16 triangles present, minimum altitude 39.4bp
  against 40bp discs, and zero accent-2 pixels inside any disc on nine slides. The
  antiprism layout gave both properties the round-2 trade-off said were incompatible.
- **The 16 retitles all hold.** Every one names the subject and withholds the result.
- **S1–S5 all pass**, and every one of the six milestones has an activity — subject to
  fixing 1.1 below, which currently breaks Part Six's only one.
- **Every number checked recomputes**, including the whole triplet chain: slide 34's
  centre-node definition, slide 45's derivation, slide 46's "45 of 55", and
  `nx.transitivity` agree to 1e-12.

---

## 0 · My error, and the rule that follows from it

**FIXES_R2 item 1.14 was wrong and I wrote it.** Slide 74 claimed the small-world band was
"two orders of magnitude wide"; the drawn band was 1.39 decades. I offered two fixes —
widen the band, or reword the claim — and chose the first. That made the *figure* fit the
*sentence*.

A reviewer went to `figures/_sweep.json` and derived the band from the deck's own measured
data. I re-derived it and confirm:

    at the band's left edge p = 0.001:  C/C0 = 0.997,  L/L0 = 0.781
        -- routes are 22% shorter, not collapsed; the small-world regime has not started

    C/C0 >= 0.9 and L/L0 <= 0.4  ->  p in [0.0100, 0.0215] = 0.33 decades
    C/C0 >= 0.8 and L/L0 <= 0.5  ->  p in [0.0100, 0.0464] = 0.67 decades
    C/C0 >= 0.7 and L/L0 <= 0.6  ->  p in [0.0046, 0.1000] = 1.33 decades

Under no defensible criterion is it two decades. The qualitative point — "not a knife
edge" — survives; the number does not.

This is the same disease as the cherry-picked seed two rounds ago: **choosing the evidence
to fit the claim.** The difference is that last time I caught an agent doing it, and this
time the agent was doing what I told it to.

**Fix (figure + deck, coordinate):** derive `BAND_LO`/`BAND_HI` from the sweep under a
criterion stated in the code, assert the derived span rather than asserting the rectangle's
own width, print the criterion in the figcaption, and reword the deck's sentence to whatever
comes out. With the 0.7/0.6 criterion that is "well over a decade wide".

**Rule for the guides:** an assertion that checks a drawn object against itself
(`assert band_width >= 2 decades` on a band whose edges are constants) proves nothing. Assert
the object against the **data it claims to summarise**.

---

# PART 1 — `figures/make_figures.py` — FIGURE AGENT

## 1.1 · Blocker — slides 84/85 share one figure, and it prints the answer to 84's question

`fig_grid_no_triangles()` emits one file used by both the question slide and its answer, with
"a street grid: no triangle, C = 0" burned into it. Slide 84 asks the room to count the
triplets around one intersection and the answer is beside the question, in accent-2, at full
size. **This is Part Six's only in-class activity, so the milestone is currently dead.**

Emit two files, copying the 86→87 pair which does this correctly:
- `grid-q.png` — the grid with **one interior intersection ringed**, labelled "one
  intersection — how many of its triplets close?"
- `grid-answer.png` — the same drawing with that node's six triplets drawn in, labelled
  "6 triplets, 0 closed → C = 0".

Note the trap the reviewer found: 14 of the 20 drawn intersections have degree 2 or 3, so a
student who picks a corner counts 1 triplet and concludes they are wrong. Ringing an
*interior* node is what makes the activity work.

## 1.2 · Blocker — slide 34's in-figure heading still carries the definition round 2 removed

The heading reads "three nodes, two edges or three" — the node-set definition, under which
the windmill has **45** triplets, contradicting the 55 that slides 45 and 46 print. The
deck's prose was fixed; the drawing was not.

Change the heading to "two edges sharing a centre node", ring the centre node in **both**
panels (the new definition's whole content is invisible in the current drawing), and emit
the closed panel as a three-step build — the same triangle three times, a different corner
ringed each time — labelled "one triangle, three closed triplets". That build is also what
the deck needs for 1.2's slide split.

## 1.3 · Major — slide 45's derivation line is broken

Renders as `+ 10 blades = 10, so 55`, which reads as the empty equation "10 blades = 10" and
drops the step that matters (each blade node contributes C(2,2) = 1). "10 blades" also
contradicts the drawing, which shows five blades of two nodes each.

Split into `each blade node $\binom{2}{2} = 1$` and `$45 + 10 = 55$ triplets`.

## 1.4 · Major — slide 45: the five shaded wedges are the largest object on the slide and unnamed

They are the only visual referent for the `5` in `3 × 5`, and the label that used to say so
was dropped when the derivation replaced it. Restore "5 triangles shaded" beside the wedges.

## 1.5 · Major — slide 83's printed ratios do not divide to its printed σ

The figure prints `C 0.50/0.27, L 2.4/2.0, σ = 1.56`; (0.50/0.27)/(2.4/2.0) = **1.543**. σ is
computed from the exact C_rand = 4/15 = 0.2667 but displayed at two decimals. Print C_rand at
three decimals — `C 0.50/0.267` reconciles to 1.5605 → 1.56. This is the slide whose job is
to show the arithmetic settling the question, so a student who does the division must get the
printed answer.

## 1.6 · Major — slides 26 and 28: the red chord is drawn through two labels

50 red pixels inside the "teacher" glyph box and 114 inside "printer" on slide 26; 62 and 114
on slide 28. The stroke cuts the foot of the *t* and the bowl of the *p*. Drop the occupation
labels on these two figures (A–G plus the red annotation already name them), or deepen the
chord until its whole span clears y = 365. Assert that no drawn path intersects a label box —
`assert_text_clear()` already exists for exactly this and is not applied here.

## 1.7 · Major — slide 27: the mean rule is drawn behind the discs it should sit above

L̄ = 1.81 puts the rule inside the d = 2 disc band, so it survives only in the gaps and reads
as decoration threading the row. Slide 25's rule clears its row and reads correctly, so the
convention is set one slide earlier and broken here. Draw the rule in front, or give it a
white casing so it stays continuous across the discs.

## 1.8 · Major — slide 58: the rotated y-axis title collides with the tick labels

"reached" shares pixels with the 1 of $10^{11}$; "people" touches the 1 of $10^2$. Move the
title 25bp further left or cut it — the x-axis title already gives the context — and assert
the title box against every tick-label box.

## 1.9 · Major — slide 89: the axis label sits under the wrong panel

"rewiring probability p" spans x 121–459 while the arrow it names spans 453–1100, so it reads
as a second caption for the lattice panel — and it sits 5px under that panel's own label,
against a body leading of 44px. Centre it under the arrow (x ≈ 775) and assert every
in-figure note's box clears every panel-label box.

## 1.10 · Major — slide 91: one ✗ is planted on the shortcut that is not cut

The solid (uncut) chord's last 26px terminate inside the right ✗ box; red-pixel counts inside
the two boxes are 136 against 42, the difference being the chord it sits on. The existing
assertion only checks the two ✗ marks are 80bp from **each other**, which passes. Offset each
✗ along its own dashed chord until its box clears every other drawn path, and assert that
each ✗ box intersects only the edge it marks.

## 1.11 · Major — slide 30: the worksheet check prints four bare numbers over an unannotated graph

No route is traced, so a student who got d(D,G) = 4 the long way has nothing to compare
against — and slide 28 established the tracing device four slides earlier. Trace each answered
pair's shortest route and put its number at the route.

## 1.12 · Minors (figure side)

1. Slide 40 — see 2.1; the figure is right, the caption is stale. No figure change.
2. Slide 50 — the gray "long way out" is 5 edges, so the drawing quietly answers its own
   "why is anyone 4.74 steps away?". Lengthen the chain to 10–12 hops.
3. Slide 61 — the gray axis tag "path length" sits under the "C. elegans" row and reads as a
   fourth network name. Move both tags below the axis line.
4. Slide 65 — the in-figure label restates the body verbatim. Give it $\bar C = 0.5$ instead.
5. Slide 71 — the GIF loops forever, so the slide never rests on the end state the prose
   describes. Loop once with a long final-frame delay.
6. Slide 86 — the two panels use different node layouts on a slide whose job is a
   side-by-side comparison. Same six positions, only the edges differ.
7. Slide 88 — the figure repeats slide 62's chart with the σ labels removed, so the reprise
   shows strictly less. Put the three domains, or the three sizes, in the drawing.
8. Slide 89 — accent-2 means both "rewired edges" and "the panel to look at". Set all three
   panel labels in ink.
9. Slide 16 — the two visible neighbours are accent blue while every other node is white,
   which inverts the deck's own convention (blue = ordinary node everywhere else). Make them
   white and let the dashed box carry it.

---

# PART 2 — `m02-small-world.md` — DECK AGENT

## 2.1 · Blocker — slide 40's figcaption names a colour that is not on the slide

"red one way round, gold the other" — **zero** gold pixels; both loops are accent-2, and the
generator's docstring says why (gold measures 2.01:1 and was demoted to fills only). Change
to "two closed walks, one arrow each way round".

This is the second stale-colour caption in two rounds. `check_render.py` now fails the build
on any figcaption naming a palette colour the figure does not contain, so it cannot recur.

## 2.2 · Blocker — slide 34 makes three claims

"A triplet is two edges sharing a centre node, **and** it is closed if the third edge exists,
**and** therefore one triangle holds three closed triplets." The third is load-bearing for
the 55 and arrives as an aside. Split into two slides, paired with the figure build in 1.2:
34a the definition (closed/open with the centre ringed), 34b "one triangle, three closed
triplets".

## 2.3 · Blocker — slide 55 introduces two concepts

Expected fraction is p **and** average degree ⟨k⟩ = p(n−1) as a new bolded term. Split: 55a
"the expected fraction is p, whatever the degree", 55b "⟨k⟩ = p(n−1), so C_rand = ⟨k⟩/(n−1)"
— which is also the direct set-up for slide 59.

## 2.4 · Major — slide 74's "two orders of magnitude"

See section 0. Reword to whatever the figure agent's derived band comes out at. Coordinate
before writing the number.

## 2.5 · Major — slide 58's title is its answer

"Four and a half steps" states 4.55 before the figure solves for it. This is the lecturer's
own standard and I missed this slide in the pass of 16. Change to "Solve for the number of
steps" or "Where the fan-out meets eight billion".

## 2.6 · Major — slide 60 defines σ without bars

$\sigma = \frac{C/C_{\mathrm{rand}}}{L/L_{\mathrm{rand}}}$, where the deck uses $\bar C$ and
$\bar L$ everywhere else and has just spent two slides teaching that $C$ and $\bar C$ are
different numbers on the same network. Use the barred symbols, or state in one line which
clustering coefficient goes into σ.

## 2.7 · Major — slide 5's caption overclaims, and its route pre-empts the reveal

The lecturer's map shows a completed 4-hop route; slide 7 then asks "how many people end up in
the chain?" and slide 9 answers "roughly six". A student who counts the arrows gets 4, two
slides before the question. The source is also captioned in his own note as a schematic of the
experiment, not a traced packet.

**Keep his figure** — this is his asset and his call. Change the caption to
"Milgram's experiment: starters in the Midwest, one target near Boston" so slide 5 shows the
setup and the count stays slide 9's reveal.

## 2.8 · Major — slide 67's figcaption contradicts its own body

Body: "0.50 to 0.24 — at sixteen nodes, only a halving." Figcaption: "a quarter of the
closure." 0.24/0.50 is a halving. Change the caption to "short routes, and half the closure".

## 2.9 · Major — slide 23's dashed gray means the opposite of what it means elsewhere

Here it marks a route made of **real** edges ("the route it replaces"); on slide 37 dashed
gray marks edges that **do not exist** ("possibilities, not edges"). Draw A–B and B–C solid
black as on every neighbouring slide and let red alone carry "the minimum".

## 2.10 · Minors (deck side)

1. Slide 9 — "six hands" in the figure vs "six links" in the body vs "seven people" on slide
   21; counting hands on that figure gives 7. Settle on "six links".
2. Slide 13 — restate "red: the new measurement"; red's referent moves between 12 and 13
   without the caption saying so.
3. Slide 19 — the caption claims symmetry the figure never shows. Drop the claim.
4. Slide 23 — shorten the caption to "red: the shorter route" (it currently wraps to an
   orphan).
5. Slide 28 — caption says "the worst pair", the figure says "one of the 4 worst pairs".
6. Slides 37, 45, 59 — a `*` fragment restating a number the figure already prints
   statically. Cut the fragment or strip the number from the figure.
7. Slide 41 — the same formula appears in the body panel and inside the figure.
8. Slide 67 — inline math wraps mid-expression ("⟨k⟩/(n −" / "1)").
9. Slide 70 — the caption wraps to a two-word orphan.
10. Slide 79 — the second bullet introduces harmonic averaging in one line, with no visual,
    never used again. Cut it or move it to the speaker note.
11. Slide 85 — retitle; "Counted together" names nothing that was counted.
12. Slide 87 — "coupled" in gray and "independent" in accent-2, unexplained.
13. Slides 45, 46 — the only two figures in the deck with no figcaption.
14. Slides 63, 83, 86, 88 — straight quotes and apostrophes.

---

# PART 3 — the lead

* `check_render.py` — **done this round**: fails on any figcaption naming a palette colour the
  figure does not contain. This defect shipped twice (slides 23 and 40).
* Re-export `m02-small-world.html` — the checked-in copy is from before the retitles and still
  shows headings the deck no longer has.
* Guides — add section 0's rule: assert a drawn object against the data it summarises, never
  against itself. And `.cols` should centre its text column against the figure column; eight
  slides carry 150–208px of empty wedge that `_class: mid` cannot fix because it centres the
  body block, not the columns.

# Slide review — m04-node-degree.md, slides 069–090 — 2026-08-05 (round 1, reviewer D)

**Verdict:** FAIL
**Slides:** 22 (069–090, all opened; several figures cropped and upscaled to check crossings) ·
**Blockers:** 2 · **Majors:** 8 · **Minors:** 10

**Slide numbering correction to the brief:** `quiz.png` is on **072** (the question); **073** is the answer
slide with `quiz-answer.png`. Question slides are 069, 075, 077, 079, 081, **085**; 086 is the answer.

**Milestones in range (S5):** Part Six end (069–073) — 072 "Which is which? … Vote" plus the `ba-growth.gif`
loop; Part Seven (074–083) — 077 "Open the builder and try"; Part Eight (084–090) — 085 "Hands up for yes."

## Withholding checks — both pass

- **`quiz.png` (072): no leak.** Panels captioned only "A"/"B"; CCDF curves labelled only "A"/"B"; the
  figcaption gives no tell. The generator asserts a banned-string list does not appear. The answer is
  *inferable* from the tail, which is the reasoning the slide wants.
- **Gray notes (069/075/077/079/081/085): no leak.** There is **no `<div class="note">` anywhere in
  069–090**; every note in the range is an HTML comment, i.e. presenter-only, confirmed against the PNGs.
- **S4 holds.** Part Seven is exactly four question→answer pairs, question first: 075→076, 077→078,
  079→080, 081→082(+083).
- **F3 holds.** `check_render.py` exits 0; its 35 warnings are all minus signs and dashes, not glyphs.

## Blockers

1. **076 "'On average' is not 'for you'" — P1 — two unrelated things at once.** Left panel: the eight girls
   sorted 5/2/1. Right panel: a different dataset (Facebook, 721M) on an 80–100 line carrying 83.6% and
   92.7%. The body states both claims — the hub reversal *and* mean-vs-median. **Fix:** split; give
   mean-vs-median its own slide with its own question beat. Also fix the left panel's "5 have fewer", which
   never says fewer *than what*.
2. **073 "Preference is the whole difference" — F1 — the caption's number is not the drawing's.** The
   figcaption reads "largest degree 315 with preference, 29 without" directly beneath a drawing whose
   busiest node has **15** edges: the sketches are the n=24 growth graphs, the CCDF and 315/29 come from
   n=20 000 runs. Slide 071 printed "largest 15 edges" over that same drawing, so the deck states two
   maxima for one picture. **Fix:** state the switch in the caption ("sketches: 24 nodes · tails: 20 000"),
   or drop the sketches here and let the CCDF carry the answer.

## Majors

3. **071 — F1 — accent-2 carries two meanings on one frame.** In the drawing it marks the node that just
   arrived (degree 1); at the right edge, in the same red, sits "largest / 15 edges". The eye reads *that
   little node has 15 edges*. The real hub is plain accent and unmarked. **Fix:** draw the counter in
   annotation gray like the "24 nodes / 45 edges" one, and put an accent-3 ring on the current maximum.
4. **071/072/073 — F2 — 20 crossings in the preferential layout, 21 in the uniform one** (counted from the
   generator's coordinates). Both graphs are non-planar so some are forced, but 20 is far above the
   minimum, and the discs are 29px — the smallest in the deck against 39–40px elsewhere. Slide 072 asks the
   room to tell two hairballs apart. **Fix:** a crossing-minimising pass in `growth_pos` with a crossing
   budget asserted, or drop to ~14 nodes.
5. **072 — F1 — same n=24-vs-n=20 000 conflation as Blocker 2**, without the numeric contradiction: the
   caption says "two networks … and their two tails", which claims the drawn networks are the plotted ones.
6. **080 "Both directions tilt" — F4 — the figure does not show the point.** Two panels of one 6-node
   digraph labelled with in- and out-degrees; nothing compares a node to the nodes at the other end of its
   arrows, which is what "tilt" means. The "8 arrows = 8 in = 8 out" annotation is a different idea the
   slide never uses. **Fix:** print the comparison computed from the drawn graph ("you: 1.3 · the account
   at the other end of an arrow: 2.7") and cut the conservation line.
7. **083 — F1 — the dot plot's axis has no title and `r` is never defined.** Slide 082 names
   **assortativity** in bold but gives no symbol, no number, no range. **Fix:** title the axis
   "assortativity $r$", mark −1/+1, and print the three r values on 082's schematics — computed from the
   graphs as drawn they are **+0.30 / −0.70 / 0.00**, which is the story and is currently invisible.
8. **086 — F4 — "three decades" is not what the picture shows.** The data runs ~5 to 1000 (2.3 decades) and
   the fit window is `ccdf_fit(..., 3, 500)` = 2.2 decades. `verify_numbers.lognormal_degrees`'s docstring
   repeats the same wrong claim. **Fix:** say two decades, or widen the drawn and fitted range.
9. **087 — F4 — title, figure and body each say something different.** The title promises a statistical
   test; the figure is a 1999/2011/2019 chronology; the body is about Ugander's "substantial curvature". No
   test is named. The 2019 dot carries no content, and the punchline (927 networks, strong evidence in ~4%)
   is only in the speaker notes. **Fix:** put "927 networks, fitted properly · strong evidence in 4%" under
   the 2019 dot.
10. **088 — N1 — a result asserted as proved that the course never derived.** The caption says "three
    results we have already proved"; the third branch, "spreading, ⟨k⟩/⟨k²⟩ = 0.045", names no module
    because no module covers the epidemic threshold. **Fix:** mark it forthcoming and change the caption to
    "two results we proved, and one to come".

## Minors

11. **069** — "What **is** real networks doing" — subject-verb disagreement at 40px on the pivot slide.
12. **076** — the number line's axis title renders as "% below their friends'" — a dangling apostrophe that
    reads as clipped text.
13. **077** — "Open the builder and try" names no builder and shows no link; the path is only in the notes.
14. **078** — "Var(k)=0" appears four times on one slide. Print it once, centred under the row.
15. **078 and 082** — three-panel comparisons delivered all at once; each would read better as a build.
    Not a dump (three instances of one point), so not a Major.
16. **087** — L6: ink stops at row 495 of 660, ~130px higher than its neighbours. Take `mid`, or fill it
    with the 2019 content from Major 9.
17. **088** — F1: `f_c = 0.95` and `⟨k⟩/⟨k²⟩ = 0.045` name no network. They are cond-mat, last seen 32
    slides earlier. Add it to the figcaption.
18. **089** — F1 across slides: the recap draws the eight girls as **5 red + 3 gray**, where 076 drew them
    5 red / 2 blue / 1 gray with gray meaning *equal* — so a student reads three ties. Red also changes
    meaning inside the one figure ("below" in panel 1, "the gap" in panel 2).
19. **089** — P3/L6: the only figure slide in the range with no takeaway line; ink stops at row 487 of 660.
    The module's summary is the thinnest slide of the part, and it silently drops all of Part Seven.
20. **089** — the figcaption says "one distribution" while the panel says "one tail".

## Clean on the render — do not re-check

070 (three growth steps, crossing-free, counts 4→5→6, two red edges per arrival); 078 (all three panels
planar as drawn, including the ring lattice); 080 (both digraph panels crossing-free, degree labellings
correct against the eight arrows); 082 (all three wirings crossing-free and all three carry the degree
sequence 4,4,3,3,2,2,1,1 exactly as the in-figure line claims — so the F1 concern flagged in the brief does
not fire); 090 (two 6-node clumps and a bridge, crossing-free).

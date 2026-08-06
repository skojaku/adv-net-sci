# Slide review — m04-node-degree.md, slides 024–046 — 2026-08-05 (round 1, reviewer B)

**Verdict:** FAIL
**Slides:** 23 reviewed (024–046, all opened — none skipped) · **Blockers:** 2 · **Majors:** 8 · **Minors:** 7

**Milestones in range** (S5)
- Part Two (ends at 024) — demo: yes, slide 019 "Try to build this" (two-minute construction task).
- Part Three, 025–036 — demo: yes, slides 035/036, the star-and-ring worksheet, predict-before-you-count.
- Part Four, 037–045 — demo: yes, `vaccination-game.html` in slide 045's speaker note — but run from a
  slide that already prints both outcomes (Major 3).

Corrections to the brief, from the render: the star-and-ring worksheet is slide **035**, its answer **036**;
and `rosters.png` draws **no** horizontal rules — the table reading comes from the column grid alone.
`check_render.py` exits 0 on this render (node discs 27–42px over 361 discs), so systematic in-figure type
size is not a finding in this range; the size findings below are things the gate does not measure.

## Blockers

1. **024 "Hubs are on everybody's list" — L2 — `rosters.png` is a grid of text.** A header row of eight
   names, a row of eight degree discs, then eight equal-width top-aligned columns of friend names: 24 cells
   on a shared baseline grid. No rules, but a room reads a header row over aligned columns as a table, and
   here the alignment is actively misleading — the third line of Sue's column ("Dale") has nothing to do
   with the third line of Alice's ("Pam"), so every horizontal read is noise. **Fix:** destroy the grid,
   keep the mark-up. Either (a) eight left-aligned ragged-right lines — "Betty: Sue", "Sue: Alice, Betty,
   Dale, Pam" — which read as eight sentences; or (b) reveal one roster at a time as a build, which is what
   L2 prescribes in place of a table. Keep accent-2 on the recurring hub names either way.

2. **040 "Seven hundred million people" — P1 — two points on one slide.** `fb-twitter.png` renders three
   labelled bars: Facebook mean 92.7%, Facebook median 83.6%, Twitter >98%. The body states only 92.7% and
   >98%; the word *median* appears nowhere on the slide, and the mean-vs-median distinction is not
   introduced until slide 076, 36 slides later. **Fix:** cut the median bar. Slide 076 already owns that
   point and carries both numbers.

## Majors

1. **045 "Try it" — F3/accuracy — figure and body disagree.** The curve label reads "random **87%**"; the
   body reads "At random, **88%**". **Fix:** compute label and prose from one value.
2. **045 — F1 + N1 — the y-axis is unnamed and secretly logarithmic.** Ticks 100/10/1/0.1% at even
   spacing, no axis title, nothing saying the scale is log — five slides before Part Five's whole argument
   that an unannounced change of ruler misleads you. **Fix:** title the axis ("largest component
   remaining") and mark the log scale, or go linear.
3. **045 — N4 / S5 — the milestone demo runs on top of its own answer.** The note says to let two students
   play before showing the curves; the slide already prints 88% and 2% and both labelled curves.
   **Fix:** split into a prompt slide and a reveal.
4. **029/030/031 — F4/P3 — every new line is printed twice.** Each slide adds one line inside the panel and
   repeats that identical equation underneath as large KaTeX, with the figcaption stating it a third time in
   words. **Fix:** delete the KaTeX line beneath the figure on all three; keep the panel's reserved height so
   the figure does not jump. The build itself is sound.
5. **029 "The average friend" — N1 — `⟨k²⟩` arrives undefined.** The panel jumps from `Σ k q(k)` to
   `⟨k²⟩/⟨k⟩`; the substitution `Σ k·k p(k)/⟨k⟩` is not shown and the second-moment notation has not
   appeared before. **Fix:** two lines — substitute, then name the numerator.
6. **028 "A hub has more hands in the bag" — F4 — the figure redraws the previous slide.** `qk-formula.png`
   is 20 tallies with 4 in accent-2; slide 027's `bag-of-hands.png` is 20 discs with 4 in accent-2. Same
   count, same colour, different glyph — while the new content (proportionality) has no visual. **Fix:**
   draw all eight girls' hand-counts side by side so the draw probability visibly rises with k.
7. **044 "Ask them to name a friend" — F4 — a three-panel strip shown at once.** Three near-identical
   five-node graphs; the reader has to diff them. **Fix:** three consecutive slides, one step each.
8. **042 "Everything tilts" — F3 — the marks that carry the point are 13px** on a figure whose node discs
   are 40px. The arithmetic (1/7 vs 6/18 = 2.3×) is right. `check_render.py` does not catch these — they
   fall below its disc threshold. **Fix:** draw the tally dots at 26–40px, wrapping onto two rows.
9. **040 — F4 — it is a bar chart and the bars encode nothing.** Three nearly-full bars on a common 0–100
   scale; everything comes from the printed numbers. **Fix:** two dot-strips of 100 people with 93 and 98
   marked, or the slide-039 treatment.

## Minors

1. **039 — F5/accuracy — 82.8% in the figure against "nearly 83%" in the body**; also 8.1/22.1 against
   "eight … twenty-two" in the caption. Pick one form per number.
2. **028 and 032 — L6 — shallow slides hanging from the rule** (ink ends at y=416 and y=478 of 720).
   Take `<!-- _class: mid -->`.
3. **024 — F4 — half the caption cannot be checked.** "Betty and Tina on one" — those two occurrences sit
   in the same annotation gray as the other 14 names. Mark them, or cut the clause.
4. **027 — F1/F5 — unexplained initials, and a colour that changed meaning.** Discs lettered B/S/A/J/P/D/C/T
   with nothing saying they are initials; accent-2 meant "the two hubs" on 024 and means "Sue only" here.
5. **034 — F5 — the same object at half size.** The edge-end glyph is 4×39px here, 8×63px on 028.
6. **044 — F1/F3 — two disc conventions, neither stated** (ring = picked, fill = immunised), at 28px where
   the range's other graphs draw 40px.
7. **040 — F4 — the title's number is nowhere on the slide.** 721 million lives only in the speaker note.

## Checks that passed — do not re-run

- **N4 on every question slide in range** (026, 035, 038, 041, 043): no answer in body, figure or gray note.
  `worksheet-star-ring.png` carries blank rules and no gap value — the degrees are not even printed.
- **Arithmetic on every figure checkable**: 033 (7.5 / 1.25 / 2.5+0.5=3.0 against 20 ends, 60 friends),
  034 (2.9896 → 2.99), 035/036 (star 0.5, ring 0), 042 (2.33×), 027 (20 discs, right multiplicity). Correct.
- **F2**: no edge crossings in 035, 036, 042, 044.
- **F5 accent-3**: gold appears nowhere in this range.
- **L1, L3, L4, L5**: no two-text-column slides, no code, no bullet lists at all.
- **Contrast**: every gray sampled is exactly #6b6b6b, 5.33:1 on white.

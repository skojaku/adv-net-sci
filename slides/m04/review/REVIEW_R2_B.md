# Slide review — m04-node-degree.md, slides 025–048 — round 2, reviewer B

**Verdict:** FAIL · **Slides:** 24 (all opened) · **Blockers:** 1 · **Majors:** 7 · **Minors:** 8

## Round 1 items — what landed

Confirmed on the render: KaTeX gone from the derivation build, and states 1 and 2 are **byte-identical**
to state 3 above the added line (0 differing pixels); acquaintance is three slides with 40px discs and both
marks labelled; the vaccination demo is split into prompt (046) and reveal (047), and the prompt leaks
nothing; 87% agrees between figure and body; `coauthor-gap` agrees at 82.8% and its bar measures 0.827;
`qk-formula` redrawn as the eight girls' hand-counts, and the edge-end glyph is 6×33px on both 027 and 033
(the 8×63 / 4×39 mismatch is gone); `mid` on 027 and 031; no gold anywhere; every red exactly #B14434.

**Did not land: three of the six.** See Blocker 1 and Majors 1–3.

## Blockers

1. **039 "Seven hundred million people" — P1 + F4 — `fb-twitter.png` is untouched.** Still three bars
   measuring 0.925 / 0.834 / 0.978 of their boxes, still carrying the **median** 43 slides before the deck
   introduces it, still leaving 721 million in the speaker note. R1 Blocker A-2 verbatim.

## Majors

1. **028 — N1 + P1 — ⟨k²⟩ still arrives undefined.** Line 1 still reads `= Σ k q(k) = ⟨k²⟩/⟨k⟩`; the
   substitution is not shown and ⟨k²⟩ appears nowhere earlier in the deck. R1 A-14/D-5, unfixed.
   **Fix:** four states, not three; grow the frame rather than tightening the leading.
2. **047 — F1 + N1 — the y-axis fix went to the other axis.** y ticks 100/10/1/0.1% at even spacing, no
   title, no scale marker; what is new is an **x** title, "fraction immunised". This is the error moving
   one slide-position over instead of landing — one slide before Part Five, whose argument is that an
   unannounced change of ruler misleads you.
3. **041 — F3 — `sampling-bias.png`'s countable people are still 13px**, in the same figure as 39–40px
   node discs. R1 A-8, which the fix spec's adjudication named specifically as in scope.
4. **045 — F1 + F4 — the fix introduced a new defect.** The "picked" ring vanishes on state 3 and an
   identical ring reappears on the hub labelled "immunised", so the slide titled "not the volunteer" no
   longer shows the volunteer, and one glyph means two things across a three-slide build.
5. **041 — F1 — one dot's unit is never stated** and the 1-of-7 / 6-of-18 behind "2.3×" are not printed,
   so the claim can only be checked by counting 25 marks at 13px.
6. **025, 037, 040, 042 — N4 — four more question slides pose and stop**, beats only in the speaker notes.
   D-10 was applied by slide list rather than by criterion.
7. **047 — P2 — the payoff slide is dense and static**: figure, caption, setup, two-number answer and a
   gray note all at once. The deck has six `*` markers in 96 slides and none in this range.

## Minors

1. **026** — the legend explains three initials of eight.
2. **026 → 033** — a 40px blue disc is an *edge end* on 026 and a *person* on 033.
3. **027** — the caption names Sue, but all twenty tallies are the same colour.
4. **030** — the figcaption restates the boxed equation in words, above a black body line that wins the eye.
5. **032** — the same three numbers in the figure, the caption and the body, within 130px.
6. **035** — caption restates the figure's own printed values.
7. **038** — still a `strip()` bar; if 039's bars go, this should move with them.
8. **043–045** — a pure star makes nomination look infallible: every nomination lands on the hub with
   probability 1, so "usually, not always" cannot be shown. Give two leaves an edge to each other.

## Passed — do not re-run

N4 on 025, 034, 037, 040, 042, 046 (no answer in body, figure or note; the worksheet draws blank discs and
blank rules). The derivation build is monotone and pixel-identical above each added line. F2 clean on 034,
035, 041, 043, 044, 045. Arithmetic correct on 026, 027, 032, 035, 038, 039, 041. Palette clean. Discs
39–40px throughout. L1–L4 clean. L6: 027 and 031 centred.

**Note for the figure agent:** on 045 the accent-2 ring and accent-2 fill merge into one 58×58px blob.
`check_render` passes today, but if `NODE_FILLS` ever gains accent-2 that slide fails the 26–52px band.

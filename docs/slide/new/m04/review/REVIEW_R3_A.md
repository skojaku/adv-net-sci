# Slide review — m04-node-degree.md, slides 001–033 — round 3, reviewer A

**Verdict:** FAIL · **Slides:** 33 (all opened) · **Blockers: 1** · **Majors: 7** · **Minors: 11**

S1 ✓ (Coleman 1961, Feld 1991, Marketville, eight named girls — the word *degree* does not appear
until 014). S2 ✓. S3 ✓. Milestones present in all three parts in range.

## Blocker

1. **023 — F1 — two unexplained colours, and they are the exact inverse of the same two on 010.**
   Every "Sue"/"Alice" in `rosters.png` is accent-2 and every "Betty"/"Tina" is accent, with
   **nothing on the slide saying what either means**. Thirteen slides earlier 010 states "Red: she
   has fewer friends than her friends average. Blue: more" — and there Sue and Alice are *blue*.
   So the four girls a student can track carry the opposite colour. 026 keeps 023's polarity and
   014 makes the accent-2 disc the highest-degree node. **This is R1 Major 2 with the sign
   flipped**: the 010↔012 conflict was removed and the same conflict reappeared at 010↔014/023/026.
   **Fix:** one meaning deck-wide — cheapest is "accent-2 = the node we are counting, or the hub",
   which 014/023/026/027 already use — recolour 010, and print the key on 023 the way 010 does.

## Majors

1. **016 — F4 — five edges draw both their end-ticks as an adjacent pair at the edge's midpoint.**
   The five long edges carry ticks at 20–30% and 70–85%; Sue–Pam, Pam–Alice, Sue–Dale, Dale–Alice
   and Alice–Jane are each 150px long and carry theirs at 44% and 56% — **18px apart, a "⫽"
   dead centre**, which is the standard geometry mark for *equal lengths*, not for ends. Around Sue
   the eye counts six marks, not four. The generator places each tick a fixed ~66px from its node,
   which separates on a 194–292px edge and collides on a 150px one. **The 20-component assertion
   cannot see where any component is.** Fix: place ticks at a fixed *fraction* of each edge and
   assert the two are ≥40% of its length apart.
2. **011 — N1 — "Their friends average 3.0" is not the number the room just produced.** 009 has
   eight students each compute one girl's friends' mean; 010 prints their eight answers; those
   average **2.99**. The deck says so itself on 034 and `verify_numbers.py` asserts 2.9896. 033
   then says "counting the sixty friends of the twenty friends by hand gave exactly the same" — a
   hand count nobody performed. The person/edge distinction that reconciles them arrives on 034.
3. **011 — N4 — the third bullet answers 022's question eleven slides early, with a reason that
   does not produce the effect.** "every one of those ten friendships was counted twice, once from
   each end" — double counting is symmetric and is not the mechanism: a ring counts every
   friendship twice and has a gap of exactly zero, which 032 asserts and 035's ring demonstrates.
   022 then asks "where does the extra friend come from?" and 023 supplies the real answer.
4. **028–031 — F3 — the subscript "friend" measures 12px x-height against the 15px floor**, and it
   is the only mark separating ⟨k⟩_friend from ⟨k⟩ — lose it and lines 1, 2 and 4 all read
   "⟨k⟩ = …", which is the whole derivation. `check_render` reports 11px and downgrades it to a
   warning; it is a glyph, not a dash. Assert the *rendered* x-height of the subscript.
5. **027 — F4 — the figure shows a per-girl probability while the boxed formula is a per-degree
   one.** The tally reads 4/20 = 0.2 for a degree-4 girl; q(4) = 4·(2/8)/2.5 = **0.4**, because two
   girls sit at degree 4. The body says "the chance of drawing **her**", and q(k) is not her chance
   — it is the chance the girl you draw has degree k. The figure already pairs the two girls at
   each degree, so it is one bracket away from correct.
6. **016 → 018 — N4 — the answer to the two-minute challenge is in a slide title two slides
   before it is posed.** 016's title is "Twenty, and **never odd**"; 018 asks the room to build a
   network with exactly three odd-degree nodes. 016's body never demonstrates parity, so the title
   is pure spoiler.
7. **026 — F1 — the figure draws edge *ends* with the 40px lettered disc that has meant a *person*
   on every slide since 006**, on the slide whose single point is "you do not pick a person — you
   pick one end of one edge". The deck's own end-glyph (the red tick) does this job on 016, 017 and
   027. R2 filed it as a Minor; it is the slide's whole point.

## Minors

1. **026** — legend explains three initials of eight. 2. **027** — caption names Sue; nothing marks
her. 3. **031** — caption puts the boxed equation into words beneath it, with the only new
information below the caption where it wins the eye; inserting the fourth state moved R2's finding
down a slide rather than removing it (030 now has no body line at all). 4. **033** — the same three
numbers in figure, caption and body within 130px. 5. **017** — "2.5" is red here and on 008 but blue
on 011, where colour *is* the encoding; R1's fix made 011 internally consistent and left the
disagreement between slides. 6. **012** — "every girl in the survey" should be "in that school";
the survey is twelve schools and 146 is one school's girls with a mutual friend. 7. **006** — the
figcaption says nothing about what is drawn; the figure's key is in the body above it. 8. **019** —
"Odd degrees pair off" does not describe what the figure pairs (it pairs *ends*), and the sentence
then contradicts its own first clause. 9. **021** — the same fact three times. 10. **014** — the
four edge numbers run 2, 1, 3, 4 clockwise. 11. **030** — the only derivation slide with no prose,
and the one introducing Var(k).

## Clean — do not re-run

Arithmetic measured off the pixels: 012 (80/41/25 = 146), 016 (20 ticks), 017 (20 ticks, 8 discs),
019 (5 ticks), 026 (20 discs, 8 accent-2, letter counts correct), 027 (20 ticks as 1,1,2,2,3,3,4,4),
010 (all eight friends'-means correct, 5 red / 2 blue / 1 gray), 023 (Pam's list matches Feld's
Table 1, not the widely-copied wrong version), 033. The derivation build is monotone and
pixel-identical above each added line. Palette exact; no green, no accent-3 in range. F2: zero
crossings on 006, 008, 009, 010, 016; 014's star has no collinear pair. N4 clean on 002, 007, 015,
018, 022, 025. L1/L2/L3/L5, N2/N3 clean.

**Landed and confirmed:** R1 M1 (fragments now on five slides where the range had none), M2 (010↔012
polarity), M3, M4, M6, M7, M8, M9, m6; R2 M1 (four derivation states).

## The reviewer's own closing note, worth keeping

Both gates added since round 2 did their job and both have the same blind spot: **the collision
gate sees overlap but not placement** (016's ticks are 18px apart — legal and wrong), and
`sum-ends.png`'s ink assertion counts 20 components without checking where any of them sits.
Assert the *position* against the data, not just the count.

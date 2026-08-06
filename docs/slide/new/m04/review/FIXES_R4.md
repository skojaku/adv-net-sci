# m04 round 4 — fix spec

    round 1   6 Blockers   38 Majors   34 Minors
    round 2   5            33          36
    round 3   3            20          39
    round 4   3            11          26

Majors have halved again. `check_render.py` exits 0 throughout.

## Read this before your section

**All three of round 4's Blockers were made by round 3's fixes, and all three trace to how I wrote
the spec rather than to how anyone applied it.**

- I ruled "accent-2 = the node we are counting, or the hub" and asked for one figure to be
  recoloured. The sibling function twelve lines below it was not touched, so accent-2 now means
  *above her friends' average* on slide 010 and *below* on slide 012 — on the slide built to
  confirm the result at eighteen times the scale. Third address in three rounds. **I should have
  asked for a declaration, not a recolour.**
- I asked for the exponent reconciliation and **named slide 062**. 062 is two slides before the
  poll that asks the room whether the CCDF slope is γ, and three before the derivation of the +1
  rule. The note leaks both.
- I asked for a "neutral fill" on the quiz question sketches. The neutral fill chosen was ink,
  which is the edge colour, so every disc within 10px of a neighbour fused with its edge into one
  black mass — on the slide that asks the room to compare two structures.

Three rounds have now produced three versions of one lesson, each a level up from the last:

1. R3 — **the gates see quantity, not position.** Fixed; the position assertions hold.
2. R4a — **the gates see one figure, not two.** A role written into one function's comment binds
   nothing.
3. R4b — **an assertion that fits data you constructed measures your construction, not your
   drawing.** `fig_slope_derivation`'s new guard fits two arrays built one apart and asserts they
   differ by one. The defect is that the two panels are *drawn* at 0.4099 and 0.3915 — a 4.5%
   difference where the claim is 2.5 against 1.5 — because they use different y ranges in
   identical boxes, and the ruler change cancels the slope change.

So the standing instruction for this round: **declare shared meanings once per file and assert
them; and assert on the rendered drawing, not on the arrays that fed it.**

---

## A. `figures/figs_story.py`

**A4-1 · BLOCKER · accent-2 means "above her friends' average" on 010 and "below" on 012.** 010 has
zero accent pixels: Sue and Alice are the only filled discs, in accent-2, under "**Red**: she has
more friends than her friends average". 012 draws 80 discs in accent-2 under "**80 below**" and 41
in accent under "41 above" — and 012's block is the largest single piece of ink in Part One. Read
with 010's key, slide 012 says eighty girls are ahead, which inverts the module's thesis on the
slide built to prove it. `fig_feld_friendmeans` was recoloured under the A3-1 ruling;
`fig_marketville_146`, twelve lines below, still hardcodes
`(MARKETVILLE_BELOW, "accenttwo"), (MARKETVILLE_ABOVE, "accent")`.

**Fix — and do this part first, because it is the fix:** declare the roles at module level in
`figs_story.py`, the way `figs_tail.py` declares `HUBS`/`NO_HUBS`:

    ABOVE_FRIENDS = ACCENT2      # she has more friends than her friends average
    BELOW_FRIENDS = ...          # hollow, or annotation gray
    EQUAL_FRIENDS = GRAY

Use them in **both** functions and assert. Then swap 012 to match 010: **41 above in accent-2, 80
below hollow or gray, 25 equal in the third state.** The labels are drawn in the matching colour,
so they relabel themselves. Accent also needs a decision: it is the per-girl average on 011, "41
above" on 012, and "on one list" on 023 — three meanings in fourteen slides.

**A4-2 · MAJOR · 010's title counts the group the figure does not mark.** Five hollow (below), two
accent-2 (above), one gray (Carol). "Five of eight" names the unmarked remainder while the body
spends its first clause on the two. Retitle to what the colour marks, or state the third state —
the body names Carol and never says gray means equal. *(Coordinate with the deck agent, D4-2.)*

**A4-3 · MAJOR · the derivation frame's right border is drawn through the last letter of "name the
numerator"** on 029, 030 and 031. Annotation ink runs to x = 1151; the border sits at 1139–1140.
Present in the source PNG too (border 4164, ink 4209 — 45bp over). **The collision gate does not
see it: a frame rectangle is not in its blocker set.** Widen the frame or shorten to "name it", and
tell figs-tail to add emitted frame rectangles to the gate's blockers (same shape as R3's fill
finding).

**A4-4 · MAJOR · the deck body colours 2.5 accent while the figure on the same slide prints it
black.** `fig_feld_two_numbers`'s own comment states the rule — only the number the slide is about
is coloured — and the deck still carries `<span class="accent">2.5</span>`. The figure half landed;
the deck half did not, and the two halves disagree inside one slide. *(Deck side is D4-3; yours is
to keep the figure as it is.)*

**A4-5 · MAJOR · `binning` panels fit a different window from `pdf_fit`.** 054 prints slope −2.44
and 058 prints −2.25 for the identical 122 points on identical axes; the y quantity differs only by
a constant factor, which cannot change a slope. `_fig_binning_panel` fits every bin including
k = 1 and 2, where the distribution turns over; `pdf_fit` excludes them. It also confounds the
build's claim: at w = 32 the first bin centre is k = 16.5, so part of the −2.25 → −3.80 movement is
the change of fitted range, not of bin width. **Fix:** fit all three panels over
`PDF_KMIN..PDF_KMAX`. The w = 1 panel then prints −2.44 and the remaining spread is bin width
alone. *(This figure is in `figs_tail.py` — B4-4. Listed here because 054 is yours.)*

**A4-6 · MINOR · `immunization-curves`' curve label reads "named 2%"** where the deck says
*nominated* in its title, body and figcaption. Carried from round 3.

**A4-7 · MINOR · the `binning` build drops the "one bin / width 1" caliper** that 056 introduces,
on the *first* panel of the build about bin width — same class as the arrow that vanished from
`acquaintance-3`. *(Also `figs_tail.py`.)*

**A4-8 · MINOR · 052's leader stops 52px short of the data it points into** (rule ends y = 335,
dots at y ≈ 387), so the arrowhead ends in blank gold.

**A4-9 · MINOR ·** 035 → 036 still jumps 66px between question and answer, and 036 prints "= 0.5"
beside the label rather than on the rule the question drew for it. **A4-10 · MINOR ·** 026 has
nothing on the slide decoding B/S/A/J/P/D/C/T — round 3's three-of-eight legend was deleted rather
than completed. **A4-11 · MINOR ·** captions restating the drawing on 005, 014, 020, 026, 027, 032,
033 — Parts Two and Three never got the criterion that was run over Parts Four to Eight.
**A4-12 · MINOR ·** 028 is now the only derivation slide with no body prose. **A4-13 · MINOR ·**
011's fragments are defeated by its own figure: the right column shows 2.5 and 3.0 from the first
beat, so bullet 2's numbers are on screen before bullet 2.

---

## B. `figures/figs_tail.py` (owns `figlib.py`)

**B4-1 · BLOCKER · `slope-derivation` (065) draws the two slopes at the same steepness.** Measured
on the render by column-mean fit: left **0.4099**, right **0.3915** — 4.5% apart, where the claim
is γ = 2.5 against γ − 1 = 1.5. The left panel spends 6 decades and the right 4 in boxes of
identical height (`y 140→258`), because each was sized to end its line one decade above its own
floor. **The ruler change cancels the slope change**, on the answer slide to a poll whose own note
calls this "the single most common error in this material". The picture shows the error.

The new assertion cannot see it — it fits `xs ** -g` against `xs ** -(g-1)` and asserts they differ
by one, which is arithmetic on arrays you constructed. **Fix:** identical boxes and identical
`ylim` for both panels (`1e-6, 1` works; the CCDF then ends three decades above the floor, and that
white space *is* the shallower slope). Drawn angles become 0.410 and 0.246. Then **assert the
drawing**: compute each panel's bp-per-decade on both axes, derive the two on-canvas slopes, and
assert their ratio is γ/(γ−1).

**B4-2 · BLOCKER · the reconciliation note is on the wrong slide.** `ccdf-condmat` (062) carries,
in accent-2 at the top, "fitted slope −2.29 over 3 ≤ k ≤ 279, not −2.44 + 1". 062's point is that
the CCDF has no bin width to choose (title, caption, and the whole 056–061 build), so this is a
second and harder claim on a slide that had one. Worse: **064 asks the room whether the CCDF slope
is the same exponent as p(k)'s, hands up for yes and no — and 062 has already answered it and shown
them the +1 rule that 065 exists to derive.** And the honesty ask is half-met: I asked for "because
the tail is not a clean power law" and the render says only "not −2.44 + 1", so a student is shown
a contradiction and given nothing to do with it. **My spec named the wrong slide.** **Fix:** strip
the note from 062 back to the plain fitted slope or nothing, and put the full statement — measured
slope, the +1 prediction, and the sentence about the tail — on **067 or in Part Eight**, after 065
has derived the rule and 067 has said what one unit of γ costs.

**B4-3 · MAJOR · B3-3 equalised the y ruler and the x ruler is the one that sets apparent slope.**
One decade of P(k′>k) now measures 37.5 / 37.75 / 37.5 / 34.5px across 070, 071, 073, 074 — good.
One decade of *k* measures **264.5 / 264.5 / 545.0 / 323.5px**, so the log-log aspect runs 0.142 /
0.143 / 0.069 / 0.107, a factor of 2.1. A slope of −1 draws at 8.1° on 071, 3.9° on 073, 6.1° on
074. **The same random graph appears on 073 and 074** and its cliff reads as a gentle roll-off on
one and a wall on the other. **Fix:** fix px-per-decade on *both* axes and let the frame **width**
vary with the data range (`x1 = x0 + decades * PX_PER_DECADE`), so a short x range gives a narrow
panel rather than a stretched ruler. Route 074 through `CCDF_BOX` — it still hand-rolls
`Axes((185,145,1058,318))`.

**B4-4 · MAJOR · the three binning panels fit a different window from `pdf_fit`** — see A4-5. Fit
over `PDF_KMIN..PDF_KMAX`.

**B4-5 · MAJOR · 059's body says each bucket holds eight times as many and the axis says
per-unit-of-k**, where the leftmost point measures y = 229.5 on 058 and 231.4 on 059 — unchanged.
The division by bin width is never stated on 056, 058, 059 or 060; it did not need to be at w = 1,
which is why nobody noticed it had to be said by 059. **Fix (figure side):** state the
normalisation in the drawing. *(Deck side is D4-5.)*

**B4-6 · MAJOR · `three-ccdfs` (074) — the lattice is still black chart furniture.** B3-4 asked for
gray or accent-3, at the other curves' weight, ending open, with the label outside the step. Only
the weight landed: the stroke is 4px against 2px axes, it runs along P = 1 to k = 8 and drops to
y ≈ 336, leaving a 25px gap at one corner of a rectangle whose other three sides are the black
axes — with the black word "lattice" inside it. It reads as an inset panel with a title.
**Fix:** annotation gray (**not** accent-3 — the guide bans gold for strokes), and move the label
right of the step.

**B4-7 · MAJOR · `hubs-share` (070) — the headline number has neither a picture nor a sentence.**
The figure's top line is "65 routers hold 33.8% of all 25,144 edge ends" and the drawing shows only
how few the hubs are. B3-9 offered two exits and the generator's comment chose "the deck body
carries the sentence" — and 070's body never received it. **Fix:** the shaded rectangle is ~100px
tall and empty below the curve; draw the split rule *inside it*, 33.8% of its width in a darker
accent-3. Or tell the deck agent to carry the share in the body and let the headline read "65
routers: the top 1%".

**B4-8 · Add emitted frame rectangles to the collision gate's blocker set** (see A4-3). A frame
border currently draws through annotation text on three consecutive slides and the gate is blind
to it. Same shape as R3's fill finding, which you closed with a ray-cast region test.

**B4-9 · MINOR ·** 063's two panels still have different x rulers (139.7 vs 121.1 px/decade over
the same k = 1…300) — the y halves matched, which is the half B3-8 named. **B4-10 · MINOR ·** 071's
"physicists" label sits 43px above where two curves cross, the next curve 54px away and the two of
them 11px apart; with all three curves one colour and told apart by dash pattern, proximity cannot
resolve it, and the solver's `margin=1.6` passes on its own metric. **B4-11 · MINOR ·** 048's
random curve reads as a flat line at 100% on a log y (87% is 3.6px below), so the figure overstates
its own bullet. **B4-12 · MINOR ·** 052's caliper/leader, A4-7's dropped caliper, and A4-6's
"named" label are all in your file if `figs_story` does not own them — check before editing.

---

## C. `figures/figs_edge.py`

**C4-1 · MAJOR · 078's neutral fill is the edge colour.** The B3-1 exemption drew both quiz
sketches in ink, and the edges are ink, so a disc and its edge are one shape: sampling straight
between two disc centres 46px apart returns `(0,0,0)` at every point but one. Panel A is a single
connected black component of 38,549px; panel B one of 36,413px. Nine disc pairs sit under 10px
apart and every one carrying an edge fuses. On the one slide asking the room to compare two
structures, neither structure can be traced. **Fix:** keep the exemption, draw the sketches in
**annotation gray** — still one neutral fill, still no hub/no-hub key, and the disc–edge boundary
returns.

**C4-2 · MAJOR · the two round-3 fixes moved 46 discs out of the node-size gate.**
`check_render.NODE_FILLS` is `[accent, accent-2]`, so `node_discs()` returns **0** on 078 and 6 of
24 on 089 — including the 28 discs whose clearance was round 3's Blocker. The green "394 discs,
27–40px" run does not cover either figure. Drawing 078 in gray (C4-1) and **adding `#6b6b6b` to
`NODE_FILLS`** puts both back under the gate. Pure black cannot be added: the edges are black.
*(`check_render.py` is mine; I will make that change once you confirm the gray.)*

**C4-3 · MAJOR · `lognormal-trap` (093) hand-rolls its axes** — y titled "CCDF", ticks
1/10⁻¹/10⁻²/10⁻³ at 65px per decade, x at 371.5px per decade — where every other CCDF in the deck
is titled P(k′>k), ticks 1/10⁻²/10⁻⁴, 37.5px per decade. `figs_edge.py` never imports
`CCDF_BOX`/`CCDF_YLIM`/`CCDF_YTICKS`. This is C3-1's file-boundary failure again, same file,
different constants. **Import them.**

**C4-4 · MAJOR · 077's accent-3 ring is not in the clearance solve.** The layout holds discs to
10.6bp; the ring is added afterwards with `grow=13` and clears the nearest disc by **5.7bp**,
visible on the render as a near-touch above-right of the hub. Same shape as B3-2 — a property
asserted on something other than what is drawn. Include the ring radius in `clearance_bad`, or drop
`grow` to ~6.

**C4-5 · MINOR ·** 079's "315" and "29" sit at x-positions that read as k ≈ 138 and k ≈ 10, and
neither is glossed (073 spells out "largest degree 28"). A short leader to each curve's last point,
or write "largest 315". **C4-6 · MINOR ·** 082 still does not name Sue and Alice in the drawing.
**C4-7 · MINOR ·** 094's timeline is drawn as a metric axis and is not one: dots at 180/520/850 for
intervals of 12 and 8 years, so the same length is 55% more time on the left. **C4-8 · MINOR ·**
096's "one tail" panel is the only one of five with no gray gloss. **C4-9 · MINOR ·** captions
restating the drawing on 089, 090, 095.

**C4-10 · noted, not filed ·** panel B of the quiz is the same graph 077 animates — same 14 nodes,
25 edges, degree-10 hub — so a student who counts can match "B has a hub" to the GIF. The reviewer
judged this weak, since "B has a hub, preference makes hubs" is the reasoning the slide wants. If
we want it closed, draw panel B from a different seed and assert its maximum degree differs from
the GIF's. **Your call; tell me which way you went.**

---

## D. `m04-node-degree.md`

**D4-1 · MAJOR · 023 is dense and static, and its second text block is the answer to 022.** "When
you average over *friends*, you are averaging over the lists — and a popular girl is on many lists"
is the mechanism 022 asked the room to guess, landing in the same instant as the evidence it is
drawn from. **Fix:** make it a `*` fragment.

**D4-2 · MAJOR · 010's title names the unmarked group** (see A4-2). Coordinate with figs-story on
which group the colour marks after A4-1, then retitle.

**D4-3 · MAJOR · drop `<span class="accent">2.5</span>` on 011.** The figure prints 2.5 in black by
deliberate decision — its comment says only the number the slide is about is coloured — and the
deck's span contradicts it inside one slide.

**D4-4 · MAJOR · 055 is dense and static and Part Five has no fragments at all.** Title, formula
box, two paragraphs, a two-curve figure. Make "γ is the one number that says how fast hubs become
rare." a `*` fragment.

**D4-5 · MAJOR · 059's sentence promises 8× and the figure shows 1×.** With the figure now
normalised per unit of k, "each holds eight times as many" is false as drawn. **Fix:** say the
division — "each bucket holds eight times as many, so we divide by the width and the heights stay
comparable" — which makes the normalisation the slide's content instead of a silent step.

**D4-6 · MINOR · 093's body rounds the figure's own number down** — the drawing prints "R² = 0.99
across 2.3 decades" and the body says "over two decades", on the slide whose point is that the
length of the straight stretch is what fools you. Say 2.3.

**D4-7 · MINOR ·** captions restating the drawing on 005, 014, 020, 026, 027, 032, 033, 089, 090,
095 — Parts Two and Three never got the criterion. **D4-8 · MINOR ·** 040's body restates the
figure verbatim and Twitter's 98% is still text-only, never drawn. **D4-9 · MINOR ·** 039's and
048's bodies restate numbers their figures print. **D4-10 · MINOR ·** 033's body restates every
number its figure prints, ~90px below them.

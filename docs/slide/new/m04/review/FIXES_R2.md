# m04 round 2 — fix spec

Four reviewers, disjoint ranges, all four returned. **5 Blockers · 33 Majors · 36 Minors. FAIL.**
`check_render.py` exits 0 throughout; everything here is invisible to the gate.

The severity class fell, which is what should happen: round 1's Blockers were a table, a slide teaching two
things, a missing derivation step. Round 2's are figure geometry and one answer leak. Track that, not the count.

## The one thing to fix first — it is six of the seven new defects

Reviewer C named the class: **an in-figure text box drawn where something else already is.** Round 2 found it
on 057, 058, 059 (annotation × annotation), 064 (five separate collisions), 072 (annotation × axis rule ×
tick label), 073 (annotation × curve). Every one is a box that grew, or an axis that moved, after the
position was chosen by hand.

`FIGURE_GUIDE` already prescribes the cure and the deck already owns the machinery — `place_labels` solves
names against discs, edges and each other, and `note()` asserts a note clears the solved labels. The data
figures in `figs_tail.py` do not use either; they place annotations at fixed corners.

**R2-0 · BLOCKER-class, `figlib.py` (figs-tail owns this file for this round; nobody else touches it).**
Add a collision gate that every figure runs, and make it fail the build:

- collect every drawn text box: `text()` calls, tick labels, axis titles, curve labels, in-figure notes
- collect every drawn rule: axis spines, ticks, the drawn curves (sampled), reference lines
- assert no text box intersects another text box, and no text box intersects a rule or a curve
- the failure message names both objects and says *shorten the note or move the panel*, never *shrink the type*

Then delete the fixed-corner placements in `figs_tail.py` and let the gate drive them. Six findings below
(C-3, C-7 partly, C-12, D-9, D-10 and the 073 boundary note) close themselves once this exists — do not fix
them one at a time.

---

## A. `figures/figs_story.py`

**A2-1 · BLOCKER · `sum-ends.png` (016) renders twenty end-ticks as thirteen marks.** The slide's
instruction is "a tick at every end of every line" and the in-figure label asserts "10 lines, 20 ends".
Measured on the render, the accent-2 ink forms **13 connected components**: a single tick is ~190px², but
Sue's three ticks fuse into one 574px² chevron, Alice's likewise, and Pam's, Dale's and Jane's fuse in
pairs. The fusion is worst at the two hubs the module is about. **Fix:** push each end-tick out along its
own edge until its bounding box clears every other tick at that node, and **assert that the number of
accent-2 connected components in the rendered figure equals 2M = 20** — that is the number the label
prints, so assert exactly it.

**A2-2 · MAJOR · `handshake.png` (019) — accent-2 carries four roles and the end-tick changed colour.**
Red is the fill of all three discs, the dashed stub, the X, and the words "no partner". Worse, the
end-ticks here are **black**, where 016 and 017 draw the identical object in accent-2 — the deck spends two
slides establishing that a red tick is an end, then switches. And the dashed red line still leaves a disc
the way an edge does, which is R1's A-4 complaint answered at a different angle rather than removed.
**Fix:** discs in accent like every other graph; end-ticks in accent-2 as on 016/017; draw the unpaired end
as a tick with no line, bracketed rather than joined, labelled in-drawing.

**A2-3 · MAJOR · `handshake.png` (019) shows the failure and never shows the pairing.** The body says
"odd degrees **pair off**" and "must come in **pairs**"; no pair is drawn anywhere — no bracket, no lasso,
no matched mark. The mechanism being taught is the pairing; what is drawn is its absence. **Fix:** bracket
the ends in gray as two matched pairs, leave the fifth under the X, so "3 + 1 + 1 = 5" reads as two pairs
plus one.

**A2-4 · MAJOR · `rosters.png` (023) — the tally column encodes an unnamed quantity, and not the claimed
one.** A column of bars sits at the end of each girl's own line, so it counts the names *on that line* —
her degree, already visible. The caption claims the opposite direction: "Sue and Alice **appear on** four
lists each". The two coincide only because the graph is undirected and the slide never says so. **Fix:**
cut the tally column (the red/blue mark-up already carries the point), or move the count to a per-name
tally beneath the eight lines, labelled in-drawing "times her name appears".

**A2-5 · MINOR · `degree-def.png` (014) draws its four neighbours in annotation gray**, where every other
graph in the deck draws nodes in accent and gray means "exactly equal" two slides earlier. Neighbours in
accent, hub in accent-2.

**A2-6 · MINOR · `pk-def.png` (020) and `feld-pk.png` (021) are the same picture one slide apart** — four
piles of two 40px discs at k = 1…4 with the same fractions. R1's A-5 fixed the counts-vs-fraction defect by
importing 021's content into 020. **Fix:** keep 020 generic (unlabelled discs at k = 1, 2, 3, fraction
under each, no tie to the eight girls) so 021 still has something to reveal.

**Already done by me, do not redo:** `fb-twitter` (R1 A-2, now 100 discs with 93 in accent-2, median cut,
721 million on the drawing); the four-state derivation (R1 A-14); `sampling-bias`'s 28px marks with "1 of
7" and "6 of 18" printed (R1 A-8 and R2-B Major 5); `immunization-curves`'s y title and log-scale mark
(R1 A-15, which round 1 had applied to the x axis); `acquaintance-3` keeping the "picked" ring (R2-B
Major 4).

---

## B. `figures/figs_tail.py` (+ `figlib.py`, this round only)

**B2-0 · Do R2-0 first.** It is your file for this round and it closes six findings.

**B2-1 · BLOCKER · `slope-derivation.png` (064) gained its drawing and five collisions with it.** Measured
overlaps: the right panel's rotated `P(k′>k)` × gray "add it up" (133×49px); that title × the `10⁻²` tick
(50×34); the gray arrow × the `10⁻²` tick (60×24, the arrowhead on the exponent); the arrow × the title
(133×24); the left panel's "10" tick × the accent-2 `k` marker (15×21, rendering as `1ᛕ0`). The red
"everything above k" ends at x=653 and the title starts at x=666, so those run together too. **The
mathematics is right** — γ = 2.5 gives a five-decade drop left and three right, and the red point sits at
10⁻¹·⁵ at k = 10. **Fix:** the y title inside its own frame (it is in the inter-panel gutter, which causes
three of the five); "add it up" above the arrow, not on it; the `k` marker below the tick row or replacing
the k = 10 tick.

**B2-2 · MAJOR · the ruler changes twice, unannounced, on the slides whose thesis is that.** 055 plots
**counts** ("authors in the bin", 1…3000) over k ≥ 1; 057 plots **share** (10⁻⁶…10⁻²) over k ≥ 10 — same
construction, same bin width, nothing saying either transform happened, and 057's caption asserts it is the
same picture. The tell is on the slide: 055 says "122 bins hold all 23,133 authors", 057 says "113 bins
with anything in them", and the nine bins at k < 10 are never mentioned. **Fix:** draw `binned-once.png` on
`binning-1.png`'s axes and window, or state the change in 057's frame.

**B2-3 · MAJOR · `binning-1/2/3.png` (057–059) — the two annotations overlap on all three panels.**
accent-2 "bin width N" at y[152..176] against gray "N bins with anything in them" at y[171..202]: a
159–177px wide, 5px tall interpenetration, red baseline inside gray's cap band. On the render "in them" is
struck by "width 1". This is the annotation carrying the whole 122 → 24 → 7 comparison. Closed by R2-0.

**B2-4 · MAJOR · `ccdf-def.png` (060) — the countable objects are 12px.** All 52 discs measure 12px against
the 26–40px floor adjudication 1 set for *countable* objects. This is not the settled scatter-marker class:
the figure has no data x-axis and its explicit job is that one dot is one edge and one column is one node,
so the room can count 5 of 20. The gate is blind to them. The "1 edge" caliper is a 1px shaft with 5px
heads, drawn at a column x where that column has no dot at that height. **Fix:** lay 060 out full width
instead of a 537px `cols` column (the deck agent has D2-4), or scale the schematic so the discs land ≥26px;
redraw the caliper as a heavier bracket against the two dots it measures.

**B2-5 · MAJOR · `slope-worksheet.png` (065) still does not disclose that its data is synthetic.** Nothing
on the render says "a different network". It arrives after fifteen slides of cond-mat and the only tell is
that x reaches 1000 where cond-mat stopped at 279 — so a student reading it as the same network gets
**γ = 2.3 here against γ = 2.44 printed on 053**, on the pair of slides teaching that the two routes agree.
The triangle itself is exact (172px horizontal against a 172.2px decade; 55px drop = 1.3 × the 42.5px
y-decade). R1 B-6, unfixed. **Fix:** an in-figure panel title, "a different network".

**B2-6 · MAJOR · `slope-answer.png` (066) — the strike moved, it did not change colour.** The rule measures
`#B14434` while the text it cancels is now gray, so accent-2 still sets the right answer and cancels the
wrong one 90px apart. Half of R1 B-6 landed. **Fix:** the rule in annotation gray too.

**B2-7 · MAJOR · `exercise-card.png` (067) is still a picture of a text column.** Restyled, not rebuilt: it
reads "Data Visualization / one distribution / four pictures / one of them lies" against a left column
reading the same three facts in the same order. Under L1 the slide is two columns of text. R1 B-7 offered
two fixes and neither was taken. **Fix:** the four thumbnails, or tell me and the deck agent cuts the
figure.

**B2-8 · MAJOR · `hubs-share.png` (069) — the rank axis is still there.** The x axis is titled "rank",
running 1 → ~6000, and `grep -c rank m04-node-degree.md` returns **0**: the word appears nowhere in the
deck's prose, and every plot in the preceding twenty slides is p(k) or P(k′>k) against k. The figure also
never names its own network — 6,500 nodes arriving after twenty slides of a 23,133-node one. The
arithmetic is sound (65 = 1% of 6,500; 25,144/6,500 = 3.87). R1 B-8, unfixed. **Fix:** mark the top 65 on
the CCDF already on screen and shade their share; name the network in the drawing.

**B2-9 · MAJOR · `universality.png` (070) — the "physicists" label is still nearest the curve it does not
name.** Re-measured, identical to round 1: nearest ink is the **yeast curve at 23.0px**, its own at 50.2px,
the Internet at 54.6px. The generator was not touched. R1 B-9, unfixed. **Fix:** other curves as blockers
with a clearance floor, own curve as the attractor, and **assert each label's nearest curve is the one it
names.**

**B2-10 · MAJOR · the accent-2 role flip moved two slides later instead of going away.** On **069** red
marks the hubs; on **070** red is the Internet and blue the physicists, both hub-rich; on **072/073** red is
the random graph, the one with no hubs. Four slides, three meanings. B-10's ruling (accent = has hubs,
accent-2 = does not) holds on 072/073 only. **Fix:** apply it to 069 and 070 — hubs in accent on 069, and
on 070 give yeast a third mark so all three real networks can share accent. **Assert the role once at
module level.**

**B2-11 · MAJOR · `three-ccdfs.png` (073) — the caption, the body and the drawing disagree after the
rewiring.** The blue curve is labelled "physicists" in the drawing; the figcaption still says "**power
law**, random, and a lattice"; the body says "preference stretches it, randomness cuts it short", and
*preference* is not introduced until 077, four slides later. The rewiring itself is sound — the colour role
and ⟨k⟩ ≈ 8 are correct and the lattice step is at k ≈ 8 — it is the prose layer that is stale. Caption and
body are the deck agent's (D2-6); yours is the drawing.

**B2-12 · MINOR · the lattice wall on 073 and the γ = 3.5 curve's twin still terminate on the x-axis.**
054's was fixed and 073's was not; on a log axis whose floor is 10⁻⁵ this reads as "the distribution ends
here". R1 B-16, half-landed.

**B2-13 · MINOR · `fat-tail-reveal.png` (051) — the accent-3 band's left edge is now exact** (x = 588 = the
"100" tick) **and its top edge still encodes nothing** (band top y = 337, data top ≈ y = 358). Clip it to
the data or make it a full-height span.

**B2-14 · MINOR · `ccdf-def.png` (060) — the y ticks sit half a step above the dots they count.** Ticks
1/3/5/7 at y = 283.0/239.5/195.5/151.0 (22px per degree); dot rows at 294.5/250.5/206.5/162.5 — a uniform
11px = ½ pitch offset. Self-consistent (a column crosses k = 3 iff k > 3, which is what CCDF needs) but a
column of four dots visually reaches k ≈ 3.5. Tick the cell boundaries, or draw a faint gridline per degree.

**B2-15 · MINOR · `cdf-vs-ccdf.png` (062) draws the CDF curve and its label in annotation gray**, a colour
the deck reserves for annotation, opposite an accent CCDF. And "values reach down to 0" sits over a log
axis, which cannot show 0.

---

## C. `figures/figs_edge.py` and `figures/make_animations.py`

**C2-1 · BLOCKER · the quiz's answer is drawn in full, node for node, two slides before the question.**
`growth_pos(True, box)` returns one canonical layout, and `make_animations.py` **asserts** the GIF's layout
equals `quiz.png`'s preferential panel to 1e-9. So slide 076 ("Second ingredient: preference") shows that
exact graph with a gold ring on its hub, and 077 then asks which of A/B grew with preference — where B is
that same drawing recoloured. The room can answer by matching pictures, which the speaker note explicitly
forbids. `fig_quiz`'s withholding assertion scans **banned strings only**, so a graphical leak passes it,
and round 1 certified "no leak" on that assertion's strength. **Fix:** build the GIF from a different seed
(or a different rotation/scale) than the quiz's B panel, **and replace the equality assertion with its
negation** — assert the normalised layouts of the GIF's last frame and `QUIZ_B` are *not* equal. Keep some
other invariant tying the two (same generator, same m, same n) so they still cannot drift in the ways that
matter.

**C2-2 · MAJOR · `ba-growth.gif` (076) draws its network at 28% of the available width.** The graph spans
**304 × 252px** with 30px discs; every other single-graph slide in the range spans 950–1070px at 39–40px.
The cause is `BOX = (384, 24, 696, 338)` — frozen at the size of a *quiz panel* so the two counters can sit
at the canvas edges, where two short gray lines eat 780px. The GIF-to-quiz assertion is on the
**normalised** layout, so the box can grow freely. **Fix:** counters above or below the drawing; give the
graph the width. The hub's 15 spokes are the thing the room must see.

**C2-3 · MAJOR · the arriving node's two edges are drawn in two different colours** on the GIF's static
frame. `ba_frames()` emits one frame per *edge*, so the last frame highlights only the second of the
arrival's two edges: the red node has one red edge and one black. Slide 075 draws both of an arrival's
edges red under "a node arrives, brings **two** edges". **Fix:** one frame per arrival for the highlight,
or highlight both of the new node's edges.

**C2-4 · MAJOR · the accent-3 ring is drawn on top of the hub's spokes**, severing all ~15 of them at the
disc; only stubs survive between ring and disc. E-1's ring is otherwise correct. Draw the ring under the
edges.

**C2-5 · MAJOR · `quiz.png` / `quiz-answer.png` (077/078) — R1's B-13 landed in the caption only.** The
spec said in so many words: put the switch **in the drawing**; a caption is not where a student looks when
counting spokes. Grepping `figures/` for "sketches" returns nothing; the string is in the 24px gray
figcaption. **Fix:** a line under the two sketches, in the drawing, on both files.

**C2-6 · MAJOR · 077/078 — the crossings and disc sizes did not move.** Recomputed: **21 crossings** in
panel A, **20** in panel B, the identical numbers round 1 reported; `GROWTH_NODE` went 29 → 30 against
39–40px everywhere else in the range. R1 B-12, unfixed. **Fix:** a crossing-minimising pass with an
asserted budget, or drop to ~14 nodes; raise the discs.

**C2-7 · MAJOR · 077/078 — accent-2 is inverted against the role established five slides earlier.** On
072/073 accent-2 is the random graph with no hubs; on 077/078, on the same log-log form, accent-2 is B,
"preference", the hub-rich one. **Fix:** swap the two colours in `_quiz_body`'s panel loop and assert the
role at module level. (Coordinate with B2-10 — one ruling, applied everywhere.)

**C2-8 · MAJOR · `individual-vs-average.png` (081) — the only number the figure draws contradicts the
grouping.** Every disc carries her own k and the girls are split 5/2/1 by whether she is below, above or
equal to her friends' average, which is nowhere on the drawing. On the render the red group reads 1, 2, 3,
3, 1 and the gray "same" disc reads 2 — so two discs printing **2** sit in different groups and two
printing **3** sit in "fewer". **Fix:** draw the comparison — a caliper per girl from her k to her friends'
mean, the idiom `feld-friendmeans.png` already uses — or print the pair ("2 vs 3.5") under each disc.

**C2-9 · MAJOR · `scale-free-debate.png` (093) still names no test.** C-4 landed the 2019 content, but the
title promises a statistical test and no test is named anywhere — no Clauset–Shalizi–Newman, no likelihood
ratio, no KS. **Fix:** name it under the 2019 dot.

**C2-10 · MINOR · `recap.png` (095) — the new "one wiring" panel draws its two hubs in accent** where slide
088 draws the same two degree-4 hubs in accent-2. This is C-8's exact defect reproduced inside the panel
C-8's fix added, two lines below a comment guarding panel one against it.

**C2-11 · MINOR · `assortativity-real.png` (089) — the axis is a ±0.30 window and the drawing does not say
so.** "r runs −1 to +1" sits ~470px from the axis it qualifies and is read after the dots, so a reader takes
Facebook's +0.226 for near-maximal. Put the caveat beside the axis.

---

## D. `m04-node-degree.md`

**D2-1 · BLOCKER · slide 011 states two different counts for the same ten lines, 120px apart.** The third
bullet says "every one of those **twenty friendships** was counted from both ends"; the figcaption below
says "two averages over the same **ten** friendships". The drawn network has ten lines. **This got worse in
round 1's fix**: the sentence was a gray `note` and D-3 made it a full-weight black bullet, so the wrong
number now carries the same visual weight as the two correct ones — five slides before 016 teaches the very
distinction it is garbling. **Fix:** "every one of those **ten** friendships was counted twice, once from
each end."

**D2-2 · MAJOR · slide 011 — the body's 2.5 is red where the figure's 2.5 is blue**, on a slide where
colour *is* the encoding (blue "each girl", red "her friends"). Round 1's reviewer A filed this and it never
entered `FIXES_R1.md`, so nobody was assigned it. **Fix:** body "2.5" in accent, "3.0" in accent-2.

**D2-3 · MAJOR · slides 008 and 015 — the milestone's answer is printed seven slides before the question.**
015 asks "add every girl's degree together — what do you get?" and says "shout the total"; 008's first
bullet already reads "**Twenty** friendships end here". That bullet also uses the edge-end idea eight slides
before 016 introduces it, and states twenty friendships above a figure showing ten lines. **Fix:** rewrite
008's bullet to reach 2.5 without naming twenty — "their eight counts average **2.5 friends**" — and let
015/016 own the number and the word "ends".

**D2-4 · MAJOR · lay slide 060 out full width.** Its schematic is a 537px `cols` column, which is why its
countable discs are 12px (B2-4). Move the two paragraphs above the figure.

**D2-5 · MAJOR · slides 016, 019, 021 — the conclusion sits below the figure and lands with it.** On 016
"$\sum_i k_i = 2M$" is on screen while the room is still counting ticks; on 019 the handshaking lemma is on
screen with the figure meant to make them ask why; on 021 "about as flat as a degree distribution gets"
arrives with the sorted girls. The deck has six `*` markers in 96 slides. **Fix:** make the closing
sentence a `*` fragment on each.

**D2-6 · MAJOR · slide 073's caption and body are stale after the rewiring.** Caption still says "**power
law**, random, and a lattice" where the drawing says "physicists"; body says "preference stretches it"
where *preference* arrives four slides later (N1). **Fix:** caption names what is drawn; body drops the
mechanism words until 077.

**D2-7 · MAJOR · slide 086's second clause names a comparison the figure does not compute.** "The accounts
you follow are followed more than you are — **and so are the accounts that follow you**." The right panel is
**out-degree**: an arrow's tail 1.8, i.e. "the accounts that follow you follow more accounts than you do".
The figure draws Hodas' versions 3 and 2; the sentence claims 3 and 1. C-1's arithmetic landed correctly and
the sentence did not follow. **Fix:** match the clause to the panel.

**D2-8 · MAJOR · slides 025, 037, 040, 042, 080, 085, 087 — seven more question slides with no visible
beat.** D-10 was applied to the six slides it enumerated rather than to every slide meeting the criterion.
**Fix:** one visible line each. 042 especially — "thirty seconds with your neighbour: you cannot see the
network, so what can you ask?" — since the room is about to spend a whole part on the answer.

**D2-9 · MAJOR · slide 047 is dense and static** — figure, caption, setup, the two-number answer and a gray
note teasing Thursday, all at once. **Fix:** fragment the left column.

**D2-10 · MINOR · slide 072's speaker note says "the largest degree in that network is fifteen"** where the
figure now prints **28**. Fifteen was the old ⟨k⟩ = 4 graph. The lecturer will say a number the room can see
is wrong.

**D2-11 · MINOR · slide 093's figcaption restates the in-figure labels verbatim** within 100px of them;
**095 still has no takeaway line** (the only figure slide in the range with no body text); **095's caption
names four items for five panels** and calls the fourth "one distribution" where the panel says "one tail",
while the new "one wiring" panel is missing from the caption entirely.

**D2-12 · MINOR · slide 083 names `friendship-paradox-game.html` with no path**; `docs/lecture-note/assets/vis/`
is still only in the speaker note.

**D2-13 · MINOR · slides 014, 020, 060, 064, 096 — L6.** Bottom-most ink out of 720: 014 → 497, 020 → 485,
060 → 561, 064 → 527, 096 → 496.

**D2-14 · MINOR · slide 010 says the key two ways** ("Red: her friends average more than she has" in the
body, "five below their own friends" in the caption, 400px apart). One phrasing, anchored on the girl.

**D2-15 · MINOR · slide 012's caption repeats the drawing's headline** ("2.7 friends each, and 3.4 friends
per friend" against the drawing's "2.7 friends each, 3.4 per friend") — round 1 replaced one duplication
with another. **005** does the same at greater length: the timeline's labels restate the body almost
verbatim 150px away.

**D2-16 · MINOR · slide 023's caption is the figure's key and sits under the drawing** — D-24 fixed exactly
this on five slides and `rosters.png` was not on the list.

**D2-17 · MINOR · slide 066 states γ = 2.3 three times** (title, figure, body) and **088 prints `r` three
times before 089's axis title binds it to "assortativity"**.

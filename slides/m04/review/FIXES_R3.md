# m04 round 3 — fix spec

Three reviewers, disjoint ranges, all three returned. **3 Blockers · 20 Majors · 39 Minors.**
Reports: `REVIEW_R3_A.md` (001–033), `REVIEW_R3_B.md` (034–065), and reviewer C's (066–097).

    round 1   6 Blockers   38 Majors   34 Minors
    round 2   5            33          36
    round 3   3            20          39

Blockers halved, Majors halved, Minors up because the reviewers are measuring harder. That is the
shape to expect. `check_render.py` exits 0 throughout.

## What the round is really about

**Two of the three Blockers were created by round 2's own fixes**, and both by the same fix:

- C2-7 made the colour role consistent (accent = has hubs, accent-2 = does not) from Part Six on.
  Three slides then spend that key in words — "hubs effectively impossible", "randomness cuts it
  short", "real networks have hubs and random ones do not" — and the quiz question slide draws
  panel A entirely accent-2 and panel B entirely accent. **A student reads the answer off the key
  and votes without looking at a tail**, which the speaker note explicitly forbids. A consistency
  fix collided with N4.
- C2-5 put the sketch/tail switch in the drawing, as specified, and left the caption it was
  replacing. The drawing says 14 nodes; the caption says 24.

And the round's structural lesson, which both reviewers arrived at independently:

> **The gates see quantity, not position.** The collision gate finds overlap but not placement —
> `sum-ends`'s twenty ticks are all present and five pairs sit 18bp apart at their edges' midpoints,
> reading as the geometry mark for *equal lengths*. `growth_layout`'s clearance gate runs on the
> canonical box and `growth_pos` then scales by 0.873, so 46bp of clearance becomes 40.1bp against
> 40bp discs and six discs fuse. **Assert the property on the coordinates actually drawn.**

---

## A. `figures/figs_story.py`

**A3-1 · BLOCKER (shared with the deck) · accent-2 means the opposite thing on 010 and on
014/023/026.** On 023 every "Sue"/"Alice" is accent-2 and every "Betty"/"Tina" accent, with nothing
on the slide saying what either means; 010 states "Red: she has fewer friends than her friends
average" and draws Sue and Alice *blue*. This is round 1's Major 2 with the sign flipped — that fix
removed the 010↔012 conflict and the conflict reappeared at 010↔014/023/026. **Ruling: accent-2 =
the node we are counting, or the hub**, which 014, 023, 026 and 027 already do. Recolour **010**
(e.g. below = hollow disc, above = filled accent-2) and keep every other figure as it is. The deck
agent restates the key on 010 and prints one on 023.

**A3-2 · MAJOR · `sum-ends.png` — five edges draw both end-ticks as an adjacent pair at the
midpoint.** The long edges carry ticks at 20–30% and 70–85%; the five 150px edges carry theirs at
44% and 56%, 18px apart. Around Sue the eye counts six marks, not four, and "⫽" at a midpoint is
the standard mark for equal lengths. Cause: the generator places each tick a fixed ~66px from its
node. **Fix:** place at a fixed *fraction* of each edge (0.20 / 0.80) and **assert the two ticks on
every edge are ≥40% of that edge's length apart** — the component count cannot see position.

**A3-3 · MAJOR · `derivation-1..4` — the subscript "friend" measures 12px x-height** against the
15px floor, and it is the only mark separating ⟨k⟩_friend from ⟨k⟩; without it lines 1, 2 and 4 all
read "⟨k⟩ = …", which is the whole derivation. `check_render` reports 11px as a *warning*. The
frame is sized for four lines and stands two-thirds empty on 028. **Fix:** raise the subscript
until it lands ≥15px on the slide, grow the frame, and assert the rendered x-height of the
subscript specifically.

**A3-4 · MAJOR · `qk-formula.png` (027) shows a per-girl probability under a per-degree formula.**
The tally reads 4 of 20 = 0.2 for a degree-4 girl; q(4) = 4·(2/8)/2.5 = **0.4**, because two girls
sit at degree 4. The figure already pairs the two girls at each degree, so it is one bracket away:
group them and label "k = 4: 8 of the 20 hands → q(4) = 8/20". The deck fixes the sentence.

**A3-5 · MAJOR · `bag-of-hands.png` (026) draws edge *ends* with the 40px lettered disc that has
meant a person on every slide since 006** — on the slide whose single point is "you do not pick a
person, you pick one end of one edge". The deck's own end-glyph, the red tick, does this job on
016, 017 and 027. Round 2 filed it as a Minor; it is the slide's whole point. **Fix:** twenty red
ticks labelled with their owner's initial; keep discs for people. Spell all eight initials in the
legend while you are there, or drop the legend.

**A3-6 · MAJOR · `acquaintance-3.png` (046) — the build stops accumulating.** 045 draws the
nomination as a 4.4bp accent-2 arrow; on 046 that edge is a plain 2.6bp black stroke, so the slide
titled "vaccinate the friend, not the volunteer" has lost the mark saying how the friend was
reached. `_acq_base(treated=("H",))` never re-draws it. *(Mine. Keep the ring AND the arrow.)*

**A3-7 · MAJOR · `fat-tail-reveal.png` (052) — the head-of-distribution annotation is drawn on the
tail highlight.** The accent-3 band spans x = 588–1157 (left edge correct at the k = 100 tick);
"78% of 23,133 authors" spans 414–715, so 127px of it lies inside the band, describing k ≤ 10 while
sitting over k = 43…142. **Fix:** anchor it east of the band's left edge, or give it a leader down
to the k ≤ 10 column. **And add accent-3 fills to the collision gate's blocker set** — the gate
checks text against text, rules and curves, not against fills. Coordinate with figs-tail, who owns
`figlib.py`.

**A3-8 · MINOR · 039's 82.8% strip is now the only bar in the deck** — 040's three bars became 100
discs for exactly this rule and this one was left. **A3-9 · MINOR ·** `feld-two-numbers` (017)
prints "2.5" in accent-2 where 011 encodes 2.5 as accent; same family as A3-1. **A3-10 · MINOR ·**
`worksheet-star-ring`/`worksheet-answer` jump 66px between question and answer and the
`Var(k)/⟨k⟩` label changes colour — the acquaintance build holds still across three slides and this
one should too. **A3-11 · MINOR ·** `degree-def` numbers its four edges 2, 1, 3, 4 clockwise.

---

## B. `figures/figs_tail.py` (owns `figlib.py`)

**B3-1 · BLOCKER · the quiz question slide (078) is answerable from the deck's colour key.** Panel
A is entirely `NO_HUBS`, panel B entirely `HUBS`, and 073/074/075 spend that key in words.
**Fix:** on the *question* figure only, draw both sketches in one neutral fill (ink or annotation
gray) and separate the two CCDF curves by dash pattern with the A/B labels. Introduce accent and
accent-2 on the *answer* figure (079), where "no preference"/"preference" arrive and the roles
become legible. Keep the module-level role assertion for every other figure — the ruling is right;
it is one slide that must be exempt, and the exemption should be explicit and commented, not
accidental.

**B3-2 · MAJOR · six of the twenty-eight quiz discs fuse into three blobs.** `growth_layout`
enforces `gap >= node + 2` in `GROWTH_BOX` (312×314) and passes at 46.0bp; `growth_pos` then maps
into `QUIZ_A`/`QUIZ_B` (312×**274**), `s = 0.8726`, taking the gap to **40.1bp against 40bp discs**
— which the render's antialiasing bridges. The gate never re-runs after the mapping. This is C2-6's
disc-size fix landing without its clearance check. **Fix:** solve the layout in the panel box
directly (`growth_layout(box=QUIZ_A)`), and **re-assert minimum pairwise distance on the positions
actually drawn**.

**B3-3 · MAJOR · four consecutive CCDF panels, four different vertical rulers.** One decade of
P(k′>k) measures **42.2px on 071, 34.7px on 074, 27.2px on 070, 21.8px on 073**, and the x ranges
differ too. 073's caption says "the same 23,133 nodes and the same average as the physicists" —
i.e. compare me to 071 — while being drawn on a ruler half as tall. 073 also carries two y ticks
where its neighbours carry three, and a 254bp frame against `FRAME`'s 356. This is the failure Part
Five spends ten slides teaching. **Fix:** one frame and one y range across all four; if 073 must be
short, say on the drawing that the axis is cropped.

**B3-4 · MAJOR · `three-ccdfs.png` (074) draws the lattice as chart furniture.** Solid black at
4px — heavier than the 2px axes — running along P = 1 and straight down to the x-axis row, closing
a rectangle against the black axes that reads as an inset panel border, with the black word
"lattice" inside it. B2-12 ("terminates on the axis"; the floor is 10⁻⁵, not zero) is unfixed here.
**Fix:** annotation gray or accent-3 at the same weight as the other two, stopping one grid step
above the axis with an open end, label outside the step.

**B3-5 · MAJOR · the deck's two exponents for cond-mat are 0.85 apart where it teaches they must be
exactly 1.0 apart.** 054 prints slope −2.44 on p(k) and 055 says "slope is −γ"; the same network's
CCDF falls at **−2.29** over the same range, and 065's rule predicts −1.44. Apply the deck's own
rule to its own two pictures and you get γ = 2.44 and γ = 3.29 — while 067's note calls a gap of one
"a different physics". `figs_tail.py`'s docstring still quotes −2.571, which the code no longer
computes. **Fix (preferred):** print the fitted CCDF slope on 062 with a body line saying it does
not reconcile by the +1 rule *because the tail is not a clean power law* — that is Part Eight's
argument arriving where its evidence lives, and it is better teaching than either number alone.
Update the docstring. Coordinate the body line with the deck agent.

**B3-6 · MAJOR · `binning` — widening the bin multiplies every height, and the slide says nothing
was recomputed.** `binned(w)` returns raw counts and never divides by w: the leftmost point goes
from 2,373 at k = 1 to 16,588 at k = 4.5, a 0.85-decade rise on identical axes. **Fix:** plot per
unit k, which puts all three panels on one comparable scale and leaves the change in *shape* as the
only visible difference — which is what the build is about.

**B3-7 · MAJOR · `binning` — the claim is asserted and the number that would show it is computed and
thrown away.** The visible change across the three panels is that the scatter thins, which reads as
"wider bins are cleaner", the opposite of the point. The fitted slopes are **−2.25, −2.90, −3.80**;
`_fig_binning_panel` computes all three, asserts they differ by 0.3, and prints none. Bin width
alone moves cond-mat across the γ = 3 boundary. **Fix:** print the fitted slope beside each panel's
bin-width note.

**B3-8 · MAJOR · `cdf-vs-ccdf.png` (063) varies quantity and axis together and says so out loud.**
Panel titles read "CDF · linear y" and "CCDF · log y", so a student can correctly answer "the left
one is bad because you used the wrong axis" and the slide has no reply. R1 B-2 asked for the ruler
change to be *stated*; it was stated rather than removed. **Fix:** draw the CDF on the same log y.
It still flattens at 1 from k ≈ 30 and still shows nothing of the tail, so the point lands harder
and the only difference is the quantity.

**B3-9 · MAJOR · `hubs-share.png` (070) — the headline number is text, never drawn.** The in-figure
line and the caption both lead with "33.8% of all edge ends", and the figure is a CCDF with a
shaded band: it shows how *few* the hubs are and nothing about the third of the ends they hold.
B2-8 asked for both halves; the first landed. **Fix:** draw the share as a single split rule under
the plot, 33.8% of its length in accent-3, or demote the share to the body.

**B3-10 · MINOR ·** 070's accent-3 fill spans the full plot width while its label says "k ≥ 36" —
everything left of the dashed line is shaded and is not k ≥ 36. **B3-11 · MINOR ·** 071's
"physicists" label is anchored where two curves cross (37.7px own, 45.2px Internet, the two nearest
points 12px apart) and all three curves are now one colour, so proximity is the only cue; add a
clearance floor to the solver rather than a strict inequality. **B3-12 · MINOR ·** 073's CCDF's
rightmost point is k = 21 while its headline says "largest degree 28", because `ccdf()` evaluates
only at observed degrees. **B3-13 · MINOR ·** 073's x axis runs to 300 with the last point at 28,
and half the panel is empty. **B3-14 · MINOR ·** `fig_slope_derivation`'s only assertion compares a
value with itself (`abs((g-1)-(g-1)) < 1e-12`). **B3-15 · MINOR ·** 061's "1 edge" caliper still
sits in the gutter rather than against the two dots it measures, and calls "an end" an "edge".
**B3-16 · MINOR ·** 093 titles its y axis "CCDF" and ticks 10²/10³ where every other CCDF in the
deck titles it P(k′>k) and ticks 1/10/100/1000.

**B3-17 · Add fills to the collision gate's blocker set** (see A3-7). Text over an accent-3 band is
invisible to it today.

---

## C. `figures/figs_edge.py`

**C3-1 · MAJOR · 089's hubs are accent-2, inverting the role the module declares.** `figs_edge.py`
never imports `HUBS`/`NO_HUBS`. Ten slides after 073 taught that an accent-2 network is the one
*without* hubs, the six red discs on 089 are the hubs, and nothing on the slide says what red means.
B2-10 asked for the role to be asserted once at module level; the declaration exists and stops at
the file boundary. **Fix:** import and apply it — hubs in accent, the rest in annotation gray — or,
if the within-graph axis needs its own key, print that key in the drawing.

**C3-2 · MINOR ·** 095's "⟨k²⟩" floats ~110px above the arrow it labels with nothing joining them,
and all three branch values are accent-2 so nothing distinguishes the two proved results from the
one "still to come" (which nonetheless prints a value). **C3-3 · MINOR ·** 096's accent-2 carries
three meanings across five panels; a one-word gloss under each closes it. **C3-4 · MINOR ·** 085's
first and third panels are both rings ("ring" C6 and "ring lattice" C8(1,2)); retitle the first
"cycle". **C3-5 · MINOR ·** 085's K₅ is drawn pentagon-plus-pentagram, five crossings where the
minimum is one — noted as a trade, not an error, since the symmetric form makes "every node has 4"
instantly readable.

---

## D. `m04-node-degree.md`

**D3-1 · BLOCKER (with A3-1) · state the colour key where the colours are used.** 023 carries two
unexplained colours; 010 states a key that the rest of the deck contradicts. Once figs-story
recolours 010 under the A3-1 ruling, rewrite 010's key sentence to match and add a one-line key to
023.

**D3-2 · BLOCKER · 078's figcaption says 24 nodes where the drawing says 14.** The panels contain
14 discs. C2-5 put the switch in the drawing and left the caption it replaced. **Fix:** cut the
switch clause from the caption entirely — the drawing carries it — leaving "two networks, same
average degree, and their two tails". This also removes a "20,000"/"20 000" separator mismatch.

**D3-3 · MAJOR · 011 claims 3.0 as the outcome of an exercise that produces 2.99.** 009 has eight
students each compute one girl's friends' mean; 010 prints their eight answers; those average 2.99.
033 then says "counting the sixty friends of the twenty friends by hand gave exactly the same" — a
hand count nobody performed. The reconciling distinction arrives on 034. **Fix:** "Your eight
numbers average **2.99**. Feld's number — averaging over the twenty friendships rather than the
eight girls — is **3.0**", and let 034 do the why.

**D3-4 · MAJOR · 011's third bullet answers 022's question eleven slides early, with a reason that
does not produce the effect.** "every one of those ten friendships was counted twice, once from
each end" — double counting is symmetric and is not the mechanism: a ring counts every friendship
twice and has a gap of exactly zero, which 032 asserts and 035 demonstrates. **Fix:** end the
bullet at "Not an insult, and not about being unpopular — we will find out why in a moment."

**D3-5 · MAJOR · 016's title spoils 018's two-minute challenge.** "Twenty, and **never odd**" is
asserted two slides before the room is asked to build a network with exactly three odd-degree
nodes, and 016's body never demonstrates parity. **Fix:** retitle to what the slide shows ("Twenty
ends, ten lines"); keep "never odd" for 019.

**D3-6 · MAJOR · 030 is the only derivation slide with no prose, and it is the one introducing
Var(k).** The gloss says "rewrite ⟨k²⟩" (what, not why), the figcaption does not contain the word
*variance*, and 032 opens "A variance cannot be negative" as established. **Fix:** one body line
matching 029's treatment of ⟨k²⟩.

**D3-7 · MAJOR · 059's "Nothing was recomputed" is false as drawn** (see B3-6). If figs-tail plots
per unit k, the sentence becomes true; if not, rewrite it to "the degrees are unchanged; only the
buckets are wider, so each holds eight times as many". Coordinate.

**D3-8 · MAJOR · 082 is dense and static and there are zero fragments in slides 066–097.** Its
closing question is the setup for 083, so the room reads the next slide's premise while parsing
this one. **Fix:** make the closing question a `*` fragment. D2-5 applied this by slide list; this
slide meets the criterion.

**D3-9 · MAJOR · 027's sentence describes the wrong quantity** (see A3-4): "the chance of drawing
**her** is proportional to k" — q(k) is not her chance, it is the chance the girl you draw has
degree k.

**Minors, grouped.** *Captions restating what the drawing prints:* 006, 021, 031, 033, 039, 050,
052, 058, 059, 060, 070, 071, 073, 079, 082, 085, 087, 089 — round 2 fixed this class by slide list
three times and never ran the criterion over Parts Four to Eight. Give each caption the thing the
drawing cannot say. *Wording:* 012 "every girl in that school", not "in the survey" (146 is one
school's girls with a mutual friend); 019 "Ends pair off", since the figure pairs ends and the
sentence then contradicts its own first clause; 048 uses three names for one strategy; 050's title
promises "the variance" over a figure printing Var/⟨k⟩; 074's "a lattice flattens it" sits under
the steepest cliff on the slide; 094's "on these axes" has no referent on its own slide; 084's
48-character path wraps across two lines. *Typography:* straight quotes and apostrophes at heading
size on 082, 084, 090, 094; an en-dash doing the work of "the same as" on 073. *Layout:* 076 takes
`mid` (ink stops at 552 of 720). *Redundancy:* 067 prints "1 − γ = −1.3" twice ~250px apart; 065's
figure and speaker note state the sign relation in opposite words on the slide about the most
common error in this material. *082:* name Sue and Alice under their discs — the body names them
and the drawing does not.

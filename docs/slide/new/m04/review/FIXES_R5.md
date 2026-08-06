# m04 round 5 — fix spec

    round 1   6 Blockers   38 Majors   34 Minors
    round 2   5            33          36
    round 3   3            20          39
    round 4   3            11          26
    round 5   2             4          12

Two reviewers over 49 and 48 slides. `check_render.py` exits 0 — and now covers 453 discs rather
than 435, because annotation gray has been added to `NODE_FILLS` (see the note at the end).

## Both Blockers are one defect, at its fourth and fifth address

Accent-2 on a person means *above her friends' average* on slides 010 and 012, and *below* on 039,
040, 082 and 096. A student holding the key that slide 010 spends its whole body teaching reads the
Facebook slide as "93 people in 100 have more friends than their friends" — the module's thesis
inverted, on the slide that scales it to 721 million, and again on the one-page recap.

The history is the point:

| round | what I specified | what happened |
|---|---|---|
| R3 | "recolour slide 010" | it was recoloured; the sibling function twelve lines below was not |
| R4 | "declare the roles at module level and use them in **both** functions" | declared; the two functions I named went through it |
| R5 | — | the other two call sites in that file still call `dot(color=...)` raw, **and a second file has its own contradicting declaration, with an assertion that guarantees the inversion** |

Every round I have specified the instances I could see, and every round the instances I could not
see became the next round's Blocker. **This round the fix is the mechanism, not the instances.**

`figs_edge.py:141` currently asserts the inversion:

    assert rel == {"accenttwo": 1, "accent": -1, "annot": 0}[fill]

So the generator now guarantees the contradiction it should be preventing. That is what an
assertion written against a literal rather than against a shared constant buys.

---

## A. The role fix — `feld.py`, `figs_story.py`, `figs_edge.py`

**One change, three files, and it closes the class.** figs-story leads; figs-edge follows once the
constants exist.

**A5-1 · BLOCKER · move the roles into the module both files already share.** `figs_edge.py`
already does `from feld import ABOVE, BELOW, EQUAL` — it imports the *data* and re-invents the
*roles*. So:

1. Move `ABOVE_FRIENDS` / `BELOW_FRIENDS` / `EQUAL_FRIENDS` from `figs_story.py` into **`feld.py`**,
   beside the group memberships they colour.
2. Import them in both `figs_story.py` and `figs_edge.py`. Delete `figs_edge.py`'s own comment and
   colour literals at lines 141–150 and 599.
3. **Rewrite `figs_edge.py`'s assertion to read the constants, not a colour string.** As written it
   encodes the wrong answer and passes; reading the constants makes the same assertion catch the
   defect it was meant to catch.
4. Route the raw call sites through `role_disc()` / `friend_role()`: **`fig_coauthor_gap`
   (`figs_story.py:973`) and `fig_fb_twitter` (:1007)**, which call
   `dot(color="accenttwo" if i < hit else "accent")` with `hit` counting the group *below*.
5. Swap the polarity on **039, 040, 082 and 096** to match 010 and 012: the minority above in
   accent-2, the majority below hollow, equal in gray. 012 already shows this reads well — 80
   hollow discs are fine and the printed number carries the weight.

**And make the raw call impossible, not merely corrected.** Four rounds of naming call sites have
produced four rounds of one more call site. Whatever mechanism you choose — routing every person
disc through one helper and asserting the colours it emitted, counting accent-2 discs per figure
and checking against the size of the group they are supposed to mark — the test is: *if someone
adds a fifth figure that colours people, does the build fail?* If the answer is no, the class is
not closed.

**Two dependent edits.** 039's headline "8.1 / 22.1" is currently drawn in accent and accent-2, so
the same two colours mean both *the two averages* and *which authors* inside one figure (Major
below). And 040's seven accent discs have nothing on the slide saying what they are; under the swap
they become the accent-2 minority and explain themselves.

---

## B. `figs_story.py`

**B5-1 · MAJOR · `coauthor-gap` (039) uses each colour twice inside one figure.** Top line: **8.1**
in accent under "each author", **22.1** in accent-2 under "their coauthors". Directly beneath, a
4×25 field where accent-2 is the 83 authors *below* and accent the 17 above — and the red headline
sits in a column straight above the red field, so the available misreading is *the red dots are the
coauthors*. **Fix:** draw 8.1 and 22.1 in ink, or keep only 22.1 in accent-2 if the slide is about
the gap (the `fig_feld_two_numbers` rule), and let the disc field be the only colour-carrying
element.

**B5-2 · MAJOR · `sampling-bias` (042) draws edge-ends with the disc that means a person** — on the
slide whose whole point is that picking a person and picking an end are different samples. Measured:
both rows use the same 28×27px disc, and accent-2 means "the hub, a person" in the top row and "one
of the hub's ends" in the rows below. Eight slides earlier, 034 distinguishes them by glyph (20 red
ticks against 8 discs). This is R3's A Major 7 — fixed on 026, still live on 042, in the same file.
**Fix:** draw the 18 as the deck's red tick, the hub's six in accent-2, the rest in ink or gray.
"1 of 7 people" against "6 of 18 ends" then reads off the glyph alone. *(Arithmetic is correct: 9
edges, hub degree 6, (6/18)/(1/7) = 2.33.)*

**B5-3 · MINOR ·** 009's "picked" ring shares a pixel column with the "J" of "Jane" — the ring is
added after the label solve and is not in it, the same root as C4-4. **B5-4 · MINOR ·** 028 is still
the only derivation slide with no body prose, in a frame three-quarters empty (ink rows 154–238 of
140–475); the fixed frame height is right, so the fix is the prose. **B5-5 · MINOR ·** 035→036 still
jumps 66px because 036 adds a body paragraph below the figure. **B5-6 · MINOR ·** 011's figure
prints 3.0 at 88pt from the first beat, so bullet 2's punchline precedes bullet 2.

---

## C. `figs_tail.py`

**C5-1 · MAJOR · `hubs-share` (070) — the share bar is a proportion scale drawn on the degree
axis.** The split is arithmetically exact (295/872px = 33.83% against a printed 33.8%, and 65
routers do hold 33.85% of 25,144 ends), but it sits *inside the plot frame* on the P = 10⁻⁴
gridline, so the red/gray boundary at x = 580 reads **k ≈ 13** on the x ruler, while the hubs start
at the dashed line at k = 36, 116px to the right. The hubs' share therefore ends inside the
low-degree region. It also reads first as a reference line at P = 10⁻⁴, and the CCDF's last pixel
touches its top edge. **Fix:** take the bar out of the axes — a standalone strip above the frame or
below the x-axis title, both ends labelled ("65 routers · 33.8% of edge ends" / "the other 6,409 ·
66.2%"). **Do not** confine the split to the shaded rectangle; 33.8% of the shaded width is a worse
mis-encoding than what is there now.

**C5-2 · MINOR ·** `ccdf-condmat` and `three-ccdfs` are left-anchored in a full-width canvas —
22.2% and 16.8% blank on the right — so the ink centres 114px and 85px left of centred figcaptions.
B4-3 narrowed the frame and left the canvas. Centre the drawing, or crop the canvas to the frame.
**C5-3 · MINOR ·** 066→067 jumps 66px, same cause as B5-5. **C5-4 · MINOR ·** 074's leader to the
red "random" curve is drawn in annotation gray, which on that figure is the lattice — draw it in
accent-2 or drop it.

---

## D. `figs_edge.py`

**D5-1 · BLOCKER · see A5-1** — the roles, the assertion, and 082/096's polarity.

**D5-2 · MINOR · `lognormal-trap` (093): C4-3 landed on the y axis and not the x.** The k ruler
measures 379.5px per decade against 264.5 everywhere else, so a given exponent draws at 5.2° here
and 7.4° there — and 092 explicitly invites the comparison ("we drew a straight line through those
points an hour ago"). Ticks are 10/10²/10³ where every other k axis uses 1/10/100/1000. Route the x
range through `CCDF_BOX`'s px-per-decade: 2.3 decades × 264.5 = 608px fits.

**D5-3 · MINOR ·** 094's timeline still draws 12 years and 8 years at 340 and 330px. The new
interval chips now print the numbers the drawing contradicts, which makes it easier to catch rather
than harder — make the spacing metric, or drop the chips.

---

## E. `m04-node-degree.md`

**E5-1 · MAJOR · 094's reconciliation reads as the +1 rule the deck just taught.** The fragment says
"cond-mat's p(k) gives γ = 2.44, its CCDF gives 3.57. One tail, two answers." Both numbers are
right. But 064–067 have just drilled "the CCDF slope is γ − 1, so add one", the slide prints no
slope, and 2.44 → 3.57 looks like exactly that rule being applied — the opposite of the claim, on
the deck's closing piece of evidence. 062 used to print a fitted slope a student could point back
to and no longer does. **Fix:** put the slope on the fragment — "cond-mat's p(k) gives γ = 2.44;
its CCDF slope is −2.57, and γ − 1 = 1.44 is what the rule predicts. One tail, two answers." — or
ask figs-tail to restore a plain fitted-slope annotation to 062 (the number only, no comparison, no
"not −2.44 + 1") so 094 has something on the deck to point at.

**E5-2 · MINOR · 033's "Two routes with no arithmetic in common" is false**, and both routes are on
the slide: the left prints ⟨k²⟩ = 7.5 and the right "60 friends", and 7.5 = 60/8. Both routes are
Σk² = 60, which is what 028–031 derived. Also "60 friends" invites "60 friendships" on a slide about
counting (there are 10). **Fix:** "Two very different countings, landing on the same number", and
"60 friends across the 20 ends".

**E5-3 · MINOR ·** 011 and 034 use the same person/friendship grammar for different quantities —
011's figure says "2.5 per girl / 3.0 per friendship", 034's says "pick an edge end → 3.00 / pick a
person → 2.99". Say what is being averaged on 034.

---

## Done by me this round

`check_render.py`'s `NODE_FILLS` now includes annotation gray. Two round-4 fixes recoloured discs to
gray — the quiz sketches so a disc could be told from its edge, and `assortativity`'s non-hub nodes
— and both silently left the size gate, which went on printing a confident "435 discs, 27–40px"
while 28 discs on one slide and 15 on another were not among them, including the ones whose
clearance had been a Blocker two rounds earlier. Nothing was out of band, which is the point: the
number was true and the coverage it implied was not. The gate now measures **453 discs at 27–42px**
and still exits 0. Black cannot be added — the edges are black, and a graph would come back as one
disc.

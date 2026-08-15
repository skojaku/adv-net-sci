# FIXES R4 — m02

Round 4. **Blockers 3 · Majors 5 · Minors 6** so far (slides 1–31 still to report).
R1 16/35/39 · R2 5/18/26 · R3 4/20/28 · R4 3/5/6.

**Settled and verified this round — do not re-litigate:**
- **The band's originating defect is closed.** A reviewer measured the drawn rectangle
  against the drawn curves: left edge L/L0 = 0.498 against a ≤ 0.50 rule, right edge
  C/C0 = 0.805 against a ≥ 0.80 rule, both to within 2px, and both constraints hold
  *inside* the band. It no longer sits where its own claimed property fails.
- Slides 86/87 (grid question/answer), slide 85's σ = 1.56 arithmetic, and the `cols`
  column centring on all 17 slides in range are all confirmed fixed on the render.
- S1–S5 all pass; all six milestones carry an activity.

---

## 1 · Blocker — slide 93: a ✗ marks the shortcut that is not cut

`assert_marks_own_edge` is **defined and never called** — `grep -c` returns 1, the
definition line — and run against `fig_m03_teaser`'s own geometry it fails:
`the mark on (9, 14) touches [[3, 13], [9, 14]]`. Its docstring names this figure and this
failure. The only gate in force checks the two marks against *each other*, which the
docstring itself calls the wrong question.

This is the **second** uncalled guard this build: `assert_planar` sat uncalled through two
rounds while the figure it was written for shipped 34 crossings.

**Fix (figure agent):** call it, let it fail, then move the mark along its own chord until
it clears the chord it does not mark. Then audit every other guard in the file the same
way — for each one, name the figures it is called on, and prove it fires by breaking one
deliberately.

## 2 · Blocker — slide 89: the figcaption's colour key is not in the drawing

Caption: "red: independent edges — gray: coupled ones". Measured: **zero** accent-2 pixels
in the drawing area; all 617 red pixels are in the right panel's heading text. The only
gray lines are the dashed non-edges, and they sit inside the panel headed "edges are
independent" — so a student following the caption reads the independent panel's lines as
the coupled ones. The deck has trained this "red: … — gray: …" grammar on five other
slides, so it will be read as an in-figure key.

**Fix (deck agent):** describe what is drawn — "left: a fixed number of edges, dealt —
right: one coin per pair, dashed where it came up tails" — or drop the colour words, since
the two panel headings already carry the contrast.

*Note for the gate:* my caption-colour check passed this, correctly by its own
specification — the figure does contain red. The defect is that the caption names an
**encoding** red does not carry. A pixel count cannot see that; it stays a review finding.

## 3 · Blocker — slide 76: the deck quotes a number the figure no longer computes

Body says "a factor of five in $p$" — the old grid-snapped band. The generator now prints
factor 15, and after the resample it will print something else again. Third round in which
this rectangle and its sentence disagree.

**Fix:** the sentence must be written from the generator's output, not edited by hand.
Figure agent: have the build print the exact clause the deck should carry. Deck agent:
paste it. Do not paraphrase.

## 4 · Major — slide 43 spends a convention the deck introduces 40 slides later

Slide 43 prints C̄ = 5/21 = 0.24 for the seven-person chain. Node G has degree 1, so its
C_i is undefined; 5/21 is only reachable by counting it as **zero**, which slide 83
introduces as new. Verified:

    sum C_i = 5/3
      / 7  (leaf counted 0 -- the standard definition)  = 5/21 = 0.2381
      / 6  (leaf dropped -- a variant)                  = 5/18 = 0.2778
    nx.average_clustering divides by n: 0.2381

Slide 43's own body even says "every node the same weight — hub or **leaf**". So slide 82
asks the room to spend 30 seconds on something the deck answered on screen in Part Three.

**Decision — take the second option, not the reviewer's preferred one.** Averaging over
the six defined nodes would make the deck's C̄ non-standard: the textbook definition, and
`nx.average_clustering`, divide by n. Teaching a variant to protect a later question is the
wrong trade.

Instead: **say it on slide 43 where it is first used, and sharpen slide 82 rather than
soften it.**
- Slide 43 (deck): add a clause — "G has a single friend, so it has no pairs at all; we
  count it as zero here." One sentence, no number changes, C̄ stays 5/21.
- Slide 82 (deck): reframe the question so it interrogates what the deck has been doing
  rather than pretending the case has not arisen — "We have been counting G's coefficient
  as zero since Part Three. Is that a fact, or a choice?" Slide 83 then supplies 0/0 and
  the word *convention*, which is a stronger Part Six beat than asking a question the room
  can already answer.

## 5 · Majors and Minors from slides 32–62

- **Blocker→now Major, slide 46** — the five shaded wedges are unnamed, and the figcaption
  ("every triplet counted once, at its centre node") makes them read as *the triplets*,
  five of them, on the slide that derives 55. The `5` in `3 × 5 / 55` exists on the slide
  only as the count of shaded shapes, and the deck never states the windmill has five
  triangles. **Figure:** restore a gray in-figure line, "5 triangles shaded". **Deck:**
  caption the shading, not the triplets.
- **Slide 46** — `+ 10 blades = 10, so 55` is not readable arithmetic and uses the wrong
  noun. **Figure:** `+ 10 blade nodes × C(2,2) = 10`, then `45 + 10 = 55` on its own line.
  (The split reported as landed in R3 is not in the rendered figure.)
- **Slide 57** — reuses slide 54's `er-coin.png` unchanged while claiming a per-node
  reading the drawing does not contain. **Figure:** emit a second file with one node
  ringed and its n−1 coins picked out.
- **Slide 60** — the y-axis title still runs into its tick labels: 4.5px separation against
  a 5px gap *inside* the label "10". `assert_boxes_clear` is never called for this figure.
  **Figure:** move the title and wire the assertion.
- **Minors:** slide 72's run-on legend needs an em dash; slide 90's "three orders of
  magnitude apart" must name the quantity ($n$); slide 91's middle panel heading should not
  be red when red means rewired edges; slides 35/43/48/51/59 have the figcaption glued to
  the body paragraph (theme: raise the caption's bottom margin); slide 35 states one claim
  three times; slide 47's caption names red for something not drawn in red.

---

## 6 · The pattern to fix, not just the instances

Two of this round's three Blockers are guards that exist and do not run, and the third is a
number that drifted between two files. Neither is a drawing problem. Before round 5:

- **Every guard is called, and proved to fire.** For each assertion in the generator, list
  the figures it runs on and break one deliberately to see it fail. A guard whose docstring
  describes a defect it never checks reads as coverage and is worse than nothing — this is
  now twice.
- **Every number the deck quotes from a figure is emitted by the build.** The band has
  disagreed with its sentence in three consecutive rounds because a human retyped it each
  time. Print the clause; paste the clause.

---

## 7 · From slides 1–31 (0 Blockers, 1 Major, 4 Minors)

### 7.1 · Major — slide 30: R3 1.11 was never applied

`figures/worksheet-a-answer.png` is dated **21:38**, before the render. Measured on the
current slide: **zero accent-2 pixels anywhere in the network drawing**; all eight edges are
ink black, and the red is confined to a text line above and one below. The figcaption says
"the four answers, **on the network**" and describes a figure that does not exist.

**Figure agent:** trace each answered pair's shortest route in accent-2 with its number at
the route — slide 28 already establishes the device four slides earlier. Then confirm the
file's mtime moved.

### 7.2 · Minor, but fix it — the same chain sits at eight different heights

Disc-centre y across slides 18/20/21/22/26/28/29/30: **279, 363, 337, 291, 301, 298, 301,
301**. The x positions and disc sizes are identical, so only the vertical position moves —
and it moves most between 20 and 21 (a question and its answer on the same figure) and
between 21 and 22 (a build step adding one chord). The five slides without `_class: mid`
land within 10px of each other; the three with it swing.

**Deck agent:** drop `_class: mid` from slides 18, 20 and 21. A build that jumps 83px
between a question and its answer is not a build.

### 7.3 · Minor — slides 28 → 29: the diameter is answered before it is asked

Worksheet A's fourth question is "and the diameter?", but slide 28's in-figure label reads
"one of the 4 worst pairs — **3 edges**" over the same graph. The three distances are
genuinely new work; the diameter is not.

**Figure agent:** shorten slide 28's label to "one of the worst pairs". **Deck agent:**
nothing — slide 30 becomes where 3 first appears.

### 7.4 · Minor — slide 9's "six hands" (R3 2.10.1, still unfixed)

Figure says "six **hands**", body says "six **links**", slide 21 says "seven people";
counting hands on the drawing gives 7. **Figure agent:** "six links, Omaha to Boston".

### 7.5 · For the lecturer, not for us — slide 5's palette

The map carries six off-palette colours including **61px of green** (`#05AE3C`, a star at
Boston), against the guide's flat "no green", plus a four-hop route and four colour-coded
states that the caption does not explain. R3 settled that this is his asset and his call, and
that stands. Raise it with him; do not change it.

### 7.6 · Verified landed on the current render (do not re-report)

Slide 23's route solid black (one continuous 120-column ink run, zero dash gaps); slides
26/28 chord clear of every label glyph; slide 16's neighbours white; `cols` centring on all
ten two-column slides in range; slide 5's caption. Slides 25 and 27 could not be judged —
their figures are newer than the render, and `apl-shortcut.png` opened directly shows the
mean rule in front of the discs, so that fix is real but not exported.

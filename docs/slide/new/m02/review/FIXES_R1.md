# FIXES R1 — m02

Round 1. Five reviewers over disjoint ranges + the lead. Totals across the deck:
**16 Blockers · 35 Majors · 39 Minors.** Verdict FAIL.

**Deck edits and figure edits go to separate agents. Neither opens the other's file.**
The lead owns `check_render.py` and the three guide files.

Where a defect is a *class*, the fix goes in the generator with an assertion, not on the
named figure (`REVIEW_PLAYBOOK.md`).

---

# PART 1 — `figures/make_figures.py` (+ `make_animations.py`) — FIGURE AGENT

## 1.1 · Blocker — every label in the deck is 17% too small (root cause found)

Stock Computer Modern has no 30pt design size, so LaTeX silently substitutes 24.88pt:

    LaTeX Font Warning: Font shape `OT1/cmr/m/n' in size <30> not available
    (Font) size <24.88> substituted

Measured on a minimal case: cap height **17.0bp** without `lmodern`, **20.5bp** with it.
`CAP_RATIO = 0.70` was therefore fiction, and the `TEXT_MIN_PX` assertion never saw it
because it **computed** the size from `FONT` instead of measuring the render.

Do both halves:

1. Add `\usepackage{lmodern}` to `PREAMBLE`, immediately after `\documentclass`.
2. **Replace the computed assertion with a measured one.** At module import, compile one
   calibration figure containing `H` at `FONT` pt, measure its ink height in bp, and store
   it as `CAP_BP`. Assert `CAP_BP * factor >= TEXT_MIN_PX` in `emit()` for every figure,
   and assert at import that `CAP_BP >= 0.66 * FONT` so any future silent substitution
   fails the build instead of shrinking the deck.
3. Fail the build on the substitution directly too: if `pdflatex`'s log contains
   `Font shape ... not available`, raise.

## 1.2 · Blocker — text drawn outside the canvas vanishes silently

`fig_fanout_solve` writes its x-axis title at `y = y0 - 62 = -2`. It is simply absent from
the figure. The canvas-edge assertion only catches ink *touching* the border, so ink fully
outside it passes.

Add a coordinate-bounds check to `emit()`: parse every `at (x,y)` and every explicit
coordinate pair out of the body and assert `0 <= x <= w` and `0 <= y <= hmax`. This is
exact — the generator writes those numbers.

## 1.3 · Blocker — slides 66/67: the "random" graph is not triangle-free

`RND16 = nx.gnm_random_graph(16, 32, seed=2)` has **three triangles** ({1,5,8}, {5,10,14},
{11,14,15}) and C̄ = 0.054. The deck says "nothing closed" / "no triangles". The assertion
`RND16_C < 0.10` was too weak to catch it.

Pick a seed whose 16-node, 32-edge graph is connected and genuinely triangle-free, and
assert `sum(nx.triangles(RND16).values()) == 0` — the same assertion `fig_free_vs_not`
already carries. If no such seed exists at m = 32, say so and switch the claim to the
measured number instead (see 2.6).

## 1.4 · Blocker — `fig_sigma_def` builds its tick labels and never draws them

The loop binds `lab` to `$\sigma < 1$`, `$\sigma \approx 1$`, `$\sigma > 1$` and then emits
only `seg(...)`. The rendered number line has three bare ticks and not one number, so
σ = 1 — the whole point of the slide — is marked by an unlabelled gray dot.

Emit the three labels under their ticks; put "1" under the dot; start the accent-2 segment
**at** the dot (currently 0.58 vs the dot at 0.5, leaving a gray gap). Also delete the σ
definition from inside the figure — the slide's formula panel already carries it — and give
the freed height to the labelled axis.

## 1.5 · Blocker — `fig_a3_walks` draws every triangle edge twice, with no arrowheads

Six arcs among three nodes and no direction anywhere, on the one slide whose job is
counting. A student counting edges counts 6.

Draw the triangle **once** in black. Outside it, add two arrowed arcs — one accent-2
clockwise, one accent-3 anticlockwise — each with a visible arrowhead.

## 1.6 · Blocker — `fig_er_clustering`: an unexplained 59px ring

A hollow accent-2 ring, larger than every node disc, floats on one of the ten pairs. It
reads as an extra node, or as "this pair is special" — the opposite of the slide's point
that all ten pairs are the same coin.

Cut the ring. The in-figure line already says "each of the 10 pairs: its own coin".

## 1.7 · Blocker — content errors: the labels contradict the edges they name

`NAMES = [farmer, buyer, teacher, minister, printer, clerk, broker]`, `CHORD = (0, 2)`,
`SHORTCUT = (1, 5)`. The drawings and all the arithmetic are right; the labels are wrong.

* `fig_chain_chord`: "the buyer already knew the teacher" → **"the farmer already knew the
  teacher"**.
* `fig_chain_shortcut`: "one long edge: the printer knows the buyer" → **"one long edge:
  the clerk knows the buyer"**.

**Then build both strings from `NAMES` and the edge tuple** so a label can never disagree
with its edge again.

## 1.8 · Blocker — accent-2 means two things at once

* `_names()` colours name index 6 accent-2 unconditionally. On the Part Two figures accent-2
  has been reassigned in the same picture to the edge counters, the chord, the shortcut and
  the diameter route. Add a `highlight=None` parameter; pass `highlight=6` only from
  `fig_milgram_chain`, whose caption explains it.
* `fig_distance_def`: three discs in two colours with nothing explaining the split, and the
  slide defines $d(i,j)$ while no node is labelled $i$ or $j$. Make all three discs accent,
  label the two ends `$i$` and `$j$`, and let accent-2 mark only the two route edges and
  their counters.
* `fig_milgram_map`: Boston is drawn at `DOT + 8` = 34bp against 26bp for Omaha and Wichita.
  Size encodes nothing here — make all three the same.
* `fig_cbar_milgram`: the three nonzero $C_i$ values are accent-2 and the four zeros are
  gray — an unstated encoding that also collides with accent-2's job as the result line. Set
  all seven values in ink black; keep accent-2 for the result line only.
* `fig_lattice_vs_random`: the left panel label is accent-2, the right black, for no reason.
  Both black.
* `fig_ws_rewire_step`: the red in-figure line names the **gray** thing ("the gray stub is
  where that edge used to end") while the gray figcaption names the **red** thing. Draw each
  annotation in the colour of the element it names, next to that element.

## 1.9 · Blocker — `fig_sw_map` panel 3 contradicts its own axis

The caption says "red: the rewired edges"; panel 3 sits at the far end of the *p* arrow and
draws all 24 edges black, because `new = k == 1 and ...` only ever fires on the middle
panel. Build panel 3 by rewiring the lattice at p = 1 (not a fresh `gnm_random_graph`) and
colour every edge that has moved off the lattice.

## 1.10 · Major — the ring lattice draws 16 crossings on the "triangles are everywhere" slide

Every second-neighbour chord bows inward, so each crosses its two neighbours. C₁₆(1,2) is
planar (`nx.check_planarity` → True) and admits a zero-crossing drawing.

In `_ring`, bow skip chords with even `i` inward and odd `i` outward. **Assert the crossing
count is zero** for the lattice — count intersections between all pairs of drawn Bézier
paths with disjoint endpoints.

## 1.11 · Major — free-standing dots are under the floor

`DOT = 26` lands at 22px measured on the rendered slide (the antialiased colour mask shrinks
a small disc by ~2px a side). Slides 8, 60, 61 and 85 all fail the node band now that the
gate works. Raise `DOT` to **32**.

## 1.12 · Major — `fig_fanout_solve` has no y axis and a silent log scale

`Y(v)` is logarithmic and nothing says so, so exponential fan-out renders as a straight
line — the opposite of the slide's point. Label the vertical axis "people reached" with
decade ticks, restore the x-axis title **inside** the canvas, and right-align the "8 billion
people" label clear of the last dot (it currently overprints it: "8 billion p⬤ple").

## 1.13 · Major — `_sweep_frame` has a bare y axis on both slides that use it

Slides 72 and 73 assert how far each curve has fallen and neither says the axis runs 0 to 1.
Tick and label the y axis at 0, 0.5, 1 and title it "fraction of the lattice value".

## 1.14 · Major — the small-world band is 1.39 decades, not two

The band runs p = 0.004 → 0.1 = a factor of 25. Either move the left edge to **p = 0.001**
so "two decades" is true, or tell the deck agent to reword (see 2.7). Pick the first: change
`X(0.004)` to `X(0.001)`, and assert the drawn band spans ≥ 2 decades.

## 1.15 · Major — `fig_ws1998_dots` cannot deliver the exercise it is used for

Slide 60 asks students to read both ratios off the axis. The three L/L_rand dots (1.22,
1.51, 1.18) land within 17px of each other on a log axis where a decade is 158px. Print the
numeric value beside every dot — both ratios, all three rows.

## 1.16 · Major — sweep noise reads as "L rises with p"

At 6 runs the first three p values expect 0.16 / 0.34 / 0.74 rewirings out of 1600 edges, so
L/L(0) goes 0.964 → 0.928 → 0.960. Raise `runs` to 24 for the first three points (or start
the sweep at 10⁻³) and delete `_sweep.json` so it recomputes.

## 1.17 · Major — `fig_grid_no_triangles`: the annotation sits on the top row of discs

Text at `y = 340`; the top row occupies y 310–350. Move the annotation below the grid, where
every other figure in the deck puts it.

## 1.18 · Major — `fig_gnm_gnp` forces a crossing on a tree

`GNM_EDGES` is a 5-edge tree, so a crossing-free drawing exists, but the hexagon layout
interleaves two of them. Choose five edges that draw planar on the hexagon (e.g. five of the
six boundary edges) and **assert zero crossings**. One change fixes both panels on slides 83
and 84.

## 1.19 · Major — `fig_m03_teaser`: the two X marks overlap into one scribble

Both land near the chords' crossing point, so the render X-es out the crossing rather than
either edge. Put one X at the midpoint of each cut edge, well separated, and draw the two
cut chords dashed so "removed" reads without the marker.

## 1.20 · Major — `fig_transitivity_def`: the triangle fill is invisible

The fill samples `#f2e1de`, a 7% tint, while the caption names it. Raise to a 20–25% tint.

## 1.21 · Major — accent-3 is too light to be text or a thin stroke

Slide 23's gold "2 edges" label measures **2.01:1** contrast against white where the red
annotation on the same figure measures 5.53:1 — below the 3:1 floor. Draw `fig_two_routes`'
replaced route and its label in annotation gray. **Then make it a rule:** accent-3 is for
fills and rings only — never text, never a stroke under 4bp. Assert it in the generator.

## 1.22 · Minors (figure side)

1. `fig_apl_chain` — the mean rule overruns the dot field by 119px left and 135px right.
   Clip it to the dot field plus a small overhang.
2. `fig_apl_shortcut` — the mean rule crosses the "d = 2" row label and reads as a
   strikethrough. Start the rule right of the row labels.
3. `fig_wikirace` — delete the dotted Bagel→Chopin edge: it is an unexplained edge style, and
   if real it makes the route two clicks, contradicting the figure's own "three clicks"
   label. Also move the "Chopin" and "Piano" labels outside the path's turn — the red edge
   currently runs through the last two letters of "Chopin", and the label is partly behind
   its disc.
4. `fig_milgram_map` — the coastline strikes through the "Boston" label at cap height, and
   the label abuts the red disc. Move it clear.
5. `fig_milgram_rule` — the in-figure sentence repeats eleven consecutive words of the slide
   body. Cut it; the three-node hop and the sender / you / next hop labels carry it.
6. `fig_shortcut_effect` — the gold rings mean "closer to node 0", but node 0 is an ordinary
   blue disc and is never named. Ring the source node in accent-3 too.
7. `fig_recap` — the deck's caption says "a few shortcuts"; the figure draws exactly one.
   Draw a second chord.
8. `fig_universality` — the axis has no name. Add "small-world index" beneath it. (No `$`.)
9. `fig_sigma_lt_1_q` — cut "high clustering" from the in-figure label, leaving "a ring
   lattice: long routes". It is half the answer on a question slide (N4).
10. `fig_random_graph` — 109 crossing pairs makes the triangle claim uncheckable. Thin the
    stroke, or accept it and let 1.3's caption carry the number.

---

# PART 2 — `m02-small-world.md` — DECK AGENT

## 2.1 · Blocker — nine figcaptions and one roadmap item render LaTeX literally

KaTeX does not process `<figcaption>`, or any raw HTML block. `check_render.py` now fails
the build on this, so the gate will list them. Rewrite in words — no `$`:

| current | replace with |
|---|---|
| `one triangle at $i$, degree two: $C_i = 1$` | `one triangle, degree two` |
| `each node's own $C_i$, printed beneath it` | `each node's own value, printed beneath it` |
| `one step reaches $\langle k \rangle$, two steps reach $\langle k \rangle^2$` | `one step reaches k friends, two steps k squared` |
| `gray: $L/L_{\mathrm{rand}}$ — red: $C/C_{\mathrm{rand}}$, on a log axis` | `gray: the path-length ratio — red: the clustering ratio, log axis` |
| `every network sits far to the right of $\sigma = 1$` | `every network sits far to the right of the random baseline` |
| `the two extremes, same $n$ and same $m$` | `the two extremes, same nodes and same edge count` |
| `gold: two decades of $p$ where both hold` | `gold: two decades of rewiring where both hold` |
| `the ring at $p = 0.14$` | `the ring at fourteen percent rewiring` |
| `fixing $m$ couples the edges to each other` | `fixing the edge count couples the edges to each other` |

Roadmap item 04 (`<div class="steps-list">`): `the index $\sigma$` → `the index sigma`.

## 2.2 · Blocker — two figures are used in the wrong container

`transitivity-def.png` (slide 44) and `fanout-solve.png` (slide 57) are authored full-width
and placed inside `<div class="cols">`, so they render at 48% scale — 19px node discs and
12px cap heights. Move both slides to the full-width stacked layout
(`<div class="fig tight">` with the text above), as slides 56/60/61 already do.

## 2.3 · Blocker — slide 33 "Triangles and triplets" defines two terms

Split into two slides, paired with the figure build the figure agent is emitting:

* **"Triangles"** — `triangle-only.png`. One point: three mutually connected nodes are a
  **triangle**.
* **"Open and closed triplets"** — `triangle-triplet.png`. One point: any three nodes with
  two edges are a **triplet**; the triangle is the closed case.

## 2.4 · Blocker — slide 82 makes two claims about two networks

Split into a build:

* **"Not the lattice"** — figure `ring-lattice.png`. Point: a ring lattice's clustering
  advantage beats its distance penalty, so σ > 1. State the size: **σ ≈ 5 for a ring of a
  thousand nodes; even the 16-node ring above scores 1.56.** (Verified: 1.56 / 3.19 / 4.96 at
  n = 16 / 100 / 1000.)
* **"You have to kill the triangles"** — figure `grid-no-triangles.png`. Point: a square
  street grid has no triangle at all, so C = 0 and σ = 0.

## 2.5 · Blocker — slide 38 leaks its own answer

The formula panel asks what $(\mathbf{A}^3)_{ii}$ counts and the italic line beneath reads
"*30 seconds — a walk of length three that starts and ends at i.*", which is the answer.
Cut the second clause: leave "*30 seconds.*"

## 2.6 · Blocker — slides 66 and 67 claim the random graph has no triangles

It has three (C̄ = 0.054). If the figure agent finds a triangle-free seed the prose can
stand; if not, change both to the measured claim — "clustering falls from 0.5 to 0.05".
**Coordinate with the figure agent before writing either version.**

## 2.7 · Major — slide 73 "two orders of magnitude"

The figure agent is widening the band to p = 0.001 so the claim becomes true. If they report
they could not, reword to "more than a decade wide — a factor of twenty-five".

## 2.8 · Major — two slides run under the page number

Slides 45 and 47 render ink to y = 679 and y = 681; the page number sits at y 616–630, so
the digits print inside the text. `CONTENT_BOTTOM` is now 660 and the gate fails both.
Slide 45: cut the paragraph to two lines. Slide 47: drop the trailing "and averaging all
seven gives C̄ = 5/21" — the figure already prints it. Slide 87's last bullet has the same
problem: shorten to "Watts–Strogatz: a few shortcuts buy short routes".

## 2.9 · Major — three worksheets ask for numbers already on screen

* **Worksheet A (slide 29).** Slide 27 prints "mean 38/21 = 1.81" and slide 28 draws
  d(A,G) = 3. Ask instead for **d(A,E), d(D,G), d(B,G)** and the **diameter**. The figure
  agent recomputes and asserts all four; do not type numbers into the deck.
* **Worksheet B (slide 46).** Slide 41 already prints all seven $C_i$ values. Ask the figure
  agent to strip the per-node values from `cbar-milgram.png` (that slide's point is the
  averaging, not the individual values) — then the worksheet has something left to compute.
* **Slide 47.** The three `*` fragments reveal values the figure above already shows
  statically. Ask the figure agent for a `worksheet-b-answer.png` without the value row, so
  the fragments are the only reveal.

## 2.10 · Major — slide 45 lands five components at once, static

Full-width figure with three baked annotations, a figcaption and a three-line paragraph
carrying two contrasts plus a conclusion. Make the paragraph two `*` fragments **above** the
figure.

## 2.11 · Major — slide 65 puts a paragraph below a fragmented list (L5)

"Distance grows **linearly** with n — the opposite of what we measured." sits under two `*`
bullets. Make it a third fragment.

## 2.12 · Major — Part Six has no milestone activity (S5)

The only part of six without one. Add a hand computation on the street-grid slide: *"Count
the triplets around one intersection: how many are closed? 60 seconds."* — it lands directly
on the transitivity definition from Part Three.

## 2.13 · Major — slide 13's caption contradicts its own figure

"bigger network, shorter distance", but the Facebook dot (4.74) is drawn to the **right** of
the email dot (4.0). Caption what is drawn: "eight hundred times the people, still under
five".

## 2.14 · Minors (deck side)

1. `<!-- _class: mid -->` on slides 6, 10, 18, 19, 20, 21, 57, 59 — all carry 220–273px of
   empty frame.
2. Slide 35 — move the "Take 20 seconds" prompt inside the left column; it currently sits
   outside the `cols` div, leaving a 335px hole.
3. Unbold stress-only `strong`: "**among those five**" (34), "**2.67**"/"**1.81**" (27),
   "**two ways**" (39), "**nodes**"/"**triplets**" (45), "**4.74**" (49), "**structureless
   network of the same size**" (52), and the two city names on slide 5 (they are blue on the
   map while red points at Boston). Bold marks terms only.
4. Slide 30 — the two `*` bullets restate the figure verbatim, and `3 · d(B,E)` reads as a
   product. One equation per fragment.
5. Retire figcaptions that repeat the in-figure line word for word: slides 19, 36, 58, 74,
   78, 80, 81, 88. Give each a fact the drawing does not carry, or delete it.
6. Slide 9 — cut the in-figure red label duplication by dropping "six" from the figcaption's
   neighbourhood; "six" currently appears four times on one slide.
7. Slide 18 — drop the in-figure title (three text layers say one thing).
8. Slides 80 and 82 — shorten the bullets so an inline formula does not wrap at its relation
   sign and strand a lone "0." on the next line.
9. Slide 84 — write $C_{\mathrm{rand}} = p$, not $E[C_i] = p$; the deck has never used
   $E[\cdot]$.
10. Slide 2 promises "we come back to it twice" and nothing ever does. Add the callback on
    slide 21 ("Six") and slide 13 (Facebook's 4.74).
11. Drop the timing from the two ritual prompts on slides 38 and 43; keep the ones on 50 and
    53, which are followed by their answer slides.
12. Slides 37, 42, 44, 51 — the body restates the figure's own annotation almost verbatim.
    Keep the number in one place. Deleting the duplicates also buys back the lines slide 45
    needs.

---

# PART 3 — the lead

* `check_render.py` — **done this round**: node discs found by colour instead of luminance
  (the band was inert on this palette), part-divider bands masked out, `CONTENT_BOTTOM`
  lowered from 690 to the theme's real content box at 660, plus two new source-level gates
  (math inside a raw HTML block, and figure-authored-width vs container-used-in).
* `FIGURE_GUIDE.md` — add: measure the rendered cap height, never compute it; accent-3 is
  fills and rings only; assert the crossing count on any figure whose claim is a triangle.
* `REVIEW_PLAYBOOK.md` — add: a build gate that cannot fire is worse than no gate, because it
  reads as coverage. Check that each gate's threshold actually matches the artefact.
* `DECK_BUILD_GUIDE.md` — add: a figure authored for one container and used in the other
  renders at 48%; the deck and the generator must agree, and now the gate checks it.

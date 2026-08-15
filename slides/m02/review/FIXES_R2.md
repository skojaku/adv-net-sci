# FIXES R2 — m02

Round 2. Four reviewers over the 90 slides. **Blockers 5 · Majors 18 · Minors 26**
(round 1: 16 · 35 · 39). Severity class has fallen as it should — round 1's blockers were
tables, a missing act and a gate that could not fire; round 2's are figure geometry, a
definition that does not produce its own number, and three captions naming the wrong thing.

**Deck edits and figure edits go to separate agents. Neither opens the other's file.**
The lead owns `check_render.py`, `network-science.css` and the guides.

---

# PART 0 — the cross-cutting one, do this first

## 0.1 · Blocker — the scale model is wrong for 68 of 90 slides (FIGURE + LEAD)

Two reviewers found this independently. The generator asserts one slide-pixels-per-bp
factor per container (col 1.033, full 1.018). Neither number is what the theme applies.
Measured on the rendered deck, disc by disc, on discs the generator draws at a uniform 40bp:

| container in the deck | discs measured | implied px/bp | generator assumes |
|---|---|---|---|
| `cols` column | 32–42px | 0.800–1.038 | 1.033 |
| `fig` full width | 38–40px | 0.950–0.988 | 1.018 |
| `fig tight` full width | 34–38px | 0.850–0.938 | 1.018 |

Two separate causes, both read straight out of `network-science.css`:

* `section p { max-width: 1080px }` (line 144). Marp wraps the image in a `<p>`, so a
  full-width figure is bounded at **1080**, not 1120. Factor 1080/1100 = **0.982**.
* `section .fig.tight img { max-height: 320px }` (line 277) and
  `section .fig.stack img { max-height: 190px }` (line 279). For the 16 `fig tight`
  slides the **height** binds, not the width, and the factor drops to ~0.87.

Consequence: the x-height floor that round 1 spent its whole budget getting right is
**still not met on the `fig tight` slides** — 13–14px measured against a 15px floor on
slides 8, 16, 45 and 46 — and the gate passes them because it uses 380 for everything.

**Figure agent:** `emit()` must take the container the deck actually uses, including the
modifier, and compute `scale = min(width_cap / file_w, height_cap / file_h)` from the real
caps: width 537 for `cols`, 1080 for full width; height 380 for `fig`, 320 for `fig tight`,
190 for `fig stack`. Parse the deck for which class wraps each figure rather than taking it
from the `FIGURES` table — the table records intent, the deck records fact, and they have
already disagreed twice. Then assert the x-height against the resulting factor, and shorten
the canvases of the `fig tight` figures until they clear it.

**Lead:** the same three caps go into `check_render.py`, and the container check compares
against them.

---

# PART 1 — `figures/make_figures.py` / `make_animations.py` — FIGURE AGENT

## 1.1 · Blocker — `free-vs-not`: 34 crossings on a planar graph, under a "no triangle" caption

`nx.check_planarity(RND12)` is True and a zero-crossing drawing exists; the drawn layout has
**34 crossings across 14 edges**, and the crossings manufacture apparent triangles directly
under a caption asserting there are none. `assert_planar()` already exists and is applied to
the G(n,m) panel — it was never applied to the one figure whose claim is the absence of
triangles.

Lay `RND12_POS` out from a planar embedding (`nx.combinatorial_embedding_to_pos`) and add
`assert_planar` to `fig_free_vs_not`.

**Generalise it while you are there** — a reviewer measured the two gaps that let this
through, and closing them is one pass:

* `assert_planar` exists and is called on exactly one figure. Call it on **every** figure
  whose graph `nx.check_planarity` calls planar. `fig_routing_vs_existence` currently draws
  zero crossings by luck of layout, not by gate.
* `clearance_ok` tests **straight segments only**, so every curved edge in the deck is
  unchecked at source — the chord on slide 22 and the arc on slide 23 had to be measured off
  the render by hand. Sample the Bézier paths the way `curve_edge` already does internally.

## 1.2 · Major — the same figure prints "3 hops across" for a graph of diameter 4

`RND12_PATH` takes the farthest node **from node 0** — that is the eccentricity of node 0
(3), not the diameter (4). Verified: eight pairs sit at distance 4. Seven slides later the
ring figure prints the same phrase and *does* assert it equals the diameter.

Use a diameter-realising pair and add `assert len(RND12_PATH) - 1 == nx.diameter(RND12)`.

## 1.3 · Major — the ring lattice's 16 crossings, and the layout that dissolves the trade-off

Round 1 traded crossings for legible triangles and recorded the reasoning; a reviewer
confirmed the trade was reasonable, and then supplied the layout that gets both.

**C₁₆(1,2) is the 8-antiprism.** Put the even nodes on an outer ellipse and the odd nodes on
a concentric inner one: the +2 edges become the two octagons, the +1 edges the zigzag
between them. Zero crossings, and all 16 triangles draw as triangles rather than lenses.
Add `assert_planar` to `_ring()`.

If it does not come out legible, keep the current drawing and say so in your report — it is
then a recorded decision, and I will mark it wontfix so round 3 stops re-reporting it.

## 1.4 · Major — `ws-rewire.gif`: the caption is clipped at both ends on every frame

Rendered text reads `ewired so far: 0 of the 32 lattice edge`. Six ink pixels in column 0
and seven in the last column, on frames 0, 3 and 6. The label is ~6% wider than the canvas
and the crop is full-width, so nothing rescues it.

Shorten to `rewired: {n} of 32`, and port `emit()`'s canvas-edge assertion into
`make_animations.py` so a clipped frame fails the build.

## 1.5 · Major — `a3-walks`: the second walk is a thin gold stroke

Measured 2.01:1 against white where accent-2 on the same figure measures 5.61:1, and the
caption asks the room to tell the two apart by colour. Draw both directions in accent-2,
offset to opposite sides, and distinguish them by arrowhead direction.

## 1.6 · Major — `a3-formula`: the triangle's edge strikes through the exponent

The accent-2 edge runs through the numerator glyphs of $(A^3)_{ii}$ and crosses out the
**3** — the one symbol the slide teaches. Move the formula clear of the drawing and assert
no glyph box intersects a drawn path.

## 1.7 · Major — `ws-band`: the annotation is the wrong colour and sits outside the band

"both at once" is accent-2, which already labels the C curve in the same figure, and it is
positioned entirely to the right of the gold band it names. Set it `annot` and centre it
over the band.

## 1.8 · Major — `shortcut-effect`: a red legend describing gold rings

The legend is accent-2, the rings are accent-3, and accent-2 is also the shortcut chord in
the same drawing. Set the legend `annot` — not accent-3, which fails contrast.

## 1.9 · Major — slide 83 reuses slide 65's file unchanged

The answer slide shows the question slide's drawing with nothing added, and its in-figure
line still reads "joined to its 4 nearest neighbours" — written for a slide 18 earlier.
Emit a third file whose in-figure line carries the arithmetic that settles it:
`C 0.50 vs 0.27 · L 2.2 vs 1.9 → σ = 1.56`.

## 1.10 · Major — `universality` shows strictly less than `ws1998-sigma`

Same three networks, same axis, same baseline — but the row names become "social /
technological / biological" and the σ values are dropped, so the later figure is the earlier
one with its information removed. Keep the network names **and** add each one's size
(n = 225,226 / 4,941 / 282): orders of magnitude apart, same signature. That is the
universality claim, made with evidence.

## 1.11 · Minors (figure side)

1. `six-degrees-timeline` — the rule overhangs the last dot by 30bp below against 20bp
   above; draw it between the dot centres.
2. `milgram-map` — the two dashed arrowheads merge into one smudge and stop 14px short of
   Boston. Land them on different anchors of the disc and close the standoff.
3. `worksheet-b-answer` — drop the C̄ line from the figure (it leads, in the only coloured
   type, while the three asked values reveal one at a time below).
4. `diameter` — four pairs tie at distance 3, and red marks a route, not a pair. "one of the
   worst pairs — 3 edges".
5. `windmill-cbar` / `windmill-split` — the leader line starts on the hub disc at the same
   origin as the ten spokes, so the hub reads as having eleven edges. Start it clear.
6. `windmill-split` — the blade digits `1` are unexplained on this slide; re-label or drop.
7. `ws1998-dots` — the connector encodes the gap and nothing says so; lighten it or state it.
8. `ws1998-sigma` — the σ=1 baseline and the σ dots are both accent-2. Baseline to `annot`.
9. `lattice-vs-random` — its two panels differ in aspect and disc size from the same graphs'
   single-panel versions (1.45:1 ellipse vs circle; 40px vs 34px). Match them.
10. `random-graph` — "shuffled at random: C̄ = 0.24" reads as a prediction of the formula
    named two lines below it. "this draw: C̄ = 0.24".
11. `disconnected-answer` — the slide draws a connector between the one pair it says has no
    route. Drop it; the gap carries the point.
12. `ws-sweep` / `ws-band` — the x axis mixes $10^{-4}$, $10^{-3}$, 0.01, 0.1, 1. One
    convention.
13. `universality` — "σ = 1" collides with the red header on nearly the same baseline.

---

# PART 2 — `m02-small-world.md` — DECK AGENT

## 2.1 · Blocker — slide 22 names the wrong person

The figure's title is generated from `CHORD = (0, 2)` and reads "the farmer already knew the
teacher". The body says "the **grain buyer** already knew the teacher" — B, whose edge to C
is an ordinary chain edge. The figure is the source of truth. Change the body to "the
farmer".

## 2.2 · Blocker — slide 26's figcaption contradicts its own figure

In-figure header: "one long edge: **the clerk** knows the buyer" (generated from
`SHORTCUT = (1, 5)`). Hand-written figcaption: "red: **the printer** turns out to know the
buyer". The generator has a helper whose whole purpose is that a caption cannot name the
wrong pair, and the figcaption bypassed it. Change it to the clerk, or delete it — the
in-figure header already says it.

## 2.3 · Blocker — the deck's definition of "triplet" does not produce the deck's number

Slide 34 defines a triplet as a **set**: "any three nodes with at least two edges among
them". Applied to the windmill that gives **45** triplets, 5 closed → 3×5/45 = 0.33.
Slide 45 prints 15/**55** = 0.27. Both were verified by enumeration:

    windmill: node-set triplets 45 (5 closed) -> 0.333
              centred triplets  55            -> 0.2727 = nx.transitivity  ✓

The deck's 0.27 is correct transitivity, but it needs triplets counted **at their centre**,
so one triangle holds three. The deck never says this — and slide 46's "the hub owns 45 of
55" makes the wrong reading look confirmed, because 45 is exactly the number the wrong
reading produces.

Add to slide 34: a triplet is counted **at its centre node** — the middle node of the two
edges — so a triangle contains three closed triplets. Slide 45's factor of 3 and its 55 then
both follow.

## 2.4 · Major — slide 23's figcaption names a colour that is not on the slide

"red: the shortest route — **gold**: the route it replaces". Zero gold pixels: round 1 moved
that route to annotation gray for contrast, and the caption was not updated. Change to
"dashed gray: the route it replaces".

## 2.5 · Major — slide 84 answers its own activity two lines above the prompt

The body states "A square street grid has no triangle at all. C = 0, and σ = 0 with it." and
then asks the room to count the triplets around one intersection. This is Part Six's only
hand activity.

Split into two slides: the grid figure + the prompt and nothing else, then the resolution
("Six triplets, none closed: C = 0, and σ = 0 with it"). That fixes the leak and gives the
pair a build.

## 2.6 · Major — slide 29's fourth worksheet question was answered on slide 28

Slide 28's prose says "it fell from 6 to **3**" and its figure header says "worst pair in
the whole network: 3 edges"; slide 29 then asks for the diameter. Drop the diameter from
slide 28's prose and let the worksheet establish it.

## 2.7 · Major — slide 55 uses ⟨k⟩ without ever defining it

`\langle k \rangle` first appears inside the punchline formula and then carries five more
slides. Neither m02 nor m01 ever writes "average degree" or introduces the notation. Add one
clause above the formula: "a node has ⟨k⟩ = p(n−1) neighbours on average, so p = ⟨k⟩/(n−1)".

## 2.8 · Major — slide 46: the figure gives away both bullets before they reveal

The figure is emitted after the fragments but is on screen from the start, and it prints
both bullets' content including the second's punchline. Move the figure above the list, or
split into a two-slide build (node-weighted, then triplet-weighted).

## 2.9 · Major — slide 67: three static paragraphs, and the third is a separate argument

The asymptotic sentence ("Grow the network and ⟨k⟩/(n−1) takes it to nothing") is a
different claim from what this 16-node draw measures, and it lands at the same time. Make
paragraphs two and three `*` fragments, or move the asymptotic sentence to slide 68.

## 2.10 · Minors (deck side)

1. `<!-- _class: mid -->` on slides 9 and 33.
2. Slide 14 — the URL breaks across lines at its own hyphen ("wiki-" / "race.com") on the
   slide that asks the room to type it. Shorten the sentence before it.
3. Slide 66 — write $\bar L \approx 125$, not `=` (the value is 125.375; the deck uses ≈ for
   the comparable case on slide 58).
4. Slide 70 — the figcaption repeats the in-figure legend verbatim. Replace with something
   the drawing does not say, or drop.
5. Slide 26 — two arcs are on screen and only red is explained; name the black one.
6. Slides 78, 80, 82 — three of Part Six's four prompts have no thinking beat. Add one line
   each.
7. Slide 86 — the body's last line runs into the page-number box. Cut to two lines.
8. Slides 37, 38, 43, 45 — where a slide ends in a computed number, make that line a
   fragment; the range is otherwise entirely static.
9. Part Six's divider covers four edge cases and then four slides that are not edge cases.
   Rename the card, or add a short closing divider before slide 87.

---

# PART 3 — the lead

* `check_render.py` — teach it the three height caps and the 1080 width cap; make the
  container check compare against them. Without this the gate keeps passing 13px type.
* `FIGURE_GUIDE.md` — add: the container is not what the generator's table says, it is what
  the deck's markup says, and the theme's modifiers change the cap. Read the deck.
* `REVIEW_PLAYBOOK.md` — add: when a fix is reported as landed and a later round measures it
  as absent, believe the measurement (the ring-lattice crossing fix was reported landed in
  round 1 and was still 16 crossings in round 2 — because what landed was a different fix
  than the one specified, for a good reason that was recorded only in a docstring).

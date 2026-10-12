# R1, reviewer A: slides 1–24

Every PNG in the range was opened. Every frame of `roma-to-graph.gif`, `w5-walks.gif`,
`closeness-def.gif`, `harmonic-def.gif` and `ecc-def.gif` was extracted and viewed
(`scratchpad/review_frames/`). Numbers were checked against `python3 smallgraphs.py` (all assertions
pass) and against `data/ny_network.json`.

**Render currency.** `m06-centrality.md` (07:19:32) is newer than `review/slide.001.png` (07:17:04),
so the staleness check prints STALE. No figure is newer than the render. I compared the rendered text of
slides 1–24 against the source line by line and found them identical, so the findings below stand.

**Count:** Blockers 2 · Majors 10 · Minors 17

## Blockers

- **slide 6 — Blocker (F1)** — The discs are shaded in five tones (Londinium palest, Tarraco pale,
  Alexandria darker, Roma darkest) and Roma wears a red crown. Nothing on the slide says what the shade
  or the crown means. — Fix: merge with slide 7 (see slide 7). Replace `roma-degree` with the
  `two-roads-ahead` colouring reduced to two classes: Roma red, its five neighbours blue, every other
  city white. Body: "**Degree**: $d_i = \sum_j A_{ij}$. Roma: 5, the blue cities. Nothing beyond them
  counts." No crown.
- **slide 17 — Blocker (F1)** — On `ny-closeness` the dots vary in both shade and size, with no legend
  and no sentence saying what they encode. Slide 8 has a legend, so its absence here is also
  inconsistent. — Fix: add a legend in the style of slide 8's (two or three dots: "high closeness",
  "low closeness"), or add the bullet "* Darker, larger dot: higher closeness."

## Majors

- **slide 3 — Major (figure/caption)** — The title reads "The roads themselves" and the text reads "The
  main roads of the empire joined these twelve cities", but the map shows no roads, only pins. Also,
  5 of the 18 links that slide 4 draws are sea lanes (Roma–Carthago, Roma–Alexandria, Tarraco–Carthago,
  Athenae–Byzantium, Athenae–Alexandria; `verify_numbers.ROMA_EDGES`), and 2 more include a sea crossing.
  Frames 5–6 of `roma-to-graph.gif` show these lines crossing open sea. — Fix: title "Twelve cities of
  the empire"; text "Roads and sea lanes joined these twelve cities."
- **slide 3 — Major (F3)** — The basemap is too pale to read as a map. Sampled on the slide, sea is
  (225,230,232) and land is (240,241,236), about 12 grey levels apart. A projector will lose the
  coastline. — Fix: rebuild `roma-basemap` without the pale filter, or tint the sea `accent!20`, so that
  land and sea differ by at least 30 grey levels. Apply the same change to frames 1–3 of
  `roma-to-graph.gif`.
- **slide 4 (and 6, 7, same geometry) — Major (F3)** — Edges run through the city names: Londinium,
  Tarraco, Massilia, Mediolanum, Lugdunum, Thessalonica, Alexandria, and "Roma", which is struck by two
  edges (to Thessalonica and to Alexandria). On slide 6 the crown also sits on the Mediolanum–Roma edge.
  — Fix in `romelib`: draw each name after the edges, on an opaque white box (`fill=white, inner
  sep=1pt`). Where a free side exists, move the name there instead: Roma above-right, Massilia below,
  Londinium and Tarraco above. Add a build assertion that no label box meets an edge segment.
- **slide 5 — Major (lecturer order, flow)** — The New York question sits between the Rome network
  (slide 4, "Which city is the most important?") and degree (slide 6, which answers that question with
  Roma). The required sequence is network, then degree. — Fix: move this slide to just before "New
  York: degree". The order becomes 2, 3, 4, 6 (merged with 7), 5, 8.
- **slide 6 — Major (named objects defined)** — $A_{ij}$ appears in the deck's first formula and is
  never defined anywhere in the deck. The deck uses it again on slides 37, 52 and 59. — Fix: add above
  the degree line: "$A_{ij} = 1$ if a road joins $i$ and $j$, else 0."
- **slide 7 — Major (duplicate)** — "degree sees only the blue" restates slide 6's "Nothing beyond them
  counts". The lecturer asked for degree on one slide and for no two slides that say the same thing. —
  Fix: cut slide 7 and move its colouring onto slide 6, as given under slide 6. The merged figure must
  still state what white means. Slide 8 makes a different point (ties) and stays.
- **slide 11 — Major (F4, two axes)** — The slide asks "Which routes count, and how do they become one
  number?", but `grid-empty` draws only the first axis (the row labels "shortest paths" and "walks").
  Nothing tells the room that the black text in a cell answers the second question. — Fix: add two grey
  headers to `grid-empty` and to every later grid: "which routes count" over the row labels, and "how
  they become one number" over the cell area.
- **slide 15 — Major (tricky example, figure cue)** — Both winners are the node nearest the middle of
  their drawing. In `CA_XY` the bounding-box centre is x = 3.25; F sits 0.25 from it, and the next
  nearest node (G) sits 1.05 from it. In `CB_XY` the centre is 2.95; P sits 0.15 from it, and the next
  nearest (Q, T) sit 0.75 from it. On the slide: F is at x≈350 against a drawing centre of ≈360, and P
  is at ≈897 against ≈901. A student who picks the middle of the picture gets both right without
  computing anything. — Fix: re-lay out so that a loser sits at the visual centre. On the left, hang K
  directly below J and spread A–D further left, so that E is the node nearest the centre. On the right,
  fold the Q–R–S arm upward and the T–U arm downward instead of rightward, so that N is nearest. Assert
  in `figs_quiz` that the winner is not the node nearest the bounding-box centre. Slides 16, 18–22
  inherit `CA_XY` and must be rebuilt.
- **slide 21 — Major (ambiguous setup)** — The text says "Left: the same network as before". The slide
  just before (20) showed the cut network, where G wins with 9/2. This slide's left graph has road E–F
  open again, and nothing says so. — Fix: "Left: the closeness quiz network, with road E–F open again.
  Right: two pieces."
- **slide 23 — Major (N4, answer in the same breath)** — The title asks "Would you site a fire station
  on the average?" and the only body line, "A fire station must reach its farthest house in time.",
  answers it. — Fix: delete the body line, add the cue "*Take 30 seconds.*", and retitle "Would you place
  a fire station by its average distance?". Put "A fire station must reach its farthest house." as the
  first line of the left column on slide 24, above the formula.

## Minors

- **slide 2** — The photos have no individual labels; the names appear only in the 16 px credit line.
  "said to" appears in two consecutive bullets, and "BC." is left alone on the second line of bullet 1.
  — Fix: put a label under each photo: "Julius Caesar", "Augustus", "Golden Milestone (remains)". Bullet
  1: "In 20 BC Augustus, Caesar's adopted heir, set up the **Golden Milestone**." Bullet 4: "Plutarch:
  all the roads of Italy end at it."
- **slide 3** — All twelve pins are red, which uses red as a group colour. Londinium sits in the
  frame's top-left corner and Alexandria on its bottom border. — Fix: make the pins accent blue (they
  become the blue discs on slide 4), and widen the crop by about 5% so that no pin touches the frame.
- **slide 5** — "cross-state trips" is vague for what betweenness counts, and this New York slide uses
  paragraphs where the lecturer asked for bullets. — Fix: "* New York State highways: 289 interchanges.
  * Take the shortest drive between every pair of interchanges. Which of these eight cities do the most
  drives pass through?"
- **slide 8** — "Degree cannot tell them apart." also reads as "cannot tell degree 3 from degree 4". The
  text is paragraphs, not bullets. — Fix: "* 201 of the 289 interchanges have degree 3. * Degree gives
  those 201 the same score."
- **slide 9** — The speaker note gives the answer ("Someone says 2"), which the rubric bans on a
  question slide (N4a). — Fix: "Take answers. Then ask: in how many ways in 3 steps? In 4?"
- **slide 10** — "A count for each length: 2, 1, 11, …" reads as lengths 1, 2, 3, but length 1 has 0
  walks. Also, the GIF never shows a revisit: the only length-3 walk shown (u, top-left, middle-left, v)
  is a path, yet "revisits allowed" is what defines a walk. — Fix: "Walks of length 2, 3, 4: 2, 1, 11,
  …". Add one GIF frame "length 4: one of 11" drawing u → middle-left → top-left → middle-left → v.
- **slide 11** — The speaker note says degree "sits at the corner" (in both rows), but the cell sits in
  the walks row only. — Fix: note "Degree sits in the walk row: walks of length 1."
- **slides 9, 10, 11** — `w5-blank`, `w5-walks` and `grid-empty` carry four 2 px grey specks at their
  corners (for example, slide 9 at (676,200), (1186,200), (676,552), (1186,552)). — Fix: remove the
  bounding-box marks from these figures in `figs_quiz`, or draw them in white.
- **slide 13** — $N$ is not defined. The GIF ends on sums ("smallest sum: D, 10") and never shows a
  value of $c$. — Fix: add "$N$: the number of nodes." and end the GIF with "smallest sum: D, 10, so
  c = 6/10".
- **slide 14** — The figure states the result ("hub closeness = 1.0") but not the reason. The hub's red
  ring is thin, unlike the `figlib.mark` ring on slide 13. — Fix: caption "hub: sum = 6 = N − 1, so c =
  6/6 = 1", and draw the hub's ring with `figlib.mark`.
- **slide 16** — The answer slide has no body line, so the graph sits about 105 px higher than on
  slide 15 and jumps at the reveal. — Fix: add one body line ("F and P have the smallest sums."), or a
  spacer of the same height, so that the figure keeps slide 15's position.
- **slide 17** — The winning node is the NY 17 / US 209 interchange (41.56 N, 74.50 W), 14.6 km from
  Middletown (`near_km`). "a third" is 91/289 = 31%. — Fix: "* Winner: NY 17 at US 209, 15 km from
  Middletown." and "* Nearly a third of the interchanges lie within 60 km of Manhattan." Change the map
  label to "near Middletown".
- **slide 18** — Question slide with no beat for thinking and no note. — Fix: add the cue "*Take 30
  seconds.*"
- **slide 20** — G's red "9/2" sits below the F–G edge, about as close to F (which already carries
  17/6) as to G. The line break falls inside the math: "with 1/∞ =" / "0.". — Fix: place 9/2 directly
  below G. Body: "**Harmonic centrality**. An unreachable node adds $1/\infty = 0$."
- **slide 22** — The caption's "crown" is a figure of speech. — Fix: "on the left, closeness picks F
  and harmonic picks E".
- **slide 23** — "on the average" is unclear. This is covered by the retitle under Majors.
- **slide 6** — The body wraps, leaving "them counts." alone on the second line. The merged wording
  under slide 6 fixes this.

## Checked and clean

1, 12, 19, 24 (24 also gets the fire-station line moved in from slide 23).

All other slides in 1–24 are clean apart from the entries above. All numbers I checked are correct:
- closeness sums: E 20, F 19, G 20; N 18, P 16
- the cut graph: every closeness 0, and every harmonic value
- harmonic quiz: E 27/4, G 19/3, F 35/6; N 4, T 11/3
- BT graph: every sum and every eccentricity
- walks from u to v: 2, 1, 11
- New York degree counts: 201 and 57 (degree 2 does not occur; there is one node of degree 5, inside the "4+" legend class)

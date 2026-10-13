# R3, reviewer A: slides 1–28 (+ transition to 29)

I opened every slide PNG from 001 to 029. For the five builds in the range (`roma-to-graph`,
`w5-walks`, `closeness-def`, `harmonic-def`, `ecc-def`) I read every frame on a contact sheet,
and I read zoomed crops of roma-degree, ny-overview, closeness-def, q-close-CB-ans,
q-close-CA-ans, q-harm-CA-ans, q-harm-HD-ans and q-ecc-EA-ans.

**Numbers.** `python3 -B smallgraphs.py` passes. Every number in the range matches it and the
speaker notes:
- walks u→v: 2, 1, 11;
- bowtie sums 15/11/10 and eccentricities 4/3/2;
- closeness quizzes: N 18, P 16; E 20, F 19, G 20;
- the cut: all 0; harmonic on the cut graph: G 9/2, E/I/J 4, H 10/3, F 17/6, K 8/3, A–D 5/2;
- harmonic quizzes: E 27/4, G 19/3, F 35/6; N 4, T 11/3;
- eccentricity quiz: E 3 (sum 10), F 2.

The NY counts match `figs_ny.py`'s asserts and the data: 289/433, degree 3: 201, degree 4: 57,
closeness winner node 53 at 41.56 N, −74.50.

**Continuity.** Pixel checks, done in RGB:
- These pairs are identical, as the spec requires:
  - roma-to-graph frame 00 = roma-basemap;
  - w5-walks 00 = w5-blank;
  - ecc-def 00 = bowtie-closeness = closeness-def last;
  - harmonic-def 00 = cut-blank;
  - closeness-def 00 = btw-def 00.
- Every Q/A pair has the same size and crop. The answer differs from its question only in the
  marks and values.
- On every consecutive pair that shares a drawing (3→4→5, 6→7, 8→9, 15→16→17→18, 20→21, 22→23,
  25→26, 27→28), the drawing sits at the same slide position.

Layout:
- Nothing in the range runs below y = 660.
- The figure is on the right everywhere the spec says so.

**Blockers: none.**

---

## Majors

**M1. Slide 19 (`harmonic-def`, frame 08 → 09): ten labels change meaning in one step.**
- Up to frame 08, the label beside each node is *G's* term for that node (1/1, 1/2, 0).
- In frame 09, all ten of those labels become *each node's own* harmonic score, in the same
  positions. For example, the "1/1" above H turns into "10/3".
- This is the large, silent jump the lecturer asked to remove. The closeness-def build next to
  it does one node per frame.
- Also, G turns hot with its underline at frame 08, before any other score is visible. The
  winner is marked before the comparison exists. closeness-def and ecc-def mark D only at the
  end.

Fix: rebuild the tail of the build as four frames.
1. Frame 08: G's sum 9/2 appears in **ink**; G stays cool; the contribution labels stay.
2. Frame 09: the contribution labels clear; only G's 9/2 remains.
3. Frame 10: the star piece's scores appear (E 4, A–D 5/2).
4. Frame 11: the other piece's scores appear (F 17/6, H 10/3, I 4, J 4, K 8/3). Then G turns hot
   and its value is underlined.

**M2. Slide 21 (and slide 16): G's value sits over the F–G edge, beside H, so it reads as an
edge label or as H's value.**
- On slide 21, "19/3" is in ink, centred above the F–G edge, at H's height, immediately left of
  H's disc. H has no value of its own on that slide.
- So the label can be read as H's score or as a length on the F–G edge. In a module about
  distances, a number over an edge reads as an edge length.
- Slide 16 has the same pattern. E's "20" sits over the E–F edge and G's "20" over the F–G edge,
  flanking F's "19". Because the two values are equal, the misreading costs less there (Minor on
  its own).
- Slide 19's hot "9/2" sits in the same spot. The colour match with the hot G saves it (Minor).

Fix: use the bowtie convention of slide 12, where every value sits directly above or below its
own disc and never over an edge's midpoint.
- In `smallgraphs.py` CA_XY, move the H–I–J–K block about 0.3 units right (and H up a little),
  so that G's value fits directly above G.
- Put F's value directly below F, and E's value directly above E (nudge A left if needed).
- This applies to q-close-CA-ans, q-harm-CA-ans and harmonic-def, all one CA canvas and box.

**M3. Slides 22–23 (`q-harm-HD`): no trick. The hub wins.**
- The star's centre N (degree 4, the most central-looking node in the picture) wins with 4
  against the path middle's 11/3. Most of the room will pick N at once.
- With slide 21, both harmonic questions now end with "the hub wins". The brief's rule is that
  the hub must NOT win.

Fix: make the path 9 nodes long (Q…Y).
- Its middle node then scores 2(1 + 1/2 + 1/3 + 1/4) = 25/6 ≈ 4.17, which beats the star centre's
  4. A degree-2 node beats the degree-4 hub, and the bigger piece now does win.
- Change the A-line to "The middle of the long path beats the star's centre." and change the note
  to "many far nodes add up".
- Update the asserts in `smallgraphs.check()` (T → the new middle node, 25/6).
- Nine 40-px discs fit in 537 px at about 57 px spacing; or bend the path into a shallow arc.
- If the lecturer wants to keep "the bigger piece is not the better one", keep the slide, but
  then the harmonic section has no question where the central-looking node loses.

---

## Minors

**m1. Slide 2.**
- The photo strip runs to x ≈ 1212, past the 1200 content edge where the title rule ends.
- Fix: shrink the three photos by about 4 %, or tighten their gap.

**m2. Slide 3.**
- The OSM credit floats about 65 px below the map (the `tall` box is taller than the image).
- The stippled sea and the white land have so little contrast that Italy is not recognisable at
  slide size.
- Fix:
  - Darken the sea stipple one step, or add a muted coastline stroke.
  - Pull the caption up under the map.
- Optional: slide 4's frame 00 is pixel-identical to slide 3, and slide 4's bullet "Edge: a road
  or a sea lane" restates slide 3's bullet. Slide 3 could be dropped, with slide 4 opening on the
  map, so one slide carries the same content.

**m3. Slide 4 (`roma-to-graph`, frame 04).**
- The first links drawn are Roma's five, which answers "Which city is the most important?"
  before it is asked.
- Fix: draw the links west to east (Britain/Gaul, then Italy, then the east), so that Roma's five
  are not grouped.
- Also, Thessalonica and Athenae nearly touch, and their edge is about 8 px long on the slide.
  Nudge Athenae down about 10 px.

**m4. Slide 5 (`roma-degree`).**
- The hot "5" and its underline sit about 2 px from the Mediolanum–Roma edge.
- The "5" is set high against "Roma", so the pair reads "5Roma".
- Fix: put the 5 after the name ("Roma  5"), or directly below-right of the Roma disc, clear of
  edges.

**m5. Slide 6 (`ny-overview`).**
- "Syracuse" sits between the Syracuse dot and the Binghamton dot, a little nearer Binghamton's,
  and has no leader line. Binghamton has a leader line to its own label below.
- Roads and interchange dots show through "Syracuse", "Buffalo" and "Utica"; the halo does not
  cover them.
- The OSM caption wraps to two lines.
- Fix:
  - Move "Syracuse" above its dot, between Rochester and Utica, or give it a short leader line.
  - Widen the halo for these three labels.
  - Shorten the credit to "© OpenStreetMap", or let the figcaption use the full column width.
- Bullet 2 runs three lines: "Which city do the most cross-state trips pass through?" is enough,
  since the figure shows the eight.

**m6. Slides 6 → 7 → 24 (NY group).**
- The eight city names vanish after slide 6.
- Slide 24's bullet then talks about Manhattan, which is not marked on its map.
- `figs_ny.circle60()` exists but is drawn only on ny-eigenvector. Slide 24's main point
  ("closeness is pulled to where the nodes are") is carried only by the third bullet.
- Fix:
  - Keep a muted "NYC" label on every NY map.
  - Add the dashed 60 km circle (muted) to ny-closeness, with "31%" beside it.
  - Shorten bullet 3 to "31% of interchanges inside the circle."
- Also on slide 24, bullet 2 "Winner: NY 17 near Middletown" repeats the figure's hot label.
  "Winner: NY 17" would do.

**m7. Slide 7.** "Degree cannot tell them apart": "them" has no referent on the slide. Write
"Degree cannot tell the interchanges apart."

**m8. Slide 9 (`w5-walks`).**
- Frame 01 reads "shortest path: 2", where 2 is a length.
- Frame 02 reads "walks of length 2: 2", where 2 is a count.
- The same digit means two different things in consecutive frames.
- Fix: "shortest path: 2 steps".
- Bullet 2's "2, 1, 11, …" repeats the frame labels and could go.

**m9. Slide 10 (`grid-empty`).**
- "which routes count" and the row label "shortest paths" are stacked in the same muted style,
  so they read as one two-line heading.
- "how they become one number" floats top-right over nothing. The two rows have 4 and 5 cells of
  different widths, so no column stands for a shared choice, and the second axis that the title
  promises is not visible.
- Fix:
  - Set the axis title apart from the row labels: put the row labels at the left of their rows,
    or put the axis title in italic followed by a colon.
  - Move the column header to sit over the cells, or drop it and name the second choice inside
    each cell. grid-row1, grid-row2 and grid-final share the box, so the change carries through.

**m10. Slide 12.**
- It is the only definition slide whose key term is not bold and hot. Degree, Shortest path,
  Walk, Harmonic centrality and Eccentricity all are.
- Fix: "Add up the distances ℓ_ij to every other node" → "**Closeness**: add up the distances
  ℓ_ij to every other node."

**m11. Slide 21.**
- The hub E wins here, which the brief's quiz rule forbids. Here it is deliberate: it reverses
  slide 16's answer, and the cue "Does the winner change?" sets it up.
- Keep it, but see M3: together with slides 22–23, the hub wins twice in a row.

**m12. Slide 19.** Covered in M2: "9/2" sits immediately left of H at H's height. Moving it
directly above or below G removes the ambiguity.

---

## Transition out of range

The step from slide 28 to slide 29 is clean:
- same title;
- the left text drops back to the Q's single line;
- a new graph (q-ecc-EB) with its own crop, top-aligned at the same y as slide 28's.

Slide 29 shows no values and no marks.

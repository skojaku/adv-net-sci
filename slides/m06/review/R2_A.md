# R2, reviewer A: slides 1–35

I opened every PNG from 1 to 35. I extracted every frame of `roma-to-graph`, `w5-walks`,
`closeness-def`, `harmonic-def`, `ecc-def` and `btw-def` and read each GIF as a contact sheet
(`scratchpad/review_frames_r2/sheet_*.png`). I also looked at the four grid figures stacked
(`grids.png`) and at zoomed crops of slides 4, 6 and 29.

`python3 smallgraphs.py`: all assertions pass. Every small-graph number in the range matches it:
- closeness sums E 20, F 19, G 20, N 18, P 16;
- the cut graph's closeness (all 0) and harmonic values;
- harmonic E 27/4, F 35/6, G 19/3, N 4, T 11/3;
- eccentricity on both quiz graphs and on the BT graph;
- betweenness on BT (C 8, D 9, E 8) and on the quiz (E 30, F 25, G 30, M 9, O 19/2);
- walks u to v: 2, 1, 11.

The New York numbers match `data/ny_network.json`:
- degree: 201 / 57 (30 of degree 1, one of degree 5);
- closeness: winner node 53, NY 17/US 209, 14.6 km from Middletown; 91 / 289 = 31%;
- eccentricity: 472.7 km at node 200, lon −75.42, east of Binghamton;
- betweenness: Monticello top; four of the top five on NY 17; Binghamton / Syracuse = 3.498.

`check_deck.py` passes.

Mapping from Round 1: old slide n is now n for n ≤ 6, and n − 1 for n = 8–36 (old 7 was cut).

**Closeness quiz layout (slide 14): verified.**
- Left: the drawing spans x 123–616, so its centre is at 370. E sits at 340 (30 px off) and F at 430 (60 px off).
- Right: the drawing spans 660–1160, centre 910. N sits at 883 (27 px off) and P at 965 (55 px off).
- So the hub is the node at the centre of each picture, and the winner is not.
- Caveat, not a finding: the mean of the node positions lies nearer the winner (left 401 px against F 430, right 943 against P 965). Any faithful layout puts the closeness winner near the centre of mass, so this cannot be avoided; the eye reads the hub as the middle.

---

## Part 1 — Round-1 status

### R1_A (old 1–24)

| R1 item | now | status |
|---|---|---|
| slide 6 Blocker: shade and crown unexplained | 6 | **fixed.** The caption "darker: more roads; Roma has the most, 5" explains the shade. The crown stays, redundant with the red ring (new Minor N15). |
| slide 17 Blocker: NY closeness has no legend | 16 | **fixed** (figcaption) |
| slide 3 Major: title and text claim roads | 3 | **fixed** |
| slide 3 Major: basemap too pale | 3 | **fixed.** The dominant land is grey 241 and the sea 207: 34 levels apart (target ≥ 30). Frame 1 of the GIF matches. |
| slide 4/6 Major: edges run through the names | 4, 6 | **fixed, but a new problem.** The names are now legible on white boxes, but the boxes hide the edges (new Major N1). |
| slide 5 Major: move the NY question | 5 | rejected |
| slide 6 Major: $A_{ij}$ undefined | 6 | **fixed** |
| slide 7 Major: duplicate slide | — | **fixed** (cut) |
| slide 11 Major: grid's second axis missing | 10 | **fixed** (both grey headers) |
| slide 15 Major: winners at the picture centre | 14 | **fixed** (see the check above). Slides 17–21 are rebuilt on the new layout. |
| slide 21 Major: "the same network as before" | 20 | **fixed** |
| slide 23 Major: the question answered in its own body | 22 | **fixed.** The body is now only the cue, and the fire-station line moved to slide 23. The retitle was not done (see the Minor below). |
| slide 2 Minor | 2 | **mostly not fixed.** The duplicate "said to" is gone, but there is still no label under each photo, and "BC." sits alone on line 2 of bullet 1. |
| slide 3 Minor: red pins, tight crop | 3 | **half fixed.** The pins are blue, but the crop was not widened: the Londinium pin touches the top-left corner of the frame and the Alexandria pin its bottom edge. |
| slide 5 Minor: "cross-state trips", paragraphs | 5 | not fixed (not triaged) |
| slide 8 Minor: "cannot tell them apart", paragraphs | 7 | not fixed |
| slide 9 Minor: the note gives "2" on a question slide | 8 | not fixed |
| slide 10 Minor: lengths unclear, no revisit shown | 9 | **half fixed.** The GIF header now reads "walks of length 2, 3, 4: 2, 1, 11", but no frame shows a walk that revisits a node. |
| slide 11 Minor: note says degree is "at the corner" | 10 | not fixed |
| slides 9–11 Minor: grey corner specks | 8, 9, 10, 33 | **not fixed.** They are still visible at the four corners of `w5-blank`, `w5-walks`, `grid-empty` and `grid-row1`, e.g. slide 33 at (113,138), (1166,138), (113,491), (1166,491). |
| slide 13 Minor: $N$ undefined; GIF never shows $c$ | 12 | **half fixed.** $N$ is now defined. The GIF still ends on "smallest sum: D, 10" with no value of $c$. |
| slide 14 Minor: no reason for 1.0; thin ring | 13 | not fixed |
| slide 16 Minor: graph jumps at the reveal | 15 | **fixed, but a new problem.** The answer line was added, but the question line on slide 14 wraps to two lines, so the graph still jumps 43 px. The same happens on harmonic, 20 → 21 (42 px). See new Minor N4. |
| slide 17 Minor: wording | 16 | **fixed** |
| slide 18 Minor: no cue | 17 | **fixed** |
| slide 20 Minor: 9/2 placement; line break inside the math | 19 | **half fixed.** 9/2 now sits under G. The math still breaks: "adds 1/∞ =" / "0." |
| slide 22 Minor: "crown" | 21 | **fixed** |
| slide 23 Minor: "on the average" unclear | 22 | not fixed (see N10) |
| slide 6 Minor: lone "them counts." | 6 | **fixed** |

### R1_B (old 25–36)

| R1 item | now | status |
|---|---|---|
| old 26 Minor: "closeness" tag | 25 | **fixed** ("best closeness"). On the left, the tag sits directly under F (new Minor N8). |
| old 27 Blocker: NY eccentricity has no legend | 26 | **fixed** |
| old 27 Minor: bullets | 26 | **fixed** in substance (473 km, NY 17 east of Binghamton) |
| old 29 Minor: neighbour pairs skipped; "carries" | 28 | not fixed (not triaged). The GIF says "a letter for every pair" and then shows only 13 of the 21 pairs. |
| old 30 Major: wrong in-figure label | 29 | **fixed, but a new problem.** The banner is gone, and the replacement figcaption was deleted in b841ad5a to fit the frame. Nothing on screen now says that 1/2, 1/2, 1 are the shares of the one pair S, D (new Major N2). |
| old 30 Major: σ undefined | 29 | **fixed** |
| old 30 Major: red as a group colour; "1" touching T | 29 | **fixed** (blue and gold routes, black values, "1" clear of T) |
| old 31 Minor: wording | 30 | **fixed** |
| old 33 Major: bullets disagree with the map | 32 | **fixed** |
| old 33 Major: no legend | 32 | **fixed.** The caption leaves "through" alone on line 2 (N11). |
| old 33 Minor: overclaim | 32 | **fixed** |
| old 34 Minor: "longest" | 33 | **fixed** ("longest distance") |
| old 34 Minor: red names, specks | 33 | **red: done as the lead directed.** All four cells are new on this slide, so all four names are accent-2. **Specks: not fixed.** |
| old 36/37 Minor: divider repeats the Aesop moral | 35 | not fixed (not triaged). The title also wraps now, leaving "keep" alone (N14). |

---

## Part 2 — New findings

**Count: Blockers 0 · Majors 2 · Minors 13**

### Majors

**N1. slide 4 (same geometry on slide 6 and the last frame of `roma-to-graph`) — Major — The white label boxes now hide the edges, and one edge reads as a road that does not exist.**
- The Roma–Alexandria sea lane leaves Roma under the "Roma" box. It shows as a short stub, disappears under the "Thessalonica" box, and comes out of that box's right end toward Alexandria. On screen it reads as **Thessalonica–Alexandria**, which is not an edge.
- Of Roma's 5 links, only 3 visibly leave its disc. The links to Thessalonica and to Alexandria start behind the "Roma" box, as two small "=" stubs between the disc and the label.
- Slide 6's caption says "Roma has the most, 5". A student who counts the lines gets Roma 3 + 2 stubs and Thessalonica 4.
- The same disc-to-label stubs appear at Tarraco, Londinium and Alexandria.
- **Fix in `romelib`:**
  - Draw Roma–Alexandria as a curve (`bend right` of about 15°) that passes below the "Thessalonica" box. It is a sea lane, so a curve also reads correctly.
  - Put "Roma" above-right of its disc. That space is free once the crown goes (N15).
  - Add a build assertion that no label box covers any edge other than its own city's, over more than its first 10 bp.

**N2. slide 29 — Major — The figure's numbers read as betweenness values, and they are not.**
- The figure prints 1/2 by A, 1/2 by B and 1 by T, in the same place where every other figure in the deck prints a node's score.
- The true values are b_A = 1, b_B = 1, b_T = 7/2, b_S = 1/2. The printed numbers are the shares of the single pair S, D.
- The blue and gold routes are also unexplained (F1).
- The caption that said this was deleted in b841ad5a to make the slide fit.
- **Fix:**
  - Regenerate `sigma-answer` about 25% shorter: put A and B closer to the S–D line, for example A at y + 0.9 and B at y − 0.9 in place of the current spread.
  - Restore `<figcaption>S to D: two shortest paths, so A and B each carry half of this pair</figcaption>`.

### Minors

**N3. slide 33 — Minor — The degree cell disappears.**
- Slide 10 put "degree / walks of length 1" in the walk row, and `grid-row2` (day 2) puts it back.
- `grid-row1` leaves the walk row empty, so the cell vanishes for one slide.
- Fix: draw the degree cell, in black, in `grid-row1`'s walk row, with the same geometry as `grid-empty`.

**N4. slides 14 → 15 and 20 → 21 — Minor — The graph jumps about 43 px at the reveal.**
- Each question line wraps to two lines, but each answer line takes one.
- Fix: shorten both question lines to one line.
  - Slide 14: "The smallest sum of distances wins. Left and right are two networks."
  - Slide 20: "Left: the closeness network, road E–F open again. Right: two pieces."

**N5. slides 8 → 9 and 17 → 18 — Minor — The same graph jumps 62 px and 57 px.**
- The question slide has `<!-- _class: mid -->` and the next slide does not.
- Fix: remove `mid` from slides 8 and 17.

**N6. slides 24 and 30 — Minor — These question slides have no thinking cue.** Every other quiz has one.
- Fix: add `<div class="cue">` with "*Take a minute. Pick one on each side.*" to both slides.

**N7. slide 24 (left) and slide 30 (right) — Minor — The winner is the node in the middle of the picture.** This is the cue the closeness quiz was redrawn to remove.
- Slide 24, left: F is at x 363, and the drawing's centre is at 370.
- Slide 30, right: O is at 935, the centre is at 910, and M is at 810.
- The left of slide 30 is fine: there the node at the centre, F, is the one that loses.
- **Fix in `smallgraphs.py`:**
  - `EA_XY`: B and C to x = −1.5, giving long spokes as in `CA_XY`. E then becomes the node nearest the centre.
  - `SQ_XY`: L to (−1.0, 3.2) and N to (−1.0, 0.8). M then becomes the node nearest the centre.
  - Add the same not-nearest-the-centre assertion that the closeness quiz has.

**N8. slide 25 — Minor — The left "best closeness" tag sits directly under F.**
- F is the red eccentricity winner. The thin grey leader line to E is easy to miss, so the tag reads as labelling F, which is the opposite of the slide's point.
- Fix: replace both tags with a grey ring (annotation grey, the same width as the red ring) on E and on K. Change the line above the figure to "Eccentricity, beside every node. Grey ring: best closeness."

**N9. slide 19 — Minor — Two problems.**
- The math still breaks across lines: "adds 1/∞ =" / "0.". Fix: "Out of reach: $1/\infty = 0$."
- "10/3" sits above I, not H: it is centred 8 px from I and 54 px from H, and it does the same on frame 0 of `harmonic-def`. Fix: place it directly above H.

**N10. slide 22 — Minor — The cue and the title need work.**
- `*Take 30 seconds.*` renders as black body text, centred, unlike every other cue.
- The title's "on the average" is still unclear (R1).
- Fix: title "Would you place a fire station by its average distance?", and wrap the cue in `<div class="cue">`.

**N11. slide 32 — Minor — The caption wraps, leaving "through" alone on line 2.**
- Fix: "darker, larger dot: more shortest paths through it".

**N12. slide 12 — Minor — "of nodes." sits alone on line 3.**
- Fix: "$\ell_{ij}$: shortest-path length from $i$ to $j$. $N$: number of nodes."

**N13. slide 16 — Minor — The bullet "31% of the interchanges lie within 60 km of Manhattan" does not say why it matters.**
- The note says why, but the slide does not: the nodes are concentrated there, so closeness is pulled toward them.
- Fix: "31% of the interchanges lie within 60 km of Manhattan; closeness is pulled toward them."

**N14. slide 35 — Minor — The divider title wraps, leaving "keep" alone.**
- It also states the same thing as the Aesop moral on the next slide (R1_B, never triaged).
- Fix: title "Importance you inherit", subtitle "day 2: the routes become walks". Retitle slide 37 "A score made of scores", as R1_B proposed.

**N15. slide 6 — Minor — The crown repeats what the red ring already marks.**
- It also sits on the Mediolanum–Roma edge, and it blocks the free side that the "Roma" label needs (N1).
- Fix: drop the crown and keep the ring.

## Checked and clean

1, 5 (apart from the R1 wording), 11, 13 (apart from the R1 Minor), 15, 18, 21, 23, 26, 27, 28 (apart from the R1 Minor), 31, 34.
- No question slide in the range gives its answer in the body, the figure or the notes. Slide 8's note "Someone says 2" is the R1 Minor.
- No em dashes in the range.
- Red is used for emphasis only, apart from the grid's new-cell names, which follow the lead's rule.

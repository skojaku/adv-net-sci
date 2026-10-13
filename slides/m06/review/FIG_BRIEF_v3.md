# m06 figures v3: brief for the figure agents

Read first: `review/DECK_SPEC.md` (the slide list and the figure groups) and the palette and
drawing sections of `figures/figlib.py` (already rewritten; do not edit figlib.py).

All paths below are relative to `slides/m06/`. Work in `figures/`. Do not commit.

## What changed and why

The lecturer wants (1) small differences between consecutive slides, (2) the figure in the
right half (a 537 bp `col` container) with short bullets on the left, (3) a two-graph question
split into two one-graph questions, (4) no autoplay: every build is a set of frames he steps
through, and (5) his own figure style. His reference figures: hand-drawn nodes with a dark
pencil outline and a grainy fill, brush strokes for highlighted routes and for underlines,
MesloLGS NF for every label, muted colours overall, saturation only on what matters, no pure
black, and very little text.

## The style contract (figlib.py provides all of it)

- **Nodes:** `F.disc(x, y, label, fill=...)` for every node. Fill `"white"` is the default node;
  `"pale"` is a de-emphasised node; `"hot"` (orange) is the point of the slide (the winner, the
  answer); `"cool"` (sky blue) is a second emphasis; `F.shade(v)` (v in 0..1) maps a value from
  near-paper (low) to saturated cool (high). The label colour is chosen for you. `F.mark(x, y)`
  is a hot pencil ring around a node, if a filled disc is not right.
- **Edges:** `F.seg(p, q)` (soft ink, a faint second pencil stroke). Context edges:
  `color="muted"`. A removed edge: `color="muted", dash=F.DASH`.
- **Routes, walks, highlighted paths:** `F.brush(points, color="gold" | "hot" | "cool", w=14)`,
  drawn BEFORE the discs, so the nodes stay on top.
- **Underline:** `F.underline(x0, x1, y, color="hot")` under the emphasised value or word,
  in the colour of what it underlines (his "query vector" figure).
- **Text:** `F.text(...)`, MesloLGS NF at `F.FONT` (30). Colours `"ink"` (default), `"muted"`
  (context), `"hot"`, `"cool"`. A label with `$...$` must use `size=F.FONT_MATH` (38): Latin
  Modern math has a smaller x-height and the gate fails it otherwise. Prefer plain text for
  numbers ("27/4", "0.85") in Meslo.
- **Answers:** the winner's disc filled `"hot"`, its value in `"hot"` with an underline; the
  other candidates' values in `"ink"`; tags such as "best closeness" in `"muted"`.
- **Little text in figures.** Numbers and two- or three-word labels. No sentences: the deck has
  the bullets.
- **Never** draw with pure black, the old blue `3959A6` or red `B14434`. The names `accent`,
  `accenttwo`, `annot`, `black` still compile (mapped to cool, hot, muted, ink), but write new
  code with the new names.
- Raw TikZ is fine for things figlib has no helper for (bars, boxes, arrows), in the palette
  colours `ink muted pale faint hot cool tealc olivec deep gold`. For a box, add `pencil` to
  the draw options to get the hand-drawn edge.

## Emitting

- `F.emit(name, body, container="col", h=..., hmod="", nodes=True, box=None)`
- `F.emit_group([(name, body), ...], container, h, box=None, prefix=True)`: one crop for all;
  with `prefix=True` every later body must start with the first (the answer is the question
  plus marks and values).
- `F.emit_frames(name, frames, container, h, box=None)`: writes `figures/frames/<name>/00.png
  ...` and `figures/<name>.png` (the LAST frame, which the PDF export and the render gate
  see). `emit_gif` is now an alias of it; no GIFs any more. Each frame is ONE small step (one
  value appears, one edge is drawn, one node changes); 4 to 10 frames is typical. When the spec
  says "frame 0 = slide N", frame 0's body must be exactly that figure's body, on the same
  canvas and the same `box`, so the picture does not move when the slide changes.
- `box=(top, bottom)` in bp from the canvas top fixes the crop, for figures of one group that
  are built in different functions. Every figure in a group must have the same canvas width
  and height, the same coordinates, and the same box.
- Containers: `col` = 537 bp wide, height cap 380 (`hmod=""`) or 400 (`"tall"`); `full` =
  1080 bp. Node discs must land 26 to 52 px on the slide (NODE = 40 at col scale 1.0).

The TikZ random strokes and the grain are seeded by position, so the same element looks the
same in every figure that draws it at the same place.

## Build and check

From `figures/`, build only your own module (other modules are being edited at the same time):

    python3 -c "import figlib as F, figs_quiz as M; F.run(M.FIGURES)"

Fix every FAIL. Then open every PNG you produced with Read, and for each build frame 00, one
middle frame and the last. Check: no label touches a disc, an edge or another label; numbers
are right (they come from `smallgraphs.py` and are asserted); the figures of one group have
identical pixel sizes (`python3 -c "from PIL import Image; print(Image.open(p).size)"`), and a
"frame 0 = slide N" pair is pixel-identical. Report the names you emitted, their sizes, and
anything you could not do.

Keep each module's docstring and FIGURES list up to date. Remove figures the spec no longer
uses from FIGURES (do not delete the code if another module imports it).

## Assignments (disjoint files; never edit another agent's file)

**A. Intro + NY** — `figs_intro.py`, `figs_rome.py` (roma-degree only), `romelib.py`,
`figs_ny.py`.
- `roma-basemap` (col): the OSM map with hand-drawn pins (small `F.disc(..., size=...)` or
  dots in cool with an ink outline), "Roma" labelled.
- `roma-to-graph` frames (col): frame 0 = roma-basemap exactly (same canvas, same box). Then
  the map fades in two or three steps, the links are drawn a few at a time as straight soft-ink
  edges between the pins, and the pins become discs (white fill, pencil outline) at the pin
  positions (nudge only where two discs would touch). Last frame: the network on white paper,
  only "Roma" labelled. At least 26 px discs.
- `roma-degree` (col): the last frame of roma-to-graph plus `F.shade(degree / 5)` fills, Roma
  marked hot, and a "5" beside Roma in hot. Same box as roma-to-graph.
- `ny-overview`, `ny-degree`, `ny-closeness`, `ny-eccentricity`, `ny-betweenness`,
  `ny-eigenvector`, `ny-five` (col): restyle (muted road lines, dots from faint to saturated
  cool by value, the winner hot, Meslo labels, an underline under the one label that is the
  point). All seven on ONE canvas and ONE box, so switching slides changes only dots and labels.

**B. Definitions** — `figs_defs.py`, and in `figs_small.py` only `sigma-answer`.
- `w5-blank` (col) and `w5-walks` frames (col, frame 0 = w5-blank; same box). Walk frames:
  the shortest path u→v as a hot brush, then one frame per walk length with the count.
- Bowtie group (col, one box): `closeness-def` frames (the sum of distances appears one node at
  a time; D, the smallest, hot and underlined at the end), `bowtie-closeness` (= that last
  frame, a PNG), `ecc-def` frames (frame 0 = bowtie-closeness; the sums give way to
  eccentricities; D hot at the end), `btw-def` frames (frame 0 = the bare bowtie; letters
  counted; D hot at the end, 9).
- `sigma-answer` (col, was full): S to D, two shortest paths, through A and through B, as two
  brushes (hot and cool), "1/2" beside A and B, T carries the whole pair.
- `grid-empty`, `grid-row1`, `grid-row2`, `grid-final` (full): restyle (hand-drawn boxes, Meslo,
  the new cells of each slide in hot, the old ones ink, the axis headers muted). One box for
  all four, so the grid never moves.
- `harmonic-def` moves to figs_quiz.py (agent C): remove it from figs_defs' FIGURES.

**C. Quizzes** — `figs_quiz.py`, and layouts in `smallgraphs.py` (you are the only agent who may
edit smallgraphs.py; keep `check()` passing).
- Split every two-graph question into one-graph `col` figures, Q and answer per graph, one crop
  per pair: `q-close-CB`, `q-close-CB-ans`, `q-close-CA`, `q-close-CA-ans`, `q-harm-CA-ans`,
  `q-harm-HD`, `q-harm-HD-ans`, `q-ecc-EA`, `q-ecc-EA-ans`, `q-ecc-EB`, `q-ecc-EB-ans`,
  `q-btw-DB`, `q-btw-DB-ans`, `q-btw-SQ`, `q-btw-SQ-ans`, `q-eig-L`, `q-eig-L-ans`,
  `q-katz-L-ans`, `q-eig-R`, `q-eig-R-ans`, `q-katz-R-ans`. The Katz questions reuse q-eig-L and
  q-eig-R, so q-katz-*-ans must be q-eig-* plus values (prefix rule).
- CA group, one canvas, one box: `q-close-CA`, `q-close-CA-ans`, `q-harm-CA-ans`, `cut-blank`
  (CA with E–F dashed muted and crossed out in hot), `cut-closeness` (every node "0"),
  `harmonic-def` frames (moved here from figs_defs; frame 0 = cut-blank; then G's reciprocals
  appear one at a time, then every node's harmonic score).
- Keep the trick: the node drawn in the middle of the picture loses. Keep every asserted number.
- Remove the old two-graph names (quiz-close, quiz-harm, …) from FIGURES.

**D. Eigenvectors** — `figs_eigen.py`.
- EIG group (col, one box): `eigen-inherit` frames (the sums arrive at A one neighbour at a time,
  then all scores) and `eig-pf` (the final scores, largest = 1, as the last frame).
- `eigen-equation` (col, was full): A (a 7 × 7 box) times a bar c = λ times the same bar,
  hand-drawn boxes, the bar's cells shaded by c.
- `eig-all-q` and `eig-all` (full, one crop): the seven eigenvectors on the 7-node graph, sign by
  hue (cool positive, hot negative), magnitude by saturation, eigenvalues on a number line;
  eig-all adds a hand-drawn cool frame around the λmax panel and "all positive" in cool.
- Ring group (col, one box): `ring-4444` and `ring-local` frames (frame 0 = ring-4444; K = 5, 6,
  7, 8, each adding one node to the last clique; fill by `F.shade`; one short label "K = 5: 68%"
  per frame, from `smallgraphs.eig_share`).
- `katz-floor` (col), `walks-discount` frames (col): restyle.
- `eig-centrality` is no longer used: drop it from FIGURES.

**E. Linear algebra and the Web** — `figs_decomp.py`, `figs_dir.py`, `figs_web.py` (genealogy
only).
- `decomp-sum`, `decomp-square`, `decomp-power`, `katz-why` (full, frames) and `decomp-orth`
  (full): restyle in the palette: an eigenvalue's circle cool if positive, hot if negative, area
  by size; the bars ink-outlined (`pencil`) with a cool fill; Meslo for words, Latin Modern
  math at FONT_MATH. The lecturer will send a reference for these later, so restyle only; keep
  the geometry.
- `hits-graph` (col): restyle (hub hot, authority cool).
- PR group (col, one canvas, one box): `pr-split`, `pr-split-answer`, `pr-leak` frames (the
  total drains step by step), `pr-teleport`, `ppr`.
- `genealogy` (full): restyle.

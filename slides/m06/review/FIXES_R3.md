# m06 review round 3: fix direction

From R3_A.md (slides 1–28), R3_B.md (29–56), R3_C.md (57–82). No Blockers; 13 Majors.

**Not taken:** R3_A M3 (rebuild the harmonic HD question so the path's middle wins). The
lecturer's brief allows "two candidates need computing" as the trick, and the HD lesson (the
bigger piece is not the better one) is deliberate. Also not taken: column headers for the
grid's second axis (carried over from v2), the empty lower third of the Katz-dial panel.

Every agent: build only your own module(s) (`python3 -c "import figlib as F, <mod> as M;
F.run(M.FIGURES)"` from `figures/`), open every PNG you change with Read, keep every group's
canvas and box shared, re-verify the pixel identities the spec requires (frame 00 = the slide
before), do not commit. The figlib API is unchanged.

---

## Agent Q — `figs_quiz.py`, `smallgraphs.py`
1. **harmonic-def tail** (R3_A M1): frame 08 = G's sum 9/2 in ink, G stays cool, the
   contribution labels stay; 09 = contribution labels cleared, only 9/2 remains; 10 = the star
   piece's scores (E 4, A–D 5/2) in ink; 11 = the other piece's scores (F 17/6, H 10/3, I 4,
   J 4, K 8/3), then G hot with its value underlined. 12 frames in all.
2. **CA values beside their own discs** (R3_A M2): no value may sit over an edge's midpoint or
   level with a neighbour's disc. Every value directly above or below its own disc. Move the
   H–I–J–K block right (and H up) in `CA_XY` so G's value fits above G; F's value below F;
   E's above E. Applies to the whole CA group (q-close-CA-ans, q-harm-CA-ans, cut-closeness,
   harmonic-def). E must still be drawn at the centre of the picture; keep `check()` passing.
3. **EQ_L layout** (R3_B m49, R3_C): the loser X must sit at the horizontal centre of the
   drawing, not the winner M. Re-lay `EQ_L_XY`; assert it in `check()` like EA and SQ.
   Applies to q-eig-L, q-eig-L-ans, q-katz-L-ans.
4. q-katz-L-ans: X's "0.81" directly above X or to its right, clear of the X–leaf edges.
5. q-katz-R-ans: H's and K's values at the SAME positions as in q-eig-R-ans (slide 70 shows the
   flip; only the numbers may change). q-eig-R-ans: K's underline clear of the K1–K edge.

## Agent D — `figs_defs.py`, `figs_small.py` (sigma-answer only)
1. **sigma-answer** (R3_B M4): endpoints named `s` and `t` (lower case, as in σ_st); the
   through-node (was T) named `C`. Both routes in non-hot brushes (one cool, one gold) up to C;
   one gold brush on the shared C–t segment (no railway track). C filled hot with its "1"
   underlined; "1/2" beside A and B in ink; a muted tag "pair s, t".
2. **btw-def** (R3_B): about 9 frames, not 16: one frame per source node's letters (A's four
   at once, then B's, C's, D's), then the zeros, then D hot with 9. Frame 00 unchanged.
3. **w5-walks** (R3_A m8): frame 01 label "shortest path: 2 steps".
4. **Grid** (R3_A m9, R3_C): the axis titles ("which routes count", "how they become one
   number") muted italic; the row labels ("shortest paths", "walks") in ink, so the two do not
   read as one phrase. "eigenvector" and "paths passing" must not touch their cell borders
   (widen those cells). In grid-final put **HITS before PageRank** (the order taught). All four
   grid figures keep one box.

## Agent E — `figs_eigen.py`
1. **eigen-inherit / eig-pf** (R3_B M3): the last frame keeps the sum line
   "0.64 + 0.58 + 0.81 + 0.85 = 2.88 × 1.00" (in ink; A not hot, no brushes). eig-pf stays
   pixel-identical to that last frame. A's "1.00": move it left of A, between the B–A and A–D
   edges (every value directly beside its own disc).
2. **Ring** (R3_C M5): draw each 4-clique as a square with both diagonals. ring-local grows the
   right clique to a pentagon, hexagon, heptagon, octagon around a FIXED centre, with the two
   port nodes (the ones that carry the ring edges) at fixed positions, so each step visibly adds
   one node. Frame 00 = ring-4444; frame 01 = the K = 4 shading with "K = 4: 25%" in ink; from
   K = 5 the percentage in hot. Label "K = 5: 68% of the score" may be shortened to fit, but
   say "of the score" at least once (frame 01).
3. **walks-discount** (R3_C M1 and m64): draw the network in the SAME layout as w5-blank (import
   the coordinates from figs_defs; do not edit figs_defs). Each legend entry appears in the same
   frame as its first walk (α² with the first length-2 walk, α³ with the length-3 walk); nothing
   right of the graph in frame 00. Colours: gold for the length-2 walks, cool for length 3.
4. **eigen-equation** (R3_B m45): λ in ink; the two "c" labels hot (the eigenvector is the
   point).
5. **eig-all-q / eig-all** (R3_B m46): put "−0.43" above the axis (no long leader tick).
6. **katz-floor** (R3_C m62): use the EIG layout (eig-pf's coordinates) so the room recognises
   the network.
7. Report the final node coordinates of ring-local's K = 6 frame (in bp, with the canvas size):
   the lead will port them to the Katz-dial stage.

## Agent F — `figs_decomp.py`, `figs_dir.py`, `figs_web.py` (genealogy only)
1. **decomp row** (R3_B M1): decomp-sum, decomp-square and decomp-power on ONE canvas and ONE
   box; the left-hand side right-aligned at a fixed x so the terms sit in the same columns on
   all three; reserve the "t = …" band in all three (empty in sum and square). "t = 16" etc. in
   ink, not hot. Right-align each coefficient against its u (no extra gap for "0.02").
2. **Bars neutral** (R3_B M5): every eigenvector bar (tall and wide, all decomp figures,
   decomp-orth, katz-why) filled `pale` or `faint` with the pencil ink outline. cool/hot only on
   the eigenvalue circles. decomp-square frame 01: mark the multiplied pair with a hot outline
   or underline, not a hot fill.
3. **Notation**: italic $A$, $I$ (as on the slides) in every decomp figure and katz-why; katz-why
   labels "α = 1.1/λmax" (λmax, not λ₁).
4. **pr-leak** (R3_C M3): frame 00 = pr-split-answer exactly; 01 = the weights and scores
   cleared; 02 = E's out-link dashed muted with the hot ×, "dead end"; 03… the drain, "total
   1.00" first appearing at 03.
5. **pr-split-answer** (R3_C m76): B and D white (they score lowest), A's "3/11" left of A.
6. **pr-teleport / ppr** (R3_C m78, m79): draw the jump in its own style, dotted cool arrows:
   on pr-teleport from E to every other page (a dead end links to every page); on ppr every
   jump goes to A (dotted cool arrows into A). The removed link stays dashed muted.
7. **genealogy** (R3_C m74): drop the banner sentence (the deck gets it as a line); dots with
   ink outlines and a pale fill, not saturated cool.

## Agent A — `figs_intro.py`, `romelib.py`, `figs_rome.py` (roma-degree), `figs_ny.py`
1. **roma-basemap** (R3_A m2): the sea a solid muted pale blue-grey and the land paper, with a
   muted coastline stroke, so Italy is recognisable at slide size; trim the box so the figure
   has no blank band below. roma-to-graph frame 00 must still equal it.
2. **roma-to-graph** (R3_A m3): draw the links west to east (Britain and Gaul, Italy, the
   east), never Roma's five together; nudge Athenae down about 10 bp from Thessalonica.
3. **roma-degree** (R3_A m4): the hot "5" below-right of Roma's disc, clear of every edge.
4. **ny-overview** (R3_A m5): "Syracuse" above its dot (or with a short leader); a wider white
   halo behind every city label so roads do not show through.
5. **all NY maps** (R3_A m6): a muted "NYC" label on every map. ny-closeness: the dashed 60 km
   circle (muted, `circle60()`) with a muted "31%" beside it.
6. **ny-betweenness** (R3_B m39): "Binghamton" in cool.
7. **ny-eigenvector, ny-five** (R3_C m60, m80): a thin muted leader from the NYC box to the
   inset. ny-five: move "eigenvector" off the Hudson-valley roads into white space; keep the
   closeness and betweenness discs from touching.

## Lead — the deck, the theme, the stages
- Deck text per the three reports' Minors (bullets shortened, the λmax line on 47 in plain
  text, slide 44's ∝, slide 34's bullets, the Katz quiz lines, slide 62 retitled "Katz
  centrality", 63 keeps the formula, 66 without figcaption, 73 Authority in cool, 74's banner
  as a line, 78 "A dead end links to every page", notes fixes).
- Stages (R3_C M4): softer fills (a faint→cool ramp that tops out below full saturation), a
  pencil filter on the discs, power-step D's label below-right and a shorter panel note; the
  Katz-dial ring on ring-local's K = 6 coordinates (after agent E reports them).

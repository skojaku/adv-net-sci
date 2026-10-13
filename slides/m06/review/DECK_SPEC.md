# m06 deck spec, v3 (2026-10-13)

v2 (72 slides) was reviewed by the lecturer. v3 answers that review:

1. **Small differences between consecutive slides.** The cost of new information grows like
   n² in its amount n, so information arrives in small steps. Consecutive slides keep the same
   drawing at the same place and add one thing (a value, a mark, a bullet).
2. **One layout, almost everywhere:** the figure fixed in the right half (`cols`, 537 px),
   minimal bullets in the left half, revealed one by one (`*` fragments). Exceptions (full
   width): the classification grid, the seven eigenvectors, the eigendecomposition row, the
   two live stages, the genealogy.
3. **A two-graph question becomes two one-graph questions:** Q1 → A1 → Q2 → A2. Q and A share
   the title, the left text (A adds one line) and the crop (A = Q + marks and values).
4. **Figures over text, and little text.** No fact that the lecture does not use (the Temple of
   Saturn, the lost inscription, Caesar as curator).
5. **No autoplay.** Every build is a set of frames the lecturer steps with a slider, ◀ ▶, or
   the clicker (`scrub.js`). The PNG/PDF export shows the last frame.
6. **The lecturer's figure style** (his reference figures): hand-drawn nodes with a dark pencil
   outline, grain, brush strokes for routes and underlines, MesloLGS NF for every label, muted
   colours with saturation only on what matters, no pure black. See `figures/figlib.py`.

Day 1 (10/20): slides 1–41. Day 2 (10/22): slides 42–82.

Markup for the right half: `<div class="cols"><div>` bullets `</div><div class="fig">` image
`</div></div>`. A build: `<div class="fig scrub">` with the still `figures/<name>.png`; the
script finds `figures/frames/<name>/NN.png`.

## Slides

| # | title | left | right | what changes |
|---|---|---|---|---|
| 1 | All Roads Lead to Rome | lead | | |
| 2 | The Golden Milestone | * 20 BC: Augustus, Caesar's heir, set it up in Rome. * Every road of Italy ended at it. * Distances were counted in miles from Rome. | photos (Caesar, Augustus, milestone) | |
| 3 | Twelve cities of the empire | - Roads and sea lanes joined them. | roma-basemap | new figure |
| 4 | Keep the links, drop the map | * Node: a city. Edge: a road or a sea lane. * Which city is the most important? | scrub roma-to-graph (frame 0 = slide 3) | the map goes, the links come |
| 5 | Degree centrality | * **Degree**: the number of roads at a city. * $d_i=\sum_j A_{ij}$ … * Roma: 5, the most. * It sees only the neighbours. | roma-degree | shading added |
| 6 | New York State highways | * 289 interchanges, 433 road segments. * Which of the eight cities do the most cross-state trips pass through? | ny-overview | new figure |
| 7 | New York: degree | - Degree 3: 201 interchanges. Degree 4: 57. - Degree cannot tell them apart. | ny-degree | same map, dots shaded |
| 8 | How far is u from v? | - The network from Module 01. | w5-blank | new figure |
| 9 | Two ways to count | * Shortest path … * Walk … | scrub w5-walks (frame 0 = slide 8) | path, then walks |
| 10 | Two choices make a centrality | (none) | grid-empty (full) | |
| 11 | Part One | | | |
| 12 | Closeness centrality | 4 fragments, formula third, "$N-1$: a star's centre scores exactly 1." | scrub closeness-def (bowtie) | |
| 13–16 | Which node is closest to everything? | Q: - Smallest sum of distances wins. / A adds one line | q-close-CB, -ans, q-close-CA, -ans | |
| 17–18 | What if one road closes? | Q / A adds "every closeness is 0" | cut-blank, cut-closeness | CA group |
| 19 | Take the reciprocal first | 3 fragments (harmonic, formula, 1/∞) | scrub harmonic-def (frame 0 = cut-blank) | CA group |
| 20–23 | Which node has the highest harmonic centrality? | Q/A ×2 | q-close-CA (reused), q-harm-CA-ans, q-harm-HD, -ans | CA group, then HD |
| 24 | New York: closeness | 3 fragments | ny-closeness | |
| 25 | Would you site a fire station on the average? | - Closeness picks D: the smallest sum. | bowtie-closeness | bowtie group |
| 26 | Eccentricity | 3 fragments | scrub ecc-def (frame 0 = slide 25) | bowtie group |
| 27–30 | Which node has the smallest eccentricity? | Q/A ×2 | q-ecc-EA, -ans, q-ecc-EB, -ans | |
| 31 | New York: eccentricity | 2 fragments | ny-eccentricity | |
| 32 | Part Two | | | |
| 33 | Trace a letter | 2 fragments | scrub btw-def (bowtie) | bowtie group |
| 34 | Betweenness centrality | 3 fragments | sigma-answer (col) | |
| 35–38 | Which node carries the most? | Q/A ×2 | q-btw-DB, -ans, q-btw-SQ, -ans | |
| 39 | New York: betweenness | 3 fragments | ny-betweenness | |
| 40 | The shortest-path row | | grid-row1 (full) | grid group |
| 41 | A question to sleep on | mid | | |
| 42 | Part Three | | | |
| 43 | Aesop | quote | aesop.jpg | |
| 44 | Importance you inherit | 2 fragments | scrub eigen-inherit | EIG group |
| 45 | It is an eigenvector equation | 2 fragments | eigen-equation (col) | |
| 46–47 | Seven eigenvectors. Which one? | one line above (same length on both) | eig-all-q, eig-all (full) | highlight added |
| 48 | Eigenvector centrality | 1 fragment | eig-pf | EIG group |
| 49–52 | Which lettered node scores higher? | Q/A ×2 | q-eig-L, -ans, q-eig-R, -ans | |
| 53–56 | Eigendecomposition / orthogonal / Square it / Keep multiplying | one line above each | decomp-sum, decomp-orth, decomp-square, decomp-power (full; builds are scrubs) | |
| 57 | Power iteration | stage | power-step | |
| 58 | Where does eigenvector centrality break? | 2 lines + cue | ring-4444 | ring group |
| 59 | Localization | 2 fragments | scrub ring-local (frame 0 = ring-4444) | ring group |
| 60 | New York: eigenvector | 2 fragments | ny-eigenvector | |
| 61 | Part Four | | | |
| 62 | Give everybody a baseline | 3 fragments | katz-floor | |
| 63 | What is that inverse? | 2 lines + cue | katz-floor (same) | text only |
| 64 | The same series for matrices | 3 fragments | scrub walks-discount | |
| 65 | Turn the dial | stage | katz-dial | |
| 66 | Why 1/λmax? | formula above | scrub katz-why (full) | |
| 67–70 | Which lettered node scores higher now? | Q/A ×2 | q-eig-L, q-katz-L-ans, q-eig-R, q-katz-R-ans | |
| 71 | The walk row | | grid-row2 (full) | grid group |
| 72 | Part Five | | | |
| 73 | Hubs and authorities | 3 fragments (the last: on a road map, eigenvector centrality) | hits-graph | |
| 74 | The same idea, six times | | genealogy (full) | |
| 75–76 | Divide the vote | Q (3 fragments) / A (2 lines) | pr-split, pr-split-answer | PR group |
| 77 | A dead end | 2 fragments | scrub pr-leak | PR group |
| 78 | Teleportation | 4 fragments | pr-teleport | PR group |
| 79 | Personalized PageRank | 2 fragments | ppr | PR group |
| 80 | New York: five measures, five places | 2 lines | ny-five | |
| 81 | Two choices, every centrality | | grid-final (full) | grid group |
| 82 | Quiz | mid | | |

Dropped from v2: "Why N − 1?" (now a bullet; star-closeness is no longer built), the "fire
station" text-only slide (now on the bowtie), "On a road map, HITS is eigenvector centrality"
(now a bullet; eig-centrality is no longer built).

## Figure groups (one drawing, one crop)

A group's figures use the same canvas, the same node coordinates and the same crop
(`figlib.emit_group`, or `box=` for figures built in different functions). A build's frame 0
is pixel-identical to the slide before it.

- **Rome** (figs_intro, figs_rome, romelib): roma-basemap → roma-to-graph frames → roma-degree.
- **NY** (figs_ny): every ny-* map, one canvas and one crop.
- **W5** (figs_defs): w5-blank → w5-walks frames.
- **Bowtie** (figs_defs): closeness-def frames, bowtie-closeness (= its last frame), ecc-def
  frames (frame 0 = bowtie-closeness), btw-def frames.
- **CA** (figs_quiz): q-close-CA, q-close-CA-ans, cut-blank, cut-closeness, harmonic-def frames
  (frame 0 = cut-blank), q-harm-CA-ans.
- **Quiz pairs** (figs_quiz): each Q with its answer(s): CB, HD, EA, EB, DB, SQ, EQ_L (eig +
  Katz answers), EQ_R (eig + Katz answers).
- **EIG** (figs_eigen): eigen-inherit frames, eig-pf.
- **Eigen panels** (figs_eigen): eig-all-q, eig-all.
- **Ring** (figs_eigen): ring-4444, ring-local frames.
- **Grid** (figs_defs): grid-empty, grid-row1, grid-row2, grid-final.
- **PR** (figs_dir): pr-split, pr-split-answer, pr-leak frames, pr-teleport, ppr.

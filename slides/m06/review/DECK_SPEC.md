# m06 "All Roads Lead to Rome" — deck spec v2

Slide-by-slide plan for `m06-centrality.md`, expanded from `plan.md` (v2, 2026-10-12).
Sessions **10/20** (slides 1–35) and **10/22** (slides 36–69). One minute per slide.

Every number below comes from `figures/smallgraphs.py` (small graphs) or
`figures/data/ny_network.json` (built by `figures/make_ny.py`). A figure imports the value;
it never types it.

    python3 figures/smallgraphs.py      # prints every quoted number, asserts them

## Non-negotiables (SLIDE_RUBRIC.md, DECK_BUILD_GUIDE.md)

- One point per slide. At most **two lines of body text**; the lecturer says the rest.
- Fragments use `*`. No tables, no code, `cols` is text + figure only.
- A question slide carries no answer anywhere. The answer is on the next slide.
- Every concept slide has a figure. Bold marks key terms only.
- KaTeX does not run inside `<figcaption>` or raw HTML blocks: write symbols as words there.
- Figures: TikZ through `figlib` (never matplotlib), 1 bp = 1 slide px, in-figure text ≥ 36 pt
  (x-height ≥ 15.5 px), node discs 26–52 px (40 bp by default), palette tokens only,
  **no green, no bar charts**, no edge crossings where the graph is planar.

## Containers

| container | authored width | height cap (`.fig` / `tight` / `stack` / `tall`) |
|---|---|---|
| `full` | 1080 bp | 380 / 320 / 190 / 400 |
| `col` (right half of `cols`) | 537 bp | same |

A figure authored for `full` must not be used in a `cols` column, and vice versa.

---

# Day 1 (10/20): measured by shortest paths

| # | title | class/layout | figure (container) | content |
|---|---|---|---|---|
| 1 | All Roads Lead to Rome | lead | — | eyebrow "Module 06", sub "… do they?" |
| 2 | 20 BC, the Forum Romanum | photos row + 3 bullets | `photos/caesar.jpg`, `augustus.jpg`, `milliarium.jpg` (hand-placed) | bullets: Augustus set up the Golden Milestone in 20 BC / A gilded column in the Forum, by the Temple of Saturn / All the roads of Italy were said to end at it. Inscription: lost (speaker note: "a list of cities and miles" is a modern guess, Platner; Digital Augustan Rome). Credit line from `photos/CREDITS.md`. |
| 3 | The roads themselves | cols | `roma-basemap` (col) | OSM map, pins on the 12 cities; credit "© OpenStreetMap contributors" |
| 4 | Keep the roads, drop the map | one line + fig tall | `roma-to-graph.gif` (full, tall) | Q line: "Which city is the most important?" |
| 5 | Today's question, at home | cols | `ny-overview` (col) | "New York State highways: 289 interchanges, 433 roads." Q: "Which of these eight cities do the most cross-state trips pass through?" (answer: slide 33) |
| 6 | Degree centrality | formula + fig tall | `roma-degree` (full, tall; existing) | $d_i = \sum_j A_{ij}$; "counts the neighbours, nothing beyond" |
| 7 | Degree sees one step | fig tall | `two-roads-ahead` (full, tall; existing) | two cities, same degree, different reach two steps out |
| 8 | New York: degree | cols | `ny-degree` (col) | "201 interchanges have degree 3, 57 have 4." "Degree cannot tell them apart." |
| 9 | How far is u from v? | mid, cols | `w5-blank` (col) | question only |
| 10 | Two ways to count | cols | `w5-walks.gif` (col) | * shortest path: one number, 2 * walks: a count for every length: 2, 1, 11, … |
| 11 | Two choices make a centrality | one line + fig | `grid-empty` (full) | "Which routes count? How do they become one number?" |
| 12 | Close to everything | part | — | |
| 13 | Closeness centrality | cols | `closeness-def.gif` (col) | $c_i = \dfrac{N-1}{\sum_{j \ne i} \ell_{ij}}$, $\ell_{ij}$ = length of a shortest path |
| 14 | Why N − 1? | cols | `star-closeness` (col; existing) | "Best case: everyone one step away. Score exactly 1." |
| 15 | Which node is closest to everything? | one line + fig | `quiz-close` (full) | question only |
| 16 | Answer | fig | `quiz-close-answer` (full) | left F (19) beats E and G (20); right P (16) beats N (18) |
| 17 | New York: closeness | cols | `ny-closeness` (col) | distance = km of road; winner NY 17 / US 209 at Middletown; a third of the interchanges are within 60 km of Manhattan |
| 18 | What if one road closes? | mid, cols | `cut-blank` (col) | left quiz graph with E–F removed; question only |
| 19 | Every score drops to zero | cols | `cut-closeness` (col) | "Some ℓ = ∞, so every sum = ∞, so every c = 0." |
| 20 | Take the reciprocal first | cols | `harmonic-def.gif` (col) | $h_i = \sum_{j \ne i} \dfrac{1}{\ell_{ij}}$, $1/\infty = 0$ |
| 21 | Which node has the highest harmonic centrality? | one line + fig | `quiz-harm` (full) | question only |
| 22 | Answer | fig | `quiz-harm-answer` (full) | left E (27/4) now beats G (19/3) and F (35/6); right N (4) beats T (11/3) |
| 23 | Would you site a fire station on the average? | mid | — | question only |
| 24 | Eccentricity | cols | `ecc-def.gif` (col) | $e_i = \max_{j} \ell_{ij}$, eccentricity centrality $= 1/e_i$ |
| 25 | Which node has the smallest eccentricity? | one line + fig | `quiz-ecc` (full) | question only |
| 26 | Answer | fig | `quiz-ecc-answer` (full) | left F (2) while E wins closeness; right L (2, degree 2) while K wins closeness |
| 27 | New York: eccentricity | cols | `ny-eccentricity` (col) | the smallest worst-case drive: 473 km, NY 17 east of Binghamton |
| 28 | The broker | part | — | |
| 29 | Trace a letter | cols | `btw-def.gif` (col) | "A letter for every pair, along a shortest path. Count the letters each node carries." |
| 30 | Betweenness centrality | formula + fig | `sigma-answer` (full; existing) | $b_i = \sum_{s<t} \dfrac{\sigma_{st}(i)}{\sigma_{st}}$; "two shortest routes: each carries half" |
| 31 | Which node carries the most? | one line + fig | `quiz-btw` (full) | question only |
| 32 | Answer | fig | `quiz-btw-answer` (full) | left E and G (30) beat the bridge F (25); right O (19/2) beats M (9) |
| 33 | New York: betweenness | cols | `ny-betweenness` (col) | Binghamton first of the eight (3.5 times Syracuse); the NY 17 corridor joins NYC to upstate |
| 34 | The shortest-path row | fig | `grid-row1` (full) | |
| 35 | A question to sleep on | mid | — | "Is a city important because its neighbours are important?" |

# Day 2 (10/22): measured by walks

| # | title | class/layout | figure (container) | content |
|---|---|---|---|---|
| 36 | Known by the company you keep | cols | `photos/aesop.jpg` (hand-placed) | "A man is known by the company he keeps." — The Ass and His Purchaser (Perry 237) |
| 37 | Importance you inherit | cols | `eigen-inherit.gif` (col) | $c_i = \dfrac{1}{\lambda} \sum_j A_{ij} c_j$ |
| 38 | It is an eigenvector equation | fig | `eigen-equation` (full) | $A\mathbf{c} = \lambda \mathbf{c}$ on the 7-node graph |
| 39 | Seven eigenvectors. Which one? | mid | — | question only |
| 40 | All seven | fig tall | `eig-all` (full, tall) | 7 copies of the graph, nodes coloured by sign and size of the entry; eigenvalues on a number line with values and arrows; only the largest is all positive |
| 41 | Perron and Frobenius | cols | `eig-pf` (col) | "Connected network: the largest eigenvalue's eigenvector is the only one with every entry positive." |
| 42 | Eigendecomposition | fig | `decomp-sum.gif` (full) | $A = \sum_k \lambda_k \mathbf{u}_k \mathbf{u}_k^\top$; each term is a rank-1 matrix |
| 43 | The eigenvectors are orthogonal | fig | `decomp-orth` (full) | $\mathbf{u}_k^\top \mathbf{u}_\ell = 0$ for $k \ne \ell$, $= 1$ for $k = \ell$ |
| 44 | Square it | fig | `decomp-square.gif` (full) | $A^2 = \sum_k \lambda_k^2 \mathbf{u}_k \mathbf{u}_k^\top$ |
| 45 | Keep multiplying | fig | `decomp-power.gif` (full) | $A^t = \sum_k \lambda_k^t \mathbf{u}_k \mathbf{u}_k^\top$; the largest circle wins |
| 46 | Power iteration | stage | `power-step` (stage) | button "× A"; colours and values per node; B overtakes D by step 5 |
| 47 | Step one is degree | cols | `power-step1` (col) | $A\mathbf{1}$ = the degrees |
| 48 | Where does this break? | mid, cols | `ring-4444` (col) | question only |
| 49 | Localization | fig | `ring-local.gif` (full) | one clique grows 4 → 8; share of the eigenvector in it: 25% → 89% → 97% → 99% → 99% |
| 50 | New York: eigenvector | cols | `ny-eigenvector` (col) | 99.7% of the score within 60 km of Manhattan, where 31% of the interchanges sit |
| 51 | Everyone gets a floor | part | — | |
| 52 | Give everybody a baseline | cols | `katz-floor` (col) | $c_i = \beta + \alpha \sum_j A_{ij} c_j \;\Rightarrow\; \mathbf{c} = \beta (I - \alpha A)^{-1} \mathbf{1}$ |
| 53 | What is that inverse? | mid | — | $\dfrac{1}{1-x} = 1 + x + x^2 + \cdots$ for $\lvert x \rvert < 1$ |
| 54 | The same series for matrices | cols | `walks-discount.gif` (col) | $(I - \alpha A)^{-1} = I + \alpha A + \alpha^2 A^2 + \cdots$; $A^k$ counts walks of length $k$ |
| 55 | Turn the dial | stage | `katz-dial` (stage) | α slider, 0 to 1.2 × 1/λ_max, on the ring (4,4,4,6) |
| 56 | Why 1/λ_max? | fig | `katz-why.gif` (full) | $(I-\alpha A)^{-1} = \sum_k \dfrac{1}{1-\alpha\lambda_k} \mathbf{u}_k\mathbf{u}_k^\top$ |
| 57 | The walk row | fig | `grid-row2` (full) | |
| 58 | The Web has direction | part | — | "A road runs both ways. A link does not." |
| 59 | Hubs and authorities | cols | `hits-graph` (col) | $a_i = \sum_j A_{ji} h_j$, $h_i = \sum_j A_{ij} a_j$; hub A, authority E |
| 60 | On a road map, HITS is eigenvector centrality | cols | `eig-centrality` (col) | $A^\top A = A^2$ when $A$ is symmetric |
| 61 | The same equation, six times | fig | `genealogy` (full; existing) | |
| 62 | Divide the vote | cols | `pr-split` (col) | $c_i = \sum_j A_{ji}\, c_j / d^{\text{out}}_j$; Q: "C has three links in, E has one. Who ranks higher?" |
| 63 | A three-way tie | cols | `pr-split-answer` (col) | A, C, E: 3/11 each; B, D: 1/11 |
| 64 | A dead end | cols | `pr-leak.gif` (col) | E loses its only link; the total drains 1 → 0.8 → 0.6 → 0.13 → 0 |
| 65 | Teleportation | cols | `pr-teleport` (col) | $c_i = (1-r)\sum_j A_{ji}\, c_j / d^{\text{out}}_j + r/N$, r = 0.15 |
| 66 | Personalized PageRank | cols | `ppr` (col) | teleport only to A |
| 67 | New York: five measures, five places | cols | `ny-five` (col) | closeness Middletown, harmonic the Bronx, eccentricity east of Binghamton, betweenness Monticello, eigenvector Long Island |
| 68 | Two choices, every centrality | fig tall | `grid-final` (full, tall) | the classification, completed |
| 69 | Quiz | mid | — | "Draw a network where degree, closeness, eccentricity and betweenness each crown a different node." |

---

# Figure contract (every figure agent reads this)

## Pipeline
- Read `slides/FIGURE_GUIDE.md` first, then `figures/figlib.py` (docstrings and the drawing helpers).
- One module per agent, `figures/figs_<part>.py`, exposing `FIGURES = [(name, fn), ...]`. Build and
  check your own module only:

      cd slides/m06/figures && python3 -c "import figlib, figs_<part> as m; figlib.run(m.FIGURES)"

  Do not edit another agent's module, `make_figures.py`, the deck, or `smallgraphs.py`
  (ask the lead if a number is missing).
- Stills: `figlib.emit(name, body, container=..., h=..., hmod=...)`.
  GIFs: `figlib.emit_gif(name, frames, container=..., h=..., hmod=..., ms=..., hold=..., durations=...)`.
  A GIF's **last frame is the complete picture** (it is held), and where a still of the same scene
  exists the last frame equals it.
- Every number on a figure comes from `smallgraphs.py` or `data/ny_network.json`. Assert the facts a
  figure depends on (who wins, ties) at build time.
- **Open every PNG you write with the Read tool** and check it against this spec before you report.
  For a GIF, also check a middle frame (extract it with PIL into `figures/data/`).

## Visual language (shared by all modules)
- Node: `figlib.disc` (40 bp, accent blue fill, white letter inside). Letters are the node names in
  `smallgraphs.py`. Edges black 2.6 bp.
- The winner of a question: `figlib.mark` (thick accent-2 border) plus its value printed beside it
  in accent-2. Other candidates' values in black. Never a ring (the gate measures it as a disc).
- A score shown as colour: a sequential ramp from white-ish (`accent!10`) to full `accent`; the
  number itself printed beside the node when the slide quotes it.
- A sign: positive = `accent` (blue), negative = `accentthree` (gold), strength = shade (`!xx`).
- Accent-2 red is for the one thing the slide is about (winner, emphasised label). Never a group colour.
- Text ≥ 36 pt. Figure text in Latin Modern (the preamble default). Math via `$...$` inside TikZ nodes.
- Quiz figures (`full`): left graph in x ∈ [20, 520], right graph in x ∈ [560, 1060], a thin gray
  vertical rule between them is optional. Scale grid units of `smallgraphs.*_XY` uniformly; the
  same scale for both graphs on one slide. Answer figures are the question figure plus values and
  marks, same geometry (assert it).

## NY maps (`figs_ny.py`)
- Data: `figures/data/ny_network.json` (nodes with lon/lat and all measures, edges with km,
  cities, outline). Project lon/lat with a simple equirectangular map scaled by cos(42.5°).
- `col` container, map about 490 bp wide. Outline in gray, edges in light gray, nodes as small
  dots (`figlib.dot`, 8–12 bp), so call `emit(..., nodes=False)`. Colour/size the dots by the
  measure (sequential ramp). Mark the winner with a larger accent-2 dot and a short label.
- Labels: at most 4 place names per map at 36 pt, with short leader lines if needed.
- `ny-overview`: the 8 cities as accent dots with names (abbreviate "New York City" to "NYC").
- `ny-five`: five winners, each marked and labelled with the measure name.

## Small graphs and quizzes (`figs_quiz.py`)
- `w5-blank` (col): Module 01's 5-node graph (`W5`, `W5_XY`), u and v marked, other nodes unlabeled.
- `w5-walks.gif` (col): stage 1 the shortest path u → n2 → v drawn heavy, "shortest path: 2";
  stage 2 the two walks of length 2 one after the other ("length 2: 2 walks"); stage 3 the one walk
  of length 3 ("length 3: 1"); last frame: the numbers 2, 1, 11 listed as "walks of length 2, 3, 4".
- `grid-empty`, `grid-row1`, `grid-row2`, `grid-final` (full): two rows, "shortest paths" and
  "walks". Shortest-path row cells: closeness "sum of lengths", harmonic "sum of 1/length",
  eccentricity "longest", betweenness "paths passing through". Walk row cells: degree "walks of
  length 1", Katz "all lengths, discounted", eigenvector "the longest walks", PageRank "walks that
  split the vote", HITS "walks that alternate direction". `grid-empty` shows the two row labels and
  only degree; `grid-row1` adds the first row; `grid-row2` adds degree, Katz and eigenvector;
  `grid-final` (tall) has everything plus a small icon per cell in the manner of the old
  `purpose-5.png` if it fits at the 26 px disc floor (drop the icons if not).
- Definition GIFs on `BT` (`BT_XY`), each col:
  - `closeness-def.gif`: from A, distances appear ring by ring next to each node; "sum = 15";
    last frame: every node's sum (D smallest, 9). Assert from `dsum(BT)`.
  - `ecc-def.gif`: for each node in turn an arrow to its farthest node with the distance; last frame
    every node's eccentricity, D = 2 marked.
  - `btw-def.gif`: pairs (s, t) one at a time, the shortest path highlighted, the counter on each
    inner node increases; last frame all counts (D 9, C and E 8).
- `harmonic-def.gif` (col) on `CA_CUT` (`CA_XY`, edge E–F drawn dashed and crossed out): from G,
  "1/1" on F, H, I, J, "1/2" on K, "1/∞ = 0" on the other piece; "sum = 9/2"; last frame every
  node's harmonic value. Assert from `harmonic(CA_CUT)`.
- `cut-blank` (col): `CA_CUT`, no numbers. `cut-closeness` (col): same, "0" beside every node.
- `quiz-close`, `quiz-close-answer`: `CA` left, `CB` right. Answer prints the sum of distances next
  to the candidates (E, F, G; N, P) and marks F and P.
- `quiz-harm`, `quiz-harm-answer`: `CA` left, `HD` right. Answer prints harmonic values as
  fractions (E 27/4, G 19/3, F 35/6; N 4, T 11/3) and marks E and N.
- `quiz-ecc`, `quiz-ecc-answer`: `EA` left, `EB` right. Answer prints the eccentricity beside every
  node and marks F and L; the closeness winners (E, K) get "closeness" as a small gray tag.
- `quiz-btw`, `quiz-btw-answer`: `DB` left, `SQ` right. Answer prints the betweenness of the
  candidates (E 30, F 25, G 30; M 9, O 19/2) and marks E, G and O.

## Eigenvectors, decomposition, Katz (`figs_eigen.py`)
- Graph `EIG` (`EIG_XY`, `EIG_ORDER`), spectrum from `smallgraphs.spectrum`.
- `eigen-inherit.gif` (col): node A's score is the sum of its neighbours' scores: arrows from
  B, D, F, G into A light up one at a time; then the same for B. Last frame: the graph with the
  eigenvector shading.
- `eigen-equation` (full): in the style of the old `eigen-equation.png` (A as a square labelled
  "7 × 7", c as a shaded column, "= λ c"), λ = 2.88.
- `eig-all` (full, tall): seven small copies of the graph (disc 26–28 bp, no letters), one per
  eigenvector, nodes filled by sign and strength (blue positive, gold negative, white near 0); a
  number line below with the seven eigenvalues as dots and their values, an arrow from each dot
  to its copy. The largest (2.88) copy marked with accent-2. Assert exactly one all-positive.
- `eig-pf` (col): the largest eigenvalue's copy, large, letters in discs, every entry printed.
- Decomposition figures use the notation of `lecture-note/figs/spectral-decomposition.jpg`:
  eigenvalue = filled circle whose diameter ∝ |λ| (blue for positive, gold for negative) with its
  value printed; u_k = tall rectangle; u_kᵀ = wide rectangle; matrix = square. Show the first
  three terms, "+ ⋯", and the last term.
  - `decomp-sum.gif`: "A =" then the terms appear one at a time; last frame complete.
  - `decomp-orth`: u_kᵀ u_ℓ as a wide-rect × tall-rect = 0 for k ≠ ℓ, = 1 for k = ℓ.
  - `decomp-square.gif`: A² written as the product of two sums; the cross terms fade out (marked
    "= 0"); the circles become λ_k² (sizes and values update).
  - `decomp-power.gif`: t = 1, 2, 4, 8, 16: circle k drawn with diameter ∝ (|λ_k|/λ_1)^t, values
    (λ_k/λ_1)^t printed; by t = 16 only the first circle is visible.
- `power-step1` (col): the graph with each node's degree printed; caption-free.
- `ring-4444` (col): `clique_ring((4,4,4,4))` drawn as four cliques on a ring, shaded by the
  eigenvector (all equal).
- `ring-local.gif` (full): K = 4, 5, 6, 7, 8 for the last clique, shaded by the eigenvector,
  share printed: 25%, 89%, 97%, 99%, 99% (from `eig_share`; use `figlib.pct`).
- `katz-floor` (col): the 7-node graph, each disc with a small "β" tag, arrow-in from neighbours
  labelled α.
- `walks-discount.gif` (col): on `W5`, walks from u of length 1, 2, 3 drawn in turn, the weight
  α, α², α³ beside them, each longer walk drawn fainter.
- `katz-why.gif` (full): the circle picture of Σ_k 1/(1 − αλ_k) u_k u_kᵀ for α = 0, 0.5, 0.8, 0.95,
  0.99 × 1/λ_1, then 1.1 × 1/λ_1 (first circle turns gold: negative). Values printed.
- `eig-centrality` (col): the 7-node graph shaded by the eigenvector, values printed.

## Directed (`figs_dir.py`)
- Pages as rounded boxes with a letter, arrows with arrowheads that stop at the box border.
- `hits-graph` (col): `HITS_EDGES`; A marked "hub", E marked "authority" (values 1.0).
- `pr-split` (col): `PR_EDGES`; each arrow labelled with the share it carries (1/3 from A, 1 from
  the others). No scores (question slide).
- `pr-split-answer` (col): same + scores: A, C, E 3/11; B, D 1/11.
- `pr-leak.gif` (col): `PR_DEAD` (E→A removed, E drawn as a dead end); frames = steps 0..4, page
  shading by score, "total = 1, 0.8, 0.6, 0.13, 0" (from `PR_leak_trace`).
- `pr-teleport` (col): `PR_EDGES` with r = 0.15; scores printed (C 0.276, E 0.265, A 0.255,
  B 0.102, D 0.102), C marked.
- `ppr` (col): teleport only to A (dashed arrows from every page back to A); scores printed, A marked.

## Rome (`figs_intro.py`)
- `roma-basemap` (col): `figures/data/roma-basemap-pale.png` (from `make_basemap.py`) placed with
  `\includegraphics` in TikZ, about 416 bp wide × 380 bp tall; pins (accent-2 dots, 14 bp) at the 12
  cities from `roma-basemap.json`; label only "Roma"; small "© OpenStreetMap contributors" in the
  corner at 36 pt is too large, so the credit goes in the slide's figcaption instead.
- `roma-to-graph.gif` (full, tall, h = 470 like the old map): frame 0 the map with pins (map at the
  left, scaled to the 396 bp ink height); the map fades (3 frames); straight edges appear between
  pins (`romelib.EDGES`); the pins slide to `romelib.NODE_XY` (6 frames, linear interpolation) and
  become discs; last frame = the old `roma-graph.png` picture (names placed by `romelib`).

# m06 — figure spec

What each figure draws, which container it is authored for, and what the generator must
assert. Standards are `FIGURE_GUIDE.md`; this file is the work list.

    python3 figures/make_figures.py             # all of them
    python3 figures/make_figures.py roma        # only names containing "roma"
    python3 figures/make_animations.py          # the GIF

## Layout of the generator

    figures/figlib.py          the pipeline and every gate (copied from m04, unchanged)
    figures/verify_numbers.py  every number, computed and asserted (already green)
    figures/romelib.py         the ONE Roman-map geometry every metric figure reuses
    figures/figs_rome.py       Parts 1-4: the map and its crowns
    figures/figs_small.py      the purpose-built small graphs (club, sigma, broker, star…)
    figures/figs_walk.py       Parts 5-6: eigenvector, power iteration, Katz
    figures/figs_web.py        Parts 7-8: the directed web, and the closing figures
    figures/make_figures.py    entry point; `figlib.run()` catches per figure

Nothing may hardcode a number a slide states. Import it from `verify_numbers`.

## Rules that bite in this module specifically

- **One geometry, seven scores (F1).** Every Roman-map figure is drawn from
  `romelib.NODE_XY` and `romelib.EDGES`. The *only* things that may differ between two
  metric figures are node shading and the crown. `romelib.assert_same_geometry()` is
  called by every one of them, and `make_figures.py` fails if a figure draws a node
  anywhere else.
- **A crown can be shared.** Eccentricity crowns three cities and the path graph's degree
  crowns five. The drawing must show all of them; a figure that silently draws one crown
  where the data has three is a false claim.
- **Shading encodes the score and nothing else.** State the encoding in the figcaption of
  every metric figure ("darker = higher *closeness*"). Two figures that shade by different
  metrics must never be reused for each other's slide.
- **`accent-3` is fills and rings only** — never a label, never a thin stroke (2.0:1 on
  white).
- **No green anywhere.** Palette is accent `#3959A6`, accent-2 `#B14434`, accent-3
  `#DAB167`, gray `#6b6b6b`, ink black.
- **No bar charts.** Where a figure would compare scores, draw the objects and annotate
  the numbers, or use a dot plot / slope.
- **Reuse only where both slides explain the figure identically.** `club-three-kings.png`
  is used on slides 12 and 41 and that is the only reuse in the deck; everything else
  emits its own file. (m01 leaked a concept 41 slides early doing otherwise.)

---

# THE SHARED ROMAN MAP  (`romelib.py`)

Twelve discs at fixed positions derived from the real longitude/latitude in
`verify_numbers.ROMA_POS`, linearly mapped into the drawing box and then **frozen**. Every
figure imports `NODE_XY`; none recomputes it.

Assertions in `romelib`, run once at import:

- the drawing has **zero edge crossings** (`figlib.assert_planar_drawing`)
- no edge passes through a disc it does not end at
- every city name is placed by `figlib.place_labels` — no hand-assigned sides
- the label solver is given a vertical band, not the whole canvas, so a label cannot push
  the figure past its height cap
- `assert_same_geometry(name, xy)` — any figure whose node coordinates differ from
  `NODE_XY` fails the build with the offending city named

Two container variants are needed and both are authored explicitly:

- `full` — 1080 bp wide, for the slides where the map is the whole slide
- `col` — 537 bp wide, for the slides where the map sits beside text

A figure authored `full` and used in a `cols` column renders at 48% and
`check_render.py` fails the build. Keep the generator's declaration and the deck's markup
in step; the gate compares them.

---

# FIGURE LIST

Container is `full` unless marked `col`. Every metric map takes the same
`shade = score / max(score)` ramp from white to accent, with the crown drawn as an
accent-2 ring plus a small crown glyph above the disc.

## Part 1 — the story

| name | what it draws | assert |
|---|---|---|
| `milestone` | the Milliarium Aureum: a drawn bronze-clad column on its surviving base, in the Forum. **Drawn in TikZ, not a photograph** — no licence to clear, and a photo cannot be held to the type floor. | ink on page; x-height ≥ 15.5 px |
| `milestone-radial` | the stone at the centre, four labelled spokes to real provinces with their real distances in Roman miles | the four distances come from a constant in the module with a source comment; spokes do not cross labels |
| `roma-map` | the Mediterranean coastline sketched in gray, the eighteen routes drawn on top in ink, cities as discs | zero crossings; coastline is annotation-gray and never accent |
| `roma-graph` | the same twelve discs and eighteen edges with the coastline removed — **the base drawing of the deck** | `assert_same_geometry`; zero crossings; node 26–52 px |
| `club-blank` | thirteen student names as discs, no edges, laid out so the eight clubs can be drawn without a crossing | `nx.check_planarity` is True and the drawn layout has zero crossings |
| `club-three-kings` | the club network three times (build): crown on Noah / Sophia / Alex, each panel captioned with the question it answers | the three crowned names come from `verify_numbers.CLUB_*`; the three panels are geometrically identical |

## Part 2 — degree

| name | what it draws | assert |
|---|---|---|
| `degree-count` | one city with its five edge-ends marked one at a time (build) | the count drawn equals `ROMA.degree` |
| `roma-degree` | the map shaded by degree, crown on Roma, the two counts 5 and 4 annotated | crown set equals `ROMA_CROWNS["degree"]` |
| `degree-local` (col) | the same map with everything past one city's neighbours in 15% gray | greyed set is exactly the non-neighbours |
| `two-roads-ahead` | one city with a one-step ring and a two-step ring, the two onward paths labelled "distance" and "walks" | ring radii do not overlap a disc |

## Part 3 — distance

| name | what it draws | assert |
|---|---|---|
| `roma-distance-rings` | shortest-path distance from Rome as shaded bands (0,1,2,3) | band membership equals BFS layers |
| `closeness-one-city` | Massilia with its eleven distances written on the map | the eleven numbers equal the BFS distances; sum = 22 |
| `closeness-blank` | the same, distances blank — the Your-turn slide | no digits drawn anywhere in the figure |
| `roma-closeness` | the map shaded by closeness, crown on Roma, 0.611 and 0.500 annotated | crown equals `ROMA_CROWNS["closeness"]` |
| `star-closeness` (col) | a 7-node star, hub annotated exactly 1.0 | `STAR_C["closeness"][0] == 1.0` |
| `roma-cut` | the map with the Channel crossing drawn as a broken edge | exactly one edge is broken, and it is `CUT_EDGE` |
| `roma-cut-closeness` | the cut map, **every** disc the same shade, no crown, one annotation "every score: 0" | all shades equal; no crown glyph present |
| `roma-cut-harmonic` | the cut map shaded by harmonic, Rome crowned, Londinium alone at 0 | 8 distinct shade levels; Londinium is the only white disc |
| `roma-eccentricity` | the map shaded by eccentricity with **three** crowns | crown set equals the three cities in `ROMA_CROWNS["eccentricity"]` |

## Part 4 — betweenness

| name | what it draws | assert |
|---|---|---|
| `betweenness-idea` | one node with the shortest paths that cross it drawn through it | the drawn paths really are shortest paths |
| `sigma-graph` | the five-node σ demo, S and D marked | matches `SIGMA_EDGES` |
| `sigma-blank` | the same with nothing counted | no digits |
| `sigma-answer` | the two routes drawn in accent and accent-2, the fractions ½, ½, 1 placed | fractions equal `SIGMA_BT` |
| `roma-betweenness` | the map shaded by betweenness, crown on Roma | crown equals `ROMA_CROWNS["betweenness"]` |
| `roma-betweenness-runnerup` | the same map, Mediolanum ringed, "3 roads · 0.270" and "4 roads · 0.182" annotated | the two pairs come from `ROMA_C` and `ROMA.degree` |
| `broker` | two 4-cliques joined through M, M crowned, "16 pairs" annotated | `BROKER_C` crown is M and `BROKER_PAIRS == 16`; zero crossings |
| `attack-compare` | two small maps side by side (build): after two degree strikes, after two betweenness strikes, survivors shaded | survivor counts equal `ATTACK_SURVIVORS` (7 and 5) |

## Part 5 — the recursion

| name | what it draws | assert |
|---|---|---|
| `same-degree-different-friends` (col) | two nodes of equal degree with visibly different neighbourhoods | the two degrees really are equal |
| `recursive-flow` | score arriving at one node from its neighbours, arrows weighted | arrowheads meet the discs (TikZ `--` to node border) |
| `eigen-equation` | A · c returning c rescaled, drawn as the matrix acting on the vector | the drawn matrix is `ROMA`'s adjacency, no invented entries |
| `spectrum` | the twelve eigenvalues on a line, λ_max = 3.35 marked | values equal `np.linalg.eigvalsh` |
| `power-iteration.gif` | the map re-shading each iteration, step counter, crown appearing at step 1 | frames come from `POWER_TRACE`; the final frame equals `roma-eigenvector`'s shading (loop hands off) |
| `decay` | \|λ_i/λ_1\|^t against t for every mode, the slowest (0.795) labelled | the labelled mode is the max **absolute** ratio, not λ_2 |
| `walks-arrive` | walks of length t arriving at a node | drawn walks are real walks in `ROMA` |
| `roma-eigenvector` | the map shaded by eigenvector, crown on Roma, Alexandria annotated "8% behind, one road fewer" | 8 equals `EIG_GAP_PCT` |
| `localization` | 5-clique with a 4-node tail, shaded by eigenvector, tail annotated 0.0045 | equals `LOCAL_TAIL_FRACTION`; zero crossings |

## Part 6 — Katz

| name | what it draws | assert |
|---|---|---|
| `katz-floor` | the localization graph shaded by Katz, tail annotated 0.184 | equals `LOCAL_KATZ_FRACTION` |
| `katz-solve` | the rearrangement to the closed form, annotated | no numbers invented |
| `katz-series` | the walk series as a build: t = 0, 1, 2, 3 terms with λ^t weights | term magnitudes equal `katz_series` output |
| `katz-dial` | the ranking under three λ values, shown as three columns of ordered discs (a slope, not bars) | orderings computed, not asserted by hand |
| `katz-diverge` | scores against λ, crossing zero past 1/λ_max = 0.2989 | eleven cities go negative at λ = 0.3437 |
| `roma-katz` | the map shaded by Katz, crown on Roma | crown equals `ROMA_CROWNS["katz"]` |

## Part 7 — the web

| name | what it draws | assert |
|---|---|---|
| `web-graph` | eight pages, fourteen **arrows**, the dangling page and the link page visibly so | arrowheads meet the discs; zero crossings; out/in degrees match `WEB` |
| `hub-authority` | the two roles, drawn on two small sub-networks | — |
| `hits-equations` | x = Ay and y = Aᵀx as a picture | follows the standard convention (see spec note on c20) |
| `web-blank` | the web with no scores — the Your-turn slide | no digits |
| `web-hits` | both crowns on one drawing, each labelled with its meaning | crowns equal `WEB_HUB_KING` and `WEB_AUT_KING` |
| `hits-collapses` | the Roman map scored as hub and as authority, identical | the two score vectors agree to 1e-8 |
| `genealogy` | 1895 → 1998 as a **timeline figure**, six markers, each with name and what they were ranking | the six years are the verified ones; never a table |
| `pagerank-split` | one page's score divided among its out-links, the fractions drawn on the arrows | fractions sum to 1 |
| `web-pagerank` | the web shaded by PageRank, Blog crowned, **Links annotated "8th of 8"** | equals `WEB_PR_RANK_OF_LINKS` |
| `web-dangling` | the dead-end page marked, nothing else | exactly one page marked, and it is `WEB_DANGLING[0]` |
| `teleport` | the walker's jump drawn as a dashed accent-2 arc out of the dead end | dashed arc does not cross a disc |
| `ppr` | the web under personalization on Course, the focus ringed, Course/Blog scores annotated | equals `WEB_PPR`; the margin flip (0.009 → 0.125) is computed |

## Part 8 — choosing

| name | what it draws | assert |
|---|---|---|
| `crown-summary` | the six results as a build, one metric per step, same geometry each time | every panel passes `assert_same_geometry` |
| `purpose` | five purposes, each with its metric, revealed one at a time as annotated graphics | **not a table** — check the emitted markup has no `\|` rows |
| `robustness` | for each metric, the share of the 4992 variants in which Rome keeps the crown, as a **dot plot** with the metric names — no bars | values equal `crown_robustness()` |
| `redraw` | the two maps as a build, the traded edges highlighted, the crown moving to Mediolanum | the second panel's crown equals `REDRAW_CROWNS["betweenness"]` |
| `cost` | cost against n as curves (n·m vs m per step), log axes, the 10⁶ point marked | the 33,000 ratio is computed |
| `star-vs-path` | two panels: the star with one crown on every metric, the path with five degree crowns and one betweenness crown | crown counts equal `STAR_CROWNS` / `PATH_CROWNS` |
| `applications` | three small networks: vaccination, infrastructure, financial contagion, each with its metric named | — |
| `next-module` | a walker mid-teleport on the web | hands off to M07 |

---

# THE SLIDER  (slide 50)

Built the way m01's was: a `<script>` plus `<input type="range">`, styled from the theme
(Marp strips `style` attributes). Two conditions carried over from `DECK_BUILD_GUIDE.md`:

1. It needs `--html` (or `html: true`), **and that flag changes the whole deck** — without
   it every raw `<div class="cols">` is escaped to literal text.
2. `--images png` parses raw HTML either way, so **`check_render.py` never exercises the
   export the lecture is given from**. After adding the slider, open the HTML build and
   drive the real control; checking that the `<script>` survived is not checking that it
   runs.

Data comes from `verify_numbers.POWER_TRACE`, serialised into the deck at build time by the
generator, so the slider and `power-iteration.gif` cannot drift.

If driving the real slider is not possible in this environment, **say so in the round
report** and ship the GIF alone rather than an untested widget.

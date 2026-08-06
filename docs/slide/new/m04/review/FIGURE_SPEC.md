# m04 figure spec

53 figures + 1 animation, all emitted by `figures/make_figures.py`, which imports the
pipeline from `figures/figlib.py` and every number from `figures/verify_numbers.py`.
Figures are grouped into `figs_story.py` (Parts 1–4), `figs_tail.py` (Parts 5–6) and
`figs_edge.py` (Parts 7–8) so they can be authored in parallel without touching one file.

## The contract every figure is held to

Read `../../FIGURE_GUIDE.md` first; this is the module-specific part.

- **One bp is one slide pixel.** Canvas widths are 1080 bp (`container="full"`) and
  537 bp (`container="col"`). Nothing else. Do not pass a `w:` directive in the deck —
  it is inert under this theme.
- **Height budget.** After the height crop, the drawing must be at most **380 bp** tall
  (`hmod=""`), 320 bp (`hmod="tight"`) or 190 bp (`hmod="stack"`). Over that, the height
  binds the scale and every label in the figure shrinks; `crop_and_check` fails the build
  and tells you to shorten the drawing, never the type.
- **Type floor.** `FONT = 36` pt is the floor and `figlib.text()` refuses anything smaller.
  At scale 1.0 that is 15.5 px x-height on the slide against a 15 px gate. The ratio is
  **measured** from a compiled glyph each build (`calibrate()`), not quoted.
- **Node discs** are `NODE = 40` bp (`SMALLNODE = 28` only where a figure draws dozens).
  The gate band is 26–52 px on the slide.
- **Ink must span ≥ 76% of the canvas width.** A figure that does not is scaling white
  margin; widen the drawing rather than narrowing the canvas.
- **Palette:** accent `#3959A6`, accent-2 `#B14434`, accent-3 `#DAB167` (fills and rings
  only — 2.0:1 on white, never text and never a thin stroke), gray `#6b6b6b` for
  annotation, black for ink. **No green. No bar charts.**
- **One colour, one meaning, per figure**, and the meaning is stated on the slide or in
  an in-drawing label.
- **Assert what the figure draws.** Every printed number is computed from
  `verify_numbers.py`, never typed. Every node-link figure of a planar graph calls
  `assert_planar_drawing(edges, pos, name)`. Names are placed by `place_labels()`, which
  raises rather than shrinking type when no collision-free assignment exists.
- **Never share a figure between slides that explain it differently.** Two slides needing
  different content means two files. The one deliberate reuse is `feld-names.png` on
  slides 6 and 7, and `linear-axes.png` on 47 and 48 — same picture, same explanation.
- Emit failures do not stop the build: `figlib.run()` catches per figure, prints each,
  and exits non-zero at the end.

## The Feld graph — one layout, used by nine figures

Eight girls, ten edges, **planar**. Feld's own Figure 1 crosses Sue–Dale with Alice–Pam;
ours must not (F2). One `FELD_POS` dict lives in `figs_story.py` and every Feld figure
imports it, so the graph never changes size or shape between consecutive slides.

Required layout properties, all asserted:

- `assert_planar_drawing(FELD_EDGES, FELD_POS, "feld")` — zero crossings, and no edge
  passing through a disc it does not end at
- `place_labels()` solves the eight names against the discs, the edges and each other
- the drawing fits the full-width canvas at ≤ 380 bp tall

Suggested shape (Betty and Tina are the pendants, Carol the bridge): the K₅-minus-3-edges
core {Sue, Alice, Jane, Dale, Pam} on the left, Pam → Carol → Tina running right, Betty
hanging off Sue. Solve the positions so the four core faces are convex.

---

## Batch A — `figs_story.py` (Parts 1–4, 24 figures)

| file | container | contents | asserted |
|---|---|---|---|
| `timeline-1961.png` | full | a horizontal rule with two marks: **1961 · James Coleman surveys 12 high schools** and **1991 · Scott Feld reopens one of them**. Gray rule, accent marks, names in ink. | both years present; ink span ≥ 76% |
| `feld-names.png` | full | the eight girls, names only, no degrees anywhere | planar; no number appears in the body |
| `feld-degrees.png` | full | same layout, each disc carrying its degree in white | degrees drawn = degrees computed from `FELD_EDGES` |
| `feld-worksheet.png` | full | same layout with degrees, one girl (Jane) ringed accent-2, and a blank rule under the drawing where the room writes her friends' average | **no friend-mean value anywhere** — this sits on a question slide |
| `feld-friendmeans.png` | full | each disc keeps its degree; a chip beside each girl gives her friends' mean (4.00, 2.75, 3.00, 3.50, 3.33, 3.33, 2.00, 2.00); discs of the five below are accent-2, the two above accent, Carol gray | chip values recomputed; exactly 5 / 2 / 1 by colour |
| `feld-two-numbers.png` | full | two large numerals, **2.5** (what a girl has) and **3.0** (what her friends have), with the network small at the left | both from `moments()` |
| `marketville-146.png` | full | 146 small discs in a block, coloured 80 accent-2 (below) / 41 accent (above) / 25 gray (equal), with the two means marked | counts sum to 146; colours match the verified split |
| `degree-def.png` | col | one node with four edges, the edges counted 1–4 | count = drawn degree |
| `sum-ends.png` | full | the Feld graph with a small tick at **each end** of every edge, 20 ticks, and the running total | ticks = 2M = 20 |
| `mean-degree.png` | col | the division 20 ÷ 8 = 2.5 set as a diagram, not a formula panel | value from `moments()` |
| `odd-three-attempt.png` | full | three ringed nodes labelled "odd" and a half-drawn edge that cannot find a partner — an *attempt*, not a proof | shows no resolution (question slide) |
| `handshake.png` | full | odd-degree nodes pairing up: four odd nodes joined by dashed accent-2 arcs, one left over crossed out | pairing is exhaustive; the leftover is unmatched |
| `pk-def.png` | col | p(k) as "how many of the eight sit at each k", drawn as columns of discs | — |
| `feld-pk.png` | full | four columns of two discs each, k = 1, 2, 3, 4, annotated "a quarter each" | column heights = the computed p(k) |
| `rosters.png` | full | eight friend lists side by side; every occurrence of Sue and Alice accent-2; a count strip beneath reading 4, 4, … 1, 1 | occurrence counts = degrees |
| `bag-of-hands.png` | full | a bag holding 20 hands, each hand tagged with its owner; Sue's four and Betty's one visible | hands = 2M = 20 |
| `qk-formula.png` | full | q(k) = k·p(k)/⟨k⟩ built as a picture: k hands out of 2M | — |
| `derivation-1.png` `derivation-2.png` `derivation-3.png` | full | **one figure in three states.** Same box, same left margin, one line added each time. (1) mean friend degree = Σ k q(k) = ⟨k²⟩/⟨k⟩ (2) + the variance substitution (3) + the theorem, boxed | states 1 and 2 are pixel-identical to state 3 above the added line |
| `gap-nonneg.png` | col | a number line with the gap Var/⟨k⟩ ≥ 0 marked, equality at "everyone the same" | — |
| `feld-check.png` | full | the four numbers landing: ⟨k²⟩ = 7.5, Var = 1.25, gap = 0.5, 2.5 + 0.5 = 3.0, against the hand count 60/20 | every number from `moments()` |
| `two-averages.png` | full | two sampling procedures side by side — **pick an edge end** (→ 3.0) and **pick a person** (→ 2.99) — each drawn as its own draw from the graph | both values computed |
| `worksheet-star-ring.png` | full | a 4-node star and a 6-node ring, no numbers filled in | **no gap value anywhere** |
| `worksheet-answer.png` | full | the same two graphs with Var/⟨k⟩ = 0.5 and 0 | values from `moments()` |
| `coauthor-gap.png` | full | cond-mat: ⟨k⟩ = 8.1 against friends' 22.1, with 82.8% marked | all three from `net_stats()` / `paradox_share()` |
| `fb-twitter.png` | full | Facebook 92.7% (mean) and 83.6% (median) and Twitter >98%, as annotated proportion strips — **not bars, not a table** | percentages hard-checked against the quoted sentences |
| `sampling-bias.png` | full | the same network sampled two ways: nodes at random (flat) and edges followed (hub-heavy) | the hub is over-picked by the computed factor |
| `acquaintance.png` | full | three steps: pick a person at random → ask for one friend → immunise the friend | — |
| `immunization-curves.png` | full | giant component against fraction immunised, three curves (random / acquaintance / degree-targeted) on the Internet AS graph, with f = 0.10 marked: 0.877, 0.024, 0.002 | curves from `immunization_curves()` |
| `demo-still.png` | col | a still pointing at `vaccination-game.html` | — |

## Batch B — `figs_tail.py` (Parts 5–6, 20 figures + 1 GIF)

All degree data comes from `condmat()`; nothing is re-derived.

| file | container | contents | asserted |
|---|---|---|---|
| `linear-axes.png` | full | p(k) against k on linear axes, k from 0 to 279 — everything in the first few columns | max drawn k = 279; ≥ 78% of mass in k ≤ 10 |
| `fat-tail-reveal.png` | full | the same axes with the tail region ringed accent-3 and "28 authors out of 23 133 live past k = 100" | counts computed |
| `loglog.png` | full | same data, both axes log; decade ticks | same point count as `linear-axes` |
| `loglog-line.png` | full | `loglog` plus the fitted line over 10 ≤ k ≤ 200 | slope = −2.571 from `ccdf_fit`-equivalent on the PDF; R² printed |
| `powerlaw-def.png` | col | p(k) ~ k^−γ with γ named as "how fast hubs get rare" | — |
| `binning.png` | full | three bin widths over the same tail, side by side as a build | the three tails genuinely differ |
| `ccdf-def.png` | col | CCDF(k) = share of nodes above k, drawn as a cut through the sorted degrees | — |
| `ccdf-condmat.png` | full | the cond-mat CCDF, every point a real degree | point count = number of distinct degrees |
| `cdf-vs-ccdf.png` | full | the same data as CDF and as CCDF, the CDF flattening into a wall | — |
| `slope-derivation.png` | full | ∫ from k to ∞ of k^−γ → k^−(γ−1) → slope 1 − γ, as a three-line build in one figure | — |
| `slope-worksheet.png` | full | a CCDF with a −1.3 slope triangle drawn on it and a blank for γ | **no γ value anywhere** |
| `slope-answer.png` | full | the same figure with γ = 2.3 filled in, and 1.3 crossed out | 2.3 = 1 − (−1.3) |
| `exercise-card.png` | col | a card pointing at the *Data Visualization* paper exercise | — |
| `hubs-share.png` | full | the Internet AS degree ranking: the top 1% (65 nodes) holding 33.8% of all connections | from `top_share()` |
| `universality.png` | full | three CCDFs on one panel — cond-mat, Internet AS, yeast proteins — each labelled in place, **no legend** | three curves, each from its own loader |
| `poisson-ccdf.png` | full | an ER graph's CCDF: a cliff, not a line | Var/⟨k⟩ ≈ 1 asserted |
| `three-ccdfs.png` | full | power law, Poisson and regular lattice on one CCDF panel | the lattice is a single vertical drop |
| `ba-growth.png` | full | three frames of growth: a node arrives with m = 2 edges, twice | — |
| `ba-growth.gif` | full | preferential attachment growing a hub, ~40 frames, **settling on the exact frame `quiz.png` uses for its preferential panel** | last frame identical to the still |
| `quiz.png` | full | two networks, same n, same ⟨k⟩ = 4, plus their two CCDFs — **unlabelled** | **no answer anywhere**; the two are the BA and uniform-growth graphs |
| `quiz-answer.png` | full | the same two, labelled, with max degree 315 against 29 | both from the generated graphs |

## Batch C — `figs_edge.py` (Parts 7–8, 9 figures)

| file | container | contents | asserted |
|---|---|---|---|
| `individual-vs-average.png` | full | the eight girls sorted by "below / above / equal", with Facebook's 92.7% (mean) and 83.6% (median) beside them | the 5/2/1 split recomputed |
| `vanishing-blank.png` | full | an empty frame inviting the room to build a paradox-free network, plus a pointer to `friendship-paradox-game.html` | **no answer** |
| `vanishing.png` | full | the ring, the complete graph and the lattice, each annotated Var(k) = 0 | all three variances computed as 0 |
| `directed.png` | full | a small directed network with in- and out-degree separated; the "you watch / they are watched" asymmetry marked | in-degree sum = out-degree sum = M |
| `assortativity.png` | full | three schematics — assortative, disassortative, neutral — same degree sequence, different wiring | the three share one degree sequence (asserted) |
| `assortativity-real.png` | full | four measured r values on one axis: Facebook +0.226, cond-mat +0.134, Internet −0.182, yeast −0.210 | three of the four computed here; Facebook quoted |
| `lognormal-trap.png` | full | two CCDFs over each other — a true power law and a log-normal — visually indistinguishable, R² printed | R² > 0.98 for the log-normal fit |
| `scale-free-debate.png` | full | a timeline: 1999 Barabási & Albert · 2011 Facebook reports "substantial curvature" · 2019 Broido & Clauset | — |
| `consequences.png` | full | one distribution feeding three earlier results: robustness (M03), distance (M02), spreading | — |
| `recap.png` | full | the four acts on one page | — |
| `m05-teaser.png` | full | a network with two visible clumps, unlabelled | — |

## Order of work

1. `figlib.py` — done.
2. `verify_numbers.py` — done; every batch imports from it.
3. Three batches in parallel; each must run standalone
   (`python3 figures/make_figures.py <name-fragment>`).
4. `make_animations.py` for the GIF, importing geometry **from** `figs_tail.py` so the
   still and the animation cannot drift.
5. `python3 figures/make_figures.py` green, then render, then `check_render.py` exit 0.

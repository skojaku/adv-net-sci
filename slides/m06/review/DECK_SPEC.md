# m06 deck spec, v4 (2026-10-14)

v4 brings the v3 deck (R5, 130 slides) to the slide skill as updated on 2026-10-14
(HOUSE_STYLE sections 8 to 10, read from the lecturer's CompleNet 2026 talk). The figures,
the numbers, the questions and the speaker notes are v3's; what changed is how each slide is
laid out and how much text it carries.

- **Theme:** `theme: house` (`theme.css` = the skill's `house/theme-house.css` + an m06
  appendix). Titles in Meslo bold, centred; Libre Baskerville only for the Aesop quotation.
- **Layouts:** every slide takes one (section 8). The v3 base layout (bullets left, figure
  right) is kept only where two or three terms are defined beside one figure.
- **Text:** the title is the message. One line under it (`.sub`: the formula, or a question's
  rule) and one at the bottom (`.take`: the answer, the result); no bullets elsewhere. What
  the bullets said and the slide no longer shows went into the speaker notes.
- **Breadcrumbs** name the measure of each run (`header:`), and "New York State highways" on
  each map.
- **Part openers** are each part's question, with the measures it covers under it.
- **The last slide** returns to the opening picture (Rome) as a question; the Module 6 lab
  answers it, so the slide does not.
- **The figure does not move** through a question and its answer, or a build: the appendix of
  `theme.css` gives the figure a box of fixed height in L-a and L-b. Checked by measuring every
  `<img>` box in headless Chrome: 0 changes between consecutive slides on one canvas.

131 slides. Day 1 (10/20): 1-61, shortest paths. Day 2 (10/22): 62-131, walks. About a third
are build steps.

## The spine (the part openers and the questions that carry the story)

1. All Roads Lead to Rome … do they? (title)
2. Which city is the most important? (on the Roman network)
3. Two choices make a centrality. (the empty grid)
4. Part One: Who is close to everyone?
5. Part Two: Which node can the traffic not avoid?
6. Part Three: Do your neighbours make you important?
7. Part Four: What if every node gets a baseline?
8. Part Five: What if a link runs one way?
9. Two choices, every centrality. (the full grid)
10. Do all roads lead to Rome? (the opening picture, back)

## The arc of each part (lecture shape: HOUSE_STYLE section 1)

Each measure: the definition (a build on a small graph, formula in the `.sub`) → one or two
one-graph questions (Q, then A = Q + the answer as `.take`) → the same measure on the New
York map. Each day closes on its row of the grid.

## Motifs (one picture per concept, back each time the concept is; rendered slide numbers)

| concept | picture | where it returns |
|---|---|---|
| the module's question | the Roman network (`roma-*`) | 3-5, 131 |
| the real network | the New York map (one canvas, `figs_ny`) | 6, 7, 38, 48, 60, 95, 128 |
| the two choices | the grid (`grid-*`) | 14, 61, 112, 129 |
| shortest paths | the bowtie (closeness, eccentricity, betweenness builds) | 16-21, 39-43, 50-54 |
| a closed road | the CA graph with the hot × | 24-35 |
| eigenvectors | circle = eigenvalue, bar = eigenvector, coloured by index | 76-85, 104-107 |
| hot / cool | hot: the winner and the point; cool: high values, Authority | throughout |

## Slides (logical slides, 83; a build is one row, so these numbers are not the rendered ones)

| # | beat | layout | title | text |
|---|---|---|---|---|
| 1 | title | lead | All Roads Lead to Rome | … do they? |
| 2 | hook | E | The Golden Milestone | three sentences beside three photographs |
| 3 | hook | A | Twelve cities of the empire | sub: roads and sea lanes |
| 4 | question | A | Which city is the most important? | sub: node, edge; cue |
| 5 | first answer | A | Degree: the roads at a city | sub $d_i$; take: only the neighbours |
| 6 | question held | B | Which city do most trips pass through? | cue: hold it until the end of today |
| 7 | evidence | B | Degree cannot tell interchanges apart | take: 201 / 57 |
| 8 | question | left | How far is u from v? | cue |
| 9 | two terms (build, 4) | left | Two ways to count | shortest path, walk |
| 10 | thesis | B | Two choices make a centrality | |
| 11 | part | part | Who is close to everyone? | |
| 12 | definition (build, 5) | A | Closeness: invert the sum of distances | sub: formula |
| 13-16 | Q A Q A | A | Which node is closest to everything? | sub: the rule; take: the winner |
| 17-18 | Q A (mystery) | A | What if one road closes? | take: every closeness is 0 |
| 19 | definition (build, 5) | A | Harmonic centrality adds 1/distance | sub: formula; take: $1/\infty = 0$ |
| 20-23 | Q A Q A | A | Who has the highest harmonic centrality? | |
| 24 | result | B | Closeness picks a spot near NYC | take: 31% within 60 km |
| 25 | question (turn) | A | A fire station at the best average? | sub: D, 0.60 |
| 26 | definition (build, 3) | A | Eccentricity: the farthest distance | sub: formula |
| 27-30 | Q A Q A | A | Smallest eccentricity: which node? | |
| 31 | result | B | Smallest worst case: near Binghamton | take: 473 km |
| 32 | part | part | Which node can the traffic not avoid? | |
| 33 | mechanism (build, 4) | A | Count the letters each node carries | sub: one letter per pair |
| 34 | three symbols | left | Betweenness: a tie splits the pair | formula, sigma_st, sigma_st(i) |
| 35-38 | Q A Q A | A | Which node carries the most? | |
| 39 | answer to slide 6 | B | Which city do most trips pass through? | take: Binghamton |
| 40 | close of day 1 | B | The shortest-path row | |
| 41 | part | part | Do your neighbours make you important? | |
| 42 | pivot | Q | (Aesop) | the company he keeps |
| 43 | mechanism (build, 3) | A | Importance you inherit | sub: formula |
| 44 | definition | A | It is an eigenvector equation | sub: $Ac = \lambda c$ |
| 45-46 | Q A | A | Which eigenvector is the centrality? | take: all positive |
| 47 | definition | A | This is eigenvector centrality | |
| 48-51 | Q A Q A | A | Which lettered node scores higher? | |
| 52-55 | derivation (two builds) | A | A is a sum of rank-1 pieces / orthogonal / Square it / Keep multiplying | sub: one line each |
| 56 | demo | stage | Multiply by A, again and again | live stage |
| 57 | test (build, 1) | B | Start anywhere: the same scores | take: flip the sign |
| 58 | question (mystery) | A | Where does eigenvector centrality break? | |
| 59 | answer (build, 4) | A | Localization: one clique takes it | |
| 60 | result | B | 96% of the score lies near NYC | take: 31% of the nodes |
| 61 | part | part | What if every node gets a baseline? | |
| 62-63 | definition, question | A | Katz: a baseline plus the neighbours / What is that inverse? | |
| 64 | answer (build, 3) | A | The same series for matrices | take: walks, discounted |
| 65 | demo | stage | Turn the dial | live stage |
| 66 | derivation (build, 3) | A | Why does α stop at 1/λmax? | sub: the spectral sum |
| 67-70 | Q A Q A | A | Which lettered node scores higher now? | |
| 71 | close of the walks | B | The walk row | |
| 72 | part | part | What if a link runs one way? | |
| 73 | two terms | left | Hubs and authorities | |
| 74 | history | A | The same idea, six times | |
| 75-76 | Q, A (build, 4) | A | Which ranks higher, C or E? | take: they tie at 3/11 |
| 77 | mystery (build, 3) | A | A dead end: the total goes to 0 | |
| 78 | answer | A | Teleportation gives PageRank | take: formula |
| 79 | variant | A | Personalized PageRank | |
| 80 | result | B | Five measures, five different winners | |
| 81 | summary | B | Two choices, every centrality | |
| 82 | homework | F | Draw a network where four measures disagree | |
| 83 | the end | A | Do all roads lead to Rome? | take: rank the twelve cities |

## Figure groups (one drawing, one crop)

A group's figures use the same canvas, the same node coordinates and the same crop
(`figlib.emit_group`, or `box=` for figures built in different functions). A build's frame 0
is pixel-identical to the slide before it, and consecutive slides of one group share a layout.

- **Rome** (figs_intro, figs_rome, romelib): roma-basemap → roma-to-graph → roma-degree.
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
- **PR** (figs_dir): pr-split, pr-split-answer frames, pr-leak frames, pr-teleport, ppr.

The v3 slide table and its round notes are in git history (this file before 2026-10-14).

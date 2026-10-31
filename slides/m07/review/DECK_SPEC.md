# DECK_SPEC: M07 Random Walks, the maths half (wireframe v1)

Stage 1 of 3: wireframe. Stage 2: real figures (one `smallgraphs.py` for every graph and number, `check()` asserting them).
Stage 3: polish. 48 slides, of which 9 are build steps and about 4 are optional or cut candidates.
Style: house (`theme.css` = `house/theme-house.css`). Layouts per HOUSE_STYLE section 8.

## Spine (the F slides, read alone)

1. A walker with no map takes random steps. What does it learn about the network?
2. Short walks see rooms. Long walks see degree. When does one turn into the other?
3. Pen & Paper, Part 1: measure it
4. Why does the walker forget where it started?
5. One eigenvalue is always 1. None is larger.
6. Pen & Paper, Parts 2 and 3: expand it
7. Next: how long does the walker take to get there?

## Time plan (about 90 minutes, Pen & Paper included)

| part | slides | count | minutes |
|---|---|---|---|
| A  Intuition: what a blind walker learns (live tool, then Pen & Paper Part 1) | 1-14 | 14 | 26 |
| B  Maths: why the walker forgets (matrices, circles, mixing time, eigenvalue 1) | 15-41 | 27 | 36 |
| C  Pen & Paper Parts 2-3, then debrief | 42-48 | 7 | 30 |

Total 92 minutes. Over budget by about 2 minutes at 1 minute per content slide: the builds take seconds, the three
Pen & Paper blocks are fixed. Cut candidates in order: the optional bound slide, the answer to Q2 (two rooms), the Q4 / A4 clique pair.

## Motifs (one picture per concept, back each time the concept is)

| concept | picture | colour | where it returns |
|---|---|---|---|
| the walker's rule | 7-node network, ring on the walker, 1/k labels | ink | slide 3, 47 |
| the real network | karate club in the live tool | tool's own | 4-6, 14, 48 |
| the two-room network (12 nodes) | two blocks, bridges 2-8 and 5-11 | room 1 cool, room 2 hot | 16-20, 23-27, 45-46 |
| eigenvalue, eigenvector | circle, tall bar, wide bar (M06) | u1 blue, u2 gold, rest pale | 21-27, 36, 39-41 |
| pi = degree / 2m | wide bar of shares, orange ticks of the tool | hot | 14, 41, 47 |

## Slide list

| # | layout | title | beat | figure |
|---|---|---|---|---|
| 1 | lead | Random Walks: What Does a Blind Walker Learn? | title |  |
| 2 | L-f | A walker with no map takes random steps. What does it learn about the network? | spine 1: the question |  |
| 3 | L-b | One step: pick a neighbour at random | mechanism: the rule | Small 7-node network, hand-drawn. A walker (ring) stands on a node with 4 neighbours. Each of the 4 edges is labelled 1/4 (an amount, not a  |
| 4 | L-g | (no title) | live: the simulator (karate club) | LIVE: random walk simulator, karate club, exactly as used last term (assets/vis/random-walks/index.html, no edits). The lecturer clicks Walk |
| 5 | L-c | Short walk vs long walk | question to the room (Q1) |  |
| 6 | L-b | Short: neighbourhood. Long: degree. | answer to Q1 | LEFT: the tool after 20 steps, nodes shaded by visits: dark nodes cluster around the start node. RIGHT: after 5,000 steps: dark nodes are th |
| 7 | L-g | (no title) | live: the simulator (two rooms) | LIVE: same tool, ?dataFile=two-cliques.json: two 5-cliques joined by a single edge. |
| 8 | L-c | Two rooms, one door | question to the room (Q2) |  |
| 9 | L-b | A short walk stays in its room | answer to Q2 | Same network. The walker's path drawn as a brush stroke, coloured by room (room 1 cool, room 2 hot); a time strip under it shows long runs o |
| 10 | L-f | Short walks see rooms. Long walks see degree. When does one turn into the other? | spine 2: the mystery |  |
| 11 | L-f | Pen & Paper, Part 1: measure it | Pen & Paper Part 1: opener | QR code (large) to the simulator, plus the short link |
| 12 | L-c | Part 1: three things to do | Pen & Paper Part 1: instructions |  |
| 13 | L-b | Correlation climbs, then flattens | debrief Q1 (the sketch) | Line plot. x: steps (log scale, 10 to 20,000). y: correlation between visit share and degree. Dots at 0.37, 0.53, 0.76, 0.89, 0.96, 0.99, 1. |
| 14 | L-a | Degree ÷ share is one number | debrief Q2 (degree ÷ share) | Scatter: x = degree, y = share of visits after 20,000 steps, 34 dots on a straight line through the origin. Node 33 (degree 17, share 0.109) |
| 15 | L-f | Why does the walker forget where it started? | spine 3: part question |  |
| 16 | L-b | The whole walk is one matrix | P (the 'two rooms' network, the motif of the rest of the lecture) | LEFT (small): the 12-node 'two rooms' network (nodes 0-5 and 6-11, two bridge edges 2-8 and 5-11). RIGHT: its transition matrix P as a heat  |
| 17 | L-a | One step is one multiplication | x P | Matrix picture in the M06 style: a wide bar (distribution x(t), 12 cells, shaded) times the square P = a wide bar (x(t+1)). Small network be |
| 18 | L-b | Rows of $P^t$ after t steps | P^t as heat maps (1/3) | Heat map of P^1 (12 x 12), same crop and position as the previous step: two dense diagonal blocks. Callout: 't = 1: stays in its room' |
| 19 | L-b | Rows of $P^t$ after t steps | P^t as heat maps (2/3) | Heat map of P^5 (12 x 12), same crop and position as the previous step: the blocks blur. Callout: 't = 5: starting to leak' |
| 20 | L-b | Rows of $P^t$ after t steps | P^t as heat maps (3/3) | Heat map of P^40 (12 x 12), same crop and position as the previous step: every row identical. Callout: 't = 40: all rows = pi' |
| 21 | L-b | Recall: a matrix = circles and bars | recap: eigendecomposition (M06, light touch) | (m06 figure reused) |
| 22 | L-a | $P$ is a sum of circles and bars too | P as a sum of circles and bars | Same pictorial grammar as M06: circle (eigenvalue, size = |lambda|), tall bar phi_k (right eigenvector), wide bar psi_k^T (left eigenvector) |
| 23 | L-b | Each step shrinks the circles | P^t as circles (1/3) | P^1 drawn as a sum of the same terms (same canvas as the previous step); circle areas = lambda^1: circles at 1, 0.89, 0, 0, 0, -0.09, -0.2,  |
| 24 | L-b | Each step shrinks the circles | P^t as circles (2/3) | P^5 drawn as a sum of the same terms (same canvas as the previous step); circle areas = lambda^5: circle 2 at 0.55, the rest almost gone. Fi |
| 25 | L-b | Each step shrinks the circles | P^t as circles (3/3) | P^40 drawn as a sum of the same terms (same canvas as the previous step); circle areas = lambda^40: circle 2 at 0.01; circle 1 untouched. Fi |
| 26 | L-c | Which circle dies last? | Q3 (which circle dies last) |  |
| 27 | L-c | The second circle dies last | A3 |  |
| 28 | L-b | Forgetting is a distance that shrinks | distance to pi (small multiples) | Five small bar charts in a row: the walker's distribution x(t) on the 12 nodes for t = 0, 1, 3, 10, 40, starting at node 0. A flat reference |
| 29 | L-a | Mixing time: every start forgotten | mixing time diagram (1/3) | Curves: distance to pi against t, one thin grey line per starting node (12), and a black line for the worst start. Callout: 'where you start |
| 30 | L-a | Mixing time: every start forgotten | mixing time diagram (2/3) | Same plot plus a horizontal line at epsilon. Callout: 'how close is close enough?' |
| 31 | L-a | Mixing time: every start forgotten | mixing time diagram (3/3) | Same plot; the point where the worst-start line crosses epsilon marked hot, with a vertical line down to the axis labelled 'mixing time'. |
| 32 | L-a | Q: how long to forget on a 10-clique? | Q4 (clique) | A 10-clique, hand-drawn, nodes in a ring; the walker on node 0 |
| 33 | L-a | A: one step is almost enough | A4 | Same clique, same position. Distance-to-pi curve as an inset: below epsilon at t = 1 |
| 34 | L-a | Q: and with a single bridge? | Q5 (two cliques) | The two-clique network (the tool's two-cliques.json), the walker in room 1 |
| 35 | L-a | A: fifteen times slower | A5 | Same network. Inset: distance-to-pi curve with the clique's curve in pale for comparison |
| 36 | L-a | The slowest circle sets the clock | spectral gap (gauge) | A horizontal gauge for lambda_2 from -0.2 to 1 with markers: 10-clique (-0.11, tau 0.9), karate club (0.87, tau 7.6), two rooms (0.89, tau 9 |
| 37 | L-b | Mixing time is a few relaxation times | (optional) the bound | The formula t_mix < tau log(1/(epsilon pi_min)) on the left; on the right the 12-node distance curve with tau marked and 2 tau, 3 tau as tic |
| 38 | L-f | One eigenvalue is always 1. None is larger. | spine 4: the fact |  |
| 39 | L-b | Why 1? Every row of $P$ sums to 1 | lambda = 1 exists (P 1 = 1) | Picture: the square P times a tall bar of all ones (cells '1') = the same tall bar. One row of P highlighted; its cells sum to the first cel |
| 40 | L-b | Why not more? An average can't grow | no eigenvalue above 1 | Two frames on a 7-node network: numbers on the nodes (largest = 9); one step replaces every number by the average of its neighbours; the lar |
| 41 | L-a | The circle at 1 is π | lambda = 1 is pi (ties to the tool) | The first term alone: a tall bar of ones times a wide bar pi = a matrix whose every row is pi (the last heat map of the previous build, at t |
| 42 | L-f | Pen & Paper, Parts 2 and 3: expand it | Pen & Paper Parts 2-3: opener |  |
| 43 | L-c | Parts 2 and 3: two things to do | Pen & Paper Parts 2-3: instructions |  |
| 44 | L-a | $x(t)$ = π + shrinking pieces | debrief Part 2 | The 4-node diamond network (degrees 2, 2, 3, 3) on the left. Right: bar charts of x(t) for t = 0, 1, 2, 5, 10 converging to pi = (0.2, 0.2,  |
| 45 | L-b | The second eigenvector splits the rooms | debrief Part 3 (second eigenvector) | Point plot: x = node index 0 to 11, y = second eigenvector of P (scaled to max 1). Nodes 0-5 on top (about +1; the bridge nodes 2 and 5 at a |
| 46 | L-a | Early on, the community is what is left | debrief Part 3 (what dominates early) | Line plot: x = steps (0 to 40), y = probability of being in room 1: 1.00, 1.00, 0.92, 0.88, 0.80 (t = 5), 0.67 (t = 10), 0.55 (t = 20), 0.50 |
| 47 | L-g | (no title) | summary (claims with thumbnails) | Summary, three rows, each with a thumbnail of its figure: (1) the circle at 1 = degree (thumb: scatter, slide 14). (2) The second circle = t |
| 48 | L-f | Next: how long does the walker take to get there? | close: back to the opening picture, then a question for next time | The opening picture again: the karate club, nodes shaded by long-run visits, with two nodes marked A and B |

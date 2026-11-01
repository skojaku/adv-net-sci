# DECK_SPEC: M07 Random Walks, the maths half (v2, after the red-pen round)

46 slides, 9 of them build steps, 3 optional (the answer to Q2, the 10-clique pair). Style: house (`theme.css` = `house/theme-house.css`).
Figures: `figures/BRIEF.md` (who draws what); numbers: `figures/smallgraphs.py`. The P^t slider uses `scrub.js` (frames in `figures/frames/Pt-slider/`).

## Spine (the F slides, read alone)

1. How does it tell us about a network?
2. Pen & Paper
3. Short walks show communities. Long walks show degree. Why?
4. Why does a long walk not depend on the start?
5. One eigenvalue is always 1. Others diminish.
6. Pen & Paper

## Time plan (about 90 minutes, Pen & Paper included)

| part | slides | count | minutes |
|---|---|---|---|
| A  Intuition: Pearson's walker, then what a blind walker learns (Pen & Paper first) | 1-12 | 12 | 30 |
| B  Maths: why the start stops mattering (matrices, circles, mixing time, eigenvalue 1) | 13-42 | 30 | 38 |
| C  Pen & Paper, then debrief | 43-46 | 4 | 20 |

Total 88 minutes. The Pen & Paper blocks (10 and 10 minutes) are fixed; the builds take seconds.

## Slide list

| # | layout | title | beat | figures |
|---|---|---|---|---|
| 1 | lead | Random Walks | title |  |
| 2 | L-c | Where is the walker after 100 steps? | hook (story): Pearson's question, 1905 | pearson-walker |
| 3 | L-g | (no title) | story: Polya's recurrence (2D returns, 3D does not) | polya |
| 4 | L-b | Random walks appear in many fields | hook: the same walk in three fields | fields |
| 5 | L-f | How does it tell us about a network? | spine 1: the question |  |
| 6 | L-b | What is a random walk? | mechanism: the rule | walk-rule |
| 7 | L-f | Pen & Paper | Pen & Paper: first block |  |
| 8 | L-c | (no title) | the simulator (QR code and link) | qr-sim |
| 9 | L-c | Two communities joined by one edge | question to the room (Q2) | two-comm-q |
| 10 | L-b | A short walk stays in its community | answer to Q2 | two-comm-walk |
| 11 | L-f | Short walks show communities. Long walks show degree. Why? | spine 2: the mystery |  |
| 12 | L-a | Degree ÷ share is constant | debrief Part 1 (degree ÷ share) | degree-share |
| 13 | L-f | Why does a long walk not depend on the start? | spine 3: part question |  |
| 14 | L-b | The walk is defined by one matrix | P (the two-community network, the motif of the rest of the lecture) | P-def |
| 15 | L-b | One step is a multiplication by $P$ | x P, how to read it (1/3) | xP-1 |
| 16 | L-b | One step is a multiplication by $P$ | x P, how to read it (2/3) | xP-2 |
| 17 | L-b | One step is a multiplication by $P$ | x P, how to read it (3/3) | xP-3 |
| 18 | L-a | After $t$ steps | x(0) P^t | xPt |
| 19 | L-b | Rows of $P^t$ after t steps | P^t as a heat map (slider) | Pt-slider |
| 20 | L-b | Rows of $P^t$ at $t = 40$ | P^t, the numbers at t = 40 | Pt-40 |
| 21 | L-b | What each entry of $P^t$ says | zoom into P^t | Pt-zoom |
| 22 | L-b | Recall: eigendecomposition | recap: eigendecomposition (M06, light touch) | m06-decomp-sum |
| 23 | L-a | $P$ has an eigendecomposition too | P as a sum of circles and bars | P-decomp |
| 24 | L-b | The eigenvalues shrink as $t$ grows | P^t as circles (1/3) | Pt-circles-1 |
| 25 | L-b | The eigenvalues shrink as $t$ grows | P^t as circles (2/3) | Pt-circles-2 |
| 26 | L-b | The eigenvalues shrink as $t$ grows | P^t as circles (3/3) | Pt-circles-3 |
| 27 | L-c | Which term stays the longest? | Q3 (which term stays the longest) | lam-curves-q |
| 28 | L-c | The second term stays the longest | A3 | lam-curves-a |
| 29 | L-a | Mixing time | mixing time (1/3) | mix-1 |
| 30 | L-a | Mixing time | mixing time (2/3) | mix-2 |
| 31 | L-a | Mixing time | mixing time (3/3) | mix-3 |
| 32 | L-a | Q: mixing time of a 10-clique? | Q4 (clique) | clique-q |
| 33 | L-a | A: about 1 step | A4 | clique-a |
| 34 | L-a | Q: mixing time with one bridge? | Q5 (two cliques) | twoclique-q |
| 35 | L-a | A: about 10 times longer | A5 | twoclique-a |
| 36 | L-a | The relaxation time | relaxation time | relax-curve |
| 37 | L-a | Small gap, long relaxation time | spectral gap (gauge) | gap-gauge |
| 38 | L-a | Mixing time is a few $\tau$ | mixing time versus relaxation time | tau-vs-mix |
| 39 | L-f | One eigenvalue is always 1. Others diminish. | spine 4: the fact |  |
| 40 | L-b | Why 1? Every row of $P$ sums to 1 | lambda = 1 exists (P 1 = 1) | P1-eq-1 |
| 41 | L-a | No eigenvalue is larger than 1 | no eigenvalue above 1 | no-larger |
| 42 | L-a | Detailed balance condition | the eigenvalue 1 gives pi (ties to the simulator's ticks) | detailed-balance |
| 43 | L-f | Pen & Paper | Pen & Paper: second block |  |
| 44 | L-b | $x(t) = \pi\,+$ decaying terms | debrief Part 3 (second eigenvector; the expansion) | eigvec2 |
| 45 | L-a | Early on, the community signal dominates | debrief Part 3 (what dominates early) | comm-curve |
| 46 | L-g | (no title) | summary (claims with thumbnails) | summary |

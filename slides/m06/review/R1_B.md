# R1 review, reviewer B: slides 25–47

Deck `slides/m06/m06-centrality.md`, renders `review/slide.025.png` … `slide.047.png`, stage
screenshots `stage-power-t4.png`, `stage-power-t30.png`. Every PNG in range opened; every GIF in
range (btw-def, eigen-inherit, decomp-sum, decomp-square, decomp-power) read frame by frame
(frames saved under `scratchpad/review_frames/B_*`). Numbers checked against
`python3 figures/smallgraphs.py` (all assertions pass) and `figures/data/ny_network.json`.
`check_render.py` exit=0 (it does not measure the HTML stage on slide 47).

Note on numbering: the deck has 70 slides; DECK_SPEC numbers are one lower from slide 37 on
(the Aesop slide was split from the part divider). Numbers below are the deck's.

**Count:** 1 Blocker · 14 Major · 20 Minor

## Findings

slide 26 — Minor — The gray tag "closeness" beside E and K reads as a property or value of that node, not as "this node wins closeness". — Change the tag text to "best closeness" on both graphs (`quiz-ecc-answer`).

slide 27 — Blocker (F1) — Dot shade and dot size encode 1/eccentricity (`figs_ny.py`: "darker = more central … the figcaption must say so"), and nothing on the slide says so. Eccentricity is the measure where smaller is better, so the natural reading of the map (dark = long drive) is the inverse of the truth. — Add `<figcaption>darker and larger: a shorter worst-case drive</figcaption>` under the map.

slide 27 — Minor — Bullet 1 is a fragment that names neither the unit nor what the map shows; bullet 2 can be exact. — Bullets: "* Each interchange's worst-case drive, in km of highway." / "* Shortest: 473 km, on NY 17 at Deposit, 42 km east of Binghamton." (winner node 200: NY 17 / NY 8 / NY 10, `near_km` 41.6).

slide 29 — Minor — The text says to send a letter "between every pair", and the GIF's first frame says "a letter for every pair", but the GIF then shows only the 13 letters that pass through a third node; the 8 neighbour pairs (A–B, C–D, …) are skipped without a word. "Carries" is also ambiguous for the sender. — Slide line 2: "Count the letters each node passes on for others." GIF frame 1 text: "a letter for every pair; neighbours need no carrier".

slide 30 — Major — The in-figure label "each route earns 1, split where they tie" is wrong: a *pair* (s, t) contributes 1 in total, split across its σ_st shortest paths. The printed 1/2, 1/2, 1 are the shares of the single pair S, D, yet they sit on the nodes like b_A, b_B, b_T (the real values are b_A = 1, b_B = 1, b_T = 7/2, b_S = 1/2). — Replace the label (`figs_small.py` line 438) with "the pair S, D: two shortest paths, each gets half".

slide 30 — Major — σ_st and σ_st(i) are defined only in the speaker note; the lecturer requires named objects to be defined. — Add one line under the formula: "$\sigma_{st}$: the number of shortest paths from s to t; $\sigma_{st}(i)$: how many of them pass through i."

slide 30 — Major — Red is used as a group colour: one route is red, the other blue (the same blue as the node discs), and the T–D edge is drawn as red + black + blue stripes. The "1" over T touches T's disc. — Draw the two routes in accent blue and accent-3 gold (two stripes on T–D), print 1/2, 1/2 and 1 in black, and lift the "1" about 8 bp off T.

slide 31 — Minor — "Count the shortest paths through each node." disagrees with the formula on slide 30, which splits a tied pair (the right graph has the tied pair P, Q). — "Add up each node's share of the letters."

slide 33 — Major — The map's red winner is labelled "Monticello", but no bullet mentions it; the bullets are about Binghamton. Figure and text disagree about what the red mark is. — Bullets: "* Top interchange: NY 17 at Monticello." / "* Of the eight cities, Binghamton is first: 3.5 times Syracuse." / "* The four highest interchanges are all on NY 17." (data: Monticello 0.3632, NY 17 at Deposit 0.3626, NY 17/I-84 and NY 17/US 209 at Middletown 0.349; Binghamton/Syracuse = 3.498).

slide 33 — Major (F1) — Dot shade and size encode betweenness and nothing on the slide says so. — Add `<figcaption>darker and larger: more shortest paths pass through</figcaption>`. (Same gap on the NY maps at slides 8, 17 and 50, outside this range.)

slide 33 — Minor — "NY 17 joins New York City to the rest of the state" overclaims: I-87 interchanges also rank high (I-87/I-287 at White Plains is 5th, I-87 at Suffern 6th). — Replaced by the third bullet above.

slide 34 — Minor — "eccentricity: longest" does not say longest what. — "longest distance".

slide 34 — Minor — All four measure names are red, so red marks a category, not one emphasised thing; faint gray specks sit at the four corners of the figure's bounding box (RGB 210 at about (113,138), (1165,138), (113,480), (1165,480)). — Set the names in black (or accent blue) in `grid-row1` and the later grids; remove the corner marks in the generator.

slide 36 / 37 — Minor — The divider title "Known by the company you keep" and the next slide's quote "A man is known by the company he keeps" say the same thing back to back. — Divider title "Importance you inherit", sub "day 2: the routes become walks"; retitle slide 38 "A score made of scores".

slide 37 — Minor — The quote uses straight ASCII quotes. — “A man is known by the company he keeps.”

slide 38 — Major — "A node's score is the sum of its neighbours' scores" contradicts the formula, which divides by λ, and λ is not defined on the slide. — "A node's score is the sum of its neighbours' scores, divided by a constant λ."

slide 38 — Major — `eigen-inherit.gif`: in every arrow frame (1–8) all discs are the same blue and no number appears, so the animation shows which nodes are neighbours, not that scores add up. The final shading is not explained on the slide (F1). — Keep the final shading in every frame and print each node's score with the largest set to 1 (A 1.00, G 0.85, F 0.81, B 0.64, D 0.58, E 0.48, C 0.20). When the arrows into A have built up, show "0.64 + 0.58 + 0.81 + 0.85 = 2.88 × 1.00" by A; for B show "1.00 + 0.85 = 2.88 × 0.64" (checked: 2.8841 and 1.8495 = 2.884 × 0.6413). Figcaption: "shade: the score".

slide 38 — Minor — GIF frame 1 flashes all four arrows into A for 1.2 s, frame 2 clears them, and frames 3–6 rebuild the same picture one arrow at a time. It reads as a glitch. — Drop frame 1.

slide 39 — Minor — The in-figure line "λ = 2.88: the same seven numbers, each 2.88 times bigger" contradicts itself ("same" and "bigger"), and it names the eigenvalue one slide before slide 40 asks which eigenvector is the centrality. — "λ: multiplying by A only stretches c, by the factor λ". No numeric value.

slide 40 — Minor — The body repeats the title, and "A 7 × 7 matrix has seven eigenvectors" is not true of every 7 × 7 matrix. — Title "Which eigenvector?"; body "Our A has seven eigenvectors. Which one is the centrality?"

slide 41 / 42 — Major — The two adjacent slides state the same fact: 41 marks one copy "all positive" with the caption "only one is blue everywhere"; 42 says "the eigenvector of the largest eigenvalue is the only one with every entry positive". The lecturer wants Perron–Frobenius shown *with* the all-eigenvector figure. — Slide 41: title "Perron and Frobenius", caption "connected network: only the largest eigenvalue's eigenvector is positive everywhere; blue positive, gold negative, pale near 0". Slide 42: title "Eigenvector centrality", one line "Its entries are the scores.", figure `eig-pf` (rescaled as in the next finding).

slide 42 + 47 — Major — Slide 42 prints the eigenvector at unit length (A 0.54, G 0.46, …). The power-iteration stage converges to A 1.00, G 0.85, … (largest = 1), and its last note says only "converged: B (2 neighbours) ends above D (3 neighbours)". Nothing on screen tells the room that the stage landed on slide 42's vector; that is the "power iteration converges to the leading eigenvector" requirement. — Print slide 42's values with the largest set to 1 (A 1.00, G 0.85, F 0.81, B 0.64, D 0.58, E 0.48, C 0.20) and caption it "scaled so the largest is 1". Stage step-30 note: "converged: the eigenvector centrality; B (2 neighbours) ends above D (3)".

slide 42 — Minor — An eigenvector's sign is arbitrary, so "the only one with every entry positive" is not exact. — "… is the only one whose entries all have the same sign."

slides 42–47 — Major (lecturer requirement) — Eigenvector centrality never gets "a question with two example graphs, then the answer". The only question is B vs D, and it is in the stage's speaker note on one graph. — Insert a question slide before the stage: "Which scores higher?" Left: the 7-node graph, unshaded, B (2 neighbours) against D (3). Right: a hub H with five leaves, joined to one corner K1 of a 4-clique K1–K4; H (6 neighbours) against K2 (3). Answer slide after the stage: B 0.64 > D 0.58; K2 0.85 > H 0.62, with K1 top at 1.00 (largest = 1; computed with numpy, to be added to `smallgraphs.py`). Day 2 grows from 35 to 37 slides.

slide 43 (also 44, 45, 46) — Major (F3) — The tall and wide bars, which are the notation's eigenvector and its transpose, are filled #CDD5E9 on white (contrast about 1.4 : 1). From the back they look like an empty L-shaped frame. The lecturer's original (`spectral-decomposition.jpg`) draws them solid. — Fill u_k and u_kᵀ in solid accent blue in `figs_decomp.py`; keep the square's outline light gray. On slide 44 tell u_ℓ from u_k by solid accent blue against solid dark gray, not by two lightnesses of blue.

slide 43 — Minor — "rank-1" is not defined. **A** is bold on 43–46 but italic $A$ on 38, 39 and 47. — Text: "A symmetric matrix is a sum of rank-1 matrices, each a column times a row." Draw $A$ in italic in the decomposition figures.

slide 44 — Minor — "one with itself gives 1" holds only for eigenvectors scaled to length 1, which no slide states (and 42/47 use other scalings). "Multiply" is ambiguous (the outer product of two eigenvectors is not 0). — Caption: "a wide bar times a different tall bar gives 0; times its own tall bar, 1 (each eigenvector scaled to length 1)".

slide 45 — Major — The slide's one point, that squaring keeps the eigenvectors and squares each eigenvalue, is written nowhere. The final frame drops the λ_k labels slide 43 had, so the room must work out 2.88² to see 8.32, and (−2.26)² to see why the last circle turned blue. — Label the circles $\lambda_1^2$, $\lambda_2^2$, $\lambda_3^2$, $\lambda_7^2$ as slide 43 labels them, and add one line above the figure: "$A^2 = \sum_k \lambda_k^2\,\mathbf{u}_k\mathbf{u}_k^\top$: same eigenvectors, eigenvalues squared."

slide 45 — Minor (L6) — The figure hangs at the top and the bottom half of the slide is empty. — `<!-- _class: mid -->`.

slide 46 — Major — Two links are missing. (a) The walk axis: $A^t$ counts walks of length t (slide 10's note), but the word "walk" appears on no slide of Part Three (36–50). Its first use after slide 11 is slide 55 (Katz), so eigenvector centrality gets its place on the "which routes count" axis only at the grid. (b) The step from "the λ₁ term dominates $A^t$" to "power iteration converges to u₁" is not written; the next slide starts iterating without it. — Replace the text line with: "$A^t$ counts walks of length t. Divided by $\lambda_1^t$, every term but the first fades, so $A^t\mathbf{1}$ points along $\mathbf{u}_1$."

slide 46 — Minor — "Each term grows as λ_k^t" is wrong for |λ_k| < 1 (0.56^t shrinks) and ignores the sign flips of negative λ_k. — Covered by the replacement line above.

slide 46 — Minor — In every frame of `decomp-power.gif` the "+" after the third box overprints the box's right edge. — Move "+ ⋯ +" about 10 bp to the right.

slide 47 — Major (F3) — The node values, which are what the stage teaches, render with 13–14 px digit height (`.ps-val` 25px in the hand font). That is about two-thirds of the body text's 21 px cap height. "ranking" and "x ← A x, then divide by the largest entry" are similarly small. `check_render.py` does not measure HTML stages. — `.ps-val` font-size 36px (digits ≥ 21 px); `#power-step .anim-caption` 30px; re-check with a stage screenshot.

slide 47 — Minor — x is not defined on screen (the deck has used c and u_k so far). — Caption: "x: the numbers on the nodes. x ← A x, then divide by the largest."

slide 47 — Minor — The step notes are partly wrong or redundant. Step 5 "the order A G F B D E C is settled": the order has not changed since step 4. Step 7 "the wobble shrinks every step" is false (D moves 0.0043 from step 6 to 7, then 0.0051 from 7 to 8), and the speaker note repeats it ("each step moves it a little less"). — Step 5: "same order as step 4; only the values move". Step 7: "D back up to 0.59; every value now moves by less than 0.01". Step 8: "D down to 0.58; the order has held since step 4". In the speaker note, delete "each step moves it a little less".

## Checked and clean

- slide 25: the question gives nothing away, both graphs are tricky (hub E and hub K lose), and the fire-station line carries the motivation.
- slide 28: part divider.
- slide 32: values E 30, F 25, G 30, M 9, O 19/2 match `smallgraphs.py`; no label collisions.
- slide 35: closing question for day 1.

Lecturer requirements met in range: eccentricity has a formula and a fire station (23–26). Betweenness has the simple example, then formula, then two-graph question (29–32). Aesop picture (37). Eigenvector-equation figure kept (39). All seven eigenvectors with eigenvalues and values, exactly one all positive (41; checked against `spectrum`). Power iteration shown (47). Circle / tall bar / wide bar notation used (43–46). No em dashes or green in slides 25–47. Both days have 35 slides.

# R2 review, reviewer B: slides 36–70

Every PNG from 35 to 70 was opened. Every frame of every GIF in range was extracted and viewed
(`scratchpad/review_frames_r2b/`): eigen-inherit, decomp-sum, decomp-square, decomp-power,
ring-local, walks-discount, katz-why and pr-leak. The stage screenshots and `power-step.js` /
`katz-dial.js` were also read.

Numbers were checked in four ways:
- `python3 smallgraphs.py`: all assertions pass.
- Recomputed independently:
  - the power-iteration trace for steps 1–9 and 30, and every stage note against it;
  - the Katz-dial shares at k = 0, 50, 60, 90, 99 (33/40/43/63/81%) and its sign pattern past the pole;
  - PR_plain, PR_dead and PPR_A on the dead-end graph;
  - every coefficient in katz-why and decomp-power;
  - the λ² values.
- From `data/ny_network.json`: 96.4% of the eigenvector sum lies within 60 km of Manhattan, and
  91 of 289 interchanges (31%) do. The five winners match slide 68.
- `check_deck.py`: passes.

**Count:** Blockers 0 · Majors 1 · Minors 18

## Part 1: Round-1 items in range

Old slide numbers are R1's. Current numbers are in brackets.

### R1_B (old 36–47 → now 35–48)

- old 36/37 [35/36] divider title repeats the Aesop quote: **not fixed**. It was not in FIXES and was not rejected. Minor.
- old 37 [36] straight quotes: **not fixed**. Minor.
- old 38 [37] body contradicts the formula: **fixed**.
- old 38 [37] eigen-inherit (shading, numbers, sum): **fixed**.
  - Every frame carries the scores, and the A identity appears.
  - Residual Minor, see Part 2: the identity is on screen only briefly and is absent from the still, and the shade is unexplained.
- old 38 [37] first-frame flash: **fixed**.
- old 39 [38] "same … bigger" caption: **fixed**.
- old 40 [39] title/body wording: **fixed**.
- old 41/42 [40/41] Perron–Frobenius stated twice: **fixed**.
- old 42+47 [41/48] scale to largest = 1, and the converged note: **fixed**.
- old 42 [40] sign of the eigenvector: **not fixed**. Minor, merged into Part 2 (slide 40).
- old 42–47 [42–43] missing two-graph eigenvector question: **fixed-but-new-problem**.
  - The question is good: planar, letters only, no values, no note. The answer values are correct (M 0.85, X 0.46, K 0.85, H 0.62).
  - New problems: the figure jumps at the reveal, the title says "marked", and a label touches a ring (Part 2).
- old 43–46 [44–47] pale bars: **fixed**. Solid accent everywhere, including katz-why.
- old 43 [44] rank-1 and bold **A**: rank-1 is now explained in the note. Bold **A** in the figures against italic $A$ in the text: **not fixed**. Minor.
- old 44 [45] caption: **fixed**.
- old 45 [46] λ² labels and line: **fixed**. Values 8.32 / 1.74 / 0.31 / 5.10 are correct.
- old 45 [46] L6, top-heavy layout: **not fixed**. Minor.
- old 46 [47] walk link: **fixed**.
- old 46 [47] "grows as λ^t": **fixed**.
- old 46 [47] "+" overprint: **fixed**.
- old 47 [48] stage font: **fixed**. Digits are 16–17 px tall and the note line is 29 px, at the x-height floor.
- old 47 [48] x undefined: **fixed**.
- old 47 [48] wrong step notes: **fixed**. Every note matches a fresh trace; the order is fixed from step 4.

### R1_C (48–70)

- #1, old 48 repeat: **fixed** (cut; the step-1 note is in the stage).
- #2, #3 [49] question wording and plain fill: **fixed**.
- #4 localization percentages: **fixed**. 25/68/85/91/94% match `eig_share`; NY 96% and 31% are verified. The dial limit (85%) now agrees with slide 50.
- #5 [50]: timing **fixed** (1.8 s per frame, 2.4 s on the last). "last clique" vs "growing clique", the undefined K and the unstated shade: **not fixed**. Minor.
- #6 [51]: circle and inset **fixed**. "60 km" still breaks across lines: **not fixed** (Part 2).
- #7 [52] baseline: **fixed**.
- #8 [53–54]: 54 now shows the inverse: **fixed**. On 53, I and 𝟏 are still undefined, and 54 has no cue: **not fixed**. Minor.
- #9 [55]: series label **fixed**. The "⋯" still overflows the formula panel: **not fixed**. Minor.
- #10 [56] dial geometry: **fixed-but-new-problem**. The enlarged discs nearly hide the K4 spokes (Part 2).
- #11 [56]: λ_max is now defined on 44, and gold is named by the warning text: fixed. The shade is still only in the note. Negligible.
- #12 [57] katz-why: **fixed**.
  - √ scaling reads 1 → 2 → 5 → 20 → 100.
  - No cap, no stripe; the 0.95/0.99 frames hold 2 s and the gold frame comes last.
  - All coefficients are correct.
  - New problem: the caption is written in pseudo-code (Part 2).
- #13 [57] notation: partly fixed (the note gives λ_1 = λ_max). The figure still repeats a bold (**I** − α**A**)⁻¹ and uses λ_1: **not fixed**. Minor.
- #14 [58] caption: wording **fixed-but-new-problem** (pseudo-code, two lines; Part 2).
- #15 [58] red names: **fixed**. Katz and eigenvector are red, degree black (it was on slide 10).
  - Side effect, out of range: slide 33's grid drops degree (Part 2).
- #16 [69] second axis: **fixed**.
- #17 [60]: HITS named, two lines, convention stated: **fixed**. "=" instead of "∝" is **not fixed**. Minor.
- #18 [61] note on bipartite networks: **fixed**.
- #19 [62]: title and banner text **fixed**.
  - Banner and six dots are still red, and Brin & Page still precede PageRank: **not fixed**. Minor.
  - Kleinberg was rejected.
- #20 [63]: **fixed**.
- #21 [65] outgoing link, crossed dashed arrow: **fixed**. Totals 1.00/0.80/0.60/0.13/0.00 are correct.
- #22 [66] teleportation on the dead-end graph: **fixed**. E 0.359, C 0.316, B and D 0.117, A 0.091, total 1.00, all recomputed.
- #23 [67] PPR wording and dashed caption: **fixed**. Values recomputed on the dead-end graph.
- #24 [68] place names on the left: **fixed**. They are in two paragraphs (Part 2, Minor).
- #25 [68] fused markers and border labels: **fixed**.
- #26 [64–67] bullets: **fixed**.
- #27 [70] cue colour: rejected, not re-raised.

## Part 2: New findings

slides 53–58 — Major — Katz has no tricky question-then-answer pair. The lecturer asks for concept → formula → tricky two-graph question → answer for every measure; eigenvector has 42–43 and PageRank has 63–64. — Fix: after slide 57, insert two slides.
- Question: "## Which lettered node scores higher?", with the line "Katz, α = 0.5 / λ_max of each network." It reuses `quiz-eig.png`, with the cue "*Take 30 seconds.*".
- Answer: "## Answer", left M 0.87 > X 0.81, right H 1.00 > K 0.81 (largest = 1). Computed with `np.linalg.solve` on `EQ_L`/`EQ_R`; add them to `smallgraphs` as `N["KQ"]`.
- Answer caption: "halfway to 1/λ_max, Katz agrees with eigenvector centrality on the left and with degree on the right".

slide 57 — Minor — The caption is pseudo-code: "1 / (1 - alpha lambda_k)". — Fix: "circle: the weight of term k, 1/(1 − αλ<sub>k</sub>)". Unicode α and λ are not KaTeX and already render in the hand font on the stages (slides 48 and 56).

slide 58 — Minor — The caption is pseudo-code and wraps to two lines, with "1 /" at the end of line 1 and "lambda_max" on line 2. — Fix, one line: "the two ends of Katz: α → 0 gives degree, α → 1/λ<sub>max</sub> gives eigenvector centrality".

slide 42→43 — Minor — The figure jumps about 40 px up at the reveal: 42's line wraps to two lines, while 43's is one. The title says "marked", but the nodes are only lettered. — Fix: title "Which lettered node scores higher?"; line "Eigenvector centrality: compare the two lettered nodes." (one line).

slide 43 — Minor — The red "0.85" beside K touches K's red ring (gap of about 2 px). — Fix: move the label about 8 bp left in `quiz-eig-answer`.

slide 37 — Minor — The identity "0.64 + 0.58 + 0.81 + 0.85 = 2.88 × 1.00" is visible for 2.4 s of an 11 s loop and is absent from frame 0, the exported still. The shade is unexplained. — Fix: keep the identity on in frame 0 and through the B frames (or hold frame 4 for ≥ 5 s); figcaption "shade and number: the score".

slide 48 — Minor — The note "Ask before step 3: which of B and D will end up higher? Most of the room says D" is stale: slides 37 and 41 already print B 0.64 > D 0.58, and 42–43 just taught the pattern. — Fix: ask "After how many steps does the order stop changing?" (step 4).

slide 50 — Minor — The figure says "last clique" and the caption says "growing clique"; K is undefined; the shade is unstated. — Fix: figure text "… of the score in the growing clique"; caption "K: size of the growing clique; shade: eigenvector centrality".

slide 51 — Minor — Three problems with "60 km" and its circle:
- "60 km" breaks between "60" and "km" in bullet 1 and in the caption.
- Manhattan, the circle's centre, is not marked.
- The NYC locator box and the dots hide the circle's right half, so it reads as a "C".
— Fix: `60&nbsp;km`; caption "dashed circle: 60 km around Manhattan"; draw the circle above the locator box.

slide 53 — Minor — $I$ and $\mathbf{1}$ in $\mathbf{c} = \beta(I-\alpha A)^{-1}\mathbf{1}$ are undefined. — Fix: append "$I$: identity; $\mathbf{1}$: all ones." to the body line.

slides 39, 54 — Minor — These are the only question slides in range with no thinking cue. — Fix: add "*Take 30 seconds.*" to both.

slide 55 — Minor — The formula's "+ ⋯" runs past the panel edge (x ≈ 617) to x ≈ 655, about 35 px from the figure's top-left node. — Fix: $(I-\alpha A)^{-1} = \sum_{k\ge 0} \alpha^k A^k$, or break the line after "=".

slide 56 — Minor — With the enlarged discs, each 4-clique's centre node sits 6–8 px from its three neighbours, and the K4 spokes shrink to slivers. Slide 49 shows them clearly. — Fix: raise the 4-clique radius in `ring_layout` from 52 to about 60 and re-paste `POS`. Keep NODE_R at 21.

slide 57 — Minor — The figure repeats the panel's left side as a bold (**I** − α**A**)⁻¹, and its α labels use λ_1 while the title and the dial use λ_max. — Fix: drop the figure's left label; set the `KSTEPS` labels to "α = 0.5/λ_max", and so on.

slide 62 — Minor — Red is used as decoration: the banner and all six dots are red. Brin & Page appear four slides before PageRank is taught. — Fix: dots in accent blue, banner in black; move the slide after 67.

slide 40 — Minor — Gold (negative) is never named on screen, here or on 44 and 47. "Positive everywhere" ignores that an eigenvector's sign is free. — Fix: "In a connected network, only the eigenvector of the largest eigenvalue can be taken positive (blue) everywhere; gold: negative."

slide 60 — Minor — With "=", $a = A^\top h$ and $h = A a$ have only the zero solution unless $A^\top A$ has eigenvalue 1; slide 61 uses ∝. — Fix: write ∝ in both lines.

slide 68 — Minor — The five places run as two paragraphs split 3/2 for no reason, so the room reads a run-on list. — Fix: five lines, "Closeness: Middletown" / "Harmonic: the Bronx" / "Eccentricity: east of Binghamton" / "Betweenness: Monticello" / "Eigenvector: Hempstead".

slide 33 (outside range; affects 58) — Minor — `grid-row1` drops the degree cell that `grid-empty` (slide 10) shows; the cell reappears on 58. — Fix: keep degree (black) in `grid-row1`.

## Checked and clean

36 (apart from the quote marks), 38, 41, 44, 45, 46, 47 (values for t = 1…16), 49, 52, 59, 61, 63,
64, 65, 66, 67, 69, 70. No em dash, no "crown", and no answer leak on any question slide (39, 42, 49, 54, 63).

# R3 review, reviewer B: slides 29–56

## What was checked

- **Slides:** every PNG from 028 to 057 was opened (028 and 057 only for the transitions).
- **Builds:** every frame was viewed for btw-def (00–15) and eigen-inherit (00–08). For decomp-sum, decomp-square and decomp-power, frames 00, 01, a middle frame and the last were viewed.
- **Pixel comparisons:**
  - Each Q/A pair was compared for vertical offset (29/30, 35/36, 37/38, 46/47, 49/50, 51/52).
  - The grid was compared on slides 10, 40 and 71, and the decomposition row on 53, 55 and 56.
  - Each build's last frame was compared against its still.
- **Numbers:**
  - Recomputed with numpy:
    - the EIG spectrum and eigenvector;
    - the EQ_L and EQ_R eigenvectors;
    - the betweenness and eccentricity of DB, SQ, EB and the bowtie, by hand;
    - every decomp-power coefficient for t = 1, 2, 3, 8 and 16.
  - From `data/ny_network.json`:
    - the 473 km eccentricity;
    - Binghamton ÷ Syracuse = 3.50;
    - four of the top five betweenness interchanges are on NY 17.
- **Result:** every number in figures, bullets and notes matches. No winner is wrong, and no Q slide shows its answer.

**Count:** Blockers 0 · Majors 5 · Minors 20

---

## Majors

### M1. Slides 55 → 56 (and 53): the decomposition row moves between slides
Slides 53, 55 and 56 show the same drawing: "LHS = circle + rank-1 piece + …". It does not stay in place. The table gives where the first circle sits on each slide (measured on the PNGs).

| slide | first circle, left x | top y | piece size |
|---|---|---|---|
| 53 | 199 | 252 | ~85 px |
| 55 | 241 | 256 | ~77 px |
| 56 | 262 | 279 | ~73 px |

- 55 → 56 are consecutive slides, and the row jumps 21 px right and 23 px down.
- Causes:
  - each left-hand side ("A =", "A² =", "Aᵗ/λ₁ᵗ =") has a different width;
  - decomp-power reserves a "t = …" band at its top;
  - the three figures have different canvas heights (827, 814 and 889 px).
- This breaks the lecturer's first rule: the same drawing stays in the same place.
- **Fix:**
  - Emit decomp-sum, decomp-square (last frame) and decomp-power on one canvas with one `box`.
  - Right-align the left-hand side at a fixed x, so the four terms sit in the same columns on all three slides.
  - Either reserve the "t = …" band (empty) in decomp-sum and decomp-square too, or move "t = 16" out of the figure into the line above.

### M2. Slides 46 → 47: the seven-panel figure drops 4 px between Q and A
- The PNG diff gives a best match at dy = +4 px (residual 0.017). Everything else is identical, except the added frame and the "all positive" tag.
- Cause: the line above on 47 contains `$\lambda_{\max}$`, which makes that line box taller than the plain line on 46.
- **Fix:** do one of these:
  - write "λmax" in Meslo, not as math;
  - give the lead line a fixed height on both slides;
  - put the same math on 46.

### M3. Slide 44: bullet 1 contradicts the final picture, and the 2.88 has gone before the formula appears
- Bullet 1 says "A node's score: **the sum** of its neighbours' scores."
- The last frame (the still, and the frame on screen when bullet 2 is revealed) shows A = 1.00. Its neighbours sum to 0.64 + 0.58 + 0.81 + 0.85 = 2.88.
- The line "… = 2.88 × 1.00" reconciles the two, but it exists only in frames 04–07. Frame 08 removes it, together with the hot A and the brushes.
- So the formula's 1/λ arrives with no 2.88 on screen, and the PDF shows a slide whose bullet and figure disagree.
- **Fix:**
  - Bullet 1: "A node's score ∝ the sum of its neighbours' scores."
  - Keep "= 2.88 × 1.00" (or a short "λ = 2.88") in the last frame. eig-pf is pixel-identical to frame 08, so it would carry that line on slide 48 too, which suits "That eigenvector …".

### M4. Slide 34: the node names clash with the formula, and the numbers mean something new
- The formula and the second bullet use σ_st, with s and t as the endpoints.
- In the figure, the endpoints are **S and D**, and the node called **T** is a through-node. A student will read t = T.
- The values 1/2, 1/2 and 1 are shares of the single pair S–D. Slide 33, one slide earlier, used the same "number beside a node" for the node's total betweenness.
- In this graph T's total is 3.5 (asserted in `verify_numbers.py`) and A's and B's are 1, so the figure invites a misread.
- **Fix:**
  - Name the endpoints `s` and `t` (lower case, as in the formula) and give the through-node any other letter (e.g. C).
  - Add a muted tag "pair s, t" next to the brushes.

### M5. Slides 53–56: every eigenvector bar is filled cool blue, three slides after "blue = positive"
- Slides 46–47 teach the colour code "Blue: positive, orange: negative", and that only the λmax eigenvector is all positive.
- Slides 53, 55 and 56 then draw every u_k (tall bar and wide bar) solid blue. Read with that code, every eigenvector is all positive.
- On **54** it is impossible: two all-blue (all-positive) vectors "multiply to 0".
- The eigenvalue circles do use the code correctly (λ₇ orange, λ₇² blue). Only the bars break it.
- In decomp-square frame 01, the multiplied bars turn orange, which on these slides also reads as "negative".
- **Fix:**
  - Fill the bars with a neutral fill (`pale`, or `faint` with the pencil outline), and keep cool/hot for the eigenvalue circles only.
  - In decomp-square frame 01, mark the multiplied pair with a hot outline or underline, not a hot fill.

---

## Minors

**29–30**
- **28 / 30, answer bullets not parallel.** Slide 28 gives numbers ("F: worst case 2. E, the best on average, has 3."). Slide 30 does not ("L beats K, the best on average."), although its figure shows 2 and 3. Fix: "L: worst case 2. K, the best on average, has 3."

**33**
- **16 frames, 15 clicks.** The brief says 4–10 is typical. Frames 09–13 repeat the same move (one more letter, +1). Fix: step A's four letters one at a time, then B's four, C's three and D's two as one frame each, then the zeros and the hot D (about 9 frames). Every intermediate count was checked, and all are correct.
- **Bullet 1 wraps to three lines.** Fix: "One letter per pair, along a shortest path."

**34**
- **Bullet 2 holds two definitions, and "shortest paths" should be "number of shortest paths".** Fix: "σ_st: number of shortest s–t paths." Move σ_st(i) to the notes, or make it its own short bullet.
- **∑ is text-size beside a `\dfrac`.** Bullet 1 here and bullet 2 on 44 both do this, so the sum looks undersized. Fix: `\displaystyle\sum`.
- **The A route is brushed hot, the same colour as T (the point).** The hot route suggests the A route is special. Fix: brush both routes in non-hot colours (cool and gold), and keep hot only on T and its "1".
- **The two brushes on the shared T–D segment show the ink edge between them, so they read like a railway track.** Fix: offset them less, or draw one gold brush on T–D.

**39**
- **Bullet 2 wraps to three lines.** Fix: "Of the eight cities: Binghamton, 3.5 × Syracuse."
- **Binghamton is muted grey.** The notes call this slide the answer to this morning's question (slide 6, "which of the eight cities"). Fix: label Binghamton in cool (second emphasis).
- **Notes only:** Monticello beats the NY 17 / NY 8 / NY 10 interchange near Binghamton by 0.2% (0.3632 against 0.3626). It is worth one clause in the notes, in case a student asks.

**40**
- **The grid's columns do not align.** The shortest-path row has 4 cells and the walk row has 5, so "how they become one number" does not read as a column axis. This is a group issue, also on slides 10, 71 and 81 (the grid itself does not move between 10, 40 and 71; checked).
- **Cramped labels.** The "walks" row label sits in an 18 px gap between the two rows. The degree cell's text is top-aligned, with an empty lower half.

**44 / 48**
- **A's "1.00" sits diagonally lower-right, halfway towards E.** Every other value sits directly above or below its node. Fix: put it left of A, where there is free space between the B–A and A–D edges.
- **48, speaker note.** "The same numbers as two slides ago": the numbers were on 44, four slides back, and 46 shows none. Fix: "as on 'Importance you inherit'".

**45**
- **Hot is on λ, but the bullet's hot is on "eigenvector".** The eigenvector is the c bar. Fix: draw λ in ink. If anything in the figure is hot, make it the c bar or its label.

**46–47**
- **"Perron–Frobenius" is hot bold with an underline (the deck's strong style).** On these slides orange means negative. Fix: plain ink bold for this term here.
- **46/47: the leader tick for "−0.43" reads as a bar.** It runs down between "−0.72" and "0", so it looks like a separator. Fix: shorten the tick, or put "−0.43" above the axis.

**49**
- **The middle-node rule fails.** M is drawn at the horizontal centre of the figure (x ≈ 943 of 690–1175), and M wins, so a guess by position is right. The degree trap works (X has 4 neighbours and loses), but the "drawn in the middle loses" rule does not. Fix: lengthen X's leaf edges, or move the hub pair right, so X sits at the visual centre.

**52**
- **K's underline ends about 9 px from the K1–K edge.** Fix: move "0.85" a little up and left.

**53**
- **The caption is prose and wraps to two lines, with "transposed" orphaned.** Fix: "circle: eigenvalue · tall bar: eigenvector · wide bar: its transpose" on one line, or move it to the notes.
- **Italic $A$ in the line above, bold upright **A** in the figure.** Slide 45 uses italic. Fix: use one.

**53–56**
- **Empty space below the figures.** The figures end near y = 410, leaving about 250 px empty. Fix: emit at a larger scale (also helps M1).

**55**
- **Frames 00–02 are hard to parse.** The product terms have no λ labels and no product sign, so "○▯□ ○▯□" is hard to read as a matrix product. Fix: small λ₁ and λ₂ labels above the circles in frame 00, or parentheses around each factor.

**56**
- **The step counter "t = 16" (and t = 1, 2, 3, 8) is hot.** It is not the point, and in frames t = 1 and t = 3 hot is also the negative circle. Fix: draw it in ink or muted.
- **Uneven spacing in "0.02  u₇u₇ᵀ".** The term has a wider gap than the others (also "0.61" and "0.14" in earlier frames), because the label reserves a slot for the minus sign. Fix: right-align the number against the u.

**Transition 56 → 57 (57 is outside my range)**
- **The power-iteration stage draws the same seven-node graph in another style and another layout from slides 44 and 48.** The stage uses saturated blue discs with white bold letters and a grid-paper background. Worth a look by whoever has slide 57.

---

## Checked and fine

- **29–30, 35–38, 49–52:**
  - Q and A at the same place (dy = 0).
  - Winners correct: L 2 vs K 3; E = G = 30 vs F 25; O 19/2 vs M 9; M 0.85 vs X 0.46; K 0.85 vs H 0.62.
  - The middle node or hub loses on EB, DB, SQ and EQ_R.
- **31:** 473 km (472.7) is correct, and so is "on NY 17 east of Binghamton" (NY 17 / NY 8 / NY 10).
- **33:** btw-def frames 01–15 are each one letter, and every running count is correct. The final values are 0 / 8 / 9 / 8 / 0.
- **44:** the eigen-inherit values match the computed eigenvector (A 1, G 0.85, F 0.81, B 0.64, D 0.58, E 0.48, C 0.20; λ = 2.884).
- **46–47:** the eigenvalues (−2.26 … 2.88) and their order are correct.
- **53–56:**
  - λ² values: 8.32, 1.74, 0.31, 5.10.
  - decomp-power coefficients: 0.46/0.19/−0.78; 0.21/0.04/0.61; 0.10/0.01/−0.48; 0.00/0.00/0.14; 0.00/0.00/0.02. The 2% note at t = 16 is right.
- **Layout:** nothing on 29–56 overflows the frame (the lowest element is the cue on 46, at y ≈ 608).
- **Part slides 32 and 42, and slides 41 and 43:** fine.

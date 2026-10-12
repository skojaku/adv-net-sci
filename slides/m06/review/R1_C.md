# R1 review C — m06-centrality.md, slides 48–70 — 2026-10-12

**Verdict:** NEEDS WORK · **Blockers:** 0 · **Majors:** 16 · **Minors:** 11

Every PNG 48–70 was read, along with the four katz-dial stage screenshots. Every frame of
`ring-local`, `walks-discount`, `katz-why` and `pr-leak` was checked (contact sheets are in
`scratchpad/review_frames/sheet_*.png`). The numbers were checked against
`smallgraphs.py` and `data/ny_network.json`.

## Findings

1. **slide 48 — Major — It repeats slide 47.**
   - The power-iteration stage's step-1 note already reads "every node now holds its degree, divided by the largest, 4".
   - This slide also goes back to step 1 after the stage has reached step 30.
   - Smaller points: the letters D, F and G are black on mid-blue discs (low contrast), and the slide never says what the shade means.
   - **Fix:** cut the slide. Move its formula into the stage: the step-1 note in `power-step.js` becomes "step 1: A·1 = each node's degree, divided by the largest, 4".

2. **slide 49 — Major — The question cannot be answered as posed.**
   - "this" in "Where does this break?" refers to nothing (the slide before is about degree).
   - The body describes a construction but asks nothing, and there is no beat for thinking.
   - **Fix:**
     - Title: "Where does eigenvector centrality break?"
     - Body: "Four cliques of four, in a ring." / "Add one node to one clique. Where does the score go?"
     - Add the cue `*Predict, then tell your neighbour.*`

3. **slide 49 — Major (F1) — The shading is unexplained.**
   - In `ring-4444` the 8 nodes that join the ring are darker than the 8 inner nodes, and nothing on the slide says what the shade means.
   - **Fix:** fill all 16 discs with one plain accent colour on this question slide.

4. **slides 50, 51 (and the slide-56 note) — Major — The percentages are not shares of the score.**
   - They measure squared mass. `eig_share` sums v_i², and the NY eigenvector is unit L2-norm.
   - The slides call them "share of the eigenvector" and "of the score". Measured as a share of the sum of entries, they are lower:

     | | as shown (squared) | share of the sum |
     |---|---|---|
     | ring, K = 4 | 25% | 25% |
     | ring, K = 5 | 89% | 68% |
     | ring, K = 6 | 97% | 85% |
     | ring, K = 7 | 99% | 91% |
     | ring, K = 8 | 99% | 94% |
     | NY, within 60 km of Manhattan | 99.7% | 96% |

   - This also breaks the link to the dial. `katz-dial.js` reports the linear share, which tends to 85% as α → 1/λ_max on the same (4,4,4,6) graph, while slide 50 said 97%. So the note "it approaches … the previous slides' localization" does not hold on screen.
   - **Fix:**
     - Switch `eig_share` and the NY figure to the share of the sum of entries.
     - Slide 50 labels become 25 / 68 / 85 / 91 / 94%.
     - Slide 51 bullet: "96% of the score lies within 60 km of Manhattan."
     - Update the slide-50 note: 89% → 68%, 97% → 85%.

5. **slide 50 — Minor — Naming and timing.**
   - The figure says "in the last clique" and the caption says "the growing clique": two names for one thing, and "last" comes from the order of the code's tuple.
   - K is never defined, "Localization" is never defined in words, and the shading is unexplained.
   - Each of the K = 4 and K = 5 frames lasts 0.9–1.1 s, so the key jump flashes by.
   - **Fix:**
     - In-figure label: "8 nodes: 94% of the score in this clique".
     - Caption: "shade: eigenvector centrality. **Localization**: the score piles into the densest clique".
     - `ring-local` durations: 2500 ms on the K = 4 and K = 5 frames.

6. **slide 51 — Major (F4) — The map does not show the point.**
   - At column size, the NYC and Long Island dots fuse under the red Hempstead marker, and every visible dot is pale.
   - Manhattan and the 60 km radius are not drawn, so the bullet has nothing to point at.
   - "60 km" wraps between "60" and "km".
   - **Fix:**
     - Draw a dashed 60 km circle around Manhattan, labelled "60 km".
     - Add a 3× inset of NYC and western Long Island in the empty lower right of the column (y ≈ 470–600).
     - Use `60&nbsp;km`.

7. **slide 52 — Minor — Two words for one idea.** The part title says "floor"; the next slide and the lecturer's brief say "baseline".
   - **Fix:** retitle it "Everyone gets a baseline".

8. **slides 53–54 — Major (P1/N1) — The solution arrives too early and the question arrives without its object.**
   - Slide 53 gives the definition and its solved form β(I − αA)⁻¹𝟏 together, with no step between them.
   - Slide 54 then asks "What is that inverse?" without the inverse on screen.
   - I and 𝟏 are undefined, and α and β are not defined in words.
   - **Fix:**
     - Slide 53: keep only $c_i = \beta + \alpha\sum_j A_{ij}c_j$ plus "β: every node's baseline. α: the weight of a neighbour's score. This is **Katz centrality**."
     - Slide 54 top line: "Solve for **c**: $\mathbf{c} = \beta(I-\alpha A)^{-1}\mathbf{1}$ (I: identity, **1**: all ones). What is that inverse?"
     - Below it, the scalar series as the hint, with the cue `*30 seconds: guess the matrix version.*`

9. **slide 55 — Minor — The formula overflows and the series is untidy.**
   - "+ ⋯" runs out of the formula box: the box ends at x = 617 px, the dots at about 655 px, 35 px from the figure's top-left node.
   - "0α + 2α² + 1α³" shows a zero term and a coefficient of 1.
   - The convergence condition stated for the scalar series is dropped.
   - **Fix:**
     - Break the formula after "=" or write $\sum_{k\ge 0}\alpha^k A^k$.
     - Text: "$A^k$ counts walks of length $k$. So Katz counts walks, each step discounted by α (while the series converges)."
     - Figure series: "$2\alpha^2+\alpha^3+11\alpha^4+\cdots$".

10. **slide 56 — Major (F2, consistency) — The dial draws the graph differently from slide 50, with avoidable crossings.**
    - The dial draws the (4,4,4,6) ring as a rectangle, with each 4-clique as a square plus both diagonals: 3 crossings on a planar K4.
    - Students just saw the same graph as the K = 6 frame of slide 50: a diamond ring, 4-cliques drawn as a triangle with a centre node, and the big clique on the right.
    - **Fix:** use `ring-local`'s K = 6 node coordinates for `CENTER`/`POS` in `katz-dial.js`.

11. **slide 56 — Minor (F1) — Undefined symbol and unexplained colours.**
    - λ_max first appears here and is never defined.
    - The meaning of the shade and of gold is only in the speaker note.
    - **Fix:** add one line under the slider in the side card: "λ_max: largest eigenvalue of A. Shade: score ÷ largest; gold: negative."

12. **slide 57 — Major (F1, lecturer requirement "intuitive from the circle picture") — The blow-up is not visible in the circles.**
    - Diameters are capped at 100 bp, so 5 (90 bp), 20, 100 and −10 are drawn almost the same size.
    - The cap is marked by a white band across the circle (`cap_break`) that nothing explains; it reads as "crossed out".
    - Frames last 1.3 s.
    - The slide never says that the circle is now 1/(1 − αλ_k), not λ_k.
    - **Fix:**
      - Drop the white band. Let circle 1 grow past its slot, drawn behind the other terms: 18 bp per unit up to the full figure height. That gives 0.8 → 90 bp, 0.95 → 280 bp ("20"), 0.99 → 280 bp ("100 → ∞ at 1/λ_max"), and 1.1 → a gold circle at its true 180 bp.
      - Hold the 0.95, 0.99 and 1.1 frames for 2.5 s each.
      - Add the caption "circle: 1/(1 − αλ_k)".

13. **slide 57 — Minor — Notation clashes on one slide.**
    - The title uses λ_max; the figure uses λ_1.
    - The formula box has italic $(I-\alpha A)^{-1}$; the figure has bold $(\mathbf{I}-\alpha\mathbf{A})^{-1}$.
    - **Fix:** in `figs_decomp.py`, the `KSTEPS` labels become `\lambda_{\max}`, and the left label becomes `$(I-\alpha A)^{-1}$`.

14. **slide 58 — Major (exact wording) — The caption is inexact.**
    - "one series, cut at different lengths" is wrong for two of the three: Katz is the whole series, not a cut, and eigenvector centrality is its limit as α → 1/λ_max, not a cut.
    - **Fix:** caption "degree and eigenvector are the two ends of Katz: α → 0 ranks by degree, α → 1/λ_max ranks by the eigenvector".

15. **slides 58, 69 — Major (lecturer: red for emphasis only) — Red marks a category, not emphasis.**
    - Every centrality name in the grid is accent-2 red: 7 on slide 58, 9 on slide 69.
    - **Fix:** names in black. On each build slide, only the cells new on that slide are red: degree, Katz and eigenvector on 58; PageRank and HITS on 69 (the same rule applies to slide 34 for row 1).

16. **slide 69 — Major (lecturer requirement: classification by the two axes) — Only one axis is labelled.**
    - The rows give "shortest paths" and "walks" (which routes count).
    - Nothing names the second axis, how the routes become one number. It exists only implicitly in the cell texts.
    - **Fix:** add a vertical title "which routes count" left of the row labels, and a header "how they become one number" above the cells.

17. **slide 60 — Minor — Missing name, overflow and loose notation.**
    - "HITS" never appears on the slide, yet the next slide's title says "HITS is eigenvector centrality".
    - The second equation overflows its box: "a_j" ends at about 633 px, the box at 617 px.
    - The directed convention for A_ij is not stated.
    - "=" here conflicts with "∝" on slide 61.
    - **Fix:**
      - Text: "**HITS** (Kleinberg, 1999). $A_{ij}=1$ if i links to j."
      - Put the two equations on two lines, written with ∝: $a_i \propto \sum_j A_{ji}h_j$ and $h_i \propto \sum_j A_{ij}a_j$.

18. **slide 61 — Minor — The figure is not tied to HITS.**
    - It shows the 7-node graph's eigenvector again, as on slides 41 and 47, without saying that it is HITS.
    - The claim needs λ_max > |λ_min|. That holds here (2.88 against −2.26) but fails on a bipartite network.
    - **Fix:**
      - Caption: "HITS on this road map: authority = hub = eigenvector centrality".
      - Add to the note: "needs λ_max > |λ_min|; on a bipartite network HITS is not unique."

19. **slide 62 — Major (correctness) — The heading's claim is false for two of the six.**
    - "one equation, six times: Ac = λc" is false for Katz (1953) and Hubbell (1965). The deck has just shown Katz as β(I − αA)⁻¹𝟏.
    - Brin & Page appear before PageRank is introduced (slides 63–66), and Kleinberg (HITS, slide 60) is missing.
    - The red in-figure heading repeats the title, and all six dots are red.
    - **Fix:**
      - Move the slide to after slide 67 and add "1999 Kleinberg".
      - Title: "The same idea, seven times".
      - In-figure heading, in black: "a node's score is built from its neighbours' scores".
      - Dots in accent blue.

20. **slide 63 — Minor — Undefined symbol and no beat.** $d^{\text{out}}_j$ is undefined, and there is no thinking beat.
    - **Fix:** add "$d^{\text{out}}_j$: number of links out of j." and the cue `*Vote: C or E?*`.

21. **slide 65 — Minor — Inexact wording and a hidden change.**
    - "E loses its only link" is inexact: E still has its incoming link from C.
    - The removed E → A link is simply absent, so students must notice that the bottom loop is gone.
    - **Fix:**
      - Text: "E loses its only outgoing link."
      - Draw E → A as a dashed gray line with a cross, as the cut E–F edge is drawn on day 1.

22. **slide 66 — Major (flow) — The dead end from slide 65 is never shown fixed.**
    - The figure is drawn on the original graph, with E → A restored.
    - **Fix:**
      - Draw `pr-teleport` on `PR_DEAD`.
      - Print `pagerank(PR_DEAD, r=0.15)`: E 0.359 (marked), C 0.316, B 0.117, D 0.117, A 0.091.
      - Print "total 1.00" where slide 65 printed "total 0.00".
      - Text: "With probability r = 0.15, jump to a random page. A dead end always jumps. This is **PageRank**." This matches the existing speaker note.
      - With the slide's formula alone, the total settles at 0.33 instead of 0. Rescaled to 1, it gives the same scores.
      - Slide 67 can then use `PR_DEAD` too. Its numbers do not change (A .335, B .095, C .257, D .095, E .218), because the dead end jumping to A equals the old E → A link.

23. **slide 67 — Major (correctness) — The figure contradicts the text.**
    - The text says "The scores now measure how close each page is to A". But B and D are one step from A and score 0.095, while E is two steps away and scores 0.218.
    - The dashed edges are unexplained.
    - **Fix:**
      - Text: "Each score is how often a surfer who keeps restarting at A is on that page."
      - Caption: "dashed: the jump back to A".

24. **slide 68 — Major (lecturer requirement: map right, bullets left) — No bullets and no place names.**
    - The left side is one sentence.
    - The five places exist only in the speaker note, though the title promises "five places".
    - **Fix:** make the left side `*` fragments:
      - "closeness: NY 17 at Middletown"
      - "harmonic: I-95 in the Bronx"
      - "eccentricity: NY 17 east of Binghamton"
      - "betweenness: NY 17 at Monticello"
      - "eigenvector: I-495 at Hempstead"

      Drop "One network. Each measure crowns a different place." or keep it as the line above the list.

25. **slide 68 — Major (F3) — Two markers fuse and three labels sit on the border.**
    - The harmonic (Bronx) and eigenvector (Hempstead) winner dots overlap into one red blob, so two leader lines end on one mark.
    - "closeness", "harmonic" and "eigenvector" sit on the state's eastern border, which runs through their first letters.
    - **Fix:**
      - Add a 3× inset of NYC and western Long Island in the empty band below the map, holding the two dots apart.
      - Move the three east labels to x ≥ 1030 px, clear of the outline, or below the map.

26. **slides 64–67 — Minor (lecturer requirement: concise bullets on the left) — The left text is paragraphs.**
    - The left side is two sentences as paragraphs, so both land at once.
    - **Fix:** make them `*` fragments. For example, 64: "* A, C, E: 3/11 each. B, D: 1/11." "* E's one link comes from C, and C passes on everything."

27. **slide 70 — Minor (F3) — The cue is too faint.**
    - The cue "Bring it to the next class." is rgb(210,210,210) on white, a contrast of about 1.5:1, unreadable from the back row.
    - **Fix:** set the `.cue` colour to the annotation gray #6b6b6b (theme-wide).

## Checked and clean
- **59** (part divider, Web has direction)

## Minor findings only
- **52**, **63**, **65**, **70**. Slide 70 matches the lecturer's quiz wording, and nothing follows it.

## Numbers verified correct
- **48**: degrees.
- **56**: 33% at α = 0, 40/63/81% shares, λ_max = 5.084.
- **57**: coefficients 1, 2, 5, 20, 100, −10 and the u_2, u_3, u_7 values.
- **60**: HITS edges, hub A, authority E.
- **61**: eigenvector values.
- **64**: 3/11 and 1/11.
- **65**: totals 1, 0.8, 0.6, 0.13, 0.
- **66**: PageRank values.
- **67**: PPR values.
- **55**: walk counts 0, 2, 1, 11.
- **51**: 31% of interchanges (91 of 289).

Day 2 length: 35 slides, within the limit.

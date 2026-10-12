# m06 review round 2: fix direction

From R2_A.md (slides 1–35) and R2_B.md (36–70), triaged by the lead. No Blockers; three Majors
(Roman labels hiding an edge, sigma-answer without its caption, no Katz question).

**Not taken:** the crown on roma-degree; the genealogy's position; bold vs italic A in figures;
"=" vs "∝" on the HITS slide; katz-dial edge contrast; slide 46's empty lower half.

Already changed in `figures/smallgraphs.py` (import, never type):
- `EA_XY` (broom) and `SQ_XY` (fork + square) re-laid so the drawn middle is the loser
  (E, M), not the winner (F, O); asserted in `check()`.
- `katz_q()` and `N["KQ"]`: Katz centrality at α = 0.5/λ_max on the eigenvector-quiz graphs,
  largest = 1. Left M 0.87 > X 0.81 (agrees with the eigenvector); right H 1.00 > K 0.81
  (agrees with degree).

Every agent: build only your own modules, open every PNG you change with Read, do not commit.

---

## Agent Q2 — `figs_quiz.py`, and `fig_sigma_answer` in `figs_small.py`
1. Rebuild `quiz-ecc`, `quiz-ecc-answer`, `quiz-btw`, `quiz-btw-answer` with the new `EA_XY`
   and `SQ_XY`. In `quiz-ecc-answer` the grey "best closeness" tags must point at E and K from
   the side away from the eccentricity winners (F, L), never sitting under or beside F or L.
2. `quiz-eig-answer`: K's value must not touch K's ring.
3. New `quiz-katz-answer` (full): exactly the `quiz-eig` question geometry (assert it), values
   from `N["KQ"]` beside M, X, H, K (2 decimals), M and H marked. The Katz question slide
   reuses `quiz-eig.png` itself, so no new question figure.
4. `sigma-answer`: about 25% shorter (compress the vertical layout; type and discs stay the
   same size) so its slide has room for a one-line caption again.

## Agent R2 — `figs_defs.py`, `figs_eigen.py`, `romelib.py` (+ `figs_rome.py` for `roma-degree` only)
1. `grid-row1`: keep the degree cell (shown on `grid-empty`); it must not vanish and reappear.
2. `eigen-inherit`: the final frame (which is also the still and the first frame) keeps A's sum
   line "0.64 + 0.58 + 0.81 + 0.85 = 2.88 × 1.00".
3. Roman map labels (`romelib`, used by `roma-degree` and the last frame of `roma-to-graph`):
   no label box may cover an edge that does not end at that label's own city. In particular the
   Roma–Alexandria link must be visible end to end, and all 5 of Roma's links must visibly
   leave its disc. Move labels (Thessalonica, Roma, others as needed) to free sides; add a build
   assertion that checks label boxes against all non-incident edges. Then rebuild
   `roma-degree` (figs_rome) and `roma-to-graph` (figs_intro). If the crown on Roma sits on an
   edge, move it to a free side.

## Agent T2 — the deck `m06-centrality.md` (+ `review/DECK_SPEC.md` slide list)
Slides by title. Apply exactly:
1. **20 BC, the Forum Romanum**: first bullet → "Augustus (Caesar's heir) set up the **Golden
   Milestone** in 20 BC."
2. **How far is u from v?** and **What if one road closes?**: remove `<!-- _class: mid -->`.
   On the first, delete "Someone says 2." from the note.
3. **Closeness centrality**: second line → "$\ell_{ij}$: shortest-path length from $i$ to $j$;
   $N$: number of nodes."
4. **Which node is closest to everything?** line → "Smallest sum of distances wins. Two
   separate networks."
5. **New York: closeness** third bullet → "31% of the interchanges lie within 60 km of
   Manhattan, so the winner sits near the city."
6. **Take the reciprocal first**: body → "**Harmonic centrality**." then a new paragraph
   "$1/\infty = 0$: an unreachable node adds nothing."
7. **Which node has the highest harmonic centrality?** line → "Left: the closeness network,
   road E–F open. Right: two pieces."
8. **Which node has the smallest eccentricity?** and **Which node carries the most?**: add the
   cue `<div class="cue">` "*Take a minute.*" after the figure.
9. **Betweenness centrality**: restore a figcaption: "S to D: two shortest paths, so A and B
   each carry half of this pair".
10. **New York: betweenness** figcaption → "darker, larger dot: more paths pass through".
11. Part Three divider: title "The company you keep", subtitle "importance you inherit".
12. **Aesop**: curly quotes “A man is known by the company he keeps.”
13. **Seven eigenvectors. Which one?** and **What is that inverse?**: add the cue
    "*Take 30 seconds.*".
14. **Perron and Frobenius** line → "In a connected network, only the eigenvector of the
    largest eigenvalue is positive (blue) everywhere. Gold: a negative entry."
15. **Which marked node scores higher?** → title "Which lettered node scores higher?"; line →
    "Eigenvector centrality: compare the lettered nodes."
16. **Power iteration** note: delete the sentence that asks the room "which of B and D will
    end up higher" (the values were already shown).
17. **Localization** figcaption → "K: the size of the last clique; the share of the total
    score inside it".
18. **New York: eigenvector** figcaption → "darker dot: higher score; dashed: 60 km".
19. **Give everybody a baseline**: add a line under the bold one: "$I$: the identity matrix;
    $\mathbf{1}$: all ones."
20. **The same series for matrices**: the formula on two lines,
    `$$\begin{aligned}(I-\alpha A)^{-1} &= I + \alpha A \\ &\quad + \alpha^2 A^2 + \cdots\end{aligned}$$`
21. **Why 1/λ<sub>max</sub>?** figcaption → "circle: the weight of term k, 1 / (1 − α λₖ)".
    **The walk row** figcaption → "degree and eigenvector centrality are the two ends of Katz:
    α near 0 ranks by degree, α near 1/λmax by the eigenvector".
22. Insert after **Why 1/λ<sub>max</sub>?** (before **The walk row**) two slides:
    - "## Which lettered node scores higher now?" / line "Katz centrality, $\alpha =
      0.5/\lambda_{\max}$. The same two networks." / figure `quiz-eig.png` (full) / cue
      "*Take a minute.*"
    - "## Answer" / line "Katz centrality, largest = 1." / figure `quiz-katz-answer.png`
      (full) / figcaption "left: as the eigenvector ranks them; right: as degree ranks them" /
      note "Left: M 0.87, X 0.81. Right: H 1.00, K 0.81. At alpha = 0.5/lambda_max short walks
      still weigh a lot, so H's six neighbours count; as alpha approaches 1/lambda_max, Katz
      turns into the eigenvector and K passes H."
23. **New York: five measures, five places**: one paragraph "Closeness: Middletown. Harmonic:
    the Bronx. Eccentricity: east of Binghamton. Betweenness: Monticello. Eigenvector:
    Hempstead."
24. Update `review/DECK_SPEC.md`'s slide list (two new Katz slides; day 2 is now 38).

Then `python3 ../gatelib/check_deck.py m06-centrality.md` must pass.

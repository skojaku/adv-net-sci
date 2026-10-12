# m06 review round 1: fix direction

From R1_A.md (slides 1–24), R1_B.md (25–47), R1_C.md (48–70), triaged by the lead.
Slide titles are used, not numbers, because two slides are cut and two inserted.

**Rejected:** moving the NY question (it is the opening hook, by the lecturer's request);
the grey cue colour (lectern-only by design); adding Kleinberg to the genealogy.

Numbers already changed in `figures/smallgraphs.py` (do not edit it; import):
- `eig_share` is now the share of the eigenvector-centrality **score** (sum of entries), not of the
  squares: ring K = 4, 5, 6, 7, 8 gives 25%, 68%, 85%, 91%, 94%. NY within 60 km of Manhattan: 96%
  (sum share, 91 of 289 interchanges = 31%).
- `CA_XY` and `CB_XY` re-laid so the hub (E, N) is at the centre of the drawing and the
  closeness winner (F, P) is not.
- New eigenvector quiz: `EQ_L`, `EQ_L_XY`, `EQ_R`, `EQ_R_XY`, `EQ_LABELS`, `eigvec()`;
  `N["EQ"]`: left M 0.85 vs X 0.46, right K 0.85 vs H 0.62 (largest entry 1).
- `N["PPR_A_dead"]` equals `N["PPR_A"]`; `N["PR_dead"]` has E on top (0.359).

Every agent: build only your own module, open every PNG you change with Read, do not commit.

---

## Agent Q — `figs_quiz.py` (+ `fig_sigma_answer` in `figs_small.py` only)
1. Rebuild all quiz/cut figures with the new `CA_XY` and `CB_XY`; fix label placement if needed.
   The answer figure keeps the question's geometry (already asserted).
2. `quiz-ecc-answer`: the grey tag "closeness" becomes "best closeness".
3. New `quiz-eig` and `quiz-eig-answer` (full): `EQ_L` left, `EQ_R` right, layouts `EQ_L_XY`,
   `EQ_R_XY`. Only the four candidates carry letters (M, X; H, K); every other disc is blank.
   In the question, the candidates are marked only by their letters (no rings: the render gate
   measures a ring as a disc); no values. Answer: values
   (2 decimals, from `N["EQ"]`) beside M, X, H, K; M and K marked (accent-2 border + red value).
   Assert M > X and K > H and that the lower-degree node wins on both sides. Planar drawing
   (the 4-clique is a triangle with a centre node).
4. `sigma-answer` (in `figs_small.py`, only that function): drop the grey banner at the top (it was
   wrong: the numbers are the shares of the single pair S, D); draw the two routes in accent blue
   and gold (`accentthree`), not red; values in black. Keep the 1/2, 1/2, 1 labels.

## Agent D — `figs_defs.py`
1. Rebuild `harmonic-def` with the new `CA_XY`; G's value must sit clearly nearer G than F.
2. Grid figures (`grid-empty`, `-row1`, `-row2`, `-final`): add the two axis headers in grey:
   "which routes count" above the row labels (or beside them, rotated is not allowed — keep
   horizontal), and "how they become one number" above the cells. Centrality names in **black**,
   not red; in `grid-row1` and `grid-row2` the cells new on that slide get their name in accent-2,
   everything else black. "longest" becomes "longest distance". Keep the four states' geometry
   identical (asserted).

## Agent E — `figs_eigen.py`
1. `ring-local`: labels from the new `eig_share` (25%, 68%, 85%, 91%, 94%), text
   "K = 6: 85% of the score in the last clique". Hold each key frame ≥ 1.6 s.
2. `ring-4444`: one plain fill for every disc (the question slide must not shade).
3. `eigen-inherit`: keep the eigenvector shading throughout, print each node's score (2 decimals,
   largest = 1), and when the four arrows into A are lit show beside A
   "0.64 + 0.58 + 0.81 + 0.85 = 2.88 × 1.00" (values from `spectrum`/`EIG_v`; assert the identity
   to 2 decimals). Remove the first-frame flash of all four arrows (frame 0 = the complete
   picture is added by `emit_gif` itself).
4. `eig-pf`: largest entry set to 1 (same numbers as `eig-centrality`); it is now the
   "Eigenvector centrality" slide's figure.
5. `eigen-equation`: replace the caption line "λ = 2.88: the same seven numbers, each 2.88 times
   bigger" with "λ c: every entry of c times the same number λ" (no value of λ here).
6. `walks-discount`: the sum line becomes "$2\alpha^2 + \alpha^3 + 11\alpha^4 + \cdots$".
7. Remove `power-step1` from `FIGURES` (its slide is cut).

## Agent C — `figs_decomp.py`
1. Bars (u_k, u_kᵀ) in solid `accent` (they were 1.4:1 contrast). Matrix outline stays light grey.
2. `decomp-square`: label the final circles $\lambda_1^2$, $\lambda_2^2$, … above them (like
   `decomp-sum`'s $\lambda_k$ labels).
3. `katz-why`: circle diameter ∝ √|coefficient| (so 1, 2, 5, 20, 100 read as growing), **no cap and
   no white stripe**; the canvas may be taller (≤ 380 bp). Hold the 0.95, 0.99 and 1.1 frames
   ≥ 2 s. Keep the gold "negative" frame last.
4. `decomp-power`: the "+" before the last term must not overprint a box edge.

## Agent W — `figs_dir.py` (+ `fig_genealogy` in `figs_web.py` only)
1. `pr-teleport`: draw `PR_DEAD` (E is a dead end, no E→A arrow) with r = 0.15 and the scores
   from `N["PR_dead"]`: E 0.359, C 0.316, B 0.117, D 0.117, A 0.091; mark E; print "total 1.00".
2. `ppr`: draw on `PR_DEAD` too; scores from `N["PPR_A_dead"]` (same values as now). Keep the
   dashed grey jump-back arrows to A.
3. `pr-leak`: show the removed link E→A as a grey dashed arrow with a small black cross.
4. `genealogy`: banner "a node's score is built from its neighbours' scores" (replaces the
   equation). Nothing else changes.

## Agent N — `figs_ny.py`, `figs_intro.py`, `romelib.py` (labels only), `make_basemap.py`
1. `ny-eigenvector`: a dashed grey circle of radius 60 km around Manhattan (−73.9712, 40.7831),
   labelled "60 km"; and a 3× inset of the NYC area (lower right, framed) so the dots separate.
2. `ny-five`: the same NYC inset; the Bronx (harmonic) and Hempstead (eigenvector) winners drawn
   in the inset, their labels off the state border.
3. Roman figures: city labels on white boxes so edges pass behind them (`romelib` label drawing:
   `fill=white` on the label node, labels drawn after edges). Affects `roma-degree`,
   `roma-to-graph`. Pins in `roma-basemap` and the GIF in accent blue, not red.
4. `make_basemap.py`: the pale basemap's land/sea contrast ≥ 30 grey levels (it is about 12).
   Rebuild `data/roma-basemap-pale.png`, then `roma-basemap` and `roma-to-graph`.

## Agent S — `lecture-note/assets/anim/power-step.js`, `katz-dial.js`, per-stage CSS
1. katz-dial: draw the (4,4,4,6) ring with the same geometry as `ring-local`'s K = 6 frame (get
   the coordinates from `figs_eigen`'s ring layout function; no crossed squares). Note text:
   "past 1/λ_max the scores turn negative" etc. unchanged; the share label is the share of the
   **sum** (it already is).
2. power-step: node values at 26–28 px (were 13–14), note line 30 px. Notes: step 1 →
   "step 1: x = A·1, every node holds its degree (÷ 4)"; first note defines x ("x: one score per
   node"); the order is fixed from step 4 (not 5); drop the claim that the wobble shrinks every
   step; last scene → "converged: eigenvector centrality. B (2 neighbours) ends above D (3)".
3. Re-verify both in headless Chrome as before (overflow 0, no errors), new screenshots.

## Agent T — the deck `m06-centrality.md` and `review/DECK_SPEC.md`
Apply exactly (titles identify slides):
1. **20 BC, the Forum Romanum**: last bullet → "Plutarch: every road of Italy ended at it."
2. **The roads themselves** → title "Twelve cities of the empire"; body
   "Roads and sea lanes joined these twelve cities."
3. **Keep the roads, drop the map** → title "Keep the links, drop the map".
4. **Degree centrality**: body → "**Degree**: $d_i = \sum_j A_{ij}$, where $A_{ij} = 1$ if a road
   joins $i$ and $j$." Add figcaption "darker: more roads; Roma has the most, 5".
5. Delete the slide **Degree sees one step**.
6. **Closeness centrality**: second line → "$\ell_{ij}$: the length of a shortest path from $i$ to
   $j$. $N$: the number of nodes."
7. Each **Answer** slide gets one line above its figure, so the figure sits where the question's
   did: closeness "The sum of distances, beside each candidate."; harmonic "Harmonic centrality,
   beside each candidate."; eccentricity "Eccentricity, beside every node."; betweenness
   "Betweenness, beside each candidate."; eigenvector (new) "Eigenvector centrality, largest = 1."
8. Harmonic answer caption → "on the left, closeness and harmonic pick different nodes".
9. **New York: closeness**: bullets "Distance: km of highway." / "Winner: NY 17 near Middletown,
   in the Hudson Valley." / "31% of the interchanges lie within 60 km of Manhattan."; figcaption
   "darker, larger dot: closer to everything".
10. **What if one road closes?**: add the cue "*Take 30 seconds.*".
11. **Take the reciprocal first**: body → "**Harmonic centrality**." then a new paragraph
    "An unreachable node adds $1/\infty = 0$."
12. Harmonic question line → "Left: the closeness network, with the road E–F open again. Right:
    two pieces."
13. **Would you site a fire station on the average?**: replace the body line with the cue
    "*Take 30 seconds.*". On **Eccentricity**, body → "A fire station must reach its farthest
    house. **Eccentricity**: the distance to the farthest node; its centrality is $1/e_i$."
14. **New York: eccentricity**: figcaption "darker, larger dot: a shorter worst-case drive".
15. **Betweenness centrality**: one line between formula and figure: "$\sigma_{st}$: the number of
    shortest paths from $s$ to $t$; $\sigma_{st}(i)$: those through $i$." Figcaption "the pair S, D
    has two shortest paths, so A and B each carry half".
16. Betweenness question line → "Count the shortest paths through each node; a tie splits the
    count."
17. **New York: betweenness**: bullets "Top interchange: NY 17 at Monticello." / "Of the eight
    cities, Binghamton is first: 3.5 times Syracuse." / "Four of the top five interchanges are on
    NY 17."; figcaption "darker, larger dot: more shortest paths pass through".
18. **Importance you inherit**: body → "A node's score is the sum of its neighbours' scores,
    divided by a constant $\lambda$."
19. **Seven eigenvectors. Which one?**: body → "This symmetric 7 × 7 matrix has seven
    eigenvectors. Which one is the centrality?"
20. **All seven** → title "Perron and Frobenius"; one line above the figure: "In a connected
    network, only the eigenvector of the largest eigenvalue is positive everywhere."
21. The old **Perron and Frobenius** slide → title "Eigenvector centrality"; body "That
    eigenvector, with its largest entry set to 1, is **eigenvector centrality**." (one paragraph;
    drop the theorem sentence). Speaker note keeps the theorem's conditions.
22. Insert after it two slides:
    - "## Which marked node scores higher?" / line "Eigenvector centrality. In each network,
      compare the two lettered nodes." / figure `quiz-eig.png` (full) / cue "*Take a minute.*"
    - "## Answer" / line from item 7 / figure `quiz-eig-answer.png` / figcaption "in both
      networks, the node with fewer neighbours scores higher" / note: "Left: M 0.85, X 0.46. M's
      three neighbours include two hubs; X's four include three leaves. Right: K 0.85, H 0.62."
23. **Eigendecomposition**: line → "A symmetric matrix is a sum of rank-1 matrices.
    $\lambda_1 = \lambda_{\max}$ is the largest eigenvalue." Note: "rank 1: every row of
    u_k u_kᵀ is a multiple of u_kᵀ."
24. **The eigenvectors are orthogonal**: figcaption → "each eigenvector scaled to length 1: two
    different ones multiply to 0, one with itself to 1".
25. **Square it**: line above the figure: "$A^2 = \sum_k \lambda_k^2\, \mathbf{u}_k
    \mathbf{u}_k^\top$: squaring squares every eigenvalue."
26. **Keep multiplying**: body → "$A^t$ counts walks of length $t$. Divided by $\lambda_1^t$, every
    term but the first fades, so $A^t \mathbf{1}$ points along $\mathbf{u}_1$." Update the note
    (0.78 per step, about 2% after 16 steps).
27. Delete the slide **Step one is degree**.
28. **Where does this break?** → title "Where does eigenvector centrality break?"; body "Four
    cliques of four, in a ring. Add one node to one clique. Where does the score go?"; cue
    "*Take 30 seconds.*"
29. **Localization**: figcaption → "share of the total score inside the growing clique"; note:
    68% with one extra node, 85% with two, 94% at K = 8.
30. **New York: eigenvector**: bullets "96% of the score lies within 60 km of Manhattan." / "31% of
    the interchanges lie there."; figcaption "darker, larger dot: higher score; dashed circle: 60
    km". Fix the note (96%, not 99.7%).
31. Part Four divider title → "Everyone gets a baseline".
32. **Give everybody a baseline**: body under the formulas → "**Katz centrality**: $\beta$ for
    free, plus $\alpha$ times each neighbour's score."
33. **What is that inverse?**: formula panel → two lines: "$(I - \alpha A)^{-1} = \;?$" and
    "$\dfrac{1}{1-x} = 1 + x + x^2 + \cdots$ for $|x| < 1$".
34. **Why 1/λ<sub>max</sub>?**: figcaption "circle: the weight of term k, 1 / (1 - alpha
    lambda_k)". Note: λ_1 = λ_max.
35. **The walk row**: figcaption → "degree and eigenvector centrality are the two ends of Katz:
    alpha near 0 ranks by degree, alpha near 1 / lambda_max by the eigenvector".
36. **Hubs and authorities**: formula panel stacks the two formulas on two lines and adds a third
    line "$A_{ij} = 1$ if page $i$ links to page $j$"; body "**HITS** (Kleinberg, 1999): an
    **authority** is pointed to by good hubs; a **hub** points to good authorities."
37. **On a road map, HITS is eigenvector centrality**: body → "If $A$ is symmetric,
    $A^\top A = A^2$, whose leading eigenvector is that of $A$." Note: holds when the network is
    not bipartite (λ_max > |λ_min|; here 2.88 > 2.26).
38. **The same equation, six times** → title "The same idea, six times".
39. **Divide the vote**: body → "$d^{\text{out}}_j$: the number of links out of $j$." then "C has
    three links in, and E has one. Which ranks higher?"; cue "*Take 30 seconds.*"
40. **A three-way tie**, **A dead end**, **Teleportation**, **Personalized PageRank**: body as
    `-` bullets (not paragraphs):
    - tie: "A, C and E: 3/11 each. B and D: 1/11." / "E's one link comes from C, which passes on
      everything."
    - dead end: "E loses its only outgoing link." / "Its score has nowhere to go: the total drains
      to zero."
    - teleportation: keep the formula; bullets "With probability r = 0.15, jump to a random page."
      / "A dead end always jumps." / "This is **PageRank**." Note: on the dead-end graph E 0.359,
      C 0.316, B and D 0.117, A 0.091.
    - personalized: "Jump back to A only." / "Score: how often a walker that keeps restarting at A
      visits each page."; figcaption "dashed: the jump back to A".
41. **New York: five measures, five places**: body → two paragraphs "Closeness: Middletown.
    Harmonic: the Bronx. Eccentricity: east of Binghamton." / "Betweenness: Monticello.
    Eigenvector: Hempstead."
42. Replace every "crown"/"crowns" in slide text: the quiz → "…each rank a different node first."
43. Update `review/DECK_SPEC.md`'s tables to the new slide list and numbers (68/85/94%, 96%).

Then `python3 ../gatelib/check_deck.py m06-centrality.md` must pass.

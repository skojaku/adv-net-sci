# m06 round 6 fixes (2026-10-14)

From R6_A (1-43), R6_B (44-88), R6_C (89-131), Tier 2 on the v4 deck, plus the lead's own pass.
Deck text and theme.css: the lead. Figure generators: one figure agent. Never both on one file.

## Deck (m06-centrality.md, theme.css)

| slides | finding | fix |
|---|---|---|
| all A/B | a long .take or cue ends against the page number (A11, B-m1, C-m1) | theme.css: `.take` and `.cue` in L-a / L-b at most 1000 px wide, so they end 40 px short of the number |
| 2 | "set it up": no antecedent (A-m1) | "set up the milestone in Rome." |
| 5 | sub too long (A-m6) | `$d_i = \sum_j A_{ij}$, with $A_{ij} = 1$ for a road.` |
| 7 | take without a hot keyword; "4" vs the legend's "4+" (A-m4) | take `Degree 3: <hot>201</hot> of 289 interchanges.`; the rest to the notes |
| 8 | the bullet is filler (A-m5) | `Count the steps from u to v.`; Module 01 to the notes |
| 23 | figure of speech, no number (A-m9) | `<hot>P</hot> wins: 0.56 against N's 0.50.` |
| 26-27 | the question does not say what to predict (A-m10) | sub `Close E–F. What is every node's closeness?` |
| 28-33 | take without a hot keyword, too wide (A-m11) | `<hot>Unreachable</hot> nodes add $1/\infty = 0$.` |
| 35 | 27/4 vs 19/3 not rankable at a glance (A-m12) | `Harmonic picks the hub <hot>E</hot>: 27/4 = 6.75.` |
| 40-43 | sub too long, two rules (A-m7) | `$e_i = \max_j \ell_{ij}$: the smallest wins.`; $1/e_i$ to the notes |
| 45, 47 | take at the limit (B-m1) | `…, best on average, 3.` |
| 57 | take runs into the page number (B-m1) | `Each <hot>hub</hot> carries 30; the bridge F, 25.` |
| 60 | hot Binghamton in the take, hot Monticello on the map (B-M1) | take `<hot>Binghamton</hot>: first of the eight cities.` + figure F6c |
| 61, 112 | grid titles name the figure (C-m8) | `Shortest paths: five measures`, `Walks: degree, Katz, eigenvector` |
| 63 | caption wraps inside the date (B-m8, lead) | `Velázquez, 1638–41, Prado` |
| 76 | caption says colour = eigenvector, circles are coloured by sign (B-M2) | caption names both |
| 77 | sub 56 characters (B-m3) | `Two colours multiply to 0; the same colour, to 1.` |
| 87-88 | panels unexplained (B-M3) | title `Random starts: the same scores` + figure F7 |
| 90-94 | shade unexplained; "one node at a time" is wrong at K = 8 (C-M2, C-m4) | sub `Shade: score. Grow one clique to K nodes.` |
| 95, 127 | take without a hot keyword (C-m2) | hot `31%`; hot `restarts` |
| 98 | the cue sits under the take, at the frame's edge (lead) | cue before the take |
| 99-102 | the walks are not said to be from u to v (C-M1) | take `Entry (u, v): <hot>walks</hot> from u to v, discounted.` |
| 108-111 | the scale of the values is only in the notes (C-m7) | sub `Katz, α = 0.5/λmax. Top score = 1.`; shorter cue |
| 114 | figcaption prints `A_ij` raw (C-m9) | `Aᵢⱼ = 1: page i links to page j` (KaTeX does not run in a figcaption) |
| 122-125 | "total" unexplained, shade unexplained (C-M3) | sub `E loses its only link out. Shade: score.` + figure F11 |
| 130 | title wraps (C-m13) | `Draw a network with four winners` |
| 131 | take ends against the number (C-m1) | covered by the 1000 px rule |
| 86 | the stage frame covers the page number (B-m10) | theme.css: stage margin-bottom |

## Figures (figure agent; keep every group's canvas, crop and frame-00 equalities)

- F1 `roma-degree` (A-B1, Blocker F1): the shade is degree but nothing says so. Add a muted key
  "degree" with the shades it uses, as on `ny-degree`, inside the existing crop.
- F2 `harmonic-def` frames (A-M1): H's values ("1/1", "10/3") directly beside H, clear of the callouts.
- F3 `q-close-CB-ans` (A-m8): N's "0.50" directly above or below N.
- F4 `q-harm-HD-ans` (A-m13): the brush under the hot "4" sits under the number.
- F5 `q-eig-R-ans` (B-m7): "0.62" directly under H.
- F6 New York maps (A-M2, A-M3, B-m9, B-M1): (a) `ny-overview`: "Rochester" clear of the Watertown pin,
  "Buffalo" on a halo; (b) every measure map (closeness, eccentricity, betweenness, eigenvector) gets a
  two-end shade key like `ny-degree`'s legend, naming its measure; (c) `ny-betweenness`: Binghamton is
  the answer, so it is hot (disc, label, underline); Monticello's label muted.
- F7 `power-starts` (B-M3): a muted label on each panel, "start 1" to "start 4", the fourth also on
  frame 00 where its panel is still empty.
- F8 `eigen-inherit` frame 02 (B-m5): A's "1.00" printed as on frame 03.
- F9 `decomp-power` frame 00 (B-m4): the callout says what the numbers are ("circles: λk / λ1").
- F10 `katz-why` (C-m5, C-m6): callouts without "wall" (e.g. "1/α near λ₁: weight 5"); the stray piece of
  the curve on frame 02 clipped.
- F11 `pr-leak` (C-M3, C-m12): from frame 01 A, C, E pale (the answer's hot no longer means anything);
  "total 0.60" -> "sum of scores 0.60" (and 0.00).

## Not done, and why

- A-m2 (slide 3 sub names links the map does not draw): the next slide draws them; the sub sets it up.
- A-m3 (name all twelve cities): the names are in the notes; the figure was signed off.
- B-m2 ("letters" in the betweenness build): the lecturer's story since v1, defined by the sub.
- B-m6 (the 2.88 sum on `eig-pf`): it ties the definition back to the build two slides earlier.
- C-m3 (slide 97's take is the matrix form): the derivation's step; slide 98 asks about it.
- C-m10 (one word under each name in the genealogy): the notes carry it.
- C-m11 (shares on the PageRank question): the trap the answer build then resolves (amounts, 7/3 vs 3/11).

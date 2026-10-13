# R3 review, reviewer C: slides 57–82

I opened every PNG from 056 to 082 with Read. For each build in range I opened frames 00 and
the last frame, plus the middle frames: ring-local 00–05, walks-discount 00/01/03/04, katz-why
00–05 (as a stack), and pr-leak 00–04 (as a stack). Pixel checks were run on RGB composites:
- ring-local/00 = ring-4444: identical.
- Each build's last frame = its still: identical.
- slide 62 vs 63, right half: identical.
- pr-leak/00 vs pr-split-answer: different.

I also rendered `m06-centrality.html` with headless Chrome at slides 59, 64, 66 and 77. This shows
what the room sees when a slide opens: frame 00 and the scrub bar, which the PNG export does not
show.

Numbers were recomputed from `smallgraphs.py`, and `check()` passes:
- ring shares 25/68/85/91/94%;
- Katz quiz M 0.87 / X 0.81 and H 1.00 / K 0.81;
- dial shares 33/40/63/81% with λmax 5.084;
- u→v walks 0, 2, 1, 11;
- katz-why coefficients for α = 0, 0.5, 0.8, 0.95, 0.99 and 1.1 over λ1;
- PR split 3/11 and 1/11;
- leak totals 1, 0.8, 0.6, 0.13, 0;
- teleport 0.091/0.117/0.316/0.117/0.359;
- PPR 0.335/0.095/0.257/0.095/0.218;
- HITS hub A, authority E.

Every number drawn in range matches the bullets and the notes.

**Count:** Blockers 0 · Majors 5 · Minors 44 (one per bullet below)

---

## Majors

**M1 · slide 64 (walks-discount), frames 00–02.** The legend labels "= α²" and "= α³" are
drawn from frame 00, before the brush strokes they stand for. The headless render confirms what
the room sees for the first two bullets: the bare network with two orphan "= α²" / "= α³"
fragments floating at the right. In frames 01–02, "= α³" is still orphaned.
*Fix:* each legend entry appears in the same frame as its first walk. That is "→→ = α²" with
frame 01 and "→→→ = α³" with frame 03. Nothing is to the right of the graph in frame 00.

**M2 · slide 66 (Why 1/λmax?), presentation only.** In the presentation, the scrub bar is
appended below the figcaption and sits at y ≈ 650–672, past the 660 line (headless render). The
caption itself is at y ≈ 621, level with the page number. The PNG gate cannot see this because
the export has no bar.
*Fix:* drop the figcaption. Its content is already in the formula panel (1/(1 − αλk) is the
coefficient). If the caption must stay, move "circle = 1/(1 − αλₖ)" into the figure as a muted
tag at the left, under "=", so the bar rises by one line.

**M3 · slides 76 → 77 (pr-split-answer → pr-leak/00).** The spec says a build's frame 0 equals
the slide before it within a group, and PR is a group. Frame 00 differs from slide 76 in five
ways at once:
- the edge weights vanish;
- the scores vanish;
- every disc turns cool;
- the E→A link becomes dashed with a hot ×;
- "dead end" and "total 1.00" appear.

The render also shows the cut link before the first bullet, "E loses its only link out", is
revealed (`data-at="1"`).
*Fix:*
- Frame 00 = slide 76's picture with the values and weights removed (or exactly slide 76).
- Frame 01 = E→A turns dashed with the ×, and "dead end" appears.
- The following frames are the drain, with "total" first appearing at 1.00.
- Keep `data-at="1"`, so the bullet arrives and then the click cuts the link.

**M4 · slides 57 and 65 (the two live stages): not his figure style.** These are the only
figures in range with flat, vector-crisp discs in fully saturated sky blue:
- At step 0 (57) and at α = 0 (65), every disc is the saturated maximum: 7 discs on 57 and 18
  on 65. Saturation lands on everything, against "saturation only on what matters".
- The neighbouring figures of the same networks are hand-drawn with grain: eig-pf on 48 and
  ring-local on 59.
- The dial's ring is also a different drawing from ring-local's K = 6 frame. It is flatter
  (aspect ≈ 2.4 against 1.4). The notes then ask the room to connect it to "the previous
  slides' localization". FIXES_R1 asked for that geometry, and v3 changed ring-local's layout
  after it.

*Fix (CSS/JS only):*
- Fill with the paper→cool ramp, so equal scores read pale, not saturated: map the shade on a
  fixed 0..1 scale, or start the ramp at `pale`.
- Outline in `ink` at 2 px with a slight SVG turbulence filter for the pencil edge.
- Take katz-dial's node coordinates from ring-local frame 03, scaled to the stage.

**M5 · slide 59 (ring-local): each step re-lays out the clique.** From K = 4 to K = 5:
- the triangle-with-centre K4 becomes a pentagon;
- all four old nodes move;
- the two ring edges re-route.

Each later step re-draws the polygon again: hexagon, heptagon, octagon. The step is meant to add
one node, but the eye sees a new shape each time. Frame 00 → 01 also adds the shading and the
"K = 4: 25%" label together.
*Fix:* draw every K4 in ring-4444 as a square with both diagonals. Each step then turns the
right clique's square into a pentagon, hexagon and so on around a fixed centre, with the two port
nodes kept at fixed positions. This also makes the cliques read as cliques: the
triangle-with-centre drawing reads as a wheel. Optional: split frame 01 into shading first, then
the label.

---

## Minors

**57**
- The value labels of C and D are both below their nodes. D's "1.00" sits at the C–D edge's
  midpoint, nearer C than D. At step 1 (C 0.25, D 0.75), the numbers can be swapped by eye.
  *Fix:* put D's value below-right of D (D has no edge there).
- The side panel's note "x ← A x, then divide by the largest entry" wraps, and "entry" sits
  alone. Shorten to "x ← Ax, ÷ largest".

**58**
- Bullet 1 wraps with "ring." alone on the second line. Use "Four 4-cliques in a ring."
- The slide has no speaker notes. Add one line: "Ask: one clique of 5, three of 4. Who gets the
  score?"

**59**
- "K = 8: 94%" does not say what K is or what the 94% is a share of. *Fix:* label "K = 8:
  94% of the score", or define K in bullet 1: "Grow one clique to K nodes."
- The orange "25%" in frame 01 is not a point; the even split is the baseline. Ink for K = 4,
  hot from K = 5 on.

**60**
- No leader joins the small NYC box on the main map to the inset. Add a thin muted line from
  the box's top-right corner to the inset's lower-left corner.
- "Hempstead" is the underlined label, but neither the bullets nor the notes name it. Either
  say it in the notes ("the top node: Hempstead, Long Island") or drop the underline.

**61/62**
- The part title "Everyone gets a baseline" is followed by the slide title "Give everybody a
  baseline". *Fix:* rename slide 62 "Katz centrality", or make the part title "Katz centrality"
  with the subtitle "Everyone gets a baseline".

**62**
- Bullet 1 runs to three lines and repeats in words what bullet 2 says in symbols. *Fix:*
  "**Katz centrality**: a free β, plus α × neighbours."
- katz-floor draws the 7-node network taller than eig-pf (slide 48). Using the EIG group's
  coordinates would let the room recognise it.

**63**
- All three bullets of slide 62 disappear, so "that inverse" has nothing on screen to point
  at. *Fix:* keep $\mathbf{c} = \beta (I-\alpha A)^{-1}\mathbf{1}$ as line 1 and add "= ?"
  under it.

**64**
- Bullet 1's formula breaks mid-expression: "… + αA +" / "α²A² + ⋯". Shorten to
  $(I-\alpha A)^{-1} = \sum_k \alpha^k A^k$, or force a break before "=".
- Bullet 2 has no full stop, while the other bullets do.
- This is the u–v network from slides 8–9, but it is drawn in a different layout: compact and
  tall here, wide there. Its count line "2α² + α³ + 11α⁴" calls back to slide 9's "2, 1, 11".
  The same drawing would make the callback instant.
- The α³ walk is in hot, but it is not more "the point" than the α² walks. Use gold for one
  family (the deck's route colour) and cool for the other.

**65**
- The panel's lower third (y ≈ 410–485) is empty. Either shrink the panel or move the
  caption into it.

**66**
- Notation differs between the parts of the slide:
  - the figure says α = 1.1/λ₁;
  - the title, the formula panel and the dial on 65 say λmax;
  - the panel uses italic I, A, and the figure uses bold.

  *Fix:* write λmax in the figure labels ("α = 0.99/λmax").
- The slide does not say which network the coefficients belong to. It is the 7-node graph
  (λ₁ = 2.884), not the ring on the previous slide (λmax = 5.084). Add "7-node network" as a
  muted tag, or say it in the notes.

**67–70**
- "Katz centrality, α = 0.5/λmax." wraps after "α =". Shorten to "Katz, α = 0.5/λmax."
- "The same network." refers to slides 49–52, eighteen slides back. *Fix:* "The network from
  the eigenvector quiz."
- In the answer, line 2 is replaced instead of a line being added (the spec says "A adds one
  line"). *Fix:* keep "The same network." and add the answer line under it.
- 68: X's "0.81" sits above the M–X edge and close to the X–p edge. Move it directly above X,
  or to its right.
- 70 against 52: H's and K's values are placed differently from the eigenvector answer. On 52,
  H's value is above-right and K's is to the left; on 70, H's is below-right and K's is
  above-left. The point of 70 is the flip, so place the values at the same spots as on 52.
- Origin out of range, noted for the owner of 49–50: in q-eig-L the lettered node drawn at the
  picture's centre (M) wins. The Katz-L question on 67 inherits this. This is acceptable
  because the trick is "X has more neighbours". Say so in the notes, or shift X towards the
  centre.

**71 / 81 (grid)**
- "eigenvector" runs edge to edge in its cell (x 541–737 in a 536–744 box), and "paths
  passing" nearly does too. Drop the font by 2 pt in the grid, or widen those two cells.
- The axis header "which routes count" and the row label "shortest paths" have the same colour
  and size, so they read as one phrase. Make the row labels ink.
- 81: the order is PageRank then HITS, but the lecture teaches HITS (73) before PageRank (75).
  Swap the two cells.
- Rows 1 and 2 have different column widths, so "how they become one number" heads no column.
  This was carried over from v2 and is out of scope unless the lecturer wants it.

**73**
- "Authority" is underlined in hot, but the authority E is cool in the figure. *Fix:*
  underline "Authority" in cool.
- The caption explains the arrows but not $A_{ij}$, which the bullets use. *Fix:* replace it
  with "$A_{ij}=1$: page i links to page j".

**74**
- The banner "a node's score is built from its neighbours' scores" is a sentence inside a
  figure. Move it to the slide as one line above the figure, or keep it and accept it.
- All six dots are saturated cool, though none is the point. Use ink outlines with a pale
  fill.
- "Brin & Page" appears before PageRank is taught (75–78). The genealogy's position was
  declined in R2, so just note it in the speaker notes.
- The slide has no speaker notes. Add one line per name, saying what each built.

**75**
- Bullet 3 runs to three lines. Shorten to "C: three links in. E: one. Which ranks higher?"

**76**
- B and D are tinted cool, though they score lowest. Use plain white.
- A's "3/11" sits just under the A→D "1/3" weight, which makes a stack of two fractions. Move
  A's value to the left of A.

**78**
- The formula omits the dead-end term. Taken literally, it gives c_A = r/N = 0.03 and a total
  of 0.33. The figure's 0.091 and "total 1.00" match only after rescaling, which is equivalent
  to sending the dead end's score to every page. *Fix:* change bullet 2 to "A dead end links to
  every page." Then $d^{out}_E = N$ and the formula holds as written.
- The jump itself is never drawn, and so the diff from 77 (and to 79) is large. *Fix:* draw E's
  jumps as dotted cool arrows from E to every page. On 79 these then collapse onto A: a
  one-thing diff.

**79**
- The dashed grey E→A loop means "the removed link" on 77 (with the ×) and "jump back to A"
  on 79. *Fix:* draw jumps in their own style (dotted cool, as above).

**80**
- The "eigenvector" label starts on top of the Hudson-valley roads and dots. Move it right or
  up, into the white band left of the inset.
- The closeness and betweenness discs touch each other; the leaders separate them, but only
  just. Shrink the winner discs a little, or offset the leaders so they leave the discs on
  opposite sides.

**82**
- The take-home quiz covers only day-1 measures (degree, closeness, eccentricity,
  betweenness), but it closes day 2. Consider adding "and eigenvector centrality", or say in
  the notes that this is deliberate.

---

## Checked, no issue
- 56 → 57: a new picture, so no diff rule applies.
- 58 → 59: ring-local/00 is pixel-identical to ring-4444, at the same position on the slide
  (confirmed in the presentation render).
- 62 → 63: the figure is identical, and only the text changes.
- Q/A pairs 67/68 and 69/70: the same crop, and A = Q plus marks and values.
- 71 → 81: the grid never moves.
- 60 and 80 share the NY canvas and the inset.
- 75 → 76: the same crop.
- In every slide in range, content ends above y = 660 in the PNGs. The only exception is the
  presentation-only scrub bar on 66 (M2).
- No question slide shows its answer. Slide 69's trick (the hub H wins under Katz after
  losing under the eigenvector) is deliberate and is spelled out in 70's notes.

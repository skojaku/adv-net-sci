# m06 round 4: builds become slides, and every step says what changed

The lecturer (2026-10-13): the slider is hard to talk over. He explains the bullets first,
then steps the build, so each step becomes its own slide (same title, same bullets, the next
frame). Not everything needs a build (the Roman map does not). When a path is shown, annotate
it. On every step, a light-grey note with a thin arrow points at what changed and says it.

## Rules for every build

- **Few steps.** Only the steps listed below; each step changes ONE thing.
- **A callout on every step after frame 00:** `F.callout(text, at, target, ...)` (figlib, new):
  muted text of at most ~5 words, a thin muted arrow to the thing that changed. Frame 00 has no
  callout (it equals the previous slide).
- **Reserve the callout room on the group's canvas** (a band above or beside the drawing), so
  every frame and every figure of the group keeps one canvas and one box, and frame 00 stays
  pixel-identical to the slide before it.
- **Every brushed path or walk gets a callout naming it** ("u → v: 2 steps", "s–A–C–t").
- Callouts must not touch discs, edges, values or each other (use the returned box as a blocker).
- `emit_frames` as before: `figures/frames/<name>/00.png …` and `figures/<name>.png` (the last
  frame). The deck will show each frame as its own slide, so the frame count below is final.
- Numbers come from `smallgraphs.py`; assert what a callout states.

## Agent B — `figs_defs.py`, `figs_small.py` (sigma-answer)

**w5-walks** (5 frames). 00 = w5-blank. 01 hot brush on the shortest u→v path; callout
"shortest path: 2 steps". 02 gold brushes on the two walks of length 2; callout "length 2:
2 walks". 03 the one walk of length 3 (cool); callout "length 3: 1 walk". 04 one length-4 walk
that revisits a node (cool), callout "length 4: 11 walks; this one revisits x" (name the node).

**closeness-def** (6 frames). 00 bare bowtie. 01 the distances from A beside every node
(1, 1, 2, 3, 4, 4); callout "distances from A" → A. 02 those cleared, A's sum "15"; callout
"1+1+2+3+4+4 = 15" → the 15. 03 every node's sum; callout "every node's sum" → D's 10 (all
ink). 04 A's 15 becomes "0.40"; callout "6/15 = 0.40" → it. 05 every sum becomes its
closeness, D hot with 0.60 underlined; callout "highest: D" → D.

**bowtie-closeness** = frame 05 WITHOUT its callout (the fire-station slide).

**ecc-def** (4 frames). 00 = bowtie-closeness. 01 closeness values cleared; A's farthest node
by a gold brush along A→…→F (or G) with "4" at A; callout "A's farthest: 4 steps" → the brush.
02 every node's eccentricity (4 4 3 2 3 4 4); callout "every node's worst case". 03 D hot with
"2" underlined; callout "smallest: D".

**btw-def** (5 frames). 00 bare bowtie. 01 the letter A→F as a gold brush through C, D, E, and
"1" on C, D, E; callout "A to F passes C, D, E" → the brush. 02 every letter from A counted
(the counts on C, D, E); callout "all of A's letters". 03 every pair counted (C 8, D 9, E 8,
ends 0); callout "every pair". 04 D hot with 9 underlined; callout "D carries the most".

**sigma-answer** (static): callouts naming the two paths, "s–A–C–t" and "s–B–C–t", each
pointing at its brush.

## Agent Q — `figs_quiz.py` (harmonic-def, on the CA group canvas)

**harmonic-def** (6 frames). 00 = cut-blank. 01 "1/1" on G's neighbours F, H, I, J; callout
"G's neighbours: 1/1 each". 02 "1/2" on K; callout "K: 2 steps, 1/2" → K. 03 "0" on A–E;
callout "unreachable: 1/∞ = 0" → the E side. 04 contributions cleared, G's "9/2"; callout
"4 + 1/2 = 9/2" → it. 05 every node's score, G hot underlined; callout "highest: G".
The CA group's canvas must hold the callouts on every figure of the group (q-close-CA,
cut-blank etc. keep the band empty).

## Agent E — `figs_eigen.py`

**eigen-inherit** (4 frames). 00 the graph, scores hidden, A outlined hot. 01 B, D, F, G show
their scores, gold brushes into A; callout "A's neighbours: B, D, F, G". 02 the sum line
"0.64 + 0.58 + 0.81 + 0.85 = 2.88 × 1.00"; callout "their sum = 2.88 × A's score" → the line.
03 every score (the final picture; = eig-pf), callout "true at every node: λ = 2.88".
eig-pf = frame 03 without its callout.

**ring-local** (5 frames). 00 = ring-4444. 01 K = 4 shading and "K = 4: 25% of the score";
callout "equal cliques, equal shares". 02 K = 5; callout "one more node" → the new node.
03 K = 6; callout "+1" → the new node. 04 K = 8; callout "+2: 94%" → the clique.

**walks-discount** (4 frames). 00 = w5-blank layout. 01 the two length-2 walks (gold) and
"= α²"; callout "2 walks of length 2, α² each". 02 the length-3 walk (cool) and "= α³";
callout "1 walk of length 3: α³". 03 the sum line; callout "every length, discounted".

**katz-floor** (static): callout on the hot brushes, "α × each neighbour's score".

## Agent F — `figs_decomp.py`, `figs_dir.py`

**decomp-sum**: static (the final picture). Drop its frames from use.

**decomp-square** (2 frames). 00 the product A·A with one cross term marked (hot outline) and
callout "u₁ᵀu₂ = 0: cross terms vanish". 01 the result A² = Σ λₖ² uₖuₖᵀ; callout
"each eigenvalue squared" → the first circle.

**decomp-power** (4 frames): t = 1, 2, 4, 16. Callouts: "t = 1: every term", "t = 2: the
negative term turns positive", "t = 4: the small terms fade", "t = 16: only the first is left".

**katz-why** (3 frames): α = 0.5, 0.95, 1.1 × 1/λmax. Callouts: "small α: weights comparable",
"α near 1/λmax: the first term dominates", "past 1/λmax: the first weight is negative" → its
circle.

**pr-leak** (4 frames). 00 = pr-split-answer. 01 weights and scores cleared, E's link dashed
with the hot ×, "dead end"; callout "E's only link out is gone" → the ×. 02 total 0.60;
callout "score leaks out at E" → E. 03 total 0.00; callout "nothing left".

**pr-teleport / ppr** (static): callouts naming the jumps, "E jumps to every page" and
"every jump lands on A".

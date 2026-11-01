---
marp: true
theme: house
paginate: true
math: katex
html: true
---

<script src="scrub.js"></script>
<script>window.animStepOnly = true;</script>

<style>
section .optflag { position: absolute; top: 18px; right: 28px; font-size: 18px; color: #fff; background: #3959A6; padding: 2px 12px; border-radius: 4px; z-index: 9; }
</style>

<!-- Lecture plan and timing: review/DECK_SPEC.md. Figures: figures/*.png, built by figures/figs_a.py, figs_b.py, figs_c.py (BRIEF.md). -->

<!-- _class: lead -->
<!-- _footer: "" -->

# Random Walks

<div class="eyebrow">Advanced Topics in Network Science · Module 07</div>

<div class="credit">Sadamori Kojaku · Binghamton University</div>
<!--
[#1] beat: title
About 90 minutes. The Pen & Paper sheet is worked in two blocks: Part 1 right after slide 6 (before any maths, so the room finds the facts first), Parts 2 and 3 after the maths. 1 minute per content slide; builds take seconds.
-->

---

<!-- _class: L-c -->
<!-- _footer: "" -->

## Where is the walker after 100 steps?

<div class="cols">
<div>

A man walks **1 yard**, turns in a random direction, and walks **1 yard** again. He repeats this 100 times.

Pearson asked this in *Nature* in 1905.

</div>
<div class="fig">

![w:537](figures/pearson-walker.png)

</div>
</div>

<div class="cue">

Far from the start, or near it? Tell your neighbour.

</div>
<!--
[#2] beat: hook (story): Pearson's question, 1905
source: K. Pearson, The Problem of the Random Walk, Nature 72, 294 (1905), doi:10.1038/072294b0. Check the wording against the original before quoting it.
Open with the history. In July 1905 the statistician Karl Pearson asked the readers of Nature: a man walks l yards, turns through any angle, walks l yards again, n times; where is he? The problem came from a question about how far mosquitoes spread (Pearson corresponded with Ronald Ross about malaria). A question slide: it never shows the answer.
-->

---

<!-- _class: L-g -->
<!-- _footer: "" -->

<div class="fig">

![w:1080](figures/pearson-answer.png)

</div>

<div class="take">

Rayleigh replied the next week: he had solved it in 1880, for <span class="hot">waves</span>

</div>

<!--
[#3] beat: answer: Pearson's walker (the density peaks at the start)
source: J. W. Strutt (Lord Rayleigh), Nature 72, 318 (1905); K. Pearson, Nature 72, 342 (1905). Figure: simulation, seed fixed in figures/figs_a.py.
Pearson's own remark, as quoted in secondary sources (verify in the original): the most probable place to find a drunken man who is at all capable of keeping on his feet is somewhere near his starting point. Careful: per unit area the density is highest at the start, yet the typical distance grows like the square root of n (about 10 yards after 100 steps; the grey ring). A short walk remembers where it began; a long one spreads out. Rayleigh had met the same mathematics in 1880, adding n waves of random phase.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## Random walks appear in many fields

<div class="fig">

![w:1080](figures/fields.png)

</div>

<!--
[#4] beat: hook: the same walk in three fields
source: Pollen: Brown 1827, Einstein 1905, Perrin (Les atomes, 1913). PageRank: Page, Brin, Motwani, Winograd (1998). Check each year before the slide is final.
One idea, many fields. Verify the dates before the lecture: Brown 1827 (pollen); Einstein 1905 (the explanation); Perrin (the measurement that settled it); Page and Brin 1998. The arrow is the question for the next slide.
-->

---

<!-- _class: L-f -->
<!-- _footer: "" -->

## How does it tell us about a <span class="hot">network</span>?

<div class="sub muted">

But it is a “random” walk, right?

</div>

<!--
[#5] beat: spine 1: the question
The objection first: a random walk looks like noise. The answer of the whole lecture: the walker is a measuring instrument. It has no map, no destination and no memory, so what it does depends only on the network.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## What is a <span class="hot">random walk</span>?

<div class="fig">

![w:1080](figures/walk-rule.png)

</div>

<!--
[#6] beat: mechanism: the rule
source: lecture-note/m07 fig-m07-net (redrawn in house style)
The only rule: divide the chance evenly among the edges. Four edges: 1/4 each. No memory of where it came from. This picture returns when P is introduced.
-->

---

<!-- _class: L-f -->
<!-- _footer: "" -->

## Pen & Paper

<div class="sub">

10 minutes · stop at the line on the sheet

</div>

<!--
[#7] beat: Pen & Paper: first block
Hand out the sheet. Part 1 is done now, before the lecture names anything. Students open the simulator (next slide), sketch how the visits correlate with degree over time, run 20,000 steps, read the most and the least visited node, compute degree ÷ share for both, and compute the one-step and three-step probabilities on the small drawn network. The sheet has a printed line: STOP, wait for the lecture. Walk around the room.
-->

---

<!-- _class: L-c -->
<!-- _footer: "" -->

<div class="cols">
<div>

### Random walk simulator

<code>skojaku.github.io/<br>adv-net-sci/assets/vis/<br>random-walks/index.html</code>

</div>
<div class="fig">

![w:440](figures/qr-sim.png)

</div>
</div>
<!--
[#8] beat: the simulator (QR code and link)
The simulator is last term's tool, unchanged (lecture-note/assets/vis/random-walks/index.html). Default network: the karate club. ?dataFile=two-cliques.json loads two 5-cliques joined by one edge. No short link yet (go.skojaku.com/m07sim is not created): the QR code points at the full address.
-->

---

<!-- _class: L-c -->
<!-- _footer: "" -->

## Two communities joined by one edge

<div class="cols">
<div>

**How many steps**, on average, until the walker crosses to the other community?

A: about 3

B: about 20

C: about 200

</div>
<div class="fig">

![w:537](figures/two-comm-q.png)

</div>
</div>

<div class="cue">

Take a guess.

</div>
<!--
[#9] beat: question to the room (Q2)
A question slide: it never shows the answer. Answer B. A walker in community 1 uses the bridge with chance 1/21 per step; it stays about 21 steps (k/2m: the bridge is used with probability 1/42 per step overall, and the walker is in community 1 half of the time). The students can check with the simulator: ?dataFile=two-cliques.json.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

<div class="optflag">OPTIONAL</div>

## A short walk stays in its <span class="hot">community</span>

<div class="fig">

![w:1080](figures/two-comm-walk.png)

</div>

<!--
[#10] beat: answer to Q2
Short walks remember the community they started in. Long runs of one colour: about 21 steps each. This is the community signal we find in the second eigenvector.
-->

---

<!-- _class: L-f -->
<!-- _footer: "" -->

## Short walks show <span class="hot">communities</span>. Long walks show <span class="hot">degree</span>. Why?

<!--
[#11] beat: spine 2: the mystery
The maths answers exactly this. First, what the sheet found about degree.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## Degree ÷ share is <span class="hot">constant</span>

<div class="sub">

Karate club: 34 nodes, 78 edges, so 2m = 156

</div>

<div class="fig">

![w:1080](figures/degree-share.png)

</div>

<div class="take">

Share of time = degree ÷ <span class="hot">2m</span>

</div>

<!--
[#12] beat: debrief Part 1 (degree ÷ share)
The students' ratios scatter (node 11 is noisy: the ratio is a law of large numbers, not an identity of one run). The most visited node is 33 in about 3 runs out of 4 and node 0 otherwise; both give 156.
-->

---

<!-- _class: L-f -->
<!-- _footer: "" -->

## Why does a long walk not depend on the <span class="hot">start</span>?

<!--
[#13] beat: spine 3: part question
From here: the maths, as pictures of vectors and matrices drawn as in the centrality lecture (circle = eigenvalue, tall bar = vector).
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## The walk is defined by <span class="hot">one matrix</span>

<div class="fig">

![w:1080](figures/P-def.png)

</div>

<!--
[#14] beat: P (the two-community network, the motif of the rest of the lecture)
source: figures/smallgraphs.py (the same 12-node network as Part 3 of the sheet)
Introduce the 12-node two-community network that runs to the end and that the sheet uses in Part 3. Row i of P is the odds of leaving node i; rows sum to 1. Do not show the eigenvector yet. Convention: row vectors, as in the lecture note (P_ij = A_ij / k_i, x(t+1) = x(t) P).
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## One step is a <span class="hot">multiplication</span> by $P$

<div class="sub">

$x(t+1) = x(t)\,P$

</div>

<div class="fig">

![w:1080](figures/xP-1.png)

</div>

<div class="take">

$x = (1, 0, 0, \dots)$: $xP$ is the row of node 0

</div>

<!--
[#15] beat: x P, how to read it (1/3)
Build 1/3. x = e_0: the walker's distribution is a wide bar (a row vector); one step is the wide bar times the square P. A walker certain to be at node 0 moves to the row of node 0 of P; with a mix, the new distribution is the mix of the rows. The same canvas on all three.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## One step is a <span class="hot">multiplication</span> by $P$

<div class="sub">

$x(t+1) = x(t)\,P$

</div>

<div class="fig">

![w:1080](figures/xP-2.png)

</div>

<div class="take">

$x = (0, 1, 0, \dots)$: $xP$ is the row of node 1

</div>

<!--
[#16] beat: x P, how to read it (2/3)
Build 2/3. x = e_1: the walker's distribution is a wide bar (a row vector); one step is the wide bar times the square P. A walker certain to be at node 0 moves to the row of node 0 of P; with a mix, the new distribution is the mix of the rows. The same canvas on all three.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## One step is a <span class="hot">multiplication</span> by $P$

<div class="sub">

$x(t+1) = x(t)\,P$

</div>

<div class="fig">

![w:1080](figures/xP-3.png)

</div>

<div class="take">

$x = (0.5, 0.05, \dots)$: $xP$ is a mix of the rows

</div>

<!--
[#17] beat: x P, how to read it (3/3)
Build 3/3. x = a mix: the walker's distribution is a wide bar (a row vector); one step is the wide bar times the square P. A walker certain to be at node 0 moves to the row of node 0 of P; with a mix, the new distribution is the mix of the rows. The same canvas on all three.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## After $t$ steps

<div class="sub">

$x(t) = x(0)\,P^{t}$

</div>

<div class="fig">

![w:1080](figures/xPt.png)

</div>

<!--
[#18] beat: x(0) P^t
t steps are t multiplications by the same matrix. The next slides show P^t itself.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## Rows of $P^t$ <span class="hot">after t steps</span>

<div class="fig scrub">

![w:1080](figures/Pt-slider.png)

</div>

<!--
[#19] beat: P^t as a heat map (slider)
Use the slider under the figure (or the arrow keys): t from 1 to 40. t = 1: the two dense blocks, the walker stays in its community. t = 5: the blocks blur, the walker starts to leak. t = 40: every row is the same. The PNG export shows the last frame.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## Rows of $P^t$ at $t = 40$

<div class="fig">

![w:1080](figures/Pt-40.png)

</div>

<div class="take">

Every row becomes the same: <span class="hot">π</span>

</div>

<!--
[#20] beat: P^t, the numbers at t = 40
The same drawing as the slider's last frame, now with the numbers. Each row is where a walker starting at that node is after 40 steps; all twelve rows agree to two decimals. At t = 40 the worst start is about 0.01 from pi in the 1-norm.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## What each entry of $P^t$ says

<div class="fig">

![w:1080](figures/Pt-zoom.png)

</div>

<!--
[#21] beat: zoom into P^t
Zoom in on one corner of P^5. Row = where the walker starts; column = where it is; the entry is the probability of being there after 5 steps.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## Recall: eigendecomposition

<div class="fig">

![w:1080](figures/m06-decomp-sum.png)

</div>
<!--
[#22] beat: recap: eigendecomposition (M06, light touch)
source: slides/m06/figures/decomp-sum.png (reused unchanged)
Two sentences only: circle = eigenvalue, tall bar = eigenvector, wide bar = its transpose. Do not re-derive; the room saw this for the adjacency matrix.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## $P$ has an eigendecomposition too

<div class="sub">

$P = \sum_k \lambda_k\,\phi_k\,\psi_k^{\top}$

</div>

<div class="fig">

![w:1080](figures/P-decomp.png)

</div>

<div class="take">

$P^t$ changes only the <span class="hot">eigenvalues</span>

</div>

<!--
[#23] beat: P as a sum of circles and bars
The bars multiply to 1 or 0 as in M06, so P^t = sum of lambda_k^t phi_k psi_k^T. For P the tall bar (right eigenvector) and the wide bar (left eigenvector) are two different vectors: each is the other rescaled by degree. Say it once; the appendix of the note has it.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## The eigenvalues <span class="hot">shrink</span> as $t$ grows

<div class="fig">

![w:1080](figures/Pt-circles-1.png)

</div>

<!--
[#24] beat: P^t as circles (1/3)
Build 1/3, t = 1: one step. Eigenvalues of the 12-node network (computed): 1, 0.889, 0, 0, 0, -0.088, -0.2, -0.2, -0.266, -0.333, -0.379, -0.423.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## The eigenvalues <span class="hot">shrink</span> as $t$ grows

<div class="fig">

![w:1080](figures/Pt-circles-2.png)

</div>

<!--
[#25] beat: P^t as circles (2/3)
Build 2/3, t = 5: $\lambda_2^5 = 0.56$. Eigenvalues of the 12-node network (computed): 1, 0.889, 0, 0, 0, -0.088, -0.2, -0.2, -0.266, -0.333, -0.379, -0.423.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## The eigenvalues <span class="hot">shrink</span> as $t$ grows

<div class="fig">

![w:1080](figures/Pt-circles-3.png)

</div>

<!--
[#26] beat: P^t as circles (3/3)
Build 3/3, t = 40: only the circle at 1 is left. Eigenvalues of the 12-node network (computed): 1, 0.889, 0, 0, 0, -0.088, -0.2, -0.2, -0.266, -0.333, -0.379, -0.423.
-->

---

<!-- _class: L-c -->
<!-- _footer: "" -->

## Which term stays the longest?

<div class="cols">
<div>

The 12 eigenvalues of $P$.

After many steps, which term is still there?

</div>
<div class="fig">

![w:537](figures/lam-curves-q.png)

</div>
</div>

<div class="cue">

Take 20 seconds.

</div>
<!--
[#27] beat: Q3 (which term stays the longest)
Each curve is |lambda_k|^t. The first (1) never decays. The question is about the last of those that die. Be explicit after the answer.
-->

---

<!-- _class: L-c -->
<!-- _footer: "" -->

## The <span class="hot">second</span> term stays the longest

<div class="cols">
<div>

$\lambda_2 = 0.89$

$0.89^{t}$: 0.56 at $t = 5$, 0.31 at $t = 10$, 0.01 at $t = 40$

</div>
<div class="fig">

![w:537](figures/lam-curves-a.png)

</div>
</div>
<!--
[#28] beat: A3
Same figure as the question, with the answer added.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## <span class="hot">Mixing time</span>

<div class="fig">

![w:1080](figures/mix-1.png)

</div>

<!--
[#29] beat: mixing time (1/3)
Build 1/3: where you start matters at first; later the second term dominates. One thin line per starting node, a black line for the worst start; epsilon = 0.25 gives t = 13 on this network. The formula appears only at the end, after the diagram has said it.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## <span class="hot">Mixing time</span>

<div class="fig">

![w:1080](figures/mix-2.png)

</div>

<!--
[#30] beat: mixing time (2/3)
Build 2/3: how close is close enough?. One thin line per starting node, a black line for the worst start; epsilon = 0.25 gives t = 13 on this network. The formula appears only at the end, after the diagram has said it.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## <span class="hot">Mixing time</span>

<div class="sub">

$t_{\mathrm{mix}} = \min\{\,t : \max_{x(0)} \|x(t) - \pi\|_1 \le \epsilon\,\}$

</div>

<div class="fig">

![w:1080](figures/mix-3.png)

</div>

<!--
[#31] beat: mixing time (3/3)
Build 3/3: the mixing time: the first t at which every start is within the threshold. One thin line per starting node, a black line for the worst start; epsilon = 0.25 gives t = 13 on this network. The formula appears only at the end, after the diagram has said it.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

<div class="optflag">OPTIONAL</div>

## Q: mixing time of a 10-clique?

<div class="sub">

10 nodes, every pair connected (45 edges)

</div>

<div class="fig">

![w:1080](figures/clique-q.png)

</div>

<div class="cue">

Take a guess: 1 step, 5 steps, 50 steps.

</div>

<!--
[#32] beat: Q4 (clique)
One graph per question. Answer: 1 step. lambda_2 = -1/9; the relaxation time is about 0.9 steps.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

<div class="optflag">OPTIONAL</div>

## A: about 1 step

<div class="sub">

10 nodes, every pair connected (45 edges)

</div>

<div class="fig">

![w:1080](figures/clique-a.png)

</div>

<div class="take">

$\lambda_2 = -1/9$: mixing takes <span class="hot">about 1 step</span>

</div>

<!--
[#33] beat: A4
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## Q: mixing time with one bridge?

<div class="sub">

Two 5-cliques joined by one edge (21 edges)

</div>

<div class="fig">

![w:1080](figures/twoclique-q.png)

</div>

<div class="cue">

The same, 5 times longer, or 20 times longer?

</div>

<!--
[#34] beat: Q5 (two cliques)
The graph has fewer edges than the clique, and mixing takes 20 times longer. What matters is the bottleneck.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## A: about 20 times longer

<div class="sub">

Two 5-cliques joined by one edge (21 edges)

</div>

<div class="fig">

![w:1080](figures/twoclique-a.png)

</div>

<div class="take">

$\lambda_2 = 0.93$: mixing takes about <span class="hot">20 steps</span>

</div>

<!--
[#35] beat: A5
At epsilon = 0.25: 1 step for the clique, 20 for the bridged cliques. The relaxation time tau = 1/(1 - 0.927) = 13.8 against 0.9.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## The <span class="hot">mixing time</span> follows from $\lambda_2$

<div class="sub">

$\tau = \dfrac{1}{1-\lambda_2}$

</div>

<div class="fig">

![w:1080](figures/gap-gauge.png)

</div>

<div class="take">

Small gap, <span class="hot">long mixing time</span>

</div>

<!--
[#36] beat: spectral gap (gauge)
'Spectral gap' = 1 - lambda_2. The mixing time is a few tau: the logarithm in the lecture note's bound pays for epsilon and the rarest node. Not derived here.
-->

---

<!-- _class: L-f -->
<!-- _footer: "" -->

## One eigenvalue is always <span class="hot">1</span>. Others diminish.

<!--
[#37] beat: spine 4: the fact
Taught as a fact. The next three slides give a reason, in pictures, not a proof.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## Why 1? Every row of $P$ sums to <span class="hot">1</span>

<div class="fig">

![w:1080](figures/P1-eq-1.png)

</div>

<!--
[#38] beat: lambda = 1 exists (P 1 = 1)
P times the vector of ones is the vector of ones, because each row of P is a list of odds that adds to 1. A vector that P does not change. (The walker's own stationary distribution is the matching LEFT eigenvector; the next slides.)
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## No eigenvalue is <span class="hot">larger</span> than 1

<div class="fig">

![w:1080](figures/no-larger.png)

</div>

<!--
[#39] beat: no eigenvalue above 1
P f replaces each entry by the average of the neighbours' entries. An average cannot exceed the largest entry, so |lambda| <= 1.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## Detailed balance condition

<div class="sub">

$\pi_i\,P_{ij} = \pi_j\,P_{ji}$

</div>

<div class="fig">

![w:1080](figures/detailed-balance.png)

</div>

<div class="take">

$\pi_i = k_i / 2m$: proportional to <span class="hot">degree</span>

</div>

<!--
[#40] beat: the eigenvalue 1 gives pi (ties to the simulator's ticks)
If walkers are spread as pi, the flow along an edge is the same in both directions: pi_i / k_i = pi_j / k_j, so pi is proportional to the degree. This is why the bars of the simulator settled on their k/2m ticks and why degree ÷ share = 2m on the sheet.
-->

---

<!-- _class: L-f -->
<!-- _footer: "" -->

## Pen & Paper

<div class="sub">

20 minutes

</div>

<!--
[#41] beat: Pen & Paper: second block
Everyone has finished Part 1 and crossed the line on the sheet. Parts 2 and 3 follow.
-->

---

<!-- _class: L-c -->
<!-- _footer: "" -->

## Tasks

<div class="cols">
<div>

2. Four nodes: write $x(t)$ with the eigenvalues, check $t = 2$

3. Twelve nodes: run one cell, plot the second eigenvector

</div>
<div class="fig">

![w:537](figures/tasks-diamond.png)

</div>
</div>
<!--
[#42] beat: Pen & Paper: instructions
Part 2 can be done with a pencil only; Part 3 needs a laptop or a phone (the QR code on the slide is a placeholder until the notebook is published). Pair students if there are not enough devices.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## $x(t)$ = π + <span class="hot">decaying</span> terms

<div class="sub">

Four nodes; eigenvalues $1,\ 0,\ -\tfrac13,\ -\tfrac23$

</div>

<div class="fig">

![w:1080](figures/diamond-expansion.png)

</div>

<!--
[#43] beat: debrief Part 2
x(0) = (1, 0, 0, 0) = pi - 0.5 psi_2 + 0.3 psi_4. x(1) = (0, 0, 0.5, 0.5), x(2) = (1/3, 1/3, 1/6, 1/6). The eigenvalue -2/3 alternates the sign: the walker hops between {0, 1} and {2, 3}, then settles. The eigenpairs are on the sheet; the students do not compute them.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## What is the decaying term?

<div class="fig">

![w:1080](figures/eigvec2.png)

</div>

<!--
[#44] beat: debrief Part 3 (second eigenvector)
source: numpy, the sheet's one-cell code
The cell computes np.linalg.eig(P), orders by the real part, and plots column 1. The sign gives the community; the sign itself is arbitrary, so the two communities may swap colours on a student's screen.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## Early on, the <span class="hot">community</span> signal dominates

<div class="sub">

Walker starts at node 0

</div>

<div class="fig">

![w:1080](figures/comm-curve.png)

</div>

<div class="take">

The community signal decays like $\lambda_2^{\,t}$. Degree remains.

</div>

<!--
[#45] beat: debrief Part 3 (what dominates early)
After about three steps only two terms are left: the one with eigenvalue 1 (degree) and the one at 0.89 (the communities). The second decays on the scale tau = 9. The bookend: short walks see communities, long walks see degree.
-->

---

<!-- _class: L-g -->
<!-- _footer: "" -->

<div class="fig">

![w:1080](figures/summary.png)

</div>

<!--
[#46] beat: summary (claims with thumbnails)
Three claims, each pointing back at the picture that showed it. Next lecture: how long a walker takes to reach a node (hitting time), PageRank and Walktrap.
-->

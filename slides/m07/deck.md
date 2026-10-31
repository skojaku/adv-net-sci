---
marp: true
theme: house
paginate: true
math: katex
html: true
---

<!-- WIREFRAME v1 (M07 random walks). Dashed boxes = figures to be made; the text in each box says what goes there.
     Slide list and timing: review/DECK_SPEC.md. -->

<style>
section .ph { box-sizing: border-box; border: 3px dashed #6B6B6B; background: #EEEEEE; color: #6B6B6B;
  display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
  font-size: 23px; line-height: 1.35; padding: 14px 22px; width: 100%; border-radius: 6px; position: relative; flex: 1; }
section .ph::before { content: "FIGURE"; position: absolute; top: 8px; left: 12px; font-size: 14px; letter-spacing: .08em; color: #B14434; }
section .ph.live::before { content: "LIVE TOOL"; color: #3959A6; }
section .optflag { position: absolute; top: 18px; right: 28px; font-size: 18px; color: #fff; background: #3959A6; padding: 2px 12px; border-radius: 4px; z-index: 9; }
section .buildflag { position: absolute; top: 18px; left: 28px; font-size: 18px; color: #6B6B6B; border: 2px solid #6B6B6B; padding: 2px 12px; border-radius: 4px; z-index: 9; }
section .fig > .ph { margin: 0 auto; }
section .katex-display { font-size: 1.6em; margin: 0.3em 0; }
section.L-b .fig img { max-height: 560px; max-width: 1230px; }
section.L-g .fig img { max-height: 640px; max-width: 1230px; }
section.L-a .fig img { max-height: 470px; max-width: 1200px; }
section.L-c .cols .fig .ph { height: 380px; flex: none; }
</style>

<!-- _class: lead -->
<!-- _footer: "" -->

# Random Walks

<p class="sub">Module 7 · Advanced Network Science<br>Sadamori Kojaku</p>

<p class="ref">(school logo, bottom left, as in the CCS deck)</p>
<!--
[#1] beat: title
Lecture plan: about 90 minutes. Say the budget here: 1 minute per content slide, builds take seconds. The Pen & Paper sheet is worked in two blocks (Part 1 before the maths, Parts 2-3 after).
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
<div class="ph">The first lines of Karl Pearson's letter to Nature, 27 July 1905 (facsimile or a re-typeset quotation, with credit). Under it: a pub, a lamp post, no answer yet</div>
</div>
</div>

<div class="cue">Far from the start, or near it? Tell your neighbour.</div>
<!--
[#2] beat: hook (story): Pearson's question, 1905
source: K. Pearson, The Problem of the Random Walk, Nature 72, 294 (1905), doi:10.1038/072294b0. Check the exact wording against the original before quoting.
Open with the history. In July 1905 the statistician Karl Pearson asked the readers of Nature: a man walks l yards, turns through any angle, walks l yards again, n times; where is he? The problem came from a biological question about how far mosquitoes spread (Pearson corresponded with Ronald Ross about malaria). Question slide: never shows the answer.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## Most likely near the start

<div class="fig">
<div style="display:flex;width:100%;height:360px"><div class="ph">LEFT: the paths of 5 walkers of 100 steps from the same lamp post (hand-drawn paths in pale colours, the pub in the middle). RIGHT: the end points of 10,000 walkers as a cloud of points centred on the pub; a grey ring at distance about 10 yards with the call-out 'typical distance after 100 steps'.</div></div>
</div>


<div class="take">

Rayleigh replied the next week: he had solved it in 1880, for <span class="hot">waves</span>

</div>

<!--
[#3] beat: answer: Pearson's walker (the density peaks at the start)
source: J. W. Strutt (Lord Rayleigh), Nature 72, 318 (1905); K. Pearson, Nature 72, 342 (1905). Figure: simulation, seed fixed in the figure script.
figure: LEFT: the paths of 5 walkers of 100 steps from the same lamp post (hand-drawn paths in pale colours, the pub in the middle). RIGHT: the end points of 10,000 walkers as a cloud of points centred on the pub; a grey ring at distance about 10 yards with the call-out 'typical distance after 100 steps'.
Pearson's own remark, as quoted in secondary sources (verify in the original): the most probable place to find a drunken man who is at all capable of keeping on his feet is somewhere near his starting point. Be careful about the claim: per unit area the density is highest at the start, yet the typical distance grows like the square root of n (about 10 yards after 100 steps). Link: a short walk remembers where it began; a long one spreads out. Rayleigh had met the same mathematics in 1880, adding n waves of random phase.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## Random walks appear in many fields

<div class="fig">
<div style="display:flex;width:100%;height:400px"><div class="ph">THREE PANELS in a row, each a picture with a one-line caption: (1) pollen grains in water, the zig-zag trace of one grain (Perrin's drawing, public domain): 'pollen, explained by Einstein in 1905'; (2) a mosquito: 'mosquitoes and malaria, the question behind Pearson's letter'; (3) a hand-drawn web graph with a surfer: 'the web, 1998: a random surfer ranks pages'. A grey arrow pointing right with the aside: 'and on a network?'</div></div>
</div>


<!--
[#4] beat: hook: the same walk in three fields
source: Perrin, Les atomes (1913) for the trace; PageRank: Page, Brin, Motwani, Winograd (1998). Check each year before showing it.
figure: THREE PANELS in a row, each a picture with a one-line caption: (1) pollen grains in water, the zig-zag trace of one grain (Perrin's drawing, public domain): 'pollen, explained by Einstein in 1905'; (2) a mosquito: 'mosquitoes and malaria, the question behind Pearson's letter'; (3) a hand-drawn web graph with a surfer: 'the web, 1998: a random surfer ranks pages'. A grey arrow pointing right with the aside: 'and on a network?'
Dates to verify before the slide is finished: Brown 1827 (pollen); Einstein 1905 (explanation); Perrin (the measurement that settled it); Page and Brin 1998 (PageRank). The point: one idea, many fields. What does it tell us on a network? That is the next slide.
-->

---

<!-- _class: L-f -->
<!-- _footer: "" -->

## What does a random walk tell us about a <span class="hot">network</span>?


<!--
[#5] beat: spine 1: the question
Open with the drunkard in the lecture note: no map, no destination, no memory. The walker is the measuring instrument.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## One step: move to a random <span class="hot">neighbour</span>

<div class="fig">
<div style="display:flex;width:100%;height:400px"><div class="ph">Small 7-node network, hand-drawn. A walker (ring) stands on a node with 4 neighbours. Each of the 4 edges is labelled 1/4 (an amount, not a share). A grey aside: 'no memory of where it came from'.</div></div>
</div>


<!--
[#6] beat: mechanism: the rule
source: lecture-note/m07 fig-m07-net (re-drawn in house style)
figure: Small 7-node network, hand-drawn. A walker (ring) stands on a node with 4 neighbours. Each of the 4 edges is labelled 1/4 (an amount, not a share). A grey aside: 'no memory of where it came from'.
The only rule: divide your chance evenly among your edges. Keep this picture; it returns when P is introduced.
-->

---

<!-- _class: L-g -->
<!-- _footer: "" -->

<div class="fig">
<div style="display:flex;width:100%;height:400px"><div class="ph live">LIVE: random walk simulator, karate club, exactly as used last term (assets/vis/random-walks/index.html, no edits). The lecturer clicks Walk x20, then Run 5,000 steps.</div></div>
</div>


<!--
[#7] beat: live: the simulator (karate club)
figure: LIVE: random walk simulator, karate club, exactly as used last term (assets/vis/random-walks/index.html, no edits). The lecturer clicks Walk x20, then Run 5,000 steps.
Drive the tool in front of the room: click Walk about twenty times, then Run 5,000 steps. Default network is the karate club (34 nodes, 78 edges). The orange ticks (k/2m) are visible in this tool; on the student sheet we hide them (see plan.md, open question 2).
-->

---

<!-- _class: L-c -->
<!-- _footer: "" -->

## Short walk vs long walk

<div class="cols">
<div>

**20 steps:** what do you learn?

**5,000 steps:** what do you learn?

</div>
<div class="fig">
<div class="ph">Two small screenshots of the tool: after 20 steps, after 5,000 steps (no answer marks yet)</div>
</div>
</div>

<div class="cue">Take a minute. Tell your neighbour.</div>
<!--
[#8] beat: question to the room (Q1)
Question slide: never shows the answer. Let a few people answer aloud. Expect: 'neighbourhood of the start' and 'the popular nodes'.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## Short: <span class="hot">neighbourhood</span>. Long: <span class="hot">degree</span>.

<div class="fig">
<div style="display:flex;width:100%;height:400px"><div class="ph">LEFT: the tool after 20 steps, nodes shaded by visits: dark nodes cluster around the start node. RIGHT: after 5,000 steps: dark nodes are the hubs (33 and 0). Grey ring call-outs: 'the start', 'hubs'.</div></div>
</div>


<!--
[#9] beat: answer to Q1
source: screenshots of the unchanged tool
figure: LEFT: the tool after 20 steps, nodes shaded by visits: dark nodes cluster around the start node. RIGHT: after 5,000 steps: dark nodes are the hubs (33 and 0). Grey ring call-outs: 'the start', 'hubs'.
The answer to the previous slide, on its own figure. Short: where you started. Long: the most connected nodes. Do not yet say 'proportional to degree'; the sheet finds that.
-->

---

<!-- _class: L-g -->
<!-- _footer: "" -->

<div class="fig">
<div style="display:flex;width:100%;height:400px"><div class="ph live">LIVE: same tool, ?dataFile=two-cliques.json: two 5-cliques joined by a single edge.</div></div>
</div>


<!--
[#10] beat: live: the simulator (two communities)
figure: LIVE: same tool, ?dataFile=two-cliques.json: two 5-cliques joined by a single edge.
Switch to the two-community network. Ask the room to watch the walker, not the bars.
-->

---

<!-- _class: L-c -->
<!-- _footer: "" -->

## Two communities joined by one edge

<div class="cols">
<div>

**How many steps** until the walker crosses to the other community?

A: about 3

B: about 20

C: about 200

</div>
<div class="fig">
<div class="ph">The 10-node two-community network, the walker in community 1, the single edge between the communities marked with a grey arrow</div>
</div>
</div>

<div class="cue">Take a guess.</div>
<!--
[#11] beat: question to the room (Q2)
Answer B. A walker in community 1 uses the bridge with chance 1/21 per step, so it stays about 21 steps (computed from k/2m: the bridge is used with probability 1/42 per step overall, and the walker is in community 1 half of the time).
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

<div class="optflag">OPTIONAL</div>

## A short walk stays in its <span class="hot">community</span>

<div class="fig">
<div style="display:flex;width:100%;height:400px"><div class="ph">Same network. The walker's path drawn as a brush stroke, coloured by community (community 1 cool, community 2 hot); a time strip under it shows long runs of one colour, about 21 steps each. Grey call-out: 'about 21 steps per visit'.</div></div>
</div>


<!--
[#12] beat: answer to Q2
figure: Same network. The walker's path drawn as a brush stroke, coloured by community (community 1 cool, community 2 hot); a time strip under it shows long runs of one colour, about 21 steps each. Grey call-out: 'about 21 steps per visit'.
Short walks remember the community they started in. This is the community signal we will find in the second eigenvector.
-->

---

<!-- _class: L-f -->
<!-- _footer: "" -->

## Short walks show <span class="hot">communities</span>. Long walks show <span class="hot">degree</span>. Why?


<!--
[#13] beat: spine 2: the mystery
The maths answers exactly this. First, your hands: Pen & Paper Part 1.
-->

---

<!-- _class: L-f -->
<!-- _footer: "" -->

## Pen & Paper, Part 1

<div class="sub">

10 minutes · stop at the line on the sheet

</div>

<div class="fig">
<div style="display:flex;width:100%;height:250px"><div class="ph">QR code (large) to the simulator, plus the short link</div></div>
</div>


<!--
[#14] beat: Pen & Paper Part 1: opener
figure: QR code (large) to the simulator, plus the short link
Students open the tool on their phones or laptops from the QR code on the sheet. Part 1 must be finished before the maths. The sheet has a printed line: STOP, wait for the lecture.
-->

---

<!-- _class: L-c -->
<!-- _footer: "" -->

## Part 1: tasks

<div class="cols">
<div class="left">

1. Sketch: correlation with degree over time

2. Run 20,000 steps. Read the most and least visited node.

3. Compute degree ÷ share, for both

</div>
<div class="fig">
<div class="ph">Large timer (10:00) and the QR code</div>
</div>
</div>
<!--
[#15] beat: Pen & Paper Part 1: instructions
The wording on the slide is a reminder only; the sheet carries the full text. Walk around the room.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## Correlation <span class="hot">rises</span> with the steps

<div class="fig">
<div style="display:flex;width:100%;height:400px"><div class="ph">Line plot. x: steps (log scale, 10 to 20,000). y: correlation between visit share and degree. Dots at 0.37, 0.53, 0.76, 0.89, 0.96, 0.99, 1.00 (mean over all 34 starts), a pale band for min to max. Grey call-out: 'at 20 steps, it depends on where you start'.</div></div>
</div>


<!--
[#16] beat: debrief Q1 (the sketch)
source: simulation, 6 walkers per start node, seed fixed in the figure script
figure: Line plot. x: steps (log scale, 10 to 20,000). y: correlation between visit share and degree. Dots at 0.37, 0.53, 0.76, 0.89, 0.96, 0.99, 1.00 (mean over all 34 starts), a pale band for min to max. Grey call-out: 'at 20 steps, it depends on where you start'.
Compare with the sketches on the sheets. The common mistake: a straight line. The real curve rises fast, then saturates. Numbers in this wireframe come from a 204-walker simulation; the final figure script asserts them.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## Degree ÷ share is <span class="hot">constant</span>

<div class="sub">

Karate club: 34 nodes, 78 edges, so 2m = 156

</div>

<div class="fig">
<div style="display:flex;width:100%;height:330px"><div class="ph">Scatter: x = degree, y = share of visits after 20,000 steps, 34 dots on a straight line through the origin. Node 33 (degree 17, share 0.109) and node 11 (degree 1, share 0.0064) circled, hot. Grey call-outs: '17 ÷ 0.109 = 156', '1 ÷ 0.0064 = 156'.</div></div>
</div>


<div class="take">

Share of time = degree ÷ <span class="hot">2m</span>

</div>

<!--
[#17] beat: debrief Q2 (degree ÷ share)
figure: Scatter: x = degree, y = share of visits after 20,000 steps, 34 dots on a straight line through the origin. Node 33 (degree 17, share 0.109) and node 11 (degree 1, share 0.0064) circled, hot. Grey call-outs: '17 ÷ 0.109 = 156', '1 ÷ 0.0064 = 156'.
The student ratios scatter (node 11 is noisy: about 130 to 180 at 5,000 steps, about 140 to 180 at 20,000). Say so: the ratio is a law of large numbers, not an identity of one run. The most visited node is 33 in about 3 runs out of 4 and node 0 otherwise; both give 156.
-->

---

<!-- _class: L-f -->
<!-- _footer: "" -->

## Why does a long walk not depend on the <span class="hot">start</span>?


<!--
[#18] beat: spine 3: part question
From here: the maths. Everything is a picture of vectors and matrices, drawn as in the centrality lecture (circle = eigenvalue, tall bar = vector).
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## The walk is defined by <span class="hot">one matrix</span>

<div class="fig">
<div style="display:flex;width:100%;height:400px"><div class="ph">LEFT (small): the 12-node 'two communities' network (nodes 0-5 and 6-11, two bridge edges 2-8 and 5-11). RIGHT: its transition matrix P as a heat map, 12 x 12, two dense blocks on the diagonal, thin entries off the blocks. Grey call-out on one row: 'row i = the odds of leaving i, sums to 1'.</div></div>
</div>


<!--
[#19] beat: P (the 'two communities' network, the motif of the rest of the lecture)
source: figure script on smallgraphs.py (same graph as the sheet's Part 3)
figure: LEFT (small): the 12-node 'two communities' network (nodes 0-5 and 6-11, two bridge edges 2-8 and 5-11). RIGHT: its transition matrix P as a heat map, 12 x 12, two dense blocks on the diagonal, thin entries off the blocks. Grey call-out on one row: 'row i = the odds of leaving i, sums to 1'.
Introduce the two-community network that we use until the end and that the sheet uses in Part 3. Do not reveal the eigenvector yet.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## One step is a <span class="hot">multiplication</span> by $P$

<div class="sub">

$x(t+1) = x(t)\,P$

</div>

<div class="fig">
<div style="display:flex;width:100%;height:330px"><div class="ph">Matrix picture in the M06 style: a wide bar (distribution x(t), 12 cells, shaded) times the square P = a wide bar (x(t+1)). Small network beside it with the walker's probability mass drawn as node shading. Grey call-out: 'x is a row vector: row x column'.</div></div>
</div>


<div class="take">

After $t$ steps: $x(t) = x(0)\,P^{t}$

</div>

<!--
[#20] beat: x P
figure: Matrix picture in the M06 style: a wide bar (distribution x(t), 12 cells, shaded) times the square P = a wide bar (x(t+1)). Small network beside it with the walker's probability mass drawn as node shading. Grey call-out: 'x is a row vector: row x column'.
Convention: row vector, as in the lecture note (x(t) = x(0) P^t, P_ij = A_ij / k_i). If you want the column form from your brief, we use P transposed; see plan.md.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

<div class="buildflag">build 1/3</div>

## Rows of $P^t$ <span class="hot">after t steps</span>

<div class="fig">
<div style="display:flex;width:100%;height:430px"><div class="ph">Heat map of P^1 (12 x 12), same crop and position as the previous step: two dense diagonal blocks. Callout: 't = 1: stays in its community'</div></div>
</div>


<!--
[#21] beat: P^t as heat maps (1/3)
figure: Heat map of P^1 (12 x 12), same crop and position as the previous step: two dense diagonal blocks. Callout: 't = 1: stays in its community'
Build step 1/3, t = 1. The same drawing grows: only the matrix changes. At t = 40 the total variation distance of the worst start is about 0.005.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

<div class="buildflag">build 2/3</div>

## Rows of $P^t$ <span class="hot">after t steps</span>

<div class="fig">
<div style="display:flex;width:100%;height:430px"><div class="ph">Heat map of P^5 (12 x 12), same crop and position as the previous step: the blocks blur. Callout: 't = 5: starting to leak'</div></div>
</div>


<!--
[#22] beat: P^t as heat maps (2/3)
figure: Heat map of P^5 (12 x 12), same crop and position as the previous step: the blocks blur. Callout: 't = 5: starting to leak'
Build step 2/3, t = 5. The same drawing grows: only the matrix changes. At t = 40 the total variation distance of the worst start is about 0.005.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

<div class="buildflag">build 3/3</div>

## Rows of $P^t$ <span class="hot">after t steps</span>

<div class="fig">
<div style="display:flex;width:100%;height:430px"><div class="ph">Heat map of P^40 (12 x 12), same crop and position as the previous step: every row identical. Callout: 't = 40: all rows = pi'</div></div>
</div>


<div class="take">

Every row becomes the same: <span class="hot">π</span>

</div>

<!--
[#23] beat: P^t as heat maps (3/3)
figure: Heat map of P^40 (12 x 12), same crop and position as the previous step: every row identical. Callout: 't = 40: all rows = pi'
Build step 3/3, t = 40. The same drawing grows: only the matrix changes. At t = 40 the total variation distance of the worst start is about 0.005.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## Recall: eigendecomposition

<div class="fig">

![](figures/m06-decomp-sum.png)

</div>


<!--
[#24] beat: recap: eigendecomposition (M06, light touch)
source: slides/m06/figures/decomp-sum.png (reused unchanged)
Two sentences only: circle = eigenvalue, tall bar = eigenvector, wide bar = its transpose. Do not re-derive. The students saw this for the adjacency matrix.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## $P$ has an eigendecomposition too

<div class="sub">

$P = \sum_k \lambda_k\,\phi_k\,\psi_k^{\top}$

</div>

<div class="fig">
<div style="display:flex;width:100%;height:320px"><div class="ph">Same pictorial grammar as M06: circle (eigenvalue, size = |lambda|), tall bar phi_k (right eigenvector), wide bar psi_k^T (left eigenvector); k = 1 blue, k = 2 gold, the rest pale; shown as terms 1, 2, ..., 12. A grey aside: 'for P, the tall and wide bars are two different vectors (each is the other rescaled by degree)'.</div></div>
</div>


<div class="take">

$P^t$ changes only the <span class="hot">eigenvalues</span>

</div>

<!--
[#25] beat: P as a sum of circles and bars
figure: Same pictorial grammar as M06: circle (eigenvalue, size = |lambda|), tall bar phi_k (right eigenvector), wide bar psi_k^T (left eigenvector); k = 1 blue, k = 2 gold, the rest pale; shown as terms 1, 2, ..., 12. A grey aside: 'for P, the tall and wide bars are two different vectors (each is the other rescaled by degree)'.
The bars multiply to 1 or 0 as in M06, so P^t = sum of lambda_k^t phi_k psi_k^T. The left-right distinction is a detail: stated once, kept in the appendix. See plan.md, open question 3.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

<div class="buildflag">build 1/3</div>

## The eigenvalues <span class="hot">shrink</span> as $t$ grows

<div class="fig">
<div style="display:flex;width:100%;height:430px"><div class="ph">P^1 drawn as a sum of the same terms (same canvas as the previous step); circle areas = lambda^1: circles at 1, 0.89, 0, 0, 0, -0.09, -0.2, -0.2, -0.27, -0.33, -0.38, -0.42. First circle always full size, blue. Callout: 'one step'</div></div>
</div>


<!--
[#26] beat: P^t as circles (1/3)
figure: P^1 drawn as a sum of the same terms (same canvas as the previous step); circle areas = lambda^1: circles at 1, 0.89, 0, 0, 0, -0.09, -0.2, -0.2, -0.27, -0.33, -0.38, -0.42. First circle always full size, blue. Callout: 'one step'
Build step 1/3, t = 1. Eigenvalues are those of the 12-node two-community network (computed): 1, 0.889, 0, 0, 0, -0.088, -0.2, -0.2, -0.266, -0.333, -0.379, -0.423.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

<div class="buildflag">build 2/3</div>

## The eigenvalues <span class="hot">shrink</span> as $t$ grows

<div class="fig">
<div style="display:flex;width:100%;height:430px"><div class="ph">P^5 drawn as a sum of the same terms (same canvas as the previous step); circle areas = lambda^5: circle 2 at 0.55, the rest almost gone. First circle always full size, blue. Callout: 'lambda_2^5 = 0.55'</div></div>
</div>


<!--
[#27] beat: P^t as circles (2/3)
figure: P^5 drawn as a sum of the same terms (same canvas as the previous step); circle areas = lambda^5: circle 2 at 0.55, the rest almost gone. First circle always full size, blue. Callout: 'lambda_2^5 = 0.55'
Build step 2/3, t = 5. Eigenvalues are those of the 12-node two-community network (computed): 1, 0.889, 0, 0, 0, -0.088, -0.2, -0.2, -0.266, -0.333, -0.379, -0.423.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

<div class="buildflag">build 3/3</div>

## The eigenvalues <span class="hot">shrink</span> as $t$ grows

<div class="fig">
<div style="display:flex;width:100%;height:430px"><div class="ph">P^40 drawn as a sum of the same terms (same canvas as the previous step); circle areas = lambda^40: circle 2 at 0.01; circle 1 untouched. First circle always full size, blue. Callout: 'only the circle at 1 is left: every row is pi'</div></div>
</div>


<!--
[#28] beat: P^t as circles (3/3)
figure: P^40 drawn as a sum of the same terms (same canvas as the previous step); circle areas = lambda^40: circle 2 at 0.01; circle 1 untouched. First circle always full size, blue. Callout: 'only the circle at 1 is left: every row is pi'
Build step 3/3, t = 40. Eigenvalues are those of the 12-node two-community network (computed): 1, 0.889, 0, 0, 0, -0.088, -0.2, -0.2, -0.266, -0.333, -0.379, -0.423.
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
<div class="ph">The 12 eigenvalue circles in a row, ordered by value; no mark yet</div>
</div>
</div>

<div class="cue">Take 20 seconds.</div>
<!--
[#29] beat: Q3 (which term stays the longest)
Trick: the second circle (0.89) lasts long, but the first (1) never decays. The question is about 'last of those that die'. Be explicit after the answer.
-->

---

<!-- _class: L-c -->
<!-- _footer: "" -->

## The <span class="hot">second</span> term stays the longest

<div class="cols">
<div>

$\lambda_2 = 0.89$

$0.89^{t}$: 0.55 at $t = 5$, 0.31 at $t = 10$, 0.01 at $t = 40$

</div>
<div class="fig">
<div class="ph">Same 12 circles, now drawn at t = 10 sizes; circle 2 hot, the rest pale</div>
</div>
</div>
<!--
[#30] beat: A3
Same figure as the question, with the answer added.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## The <span class="hot">distance</span> to $\pi$ decreases

<div class="fig">
<div style="display:flex;width:100%;height:400px"><div class="ph">Five small bar charts in a row: the walker's distribution x(t) on the 12 nodes for t = 0, 1, 3, 10, 40, starting at node 0. A flat reference line pi on each chart (pi = degree / 60). Under each: 'distance to pi' as a number (1-norm), shrinking to about 0.</div></div>
</div>


<!--
[#31] beat: distance to pi (small multiples)
figure: Five small bar charts in a row: the walker's distribution x(t) on the 12 nodes for t = 0, 1, 3, 10, 40, starting at node 0. A flat reference line pi on each chart (pi = degree / 60). Under each: 'distance to pi' as a number (1-norm), shrinking to about 0.
Define distance as the 1-norm, as the lecture note does. Numbers come from the figure script (total variation 0.93, 0.63, 0.38, 0.17, 0.005; the 1-norm is twice these).
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

<div class="buildflag">build 1/3</div>

## <span class="hot">Mixing time</span>

<div class="fig">
<div style="display:flex;width:100%;height:380px"><div class="ph">Curves: distance to pi against t, one thin grey line per starting node (12), and a black line for the worst start. Callout: 'where you start matters at first'.</div></div>
</div>


<!--
[#32] beat: mixing time diagram (1/3)
figure: Curves: distance to pi against t, one thin grey line per starting node (12), and a black line for the worst start. Callout: 'where you start matters at first'.
Build step 1/3. The same canvas. The formula appears only at the end, after the diagram has said it.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

<div class="buildflag">build 2/3</div>

## <span class="hot">Mixing time</span>

<div class="fig">
<div style="display:flex;width:100%;height:380px"><div class="ph">Same plot plus a horizontal line at epsilon. Callout: 'how close is close enough?'</div></div>
</div>


<!--
[#33] beat: mixing time diagram (2/3)
figure: Same plot plus a horizontal line at epsilon. Callout: 'how close is close enough?'
Build step 2/3. The same canvas. The formula appears only at the end, after the diagram has said it.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

<div class="buildflag">build 3/3</div>

## <span class="hot">Mixing time</span>

<div class="sub">

$t_{\mathrm{mix}} = \min\{\,t : \max_{x(0)} \|x(t) - \pi\|_1 \le \epsilon\,\}$

</div>

<div class="fig">
<div style="display:flex;width:100%;height:380px"><div class="ph">Same plot; the point where the worst-start line crosses epsilon marked hot, with a vertical line down to the axis labelled 'mixing time'.</div></div>
</div>


<!--
[#34] beat: mixing time diagram (3/3)
figure: Same plot; the point where the worst-start line crosses epsilon marked hot, with a vertical line down to the axis labelled 'mixing time'.
Build step 3/3. The same canvas. The formula appears only at the end, after the diagram has said it.
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
<div style="display:flex;width:100%;height:420px"><div class="ph">A 10-clique, hand-drawn, nodes in a ring; the walker on node 0</div></div>
</div>


<div class="cue">Take a guess: 1 step, 5 steps, 50 steps.</div>

<!--
[#35] beat: Q4 (clique)
figure: A 10-clique, hand-drawn, nodes in a ring; the walker on node 0
One graph per question. A: one step. lambda_2 = -1/9; relaxation time about 0.9 steps.
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
<div style="display:flex;width:100%;height:420px"><div class="ph">Same clique, same position. Distance-to-pi curve as an inset: below epsilon at t = 1</div></div>
</div>


<div class="take">

$\lambda_2 = -1/9$: mixing takes <span class="hot">about 1 step</span>

</div>

<!--
[#36] beat: A4
figure: Same clique, same position. Distance-to-pi curve as an inset: below epsilon at t = 1
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## Q: mixing time with one bridge?

<div class="sub">

Two 5-cliques joined by one edge (21 edges)

</div>

<div class="fig">
<div style="display:flex;width:100%;height:420px"><div class="ph">The two-clique network (the tool's two-cliques.json), the walker in community 1</div></div>
</div>


<div class="cue">The same, 5 times longer, or 15 times longer?</div>

<!--
[#37] beat: Q5 (two cliques)
figure: The two-clique network (the tool's two-cliques.json), the walker in community 1
The edges halved but the answer is 15x slower. Trick: the clique has more edges, but what matters is the bottleneck.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## A: about 15 times longer

<div class="sub">

Two 5-cliques joined by one edge (21 edges)

</div>

<div class="fig">
<div style="display:flex;width:100%;height:420px"><div class="ph">Same network. Inset: distance-to-pi curve with the clique's curve in pale for comparison</div></div>
</div>


<div class="take">

$\lambda_2 = 0.93$: mixing takes about <span class="hot">14 steps</span>

</div>

<!--
[#38] beat: A5
figure: Same network. Inset: distance-to-pi curve with the clique's curve in pale for comparison
tau = 1/(1 - 0.927) = 13.7. Compare 0.9 for the clique: fifteen-fold.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## The <span class="hot">mixing time</span> follows from $\lambda_2$

<div class="sub">

$\tau = \dfrac{1}{1-\lambda_2}$

</div>

<div class="fig">
<div style="display:flex;width:100%;height:300px"><div class="ph">A horizontal gauge for lambda_2 from -0.2 to 1 with markers: 10-clique (-0.11, tau 0.9), karate club (0.87, tau 7.6), two communities (0.89, tau 9), two 5-cliques + bridge (0.93, tau 14), ring of 1,000 (0.99998, tau 50,000). Past 0.99 the gauge is shaded hot.</div></div>
</div>


<div class="take">

Small gap, <span class="hot">long mixing time</span>

</div>

<!--
[#39] beat: spectral gap (gauge)
figure: A horizontal gauge for lambda_2 from -0.2 to 1 with markers: 10-clique (-0.11, tau 0.9), karate club (0.87, tau 7.6), two communities (0.89, tau 9), two 5-cliques + bridge (0.93, tau 14), ring of 1,000 (0.99998, tau 50,000). Past 0.99 the gauge is shaded hot.
'Spectral gap' = 1 - lambda_2. t_mix is a few tau: the logarithm in the lecture note's bound pays for epsilon and the rarest node. Not derived here.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

<div class="optflag">OPTIONAL</div>

## Mixing time is a few relaxation times

<div class="fig">
<div style="display:flex;width:100%;height:400px"><div class="ph">The formula t_mix < tau log(1/(epsilon pi_min)) on the left; on the right the 12-node distance curve with tau marked and 2 tau, 3 tau as ticks.</div></div>
</div>


<!--
[#40] beat: (optional) the bound
figure: The formula t_mix < tau log(1/(epsilon pi_min)) on the left; on the right the 12-node distance curve with tau marked and 2 tau, 3 tau as ticks.
Cut candidate: the formula is in the lecture note; show it only if the room is quick.
-->

---

<!-- _class: L-f -->
<!-- _footer: "" -->

## One eigenvalue is always <span class="hot">1</span>. None is larger.


<!--
[#41] beat: spine 4: the fact
Taught as a fact; the next two slides give a reason for each half, in pictures, not a proof.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## Why 1? Every row of $P$ sums to <span class="hot">1</span>

<div class="fig">
<div style="display:flex;width:100%;height:400px"><div class="ph">Picture: the square P times a tall bar of all ones (cells '1') = the same tall bar. One row of P highlighted; its cells sum to the first cell of the result (= 1). Callout: 'P 1 = 1'.</div></div>
</div>


<!--
[#42] beat: lambda = 1 exists (P 1 = 1)
figure: Picture: the square P times a tall bar of all ones (cells '1') = the same tall bar. One row of P highlighted; its cells sum to the first cell of the result (= 1). Callout: 'P 1 = 1'.
The vector of ones is a right eigenvector with eigenvalue 1, because each row of P is a list of odds.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## No eigenvalue is <span class="hot">larger</span> than 1

<div class="fig">
<div style="display:flex;width:100%;height:400px"><div class="ph">Two frames on a 7-node network: numbers on the nodes (largest = 9); one step replaces every number by the average of its neighbours; the largest number can only stay or fall. Frame 2 is the same drawing with the new numbers; the largest is now 6.5.</div></div>
</div>


<!--
[#43] beat: no eigenvalue above 1
figure: Two frames on a 7-node network: numbers on the nodes (largest = 9); one step replaces every number by the average of its neighbours; the largest number can only stay or fall. Frame 2 is the same drawing with the new numbers; the largest is now 6.5.
P f replaces each entry by a neighbour average. That cannot raise the maximum, so |lambda| <= 1.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## The eigenvalue 1 gives <span class="hot">π</span>

<div class="sub">

The stationary distribution: $P^{t} \to \mathbf{1}\,\pi$

</div>

<div class="fig">
<div style="display:flex;width:100%;height:330px"><div class="ph">The first term alone: a tall bar of ones times a wide bar pi = a matrix whose every row is pi (the last heat map of the previous build, at the same position). Beside it the simulator's bars with the orange k/2m ticks (thumbnail).</div></div>
</div>


<div class="take">

$\pi_i = k_i / 2m$: proportional to <span class="hot">degree</span>

</div>

<!--
[#44] beat: lambda = 1 is pi (ties to the tool)
figure: The first term alone: a tall bar of ones times a wide bar pi = a matrix whose every row is pi (the last heat map of the previous build, at the same position). Beside it the simulator's bars with the orange k/2m ticks (thumbnail).
This is why the bars of the tool settled on their ticks and why degree ÷ share = 2m on the sheet. Reversibility is in the appendix.
-->

---

<!-- _class: L-f -->
<!-- _footer: "" -->

## Pen & Paper, Parts 2 and 3

<div class="sub">

20 minutes

</div>


<!--
[#45] beat: Pen & Paper Parts 2-3: opener
Everyone has now finished Part 1 and crossed the line on the sheet.
-->

---

<!-- _class: L-c -->
<!-- _footer: "" -->

## Parts 2 and 3: tasks

<div class="cols">
<div class="left">

2. Four nodes: write $x(t)$ with the eigenvalues, check $t = 2$

3. Twelve nodes: run one cell, plot the second eigenvector

</div>
<div class="fig">
<div class="ph">Left: the 4-node "diamond" network of Part 2. Right: QR code to the one-cell notebook of Part 3</div>
</div>
</div>
<!--
[#46] beat: Pen & Paper Parts 2-3: instructions
Part 2 can be done with a pencil only; Part 3 needs a laptop or a phone. Pair students if there are not enough devices.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## $x(t)$ = π + <span class="hot">decaying</span> terms

<div class="sub">

Four nodes; eigenvalues $1,\ 0,\ -\tfrac13,\ -\tfrac23$

</div>

<div class="fig">
<div style="display:flex;width:100%;height:340px"><div class="ph">The 4-node diamond network (degrees 2, 2, 3, 3) on the left. Right: bar charts of x(t) for t = 0, 1, 2, 5, 10 converging to pi = (0.2, 0.2, 0.3, 0.3). Under them the expansion: pi - 0.5 (0)^t psi_2 + 0 psi_3 + 0.3 (-2/3)^t psi_4, with the t = 2 line checked against x(2) = (1/3, 1/3, 1/6, 1/6).</div></div>
</div>


<div class="take">

Only the term with $\lambda = 1$ <span class="hot">remains</span>

</div>

<!--
[#47] beat: debrief Part 2
figure: The 4-node diamond network (degrees 2, 2, 3, 3) on the left. Right: bar charts of x(t) for t = 0, 1, 2, 5, 10 converging to pi = (0.2, 0.2, 0.3, 0.3). Under them the expansion: pi - 0.5 (0)^t psi_2 + 0 psi_3 + 0.3 (-2/3)^t psi_4, with the t = 2 line checked against x(2) = (1/3, 1/3, 1/6, 1/6).
Check: x(1) = pi + 0.3 (-2/3) psi_4 = (0, 0, 0.5, 0.5). x(2) = (1/3, 1/3, 1/6, 1/6). The eigenvalue -2/3 alternates the sign: the walker hops between {0,1} and {2,3}, then settles. Eigenpairs are on the sheet, not computed by students.
-->

---

<!-- _class: L-b -->
<!-- _footer: "" -->

## The second eigenvector separates the <span class="hot">communities</span>

<div class="fig">
<div style="display:flex;width:100%;height:400px"><div class="ph">Point plot: x = node index 0 to 11, y = second eigenvector of P (scaled to max 1). Nodes 0-5 on top (about +1; the bridge nodes 2 and 5 at about +0.74), nodes 6-11 on the bottom (about -1; 8 and 11 at -0.74). Community 1 cool, community 2 hot. A dashed line at 0. Callout: 'the sign gives the community'.</div></div>
</div>


<!--
[#48] beat: debrief Part 3 (second eigenvector)
source: numpy, the sheet's one-cell code
figure: Point plot: x = node index 0 to 11, y = second eigenvector of P (scaled to max 1). Nodes 0-5 on top (about +1; the bridge nodes 2 and 5 at about +0.74), nodes 6-11 on the bottom (about -1; 8 and 11 at -0.74). Community 1 cool, community 2 hot. A dashed line at 0. Callout: 'the sign gives the community'.
The cell computes np.linalg.eig(P), orders by the real part, and plots column 1. The eigenvector of P (right) is constant inside each community by symmetry; sign is arbitrary, so the two communities may swap colours.
-->

---

<!-- _class: L-a -->
<!-- _footer: "" -->

## Early on, the <span class="hot">community</span> signal dominates

<div class="sub">

Walker starts at node 0

</div>

<div class="fig">
<div style="display:flex;width:100%;height:360px"><div class="ph">Line plot: x = steps (0 to 40), y = probability of being in community 1: 1.00, 1.00, 0.92, 0.88, 0.80 (t = 5), 0.67 (t = 10), 0.55 (t = 20), 0.505 (t = 40). A dashed curve 0.5 + 0.5 x 0.889^t over it. Callout at t about 3: 'the other eleven circles are gone'.</div></div>
</div>


<div class="take">

The community signal decays like $\lambda_2^{\,t}$. Degree remains.

</div>

<!--
[#49] beat: debrief Part 3 (what dominates early)
figure: Line plot: x = steps (0 to 40), y = probability of being in community 1: 1.00, 1.00, 0.92, 0.88, 0.80 (t = 5), 0.67 (t = 10), 0.55 (t = 20), 0.505 (t = 40). A dashed curve 0.5 + 0.5 x 0.889^t over it. Callout at t about 3: 'the other eleven circles are gone'.
After about three steps, only two terms are left: the term with eigenvalue 1 (degree) and the one at 0.89 (the communities). The second decays on the time scale tau = 9. This is the bookend: short walks see communities, long walks see degree.
-->

---

<!-- _class: L-g -->
<!-- _footer: "" -->

<div class="fig">
<div style="display:flex;width:100%;height:560px"><div class="ph">Summary, three rows, each with a thumbnail of its figure: (1) the eigenvalue 1 = degree (thumb: scatter, slide 17). (2) The second eigenvalue = the communities, and its size determines the mixing time (thumb: gauge). (3) Short walks see communities; long walks see degree (thumb: the community-probability curve).</div></div>
</div>


<!--
[#50] beat: summary (claims with thumbnails)
figure: Summary, three rows, each with a thumbnail of its figure: (1) the eigenvalue 1 = degree (thumb: scatter, slide 17). (2) The second eigenvalue = the communities, and its size determines the mixing time (thumb: gauge). (3) Short walks see communities; long walks see degree (thumb: the community-probability curve).
Three claims, each pointing back at the picture that proved it. Then say what is next.
-->

---

<!-- _class: L-f -->
<!-- _footer: "" -->

## Next: how long does it take to <span class="hot">reach</span> a node?

<div class="fig">
<div style="display:flex;width:100%;height:300px"><div class="ph">The opening picture again: the karate club, nodes shaded by long-run visits, with two nodes marked A and B</div></div>
</div>


<!--
[#51] beat: close: back to the opening picture, then a question for next time
figure: The opening picture again: the karate club, nodes shaded by long-run visits, with two nodes marked A and B
Next time: hitting time, commute time, PageRank and Walktrap (see the lecture note). The close answers the opening picture; it never says 'Thank you'.
-->

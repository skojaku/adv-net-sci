#!/usr/bin/env python3
"""M07 random walks, wireframe v1: writes deck.md and review/DECK_SPEC.md from one slide list.

Dashed boxes are figures to be made; the text in each box says what goes there.
Run:  python3 review/make_wireframe.py   (then review/render.sh)
"""
import os, re

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLIDES, PARTS = [], []

TOOL = "../../lecture-note/assets/vis/random-walks/index.html"   # last term's simulator, unchanged


def part(name, minutes):
    PARTS.append((len(SLIDES) + 1, name, minutes))


def S(cls, title=None, sub=None, ph=None, take=None, cue=None, beat="", note="", src="", opt=False,
      body=None, h=400, build=None, live=None, img=None):
    SLIDES.append(dict(cls=cls, title=title, sub=sub, ph=ph, take=take, cue=cue, beat=beat, note=note,
                       src=src, opt=opt, body=body, h=h, build=build, live=live, img=img))


def hot(w):
    return f'<span class="hot">{w}</span>'


def cool(w):
    return f'<span class="cool">{w}</span>'


# ============================================================================ A. INTUITION
part("A  Intuition: Pearson's walker, then what a blind walker learns (live tool, Pen & Paper Part 1)", 29)

S("lead", title="Random Walks",
  body='<p class="sub">Module 7 · Advanced Network Science<br>Sadamori Kojaku</p>\n\n<p class="ref">(school logo, bottom left, as in the CCS deck)</p>',
  beat="title", note="Lecture plan: about 90 minutes. Say the budget here: 1 minute per content slide, builds take seconds. The Pen & Paper sheet is worked in two blocks (Part 1 before the maths, Parts 2-3 after).")

S("L-c", title="Where is the walker after 100 steps?",
  body='<div class="cols">\n<div>\n\nA man walks **1 yard**, turns in a random direction, and walks **1 yard** again. He repeats this 100 times.\n\nPearson asked this in *Nature* in 1905.\n\n</div>\n<div class="fig">\n<div class="ph">The first lines of Karl Pearson\'s letter to Nature, 27 July 1905 (facsimile or a re-typeset quotation, with credit). Under it: a pub, a lamp post, no answer yet</div>\n</div>\n</div>',
  cue="Far from the start, or near it? Tell your neighbour.", beat="hook (story): Pearson's question, 1905",
  src="K. Pearson, The Problem of the Random Walk, Nature 72, 294 (1905), doi:10.1038/072294b0. Check the exact wording against the original before quoting.",
  note="Open with the history. In July 1905 the statistician Karl Pearson asked the readers of Nature: a man walks l yards, turns through any angle, walks l yards again, n times; where is he? The problem came from a biological question about how far mosquitoes spread (Pearson corresponded with Ronald Ross about malaria). Question slide: never shows the answer.")

S("L-a", title="Most likely near the start",
  ph=["LEFT: the paths of 5 walkers of 100 steps from the same lamp post (hand-drawn paths in pale colours, the pub in the middle). RIGHT: the end points of 10,000 walkers as a cloud of points centred on the pub; a grey ring at distance about 10 yards with the call-out 'typical distance after 100 steps'."],
  take=f"Rayleigh replied the next week: he had solved it in 1880, for {hot('waves')}", beat="answer: Pearson's walker (the density peaks at the start)", h=360,
  src="J. W. Strutt (Lord Rayleigh), Nature 72, 318 (1905); K. Pearson, Nature 72, 342 (1905). Figure: simulation, seed fixed in the figure script.",
  note="Pearson's own remark, as quoted in secondary sources (verify in the original): the most probable place to find a drunken man who is at all capable of keeping on his feet is somewhere near his starting point. Be careful about the claim: per unit area the density is highest at the start, yet the typical distance grows like the square root of n (about 10 yards after 100 steps). Link: a short walk remembers where it began; a long one spreads out. Rayleigh had met the same mathematics in 1880, adding n waves of random phase.")

S("L-b", title="Random walks appear in many fields",
  ph=["THREE PANELS in a row, each a picture with a one-line caption: (1) pollen grains in water, the zig-zag trace of one grain (Perrin's drawing, public domain): 'pollen, explained by Einstein in 1905'; (2) a mosquito: 'mosquitoes and malaria, the question behind Pearson's letter'; (3) a hand-drawn web graph with a surfer: 'the web, 1998: a random surfer ranks pages'. A grey arrow pointing right with the aside: 'and on a network?'"],
  beat="hook: the same walk in three fields", src="Perrin, Les atomes (1913) for the trace; PageRank: Page, Brin, Motwani, Winograd (1998). Check each year before showing it.",
  note="Dates to verify before the slide is finished: Brown 1827 (pollen); Einstein 1905 (explanation); Perrin (the measurement that settled it); Page and Brin 1998 (PageRank). The point: one idea, many fields. What does it tell us on a network? That is the next slide.")

S("L-f", title=f"What does a random walk tell us about a {hot('network')}?",
  beat="spine 1: the question", note="Open with the drunkard in the lecture note: no map, no destination, no memory. The walker is the measuring instrument.")

S("L-b", title=f"One step: move to a random {hot('neighbour')}",
  ph=["Small 7-node network, hand-drawn. A walker (ring) stands on a node with 4 neighbours. Each of the 4 edges is labelled 1/4 (an amount, not a share). A grey aside: 'no memory of where it came from'."],
  beat="mechanism: the rule", src="lecture-note/m07 fig-m07-net (re-drawn in house style)",
  note="The only rule: divide your chance evenly among your edges. Keep this picture; it returns when P is introduced.")

S("L-g", title=None, live=TOOL, beat="live: the simulator (karate club)",
  ph=["LIVE: random walk simulator, karate club, exactly as used last term (assets/vis/random-walks/index.html, no edits). The lecturer clicks Walk x20, then Run 5,000 steps."],
  note="Drive the tool in front of the room: click Walk about twenty times, then Run 5,000 steps. Default network is the karate club (34 nodes, 78 edges). The orange ticks (k/2m) are visible in this tool; on the student sheet we hide them (see plan.md, open question 2).")

S("L-c", title="Short walk vs long walk",
  body='<div class="cols">\n<div>\n\n**20 steps:** what do you learn?\n\n**5,000 steps:** what do you learn?\n\n</div>\n<div class="fig">\n<div class="ph">Two small screenshots of the tool: after 20 steps, after 5,000 steps (no answer marks yet)</div>\n</div>\n</div>',
  cue="Take a minute. Tell your neighbour.", beat="question to the room (Q1)",
  note="Question slide: never shows the answer. Let a few people answer aloud. Expect: 'neighbourhood of the start' and 'the popular nodes'.")

S("L-b", title=f"Short: {hot('neighbourhood')}. Long: {hot('degree')}.",
  ph=["LEFT: the tool after 20 steps, nodes shaded by visits: dark nodes cluster around the start node. RIGHT: after 5,000 steps: dark nodes are the hubs (33 and 0). Grey ring call-outs: 'the start', 'hubs'."],
  beat="answer to Q1", src="screenshots of the unchanged tool",
  note="The answer to the previous slide, on its own figure. Short: where you started. Long: the most connected nodes. Do not yet say 'proportional to degree'; the sheet finds that.")

S("L-g", title=None, live=TOOL + "?dataFile=two-cliques.json", beat="live: the simulator (two communities)",
  ph=["LIVE: same tool, ?dataFile=two-cliques.json: two 5-cliques joined by a single edge."],
  note="Switch to the two-community network. Ask the room to watch the walker, not the bars.")

S("L-c", title="Two communities joined by one edge",
  body='<div class="cols">\n<div>\n\n**How many steps** until the walker crosses to the other community?\n\nA: about 3\n\nB: about 20\n\nC: about 200\n\n</div>\n<div class="fig">\n<div class="ph">The 10-node two-community network, the walker in community 1, the single edge between the communities marked with a grey arrow</div>\n</div>\n</div>',
  cue="Take a guess.", beat="question to the room (Q2)",
  note="Answer B. A walker in community 1 uses the bridge with chance 1/21 per step, so it stays about 21 steps (computed from k/2m: the bridge is used with probability 1/42 per step overall, and the walker is in community 1 half of the time).")

S("L-b", title=f"A short walk stays in its {hot('community')}", opt=True,
  ph=["Same network. The walker's path drawn as a brush stroke, coloured by community (community 1 cool, community 2 hot); a time strip under it shows long runs of one colour, about 21 steps each. Grey call-out: 'about 21 steps per visit'."],
  beat="answer to Q2", note="Short walks remember the community they started in. This is the community signal we will find in the second eigenvector.")

S("L-f", title=f"Short walks show {hot('communities')}. Long walks show {hot('degree')}. Why?",
  beat="spine 2: the mystery", note="The maths answers exactly this. First, your hands: Pen & Paper Part 1.")

S("L-f", title=f"Pen & Paper, Part 1",
  sub="10 minutes · stop at the line on the sheet", beat="Pen & Paper Part 1: opener",
  ph=["QR code (large) to the simulator, plus the short link"],
  note="Students open the tool on their phones or laptops from the QR code on the sheet. Part 1 must be finished before the maths. The sheet has a printed line: STOP, wait for the lecture.", h=250)

S("L-c", title="Part 1: tasks",
  body='<div class="cols">\n<div class="left">\n\n1. Sketch: correlation with degree over time\n\n2. Run 20,000 steps. Read the most and least visited node.\n\n3. Compute degree ÷ share, for both\n\n</div>\n<div class="fig">\n<div class="ph">Large timer (10:00) and the QR code</div>\n</div>\n</div>',
  beat="Pen & Paper Part 1: instructions", note="The wording on the slide is a reminder only; the sheet carries the full text. Walk around the room.")

S("L-b", title=f"Correlation {hot('rises')} with the steps",
  ph=["Line plot. x: steps (log scale, 10 to 20,000). y: correlation between visit share and degree. Dots at 0.37, 0.53, 0.76, 0.89, 0.96, 0.99, 1.00 (mean over all 34 starts), a pale band for min to max. Grey call-out: 'at 20 steps, it depends on where you start'."],
  beat="debrief Q1 (the sketch)", src="simulation, 6 walkers per start node, seed fixed in the figure script",
  note="Compare with the sketches on the sheets. The common mistake: a straight line. The real curve rises fast, then saturates. Numbers in this wireframe come from a 204-walker simulation; the final figure script asserts them.")

S("L-a", title=f"Degree ÷ share is {hot('constant')}",
  sub="Karate club: 34 nodes, 78 edges, so 2m = 156",
  ph=["Scatter: x = degree, y = share of visits after 20,000 steps, 34 dots on a straight line through the origin. Node 33 (degree 17, share 0.109) and node 11 (degree 1, share 0.0064) circled, hot. Grey call-outs: '17 ÷ 0.109 = 156', '1 ÷ 0.0064 = 156'."],
  take=f"Share of time = degree ÷ {hot('2m')}", beat="debrief Q2 (degree ÷ share)",
  note="The student ratios scatter (node 11 is noisy: about 130 to 180 at 5,000 steps, about 140 to 180 at 20,000). Say so: the ratio is a law of large numbers, not an identity of one run. The most visited node is 33 in about 3 runs out of 4 and node 0 otherwise; both give 156.", h=330)

# ============================================================================ B. MATHS
part("B  Maths: why the start stops mattering (matrices, circles, mixing time, eigenvalue 1)", 36)

S("L-f", title=f"Why does a long walk not depend on the {hot('start')}?", beat="spine 3: part question",
  note="From here: the maths. Everything is a picture of vectors and matrices, drawn as in the centrality lecture (circle = eigenvalue, tall bar = vector).")

S("L-b", title=f"The walk is defined by {hot('one matrix')}",
  ph=["LEFT (small): the 12-node 'two communities' network (nodes 0-5 and 6-11, two bridge edges 2-8 and 5-11). RIGHT: its transition matrix P as a heat map, 12 x 12, two dense blocks on the diagonal, thin entries off the blocks. Grey call-out on one row: 'row i = the odds of leaving i, sums to 1'."],
  beat="P (the 'two communities' network, the motif of the rest of the lecture)", src="figure script on smallgraphs.py (same graph as the sheet's Part 3)",
  note="Introduce the two-community network that we use until the end and that the sheet uses in Part 3. Do not reveal the eigenvector yet.")

S("L-a", title=f"One step is a {hot('multiplication')} by $P$",
  sub="$x(t+1) = x(t)\\,P$",
  ph=["Matrix picture in the M06 style: a wide bar (distribution x(t), 12 cells, shaded) times the square P = a wide bar (x(t+1)). Small network beside it with the walker's probability mass drawn as node shading. Grey call-out: 'x is a row vector: row x column'."],
  take=f"After $t$ steps: $x(t) = x(0)\\,P^{{t}}$", beat="x P", h=330,
  note="Convention: row vector, as in the lecture note (x(t) = x(0) P^t, P_ij = A_ij / k_i). If you want the column form from your brief, we use P transposed; see plan.md.")

for k, (t, d) in enumerate([(1, "two dense diagonal blocks"), (5, "the blocks blur"), (40, "every row identical")], 1):
    S("L-b", title=f"Rows of $P^t$ {hot('after t steps')}",
      ph=[f"Heat map of P^{t} (12 x 12), same crop and position as the previous step: {d}. Callout: " + {1: "'t = 1: stays in its community'", 5: "'t = 5: starting to leak'", 40: "'t = 40: all rows = pi'"}[t]],
      take=(f"Every row becomes the same: {hot('π')}" if t == 40 else None), build=(k, 3), h=430,
      beat=f"P^t as heat maps ({k}/3)",
      note=f"Build step {k}/3, t = {t}. The same drawing grows: only the matrix changes. At t = 40 the total variation distance of the worst start is about 0.005.")

S("L-b", title="Recall: eigendecomposition",
  img="figures/m06-decomp-sum.png", beat="recap: eigendecomposition (M06, light touch)",
  src="slides/m06/figures/decomp-sum.png (reused unchanged)",
  note="Two sentences only: circle = eigenvalue, tall bar = eigenvector, wide bar = its transpose. Do not re-derive. The students saw this for the adjacency matrix.")

S("L-a", title=f"$P$ has an eigendecomposition too",
  sub="$P = \\sum_k \\lambda_k\\,\\phi_k\\,\\psi_k^{\\top}$",
  ph=["Same pictorial grammar as M06: circle (eigenvalue, size = |lambda|), tall bar phi_k (right eigenvector), wide bar psi_k^T (left eigenvector); k = 1 blue, k = 2 gold, the rest pale; shown as terms 1, 2, ..., 12. A grey aside: 'for P, the tall and wide bars are two different vectors (each is the other rescaled by degree)'."],
  take=f"$P^t$ changes only the {hot('eigenvalues')}", beat="P as a sum of circles and bars", h=320,
  note="The bars multiply to 1 or 0 as in M06, so P^t = sum of lambda_k^t phi_k psi_k^T. The left-right distinction is a detail: stated once, kept in the appendix. See plan.md, open question 3.")

for k, (t, d) in enumerate([(1, "circles at 1, 0.89, 0, 0, 0, -0.09, -0.2, -0.2, -0.27, -0.33, -0.38, -0.42"),
                            (5, "circle 2 at 0.55, the rest almost gone"), (40, "circle 2 at 0.01; circle 1 untouched")], 1):
    S("L-b", title=f"The eigenvalues {hot('shrink')} as $t$ grows",
      ph=[f"P^{t} drawn as a sum of the same terms (same canvas as the previous step); circle areas = lambda^{t}: {d}. First circle always full size, blue. Callout: " +
          {1: "'one step'", 5: "'lambda_2^5 = 0.55'", 40: "'only the circle at 1 is left: every row is pi'"}[t]],
      build=(k, 3), h=430, beat=f"P^t as circles ({k}/3)",
      note=f"Build step {k}/3, t = {t}. Eigenvalues are those of the 12-node two-community network (computed): 1, 0.889, 0, 0, 0, -0.088, -0.2, -0.2, -0.266, -0.333, -0.379, -0.423.")

S("L-c", title="Which term stays the longest?",
  body='<div class="cols">\n<div>\n\nThe 12 eigenvalues of $P$.\n\nAfter many steps, which term is still there?\n\n</div>\n<div class="fig">\n<div class="ph">The 12 eigenvalue circles in a row, ordered by value; no mark yet</div>\n</div>\n</div>',
  cue="Take 20 seconds.", beat="Q3 (which term stays the longest)",
  note="Trick: the second circle (0.89) lasts long, but the first (1) never decays. The question is about 'last of those that die'. Be explicit after the answer.")

S("L-c", title=f"The {hot('second')} term stays the longest",
  body='<div class="cols">\n<div>\n\n$\\lambda_2 = 0.89$\n\n$0.89^{t}$: 0.55 at $t = 5$, 0.31 at $t = 10$, 0.01 at $t = 40$\n\n</div>\n<div class="fig">\n<div class="ph">Same 12 circles, now drawn at t = 10 sizes; circle 2 hot, the rest pale</div>\n</div>\n</div>',
  beat="A3", note="Same figure as the question, with the answer added.")

S("L-b", title=f"The {hot('distance')} to $\\pi$ decreases",
  ph=["Five small bar charts in a row: the walker's distribution x(t) on the 12 nodes for t = 0, 1, 3, 10, 40, starting at node 0. A flat reference line pi on each chart (pi = degree / 60). Under each: 'distance to pi' as a number (1-norm), shrinking to about 0."],
  beat="distance to pi (small multiples)", note="Define distance as the 1-norm, as the lecture note does. Numbers come from the figure script (total variation 0.93, 0.63, 0.38, 0.17, 0.005; the 1-norm is twice these).")

for k, d in enumerate(["Curves: distance to pi against t, one thin grey line per starting node (12), and a black line for the worst start. Callout: 'where you start matters at first'.",
                       "Same plot plus a horizontal line at epsilon. Callout: 'how close is close enough?'",
                       "Same plot; the point where the worst-start line crosses epsilon marked hot, with a vertical line down to the axis labelled 'mixing time'."], 1):
    S("L-a", title=f"{hot('Mixing time')}",
      sub="$t_{\\mathrm{mix}} = \\min\\{\\,t : \\max_{x(0)} \\|x(t) - \\pi\\|_1 \\le \\epsilon\\,\\}$" if k == 3 else None,
      ph=[d], build=(k, 3), h=380, beat=f"mixing time diagram ({k}/3)",
      note=f"Build step {k}/3. The same canvas. The formula appears only at the end, after the diagram has said it.")

S("L-a", title="Q: mixing time of a 10-clique?", opt=True,
  sub="10 nodes, every pair connected (45 edges)",
  ph=["A 10-clique, hand-drawn, nodes in a ring; the walker on node 0"],
  cue="Take a guess: 1 step, 5 steps, 50 steps.", beat="Q4 (clique)", h=420,
  note="One graph per question. A: one step. lambda_2 = -1/9; relaxation time about 0.9 steps.")
S("L-a", title="A: about 1 step", opt=True,
  sub="10 nodes, every pair connected (45 edges)",
  ph=["Same clique, same position. Distance-to-pi curve as an inset: below epsilon at t = 1"],
  take=f"$\\lambda_2 = -1/9$: mixing takes {hot('about 1 step')}", beat="A4", h=420)
S("L-a", title="Q: mixing time with one bridge?",
  sub="Two 5-cliques joined by one edge (21 edges)",
  ph=["The two-clique network (the tool's two-cliques.json), the walker in community 1"],
  cue="The same, 5 times longer, or 15 times longer?", beat="Q5 (two cliques)", h=420,
  note="The edges halved but the answer is 15x slower. Trick: the clique has more edges, but what matters is the bottleneck.")
S("L-a", title="A: about 15 times longer",
  sub="Two 5-cliques joined by one edge (21 edges)",
  ph=["Same network. Inset: distance-to-pi curve with the clique's curve in pale for comparison"],
  take=f"$\\lambda_2 = 0.93$: mixing takes about {hot('14 steps')}", beat="A5", h=420,
  note="tau = 1/(1 - 0.927) = 13.7. Compare 0.9 for the clique: fifteen-fold.")

S("L-a", title=f"The {hot('mixing time')} follows from $\\lambda_2$",
  sub="$\\tau = \\dfrac{1}{1-\\lambda_2}$",
  ph=["A horizontal gauge for lambda_2 from -0.2 to 1 with markers: 10-clique (-0.11, tau 0.9), karate club (0.87, tau 7.6), two communities (0.89, tau 9), two 5-cliques + bridge (0.93, tau 14), ring of 1,000 (0.99998, tau 50,000). Past 0.99 the gauge is shaded hot."],
  take=f"Small gap, {hot('long mixing time')}", beat="spectral gap (gauge)", h=300,
  note="'Spectral gap' = 1 - lambda_2. t_mix is a few tau: the logarithm in the lecture note's bound pays for epsilon and the rarest node. Not derived here.")

S("L-b", title="Mixing time is a few relaxation times", opt=True,
  ph=["The formula t_mix < tau log(1/(epsilon pi_min)) on the left; on the right the 12-node distance curve with tau marked and 2 tau, 3 tau as ticks."],
  beat="(optional) the bound", note="Cut candidate: the formula is in the lecture note; show it only if the room is quick.")

S("L-f", title=f"One eigenvalue is always {hot('1')}. None is larger.", beat="spine 4: the fact",
  note="Taught as a fact; the next two slides give a reason for each half, in pictures, not a proof.")

S("L-b", title=f"Why 1? Every row of $P$ sums to {hot('1')}",
  ph=["Picture: the square P times a tall bar of all ones (cells '1') = the same tall bar. One row of P highlighted; its cells sum to the first cell of the result (= 1). Callout: 'P 1 = 1'."],
  beat="lambda = 1 exists (P 1 = 1)", note="The vector of ones is a right eigenvector with eigenvalue 1, because each row of P is a list of odds.")

S("L-b", title=f"No eigenvalue is {hot('larger')} than 1",
  ph=["Two frames on a 7-node network: numbers on the nodes (largest = 9); one step replaces every number by the average of its neighbours; the largest number can only stay or fall. Frame 2 is the same drawing with the new numbers; the largest is now 6.5."],
  beat="no eigenvalue above 1", note="P f replaces each entry by a neighbour average. That cannot raise the maximum, so |lambda| <= 1.")

S("L-a", title=f"The eigenvalue 1 gives {hot('π')}",
  sub="The stationary distribution: $P^{t} \\to \\mathbf{1}\\,\\pi$",
  ph=["The first term alone: a tall bar of ones times a wide bar pi = a matrix whose every row is pi (the last heat map of the previous build, at the same position). Beside it the simulator's bars with the orange k/2m ticks (thumbnail)."],
  take=f"$\\pi_i = k_i / 2m$: proportional to {hot('degree')}", beat="lambda = 1 is pi (ties to the tool)", h=330,
  note="This is why the bars of the tool settled on their ticks and why degree ÷ share = 2m on the sheet. Reversibility is in the appendix.")

# ============================================================================ C. PEN & PAPER 2, 3
part("C  Pen & Paper Parts 2-3, then debrief", 30)

S("L-f", title=f"Pen & Paper, Parts 2 and 3", sub="20 minutes",
  beat="Pen & Paper Parts 2-3: opener", note="Everyone has now finished Part 1 and crossed the line on the sheet.")

S("L-c", title="Parts 2 and 3: tasks",
  body='<div class="cols">\n<div class="left">\n\n2. Four nodes: write $x(t)$ with the eigenvalues, check $t = 2$\n\n3. Twelve nodes: run one cell, plot the second eigenvector\n\n</div>\n<div class="fig">\n<div class="ph">Left: the 4-node "diamond" network of Part 2. Right: QR code to the one-cell notebook of Part 3</div>\n</div>\n</div>',
  beat="Pen & Paper Parts 2-3: instructions", note="Part 2 can be done with a pencil only; Part 3 needs a laptop or a phone. Pair students if there are not enough devices.")

S("L-a", title=f"$x(t)$ = π + {hot('decaying')} terms",
  sub="Four nodes; eigenvalues $1,\\ 0,\\ -\\tfrac13,\\ -\\tfrac23$",
  ph=["The 4-node diamond network (degrees 2, 2, 3, 3) on the left. Right: bar charts of x(t) for t = 0, 1, 2, 5, 10 converging to pi = (0.2, 0.2, 0.3, 0.3). Under them the expansion: pi - 0.5 (0)^t psi_2 + 0 psi_3 + 0.3 (-2/3)^t psi_4, with the t = 2 line checked against x(2) = (1/3, 1/3, 1/6, 1/6)."],
  take=f"Only the term with $\\lambda = 1$ {hot('remains')}", beat="debrief Part 2", h=340,
  note="Check: x(1) = pi + 0.3 (-2/3) psi_4 = (0, 0, 0.5, 0.5). x(2) = (1/3, 1/3, 1/6, 1/6). The eigenvalue -2/3 alternates the sign: the walker hops between {0,1} and {2,3}, then settles. Eigenpairs are on the sheet, not computed by students.")

S("L-b", title=f"The second eigenvector separates the {hot('communities')}",
  ph=["Point plot: x = node index 0 to 11, y = second eigenvector of P (scaled to max 1). Nodes 0-5 on top (about +1; the bridge nodes 2 and 5 at about +0.74), nodes 6-11 on the bottom (about -1; 8 and 11 at -0.74). Community 1 cool, community 2 hot. A dashed line at 0. Callout: 'the sign gives the community'."],
  beat="debrief Part 3 (second eigenvector)", src="numpy, the sheet's one-cell code",
  note="The cell computes np.linalg.eig(P), orders by the real part, and plots column 1. The eigenvector of P (right) is constant inside each community by symmetry; sign is arbitrary, so the two communities may swap colours.")

S("L-a", title=f"Early on, the {hot('community')} signal dominates",
  sub="Walker starts at node 0",
  ph=["Line plot: x = steps (0 to 40), y = probability of being in community 1: 1.00, 1.00, 0.92, 0.88, 0.80 (t = 5), 0.67 (t = 10), 0.55 (t = 20), 0.505 (t = 40). A dashed curve 0.5 + 0.5 x 0.889^t over it. Callout at t about 3: 'the other eleven circles are gone'."],
  take=f"The community signal decays like $\\lambda_2^{{\\,t}}$. Degree remains.", beat="debrief Part 3 (what dominates early)", h=360,
  note="After about three steps, only two terms are left: the term with eigenvalue 1 (degree) and the one at 0.89 (the communities). The second decays on the time scale tau = 9. This is the bookend: short walks see communities, long walks see degree.")

S("L-g", title=None,
  ph=["Summary, three rows, each with a thumbnail of its figure: (1) the eigenvalue 1 = degree (thumb: scatter, slide 17). (2) The second eigenvalue = the communities, and its size determines the mixing time (thumb: gauge). (3) Short walks see communities; long walks see degree (thumb: the community-probability curve)."],
  beat="summary (claims with thumbnails)", note="Three claims, each pointing back at the picture that proved it. Then say what is next.", h=560)

S("L-f", title=f"Next: how long does it take to {hot('reach')} a node?",
  ph=["The opening picture again: the karate club, nodes shaded by long-run visits, with two nodes marked A and B"],
  beat="close: back to the opening picture, then a question for next time", h=300,
  note="Next time: hitting time, commute time, PageRank and Walktrap (see the lecture note). The close answers the opening picture; it never says 'Thank you'.")

# ============================================================================ render
CSS = """<style>
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
"""


def part_of(i):
    cur = None
    for p in PARTS:
        if p[0] <= i:
            cur = p
    return cur


def phs(sl):
    if sl["img"]:
        return f'<div class="fig">\n\n![]({sl["img"]})\n\n</div>\n\n'
    if not sl["ph"]:
        return ""
    cls = "ph live" if sl["live"] else "ph"
    boxes = "".join(f'<div class="{cls}">{t}</div>' for t in sl["ph"])
    hh = sl["h"]
    return f'<div class="fig">\n<div style="display:flex;width:100%;height:{hh}px">{boxes}</div>\n</div>\n\n'


def render_slide(i, sl):
    out = [f'<!-- _class: {sl["cls"]} -->', '<!-- _footer: "" -->', ""]
    if sl["opt"]:
        out += ['<div class="optflag">OPTIONAL</div>', ""]
    if sl["build"]:
        out += [f'<div class="buildflag">build {sl["build"][0]}/{sl["build"][1]}</div>', ""]
    if sl["cls"] == "lead":
        out += [f"# {sl['title']}", "", sl["body"]]
    elif sl["body"] is not None:
        if sl["title"]:
            out += [f"## {sl['title']}", ""]
        out += [sl["body"]]
        if sl["cue"]:
            out += ["", f'<div class="cue">{sl["cue"]}</div>']
    else:
        if sl["title"]:
            out += [f"## {sl['title']}", ""]
        if sl["sub"]:
            out += ['<div class="sub">', "", sl["sub"], "", "</div>", ""]
        out.append(phs(sl))
        if sl["take"]:
            out += ['<div class="take">', "", sl["take"], "", "</div>", ""]
        if sl["cue"]:
            out += [f'<div class="cue">{sl["cue"]}</div>', ""]
    notes = [f"[#{i}] beat: {sl['beat']}"]
    if sl["src"]:
        notes.append(f"source: {sl['src']}")
    if sl["ph"]:
        notes.append("figure: " + " / ".join(re.sub(r"<[^>]+>", "", t) for t in sl["ph"]))
    if sl["note"]:
        notes.append(sl["note"])
    out += ["<!--", "\n".join(notes), "-->"]
    return "\n".join(out)


FRONT = """---
marp: true
theme: house
paginate: true
math: katex
html: true
---

<!-- WIREFRAME v1 (M07 random walks). Dashed boxes = figures to be made; the text in each box says what goes there.
     Slide list and timing: review/DECK_SPEC.md. -->

"""

deck = FRONT + CSS + "\n" + "\n\n---\n\n".join(render_slide(i + 1, s) for i, s in enumerate(SLIDES)) + "\n"
open(os.path.join(OUT, "deck.md"), "w").write(deck)


def strip(t):
    return re.sub(r"<[^>]+>", "", t or "").replace("\n", " ")


rows, spine = [], []
for i, s in enumerate(SLIDES, 1):
    fig = strip(" / ".join(s["ph"])) if s["ph"] else ("(m06 figure reused)" if s["img"] else "")
    rows.append(f"| {i} | {s['cls']} | {strip(s['title']) or '(no title)'} | {s['beat']} | {fig[:140]} |")
    if s["cls"] == "L-f" and s["title"]:
        spine.append(strip(s["title"]))
    if s["cls"] in ("L-b", "L-a") and s["title"] and len(strip(s["title"])) > 40:
        print("title >40:", i, len(strip(s["title"])), strip(s["title"]))

lines = []
for pi, (start, name, mins) in enumerate(PARTS):
    end = PARTS[pi + 1][0] - 1 if pi + 1 < len(PARTS) else len(SLIDES)
    lines.append(f"| {name} | {start}-{end} | {end - start + 1} | {mins} |")
total = sum(m for _, _, m in PARTS)
builds = sum(1 for s in SLIDES if s["build"])

spec = f"""# DECK_SPEC: M07 Random Walks, the maths half (wireframe v1)

Stage 1 of 3: wireframe. Stage 2: real figures (one `smallgraphs.py` for every graph and number, `check()` asserting them).
Stage 3: polish. {len(SLIDES)} slides, of which {builds} are build steps and about 4 are optional or cut candidates.
Style: house (`theme.css` = `house/theme-house.css`). Layouts per HOUSE_STYLE section 8.

## Spine (the F slides, read alone)

{chr(10).join(f"{n}. {t}" for n, t in enumerate(spine, 1))}

## Time plan (about 90 minutes, Pen & Paper included)

| part | slides | count | minutes |
|---|---|---|---|
{chr(10).join(lines)}

Total {total} minutes. Over budget by about {total - 90} minutes at 1 minute per content slide: the builds take seconds, the three
Pen & Paper blocks are fixed. Slides flagged OPTIONAL are the cut candidates, in order: the bound slide, the answer to Q2 (two communities), the Q4 / A4 clique pair.

## Motifs (one picture per concept, back each time the concept is)

| concept | picture | colour | where it returns |
|---|---|---|---|
| the walker's rule | 7-node network, ring on the walker, 1/k labels | ink | slide 6, 50 |
| the drunkard (Pearson 1905) | pub, lamp post, paths, the cloud of end points | ink, pale paths | 2-4 |
| the real network | karate club in the live tool | tool's own | 7-9, 17, 51 |
| the two-community network (12 nodes) | two blocks, bridges 2-8 and 5-11 | community 1 cool, community 2 hot | 19-23, 26-30, 48-49 |
| eigenvalue, eigenvector | circle, tall bar, wide bar (M06) | u1 blue, u2 gold, rest pale | 24-30, 39, 42-44 |
| pi = degree / 2m | wide bar of shares, orange ticks of the tool | hot | 17, 44, 50 |

## Slide list

| # | layout | title | beat | figure |
|---|---|---|---|---|
{chr(10).join(rows)}
"""
os.makedirs(os.path.join(OUT, "review"), exist_ok=True)
open(os.path.join(OUT, "review", "DECK_SPEC.md"), "w").write(spec)
print(len(SLIDES), "slides,", builds, "build steps; spine:", len(spine))

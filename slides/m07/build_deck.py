#!/usr/bin/env python3
"""M07 random walks, the real deck (v2, after the red-pen round on the wireframe): writes m07-random-walks.md
and review/DECK_SPEC.md from one slide list.

    python3 build_deck.py      (then: marp m07-random-walks.md --theme-set theme.css --html --allow-local-files)

Every figure is figures/<name>.png (figures/BRIEF.md says who draws what); a missing file stops the build.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLIDES, PARTS = [], []


def part(name, minutes):
    PARTS.append((len(SLIDES) + 1, name, minutes))


def hot(w):
    return f'<span class="hot">{w}</span>'


def img(name, w=1080, scrub=False, caption=None):
    cls = "fig scrub" if scrub else "fig"
    cap = f"\n<figcaption>{caption}</figcaption>" if caption else ""
    return f'<div class="{cls}">\n\n![w:{w}](figures/{name}.png){cap}\n\n</div>'


def S(cls, title=None, sub=None, fig=None, take=None, cue=None, beat="", note="", src="", opt=False, build=None,
      body=None, w=1080, scrub=False, sub_muted=False, caption=None, figs=(), ref=None):
    SLIDES.append(dict(cls=cls, title=title, sub=sub, fig=fig, take=take, cue=cue, beat=beat, note=note, src=src,
                       opt=opt, build=build, body=body, w=w, scrub=scrub, sub_muted=sub_muted, caption=caption, ref=ref,
                       figs=list(figs) + ([fig] if fig else [])))


def two_col(text, fig, w=537, cue=None, ref=None):
    c = f'\n\n<div class="cue">\n\n{cue}\n\n</div>' if cue else ""
    r = f'\n\n<div class="ref">{ref}</div>' if ref else ""
    return (f'<div class="cols">\n<div>\n\n{text}\n\n</div>\n<div class="fig">\n\n![w:{w}](figures/{fig}.png)\n\n</div>\n</div>' + r + c)


# ============================================================================ A. INTUITION
part("A  Intuition: Pearson's walker, then what a blind walker learns (Pen & Paper first)", 30)

S("lead", title="Random Walks", beat="title",
  body='<div class="eyebrow">Advanced Topics in Network Science · Module 07</div>\n\n<div class="credit">Sadamori Kojaku · Binghamton University</div>',
  note="About 90 minutes. The Pen & Paper sheet is worked in two blocks: the first right after slide 6 (before any maths, so the room finds the facts first), the second after the maths (the second eigenvector). 1 minute per content slide; builds take seconds.")

S("L-c", title="Where is the walker after 100 steps?", fig=None, beat="hook (story): Pearson's question, 1905",
  body=two_col("A man walks **1 yard**, turns in a random direction, and walks **1 yard** again. He repeats this 100 times.\n\nPearson asked this in *Nature* in 1905.", "pearson-walker",
               cue="Far from the start, or near it? Tell your neighbour.", ref="Pub: Jim Osley, CC BY-SA 2.0 (geograph.org.uk)"),
  figs=["pearson-walker"],
  src="K. Pearson, The Problem of the Random Walk, Nature 72, 294 (1905), doi:10.1038/072294b0. Check the wording against the original before quoting it.",
  note="Open with the history. In July 1905 the statistician Karl Pearson asked the readers of Nature: a man walks l yards, turns through any angle, walks l yards again, n times; where is he? The problem came from a question about how far mosquitoes spread (Pearson corresponded with Ronald Ross about malaria). A question slide: it never shows the answer. For the record: the typical distance after 100 steps is about 10 yards (the square root of 100); Rayleigh answered the next week that he had solved it in 1880, for waves. The room gets the next story instead.")

S("L-g", fig="polya", take=f"2D: the walker always comes home. 3D: only {hot('34%')} of walkers ever do.",
  beat="story: Polya's recurrence (2D returns, 3D does not)",
  src="G. Polya, Math. Annalen 84, 149 (1921). Return probability in 3D on the cubic lattice: 0.3405 (Polya's random walk constant). Figure: seeded walks, chosen for illustration; the numbers are asserted by simulation in figures/figs_a.py. The remark 'a drunk man will find his way home, but a drunk bird may get lost forever' is attributed to S. Kakutani; check before quoting it.",
  note="Start where Pearson stopped. Pearson asked where the walker is. Polya (1921) asked a different question: does the walker ever come back to where it started? On the street grid (2D) it comes back with probability 1, however long it takes. In space (3D) it comes back with probability about 0.34: two out of three drunken birds are lost for good. This is the first surprise about random walks: the answer depends on the dimension. On a network, the same question has an answer that depends on the shape of the network; the lecture's maths answers it for finite networks. (Pearson's answer, for the record: typical distance 10 yards, the square root of 100.)")

S("L-b", title="Random walks appear in many fields", fig="fields", beat="hook: the same walk in three fields",
  ref="Mosquito: CDC / James D. Gathany (public domain) · trajectory: Jean Perrin (public domain)",
  src="Pollen: Brown 1827, Einstein 1905, Perrin (Les atomes, 1913). PageRank: Page, Brin, Motwani, Winograd (1998). Check each year before the slide is final.",
  note="One idea, many fields. Verify the dates before the lecture: Brown 1827 (pollen); Einstein 1905 (the explanation); Perrin (the measurement that settled it); Page and Brin 1998. The arrow is the question for the next slide.")

S("L-f", title=f"How does it tell us about a {hot('network')}?", sub="But it is a “random” walk, right?", sub_muted=True,
  beat="spine 1: the question",
  note="The objection first: a random walk looks like noise. The answer of the whole lecture: the walker is a measuring instrument. It has no map, no destination and no memory, so what it does depends only on the network.")

S("L-b", title=f"What is a {hot('random walk')}?", fig="walk-rule", beat="mechanism: the rule",
  src="lecture-note/m07 fig-m07-net (redrawn in house style)",
  note="The only rule: divide the chance evenly among the edges. Four edges: 1/4 each. No memory of where it came from. This picture returns when P is introduced.")

S("L-f", title="Pen & Paper", sub="10 minutes · stop at the line on the sheet", beat="Pen & Paper: first block",
  note="Hand out the sheet. Part 1 is done now, before the lecture names anything. Students open the simulator (next slide), sketch how the visits correlate with degree over time, run 20,000 steps, read the most and the least visited node, compute degree ÷ share for both, and compute the one-step and three-step probabilities on the small drawn network. The sheet has a printed line: STOP, wait for the lecture. Walk around the room.")

S("L-c", beat="the simulator (QR code and link)",
  body='<div class="cols">\n<div>\n\n### Random walk simulator\n\n<code>skojaku.github.io/<br>adv-net-sci/assets/vis/<br>random-walks/index.html</code>\n\n</div>\n<div class="fig">\n\n![w:440](figures/qr-sim.png)\n\n</div>\n</div>',
  figs=["qr-sim"],
  note="The simulator is last term's tool, unchanged (lecture-note/assets/vis/random-walks/index.html). Default network: the karate club. ?dataFile=two-cliques.json loads two 5-cliques joined by one edge. No short link yet (go.skojaku.com/m07sim is not created): the QR code points at the full address.")

S("L-c", title="Two communities joined by one edge", beat="question to the room (Q2)",
  body=two_col("**How many steps**, on average, until the walker crosses to the other community?\n\nA: about 3\n\nB: about 20\n\nC: about 200", "two-comm-q", cue="Take a guess."),
  figs=["two-comm-q"],
  note="A question slide: it never shows the answer. Answer B. A walker in community 1 uses the bridge with chance 1/21 per step; it stays about 21 steps (k/2m: the bridge is used with probability 1/42 per step overall, and the walker is in community 1 half of the time). The students can check with the simulator: ?dataFile=two-cliques.json.")

S("L-b", title=f"A short walk stays in its {hot('community')}", fig="two-comm-walk", opt=True, beat="answer to Q2",
  note="Short walks remember the community they started in. Long runs of one colour: about 21 steps each. This is the community signal we find in the second eigenvector.")

S("L-f", title=f"Short walks show {hot('communities')}. Long walks show {hot('degree')}. Why?", beat="spine 2: the mystery",
  note="The maths answers exactly this. First, what the sheet found about degree.")

S("L-a", title=f"Degree ÷ share is {hot('constant')}", sub="Karate club: 34 nodes, 78 edges, so 2m = 156", fig="degree-share",
  take=f"Share of time = degree ÷ {hot('2m')}", beat="debrief Part 1 (degree ÷ share)",
  note="The students' ratios scatter (node 11 is noisy: the ratio is a law of large numbers, not an identity of one run). The most visited node is 33 in about 3 runs out of 4 and node 0 otherwise; both give 156.")

# ============================================================================ B. MATHS
part("B  Maths: why the start stops mattering (matrices, circles, mixing time, eigenvalue 1)", 38)

S("L-f", title=f"Why does a long walk not depend on the {hot('start')}?", beat="spine 3: part question",
  note="From here: the maths, as pictures of vectors and matrices drawn as in the centrality lecture (circle = eigenvalue, column = vector).")

S("L-b", title=f"The walk is defined by {hot('one matrix')}", fig="P-def", beat="P (the two-community network, the motif of the rest of the lecture)",
  src="figures/smallgraphs.py (the same 12-node network as Part 3 of the sheet)",
  note="Introduce the 12-node two-community network that runs to the end and that the sheet uses in Part 3. Row i of P is the odds of leaving node i; rows sum to 1. Do not show the eigenvector yet. Convention: row vectors, as in the lecture note (P_ij = A_ij / k_i, x(t+1) = x(t) P).")

for k, (case, tk) in enumerate([
        ("x = e_0", "$x = (1, 0, 0, \\dots)$: $xP$ is the row of {n0}".format(n0="node 0")),
        ("x = e_1", "$x = (0, 1, 0, \\dots)$: $xP$ is the row of node 1"),
        ("x = a mix", "$x = (0.5, 0.05, \\dots)$: $xP$ is a mix of the rows")], 1):
    S("L-b", title=f"One step is a {hot('multiplication')} by $P$", fig=f"xP-{k}", take=tk,
      build=(k, 3), beat=f"x P, how to read it ({k}/3)", w=1080,
      note=f"Build {k}/3. {case}: the walker's distribution is a row vector; one step is the row times the square P. A walker certain to be at node 0 moves to the row of node 0 of P; with a mix, the new distribution is the mix of the rows. The same canvas on all three.")

S("L-a", title="After $t$ steps", sub="$x(t) = x(0)\\,P^{t}$", fig="xPt", beat="x(0) P^t",
  note="t steps are t multiplications by the same matrix. The next slides show P^t itself.")

S("L-b", title=f"Rows of $P^t$ {hot('after t steps')}", fig="Pt-slider", scrub=True, beat="P^t as a heat map (slider)",
  note="Use the slider under the figure (or the arrow keys): t from 1 to 40. t = 1: the two dense blocks, the walker stays in its community. t = 5: the blocks blur, the walker starts to leak. t = 40: every row is the same. The PNG export shows the last frame.")

S("L-b", title=f"Rows of $P^t$ at $t = 40$", fig="Pt-40", take=f"Every row becomes the same: {hot('π')}", beat="P^t, the numbers at t = 40",
  note="The same drawing as the slider's last frame, now with the numbers. Each row is where a walker starting at that node is after 40 steps; all twelve rows agree to two decimals. At t = 40 the worst start is about 0.01 from pi in the 1-norm.")

S("L-b", title="What each entry of $P^t$ says", fig="Pt-zoom", beat="zoom into P^t",
  note="Zoom in on one corner of P^5. Row = where the walker starts; column = where it is; the entry is the probability of being there after 5 steps.")

S("L-b", title="Recall: eigendecomposition", fig=None, beat="recap: eigendecomposition (M06, light touch)",
  body='<div class="fig">\n\n![w:1080](figures/m06-decomp-sum.png)\n\n</div>', figs=["m06-decomp-sum"],
  src="slides/m06/figures/decomp-sum.png (reused unchanged)",
  note="Two sentences only: circle = eigenvalue, column = eigenvector, row = its transpose. Do not re-derive; the room saw this for the adjacency matrix.")

S("L-a", title="$P$ has an eigendecomposition too", sub="$P = \\sum_k \\lambda_k\\,\\phi_k\\,\\psi_k^{\\top}$", fig="P-decomp",
  take=f"$P^t$ changes only the {hot('eigenvalues')}", beat="P as a sum of circles and bars",
  note="The bars multiply to 1 or 0 as in M06, so P^t = sum of lambda_k^t phi_k psi_k^T. For P the column (right eigenvector) and the row (left eigenvector) are two different vectors: each is the other rescaled by degree. Say it once; the appendix of the note has it.")

for k, (t, say) in enumerate([(1, "one step"), (5, "$\\lambda_2^5 = 0.56$"), (40, "only the circle at 1 is left")], 1):
    S("L-b", title=f"The eigenvalues {hot('shrink')} as $t$ grows", fig=f"Pt-circles-{k}", build=(k, 3),
      beat=f"P^t as circles ({k}/3)",
      note=f"Build {k}/3, t = {t}: {say}. Eigenvalues of the 12-node network (computed): 1, 0.889, 0, 0, 0, -0.088, -0.2, -0.2, -0.266, -0.333, -0.379, -0.423.")

S("L-c", title="Which term stays the longest?", beat="Q3 (which term stays the longest)",
  body=two_col("The 12 eigenvalues of $P$.\n\nAfter many steps, which term is still there?", "lam-curves-q", cue="Take 20 seconds."),
  figs=["lam-curves-q"],
  note="Each curve is |lambda_k|^t. The first (1) never decays. The question is about the last of those that die. Be explicit after the answer.")

S("L-c", title=f"The {hot('second')} term stays the longest", beat="A3",
  body=two_col("$\\lambda_2 = 0.89$\n\n$0.89^{t}$: 0.56 at $t = 5$, 0.31 at $t = 10$, 0.01 at $t = 40$", "lam-curves-a"),
  figs=["lam-curves-a"], note="Same figure as the question, with the answer added.")

for k, say in enumerate(["where you start matters at first (the lower line starts at a node with 6 friends, the upper at a node with 4 or 5); later every start follows the same slope, set by the second term",
                         "how close is close enough? epsilon = 1/2 in the 1-norm, which is 1/4 in total variation distance, the usual choice in the Markov chain literature",
                         "the mixing time: the first t at which every start is within the threshold"], 1):
    S("L-a", title=f"{hot('Mixing time')}",
      sub="$t_{\\mathrm{mix}} = \\min\\{\\,t : \\max_{x(0)} \\|x(t) - \\pi\\|_1 \\le \\epsilon\\,\\}$" if k == 3 else None,
      fig=f"mix-{k}", build=(k, 3), beat=f"mixing time ({k}/3)",
      note=f"Build {k}/3: {say}. One thin line per starting node, a black line for the worst start; Epsilon is a free choice; epsilon = 1/2 (1-norm) is the textbook 1/4 in total variation (total variation is half the 1-norm), and it gives t = 7 on this network. A smaller epsilon costs a few more relaxation times: see the table two slides after the clique questions. The formula appears only at the end, after the diagram has said it.")

S("L-a", title="Q: mixing time of a 10-clique?", sub="10 nodes, every pair connected (45 edges)", fig="clique-q", opt=True,
  cue="Take a guess: 1 step, 5 steps, 50 steps.", beat="Q4 (clique)",
  note="One graph per question. Answer: 1 step. lambda_2 = -1/9; the relaxation time is about 0.9 steps.")
S("L-a", title="A: about 1 step", sub="10 nodes, every pair connected (45 edges)", fig="clique-a", opt=True,
  take=f"$\\lambda_2 = -1/9$: mixing takes {hot('about 1 step')}", beat="A4")
S("L-a", title="Q: mixing time with one bridge?", sub="Two 5-cliques joined by one edge (21 edges)", fig="twoclique-q",
  cue="The same, 3 times longer, or 10 times longer?", beat="Q5 (two cliques)",
  note="The graph has fewer edges than the clique, and mixing takes 10 times longer. What matters is the bottleneck.")
S("L-a", title="A: about 10 times longer", sub="Two 5-cliques joined by one edge (21 edges)", fig="twoclique-a",
  take=f"$\\lambda_2 = 0.93$: mixing takes about {hot('10 steps')}", beat="A5",
  note="At epsilon = 1/2: 1 step for the clique, 10 for the bridged cliques. The relaxation time tau = 1/(1 - 0.927) = 13.8 against 0.9 (the lecture note's fifteen-fold).")

S("L-a", title=f"The {hot('relaxation time')}", sub="$\\tau = \\dfrac{1}{1-\\lambda_2}$", fig="relax-curve",
  take=f"The slowest term shrinks by a factor of $e$ in {hot('$\\tau$ steps')}", beat="relaxation time",
  note="The relaxation time is a property of the network alone: the time in which the slowest term, lambda_2^t, shrinks by a factor e (0.889^9 = 0.35, close to 1/e = 0.37). It is NOT the mixing time. The mixing time is the time until every start is within epsilon of pi, and it depends on epsilon.")

S("L-a", title=f"Small gap, long {hot('relaxation time')}", sub="$\\tau = \\dfrac{1}{1-\\lambda_2}$, the gap is $1-\\lambda_2$", fig="gap-gauge",
  take=f"The closer $\\lambda_2$ is to 1, the longer {hot('$\\tau$')}", beat="spectral gap (gauge)",
  note="'Spectral gap' = 1 - lambda_2. A bottleneck (two cliques and one edge, a ring) gives lambda_2 near 1 and a long relaxation time. tau is the lecture note's 1/(1 - lambda_2).")

S("L-a", title=f"{hot('Mixing time')} is a few $\\tau$", sub="A smaller $\\epsilon$ costs a few more $\\tau$", fig="tau-vs-mix",
  take="$t_{\\mathrm{mix}} < \\tau\\,\\log\\bigl(1/(\\epsilon\\,\\pi_{\\min})\\bigr)$", beat="mixing time versus relaxation time",
  note="Relaxation time and mixing time are two numbers. tau = 1/(1 - lambda_2) is a time scale of the network. The mixing time t_mix(epsilon) is the first t at which every start is within epsilon of pi. They are of the same order: the table shows t_mix at epsilon = 1/2 and at 0.05 next to tau. The bound in the lecture note pays for epsilon and for the rarest node inside the logarithm; it is an upper bound, not an equality. Do not derive it.")

S("L-f", title=f"One eigenvalue is always {hot('1')}. Others diminish.", beat="spine 4: the fact",
  note="Taught as a fact. The next three slides give a reason, in pictures, not a proof.")

S("L-b", title=f"Why 1? Every row of $P$ sums to {hot('1')}", fig="P1-eq-1", beat="lambda = 1 exists (P 1 = 1)",
  note="P times the vector of ones is the vector of ones, because each row of P is a list of odds that adds to 1. A vector that P does not change. (The walker's own stationary distribution is the matching LEFT eigenvector; the next slides.)")

S("L-a", title=f"No eigenvalue is {hot('larger')} than 1", sub="$Pf$ gives each node the average of its neighbours' values", fig="no-larger",
  take="The largest value can only shrink, so $\\lambda \\le 1$", beat="no eigenvalue above 1",
  note="Take a vector f with P f = lambda f, and look at the node i where |f| is largest. P f gives node i the average of its neighbours' values. An average of numbers that are at most f_i in size is at most f_i in size. So |lambda| f_i <= f_i, that is |lambda| <= 1. The drawing uses a node holding the largest number, 9: its new number is the average of its neighbours, 6.")

S("L-a", title="Detailed balance condition", sub="$\\Pr(i \\to j) = \\Pr(j \\to i)$", fig="detailed-balance",
  take=f"$\\pi_i = k_i / 2m$: proportional to {hot('degree')}", beat="the eigenvalue 1 gives pi (ties to the simulator's ticks)",
  note="Detailed balance: when the walkers are spread as pi, the chance that a walker is at i and steps to j equals the chance that a walker is at j and steps to i: pi_i P_ij = pi_j P_ji. Here Pr(i -> j) means that joint event, not the conditional P_ij. With P_ij = 1/k_i and P_ji = 1/k_j this reads pi_i / k_i = pi_j / k_j for every edge, so pi is proportional to the degree k_i, and the total is 2m: pi_i = k_i / 2m. That is why the bars of the simulator settled on their k/2m ticks and why degree ÷ share = 2m on the sheet.")

# ============================================================================ C. PEN & PAPER 2, 3
part("C  Pen & Paper, then debrief", 20)

S("L-f", title="Pen & Paper", sub="10 minutes · plot the second eigenvector", beat="Pen & Paper: second block",
  note="Everyone has finished the first block and crossed the line on the sheet. This block: twelve nodes, run one cell, plot the second eigenvector (a laptop or a phone; pair students if there are not enough devices). The QR code and link of the notebook come with the sheet. The four-node exercise (the diamond) is not used on the slides any more.")

S("L-b", title=f"$x(t) = \\pi\\,+$ {hot('decaying')} terms",
  body='<div class="cols" style="gap: 36px;">\n<div class="fig">\n\n![w:756](figures/eigvec2.png)\n\n</div>\n<div style="flex: 0 0 250px; text-align: left; font-size: 30px; line-height: 1.4;">\n\nThe slowest decaying term is the **second eigenvector**.\n\nPositive: one community. Negative: the other.\n\n</div>\n</div>',
  figs=["eigvec2"], beat="debrief Part 3 (second eigenvector; the expansion)",
  src="numpy, the sheet's one-cell code",
  note="x(t) = pi + sum over k >= 2 of c_k lambda_k^t psi_k: the walker's distribution is pi plus terms that decay. The slowest decaying term is the one with lambda_2 = 0.89, and its eigenvector is the plot: nodes 0-5 on one side of zero, nodes 6-11 on the other. The sheet's cell computes np.linalg.eig(P), orders by the real part, and plots column 1. The sign itself is arbitrary, so the two communities may swap colours on a student's screen.")

S("L-a", title=f"Early on, the {hot('community')} signal dominates", sub="Walker starts at node 0", fig="comm-curve",
  take="The community signal decays like $\\lambda_2^{\\,t}$. Degree remains.", beat="debrief Part 3 (what dominates early)",
  note="After about three steps only two terms are left: the one with eigenvalue 1 (degree) and the one at 0.89 (the communities). The second decays on the scale tau = 9. The bookend: short walks see communities, long walks see degree.")

S("L-g", fig="summary", beat="summary (claims with thumbnails)",
  note="Three claims, each pointing back at the picture that showed it. Next lecture: how long a walker takes to reach a node (hitting time), PageRank and Walktrap.")

# ============================================================================ render
FRONT = """---
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

"""


def render_slide(i, sl):
    out = [f'<!-- _class: {sl["cls"]} -->', '<!-- _footer: "" -->', ""]
    if sl["cls"] == "L-g" or sl["cls"] == "lead":
        pass
    if sl["opt"]:
        out += ['<div class="optflag">OPTIONAL</div>', ""]
    if sl["cls"] == "lead":
        out += [f"# {sl['title']}", "", sl["body"]]
    elif sl["body"] is not None:
        if sl["title"]:
            out += [f"## {sl['title']}", ""]
        out += [sl["body"]]
    else:
        if sl["title"]:
            out += [f"## {sl['title']}", ""]
        if sl["sub"]:
            klass = "sub muted" if sl["sub_muted"] else "sub"
            out += [f'<div class="{klass}">', "", sl["sub"], "", "</div>", ""]
        if sl["fig"]:
            out += [img(sl["fig"], sl["w"], sl["scrub"], sl["caption"]), ""]
        if sl["ref"]:
            out += [f'<div class="ref">{sl["ref"]}</div>', ""]
        if sl["take"]:
            out += ['<div class="take">', "", sl["take"], "", "</div>", ""]
        if sl["cue"]:
            out += ['<div class="cue">', "", sl["cue"], "", "</div>", ""]
    notes = [f"[#{i}] beat: {sl['beat']}"]
    if sl["src"]:
        notes.append(f"source: {sl['src']}")
    if sl["note"]:
        notes.append(sl["note"])
    out += ["<!--", "\n".join(notes), "-->"]
    return "\n".join(out)


def main():
    missing = sorted({f for sl in SLIDES for f in sl["figs"] if not os.path.exists(os.path.join(HERE, "figures", f + ".png"))})
    if missing and "--allow-missing" not in sys.argv:
        print("missing figures:", ", ".join(missing))
        sys.exit(1)
    deck = FRONT + "\n\n---\n\n".join(render_slide(i + 1, s) for i, s in enumerate(SLIDES)) + "\n"
    open(os.path.join(HERE, "m07-random-walks.md"), "w").write(deck)

    def strip(t):
        return re.sub(r"<[^>]+>", "", t or "").replace("\n", " ")

    rows, spine = [], []
    for i, s in enumerate(SLIDES, 1):
        rows.append(f"| {i} | {s['cls']} | {strip(s['title']) or '(no title)'} | {s['beat']} | {', '.join(s['figs'])} |")
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
    spec = f"""# DECK_SPEC: M07 Random Walks, the maths half (v2, after the red-pen round)

{len(SLIDES)} slides, {builds} of them build steps, 3 optional (the answer to Q2, the 10-clique pair). Style: house (`theme.css` = `house/theme-house.css`).
Figures: `figures/BRIEF.md` (who draws what); numbers: `figures/smallgraphs.py`. The P^t slider uses `scrub.js` (frames in `figures/frames/Pt-slider/`).

## Spine (the F slides, read alone)

{chr(10).join(f"{n}. {t}" for n, t in enumerate(spine, 1))}

## Time plan (about 90 minutes, Pen & Paper included)

| part | slides | count | minutes |
|---|---|---|---|
{chr(10).join(lines)}

Total {total} minutes. The Pen & Paper blocks (10 and 10 minutes) are fixed; the builds take seconds.

## Slide list

| # | layout | title | beat | figures |
|---|---|---|---|---|
{chr(10).join(rows)}
"""
    os.makedirs(os.path.join(HERE, "review"), exist_ok=True)
    open(os.path.join(HERE, "review", "DECK_SPEC.md"), "w").write(spec)
    print(len(SLIDES), "slides,", builds, "build steps; spine:", len(spine))


if __name__ == "__main__":
    main()

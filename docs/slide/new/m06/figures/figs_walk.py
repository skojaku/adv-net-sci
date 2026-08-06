#!/usr/bin/env python3
"""Parts 5 and 6 of the Module 06 deck: the recursion, power iteration, and Katz.

Everything numeric comes from `verify_numbers.py`.  Nothing here retypes a number a
slide states, and every figure asserts the arithmetic it prints before it is drawn.

Three things in this file are worth reading before changing it.

**The graphs that are not the Roman map.**  `romelib.py` owns the twelve-city
geometry and every metric slide reuses it; a second agent draws those.  The figures
here need graphs the map cannot give -- a node whose neighbours have visibly
different scores, a five-clique with a tail, a seven-node network small enough to
print a number beside every disc -- so they build their own, and each one is gated
by `F.assert_planar_drawing` (or, for the clique, by an asserted crossing count).

**`katz-floor` draws K5, so zero crossings is not available.**  `LOCAL` is a
five-clique with a four-node tail and K5 is the smallest non-planar graph: its
rectilinear crossing number is 1, so *one* crossing is the honest floor, not zero.
The layout below was found by a search that minimised crossings and then maximised
the distance between every edge and every disc it does not end at; the result is
frozen here and `fig_katz_floor` asserts both properties on every build.  Drawing
the offending chord as a curve would have hidden the crossing from `F.crossings`
rather than removed it, which is the trap FIGURE_GUIDE names.

**`power-step-*` shows step 4, and step 4 is not the eigenvector.**  The brief asked
for the final panel to match the leading eigenvector to 1e-3.  On a seven-node graph
that is only reachable when the all-ones start is already nearly the answer -- i.e.
when the graph is near-regular and every node scores about the same, which is the
one thing this figure must not show.  A search over 7-node connected planar graphs
found the trade-off explicitly: every candidate meeting 1e-3 at step 4 had at most
three distinct scores and four nodes tied at the top.  So the gate here is what the
figure actually claims: the two-decimal numbers printed at step 4 are exactly the
two-decimal numbers of the leading eigenvector, the residual is asserted below 0.01,
and step 4 prints that residual on the slide.
"""

import math
import re

import networkx as nx
import numpy as np

import figlib as F
from figlib import DASH, FONT, NODE, Axes, boxes_overlap, label_box
from verify_numbers import (KATZ_BAD_LAMBDA, KATZ_BAD_NEGATIVE, KATZ_CRITICAL, KATZ_SAFE,
                            LAMBDA2, LOCAL, LOCAL_CORE, LOCAL_KATZ_FRACTION,
                            LOCAL_TAIL_FRACTION, RATIO, ROMA, ROMA_C,
                            ROMA_KATZ_LAMBDA, ROMA_LMAX, katz_at, katz_series)

# Every figure in this file is a plain `.fig` (380px cap).  The page is authored 20bp
# taller than the cap so that a drawing which grows into its margin fails the height
# assertion with a number rather than the CLIP assertion with a mystery.
H = 400
INK_TOP = 380                       # nothing may be drawn above this

ROMA_NAMES = list(ROMA)
ROMA_A = nx.to_numpy_array(ROMA, nodelist=ROMA_NAMES)
ROMA_EVEC = np.array([ROMA_C["eigenvector"][n] for n in ROMA_NAMES])
ROMA_EVALS = np.linalg.eigvalsh(ROMA_A)


# --------------------------------------------------------------------------- helpers
def shade(t, base="accent", floor=0.16):
    """A white->colour fill at fraction t, as a TikZ colour expression.

    Floored the way romelib floors it: a pure-white disc reads as a hole in the
    drawing rather than as a node that scored nothing.
    """
    t = max(0.0, min(1.0, float(t)))
    return f"{base}!{int(round((floor + (1 - floor) * t) * 100))}"


_TEX = re.compile(r"\\[a-zA-Z]+|\\[,;!]|[${}^_]")


def visible(s):
    """What a label roughly occupies on the page, for the collision boxes.

    `label_box` counts characters and a TeX label is mostly markup: control words
    count as one glyph, braces/dollars/spacing count as none.  Measuring the raw
    string reported collisions that are not there.

    Line by line, because the `\\\\` that separates two lines is itself a backslash
    followed by a letter: run the substitution over the whole string and the break
    is eaten, `label_box` sees one line, and a two-line note measures as one 40-glyph
    line.  That is how the first pass reported the eigen-equation note as 1396bp wide.
    """
    return "\\\\".join(
        _TEX.sub(lambda m: "" if m.group(0)[0] in "${}^_" or len(m.group(0)) == 2
                 else "n", line)
        for line in s.split("\\\\"))


def curve_pts(ax, xs, ys, step=7.0):
    """A curve's drawn path, sampled every `step` bp, for the label checks."""
    pts = [ax.P(x, y) for x, y in zip(xs, ys) if ax.inside(x, y)]
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        out += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n)]
    return out + pts[-1:]


def fixed_label(spots, s, curves, boxes, color="black", anchor="center", size=FONT,
                pad=7, bounds=(8, 10, 1072, INK_TOP)):
    """A note at the first of `spots` clear of every curve and every other label.

    FIGURE_GUIDE, "place labels with a solver, not by hand": on a plot whose curves
    sweep the whole panel, "just above the line" is not a position.  Every offset
    chosen by eye here put at least one note straight through a curve.
    """
    why = []
    for x, y in spots:
        b = label_box(x, y, visible(s), anchor, size=size)
        if not (bounds[0] <= b[0] and b[2] <= bounds[2]
                and bounds[1] <= b[1] and b[3] <= bounds[3]):
            why.append(f"({x:.0f},{y:.0f}) off-page")
            continue
        if any(boxes_overlap(b, o) for o in boxes):
            why.append(f"({x:.0f},{y:.0f}) hits a label")
            continue
        on = [p for p in curves
              if b[0] - pad <= p[0] <= b[2] + pad and b[1] - pad <= p[1] <= b[3] + pad]
        if on:
            why.append(f"({x:.0f},{y:.0f}) sits on a curve at "
                       f"{on[0][0]:.0f},{on[0][1]:.0f}")
            continue
        boxes.append(b)
        return F.text(x, y, s, color=color, anchor=anchor, size=size)
    raise SystemExit(f"nowhere clear to put {s!r}: " + "; ".join(why))


def axis_titles(ax, xtitle, ytitle, ytx=100, xdrop=66):
    """Both axis titles placed by hand.

    `Axes.frame`'s own y title lands `2.6em` left of the spine, which is on top of a
    four-character tick label at the 36pt floor.
    """
    o = F.text((ax.x0 + ax.x1) / 2, ax.y0 - xdrop, xtitle, anchor="north")
    o += F.text(ytx, (ax.y0 + ax.y1) / 2, ytitle, rot=90)
    return o


def arrow(a, b, color="accent", w=F.EDGE_W, head=(20, 24)):
    """An arrow between two *named* TikZ nodes.

    `--` between node names stops at each node's border, whatever its shape, so the
    head meets the disc and the tail leaves it -- the defect class FIGURE_GUIDE says
    cannot be written in TikZ.  Computing a standoff by hand is what got it wrong in
    m01, four times.
    """
    return (f"\\draw[line width={w:.1f}bp,draw={color},"
            f"-{{Latex[length={head[0]}bp,width={head[1]}bp]}}] ({a}) -- ({b});\n")


# =============================================================================
# Part 5 -- the recursion
# =============================================================================
# A seven-node graph built for one job: the focal node's four neighbours must carry
# four *different* scores, so the arrows into it have four different widths.  Two
# feeder nodes (p, q) are drawn because they are the reason a and b differ; without
# them the four scores would look arbitrary.
FLOW_EDGES = [("p", "a"), ("q", "a"), ("q", "d"), ("a", "c"), ("b", "c"),
              ("d", "c"), ("c", "r"), ("a", "b")]
FLOW_POS = {"p": (80, 330), "q": (80, 130), "a": (330, 330), "b": (330, 230),
            "d": (330, 130), "c": (700, 230), "r": (980, 230)}
FLOW_FOCUS = "c"


def flow_steps():
    """Unnormalised power iteration on the flow graph.  Integers, so the sum is exact.

    Round t is `A^t 1`: the counts of t-step walks leaving each node.  Drawing round 2
    for the neighbours and round 3 for the focal node makes the figure's arithmetic
    literally true -- 9 + 8 + 6 + 4 = 27 -- which a normalised eigenvector cannot do,
    because there the sum is lambda times the score, not the score.
    """
    G = nx.Graph(FLOW_EDGES)
    names = sorted(G)
    A = nx.to_numpy_array(G, nodelist=names)
    x = np.ones(len(names))
    out = [dict(zip(names, x.astype(int)))]
    for _ in range(4):
        x = A @ x
        out.append(dict(zip(names, x.astype(int))))
    return G, out


def fig_recursive_flow():
    """Your score is the sum of your neighbours' scores.  One node, one update."""
    G, steps = flow_steps()
    assert set(G) == set(FLOW_POS) and G.number_of_edges() == len(FLOW_EDGES)
    F.assert_planar_drawing(FLOW_EDGES, FLOW_POS, "recursive-flow")

    have = steps[2]                      # what everyone is carrying
    nbrs = sorted(G[FLOW_FOCUS], key=lambda n: -have[n])
    total = steps[3][FLOW_FOCUS]
    assert total == sum(have[n] for n in nbrs), (total, [have[n] for n in nbrs])
    assert len({have[n] for n in nbrs}) == len(nbrs), \
        "the four arrows must carry four different widths"
    top = max(have[n] for n in nbrs)

    body = ""
    for a, b in FLOW_EDGES:
        if FLOW_FOCUS not in (a, b):
            body += F.seg(FLOW_POS[a], FLOW_POS[b], color="black")
    for n, (x, y) in FLOW_POS.items():
        if n == FLOW_FOCUS:
            body += (f"\\node[circle,draw=accenttwo,line width=4.5bp,fill=white,"
                     f"minimum size={NODE}bp,inner sep=0pt] (f{n}) at ({x},{y}) {{}};\n")
        else:
            body += F.disc(x, y, "", fill="accent", name=f"f{n}")
    for n in nbrs:
        body += arrow(f"f{n}", f"f{FLOW_FOCUS}", color="accent",
                      w=2.5 + 9.5 * have[n] / top)

    names = {n: f"{have[n]}" for n in FLOW_POS if n != FLOW_FOCUS}
    names[FLOW_FOCUS] = f"{total}"
    sides, boxes = F.place_labels(names, FLOW_POS, FLOW_EDGES,
                                  bounds=(12, 74, 1068, 366), gap=3.0)
    for n, (anc, dx, dy) in sides.items():
        body += F.text(FLOW_POS[n][0] + dx, FLOW_POS[n][1] + dy, names[n],
                       color="accenttwo" if n == FLOW_FOCUS else "black", anchor=anc)
    body += F.note("your new score $=$ the sum of your neighbours' scores",
                   (540, 46), color="accenttwo", anchor="center", boxes=boxes)
    F.emit("recursive-flow", body, container="full", h=H)


# --------------------------------------------------------------------------- A c = lambda c
MAT_CELL = 25
MAT_X0, MAT_Y0 = 44, 62


def fig_eigen_equation():
    """The twelve-by-twelve adjacency acting on c, and handing c back 3.35x bigger."""
    A = ROMA_A
    assert A.shape == (12, 12)
    assert (A == A.T).all() and np.trace(A) == 0
    assert int(A.sum()) == 2 * ROMA.number_of_edges() == 36
    for i, a in enumerate(ROMA_NAMES):
        for j, b in enumerate(ROMA_NAMES):
            assert bool(A[i, j]) == ROMA.has_edge(a, b), (a, b)
    lmax = f"{ROMA_LMAX:.2f}"
    assert abs(float(lmax) - 3.35) < 1e-9, lmax
    assert np.abs(A @ ROMA_EVEC - ROMA_LMAX * ROMA_EVEC).max() < 1e-9, \
        "the drawn vector must actually be the eigenvector"

    n = len(ROMA_NAMES)
    side = n * MAT_CELL
    body = ""
    filled = 0
    for i in range(n):
        for j in range(n):
            x = MAT_X0 + j * MAT_CELL
            y = MAT_Y0 + (n - 1 - i) * MAT_CELL       # row 0 at the top
            if A[i, j]:
                body += (f"\\fill[accent] ({x + 1.5},{y + 1.5}) rectangle "
                         f"({x + MAT_CELL - 1.5},{y + MAT_CELL - 1.5});\n")
                filled += 1
            body += (f"\\draw[line width=0.8bp,draw=annot!45] ({x},{y}) rectangle "
                     f"({x + MAT_CELL},{y + MAT_CELL});\n")
    assert filled == 36, filled
    body += (f"\\draw[line width=2.4bp,draw=black] ({MAT_X0},{MAT_Y0}) rectangle "
             f"({MAT_X0 + side},{MAT_Y0 + side});\n")

    def column(x):
        out = ""
        for i in range(n):
            y = MAT_Y0 + (n - 1 - i) * MAT_CELL
            out += (f"\\fill[{shade(ROMA_EVEC[i] / ROMA_EVEC.max())}] ({x},{y}) "
                    f"rectangle ({x + MAT_CELL},{y + MAT_CELL});\n")
            out += (f"\\draw[line width=0.8bp,draw=annot!45] ({x},{y}) rectangle "
                    f"({x + MAT_CELL},{y + MAT_CELL});\n")
        out += (f"\\draw[line width=2.4bp,draw=black] ({x},{MAT_Y0}) rectangle "
                f"({x + MAT_CELL},{MAT_Y0 + side});\n")
        return out

    mid = MAT_Y0 + side / 2
    body += column(MAT_X0 + side + 28)
    body += F.text(452, mid, "$=$", size=46)
    body += F.text(506, mid, "$\\lambda$", color="accenttwo", size=46)
    body += column(546)

    boxes = []
    for at, s, col, anchor in (((612, 262), f"$\\lambda = {lmax}$", "accenttwo", "west"),
                               ((612, 178),
                                f"same twelve numbers,\\\\every one {lmax}$\\times$ bigger",
                                "black", "west"),
                               ((612, 92), "filled cell $=$ a road", "annot", "west")):
        b = label_box(at[0], at[1], visible(s), anchor)
        hit = [i for i, o in enumerate(boxes) if boxes_overlap(b, o)]
        assert not hit, f"{s!r} collides with note {hit}"
        assert b[2] <= 1072, f"{s!r} runs off the page at x={b[2]:.0f}"
        boxes.append(b)
        body += F.text(at[0], at[1], s, color=col, anchor=anchor)
    F.emit("eigen-equation", body, container="full", h=H)


# --------------------------------------------------------------------------- spectrum
def fig_spectrum():
    """Twelve eigenvalues on a line, and only one of them has a positive eigenvector."""
    w, V = np.linalg.eigh(ROMA_A)
    assert len(w) == 12
    assert abs(w[-1] - ROMA_LMAX) < 1e-12
    assert len(set(np.round(w, 6))) == 12, "the drawn spectrum has a repeated eigenvalue"
    lead = V[:, -1] * np.sign(V[:, -1].sum())
    assert lead.min() > 0, "the leading eigenvector must be all-positive"
    for i in range(11):
        v = V[:, i]
        assert v.min() < -1e-9 < 1e-9 < v.max(), \
            f"eigenvector {i} has one sign -- Perron-Frobenius says only the leading one does"
    shown = f"{ROMA_LMAX:.2f}"

    lo, hi = -3.1, 3.7
    x0, x1, axis = 70, 1040, 150

    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    body = F.seg((x0, axis), (x1, axis), color="black", w=2.6)
    for t in range(-3, 4):
        body += F.seg((X(t), axis), (X(t), axis - 11), color="black", w=2.2)
        body += F.text(X(t), axis - 20, f"${t}$", anchor="north")
    for v in w[:-1]:
        body += F.seg((X(v), axis), (X(v), axis + 46), color="annot", w=4.0)
    body += F.seg((X(w[-1]), axis), (X(w[-1]), axis + 82), color="accenttwo", w=7.0)

    boxes = []
    for at, s, col, anchor in (
            ((X(w[-1]) - 14, 250), f"$\\lambda_{{\\max}} = {shown}$", "accenttwo", "east"),
            ((94, 250), "twelve eigenvalues of $A$", "annot", "west"),
            ((540, 62), "only $\\lambda_{\\max}$ has an all-positive eigenvector",
             "black", "north")):
        b = label_box(at[0], at[1], visible(s), anchor)
        assert not any(boxes_overlap(b, o) for o in boxes), f"{s!r} collides"
        assert 8 <= b[0] and b[2] <= 1072, f"{s!r} runs off the page"
        boxes.append(b)
        body += F.text(at[0], at[1], s, color=col, anchor=anchor)
    F.emit("spectrum", body, container="full", h=H)


# --------------------------------------------------------------------------- decay
DECAY_FRAME = (250, 168, 1050, 372)


def fig_decay():
    """Every other mode dies as |lambda_i/lambda_1|^t.  The slowest sets the speed."""
    w = np.sort(ROMA_EVALS)
    ratios = sorted(abs(v) / w[-1] for v in w[:-1])
    slow = max(ratios)
    assert abs(slow - RATIO) < 1e-12, (slow, RATIO)
    assert abs(LAMBDA2 - abs(w[0])) < 1e-9, \
        "on this graph the slowest mode is the most NEGATIVE eigenvalue"
    assert abs(w[0]) > w[-2], \
        f"|lambda_min| = {abs(w[0]):.3f} must beat lambda_2 = {w[-2]:.3f}, or the " \
        f"label quotes {w[-2] / w[-1]:.2f} for a process that converges at {slow:.2f}"
    assert len(ratios) == 11, len(ratios)
    shown = f"{slow:.3f}"

    ax = Axes(DECAY_FRAME, (0, 20), (0, 1), xticks=[0, 5, 10, 15, 20],
              yticks=[0, 0.25, 0.5, 0.75, 1], yfmt=lambda v: f"{v:g}")
    ts = np.linspace(0, 20, 201)
    body = ax.frame()
    body += axis_titles(ax, "power-iteration steps $t$", "$|\\lambda_i/\\lambda_1|^t$")
    drawn = []
    for r in ratios:
        ys = r ** ts
        hot = r == slow
        body += ax.line(ts, ys, color="accenttwo" if hot else "annot",
                        w=5.0 if hot else 2.6)
        drawn += curve_pts(ax, ts, ys)

    boxes = []
    body += fixed_label([(ax.X(8.6), ax.Y(0.46)), (ax.X(9.6), ax.Y(0.52))],
                        f"slowest mode\\\\{shown}", drawn, boxes, color="accenttwo",
                        anchor="west")
    body += fixed_label([(ax.X(11.2), ax.Y(0.86)), (ax.X(10.4), ax.Y(0.9))],
                        "the other ten modes", drawn, boxes, color="annot",
                        anchor="west")
    F.emit("decay", body, container="full", h=H)


# --------------------------------------------------------------------------- walks
# Six nodes, seven edges, built so that three different 3-step walks land on T by
# three visibly different routes.  Drawn three times because three highlighted walks
# on one copy is three colours and a legend.
WALK_EDGES = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d"), ("d", "e"),
              ("d", "T"), ("e", "T")]
WALK_POS = {"a": (10, 110), "b": (95, 210), "c": (95, 10), "d": (185, 110),
            "e": (270, 210), "T": (270, 10)}
WALKS = [("a", "b", "d", "T"), ("a", "c", "d", "T"), ("b", "d", "e", "T")]
WALK_OX = (40, 400, 760)
WALK_OY = 115


def fig_walks_arrive():
    """A^t counts walks, so a high score means many walks end on you."""
    G = nx.Graph(WALK_EDGES)
    assert set(G) == set(WALK_POS)
    F.assert_planar_drawing(WALK_EDGES, WALK_POS, "walks-arrive")
    for wk in WALKS:
        assert len(wk) == 4 and wk[-1] == "T"
        for u, v in zip(wk, wk[1:]):
            assert G.has_edge(u, v), f"{u}-{v} is not an edge: {wk} is not a walk"
    assert len({tuple(wk) for wk in WALKS}) == 3

    names = sorted(G)
    A = nx.to_numpy_array(G, nodelist=names)
    arriving = int(round(np.linalg.matrix_power(A, 3)[:, names.index("T")].sum()))
    assert arriving == 14, arriving

    body = ""
    for k, (ox, wk) in enumerate(zip(WALK_OX, WALKS)):
        pos = {n: (x + ox, y + WALK_OY) for n, (x, y) in WALK_POS.items()}
        for a, b in WALK_EDGES:
            body += F.seg(pos[a], pos[b], color="annot", w=2.4)
        for n, (x, y) in pos.items():
            body += F.disc(x, y, "", fill="accent", name=f"w{k}{n}")
        body += F.ring(*pos["T"], size=NODE, color="accenttwo", w=4.5, grow=13)
        for u, v in zip(wk, wk[1:]):
            body += arrow(f"w{k}{u}", f"w{k}{v}", color="accenttwo", w=6.0,
                          head=(18, 22))
    body += F.note(f"three of the ${arriving}$ 3-step walks ending at the ring",
                   (540, 62), color="accenttwo", anchor="center")
    F.emit("walks-arrive", body, container="full", h=H)


# --------------------------------------------------------------------------- power iteration
# Seven nodes: a triangle with a two-node arm on each of two corners.  Chosen from a
# search over connected planar 7-node graphs (see the module docstring) because at
# step 1 the three degree-2 nodes are tied at 0.67 and by step 4 the one inside the
# triangle has pulled away to 0.85 -- which is the whole argument of Part 5 in one
# picture, and cannot be said with degree.
BOW_EDGES = [("A", "B"), ("A", "P"), ("A", "M"), ("L", "M"),
             ("B", "P"), ("B", "N"), ("R", "N")]
BOW_POS = {"L": (60, 150), "M": (216, 150), "A": (372, 150), "P": (556, 300),
           "B": (740, 150), "N": (896, 150), "R": (1040, 150)}
BOW_ORDER = ["L", "M", "A", "P", "B", "N", "R"]
POWER_STEPS = (0, 1, 2, 4)


def bow_trace(steps=40):
    G = nx.Graph(BOW_EDGES)
    A = nx.to_numpy_array(G, nodelist=BOW_ORDER)
    x = np.ones(len(BOW_ORDER))
    out = [x / x.max()]
    for _ in range(steps):
        x = A @ x
        out.append(x / x.max())
    w, V = np.linalg.eigh(A)
    v = np.abs(V[:, -1])
    return G, out, v / v.max()


def fig_power_step(step):
    """One frame of power iteration on the bowtie: everyone starts at 1."""
    G, trace, lead = bow_trace()
    assert set(G) == set(BOW_POS) and nx.is_connected(G)
    F.assert_planar_drawing(BOW_EDGES, BOW_POS, f"power-step-{step}")

    val = trace[step]
    printed = [f"{v:.2f}" for v in val]
    final = trace[POWER_STEPS[-1]]
    resid = float(np.abs(final - lead).max())
    # The figure never claims step 4 IS the eigenvector -- it prints step 4 and prints
    # how far that is from the answer.  See the module docstring for why 1e-3 is not
    # reachable on a seven-node graph whose scores are worth printing; 0.0093 is, and
    # the last panel says so on the slide.
    assert resid < 0.01, resid
    assert np.abs(trace[-1] - lead).max() < 1e-6, "the iteration must actually converge"
    # The point of the figure, asserted: degree cannot separate P from M and N, and
    # four rounds of the recursion can.
    iP, iM, iN = (BOW_ORDER.index(n) for n in ("P", "M", "N"))
    assert G.degree("P") == G.degree("M") == G.degree("N") == 2
    tied = printed[iP] == printed[iM] == printed[iN]
    assert tied == (step <= 1), (
        f"step {step}: the three degree-2 nodes read {printed[iP]}, {printed[iM]}, "
        f"{printed[iN]} -- they must tie while the score is still degree and split "
        f"once the recursion has run")
    if step == 1:
        deg = np.array([G.degree(n) for n in BOW_ORDER], float)
        assert np.abs(val - deg / deg.max()).max() < 1e-12, "step 1 is degree, exactly"

    body = ""
    for a, b in BOW_EDGES:
        body += F.seg(BOW_POS[a], BOW_POS[b], color="black")
    for i, n in enumerate(BOW_ORDER):
        body += F.disc(*BOW_POS[n], "", fill=shade(val[i]))

    names = {n: printed[i] for i, n in enumerate(BOW_ORDER)}
    sides, boxes = F.place_labels(names, BOW_POS, BOW_EDGES,
                                  bounds=(8, 62, 1072, 374), gap=3.0)
    body += F.draw_labels(names, BOW_POS, sides)
    body += F.note(f"step ${step}$", (24, 34), color="accenttwo", anchor="west",
                   boxes=boxes)
    if step == POWER_STEPS[-1]:
        body += F.note(f"every value within ${resid:.3f}$ of the eigenvector",
                       (1056, 34), color="accenttwo", anchor="east", boxes=boxes)
    F.emit(f"power-step-{step}", body, container="full", h=H)


# =============================================================================
# Part 6 -- Katz
# =============================================================================
# LOCAL is a five-clique with a four-node tail, so the drawing contains K5 and cannot
# be planar.  These coordinates came out of a search that fixed c1 (the node the tail
# hangs from) and moved the other four to minimise crossings first and then maximise
# the distance from every edge to every disc it does not end at.  Both properties are
# re-asserted on every build, so a "tidying" edit that costs a crossing fails here.
LOCAL_XY = {
    "c1": (285.0, 180.0), "c2": (175.7, 160.9), "c3": (46.3, 315.0),
    "c4": (44.8, 45.0), "c5": (82.9, 213.8),
    "t1": (430.0, 180.0), "t2": (590.0, 180.0), "t3": (750.0, 180.0),
    "t4": (910.0, 180.0),
}
LOCAL_DRAW_EDGES = [(a, b) for a, b in LOCAL.edges()]
K5_CROSSING_NUMBER = 1


def fig_katz_floor():
    """The same tail node, lifted off the floor by Katz's beta."""
    assert set(LOCAL_XY) == set(LOCAL), sorted(set(LOCAL_XY) ^ set(LOCAL))
    assert LOCAL.subgraph(LOCAL_CORE).number_of_edges() == 10, "the core must be K5"
    x = F.crossings(LOCAL_DRAW_EDGES, LOCAL_XY)
    assert len(x) == K5_CROSSING_NUMBER, (
        f"katz-floor: {len(x)} crossings -- K5's rectilinear crossing number is "
        f"{K5_CROSSING_NUMBER}, so that is the floor, and more than that is a defect: {x}")
    bad = F.clearance_bad(LOCAL_DRAW_EDGES, LOCAL_XY, r=NODE / 2 + 8)
    assert not bad, f"katz-floor: edge passes through a disc it does not end at -- {bad}"

    scores = katz_at(LOCAL, KATZ_SAFE / _local_lmax())
    top = max(scores.values())
    frac = scores["t4"] / top
    assert abs(frac - LOCAL_KATZ_FRACTION) < 1e-9, (frac, LOCAL_KATZ_FRACTION)
    assert LOCAL_TAIL_FRACTION < 0.02 < LOCAL_KATZ_FRACTION
    katz_txt, eig_txt = f"{LOCAL_KATZ_FRACTION:.3f}", f"{LOCAL_TAIL_FRACTION:.4f}"
    assert katz_txt == "0.184" and eig_txt == "0.0045", (katz_txt, eig_txt)

    body = ""
    for a, b in LOCAL_DRAW_EDGES:
        body += F.seg(LOCAL_XY[a], LOCAL_XY[b], color="black")
    for n, (px, py) in LOCAL_XY.items():
        body += (f"\\draw[line width=1.8bp,draw=black,fill={shade(scores[n] / top)}] "
                 f"({px},{py}) circle ({NODE / 2}bp);\n")

    boxes = []
    for at, s, col, anchor in (
            ((1058, 296), f"Katz  ${katz_txt}$\\\\eigenvector  ${eig_txt}$",
             "accenttwo", "east"),
            ((470, 78), "darker $=$ higher Katz", "annot", "west")):
        b = label_box(at[0], at[1], visible(s), anchor)
        assert not any(boxes_overlap(b, o) for o in boxes), f"{s!r} collides"
        assert 8 <= b[0] and b[2] <= 1072 and b[3] <= INK_TOP, f"{s!r} off the page"
        assert not any(F.box_hits_disc(b, *p) for p in LOCAL_XY.values()), \
            f"{s!r} sits on a disc"
        boxes.append(b)
        body += F.text(at[0], at[1], s, color=col, anchor=anchor)
    body += F.seg((910, 250), (910, 204), color="accenttwo", w=3.0)
    F.emit("katz-floor", body, container="full", h=H)


def _local_lmax():
    A = nx.to_numpy_array(LOCAL, nodelist=list(LOCAL))
    return float(np.linalg.eigvalsh(A)[-1])


# --------------------------------------------------------------------------- the solve
def _katz_rows(final):
    """The two (or three) lines of the rearrangement, as (y, text, colour, gloss)."""
    rows = [(330, "$c = \\beta\\mathbf{1} + \\lambda A c$", "black", None),
            (170, "$(I - \\lambda A)\\,c = \\beta\\mathbf{1}$", "black",
             "$c$ on one side")]
    if final:
        rows.append((62, "$c = \\beta\\,(I - \\lambda A)^{-1}\\mathbf{1}$", "accenttwo",
                     "one linear solve"))
    return rows


def _katz_solve_body(final):
    body, boxes = "", []
    for y, s, col, gloss in _katz_rows(final):
        b = label_box(180, y, visible(s), "west", size=46)
        assert not any(boxes_overlap(b, o) for o in boxes), f"{s!r} collides"
        boxes.append(b)
        body += F.text(180, y, s, color=col, anchor="west", size=46)
        if gloss:
            g = label_box(1058, y, visible(gloss), "east")
            assert not boxes_overlap(b, g), f"{s!r} runs into its gloss -- shorten it"
            assert g[0] >= 8, f"{gloss!r} runs off the page"
            boxes.append(g)
            body += F.text(1058, y, gloss, color="annot", anchor="east")
    # The two annotations under the first line: what the floor is, and what the
    # recursion is.  Each has a leader to its own term, so neither can be read as
    # naming the whole equation.
    body += F.seg((306, 300), (200, 278), color="accenttwo", w=2.6)
    body += F.seg((458, 300), (700, 278), color="accent", w=2.6)
    for at, s, col, anchor in (((30, 246), "$\\beta$: a floor for everyone",
                                "accenttwo", "west"),
                               ((1058, 246), "$\\lambda\\times$ your neighbours",
                                "accent", "east")):
        b = label_box(at[0], at[1], visible(s), anchor)
        assert not any(boxes_overlap(b, o) for o in boxes), f"{s!r} collides"
        assert 8 <= b[0] and b[2] <= 1072, f"{s!r} off the page"
        boxes.append(b)
        body += F.text(at[0], at[1], s, color=col, anchor=anchor)
    return body


def fig_katz_solve_1():
    """The fixed point: a floor, plus a share of your neighbours."""
    F.emit("katz-solve-1", _katz_solve_body(False), container="full", h=H)


def fig_katz_solve_2():
    """...and it is linear, so it is one solve."""
    F.emit("katz-solve-2", _katz_solve_body(True), container="full", h=H)


# --------------------------------------------------------------------------- the series
SERIES_TERMS = 4
SERIES_FRAME = (300, 150, 1040, 320)
SERIES_TICKS = ["$\\mathbf{1}$", "$\\lambda A\\mathbf{1}$",
                "$\\lambda^2 A^2\\mathbf{1}$", "$\\lambda^3 A^3\\mathbf{1}$"]


def series_totals():
    rows = katz_series(ROMA, ROMA_KATZ_LAMBDA, terms=SERIES_TERMS)
    return [float(term.sum()) for _, term, _ in rows]


def _series_body(upto):
    tot = series_totals()
    assert len(tot) == SERIES_TERMS
    assert abs(tot[0] - ROMA.number_of_nodes()) < 1e-12, tot[0]
    assert all(a > b for a, b in zip(tot, tot[1:])), f"the terms must shrink: {tot}"
    ratio = KATZ_SAFE
    assert abs(ratio - ROMA_KATZ_LAMBDA * ROMA_LMAX) < 1e-12
    assert ratio < 1.0

    ax = Axes(SERIES_FRAME, (-0.5, SERIES_TERMS - 0.5), (0, 14),
              xticks=list(range(SERIES_TERMS)), yticks=[0, 4, 8, 12],
              xfmt=lambda v: SERIES_TICKS[int(round(v))], yfmt=lambda v: f"{v:g}")
    body = ax.frame()
    body += F.text(126, (ax.y0 + ax.y1) / 2, "score added", rot=90)
    # The term names are the x tick labels, so they are blockers for everything else.
    boxes = [label_box(ax.X(t), ax.y0 - 17, visible(SERIES_TICKS[t]), "north")
             for t in range(SERIES_TERMS)]
    for t in range(upto):
        body += F.dot(*ax.P(t, tot[t]), color="accent", d=22)
        s = f"${tot[t]:.2f}$"
        b = label_box(ax.X(t), ax.Y(tot[t]) + 24, visible(s), "south")
        assert not any(boxes_overlap(b, o) for o in boxes), f"{s!r} collides"
        assert b[3] <= INK_TOP, f"{s!r} runs off the top"
        boxes.append(b)
        body += F.text(ax.X(t), ax.Y(tot[t]) + 24, s, anchor="south")
    note = (f"$\\lambda = {ROMA_KATZ_LAMBDA:.3f}$,  "
            f"$\\lambda\\lambda_{{\\max}} = {ratio:.2f} < 1$")
    nb = label_box(1050, 52, visible(note), "east")
    assert not any(boxes_overlap(nb, o) for o in boxes), "the lambda note collides"
    assert nb[0] >= 8, "the lambda note runs off the page"
    body += F.text(1050, 52, note, color="accenttwo", anchor="east")
    return body


def fig_katz_series(k):
    F.emit(f"katz-series-{k}", _series_body(k), container="full", h=H)


# --------------------------------------------------------------------------- the dial
LAM_LO = 0.15 / ROMA_LMAX
LAM_MID = ROMA_KATZ_LAMBDA
LAM_HI = 0.98 / ROMA_LMAX
DIAL_X = (340, 580, 820)
DIAL_Y = (288, 226, 164, 102)
DIAL_HEAD = 348


def dial_columns():
    cols = []
    for lam in (LAM_LO, LAM_MID, LAM_HI):
        k = katz_at(ROMA, lam)
        cols.append((lam, k, sorted(k, key=lambda n: (-k[n], n))))
    return cols


def fig_katz_dial():
    """Turning lambda moves the fourth place, and leaves the top three alone."""
    cols = dial_columns()
    tops = [order[:4] for _, _, order in cols]
    assert all(t[:3] == tops[0][:3] for t in tops), tops
    assert tops[0][3] == tops[1][3] == "Carthago", tops
    _, khi, order_hi = cols[2]
    assert order_hi[3] == "Athenae" and order_hi[4] == "Byzantium", order_hi[:6]
    assert abs(khi["Athenae"] - khi["Byzantium"]) < 1e-9, \
        "Athenae and Byzantium are the same node up to symmetry -- they cannot be split"
    assert order_hi.index("Carthago") == 5, order_hi
    shared = "Athenae\\\\Byzantium"
    moving = {"Carthago", "Athenae", "Byzantium"}

    body = ""
    # slope lines first, so the discs sit on top of them
    for c in range(2):
        for i, name in enumerate(tops[c]):
            if name not in tops[c + 1]:
                continue
            j = tops[c + 1].index(name)
            body += F.seg((DIAL_X[c] + 26, DIAL_Y[i]), (DIAL_X[c + 1] - 26, DIAL_Y[j]),
                          color="accenttwo" if name in moving else "accent", w=3.4)
    for c, top in enumerate(tops):
        for i, name in enumerate(top):
            body += F.disc(DIAL_X[c], DIAL_Y[i], "",
                           fill="accenttwo" if name in moving else "accent")

    boxes = []

    def put(at, s, col, anchor):
        b = label_box(at[0], at[1], visible(s), anchor)
        assert not any(boxes_overlap(b, o) for o in boxes), f"{s!r} collides"
        assert 8 <= b[0] and b[2] <= 1072 and b[3] <= INK_TOP, f"{s!r} off the page"
        assert not any(F.box_hits_disc(b, x, y) for x in DIAL_X for y in DIAL_Y), \
            f"{s!r} sits on a disc"
        boxes.append(b)
        return F.text(at[0], at[1], s, color=col, anchor=anchor)

    body += put((200, DIAL_HEAD), "$\\lambda$:", "annot", "east")
    for c, (lam, _, _) in enumerate(cols):
        body += put((DIAL_X[c], DIAL_HEAD), f"${lam:.3f}$", "annot", "center")
    for i, name in enumerate(tops[0]):
        body += put((DIAL_X[0] - 28, DIAL_Y[i]), name,
                    "accenttwo" if name in moving else "black", "east")
    body += put((DIAL_X[2] + 28, DIAL_Y[3]), shared, "accenttwo", "west")
    body += put((30, 40), "only 4th place moves", "accenttwo", "west")
    F.emit("katz-dial", body, container="full", h=H)


# --------------------------------------------------------------------------- divergence
DIVERGE_FRAME = (250, 168, 1050, 372)
DIVERGE_CITIES = ["Roma", "Mediolanum", "Tarraco", "Londinium"]
DIVERGE_XLIM = (0.10, 0.40)
DIVERGE_YLIM = (-25, 25)


def fig_katz_diverge():
    """Past 1/lambda_max the solve still returns numbers, and they are nonsense."""
    assert abs(KATZ_CRITICAL - 1 / ROMA_LMAX) < 1e-12
    assert DIVERGE_XLIM[0] < KATZ_CRITICAL < KATZ_BAD_LAMBDA < DIVERGE_XLIM[1]
    crit_txt, bad_txt = f"{KATZ_CRITICAL:.4f}", f"{KATZ_BAD_LAMBDA:.3f}"
    assert crit_txt == "0.2989" and bad_txt == "0.344", (crit_txt, bad_txt)

    bad = katz_at(ROMA, KATZ_BAD_LAMBDA)
    negatives = sorted(n for n, v in bad.items() if v < 0)
    assert negatives == KATZ_BAD_NEGATIVE and len(negatives) == 11, negatives
    just_over = katz_at(ROMA, KATZ_CRITICAL * 1.005)
    assert all(v < 0 for v in just_over.values()), \
        "immediately past the critical lambda every score must be negative"
    just_under = katz_at(ROMA, KATZ_CRITICAL * 0.995)
    assert all(v > 0 for v in just_under.values()), \
        "below the critical lambda every score must still be positive"

    ax = Axes(DIVERGE_FRAME, DIVERGE_XLIM, DIVERGE_YLIM,
              xticks=[0.1, 0.2, 0.3, 0.4], yticks=[-20, -10, 0, 10, 20],
              xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    body = ax.frame()
    body += axis_titles(ax, "$\\lambda$", "Katz score")
    body += F.seg((ax.x0, ax.Y(0)), (ax.x1, ax.Y(0)), color="annot", w=2.0)

    lo = np.linspace(DIVERGE_XLIM[0], KATZ_CRITICAL - 1e-4, 400)
    hi = np.linspace(KATZ_CRITICAL + 1e-4, DIVERGE_XLIM[1], 400)
    drawn = []
    for city in DIVERGE_CITIES:
        assert city in ROMA_NAMES, city
        for branch in (lo, hi):
            ys = np.array([katz_at(ROMA, lam)[city] for lam in branch])
            keep = (ys > DIVERGE_YLIM[0]) & (ys < DIVERGE_YLIM[1])
            body += ax.line(branch[keep], ys[keep], color="accent", w=3.4)
            drawn += curve_pts(ax, branch[keep], ys[keep])

    body += F.seg((ax.X(KATZ_CRITICAL), ax.y0), (ax.X(KATZ_CRITICAL), ax.y1),
                  color="accenttwo", w=3.4, dash=DASH)
    drawn += [(ax.X(KATZ_CRITICAL), y) for y in
              range(int(ax.y0), int(ax.y1), 6)]

    boxes = []
    body += fixed_label([(ax.X(KATZ_CRITICAL) + 14, 340),
                         (ax.X(KATZ_CRITICAL) + 14, 330)],
                        f"$1/\\lambda_{{\\max}} = {crit_txt}$", drawn, boxes,
                        color="accenttwo", anchor="west")
    body += fixed_label([(ax.x0 + 24, 210), (ax.x0 + 24, 226)],
                        f"at $\\lambda = {bad_txt}$: ${len(negatives)}$ of "
                        f"${ROMA.number_of_nodes()}$\\\\scores are negative",
                        drawn, boxes, color="accenttwo", anchor="west")
    body += fixed_label([(ax.x0 + 24, 348), (ax.x0 + 24, 336)], "four cities",
                        drawn, boxes, color="annot", anchor="west")
    F.emit("katz-diverge", body, container="full", h=H)


FIGURES = [
    ("recursive-flow", fig_recursive_flow),
    ("eigen-equation", fig_eigen_equation),
    ("spectrum", fig_spectrum),
    ("decay", fig_decay),
    ("walks-arrive", fig_walks_arrive),
] + [
    (f"power-step-{s}", (lambda s=s: fig_power_step(s))) for s in POWER_STEPS
] + [
    ("katz-floor", fig_katz_floor),
    ("katz-solve-1", fig_katz_solve_1),
    ("katz-solve-2", fig_katz_solve_2),
] + [
    (f"katz-series-{k}", (lambda k=k: fig_katz_series(k)))
    for k in range(1, SERIES_TERMS + 1)
] + [
    ("katz-dial", fig_katz_dial),
    ("katz-diverge", fig_katz_diverge),
]

#!/usr/bin/env python3
"""Parts 5 and 6 of the Module 06 deck: the recursion, power iteration, and Katz.

**Every figure here is authored for the 537 bp `cols` column**, because that is where
the deck puts them -- `![w:537]` on all eleven referenced figures, checked against
`m06-centrality.md`. A figure authored at 1080 and dropped into a 537 column renders
at 50% and takes its type down with it, which `check_render.py` fails.

Half the width is a re-composition, not a re-declaration: a wide slope chart or a
wide axis does not survive being halved. Four places where that changed the figure
rather than just its box:

**`eigen-equation` draws A as a block, not as 144 cells.** At 537 bp a 12x12 grid
gives 22 bp cells, under the 26 bp floor the deck holds every disc to, and shrinking
them is the one repair FIGURE_GUIDE forbids. The block states its own shape, and the
two facts behind it -- 12 by 12, 36 filled cells, one per road end -- are asserted
against `ROMA`'s real adjacency even though only the shape is drawn.

**`katz-floor` draws K5, so zero crossings is not available.** K5 is the smallest
non-planar graph and its rectilinear crossing number is 1, so one crossing is the
honest floor. The layout is the output of a search that minimised crossings first and
then maximised the distance from every edge to every disc it does not end at; both
are re-asserted on every build. Bending the offending chord would have hidden the
crossing from `F.crossings` rather than removed it, which is the trap FIGURE_GUIDE
names.

**`katz-dial` follows four named cities by rank, rather than drawing a top four.**
At 537 bp "Thessalonica" is 250 bp -- nearly half the column -- so one name per line
is the budget, and a top-four chart cannot say that at the largest lambda the fourth
place is *shared*: Athenae and Byzantium are the same node up to symmetry and tie at
every lambda, so drawing one of them in a "top four" and dropping the other would be
a false claim of the kind FIGURE_SPEC calls out for shared crowns. A rank axis says
the true thing instead -- Carthago falls 4th to 6th, Athenae climbs 6th to 4th, the
top three never move -- and each disc prints its own rank, so the axis needs no label.

**`power-step-*` shows step 4, and step 4 is not the eigenvector.** The brief asked
for 1e-3. On a seven-node graph that is only reachable when the all-ones start is
already nearly the answer -- i.e. when the graph is near-regular and every node
scores about the same, which is the one thing this figure must not show. A search
over connected planar 7-node graphs found every candidate meeting 1e-3 at step 4 had
at most three distinct scores and four nodes tied at the top. So the gate is what the
figure claims: the residual is asserted under 0.01 and the last panel prints it.
"""

import math
import re

import networkx as nx
import numpy as np

import figlib as F
from figlib import DASH, FONT, NODE, Axes, boxes_overlap, box_hits_segment, label_box
from verify_numbers import (KATZ_BAD_LAMBDA, KATZ_BAD_NEGATIVE, KATZ_CRITICAL, KATZ_SAFE,
                            LAMBDA2, LOCAL, LOCAL_CORE, LOCAL_KATZ_FRACTION,
                            LOCAL_TAIL_FRACTION, RATIO, ROMA, ROMA_C,
                            ROMA_KATZ_LAMBDA, ROMA_LMAX, katz_at, katz_series)

# The column is 537 bp and a plain `.fig` caps at 380 px, so after the crop's 12 bp of
# padding on each side the ink may be at most 356 bp tall. The page is authored taller
# than the cap so that a drawing which grows fails the height assertion, with a number,
# rather than the CLIP assertion, with a mystery.
W = 537
H = 400
INK_TOP = 380
BOUNDS = (8, 8, W - 8, INK_TOP)

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
    count as one glyph, braces/dollars/spacing count as none.

    Line by line, because the `\\\\` that separates two lines is itself a backslash
    followed by a letter: run the substitution over the whole string and the break is
    eaten, `label_box` sees one line, and a two-line note measures as one 40-glyph
    line 1396 bp wide. That is how the first pass mis-sized this module's notes.
    """
    return "\\\\".join(
        _TEX.sub(lambda m: "" if m.group(0)[0] in "${}^_" or len(m.group(0)) == 2
                 else "n", line)
        for line in s.split("\\\\"))


class Notes:
    """In-drawing notes, each checked against everything already on the page.

    A note is placed at a fixed spot while the drawing around it is computed, so a
    note that grows collides with whatever is there -- m03 wrote "every town is its
    own island" straight through the word "Znojmo". Every `put` asserts the box
    against the notes before it, the canvas bounds, the discs, the drawn edges and a
    sampled curve, and the failure message says which.
    """

    def __init__(self, discs=(), segs=(), curves=(), bounds=BOUNDS, pad=7):
        self.boxes = []
        self.discs = list(discs)
        self.segs = list(segs)
        self.curves = list(curves)
        self.bounds = bounds
        self.pad = pad

    def box(self, at, s, anchor="center", size=FONT, meas=None):
        # `meas` is the plain-TeX equivalent of `s`, for strings `visible()` cannot
        # measure: it drops control words but keeps their arguments, so the nine
        # letters of `\color{accenttwo}` counted as nine glyphs and a 340 bp equation
        # measured 820.
        return label_box(at[0], at[1], visible(meas if meas is not None else s),
                         anchor, size=size)

    def why(self, b, s):
        lo_x, lo_y, hi_x, hi_y = self.bounds
        if not (lo_x <= b[0] and b[2] <= hi_x and lo_y <= b[1] and b[3] <= hi_y):
            return (f"{s!r} runs off the page: box {tuple(round(v) for v in b)} "
                    f"outside {self.bounds} -- shorten it or move it")
        hit = [i for i, o in enumerate(self.boxes) if boxes_overlap(b, o)]
        if hit:
            return f"{s!r} collides with note {hit} -- shorten one of them"
        on = [p for p in self.discs if F.box_hits_disc(b, *p)]
        if on:
            return f"{s!r} sits on the disc at {on[0]}"
        seg = [e for e in self.segs if box_hits_segment(b, *e)]
        if seg:
            return f"{s!r} sits on the edge {seg[0]}"
        p = self.pad
        cur = [q for q in self.curves
               if b[0] - p <= q[0] <= b[2] + p and b[1] - p <= q[1] <= b[3] + p]
        if cur:
            return f"{s!r} sits on a curve at {cur[0][0]:.0f},{cur[0][1]:.0f}"
        return None

    def put(self, at, s, color="black", anchor="center", size=FONT, meas=None):
        b = self.box(at, s, anchor, size, meas)
        bad = self.why(b, s)
        assert bad is None, bad
        self.boxes.append(b)
        return F.text(at[0], at[1], s, color=color, anchor=anchor, size=size)

    def first(self, spots, s, color="black", anchor="center", size=FONT):
        """The first spot that is clear. Reports every rejection when none is."""
        why = []
        for at in spots:
            b = self.box(at, s, anchor, size)
            bad = self.why(b, s)
            if bad is None:
                self.boxes.append(b)
                return F.text(at[0], at[1], s, color=color, anchor=anchor, size=size)
            why.append(f"at {at}: {bad}")
        raise SystemExit(f"nowhere clear for {s!r}\n  " + "\n  ".join(why))

    def block(self, box):
        """Reserve a rectangle so later notes work around it."""
        self.boxes.append(box)


def curve_pts(ax, xs, ys, step=6.0):
    """A curve's drawn path, sampled every `step` bp, for the note checks."""
    pts = [ax.P(x, y) for x, y in zip(xs, ys) if ax.inside(x, y)]
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        out += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n)]
    return out + pts[-1:]


def axis_titles(ax, xtitle, ytitle, ytx, xdrop=62):
    """Both axis titles placed by hand.

    `Axes.frame`'s own y title sits 2.6 em left of the spine, which in a 537 bp
    column lands on top of a four-character tick label at the 36 pt floor.
    """
    o = F.text((ax.x0 + ax.x1) / 2, ax.y0 - xdrop, xtitle, anchor="north")
    o += F.text(ytx, (ax.y0 + ax.y1) / 2, ytitle, rot=90)
    return o


def tick_boxes(ax):
    """The frame's own tick labels, as blockers for everything placed afterwards."""
    out = []
    for v in ax.xticks:
        if ax.xlim[0] <= v <= ax.xlim[1]:
            out.append(label_box(ax.X(v), ax.y0 - 17, visible(ax.xfmt(v)), "north"))
    for v in ax.yticks:
        if ax.ylim[0] <= v <= ax.ylim[1]:
            out.append(label_box(ax.x0 - 17, ax.Y(v), visible(ax.yfmt(v)), "east"))
    return out


def arrow(a, b, color="accent", w=F.EDGE_W, head=(15, 18)):
    """An arrow between two *named* TikZ nodes.

    `--` between node names stops at each node's border, whatever its shape, so the
    head meets the disc and the tail leaves it -- the defect class FIGURE_GUIDE says
    cannot be written in TikZ. Computing the standoff by hand is what got it wrong in
    m01, four times.
    """
    return (f"\\draw[line width={w:.1f}bp,draw={color},"
            f"-{{Latex[length={head[0]}bp,width={head[1]}bp]}}] ({a}) -- ({b});\n")


def edge_pts(edges, pos):
    return [(pos[a], pos[b]) for a, b in edges]


# =============================================================================
# Part 5 -- the recursion
# =============================================================================
# Seven nodes built for one job: the focal node's four neighbours must carry four
# *different* scores, so the four arrows into it have four different widths. Two
# feeder nodes (p, q) are drawn because they are the reason a and b differ.
FLOW_EDGES = [("p", "a"), ("q", "a"), ("q", "d"), ("a", "c"), ("b", "c"),
              ("d", "c"), ("c", "r"), ("a", "b")]
FLOW_POS = {"p": (40, 330), "q": (40, 150), "a": (165, 330), "b": (165, 240),
            "d": (165, 150), "c": (320, 240), "r": (460, 240)}
FLOW_FOCUS = "c"


def flow_steps():
    """Unnormalised power iteration on the flow graph. Integers, so the sum is exact.

    Round t is `A^t 1`: the number of t-step walks leaving each node. Drawing round 2
    for the neighbours and round 3 for the focal node makes the arithmetic on the
    slide literally true -- 9 + 8 + 6 + 4 = 27 -- which a normalised eigenvector
    cannot do, because there the sum is lambda times the score, not the score.
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
    """Your score is the sum of your neighbours' scores. One node, one update."""
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
    # Every score is one digit, so it goes INSIDE its own disc. Placed beside the
    # discs by the solver, the "9" on node a landed halfway down the a-b edge and read
    # as if it belonged to b.
    assert all(have[n] < 10 for n in FLOW_POS if n != FLOW_FOCUS), have

    body = ""
    for a, b in FLOW_EDGES:
        if FLOW_FOCUS not in (a, b):
            body += F.seg(FLOW_POS[a], FLOW_POS[b], color="black")
    for n, (x, y) in FLOW_POS.items():
        if n == FLOW_FOCUS:
            body += (f"\\node[circle,draw=accenttwo,line width=4.5bp,fill=white,"
                     f"minimum size={NODE}bp,inner sep=0pt] (f{n}) at ({x},{y}) {{}};\n")
        else:
            body += F.disc(x, y, f"{have[n]}", fill="accent", name=f"f{n}")
    for n in nbrs:
        body += arrow(f"f{n}", f"f{FLOW_FOCUS}", color="accent",
                      w=2.2 + 7.0 * have[n] / top)

    names = {FLOW_FOCUS: f"{total}"}
    sides, boxes = F.place_labels(names, FLOW_POS, FLOW_EDGES,
                                  bounds=(10, 118, W - 10, 356), gap=3.0)
    body += F.draw_labels(names, FLOW_POS, sides, color="accenttwo")
    notes = Notes()
    for b in boxes.values():
        notes.block(b)
    body += notes.put((W / 2, 62), "new score $=$ sum of\\\\your neighbours' scores",
                      color="accenttwo")
    F.emit("recursive-flow", body, container="col", h=H)


# --------------------------------------------------------------------------- A c = lambda c
def fig_eigen_equation():
    """A acting on c and handing c back, 3.35 times bigger.

    At 537 bp a 12x12 grid is 22 bp per cell, under the 26 bp floor the deck holds
    every disc to, so A is drawn as a block that states its own shape. The adjacency
    is still checked here, cell by cell, against `ROMA`.
    """
    A = ROMA_A
    n = len(ROMA_NAMES)
    assert A.shape == (n, n) and n == 12
    assert (A == A.T).all() and np.trace(A) == 0
    assert int(A.sum()) == 2 * ROMA.number_of_edges() == 36
    for i, a in enumerate(ROMA_NAMES):
        for j, b in enumerate(ROMA_NAMES):
            assert bool(A[i, j]) == ROMA.has_edge(a, b), (a, b)
    lmax = f"{ROMA_LMAX:.2f}"
    assert abs(float(lmax) - 3.35) < 1e-9, lmax
    assert np.abs(A @ ROMA_EVEC - ROMA_LMAX * ROMA_EVEC).max() < 1e-9, \
        "the drawn vector must actually be the eigenvector"

    bx0, bx1, by0, by1 = 20.0, 180.0, 130.0, 280.0
    body = (f"\\fill[accent!14] ({bx0},{by0}) rectangle ({bx1},{by1});\n"
            f"\\draw[line width=3bp,draw=black] ({bx0},{by0}) rectangle "
            f"({bx1},{by1});\n")

    def column(x, w=25.0):
        """The score vector: twelve cells, shaded by the eigenvector, top to bottom."""
        out = ""
        cell = (by1 - by0) / n
        for i in range(n):
            y = by0 + (n - 1 - i) * cell
            out += (f"\\fill[{shade(ROMA_EVEC[i] / ROMA_EVEC.max())}] ({x},{y:.2f}) "
                    f"rectangle ({x + w},{y + cell:.2f});\n")
        out += (f"\\draw[line width=2.4bp,draw=black] ({x},{by0}) rectangle "
                f"({x + w},{by1});\n")
        return out

    mid = (by0 + by1) / 2
    body += column(210)
    body += column(380)
    notes = Notes()
    body += notes.put(((bx0 + bx1) / 2, mid + 22), "$A$", size=46)
    body += notes.put(((bx0 + bx1) / 2, mid - 34), f"${n} \\times {n}$")
    body += notes.put((272, mid), "$=$", size=46)
    body += notes.put((330, mid), "$\\lambda$", color="accenttwo", size=46)
    body += notes.put((W / 2, 330), "$A\\,c = \\lambda\\,c$", size=46)
    body += notes.put((W / 2, 68),
                      f"$\\lambda = {lmax}$: the same twelve\\\\"
                      f"numbers, every one bigger", color="accenttwo")
    F.emit("eigen-equation", body, container="col", h=H)


# --------------------------------------------------------------------------- spectrum
def fig_spectrum():
    """Twelve eigenvalues on a line, and only one of them has a positive eigenvector.

    A stacking dot plot rather than a row of stems: two of the twelve sit 0.037 apart,
    which at 537 bp is 2.6 bp, so stems would have shown eleven marks under a label
    that says twelve.
    """
    w, V = np.linalg.eigh(ROMA_A)
    assert len(w) == 12
    assert abs(w[-1] - ROMA_LMAX) < 1e-12
    assert len(set(np.round(w, 6))) == 12, "the drawn spectrum has a repeated eigenvalue"
    lead = V[:, -1] * np.sign(V[:, -1].sum())
    assert lead.min() > 0, "the leading eigenvector must be all-positive"
    for i in range(11):
        v = V[:, i]
        assert v.min() < -1e-9 < 1e-9 < v.max(), (
            f"eigenvector {i} has one sign -- Perron-Frobenius says only the leading "
            f"one does")
    shown = f"{ROMA_LMAX:.2f}"

    lo, hi = -3.0, 3.6
    x0, x1, axis = 40.0, 500.0, 175.0
    d, gap, rise = 16.0, 20.0, 20.0

    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    body = F.seg((x0 - 10, axis), (x1 + 22, axis), color="black", w=2.6)
    for t in range(-3, 4):
        body += F.seg((X(t), axis), (X(t), axis - 10), color="black", w=2.2)
        body += F.text(X(t), axis - 18, f"${t}$", anchor="north")

    # Beeswarm: a value within `gap` of one already placed goes up a row, so twelve
    # eigenvalues read as twelve marks even where two of them nearly coincide.
    placed = []
    for v in w:
        r = 0
        while any(abs(X(v) - X(u)) < gap and s == r for u, s in placed):
            r += 1
        placed.append((v, r))
    rows = [r for _, r in placed]
    assert max(rows) <= 1, f"the spectrum needs {max(rows) + 1} rows to separate"
    assert sum(1 for r in rows if r) == 2, \
        f"exactly two eigenvalues should have to stack, got rows {rows}"
    for v, r in placed[:-1]:
        body += F.dot(X(v), axis + 16 + r * rise, color="annot", d=d)
    body += F.dot(X(w[-1]), axis + 16, color="accenttwo", d=d + 8)

    notes = Notes()
    body += notes.put((X(w[-1]) - 14, 252), f"$\\lambda_{{\\max}} = {shown}$",
                      color="accenttwo", anchor="east")
    # A leader, because the label has to sit left of its own dot to stay on the page
    # and without one it reads as a caption for the pair of dots underneath it.
    body += F.seg((X(w[-1]) - 20, 234), (X(w[-1]) - 2, 204), color="accenttwo", w=2.4)
    body += notes.put((30, 308), f"{len(w)} eigenvalues of $A$", color="annot",
                      anchor="west")
    body += notes.put((W / 2, 58), "only $\\lambda_{\\max}$ has an\\\\"
                      "all-positive eigenvector")
    F.emit("spectrum", body, container="col", h=H)


# --------------------------------------------------------------------------- decay
DECAY_FRAME = (170, 150, 520, 350)


def fig_decay():
    """Every other mode dies as |lambda_i/lambda_1|^t. The slowest sets the speed."""
    w = np.sort(ROMA_EVALS)
    ratios = sorted(abs(v) / w[-1] for v in w[:-1])
    slow = max(ratios)
    assert abs(slow - RATIO) < 1e-12, (slow, RATIO)
    assert abs(LAMBDA2 - abs(w[0])) < 1e-9, \
        "on this graph the slowest mode is the most NEGATIVE eigenvalue"
    assert abs(w[0]) > w[-2], (
        f"|lambda_min| = {abs(w[0]):.3f} must beat lambda_2 = {w[-2]:.3f}, or the "
        f"label quotes {w[-2] / w[-1]:.2f} for a process that converges at {slow:.2f}")
    assert len(ratios) == 11, len(ratios)

    ax = Axes(DECAY_FRAME, (0, 20), (0, 1), xticks=[0, 5, 10, 15, 20],
              yticks=[0, 0.25, 0.5, 0.75, 1], yfmt=lambda v: f"{v:g}")
    ts = np.linspace(0, 20, 201)
    body = ax.frame()
    body += axis_titles(ax, "steps $t$", "$|\\lambda_i/\\lambda_1|^t$", ytx=40)
    drawn = []
    for r in ratios:
        hot = r == slow
        body += ax.line(ts, r ** ts, color="accenttwo" if hot else "annot",
                        w=4.6 if hot else 2.4)
        drawn += curve_pts(ax, ts, r ** ts)

    notes = Notes(curves=drawn)
    for b in tick_boxes(ax):
        notes.block(b)
    body += notes.first([(520, 260), (520, 250), (520, 240)],
                        f"slowest mode\\\\{slow:.3f}", color="accenttwo", anchor="east")
    body += notes.first([(520, 345), (520, 336), (500, 345)],
                        f"${len(ratios) - 1}$ other modes", color="annot", anchor="east")
    F.emit("decay", body, container="col", h=H)


# --------------------------------------------------------------------------- walks
# Six nodes, seven edges, and ONE walk drawn. At 537 bp three side-by-side panels of
# this graph would be 179 bp each, and three walks on one copy cannot be told apart:
# three length-3 walks need nine edge slots and the graph has seven, so no three of
# them are edge-disjoint. The count carries the "many".
WALK_EDGES = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d"), ("d", "e"),
              ("d", "T"), ("e", "T")]
WALK_POS = {"a": (30, 150), "b": (156, 240), "c": (156, 60), "d": (282, 150),
            "e": (426, 240), "T": (426, 60)}
WALK = ("a", "b", "d", "T")


def fig_walks_arrive():
    """A^t counts walks, so a high score means many walks end on you."""
    G = nx.Graph(WALK_EDGES)
    assert set(G) == set(WALK_POS)
    F.assert_planar_drawing(WALK_EDGES, WALK_POS, "walks-arrive")
    assert WALK[-1] == "T"
    for u, v in zip(WALK, WALK[1:]):
        assert G.has_edge(u, v), f"{u}-{v} is not an edge: {WALK} is not a walk"
    steps = len(WALK) - 1

    names = sorted(G)
    A = nx.to_numpy_array(G, nodelist=names)
    arriving = int(round(np.linalg.matrix_power(A, steps)[:, names.index("T")].sum()))
    assert arriving == 14, arriving

    body = ""
    for a, b in WALK_EDGES:
        body += F.seg(WALK_POS[a], WALK_POS[b], color="annot", w=2.4)
    for nm, (x, y) in WALK_POS.items():
        body += F.disc(x, y, "", fill="accent", name=f"w{nm}")
    body += F.ring(*WALK_POS["T"], size=NODE, color="accenttwo", w=4.5, grow=13)
    for u, v in zip(WALK, WALK[1:]):
        body += arrow(f"w{u}", f"w{v}", color="accenttwo", w=5.4)

    notes = Notes(discs=list(WALK_POS.values()))
    body += notes.put((W / 2, 330),
                      f"${arriving}$ walks of length ${steps}$\\\\end at the ring",
                      color="accenttwo")
    F.emit("walks-arrive", body, container="col", h=H)


# --------------------------------------------------------------------------- power iteration
# A triangle with a two-node arm on each of two corners, folded into two rows so that
# seven values fit beside seven discs in a 537 bp column. Chosen from a search over
# connected planar 7-node graphs (see the module docstring): at step 1 the three
# degree-2 nodes are tied at 0.67 and by step 4 the one inside the triangle has pulled
# away to 0.85 -- the whole argument of Part 5 in one picture, and a thing degree
# cannot say.
BOW_EDGES = [("A", "B"), ("A", "P"), ("A", "M"), ("L", "M"),
             ("B", "P"), ("B", "N"), ("R", "N")]
BOW_POS = {"L": (40, 296), "M": (180, 296), "A": (320, 296), "P": (450, 200),
           "B": (320, 104), "N": (180, 104), "R": (40, 104)}
BOW_ORDER = ["L", "M", "A", "P", "B", "N", "R"]
POWER_STEPS = (0, 1, 2, 4)
# The band between the two rows is the only rectangle in this drawing that no edge
# crosses (A-B runs at x = 320, so the notes stop short of it). Claimed before the
# labels are solved, so the solver works around it rather than into it.
POWER_NOTE_SPOTS = ((30, 250), (30, 170))


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
    # how far that is from the answer. See the module docstring for why 1e-3 is not
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

    tags = [(POWER_NOTE_SPOTS[0], f"step ${step}$")]
    if step == POWER_STEPS[-1]:
        tags.append((POWER_NOTE_SPOTS[1], f"within ${resid:.3f}$"))
    reserved = [label_box(at[0], at[1], visible(s), "west") for at, s in tags]

    names = {n: printed[i] for i, n in enumerate(BOW_ORDER)}
    sides, boxes = F.place_labels(names, BOW_POS, BOW_EDGES, blockers=reserved,
                                  bounds=(8, 20, W - 8, 378), gap=2.0)
    body += F.draw_labels(names, BOW_POS, sides)

    notes = Notes(discs=list(BOW_POS.values()),
                  segs=edge_pts(BOW_EDGES, BOW_POS))
    for b in boxes.values():
        notes.block(b)
    for at, s in tags:
        body += notes.put(at, s, color="accenttwo", anchor="west")
    F.emit(f"power-step-{step}", body, container="col", h=H)


# =============================================================================
# Part 6 -- Katz
# =============================================================================
# LOCAL is a five-clique with a four-node tail, so the drawing contains K5 and cannot
# be planar. These coordinates are the output of a search that fixed c1 (the node the
# tail hangs from) and moved the other four to minimise crossings first and then
# maximise the distance from every edge to every disc it does not end at. Both are
# re-asserted on every build, so a "tidying" edit that costs a crossing fails here.
LOCAL_XY = {
    "c1": (196.0, 175.0), "c2": (27.1, 325.0), "c3": (26.0, 29.0),
    "c4": (59.2, 170.5), "c5": (112.9, 205.3),
    "t1": (268.0, 175.0), "t2": (340.0, 175.0), "t3": (412.0, 175.0),
    "t4": (484.0, 175.0),
}
LOCAL_DRAW_EDGES = [(a, b) for a, b in LOCAL.edges()]
K5_CROSSING_NUMBER = 1


def _local_lmax():
    A = nx.to_numpy_array(LOCAL, nodelist=list(LOCAL))
    return float(np.linalg.eigvalsh(A)[-1])


def fig_katz_floor():
    """The same tail node, lifted off the floor by Katz's beta."""
    assert set(LOCAL_XY) == set(LOCAL), sorted(set(LOCAL_XY) ^ set(LOCAL))
    assert LOCAL.subgraph(LOCAL_CORE).number_of_edges() == 10, "the core must be K5"
    x = F.crossings(LOCAL_DRAW_EDGES, LOCAL_XY)
    assert len(x) == K5_CROSSING_NUMBER, (
        f"katz-floor: {len(x)} crossings -- K5's rectilinear crossing number is "
        f"{K5_CROSSING_NUMBER}, so that is the floor and anything above it is a "
        f"defect: {x}")
    bad = F.clearance_bad(LOCAL_DRAW_EDGES, LOCAL_XY, r=NODE / 2 + 4)
    assert not bad, f"katz-floor: edge through a disc it does not end at -- {bad}"

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
    for nm, (px, py) in LOCAL_XY.items():
        body += (f"\\draw[line width=1.8bp,draw=black,fill={shade(scores[nm] / top)}] "
                 f"({px},{py}) circle ({NODE / 2}bp);\n")

    notes = Notes(discs=list(LOCAL_XY.values()),
                  segs=edge_pts(LOCAL_DRAW_EDGES, LOCAL_XY))
    body += notes.put((W - 10, 285),
                      f"Katz  ${katz_txt}$\\\\eigenvector\\\\${eig_txt}$",
                      color="accenttwo", anchor="east")
    body += notes.put((W - 10, 60), "darker $=$ higher Katz", color="annot",
                      anchor="east")
    # The leader runs from inside the note's own descender line down to the disc's
    # rim: drawn shorter it read as a stray dash between two unrelated things.
    body += F.seg((484, 224), (484, 197), color="accenttwo", w=2.4)
    F.emit("katz-floor", body, container="col", h=H)


# --------------------------------------------------------------------------- the solve
def _katz_solve_body(final):
    """The rearrangement, as a two-step build.

    The two terms of the fixed point are coloured inside the equation and the two
    annotations under it repeat those colours: at 537 bp there is no room for a leader
    from each term out to a note beside it, and an uncoloured note under a two-term
    equation names neither term.

    The annotations are flush left and flush right -- the side each term sits on in
    the equation above -- which is also what carries the ink across the column. A
    centred stack of five lines spans 64% of 537 bp and the width gate wants 76%.
    """
    notes = Notes()
    body = notes.put((W / 2, 336),
                     "$c = {\\color{accenttwo}\\beta\\mathbf{1}}"
                     " + {\\color{accent}\\lambda A c}$", size=46,
                     meas="$c = \\beta\\mathbf{1} + \\lambda A c$")
    body += notes.put((14, 268), "$\\beta$: a floor for everyone",
                      color="accenttwo", anchor="west")
    body += notes.put((W - 14, 210), "$\\lambda A c$: your neighbours",
                      color="accent", anchor="east")
    body += notes.put((W / 2, 140), "$(I - \\lambda A)\\,c = \\beta\\mathbf{1}$",
                      size=46)
    if final:
        body += notes.put((W / 2, 48),
                          "$c = \\beta\\,(I - \\lambda A)^{-1}\\mathbf{1}$",
                          color="accenttwo", size=46)
    return body


def fig_katz_solve_1():
    """The fixed point: a floor, plus a share of your neighbours."""
    F.emit("katz-solve-1", _katz_solve_body(False), container="col", h=H)


def fig_katz_solve_2():
    """...and it is linear, so it is one solve."""
    F.emit("katz-solve-2", _katz_solve_body(True), container="col", h=H)


# --------------------------------------------------------------------------- the series
# A horizontal dot plot, one row per term. Drawn the other way up at 537 bp the four
# value labels are 111 bp wide on a 91 bp pitch and overlap each other; one term per
# row, they cannot.
SERIES_TERMS = 4
SERIES_TICKS = ["$\\mathbf{1}$", "$\\lambda A\\mathbf{1}$",
                "$\\lambda^2 A^2\\mathbf{1}$", "$\\lambda^3 A^3\\mathbf{1}$"]
SERIES_ROWS = (320, 246, 172, 98)
SERIES_X0, SERIES_X1, SERIES_MAX = 200.0, 400.0, 13.0


def series_totals():
    rows = katz_series(ROMA, ROMA_KATZ_LAMBDA, terms=SERIES_TERMS)
    return [float(term.sum()) for _, term, _ in rows]


def _series_body(upto):
    tot = series_totals()
    assert len(tot) == SERIES_TERMS == len(SERIES_ROWS) == len(SERIES_TICKS)
    assert abs(tot[0] - ROMA.number_of_nodes()) < 1e-12, tot[0]
    assert all(a > b for a, b in zip(tot, tot[1:])), f"the terms must shrink: {tot}"
    assert max(tot) < SERIES_MAX, (max(tot), SERIES_MAX)
    ratio = KATZ_SAFE
    assert abs(ratio - ROMA_KATZ_LAMBDA * ROMA_LMAX) < 1e-12
    assert ratio < 1.0

    def X(v):
        return SERIES_X0 + v / SERIES_MAX * (SERIES_X1 - SERIES_X0)

    # A zero baseline, so a dot's distance from it is the quantity and not decoration.
    body = F.seg((SERIES_X0, SERIES_ROWS[-1] - 30), (SERIES_X0, SERIES_ROWS[0] + 30),
                 color="annot", w=2.2)
    notes = Notes()
    body += notes.put((SERIES_X0, SERIES_ROWS[-1] - 40), "$0$", color="annot",
                      anchor="north")
    for t in range(SERIES_TERMS):
        body += notes.put((SERIES_X0 - 30, SERIES_ROWS[t]), SERIES_TICKS[t],
                          anchor="east")
    for t in range(upto):
        body += F.dot(X(tot[t]), SERIES_ROWS[t], color="accent", d=22)
        body += notes.put((X(tot[t]) + 22, SERIES_ROWS[t]), f"${tot[t]:.2f}$",
                          anchor="west")
    body += notes.put((W - 10, 40),
                      f"$\\lambda\\lambda_{{\\max}} = {ratio:.2f} < 1$",
                      color="accenttwo", anchor="east")
    return body


def fig_katz_series(k):
    F.emit(f"katz-series-{k}", _series_body(k), container="col", h=H)


# --------------------------------------------------------------------------- the dial
LAM_LO = 0.15 / ROMA_LMAX
LAM_MID = ROMA_KATZ_LAMBDA
LAM_HI = 0.98 / ROMA_LMAX
DIAL_LAMBDAS = (LAM_LO, LAM_MID, LAM_HI)
DIAL_CITIES = ("Roma", "Alexandria", "Carthago", "Athenae")
DIAL_X = (250, 365, 480)
DIAL_RANK_Y = {1: 300, 2: 250, 3: 200, 4: 150, 5: 100, 6: 50}
DIAL_HEAD = 376


def dial_ranks():
    """Competition rank (ties share the better rank) for each city at each lambda."""
    out = []
    for lam in DIAL_LAMBDAS:
        k = katz_at(ROMA, lam)
        order = sorted(k, key=lambda n: (-k[n], n))
        rank = {}
        for i, n in enumerate(order):
            same = [m for m in order[:i] if abs(k[m] - k[n]) < 1e-9]
            rank[n] = rank[same[0]] if same else i + 1
        out.append((lam, k, rank))
    return out


def fig_katz_dial():
    """Turning lambda leaves the top three alone and swaps the fourth place."""
    cols = dial_ranks()
    ranks = {c: [r[c] for _, _, r in cols] for c in DIAL_CITIES}
    assert ranks["Roma"] == [1, 1, 1], ranks["Roma"]
    assert ranks["Alexandria"] == [2, 2, 2], ranks["Alexandria"]
    assert ranks["Carthago"] == [4, 4, 6], ranks["Carthago"]
    assert ranks["Athenae"] == [6, 5, 4], ranks["Athenae"]
    # Athenae and Byzantium are the same node up to symmetry: they tie at every lambda,
    # so the fourth place at LAM_HI is shared. Following named cities by rank is what
    # lets the figure say that without drawing one of a tied pair and dropping the
    # other, which is the false claim FIGURE_SPEC names for shared crowns.
    for _, k, r in cols:
        assert abs(k["Athenae"] - k["Byzantium"]) < 1e-9
        assert r["Athenae"] == r["Byzantium"]
    assert max(max(v) for v in ranks.values()) <= max(DIAL_RANK_Y)
    movers = {c for c in DIAL_CITIES if len(set(ranks[c])) > 1}
    assert movers == {"Carthago", "Athenae"}, movers

    body, discs = "", []
    for c in DIAL_CITIES:
        col = "accenttwo" if c in movers else "accent"
        for i in range(len(DIAL_X) - 1):
            body += F.seg((DIAL_X[i] + 26, DIAL_RANK_Y[ranks[c][i]]),
                          (DIAL_X[i + 1] - 26, DIAL_RANK_Y[ranks[c][i + 1]]),
                          color=col, w=3.4)
    for c in DIAL_CITIES:
        col = "accenttwo" if c in movers else "accent"
        for i, x in enumerate(DIAL_X):
            y = DIAL_RANK_Y[ranks[c][i]]
            body += F.disc(x, y, f"{ranks[c][i]}", fill=col)
            discs.append((x, y))

    notes = Notes(discs=discs)
    body += notes.put((DIAL_X[0] - 100, DIAL_HEAD), "$\\lambda$:", color="annot",
                      anchor="north east")
    for x, (lam, _, _) in zip(DIAL_X, cols):
        body += notes.put((x, DIAL_HEAD), f"${lam:.2f}$", color="annot",
                          anchor="north")
    for c in DIAL_CITIES:
        body += notes.put((DIAL_X[0] - 26, DIAL_RANK_Y[ranks[c][0]]), c,
                          color="accenttwo" if c in movers else "black", anchor="east")
    F.emit("katz-dial", body, container="col", h=H)


# --------------------------------------------------------------------------- divergence
DIVERGE_FRAME = (140, 180, 515, 310)
DIVERGE_CITIES = ["Roma", "Mediolanum", "Tarraco", "Londinium"]
DIVERGE_XLIM = (0.10, 0.40)
DIVERGE_YLIM = (-25, 25)


def fig_katz_diverge():
    """Past 1/lambda_max the solve still returns numbers, and they are nonsense.

    Both notes sit outside the frame. Inside it there is no rectangle wide enough for
    twenty characters that one of the four curves does not cross -- the divergence
    fills the panel, which is the point of the panel.
    """
    assert abs(KATZ_CRITICAL - 1 / ROMA_LMAX) < 1e-12
    assert DIVERGE_XLIM[0] < KATZ_CRITICAL < KATZ_BAD_LAMBDA < DIVERGE_XLIM[1]
    crit_txt, bad_txt = f"{KATZ_CRITICAL:.4f}", f"{KATZ_BAD_LAMBDA:.3f}"
    assert crit_txt == "0.2989" and bad_txt == "0.344", (crit_txt, bad_txt)

    bad = katz_at(ROMA, KATZ_BAD_LAMBDA)
    negatives = sorted(n for n, v in bad.items() if v < 0)
    assert negatives == KATZ_BAD_NEGATIVE and len(negatives) == 11, negatives
    assert all(v < 0 for v in katz_at(ROMA, KATZ_CRITICAL * 1.005).values()), \
        "immediately past the critical lambda every score must be negative"
    assert all(v > 0 for v in katz_at(ROMA, KATZ_CRITICAL * 0.995).values()), \
        "below the critical lambda every score must still be positive"

    ax = Axes(DIVERGE_FRAME, DIVERGE_XLIM, DIVERGE_YLIM,
              xticks=[0.1, 0.2, 0.3], yticks=[-20, 0, 20],
              xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    body = ax.frame()
    body += F.text(32, (ax.y0 + ax.y1) / 2, "Katz score", rot=90)
    body += F.seg((ax.x0, ax.Y(0)), (ax.x1, ax.Y(0)), color="annot", w=2.0)

    lo = np.linspace(DIVERGE_XLIM[0], KATZ_CRITICAL - 1e-4, 400)
    hi = np.linspace(KATZ_CRITICAL + 1e-4, DIVERGE_XLIM[1], 400)
    for city in DIVERGE_CITIES:
        assert city in ROMA_NAMES, city
        for branch in (lo, hi):
            ys = np.array([katz_at(ROMA, lam)[city] for lam in branch])
            keep = (ys > DIVERGE_YLIM[0]) & (ys < DIVERGE_YLIM[1])
            body += ax.line(branch[keep], ys[keep], color="accent", w=3.0)
    body += F.seg((ax.X(KATZ_CRITICAL), ax.y0), (ax.X(KATZ_CRITICAL), ax.y1),
                  color="accenttwo", w=3.4, dash=DASH)

    notes = Notes()
    for b in tick_boxes(ax):
        notes.block(b)
    body += notes.put((ax.X(KATZ_CRITICAL), DIAL_HEAD),
                      f"$1/\\lambda_{{\\max}} = {crit_txt}$",
                      color="accenttwo", anchor="north")
    body += notes.put((W / 2, 108),
                      f"at $\\lambda = {bad_txt}$:\\\\"
                      f"${len(negatives)}$ of ${ROMA.number_of_nodes()}$ scores $< 0$",
                      color="accenttwo", anchor="north")
    F.emit("katz-diverge", body, container="col", h=H)


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

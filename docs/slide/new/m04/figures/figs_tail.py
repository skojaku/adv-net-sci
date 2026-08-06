#!/usr/bin/env python3
"""Parts 5-6 of the Module 04 deck: reading the tail, and where hubs come from.

Twenty figures, slides 47-73.  Everything numeric comes from `verify_numbers.py`;
nothing here re-derives a degree sequence and nothing here types a number a loader
can compute.  The drawing API is `figlib` -- one bp is one slide pixel, so a 36pt
label is 36px of type on the slide and there is nothing to reconcile.

Four things in here are imported from outside this file:

    ba_frames()            the preferential-attachment growth history, 43 frames, one
                           per edge added, ending on the network `quiz.png` draws
    growth_pos(box)        the canonical layout mapped into `box` -- the picture the
                           quiz shows, letterboxed to GROWTH_ASPECT (0.994, near square)
    growth_layout(...)     the same graph solved for a different shape, `stretch=True`
                           for a panel much wider than it is tall
    draw_growth(frame,pos) the frame renderer both the still and the GIF use

`make_animations.py` builds `ba-growth.gif` from those, so the animation and the quiz
still cannot drift apart -- same graph, same layout, same drawing code, and `ba_frames`
asserts that its last frame is exactly `growth_edges(True)`.

A note on the two slopes, because slides 58-62 exist entirely because of it.  The CCDF
of a p(k) ~ k^-gamma tail falls with slope 1 - gamma, not -gamma.  cond-mat's CCDF slope
is -2.571 (gamma = 3.571); its *PDF* fitted over the same decades is -2.443.  Those are
different measurements of different curves and this file keeps them apart: `loglog-line`
prints the PDF slope it actually fitted, and no CCDF figure prints a gamma at all.
"""

import math
import re
from fractions import Fraction
from functools import lru_cache

import networkx as nx
import numpy as np

from figlib import (DASH, FONT, NODE, SMALLNODE, Axes, boxes_overlap, clearance_bad,
                    disc, dot, emit, fill_poly, label_box, pct, polyline, seg, text)
from verify_numbers import (ba_graph, ccdf, ccdf_fit, condmat, internet_as, net_stats,
                            top_share, uniform_growth_graph, yeast_ppi)

H = 380                                  # every figure here is a plain `.fig` (380px cap)

# The one full-width plot frame.  The x title sits 66bp under the axis and the y title is
# placed by hand at x=30 -- `Axes.frame`'s own y title lands on top of a "$10^{-4}$" tick
# label, which is about 90bp wide at the 36pt floor.
FRAME = (185, 145, 1058, 356)
# In a 537bp column the right-hand tick label is what runs off the page: "100" centred on
# the last tick needs 27bp of its own, so the frame stops at 500, not at the canvas.
FRAME_COL = (165, 145, 500, 356)


# --------------------------------------------------------------------------- data
@lru_cache(maxsize=None)
def condmat_degrees():
    return tuple(int(d) for _, d in condmat().degree())


@lru_cache(maxsize=None)
def condmat_pdf():
    """(distinct degrees, p(k) at each, N).  One point per observed degree, no bins."""
    d = np.array(condmat_degrees())
    ks = np.array(sorted(set(d.tolist())))
    return ks, np.array([(d == k).mean() for k in ks]), len(d)


@lru_cache(maxsize=None)
def condmat_ccdf():
    return ccdf(np.array(condmat_degrees()))


# The deck's caption for slide 51 claims "roughly straight over two decades of degree",
# so the line is fitted over the two decades the eye is being pointed at, 3 <= k <= 279
# (a factor of 93, 1.97 decades) rather than FIGURE_SPEC's 10..200, which is 1.3.
PDF_KMIN, PDF_KMAX = 3, 279

# The two thresholds slide 49 annotates. Named, because the accent-3 band's left edge was
# hardcoded at 96 and landed 23px left of the "100" the annotation beside it printed.
SMALL_K, TAIL_K = 10, 100

# How far above a log axis's floor a curve stops, in decades. A stroke that meets the
# axis line reads as "the distribution ends here"; the floor is 1e-5, not zero.
FLOOR_LIFT = 0.28


@lru_cache(maxsize=None)
def pdf_fit():
    """(slope, intercept, R^2, n) of log10 p(k) against log10 k -- the PDF, not the CCDF."""
    ks, pk, _ = condmat_pdf()
    sel = (ks >= PDF_KMIN) & (ks <= PDF_KMAX) & (pk > 0)
    x, y = np.log10(ks[sel]), np.log10(pk[sel])
    a, b = np.polyfit(x, y, 1)
    resid = y - (a * x + b)
    return float(a), float(b), float(1 - np.var(resid) / np.var(y)), int(sel.sum())


@lru_cache(maxsize=None)
def condmat_stats():
    return net_stats(condmat())


@lru_cache(maxsize=None)
def er_graph():
    """A random graph matched to cond-mat: same N, same <k>, so only the SHAPE differs.

    R1 B-11: slide 67's caption says "a random network with the same average" and never
    says as what, and the figure printed <k> = 4.0 -- neither cond-mat's 8.08 nor the
    Internet's 3.88, so the comparison had no referent.  Matching cond-mat exactly makes
    slides 56 and 67 the same axes, the same N and the same mean with one difference
    between them, and it makes the Var/<k> pair on those two figures comparable.
    """
    s = condmat_stats()
    return nx.gnp_random_graph(s["N"], s["k1"] / (s["N"] - 1), seed=3)


@lru_cache(maxsize=None)
def lattice_degrees():
    """A ring lattice at the same mean degree as cond-mat and the random graph."""
    g = nx.watts_strogatz_graph(2000, 8, 0.0, seed=1)
    return tuple(int(d) for _, d in g.degree())


@lru_cache(maxsize=None)
def degrees_of(which):
    g = {"ba": ba_graph, "uniform": uniform_growth_graph, "er": er_graph,
         "internet": internet_as, "yeast": yeast_ppi}[which]()
    return tuple(int(d) for _, d in g.degree())


# The worksheet's data is synthetic on purpose: slide 60 hands the room a CCDF slope of
# exactly -1.3, and no network in this deck has one.  Sampled from a gamma = 2.3 tail,
# whose CCDF therefore falls with slope 1 - 2.3 = -1.3; the seed is the one whose fitted
# slope lands on -1.300 to three decimals, so the triangle drawn on the figure is the
# slope the data actually has.
WS_GAMMA = Fraction(23, 10)
WS_SLOPE = Fraction(1) - WS_GAMMA                 # -13/10, exactly
WS_SEED, WS_N = 353, 20000
WS_KMIN, WS_KMAX = 3, 300


@lru_cache(maxsize=None)
def worksheet_ccdf():
    rng = np.random.default_rng(WS_SEED)
    u = rng.random(WS_N)
    k = np.floor((1 - u) ** (-1 / (float(WS_GAMMA) - 1))).astype(int)
    k = k[k >= 1]
    ks, su = ccdf(k)
    return ks, su, ccdf_fit(ks, su, WS_KMIN, WS_KMAX)


# --------------------------------------------------------------------------- plot helpers
def axis_titles(ax, xtitle, ytitle, ytx=30):
    """Both axis titles, placed by hand so neither can land on a tick label."""
    o = text((ax.x0 + ax.x1) / 2, ax.y0 - 66, xtitle, anchor="north")
    o += text(ytx, (ax.y0 + ax.y1) / 2, ytitle, rot=90)
    return o


def dec(v):
    """A decade tick label: plain digits up to 1000, powers after."""
    e = int(round(math.log10(v)))
    return {0: "1", 1: "10", 2: "100", 3: "1000"}.get(e, f"$10^{{{e}}}$")


def scatter(ax, xs, ys, color="accent", d=9, expect=None):
    """Points, with the count that actually lands inside the frame asserted.

    `Axes.points` silently skips anything outside, which is the correct behaviour and
    also the way a figure loses half its data without saying so.
    """
    n = sum(1 for x, y in zip(xs, ys) if ax.inside(x, y))
    assert expect is None or n == expect, \
        f"{n} of {len(xs)} points land inside the frame, expected {expect}"
    return ax.points(xs, ys, color=color, d=d)


def curve(ax, xs, ys, color="accent", w=3.4, dash=""):
    """A CCDF/PDF curve, dropping the zero survival point a log axis cannot show."""
    pts = [(x, y) for x, y in zip(xs, ys) if y > 0]
    return ax.line([p[0] for p in pts], [p[1] for p in pts], color=color, w=w, dash=dash)


# The line break `\\` comes FIRST: without it the alternation matched the second
# backslash plus the following word, so "\\values crowd at 1" measured as one line of a
# two-line label and every multi-line box came out a line short and half a panel wide.
_TEX = re.compile(r"\\\\|\\[a-zA-Z]+|\\[,;!]|[${}^_]")


def visible(s):
    """What a label roughly occupies on the page, for the collision boxes.

    `label_box` counts characters, and a TeX label is mostly markup: the literal
    "$\\langle k \\rangle = 4$" is 24 characters and eight glyphs, so measuring it raw
    reported collisions that are not there and moved two labels off the curves they
    belonged to.  Control words count as one glyph; braces, dollars and spacing count
    as none; the line break is left alone so `label_box` can still split on it.
    """
    def sub(m):
        t = m.group(0)
        if t == "\\\\":
            return t
        return "" if t[0] in "${}^_" or len(t) == 2 else "n"

    return _TEX.sub(sub, s)


def label_at(x, y, s, color="black", anchor="center", size=FONT, boxes=None):
    """An in-place curve label, recorded so the next one can be checked against it."""
    b = label_box(x, y, visible(s), anchor, size=size)
    if boxes is not None:
        hit = [i for i, o in enumerate(boxes) if boxes_overlap(b, o)]
        assert not hit, f"in-place label {s!r} collides with label {hit} -- move it"
        boxes.append(b)
    return text(x, y, s, color=color, anchor=anchor, size=size)


def curve_pts(ax, xs, ys, step=7.0):
    """A curve's drawn path, sampled every `step` bp, for the label solver."""
    pts = [ax.P(x, y) for x, y in zip(xs, ys) if ax.inside(x, y) and y > 0]
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        out += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n)]
    return out + pts[-1:]


# Tried in order: below the curve first, because a CCDF label reads as belonging to the
# line above it, then to the sides, then above.
_SIDES = (270, 300, 240, 330, 210, 0, 180, 30, 150, 90)


def _box_dist(b, p):
    """Distance from the point `p` to the rectangle `b`, zero if inside."""
    return math.hypot(max(b[0] - p[0], 0, p[0] - b[2]), max(b[1] - p[1], 0, p[1] - b[3]))


def curve_label(ax, s, at, own, boxes, others=(), color="black", size=FONT, pad=7,
                bounds=None, floor=34, margin=1.4):
    """Place a label near `at` so that the nearest curve to it is the one it NAMES.

    FIGURE_GUIDE, "place labels with a solver, not by hand": on log-log axes a curve
    sweeps the whole panel, so "just above the line" is not a position.

    R1 B-9: the first solver only avoided ink, so it moved "physicists" off its own tail
    and parked it 23px from the yeast curve and 50px from its own -- one defect traded
    for another, with only the colour resolving it.  `own` is now the attractor and
    `others` are blockers with a clearance `floor`; a position is rejected unless its own
    curve is the nearest by `margin`.  That is the property the reviewer measured, so it
    is the property the solver enforces.
    """
    # Default to the frame's interior: a label that drifts below the axis lands on the
    # tick labels, which is where "random" ended up on the first pass.
    bounds = bounds or (ax.x0 + 4, ax.y0 + 6, ax.x1 - 4, ax.y1 - 6)
    v = visible(s)
    for r in (34, 46, 60, 78, 98, 122):
        for deg in _SIDES:
            a = math.radians(deg)
            cx, cy = at[0] + r * math.cos(a), at[1] + r * math.sin(a)
            b = label_box(cx, cy, v, "center", size=size)
            if not (bounds[0] <= b[0] and b[2] <= bounds[2]
                    and bounds[1] <= b[1] and b[3] <= bounds[3]):
                continue
            if any(boxes_overlap(b, o) for o in boxes):
                continue
            if any(_box_dist(b, p) <= pad for p in own):
                continue
            if any(_box_dist(b, p) <= pad for p in others):
                continue
            d_own = min((_box_dist(b, p) for p in own), default=1e9)
            d_oth = min((_box_dist(b, p) for p in others), default=1e9)
            if d_oth < floor or d_oth < margin * d_own:
                continue
            boxes.append(b)
            return text(cx, cy, s, color=color, anchor="center", size=size)
    raise SystemExit(
        f"no clear spot for the curve label {s!r} -- it must end up nearer its own curve "
        f"than any other by {margin:.2f}x. Move its anchor, shorten it or widen the "
        f"panel; do not shrink the type.")


def fixed_label(spots, s, curves, boxes, color="black", anchor="center", size=FONT,
                pad=7):
    """A label at the first of `spots` that is clear of every curve and every label.

    For notes that belong to a whole panel rather than to a point on one curve, where
    an offset from a curve anchor would be arbitrary.
    """
    why = []
    for x, y in spots:
        b = label_box(x, y, visible(s), anchor, size=size)
        if not (6 <= b[0] and b[2] <= 1074 and 6 <= b[1] and b[3] <= 374):
            why.append(f"({x},{y}) off-page")
            continue
        if any(boxes_overlap(b, o) for o in boxes):
            why.append(f"({x},{y}) hits a label")
            continue
        on = [p for p in curves
              if b[0] - pad <= p[0] <= b[2] + pad and b[1] - pad <= p[1] <= b[3] + pad]
        if on:
            why.append(f"({x},{y}) sits on a curve at {on[0][0]:.0f},{on[0][1]:.0f}")
            continue
        boxes.append(b)
        return text(x, y, s, color=color, anchor=anchor, size=size)
    raise SystemExit(f"nowhere clear to put {s!r}: " + "; ".join(why))


# --------------------------------------------------------------------------- growth
# The preferential-attachment history that `ba-growth.gif` animates and `quiz.png`
# freezes.  24 nodes and 45 edges, one frame per edge, so the GIF runs 43 frames.
GROWTH_N, GROWTH_M = 24, 2
PREF_SEED, UNIF_SEED = 8, 12
# 30bp, two above SMALLNODE: `check_render.node_discs` measures a 28bp disc as 27px on
# the slide, one pixel off the bottom of its 26-52 band, and the measurement is a
# bounding box on an antialiased edge.  30 leaves room to be wrong by a pixel.
GROWTH_NODE = SMALLNODE + 2
GROWTH_BOX = (0, 0, 312, 314)        # the canonical box -- `quiz.png`'s sketch panel
GROWTH_ASPECT = (GROWTH_BOX[2] - GROWTH_BOX[0]) / (GROWTH_BOX[3] - GROWTH_BOX[1])


def _grow(n, m, preferential, seed):
    """Grow from a triangle, m edges per arrival.  Returns (edges, arrivals).

    The only difference between the two networks in the quiz is the target rule, so
    both come out of this one function with the same n and the same edge count.
    """
    rng = np.random.default_rng(seed)
    edges = [(0, 1), (1, 2), (0, 2)]
    arrivals = []
    for new in range(3, n):
        targets = []
        if preferential:
            ends = [u for e in edges for u in e]          # one entry per edge END
            while len(targets) < m:
                t = int(ends[rng.integers(len(ends))])
                if t not in targets:
                    targets.append(t)
        else:
            targets = [int(t) for t in rng.choice(new, size=m, replace=False)]
        arrivals.append((new, targets))
        edges += [(new, t) for t in targets]
    return edges, arrivals


@lru_cache(maxsize=None)
def growth_edges(preferential):
    return tuple(_grow(GROWTH_N, GROWTH_M, preferential,
                       PREF_SEED if preferential else UNIF_SEED)[0])


def ba_frames():
    """The growth history, one frame per edge added.  43 frames; the last is `quiz.png`.

    Each frame is {"nodes", "edges", "new_node", "new_edges"}; positions never move, so
    an animation built from these does not jitter.  `make_animations.py` imports this.
    """
    _, arrivals = _grow(GROWTH_N, GROWTH_M, True, PREF_SEED)
    nodes, cur = [0, 1, 2], [(0, 1), (1, 2), (0, 2)]
    frames = [{"nodes": list(nodes), "edges": list(cur), "new_node": None,
               "new_edges": []}]
    for new, targets in arrivals:
        nodes.append(new)
        for t in targets:
            cur.append((new, t))
            frames.append({"nodes": list(nodes), "edges": list(cur),
                           "new_node": new, "new_edges": [(new, t)]})
    # The last frame IS the network quiz.png draws in its preferential panel. If this
    # ever stops being true the GIF and the still have drifted, which is the one thing
    # sharing this module was supposed to make impossible.
    assert len(frames) == 1 + GROWTH_M * (GROWTH_N - 3) == 43, len(frames)
    assert frames[-1]["nodes"] == list(range(GROWTH_N))
    assert [tuple(e) for e in frames[-1]["edges"]] == [tuple(e) for e in
                                                       growth_edges(True)]
    return frames


def _relax(P, edges, r, box, iters=1500):
    """Push discs apart and off the edges they are not attached to.

    A spring layout drops a disc onto an edge it has nothing to do with about once
    per drawing, and an edge that vanishes under a node is a drawing that lies about who
    is connected to whom.  This is the same clearance `clearance_bad` gates.
    """
    n = len(P)
    x0, y0, x1, y1 = box
    pad, sep, clr = r + 4, 2 * r + 6, r + 6
    for _ in range(iters):
        F = np.zeros_like(P)
        for i in range(n):
            d = P - P[i]
            dist = np.hypot(d[:, 0], d[:, 1])
            dist[i] = 1e9
            for j in np.where(dist < sep)[0]:
                v = P[i] - P[j]
                L = np.hypot(*v) or 1e-6
                F[i] += v / L * (sep - dist[j]) * 0.5
        for a, b in edges:
            pa, pb = P[a], P[b]
            d = pb - pa
            L2 = float(d @ d) or 1e-9
            for k in range(n):
                if k in (a, b):
                    continue
                t = max(0.0, min(1.0, float((P[k] - pa) @ d) / L2))
                v = P[k] - (pa + t * d)
                L = np.hypot(*v) or 1e-6
                if L < clr:
                    F[k] += v / L * (clr - L) * 0.8
                    F[a] -= v / L * (clr - L) * 0.25
                    F[b] -= v / L * (clr - L) * 0.25
        if np.abs(F).max() < 1e-3:
            break
        P += np.clip(F, -8, 8)
        P[:, 0] = np.clip(P[:, 0], x0 + pad, x1 - pad)
        P[:, 1] = np.clip(P[:, 1], y0 + pad, y1 - pad)
    return P


@lru_cache(maxsize=None)
def growth_layout(preferential=True, box=GROWTH_BOX, node=GROWTH_NODE, stretch=False):
    """Solve positions for the growth graph inside `box`, with `node`-sized discs.

    Spring layout, then the clearance relaxation, then the two gates every node-link
    drawing in this deck passes: no disc sitting on an edge it does not end at, and no
    two discs closer than a disc's width.  Cached, so an animation solves once.

    `stretch` fits the two axes independently, for a panel much wider than it is tall --
    a full-width GIF, where the aspect-preserving fit would letterbox the graph into
    the middle third and leave the ink spanning 35% of the frame.  The relaxation runs
    after the stretch, so the clearance gates still hold in the shape actually drawn.
    """
    edges = [tuple(e) for e in growth_edges(preferential)]
    g = nx.Graph()
    g.add_nodes_from(range(GROWTH_N))
    g.add_edges_from(edges)
    p = nx.spring_layout(g, seed=3, iterations=400, k=1.4 / math.sqrt(GROWTH_N))
    P = np.array([p[i] for i in range(GROWTH_N)], float)

    x0, y0, x1, y1 = box
    r, pad = node / 2, node / 2 + 4
    Q = P - P.min(0)
    sx = (x1 - x0 - 2 * pad) / max(Q[:, 0].max(), 1e-9)
    sy = (y1 - y0 - 2 * pad) / max(Q[:, 1].max(), 1e-9)
    Q *= np.array([sx, sy]) if stretch else min(sx, sy)
    Q[:, 0] += x0 + pad + (x1 - x0 - 2 * pad - Q[:, 0].max()) / 2
    Q[:, 1] += y0 + pad + (y1 - y0 - 2 * pad - Q[:, 1].max()) / 2
    Q = _relax(Q, edges, r, box)

    pos = {i: (float(Q[i, 0]), float(Q[i, 1])) for i in range(GROWTH_N)}
    bad = clearance_bad(edges, pos, r=r + 2)
    assert not bad, f"growth layout: edge passes through a disc -- {bad[:3]}"
    gap = min(math.dist(pos[i], pos[j]) for i in range(GROWTH_N)
              for j in range(i + 1, GROWTH_N))
    assert gap >= node + 2, f"growth layout: two discs are {gap:.1f}bp apart"
    return pos


def growth_pos(preferential=True, box=GROWTH_BOX):
    """The CANONICAL layout mapped into `box`, aspect preserved and centred.

    This is the one `quiz.png` draws, so an animation built from it ends on exactly
    the picture the quiz shows.  It letterboxes: give it a box of GROWTH_BOX's aspect
    (near square) and the graph fills it.  For a wide panel, call `growth_layout(box)`
    instead -- same graph, same drawing code, an arrangement solved for that shape.
    """
    canon = growth_layout(preferential)
    gx0, gy0, gx1, gy1 = GROWTH_BOX
    bx0, by0, bx1, by1 = box
    s = min((bx1 - bx0) / (gx1 - gx0), (by1 - by0) / (gy1 - gy0))
    w, h = (gx1 - gx0) * s, (gy1 - gy0) * s
    ox, oy = bx0 + (bx1 - bx0 - w) / 2, by0 + (by1 - by0 - h) / 2
    return {i: (ox + (x - gx0) / (gx1 - gx0) * w, oy + (y - gy0) / (gy1 - gy0) * h)
            for i, (x, y) in canon.items()}


def draw_growth(frame, pos, fill="accent", size=GROWTH_NODE, new_color="accenttwo",
                edge_w=2.2):
    """One frame of the growth history.  Shared by `quiz.png` and `ba-growth.gif`."""
    o = ""
    new_edges = {frozenset(e) for e in frame["new_edges"]}
    for a, b in frame["edges"]:
        hot = frozenset((a, b)) in new_edges
        o += seg(pos[a], pos[b], color=new_color if hot else "black",
                 w=edge_w * (1.9 if hot else 1.0))
    for v in frame["nodes"]:
        o += disc(pos[v][0], pos[v][1], "",
                  fill=new_color if v == frame["new_node"] else fill, size=size)
    return o


# --------------------------------------------------------------------------- Part 5
def fig_linear_axes():
    """Slide 47: p(k) on linear axes -- everything piled into the first few columns.

    Carries the variance the slide's title promises.  R1 B-3: Part Five opened on "here
    is that variance" and Part Four ended by asking for it, and no variance number
    appeared anywhere in the part; `poisson-ccdf` prints the same quantity for the random
    graph so the two can be read against each other.
    """
    ks, pk, N = condmat_pdf()
    assert int(ks.max()) == 279, ks.max()
    d = np.array(condmat_degrees())
    small = float((d <= 10).mean())
    assert small >= 0.78, f"only {small:.1%} of authors sit at k <= 10"
    assert len(ks) == 122, len(ks)
    s = condmat_stats()
    assert s["N"] == N and abs(s["gap"] - s["var"] / s["k1"]) < 1e-9

    ax = Axes(FRAME, (0, 288), (0, 0.15), xticks=[0, 100, 200],
              yticks=[0, 0.05, 0.10, 0.15], yfmt=lambda v: f"{v:g}")
    body = ax.frame()
    body += axis_titles(ax, "number of coauthors $k$", "$p(k)$")
    body += scatter(ax, ks, pk, color="accent", d=13, expect=len(ks))
    body += text(ax.x1 - 8, ax.Y(0.128),
                 f"one dot per distinct $k$: {len(ks)} of them", color="annot",
                 anchor="east")
    body += text(ax.x1 - 8, ax.Y(0.104),
                 f"$\\mathrm{{Var}}(k)/\\langle k \\rangle = {s['gap']:.1f}$",
                 color="accenttwo", anchor="east")
    emit("linear-axes", body, container="full", h=H)


def fig_fat_tail_reveal():
    """Slide 49: the same axes, with both ends of the distribution named."""
    ks, pk, N = condmat_pdf()
    d = np.array(condmat_degrees())
    small = float((d <= SMALL_K).mean())
    far = int((d > TAIL_K).sum())
    assert far == 28 and N == 23133, (far, N)

    ax = Axes(FRAME, (0, 288), (0, 0.15), xticks=[0, 100, 200],
              yticks=[0, 0.05, 0.10, 0.15], yfmt=lambda v: f"{v:g}")
    body = ax.frame()
    body += axis_titles(ax, "number of coauthors $k$", "$p(k)$")
    # accent-3 carries area, never a stroke and never text: the tail band is a fill. Its
    # left edge is TAIL_K, the same constant the annotation prints -- R1 B-14: it was
    # hardcoded at 96 and landed 23px left of the "100" tick the annotation named.
    body += fill_poly([ax.P(TAIL_K, 0), ax.P(288, 0), ax.P(288, 0.018),
                       ax.P(TAIL_K, 0.018)], color="accentthree", opacity=0.75)
    body += scatter(ax, ks, pk, color="accent", d=13, expect=len(ks))

    boxes = []
    body += label_at(ax.X(40), ax.Y(0.118),
                     f"{pct(small)} of {N:,} authors\\\\sit at $k \\le {SMALL_K}$"
                     .replace(",", "{,}"),
                     color="accenttwo", anchor="west", boxes=boxes)
    body += seg(ax.P(190, 0.044), ax.P(190, 0.022), color="accenttwo", w=3.0,
                arrow="-{Latex[length=9bp]}")
    body += label_at(ax.X(190), ax.Y(0.048), f"{far} run past $k = {TAIL_K}$",
                     color="accenttwo", anchor="south", boxes=boxes)
    emit("fat-tail-reveal", body, container="full", h=H)


def fig_loglog():
    """Slide 50: identical data, logarithmic ruler."""
    ks, pk, N = condmat_pdf()
    assert len(ks) == 122
    ax = Axes(FRAME, (1, 300), (1e-5, 1), xlog=True, ylog=True,
              xticks=[1, 10, 100], yticks=[1e-4, 1e-2, 1], xfmt=dec)
    body = ax.frame()
    body += axis_titles(ax, "number of coauthors $k$", "$p(k)$")
    body += scatter(ax, ks, pk, color="accent", d=13, expect=len(ks))
    emit("loglog", body, container="full", h=H)


def fig_loglog_line():
    """Slide 51: the same points with the straight stretch fitted."""
    ks, pk, N = condmat_pdf()
    a, b, r2, n = pdf_fit()
    decades = math.log10(PDF_KMAX / PDF_KMIN)
    assert 1.9 < decades < 2.05, decades

    ax = Axes(FRAME, (1, 300), (1e-5, 1), xlog=True, ylog=True,
              xticks=[1, 10, 100], yticks=[1e-4, 1e-2, 1], xfmt=dec)
    body = ax.frame()
    body += axis_titles(ax, "number of coauthors $k$", "$p(k)$")
    body += scatter(ax, ks, pk, color="accent", d=13, expect=len(ks))

    # The fit runs to k = 279; the fitted line leaves the bottom of the frame at k = 245,
    # so it is clipped there rather than silently dropped by `Axes.line`.
    kfloor = 10 ** ((math.log10(ax.ylim[0]) - b) / a)
    fx = np.array([PDF_KMIN, min(PDF_KMAX, kfloor)], float)
    fy = 10 ** (a * np.log10(fx) + b)
    assert all(ax.inside(x, y) for x, y in zip(fx, fy)), (fx, fy)
    assert fx[1] / fx[0] > 50, f"the drawn fit only covers a factor of {fx[1] / fx[0]:.0f}"
    body += ax.line(fx, fy, color="accenttwo", w=5.0)
    # R1 B-15: the R^2 was the only inferential statistic in Part Five and nothing on the
    # slide or after it said what to do with it. The slope is what slide 52 picks up.
    body += label_at(ax.X(1.25), ax.Y(3.0e-4), f"slope $= {a:.2f}$",
                     color="accenttwo", anchor="west")
    emit("loglog-line", body, container="full", h=H)


def fig_powerlaw_def():
    """Slide 52: gamma is the steepness, and steeper means hubs run out sooner.

    The frame stops at x=400 so both curves can be named where they END, off to the
    right.  A label placed *beside* a steep diagonal in a 537bp column sits on top of
    it: every offset tried put one of the two lines straight through its own name.
    """
    ax = Axes((165, 145, 400, 356), (1, 100), (1e-6, 1), xlog=True, ylog=True,
              xticks=[1, 10, 100], yticks=[1e-4, 1e-2, 1], xfmt=dec)
    body = ax.frame()
    body += axis_titles(ax, "$k$", "$p(k)$")
    xs = np.logspace(0, 2, 400)
    drawn, ends = [], []
    for g, col in ((3.5, "accenttwo"), (2.0, "accent")):
        ys = xs ** (-g)
        # R1 B-16: a curve that runs into the x axis reads as "the distribution ends
        # here". On a log axis the floor is 1e-6, not zero, so the stroke stops short of
        # it and the reader sees it leave the frame.
        keep = ys > ax.ylim[0] * 10 ** FLOOR_LIFT
        body += ax.line(xs[keep], ys[keep], color=col, w=4.6)
        pts = curve_pts(ax, xs[keep], ys[keep])
        drawn += pts
        ends.append((pts[-1], col, g))

    # Each name goes just up and to the right of where its own line stops -- the steep
    # one leaves the bottom of the frame first, so the two names do not compete for the
    # same corner.  The x tick labels are entered as blockers: they are outside the
    # frame and the solver would otherwise write straight over "100".
    boxes = [label_box(ax.X(v), ax.y0 - 17, dec(v), "north") for v in (1, 10, 100)]
    for (at, col, g), spots in zip(ends, ([(376, 178), (376, 172), (390, 178)],
                                          [(410, 250), (410, 268), (410, 232)])):
        body += fixed_label([(x, y) for x, y in spots], f"$\\gamma = {g:g}$", drawn,
                            boxes, color=col, anchor="west")
        assert math.dist(spots[0], at) < 130, "the name has drifted off its own curve"
    emit("powerlaw-def", body, container="col", h=H)


BIN_WIDTHS = (1, 8, 32)
BIN_LO, BIN_HI = 10, 282


def _binned(w):
    """(centres, densities, count) of the cond-mat tail in bins of width w."""
    d = np.array(condmat_degrees())
    e = np.arange(BIN_LO, BIN_HI, w)
    c, _ = np.histogram(d, bins=e)
    ctr = (e[:-1] + e[1:] - 1) / 2
    dens = c / (len(d) * w)
    m = c > 0
    return ctr[m], dens[m], c[m]


def fig_binned_once():
    """The new slide before 53: the same tail, expressed once, in bins of width 1.

    R1 B-4: slides 50 and 51 plot one point per observed degree and are not binned, yet
    slide 53 asks "that plot had bins -- what if I choose different ones?".  The question
    had no referent.  This is the referent: the same authors, counted into bins, with one
    bin drawn as a caliper so the width is a visible object rather than a word.
    """
    d = np.array(condmat_degrees())
    ks = np.arange(1, int(d.max()) + 1)
    cnt = np.bincount(d, minlength=int(d.max()) + 1)[1:]
    m = cnt > 0
    assert int(m.sum()) == 122 and int(cnt.sum()) == len(d) == 23133

    ax = Axes(FRAME, (0.8, 400), (0.6, 4000), xlog=True, ylog=True,
              xticks=[1, 10, 100], yticks=[1, 10, 100, 1000], xfmt=dec, yfmt=dec)
    body = ax.frame()
    body += axis_titles(ax, "number of coauthors $k$", "authors in the bin")
    body += scatter(ax, ks[m], cnt[m], color="accent", d=13, expect=int(m.sum()))

    # One bin, drawn as a caliper at the left, where a unit of k is a whole decade wide
    # on the axis and the gap is visible. Out at k = 30 the same caliper is 5bp long --
    # which is the reason binning is a choice at all, and is what slide 54 goes on to.
    k0, ycal = 1, 200.0
    body += seg(ax.P(k0, ycal), ax.P(k0 + 1, ycal), color="annot", w=3.0,
                arrow="{Latex[length=8bp]}-{Latex[length=8bp]}")
    body += text((ax.X(k0) + ax.X(k0 + 1)) / 2, ax.Y(ycal) - 14, "one bin\\\\width 1",
                 color="annot", anchor="north")
    body += text(ax.x1 - 8, ax.Y(1400),
                 f"{int(m.sum())} bins hold all {len(d):,} authors".replace(",", "{,}"),
                 color="accenttwo", anchor="east")
    emit("binned-once", body, container="full", h=H)


def _fig_binning_panel(i):
    """One state of the three-slide build: the same tail at one bin width.

    R1 B-4: this was one figure with three panels side by side, and panels 2 and 3 had no
    y tick labels -- so the shared vertical scale the whole comparison rests on could not
    be read off the slide.  Three files, three slides, and every panel carries its ticks.
    """
    w = BIN_WIDTHS[i]
    cx, cy, cn = _binned(w)
    # The three tails must genuinely differ, or the build has nothing to show.
    fits = []
    for ww in BIN_WIDTHS:
        ax_, ay_, _ = _binned(ww)
        fits.append(float(np.polyfit(np.log10(ax_), np.log10(ay_), 1)[0]))
    counts = [len(_binned(ww)[0]) for ww in BIN_WIDTHS]
    assert len(set(counts)) == 3, counts
    assert max(fits) - min(fits) > 0.5, fits

    ax = Axes(FRAME, (9, 320), (1e-6, 1e-1), xlog=True, ylog=True,
              xticks=[10, 100], yticks=[1e-6, 1e-4, 1e-2], xfmt=dec)
    body = ax.frame()
    body += axis_titles(ax, "number of coauthors $k$", "share of authors")
    body += scatter(ax, cx, cy, color="accent", d=13, expect=len(cx))
    body += text(ax.x1 - 8, ax.Y(4.0e-2), f"bin width {w}", color="accenttwo",
                 anchor="east")
    body += text(ax.x1 - 8, ax.Y(1.2e-2), f"{len(cx)} bins with anything in them",
                 color="annot", anchor="east")
    emit(f"binning-{i + 1}", body, container="full", h=H)


def fig_binning_1():
    _fig_binning_panel(0)


def fig_binning_2():
    _fig_binning_panel(1)


def fig_binning_3():
    _fig_binning_panel(2)


# The twenty toy degrees slide 55 cuts through.  Small enough to count on the slide.
CCDF_DEMO = (7, 6, 5, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1)


def fig_ccdf_def():
    """Slide 55: the CCDF is a cut through the sorted degrees -- count everybody above.

    R1 B-1 was a Blocker on three counts, all of them about what a dot is.  Nothing said
    that a column is a node and a dot is one edge; the caption said "count everybody
    above the line" and 11 dots sat above it while the text printed "5 of 20"; and
    accent-2 filled whole columns, so 26 dots were red and 15 of them were below the very
    line the label said they were above.

    So: the encoding is stated in the drawing (a bracket under one column reading "one
    node", a caliper beside one dot reading "1 edge"), the y axis carries ticks so "above
    k = 3" can be checked, the x axis says what the columns are, and the counted thing is
    named -- **nodes** -- with exactly the five counted columns in accent-2.
    """
    ks = sorted(CCDF_DEMO, reverse=True)
    cut = 3
    above = [k for k in ks if k > cut]
    share = len(above) / len(ks)
    assert len(above) == 5 and abs(share - 0.25) < 1e-12, (above, share)
    # What is red and what is counted are the same five columns, by construction.
    red = [i for i, k in enumerate(ks) if k > cut]
    assert len(red) == len(above) == 5 and red == list(range(5))

    x0, y0 = 214, 196
    pitch, unit = 15.0, 22.0
    kmax = max(ks)

    def Y(v):
        return y0 + v * unit

    body = ""
    for v in (1, 3, 5, 7):
        body += seg((x0 - 46, Y(v)), (x0 - 37, Y(v)), color="black", w=2.2)
        body += text(x0 - 54, Y(v), f"{v}", anchor="east")
    body += seg((x0 - 46, Y(0)), (x0 - 46, Y(kmax) + 10), color="black", w=2.2)
    body += text(34, Y(kmax / 2), "degree $k$", rot=90)

    for i, k in enumerate(ks):
        for j in range(1, k + 1):
            body += dot(x0 + i * pitch, Y(j - 0.5),
                        color="accenttwo" if k > cut else "annot", d=13)
    right = x0 + (len(ks) - 1) * pitch

    # The cut, and the five columns that cross it.
    body += seg((x0 - 46, Y(cut)), (right + 18, Y(cut)), color="accenttwo", w=3.0,
                dash=DASH)
    body += text(517, Y(cut) + 10, f"$k = {cut}$", color="accenttwo",
                 anchor="south east")

    # What one column is, and what one dot is.
    bx = x0 - pitch / 2
    body += polyline([(bx, Y(0) - 8), (bx, Y(0) - 18), (bx + pitch, Y(0) - 18),
                      (bx + pitch, Y(0) - 8)], color="annot", w=3.0)
    body += seg((bx + pitch, Y(0) - 18), (x0 + 18, Y(0) - 18), color="annot", w=3.0)
    body += text(x0 + 24, Y(0) - 22, "one node", color="annot", anchor="west")
    cal = x0 + pitch + 14
    body += seg((cal, Y(5)), (cal, Y(6)), color="annot", w=2.6,
                arrow="{Latex[length=7bp]}-{Latex[length=7bp]}")
    body += text(cal + 10, Y(5.5), "1 edge", color="annot", anchor="west")

    body += text(268, 140, f"{len(ks)} nodes, sorted by degree", anchor="north")
    body += text(268, 96,
                 f"{len(above)} of {len(ks)} nodes above $k = {cut}$\\\\"
                 f"$\\mathrm{{CCDF}}({cut}) = {share:.2f}$",
                 color="accenttwo", anchor="north")
    emit("ccdf-def", body, container="col", h=H)


def fig_ccdf_condmat():
    """Slide 56: the same authors as a CCDF -- one point per distinct degree."""
    ks, su = condmat_ccdf()
    # The survival at the largest degree is exactly zero and a log axis has no room for
    # it, so 121 of the 122 distinct degrees are drawn.
    plot = [(k, s) for k, s in zip(ks, su) if s > 0]
    assert len(ks) == 122 and len(plot) == 121, (len(ks), len(plot))

    ax = Axes(FRAME, (1, 300), (1e-5, 1), xlog=True, ylog=True,
              xticks=[1, 10, 100], yticks=[1e-4, 1e-2, 1], xfmt=dec)
    body = ax.frame()
    body += axis_titles(ax, "number of coauthors $k$", "$P(k' > k)$")
    body += scatter(ax, [p[0] for p in plot], [p[1] for p in plot], color="accent", d=13,
                    expect=121)
    emit("ccdf-condmat", body, container="full", h=H)


def fig_cdf_vs_ccdf():
    """Slide 57: the CDF piles up against one; the CCDF spends its range on the tail.

    R1 B-2 was a Blocker: one "share of authors" title sat at the far left over a linear
    panel and a logarithmic one, and nothing said so -- the unannounced change of ruler
    is exactly what produces the difference in shape the slide asks the room to read, on
    a deck whose Part Five argument is that an unannounced change of ruler misleads you.
    Each panel now carries its own y title, its own scale word, and the reason: the CDF's
    values run to 1, which a log axis cannot spread; the CCDF's run to 0, which it can.
    """
    ks, su = condmat_ccdf()
    cdf = 1 - su
    assert abs(cdf[-1] - 1.0) < 1e-12 and cdf[0] < 0.11, (cdf[0], cdf[-1])

    left = Axes((174, 152, 520, 286), (1, 300), (0, 1.05), xlog=True,
                xticks=[1, 10, 100], yticks=[0, 0.5, 1.0], xfmt=dec,
                yfmt=lambda v: f"{v:g}")
    right = Axes((744, 152, 1058, 286), (1, 300), (1e-5, 1), xlog=True, ylog=True,
                 xticks=[1, 10, 100], yticks=[1e-4, 1e-2, 1], xfmt=dec)
    body = left.frame() + right.frame()
    body += curve(left, ks, cdf, color="annot", w=4.6)
    body += curve(right, ks, su, color="accent", w=4.6)

    for ax, ytitle, ytx in ((left, "$P(k' \\le k)$", 34), (right, "$P(k' > k)$", 604)):
        body += text(ytx, (ax.y0 + ax.y1) / 2, ytitle, rot=90)
        body += text((ax.x0 + ax.x1) / 2, 82, "number of coauthors $k$", anchor="north")

    # Each panel says which ruler it is drawn on, and why that ruler was chosen. Two
    # lines above each frame: the panels are 134bp tall so there is no room inside them
    # for three lines of prose, and prose over a curve is what put "physicists" on the
    # yeast tail in round 1.
    boxes = []
    body += label_at((left.x0 + left.x1) / 2, 372,
                     "CDF · linear $y$\\\\values crowd at 1",
                     color="annot", anchor="north", boxes=boxes)
    body += label_at((right.x0 + right.x1) / 2, 372,
                     "CCDF · log $y$\\\\values reach down to 0",
                     color="accent", anchor="north", boxes=boxes)
    emit("cdf-vs-ccdf", body, container="full", h=H)


DERIV_GAMMA = 2.5          # the exponent the schematic is drawn at
DERIV_KCUT = 10.0          # where the tail is cut


def fig_slope_derivation():
    """Slide 59: adding up the tail raises the exponent by one -- drawn, not written.

    R1 B-5: this was three numbered text lines and a gray gloss column, which is not a
    visual.  Now it draws the thing being integrated -- the power law with everything
    above k shaded -- and that shaded mass re-plotted as one point on the CCDF beside it.

    No integral sign anywhere: LaTeX declares math sizes only to about 25pt, so the
    large-operator font does not follow `\\selectfont` and a 44pt `\\int` renders at
    roughly 10pt, with or without `\\displaystyle`.  The slide body sets it in KaTeX.
    """
    g = DERIV_GAMMA
    k0 = DERIV_KCUT
    xs = np.logspace(0, 2, 240)
    pdf = xs ** (-g)
    cc = xs ** (-(g - 1))
    # The CCDF exponent is one smaller: that is the whole content of the figure.
    assert abs((g - 1) - (g - 1)) < 1e-12 and abs(cc[0] - 1) < 1e-12

    left = Axes((174, 150, 500, 282), (1, 100), (1e-6, 1), xlog=True, ylog=True,
                xticks=[1, 10, 100], yticks=[1e-4, 1e-2, 1], xfmt=dec)
    right = Axes((724, 150, 1040, 282), (1, 100), (1e-4, 1), xlog=True, ylog=True,
                 xticks=[1, 10, 100], yticks=[1e-4, 1e-2, 1], xfmt=dec)
    body = left.frame() + right.frame()

    # Everything above k, as area. accent-3 is a fill here, which is what it is for.
    tail = xs >= k0
    poly = ([left.P(k0, left.ylim[0])]
            + [left.P(x, y) for x, y in zip(xs[tail], pdf[tail])]
            + [left.P(xs[tail][-1], left.ylim[0])])
    body += fill_poly(poly, color="accentthree", opacity=0.8)
    body += left.line(xs, pdf, color="accent", w=4.6)
    body += seg(left.P(k0, left.ylim[0]), left.P(k0, k0 ** -g), color="annot", w=2.6,
                dash=DASH)
    body += text(left.X(k0), left.y0 - 17, "$k$", color="accenttwo", anchor="north")
    body += text(left.X(26), left.Y(0.06), "everything\\\\above $k$", color="accenttwo",
                 anchor="west")

    # The same mass, as one point on the CCDF.
    body += right.line(xs, cc, color="accent", w=4.6)
    body += dot(*right.P(k0, k0 ** -(g - 1)), color="accenttwo", d=20)
    body += text(right.X(k0) + 16, right.Y(k0 ** -(g - 1)) + 10, "one point",
                 color="accenttwo", anchor="south west")

    body += seg((512, 216), (712, 216), color="annot", w=3.4,
                arrow="-{Latex[length=11bp]}")
    body += text(612, 230, "add it up", color="annot", anchor="south")

    body += text(34, (left.y0 + left.y1) / 2, "$p(k)$", rot=90)
    body += text(584, (right.y0 + right.y1) / 2, "$P(k' > k)$", rot=90)
    body += text((left.x0 + left.x1) / 2, 86, "$k$", anchor="north")
    body += text((right.x0 + right.x1) / 2, 86, "$k$", anchor="north")
    body += text((left.x0 + left.x1) / 2, 330, "$p(k) \\sim k^{-\\gamma}$",
                 anchor="north")
    body += text(875, 330, "$P(k' > k) \\sim k^{-(\\gamma-1)}$", anchor="north")
    body += text(1060, 372,
                 "the log-log slope goes from $-\\gamma$ to $1-\\gamma$",
                 color="accenttwo", anchor="north east")
    body += text(14, 372, f"drawn at $\\gamma = {g:g}$", color="annot",
                 anchor="north west")
    emit("slope-derivation", body, container="full", h=H)


def _slope_panel():
    """The worksheet's CCDF, its fitted line, and the -1.3 slope triangle.

    Shared by slides 60 and 61 so the picture does not move under the answer.  Returns
    (body, axes, fitted slope, the strings it draws).
    """
    ks, su, (a, b, r2, n) = worksheet_ccdf()
    assert round(a, 1) == float(WS_SLOPE), (a, float(WS_SLOPE))

    ax = Axes((175, 145, 690, 356), (1, 1000), (1e-5, 1), xlog=True, ylog=True,
              xticks=[1, 10, 100, 1000], yticks=[1e-4, 1e-2, 1], xfmt=dec)
    body = ax.frame()
    body += axis_titles(ax, "$k$", "$P(k' > k)$")
    plot = [(k, s) for k, s in zip(ks, su) if s > 0 and ax.inside(k, s)]
    body += scatter(ax, [p[0] for p in plot], [p[1] for p in plot], color="accent", d=9,
                    expect=len(plot))

    # The triangle is a construction: one decade across, exactly 1.3 decades down.
    k0, s0 = 5.0, 0.12
    k1 = k0 * 10
    s1 = s0 * 10 ** float(WS_SLOPE)
    body += ax.line([WS_KMIN, WS_KMAX * 2],
                    [s0 * (WS_KMIN / k0) ** float(WS_SLOPE),
                     s0 * (WS_KMAX * 2 / k0) ** float(WS_SLOPE)],
                    color="accenttwo", w=5.0)
    body += polyline([ax.P(k0, s0), ax.P(k1, s0), ax.P(k1, s1)], color="annot", w=3.0)
    said = ["1 decade", "1.3"]
    body += text((ax.X(k0) + ax.X(k1)) / 2, ax.Y(s0) + 14, said[0], color="annot",
                 anchor="south")
    body += text(ax.X(k1) + 16, (ax.Y(s0) + ax.Y(s1)) / 2, said[1], color="annot",
                 anchor="west")
    said += ["$k$", "$P(k' > k)$", "1", "10", "100", "1000", "$10^{-4}$", "$10^{-2}$"]
    return body, ax, a, said


def fig_slope_worksheet():
    """Slide 60: the measured slope is on the picture; the exponent is not."""
    body, ax, a, said = _slope_panel()
    # Only the measured slope. Printing "1 - gamma = -1.3" here would hand the room the
    # substitution, and slide 60's whole job is the vote between 1.3 and 2.3.
    mine = ["measured slope", f"${float(WS_SLOPE):.1f}$", "$\\gamma \\;=$"]
    body += text(880, 274, mine[0], color="annot")
    body += text(880, 208, mine[1], color="accenttwo", size=52)
    body += text(866, 134, mine[2], color="black", size=46, anchor="east")
    body += seg((880, 114), (1024, 114), color="black", w=3.4)
    # Slide 60 is the question, so the answer may not be anywhere on the figure.  The
    # check runs over the strings drawn, not over the TikZ body: coordinates are full of
    # digits and "2.3" turns up in a dozen of them.
    for s in said + mine:
        for banned in ("2.3", "2{.}3"):
            assert banned not in s, \
                f"slope-worksheet leaks the answer in {s!r} -- slide 60 is the question"
    emit("slope-worksheet", body, container="full", h=H)


def fig_slope_answer():
    """Slide 61: 1 - gamma = -1.3, so gamma = 2.3 -- not 1.3."""
    body, ax, a, _ = _slope_panel()
    gamma = Fraction(1) - WS_SLOPE
    assert gamma == WS_GAMMA == Fraction(23, 10), gamma
    body += text(880, 300, f"$1 - \\gamma = {float(WS_SLOPE):.1f}$", color="annot")
    body += text(880, 218, f"$\\gamma = {float(gamma):.1f}$", color="accenttwo", size=52)
    body += text(880, 128, f"$\\gamma = {-float(WS_SLOPE):.1f}$", color="annot", size=44)
    body += seg((806, 128), (954, 128), color="accenttwo", w=3.0)
    emit("slope-answer", body, container="full", h=H)


def fig_exercise_card():
    """Slide 62: the handout pointer."""
    x0, x1, y0, y1 = 18, 519, 96, 344
    body = (f"\\draw[line width=4bp,draw=accent,rounded corners=14bp] "
            f"({x0},{y0}) rectangle ({x1},{y1});\n")
    body += text((x0 + x1) / 2, y1 - 34, "Data Visualization", color="accent")
    body += seg((x0 + 26, y1 - 70), (x1 - 26, y1 - 70), color="accent", w=3.0)
    body += text((x0 + x1) / 2, 232, "one distribution")
    body += text((x0 + x1) / 2, 184, "four pictures")
    body += text((x0 + x1) / 2, 136, "one of them lies", color="accenttwo")
    emit("exercise-card", body, container="col", h=H)


# --------------------------------------------------------------------------- Part 6
def fig_hubs_share():
    """Slide 64: the Internet's degree ranking, and what the top 1% is holding."""
    g = internet_as()
    d = np.sort(np.array([x for _, x in g.degree()]))[::-1]
    n_top, share = top_share(g, 0.01)
    assert n_top == 65, n_top
    assert abs(share - d[:n_top].sum() / d.sum()) < 1e-12
    ranks = np.arange(1, len(d) + 1)

    ax = Axes(FRAME, (1, 8000), (1, 2000), xlog=True, ylog=True,
              xticks=[1, 10, 100, 1000], yticks=[1, 10, 100, 1000], xfmt=dec, yfmt=dec)
    body = ax.frame()
    body += axis_titles(ax, "rank", "degree")
    body += scatter(ax, ranks[n_top:], d[n_top:], color="annot", d=6,
                    expect=len(d) - n_top)
    body += scatter(ax, ranks[:n_top], d[:n_top], color="accenttwo", d=12, expect=n_top)
    body += seg(ax.P(n_top, 1), ax.P(n_top, 2000), color="accenttwo", w=3.0, dash=DASH)
    body += label_at(ax.x1 - 10, ax.Y(220),
                     f"top {pct(0.01)} $=$ {n_top} nodes\\\\hold {pct(share, 1)} of all"
                     f"\\\\{int(d.sum()):,} edge ends".replace(",", "{,}"),
                     color="accenttwo", anchor="east")
    emit("hubs-share", body, container="full", h=H)


def fig_universality():
    """Slide 65: three unrelated systems, one shape.  Labelled in place, no legend."""
    ax = Axes(FRAME, (1, 2000), (1e-5, 1), xlog=True, ylog=True,
              xticks=[1, 10, 100, 1000], yticks=[1e-4, 1e-2, 1], xfmt=dec)
    body = ax.frame()
    body += axis_titles(ax, "degree $k$", "$P(k' > k)$")

    sets = [("physicists", np.array(condmat_degrees()), "accent", 0.55),
            ("Internet", np.array(degrees_of("internet")), "accenttwo", 0.90),
            ("yeast", np.array(degrees_of("yeast")), "black", 0.75)]
    kmax, drawn, anchors = {}, [], []
    for name, d, col, frac in sets:
        ks, su = ccdf(d)
        kmax[name] = int(d.max())
        body += curve(ax, ks, su, color=col, w=4.2)
        pts = curve_pts(ax, ks, su)
        drawn += pts
        anchors.append((name, col, pts[int(len(pts) * frac)]))
    assert kmax == {"physicists": 279, "Internet": 1458, "yeast": 56}, kmax

    boxes = []
    for name, col, at in anchors:
        body += curve_label(ax, name, at, drawn, boxes, color=col)
    emit("universality", body, container="full", h=H)


def fig_poisson_ccdf():
    """Slide 67: wire it at random and the tail is not smaller, it is absent."""
    d = np.array(degrees_of("er"))
    k1, var = float(d.mean()), float(d.var())
    assert abs(var / k1 - 1) < 0.05 and int(d.max()) == 15, (var / k1, d.max())
    ks, su = ccdf(d)

    ax = Axes(FRAME, (1, 300), (1e-5, 1), xlog=True, ylog=True,
              xticks=[1, 10, 100], yticks=[1e-4, 1e-2, 1], xfmt=dec)
    body = ax.frame()
    body += axis_titles(ax, "degree $k$", "$P(k' > k)$")
    body += curve(ax, ks, su, color="accenttwo", w=4.6)
    plot = [(k, s) for k, s in zip(ks, su) if s > 0 and ax.inside(k, s)]
    body += scatter(ax, [p[0] for p in plot], [p[1] for p in plot], color="accenttwo",
                    d=13, expect=len(plot))
    # The whole distribution is over by k = 15, so the right half of the panel is empty
    # -- which is the point of the slide, and where the numbers go.
    drawn = curve_pts(ax, ks, su)
    boxes = []
    body += fixed_label([(1050, 262)],
                        f"largest degree {int(d.max())}\\\\"
                        f"$\\mathrm{{Var}}/\\langle k \\rangle = {var / k1:.2f}$",
                        drawn, boxes, color="accenttwo", anchor="east")
    body += fixed_label([(1050, 338)],
                        f"$\\langle k \\rangle = {k1:.1f}$, {len(d):,} nodes"
                        .replace(",", "{,}"),
                        drawn, boxes, color="annot", anchor="east")
    emit("poisson-ccdf", body, container="full", h=H)


def fig_three_ccdfs():
    """Slide 68: same average degree, three shapes."""
    ba = np.array(degrees_of("ba"))
    er = np.array(degrees_of("er"))
    lat = np.array(lattice_degrees())
    for name, d in (("power law", ba), ("random", er), ("lattice", lat)):
        assert abs(d.mean() - 4) < 0.02, (name, d.mean())
    assert set(lat.tolist()) == {4} and lat.var() == 0
    assert int(ba.max()) == 315 and int(er.max()) == 15

    ax = Axes(FRAME, (1, 500), (1e-5, 1), xlog=True, ylog=True,
              xticks=[1, 10, 100], yticks=[1e-4, 1e-2, 1], xfmt=dec)
    body = ax.frame()
    body += axis_titles(ax, "degree $k$", "$P(k' > k)$")
    drawn, anchors = [], []
    for d, col, name, frac in ((ba, "accent", "power law", 0.72),
                               (er, "accenttwo", None, 0)):
        ks, su = ccdf(d)
        body += curve(ax, ks, su, color=col, w=4.6)
        pts = curve_pts(ax, ks, su)
        drawn += pts
        if name:
            anchors.append((name, col, pts[int(len(pts) * frac)]))
    # Every node has exactly four, so the survival is 1 up to k=3 and 0 from k=4: a wall.
    wall = [ax.P(1, 1), ax.P(4, 1), (ax.X(4), ax.y0)]
    body += polyline(wall, color="black", w=4.6)
    drawn += curve_pts(ax, [1, 4], [1, 1]) + [(ax.X(4), ax.y0 + t) for t in
                                              range(0, int(ax.y1 - ax.y0), 7)]
    anchors.append(("lattice", "black", (ax.X(4), ax.y0 + (ax.y1 - ax.y0) * 0.45)))

    boxes = [label_box((ax.x0 + ax.x1) / 2, 372,
                       visible("all three networks: $\\langle k \\rangle = 4$"), "north")]
    body += text((ax.x0 + ax.x1) / 2, 372,
                 "all three networks: $\\langle k \\rangle = 4$", color="annot",
                 anchor="north")
    # The random curve falls off the bottom of the frame, so every offset around a point
    # ON it lands either under the axis or on the power law.  It takes the clear pocket
    # just right of its own cliff -- claimed first, so the solver works around it.
    body += fixed_label([(626, 200), (626, 232), (660, 205), (600, 176)], "random",
                        drawn, boxes, color="accenttwo")
    for name, col, at in anchors:
        body += curve_label(ax, name, at, drawn, boxes, color=col)
    emit("three-ccdfs", body, container="full", h=H)


# Slide 70's growth illustration is its own tiny sequence: four nodes, then two arrivals.
# It is about arriving, not about preferring, so it does not need the 24-node history.
STEP_POS = {0: (72, 96), 1: (196, 62), 2: (140, 196), 3: (256, 172),
            4: (44, 214), 5: (268, 62)}
STEP_BASE = [(0, 1), (0, 2), (1, 2), (1, 3)]
STEP_ARRIVALS = [(4, [0, 2]), (5, [1, 3])]


def fig_ba_growth():
    """Slide 70: a node arrives, brings two edges, and stays.  Twice."""
    frames, nodes, edges = [], [0, 1, 2, 3], list(STEP_BASE)
    frames.append((list(nodes), list(edges), None, []))
    for new, targets in STEP_ARRIVALS:
        nodes = nodes + [new]
        new_edges = [(new, t) for t in targets]
        edges = edges + new_edges
        frames.append((list(nodes), list(edges), new, new_edges))
    assert all(len(e) == 2 for _, _, _, e in frames[1:]), "each arrival brings m = 2"

    for nds, eds, _, _ in frames:
        sub = {v: STEP_POS[v] for v in nds}
        bad = clearance_bad(eds, sub, r=NODE / 2 + 3)
        assert not bad, f"ba-growth: edge through a disc -- {bad[:3]}"

    body = ""
    for i, (nds, eds, new, new_edges) in enumerate(frames):
        ox = 24 + i * 356
        pos = {v: (STEP_POS[v][0] + ox, STEP_POS[v][1] + 74) for v in nds}
        hot = {frozenset(e) for e in new_edges}
        for a, b in eds:
            on = frozenset((a, b)) in hot
            body += seg(pos[a], pos[b], color="accenttwo" if on else "black",
                        w=4.6 if on else 2.6)
        for v in nds:
            body += disc(pos[v][0], pos[v][1], "",
                         fill="accenttwo" if v == new else "accent", size=NODE)
        body += text(ox + 156, 350, f"{i + 1}", color="annot")
        if i < len(frames) - 1:
            body += text(ox + 330, 206, "$\\rightarrow$", color="annot", size=52)
    emit("ba-growth", body, container="full", h=H)


# The quiz panels: two sketches on the left, one CCDF panel on the right.  A and B are
# identities, not answers -- the room needs them to say which tail belongs to which
# picture, and neither letter says which rule built it.
QUIZ_A = (8, 26, 320, 340)          # uniform growth
QUIZ_B = (330, 26, 642, 340)        # preferential attachment
QUIZ_FRAME = (818, 145, 1058, 356)


def _quiz_body(labels):
    """Both sketches and both tails.  `labels` is the pair drawn over the sketches."""
    ba = np.array(degrees_of("ba"))
    ua = np.array(degrees_of("uniform"))
    assert abs(ba.mean() - 4) < 0.01 and abs(ua.mean() - 4) < 0.01
    assert int(ba.max()) == 315 and int(ua.max()) == 29
    assert len(ba) == len(ua) == 20000

    ea, eb = growth_edges(False), growth_edges(True)
    assert len(ea) == len(eb), (len(ea), len(eb))       # same n, same edge count
    assert len({v for e in ea for v in e}) == GROWTH_N

    body = ""
    for box, pref, col, lab in ((QUIZ_A, False, "accent", labels[0]),
                                (QUIZ_B, True, "accenttwo", labels[1])):
        pos = growth_pos(pref, box)
        frame = {"nodes": list(range(GROWTH_N)),
                 "edges": [tuple(e) for e in growth_edges(pref)],
                 "new_node": None, "new_edges": []}
        body += draw_growth(frame, pos, fill=col, size=GROWTH_NODE)
        body += text((box[0] + box[2]) / 2, 372, lab, color=col, anchor="north")

    ax = Axes(QUIZ_FRAME, (1, 400), (1e-5, 1), xlog=True, ylog=True,
              xticks=[1, 10, 100], yticks=[1e-4, 1e-2, 1], xfmt=dec)
    body += ax.frame()
    body += text((ax.x0 + ax.x1) / 2, 79, "degree $k$", anchor="north")
    body += text(676, (ax.y0 + ax.y1) / 2, "$P(k' > k)$", rot=90)
    drawn, anchors = [], []
    for d, col, frac in ((ua, "accent", 0.80), (ba, "accenttwo", 0.72)):
        ks, su = ccdf(d)
        body += curve(ax, ks, su, color=col, w=4.2)
        pts = curve_pts(ax, ks, su)
        drawn += pts
        anchors.append((col, pts[int(len(pts) * frac)]))
    said = list(labels) + ["degree $k$", "$P(k' > k)$", "1", "10", "100",
                           "$10^{-4}$", "$10^{-2}$"]
    return body, ax, ba, ua, said, drawn, anchors


def _quiz_curve_labels(ax, drawn, anchors, texts):
    """Name each tail beside its own curve, inside the CCDF frame.

    The tick labels go in as blockers: with the bounds opened up to the whole right-hand
    third, "max 29" was written straight across the 10 and 100 on the axis.
    """
    body = ""
    boxes = [label_box(ax.X(v), ax.y0 - 17, dec(v), "north") for v in (1, 10, 100)]
    for (col, at), s in zip(anchors, texts):
        body += curve_label(ax, s, at, drawn, boxes, color=col)
    return body


def fig_quiz():
    """Slide 72: two networks and two tails, and nothing that says which rule made them."""
    body, ax, ba, ua, said, drawn, anchors = _quiz_body(("A", "B"))
    said += ["A", "B"]
    body += _quiz_curve_labels(ax, drawn, anchors, ("A", "B"))
    # Checked against the strings drawn, not the TikZ body -- coordinates are full of
    # digits and "315" turns up in several of them.
    for s in said:
        for banned in ("prefer", "uniform", "random", "grew",
                       str(int(ba.max())), str(int(ua.max()))):
            assert banned not in s, \
                f"quiz.png leaks {banned!r} in {s!r} -- slide 72 is the question"
    emit("quiz", body, container="full", h=H)


def fig_quiz_answer():
    """Slide 73: the same two, named, with the tails' largest degrees."""
    body, ax, ba, ua, _, drawn, anchors = _quiz_body(("no preference", "preference"))
    # Each tail is labelled with its own largest degree, at the end of the curve -- which
    # is where that degree sits on the axis, so the number reads as the point it marks.
    body += _quiz_curve_labels(ax, drawn, anchors,
                               (f"{int(ua.max())}", f"{int(ba.max())}"))
    emit("quiz-answer", body, container="full", h=H)


FIGURES = [
    ("linear-axes", fig_linear_axes),
    ("fat-tail-reveal", fig_fat_tail_reveal),
    ("loglog", fig_loglog),
    ("loglog-line", fig_loglog_line),
    ("powerlaw-def", fig_powerlaw_def),
    ("binned-once", fig_binned_once),
    ("binning-1", fig_binning_1),
    ("binning-2", fig_binning_2),
    ("binning-3", fig_binning_3),
    ("ccdf-def", fig_ccdf_def),
    ("ccdf-condmat", fig_ccdf_condmat),
    ("cdf-vs-ccdf", fig_cdf_vs_ccdf),
    ("slope-derivation", fig_slope_derivation),
    ("slope-worksheet", fig_slope_worksheet),
    ("slope-answer", fig_slope_answer),
    ("exercise-card", fig_exercise_card),
    ("hubs-share", fig_hubs_share),
    ("universality", fig_universality),
    ("poisson-ccdf", fig_poisson_ccdf),
    ("three-ccdfs", fig_three_ccdfs),
    ("ba-growth", fig_ba_growth),
    ("quiz", fig_quiz),
    ("quiz-answer", fig_quiz_answer),
]

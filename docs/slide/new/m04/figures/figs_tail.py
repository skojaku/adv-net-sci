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
from fractions import Fraction
from functools import lru_cache

import networkx as nx
import numpy as np

from figlib import (DASH, DASH_LONG, FONT, NODE, Axes, boxes_overlap, clearance_bad,
                    crossings, disc, dot, emit, fill_poly, label_box, pct, polyline,
                    seg, text, visible)
from verify_numbers import (ba_graph, ccdf, ccdf_fit, condmat, internet_as, net_stats,
                            top_share, uniform_growth_graph, yeast_ppi)

H = 380                                  # every figure here is a plain `.fig` (380px cap)

# R2 B2-10 / C2-7: across four consecutive slides accent-2 meant the hubs, then the
# hub-rich Internet, then the random graph with no hubs at all. From Part Six on there is
# one role and it is declared here, not chosen per figure.
HUBS, NO_HUBS = "accent", "accenttwo"

# The one full-width plot frame.  The x title sits 66bp under the axis and the y title is
# placed by hand at x=30 -- `Axes.frame`'s own y title lands on top of a "$10^{-4}$" tick
# label, which is about 90bp wide at the 36pt floor.
FRAME = (185, 145, 1058, 356)
# In a 537bp column the right-hand tick label is what runs off the page: "100" centred on
# the last tick needs 27bp of its own, so the frame stops at 500, not at the canvas.
FRAME_COL = (165, 145, 500, 356)

# R3 B3-3: four consecutive CCDF panels carried four different vertical rulers -- one
# decade of P(k'>k) measured 42.2, 34.7, 27.2 and 21.8px -- on the slides that spend ten
# of them teaching that an unannounced change of ruler misleads you. One box, one y range
# and one set of y ticks for every CCDF in the module; only x adapts to the data, and the
# band above the frame is where a figure's own numbers go.
CCDF_BOX = (185, 118, 1058, 306)
CCDF_YLIM = (1e-5, 1)
CCDF_YTICKS = [1e-4, 1e-2, 1]
CCDF_NOTE_Y = 372
CCDF_DECADE = (CCDF_BOX[3] - CCDF_BOX[1]) / 5
# R4 B4-3: B3-3 equalised the vertical ruler and the horizontal one is what sets apparent
# slope. One decade of k measured 264.5 / 264.5 / 545.0 / 323.5px across four panels, so a
# slope of -1 drew at 8.1 degrees on one and 3.9 on another -- and the same random graph
# appears on two of them, reading as a gentle roll-off here and a wall there. Both rulers
# are fixed now and the frame's WIDTH varies with the range instead: a short x range gives
# a narrow panel, not a stretched axis.
CCDF_PX_PER_DECADE = (CCDF_BOX[2] - CCDF_BOX[0]) / math.log10(2000)
# The linear pair (slides 51 and 52) shares the same box, so the two views of the same
# data are the same size, and so both have the band above the frame for their numbers.
LIN_BOX = CCDF_BOX


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
    """A ring lattice at cond-mat's mean degree: every node with exactly eight."""
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


def ccdf_dense(d):
    """P(k' > k) at EVERY integer k, not only at the degrees that happen to occur.

    R3 B3-12: `ccdf()` evaluates at the observed degrees, so the random graph's curve
    stopped at k = 21 -- the largest degree below its maximum that anything actually had
    -- while the figure's headline said "largest degree 28". Evaluated densely the curve
    runs to the last k with anyone above it, which is where the largest degree is.
    """
    d = np.asarray(d)
    ks = np.arange(1, int(d.max()) + 1)
    su = np.array([(d > k).mean() for k in ks])
    sparse_k, sparse_s = ccdf(d)
    lookup = dict(zip(ks.tolist(), su.tolist()))
    assert all(abs(lookup[int(k)] - s) < 1e-12 for k, s in zip(sparse_k, sparse_s)
               if int(k) in lookup), "the dense CCDF disagrees with verify_numbers' own"
    return ks, su


def ccdf_axes(xlim, xticks, ylim=None, yticks=None):
    """The module's one CCDF ruler: fixed bp per decade on BOTH axes.

    The box's height is fixed and its width follows the data's range, so every log-log
    panel in the module has the same aspect and a slope drawn on one can be compared with
    a slope drawn on another.
    """
    x0, y0, _, y1 = CCDF_BOX
    x1 = x0 + math.log10(xlim[1] / xlim[0]) * CCDF_PX_PER_DECADE
    assert x1 <= CCDF_BOX[2] + 1e-6, f"x range {xlim} needs {x1 - x0:.0f}bp of frame"
    return Axes((x0, y0, x1, y1), xlim, ylim or CCDF_YLIM, xlog=True, ylog=True,
                xticks=xticks, yticks=yticks or CCDF_YTICKS, xfmt=dec)


# --------------------------------------------------------------------------- plot helpers
def axis_titles(ax, xtitle, ytitle, ytx=30):
    """Both axis titles, placed by hand so neither can land on a tick label."""
    o = text((ax.x0 + ax.x1) / 2, ax.y0 - 66, xtitle, anchor="north")
    o += text(ytx, (ax.y0 + ax.y1) / 2, ytitle, rot=90)
    return o


def num(x):
    """A thousands-separated integer, with TeX's own comma so it does not kern shut."""
    return f"{int(x):,}".replace(",", "{,}")


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


def _leader(at, b, gap=5.0):
    """A line from a point on the curve to the nearest edge of its label's box."""
    cx = min(max(at[0], b[0]), b[2])
    cy = min(max(at[1], b[1]), b[3])
    d = math.hypot(cx - at[0], cy - at[1]) or 1.0
    return (at, (at[0] + (cx - at[0]) * (1 - gap / d),
                 at[1] + (cy - at[1]) * (1 - gap / d)))


def _seg_near(seg_pts, p, tol=6.0):
    (x0, y0), (x1, y1) = seg_pts
    dx, dy = x1 - x0, y1 - y0
    L2 = dx * dx + dy * dy or 1e-9
    u = max(0.0, min(1.0, ((p[0] - x0) * dx + (p[1] - y0) * dy) / L2))
    return math.hypot(x0 + u * dx - p[0], y0 + u * dy - p[1]) < tol


def _box_dist(b, p):
    """Distance from the point `p` to the rectangle `b`, zero if inside."""
    return math.hypot(max(b[0] - p[0], 0, p[0] - b[2]), max(b[1] - p[1], 0, p[1] - b[3]))


def curve_label(ax, s, ats, own, boxes, others=(), color="black", size=FONT, pad=7,
                bounds=None, floor=34, margin=1.4, force_leader=False):
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
    ats = [ats] if isinstance(ats[0], (int, float)) else list(ats)
    for at, r, deg in (() if force_leader else
                       ((a, r, d) for a in ats for r in (34, 46, 60, 78, 98, 122)
                        for d in _SIDES)):
        if True:
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
    # Nothing satisfies the margin. On `universality` nothing can: measured over every
    # anchor, radius and side, the physicists curve's best achievable ratio is 1.23 with
    # its nearest neighbour 14bp away, because the other two bracket it for its whole
    # length on a frame the module now shares. Proximity has run out as a cue, so the
    # label gets a leader instead of a worse position -- placed where there is actually
    # room, joined to its own curve by a line, and asserted to cross nothing else.
    best = None
    for at, r, deg in ((a, r, d) for a in ats for r in (46, 60, 78, 98, 122, 150)
                       for d in _SIDES):
        a = math.radians(deg)
        cx, cy = at[0] + r * math.cos(a), at[1] + r * math.sin(a)
        b = label_box(cx, cy, v, "center", size=size)
        if not (bounds[0] <= b[0] and b[2] <= bounds[2]
                and bounds[1] <= b[1] and b[3] <= bounds[3]):
            continue
        if any(boxes_overlap(b, o) for o in boxes):
            continue
        if any(_box_dist(b, q) <= pad for q in own) or \
           any(_box_dist(b, q) <= pad for q in others):
            continue
        lead = _leader(at, b)
        if any(_seg_near(lead, q) for q in others):
            continue
        d_oth = min((_box_dist(b, q) for q in others), default=1e9)
        if best is None or d_oth > best[0]:
            best = (d_oth, cx, cy, b, lead)
    if best is not None:
        _, cx, cy, b, lead = best
        boxes.append(b)
        return (seg(lead[0], lead[1], color="annot", w=2.0, record=False)
                + text(cx, cy, s, color=color, anchor="center", size=size))

    raise SystemExit(
        f"no clear spot for the curve label {s!r} -- it must end up nearer its own "
        f"curve than any other, and there is no room for a leader either. Move its "
        f"anchor, shorten it or widen the panel; do not shrink the type.")


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
# R2 C2-6: at 24 nodes and 45 edges the two sketches crossed 21 and 20 times with 30bp
# discs, against 39-40px discs everywhere else in the deck, and the slide asked the room
# to tell two hairballs apart. Fourteen nodes and 25 edges come down to a handful of
# crossings at full-size discs, and the hub is traceable spoke by spoke -- which is the
# only thing that slide needs. FIXES_R2 allows exactly this trade.
GROWTH_N, GROWTH_M = 14, 2
PREF_SEED, UNIF_SEED = 8, 37        # a degree-10 hub against a perfectly flat 5,5,5,5
GROWTH_NODE = NODE                  # 40bp, as every other graph in the deck
CROSSING_BUDGET = 8
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
        lit = []
        for tgt in targets:
            cur.append((new, tgt))
            lit.append((new, tgt))
            # R2 C2-3: `new_edges` used to hold only the edge added in THIS frame, so the
            # arrival's second frame lit one red edge and one black -- under a slide that
            # says "a node arrives, brings TWO edges". It holds every edge the arriving
            # node has brought so far, so the frame where it finishes shows both.
            frames.append({"nodes": list(nodes), "edges": list(cur),
                           "new_node": new, "new_edges": list(lit)})
    assert len(frames) == 1 + GROWTH_M * (GROWTH_N - 3), len(frames)
    assert len(frames[-1]["new_edges"]) == GROWTH_M, "the last arrival lost an edge"
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
def growth_layout(preferential=True, box=GROWTH_BOX, node=GROWTH_NODE, stretch=False,
                  pick=0):
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
    x0, y0, x1, y1 = box
    r, pad = node / 2, node / 2 + 4

    def solve(lseed):
        p = nx.spring_layout(g, seed=lseed, iterations=500, k=1.5 / math.sqrt(GROWTH_N))
        Q = np.array([p[i] for i in range(GROWTH_N)], float)
        Q -= Q.min(0)
        sx = (x1 - x0 - 2 * pad) / max(Q[:, 0].max(), 1e-9)
        sy = (y1 - y0 - 2 * pad) / max(Q[:, 1].max(), 1e-9)
        Q *= np.array([sx, sy]) if stretch else min(sx, sy)
        Q[:, 0] += x0 + pad + (x1 - x0 - 2 * pad - Q[:, 0].max()) / 2
        Q[:, 1] += y0 + pad + (y1 - y0 - 2 * pad - Q[:, 1].max()) / 2
        Q = _relax(Q, edges, r, box)
        pos = {i: (float(Q[i, 0]), float(Q[i, 1])) for i in range(GROWTH_N)}
        if clearance_bad(edges, pos, r=r + 2):
            return None
        gap = min(math.dist(pos[i], pos[j]) for i in range(GROWTH_N)
                  for j in range(i + 1, GROWTH_N))
        if gap < node + 2:
            return None
        return len(crossings(edges, pos)), pos

    # R2 C2-6: a spring layout is not a drawing gate. Both graphs are non-planar, so some
    # crossings are forced -- but 21 of them is not forced, it is the first seed that came
    # out. Take the fewest over forty seeds and hold the result to a budget, so a change
    # to the graph or the box cannot quietly put the hairball back.
    #
    # `pick` selects the pick-th best instead of the best. That exists for R2 C2-1: the
    # GIF used to be the quiz's answer panel node for node, so slide 076 showed slide
    # 077's answer, and the room could vote by matching pictures. The GIF takes a
    # different arrangement of the SAME graph -- same generator, same m, same n, same
    # edges, all still asserted -- and every candidate has passed the same budget.
    ranked = sorted((s for s in (solve(sd) for sd in range(1, 41)) if s),
                    key=lambda s: s[0])
    assert len(ranked) > pick, "no growth layout with clean disc clearance"
    n_cross, pos = ranked[pick]
    assert n_cross <= CROSSING_BUDGET, (
        f"growth layout crosses itself {n_cross} times, budget {CROSSING_BUDGET} -- "
        f"drop a node or widen the box; do not shrink the discs")
    return pos


def assert_drawn_clearance(pos, edges, node, what):
    """The clearance gates, re-run on the coordinates actually drawn.

    R3 B3-2: `growth_layout` enforced `gap >= node + 2` inside `GROWTH_BOX` and passed at
    46.0bp; `growth_pos` then mapped into a panel 40bp shorter, scale 0.8726, and the gap
    became 40.1bp against 40bp discs -- six discs fused on the render. The gate had run,
    correctly, on coordinates nothing was drawn at. Assert the property on the numbers the
    figure emits, not on the ones it solved.
    """
    bad = clearance_bad(list(edges), pos, r=node / 2 + 2)
    assert not bad, f"{what}: edge passes through a disc it does not end at -- {bad[:3]}"
    ns = sorted(pos)
    gap = min(math.dist(pos[i], pos[j]) for a, i in enumerate(ns) for j in ns[a + 1:])
    assert gap >= node + 2, (
        f"{what}: two discs are {gap:.1f}bp apart with {node}bp discs -- they will fuse "
        f"on the render. Solve the layout in the box it is drawn in.")
    return gap


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
    pos = {i: (ox + (x - gx0) / (gx1 - gx0) * w, oy + (y - gy0) / (gy1 - gy0) * h)
           for i, (x, y) in canon.items()}
    # The mapping can shrink the layout, and a gate that ran before it proves nothing.
    assert_drawn_clearance(pos, [tuple(e) for e in growth_edges(preferential)],
                           GROWTH_NODE, f"growth_pos into {box}")
    return pos


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

    ax = Axes(LIN_BOX, (0, 288), (0, 0.15), xticks=[0, 100, 200],
              yticks=[0, 0.05, 0.10, 0.15], yfmt=lambda v: f"{v:g}")
    body = ax.frame()
    body += axis_titles(ax, "number of coauthors $k$", "$p(k)$")
    body += scatter(ax, ks, pk, color=HUBS, d=13, expect=len(ks))
    body += text(ax.x1 - 8, 372,
                 f"one dot per distinct $k$: {len(ks)} of them", color="annot",
                 anchor="north east")
    body += text(ax.x1 - 8, ax.Y(0.130),
                 f"$\\mathrm{{Var}}(k)/\\langle k \\rangle = {s['gap']:.1f}$",
                 color="accenttwo", anchor="north east")
    emit("linear-axes", body, container="full", h=H)


def fig_fat_tail_reveal():
    """Slide 49: the same axes, with both ends of the distribution named."""
    ks, pk, N = condmat_pdf()
    d = np.array(condmat_degrees())
    small = float((d <= SMALL_K).mean())
    far = int((d > TAIL_K).sum())
    assert far == 28 and N == 23133, (far, N)

    ax = Axes(LIN_BOX, (0, 288), (0, 0.15), xticks=[0, 100, 200],
              yticks=[0, 0.05, 0.10, 0.15], yfmt=lambda v: f"{v:g}")
    body = ax.frame()
    body += axis_titles(ax, "number of coauthors $k$", "$p(k)$")
    # accent-3 carries area, never a stroke and never text: the tail band is a fill. Its
    # left edge is TAIL_K, the same constant the annotation prints -- R1 B-14: it was
    # hardcoded at 96 and landed 23px left of the "100" tick the annotation named.
    # R2 B2-13: the band's top edge used to stop at p = 0.018, which encodes nothing.
    # It marks a RANGE OF k, so it runs the full height of the frame.
    body += fill_poly([ax.P(TAIL_K, 0), ax.P(288, 0), ax.P(288, ax.ylim[1]),
                       ax.P(TAIL_K, ax.ylim[1])], color="accentthree", opacity=0.55)
    body += scatter(ax, ks, pk, color=HUBS, d=13, expect=len(ks))

    # R3 A3-7: the head annotation was drawn across the tail band, describing k <= 10
    # while sitting over k = 43...142. The band has to be full height -- clipped to the
    # data it is a 0.6bp sliver, since every point out there is one author -- so both
    # notes live above the frame instead, each over the range it names. Fills are in the
    # collision gate now, so neither can drift back in.
    boxes = []
    body += fixed_label([(ax.X(TAIL_K) - 20, 372)],
                        f"{pct(small)} sit at $k \\le {SMALL_K}$",
                        [], boxes, color="accenttwo", anchor="north east")
    body += fixed_label([(ax.x1 - 8, 372)], f"{far} run past $k = {TAIL_K}$",
                        [], boxes, color="accenttwo", anchor="north east")
    # R4 A4-8: the leader stopped 52px above the dots it points into, so the arrowhead
    # ended in blank gold. It reaches the tail now.
    body += seg(ax.P(190, 0.136), ax.P(190, 0.006), color="accenttwo", w=3.0,
                arrow="-{Latex[length=9bp]}")
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
# One window and one quantity for all four binning figures. R2 B2-2: `binned-once` plotted
# counts over k >= 1 and the three build panels plotted share-per-unit-k over k >= 10 --
# the ruler changed twice, unannounced, on the slides whose whole thesis is that an
# unannounced change of ruler misleads you. The tells were on the slides themselves: one
# said "122 bins hold all 23,133 authors", the next "113 bins", and the nine bins below
# k = 10 were never mentioned. Now every one of them is counts, over 1 <= k <= 300.
BIN_LO, BIN_HI = 1, 300
BIN_XLIM, BIN_YLIM = (0.8, 400), (0.02, 2e4)
BIN_XTICKS, BIN_YTICKS = [1, 10, 100], [0.1, 10, 1000]


@lru_cache(maxsize=None)
def binned(w):
    """(bin centres, authors per unit of k) of the cond-mat degrees in bins of width w.

    R3 B3-6: this returned raw counts, so widening the bin eightfold multiplied every
    height eightfold -- the leftmost point went from 2,373 to 16,588 on identical axes --
    under a slide saying "nothing was recomputed". Per unit k the three panels land on
    one scale and the change in SHAPE is the only visible difference, which is what the
    build is about.
    """
    d = np.array(condmat_degrees())
    e = np.arange(BIN_LO, BIN_HI + w, w)
    c, _ = np.histogram(d, bins=e)
    ctr = (e[:-1] + e[1:] - 1) / 2
    m = c > 0
    return tuple(ctr[m].tolist()), tuple((c[m] / w).tolist())


def _bin_axes():
    # The same box as every CCDF in the module, so the four binning slides and the four
    # CCDF slides are read on one ruler (B3-3).
    return Axes(CCDF_BOX, BIN_XLIM, BIN_YLIM, xlog=True, ylog=True,
                xticks=BIN_XTICKS, yticks=BIN_YTICKS, xfmt=dec, yfmt=dec)


def _bin_caliper(ax, w, ycal=40.0):
    """One bin, drawn at the left where a unit of k is a whole decade wide on the axis.

    Out at k = 30 the same caliper is 5bp long, which is the reason binning is a choice
    at all and is what the build goes on to.
    """
    return (seg(ax.P(1, ycal), ax.P(1 + w, ycal), color="annot", w=3.0,
                arrow="{Latex[length=8bp]}-{Latex[length=8bp]}")
            + text((ax.X(1) + ax.X(1 + w)) / 2, ax.Y(ycal) - 14,
                   f"one bin\\\\width {w}", color="annot", anchor="north"))


def fig_binned_once():
    """The slide before the binning question: the same tail, counted once, at width 1.

    R1 B-4: the two slides before it plot one point per observed degree and are not
    binned, yet the next slide asks "that plot had bins -- what if I choose different
    ones?".  The question had no referent.  This is the referent, and it is drawn on
    exactly the axes and window the three-panel build then uses.
    """
    d = np.array(condmat_degrees())
    ctr, cnt = binned(1)
    assert len(ctr) == 122 and abs(sum(cnt) - len(d)) < 1e-6 and len(d) == 23133

    ax = _bin_axes()
    body = ax.frame()
    body += axis_titles(ax, "number of coauthors $k$", "authors per unit of $k$")
    body += scatter(ax, ctr, cnt, color=HUBS, d=13, expect=len(ctr))

    body += _bin_caliper(ax, 1)
    # The note lives ABOVE the frame, on one line: inside it there is no corner that is
    # empty at every bin width, and the note is the same object on all four figures.
    body += text(ax.x1 - 8, 372,
                 f"{len(ctr)} bins hold all {num(len(d))} authors",
                 color="accenttwo", anchor="north east")
    emit("binned-once", body, container="full", h=H)


def _fig_binning_panel(i):
    """One state of the three-slide build: the same tail, counted at one bin width.

    R1 B-4: this was one figure with three panels side by side and no y tick labels on
    two of them, so the shared vertical scale the comparison rests on could not be read
    off the slide.  R2 B2-3: the two annotations then overlapped on all three panels.
    Three files, three slides, every panel with its ticks, and the two notes stacked as
    one block that the collision gate checks.
    """
    w = BIN_WIDTHS[i]
    ctr, cnt = binned(w)
    counts = [len(binned(ww)[0]) for ww in BIN_WIDTHS]
    assert len(set(counts)) == 3, counts
    for ww in BIN_WIDTHS:
        assert abs(sum(binned(ww)[1]) * ww - 23133) < 1e-6, "a bin lost an author"
    # The three tails must genuinely differ, or the build has nothing to show.
    # R4 B4-4: every bin was fitted, including k = 1 and 2 where the distribution turns
    # over, so panel one printed -2.25 for the same 122 points `pdf_fit` fits at -2.44 --
    # and part of the -2.25 -> -3.80 movement was the fitted range moving with the bin
    # centres, not the bin width. One window for all three, the same one `pdf_fit` uses.
    def _fit(ww):
        c, v = binned(ww)
        c, v = np.array(c), np.array(v)
        m = (c >= PDF_KMIN) & (c <= PDF_KMAX)
        assert m.sum() >= 4, (ww, int(m.sum()))
        return float(np.polyfit(np.log10(c[m]), np.log10(v[m]), 1)[0])

    fits = [_fit(ww) for ww in BIN_WIDTHS]
    assert abs(fits[0] - pdf_fit()[0]) < 0.02, (fits[0], pdf_fit()[0])
    assert max(fits) - min(fits) > 0.3, fits

    ax = _bin_axes()
    body = ax.frame()
    body += axis_titles(ax, "number of coauthors $k$", "authors per unit of $k$")
    body += scatter(ax, ctr, cnt, color=HUBS, d=13, expect=len(ctr))
    # R4 A4-7: the caliper that slide 56 introduces has to survive into the build's first
    # panel -- it is the object the whole build is about. Same class as the arrow that
    # vanished from `acquaintance-3`.
    body += _bin_caliper(ax, w)
    # R3 B3-7: the fitted slope was computed, asserted to differ, and thrown away, so the
    # only visible change across the build was that the scatter thinned -- which reads as
    # "wider bins are cleaner", the opposite of the point. Bin width alone moves this
    # network across the gamma = 3 boundary, and now the panel says so.
    body += text(ax.x1 - 8, 372,
                 f"bin width {w}  ·  fitted slope ${fits[i]:.2f}$\\\\"
                 f"heights are counts divided by the width",
                 color="accenttwo", anchor="north east")
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

    # R2 B2-4: at 537bp every disc measured 12px, against the 26-40px floor that
    # adjudication 1 set for objects the room is asked to COUNT -- and this figure's
    # whole job is that one dot is one edge and one column is one node. Full width (the
    # deck lays the slide out to match, D2-4) puts them at 28px.
    x0, y0 = 300, 110
    pitch, unit, dd = 34.0, 34.0, 28
    kmax = max(ks)

    def Y(v):
        return y0 + v * unit

    body = ""
    # R2 B2-14: the ticks used to sit on the CELL BOUNDARIES, half a step above the dots
    # they count, so a column of four dots visually reached k = 3.5. They sit on the dot
    # rows now; the cut still sits on the boundary, which is what "k > 3" means.
    for v in (1, 4, 7):
        body += seg((x0 - 52, Y(v - 0.5)), (x0 - 42, Y(v - 0.5)), color="black", w=2.2)
        body += text(x0 - 62, Y(v - 0.5), f"{v}", anchor="east")
    body += seg((x0 - 52, Y(0)), (x0 - 52, Y(kmax) - 8), color="black", w=2.2)
    body += text(96, Y(kmax / 2), "degree $k$", rot=90)

    for i, k in enumerate(ks):
        for j in range(1, k + 1):
            body += dot(x0 + i * pitch, Y(j - 0.5),
                        color="accenttwo" if k > cut else "annot", d=dd)
    right = x0 + (len(ks) - 1) * pitch

    body += seg((x0 - 52, Y(cut)), (right + 24, Y(cut)), color="accenttwo", w=3.4,
                dash=DASH)
    body += text(right, Y(cut) + 14, f"$k = {cut}$", color="accenttwo",
                 anchor="south east")

    # What one column is, and what one dot is -- both drawn against the objects they
    # measure, not stated in words alone.
    bx = x0 - pitch / 2
    body += polyline([(bx, Y(0) - 10), (bx, Y(0) - 22), (bx + pitch, Y(0) - 22),
                      (bx + pitch, Y(0) - 10)], color="annot", w=3.4)
    body += text(x0 + pitch, Y(0) - 30, "one node", color="annot", anchor="north west")
    cal = x0 + 17
    body += seg((cal, Y(5.5)), (cal, Y(6.5)), color="annot", w=3.4,
                arrow="{Latex[length=9bp]}-{Latex[length=9bp]}")
    body += seg((x0 + 14, Y(5.5)), (cal, Y(5.5)), color="annot", w=2.0)
    body += seg((x0 + 14, Y(6.5)), (cal, Y(6.5)), color="annot", w=2.0)
    body += text(cal + 35, Y(6), "one end", color="annot", anchor="west")

    body += text(1060, 372,
                 f"{len(above)} of {len(ks)} nodes above $k = {cut}$\\\\"
                 f"$\\mathrm{{CCDF}}({cut}) = {share:.2f}$",
                 color="accenttwo", anchor="north east")
    body += text((x0 + right) / 2, Y(0) - 74, f"{len(ks)} nodes, sorted by degree",
                 anchor="north")
    emit("ccdf-def", body, container="full", h=H)


def fig_ccdf_condmat():
    """Slide 56: the same authors as a CCDF -- one point per distinct degree."""
    ks, su = condmat_ccdf()
    # The survival at the largest degree is exactly zero and a log axis has no room for
    # it, so 121 of the 122 distinct degrees are drawn.
    plot = [(k, s) for k, s in zip(ks, su) if s > 0]
    assert len(ks) == 122 and len(plot) == 121, (len(ks), len(plot))

    # R4 B4-2: this slide's point is that a CCDF has no bin width to choose. The exponent
    # reconciliation that lived here in round 3 was a second and harder claim, and it
    # arrived two slides before the poll asking whether the CCDF slope IS gamma -- it
    # answered the poll and showed the room the +1 rule that the next slide exists to
    # derive. It belongs after both, and it is not this figure's.
    ax = ccdf_axes((1, 300), [1, 10, 100])
    body = ax.frame()
    body += axis_titles(ax, "number of coauthors $k$", "$P(k' > k)$")
    body += scatter(ax, [p[0] for p in plot], [p[1] for p in plot], color=HUBS, d=13,
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

    # R3 B3-8: the CDF used to be drawn on a linear y against the CCDF's log y, and the
    # panel titles announced it -- so a student could correctly answer "the left one is
    # bad because you used the wrong axis" and the slide had no reply. Same ruler now.
    # The CDF still flattens against 1 from k = 30 and still shows nothing of the tail,
    # so the point lands harder and the only difference left is the quantity.
    left = Axes((174, 140, 520, 262), (1, 300), CCDF_YLIM, xlog=True, ylog=True,
                xticks=[1, 10, 100], yticks=CCDF_YTICKS, xfmt=dec)
    right = Axes((694, 140, 1040, 262), (1, 300), CCDF_YLIM, xlog=True, ylog=True,
                 xticks=[1, 10, 100], yticks=CCDF_YTICKS, xfmt=dec)
    body = left.frame() + right.frame()
    body += curve(left, ks, cdf, color=HUBS, w=4.6)
    body += curve(right, ks, su, color=HUBS, w=4.6)

    # R4 B4-9: the two panels had different x rulers (139.7 against 121.1 px per decade
    # over the same k), so the quantity was not the only thing that changed. Same box.
    assert (left.x1 - left.x0) == (right.x1 - right.x0)
    assert left.xlim == right.xlim and left.ylim == right.ylim
    for ax, ytitle, ytx in ((left, "$P(k' \\le k)$", 34), (right, "$P(k' > k)$", 560)):
        body += text(ytx, (ax.y0 + ax.y1) / 2, ytitle, rot=90)
        body += text((ax.x0 + ax.x1) / 2, 76, "number of coauthors $k$", anchor="north")

    # Each panel says which ruler it is drawn on, and why that ruler was chosen. Two
    # lines above each frame: the panels are 134bp tall so there is no room inside them
    # for three lines of prose, and prose over a curve is what put "physicists" on the
    # yeast tail in round 1.
    boxes = []
    # R2 B2-15: the CDF was drawn in annotation gray -- a colour this deck reserves for
    # annotation -- against an accent CCDF, and "reaches down to 0" sat over a log axis,
    # which cannot show zero. Same data, same colour; the titles carry the difference.
    body += label_at(left.x0, 372, "CDF\\\\flat from $k = 30$",
                     color="black", anchor="north west", boxes=boxes)
    body += label_at(right.x1, 372, "CCDF\\\\still falling",
                     color="black", anchor="north east", boxes=boxes)
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
    # The CCDF exponent is one smaller: that is the whole content of the figure, so it is
    # measured off the two drawn curves rather than asserted against itself (R3 B3-14).
    fit_pdf = np.polyfit(np.log10(xs), np.log10(pdf), 1)[0]
    fit_ccdf = np.polyfit(np.log10(xs), np.log10(cc), 1)[0]
    assert abs(fit_pdf + g) < 1e-9 and abs(fit_ccdf + (g - 1)) < 1e-9
    assert abs((fit_ccdf - fit_pdf) - 1.0) < 1e-9, (fit_pdf, fit_ccdf)

    # R2 B2-1 had five overlaps, three of them caused by putting a y title in the
    # inter-panel gutter and then running an arrow and its label through the same strip.
    # The gutter now holds one unlabelled arrow; both y titles sit in their own panel's
    # column; and the two sentences that were in-panel notes are the figure's two lines
    # at the top, where nothing else is.
    # R4 B4-1 was a Blocker, and the sharpest version of this deck's recurring lesson.
    # The two panels were sized so each line ended one decade above its own floor: six
    # decades on the left, four on the right, in boxes of identical height. The ruler
    # change cancelled the slope change and both slopes DREW at 0.41 and 0.39 -- 4.5%
    # apart, where the claim is 2.5 against 1.5 -- on the answer slide to a poll whose own
    # note calls this the single most common error in the material. The picture showed the
    # error. Identical boxes, identical limits, and then the assertion below measures the
    # angles ON THE CANVAS rather than refitting the arrays that produced them.
    box_h, box_w = 118, 230
    left = Axes((230, 140, 230 + box_w, 140 + box_h), (1, 100), (1e-6, 1),
                xlog=True, ylog=True, xticks=[1, 100], yticks=[1e-4, 1], xfmt=dec)
    right = Axes((800, 140, 800 + box_w, 140 + box_h), (1, 100), (1e-6, 1),
                 xlog=True, ylog=True, xticks=[1, 100], yticks=[1e-4, 1], xfmt=dec)

    # The drawn slope of a log-log line is (decades of rise x bp per y-decade) divided by
    # (decades of run x bp per x-decade). Computed from each panel's own box, so a change
    # to either box shows up here and not on the slide.
    def drawn_slope(ax, exponent):
        bp_x = (ax.x1 - ax.x0) / math.log10(ax.xlim[1] / ax.xlim[0])
        bp_y = (ax.y1 - ax.y0) / math.log10(ax.ylim[1] / ax.ylim[0])
        return exponent * bp_y / bp_x

    s_pdf, s_ccdf = drawn_slope(left, g), drawn_slope(right, g - 1)
    assert abs(s_pdf / s_ccdf - g / (g - 1)) < 1e-9, (s_pdf, s_ccdf)
    assert s_pdf > 1.5 * s_ccdf, (
        f"the two panels draw the exponents at {s_pdf:.3f} and {s_ccdf:.3f} -- the ruler "
        f"change is cancelling the slope change. Same box, same limits, both panels.")
    body = left.frame() + right.frame()

    # Everything above k, as area. accent-3 is a fill here, which is what it is for.
    tail = xs >= k0
    poly = ([left.P(k0, left.ylim[0])]
            + [left.P(x, y) for x, y in zip(xs[tail], pdf[tail])]
            + [left.P(xs[tail][-1], left.ylim[0])])
    body += fill_poly(poly, color="accentthree", opacity=0.8)
    body += left.line(xs, pdf, color=HUBS, w=4.6)
    body += seg(left.P(k0, left.ylim[0]), left.P(k0, k0 ** -g), color="annot", w=2.6,
                dash=DASH)
    body += text(left.X(k0), left.y0 - 17, "$k$", color="accenttwo", anchor="north")

    # The same mass, as one point on the CCDF.
    body += right.line(xs, cc, color=HUBS, w=4.6)
    body += dot(*right.P(k0, k0 ** -(g - 1)), color="accenttwo", d=20)
    body += seg((500, 200), (630, 200), color="annot", w=3.4,
                arrow="-{Latex[length=11bp]}")

    # Short y titles on purpose: a rotated label is as TALL as it is long, and
    # "$P(k' > k)$" spans 216bp of a 380bp canvas, which is what the conclusion line
    # below was colliding with.
    body += text(96, (left.y0 + left.y1) / 2, "$p(k)$", rot=90)
    body += text(666, (right.y0 + right.y1) / 2, "CCDF", rot=90)
    body += text((left.x0 + left.x1) / 2, 76, "$k$", anchor="north")
    body += text((right.x0 + right.x1) / 2, 76, "$k$", anchor="north")
    body += text(540, 372,
                 "the shaded tail  $\\rightarrow$  one point on the CCDF",
                 color="annot", anchor="north")
    body += text(540, 324,
                 "so the log-log slope goes from $-\\gamma$ to $1-\\gamma$",
                 color="accenttwo", anchor="north")
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
    # R1 B-6 / R2 B2-5: it arrives after fifteen slides of cond-mat and the only tell was
    # that x reaches 1000 where cond-mat stopped at 279 -- so a student reading it as the
    # same network gets gamma = 2.3 here against the 2.44 printed earlier, on the pair of
    # slides teaching that the two routes agree.
    body += text(1050, 372, "a different network", color="annot",
                 anchor="north east")
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
    # R2 B2-6: the text went gray in round 1 and the rule stayed accent-2, so red still
    # set the right answer and cancelled the wrong one 90bp apart. The whole cancellation
    # is annotation now. `record=False`: a strike-through is the one rule whose job is to
    # cross a word, and the collision gate has to be told which one that is.
    body += seg((806, 128), (954, 128), color="annot", w=3.4, record=False)
    emit("slope-answer", body, container="full", h=H)


def fig_exercise_card():
    """The handout, as the four pictures it asks the room to compare.

    R1 B-7 and R2 B2-7: this was a rounded rectangle containing the words the left column
    already says -- a text column beside a picture of a text column.  The handout's job is
    "the same distribution, drawn four ways, and one of them is lying", so the figure is
    those four ways, drawn from the same 23,133 authors.  Thumbnails carry no ticks on
    purpose: the point is the four SHAPES, and a tick label at the 36pt floor would be
    wider than the panel it sits in.
    """
    ks, pk, N = condmat_pdf()
    kc, su = condmat_ccdf()
    wide_c, wide_n = binned(8)
    wide_d = np.array(wide_n) / (N * 8)
    panels = [
        ("linear", (0, 288), (0, 0.15), False, False, ks, pk),
        ("log-log", (1, 300), (1e-5, 1), True, True, ks, pk),
        ("wide bins", (1, 300), (1e-6, 1), True, True, np.array(wide_c), wide_d),
        ("CCDF", (1, 300), (1e-5, 1), True, True,
         kc[su > 0], su[su > 0]),
    ]
    body = ""
    for i, (name, xl, yl, xlog, ylog, xs, ys) in enumerate(panels):
        cx = 24 + (i % 2) * 267
        cy = 262 if i < 2 else 116
        ax = Axes((cx, cy, cx + 222, cy + 92), xl, yl, xlog=xlog, ylog=ylog,
                  xticks=[], yticks=[])
        body += ax.frame()
        inside = [(x, y) for x, y in zip(xs, ys) if ax.inside(x, y)]
        assert len(inside) > 8, (name, len(inside))
        body += ax.points([q[0] for q in inside], [q[1] for q in inside],
                          color=HUBS, d=5)
        body += text(cx + 111, cy - 6, name, anchor="north")
    emit("exercise-card", body, container="col", h=H)


# --------------------------------------------------------------------------- Part 6
def fig_hubs_share():
    """The top 1% of the Internet, marked on the CCDF the room has been reading.

    R1 B-8 and R2 B2-8: this was a rank-degree plot, and `grep -c rank` on the deck
    returns 0 -- no slide introduces a rank axis, and every plot in the preceding twenty
    slides is p(k) or P(k'>k) against k.  On a CCDF the top 1% is not a construction at
    all: it is the band below P = 0.01, by definition.  The network names itself too --
    6,474 nodes arriving after twenty slides of a 23,133-node one.
    """
    g = internet_as()
    d = np.array(degrees_of("internet"))
    n_top, share = top_share(g, 0.01)
    assert n_top == 65 and abs(share - 0.3385) < 1e-3, (n_top, share)
    ks, su = ccdf(d)
    top_frac = n_top / len(d)
    kstar = int(min(k for k, s in zip(ks, su) if s <= top_frac))

    # The frame stops at y = 278 so the two numbers have a band of their own above it.
    # A CCDF is a diagonal across its whole panel: there is no corner inside it that is
    # empty at both ends, which is what the collision gate kept saying.
    ax = ccdf_axes((1, 2000), [1, 10, 100, 1000])
    body = ax.frame()
    body += axis_titles(ax, "degree $k$", "$P(k' > k)$")
    # R3 B3-10: the band used to span the full width while its label said k >= 36, so
    # everything left of the dashed line was shaded and was not k >= 36. It is the
    # rectangle those 65 routers actually occupy: k >= kstar AND P <= 1%.
    body += fill_poly([ax.P(kstar, ax.ylim[0]), ax.P(ax.xlim[1], ax.ylim[0]),
                       ax.P(ax.xlim[1], top_frac), ax.P(kstar, top_frac)],
                      color="accentthree", opacity=0.55)
    body += curve(ax, ks, su, color=HUBS, w=4.6)
    body += seg(ax.P(kstar, ax.ylim[0]), ax.P(kstar, top_frac), color="annot", w=2.6,
                dash=DASH)
    drawn = curve_pts(ax, ks, su)

    # R4 B4-7: the headline number had neither a picture nor a sentence -- I chose the
    # "deck body carries it" exit in round 3 and the body never received it. The shaded
    # band is empty below the curve, so the share goes there as a length: one rule the
    # full width of the frame, standing for all 25,144 edge ends, with the hubs' share of
    # it in accent-2.
    bar_y = ax.Y(1.35e-4)
    body += seg((ax.x0, bar_y), (ax.x1, bar_y), color="annot", w=13)
    body += seg((ax.x0, bar_y), (ax.x0 + share * (ax.x1 - ax.x0), bar_y),
                color="accenttwo", w=13)
    boxes = []
    body += fixed_label([(ax.x1 - 8, CCDF_NOTE_Y)],
                        f"{n_top} routers hold {pct(share, 1)} of all "
                        f"{num(d.sum())} edge ends",
                        drawn, boxes, color="accenttwo", anchor="north east")
    body += fixed_label([(ax.x1 - 8, 290), (ax.x1 - 8, 274)],
                        f"shaded: top {pct(0.01)}, $k \\ge {kstar}$",
                        drawn, boxes, color="annot", anchor="east")
    # The number is on the top line; down here the bar IS the number, and the label only
    # has to say whose share it is. Anything longer runs into the shaded band.
    body += fixed_label([(ax.x0 + 6, 208), (ax.x0 + 6, 232)], "their share",
                        drawn, boxes, color="accenttwo", anchor="north west")
    emit("hubs-share", body, container="full", h=H)


def fig_universality():
    """Three unrelated systems, one shape.  Labelled in place, no legend.

    R2 B2-10: red meant "the Internet" here and "the random graph with no hubs" two
    slides later.  All three of these are hub-rich, so all three are accent -- the role
    is the module's, not the figure's -- and they are told apart by their dash pattern
    and by a label the solver has to put nearer its own curve than any other.

    R1 B-9 and R2 B2-9: that label was 23px from the yeast curve and 50px from its own,
    twice, because the first solver only avoided ink.  `curve_label` now takes the other
    curves as blockers and asserts the nearest-curve property the reviewer measured.
    """
    ax = ccdf_axes((1, 2000), [1, 10, 100, 1000])
    body = ax.frame()
    body += axis_titles(ax, "degree $k$", "$P(k' > k)$")

    # A dense sweep of anchors, not a handful: which stretch of a curve is isolated is
    # not something to guess at, and the physicists' curve has exactly one.
    sweep = tuple(x / 24 for x in range(2, 25))
    sets = [("physicists", np.array(condmat_degrees()), "", sweep),
            ("Internet", np.array(degrees_of("internet")), DASH_LONG, sweep),
            ("yeast", np.array(degrees_of("yeast")), DASH, sweep)]
    # Solved in order of how boxed-in each curve is: the physicists' curve is bracketed
    # by the other two for its whole length, so it claims its spot before they take the
    # room it needs.
    kmax, paths = {}, []
    for name, d, dash, fracs in sets:
        ks, su = ccdf_dense(d)
        kmax[name] = int(d.max())
        body += curve(ax, ks, su, color=HUBS, w=4.2, dash=dash)
        paths.append((name, curve_pts(ax, ks, su), fracs))
    assert kmax == {"physicists": 279, "Internet": 1458, "yeast": 56}, kmax

    boxes = []
    for i, (name, pts, fracs) in enumerate(paths):
        others = [q for j, (_, pp, _) in enumerate(paths) if j != i for q in pp]
        anchors = [pts[min(int(len(pts) * f), len(pts) - 1)] for f in fracs]
        # R4 B4-10: three curves in one colour, told apart by dash pattern, with the
        # label 43bp from a crossing and the next curve 54bp away -- the solver's own
        # margin passed and a reader still cannot tell. Every label gets a leader here,
        # so proximity stops being the cue at all.
        body += curve_label(ax, name, anchors, pts, boxes, others=others, color=HUBS,
                            floor=16, margin=1.6, force_leader=True)
    emit("universality", body, container="full", h=H)


def fig_poisson_ccdf():
    """Slide 67: wire it at random and the tail is not smaller, it is absent."""
    d = np.array(degrees_of("er"))
    cm = np.array(condmat_degrees())
    k1, var = float(d.mean()), float(d.var())
    # Matched to cond-mat by construction (B-11), so the two figures differ in SHAPE
    # only: assert the match rather than a hardcoded maximum, which is what broke when
    # the random graph stopped being an arbitrary <k> = 4.
    assert abs(k1 - cm.mean()) < 0.05, (k1, cm.mean())
    assert len(d) == len(cm), (len(d), len(cm))
    assert abs(var / k1 - 1) < 0.05, var / k1
    assert int(d.max()) < int(cm.max()) / 8, (d.max(), cm.max())
    ks, su = ccdf_dense(d)

    ax = ccdf_axes((1, 40), [1, 10])
    body = ax.frame()
    body += axis_titles(ax, "degree $k$", "$P(k' > k)$")
    body += curve(ax, ks, su, color=NO_HUBS, w=4.6)
    plot = [(k, s) for k, s in zip(ks, su) if s > 0 and ax.inside(k, s)]
    body += scatter(ax, [p[0] for p in plot], [p[1] for p in plot], color=NO_HUBS,
                    d=13, expect=len(plot))
    drawn = curve_pts(ax, ks, su)
    boxes = []
    body += fixed_label([(1050, CCDF_NOTE_Y)],
                        "same $N$ and $\\langle k \\rangle$ as the physicists",
                        drawn, boxes, color="annot", anchor="north east")
    body += fixed_label([(1050, 300), (1050, 288), (1050, 312)],
                        f"$\\langle k \\rangle = {k1:.1f}$, {num(len(d))} nodes\\\\"
                        f"$\\mathrm{{Var}}/\\langle k \\rangle = {var / k1:.2f}$\\\\"
                        f"largest degree {int(d.max())}",
                        drawn, boxes, color=NO_HUBS, anchor="north east")
    emit("poisson-ccdf", body, container="full", h=H)


def fig_three_ccdfs():
    """Slide 68: same average degree, three shapes."""
    # R1 B-10: accent named "power law" here while being drawn from a BA model, three
    # slides after accent was the physicists on `universality`. Reviewer C's own fix was
    # to use the cond-mat CCDF, which is already computed -- so accent is one network
    # across Part Six, the deck's own, and the slide compares a real heavy tail against
    # two idealisations at its own mean instead of an arbitrary <k> = 4.
    cm = np.array(condmat_degrees())
    er = np.array(degrees_of("er"))
    lat = np.array(lattice_degrees())
    means = {"physicists": cm.mean(), "random": er.mean(), "lattice": lat.mean()}
    assert max(means.values()) / min(means.values()) < 1.015, means
    assert set(lat.tolist()) == {8} and lat.var() == 0
    assert int(cm.max()) == 279, cm.max()
    assert int(er.max()) < 40, er.max()
    LAT_K = 8

    # The frame stops at 330 so the shared-mean note has a band above it: centred over
    # the panel it was crossed by the power-law curve, which is where a note goes when a
    # corner is chosen by hand instead of checked.
    ax = ccdf_axes((1, 500), [1, 10, 100])
    body = ax.frame()
    body += axis_titles(ax, "degree $k$", "$P(k' > k)$")
    drawn, anchors = [], []
    paths = []
    for d, col, name, fracs in ((cm, HUBS, "physicists", (0.72, 0.85, 0.6, 0.45)),
                                (er, NO_HUBS, "random",
                                 (0.99, 0.95, 0.9, 0.85, 0.8, 0.7, 0.6, 0.5, 0.4))):
        ks, su = ccdf(d)
        body += curve(ax, ks, su, color=col, w=4.6)
        pts = curve_pts(ax, ks, su)
        drawn += pts
        paths.append((name, col, pts, fracs))
    # Every node has exactly LAT_K, so the survival is 1 up to LAT_K-1 and 0 after: a
    # wall.  R2 B2-12: it used to run into the x axis, which on a log floor of 1e-5 reads
    # as "the distribution ends here".  It stops a fifth of a decade above it.
    floor = ax.ylim[0] * 10 ** FLOOR_LIFT
    # R3 B3-4 / R4 B4-6: drawn black at 4bp against 2bp axes it closed a rectangle with
    # them and read as an inset panel with a title inside it. Annotation gray at the other
    # curves' weight, ending open, and the label goes to the right of the step.
    wall = [ax.P(1, 1), ax.P(LAT_K, 1), ax.P(LAT_K, floor)]
    body += polyline(wall, color="annot", w=4.6)
    lat_pts = (curve_pts(ax, [1, LAT_K], [1, 1])
               + [(ax.X(LAT_K), y) for y in np.arange(ax.Y(floor), ax.Y(1), 7)])
    drawn += lat_pts
    paths.append(("lattice", "annot", lat_pts, (0.5, 0.3, 0.7, 0.9)))

    boxes = [label_box((ax.x0 + ax.x1) / 2, 372,
                       visible("all three networks: $\\langle k \\rangle \\approx 8$"),
                       "north")]
    body += text((ax.x0 + ax.x1) / 2, 372,
                 "all three networks: $\\langle k \\rangle \\approx 8$", color="annot",
                 anchor="north")
    for i, (name, col, pts, fracs) in enumerate(paths):
        others = [q for j, (_, _, pp, _) in enumerate(paths) if j != i for q in pp]
        anchors = [pts[min(int(len(pts) * f), len(pts) - 1)] for f in fracs]
        # A cliff and a straight line share a panel here, so the clearances are tighter
        # than on `universality`; the property asserted is the same one -- the nearest
        # curve to a name is the curve it names.
        body += curve_label(ax, name, anchors, pts, boxes, others=others, color=col,
                            floor=18, margin=1.02)
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
QUIZ_A = (8, 66, 320, 340)          # uniform growth
QUIZ_B = (330, 66, 642, 340)        # preferential attachment
QUIZ_FRAME = (818, 145, 1058, 356)


def _quiz_body(labels, fills, dashes):
    """Both sketches and both tails.

    R3 B3-1 was a Blocker of round 2's own making. C2-7 made the colour role consistent --
    accent has hubs, accent-2 does not -- and three slides then spend that key in words
    ("hubs effectively impossible", "randomness cuts it short"). So on the QUESTION slide
    a student could read the answer off the palette and vote without looking at a tail,
    which the speaker note explicitly forbids. The ruling stands everywhere else; this one
    figure is exempt, deliberately, and `fig_quiz` passes one neutral fill for both
    sketches and tells the two tails apart by dash pattern instead. `fig_quiz_answer`
    passes the roles, where "no preference"/"preference" arrive and they become legible.
    """
    ba = np.array(degrees_of("ba"))
    ua = np.array(degrees_of("uniform"))
    assert abs(ba.mean() - 4) < 0.01 and abs(ua.mean() - 4) < 0.01
    assert int(ba.max()) == 315 and int(ua.max()) == 29
    assert len(ba) == len(ua) == 20000

    ea, eb = growth_edges(False), growth_edges(True)
    assert len(ea) == len(eb), (len(ea), len(eb))       # same n, same edge count
    assert len({v for e in ea for v in e}) == GROWTH_N

    body = ""
    for box, pref, col, lab in ((QUIZ_A, False, fills[0], labels[0]),
                                (QUIZ_B, True, fills[1], labels[1])):
        # R3 B3-2: solved in the panel box it is drawn in, not in a canonical box and
        # then scaled into this one.
        pos = growth_layout(pref, box=box)
        edges = [tuple(e) for e in growth_edges(pref)]
        assert_drawn_clearance(pos, edges, GROWTH_NODE, f"quiz panel {lab}")
        frame = {"nodes": list(range(GROWTH_N)), "edges": edges,
                 "new_node": None, "new_edges": []}
        body += draw_growth(frame, pos, fill=col, size=GROWTH_NODE)
        body += text((box[0] + box[2]) / 2, 372, lab, color=col, anchor="north")

    ax = Axes(QUIZ_FRAME, (1, 400), (1e-5, 1), xlog=True, ylog=True,
              xticks=[1, 10, 100], yticks=CCDF_YTICKS, xfmt=dec)
    body += ax.frame()
    body += text((ax.x0 + ax.x1) / 2, 79, "degree $k$", anchor="north")
    body += text(676, (ax.y0 + ax.y1) / 2, "$P(k' > k)$", rot=90)
    drawn, anchors = [], []
    for d, col, dash, fracs in ((ua, fills[0], dashes[0], (0.85, 0.7, 0.95, 0.55)),
                                (ba, fills[1], dashes[1], (0.75, 0.6, 0.9, 0.45))):
        ks, su = ccdf_dense(d)
        body += curve(ax, ks, su, color=col, w=4.2, dash=dash)
        pts = curve_pts(ax, ks, su)
        drawn += pts
        anchors.append((col, [pts[min(int(len(pts) * f), len(pts) - 1)] for f in fracs]))
    # R1 B-13 / C2-5: the switch belongs in the DRAWING. The sketches are 14-node runs of
    # the two rules; the tails are the 20,000-node ones.
    switch = f"sketches: {GROWTH_N} nodes  ·  tails: {num(len(ba))} nodes"
    body += text((QUIZ_A[0] + QUIZ_B[2]) / 2, 8, switch, color="annot", anchor="south")
    said = list(labels) + [switch, "degree $k$", "$P(k' > k)$", "1", "10", "100",
                           "$10^{-4}$", "$10^{-2}$"]
    return body, ax, ba, ua, said, drawn, anchors


def _quiz_curve_labels(ax, drawn, anchors, texts):
    """Name each tail beside its own curve, inside the CCDF frame.

    The tick labels go in as blockers: with the bounds opened up to the whole right-hand
    third, "max 29" was written straight across the 10 and 100 on the axis.
    """
    body = ""
    boxes = [label_box(ax.X(v), ax.y0 - 17, dec(v), "north") for v in (1, 10, 100)]
    for (col, ats), s in zip(anchors, texts):
        body += curve_label(ax, s, ats, drawn, boxes, color=col, floor=20, margin=1.0)
    return body


def fig_quiz():
    """Slide 72: two networks and two tails, and nothing that says which rule made them."""
    # One neutral fill, two dash patterns: see `_quiz_body`. The palette must not
    # answer the question the slide is asking.
    # R4 C4-1: the neutral fill was ink, and the edges are ink, so a disc and its edge
    # were one shape -- each panel rendered as a single connected black mass of ~38,000px
    # on the slide that asks the room to compare two structures. Annotation gray is still
    # one neutral fill, still carries no hub/no-hub key, and the disc-edge boundary comes
    # back. It also puts the discs back under `check_render`'s node-size gate once
    # `NODE_FILLS` gains the gray.
    body, ax, ba, ua, said, drawn, anchors = _quiz_body(
        ("A", "B"), ("annot", "annot"), ("", DASH_LONG))
    said += ["A", "B"]
    body += _quiz_curve_labels(ax, drawn, anchors, ("A", "B"))
    # Checked against the strings drawn, not the TikZ body -- coordinates are full of
    # digits and "315" turns up in several of them.
    for s in said:
        for banned in ("prefer", "uniform", "random", "grew",
                       str(int(ba.max())), f" {int(ua.max())}"):
            assert banned not in s, \
                f"quiz.png leaks {banned!r} in {s!r} -- slide 72 is the question"
    emit("quiz", body, container="full", h=H)


def fig_quiz_answer():
    """Slide 73: the same two, named, with the tails' largest degrees."""
    body, ax, ba, ua, _, drawn, anchors = _quiz_body(
        ("no preference", "preference"), (NO_HUBS, HUBS), ("", ""))
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

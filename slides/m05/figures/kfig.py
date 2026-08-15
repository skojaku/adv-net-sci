#!/usr/bin/env python3
"""Drawing helpers shared by the Module 05 figure modules.

`figlib.py` owns the pipeline and the gates; this file owns the things that are specific
to *this* deck: the club drawn from its one cached layout, the small planar graphs the
mechanism slides use, and the matrix/strip primitives the SBM and evaluation parts need.

Two rules are enforced here rather than left to the author:

  * **The club is recoloured, never relaid.** `karate()` reads the cached layout and
    takes only colours, rings and dimming. There is no position argument, so no figure
    can quietly move a disc between two consecutive slides.
  * **A mechanism graph must be planar on the page.** `small()` runs
    `assert_planar_drawing` unconditionally. The club is allowed its 81 crossings
    because it has no crossing-free drawing; a nine-node example has no such excuse.
"""

import math

import numpy as np

import layout
from figlib import (
    ACCENT, ACCENT2, ACCENT3, FONT, GRAY, NODE, Axes, boxes_overlap, clearance_bad,
    crossings, disc, dot, draw_labels, label_box, place_labels, polyline, ring, seg,
    text,
)

FULL_W, COL_W = 1080, 537

# The club's discs are 34bp, not figlib's 40: 34 of them have to sit at least 46bp apart
# inside a 1044 x 336 box, and the band check_render.py enforces is 26-52px.  Everything
# else in the deck keeps 40.
KNODE = layout.NODE
KOFF_X = (FULL_W - layout.W) / 2.0
KOFF_Y = 26.0
KCANVAS_H = 380

# One colour, one meaning, deck-wide (FIGURE_SPEC's colour contract):
HI, OFFICER = ACCENT, ACCENT2          # Mr. Hi's club / the officers' club
CHI, COFF = "accent", "accenttwo"
CDIM = "annot"


# --------------------------------------------------------------------------- the club
def club():
    """(positions in canvas bp, edge list) for the karate club, from the cache."""
    pos, edges = layout.load()
    return ({n: (x + KOFF_X, y + KOFF_Y) for n, (x, y) in pos.items()}, edges)


def karate(fill=None, heavy=(), heavy_color="accentthree", rings=(),
           ring_color="accenttwo", faint=(), dashes=(), big=(), extra=""):
    """The club, recoloured.

    fill    {node: tikz colour} -- anything unlisted is drawn `annot` gray
    heavy   edges to draw thick in `heavy_color` (crossing edges, a single cut, ...)
    faint   edges to draw at low opacity (context that is not this slide's point)
    dashes  edges to draw dashed
    rings   nodes to circle in `ring_color`
    big     nodes to draw larger -- ONLY where the slide says what the size means
    """
    pos, edges = club()
    fill = fill or {}
    heavy, faint, dashes = set(map(_k, heavy)), set(map(_k, faint)), set(map(_k, dashes))
    out = ""
    for e in edges:
        k = _k(e)
        p, q = pos[e[0]], pos[e[1]]
        if k in heavy:
            out += seg(p, q, color=heavy_color, w=5.6)
        elif k in faint:
            out += seg(p, q, color="black", w=2.2, opacity=0.30)
        elif k in dashes:
            out += seg(p, q, color=GRAY and "annot", w=2.4, dash="dash pattern=on 6bp off 5bp")
        else:
            out += seg(p, q, color="black", w=2.2)
    for n, (x, y) in pos.items():
        # 1.55 lands at 52.7px and the gate's ceiling is 52 -- exactly the kind of
        # off-by-a-pixel that a computed assertion would have called fine.
        size = KNODE * 1.42 if n in big else KNODE
        out += disc(x, y, fill=fill.get(n, CDIM), size=size)
    for n in rings:
        out += ring(*pos[n], size=KNODE, color=ring_color, w=4.4, grow=13)
    return out + extra


def _k(e):
    return (min(e), max(e))


def split_fill(hi_nodes, hi=CHI, off=COFF):
    """{node: colour} for a two-club colouring, Mr. Hi's side first."""
    return {n: (hi if n in hi_nodes else off) for n in range(34)}


def parts_fill(parts, colours=(CHI, COFF, "accentthree", "annot")):
    return {n: colours[i % len(colours)] for i, c in enumerate(parts) for n in c}


def free_note(s, pos, edges, canvas=(FULL_W, KCANVAS_H), size=FONT, color="accenttwo",
              margin=16, pad=10):
    """Put a short note wherever the drawing is empty, or fail and say to shorten it.

    m03 drew an in-figure note straight through a town name because the note sat at a
    fixed corner while the names were solved.  Here nothing is fixed: candidate anchors
    are scanned and each is rejected if it touches a disc, an edge, or the page.
    """
    b0 = label_box(0, 0, s, "center", size=size)
    w, h = b0[2] - b0[0], b0[3] - b0[1]
    cands = []
    for fy in (0.94, 0.06, 0.5, 0.82, 0.18):
        for fx in np.linspace(0.08, 0.92, 22):
            cands.append((fx * canvas[0], fy * canvas[1]))
    for cx, cy in cands:
        box = (cx - w / 2 - pad, cy - h / 2 - pad, cx + w / 2 + pad, cy + h / 2 + pad)
        if not (margin <= box[0] and box[2] <= canvas[0] - margin
                and margin <= box[1] and box[3] <= canvas[1] - margin):
            continue
        if any(_box_hits_disc(box, x, y, KNODE / 2 + 6) for x, y in pos.values()):
            continue
        if any(_box_hits_seg(box, pos[a], pos[b]) for a, b in edges):
            continue
        return text(cx, cy, s, color=color, anchor="center", size=size), box
    raise SystemExit(
        f"no free space for the in-figure note {s!r} -- shorten it (numbers only; "
        f"prose belongs in the deck's figcaption), or drop it")


def _box_hits_disc(b, x, y, r):
    d = (max(b[0] - x, 0, x - b[2]), max(b[1] - y, 0, y - b[3]))
    return math.hypot(*d) < r


def _box_hits_seg(b, p, q, pad=3):
    x0, y0, x1, y1 = b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for num, den in ((p[0] - x0, -dx), (x1 - p[0], dx), (p[1] - y0, -dy), (y1 - p[1], dy)):
        if den == 0:
            if num < 0:
                return False
            continue
        t = num / den
        if den < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return False
    return True


# ------------------------------------------------------------------- small planar graphs
def small(pos, edges, fill=None, heavy=(), heavy_color="accenttwo", rings=(),
          ring_color="accenttwo", dashes=(), labels=None, node=NODE, what="figure",
          edge_w=2.8, dim=(), label_size=FONT, planar=True, edges_all=None):
    """A mechanism graph: drawn planar, and asserted planar on the page.

    `assert_planar_drawing` checks two different failures -- an edge crossing another
    edge, and an edge passing through a disc it does not end at.  Both make a small
    diagram unreadable, and both are invisible in the source.

    `planar=False` is for the handful of graphs that have no crossing-free drawing at
    all (a clique of four or more drawn as equals, two five-cliques). The disc-clearance
    half of the check still runs: an edge that appears to end at the wrong person is
    never acceptable, however dense the graph.

    `edges_all` lists edges to be drawn dashed on top of `edges` -- absent friendships,
    which are the point of the k-plex and clique slides.
    """
    fill = fill or {}
    heavy, dashes, dim = set(map(_k, heavy)), set(map(_k, dashes)), set(dim)
    edges = list(edges) + [e for e in (edges_all or []) if _k(e) in dashes
                           and _k(e) not in {_k(x) for x in edges}]
    drawn = [e for e in edges if _k(e) not in dashes]
    # The clearance radius has to follow the disc actually being drawn. figlib's default
    # is half of ITS node size, which on a 28bp figure rejects drawings that are fine and
    # on a 52bp one would pass drawings that are not.
    r = node / 2 + 3
    if planar:
        x = crossings(drawn, pos)
        assert not x, f"{what}: {len(x)} edge crossing(s) in a planar graph -- {x[:3]}"
    bad = clearance_bad(drawn, pos, r=r)
    assert not bad, f"{what}: edge passes through a disc it does not end at -- {bad[:3]}"
    out = ""
    for e in edges:
        k = _k(e)
        p, q = pos[e[0]], pos[e[1]]
        if k in dashes:
            out += seg(p, q, color="annot", w=2.4, dash="dash pattern=on 7bp off 6bp")
        elif k in heavy:
            out += seg(p, q, color=heavy_color, w=5.8)
        else:
            out += seg(p, q, color="black", w=edge_w)
    for n, (x, y) in pos.items():
        out += disc(x, y, fill="annot" if n in dim else fill.get(n, "accent"), size=node)
    for n in rings:
        out += ring(x=pos[n][0], y=pos[n][1], size=node, color=ring_color, w=4.6, grow=14)
    if labels:
        chosen, _ = place_labels(labels, pos, drawn, size=label_size)
        out += draw_labels(labels, pos, chosen, size=label_size)
    return out


def relax(pos, edges, node=NODE, box=None, sweeps=260, seed=0):
    """Push a spring layout until no disc overlaps and no edge crosses a stranger's disc.

    `nx.spring_layout` optimises edge lengths and knows nothing about disc radius, so on
    a forty-node graph it reliably parks somebody on top of an edge they have no part in.
    This is the same repair the club's own layout does, in miniature: repel overlapping
    pairs, and push a disc off any edge that is running through it.
    """
    keys = sorted(pos)
    P = np.array([pos[k] for k in keys], float)
    idx = {k: i for i, k in enumerate(keys)}
    E = np.array([[idx[a], idx[b]] for a, b in edges])
    sep, clear = node * 1.30, node / 2 + 5
    lo = np.array([box[0], box[1]]) if box else P.min(0)
    hi = np.array([box[2], box[3]]) if box else P.max(0)
    rng = np.random.default_rng(seed)
    for _ in range(sweeps):
        D = P[:, None, :] - P[None, :, :]
        d = np.linalg.norm(D, axis=-1)
        np.fill_diagonal(d, np.inf)
        bad = d < sep
        if bad.any():
            push = np.where(bad[..., None], D / np.maximum(d, 1e-6)[..., None]
                            * (sep - np.minimum(d, sep))[..., None] * 0.5, 0.0).sum(1)
            P += push
        A, B = P[E[:, 0]], P[E[:, 1]]
        seg_d = _seg_point_dist_np(A, B, P)
        for r in range(len(E)):
            seg_d[r, E[r, 0]] = seg_d[r, E[r, 1]] = np.inf
        hits = np.argwhere(seg_d < clear)
        for r, k in hits:
            a, b = P[E[r, 0]], P[E[r, 1]]
            t = a - b
            nvec = np.array([-t[1], t[0]])
            nvec = nvec / max(np.linalg.norm(nvec), 1e-6)
            if rng.random() < 0.5:
                nvec = -nvec
            P[k] += nvec * (clear - seg_d[r, k] + 2.0)
        P = np.clip(P, lo, hi)
    return {k: (float(P[i, 0]), float(P[i, 1])) for i, k in enumerate(keys)}


def _seg_point_dist_np(A, B, P):
    d = B - A
    L2 = np.maximum((d * d).sum(1), 1e-9)
    t = np.clip(((P[None, :, :] - A[:, None, :]) * d[:, None, :]).sum(-1) / L2[:, None],
                0.0, 1.0)
    foot = A[:, None, :] + t[:, :, None] * d[:, None, :]
    return np.linalg.norm(foot - P[None, :, :], axis=-1)


def blob(cx, cy, rx, ry, color="accentthree", opacity=0.30, edge="annot", lw=2.6):
    """A crowd drawn as a crowd. Forty people with 252 friendships between them is a
    hairball at any size that fits a slide, and the slide's point is the two cliques
    beside it -- so the crowd is one shape, and the figcaption says how many are in it."""
    return (f"\\fill[{color},opacity={opacity}] ({cx},{cy}) ellipse "
            f"({rx}bp and {ry}bp);\n"
            f"\\draw[line width={lw}bp,draw={edge}] ({cx},{cy}) ellipse "
            f"({rx}bp and {ry}bp);\n")


def ring_positions(n, cx, cy, rx, ry, start=90.0, order=None):
    """n points on an ellipse.  Wide, not circular: a square figure cannot pass the
    width floor and the height cap at the same time (FIGURE_GUIDE).

    `order` names which node sits at each successive angle, so a clique can be rotated
    to put the node carrying an outside edge on the side that edge leaves from. Getting
    that wrong is what drove the bridge of `two-cliques` straight through a disc it does
    not end at.
    """
    order = order if order is not None else list(range(n))
    return {order[i]: (cx + rx * math.cos(math.radians(start + 360.0 * i / n)),
                       cy + ry * math.sin(math.radians(start + 360.0 * i / n)))
            for i in range(n)}


def clique_edges(nodes):
    return [(a, b) for i, a in enumerate(nodes) for b in nodes[i + 1:]]


# --------------------------------------------------------------------------- primitives
def cell_grid(x0, y0, n, cell, filled, fill_color="accent", empty="white",
              gap=0.0, line="annot", lw=1.2, diag=None):
    """An n x n matrix of cells. `filled` is a set of (row, col), row 0 at the top."""
    out = ""
    for r in range(n):
        for c in range(n):
            x, y = x0 + c * (cell + gap), y0 - r * (cell + gap)
            col = fill_color(r, c) if callable(fill_color) else fill_color
            f = (r, c) in filled if not callable(filled) else filled(r, c)
            out += (f"\\draw[line width={lw}bp,draw={line},fill={col if f else empty}] "
                    f"({x:.1f},{y:.1f}) rectangle ({x + cell:.1f},{y - cell:.1f});\n")
    if diag:
        for a, b, colour in diag:
            out += (f"\\draw[line width=3.2bp,draw={colour}] "
                    f"({x0 + a * (cell + gap):.1f},{y0 - a * (cell + gap):.1f}) rectangle "
                    f"({x0 + b * (cell + gap):.1f},{y0 - b * (cell + gap):.1f});\n")
    return out


def number_line(x0, x1, y, lo, hi, marks, tick=11, size=FONT, fmt="{:g}", rows=3,
                row_h=None, what="number line"):
    """A single axis with named marks -- the deck's stand-in for a bar chart.

    FIGURE_GUIDE bans bars: they encode one number as a length and then need a scale to
    decode it. A position on a labelled line is the number.

    **Labels are placed, not just emitted.** The first version put every label at a fixed
    offset from its own tick, and two marks half a unit apart printed straight through
    each other -- "the rule of thumbthe real split" on one slide, "the real split" over
    "Louvain" on another, both invisible in the source and both shipped past a green
    gate. Each label now walks outward row by row on its own side of the axis and takes
    the first row that collides with nothing: no other label, and neither end label. If
    no assignment exists the build fails and says to shorten a label, because a label
    too long to place is the bug.
    """
    row_h = row_h or size * 1.30
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)                    # noqa: E731
    out = seg((x0, y), (x1, y), color="black", w=2.4)

    placed = []
    for v in (lo, hi):
        b = label_box(X(v), y - tick - 12, fmt.format(v), "north", size=size)
        placed.append(b)
        out += text(X(v), y - tick - 12, fmt.format(v), color="annot",
                    anchor="north", size=size)

    for v, lab, col, side in marks:
        assert lo <= v <= hi, f"{what}: mark {lab!r} at {v} is off the axis [{lo}, {hi}]"
        x = X(v)
        s = 1 if side == "up" else -1
        out += seg((x, y), (x, y + s * tick), color=col, w=3.6)
        anchor = "south" if s > 0 else "north"
        for r in range(rows):
            ly = y + s * (tick + 12 + r * row_h)
            b = label_box(x, ly, lab, anchor, size=size)
            if any(boxes_overlap(b, o) for o in placed):
                continue
            placed.append(b)
            out += text(x, ly, lab, color=col, anchor=anchor, size=size)
            break
        else:
            raise SystemExit(
                f"{what}: no free row for the mark {lab!r} at {v} -- it collides with a "
                f"neighbouring label on every row. Shorten it, move the mark, or put the "
                f"two marks on opposite sides of the axis; do not shrink the type.")
    return out


def dot_strip(x0, x1, y, values, lo, hi, color="accent", d=9, jitter=0.0, seed=3):
    """Every value as its own dot -- the actual objects, not a summary."""
    rng = np.random.default_rng(seed)
    out = ""
    for v in values:
        x = x0 + (v - lo) / (hi - lo) * (x1 - x0)
        out += dot(x, y + (rng.normal(0, jitter) if jitter else 0.0), color=color, d=d)
    return out


def brace(x0, x1, y, up=True, depth=14, color="annot", w=2.2):
    s = 1 if up else -1
    return polyline([(x0, y), (x0, y + s * depth), (x1, y + s * depth), (x1, y)],
                    color=color, w=w)


def arrow(p, q, color="annot", w=3.0, head=9):
    return seg(p, q, color=color, w=w,
               arrow=f"-{{Stealth[length={head}bp,width={head * 0.8:.1f}bp]}}")


def bag(cx, cy, w, h, color="annot", lw=2.6):
    """A simple open sack for the balls-and-strings game."""
    return (f"\\draw[line width={lw}bp,draw={color}] "
            f"({cx - w / 2:.1f},{cy + h / 2:.1f}) .. controls "
            f"({cx - w * 0.72:.1f},{cy - h * 0.30:.1f}) and "
            f"({cx - w * 0.34:.1f},{cy - h / 2:.1f}) .. ({cx:.1f},{cy - h / 2:.1f}) "
            f".. controls ({cx + w * 0.34:.1f},{cy - h / 2:.1f}) and "
            f"({cx + w * 0.72:.1f},{cy - h * 0.30:.1f}) .. "
            f"({cx + w / 2:.1f},{cy + h / 2:.1f});\n")


def _bow_control(p, q, bow):
    """Control point for a string that sags away from the straight line.

    The first version displaced the midpoint straight down in y, which does nothing to a
    vertical edge -- it just slides the control point along the line. Sagging along the
    PERPENDICULAR, biased downwards, bows every edge whatever its direction.
    """
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy) or 1.0
    nx_, ny_ = -dy / L, dx / L
    if ny_ > 0:                      # always hang downwards
        nx_, ny_ = -nx_, -ny_
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    return (mx + nx_ * bow * L, my + ny_ * bow * L)


def string(p, q, color="annot", w=2.4, bow=0.13):
    """A hanging string between two balls."""
    cx, cy = _bow_control(p, q, bow)
    return (f"\\draw[line width={w}bp,draw={color}] ({p[0]:.1f},{p[1]:.1f}) "
            f".. controls ({cx:.1f},{cy:.1f}) .. ({q[0]:.1f},{q[1]:.1f});\n")


def strings_graph(pos, edges, fill, node=34, bow=0.13, w=3.0, color="annot",
                  cut=False, what="strings"):
    """The network drawn as balls hanging on strings, rather than as a node-link diagram.

    The slide's claim is "every friendship is two coloured balls on a string" and the
    first version drew ordinary straight edges, so the room saw a graph and heard a
    metaphor. `cut=True` snips every string into two stubs, which is what stage three of
    the game actually does.

    The bowed curve is sampled and checked against every disc it does not end at: a sag
    that dips through somebody's head is worse than a straight line.
    """
    out = ""
    for a, b in edges:
        p, q = pos[a], pos[b]
        c = _bow_control(p, q, bow)
        for t in np.linspace(0.05, 0.95, 19):          # quadratic Bezier samples
            x = (1 - t) ** 2 * p[0] + 2 * (1 - t) * t * c[0] + t ** 2 * q[0]
            y = (1 - t) ** 2 * p[1] + 2 * (1 - t) * t * c[1] + t ** 2 * q[1]
            for k, (kx, ky) in pos.items():
                if k in (a, b):
                    continue
                assert math.hypot(x - kx, y - ky) >= node / 2 + 4, (
                    f"{what}: the string {a}-{b} sags through disc {k} -- reduce bow "
                    f"or move the node")
        if cut:
            for lo, hi in ((0.0, 0.30), (0.70, 1.0)):
                pts = []
                for t in np.linspace(lo, hi, 7):
                    pts.append(((1 - t) ** 2 * p[0] + 2 * (1 - t) * t * c[0] + t ** 2 * q[0],
                                (1 - t) ** 2 * p[1] + 2 * (1 - t) * t * c[1] + t ** 2 * q[1]))
                out += polyline(pts, color=color, w=w)
        else:
            out += string(p, q, color=color, w=w, bow=bow)
    for n, (x, y) in pos.items():
        out += disc(x, y, fill=fill[n], size=node)
    return out


def assert_boxes_clear(boxes, what):
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            assert not boxes_overlap(boxes[i], boxes[j]), \
                f"{what}: annotation boxes {i} and {j} overlap"

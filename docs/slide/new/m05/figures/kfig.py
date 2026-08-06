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
    ACCENT, ACCENT2, ACCENT3, FONT, GRAY, NODE, Axes, assert_planar_drawing,
    boxes_overlap, clearance_bad, disc, dot, draw_labels, label_box, place_labels,
    polyline, ring, seg, text,
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
            out += seg(p, q, color="black", w=2.0, opacity=0.16)
        elif k in dashes:
            out += seg(p, q, color=GRAY and "annot", w=2.4, dash="dash pattern=on 6bp off 5bp")
        else:
            out += seg(p, q, color="black", w=2.2)
    for n, (x, y) in pos.items():
        size = KNODE * 1.55 if n in big else KNODE
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
    if planar:
        assert_planar_drawing(drawn, pos, what)
    else:
        bad = clearance_bad(drawn, pos)
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


def number_line(x0, x1, y, lo, hi, marks, tick=11, size=FONT, fmt="{:.3f}"):
    """A single axis with named marks -- the deck's stand-in for a bar chart.

    FIGURE_GUIDE bans bars: they encode one number as a length and then need a scale to
    decode it.  A position on a labelled line is the number.
    """
    out = seg((x0, y), (x1, y), color="black", w=2.4)
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)                    # noqa: E731
    for v, lab, col, side in marks:
        assert lo <= v <= hi, f"mark {lab} at {v} is off the axis [{lo}, {hi}]"
        x = X(v)
        s = 1 if side == "up" else -1
        out += seg((x, y), (x, y + s * tick), color=col, w=3.6)
        out += text(x, y + s * (tick + 12), lab, color=col,
                    anchor="south" if s > 0 else "north", size=size)
    for v in (lo, hi):
        out += text(X(v), y - tick - 12, fmt.format(v), color="annot",
                    anchor="north", size=size)
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


def string(p, q, color="annot", w=2.4, sag=16):
    """A hanging string between two balls."""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2 - sag
    return (f"\\draw[line width={w}bp,draw={color}] ({p[0]:.1f},{p[1]:.1f}) "
            f".. controls ({mx:.1f},{my:.1f}) .. ({q[0]:.1f},{q[1]:.1f});\n")


def assert_boxes_clear(boxes, what):
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            assert not boxes_overlap(boxes[i], boxes[j]), \
                f"{what}: annotation boxes {i} and {j} overlap"

#!/usr/bin/env python3
"""Module 06, Parts 7-8: the directed web, and the figures that close the deck.

Everything that draws the eight-page web draws it from `WEB_XY` -- one affine map
of `verify_numbers.WEB_POS` into the drawing box, computed once here and asserted
by `assert_web_geometry()` in every figure that uses it. A page that moves between
two slides is a build failure with the page named.

Two drawing facts about this layout, both of them forced by the data rather than
chosen:

* `Links`, `Wiki` and `News` are collinear in `WEB_POS` (Wiki sits exactly at the
  midpoint), so the Links -> News link cannot be a straight line: it would run the
  length of the Wiki -> News link and straight through the Wiki disc.
* `News -- Blog` and `Course -- Wiki` cross in the straight-line drawing, and no
  affine map removes a crossing. Course can only go in a face touching both Blog
  and Wiki, and both of those faces are triangles too thin to hold a disc, so the
  long News -> Blog link is routed over the top instead.

Both are drawn as explicit cubic Beziers (control points computed here, not TikZ
`bend`), so the crossing and clearance gates below check the curve that is
actually drawn rather than its chord.
"""

import functools
import inspect
import math
import os
import re

import numpy as np

import figlib as F
from figlib import ACCENT, ACCENT2, ACCENT3, GRAY
from verify_numbers import (COST_ITER, COST_M, COST_N, COST_RATIO, COST_SWEEP,
                            PPR_FOCUS, PPR_FOCUS_MARGIN, PPR_GLOBAL_MARGIN, WEB,
                            WEB_AUT, WEB_AUT_KING, WEB_DANGLING, WEB_HUB,
                            WEB_HUB_KING, WEB_LINKS, WEB_NAMES, WEB_POS, WEB_PPR,
                            WEB_PR, WEB_PR_KING, WEB_PR_RANK_OF_LINKS,
                            crown_robustness, pagerank)

# TikZ colour names (the imported constants are hex, for \definecolor only).
A1, A2, A3, GY = "accent", "accenttwo", "accentthree", "annot"
ARROW = "-{Stealth[length=12bp,width=9.5bp]}"
R = F.NODE / 2                      # disc radius, bp
CLEAR = R + 4                       # a path may come no closer to a disc it misses

# =============================================================================
# The one web geometry
# =============================================================================
_XL, _XS = 130.0, 127.0             # x = _XL + u * _XS
_YB, _YS = 52.0, 58.0               # y = _YB + (v + 1) * _YS
WEB_XY = {n: (_XL + u * _XS, _YB + (v + 1.0) * _YS) for n, (u, v) in WEB_POS.items()}

# Ink budget for a plain full-width figure: 380 bp cap less figlib's 12 bp of crop
# padding on each side.
INK_H = 356
CANVAS_H = 372

# Two strips kept clear of city labels so that every figure has somewhere to put a
# note. Reserved once, before the labels are solved, so no annotation can ever
# land on a name.
ZONE_A = (516.0, 12.0, 1072.0, 100.0)      # bottom right, two lines
ZONE_B = (8.0, 12.0, 300.0, 100.0)         # bottom left, under Links

# Bulge of each drawn link, in bp, positive to the LEFT of travel. A reciprocal
# pair gets the same sign, so the two arcs bow apart. Zero is a straight line.
BULGE = {
    ("Links", "News"): -64.0,       # must pass under the Wiki disc it is collinear with
    ("Forum", "News"): -30.0,       # else it arrives at News along the same bearing
    ("Blog", "Course"): 24.0, ("Course", "Blog"): 24.0,
    ("Wiki", "News"): 22.0, ("News", "Wiki"): 22.0,
}
# The one link with hand-placed control points: over the top of Course, coming
# down into Blog from directly above so it clears the Blog <-> Course pair.
CTRL = {("News", "Blog"): ((555.0, 360.0), (205.0, 360.0))}


def assert_web_geometry(name, xy):
    """Every web figure calls this. A moved page fails the build, by name."""
    assert set(xy) == set(WEB_XY), f"{name}: draws {sorted(set(xy) ^ set(WEB_XY))}"
    off = [n for n in xy if abs(xy[n][0] - WEB_XY[n][0]) > 1e-9
           or abs(xy[n][1] - WEB_XY[n][1]) > 1e-9]
    assert not off, (f"{name}: {', '.join(off)} moved -- every web slide must show the "
                     f"identical eight pages, or the deck's one-web claim is false")


def _controls(a, b, bulge):
    p0, p3 = np.array(WEB_XY[a]), np.array(WEB_XY[b])
    d = p3 - p0
    u = d / np.linalg.norm(d)
    n = np.array([-u[1], u[0]])
    return tuple(p0 + d / 3 + bulge * n), tuple(p0 + 2 * d / 3 + bulge * n)


def link_ctrl(a, b):
    if (a, b) in CTRL:
        return CTRL[(a, b)]
    bulge = BULGE.get((a, b), 0.0)
    return None if bulge == 0.0 else _controls(a, b, bulge)


def link_path(a, b, n=64):
    """The sampled path actually drawn, centre to centre."""
    p0, p3 = np.array(WEB_XY[a]), np.array(WEB_XY[b])
    c = link_ctrl(a, b)
    if c is None:
        return [tuple(p0), tuple(p3)]
    p1, p2 = np.array(c[0]), np.array(c[1])
    ts = np.linspace(0, 1, n)
    pts = [(1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1
           + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3 for t in ts]
    return [tuple(p) for p in pts]


def link(a, b, color="black", w=F.EDGE_W, dash="", arrow=True, opacity=None):
    """One directed link, clipped to the two discs by TikZ so the head MEETS the disc."""
    o = [f"line width={w}bp", f"draw={color}"]
    if arrow:
        o.append(ARROW)
    if dash:
        o.append(dash)
    if opacity is not None:
        o.append(f"opacity={opacity}")
    c = link_ctrl(a, b)
    if c is None:
        return f"\\draw[{','.join(o)}] ({a}) -- ({b});\n"
    return (f"\\draw[{','.join(o)}] ({a}) .. controls "
            f"({c[0][0]:.1f},{c[0][1]:.1f}) and ({c[1][0]:.1f},{c[1][1]:.1f}) .. ({b});\n")


# --------------------------------------------------------------------------- gates
def _seg_pt_dist(p, q, x):
    p, q, x = np.array(p), np.array(q), np.array(x)
    d = q - p
    L2 = float(d @ d)
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, float((x - p) @ d) / L2))
    return float(np.linalg.norm(p + t * d - x))


def _cross_pt(p1, p2, p3, p4):
    """Intersection point of two segments, or None."""
    if not F._seg_cross(p1, p2, p3, p4):
        return None
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


_PATHS = {(a, b): link_path(a, b) for a, b in WEB_LINKS}


def _check_web_drawing():
    """Zero crossings and no path through a disc it does not end at.

    Checked on the sampled curves, not on the chords: two of these links are drawn
    as Beziers precisely because their chords are wrong.
    """
    for (a, b), P in _PATHS.items():
        for n, c in WEB_XY.items():
            if n in (a, b):
                continue
            d = min(_seg_pt_dist(P[i], P[i + 1], c) for i in range(len(P) - 1))
            assert d >= CLEAR, (f"the {a} -> {b} link passes {d:.1f}bp from the {n} disc "
                                f"(needs {CLEAR:.0f})")
    items = list(_PATHS.items())
    for i, ((a, b), P) in enumerate(items):
        for (c, d), Q in items[i + 1:]:
            if {a, b} == {c, d}:
                continue                        # a reciprocal pair, drawn as two arcs
            shared = ({a, b} & {c, d})
            for u in range(len(P) - 1):
                for v in range(len(Q) - 1):
                    x = _cross_pt(P[u], P[u + 1], Q[v], Q[v + 1])
                    if x is None:
                        continue
                    if shared and min(math.dist(x, WEB_XY[s]) for s in shared) < R + 12:
                        continue                # they meet at the disc they share
                    raise AssertionError(
                        f"{a}->{b} crosses {c}->{d} at ({x[0]:.0f},{x[1]:.0f})")


_check_web_drawing()

# The degrees the drawing is asked to make readable.
assert WEB.out_degree("Links") == 4 and WEB.in_degree("Links") == 0
assert WEB.out_degree(WEB_DANGLING[0]) == 0
assert len(WEB_LINKS) == WEB.number_of_edges() == 14
_RECIP = sorted({tuple(sorted(e)) for e in WEB_LINKS if tuple(reversed(e)) in WEB_LINKS})
assert len(_RECIP) == 2, _RECIP

# --------------------------------------------------------------------------- labels
# Solved once against the discs, the straight links, the curved links (as blocker
# boxes) and the two annotation strips, then frozen: two web figures may not place
# the same page name differently.
_STRAIGHT = [(a, b) for a, b in WEB_LINKS if link_ctrl(a, b) is None]


def _path_blockers(step=6):
    out = []
    for (a, b), P in _PATHS.items():
        if link_ctrl(a, b) is None:
            continue
        for i in range(0, len(P), 4):
            x, y = P[i]
            out.append((x - step, y - step, x + step, y + step))
    return out


LABEL_SIDES, LABEL_BOXES = F.place_labels(
    {n: n for n in WEB_NAMES}, WEB_XY, _STRAIGHT,
    blockers=_path_blockers() + [ZONE_A, ZONE_B],
    bounds=(8.0, 8.0, 1072.0, INK_H - 8.0), gap=3.0)


def labels(color="black"):
    return F.draw_labels({n: n for n in WEB_NAMES}, WEB_XY, LABEL_SIDES, color=color)


# --------------------------------------------------------------------------- ink
def anchors():
    """Phantom nodes, so TikZ clips every arrow to the disc border for us."""
    return "".join(f"\\node[circle,minimum size={F.NODE}bp,inner sep=0pt] "
                   f"({n}) at ({x:.2f},{y:.2f}) {{}};\n" for n, (x, y) in WEB_XY.items())


def links(color="black", w=F.EDGE_W):
    return "".join(link(a, b, color=color, w=w) for a, b in WEB_LINKS)


def _mix(t, base=(0x39, 0x59, 0xA6)):
    """White -> accent at fraction t, floored so a low disc is still a disc."""
    t = 0.16 + 0.84 * max(0.0, min(1.0, float(t)))
    return "".join(f"{int(round(255 + (c - 255) * t)):02X}" for c in base)


def discs(scores=None):
    """Eight discs, plain accent or shaded by `scores` (page -> value)."""
    out = ""
    top = max(scores.values()) if scores else 1.0
    for i, n in enumerate(WEB_NAMES):
        x, y = WEB_XY[n]
        if scores is None:
            fill = "accent"
        else:
            fill = f"wsh{i}"
            out += f"\\definecolor{{{fill}}}{{HTML}}{{{_mix(scores[n] / top)}}}\n"
        out += (f"\\draw[line width=1.6bp,draw=black,fill={fill}] "
                f"({x:.2f},{y:.2f}) circle ({R}bp);\n")
    return out


def web_body(scores=None, label_color="black"):
    assert_web_geometry("web_body", WEB_XY)
    return anchors() + links() + discs(scores) + labels(color=label_color)


def ring(page, color=A2, grow=14, w=4.0):
    x, y = WEB_XY[page]
    return F.ring(x, y, size=F.NODE, color=color, w=w, grow=grow)


def crown_glyph(x, y, color=A2, w=30.0, h=19.0):
    pts = [(x - w / 2, y - h / 2), (x - w / 2, y + h / 2), (x - w / 4, y),
           (x, y + h / 2 + 4), (x + w / 4, y), (x + w / 2, y + h / 2),
           (x + w / 2, y - h / 2)]
    return "\\fill[%s] %s -- cycle;\n" % (
        color, " -- ".join(f"({a:.2f},{b:.2f})" for a, b in pts))


def tri(x, y, up=True, color=A2, w=30.0, h=24.0):
    pts = ([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x, y + h / 2)] if up
           else [(x - w / 2, y + h / 2), (x + w / 2, y + h / 2), (x, y - h / 2)])
    return "\\fill[%s] %s -- cycle;\n" % (
        color, " -- ".join(f"({a:.2f},{b:.2f})" for a, b in pts))


# --------------------------------------------------------------------------- checks
def drawn_texts(body):
    """Every string the figure actually prints (node contents), for the no-digit gate."""
    b = re.sub(r"\\definecolor\{[^}]*\}\{[^}]*\}\{[^}]*\}", "", body)
    return [t for t in re.findall(r"\{([^{}]*)\};", b) if t.strip()]


def assert_no_digits(name, body):
    bad = [t for t in drawn_texts(body) if re.search(r"\d", t)]
    assert not bad, f"{name}: a digit is drawn on a question slide -- {bad}"


def dec(x, d=3):
    """Round half UP in decimal: a float 0.0575 prints 0.057 through %f."""
    from decimal import ROUND_HALF_UP, Decimal
    q = Decimal(repr(float(x))).quantize(Decimal("1." + "0" * d), rounding=ROUND_HALF_UP)
    return str(q)


def assert_clear(name, boxes, *, against=()):
    """No two annotation boxes overlap, and none lands on a page name."""
    allb = list(boxes) + list(against)
    for i, a in enumerate(allb):
        for b in allb[i + 1:]:
            assert not F.boxes_overlap(a, b), f"{name}: two labels overlap -- {a} {b}"


def note_at(name, s, at, color=A2, anchor="west", size=F.FONT, extra=()):
    """A note, asserted clear of every frozen page label and of `extra` boxes."""
    b = F.label_box(at[0], at[1], s, anchor, size=size)
    assert 4 <= b[0] and b[2] <= 1076, f"{name}: note {s!r} runs off the canvas ({b})"
    hit = [k for k, v in LABEL_BOXES.items() if F.boxes_overlap(b, v)]
    assert not hit, f"{name}: note {s!r} collides with {hit} -- shorten it or move it"
    for e in extra:
        assert not F.boxes_overlap(b, e), f"{name}: note {s!r} collides with {e}"
    return F.text(at[0], at[1], s, color=color, anchor=anchor, size=size), b

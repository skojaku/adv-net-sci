#!/usr/bin/env python3
"""Module 06, Parts 7-8: the directed web, and the figures that close the deck.

Every figure that draws the eight-page web draws it from `WEB_XY`, computed once
here and checked by `assert_web_geometry()` in each of them: a page that moves
between two slides is a build failure with the page named.

WHY THE PAGES ARE BOXES AND NOT DISCS
-------------------------------------
Because the eight names have to be readable at the 36 pt floor, and around discs
they cannot be. `verify_numbers.WEB_POS` is a schematic, and its straight-line
drawing is not usable as one:

* `Links`, `Wiki` and `News` are collinear there -- Wiki sits exactly at the
  midpoint of Links--News -- and no affine map removes that;
* `News--Blog` crosses `Course--Wiki`, and no affine map removes that either;
* `Wiki` has four links plus a reciprocal pair, so with a disc its name has no
  free side: west is taken by Links and Blog, east by News, north by Course, and
  south by whichever of the two problem links is routed under it. `place_labels`
  fails on it, which is exactly the situation FIGURE_GUIDE says to answer by
  moving the drawing, never by shrinking the type.

So the pages are drawn as page boxes with the name inside -- smaller than a disc
plus an outside label, and the shape a web page wants anyway -- and the layout is
a fresh planar drawing of the same link set. A web has no true positions (unlike
the Roman map, whose geography is a claim), so re-laying it out costs nothing and
buys a drawing with no crossings and no unplaceable name. The gates below check
the drawing that is actually emitted: no box overlaps another, no path enters a
box it does not end at, no two paths cross away from a shared page.
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

# TikZ colour names. The imported hex constants are for \definecolor only.
A1, A2, A3, GY = "accent", "accenttwo", "accentthree", "annot"
ARROW = "-{Stealth[length=12bp,width=9.5bp]}"
BOX_H = 54.0                       # page box height, bp
CLEAR = 10.0                       # a path may come no closer to a box it misses
INK_H = 356                        # 380 bp cap less figlib's 12 bp of crop padding
CANVAS_H = 372

# =============================================================================
# 1. The one web geometry
# =============================================================================
WEB_XY = {
    "Links": (110.0, 60.0),
    "Blog": (110.0, 290.0),
    "Course": (268.0, 170.0),
    "Wiki": (500.0, 168.0),
    "Forum": (450.0, 48.0),
    "News": (886.0, 175.0),
    "Paper": (880.0, 300.0),
    "Home": (1004.0, 212.0),
}
assert set(WEB_XY) == set(WEB_POS)


def box_w(name):
    return F.CHAR_W * F.FONT * len(name) + 26.0


def box(name):
    x, y = WEB_XY[name]
    w = box_w(name)
    return (x - w / 2, y - BOX_H / 2, x + w / 2, y + BOX_H / 2)


BOXES = {n: box(n) for n in WEB_XY}

# Bulge of each drawn link, bp, positive to the LEFT of travel; a reciprocal pair
# gets two so the arrows are two separated arcs and never one line with two heads.
BULGE = {
    ("Blog", "Course"): 20.0, ("Course", "Blog"): 20.0,
    ("Wiki", "News"): 10.0, ("News", "Wiki"): 10.0,
}


def assert_web_geometry(name, xy):
    """Every web figure calls this. A moved page fails the build, by name."""
    assert set(xy) == set(WEB_XY), f"{name}: draws {sorted(set(xy) ^ set(WEB_XY))}"
    off = [n for n in xy if abs(xy[n][0] - WEB_XY[n][0]) > 1e-9
           or abs(xy[n][1] - WEB_XY[n][1]) > 1e-9]
    assert not off, (f"{name}: {', '.join(off)} moved -- every web slide must show the "
                     f"identical eight pages, or the deck's one-web claim is false")


# --------------------------------------------------------------------------- paths
def _controls(a, b, bulge):
    p0, p3 = np.array(WEB_XY[a]), np.array(WEB_XY[b])
    d = p3 - p0
    u = d / np.linalg.norm(d)
    n = np.array([-u[1], u[0]])
    return tuple(p0 + d / 3 + bulge * n), tuple(p0 + 2 * d / 3 + bulge * n)


def link_ctrl(a, b):
    bulge = BULGE.get((a, b), 0.0)
    return None if bulge == 0.0 else _controls(a, b, bulge)


def link_path(a, b, n=64):
    """The path actually drawn, sampled, centre to centre."""
    p0, p3 = np.array(WEB_XY[a]), np.array(WEB_XY[b])
    c = link_ctrl(a, b)
    if c is None:
        return [tuple(p0), tuple(p3)]
    p1, p2 = np.array(c[0]), np.array(c[1])
    return [tuple((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1
                  + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3) for t in np.linspace(0, 1, n)]


def link(a, b, color="black", w=F.EDGE_W, dash="", arrow=True, opacity=None):
    """One link, clipped by TikZ to both page boxes, so the head MEETS the box."""
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
def _grow(b, m):
    return (b[0] - m, b[1] - m, b[2] + m, b[3] + m)


def _cross_pt(p1, p2, p3, p4):
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
    for a, ba in BOXES.items():
        for b, bb in BOXES.items():
            if a < b:
                assert not F.boxes_overlap(_grow(ba, 8), bb), f"{a} and {b} boxes overlap"
    for (a, b), P in _PATHS.items():
        for n, bx in BOXES.items():
            if n in (a, b):
                continue
            g = _grow(bx, CLEAR)
            hit = any(F.box_hits_segment(g, P[i], P[i + 1], pad=0)
                      for i in range(len(P) - 1))
            assert not hit, f"the {a} -> {b} link runs into the {n} box"
    items = list(_PATHS.items())
    for i, ((a, b), P) in enumerate(items):
        for (c, d), Q in items[i + 1:]:
            if {a, b} == {c, d}:
                continue                       # a reciprocal pair, drawn as two arcs
            shared = {a, b} & {c, d}
            for u in range(len(P) - 1):
                for v in range(len(Q) - 1):
                    x = _cross_pt(P[u], P[u + 1], Q[v], Q[v + 1])
                    if x is None:
                        continue
                    if shared and any(F.box_hits_segment(_grow(BOXES[s], 20), x, x, pad=0)
                                      for s in shared):
                        continue               # they meet inside the page they share
                    raise AssertionError(
                        f"{a}->{b} crosses {c}->{d} at ({x[0]:.0f},{x[1]:.0f})")


_check_web_drawing()

# The degrees the drawing has to make readable without a legend.
assert WEB.out_degree("Links") == 4 and WEB.in_degree("Links") == 0
assert WEB.out_degree(WEB_DANGLING[0]) == 0 and WEB.in_degree(WEB_DANGLING[0]) == 1
assert len(WEB_LINKS) == WEB.number_of_edges() == 14
assert WEB.number_of_nodes() == 8
_RECIP = sorted({tuple(sorted(e)) for e in WEB_LINKS if tuple(reversed(e)) in WEB_LINKS})
assert len(_RECIP) == 2 and all(link_ctrl(*e) is not None for e in WEB_LINKS
                                if tuple(sorted(e)) in _RECIP), _RECIP

# Anchor points for the in-drawing notes. `note()` proves each one clear of every
# page box and every drawn link, so these are starting points, not licence.
NOTE_BR = (1068.0, 38.0)                       # bottom right, under Forum -> News
NOTE_TC = (452.0, 300.0)                       # top centre, over News -> Blog


# =============================================================================
# 2. Drawing the web
# =============================================================================
def _mix(t, base=(0x39, 0x59, 0xA6)):
    """White -> accent at fraction t, floored so a low page is still a page."""
    t = 0.14 + 0.86 * max(0.0, min(1.0, float(t)))
    return "".join(f"{int(round(255 + (c - 255) * t)):02X}" for c in base)


def anchors():
    """Invisible boxes, emitted first, so TikZ can clip every arrow to a border.

    The arrows are drawn between these and the visible boxes go on top, so a head
    that lands exactly on the border is never buried by the fill.
    """
    return "".join(
        f"\\node[rectangle,minimum width={box_w(n):.1f}bp,minimum height={BOX_H}bp,"
        f"inner sep=0pt] ({n}) at ({x:.1f},{y:.1f}) {{}};\n"
        for n, (x, y) in WEB_XY.items())


def pages(scores=None, ring=(), ring_color=A2, mark_color=A2):
    """The eight page boxes, plain or shaded white -> accent by `scores`."""
    assert_web_geometry("pages", WEB_XY)
    out = ""
    top = max(scores.values()) if scores else 1.0
    for i, n in enumerate(WEB_NAMES):
        x, y = WEB_XY[n]
        t = (scores[n] / top) if scores else 0.0
        if scores:
            fill = f"wsh{i}"
            out += f"\\definecolor{{{fill}}}{{HTML}}{{{_mix(t)}}}\n"
        else:
            fill = "white"
        tc = "white" if (scores and t > 0.55) else "black"
        out += (f"\\node[rectangle,rounded corners=7bp,draw=black,line width=1.8bp,"
                f"fill={fill},text={tc},minimum width={box_w(n):.1f}bp,"
                f"minimum height={BOX_H}bp,inner sep=0pt,"
                f"font=\\fontsize{{{F.FONT}}}{{{int(F.FONT * 1.15)}}}\\selectfont] "
                f"at ({x:.1f},{y:.1f}) {{{n}}};\n")
    for n in ring:
        b = _grow(BOXES[n], 9)
        out += (f"\\draw[line width=4bp,draw={ring_color},rounded corners=13bp] "
                f"({b[0]:.1f},{b[1]:.1f}) rectangle ({b[2]:.1f},{b[3]:.1f});\n")
    return out


def links(color="black", w=F.EDGE_W):
    return "".join(link(a, b, color=color, w=w) for a, b in WEB_LINKS)


def web_body(scores=None, ring=()):
    return anchors() + links() + pages(scores, ring=ring)


def crown_glyph(x, y, color=A2, w=34.0, h=21.0):
    pts = [(x - w / 2, y - h / 2), (x - w / 2, y + h / 2), (x - w / 4, y),
           (x, y + h / 2 + 5), (x + w / 4, y), (x + w / 2, y + h / 2),
           (x + w / 2, y - h / 2)]
    return "\\fill[%s] %s -- cycle;\n" % (
        color, " -- ".join(f"({a:.2f},{b:.2f})" for a, b in pts))


tri_w = 34.0


def tri(x, y, up=True, color=A2, w=tri_w, h=26.0):
    pts = ([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x, y + h / 2)] if up
           else [(x - w / 2, y + h / 2), (x + w / 2, y + h / 2), (x, y - h / 2)])
    return "\\fill[%s] %s -- cycle;\n" % (
        color, " -- ".join(f"({a:.2f},{b:.2f})" for a, b in pts))


# =============================================================================
# 3. Assertions on what the figure prints
# =============================================================================
def drawn_texts(body):
    """Every string the figure prints, read back out of the emitted markup."""
    b = re.sub(r"\\definecolor\{[^}]*\}\{[^}]*\}\{[^}]*\}", "", body)
    return [t for t in re.findall(r"\{([^{}]*)\};", b) if t.strip()]


def assert_no_digits(name, body):
    bad = [t for t in drawn_texts(body) if re.search(r"\d", t)]
    assert not bad, f"{name}: a digit is drawn on a question slide -- {bad}"


def dec(x, d=3):
    """Round half UP in decimal; %f rounds a shortest-repr float the other way."""
    from decimal import ROUND_HALF_UP, Decimal
    return str(Decimal(repr(float(x))).quantize(Decimal("1." + "0" * d),
                                                rounding=ROUND_HALF_UP))


def note(name, s, at, color=A2, anchor="west", size=F.FONT, extra=(), paths=True):
    """An in-drawing note, asserted clear of every page box and every drawn link.

    A note sits where the author put it while the drawing is generated, so a note
    that grows collides with whatever is there -- m03 drew one straight through a
    city name. The failure message says shorten it, because a long note is the bug:
    notes carry numbers, prose belongs in the deck's figcaption.
    """
    b = F.label_box(at[0], at[1], s, anchor, size=size)
    assert 6 <= b[0] and b[2] <= 1074 and 6 <= b[1] and b[3] <= INK_H, \
        f"{name}: note {s!r} runs off the canvas {b} -- shorten it"
    hit = [n for n, bx in BOXES.items() if F.boxes_overlap(b, _grow(bx, 6))]
    assert not hit, f"{name}: note {s!r} collides with {hit} -- shorten it or move it"
    if paths:
        for (u, v), P in _PATHS.items():
            assert not any(F.box_hits_segment(b, P[i], P[i + 1], pad=4)
                           for i in range(len(P) - 1)), \
                f"{name}: note {s!r} sits on the {u} -> {v} link -- shorten it or move it"
    for e in extra:
        assert not F.boxes_overlap(b, e), f"{name}: note {s!r} collides with {e}"
    return F.text(at[0], at[1], s, color=color, anchor=anchor, size=size), b


def badge(page, word, up=True, mark=True, color=A2):
    """The crown on a page: a ring extended by one line, carrying the role word.

    The word rides inside the ring rather than beside the box because both crowned
    pages sit in the left column, where the free space is 94 bp wide and the words
    are not. Everything is laid out inside the ring, and the ring is asserted clear
    of every other page and every link that does not end here.
    """
    b = BOXES[page]
    ext, gap = 46.0, 10.0
    tw = F.CHAR_W * F.FONT * len(word)
    content = tw + (tri_w + gap if mark else 0.0)
    w = max(b[2] - b[0], content + 26)
    x = WEB_XY[page][0]
    r = (min(b[0] - 9, x - w / 2), b[1] - 9, max(b[2] + 9, x + w / 2), b[3] + 9)
    r = (r[0], r[1], r[2], r[3] + ext) if up else (r[0], r[1] - ext, r[2], r[3])
    # Keep it on the page: a badge wider than twice the margin has to slide sideways
    # rather than hang off the canvas, where ink simply does not render.
    shift = max(0.0, 10 - r[0]) - max(0.0, r[2] - 1070)
    r = (r[0] + shift, r[1], r[2] + shift, r[3])
    ty = (r[3] - ext / 2) if up else (r[1] + ext / 2)
    assert 6 <= r[0] and r[2] <= 1074 and 6 <= r[1] and r[3] <= INK_H, \
        f"the {word!r} badge on {page} runs off the canvas: {r}"
    for n, bx in BOXES.items():
        if n != page:
            assert not F.boxes_overlap(r, bx), f"the {word!r} badge on {page} hits {n}"
    for (u, v), P in _PATHS.items():
        if page in (u, v):
            continue
        assert not any(F.box_hits_segment(r, P[i], P[i + 1], pad=4)
                       for i in range(len(P) - 1)), \
            f"the {word!r} badge on {page} sits on the {u} -> {v} link"
    out = (f"\\draw[line width=4bp,draw={color},rounded corners=15bp] "
           f"({r[0]:.1f},{r[1]:.1f}) rectangle ({r[2]:.1f},{r[3]:.1f});\n")
    left = (r[0] + r[2]) / 2 - content / 2
    if mark:
        out += tri(left + tri_w / 2, ty, up=up, color=color)
        left += tri_w + gap
    out += F.text(left + tw / 2, ty, word, color=color, anchor="center")
    return out, r


# =============================================================================
# 4. Part 7 -- the web
# =============================================================================
def fig_web_graph():
    """Eight pages, fourteen arrows, and the notation that reads them."""
    assert_web_geometry("web-graph", WEB_XY)
    body = web_body()
    n, _ = note("web-graph", "$A_{ij}=1$: $i \\to j$", NOTE_BR, color=GY, anchor="east")
    body += n
    # The two pages the slide asks the room to find, from the arrows alone.
    assert WEB.out_degree("Links") == 4 and WEB.in_degree("Links") == 0
    assert WEB.out_degree("Home") == 0 and WEB_DANGLING == ["Home"]
    assert sum(WEB.out_degree(p) for p in WEB_NAMES) == 14
    F.emit("web-graph", body, container="full", h=CANVAS_H)


def fig_web_blank():
    """The same web with nothing scored -- the Your-turn slide."""
    assert_web_geometry("web-blank", WEB_XY)
    body = web_body()
    assert_no_digits("web-blank", body)
    F.emit("web-blank", body, container="full", h=CANVAS_H)


def fig_web_hits():
    """Both crowns, two marks, each labelled with the role it means."""
    assert_web_geometry("web-hits", WEB_XY)
    assert WEB_HUB_KING == ["Links"] and WEB_AUT_KING == ["Blog"]
    assert WEB_HUB[WEB_HUB_KING[0]] == max(WEB_HUB.values()) == 1.0
    assert WEB_AUT[WEB_AUT_KING[0]] == max(WEB_AUT.values()) == 1.0
    assert WEB_HUB_KING != WEB_AUT_KING
    body = web_body()
    b1, r1 = badge(WEB_HUB_KING[0], "hub", up=True)
    b2, r2 = badge(WEB_AUT_KING[0], "authority", up=False)
    assert not F.boxes_overlap(r1, r2)
    F.emit("web-hits", body + b1 + b2, container="full", h=CANVAS_H)


def fig_web_pagerank():
    """The web shaded by PageRank: the hub king ranks last."""
    assert_web_geometry("web-pagerank", WEB_XY)
    assert WEB_PR_KING == ["Blog"]
    order = sorted(WEB_NAMES, key=lambda n: -WEB_PR[n])
    assert order.index(WEB_HUB_KING[0]) + 1 == WEB_PR_RANK_OF_LINKS == 8
    body = web_body(scores=WEB_PR)
    x, y = WEB_XY[WEB_PR_KING[0]]
    body += crown_glyph(x, BOXES[WEB_PR_KING[0]][3] + 16)
    rank = f"{WEB_PR_RANK_OF_LINKS}th of {WEB.number_of_nodes()}"
    n1, b1 = note("web-pagerank", f"{WEB_HUB_KING[0]}: {rank}", NOTE_BR,
                  color=A2, anchor="east")
    n2, _ = note("web-pagerank", "darker $=$ more PageRank", (240, 315),
                 color=GY, anchor="west", extra=(b1,))
    F.emit("web-pagerank", body + n1 + n2, container="full", h=CANVAS_H)


def fig_web_dangling():
    """Only the dead end marked. No scores, no crowns -- it is a question slide."""
    assert_web_geometry("web-dangling", WEB_XY)
    marked = list(WEB_DANGLING)
    assert marked == ["Home"] and len(marked) == 1
    assert [p for p in WEB_NAMES if WEB.out_degree(p) == 0] == marked
    body = web_body(ring=marked)
    assert_no_digits("web-dangling", body)
    F.emit("web-dangling", body, container="full", h=CANVAS_H)


def fig_teleport():
    """The walker leaves the dead end by a dashed jump to a page nothing links to."""
    assert_web_geometry("teleport", WEB_XY)
    src, dst = WEB_DANGLING[0], "Forum"
    assert WEB.out_degree(src) == 0 and not WEB.has_edge(src, dst)
    body = web_body(ring=[src])
    # The jump bows below the News box it would otherwise run through.
    p0, p3 = np.array(WEB_XY[src]), np.array(WEB_XY[dst])
    c1, c2 = np.array((996.0, 58.0)), np.array((690.0, 18.0))
    pts = [tuple((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * c1
                 + 3 * (1 - t) * t ** 2 * c2 + t ** 3 * p3) for t in np.linspace(0, 1, 48)]
    for n, bx in BOXES.items():
        if n in (src, dst):
            continue
        assert not any(F.box_hits_segment(_grow(bx, 8), pts[i], pts[i + 1], pad=0)
                       for i in range(len(pts) - 1)), f"the teleport arc crosses {n}"
    body += (f"\\draw[line width=3.6bp,draw={A2},{F.DASH},{ARROW}] ({src}) .. controls "
             f"({c1[0]:.1f},{c1[1]:.1f}) and ({c2[0]:.1f},{c2[1]:.1f}) .. ({dst});\n")
    beta = inspect.signature(pagerank).parameters["beta"].default
    assert 0.0 < beta < 1.0
    txt = f"$\\beta = {dec(beta, 2)}$: jump"
    n1, _ = note("teleport", txt, (240, 315), color=A2, anchor="west")
    F.emit("teleport", body + n1, container="full", h=CANVAS_H)


def fig_ppr():
    """Personalizing the teleport on one page turns the margin round."""
    assert_web_geometry("ppr", WEB_XY)
    assert PPR_FOCUS == "Course"
    assert max(WEB_PR, key=WEB_PR.get) == "Blog"
    assert max(WEB_PPR, key=WEB_PPR.get) == PPR_FOCUS
    g = float(WEB_PR["Blog"] - WEB_PR["Course"])
    f = float(WEB_PPR["Course"] - WEB_PPR["Blog"])
    assert abs(g - PPR_GLOBAL_MARGIN) < 1e-12 and abs(f - PPR_FOCUS_MARGIN) < 1e-12
    assert 0 < g < f
    body = web_body(scores=WEB_PPR, ring=[PPR_FOCUS])
    n1, _ = note("ppr", f"globally: Blog $+{dec(g)}$", (240, 315),
                 color=A2, anchor="west")
    n2, _ = note("ppr", f"on Course: Course $+{dec(f)}$", NOTE_BR,
                 color=A2, anchor="east")
    F.emit("ppr", body + n1 + n2, container="full", h=CANVAS_H)


def fig_next_module():
    """The walker itself, mid-jump: the hand-off to Module 07."""
    assert_web_geometry("next-module", WEB_XY)
    body = web_body()
    here, there = WEB_DANGLING[0], "Forum"
    assert not WEB.has_edge(here, there), "a teleport is not a link"
    x, y = WEB_XY[here]
    body += F.dot(x, y, color=A2, d=26)
    p0, p3 = np.array((x, y)), np.array(WEB_XY[there])
    c1, c2 = np.array((996.0, 58.0)), np.array((690.0, 18.0))
    pts = [tuple((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * c1
                 + 3 * (1 - t) * t ** 2 * c2 + t ** 3 * p3) for t in np.linspace(0, 1, 48)]
    for n, bx in BOXES.items():
        if n in (here, there):
            continue
        assert not any(F.box_hits_segment(_grow(bx, 8), pts[i], pts[i + 1], pad=0)
                       for i in range(len(pts) - 1)), f"the walker's jump crosses {n}"
    body += (f"\\draw[line width=3.6bp,draw={A2},{F.DASH},{ARROW}] ({here}) .. controls "
             f"({c1[0]:.1f},{c1[1]:.1f}) and ({c2[0]:.1f},{c2[1]:.1f}) .. ({there});\n")
    n1, _ = note("next-module", "next: the walker itself", (240, 315),
                 color=A2, anchor="west")
    F.emit("next-module", body + n1, container="full", h=CANVAS_H)


def pagebox(x, y, label, fill="white", text_col="black", name=None):
    """One page box, the same object the web is drawn from."""
    w = F.CHAR_W * F.FONT * len(label) + 26.0
    nm = f"({name})" if name else ""
    return (f"\\node[rectangle,rounded corners=7bp,draw=black,line width=1.8bp,"
            f"fill={fill},text={text_col},minimum width={w:.1f}bp,"
            f"minimum height={BOX_H}bp,inner sep=0pt,"
            f"font=\\fontsize{{{F.FONT}}}{{{int(F.FONT * 1.15)}}}\\selectfont] "
            f"{nm} at ({x:.1f},{y:.1f}) {{{label}}};\n"), (x - w / 2, y - BOX_H / 2,
                                                           x + w / 2, y + BOX_H / 2)


def fig_hub_authority():
    """The two roles as one picture: three arrows out, three arrows in."""
    hub, aut = (120.0, 190.0), (960.0, 190.0)
    outs = [(390.0, 300.0), (400.0, 190.0), (390.0, 80.0)]
    ins = [(690.0, 300.0), (680.0, 190.0), (690.0, 80.0)]
    assert len(outs) + len(ins) + 2 == 8, "eight nodes, like the web"
    body = ""
    for i, p in enumerate(outs + ins):
        body += F.disc(p[0], p[1], name=f"n{i}")
    body += F.disc(*hub, fill=A2, name="H") + F.disc(*aut, fill=A2, name="A")
    for i in range(3):
        body += f"\\draw[ed,{ARROW}] (H) -- (n{i});\n"
        body += f"\\draw[ed,{ARROW}] (n{i + 3}) -- (A);\n"
    body += F.text(255, 40, "hub", color=A2)
    body += F.text(825, 40, "authority", color=A2)
    for e in [(hub, o) for o in outs] + [(i, aut) for i in ins]:
        for lb in ((255, 40, "hub"), (825, 40, "authority")):
            b = F.label_box(lb[0], lb[1], lb[2], "center")
            assert not F.box_hits_segment(b, e[0], e[1], pad=6), \
                f"the word {lb[2]!r} sits on an arrow"
    F.emit("hub-authority", body, container="full", h=CANVAS_H)


def fig_hits_equations():
    """x = A y and y = A^T x, drawn as the two updates they are.

    The convention is the standard one and NOT the lecture note's: verify_numbers
    .hits() records that the note has hubs and authorities swapped.
    """
    body = ""
    src, tgt = (130.0, 210.0), (950.0, 210.0)
    ys = [(390.0, 300.0), (400.0, 210.0), (390.0, 120.0)]
    xs = [(690.0, 300.0), (680.0, 210.0), (690.0, 120.0)]
    body += F.disc(*src, label="$x$", fill=A2, name="S")
    body += F.disc(*tgt, label="$y$", fill=A2, name="T")
    for i, p in enumerate(ys):
        body += F.disc(p[0], p[1], label="$y$", name=f"y{i}")
    for i, p in enumerate(xs):
        body += F.disc(p[0], p[1], label="$x$", name=f"x{i}")
    for i in range(3):
        body += f"\\draw[ed,{ARROW}] (S) -- (y{i});\n"
        body += f"\\draw[ed,{ARROW}] (x{i}) -- (T);\n"
    body += F.text(265, 55, "hub: $x = A\\,y$", color="black")
    body += F.text(795, 55, "authority: $y = A^{\\top} x$", color="black")
    for lb in ((265, 55, "hub: $x = A y$"), (795, 55, "authority: $y = A^{top} x$")):
        b = F.label_box(lb[0], lb[1], lb[2], "center")
        assert 6 <= b[0] and b[2] <= 1074, f"{lb[2]!r} runs off the canvas {b}"
        for e in [(src, y) for y in ys] + [(x, tgt) for x in xs]:
            assert not F.box_hits_segment(b, e[0], e[1], pad=6), f"{lb[2]!r} sits on an arrow"
    F.emit("hits-equations", body, container="full", h=CANVAS_H)


def fig_pagerank_split():
    """One page's score, split equally among its out-links."""
    src = WEB_HUB_KING[0]
    outs = [b for a, b in WEB_LINKS if a == src]
    d = WEB.out_degree(src)
    assert d == len(outs) == 4
    share = [1.0 / d] * d
    assert abs(sum(share) - 1.0) < 1e-12, share
    assert all(abs(s - 1.0 / WEB.out_degree(src)) < 1e-12 for s in share)
    p0 = (110.0, 180.0)
    ys = [300.0, 220.0, 140.0, 60.0]
    body, boxes = "", []
    b, bb = pagebox(*p0, src, name="S")
    body += b
    boxes.append(bb)
    for i, (n, y) in enumerate(zip(outs, ys)):
        b, bb = pagebox(520.0, y, n, name=f"t{i}")
        body += b
        boxes.append(bb)
    for i in range(d):
        body += f"\\draw[ed,{ARROW}] (S) -- (t{i});\n"
    # The fraction rides beside its own arrow, out where the fan has opened.
    chips = []
    for i, y in enumerate(ys):
        t = 0.66
        cx, cy = p0[0] + t * (520.0 - p0[0]), p0[1] + t * (y - p0[1])
        cy += 32 if y > p0[1] else -32
        txt = f"$1/{d}$"
        cb = F.label_box(cx, cy, txt, "center")
        for o in chips + boxes:
            assert not F.boxes_overlap(cb, o), f"the {txt} chip collides at {cb}"
        chips.append(cb)
        body += F.text(cx, cy, txt, color=A2)
    tot = f"${d} \\times 1/{d} = 1$"
    tb = F.label_box(1062, 180, tot, "east")
    for o in chips + boxes:
        assert not F.boxes_overlap(tb, o), "the total collides"
    assert tb[0] >= 6
    body += F.text(1062, 180, tot, color=A2, anchor="east")
    F.emit("pagerank-split", body, container="full", h=CANVAS_H)


# Verified against review/DECK_SPEC.md (slide 74), which lists each with what they
# were ranking: chess tournaments, children's popularity, sociometry, the Web.
GENEALOGY = [(1895, "Landau"), (1949, "Seeley"), (1953, "Katz"),
             (1965, "Hubbell"), (1972, "Bonacich"), (1998, "Brin \\& Page")]
GEN_SPAN = (1890, 2000)


def fig_genealogy():
    """One equation, discovered six times, on a timeline -- never a table."""
    assert [y for y, _ in GENEALOGY] == sorted(y for y, _ in GENEALOGY)
    assert GEN_SPAN[0] < GENEALOGY[0][0] and GENEALOGY[-1][0] < GEN_SPAN[1]
    x0, x1, ax = 150.0, 1000.0, 168.0

    def X(y):
        return x0 + (y - GEN_SPAN[0]) / (GEN_SPAN[1] - GEN_SPAN[0]) * (x1 - x0)

    # Staggered above/below, and nudged along the axis where two labels would
    # touch; the leader line keeps each label tied to its own year.
    place = {1895: (1, 0.0), 1949: (-1, -21.0), 1953: (1, 0.0),
             1965: (-1, 15.0), 1972: (1, 0.0), 1998: (-1, -45.0)}
    body = F.seg((x0, ax), (x1, ax), color="black", w=2.6)
    boxes = {}
    for year, who in GENEALOGY:
        side, dx = place[year]
        mx, lx = X(year), X(year) + dx
        ly = ax + side * 24
        body += F.seg((mx, ax), (mx, ax + side * 13), color="black", w=2.6)
        body += F.dot(mx, ax, color=A2, d=15)
        if abs(dx) > 1:
            body += F.seg((mx, ax + side * 13), (lx, ly), color=GY, w=1.8)
        s = f"{year}\\\\{who}"
        body += F.text(lx, ly, s, color="black",
                       anchor="south" if side > 0 else "north")
        boxes[year] = F.label_box(lx, ly, s, "south" if side > 0 else "north")
    ys = sorted(boxes)
    for i, a in enumerate(ys):
        for b in ys[i + 1:]:
            assert not F.boxes_overlap(boxes[a], boxes[b]), \
                f"the {a} and {b} labels overlap -- stagger them further"
    for b in boxes.values():
        assert 6 <= b[0] and b[2] <= 1074, f"a timeline label runs off the canvas: {b}"
    banner = "one equation, six times: $c = \\lambda A c$"
    bb = F.label_box(540, 312, banner, "center")
    for b in boxes.values():
        assert not F.boxes_overlap(bb, b), "the banner collides with a label"
    assert 6 <= bb[0] and bb[2] <= 1074 and bb[3] <= INK_H
    body += F.text(540, 312, banner, color=A2)
    F.emit("genealogy", body, container="full", h=CANVAS_H)


FIGURES = [
    ("web-graph", fig_web_graph),
    ("web-blank", fig_web_blank),
    ("web-hits", fig_web_hits),
    ("web-pagerank", fig_web_pagerank),
    ("web-dangling", fig_web_dangling),
    ("teleport", fig_teleport),
    ("ppr", fig_ppr),
    ("hub-authority", fig_hub_authority),
    ("hits-equations", fig_hits_equations),
    ("pagerank-split", fig_pagerank_split),
    ("genealogy", fig_genealogy),
    ("next-module", fig_next_module),
]

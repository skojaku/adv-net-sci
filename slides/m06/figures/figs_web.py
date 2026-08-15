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
from figlib import ACCENT          # the hex, for \definecolor; the rest are TikZ names
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

# KNOWN DEFECT, recorded rather than hidden: this layout crosses edges, and the
# underlying undirected graph is planar (twelve pairs; nx.check_planarity says
# yes), so the crossings are avoidable — an F2 Major on the five slides that use
# a web drawing. A crossing-free layout was found by annealing and rejected
# because every in-drawing note and badge in this module is anchored to the
# CURRENT geometry: moving the pages put the "A_ij = 1" note on Forum, the
# authority badge on the Links->Forum link, and the teleport arc through Wiki.
# Fixing it properly means re-placing the notes with the layout, in one pass.
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
NOTE_TC = (240.0, 315.0)                       # top centre, over News -> Blog


# =============================================================================
# 2. Drawing the web
# =============================================================================
def _mix(t, base=tuple(int(ACCENT[i:i + 2], 16) for i in (0, 2, 4))):
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
    n2, _ = note("web-pagerank", "darker $=$ more PageRank", NOTE_TC,
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
    n1, _ = note("teleport", txt, NOTE_TC, color=A2, anchor="west")
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
    n1, _ = note("ppr", f"globally: Blog $+{dec(g)}$", NOTE_TC,
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
    # The walker stands ON the page, not in the middle of its name.
    wx, wy = WEB_XY[here][0] - 14, BOXES[here][3] + 19
    for (u, v), P in _PATHS.items():
        assert not any(F.box_hits_segment((wx - 15, wy - 15, wx + 15, wy + 15),
                                          P[i], P[i + 1], pad=2)
                       for i in range(len(P) - 1)), f"the walker sits on {u} -> {v}"
    body += F.dot(wx, wy, color=A2, d=26)
    p0, p3 = np.array(WEB_XY[here]), np.array(WEB_XY[there])
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
    n1, _ = note("next-module", "next: the walker itself", NOTE_TC,
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
    body += F.text(hub[0], 40, "hub", color=A2)
    body += F.text(aut[0], 40, "authority", color=A2)
    for e in [(hub, o) for o in outs] + [(i, aut) for i in ins]:
        for lb in ((hub[0], 40, "hub"), (aut[0], 40, "authority")):
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
    tx = 620.0
    body, boxes = "", []
    b, bb = pagebox(*p0, src, name="S")
    body += b
    boxes.append(bb)
    for i, (n, y) in enumerate(zip(outs, ys)):
        b, bb = pagebox(tx, y, n, name=f"t{i}")
        body += b
        boxes.append(bb)
    for i in range(d):
        body += f"\\draw[ed,{ARROW}] (S) -- (t{i});\n"
    # The fraction rides ON its own arrow in a white chip, out where the fan has
    # opened: offset beside the line it belongs to, four arrows 58 bp apart, is
    # how m03's edge weights ended up next to the wrong edge.
    chips = []
    for i, y in enumerate(ys):
        t = 0.72
        cx, cy = p0[0] + t * (tx - p0[0]), p0[1] + t * (y - p0[1])
        txt = f"$1/{d}$"
        cb = F.label_box(cx, cy, txt, "center", pad=4)
        for o in chips + boxes:
            assert not F.boxes_overlap(cb, o), f"the {txt} chip collides at {cb}"
        chips.append(cb)
        body += (f"\\node[fill=white,inner sep=4bp,text={A2},"
                 f"font=\\fontsize{{{F.FONT}}}{{{int(F.FONT * 1.15)}}}\\selectfont] "
                 f"at ({cx:.1f},{cy:.1f}) {{{txt}}};\n")
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
    place = {1895: (1, 0.0), 1949: (-1, -30.0), 1953: (1, 0.0),
             1965: (-1, -8.0), 1972: (1, 0.0), 1998: (-1, -45.0)}
    body = F.seg((x0, ax), (x1, ax), color="black", w=2.6)
    boxes = {}
    for year, who in GENEALOGY:
        side, dx = place[year]
        mx, lx = X(year), X(year) + dx
        ly = ax + side * 24
        body += F.dot(mx, ax, color=A2, d=18)
        body += F.seg((mx, ax + side * 9), (lx, ly - side * 2), color=GY, w=1.8)
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


# =============================================================================
# 5. Part 8 -- choosing one
# =============================================================================
SMALL = 30.0                       # disc for the thumbnail networks; 26 rendered
                                   # at 25.6 px and tripped the 26-52 band


def sketch(cx, cy, nodes, edges, key, name, ring_key=True, dashed=()):
    """A thumbnail network, asserted planar as drawn and inside its slot."""
    pos = {i: (cx + x, cy + y) for i, (x, y) in enumerate(nodes)}
    F.assert_planar_drawing(edges, pos, name)
    for i, p in pos.items():
        for j, q in pos.items():
            assert i >= j or math.dist(p, q) > SMALL + 4, f"{name}: nodes {i},{j} touch"
    out = "".join(F.seg(pos[a], pos[b], color="black", w=2.2) for a, b in edges)
    out += "".join(F.seg(pos[a], pos[b], color=A2, w=2.6, dash=F.DASH) for a, b in dashed)
    out += "".join(F.disc(x, y, size=SMALL) for x, y in pos.values())
    if ring_key:
        out += F.mark(*pos[key], color=A2, size=SMALL, w=3.4)
    bb = (min(x for x, _ in pos.values()) - SMALL / 2 - 8,
          min(y for _, y in pos.values()) - SMALL / 2 - 8,
          max(x for x, _ in pos.values()) + SMALL / 2 + 8,
          max(y for _, y in pos.values()) + SMALL / 2 + 8)
    return out, bb


# purpose -> the metrics that answer it. The five pairings of DECK_SPEC slide 85,
# each drawn as its own thumbnail so the slide cannot read as a table.
PURPOSE = [
    dict(sx=70, sy=250, tx=140, anchor="west", purpose="popular", metric="degree",
         nodes=[(0, 0), (38, 0), (12, 36), (-31, 22), (-31, -22), (12, -36)],
         edges=[(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)], key=0),
    dict(sx=372, sy=250, tx=442, anchor="west", purpose="efficient",
         metric="closeness\\\\harmonic",
         nodes=[(-42, -32), (-21, -5), (0, 22), (21, -5), (42, -32)],
         edges=[(0, 1), (1, 2), (2, 3), (3, 4)], key=2),
    dict(sx=966, sy=250, tx=900, anchor="east", purpose="critical",
         metric="betweenness\\\\eccentricity",
         nodes=[(-40, 24), (-40, -24), (0, 0), (40, 24), (40, -24)],
         edges=[(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4)], key=2),
    dict(sx=175, sy=100, tx=250, anchor="west", purpose="influential",
         metric="eigenvector,\\\\Katz, PageRank",
         nodes=[(20, 28), (20, -28), (48, 0), (-18, 0), (-46, 30)],
         edges=[(0, 1), (0, 2), (1, 2), (3, 0), (3, 1), (4, 3)], key=0),
    dict(sx=966, sy=100, tx=900, anchor="east", purpose="personalized",
         metric="personalized\\\\PageRank",
         nodes=[(-38, 0), (0, 28), (0, -28), (38, 24), (38, -24)],
         edges=[(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)], key=0,
         dashed=[(4, 0)]),
]


def _purpose_boxes():
    out = []
    for i, it in enumerate(PURPOSE):
        pb = F.label_box(it["tx"], it["sy"] + 50, it["purpose"], it["anchor"])
        mb = F.label_box(it["tx"], it["sy"] - 26, it["metric"], it["anchor"])
        assert not F.boxes_overlap(pb, mb), f"purpose-{i + 1}: the two lines overlap"
        out.append((i, pb, mb))
    return out


def fig_purpose(step):
    """One purpose, one metric, one thumbnail -- revealed one at a time."""
    body = ""
    slots = []
    for i, it in enumerate(PURPOSE):
        ink, bb = sketch(it["sx"], it["sy"], it["nodes"], it["edges"], it["key"],
                         f"purpose-{i + 1}", ring_key=(i < step),
                         dashed=it.get("dashed", ()) if i < step else ())
        body += ink
        slots.append(bb)
    boxes = _purpose_boxes()
    for i, pb, mb in boxes:
        for j, qb, nb in boxes:
            if i < j:
                assert not (F.boxes_overlap(pb, qb) or F.boxes_overlap(mb, nb)
                            or F.boxes_overlap(pb, nb) or F.boxes_overlap(mb, qb)), \
                    f"the purpose-{i + 1} and purpose-{j + 1} captions overlap"
        for b in (pb, mb):
            assert 6 <= b[0] and b[2] <= 1074 and 6 <= b[1] and b[3] <= INK_H, \
                f"the purpose-{i + 1} caption runs off the canvas: {b}"
            for j, sb in enumerate(slots):
                assert not F.boxes_overlap(b, sb), \
                    f"the purpose-{i + 1} caption lands on thumbnail {j + 1}"
    for i, it in enumerate(PURPOSE[:step]):
        body += F.text(it["tx"], it["sy"] + 50, it["purpose"], color="black",
                       anchor=it["anchor"])
        body += F.text(it["tx"], it["sy"] - 26, it["metric"], color=A2,
                       anchor=it["anchor"])
    F.emit(f"purpose-{step}", body, container="full", h=CANVAS_H)


# crown_robustness() enumerates 4992 map variants and takes about a minute, so the
# figure quotes the numbers and re-derives them only when asked. Set M06_FULL_CHECK=1
# to make the build call it and check every row against this table.
ROBUST_N = 4992
ROBUST = [("degree", 1.000), ("closeness", 0.962), ("harmonic", 0.962),
          ("betweenness", 0.936), ("katz", 0.852), ("eccentricity", 0.846),
          ("eigenvector", 0.792)]
ROBUST_MARK = ("degree", "eigenvector")           # the two the slide names out loud


def _robust_full_check():
    ex, keeps = crown_robustness()
    assert ex == ROBUST_N, f"{ex} variants, not {ROBUST_N}"
    for m, v in ROBUST:
        got = keeps[m] / ex
        assert abs(got - v) < 5e-4, f"{m}: {got:.4f} computed against {v} quoted"
    return ex, keeps


def fig_robustness():
    """How much of 'who is most important' survives redrawing the map."""
    if os.environ.get("M06_FULL_CHECK"):
        _robust_full_check()
    assert dict(ROBUST)["degree"] == 1.0 > dict(ROBUST)["eigenvector"] == 0.792
    assert [m for m, _ in ROBUST] == sorted([m for m, _ in ROBUST],
                                            key=lambda m: -dict(ROBUST)[m])
    x0, x1, ay = 410.0, 930.0, 62.0
    top = 100.0 + (len(ROBUST) - 1) * 38.0
    body = F.seg((x0, ay), (x1, ay), color="black", w=2.2)
    # Gridlines, not bars: the dot's place on the axis carries the number, and a
    # leader from the axis to each dot would be a bar chart with a thin bar.
    for v in (0.0, 0.5, 1.0):
        x = x0 + v * (x1 - x0)
        body += F.seg((x, ay), (x, top + 20), color=GY, w=1.2, dash=F.DASH)
        body += F.seg((x, ay), (x, ay - 9), color="black", w=2.2)
        body += F.text(x, ay - 17, F.pct(v), color=GY, anchor="north")
    rows, boxes = [], []
    for i, (m, v) in enumerate(ROBUST):
        y = 100.0 + (len(ROBUST) - 1 - i) * 38.0
        hot = m in ROBUST_MARK
        col = A2 if hot else "black"
        label = m.capitalize() if m == "katz" else m
        body += F.text(350, y, label, color=col, anchor="east")
        boxes.append(F.label_box(350, y, label, "east"))
        body += F.dot(x0 + v * (x1 - x0), y, color=A2 if hot else A1, d=20)
        if hot:
            s = F.pct(v, 1) if v < 1 else F.pct(v)
            body += F.text(x0 + v * (x1 - x0) + 16, y, s, color=A2, anchor="west")
            boxes.append(F.label_box(x0 + v * (x1 - x0) + 16, y, s, "west"))
        rows.append(y)
    cap = f"{ROBUST_N} maps"
    cb = F.label_box(350, ay - 17, cap, "east")
    for b in boxes:
        assert not F.boxes_overlap(cb, b), "the caption collides with a row"
    assert 6 <= cb[0] and cb[2] <= 1074 and 6 <= cb[1] and cb[3] <= INK_H
    n = F.text(350, ay - 17, cap, color=GY, anchor="east")
    for b in boxes:
        assert 6 <= b[0] and b[2] <= 1074, f"a row label runs off the canvas: {b}"
    F.emit("robustness", body + n, container="full", h=CANVAS_H)


def fig_cost():
    """Cost against n: one sweep per node, against one product per step."""
    assert COST_M == 10 * COST_N, (COST_N, COST_M)
    assert COST_SWEEP == COST_N * COST_M and COST_ITER == 30 * COST_M
    assert COST_RATIO == COST_SWEEP // COST_ITER == 33333, COST_RATIO
    ax = F.Axes((300, 110, 1020, 285), (1e2, 1e7), (1e4, 1e16), xlog=True, ylog=True,
                xlabel="$n$ nodes, $m = 10n$", ylabel="",
                yticks=[1e5, 1e10, 1e15])
    body = ax.frame()
    body += F.text(170, (110 + 285) / 2, "operations", anchor="south", rot=90)
    ns = np.logspace(2, 7, 60)
    body += ax.line(ns, ns * (10 * ns), color=A2, w=3.6)
    body += ax.line(ns, 30 * (10 * ns), color=A1, w=3.6)
    for y, c in ((COST_SWEEP, A2), (COST_ITER, A1)):
        body += F.dot(*ax.P(COST_N, y), color=c, d=20)
    p1, p2 = ax.P(COST_N, COST_SWEEP), ax.P(COST_N, COST_ITER)
    body += F.seg(p1, p2, color=GY, w=2.0, arrow="{Stealth[length=9bp]}-"
                                                 "{Stealth[length=9bp]}")
    body += F.text(p1[0] + 18, (p1[1] + p2[1]) / 2, f"${COST_RATIO:,}".replace(",", "{,}")
                   + "\\times$", color=GY, anchor="west")
    body += F.text(300, 315, "closeness: $n\\,m$", color=A2, anchor="west")
    body += F.text(700, 315, "PageRank: $30\\,m$", color=A1, anchor="west")
    F.emit("cost", body, container="full", h=CANVAS_H)


APPLICATIONS = [
    dict(name="applications-1", purpose="vaccination targets", metric="degree",
         nodes=[(215, 220), (310, 220), (263, 302), (168, 302), (120, 220),
                (168, 138), (263, 138),
                (865, 220), (960, 220), (894, 310), (788, 251), (788, 189),
                (894, 130)],
         edges=[(0, i) for i in range(1, 7)] + [(7, i) for i in range(8, 13)]
               + [(1, 11)],
         targets=[0, 7]),
    dict(name="applications-2", purpose="infrastructure defence", metric="betweenness",
         nodes=[(70, 150), (70, 270), (170, 210),
                (340, 210),
                (510, 210), (610, 150), (610, 270),
                (700, 210),
                (810, 210), (910, 150), (910, 270)],
         edges=[(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6),
                (5, 7), (6, 7), (7, 8), (8, 9), (8, 10), (9, 10)],
         targets=[3, 7]),
    dict(name="applications-3", purpose="financial contagion",
         metric="eigenvector, PageRank",
         nodes=[(470, 160), (610, 160), (540, 270), (540, 202),
                (300, 110), (300, 270), (110, 190),
                (780, 110), (780, 270), (970, 190)],
         edges=[(0, 1), (0, 2), (1, 2), (3, 0), (3, 1), (3, 2),
                (4, 0), (5, 2), (6, 4), (6, 5), (7, 1), (8, 2), (9, 7), (9, 8)],
         targets=[0, 1, 2, 3]),
]


def fig_application(i):
    """One network, the nodes the metric names, and the metric."""
    it = APPLICATIONS[i]
    pos = {j: p for j, p in enumerate(it["nodes"])}
    F.assert_planar_drawing(it["edges"], pos, it["name"])
    body = "".join(F.seg(pos[a], pos[b], color="black") for a, b in it["edges"])
    body += "".join(F.disc(x, y) for x, y in pos.values())
    for t in it["targets"]:
        body += F.mark(*pos[t], color=A2)
    pb = F.label_box(540, 96, it["purpose"], "north")
    mb = F.label_box(540, 96 - 40, it["metric"], "north")
    for b in (pb, mb):
        assert 6 <= b[0] and b[2] <= 1074 and 6 <= b[1], f"{it['name']}: caption {b}"
        for x, y in pos.values():
            assert not F.box_hits_disc(b, x, y, r=F.NODE / 2 + 14), \
                f"{it['name']}: the caption lands on a node"
        for a, c in it["edges"]:
            assert not F.box_hits_segment(b, pos[a], pos[c], pad=6), \
                f"{it['name']}: the caption lands on an edge"
    body += F.text(540, 96, it["purpose"], color="black", anchor="north")
    body += F.text(540, 56, it["metric"], color=A2, anchor="north")
    F.emit(it["name"], body, container="full", h=CANVAS_H)


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
] + [(f"purpose-{k}", functools.partial(fig_purpose, k)) for k in range(1, 6)] + [
    ("robustness", fig_robustness),
    ("cost", fig_cost),
] + [(a["name"], functools.partial(fig_application, i))
     for i, a in enumerate(APPLICATIONS)] + [
    ("next-module", fig_next_module),
]

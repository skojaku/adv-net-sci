#!/usr/bin/env python3
"""Generate every Module 03 slide figure.

Pipeline (see review/FIGURE_SPEC.md for the derivation):

    TikZ body  ->  pdflatex (page fixed to the design canvas)  ->  pdftoppm -r 288

Author at final size: **1 bp = 1 slide pixel**.  The page is pinned to the design
canvas, so the deck's own scale factor is a constant per container:

    cols column : 537 / 520  = 1.033 slide px per bp
    full width  : 1120 / 1100 = 1.018 slide px per bp

Only the *height* is cropped after rasterising (to the ink, plus a pad), which leaves
the width -- and therefore the scale -- untouched.

Everything a figure prints is computed here and cross-checked against the verified
table in review/DECK_SPEC.md.  Nothing is typed in twice.

    python3 figures/make_figures.py            # all figures
    python3 figures/make_figures.py kruskal    # only figures whose name contains "kruskal"
"""

import itertools
import math
import re
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

import networkx as nx
import numpy as np
from PIL import Image

OUT = Path(__file__).resolve().parent

# --------------------------------------------------------------------------- palette
ACCENT = "3959A6"     # the object under discussion
ACCENT2 = "B14434"    # what THIS slide is about
ACCENT3 = "DAB167"    # the secondary / comparison object
GRAY = "6b6b6b"       # annotation only

# --------------------------------------------------------------------------- geometry
DPI = 288
PXBP = DPI / 72              # 4 px per bp
COL_W, FULL_W = 537, 1120    # containers, measured in a real browser render
MAX_FIG_H = 380              # network-science.css: section .fig img { max-height }

DESIGN = {"col": 520, "full": 1100}
CONTAINER = {"col": COL_W, "full": FULL_W}

NODE = 40          # disc diameter, bp  -> 40.7-41.3 px on the slide (band 26-52)
SMALLNODE = 26     # only where a figure draws dozens of dots
DOT = 14

# Type size. The gate that matters is `check_render.py`'s, and it measures
# **x-height** on the rendered slide, not cap height. Asserting cap height here
# let 30pt Latin Modern pass the generator at 21px cap while landing 13px
# x-height on the slide -- under the 15px floor, on 40 figures at once. Latin
# Modern Roman: x-height 0.431 em, cap height 0.683 em. So the generator now
# asserts the same quantity the checker reads.
FONT = 36          # pt; x-height ~= 15.8 px on the slide
XHEIGHT_RATIO = 0.431
EDGE_W = 2.6
HEAVY_W = 5.0
PAD = 12           # bp of white kept around the ink when the height is cropped

NODE_MIN_PX, NODE_MAX_PX = 26, 52
TEXT_MIN_PX = 15.5      # x-height on the slide; check_render.py fails below 15
INK_FILL_MIN = 0.76          # ink must span this share of the canvas width

# A label's bounding box, estimated for the collision assertion.  The deck's serif
# averages ~0.55 em per character at these sizes; measured against the rendered PNGs
# it over-estimates slightly, which is the safe direction for a collision test.
CHAR_W = 0.55
LINE_H = 1.05

_only = sys.argv[1:]
_built = []


# --------------------------------------------------------------------------- TeX
PREAMBLE = r"""
\documentclass{article}
\usepackage[paperwidth=%(W)dbp,paperheight=%(H)dbp,margin=0bp]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{tikz}
\usepackage{amsmath}
\usetikzlibrary{calc,positioning,arrows.meta,decorations.pathmorphing,decorations.markings,
                backgrounds,fit,shapes.geometric,patterns}
\definecolor{accent}{HTML}{%(ACCENT)s}
\definecolor{accenttwo}{HTML}{%(ACCENT2)s}
\definecolor{accentthree}{HTML}{%(ACCENT3)s}
\definecolor{annot}{HTML}{%(GRAY)s}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\begin{document}%%
\vbox to \paperheight{\vss\hbox to \paperwidth{\hss%%
\begin{tikzpicture}[x=1bp,y=1bp,
    every node/.style={inner sep=0pt,outer sep=0pt},
    disc/.style={circle,draw=none,minimum size=%(NODE)dbp,inner sep=0pt,
                 text=white,font=\fontsize{%(FONT)d}{%(FONT)d}\selectfont},
    lab/.style={font=\fontsize{%(FONT)d}{%(LEAD)d}\selectfont,align=center},
    ed/.style={line width=%(EDGE)sbp,draw=black},
]
\useasboundingbox (0,0) rectangle (%(W)d,%(H)d);
"""

POSTAMBLE = r"""
\end{tikzpicture}%
\hss}\vss}%
\end{document}
"""


def _tex(body, w, h):
    head = PREAMBLE % dict(W=w, H=h, ACCENT=ACCENT, ACCENT2=ACCENT2, ACCENT3=ACCENT3,
                           GRAY=GRAY, NODE=NODE, FONT=FONT, LEAD=int(FONT * 1.15),
                           EDGE=EDGE_W)
    return head + body + POSTAMBLE


def render(body, w, h):
    """Compile one TikZ body and return the RGB image, uncropped."""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "f.tex").write_text(_tex(body, w, h))
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "f.tex"],
                           cwd=td, capture_output=True, text=True)
        if r.returncode:
            tail = "\n".join(r.stdout.splitlines()[-25:])
            raise SystemExit(f"pdflatex failed\n{tail}")
        subprocess.run(["pdftoppm", "-png", "-r", str(DPI), "-singlefile", "f.pdf", "f"],
                       cwd=td, check=True)
        im = Image.open(td / "f.png").convert("RGB")
        im.load()
    return im


def crop_and_check(name, im, container):
    """Crop the height to the ink and assert what lands on the slide."""
    w = DESIGN[container]
    a = np.array(im.convert("L"))
    exp = (int(round(w * PXBP)), a.shape[0])
    assert im.size == exp, f"{name}: page is {im.size}, expected width {exp[0]}"

    ys, xs = np.where(a < 200)
    assert len(ys), f"{name}: blank figure"
    edge = 2
    touched = [side for side, hit in (
        ("left", xs.min() <= edge), ("right", xs.max() >= a.shape[1] - 1 - edge),
        ("top", ys.min() <= edge), ("bottom", ys.max() >= a.shape[0] - 1 - edge)) if hit]
    assert not touched, (
        f"{name}: ink runs off the {', '.join(touched)} edge of the page -- the "
        f"drawing is being CLIPPED, not cropped. Move it inward or grow the canvas.")
    lo = max(0, ys.min() - int(PAD * PXBP))
    hi = min(a.shape[0], ys.max() + int(PAD * PXBP))
    im = im.crop((0, lo, im.size[0], hi))

    fw, fh = im.size
    scale = min(CONTAINER[container] / fw, MAX_FIG_H / fh, 1.0)
    factor = scale * PXBP                      # slide px per bp
    want = CONTAINER[container] / w
    assert abs(factor - want) < 1e-6, (
        f"{name}: height binds the scale ({fh/PXBP:.0f}bp tall on a {w}bp canvas) -- "
        f"the drawing must be shorter than {w * MAX_FIG_H / CONTAINER[container]:.0f}bp")

    span = (xs.max() - xs.min() + 1) / fw
    assert span >= INK_FILL_MIN, (
        f"{name}: ink spans {span:.0%} of the canvas width (need {INK_FILL_MIN:.0%}) -- "
        f"widen the drawing, do not shrink the canvas")

    node_px = NODE * factor
    assert NODE_MIN_PX <= node_px <= NODE_MAX_PX, f"{name}: node disc {node_px:.0f}px"
    x_px = FONT * XHEIGHT_RATIO * factor
    assert x_px >= TEXT_MIN_PX, f"{name}: text x-height {x_px:.1f}px on the slide"
    return im, fw, fh, node_px, x_px, span


def emit(name, body, container="col", h=None):
    if _only and not any(k in name for k in _only):
        return
    w = DESIGN[container]
    hmax = h or int(w * 0.70)
    im = render(body, w, hmax)
    im, fw, fh, node_px, cap_px, span = crop_and_check(name, im, container)
    im.save(OUT / f"{name}.png")
    _built.append(name)
    print(f"  {name}.png  {fw}x{fh}  node {node_px:.0f}px  x-h {cap_px:.1f}px  "
          f"ink {span:.0%}")


# --------------------------------------------------------------------------- drawing
def disc(x, y, label="", fill="accent", name=None, size=NODE, text_col="white"):
    nm = f"({name})" if name else ""
    opt = f"disc,fill={fill},minimum size={size}bp"
    if text_col != "white":
        opt += f",text={text_col}"
    return f"\\node[{opt}] {nm} at ({x},{y}) {{{label}}};\n"


def opendisc(x, y, color="accenttwo", size=NODE, w=4.0):
    return (f"\\draw[line width={w}bp,draw={color},fill=white] ({x},{y}) "
            f"circle ({size / 2}bp);\n")


def ring(x, y, size=NODE, color="accenttwo", w=4.0, grow=11):
    return (f"\\draw[line width={w}bp,draw={color}] ({x},{y}) "
            f"circle ({(size + grow) / 2}bp);\n")


def dot(x, y, color="accent", d=DOT):
    return f"\\fill[{color}] ({x},{y}) circle ({d / 2}bp);\n"


def square(x, y, label="", fill="accenttwo", size=SMALLNODE + 8, text_col="white"):
    """A SQUARE marker. Circles are graph nodes and nothing else.

    Step badges were drawn as accent-2 discs, which is the same shape as a node --
    so on the slide that counts cables, seven of the marks the room had just
    learned to read as towns were not towns. Squares say "annotation" at a glance,
    and the render gate's corner test excludes them from the node-size band too.
    """
    h = size / 2
    s = (f"\\fill[{fill}] ({x - h:.1f},{y - h:.1f}) rectangle "
         f"({x + h:.1f},{y + h:.1f});\n")
    if label:
        s += (f"\\node[font=\\fontsize{{{FONT}}}{{{FONT}}}\\selectfont,"
              f"text={text_col},anchor=center] at ({x:.1f},{y:.1f}) {{{label}}};\n")
    return s


def seg(p, q, color="black", w=EDGE_W, dash="", arrow="", opacity=None):
    o = [f"line width={w}bp", f"draw={color}"]
    if dash:
        o.append(dash)
    if arrow:
        o.append(arrow)
    if opacity is not None:
        o.append(f"opacity={opacity}")
    return f"\\draw[{','.join(o)}] ({p[0]:.1f},{p[1]:.1f}) -- ({q[0]:.1f},{q[1]:.1f});\n"


def polyline(pts, color="accent", w=3.4, dash=""):
    o = [f"line width={w}bp", f"draw={color}"]
    if dash:
        o.append(dash)
    return "\\draw[%s] %s;\n" % (",".join(o),
                                 " -- ".join("(%.1f,%.1f)" % p for p in pts))


DASH = "dash pattern=on 7bp off 6bp"
DASH_LONG = "dash pattern=on 12bp off 8bp"

_fontsizes = set()


def text(x, y, s, color="black", anchor="center", size=FONT, width=None, rot=None):
    _fontsizes.add(size)
    assert size >= FONT, f"font {size}pt is below the {FONT}pt floor"
    # A bare % is a TeX comment: it swallowed the rest of a \node line and the
    # build died with "Undefined control sequence" pointing at the wrong token.
    assert not re.search(r"(?<!\\)%", s), f"unescaped % in {s!r} -- write \\%"
    # accent-3 on white is 2.0:1 contrast -- fine for a 4bp stroke, unreadable as
    # type. It is a stroke colour only.
    assert color != "accentthree", "accent-3 is not a text colour (2.0:1 on white)"
    o = [f"font=\\fontsize{{{size}}}{{{int(size * 1.15)}}}\\selectfont",
         f"text={color}", f"anchor={anchor}", "align=center"]
    if width:
        o.append(f"text width={width}bp")
    if rot is not None:
        o.append(f"rotate={rot}")
    return f"\\node[{','.join(o)}] at ({x:.1f},{y:.1f}) {{{s}}};\n"


def pct(x, d=0):
    """A percentage with the % escaped -- a bare % is a TeX comment.

    Rounds half UP. With %.0f the measured 0.575 printed "57" (the float is
    57.4999...) while the deck's prose said 58, so one slide carried both numbers.
    """
    from decimal import Decimal, ROUND_HALF_UP
    # Decimal(str(x * 100)) is not enough: 0.575 * 100 is 57.49999999999999 in
    # binary, so half-up still gave 57 while the deck's prose said 58. repr(x)
    # is the shortest string that round-trips -- "0.575" -- so the multiply
    # happens in decimal and the rounding sees the value the author meant.
    q = (Decimal(repr(float(x))) * 100).quantize(
        Decimal("1") if d == 0 else Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{q}\\%"


def clearance_bad(edges, pos, r=NODE / 2 + 3):
    """No straight edge may pass through a disc it does not end at."""
    bad = []
    for a, b in edges:
        pa, pb = np.array(pos[a], float), np.array(pos[b], float)
        d = pb - pa
        L2 = float(d @ d)
        for n, p in pos.items():
            if n in (a, b):
                continue
            p = np.array(p, float)
            t = max(0.0, min(1.0, float((p - pa) @ d) / L2))
            if np.linalg.norm(pa + t * d - p) < r:
                bad.append((a, b, n))
    return bad


def _seg_cross(p1, p2, p3, p4):
    def o(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2, d3, d4 = o(p3, p4, p1), o(p3, p4, p2), o(p1, p2, p3), o(p1, p2, p4)
    return ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0))


def crossings(edges, pos):
    """F2 as a build gate: every pair of non-adjacent edges must not cross."""
    bad = []
    for (a, b), (c, d) in itertools.combinations(edges, 2):
        if len({a, b, c, d}) < 4:
            continue
        if _seg_cross(pos[a], pos[b], pos[c], pos[d]):
            bad.append(((a, b), (c, d)))
    return bad


def label_box(x, y, s, anchor, size=FONT, pad=6):
    """Approximate bounding box of a text node, for the collision assertion."""
    w = CHAR_W * size * max(len(line) for line in s.split("\\\\")) + 2 * pad
    h = LINE_H * size * len(s.split("\\\\")) + 2 * pad
    ax = {"center": 0.0, "west": 0.5, "east": -0.5,
          "north": 0.0, "south": 0.0,
          "north west": 0.5, "north east": -0.5,
          "south west": 0.5, "south east": -0.5}[anchor]
    ay = {"center": 0.0, "west": 0.0, "east": 0.0,
          "north": -0.5, "south": 0.5,
          "north west": -0.5, "north east": -0.5,
          "south west": 0.5, "south east": 0.5}[anchor]
    cx, cy = x + ax * w, y + ay * h
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


def boxes_overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def box_hits_disc(b, x, y, r=NODE / 2):
    d = (max(b[0] - x, 0, x - b[2]), max(b[1] - y, 0, y - b[3]))
    return math.hypot(*d) < r


def box_hits_segment(b, p, q, pad=4):
    """Does the segment p--q enter the (padded) box?  Liang-Barsky clip."""
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


# Candidate sides for a town name, best first.  The placement solver below tries
# them in order; hand-assigning these was tried and cost an afternoon of nudging
# on a graph where two towns sit 17 km apart.
SIDES = [
    # (TikZ anchor, dx, dy).  The anchor names the side of the *text box* that sits
    # at the point, so a label placed to the LEFT of a node anchors "east" at a
    # point to its left.  Getting this pairing backwards put every label on top of
    # its own disc, and the collision test did not catch it because it exempted a
    # label's own node -- it no longer does.
    ("east", -26, 0),          # label left of the node
    ("west", 26, 0),           # label right of the node
    ("south", 0, 26),          # label above the node
    ("north", 0, -26),         # label below the node
    ("south east", -20, 20), ("south west", 20, 20),
    ("north east", -20, -20), ("north west", 20, -20),
    # further-out variants, tried only when every close side is blocked
    ("east", -44, 0), ("west", 44, 0), ("south", 0, 46), ("north", 0, -46),
    ("south east", -34, 34), ("south west", 34, 34),
    ("north east", -34, -34), ("north west", 34, -34),
    # Last resort: park the name well clear of the drawing and run a thin gray
    # leader back to its node.  This exists because requiring every one of the
    # thirteen cables to be clear of every name has no side-only solution -- and
    # the alternative the solver refuses to take is shrinking the type.
    ("east", -96, 0), ("west", 96, 0), ("south", 0, 92), ("north", 0, -92),
    ("south east", -74, 74), ("south west", 74, 74),
    ("north east", -74, -74), ("north west", 74, -74),
]

# Beyond this offset the name is too far from its node to read as its label, so
# the drawing routine runs a leader line to it.
LEADER_AT = 60


def place_labels(names, pos, edges, blockers=(), bounds=None, gap=0.0):
    """Choose a side per label so that nothing collides.  Returns {name: (anchor, dx, dy)}.

    Checked against: every other label, every disc that is not the label's own,
    every drawn edge, any extra blocker boxes (edge-weight chips), and the canvas
    bounds.  Backtracking, best side first, so the usual answer is also the tidy one.
    """
    order = sorted(names, key=lambda n: -len(names[n]))
    chosen, boxes = {}, {}

    def ok(n, side):
        anc, dx, dy = side
        b = label_box(pos[n][0] + dx, pos[n][1] + dy, names[n], anc)
        b = (b[0] - gap, b[1] - gap, b[2] + gap, b[3] + gap)
        if bounds and not (bounds[0] <= b[0] and b[2] <= bounds[2]
                           and bounds[1] <= b[1] and b[3] <= bounds[3]):
            return None
        for m, (x, y) in pos.items():
            if box_hits_disc(b, x, y):
                return None
        for other in boxes.values():
            if boxes_overlap(b, other):
                return None
        for blk in blockers:
            if boxes_overlap(b, blk):
                return None
        for a, c in edges:
            if box_hits_segment(b, pos[a], pos[c]):
                return None
        return b

    def solve(i):
        if i == len(order):
            return True
        n = order[i]
        for side in SIDES:
            b = ok(n, side)
            if b is None:
                continue
            chosen[n], boxes[n] = side, b
            if solve(i + 1):
                return True
            del chosen[n], boxes[n]
        return False

    if not solve(0):
        # Which name is impossible *on its own* is the only useful thing to say:
        # a solver that just reports failure sends you node-hunting at random.
        chosen.clear()
        boxes.clear()
        free = {n: sum(1 for s in SIDES if ok(n, s)) for n in order}
        raise SystemExit(
            "label placement failed — no collision-free side assignment exists.\n"
            + "\n".join(f"  {n:<10} {c} free side(s)" for n, c in sorted(free.items()))
            + "\nMove a node, shorten a name, or widen the canvas; "
              "do not shrink the type.")
    return chosen, boxes


# Where a weight chip may sit on its edge: a fraction along it, plus a perpendicular
# offset.  Chips left at the plain midpoint collided with each other wherever two
# edges converged on the same node -- "49" and "51" overlapped on the first render.
# Where a weight chip may sit on its edge: a fraction along it, plus a perpendicular
# offset. Ordered nearest-the-edge first, because a chip must end up closer to the
# cable it names than to any other (see place_chips) -- large offsets are a last
# resort, and it was the large offsets that put "17" on the wrong cable.
CHIP_SLOTS = [(t, off)
              for off in (0, 11, -11, 17, -17, 23, -23, 30, -30)
              for t in (0.50, 0.45, 0.55, 0.40, 0.60, 0.35, 0.65, 0.30, 0.70,
                        0.25, 0.75, 0.20, 0.80)]

# Tried only when no in-place slot leaves the chip nearest its own cable. Prostejov
# -- Olomouc is 59bp long and 40bp of that is inside its two discs, so it is
# geometrically impossible to label it unambiguously in place: the chip is parked
# clear and a leader line says which cable it belongs to.
CHIP_LEADER_SLOTS = [(t, off) for off in (44, -44, 56, -56, 70, -70)
                     for t in (0.50, 0.40, 0.60, 0.30, 0.70)]


def point_seg_dist(pt, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    if L2 == 0:
        return math.dist(pt, a)
    t = max(0.0, min(1.0, ((pt[0] - ax) * dx + (pt[1] - ay) * dy) / L2))
    return math.dist(pt, (ax + t * dx, ay + t * dy))


def place_chips(weights, pos, blockers=(), edges=None, margin=8.0):
    """Choose a spot per edge-weight chip so no two chips (or a chip and a name) touch.

    A chip must also be **nearest the cable it names**.  Without that rule the
    perpendicular offsets (up to +-52bp) put "17" 4px from Prostejov-Zlin and 36px
    from its own Prostejov-Olomouc, so the picture priced the wrong cable -- on the
    two slides that ask students to add the kilometres up, and in both GIFs.
    """
    items = sorted(weights, key=lambda e: math.dist(pos[e[0]], pos[e[1]]))
    chosen, boxes = {}, {}

    def slot_box(e, t, off):
        (x1, y1), (x2, y2) = pos[e[0]], pos[e[1]]
        L = math.hypot(x2 - x1, y2 - y1)
        px, py = -(y2 - y1) / L, (x2 - x1) / L
        x = x1 + t * (x2 - x1) + off * px
        y = y1 + t * (y2 - y1) + off * py
        return (x, y), label_box(x, y, str(weights[e]), "center", pad=5)

    others = list(edges if edges is not None else weights)

    def owns(e, pt):
        mine = point_seg_dist(pt, pos[e[0]], pos[e[1]])
        for f in others:
            if frozenset(f) == frozenset(e):
                continue
            if point_seg_dist(pt, pos[f[0]], pos[f[1]]) <= mine + margin:
                return False
        return True

    def free(e, p, b):
        if any(box_hits_disc(b, x, y) for x, y in pos.values()):
            return False
        if any(boxes_overlap(b, o) for o in boxes.values()):
            return False
        return not any(boxes_overlap(b, o) for o in blockers)

    def solve(i):
        if i == len(items):
            return True
        e = items[i]
        for t, off in CHIP_SLOTS:
            p, b = slot_box(e, t, off)
            if owns(e, p) and free(e, p, b):
                chosen[e], boxes[e] = (p, False), b
                if solve(i + 1):
                    return True
                del chosen[e], boxes[e]
        # No in-place slot keeps this chip nearest its own cable: park it and lead.
        for t, off in CHIP_LEADER_SLOTS:
            p, b = slot_box(e, t, off)
            if free(e, p, b):
                chosen[e], boxes[e] = (p, True), b
                if solve(i + 1):
                    return True
                del chosen[e], boxes[e]
        return False

    if not solve(0):
        raise SystemExit("weight-chip placement failed — no collision-free layout exists.")
    return chosen


# ===========================================================================
#                        the Moravian working graph
# ===========================================================================
# Eight real towns at their true relative positions (lat/lon projected to km about
# the centroid).  Weights are the true inter-town distances, rounded and nudged to
# thirteen DISTINCT integers so the MST is unique.

TOWNS_LATLON = {
    "Znojmo": (48.8555, 16.0488), "Trebic": (49.2149, 15.8815),
    "Jihlava": (49.3961, 15.5912), "Brno": (49.1951, 16.6068),
    "Hodonin": (48.8489, 17.1327), "Zlin": (49.2265, 17.6683),
    "Prostejov": (49.4720, 17.1118), "Olomouc": (49.5938, 17.2509),
}
NAME = {"Znojmo": "Znojmo", "Trebic": "T\\v{r}eb\\'{\\i}\\v{c}",
        "Jihlava": "Jihlava", "Brno": "Brno", "Hodonin": "Hodon\\'{\\i}n",
        "Zlin": "Zl\\'{\\i}n", "Prostejov": "Prost\\v{e}jov", "Olomouc": "Olomouc"}
PLAIN = {k: k for k in NAME}          # for the width estimate


CABLES = {
    ("Prostejov", "Olomouc"): 17, ("Jihlava", "Trebic"): 29,
    ("Trebic", "Znojmo"): 42, ("Brno", "Prostejov"): 48,
    ("Prostejov", "Zlin"): 49, ("Olomouc", "Zlin"): 51,
    ("Trebic", "Brno"): 53, ("Brno", "Hodonin"): 54,
    ("Znojmo", "Brno"): 55, ("Zlin", "Hodonin"): 57,
    ("Jihlava", "Brno"): 77, ("Brno", "Zlin"): 78,
    ("Znojmo", "Hodonin"): 79,
}
assert len(set(CABLES.values())) == len(CABLES), "cable weights are not distinct"

G = nx.Graph()
G.add_nodes_from(TOWNS_LATLON)
for (a, b), w in CABLES.items():
    G.add_edge(a, b, weight=w)
assert G.number_of_nodes() == 8 and G.number_of_edges() == 13

# --- canvas placement -------------------------------------------------------
FULL_H = 470
# Numbers that a slide claims are annotated in the empty lower-left corner
# (NOTE_AT); prose captions live in the deck's <figcaption>, not in the drawing.
NOTE_AT = (24, 350)
# Vertical budget for the solver: the cropped drawing must stay under
# 1100 * 380 / 1120 = 373bp, pad included, or the height binds the scale.
LABEL_BAND = (25, 374)

# Positions are DESIGNED, not geographic -- the lecturer's call, 2026-09.
#
# The true lat/lon (still in KM above, and still what fig_moravia_dark draws)
# projected onto this canvas put Prostejov and Olomouc **59bp apart** while
# Jihlava and Znojmo sat 400bp apart, and squeezed all eight towns into
# 740 x 192bp of a 1100bp-wide page.  Three weight labels then had to share the
# top-right corner and Olomouc's name needed a leader line to escape.  Nothing
# about the lesson depends on where the towns really are.
#
# So: the same eight towns, the same thirteen cables, the same 292km tree, laid
# out as what the graph actually is -- a fan of six spokes around Brno, with
# Jihlava/Trebic/Znojmo on the left arc and Hodonin/Zlin/Prostejov on the right,
# and Olomouc hung outside the Prostejov-Zlin rim.  Planar, no crossings, and the
# closest two towns are 160bp apart instead of 59.  The assertions below are the
# gate: keep them passing and the drawing stays readable from the back row.
POS = {
    "Jihlava":   (216, 300),
    "Trebic":    (92, 100),
    "Znojmo":    (341, 100),
    "Brno":      (467, 300),
    "Hodonin":   (592, 100),
    "Prostejov": (720, 300),
    "Olomouc":   (1008, 292),
    "Zlin":      (865, 103),
}

assert not crossings(list(CABLES), POS), crossings(list(CABLES), POS)
assert not clearance_bad(list(CABLES), POS), clearance_bad(list(CABLES), POS)

_MINSEP = min(math.dist(POS[a], POS[b]) for a, b in itertools.combinations(POS, 2))
assert _MINSEP >= 150, f"towns crowd at {_MINSEP:.0f}bp -- spread the layout"
assert max(y for _, y in POS.values()) - min(y for _, y in POS.values()) <= 250, (
    "the town band is too tall: names above the top row and below the bottom one "
    "will not fit inside LABEL_BAND")

# (the name placement is solved further down, once the MST is known)


# --- the algorithms, traced -------------------------------------------------
def kruskal_trace(g):
    parent = {n: n for n in g}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    trace, mst = [], []
    for a, b, w in sorted(g.edges(data="weight"), key=lambda e: e[2]):
        ra, rb = find(a), find(b)
        if ra == rb:
            trace.append((a, b, w, "skip"))
        else:
            parent[ra] = rb
            mst.append((a, b, w))
            trace.append((a, b, w, "add"))
        if len(mst) == g.number_of_nodes() - 1:
            break
    return mst, trace


def prim_trace(g, start):
    vis, tr = {start}, []
    while len(vis) < g.number_of_nodes():
        best = min(((u, v, g[u][v]["weight"]) for u in vis for v in g[u] if v not in vis),
                   key=lambda e: (e[2], e[0], e[1]))
        vis.add(best[1])
        tr.append(best)
    return tr


def boruvka_rounds(g):
    parent = {n: n for n in g}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    rounds, chosen = [], []
    while len({find(n) for n in g}) > 1:
        cheapest = {}
        for a, b, w in g.edges(data="weight"):
            ra, rb = find(a), find(b)
            if ra == rb:
                continue
            for r in (ra, rb):
                if r not in cheapest or w < cheapest[r][2]:
                    cheapest[r] = (a, b, w)
        rnd = sorted(set(cheapest.values()), key=lambda e: e[2])
        rounds.append(rnd)
        for a, b, w in rnd:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
                chosen.append((a, b, w))
    return rounds, chosen


MST_EDGES, KRUSKAL = kruskal_trace(G)
PRIM = prim_trace(G, "Brno")
BORUVKA_ROUNDS, BORUVKA_EDGES = boruvka_rounds(G)
MST_TOTAL = sum(w for _, _, w in MST_EDGES)

MST = nx.Graph()
MST.add_nodes_from(G)
MST.add_weighted_edges_from(MST_EDGES)

# --- assertions against review/DECK_SPEC.md ---------------------------------
assert MST_TOTAL == 292, MST_TOTAL
assert sum(d["weight"] for *_, d in nx.minimum_spanning_tree(G).edges(data=True)) == 292
assert MST.number_of_edges() == 7 == G.number_of_nodes() - 1
assert [w for _, _, w, _ in KRUSKAL] == [17, 29, 42, 48, 49, 51, 53, 54]
assert [a for *_, a in KRUSKAL] == ["add"] * 5 + ["skip"] + ["add"] * 2
assert [w for _, _, w in PRIM] == [48, 17, 49, 53, 29, 42, 54]
assert sum(w for _, _, w in PRIM) == 292
assert {frozenset((a, b)) for a, b, _ in PRIM} == {frozenset((a, b)) for a, b, _ in MST_EDGES}
assert len(BORUVKA_ROUNDS) == 2 and len(BORUVKA_ROUNDS[0]) == 6
assert sum(w for _, _, w in BORUVKA_EDGES) == 292
assert sorted(d for _, d in MST.degree()) == [1, 1, 1, 1, 1, 3, 3, 3]
assert {n for n, d in MST.degree() if d == 3} == {"Brno", "Prostejov", "Trebic"}

# Which side each town's name sits on — solved, not hand-assigned.
# The solver must clear **every** cable the figures draw, not just the MST's seven.
# Constraining only the MST let the Znojmo-Hodonin route run straight through the
# word "Znojmo" on every weighted figure in the deck -- a defect that survived a
# whole build because the assertion was never asked about it.
LABEL_SIDE, LABEL_BOX = place_labels(
    PLAIN, POS, list(CABLES),
    bounds=(0, LABEL_BAND[0], DESIGN["full"], LABEL_BAND[1]), gap=3.0)

# ...then the weight chips, against the names that are now fixed.
CHIP_AT = place_chips(CABLES, POS, blockers=list(LABEL_BOX.values()),
                      edges=list(CABLES))

_TREE_SET = {frozenset((a, b)) for a, b, _ in MST_EDGES}

SKIPPED = next((a, b, w) for a, b, w, act in KRUSKAL if act == "skip")
assert SKIPPED[2] == 51


# --- damage -----------------------------------------------------------------
def connectivity(g, removed):
    h = g.copy()
    h.remove_nodes_from(removed)
    if h.number_of_nodes() == 0:
        return Fraction(0)
    return Fraction(len(max(nx.connected_components(h), key=len)), 8)


def profile(g, order):
    return [connectivity(g, order[:k]) for k in range(1, 8)]


def r_index(prof):
    return Fraction(sum(prof), 8)


def adaptive_order(g):
    h = g.copy()
    order = []
    while h.number_of_nodes() > 1:
        order.append(max(sorted(h.nodes()), key=lambda x: h.degree(x)))
        h.remove_node(order[-1])
    return order + list(h.nodes())


ATTACK_ORDER = adaptive_order(MST)
ATTACK_PROFILE = profile(MST, ATTACK_ORDER)
R_ATTACK = r_index(ATTACK_PROFILE)
RANDOM_ORDER = ["Zlin", "Znojmo", "Jihlava", "Hodonin", "Prostejov", "Trebic",
                "Olomouc", "Brno"]
RANDOM_PROFILE = profile(MST, RANDOM_ORDER)
R_RANDOM = r_index(RANDOM_PROFILE)

assert ATTACK_ORDER[:3] == ["Brno", "Prostejov", "Trebic"], ATTACK_ORDER
assert R_ATTACK == Fraction(11, 64), R_ATTACK
assert R_RANDOM == Fraction(13, 32), R_RANDOM
assert connectivity(MST, ["Brno"]) == Fraction(3, 8)
assert sorted(len(c) for c in nx.connected_components(
    nx.subgraph_view(MST, filter_node=lambda n: n != "Brno"))) == [1, 3, 3]

REDUNDANT = [("Zlin", "Hodonin", 57), ("Znojmo", "Hodonin", 79)]
MST2 = MST.copy()
MST2.add_weighted_edges_from(REDUNDANT)
R_REDUNDANT = r_index(profile(MST2, adaptive_order(MST2)))
EXTRA_KM = sum(w for *_, w in REDUNDANT)
assert EXTRA_KM == 136
assert R_REDUNDANT == Fraction(17, 64), R_REDUNDANT
assert min(connectivity(MST2, [n]) for n in MST2) == Fraction(6, 8)

# the exhaustive search that picked those two, re-run so the claim cannot rot
_unused = [(a, b, w) for (a, b), w in CABLES.items() if not MST.has_edge(a, b)]
_best = max(
    (((r_index(profile(h, adaptive_order(h)))), -(e1[2] + e2[2]), (e1, e2))
     for e1, e2 in itertools.combinations(_unused, 2)
     for h in [nx.Graph(MST)] if not h.add_weighted_edges_from([e1, e2])),
    key=lambda t: (t[0], t[1]))
assert _best[0] == R_REDUNDANT and set(map(tuple, _best[2])) == set(REDUNDANT), _best


# ===========================================================================
#                         shared Moravian drawing
# ===========================================================================
def moravia(edges=None, faint=None, heavy=None, weights=None, labels=True,
            node_fill=None, node_label=None, rings=None, removed=(), badge=None,
            struck=(), extra_text="", name_color=None, weight_override=None):
    """One drawing routine for every Moravian figure, so the graph never moves.

    edges       list of (a, b) drawn solid black          -- cables in the tree
    faint       list of (a, b) drawn dashed gray          -- candidate routes
    heavy       dict (a, b) -> colour                     -- what this slide is about
    weights     iterable of (a, b) whose km is printed on the edge
    badge       dict (a, b) -> str printed in a disc on the edge
    struck      edges drawn with a cross through them
    """
    edges = list(edges or [])
    faint = list(faint or [])
    heavy = dict(heavy or {})
    weights = set(frozenset(e) for e in (weights or []))
    rings = dict(rings or {})
    badge = dict(badge or {})
    node_fill = dict(node_fill or {})
    node_label = dict(node_label or {})
    struck = set(frozenset(e) for e in struck)
    s = ""

    def draw(a, b, color, w, dash=""):
        return seg(POS[a], POS[b], color=color, w=w, dash=dash)

    for a, b in faint:
        if a in removed or b in removed:
            continue
        s += draw(a, b, "annot", 2.2, DASH)
    drawn = set()
    for a, b in edges:
        if a in removed or b in removed:
            continue
        col = heavy.get((a, b)) or heavy.get((b, a)) or "black"
        s += draw(a, b, col, HEAVY_W if col != "black" else EDGE_W + 1.2)
        drawn.add(frozenset((a, b)))
    for (a, b), col in heavy.items():
        if frozenset((a, b)) in drawn or a in removed or b in removed:
            continue
        s += draw(a, b, col, HEAVY_W, DASH if frozenset((a, b)) in struck else "")

    for e in struck:
        a, b = tuple(e)
        mx, my = (POS[a][0] + POS[b][0]) / 2, (POS[a][1] + POS[b][1]) / 2
        s += seg((mx - 15, my - 15), (mx + 15, my + 15), color="accenttwo", w=4.0)
        s += seg((mx - 15, my + 15), (mx + 15, my - 15), color="accenttwo", w=4.0)

    for e in weights:
        a, b = tuple(e)
        if a in removed or b in removed:
            continue
        key = (a, b) if (a, b) in CABLES else (b, a)
        w = (weight_override or {}).get(key, CABLES[key])
        (mx, my), lead = CHIP_AT[key]
        if lead:
            ex = (POS[key[0]][0] + POS[key[1]][0]) / 2
            ey = (POS[key[0]][1] + POS[key[1]][1]) / 2
            s += seg((mx, my), (ex, ey), color="annot", w=1.2,
                     dash="dash pattern=on 2bp off 4bp")
        col = (heavy.get((a, b)) or heavy.get((b, a))
               or (weight_override or {}).get(key) and "accenttwo" or "black")
        s += (f"\\node[fill=white,inner sep=1.5bp,"
              f"font=\\fontsize{{{FONT}}}{{{FONT}}}\\selectfont,text={col}] "
              f"at ({mx:.1f},{my:.1f}) {{{w}}};\n")

    for e, tag in badge.items():
        a, b = tuple(e)
        key = (a, b) if (a, b) in CABLES else (b, a)
        (mx, my), lead = CHIP_AT[key]
        if lead:
            ex = (POS[key[0]][0] + POS[key[1]][0]) / 2
            ey = (POS[key[0]][1] + POS[key[1]][1]) / 2
            s += seg((mx, my), (ex, ey), color="annot", w=1.2,
                     dash="dash pattern=on 2bp off 4bp")
        s += square(mx, my, tag)

    for n, (x, y) in POS.items():
        if n in removed:
            s += opendisc(x, y, "accenttwo")
            s += seg((x - 12, y - 12), (x + 12, y + 12), color="accenttwo", w=3.6)
            s += seg((x - 12, y + 12), (x + 12, y - 12), color="accenttwo", w=3.6)
        else:
            s += disc(x, y, node_label.get(n, ""), fill=node_fill.get(n, "accent"))
        if n in rings:
            s += ring(x, y, color=rings[n])

    if labels:
        for n, (anc, dx, dy) in LABEL_SIDE.items():
            col = (name_color or {}).get(n, "black")
            x, y = POS[n]
            if math.hypot(dx, dy) > LEADER_AT:      # parked clear; draw a leader
                ux, uy = dx / math.hypot(dx, dy), dy / math.hypot(dx, dy)
                s += seg((x + ux * (NODE / 2 + 3), y + uy * (NODE / 2 + 3)),
                         (x + dx - ux * 6, y + dy - uy * 6), color="annot", w=1.2,
                         dash="dash pattern=on 2bp off 4bp")
            s += text(x + dx, y + dy, NAME[n], color=col, anchor=anc)
    return s + extra_text


# ===========================================================================
#                                Part 1
# ===========================================================================
ALL_CABLES = list(CABLES)


def is_tree_edge(e):
    """Orientation-independent. MST_PAIRS stores three cables reversed relative to
    CABLES, so `e not in MST_PAIRS` priced nine cables as unused instead of six --
    three tree cables showed a price and four showed none, on the slide that asks
    the room to spend a budget."""
    return frozenset(e) in _TREE_SET


assert len([e for e in ALL_CABLES if not is_tree_edge(e)]) == 6, \
    "the unused-cable set is wrong -- MST_PAIRS orientation again"


MST_PAIRS = [(a, b) for a, b, _ in MST_EDGES]


def note(s, color="accenttwo", anchor="west", at=None, size=FONT):
    """A figure's own number note, in a corner of the Moravian map.

    Asserted clear of every town name: notes carry numbers (R1), and the one that
    did not -- "every town is its own island" -- was drawn straight through the
    word "Znojmo" on the Boruvka opening frame.
    """
    x, y = at or NOTE_AT
    plain = s.replace("\\\\", "\x00")                       # protect the line break
    plain = re.sub(r"\\[a-zA-Z]+|[${}]", "", plain)
    plain = plain.replace("\x00", "\\\\")
    b = label_box(x, y, plain, anchor, size=size)
    for n, lb in LABEL_BOX.items():
        assert not boxes_overlap(b, lb), (
            f"figure note {s!r} runs into the {n!r} label -- shorten it")
    return text(x, y, s, color=color, anchor=anchor, size=size)


def fig_mst_def():
    return moravia(faint=[e for e in ALL_CABLES if not is_tree_edge(e)],
                   edges=MST_PAIRS,
                   heavy={e: "accenttwo" for e in MST_PAIRS},
                   weights=MST_PAIRS)


def fig_mst_blank():
    return moravia(edges=MST_PAIRS)


def fig_brno_removed():
    pieces = sorted(nx.connected_components(
        nx.subgraph_view(MST, filter_node=lambda n: n != "Brno")), key=len, reverse=True)
    assert [len(p) for p in pieces] == [3, 3, 1]
    cols = ["accent", "accent", "accent"]
    fill = {n: cols[i] for i, p in enumerate(pieces) for n in p}
    return moravia(edges=MST_PAIRS, removed=["Brno"], node_fill=fill,
                   )


# --- curve plotting ---------------------------------------------------------
def axes(x0, x1, y0, y1, xlab, ylab, xticks, yticks, xfmt=str, yfmt=str):
    s = seg((x0 - 14, y0), (x1 + 18, y0), color="annot", w=2.2)
    s += seg((x0, y0 - 14), (x0, y1 + 18), color="annot", w=2.2)
    for v, X in xticks:
        s += seg((X, y0 - 9), (X, y0 + 9), color="annot", w=2.0)
        s += text(X, y0 - 16, xfmt(v), color="annot", anchor="north")
    for v, Y in yticks:
        s += seg((x0 - 9, Y), (x0 + 9, Y), color="annot", w=2.0)
        s += text(x0 - 16, Y, yfmt(v), color="annot", anchor="east")
    s += text((x0 + x1) / 2, y0 - 62, xlab, color="annot", anchor="north")
    s += text(x0 - 96, (y0 + y1) / 2, ylab, color="annot", anchor="south", rot=90)
    return s


# Curve labels live to the right of the plot box, inside the canvas: a label
# hung off x=1030 ran past the 1100bp page and the crop silently lost it.
PLOT = dict(x0=230, x1=850, y0=110, y1=330)
LAB_X = 880


def _XY():
    def X(f):
        return PLOT["x0"] + f * (PLOT["x1"] - PLOT["x0"])

    def Y(v):
        return PLOT["y0"] + v * (PLOT["y1"] - PLOT["y0"])
    return X, Y


def profile_axes():
    X, Y = _XY()
    return axes(PLOT["x0"], PLOT["x1"], PLOT["y0"], PLOT["y1"],
                "fraction of towns removed", "connectivity",
                [(v, X(v)) for v in (0, 0.25, 0.5, 0.75, 1.0)],
                [(v, Y(v)) for v in (0, 0.5, 1.0)],
                xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")


def profile_points(prof):
    X, Y = _XY()
    pts = [(X(0), Y(1.0))]
    for k, v in enumerate(prof, 1):
        pts.append((X(k / 8), Y(float(v))))
    return pts


def fig_profile_both():
    s = profile_axes()
    X, Y = _XY()
    for prof, col, lab, ly in ((RANDOM_PROFILE, "accentthree", "random", 0.72),
                               (ATTACK_PROFILE, "accenttwo", "targeted", 0.22)):
        pts = profile_points(prof)
        s += polyline(pts, color=col, w=4.0)
        s += "".join(dot(x, y, col) for x, y in pts)
    s += legend([("accentthree", "", f"random\\\\$R = {float(R_RANDOM):.2f}$"),
                 ("accenttwo", "", f"targeted\\\\$R = {float(R_ATTACK):.2f}$")])
    s += text(X(0.52), Y(0.36),
              f"$R$ is {float(R_RANDOM / R_ATTACK):.1f}$\\times$ larger", color="black")
    return s


# ===========================================================================
#           simulated networks (measured here, never drawn from memory)
# ===========================================================================
SIM_N, SIM_M, SIM_BA = 2000, 6000, 3
ER = nx.gnm_random_graph(SIM_N, SIM_M, seed=7)
SF = nx.barabasi_albert_graph(SIM_N, SIM_BA, seed=7)


def kappa_of(degs):
    d = np.asarray(list(degs), float)
    return float((d ** 2).mean() / d.mean())


ER_KAPPA = kappa_of(d for _, d in ER.degree())
SF_KAPPA = kappa_of(d for _, d in SF.degree())
ER_MEANK = 2 * ER.number_of_edges() / SIM_N
assert abs(ER_MEANK - 6.0) < 0.01 and 6.9 < ER_KAPPA < 7.2, (ER_MEANK, ER_KAPPA)
assert SF_KAPPA > 15, SF_KAPPA


def removal_curve(g, mode, seed=11, steps=40):
    n0 = g.number_of_nodes()
    rng = np.random.default_rng(seed)
    h = g.copy()
    fixed = sorted(g.nodes(), key=lambda x: -g.degree(x))
    xs, ys, removed, i = [0.0], [1.0], [], 0
    per = max(1, n0 // steps)
    while h.number_of_nodes() > per:
        if mode == "random":
            pick = list(rng.choice(list(h.nodes()), size=per, replace=False))
        elif mode == "fixed":
            pick, i = fixed[i:i + per], i + per
        else:
            pick = sorted(h.nodes(), key=lambda x: -h.degree(x))[:per]
        removed += pick
        h.remove_nodes_from(pick)
        hh = g.copy()
        hh.remove_nodes_from(removed)
        xs.append(len(removed) / n0)
        ys.append(len(max(nx.connected_components(hh), key=len)) / n0
                  if hh.number_of_nodes() else 0.0)
    return xs, ys


CURVES = {(g, m): removal_curve(gr, m)
          for g, gr in (("er", ER), ("sf", SF))
          for m in ("random", "targeted", "fixed")}


def collapse_at(key, thresh=0.05):
    xs, ys = CURVES[key]
    return next(x for x, y in zip(xs, ys) if y < thresh)


ER_RAND_C = collapse_at(("er", "random"))
SF_RAND_C = collapse_at(("sf", "random"))
ER_TARG_C = collapse_at(("er", "targeted"))
SF_TARG_C = collapse_at(("sf", "targeted"))
ER_FIXED_C = collapse_at(("er", "fixed"))
# the theory this deck teaches, checked against the measurement it shows
assert abs(ER_RAND_C - (1 - 1 / ER_MEANK)) < 0.06, (ER_RAND_C, 1 - 1 / ER_MEANK)
assert SF_TARG_C < 0.3 < ER_TARG_C, (SF_TARG_C, ER_TARG_C)
assert SF_RAND_C > ER_RAND_C, (SF_RAND_C, ER_RAND_C)
assert ER_FIXED_C > ER_TARG_C, (ER_FIXED_C, ER_TARG_C)


def legend(entries, x=846, y0=None, dy=None, sample=40):
    """A real legend: a sample of the line, then its name in ink.

    The labels used to be tinted to match their curve, which stopped working the
    moment accent-3 came out of the text palette for contrast -- a gold curve with
    a black label, beside a red curve with a red label, is not a legend, it is a
    guess. Drawing a piece of the actual line removes the guess.
    """
    _, Y = _XY()
    y = PLOT["y1"] - 26 if y0 is None else y0
    # Row pitch has to clear the tallest entry: a fixed 54bp let two-line entries
    # print on top of each other on slide 47.
    rows = max(len(t.split("\\\\")) for _, _, t in entries)
    if dy is None:
        dy = 46 * rows + 20
    out = ""
    for colour, dash, lines in entries:
        out += seg((x, y), (x + sample, y), color=colour, w=4.0, dash=dash)
        out += text(x + sample + 10, y, lines, color="black", anchor="west")
        y -= dy
    return out


def sim_axes(xlab="fraction of nodes removed", ylab="giant component"):
    X, Y = _XY()
    return axes(PLOT["x0"], PLOT["x1"], PLOT["y0"], PLOT["y1"], xlab, ylab,
                [(v, X(v)) for v in (0, 0.25, 0.5, 0.75, 1.0)],
                [(v, Y(v)) for v in (0, 0.5, 1.0)],
                xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")


def sim_curve(key, col, w=4.0, dash=""):
    X, Y = _XY()
    xs, ys = CURVES[key]
    return polyline([(X(x), Y(y)) for x, y in zip(xs, ys)], color=col, w=w, dash=dash)


# ===========================================================================
#                                Part 4
# ===========================================================================
PUD_COLS, PUD_ROWS, PUD_CELL = 88, 24, 12
PUD_FIELD = np.random.default_rng(5).random((PUD_ROWS, PUD_COLS))
PC_LITERATURE = 0.5927          # 2D site percolation, square lattice


def _clusters(mask):
    """Label 4-connected components of a boolean grid; return (labels, sizes).

    Union-find over the two neighbour offsets, not a per-cell flood fill: the
    percolation sweep labels a 200x200 grid 23 times and the flood-fill version
    made the whole figure build take over two minutes.
    """
    h, w = mask.shape
    idx = np.arange(h * w).reshape(h, w)
    parent = np.arange(h * w)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for da, db in ((mask[1:, :] & mask[:-1, :], (idx[1:, :], idx[:-1, :])),
                   (mask[:, 1:] & mask[:, :-1], (idx[:, 1:], idx[:, :-1]))):
        for u, v in zip(db[0][da], db[1][da]):
            ru, rv = find(int(u)), find(int(v))
            if ru != rv:
                parent[rv] = ru

    roots = np.array([find(i) for i in range(h * w)]).reshape(h, w)
    roots = np.where(mask, roots + 1, 0)
    uniq, counts = np.unique(roots[roots > 0], return_counts=True)
    return roots, dict(zip(uniq.tolist(), counts.tolist()))


def lattice_body(p, field, y0, label=None, cell=PUD_CELL):
    rows, cols = field.shape
    mask = field < p
    lab, sizes = _clusters(mask)
    big = max(sizes, key=sizes.get) if sizes else 0
    x0 = (DESIGN["full"] - cols * cell) / 2
    s = ""
    for r in range(rows):
        for c in range(cols):
            if not mask[r, c]:
                continue
            x, y = x0 + c * cell, y0 + r * cell
            col = "accenttwo" if lab[r, c] == big else "accent"
            s += (f"\\fill[{col}] ({x:.1f},{y:.1f}) rectangle "
                  f"({x + cell - 2:.1f},{y + cell - 2:.1f});\n")
    s += (f"\\draw[line width=2bp,draw=annot] ({x0 - 4:.1f},{y0 - 4:.1f}) rectangle "
          f"({x0 + cols * cell - 2:.1f},{y0 + rows * cell - 2:.1f});\n")
    frac = sizes.get(big, 0) / (rows * cols)
    top = y0 + rows * cell + 6
    s += text(x0, top, label or f"$p = {p:.2f}$", color="black", anchor="south west")
    s += text(x0 + cols * cell - 2, top, "largest cluster " + pct(frac),
              color="accenttwo", anchor="south east")
    return s, frac


def fig_lattice_low():
    return lattice_body(0.40, PUD_FIELD[:22], 66)[0]


PERC_N = 200
_PERC_FIELD = np.random.default_rng(9).random((PERC_N, PERC_N))


def perc_curve():
    ps = np.round(np.arange(0.30, 0.86, 0.025), 3)
    out = []
    for p in ps:
        lab, sizes = _clusters(_PERC_FIELD < p)
        out.append(max(sizes.values()) / PERC_N ** 2 if sizes else 0.0)
    return list(ps), out


PERC_P, PERC_S = perc_curve()
_steep = max(range(1, len(PERC_P)), key=lambda i: PERC_S[i] - PERC_S[i - 1])
PERC_MEASURED = (PERC_P[_steep] + PERC_P[_steep - 1]) / 2
assert abs(PERC_MEASURED - PC_LITERATURE) < 0.06, (PERC_MEASURED, PC_LITERATURE)


def fig_phase_transition():
    X0, X1, Y0, Y1 = PLOT["x0"], PLOT["x1"], PLOT["y0"], PLOT["y1"]

    def X(p):
        return X0 + (p - 0.3) / 0.55 * (X1 - X0)

    def Y(v):
        return Y0 + v * (Y1 - Y0)
    s = axes(X0, X1, Y0, Y1, "occupation probability, $p$", "largest cluster",
             [(v, X(v)) for v in (0.3, 0.45, 0.6, 0.75)],
             [(v, Y(v)) for v in (0, 0.5, 1.0)],
             xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    s += seg((X(PC_LITERATURE), Y0), (X(PC_LITERATURE), Y1),
             color="annot", w=2.6, dash=DASH)
    s += text(X(PC_LITERATURE) - 14, Y(0.86), f"$p_c \\approx {PC_LITERATURE:.2f}$",
              color="annot", anchor="east")
    s += polyline([(X(p), Y(v)) for p, v in zip(PERC_P, PERC_S)],
                  color="accenttwo", w=4.0)
    s += text(LAB_X, Y(0.72), "a finite share\\\\of the lattice", color="accenttwo",
              anchor="west")
    s += text(X(0.36), Y(0.62), "small\\\\clusters", color="annot")
    return s


# ===========================================================================
#                                Part 5
# ===========================================================================
# A small network used for q(k): degrees 4, 3, 2, 1, 1, 1 -- printed, not typed.
# The network the kappa slides argue over -- and the one the `branch-out` stage
# hands the room, at the same positions, so the drawing the room played with is
# the drawing the next slide freezes.
#
# Ten towns, ten cables, and every number the slides print comes out whole:
#   degrees 5 4 3 2 1 1 1 1 1 1   ->  <k> = 2, <k^2> = 6, kappa = 3,
#   kappa - 1 = 2 (the search doubles), f_c = 1 - 1/2 = 0.5 exactly.
# Its one cycle is four towns long, so there is no triangle and the branching
# argument's own assumption holds on the picture it is argued over.
QK_POS = {"h": (205, 215), "p": (325, 298), "q": (325, 125), "a": (430, 212),
          "l1": (70, 318), "l2": (62, 208), "l3": (85, 97),
          "l4": (265, 360), "l5": (410, 351), "l6": (235, 60)}
QK_EDGES = [("h", "p"), ("p", "a"), ("a", "q"), ("q", "h"),
            ("h", "l1"), ("h", "l2"), ("h", "l3"),
            ("p", "l4"), ("p", "l5"), ("q", "l6")]
QK_G = nx.Graph(QK_EDGES)
QK_DEG = dict(QK_G.degree())
QK_KAPPA = kappa_of(QK_DEG.values())
assert sorted(QK_DEG.values(), reverse=True) == [5, 4, 3, 2, 1, 1, 1, 1, 1, 1]
assert sum(QK_DEG.values()) == 2 * len(QK_EDGES) == 20
assert QK_KAPPA == 3 and sum(QK_DEG.values()) / len(QK_DEG) == 2
assert nx.girth(QK_G) == 4, "the branching argument assumes no triangles"
assert not clearance_bad(QK_EDGES, QK_POS)
assert not crossings(QK_EDGES, QK_POS), crossings(QK_EDGES, QK_POS)


def qk_graph(highlight=None, show_deg=False):
    s = "".join(seg(QK_POS[a], QK_POS[b],
                    color="accenttwo" if highlight in ((a, b), (b, a)) else "black",
                    w=HEAVY_W if highlight in ((a, b), (b, a)) else EDGE_W)
                for a, b in QK_EDGES)
    for n, (x, y) in QK_POS.items():
        s += disc(x, y, str(QK_DEG[n]) if show_deg else "", fill="accent")
    return s


def fig_kappa_def():
    s = qk_graph(highlight=("h", "c"), show_deg=True)
    return s


def fan_tree(x0, dx, y0, spread, levels=2, b=2, dead=(), node=NODE):
    """A branching search drawn as a proper tree: children sit under their parent.

    Returns (tikz, levels_dict).  The earlier version computed the x of every level
    from one dx and let level 2 land at x = 1300 on an 1100bp canvas, so half of
    `molloy-reed` was drawn off the page and the two panels overlapped.  Here the
    caller gives the x step and the routine asserts the tree fits.
    """
    lvl = {0: [(x0, y0)]}
    for d in range(1, levels + 1):
        pts = []
        gap = spread / (b ** d)
        for (px, py) in lvl[d - 1]:
            for j in range(b):
                pts.append((x0 + d * dx, py + (j - (b - 1) / 2) * gap))
        lvl[d] = pts
    far = x0 + levels * dx + node / 2
    assert far <= DESIGN["full"] - 8, f"fan tree runs to {far}bp on a 1100bp canvas"
    s = ""
    for d in range(1, levels + 1):
        for i, q in enumerate(lvl[d]):
            parent = lvl[d - 1][i // b]
            gone = (d, i) in dead or (d - 1, i // b) in dead
            s += seg(parent, q, color="annot" if gone else "accent",
                     w=EDGE_W + 1.0, dash=DASH if gone else "")
    for d in range(levels + 1):
        for i, (x, y) in enumerate(lvl[d]):
            gone = any((dd, ii) in dead for dd, ii in [(d, i)]) or \
                   (d > 0 and (d - 1, i // b) in dead)
            fill = "annot" if gone else ("accenttwo" if d == 0 else "accent")
            s += disc(x, y, "", fill=fill, size=node)
    return s, lvl


def _arrival(x, y, label=True):
    """The edge the search arrived on, labelled ABOVE it.

    Labelling it to the left ran the text off the canvas and the crop clipped it to
    "in / ay" -- a caption that had lost its own first letters on two slides.
    """
    s = seg((x - 130, y), (x - NODE / 2 - 3, y), color="annot", w=EDGE_W + 1.0)
    if label:
        s += text(x - 66, y + 26, "came in here", color="annot", anchor="south")
    return s


def fig_molloy_reed():
    """Two panels: a search that dies, and one that never does.

    The left panel is drawn by hand rather than as a b=1 tree: a one-child-per-step
    chain of three nodes reads as a search that is still going, which is the
    opposite of the point. It ends in a stub that reaches nothing.
    """
    s = _arrival(150, 200, label=False)
    s += seg((150, 200), (330, 200), color="accent", w=EDGE_W + 1.0)
    s += disc(150, 200, "", fill="accenttwo")
    s += disc(330, 200, "", fill="accent")
    s += seg((350, 200), (470, 200), color="annot", w=EDGE_W + 1.0, dash=DASH)
    s += text(480, 200, "nothing", color="annot", anchor="west")
    s += text(300, 70, "$\\kappa - 1 < 1$", color="annot")
    s += seg((600, 40), (600, 350), color="annot", w=2.0, dash=DASH_LONG)
    body, _ = fan_tree(690, 190, 200, 220)
    s += body
    s += text(880, 70, "$\\kappa - 1 > 1$", color="accenttwo")
    return s


def ring_pos(n, r=1.0, ry=None, start=math.pi / 2):
    """Nodes on a circle -- or an ellipse.

    A `cols` figure must span >= 76% of 520bp and stay under 368bp tall.  A circle
    big enough for the first is too tall for the second, so ring figures are drawn
    as a wide ellipse: still obviously a ring, and it clears both gates.
    """
    ry = r if ry is None else ry
    return {i: (r * math.cos(2 * math.pi * i / n + start),
                ry * math.sin(2 * math.pi * i / n + start)) for i in range(n)}


RING6 = (ring_pos(6), [(i, (i + 1) % 6) for i in range(6)])
STAR6 = ({0: (0, 0), **{i: p for i, p in enumerate(ring_pos(5).values(), 1)}},
         [(0, i) for i in range(1, 6)])
PATH5 = ({i: (i - 2, 0) for i in range(5)}, [(i, i + 1) for i in range(4)])

KAPPA_CASES = [("a ring", RING6, 90), ("a star", STAR6, 90), ("a path", PATH5, 90)]
KAPPA_VALUES = []
for _nm, (_p, _e), _s in KAPPA_CASES:
    _g = nx.Graph(_e)
    KAPPA_VALUES.append(Fraction(
        sum(d * d for _, d in _g.degree()), sum(d for _, d in _g.degree())))
assert KAPPA_VALUES == [Fraction(2), Fraction(3), Fraction(7, 4)], KAPPA_VALUES


def fig_fc_formula():
    """The dilution line, drawn for the SAME kappa the branch-out stage hands the
    room one slide earlier: kappa = 3, so branching 2 and f_c = 0.50 exactly.

    It used to be drawn for kappa = 5. Nothing was wrong with the picture, but
    the room had just dragged a dial to 0.50 on a network with kappa = 3, and the
    next slide answered with a different threshold on a network it never saw.
    """
    # The y range stops at 2, not 4: with kappa = 3 the line starts at 2, and the
    # empty upper half cost 60bp of a figure that already binds the slide's
    # CONTENT_BOTTOM.
    X0, X1, Y0 = PLOT["x0"], PLOT["x1"], PLOT["y0"]
    Y1 = PLOT["y0"] + 0.62 * (PLOT["y1"] - PLOT["y0"])
    kappa = float(QK_KAPPA)
    assert kappa == 3

    def X(f):
        return X0 + f * (X1 - X0)

    def Y(v):
        return Y0 + v / 2.0 * (Y1 - Y0)
    fc = 1 - 1 / (kappa - 1)
    s = axes(X0, X1, Y0, Y1, "fraction removed, $f$", "branching factor",
             [(v, X(v)) for v in (0, 0.25, 0.5, 0.75, 1.0)],
             [(v, Y(v)) for v in (0, 1, 2)],
             xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    s += seg((X0, Y(1)), (X1, Y(1)), color="annot", w=2.6, dash=DASH)
    s += polyline([(X(f), Y((1 - f) * (kappa - 1))) for f in (0, 1)],
                  color="accenttwo", w=4.0)
    s += seg((X(fc), Y0), (X(fc), Y(1)), color="accenttwo", w=2.6, dash=DASH)
    s += dot(X(fc), Y(1), "accenttwo", d=20)
    s += text(X(fc) + 16, Y(1.45), f"$f_c = {fc:.2f}$", color="accenttwo",
              anchor="west")
    s += text(LAB_X, Y(1.8), f"$\\kappa = {kappa:g}$", color="accenttwo", anchor="west")
    s += text(LAB_X, Y(0.95), "1 = break-even", color="annot", anchor="west")
    return s


FC_KS = list(range(2, 13))
FC_VALS = [1 - 1 / k for k in FC_KS]
assert abs(FC_VALS[FC_KS.index(4)] - 0.75) < 1e-12


def fig_fc_poisson():
    X0, X1, Y0, Y1 = PLOT["x0"], PLOT["x1"], PLOT["y0"], PLOT["y1"]

    def X(k):
        return X0 + (k - 2) / 10 * (X1 - X0)

    def Y(v):
        return Y0 + v * (Y1 - Y0)
    s = axes(X0, X1, Y0, Y1, "average degree $\\langle k \\rangle$",
             "$f_c$", [(k, X(k)) for k in (2, 4, 6, 8, 10, 12)],
             [(v, Y(v)) for v in (0, 0.5, 1.0)],
             xfmt=str, yfmt=lambda v: f"{v:g}")
    s += polyline([(X(k), Y(v)) for k, v in zip(FC_KS, FC_VALS)],
                  color="accenttwo", w=4.0)
    k4 = FC_VALS[FC_KS.index(4)]
    s += seg((X(4), Y0), (X(4), Y(k4)), color="annot", w=2.4, dash=DASH)
    s += seg((X0, Y(k4)), (X(4), Y(k4)), color="annot", w=2.4, dash=DASH)
    s += dot(X(4), Y(k4), "accenttwo", d=20)
    s += text(X(4) + 20, Y(k4) - 44, f"$\\langle k \\rangle = 4$: {pct(k4)} must go",
              color="accenttwo", anchor="west")
    s += text(LAB_X, Y(0.86), "$f_c$ rises\\\\with $\\langle k \\rangle$", color="accenttwo", anchor="west")
    return s


SF_KMAX = list(range(10, 401, 10))


def _kappa_powerlaw(kmax, gamma=2.5, kmin=1):
    ks = np.arange(kmin, kmax + 1, dtype=float)
    p = ks ** -gamma
    p /= p.sum()
    return float((p * ks ** 2).sum() / (p * ks).sum())


SF_KAPPAS = [_kappa_powerlaw(k) for k in SF_KMAX]
assert SF_KAPPAS[-1] > SF_KAPPAS[0] * 2, SF_KAPPAS[:1] + SF_KAPPAS[-1:]


def fig_fc_scalefree():
    X0, X1, Y0, Y1 = PLOT["x0"], PLOT["x1"], PLOT["y0"], PLOT["y1"]

    def X(k):
        return X0 + (k - 10) / 390 * (X1 - X0)

    def Y(v):
        return Y0 + v * (Y1 - Y0)
    s = axes(X0, X1, Y0, Y1, "largest degree present", "",
             [(k, X(k)) for k in (10, 100, 200, 300, 400)],
             [(v, Y(v)) for v in (0, 0.5, 1.0)],
             xfmt=str, yfmt=lambda v: f"{v:g}")
    fcs = [1 - 1 / (k - 1) for k in SF_KAPPAS]
    s += polyline([(X(k), Y(v)) for k, v in zip(SF_KMAX, fcs)],
                  color="accenttwo", w=4.0)
    s += seg((X0, Y(1)), (X1, Y(1)), color="annot", w=2.4, dash=DASH)
    s += text(LAB_X, Y(0.92), "$f_c \\to 1$", color="accenttwo", anchor="west")
    s += text(LAB_X, Y(0.45), "bigger hubs,\\\\bigger $\\kappa$", color="annot",
              anchor="west")
    return s


def fig_robust_fragile():
    X, Y = _XY()
    s = sim_axes()
    s += sim_curve(("er", "random"), "accentthree")
    s += sim_curve(("er", "targeted"), "accentthree", dash=DASH)
    s += sim_curve(("sf", "random"), "accenttwo")
    s += sim_curve(("sf", "targeted"), "accenttwo", dash=DASH)
    s += legend([("accenttwo", "", "scale-free"),
                 ("accentthree", "", "random graph"),
                 ("annot", DASH, "targeted")])
    return s


def fig_mst_blank_design():
    return moravia(edges=MST_PAIRS,
                   faint=[e for e in ALL_CABLES if not is_tree_edge(e)],
                   weights=[e for e in ALL_CABLES if not is_tree_edge(e)])


def fig_redundant_answer():
    new = [(a, b) for a, b, _ in REDUNDANT]
    return moravia(edges=MST_PAIRS,
                   heavy={e: "accentthree" for e in new},
                   weights=new,
                   )


ER1 = nx.gnm_random_graph(14, 7, seed=4)


# The graph is a FOREST -- three small components and four isolated nodes -- so it
# can always be drawn without a crossing. Dropping it on a circle put its two long
# chords straight across each other in the middle, on a slide about a network that
# has barely any edges at all.
ER1_POS = {1: (110, 290), 0: (45, 245), 2: (110, 215), 11: (175, 245),
           3: (270, 290), 4: (350, 290), 12: (430, 290),
           6: (110, 120), 7: (45, 70), 8: (175, 70),
           5: (270, 150), 9: (340, 150), 10: (410, 150), 13: (478, 150)}
assert set(ER1_POS) == set(ER1)
assert not crossings(list(ER1.edges()), ER1_POS), crossings(list(ER1.edges()), ER1_POS)
assert not clearance_bad(list(ER1.edges()), ER1_POS, r=SMALLNODE / 2 + 3)


BW_BRIDGE = 6
BW_POS = {0: (250, 200), 3: (150, 200), 1: (290, 310), 2: (145, 285),
          4: (145, 115), 5: (290, 90),
          BW_BRIDGE: (550, 200),
          7: (850, 200), 8: (950, 200), 9: (810, 310), 10: (955, 285),
          11: (955, 115), 12: (810, 90)}
BW_EDGES = ([(0, i) for i in (1, 2, 3, 4, 5)]
            + [(0, BW_BRIDGE), (BW_BRIDGE, 7)]
            + [(7, i) for i in (8, 9, 10, 11, 12)])
BW_G = nx.Graph(BW_EDGES)
BW_HUB = max(BW_G.degree(), key=lambda kv: kv[1])[0]
assert BW_G.degree(BW_BRIDGE) == 2 and nx.is_connected(BW_G)
assert BW_G.degree(BW_HUB) >= 6 and not clearance_bad(BW_EDGES, BW_POS)
# "the degree-2 node" is singular on the slide, so there must be exactly one.
assert [n for n, d in BW_G.degree() if d == 2] == [BW_BRIDGE], \
    "more than one degree-2 node: the slide's phrase is ambiguous"


# ===========================================================================
#                              Wrap-up
# ===========================================================================
def fig_recap():
    """One drawing: what was bought, what was lost, what was added back.

    The first version was a row of four boxed header/value pairs: a 2x4 table, which
    L2 makes a Blocker, on a slide titled "Module 03 in one picture".  The second
    put three numbers along the bottom of the map.
    Once the towns were spread to fill the canvas there was no free band left for a
    row of numbers, so the three numbers moved to the slide's own line. The drawing
    keeps what only a drawing can say: which cables were bought, which town is gone,
    and which two cables close the ring.
    """
    new = [(a, b) for a, b, _ in REDUNDANT]
    return moravia(edges=MST_PAIRS,
                   heavy={e: "accentthree" for e in new},
                   removed=["Brno"])


def fig_m04_teaser():
    """Same pile-of-edge-ends as qk-bias, at column width.

    Discs at NODE and dots at 28bp: at SMALLNODE and 18bp they landed 18px on the
    slide, under the 26px floor, which the node-size gate could not see until it
    was taught to find discs by colour rather than by darkness.
    """
    order = sorted(QK_DEG, key=lambda n: (-QK_DEG[n], n))
    x0, step, ytop = 165, 35, 300
    s = text(150, ytop, "people", color="accent", anchor="east")
    s += text(150, ytop - 96, "friend-\\\\ships", color="accenttwo", anchor="east")
    for i, n in enumerate(order):
        x = x0 + i * step
        s += disc(x, ytop, "", fill="accent", size=34)
        for j in range(QK_DEG[n]):
            s += dot(x, ytop - 44 - j * 34, "accenttwo", d=28)
    return s


FIGURES = [
    ("mst-def", fig_mst_def, "full", FULL_H),
    ("mst-blank", fig_mst_blank, "full", FULL_H),
    ("brno-removed", fig_brno_removed, "full", FULL_H),
    ("profile-both", fig_profile_both, "full", 420),
    ("lattice-low", fig_lattice_low, "full", 440),
    ("phase-transition", fig_phase_transition, "full", 420),
    ("kappa-def", fig_kappa_def, "col", 420),
    ("molloy-reed", fig_molloy_reed, "full", 400),
    ("fc-formula", fig_fc_formula, "full", 420),
    ("fc-poisson", fig_fc_poisson, "full", 420),
    ("fc-scalefree", fig_fc_scalefree, "full", 420),
    ("robust-fragile", fig_robust_fragile, "full", 420),
    ("mst-blank-design", fig_mst_blank_design, "full", FULL_H),
    ("redundant-answer", fig_redundant_answer, "full", FULL_H),
    ("recap", fig_recap, "full", 360),
    ("m04-teaser", fig_m04_teaser, "col", 380),
]


def main():
    # Report every failing figure, not just the first: the geometry gates fire in
    # clusters, and stopping at figure 3 of 60 hid the other five for a whole round.
    bad = []
    for name, fn, cont, *h in FIGURES:
        try:
            emit(name, fn(), cont, h[0] if h else None)
        except AssertionError as e:
            bad.append(str(e))
            print(f"  FAIL {name}: {e}")
    print(f"\n{len(_built)} figures written")
    if bad:
        print(f"{len(bad)} figure(s) failed their floors:")
        for b in bad:
            print("  " + b)
        sys.exit(1)


if __name__ == "__main__":
    main()

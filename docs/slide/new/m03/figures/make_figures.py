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
INK = "000000"

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
CAP_RATIO = 0.683
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


def fill_poly(pts, color="accenttwo", opacity=0.25):
    return "\\fill[%s,opacity=%s] %s -- cycle;\n" % (
        color, opacity, " -- ".join("(%.1f,%.1f)" % p for p in pts))


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
        raise SystemExit(
            "label placement failed — no collision-free side assignment exists.\n"
            "Move a node, shorten a name, or widen the canvas; do not shrink the type.")
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

_lat0 = sum(v[0] for v in TOWNS_LATLON.values()) / 8
_lon0 = sum(v[1] for v in TOWNS_LATLON.values()) / 8
KM = {n: ((lo - _lon0) * 111.32 * math.cos(math.radians(_lat0)),
          (la - _lat0) * 110.574) for n, (la, lo) in TOWNS_LATLON.items()}

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
# The map is deliberately shorter than the canvas: town names stick out top and
# bottom, and the *cropped* drawing must stay under 373bp or the height binds the
# deck's scale and every Moravian figure shrinks.  Numbers that a slide claims are
# annotated in the empty lower-left corner (NOTE_AT); prose captions live in the
# deck's <figcaption>, not in the drawing.
_X0, _X1, _Y0, _Y1 = 190, 930, 130, 322
NOTE_AT = (24, 72)
# Vertical budget for the solver: the cropped drawing must stay under
# 1100 * 380 / 1120 = 373bp, pad included, or the height binds the scale.
LABEL_BAND = (25, 374)
_xs = [p[0] for p in KM.values()]
_ys = [p[1] for p in KM.values()]
_sx = (_X1 - _X0) / (max(_xs) - min(_xs))
_sy = (_Y1 - _Y0) / (max(_ys) - min(_ys))
POS = {n: (round(_X0 + (x - min(_xs)) * _sx, 1), round(_Y0 + (y - min(_ys)) * _sy, 1))
       for n, (x, y) in KM.items()}

assert not crossings(list(CABLES), POS), crossings(list(CABLES), POS)
assert not clearance_bad(list(CABLES), POS), clearance_bad(list(CABLES), POS)

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

KRUSKAL_STEP = {frozenset((a, b)): i for i, (a, b, _, act)
                in enumerate([t for t in KRUSKAL if t[3] == "add"], 1)}
PRIM_STEP = {frozenset((u, v)): i for i, (u, v, _) in enumerate(PRIM, 1)}
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
        s += disc(mx, my, tag, fill="accenttwo", size=SMALLNODE + 8)

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


def km(e):
    """The length of a route, whichever way round its endpoints are given."""
    a, b = e
    return CABLES[(a, b)] if (a, b) in CABLES else CABLES[(b, a)]

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


# Rough populations (thousands), used only to size the discs on the map slide so
# that "town size" is something the next slide can visibly throw away.
POP = {"Brno": 380, "Olomouc": 100, "Zlin": 75, "Jihlava": 51,
       "Prostejov": 44, "Trebic": 35, "Znojmo": 34, "Hodonin": 25}
_pmin, _pmax = min(POP.values()) ** 0.5, max(POP.values()) ** 0.5
MAP_SIZE = {n: 28 + (v ** 0.5 - _pmin) / (_pmax - _pmin) * 22 for n, v in POP.items()}
assert all(NODE_MIN_PX <= d <= NODE_MAX_PX for d in MAP_SIZE.values())


def fig_moravia_dark():
    """An actual map: rivers, the southern border, towns sized by population.

    Slide 7 says "rivers, roads, borders, town size -- none of it changes which
    cables to lay", and then erases them. With slide 5 drawing eight bare dots the
    two figures were pixel-identical apart from a corner note, so the abstraction
    step -- the whole point of that slide -- never happened on screen.
    """
    s = ""
    # Geography is drawn in annotation gray, never in accent: accent is the towns,
    # and one colour may not mean two things in the same drawing. Gray is also
    # exactly what the next slide throws away.
    # the Morava, running south past Olomouc and Hodonin
    s += polyline([(800, 340), (784, 290), (770, 232), (758, 172), (744, 116)],
                  color="annot", w=2.6)
    # the Dyje, running east UNDER the Znojmo label (box y 53..109), not through it
    s += polyline([(190, 62), (330, 42), (560, 36), (700, 56)],
                  color="annot", w=2.6)
    # the southern border
    s += polyline([(150, 24), (400, 14), (700, 16), (1010, 26)],
                  color="annot", w=2.0, dash=DASH_LONG)
    for n, (x, y) in POS.items():
        s += disc(x, y, "", fill="accent", size=MAP_SIZE[n])
    for n, (anc, dx, dy) in LABEL_SIDE.items():
        s += text(POS[n][0] + dx, POS[n][1] + dy, NAME[n], anchor=anc)
    return s


def fig_abstract_1():
    return moravia()


def fig_abstract_2():
    return moravia(faint=ALL_CABLES)


def fig_abstract_3():
    return moravia(faint=ALL_CABLES, weights=ALL_CABLES,
                   heavy={("Brno", "Prostejov"): "accenttwo"},
                   )


def fig_moravia_graph():
    return moravia(faint=ALL_CABLES, weights=ALL_CABLES)


def fig_loop_waste():
    p = {"a": (55, 250), "b": (465, 250), "c": (465, 90), "d": (55, 90)}
    e = [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")]
    s = ""
    for x, y in e[:-1]:
        s += seg(p[x], p[y], w=EDGE_W + 1.2)
    s += seg(p["d"], p["a"], color="accenttwo", w=HEAVY_W, dash=DASH)
    mx, my = (p["d"][0] + p["a"][0]) / 2, (p["d"][1] + p["a"][1]) / 2
    s += seg((mx - 15, my - 15), (mx + 15, my + 15), color="accenttwo", w=4.0)
    s += seg((mx - 15, my + 15), (mx + 15, my - 15), color="accenttwo", w=4.0)
    for k, (x, y) in p.items():
        s += disc(x, y, fill="accent")
    return s


def fig_tree_def():
    p = {"r": (235, 280), "a": (110, 190), "b": (360, 190),
         "c": (40, 90), "d": (180, 90), "e": (430, 90)}
    e = [("r", "a"), ("r", "b"), ("a", "c"), ("a", "d"), ("b", "e")]
    s = "".join(seg(p[x], p[y], w=EDGE_W + 1.2) for x, y in e)
    for k, (x, y) in p.items():
        s += disc(x, y, fill="accent")
    return s


def fig_spanning_count():
    return moravia(edges=MST_PAIRS,
                   badge={frozenset(e): str(i) for e, i in KRUSKAL_STEP.items()},
                   extra_text=note(f"8 towns\\\\{MST.number_of_edges()} cables"))


def fig_mst_def():
    return moravia(faint=[e for e in ALL_CABLES if not is_tree_edge(e)],
                   edges=MST_PAIRS,
                   heavy={e: "accenttwo" for e in MST_PAIRS},
                   weights=MST_PAIRS)


# ===========================================================================
#                                Part 2
# ===========================================================================
SORTED_CABLES = sorted(CABLES.items(), key=lambda kv: kv[1])


def fig_kruskal_rule():
    """The thirteen routes laid out cheapest-first: the rule, before the run.

    Drawn as outlined chips, not numbers on a rule: the first version set white
    discs behind the numbers, which is invisible on a white page, so the row read
    as one run-on string with a stray dash at the front.
    """
    n = len(SORTED_CABLES)
    x0, x1, y = 70, 1030, 200
    step = (x1 - x0) / (n - 1)
    r = 32
    s = ""
    for i, ((a, b), w) in enumerate(SORTED_CABLES):
        x = x0 + i * step
        col = "accenttwo" if i == 0 else "annot"
        s += (f"\\draw[line width={3.0 if i == 0 else 2.0}bp,draw={col},fill=white] "
              f"({x:.1f},{y}) circle ({r}bp);\n")
        s += text(x, y, str(w), color="accenttwo" if i == 0 else "black")
    s += seg((x0 - r - 10, y - r - 26), (x1 + r + 10, y - r - 26), color="annot",
             w=2.4, arrow="-{Stealth[length=15bp,width=12bp]}")
    s += text(x0 - r - 10, y - r - 44, "cheapest", color="accenttwo",
              anchor="north west")
    s += text(x1 + r + 10, y - r - 44, "dearest", color="annot", anchor="north east")
    return s


def _kruskal_state(step):
    """Edges present after `step` decisions of Kruskal's trace."""
    added = [(a, b) for a, b, _, act in KRUSKAL[:step] if act == "add"]
    return added


def fig_kruskal_skip():
    added = _kruskal_state(5)
    a, b, w = SKIPPED
    cycle = [("Prostejov", "Olomouc"), ("Prostejov", "Zlin")]
    return moravia(
        faint=[e for e in ALL_CABLES if e not in added and e != (a, b)],
        edges=added,
        heavy={**{e: "accentthree" for e in cycle}, (a, b): "accenttwo"},
        struck=[(a, b)],
        weights=[(a, b)] + cycle,
        extra_text=note(f"{w} km"))


def fig_kruskal_worksheet():
    return moravia(faint=ALL_CABLES, weights=ALL_CABLES)


def fig_kruskal_answer():
    a, b, _ = SKIPPED
    return moravia(faint=[(a, b)], edges=MST_PAIRS,
                   heavy={(a, b): "accenttwo"}, struck=[(a, b)],
                   badge={tuple(e): str(i) for e, i in KRUSKAL_STEP.items()},
                   extra_text=note(f"{MST_TOTAL} km"))


def fig_prim_rule():
    out = [(u, v) for u, v in ALL_CABLES if "Brno" in (u, v)]
    cheapest = min(out, key=lambda e: CABLES[e])
    return moravia(faint=[e for e in ALL_CABLES if e not in out],
                   heavy={**{e: "annot" for e in out}, cheapest: "accenttwo"},
                   weights=out, rings={"Brno": "accenttwo"},
                   )


def fig_prim_worksheet():
    return moravia(faint=ALL_CABLES, weights=ALL_CABLES, rings={"Brno": "accenttwo"})


def fig_prim_vs_kruskal():
    """Same seven cables, two orders — shown as two rows, not two graphs."""
    kr = [w for _, _, w, act in KRUSKAL if act == "add"]
    pr = [w for _, _, w in PRIM]
    assert sorted(kr) == sorted(pr) and sum(kr) == sum(pr) == MST_TOTAL
    x0, x1 = 250, 1020
    step = (x1 - x0) / (len(kr) - 1)
    ytop, ybot = 250, 90
    s = ""
    for i, w in enumerate(kr):
        s += seg((x0 + i * step, ytop - 28),
                 (x0 + pr.index(w) * step, ybot + 28), color="annot", w=1.8)
    for row, (vals, col, lab) in enumerate(((kr, "annot", "Kruskal"),
                                            (pr, "accenttwo", "Prim"))):
        y = (ytop, ybot)[row]
        s += text(x0 - 60, y, lab, color=col, anchor="east")
        for i, w in enumerate(vals):
            x = x0 + i * step
            s += disc(x, y, "", fill="white", size=SMALLNODE + 22)
            s += text(x, y, str(w), color=col)
    return s


def fig_cut_property():
    p = {"a": (40, 255), "b": (40, 85), "c": (480, 255), "d": (480, 85),
         "e": (260, 170)}
    s = seg(p["a"], p["b"], w=EDGE_W + 1.2) + seg(p["c"], p["d"], w=EDGE_W + 1.2)
    s += seg(p["a"], p["e"], color="annot", w=EDGE_W + 1.2)
    s += seg(p["b"], p["e"], color="annot", w=EDGE_W + 1.2)
    s += seg(p["e"], p["c"], color="accenttwo", w=HEAVY_W)
    s += seg(p["e"], p["d"], color="annot", w=EDGE_W + 1.2)
    s += seg((370, 290), (370, 30), color="annot", w=2.4, dash=DASH_LONG)
    for k, (x, y) in p.items():
        s += disc(x, y, fill="accent")
    s += text(370, 300, "any cut", color="annot", anchor="south")
    return s


TIE_EDGE = ("Olomouc", "Zlin")
TIE_WEIGHT = 49
TIE_RIVAL = ("Prostejov", "Zlin")
assert CABLES[TIE_RIVAL] == TIE_WEIGHT


def _tie_optima():
    """With the tie in place, brute-force every optimal spanning tree."""
    w = dict(CABLES)
    w[TIE_EDGE] = TIE_WEIGHT
    best, opts = None, []
    for combo in itertools.combinations(w.items(), 7):
        h = nx.Graph()
        h.add_nodes_from(G)
        h.add_edges_from(e for e, _ in combo)
        if not nx.is_connected(h):
            continue
        tot = sum(v for _, v in combo)
        if best is None or tot < best:
            best, opts = tot, [frozenset(e for e, _ in combo)]
        elif tot == best:
            opts.append(frozenset(e for e, _ in combo))
    return best, opts


TIE_TOTAL, TIE_OPTIMA = _tie_optima()
assert TIE_TOTAL == MST_TOTAL and len(TIE_OPTIMA) == 2, (TIE_TOTAL, len(TIE_OPTIMA))
TIE_SHARED = set.intersection(*(set(o) for o in TIE_OPTIMA))
TIE_DIFFER = sorted(set.union(*(set(o) for o in TIE_OPTIMA)) - TIE_SHARED)
assert len(TIE_SHARED) == 6 and set(TIE_DIFFER) == {TIE_EDGE, TIE_RIVAL}


def fig_tie_graph():
    return moravia(faint=ALL_CABLES, weights=ALL_CABLES,
                   weight_override={TIE_EDGE: TIE_WEIGHT},
                   heavy={TIE_EDGE: "accenttwo", TIE_RIVAL: "accenttwo"},
                   )


def fig_tie_two_trees():
    return moravia(faint=[e for e in ALL_CABLES if e not in TIE_SHARED
                          and e not in TIE_DIFFER],
                   edges=sorted(TIE_SHARED),
                   heavy={TIE_DIFFER[0]: "accenttwo", TIE_DIFFER[1]: "accentthree"},
                   weights=TIE_DIFFER,
                   weight_override={TIE_EDGE: TIE_WEIGHT},
                   extra_text=note(f"both {TIE_TOTAL} km"))


def fig_boruvka_rounds():
    r1 = [(a, b) for a, b, _ in BORUVKA_ROUNDS[0]]
    r2 = [(a, b) for a, b, _ in BORUVKA_ROUNDS[1]]
    return moravia(edges=MST_PAIRS,
                   heavy={**{e: "accenttwo" for e in r1},
                          **{e: "accentthree" for e in r2}},
                   )


# ===========================================================================
#                                Part 3
# ===========================================================================
def fig_mst_alone():
    return moravia(edges=MST_PAIRS, weights=MST_PAIRS,
                   extra_text=note(f"{MST_TOTAL} km"))


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


def fig_tree_bridges():
    route = nx.shortest_path(MST, "Jihlava", "Zlin")
    pairs = list(zip(route, route[1:]))
    return moravia(edges=MST_PAIRS,
                   heavy={p: "accenttwo" for p in pairs},
                   )


def fig_real_grid_mesh():
    """A drawn meshed grid: two independent routes between the same pair."""
    cols_, rows = 7, 3
    x0, y0, dx, dy = 110, 90, 145, 95
    p = {(i, j): (x0 + i * dx, y0 + j * dy) for i in range(cols_) for j in range(rows)}
    e = [((i, j), (i + 1, j)) for i in range(cols_ - 1) for j in range(rows)]
    e += [((i, j), (i, j + 1)) for i in range(cols_) for j in range(rows - 1)]
    s = "".join(seg(p[a], p[b], color="black", w=EDGE_W) for a, b in e)
    top = [(0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (6, 1)]
    bot = [(0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (6, 1)]
    for path, col in ((top, "accenttwo"), (bot, "accentthree")):
        s += "".join(seg(p[a], p[b], color=col, w=HEAVY_W)
                     for a, b in zip(path, path[1:]))
    for k, (x, y) in p.items():
        s += disc(x, y, fill="accent")
    for k in ((0, 1), (6, 1)):
        s += ring(p[k][0], p[k][1], color="accenttwo")
    return s


def fig_connectivity_def():
    """Both largest pieces are highlighted, because they are TIED.

    Removing Brno leaves 3 + 3 + 1. Ringing only one of the two 3-node pieces --
    whichever `max` happened to return -- told the room that piece was bigger.
    """
    pieces = sorted(nx.connected_components(
        nx.subgraph_view(MST, filter_node=lambda n: n != "Brno")), key=len, reverse=True)
    top = max(len(p) for p in pieces)
    biggest = [p for p in pieces if len(p) == top]
    assert len(biggest) == 2 and top == 3, [len(p) for p in pieces]
    marked = set().union(*biggest)
    return moravia(edges=MST_PAIRS, removed=["Brno"],
                   heavy={(a, b): "accenttwo" for a, b in MST_PAIRS
                          if a in marked and b in marked},
                   rings={n: "accenttwo" for n in marked},
                   extra_text=note(f"{top} / 8"))


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


def fig_r_index():
    X, Y = _XY()
    pts = profile_points(ATTACK_PROFILE)
    s = fill_poly([(pts[0][0], Y(0))] + pts + [(pts[-1][0], Y(0))],
                  color="accenttwo", opacity=0.22)
    s += profile_axes()
    s += polyline(pts, color="accenttwo", w=4.0)
    s += "".join(dot(x, y, "accenttwo") for x, y in pts)
    s += text(LAB_X, Y(0.55), f"targeted\\\\$R = {float(R_ATTACK):.2f}$",
              color="accenttwo", anchor="west")
    return s


def fig_profile_random():
    s = profile_axes()
    pts = profile_points(RANDOM_PROFILE)
    s += polyline(pts, color="accentthree", w=4.0)
    s += "".join(dot(x, y, "accentthree") for x, y in pts)
    X, Y = _XY()
    s += text(LAB_X, Y(0.55), f"random\\\\$R = {float(R_RANDOM):.2f}$",
              color="black", anchor="west")
    return s


def fig_profile_both():
    s = profile_axes()
    X, Y = _XY()
    for prof, col, lab, ly in ((RANDOM_PROFILE, "accentthree", "random", 0.72),
                               (ATTACK_PROFILE, "accenttwo", "targeted", 0.22)):
        pts = profile_points(prof)
        s += polyline(pts, color=col, w=4.0)
        s += "".join(dot(x, y, col) for x, y in pts)
        s += text(LAB_X, Y(ly), f"{lab}\\\\$R = {float(r_index(prof)):.2f}$",
                  color="black" if col == "accentthree" else col, anchor="west")
    s += text(X(0.52), Y(0.36),
              f"{float(R_RANDOM / R_ATTACK):.1f}$\\times$ the damage", color="black")
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


def fig_fixed_vs_adaptive():
    X, Y = _XY()
    s = sim_axes()
    s += sim_curve(("er", "fixed"), "accentthree")
    s += sim_curve(("er", "targeted"), "accenttwo")
    s += text(LAB_X, Y(0.74), "fixed list\\\\gone at " + pct(ER_FIXED_C),
              color="black", anchor="west")
    s += text(LAB_X, Y(0.26), "re-ranked\\\\gone at " + pct(ER_TARG_C),
              color="accenttwo", anchor="west")
    return s


def fig_demo_still():
    """A drawn stand-in for the web demo, captioned as such on the slide."""
    p = {0: (70, 250), 1: (150, 170), 2: (70, 90), 3: (220, 250), 4: (220, 90),
         5: (150, 320)}
    e = [(0, 1), (1, 2), (1, 3), (1, 4), (3, 4), (0, 5), (5, 1)]
    s = "".join(seg(p[a], p[b], w=EDGE_W) for a, b in e)
    for k, (x, y) in p.items():
        s += disc(x, y, fill="accent", size=SMALLNODE)
    s += ring(p[1][0], p[1][1], size=SMALLNODE, color="accenttwo")
    x0, x1, y0, y1 = 320, 470, 110, 300
    s += seg((x0, y0), (x1, y0), color="annot", w=2.0)
    s += seg((x0, y0), (x0, y1), color="annot", w=2.0)
    s += polyline([(x0, y1), (x0 + 40, y1 - 90), (x0 + 80, y0 + 40), (x1, y0 + 6)],
                  color="accenttwo", w=3.4)
    return s


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


def puddle_body(p, field, y0, label=None, cell=PUD_CELL):
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
    s += text(x0 + cols * cell - 2, top, "largest puddle " + pct(frac),
              color="accenttwo", anchor="south east")
    return s, frac


def fig_puddle_low():
    return puddle_body(0.40, PUD_FIELD[:22], 66)[0]


def fig_puddle_widget():
    s, _ = puddle_body(0.65, PUD_FIELD[:16], 108)
    x0, x1, y = 300, 800, 44
    s += seg((x0, y), (x1, y), color="annot", w=3.0)
    s += dot(x0 + 0.60 * (x1 - x0), y, "accenttwo", d=28)
    s += text(x1 + 20, y, "drag $p$", color="accenttwo", anchor="west")
    return s


_SMALL = (9, PUD_COLS)
FIELD_A = np.random.default_rng(5).random(_SMALL)
FIELD_B = np.random.default_rng(23).random(_SMALL)


def fig_order_irrelevant():
    """Two different yards, the same fraction wet -- the same answer.

    At p = 0.65 on the old small yards this drew 24% beside 17% under the words
    "the same answer", and the assertion (< 0.20) was loose enough to allow it.
    Well above the threshold the two agree to ~2 points, which is the claim; near
    p_c the finite-size scatter is real and this slide must not stand there.
    """
    p = 0.75
    a, fa = puddle_body(p, FIELD_A, 206, label="one yard", cell=10)
    b, fb = puddle_body(p, FIELD_B, 40, label="another yard", cell=10)
    assert abs(fa - fb) < 0.08, f"the two yards disagree: {fa:.0%} vs {fb:.0%}"
    return a + b


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
    s = axes(X0, X1, Y0, Y1, "fraction of stones wet, $p$", "largest puddle",
             [(v, X(v)) for v in (0.3, 0.45, 0.6, 0.75)],
             [(v, Y(v)) for v in (0, 0.5, 1.0)],
             xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    s += seg((X(PC_LITERATURE), Y0), (X(PC_LITERATURE), Y1),
             color="annot", w=2.6, dash=DASH)
    s += text(X(PC_LITERATURE) - 14, Y(0.86), f"$p_c \\approx {PC_LITERATURE:.2f}$",
              color="annot", anchor="east")
    s += polyline([(X(p), Y(v)) for p, v in zip(PERC_P, PERC_S)],
                  color="accenttwo", w=4.0)
    s += text(LAB_X, Y(0.72), "one puddle\\\\spans the yard", color="accenttwo",
              anchor="west")
    s += text(X(0.36), Y(0.62), "scattered\\\\pools", color="annot")
    return s


def fig_reverse_percolation():
    y = 200
    s = seg((150, y), (950, y), color="annot", w=3.0)
    for v, lab in ((150, "empty"), (950, "full")):
        s += seg((v, y - 12), (v, y + 12), color="annot", w=2.6)
        s += text(v, y - 24, lab, color="annot", anchor="north")
    s += seg((300, y + 60), (830, y + 60), color="accent", w=4.0,
             arrow="-{Stealth[length=15bp,width=12bp]}")
    s += text(565, y + 74, "add nodes: the giant component appears",
              color="accent", anchor="south")
    s += seg((830, y - 90), (300, y - 90), color="accenttwo", w=4.0,
             arrow="-{Stealth[length=15bp,width=12bp]}")
    s += text(565, y - 104, "remove nodes: the giant component dies",
              color="accenttwo", anchor="north")
    return s


# ===========================================================================
#                                Part 5
# ===========================================================================
# A small network used for q(k): degrees 4, 3, 2, 1, 1, 1 -- printed, not typed.
QK_POS = {"h": (250, 225), "a": (70, 330), "b": (70, 120), "c": (430, 330),
          "e": (430, 120), "d": (250, 120)}
QK_EDGES = [("h", "a"), ("h", "b"), ("h", "c"), ("h", "e"), ("c", "d"), ("a", "b")]
QK_G = nx.Graph(QK_EDGES)
QK_DEG = dict(QK_G.degree())
QK_KAPPA = kappa_of(QK_DEG.values())
assert QK_DEG["h"] == 4 and sum(QK_DEG.values()) == 2 * len(QK_EDGES)
assert not clearance_bad(QK_EDGES, QK_POS)


def qk_graph(highlight=None, show_deg=False):
    s = "".join(seg(QK_POS[a], QK_POS[b],
                    color="accenttwo" if highlight in ((a, b), (b, a)) else "black",
                    w=HEAVY_W if highlight in ((a, b), (b, a)) else EDGE_W)
                for a, b in QK_EDGES)
    for n, (x, y) in QK_POS.items():
        s += disc(x, y, str(QK_DEG[n]) if show_deg else "", fill="accent")
    return s


def fig_follow_edge():
    """The arrowhead sits ON the highlighted edge, ending at the far node's border.

    Offsetting it by 34bp drew a second red mark parallel to the edge, starting and
    ending in white space and touching neither node -- a ghost edge with nothing on
    the slide to explain it.
    """
    s = qk_graph(highlight=("h", "c"))
    (x1, y1), (x2, y2) = QK_POS["h"], QK_POS["c"]
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    s += seg((x1 + ux * (NODE / 2 + 2), y1 + uy * (NODE / 2 + 2)),
             (x2 - ux * (NODE / 2 + 4), y2 - uy * (NODE / 2 + 4)),
             color="accenttwo", w=HEAVY_W,
             arrow="-{Stealth[length=16bp,width=13bp]}")
    return s


def fig_qk_bias():
    """Every edge contributes two ends; a hub owns more of the pile."""
    order = ["h", "c", "a", "b", "d", "e"]
    x0, step, ytop = 210, 148, 300
    s = ""
    for i, n in enumerate(order):
        x = x0 + i * step
        s += disc(x, ytop, "", fill="accent")
        s += text(x, ytop + 34, f"$k = {QK_DEG[n]}$", color="black", anchor="south")
        for j in range(QK_DEG[n]):
            s += dot(x, ytop - 66 - j * 38, "accenttwo", d=28)
    s += text(150, ytop - 62, "edge", color="accenttwo", anchor="east")
    s += text(150, ytop - 96, "ends", color="accenttwo", anchor="east")
    s += text(620, 40, f"the hub owns 4 of the {2 * len(QK_EDGES)} ends",
              color="accenttwo")
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


def fig_branching():
    s = _arrival(230, 200)
    body, lvl = fan_tree(230, 300, 200, 200)
    s += body
    s += text(880, 60, "$\\kappa - 1$ onward", color="accenttwo")
    return s


def fig_dilution():
    s = _arrival(230, 200)
    body, lvl = fan_tree(230, 300, 200, 200, dead={(1, 1), (2, 0)})
    s += body
    s += text(880, 60, "$(1-f)(\\kappa-1)$ survive", color="accenttwo")
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


def small_graph(pos, edges, at, scale=1.0, labels=None, col="accent",
                node=SMALLNODE, highlight=()):
    dx, dy = at
    P = {k: (dx + x * scale, dy + y * scale) for k, (x, y) in pos.items()}
    s = "".join(seg(P[a], P[b],
                    color="accenttwo" if (a, b) in highlight or (b, a) in highlight
                    else "black", w=EDGE_W + 1.0) for a, b in edges)
    for k, (x, y) in P.items():
        s += disc(x, y, (labels or {}).get(k, ""), fill=col, size=node)
    return s, P


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


def _kappa_row(show):
    s = ""
    for i, ((nm, (p, e), sc), kv) in enumerate(zip(KAPPA_CASES, KAPPA_VALUES)):
        cx = 190 + i * 340
        degs = dict(nx.Graph(e).degree())
        body, _ = small_graph(p, e, (cx, 230), scale=sc,
                              labels={k: str(degs[k]) for k in p}, node=NODE)
        s += body
        s += text(cx, 90, nm, color="black")
        # only the threshold case is accent-2; the deck's text says why, and an
        # extra sentence here pushed the drawing past the height budget
        col = ("accenttwo" if kv == 2 else "black") if show else "annot"
        val = f"{float(kv):g}" if kv.denominator != 1 else str(kv)
        s += text(cx, 40, f"$\\kappa = {val}$" if show else "$\\kappa = \\;?$",
                  color=col)
    return s


def fig_kappa_worksheet():
    return _kappa_row(False)


def fig_kappa_answer():
    return _kappa_row(True)


def fig_fc_formula():
    X0, X1, Y0, Y1 = PLOT["x0"], PLOT["x1"], PLOT["y0"], PLOT["y1"]
    kappa = 5.0

    def X(f):
        return X0 + f * (X1 - X0)

    def Y(v):
        return Y0 + v / 4.0 * (Y1 - Y0)
    fc = 1 - 1 / (kappa - 1)
    s = axes(X0, X1, Y0, Y1, "fraction removed, $f$", "branches per step",
             [(v, X(v)) for v in (0, 0.25, 0.5, 0.75, 1.0)],
             [(v, Y(v)) for v in (0, 1, 2, 3, 4)],
             xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    s += seg((X0, Y(1)), (X1, Y(1)), color="annot", w=2.6, dash=DASH)
    s += polyline([(X(f), Y((1 - f) * (kappa - 1))) for f in (0, 1)],
                  color="accenttwo", w=4.0)
    s += seg((X(fc), Y0), (X(fc), Y(1)), color="accenttwo", w=2.6, dash=DASH)
    s += dot(X(fc), Y(1), "accenttwo", d=20)
    s += text(X(fc) + 16, Y(1.9), f"$f_c = {fc:.2f}$", color="accenttwo",
              anchor="west")
    s += text(LAB_X, Y(2.6), f"$\\kappa = {kappa:g}$", color="accenttwo", anchor="west")
    s += text(LAB_X, Y(0.7), "1 = break-even", color="annot", anchor="west")
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
    s += text(LAB_X, Y(0.86), "denser\\\\is tougher", color="accenttwo", anchor="west")
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


# ===========================================================================
#                                Part 6
# ===========================================================================
def fig_sim_random():
    X, Y = _XY()
    s = sim_axes()
    s += sim_curve(("er", "random"), "accentthree")
    s += sim_curve(("sf", "random"), "accenttwo")
    s += text(LAB_X, Y(0.72), "hubs\\\\" + pct(SF_RAND_C), color="accenttwo",
              anchor="west")
    s += text(LAB_X, Y(0.30), "random net\\\\" + pct(ER_RAND_C), color="black",
              anchor="west")
    return s


def fig_sim_targeted():
    X, Y = _XY()
    s = sim_axes()
    s += sim_curve(("er", "targeted"), "accentthree")
    s += sim_curve(("sf", "targeted"), "accenttwo")
    s += text(LAB_X, Y(0.72), "hubs\\\\" + pct(SF_TARG_C), color="accenttwo",
              anchor="west")
    s += text(LAB_X, Y(0.30), "random net\\\\" + pct(ER_TARG_C), color="black",
              anchor="west")
    return s


def fig_robust_fragile():
    X, Y = _XY()
    s = sim_axes()
    s += sim_curve(("er", "random"), "accentthree")
    s += sim_curve(("er", "targeted"), "accentthree", dash=DASH)
    s += sim_curve(("sf", "random"), "accenttwo")
    s += sim_curve(("sf", "targeted"), "accenttwo", dash=DASH)
    s += text(LAB_X, Y(0.86), "hubs,\\\\random", color="accenttwo", anchor="west")
    s += text(LAB_X, Y(0.52), "random net,\\\\random", color="black",
              anchor="west")
    s += text(LAB_X, Y(0.20), "attacked\\\\(dashed)", color="black", anchor="west")
    return s


def fig_efficiency_security():
    star_p = {0: (0, 0), **{i: p for i, p in enumerate(ring_pos(6).values(), 1)}}
    star_e = [(0, i) for i in range(1, 7)]
    s, P = small_graph(star_p, star_e, (250, 220), scale=115, node=NODE)
    s += ring(P[0][0], P[0][1], color="accenttwo")
    s += text(250, 40, "one node holds it up", color="accenttwo")
    mesh_p = ring_pos(7)
    mesh_e = [(i, (i + 1) % 7) for i in range(7)] + [(i, (i + 2) % 7) for i in range(7)]
    s2, _ = small_graph(mesh_p, mesh_e, (830, 220), scale=115, node=NODE)
    s += s2
    s += text(830, 40, "no single point", color="black")
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


def fig_design_principles():
    """Degrees before and after the two extra cables, as a dot plot.

    Authored for the `cols` column so it can sit beside the five principles. The
    Moravian map is a full-width figure; putting it in a column rendered it at 48%
    and dropped its discs to 19px.
    """
    before = dict(MST.degree())
    after = dict(MST2.degree())
    towns = sorted(before, key=lambda n: (before[n], after[n], n))
    # "Even out the degrees" is a claim, so check it. The *range* does not move
    # (3 and 1 both survive); what improves is the spread and the number of towns
    # left on a single cable, which is what the dot plot actually shows.
    var = lambda d: float(np.var(list(d.values())))
    leaves = lambda d: sum(1 for v in d.values() if v == 1)
    assert var(after) < var(before), (var(before), var(after))
    assert leaves(after) < leaves(before), (leaves(before), leaves(after))

    y0, dy = 100, 34
    xs = {k: 280 + (k - 1) * 90 for k in range(1, 4)}
    s = seg((xs[1] - 40, 70), (xs[3] + 40, 70), color="annot", w=2.2)
    for k, x in xs.items():
        s += seg((x, 62), (x, 78), color="annot", w=2.0)
        s += text(x, 54, str(k), color="annot", anchor="north")
    for i, n in enumerate(towns):
        y = y0 + i * dy
        s += text(200, y, NAME[n], color="black", anchor="east")
        b, a = before[n], after[n]
        if a != b:
            s += seg((xs[b], y), (xs[a], y), color="annot", w=2.0, dash=DASH)
        s += dot(xs[b], y, "annot", d=20)
        s += dot(xs[a], y, "accentthree", d=26)
    return s


def fig_build_it_back():
    new = [(a, b) for a, b, _ in REDUNDANT]
    return moravia(edges=MST_PAIRS,
                   heavy={e: "accentthree" for e in new},
                   extra_text=note("1926\\\\today", color="black"))


# ===========================================================================
#                                Part 7
# ===========================================================================
def _ring_case(show, cut=False):
    p = ring_pos(6, r=1.0, ry=0.82, start=0.0)
    e = [(i, (i + 1) % 6) for i in range(6)]
    gone = 3 if cut else None
    s = "".join(seg((260 + p[a][0] * 196, 190 + p[a][1] * 196),
                    (260 + p[b][0] * 196, 190 + p[b][1] * 196),
                    color="black", w=EDGE_W + 1.0)
                for a, b in e if gone not in (a, b))
    for i, (x, y) in p.items():
        X, Y = 260 + x * 196, 190 + y * 196
        if i == gone:
            s += opendisc(X, Y, "accenttwo")
            s += seg((X - 12, Y - 12), (X + 12, Y + 12), color="accenttwo", w=3.6)
            s += seg((X - 12, Y + 12), (X + 12, Y - 12), color="accenttwo", w=3.6)
        else:
            s += disc(X, Y, "" if cut else "2", fill="accent")
    s += text(260, 190, f"$\\kappa = {KAPPA_VALUES[0]}$" if show else "$\\kappa = \\;?$",
              color="accenttwo" if show else "annot")
    return s


def fig_ring_q():
    return _ring_case(False)


def fig_ring_a():
    """The INTACT ring, because kappa = 2 is a fact about the intact ring.

    Drawing the ring after the cut and printing kappa = 2 on it put the wrong
    number on the graph: the cut leaves a 5-node chain with degrees 1,2,2,2,1 and
    kappa = 7/4 -- this deck's own value for "a path", three slides earlier. What
    one cut does is in the body text, where it does not have to be drawn wrong.
    """
    return _ring_case(True)


ER1 = nx.gnm_random_graph(14, 7, seed=4)
ER1_KAPPA = Fraction(sum(d * d for _, d in ER1.degree()),
                     sum(d for _, d in ER1.degree()))


def _er1_case(show):
    pos = ring_pos(14, r=1.0, ry=0.68, start=0.0)
    s, _ = small_graph({i: pos[i] for i in ER1}, list(ER1.edges()), (260, 200),
                       scale=200, node=SMALLNODE)
    s += text(260, 30, "$\\langle k \\rangle = 1$" if not show else "$\\kappa = 2$",
              color="annot" if not show else "accenttwo")
    return s


def fig_er1_q():
    return _er1_case(False)


def fig_er1_a():
    return _er1_case(True)


BW_BRIDGE = 6
BW_POS = {0: (190, 200), 3: (320, 200), 1: (230, 310), 2: (85, 268),
          4: (85, 132), 5: (230, 90),
          BW_BRIDGE: (550, 200),
          7: (790, 200), 8: (920, 200), 9: (830, 310), 10: (685, 268),
          11: (685, 132), 12: (830, 90)}
BW_EDGES = ([(0, i) for i in (1, 2, 3, 4, 5)]
            + [(3, BW_BRIDGE), (BW_BRIDGE, 7)]
            + [(7, i) for i in (8, 9, 10, 11, 12)])
BW_G = nx.Graph(BW_EDGES)
BW_HUB = max(BW_G.degree(), key=lambda kv: kv[1])[0]
assert BW_G.degree(BW_BRIDGE) == 2 and nx.is_connected(BW_G)
assert BW_G.degree(BW_HUB) >= 6 and not clearance_bad(BW_EDGES, BW_POS)


def _bw(removed=(), note_text=None, degrees=True, ring_bridge=True):
    """Degrees are printed inside the discs: no external label, no spare height."""
    s = "".join(seg(BW_POS[a], BW_POS[b], color="black", w=EDGE_W)
                for a, b in BW_EDGES if a not in removed and b not in removed)
    for n, (x, y) in BW_POS.items():
        if n in removed:
            s += opendisc(x, y, "accenttwo")
            s += seg((x - 12, y - 12), (x + 12, y + 12), color="accenttwo", w=3.6)
            s += seg((x - 12, y + 12), (x + 12, y - 12), color="accenttwo", w=3.6)
        else:
            s += disc(x, y, str(BW_G.degree(n)) if degrees else "", fill="accent")
    if ring_bridge:
        s += ring(BW_POS[BW_BRIDGE][0], BW_POS[BW_BRIDGE][1], color="accenttwo")
    if note_text:
        s += text(550, 30, note_text, color="accenttwo")
    return s


def fig_betweenness_q():
    """No ring. The ringed node was the answer to the NEXT slide."""
    return _bw(ring_bridge=False)


def fig_betweenness_a():
    """The bridge removed, and the two halves it was holding together.

    The first version printed a degree in every disc and claimed the hub result in
    a caption while drawing the bridge result -- so the slide showed one scenario
    and asserted two, and the removed node's neighbour read as "the degree-2 node".
    """
    parts = sorted(nx.connected_components(
        nx.subgraph_view(BW_G, filter_node=lambda n: n != BW_BRIDGE)), key=len,
        reverse=True)
    after_hub = len(max(nx.connected_components(
        nx.subgraph_view(BW_G, filter_node=lambda n: n != BW_HUB)), key=len))
    assert len(parts) == 2 and len(parts[0]) < after_hub, (parts, after_hub)
    s = _bw(removed=[BW_BRIDGE], degrees=False)
    for part in parts:
        xs = [BW_POS[n][0] for n in part]
        s += text(sum(xs) / len(xs), 30, str(len(part)), color="accenttwo")
    return s


TRI_POS = {i: p for i, p in enumerate(
    [(0, 0), (1.1, 0.55), (2.2, 0), (1.1, -0.55), (3.3, 0.55), (3.3, -0.55)])}
TRI_EDGES = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (2, 4), (4, 5), (5, 2), (1, 4)]


def _tri(show):
    s, P = small_graph(TRI_POS, TRI_EDGES, (70, 190), scale=110, node=NODE)
    if show:
        loop = [(0, 1), (1, 2), (2, 0)]
        s += "".join(seg(P[a], P[b], color="accenttwo", w=HEAVY_W) for a, b in loop)
        s += text(280, 30, "back where it started", color="accenttwo")
    else:
        s += text(280, 30, "triangles everywhere", color="annot")
    return s


def fig_triangles_q():
    return _tri(False)


def fig_triangles_a():
    return _tri(True)


# ===========================================================================
#                              Wrap-up
# ===========================================================================
def fig_recap():
    """One drawing, three numbers where they happened -- not four bordered cells.

    The first version was a row of four boxed header/value pairs: a 2x4 table, which
    L2 makes a Blocker, on a slide titled "Module 03 in one picture".
    """
    new = [(a, b) for a, b, _ in REDUNDANT]
    worst = connectivity(MST, ["Brno"])
    s = moravia(edges=MST_PAIRS,
                heavy={e: "accentthree" for e in new},
                removed=["Brno"])
    s += note(f"{MST_TOTAL} km", color="accent", at=(24, 72))
    s += note(f"{int(worst * 8)}/8", color="accenttwo", at=(470, 72))
    s += note(f"$+{EXTRA_KM}$ km", color="black", at=(850, 72))
    return s


def fig_m04_teaser():
    """Same pile-of-edge-ends as qk-bias, at column width.

    Discs at NODE and dots at 28bp: at SMALLNODE and 18bp they landed 18px on the
    slide, under the 26px floor, which the node-size gate could not see until it
    was taught to find discs by colour rather than by darkness.
    """
    order = ["h", "c", "a", "b", "e", "d"]
    x0, step, ytop = 175, 62, 320
    s = text(150, ytop, "people", color="accent", anchor="east")
    s += text(150, ytop - 96, "friend-\\\\ships", color="accenttwo", anchor="east")
    for i, n in enumerate(order):
        x = x0 + i * step
        s += disc(x, ytop, "", fill="accent")
        for j in range(QK_DEG[n]):
            s += dot(x, ytop - 52 - j * 36, "accenttwo", d=28)
    return s


FIGURES = [
    ("moravia-dark", fig_moravia_dark, "full", FULL_H),
    ("abstract-1", fig_abstract_1, "full", FULL_H),
    ("abstract-2", fig_abstract_2, "full", FULL_H),
    ("abstract-3", fig_abstract_3, "full", FULL_H),
    ("moravia-graph", fig_moravia_graph, "full", FULL_H),
    ("loop-waste", fig_loop_waste, "col", 320),
    ("tree-def", fig_tree_def, "col", 330),
    ("spanning-count", fig_spanning_count, "full", FULL_H),
    ("mst-def", fig_mst_def, "full", FULL_H),
    ("kruskal-rule", fig_kruskal_rule, "full", 300),
    ("kruskal-skip", fig_kruskal_skip, "full", FULL_H),
    ("kruskal-worksheet", fig_kruskal_worksheet, "full", FULL_H),
    ("kruskal-answer", fig_kruskal_answer, "full", FULL_H),
    ("prim-rule", fig_prim_rule, "full", FULL_H),
    ("prim-worksheet", fig_prim_worksheet, "full", FULL_H),
    ("prim-vs-kruskal", fig_prim_vs_kruskal, "full", 380),
    ("cut-property", fig_cut_property, "col", 350),
    ("tie-graph", fig_tie_graph, "full", FULL_H),
    ("tie-two-trees", fig_tie_two_trees, "full", FULL_H),
    ("boruvka-rounds", fig_boruvka_rounds, "full", FULL_H),
    ("mst-alone", fig_mst_alone, "full", FULL_H),
    ("mst-blank", fig_mst_blank, "full", FULL_H),
    ("brno-removed", fig_brno_removed, "full", FULL_H),
    ("tree-bridges", fig_tree_bridges, "full", FULL_H),
    ("real-grid-mesh", fig_real_grid_mesh, "full", 400),
    ("connectivity-def", fig_connectivity_def, "full", FULL_H),
    ("r-index", fig_r_index, "full", 420),
    ("profile-random", fig_profile_random, "full", 420),
    ("profile-both", fig_profile_both, "full", 420),
    ("fixed-vs-adaptive", fig_fixed_vs_adaptive, "full", 420),
    ("demo-still", fig_demo_still, "col", 360),
    ("puddle-low", fig_puddle_low, "full", 440),
    ("puddle-widget", fig_puddle_widget, "full", 460),
    ("order-irrelevant", fig_order_irrelevant, "full", 420),
    ("phase-transition", fig_phase_transition, "full", 420),
    ("reverse-percolation", fig_reverse_percolation, "full", 380),
    ("follow-edge", fig_follow_edge, "col", 420),
    ("qk-bias", fig_qk_bias, "full", 400),
    ("kappa-def", fig_kappa_def, "col", 420),
    ("branching", fig_branching, "full", 400),
    ("molloy-reed", fig_molloy_reed, "full", 400),
    ("kappa-worksheet", fig_kappa_worksheet, "full", 380),
    ("kappa-answer", fig_kappa_answer, "full", 420),
    ("dilution", fig_dilution, "full", 400),
    ("fc-formula", fig_fc_formula, "full", 420),
    ("fc-poisson", fig_fc_poisson, "full", 420),
    ("fc-scalefree", fig_fc_scalefree, "full", 420),
    ("sim-random", fig_sim_random, "full", 420),
    ("sim-targeted", fig_sim_targeted, "full", 420),
    ("robust-fragile", fig_robust_fragile, "full", 420),
    ("efficiency-security", fig_efficiency_security, "full", 400),
    ("mst-blank-design", fig_mst_blank_design, "full", FULL_H),
    ("redundant-answer", fig_redundant_answer, "full", FULL_H),
    ("design-principles", fig_design_principles, "col", 400),
    ("build-it-back", fig_build_it_back, "full", FULL_H),
    ("ring-q", fig_ring_q, "col", 420),
    ("ring-a", fig_ring_a, "col", 420),
    ("er1-q", fig_er1_q, "col", 420),
    ("er1-a", fig_er1_a, "col", 420),
    ("betweenness-q", fig_betweenness_q, "full", 400),
    ("betweenness-a", fig_betweenness_a, "full", 420),
    ("triangles-q", fig_triangles_q, "col", 380),
    ("triangles-a", fig_triangles_a, "col", 380),
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

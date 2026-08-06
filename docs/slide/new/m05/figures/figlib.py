#!/usr/bin/env python3
"""Drawing infrastructure for the Module 05 figures.

Pipeline, unchanged from m02/m03 because it works:

    TikZ body  ->  pdflatex (page pinned to the design canvas)  ->  pdftoppm -r 288

**One bp is one slide pixel.**  m03 authored a 1100bp canvas for a container it
believed was 1120px wide and got a scale of 1.018; the container is actually 1080px
(Marp wraps every figure in a `<p>` and `section p { max-width: 1080px }` binds
first, confirmed by counting `<div class="fig"><p>` in m03's own export: 72 of 72).
So m04 authors at exactly the container width and the scale is 1.000 -- a 36pt label
is 36px of type and 15.5px of x-height on the slide, with nothing to reconcile.

Every figure module imports from here; `make_figures.py` is the entry point.
"""

import itertools
import math
import re
import subprocess
import sys
import tempfile
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import numpy as np
from PIL import Image

OUT = Path(__file__).resolve().parent

# --------------------------------------------------------------------------- palette
ACCENT = "3959A6"     # the object under discussion
ACCENT2 = "B14434"    # what THIS slide is about
ACCENT3 = "DAB167"    # fills and rings only -- 2.0:1 on white, never text or a thin stroke
GRAY = "6b6b6b"       # annotation only
INK = "000000"

# --------------------------------------------------------------------------- geometry
DPI = 288
PXBP = DPI / 72                      # 4 raster px per bp

# The deck's containers, read out of network-science.css and confirmed in the render:
#   section p        { max-width: 1080px }   <- binds before the 1120px content area
#   .cols            two minmax(0,1fr) tracks, 46px gap  ->  537px each
#   .fig img         { max-height: 380px }
#   .fig.tight img   { max-height: 320px }
#   .fig.stack img   { max-height: 190px }
COL_W, FULL_W = 537, 1080
FIG_H = {"": 380, "tight": 320, "stack": 190}

DESIGN = {"col": COL_W, "full": FULL_W}
CONTAINER = {"col": COL_W, "full": FULL_W}       # authored 1:1, so the scale is 1.000

NODE = 40          # disc diameter in bp -> 40px on the slide (band is 26-52)
SMALLNODE = 28     # only where a figure draws dozens of discs
DOT = 14
EDGE_W = 2.6
HEAVY_W = 5.0
PAD = 12           # bp of white kept around the ink when the height is cropped

# Type. The gate measures **x-height on the rendered slide**, so that is what the
# generator asserts -- asserting cap height instead let 30pt Latin Modern pass at
# 21px cap while landing 13px x-height on forty of m03's figures. XHEIGHT_RATIO is
# not a constant here: calibrate() compiles a glyph and measures it (see below).
FONT = 36
NODE_MIN_PX, NODE_MAX_PX = 26, 52
TEXT_MIN_PX = 15.5          # check_render.py fails below 15
INK_FILL_MIN = 0.76         # ink must span this share of the canvas width

CHAR_W = 0.55               # em per character, for the label collision boxes
LINE_H = 1.05

DASH = "dash pattern=on 7bp off 6bp"
DASH_LONG = "dash pattern=on 12bp off 8bp"

_only = []
_built = []
_failures = []


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
    return PREAMBLE % dict(W=w, H=h, ACCENT=ACCENT, ACCENT2=ACCENT2, ACCENT3=ACCENT3,
                           GRAY=GRAY, NODE=NODE, FONT=FONT, LEAD=int(FONT * 1.15),
                           EDGE=EDGE_W) + body + POSTAMBLE


def render(body, w, h):
    """Compile one TikZ body and return the RGB image, uncropped."""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "f.tex").write_text(_tex(body, w, h))
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "f.tex"],
                           cwd=td, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("pdflatex failed\n" + "\n".join(r.stdout.splitlines()[-25:]))
        # Stock Computer Modern has no 36pt design size and LaTeX substitutes silently;
        # m02 shipped a whole deck 17% under the type floor that way. lmodern fixes it,
        # and this turns any remaining substitution into a build failure.
        if "not available" in r.stdout:
            bad = [l for l in r.stdout.splitlines() if "not available" in l]
            raise SystemExit("LaTeX substituted a font size:\n  " + "\n  ".join(bad))
        subprocess.run(["pdftoppm", "-png", "-r", str(DPI), "-singlefile", "f.pdf", "f"],
                       cwd=td, check=True)
        im = Image.open(td / "f.png").convert("RGB")
        im.load()
    return im


# --------------------------------------------------------------------------- calibration
def _measure_ink_height(glyph):
    body = f"\\node[lab,anchor=base west] at (40,60) {{{glyph}}};\n"
    a = np.array(render(body, 400, 200).convert("L"))
    ys, _ = np.where(a < 200)
    return (ys.max() - ys.min() + 1) / PXBP        # bp


_CAL = {}


def calibrate():
    """Derive the x-height ratio by measuring a compiled glyph, not by quoting a constant.

    FIGURE_GUIDE, "Measure the render": a computed assertion can only restate the
    author's intention.  m02 asserted FONT * CAP_RATIO * scale -- three numbers it
    already knew -- and passed while every label in the deck was 17% under the floor.
    """
    if not _CAL:
        _CAL["x"] = _measure_ink_height("x") / FONT
        _CAL["X"] = _measure_ink_height("X") / FONT
        assert 0.38 < _CAL["x"] < 0.50, f"measured x-height ratio {_CAL['x']:.3f} is implausible"
        print(f"  calibration: x-height {_CAL['x']:.4f} em, cap height {_CAL['X']:.4f} em "
              f"-> {FONT}pt lands {FONT * _CAL['x']:.1f}px x-height at scale 1.0")
    return _CAL["x"]


# --------------------------------------------------------------------------- emit
def crop_and_check(name, im, container, hmod):
    """Crop the height to the ink and assert what the student will actually see."""
    w = DESIGN[container]
    a = np.array(im.convert("L"))
    exp_w = int(round(w * PXBP))
    assert im.size[0] == exp_w, f"{name}: page is {im.size[0]}px wide, expected {exp_w}"

    ys, xs = np.where(a < 200)
    assert len(ys), f"{name}: blank figure"
    edge = 2
    touched = [side for side, hit in (
        ("left", xs.min() <= edge), ("right", xs.max() >= a.shape[1] - 1 - edge),
        ("top", ys.min() <= edge), ("bottom", ys.max() >= a.shape[0] - 1 - edge)) if hit]
    assert not touched, (
        f"{name}: ink runs off the {', '.join(touched)} edge -- the drawing is being "
        f"CLIPPED, not cropped. Move it inward or grow the canvas.")

    lo = max(0, ys.min() - int(PAD * PXBP))
    hi = min(a.shape[0], ys.max() + int(PAD * PXBP))
    im = im.crop((0, lo, im.size[0], hi))

    fw, fh = im.size
    hcap = FIG_H[hmod]
    scale = min(CONTAINER[container] / fw, hcap / fh, 1.0)
    factor = scale * PXBP                       # slide px per bp
    want = CONTAINER[container] / w             # 1.000 by construction
    assert abs(factor - want) < 1e-6, (
        f"{name}: the HEIGHT binds the scale -- the drawing is {fh/PXBP:.0f}bp tall and "
        f"a '{hmod or 'plain'}' figure in the {container} container may be at most "
        f"{hcap:.0f}bp. Shorten it; do not shrink the type.")

    span = (xs.max() - xs.min() + 1) / fw
    assert span >= INK_FILL_MIN, (
        f"{name}: ink spans {span:.0%} of the canvas width (need {INK_FILL_MIN:.0%}) -- "
        f"widen the drawing, do not shrink the canvas")

    node_px = NODE * factor
    assert NODE_MIN_PX <= node_px <= NODE_MAX_PX, f"{name}: node disc {node_px:.0f}px"
    x_px = FONT * calibrate() * factor
    assert x_px >= TEXT_MIN_PX, f"{name}: text x-height {x_px:.1f}px on the slide"
    return im, fw, fh, node_px, x_px, span


def emit(name, body, container="col", h=None, hmod=""):
    """Render one figure and record the failure rather than stopping the build.

    A generator that stops at the first failed assertion hides the rest, and these
    gates fire in clusters -- raising the type size broke seven of m03's figures at
    once. Every failure is printed and the run exits non-zero at the end.
    """
    if _only and not any(k in name for k in _only):
        return
    try:
        w = DESIGN[container]
        im = render(body, w, h or int(w * 0.70))
        im, fw, fh, node_px, x_px, span = crop_and_check(name, im, container, hmod)
        im.save(OUT / f"{name}.png")
        _built.append(name)
        print(f"  {name}.png  {fw//4}x{fh//4}bp  node {node_px:.0f}px  x-h {x_px:.1f}px  "
              f"ink {span:.0%}  [{container}{'/' + hmod if hmod else ''}]")
    except (AssertionError, SystemExit) as e:
        _failures.append((name, str(e)))
        print(f"  FAIL {name}: {e}")


# --------------------------------------------------------------------------- drawing
def disc(x, y, label="", fill="accent", name=None, size=NODE, text_col="white"):
    nm = f"({name})" if name else ""
    opt = f"disc,fill={fill},minimum size={size}bp"
    if text_col != "white":
        opt += f",text={text_col}"
    return f"\\node[{opt}] {nm} at ({x},{y}) {{{label}}};\n"


def opendisc(x, y, color="accenttwo", size=NODE, w=4.0):
    return f"\\draw[line width={w}bp,draw={color},fill=white] ({x},{y}) circle ({size/2}bp);\n"


def ring(x, y, size=NODE, color="accenttwo", w=4.0, grow=11):
    return f"\\draw[line width={w}bp,draw={color}] ({x},{y}) circle ({(size+grow)/2}bp);\n"


def dot(x, y, color="accent", d=DOT):
    return f"\\fill[{color}] ({x},{y}) circle ({d/2}bp);\n"


def seg(p, q, color="black", w=EDGE_W, dash="", arrow="", opacity=None):
    o = [f"line width={w}bp", f"draw={color}"]
    for extra in (dash, arrow):
        if extra:
            o.append(extra)
    if opacity is not None:
        o.append(f"opacity={opacity}")
    return f"\\draw[{','.join(o)}] ({p[0]:.1f},{p[1]:.1f}) -- ({q[0]:.1f},{q[1]:.1f});\n"


def polyline(pts, color="accent", w=3.4, dash=""):
    o = [f"line width={w}bp", f"draw={color}"]
    if dash:
        o.append(dash)
    return "\\draw[%s] %s;\n" % (",".join(o), " -- ".join("(%.2f,%.2f)" % p for p in pts))


def fill_poly(pts, color="accenttwo", opacity=0.25):
    return "\\fill[%s,opacity=%s] %s -- cycle;\n" % (
        color, opacity, " -- ".join("(%.2f,%.2f)" % p for p in pts))


_fontsizes = set()


def text(x, y, s, color="black", anchor="center", size=FONT, width=None, rot=None):
    _fontsizes.add(size)
    assert size >= FONT, f"font {size}pt is below the {FONT}pt floor"
    # A bare % is a TeX comment: it swallowed the rest of a \node line once and the
    # build died with "Undefined control sequence" pointing at the wrong token.
    assert not re.search(r"(?<!\\)%", s), f"unescaped % in {s!r} -- write \\%"
    assert color != "accentthree", "accent-3 is not a text colour (2.0:1 on white)"
    o = [f"font=\\fontsize{{{size}}}{{{int(size*1.15)}}}\\selectfont",
         f"text={color}", f"anchor={anchor}", "align=center"]
    if width:
        o.append(f"text width={width}bp")
    if rot is not None:
        o.append(f"rotate={rot}")
    return f"\\node[{','.join(o)}] at ({x:.1f},{y:.1f}) {{{s}}};\n"


def pct(x, d=0):
    """A percentage with the % escaped, rounded half UP in decimal.

    A measured 0.575 is 57.49999999999999 as a float, so "%.0f" printed 57 while the
    deck's prose said 58 -- one slide, two numbers. repr() is the shortest string that
    round-trips, so the multiply happens in decimal and the rounding sees the value
    the author meant.
    """
    q = (Decimal(repr(float(x))) * 100).quantize(
        Decimal("1") if d == 0 else Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{q}\\%"


# --------------------------------------------------------------------------- geometry gates
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
    """F2 as a build gate: no two non-adjacent edges may cross."""
    return [((a, b), (c, d)) for (a, b), (c, d) in itertools.combinations(edges, 2)
            if len({a, b, c, d}) == 4 and _seg_cross(pos[a], pos[b], pos[c], pos[d])]


def assert_planar_drawing(edges, pos, what):
    x = crossings(list(edges), pos)
    assert not x, f"{what}: {len(x)} edge crossing(s) in a planar graph -- {x[:3]}"
    c = clearance_bad(list(edges), pos)
    assert not c, f"{what}: edge passes through a disc it does not end at -- {c[:3]}"


# --------------------------------------------------------------------------- label solver
def label_box(x, y, s, anchor, size=FONT, pad=6):
    w = CHAR_W * size * max(len(line) for line in s.split("\\\\")) + 2 * pad
    h = LINE_H * size * len(s.split("\\\\")) + 2 * pad
    ax = {"center": 0.0, "west": 0.5, "east": -0.5, "north": 0.0, "south": 0.0,
          "north west": 0.5, "north east": -0.5,
          "south west": 0.5, "south east": -0.5}[anchor]
    ay = {"center": 0.0, "west": 0.0, "east": 0.0, "north": -0.5, "south": 0.5,
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
    """Does the segment p--q enter the padded box?  Liang-Barsky clip."""
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


# The anchor names the side of the TEXT BOX that sits at the offset point, so a label
# placed to the LEFT of a node anchors "east". Getting this pairing backwards put every
# m03 label on top of its own disc, and the hand-written check missed it because it
# exempted a label's own node. It does not any more.
SIDES = [
    ("east", -26, 0), ("west", 26, 0), ("south", 0, 26), ("north", 0, -26),
    ("south east", -20, 20), ("south west", 20, 20),
    ("north east", -20, -20), ("north west", 20, -20),
    ("east", -44, 0), ("west", 44, 0), ("south", 0, 46), ("north", 0, -46),
    ("south east", -34, 34), ("south west", 34, 34),
    ("north east", -34, -34), ("north west", 34, -34),
]


def place_labels(names, pos, edges, blockers=(), bounds=None, gap=0.0, size=FONT):
    """Choose a side per label so nothing collides.  Returns ({name: side}, {name: box}).

    Checked against every other label, every disc **including the label's own**, every
    drawn edge, any extra blocker boxes, and the canvas bounds.  Backtracking, best
    side first, so the usual answer is also the tidy one.
    """
    order = sorted(names, key=lambda n: -len(names[n]))
    chosen, boxes = {}, {}

    def ok(n, side):
        anc, dx, dy = side
        b = label_box(pos[n][0] + dx, pos[n][1] + dy, names[n], anc, size=size)
        b = (b[0] - gap, b[1] - gap, b[2] + gap, b[3] + gap)
        if bounds and not (bounds[0] <= b[0] and b[2] <= bounds[2]
                           and bounds[1] <= b[1] and b[3] <= bounds[3]):
            return None
        if any(box_hits_disc(b, x, y) for x, y in pos.values()):
            return None
        if any(boxes_overlap(b, o) for o in boxes.values()):
            return None
        if any(boxes_overlap(b, o) for o in blockers):
            return None
        if any(box_hits_segment(b, pos[a], pos[c]) for a, c in edges):
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
            "label placement failed -- no collision-free side assignment exists.\n"
            "Move a node, shorten a name, or widen the canvas; do not shrink the type.")
    return chosen, boxes


def draw_labels(names, pos, chosen, color="black", size=FONT):
    out = ""
    for n, (anc, dx, dy) in chosen.items():
        out += text(pos[n][0] + dx, pos[n][1] + dy, names[n], color=color,
                    anchor=anc, size=size)
    return out


def note(s, at, color="accenttwo", anchor="west", size=FONT, boxes=()):
    """An in-drawing note, asserted clear of every solved label box.

    A note sits at a fixed corner while names are placed by the solver, so a note that
    grows collides with whatever the solver put there -- m03 drew "every town is its
    own island" straight through the word "Znojmo". Notes carry numbers; prose belongs
    in the deck's figcaption, so the failure message says shorten it.
    """
    b = label_box(at[0], at[1], s, anchor, size=size)
    hit = [k for k, v in (boxes.items() if hasattr(boxes, "items") else enumerate(boxes))
           if boxes_overlap(b, v)]
    assert not hit, (f"in-drawing note {s!r} collides with {hit} -- shorten the note "
                     f"(numbers only; prose goes in the figcaption)")
    return text(at[0], at[1], s, color=color, anchor=anchor, size=size)


# --------------------------------------------------------------------------- axes
def _ticks_log(lo, hi):
    """Decade ticks covering [lo, hi]."""
    return [10 ** e for e in range(math.floor(math.log10(lo)), math.ceil(math.log10(hi)) + 1)]


class Axes:
    """A plot frame in bp, with linear or log mapping on each axis.

    Data figures are drawn in TikZ like everything else -- matplotlib models a plot
    rather than a diagram, so node radius, endpoints and text size all become things
    you compute instead of declare, and the m01 rounds were mostly spent on exactly
    that class of defect.
    """

    def __init__(self, box, xlim, ylim, xlog=False, ylog=False,
                 xlabel="", ylabel="", xticks=None, yticks=None,
                 xfmt=None, yfmt=None, size=FONT):
        self.x0, self.y0, self.x1, self.y1 = box
        self.xlim, self.ylim = xlim, ylim
        self.xlog, self.ylog = xlog, ylog
        self.xlabel, self.ylabel = xlabel, ylabel
        self.size = size
        self.xticks = xticks if xticks is not None else (
            _ticks_log(*xlim) if xlog else list(np.linspace(*xlim, 5)))
        self.yticks = yticks if yticks is not None else (
            _ticks_log(*ylim) if ylog else list(np.linspace(*ylim, 5)))
        self.xfmt = xfmt or (self._logfmt if xlog else (lambda v: f"{v:g}"))
        self.yfmt = yfmt or (self._logfmt if ylog else (lambda v: f"{v:g}"))

    @staticmethod
    def _logfmt(v):
        e = int(round(math.log10(v)))
        return {0: "1", 1: "10"}.get(e, f"$10^{{{e}}}$")

    def X(self, v):
        lo, hi = self.xlim
        if self.xlog:
            v, lo, hi = math.log10(max(v, 1e-12)), math.log10(lo), math.log10(hi)
        return self.x0 + (v - lo) / (hi - lo) * (self.x1 - self.x0)

    def Y(self, v):
        lo, hi = self.ylim
        if self.ylog:
            v, lo, hi = math.log10(max(v, 1e-12)), math.log10(lo), math.log10(hi)
        return self.y0 + (v - lo) / (hi - lo) * (self.y1 - self.y0)

    def P(self, x, y):
        return (self.X(x), self.Y(y))

    def inside(self, x, y):
        return (self.xlim[0] <= x <= self.xlim[1]) and (self.ylim[0] <= y <= self.ylim[1])

    def frame(self, ticklen=9):
        """Two spines, ticks with labels, and the axis titles."""
        o = seg((self.x0, self.y0), (self.x1, self.y0), color="black", w=2.2)
        o += seg((self.x0, self.y0), (self.x0, self.y1), color="black", w=2.2)
        for v in self.xticks:
            if not (self.xlim[0] <= v <= self.xlim[1]):
                continue
            x = self.X(v)
            o += seg((x, self.y0), (x, self.y0 - ticklen), color="black", w=2.2)
            o += text(x, self.y0 - ticklen - 8, self.xfmt(v), anchor="north", size=self.size)
        for v in self.yticks:
            if not (self.ylim[0] <= v <= self.ylim[1]):
                continue
            y = self.Y(v)
            o += seg((self.x0, y), (self.x0 - ticklen, y), color="black", w=2.2)
            o += text(self.x0 - ticklen - 8, y, self.yfmt(v), anchor="east", size=self.size)
        if self.xlabel:
            o += text((self.x0 + self.x1) / 2, self.y0 - ticklen - self.size * 1.9,
                      self.xlabel, anchor="north", size=self.size)
        if self.ylabel:
            o += text(self.x0 - ticklen - self.size * 2.6, (self.y0 + self.y1) / 2,
                      self.ylabel, anchor="south", size=self.size, rot=90)
        return o

    def points(self, xs, ys, color="accent", d=None, every=1):
        """Scatter, clipped to the frame.  Ink outside the canvas simply never renders."""
        d = d or 9
        o = ""
        for i, (x, y) in enumerate(zip(xs, ys)):
            if i % every or not self.inside(x, y):
                continue
            o += dot(*self.P(x, y), color=color, d=d)
        return o

    def line(self, xs, ys, color="accenttwo", w=3.4, dash=""):
        pts = [self.P(x, y) for x, y in zip(xs, ys) if self.inside(x, y)]
        assert len(pts) >= 2, "line has fewer than two points inside the frame"
        return polyline(pts, color=color, w=w, dash=dash)

    def step(self, xs, ys, color="accent", w=3.4):
        pts = []
        for i, (x, y) in enumerate(zip(xs, ys)):
            if not self.inside(x, y):
                continue
            if pts:
                pts.append((self.X(x), pts[-1][1]))
            pts.append(self.P(x, y))
        assert len(pts) >= 2
        return polyline(pts, color=color, w=w)


# --------------------------------------------------------------------------- run
def run(figures):
    """Build every figure, report every failure, exit non-zero if any failed."""
    global _only
    _only = [a for a in sys.argv[1:] if not a.startswith("-")]
    calibrate()
    for name, fn in figures:
        if _only and not any(k in name for k in _only):
            continue
        try:
            fn()
        except (AssertionError, SystemExit) as e:
            _failures.append((name, str(e)))
            print(f"  FAIL {name}: {e}")
    print(f"\n{len(_built)} figures written, {len(_failures)} failed")
    if _failures:
        for n, e in _failures:
            print(f"  ! {n}: {e.splitlines()[0]}")
        sys.exit(1)

#!/usr/bin/env python3
"""Drawing infrastructure for the Module 04 figures.

Pipeline, unchanged from m02/m03 because it works:

    TikZ body  ->  xelatex (page pinned to the design canvas)  ->  pdftoppm -r 288  ->  grain

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
# The lecturer's own slide style (his reference figures, 2026-10-13): muted colours
# overall, saturation reserved for what matters, and no pure black. Hand-drawn nodes
# with a dark grainy outline, brush strokes for highlights and underlines, and
# MesloLGS NF for every label. Math stays in Latin Modern, as in his slides.
#
#   INK      text, outlines, edges      a dark slate, not #000
#   MUTED    what is NOT the point      warm grey: de-emphasised text, edges, nodes
#   PALE     a de-emphasised fill       light warm grey
#   HOT      the point of the slide     orange: the answer, the winner, "this one"
#   COOL     the second emphasis        sky blue: high scores, the other side
#   TEAL, OLIVE, DEEP                   extra categories, used sparingly (desaturated)
#   GOLD     a route / a walk           the brush that traces a path
INK = "30323D"
MUTED = "8C847F"
PALE = "D9D3CF"
FAINT = "EFEBE8"     # the low end of a value scale: almost paper, slightly warm
HOT = "D9631E"
COOL = "1E96DC"
TEAL = "3F8A88"
OLIVE = "9B9922"
DEEP = "2F6FB4"
GOLD = "C08A1F"

# The names older modules import. They map onto the new palette so nothing reads the
# old blue/red; new code uses the TikZ names hot, cool, ink, muted, pale directly.
ACCENT = COOL
ACCENT2 = HOT
ACCENT3 = GOLD
GRAY = MUTED

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
FIG_H = {"": 380, "tight": 320, "stack": 190, "tall": 400}

DESIGN = {"col": COL_W, "full": FULL_W}
CONTAINER = {"col": COL_W, "full": FULL_W}       # authored 1:1, so the scale is 1.000

NODE = 40          # disc diameter in bp -> 40px on the slide (band is 26-52)
SMALLNODE = 28     # only where a figure draws dozens of discs
DOT = 14
EDGE_W = 2.4
HEAVY_W = 5.0
PAD = 12           # bp of white kept around the ink when the height is cropped

# Type. The gate measures **x-height on the rendered slide**, so that is what the
# generator asserts -- asserting cap height instead let 30pt Latin Modern pass at
# 21px cap while landing 13px x-height on forty of m03's figures. XHEIGHT_RATIO is
# not a constant here: calibrate() compiles a glyph and measures it (see below).
FONT = 30                   # MesloLGS NF: its x-height is 0.55 em, so 30pt lands 16.5px
FONT_MATH = 38              # Latin Modern math: x-height 0.43 em, so it needs the larger size
NODE_MIN_PX, NODE_MAX_PX = 26, 52
TEXT_MIN_PX = 15.5          # check_render.py fails below 15
INK_FILL_MIN = 0.76         # ink must span this share of the canvas width

CHAR_W = 0.61               # em per character (Meslo is monospaced: 0.60 em)
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
\usepackage{lmodern}
\usepackage{amsmath}
\usepackage{fontspec}
\setmainfont{MesloLGS NF}
\usepackage{tikz}
\usetikzlibrary{calc,positioning,arrows.meta,decorations.pathmorphing,decorations.markings,
                backgrounds,fit,shapes.geometric,patterns}
\definecolor{black}{HTML}{%(INK)s}
\definecolor{ink}{HTML}{%(INK)s}
\definecolor{muted}{HTML}{%(MUTED)s}
\definecolor{pale}{HTML}{%(PALE)s}
\definecolor{faint}{HTML}{%(FAINT)s}
\definecolor{hot}{HTML}{%(HOT)s}
\definecolor{cool}{HTML}{%(COOL)s}
\definecolor{tealc}{HTML}{%(TEAL)s}
\definecolor{olivec}{HTML}{%(OLIVE)s}
\definecolor{deep}{HTML}{%(DEEP)s}
\definecolor{gold}{HTML}{%(GOLD)s}
\definecolor{accent}{HTML}{%(COOL)s}
\definecolor{accenttwo}{HTML}{%(HOT)s}
\definecolor{accentthree}{HTML}{%(GOLD)s}
\definecolor{annot}{HTML}{%(MUTED)s}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\begin{document}%%
\pgfmathsetseed{%(SEED)d}%%
\vbox to \paperheight{\vss\hbox to \paperwidth{\hss%%
\begin{tikzpicture}[x=1bp,y=1bp,
    every node/.style={inner sep=0pt,outer sep=0pt},
    disc/.style={circle,draw=none,minimum size=%(NODE)dbp,inner sep=0pt,
                 text=ink,font=\fontsize{%(FONT)d}{%(FONT)d}\selectfont},
    lab/.style={font=\fontsize{%(FONT)d}{%(LEAD)d}\selectfont,align=center},
    ed/.style={line width=%(EDGE)sbp,draw=ink},
    pencil/.style={decorate,decoration={random steps,segment length=6bp,amplitude=0.45bp},
                   line join=round},
    pencilround/.style={decorate,decoration={random steps,segment length=3.2bp,amplitude=0.55bp},
                   rounded corners=1.4bp},
    rough/.style={decorate,decoration={random steps,segment length=6bp,amplitude=0.8bp},
                  line join=round},
]
\useasboundingbox (0,0) rectangle (%(W)d,%(H)d);
"""

POSTAMBLE = r"""
\end{tikzpicture}%
\hss}\vss}%
\end{document}
"""


SEED = 20261013     # TikZ's random steps: fixed, so a question and its answer draw identically


def _tex(body, w, h):
    return PREAMBLE % dict(W=w, H=h, INK=INK, MUTED=MUTED, PALE=PALE, FAINT=FAINT, HOT=HOT, COOL=COOL,
                           TEAL=TEAL, OLIVE=OLIVE, DEEP=DEEP, GOLD=GOLD, SEED=SEED,
                           NODE=NODE, FONT=FONT, LEAD=int(FONT * 1.15),
                           EDGE=EDGE_W) + body + POSTAMBLE


# Grain: the lecturer's figures have a chalky, mottled fill and a grainy outline. It is
# added to the raster, keyed to the pixel position only, so two renders of the same
# drawing (a question and its answer, the frames of a build) carry the same grain.
GRAIN = 0.075
_noise = {}


def _grain_field(h, w):
    if (h, w) not in _noise:
        from PIL import ImageFilter
        rng = np.random.default_rng(SEED)
        n = rng.normal(0.5, 0.18, (h, w)).clip(0, 1)
        im = Image.fromarray((n * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(1.1))
        f = np.asarray(im).astype(np.float32) / 255.0
        _noise[(h, w)] = (f - f.mean()) / (f.std() + 1e-6)
    return _noise[(h, w)]


def grain(im):
    """Mottle every coloured or grey pixel; leave white paper and solid ink alone."""
    a = np.asarray(im).astype(np.float32)
    lum = a.mean(axis=2)
    n = _grain_field(*lum.shape)
    m = (lum < 247) & (lum > 64)
    k = 1.0 + GRAIN * n
    a[m] = a[m] * k[m][:, None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGB")


def render(body, w, h):
    """Compile one TikZ body and return the RGB image, uncropped."""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "f.tex").write_text(_tex(body, w, h))
        r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "f.tex"],
                           cwd=td, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("xelatex failed\n" + "\n".join(r.stdout.splitlines()[-25:]))
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
    return grain(im)


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
        assert 0.45 < _CAL["x"] < 0.62, f"measured x-height ratio {_CAL['x']:.3f} is implausible"
        print(f"  calibration: x-height {_CAL['x']:.4f} em, cap height {_CAL['X']:.4f} em "
              f"-> {FONT}pt lands {FONT * _CAL['x']:.1f}px x-height at scale 1.0")
    return _CAL["x"]


# --------------------------------------------------------------------------- emit
def crop_and_check(name, im, container, hmod, nodes=True):
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
    # nodes=False: a data map (the NY highways) draws hundreds of small dots, not discs a
    # student reads one by one. The deck's check_render.py exempts the same figures.
    assert not nodes or NODE_MIN_PX <= node_px <= NODE_MAX_PX, f"{name}: node disc {node_px:.0f}px"
    x_px = FONT * calibrate() * factor
    assert x_px >= TEXT_MIN_PX, f"{name}: text x-height {x_px:.1f}px on the slide"
    return im, fw, fh, node_px, x_px, span


def _emit_set(items, container, h, hmod, nodes, box):
    """Render several bodies and crop them all to ONE box: a question and its answer, or
    the frames of a build, sit at exactly the same place on consecutive slides.

    box=None crops to the union of the ink; box=(top, bottom) in bp from the canvas top
    fixes the crop, so figures built in different functions (or modules) that share a
    drawing line up too. Every image also passes the single-figure gates.
    """
    w = DESIGN[container]
    hh = h or int(w * 0.70)
    ims = [render(body, w, hh) for _, body in items]
    H = ims[0].size[1]
    rows = []
    for (name, _), im in zip(items, ims):
        a = np.asarray(im.convert("L"))
        ys, _x = np.where(a < 200)
        assert len(ys), f"{name}: blank figure"
        rows.append((ys.min(), ys.max()))
        crop_and_check(name, im, container, hmod, nodes)        # the gates, per image
    if box is None:
        pad = int(PAD * PXBP)
        lo = max(0, min(r[0] for r in rows) - pad)
        hi = min(H, max(r[1] for r in rows) + pad)
    else:
        lo, hi = int(round(box[0] * PXBP)), int(round(box[1] * PXBP))
        assert 0 <= lo < hi <= H, f"box {box} is outside the {hh}bp canvas"
        for (name, _), r in zip(items, rows):
            assert lo <= r[0] and r[1] < hi, (
                f"{name}: ink at rows {r[0] / PXBP:.0f}-{r[1] / PXBP:.0f}bp falls outside the "
                f"fixed box {box}")
    assert (hi - lo) / PXBP <= FIG_H[hmod] + 0.5, (
        f"{items[0][0]}: the shared crop is {(hi - lo) / PXBP:.0f}bp tall; a "
        f"'{hmod or 'plain'}' figure may be at most {FIG_H[hmod]}bp")
    return [im.crop((0, lo, im.size[0], hi)) for im in ims]


def _report(name, im, container, hmod, ext="png", extra=""):
    fw, fh = im.size
    print(f"  {name}.{ext}  {fw // 4}x{fh // 4}bp  node {NODE:.0f}px  "
          f"x-h {FONT * calibrate():.1f}px  [{container}{'/' + hmod if hmod else ''}]{extra}")


def emit(name, body, container="col", h=None, hmod="", nodes=True, box=None):
    """Render one figure and record the failure rather than stopping the build.

    A generator that stops at the first failed assertion hides the rest, and these
    gates fire in clusters -- raising the type size broke seven of m03's figures at
    once. Every failure is printed and the run exits non-zero at the end.
    """
    if _only and not any(k in name for k in _only):
        return
    try:
        (im,) = _emit_set([(name, body)], container, h, hmod, nodes, box)
        im.save(OUT / f"{name}.png")
        _built.append(name)
        _report(name, im, container, hmod)
    except (AssertionError, SystemExit) as e:
        _failures.append((name, str(e)))
        print(f"  FAIL {name}: {e}")


def emit_group(items, container="col", h=None, hmod="", nodes=True, box=None, prefix=True):
    """A question and its answers (or any run of slides on one drawing), one crop.

    items: [(name, body), ...]. With prefix=True every later body must start with the
    first one: the answer is the question plus marks and values, never a redraw.
    """
    names = [n for n, _ in items]
    if _only and not any(k in n for n in names for k in _only):
        return
    try:
        if prefix:
            for n, body in items[1:]:
                assert body.startswith(items[0][1]), (
                    f"{n}: must be {items[0][0]} plus marks and values (body is not a prefix)")
        for (n, _), im in zip(items, _emit_set(items, container, h, hmod, nodes, box)):
            im.save(OUT / f"{n}.png")
            _built.append(n)
            _report(n, im, container, hmod)
    except (AssertionError, SystemExit) as e:
        _failures.append(("/".join(names), str(e)))
        print(f"  FAIL {'/'.join(names)}: {e}")


FRAMES = OUT / "frames"


def emit_frames(name, frames, container="col", h=None, hmod="", nodes=True, box=None, **_ignored):
    """A build the lecturer steps through: every frame on one crop.

    Writes figures/frames/<name>/00.png, 01.png, ... for the slide's scrubber
    (slides/m06/scrub.js) and figures/<name>.png, the LAST frame, which is the picture
    the PDF/PNG export and the render gate see. No GIF: the lecturer drives the build
    with the slider, so nothing moves on its own.
    """
    if _only and not any(k in name for k in _only):
        return
    try:
        ims = _emit_set([(f"{name}[{i}]", b) for i, b in enumerate(frames)],
                        container, h, hmod, nodes, box)
        d = FRAMES / name
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob("*.png"):
            old.unlink()
        for i, im in enumerate(ims):
            im.save(d / f"{i:02d}.png")
        ims[-1].save(OUT / f"{name}.png")
        _built.append(name)
        _report(name, ims[-1], container, hmod, extra=f"  {len(ims)} frames")
    except (AssertionError, SystemExit) as e:
        _failures.append((name, str(e)))
        print(f"  FAIL {name}: {e}")


def emit_gif(name, frames, container="full", h=None, hmod="", nodes=True, box=None, **_ignored):
    """Old name: every build is now stepped by the lecturer (emit_frames)."""
    emit_frames(name, frames, container=container, h=h, hmod=hmod, nodes=nodes, box=box)


# --------------------------------------------------------------------------- drawing
# Hand-drawn, after the lecturer's reference figures: a node is a filled disc (white by
# default) with a dark pencil outline drawn twice, slightly off each other; an edge is a
# soft-ink line with a fainter second stroke; a highlight is a brush stroke. The raster
# grain (grain()) does the rest.

def _lum(hexcol):
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


_NAMED = {"ink": INK, "black": INK, "muted": MUTED, "pale": PALE, "faint": FAINT, "hot": HOT, "cool": COOL,
          "tealc": TEAL, "olivec": OLIVE, "deep": DEEP, "gold": GOLD, "white": "FFFFFF",
          "accent": COOL, "accenttwo": HOT, "accentthree": GOLD, "annot": MUTED}


def mix(a, b, t):
    """xcolor's a!t!b as an expression (t in 0..1 is the share of a)."""
    return f"{a}!{t * 100:.0f}!{b}"


def shade(v, lo="faint", hi="cool"):
    """A value in 0..1 as a fill: near-paper warm grey (low, unimportant) to saturated
    cool (high, important). Saturation carries the importance, as on his slides."""
    v = min(max(v, 0.0), 1.0)
    return mix(hi, lo, v)


def _text_on(fill):
    """Ink on light fills, white on saturated or dark ones."""
    if "!" in fill:                     # a mix "a!p!b": estimate its lightness
        parts = fill.split("!")
        a, t = parts[0], float(parts[1]) / 100
        b = parts[2] if len(parts) > 2 else "white"
        L = t * _lum(_NAMED.get(a, "808080")) + (1 - t) * _lum(_NAMED.get(b, "FFFFFF"))
    else:
        L = _lum(_NAMED.get(fill, "FFFFFF"))
    return "white" if L < 120 else "ink"


def _seed(*xs):
    """Reseed TikZ's random steps from an element's own coordinates, so every element is
    drawn the same way whatever was drawn before it: a build's frames and a question and
    its answer never jitter."""
    v = 1 + int(abs(sum((i + 1) * 97.0 * float(x) for i, x in enumerate(xs)))) % 2147480000
    return f"\\pgfmathsetseed{{{v}}}"


def sketch_circle(x, y, d, color="ink", w=2.0):
    """A pencil circle: two strokes, slightly different radii, jittered."""
    r = d / 2
    # pencilround (rounded corners) is safe on a circle; `pencil` is the robust one for
    # rectangles and lines (random steps + rounded corners dies on some boxes).
    return _seed(x, y, d) + (f"\\draw[{color},line width={w}bp,pencilround,opacity=0.92] ({x:.2f},{y:.2f}) circle ({r:.2f}bp);\n"
            f"\\draw[{color},line width={w * 0.55:.2f}bp,pencilround,opacity=0.75] "
            f"({x + 0.5:.2f},{y - 0.4:.2f}) circle ({r + 0.7:.2f}bp);\n")


def disc(x, y, label="", fill="white", name=None, size=NODE, text_col=None, outline="ink"):
    """A node: a filled disc with a pencil outline and its label in MesloLGS NF.

    fill: "white" (the default node), "pale" (de-emphasised), "hot" (the point), "cool",
    or a shade() mix for a value. The label is ink on light fills and white on dark ones.
    """
    nm = f"({name})" if name else ""
    tc = text_col or _text_on(fill)
    out = f"\\fill[{fill}] ({x:.2f},{y:.2f}) circle ({size / 2:.2f}bp);\n"
    out += sketch_circle(x, y, size, color=outline, w=2.1 if size >= 30 else 1.6)
    out += (f"\\node[disc,minimum size={size}bp,text={tc}] {nm} at ({x:.2f},{y:.2f}) "
            f"{{{label}}};\n")
    return out


def opendisc(x, y, color="ink", size=NODE, w=2.1):
    return disc(x, y, "", fill="white", size=size, outline=color)


def ring(x, y, size=NODE, color="hot", w=3.0, grow=14):
    """A hand-drawn ring around a disc: the "this one" mark."""
    return sketch_circle(x, y, size + grow, color=color, w=w)


def mark(x, y, color="hot", size=NODE, w=3.0):
    """Mark a node as the point of the slide: a saturated ring just outside its outline."""
    return sketch_circle(x, y, size + 12, color=color, w=w)


def dot(x, y, color="cool", d=DOT):
    return f"\\fill[{color}] ({x:.2f},{y:.2f}) circle ({d / 2:.2f}bp);\n"


def seg(p, q, color="ink", w=EDGE_W, dash="", arrow="", opacity=None, sketch=True):
    """An edge. Undashed, unarrowed edges get a faint second pencil stroke."""
    o = [f"line width={w}bp", f"draw={color}"]
    for extra in (dash, arrow):
        if extra:
            o.append(extra)
    if opacity is not None:
        o.append(f"opacity={opacity}")
    out = f"\\draw[{','.join(o)}] ({p[0]:.1f},{p[1]:.1f}) -- ({q[0]:.1f},{q[1]:.1f});\n"
    if sketch and not dash and w >= 1.5:
        out += _seed(p[0], p[1], q[0], q[1])
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L * 0.8, dx / L * 0.8
        out += (f"\\draw[line width={w * 0.45:.2f}bp,draw={color},opacity=0.55,pencil] "
                f"({p[0] + nx:.1f},{p[1] + ny:.1f}) -- ({q[0] + nx:.1f},{q[1] + ny:.1f});\n")
    return out


def _resample(pts, step=6.0):
    """The polyline as points evenly spaced along its length, at least `step` apart.

    Uniform arc-length spacing matters to TikZ: `random steps` with rounded corners on a run
    of sub-bp segments (duplicate points, or a short underline sampled densely) dies with
    "Dimension too large".
    """
    P = [np.array(p, float) for p in pts]
    P = [p for i, p in enumerate(P) if i == 0 or np.linalg.norm(p - P[i - 1]) > 1e-6]
    if len(P) < 2:
        return P
    seg = [float(np.linalg.norm(b - a)) for a, b in zip(P, P[1:])]
    total = sum(seg)
    n = max(1, int(total // step))
    targets = np.linspace(0.0, total, n + 1)
    out, k, acc = [], 0, 0.0
    for t in targets:
        while k < len(seg) - 1 and acc + seg[k] < t:
            acc += seg[k]
            k += 1
        u = 0.0 if seg[k] == 0 else min(1.0, max(0.0, (t - acc) / seg[k]))
        out.append(P[k] + (P[k + 1] - P[k]) * u)
    return out


def _plen(P):
    """Length of a polyline. TikZ's `rough` (random steps, rounded corners) needs a few
    segment lengths of path; on a shorter stroke it dies with "Dimension too large"."""
    return sum(float(np.linalg.norm(b - a)) for a, b in zip(P, P[1:]))


def _trim(pts, frac):
    n = len(pts)
    k = int(round(n * frac))
    return pts[k:n - k] if n - 2 * k >= 2 else pts


def brush(pts, color="hot", w=10.0, opacity=0.85, strands=7, seed=0):
    """A brush stroke along a polyline, after the lecturer's hand-drawn highlights: a
    bundle of thin strands across the width, each with its own opacity, ragged edge and
    trimmed ends, so the stroke tapers and shows bristle streaks. Draw it BEFORE the
    discs it passes, so the nodes stay on top. Deterministic (seeded by the points), so a
    question and its answer carry the same stroke.

    The raggedness is computed here (a smoothed random offset per point), not by a TikZ
    decoration: `random steps` with rounded corners fails on short strokes."""
    P = _resample(pts, step=4.0)
    if len(P) < 2:
        return ""
    if len(P) < 6:                       # a short stroke: densify so it can taper
        P = _resample(pts, step=max(0.8, _plen(P) / 6))
    key = int(sum(abs(q[0]) * 7.3 + abs(q[1]) * 3.1 for q in P[:4])) + seed
    rng = np.random.default_rng(key % (2 ** 32))
    n = len(P)
    N = []
    for i in range(n):
        a_, b_ = P[max(i - 1, 0)], P[min(i + 1, n - 1)]
        d = b_ - a_
        L = float(np.hypot(*d)) or 1.0
        N.append(np.array([-d[1] / L, d[0] / L]))

    def wobble(amp):
        r = rng.normal(0.0, 1.0, n)
        k = np.ones(3) / 3.0
        r = np.convolve(np.pad(r, 1, mode="edge"), k, mode="valid")
        return r * amp

    def path(idx, off, amp):
        jit = wobble(amp)
        return " -- ".join(f"({P[i][0] + N[i][0] * (off + jit[i]):.2f},"
                           f"{P[i][1] + N[i][1] * (off + jit[i]):.2f})" for i in idx)

    out = ""
    lo = int(round(n * 0.06))
    idx = range(lo, n - lo) if n - 2 * lo >= 2 else range(n)
    out += (f"\\draw[{color},line width={w * 0.8:.2f}bp,line cap=round,line join=round,"
            f"opacity={opacity * 0.35:.2f}] {path(idx, 0.0, 0.5)};\n")
    for k in range(strands):
        off = (k / (strands - 1) - 0.5) * w * 0.9 if strands > 1 else 0.0
        ww = w * rng.uniform(0.16, 0.32)
        op = opacity * rng.uniform(0.45, 1.0)
        t0 = int(n * rng.uniform(0.0, 0.10 + 0.25 * abs(off) / w))
        t1 = n - int(n * rng.uniform(0.0, 0.10 + 0.25 * abs(off) / w))
        if t1 - t0 < 2:
            continue
        out += (f"\\draw[{color},line width={ww:.2f}bp,line cap=round,line join=round,"
                f"opacity={op:.2f}] {path(range(t0, t1), off, 0.45)};\n")
    return out


def underline(x0, x1, y, color="hot", w=6.0, bow=1.5):
    """A hand-drawn underline from x0 to x1 at height y: a thin tapered brush stroke,
    rising very slightly to the right, as in the lecturer's "query vector" figure."""
    pts = [(x0 + (x1 - x0) * t, y + bow * t - bow * 2.5 * t * (1 - t)) for t in np.linspace(0, 1, 30)]
    return brush(pts, color=color, w=w, opacity=0.95, strands=5)


def polyline(pts, color="accent", w=3.4, dash=""):
    o = [f"line width={w}bp", f"draw={color}"]
    if dash:
        o.append(dash)
    return "\\draw[%s] %s;\n" % (",".join(o), " -- ".join("(%.2f,%.2f)" % p for p in pts))


def fill_poly(pts, color="accenttwo", opacity=0.25):
    return "\\fill[%s,opacity=%s] %s -- cycle;\n" % (
        color, opacity, " -- ".join("(%.2f,%.2f)" % p for p in pts))


_fontsizes = set()


def text(x, y, s, color="ink", anchor="center", size=FONT, width=None, rot=None):
    _fontsizes.add(size)
    assert size >= FONT, f"font {size}pt is below the {FONT}pt floor"
    # Latin Modern math has a smaller x-height than MesloLGS NF: a label with $...$
    # in it must be set at FONT_MATH or it lands under the floor on the slide.
    assert "$" not in s or size >= FONT_MATH, (
        f"math in {s!r} at {size}pt -- use size=FONT_MATH ({FONT_MATH}) for any label with $...$")
    # A bare % is a TeX comment: it swallowed the rest of a \node line once and the
    # build died with "Undefined control sequence" pointing at the wrong token.
    assert not re.search(r"(?<!\\)%", s), f"unescaped % in {s!r} -- write \\%"
    assert color not in ("accentthree", "gold", "pale"), f"{color} is not a text colour"
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


# --------------------------------------------------------------------------- callouts
# The lecturer steps a build one slide at a time and wants every step to say what changed:
# a short note in light grey, with a thin arrow to the thing that changed (2026-10-13).
def callout(s, at, target, anchor="south", bend=0, color="muted", size=FONT, gap=7.0,
            tip=None):
    """A muted note at `at` (with `anchor`) and a thin arrow from the note to `target`.

    Returns (tikz, box): add `box` to the blockers of any later label placement. The
    arrow starts on the edge of the note's box nearest the target and stops `gap` bp short
    of the target (a disc's centre: pass gap = NODE/2 + 4). `bend` (degrees) curves it.
    `tip`, if given, overrides where the arrow starts (a point on the note's box).
    """
    b = label_box(at[0], at[1], s, anchor, size=size, pad=2)
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    tx, ty = target
    if tip is None:
        dx, dy = tx - cx, ty - cy
        hw, hh = (b[2] - b[0]) / 2, (b[3] - b[1]) / 2
        t = min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9)
        sx, sy = cx + dx * t, cy + dy * t
        L = math.hypot(dx, dy) or 1.0
        sx, sy = sx + dx / L * 4, sy + dy / L * 4          # a little air off the text
    else:
        sx, sy = tip
    L = math.hypot(tx - sx, ty - sy) or 1.0
    ex, ey = tx - (tx - sx) / L * gap, ty - (ty - sy) / L * gap
    path = (f"({sx:.1f},{sy:.1f}) to[bend left={bend}] ({ex:.1f},{ey:.1f})" if bend
            else f"({sx:.1f},{sy:.1f}) -- ({ex:.1f},{ey:.1f})")
    tikz = (text(at[0], at[1], s, color=color, anchor=anchor, size=size)
            + f"\\draw[{color},line width=1.6bp,line cap=round,"
              f"-{{Stealth[length=9bp,width=7bp]}}] {path};\n")
    return tikz, b


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

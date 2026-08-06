#!/usr/bin/env python3
"""Generate every Module 02 slide figure.

Pipeline (see review/FIGURE_SPEC.md for the derivation):

    TikZ body  ->  pdflatex (page fixed to the design canvas)  ->  pdftoppm -r 288

Author at final size: **1 bp = 1 slide pixel**.  The page is pinned to the design
canvas, so the deck's own scale factor is a constant per container:

    cols column : 537 / 520   = 1.033 slide px per bp
    full width  : 1080 / 1100 = 0.982 slide px per bp

1080, not the 1120 content area: Marp wraps the image in a `<p>` and
`section p { max-width: 1080px }` binds first.  And the theme caps the *height* three
different ways (`.fig` 380, `.fig.tight` 320, `.fig.stack` 190), so a drawing that is
too tall is scaled by its height instead and everything in it shrinks.  Which cap
applies is a fact about the deck's markup, so `_deck_usage()` reads it out of the deck
and `emit()` refuses any figure whose height binds.

Only the *height* is cropped after rasterising (to the ink, plus a pad), which leaves
the width -- and therefore the scale -- untouched.  That is the whole reason node discs
and type land at the same size on every slide, which nine review rounds of Module 01
never achieved by tuning figures one at a time.

Everything a figure prints is computed here (networkx / own BFS) and asserted against
the verified table in review/DECK_SPEC.md.  Nothing is typed in twice.

    python3 figures/make_figures.py            # all figures
    python3 figures/make_figures.py chain      # only figures whose name contains "chain"
"""

import itertools
import math
import re
import os
import random
import shutil
import subprocess
import sys
import tempfile
from collections import deque
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
PALETTE = {ACCENT, ACCENT2, ACCENT3, GRAY, INK, "ffffff", "f7f4f1"}

# --------------------------------------------------------------------------- geometry
DPI = 288
PXBP = DPI / 72              # 4 px per bp

# network-science.css caps a figure THREE ways, and this file used one number for all of
# them -- which is how type 17% under the floor passed a green build on sixteen slides.
# Read straight out of the theme:
#     section p               { max-width: 1080px }   <- Marp wraps the image in a <p>,
#                                                        so a full-width figure stops at
#                                                        1080, not the 1120 content area
#     section .fig img        { max-height: 380px }
#     section .fig.tight img  { max-height: 320px }   <- 16 slides
#     section .fig.stack img  { max-height: 190px }
# Which cap applies is a fact about the DECK's markup and never about the FIGURES table
# below -- the table records intent, and the two have already disagreed twice.
COL_W, FULL_W = 537, 1080
FIG_H = {"": 380, "tight": 320, "stack": 190}

DESIGN = {"col": 520, "full": 1100}
CONTAINER = {"col": COL_W, "full": FULL_W}

NODE = 40          # disc diameter, bp  -> 39.3-41.3 px on the slide (band 26-52)
SMALLNODE = 26     # only where a figure draws dozens of dots (arrival grid, ring lattice)
# 37, not 30: check_render.py measures X-HEIGHT on the rendered slide, and for Latin
# Modern x-height is 0.431 em against cap height 0.683 em.  30pt clears a 21px cap-height
# assertion and lands 12.9px x-height -- under the checker's 15px floor, and invisible to
# the build until the checker runs.  Both ratios are measured below, never assumed.
# 36 was set against a full-width factor of 1.018 that the theme never applies; at the
# real 0.982 it lands 15.2px, under this file's own floor.  The fix for a type-size
# failure is bigger type, never a smaller floor: 37pt lands 15.7px full width and 16.5px
# in a column, and the widest disc label ("G") still needs only 39.4bp of a 40bp disc.
FONT = 37          # pt
EDGE_W = 2.6
HEAVY_W = 5.0
PAD = 6            # bp of white kept around the ink when the height is cropped

NODE_MIN_PX, NODE_MAX_PX = 26, 52
XHEIGHT_MIN_PX = 15.5        # the floor check_render.py enforces on the rendered slide
INK_FILL_MIN = 0.76          # ink must span this share of the canvas width

_only = sys.argv[1:]
_built = []
_fontsizes = set()


# --------------------------------------------------------------------------- TeX
PREAMBLE = r"""
\documentclass{article}
\usepackage{lmodern}
\usepackage[paperwidth=%(W)dbp,paperheight=%(H)dbp,margin=0bp]{geometry}
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


COORD = re.compile(r"\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)")


def _render(name, body, w, hmax):
    """pdflatex + pdftoppm one TikZ body.  Raises on anything that would silently
    change what lands on the page -- a failed run, or a font-size substitution."""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "f.tex").write_text(_tex(body, w, hmax))
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "f.tex"],
                           cwd=td, capture_output=True, text=True)
        if r.returncode:
            tail = "\n".join(r.stdout.splitlines()[-25:])
            raise SystemExit(f"{name}: pdflatex failed\n{tail}")
        log = r.stdout
        f_log = td / "f.log"
        if f_log.exists():
            log += f_log.read_text(errors="replace")
        # Stock Computer Modern has no 30pt design size, so LaTeX substituted 24.88pt and
        # every label in the deck shrank 17% without a word of complaint.  Never again.
        if "Font shape" in log:
            bad = [l for l in log.splitlines() if "Font shape" in l][:3]
            raise SystemExit(f"{name}: LaTeX substituted a font shape -- the type on the "
                             f"slide is not the type you asked for:\n" + "\n".join(bad))
        subprocess.run(["pdftoppm", "-png", "-r", str(DPI), "-singlefile", "f.pdf", "f"],
                       cwd=td, check=True)
        im = Image.open(td / "f.png").convert("RGB")
        im.load()
        return im


DECK = OUT.parent / "m02-small-world.md"


def _deck_usage(path=DECK):
    """Which container and height cap the DECK actually wraps each figure in.

    Fact, not intent.  The `FIGURES` table records what a figure was authored for; the
    deck's markup records what the theme will apply to it, and the two have disagreed
    twice -- once by a whole container (48% of the intended scale) and once by the
    `tight` modifier (0.87 instead of 0.982, on sixteen slides at a time).  So the caps
    come from here, and `emit()` fails if the table disagrees.

    Split and match exactly the way check_render.py does, or the generator and the gate
    can read different answers out of the same file.
    """
    use = {}
    for i, chunk in enumerate(path.read_text().split("\n---\n")[1:], start=1):
        cont = "col" if 'class="cols"' in chunk else "full"
        mod = ""
        for m in ("tight", "stack"):
            if f'class="fig {m}"' in chunk:
                mod = m
        for f in re.findall(r"!\[[^\]]*\]\(figures/([^)]+)\)", chunk):
            use.setdefault(Path(f).stem, []).append((i, cont, mod))
    return use


DECK_USE = _deck_usage()


def emit(name, body, container="col", pad=PAD):
    """Compile one TikZ body to figures/<name>.png and assert what lands on the slide."""
    if _only and not any(k in name for k in _only):
        return
    uses = DECK_USE.get(name)
    if uses:
        conts = {c for _, c, _ in uses}
        assert len(conts) == 1, (
            f"{name}: the deck puts this one file in {sorted(conts)} on slides "
            f"{[s for s, _, _ in uses]} -- one file cannot be authored for two "
            f"containers, emit two")
        deck_cont = conts.pop()
        assert deck_cont == container, (
            f"{name}: the FIGURES table says {container!r}, the deck's markup says "
            f"{deck_cont!r} on slide(s) {[s for s, _, _ in uses]} -- the deck is the fact")
    else:
        # Not on any slide yet (a figure written ahead of the deck edit that will use it).
        # Nothing to read, so fall back to the table and say so.
        deck_cont, uses = container, [(None, container, "")]
    w = DESIGN[container]
    hmax = int(w * 0.70)

    # Ink drawn beyond the page is cut off, and the raster edge test below only sees ink
    # that still *touches* the border -- a label at y = -2 vanishes without a trace.  The
    # generator writes these numbers, so check them exactly, at source.
    # A Bezier control point is construction, not ink -- the curve it steers stays well
    # inside it -- so it is the one coordinate allowed off the page.
    for mx, my in COORD.findall(re.sub(r"controls \([^)]*\)", "", body)):
        cx, cy = float(mx), float(my)
        assert 0 <= cx <= w and 0 <= cy <= hmax, (
            f"{name}: coordinate ({cx},{cy}) lies outside the {w}x{hmax}bp page -- "
            f"anything drawn there is silently dropped")

    # accent-3 is a fill and a ring colour.  At 2.0:1 against white it is unreadable as
    # text and invisible as a hairline, so the build refuses both.
    assert "text=accentthree" not in body, (
        f"{name}: accent-3 used as text (2.0:1 on white, floor is 3:1) -- "
        f"annotation gray or accent-2 for anything a reader has to read")
    for opts in re.findall(r"\\draw\[([^\]]*)\]", body):
        if "accentthree" not in opts:
            continue
        mw = re.search(r"line width=([\d.]+)bp", opts)
        lw = float(mw.group(1)) if mw else 0.4
        assert lw >= 4.0, (f"{name}: accent-3 stroke at {lw}bp -- accent-3 is for fills and "
                           f"rings only, never a stroke under 4bp")

    im = _render(name, body, w, hmax)
    a = np.array(im.convert("L"))
    exp = (int(round(w * PXBP)), int(round(hmax * PXBP)))
    assert im.size == exp, f"{name}: page is {im.size}, expected {exp}"

    ys, xs = np.where(a < 200)
    assert len(ys), f"{name}: blank figure"
    # The page IS the bounding box, so anything drawn outside it is silently cut off.
    # This caught two clipped captions before a human ever saw the figure.
    for side, hit in (("top", ys.min() <= 1), ("bottom", ys.max() >= a.shape[0] - 2),
                      ("left", xs.min() <= 1), ("right", xs.max() >= a.shape[1] - 2)):
        assert not hit, (f"{name}: ink runs off the {side} of the {w}x{hmax}bp canvas -- "
                         f"it is being clipped, move it inside")
    top, bot = ys.min(), ys.max()
    lo = max(0, top - int(pad * PXBP))
    hi = min(a.shape[0], bot + int(pad * PXBP))
    im = im.crop((0, lo, im.size[0], hi))

    fw, fh = im.size
    # The deck scales the image by min(width cap / file width, height cap / file height).
    # When the HEIGHT wins, every disc and every glyph in the figure shrinks by a factor
    # nothing in this file can see -- that is the defect, so it is a build failure, and
    # the message says how short the drawing has to get.
    scale, binding = 1.0, None
    for slide, cont, mod in uses:
        wcap, hcap = CONTAINER[cont], FIG_H[mod]
        sw, sh = wcap / fw, hcap / fh
        assert sh >= sw, (
            f"{name}: the height cap binds on slide {slide} -- `fig{' ' + mod if mod else ''}`"
            f" caps the image at {hcap}px and it is {fh / PXBP:.0f}bp tall, so the deck "
            f"scales it to {sh * PXBP:.3f} slide px per bp instead of {sw * PXBP:.3f}. "
            f"Shorten the drawing to {hcap * fw / wcap / PXBP:.0f}bp or less "
            f"({(fh / PXBP) - (hcap * fw / wcap / PXBP):.0f}bp of ink to lose)")
        if sw < scale:
            scale, binding = sw, (slide, cont, mod)
    factor = scale * PXBP                      # slide px per bp, as the deck applies it

    # ink must fill the canvas width, or the deck scales white margin
    span = (xs.max() - xs.min() + 1) / fw
    assert span >= INK_FILL_MIN, (
        f"{name}: ink spans {span:.0%} of the canvas width (need {INK_FILL_MIN:.0%}) -- "
        f"widen the drawing, do not shrink the canvas")

    node_px = NODE * factor
    assert NODE_MIN_PX <= node_px <= NODE_MAX_PX, f"{name}: node disc {node_px:.0f}px"
    # x-height, because that is the quantity check_render.py measures on the slide
    xh_px = XHEIGHT_BP * factor
    assert xh_px >= XHEIGHT_MIN_PX, (
        f"{name}: text x-height {xh_px:.1f}px on the slide (floor {XHEIGHT_MIN_PX}) -- "
        f"measured {XHEIGHT_BP:.2f}bp at {FONT}pt")

    # Every filled circle in the body, checked at source. A raster detector cannot do
    # this job here: the theme's node fill (#3959A6, L=88) is lighter than the ink
    # threshold that would separate a disc from the edges touching it, so discs and
    # edges merge into one component. The radius is in the TikZ we just wrote, so read
    # it from there and there is nothing to detect.
    rr = [float(m) * 2 for m in re.findall(r"\\fill\[[^\]]*\][^;]*?circle \(([\d.]+)bp\)", body)]
    rr += [float(m) for m in re.findall(r"minimum size=([\d.]+)bp", body)]
    if rr:
        lo_d, hi_d = min(rr) * factor, max(rr) * factor
        assert NODE_MIN_PX <= lo_d and hi_d <= NODE_MAX_PX, (
            f"{name}: filled circles land {lo_d:.0f}-{hi_d:.0f}px on the slide "
            f"(band {NODE_MIN_PX}-{NODE_MAX_PX}px) -- every dot is a node-sized dot")
    else:
        lo_d = hi_d = 0

    im.save(OUT / f"{name}.png")
    _built.append(name)
    where = f"fig{' ' + binding[2] if binding and binding[2] else ''}/{deck_cont}"
    if uses[0][0] is None:
        where += " (not in the deck)"
    print(f"  {name}.png  {fw}x{fh}  {where}  {factor:.3f}px/bp  node {node_px:.0f}px  "
          f"x-height {xh_px:.1f}px  discs {lo_d:.0f}-{hi_d:.0f}px  ink {span:.0%}")


# --------------------------------------------------------------------------- drawing helpers
# 26bp measured 22px on the rendered slide -- antialiasing eats ~2px a side off a small
# disc, so the band's own floor needs the headroom.
DOT = 32          # every free-standing filled dot


def dot(x, y, color="accent", d=DOT):
    return f"\\fill[{color}] ({x},{y}) circle ({d / 2}bp);\n"


_LABEL_BOX = {}
DISC_TEXT_PAD = 2      # bp of fill kept between the glyph's corner and the disc edge


def ink_box_bp(s, size=None):
    """Ink box (w, h) of a typeset string, measured off a render.  Cached per string.

    Measured, never computed: a glyph advance is not a glyph's ink, and the one thing
    the m02 rounds proved is that any number this file derives from FONT restates the
    author's intention instead of reading the page.
    """
    key = (s, size)
    if key not in _LABEL_BOX:
        im = _render("ink-box", text(550, 150, s, **({} if size is None else {"size": size})),
                     1100, 300)
        ys, xs = np.where(np.array(im.convert("L")) < 200)
        _LABEL_BOX[key] = ((xs.max() - xs.min() + 1) / PXBP,
                           (ys.max() - ys.min() + 1) / PXBP)
    return _LABEL_BOX[key]


def _label_box_bp(label):
    """Ink box of a disc label at FONT pt, measured once per distinct label."""
    return ink_box_bp(label)


def disc(x, y, label="", fill="accent", name=None, size=NODE, text="white"):
    # Size and containment are two checks, not one.  Raising m01's type until the size
    # assertion went green pushed digits out of their cells and rendered "10" and "12" as
    # a single "1012" -- garbled text is worse than small text, because small text gets
    # skipped and garbled text gets misread.  If a label stops fitting, grow the disc.
    if label:
        w, h = _label_box_bp(label)
        need = 2 * (math.hypot(w / 2, h / 2) + DISC_TEXT_PAD)
        assert need <= size, (
            f"label {label!r} is {w:.0f}x{h:.0f}bp and needs a {need:.0f}bp disc, but this "
            f"one is {size}bp -- grow the disc, never shrink the type")
    nm = f"({name})" if name else ""
    opt = f"disc,fill={fill},minimum size={size}bp"
    if text != "white":
        opt += f",text={text}"
    return f"\\node[{opt}] {nm} at ({x},{y}) {{{label}}};\n"


def ring(x, y, size=NODE, color="accenttwo", w=4.0, grow=9):
    return (f"\\draw[line width={w}bp,draw={color}] ({x},{y}) "
            f"circle ({(size + grow) / 2}bp);\n")


def edge(a, b, color="black", w=EDGE_W, dash="", bend=0, arrow=""):
    o = [f"line width={w}bp", f"draw={color}"]
    if dash:
        o.append(dash)
    if arrow:
        o.append(arrow)
    if bend:
        o.append(f"bend left={bend}")
    return f"\\draw[{','.join(o)}] ({a}) to ({b});\n"


def seg(p, q, color="black", w=EDGE_W, dash="", arrow=""):
    o = [f"line width={w}bp", f"draw={color}"]
    if dash:
        o.append(dash)
    if arrow:
        o.append(arrow)
    return f"\\draw[{','.join(o)}] ({p[0]},{p[1]}) -- ({q[0]},{q[1]});\n"


def text(x, y, s, color="black", anchor="center", size=FONT, width=None, align="center",
         rotate=0):
    _fontsizes.add(size)
    assert size >= FONT, f"font {size}pt is below the {FONT}pt floor"
    o = [f"font=\\fontsize{{{size}}}{{{int(size*1.15)}}}\\selectfont",
         f"text={color}", f"anchor={anchor}", f"align={align}"]
    if width:
        o.append(f"text width={width}bp")
    if rotate:
        o.append(f"rotate={rotate}")
    return f"\\node[{','.join(o)}] at ({x},{y}) {{{s}}};\n"


def _ink_height_bp(glyph):
    """Ink height of one glyph at FONT pt, read off the render.

    R1's blocker was a guessed ratio: `CAP_RATIO = 0.70` described a font that was never on
    the page, because LaTeX was silently substituting 24.88pt for the 30pt asked for, and
    the assertion *computed* its answer from FONT instead of reading the render.  Measure.
    """
    im = _render(f"calibration-{glyph}", text(260, 100, glyph), 520, 200)
    ys, _ = np.where(np.array(im.convert("L")) < 200)
    return (ys.max() - ys.min() + 1) / PXBP


# "x" has neither ascender nor descender, so its ink height *is* the x-height -- and the
# x-height is what check_render.py measures on the rendered slide.
XHEIGHT_BP = _ink_height_bp("x")
CAP_BP = _ink_height_bp("H")
XHEIGHT_RATIO, CAP_RATIO = XHEIGHT_BP / FONT, CAP_BP / FONT
assert CAP_BP >= 0.66 * FONT, (
    f"cap height measures {CAP_BP:.2f}bp at {FONT}pt (ratio {CAP_RATIO:.3f}) -- LaTeX is "
    f"substituting a smaller design size, so every label in the deck is shrinking silently")
assert XHEIGHT_RATIO < CAP_RATIO, (XHEIGHT_RATIO, CAP_RATIO)
print(f"font {FONT}pt: x-height {XHEIGHT_BP:.2f}bp (ratio {XHEIGHT_RATIO:.3f}), "
      f"cap {CAP_BP:.2f}bp (ratio {CAP_RATIO:.3f})")


def _bezier_pts(p0, c, p2, n=80):
    ts = np.linspace(0, 1, n)[:, None]
    p0, c, p2 = (np.array(x, float) for x in (p0, c, p2))
    return (1 - ts) ** 2 * p0 + 2 * ts * (1 - ts) * c + ts ** 2 * p2


BOWS = (0, 14, -14, 20, -20, 26, -26, 34, -34, 38, -38, 44, -44, 58, -58, 76, -76)


def curve_edge(a, b, pos, color="black", w=EDGE_W, dash="", clear=NODE / 2 + 3,
               centroid=None, side=None, paths=None):
    """Draw a--b so it clears every disc it does not end at.

    Ring lattices are the reason this exists: with 20 nodes on a circle the
    second-neighbour chord passes 7bp inside the disc between its endpoints, which is
    what hid every triangle in the Module 01 small-world figure. The bow is searched
    for, not guessed, and the function raises if no bow clears -- so the build fails
    instead of the review.

    `side=+1` forces the bow toward the centroid, `side=-1` away from it.  Two chords
    with interleaved endpoints cannot both live inside the circle without crossing
    (Jordan), so alternating the sign is the only way a ring lattice draws planar.
    `paths` collects the sampled geometry for `count_crossings`.
    """
    pa, pb = np.array(pos[a], float), np.array(pos[b], float)
    others = [np.array(q, float) for k, q in pos.items() if k not in (a, b)]
    mid = (pa + pb) / 2
    d = pb - pa
    nrm = np.array([-d[1], d[0]])
    nrm = nrm / (np.linalg.norm(nrm) or 1.0)
    if centroid is not None and np.dot(mid - np.array(centroid, float), nrm) > 0:
        nrm = -nrm                                    # "+h" always bows toward the centre
    cand = BOWS if side is None else [h for h in BOWS if h * side > 0]
    for h in cand:
        ctrl = mid + 2 * h * nrm
        pts = _bezier_pts(pa, ctrl, pb)
        if not others or min(np.linalg.norm(pts - q, axis=1).min() for q in others) >= clear:
            o = [f"line width={w}bp", f"draw={color}"] + ([dash] if dash else [])
            if paths is not None:
                # always the sampled polyline, never the two endpoints: with h = 0 the
                # control point sits on the midpoint, so `pts` IS the straight segment,
                # and a two-point path makes every clearance test vacuously true
                paths.append((a, b, pts))
            if h == 0:
                return f"\\draw[{','.join(o)}] ({pa[0]:.1f},{pa[1]:.1f}) -- ({pb[0]:.1f},{pb[1]:.1f});\n"
            return (f"\\draw[{','.join(o)}] ({pa[0]:.1f},{pa[1]:.1f}) .. controls "
                    f"({ctrl[0]:.1f},{ctrl[1]:.1f}) .. ({pb[0]:.1f},{pb[1]:.1f});\n")
    raise AssertionError(f"no bow clears every disc for edge {a}-{b} (side={side})")


def _cross(P, Q):
    """Does any segment of polyline P properly cross any segment of polyline Q?"""
    p0, p1 = P[:-1][:, None, :], P[1:][:, None, :]
    q0, q1 = Q[:-1][None, :, :], Q[1:][None, :, :]

    def turn(o, u, v):
        return ((u[..., 0] - o[..., 0]) * (v[..., 1] - o[..., 1])
                - (u[..., 1] - o[..., 1]) * (v[..., 0] - o[..., 0]))

    return bool(np.any((turn(p0, p1, q0) * turn(p0, p1, q1) < 0)
                       & (turn(q0, q1, p0) * turn(q0, q1, p1) < 0)))


def count_crossings(paths):
    """Pairs of drawn edges that cross away from a shared endpoint."""
    n = 0
    for (a1, b1, p1), (a2, b2, p2) in itertools.combinations(paths, 2):
        if {a1, b1} & {a2, b2}:
            continue
        n += _cross(p1[::4] if len(p1) > 8 else p1, p2[::4] if len(p2) > 8 else p2)
    return n


def assert_planar(name, paths):
    """A figure whose claim is 'count the triangles' must not draw phantom ones."""
    n = count_crossings(paths)
    assert n == 0, (f"{name}: {n} crossing pairs -- every crossing reads as a node that "
                    f"is not there, on a drawing whose whole job is counting")


def bend_path(pa, pb, bend, n=60):
    """Sample what TikZ's `to[bend left=<bend>]` actually draws between two points.

    `bend left=a` leaves pa turned `a` degrees to the left of the straight line, so the
    curve is the circular arc whose end tangents make that angle -- sagitta
    (L/2)tan(a/2), to the left of the direction of travel.  A quadratic Bezier with its
    control point at twice that offset has exactly that sagitta, which is close enough
    for a crossing or a clearance test and is the same sampling `curve_edge` already
    does for its own bows.

    This exists because `clearance_ok` and `count_crossings` saw straight segments only,
    so every bent edge in the deck was unchecked at source and had to be measured off
    the render by hand.
    """
    pa, pb = np.array(pa, float), np.array(pb, float)
    d = pb - pa
    L = float(np.linalg.norm(d))
    left = np.array([-d[1], d[0]]) / (L or 1.0)
    sag = (L / 2) * math.tan(math.radians(bend) / 2)
    ctrl = (pa + pb) / 2 + 2 * sag * left
    return _bezier_pts(pa, ctrl, pb, n)


def _edge_paths(edges, pos, paths=()):
    """Every drawn edge as a polyline: the sampled curve where one was given, else the
    straight segment, sampled too.

    Sampled, not left as its two endpoints: a clearance test that measures the distance
    from a node to the two ENDS of an edge always passes, because the ends are the other
    two nodes.  The disc in the middle is the one that matters.
    """
    # keyed by an unordered pair, not by min/max: node keys in this file are ints in some
    # figures and (blade, side) tuples or "hub" in others, and those do not compare
    given = {frozenset((a, b)): p for a, b, p in paths}
    out = []
    for a, b in edges:
        k = frozenset((a, b))
        if k in given:
            out.append((a, b, given[k]))
        else:
            pa, pb = np.array(pos[a], float), np.array(pos[b], float)
            t = np.linspace(0, 1, 60)[:, None]
            out.append((a, b, pa + t * (pb - pa)))
    return out


def assert_drawn_planar(name, edges, pos, paths=()):
    """If networkx calls the graph planar, the drawing has no excuse for a crossing.

    `assert_planar` existed for a whole build and was wired to exactly one figure, so
    `free-vs-not` shipped 34 crossings across 14 edges under a caption asserting there
    are no triangles.  This is the version that takes an edge list, so every node-link
    figure can be gated in one line.

    Non-planar graphs return silently -- K6 and the ego graph's ten dashed pairs cannot
    be drawn without crossings, and saying so here is what makes the silence readable.
    """
    if not nx.check_planarity(nx.Graph(list(edges)))[0]:
        return
    assert_planar(name, _edge_paths(edges, pos, paths))


def _polyline(obj, n=200):
    """One drawn thing as an (N,2) polyline: a two-point segment gets sampled, an
    already-sampled curve passes through.

    Sampling matters: a two-point path makes every containment test below vacuously
    true except at the endpoints, which is how a chord drawn straight through the word
    "printer" passed a gate that only looked at where it started and stopped.
    """
    a = np.asarray(obj, float)
    assert a.ndim == 2 and a.shape[1] == 2, f"not a path: {obj!r}"
    if len(a) == 2:
        t = np.linspace(0, 1, n)[:, None]
        return a[0] + t * (a[1] - a[0])
    return a


def text_box(x, y, s, anchor="center", size=None, rotate=0):
    """The box a `text()` call's ink lands in -- measured off a render, not computed.

    Ink box, not node box: the node box carries the font's ascender and descender space,
    and every question these gates answer (does a stroke cross the glyphs, do two labels
    read as one block) is about ink.  `text()` writes the anchor, so this reads the same
    anchor back and there is nothing to keep in sync.
    """
    w, h = ink_box_bp(s, size)
    if rotate % 180:
        w, h = h, w
    parts = anchor.split()
    x0 = x if "west" in parts else (x - w if "east" in parts else x - w / 2)
    y0 = y if "south" in parts else (y - h if "north" in parts else y - h / 2)
    return (x0, y0, x0 + w, y0 + h)


def paths_hitting_box(box, paths, pad=6):
    """Which of `paths` enter `box`.  Items are (a, b, polyline) or a bare polyline."""
    x0, y0, x1, y1 = box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad
    hit = []
    for p in paths:
        keyed = isinstance(p, tuple) and len(p) == 3
        pts = _polyline(p[2] if keyed else p)
        if np.any((pts[:, 0] >= x0) & (pts[:, 0] <= x1)
                  & (pts[:, 1] >= y0) & (pts[:, 1] <= y1)):
            hit.append(frozenset(p[:2]) if keyed else None)
    return hit


def assert_labels_clear(name, boxes, paths, pad=6):
    """No drawn path may run through a block of type.

    The accent-2 edge of the $A^3$ triangle ran through the numerator of $(A^3)_{ii}$
    and struck out the **3** -- the one symbol that slide exists to teach.  This version
    takes a dict of boxes and a list of *sampled* paths, so it can be wired to a whole
    figure in one line instead of to one label at a time; it was written for one figure
    and left there for a build, during which a red chord shipped through two occupation
    labels on two slides.
    """
    for lab, box in boxes.items():
        hit = paths_hitting_box(box, paths, pad)
        assert not hit, (
            f"{name}: {len(hit)} drawn path(s) {sorted(map(sorted, (h for h in hit if h)))} "
            f"run through the type {lab!r} at ({box[0]:.0f},{box[1]:.0f})-"
            f"({box[2]:.0f},{box[3]:.0f}) -- move the drawing or drop the label, "
            f"a struck-through glyph is worse than no glyph")


def assert_boxes_clear(name, boxes, pad=8):
    """No two blocks of type may sit within `pad` of each other.

    A note placed at a fixed corner and a label placed against the drawing are written by
    different lines and drift into each other as either grows: slide 89's axis title sat
    5px under a panel label against a body leading of 44px, so the two read as one
    two-line caption for the wrong panel.
    """
    for (na, a), (nb, b) in itertools.combinations(sorted(boxes.items()), 2):
        if (a[0] - pad < b[2] and b[0] - pad < a[2]
                and a[1] - pad < b[3] and b[1] - pad < a[3]):
            raise AssertionError(
                f"{name}: the type {na!r} at ({a[0]:.0f},{a[1]:.0f})-({a[2]:.0f},{a[3]:.0f})"
                f" comes within {pad}bp of {nb!r} at ({b[0]:.0f},{b[1]:.0f})-"
                f"({b[2]:.0f},{b[3]:.0f}) -- two blocks of type that close read as one; "
                f"move one of them or shorten it")


def assert_marks_own_edge(name, marks, paths, pad=4):
    """Each mark's box may touch the one path it marks, and nothing else.

    The two X's on `m03-teaser` were gated against *each other* -- 80bp apart, which
    passed -- while one of them sat on the last 26px of the chord the figure says it does
    NOT cut.  A mark checked against the thing it marks is a different question from a
    mark checked against its twin, and only the first one is the claim.
    """
    for key, box in marks.items():
        hit = set(paths_hitting_box(box, paths, pad))
        assert hit == {frozenset(key)}, (
            f"{name}: the mark on {tuple(key)} touches "
            f"{sorted(map(sorted, (h for h in hit if h)))} -- a mark that lands on an edge "
            f"it does not mark says the opposite of what the drawing means")


def assert_text_clear(name, box, segs, pad=6):
    """One box against a list of straight segments -- `assert_labels_clear` for one label."""
    assert_labels_clear(name, {"the label": box}, list(segs), pad)


def clearance_ok(edges, pos, r=NODE / 2 + 3, paths=()):
    """No drawn edge may pass through a disc it does not end at (m01's ring defect).

    Curved edges are sampled rather than treated as their chord: a `to[bend]` arc that
    clears a disc as a straight line can still run through it, and the reverse.
    """
    bad = []
    for a, b, pts in _edge_paths(edges, pos, paths):
        for n, p in pos.items():
            if n in (a, b):
                continue
            if float(np.linalg.norm(pts - np.array(p, float), axis=1).min()) < r:
                bad.append((a, b, n))
    return bad


# --------------------------------------------------------------------------- verified data
# Every number below is recomputed here and cross-checked against review/DECK_SPEC.md.
CHAIN_EDGES = [(i, i + 1) for i in range(6)]
CHORD = (0, 2)
SHORTCUT = (1, 5)
NAMES = ["farmer", "buyer", "teacher", "minister", "printer", "clerk", "broker"]
LETTERS = ["A", "B", "C", "D", "E", "F", "G"]


def graph(edges):
    g = nx.Graph()
    g.add_nodes_from(range(7))
    g.add_edges_from(edges)
    return g


def apl(g):
    d = dict(nx.all_pairs_shortest_path_length(g))
    tot = sum(d[i][j] for i, j in itertools.combinations(g.nodes(), 2))
    return Fraction(tot, math.comb(g.number_of_nodes(), 2))


G_CHAIN = graph(CHAIN_EDGES)
G_CHORD = graph(CHAIN_EDGES + [CHORD])
G_FULL = graph(CHAIN_EDGES + [CHORD, SHORTCUT])

assert apl(G_CHAIN) == Fraction(8, 3) and nx.diameter(G_CHAIN) == 6
assert apl(G_FULL) == Fraction(38, 21) and nx.diameter(G_FULL) == 3
assert Fraction(nx.average_clustering(G_FULL)).limit_denominator(1000) == Fraction(5, 21)
assert Fraction(nx.transitivity(G_FULL)).limit_denominator(1000) == Fraction(1, 4)
C_FULL = [Fraction(v).limit_denominator(100) for _, v in
          sorted(nx.clustering(G_FULL).items())]
assert C_FULL == [Fraction(1), Fraction(1, 3), Fraction(1, 3), 0, 0, 0, 0], C_FULL

WINDMILL = nx.windmill_graph(5, 3)
assert WINDMILL.number_of_nodes() == 11 and WINDMILL.number_of_edges() == 15
assert Fraction(nx.average_clustering(WINDMILL)).limit_denominator(1000) == Fraction(91, 99)
assert Fraction(nx.transitivity(WINDMILL)).limit_denominator(100) == Fraction(3, 11)
assert sum(nx.triangles(WINDMILL).values()) // 3 == 5
TRIPLETS = math.comb(10, 2) + 10                     # hub's 45 + one per blade
assert Fraction(3 * 5, TRIPLETS) == Fraction(3, 11)

RING20 = nx.watts_strogatz_graph(20, 4, 0)
assert Fraction(nx.average_clustering(RING20)).limit_denominator(100) == Fraction(1, 2)
assert apl(RING20) == Fraction(55, 19) and nx.diameter(RING20) == 5

L_HUMAN = math.log(8e9) / math.log(150)
assert abs(L_HUMAN - 4.55) < 0.01, L_HUMAN

# Watts & Strogatz 1998, Table 1 -- transcribed once, every ratio derived.  The sizes are
# from the same table: three networks four orders of magnitude apart is the evidence for
# the universality claim, and a figure that drops them makes the claim without it.
WS98 = [
    ("Film actors", 225226, 3.65, 2.99, 0.79, 0.00027),
    ("Power grid", 4941, 18.7, 12.4, 0.080, 0.005),
    ("C. elegans", 282, 2.65, 2.25, 0.28, 0.05),
]
WS98_R = [(n, L / Lr, C / Cr, (C / Cr) / (L / Lr)) for n, _, L, Lr, C, Cr in WS98]
WS98_N = {n: sz for n, sz, *_ in WS98}
assert [round(s) for _, _, _, s in WS98_R] == [2397, 11, 5], WS98_R
_orders = round(math.log10(max(WS98_N.values()) / min(WS98_N.values())))
WS98_ORDERS = ["no", "one", "two", "three", "four"][_orders]
assert _orders == 3, _orders

GRID = nx.grid_2d_graph(20, 20)
assert nx.transitivity(GRID) == 0


# --------------------------------------------------------------------------- Part 1
US_OUTLINE = [  # rough (lat, lon) trace of the lower 48, clockwise from the NW corner
    (49.0, -124.7), (46.3, -124.1), (42.0, -124.4), (38.0, -123.0), (34.4, -120.5),
    (32.5, -117.1), (31.3, -111.0), (31.8, -106.5), (29.8, -101.4), (25.9, -97.4),
    (29.7, -95.0), (29.2, -90.0), (30.4, -88.0), (29.7, -84.9), (25.1, -80.4),
    (30.4, -81.4), (32.8, -79.9), (35.2, -75.5), (38.0, -75.2), (40.5, -74.0),
    (41.5, -70.0), (43.7, -70.2), (44.8, -67.0), (45.0, -71.5), (45.0, -83.0),
    (46.5, -84.5), (48.0, -89.5), (49.0, -95.2),
]
CITIES = {"Omaha": (41.26, -95.93), "Wichita": (37.69, -97.34), "Boston": (42.36, -71.06)}


def _us(x0, y0, w):
    """Equirectangular lat/lon -> bp, standard parallel 38N so the shape is not squashed."""
    lon0, lon1, lat0, lat1 = -124.7, -67.0, 25.1, 49.0
    h = w * (lat1 - lat0) / ((lon1 - lon0) * math.cos(math.radians(38)))
    def f(lat, lon):
        return (x0 + (lon - lon0) / (lon1 - lon0) * w,
                y0 + (lat - lat0) / (lat1 - lat0) * h)
    return f, h


def fig_milgram_map():
    f, h = _us(30, 74, 460)
    pts = " -- ".join("(%.1f,%.1f)" % f(a, b) for a, b in US_OUTLINE)
    s = f"\\draw[line width=1.6bp,draw=annot] {pts} -- cycle;\n"
    om, wi, bo = (f(*CITIES[c]) for c in ("Omaha", "Wichita", "Boston"))
    # Both packets aim at the same point on the same disc, so the two arrowheads land on
    # top of one another and read as one smudge.  Give each its own anchor on Boston's
    # rim -- 15 degrees either side of the straight line -- and close the standoff to
    # 2bp, so each arrow visibly ARRIVES instead of stopping short of the city.
    base = [math.atan2(p[1] - bo[1], p[0] - bo[0]) for p in (om, wi)]
    mid = sum(base) / 2
    tips = []
    for p, turn in ((om, 26), (wi, -26)):
        ang = mid + math.radians(turn)
        tip = (bo[0] + math.cos(ang) * (DOT / 2 + 2), bo[1] + math.sin(ang) * (DOT / 2 + 2))
        tips.append(tip)
        s += seg(p, tip, color="annot", w=2.2, dash="dashed",
                 arrow="-{Stealth[length=9bp]}")
        s += dot(round(p[0], 1), round(p[1], 1), "accent")
    sep = math.dist(*tips)
    assert sep >= 12, f"the two arrowheads land {sep:.0f}bp apart -- they read as one mark"
    s += dot(round(bo[0], 1), round(bo[1], 1), "accenttwo")   # size encodes nothing here
    s += text(om[0] - 22, om[1] + 6, "Omaha", anchor="east")
    s += text(wi[0] - 22, wi[1] - 10, "Wichita", anchor="east")
    # clear of both the disc and the 45th-parallel stretch of coastline it used to cross
    s += text(bo[0] + 16, bo[1] + 42, "Boston", color="accenttwo", anchor="south east")
    s += text(260, 30, "160 packets, one stockbroker", color="annot")
    return s


def fig_milgram_rule():
    ys = 150
    xs = [95, 260, 425]
    s = ""
    for i, x in enumerate(xs):
        s += disc(x, ys, "", fill="accent" if i != 1 else "accenttwo", name=f"p{i}")
    s += edge("p0", "p1", color="annot", w=EDGE_W, arrow="-{Stealth[length=10bp]}")
    s += edge("p1", "p2", color="accenttwo", w=HEAVY_W, arrow="-{Stealth[length=12bp]}")
    s += text(xs[1], 200, "you", color="accenttwo")
    s += text(xs[0], 200, "sender", color="annot")
    s += text(xs[2], 200, "next hop", color="annot")
    return s


# 32 wide, not 20: the slide is a `fig tight`, so the theme caps the image at 320px and
# eight rows of packets made the HEIGHT bind -- the deck then scaled the whole figure to
# 0.87 slide px per bp and every label on it shrank.  Five rows fit, and 64 arrivals fall
# out as exactly the top two rows instead of three and a fifth.
ARR_COLS, ARR_ROWS = 32, 5
ARR_DOT = 28              # 27.5px on the slide, inside the 26-52px band
assert ARR_COLS * ARR_ROWS == 160 and 64 % ARR_COLS == 0


def fig_milgram_arrivals():
    dx, dy = 34, 52
    x0, y0 = 20, 60
    s = ""
    for i in range(160):
        r, c = divmod(i, ARR_COLS)
        x, y = x0 + c * dx, y0 + (ARR_ROWS - 1 - r) * dy
        if i < 64:
            s += dot(x, y, "accenttwo", d=ARR_DOT)
        else:
            # same diameter as the filled dots: one object drawn at two sizes reads as
            # an encoding, and 160 packets are all the same packet
            s += f"\\draw[line width=2bp,draw=annot] ({x},{y}) circle ({ARR_DOT / 2}bp);\n"
    s += text(20, 12, "64 arrived", color="accenttwo", anchor="south west")
    s += text(1080, 12, "96 never did", color="annot", anchor="south east")
    return s


def _chain_row(names, y=150, x0=95, dx=152):
    return {i: (x0 + i * dx, y) for i in range(len(names))}


def fig_six_degrees_timeline():
    # between the dot CENTRES: run past them and the rule overhangs 30bp below against
    # 20bp above, which reads as a third, unlabelled event at each end
    s = seg((60, 230), (60, 90), color="annot", w=2.4)
    for y, yr, cap, col in ((230, "1967", "Milgram mails the packets", "accent"),
                            (90, "1990", "Guare's play names it\\\\``six degrees of separation''",
                             "accenttwo")):
        s += dot(60, y, col)
        s += text(96, y, yr, color=col, anchor="west")
        s += text(210, y, cap, color="black", anchor="west", width=300)
    return s


def _numberline(dots, x0=40, x1=490, y=140, lo=0, hi=8):
    """`dots` is ordered bottom-up; each label gets its own row.  One line each, stepped by
    more than a line box -- two-line labels at a 62bp step overlapped one another."""
    s = seg((x0, y), (x1, y), color="annot", w=2.4)
    for v in range(lo, hi + 1, 2):
        x = x0 + (v - lo) / (hi - lo) * (x1 - x0)
        s += seg((x, y - 9), (x, y + 9), color="annot", w=2.0)
        s += text(x, y - 24, str(v), color="annot", anchor="north")
    s += text((x0 + x1) / 2, y - 66, "steps between two people", color="annot",
              anchor="north")
    for k, (v, lab, col) in enumerate(dots):
        x = x0 + (v - lo) / (hi - lo) * (x1 - x0)
        s += dot(round(x, 1), y, col)
        s += text(x, y + 28 + k * 46, lab, color=col, anchor="south")
    return s


def fig_replication_yahoo():
    return _numberline([(6, "Milgram 1967", "annot"), (4, "email 2003", "accenttwo")])


def fig_replication_facebook():
    return _numberline([(6, "Milgram 1967", "annot"), (4, "email 2003", "annot"),
                        (4.74, "Facebook 2012", "accenttwo")])


def fig_wikirace():
    # A zigzag, so every label sits on the outside of the path's turn instead of under a
    # red edge.  No extra edge either: the dotted Bagel--Chopin link made the route two
    # clicks, contradicting the figure's own caption.
    pos = {0: (60, 120), 1: (210, 270), 2: (360, 120), 3: (480, 260)}
    assert_drawn_planar("wikirace", [(0, 1), (1, 2), (2, 3)], pos)
    s = ""
    for i in range(4):
        s += disc(pos[i][0], pos[i][1], "", fill="accent" if i != 3 else "accenttwo", name=f"w{i}")
    for a, b in ((0, 1), (1, 2), (2, 3)):
        s += edge(f"w{a}", f"w{b}", color="accenttwo", w=HEAVY_W,
                  arrow="-{Stealth[length=11bp]}")
    for i, (l, dy, anc) in enumerate((("Bagel", -34, "north"), ("Poland", 34, "south"),
                                      ("Chopin", -34, "north"), ("Piano", 34, "south east"))):
        x = pos[i][0] + (26 if anc.endswith("east") else 0)
        s += text(x, pos[i][1] + dy, l, color="accenttwo" if i == 3 else "annot", anchor=anc)
    s += text(270, 12, "three clicks, links only", color="accenttwo", anchor="south")
    return s


def fig_routing_vs_existence():
    """One point: the route exists, but from `you` only the two neighbours are visible.

    Flattened from 60-288 to 75-265: the slide is a `fig tight`, so the theme caps the
    image at 320px, and at the old height that cap -- not the width -- set the scale.
    """
    pos = {0: (70, 170), 1: (250, 240), 2: (250, 100), 3: (500, 245), 4: (500, 95),
           5: (700, 170), 6: (880, 240), 7: (880, 100), 8: (1040, 170)}
    edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5), (5, 6), (5, 7),
             (6, 8), (7, 8)]
    route = {(0, 2), (2, 4), (4, 5), (5, 7), (7, 8)}
    assert not clearance_ok(edges, pos)
    assert_drawn_planar("routing-vs-existence", edges, pos)
    s = ("\\draw[line width=2bp,draw=annot,dash pattern=on 9bp off 7bp,"
         "rounded corners=26bp] (20,58) rectangle (340,282);\n")
    for a, b in edges:
        hot = (a, b) in route
        s += seg(pos[a], pos[b], color="accenttwo" if hot else "annot",
                 w=HEAVY_W if hot else EDGE_W)
    # Every ordinary node is a white circle, including the two inside the box.  They were
    # accent blue while all the others were white, which inverts the deck's own
    # convention -- blue is an ordinary node on all sixty-odd other figures -- so the one
    # slide that colours the visible ones differently teaches "blue means visible" for
    # exactly one slide.  The dashed box already says what is visible.
    for i, p in pos.items():
        if i in (0, 8):
            s += disc(p[0], p[1], "", fill="accenttwo")
        else:
            s += (f"\\draw[line width=2.6bp,draw=annot,fill=white] ({p[0]},{p[1]}) "
                  f"circle ({NODE / 2}bp);\n")
    s += text(70, 143, "you", color="accenttwo", anchor="north")
    s += text(1040, 143, "target", color="accenttwo", anchor="north")
    s += text(180, 288, "all you can see", color="annot", anchor="south")
    return s



# --------------------------------------------------------------------------- Part 2
CHAIN_POS = {i: (95 + i * 152, 150) for i in range(7)}   # fixed once: the graph never moves


def _chain(edges, labels=None, hot=(), hot_col="accenttwo", ringed=(), heavy_all=False,
           name_col=None, pos=CHAIN_POS, edge_num=False, curve=True, bends=None,
           out_paths=None):
    """The Milgram acquaintance graph. One routine, so the geometry cannot drift.

    `out_paths`, when given, is filled with every drawn edge as a sampled polyline, so a
    caller that also prints type can hand the two to `assert_labels_clear`.  Without it
    the occupation names below the graph were unchecked, and the shortcut arc shipped
    through the feet of "teacher" and "printer" on two slides.
    """
    s = ""
    paths = []
    order = [e for e in edges if e in CHAIN_EDGES] + [e for e in edges if e not in CHAIN_EDGES]
    for k, (a, b) in enumerate(order):
        col = hot_col if (a, b) in hot else "black"
        w = HEAVY_W if ((a, b) in hot or heavy_all) else EDGE_W
        if curve and (b - a) > 1:
            bend = (bends or {}).get((a, b), 60 if (a, b) == CHORD else -34)
            paths.append((a, b, bend_path(pos[a], pos[b], bend)))
            s += (f"\\draw[line width={w}bp,draw={col}] ({pos[a][0]},{pos[a][1]}) "
                  f"to[bend left={bend}] ({pos[b][0]},{pos[b][1]});\n")
        else:
            s += seg(pos[a], pos[b], color=col, w=w)
    # The chord and the shortcut are `to[bend]` arcs, which every geometry gate in this
    # file used to be blind to; sampled, they are checked like anything else.
    assert not clearance_ok(edges, pos, paths=paths), clearance_ok(edges, pos, paths=paths)
    assert_drawn_planar("milgram chain", edges, pos, paths)
    if out_paths is not None:
        out_paths.extend(_edge_paths(edges, pos, paths))
    for i in pos:
        s += disc(pos[i][0], pos[i][1], labels[i] if labels else "",
                  fill="accenttwo" if i in ringed else "accent")
    if edge_num:
        for k, (a, b) in enumerate(CHAIN_EDGES):
            mx = (pos[a][0] + pos[b][0]) / 2
            s += text(mx, pos[a][1] + 14, str(k + 1), color="accenttwo", anchor="south")
    return s


def _names(pos=CHAIN_POS, col="annot", dy=-34, highlight=None, paths=()):
    """`highlight` is opt-in: on every Part Two figure accent-2 is already carrying the
    chord, the shortcut, the edge counters or the diameter route, and a permanently red
    seventh name made the colour mean two things in one picture.

    `paths` is the drawn geometry from `_chain`, checked against every name box.  Pass it.
    """
    s, boxes = "", {}
    for i in range(7):
        x, y = pos[i][0], pos[i][1] + dy
        s += text(x, y, NAMES[i], color="accenttwo" if i == highlight else col,
                  anchor="north")
        boxes[NAMES[i]] = text_box(x, y, NAMES[i], anchor="north")
    assert_boxes_clear("milgram chain names", boxes, pad=4)
    assert_labels_clear("milgram chain names", boxes, paths)
    return s


# Which figures may carry the occupation names, and why the other two may not.
#
# The names sit 34bp under a row of discs, and the shortcut arc (1,5) has to cross that
# band on its way down -- so on any figure drawing SHORTCUT the arc lands inside a name.
# Both ways out are closed: deepening the arc until it clears "teacher" and "printer"
# pulls its crossing of the label row back inside "buyer" and "clerk" (their boxes are
# directly under the arc's own endpoints), and bowing it upward instead crosses the (0,2)
# chord.  Measured, not guessed: at the shipped bend the arc sits 50 red pixels inside
# "teacher" and 114 inside "printer".
#
# So the two figures that draw the shortcut lose the names, and their red annotation
# gains the letters, which are what the drawing still shows.
NAMED_FIGURES_MAY_NOT_DRAW = SHORTCUT


def _knew(edge, verb="already knew"):
    """Built from NAMES and the edge tuple, so a caption can never name the wrong pair.

    Carries the disc letter as well: on the two figures that dropped the occupation
    names, "the clerk knows the buyer" would otherwise point at nothing on the slide.
    """
    a, b = edge
    return (f"the {NAMES[a]} ({LETTERS[a]}) {verb} the {NAMES[b]} ({LETTERS[b]})")


def fig_milgram_chain():
    s = ""
    for a, b in CHAIN_EDGES:
        s += seg(CHAIN_POS[a], CHAIN_POS[b], color="annot", w=EDGE_W,
                 arrow="-{Stealth[length=11bp]}")
    for i in range(7):
        s += disc(CHAIN_POS[i][0], CHAIN_POS[i][1], "",
                  fill="accenttwo" if i == 6 else "accent")
    s += _names(highlight=6, paths=_edge_paths(CHAIN_EDGES, CHAIN_POS))
    s += text(CHAIN_POS[0][0], 196, "Omaha", color="annot", anchor="south")
    s += text(CHAIN_POS[6][0], 196, "Boston", color="accenttwo", anchor="south")
    s += text(550, 250, "six links, Omaha to Boston", color="accenttwo", anchor="south")
    return s


def fig_chain_graph():
    # no in-figure title: the deck body carries the node/edge definition and cannot drop it
    P = []
    return _chain(CHAIN_EDGES, labels=LETTERS, out_paths=P) + _names(paths=P)


def fig_distance_def():
    """Three nodes, one colour; accent-2 marks the route and nothing else.  The two ends
    carry the names the slide's formula uses, so $d(i,j)$ points at something."""
    p = {0: (70, 130), 1: (260, 250), 2: (450, 130)}
    s = seg(p[0], p[1], color="accenttwo", w=HEAVY_W)
    s += seg(p[1], p[2], color="accenttwo", w=HEAVY_W)
    for i, lab in ((0, "$i$"), (1, ""), (2, "$j$")):
        s += disc(p[i][0], p[i][1], lab, fill="accent")
    s += text(150, 205, "1", color="accenttwo", anchor="south east")
    s += text(372, 205, "2", color="accenttwo", anchor="south west")
    s += text(260, 60, "$d(i,j)=2$: edges, not miles", color="black", anchor="north")
    return s


def fig_chain_blank():
    P = []
    s = _chain(CHAIN_EDGES, labels=LETTERS, out_paths=P)
    s += ring(*CHAIN_POS[0])
    s += ring(*CHAIN_POS[6])
    s += _names(paths=P)
    s += text(550, 245, "how many edges from A to G?", color="accenttwo", anchor="south")
    return s


def fig_distance_six():
    P = []
    s = _chain(CHAIN_EDGES, labels=LETTERS, hot=set(CHAIN_EDGES), edge_num=True,
               out_paths=P)
    s += _names(paths=P)
    s += text(550, 250, "$d(A,G) = 6$", color="accenttwo", anchor="south")
    return s


def fig_chain_chord():
    P = []
    s = _chain(CHAIN_EDGES + [CHORD], labels=LETTERS, hot={CHORD}, out_paths=P)
    s += _names(paths=P)
    s += text(550, 275, _knew(CHORD), color="accenttwo", anchor="south")
    return s


def fig_two_routes():
    """A-B and B-C are drawn solid black, like every other real edge in the deck.

    They were dashed gray, which fourteen slides later means the opposite: on the ego
    figures dashed gray marks pairs that are NOT joined -- "possibilities, not edges".
    Here the same device marked two edges that certainly exist and are the route the red
    one replaces.  One device cannot mean a thing and its negation in one deck, and the
    real edges are the ones that lose, because red alone already carries "the minimum".
    """
    p = {0: (70, 120), 1: (260, 250), 2: (450, 120)}
    s = seg(p[0], p[1], color="black", w=EDGE_W)
    s += seg(p[1], p[2], color="black", w=EDGE_W)
    s += (f"\\draw[line width={HEAVY_W}bp,draw=accenttwo] ({p[0][0]},{p[0][1]}) "
          f"to[bend right=22] ({p[2][0]},{p[2][1]});\n")
    for i in p:
        s += disc(p[i][0], p[i][1], LETTERS[i], fill="accent")
    s += text(260, 300, "2 edges", color="annot", anchor="south")
    s += text(260, 48, "1 edge --- so $d(A,C)=1$", color="accenttwo", anchor="north")
    return s


def _dist_counts(g):
    d = dict(nx.all_pairs_shortest_path_length(g))
    c = {}
    for i, j in itertools.combinations(g.nodes(), 2):
        c[d[i][j]] = c.get(d[i][j], 0) + 1
    return c


CNT_CHAIN, CNT_FULL = _dist_counts(G_CHAIN), _dist_counts(G_FULL)
assert CNT_CHAIN == {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}, CNT_CHAIN
assert CNT_FULL == {1: 8, 2: 9, 3: 4}, CNT_FULL


def _dotplot(counts, mean):
    """21 pairs, one dot each, laid out in rows by distance -- so the tallest column of
    the two plots (9 pairs at d=2) still fits inside a column figure.

    The mean rule spans the dots it summarises and nothing else.  Two separate defects
    came out of letting it run the full canvas width:

    * it reached into the row-label column.  Measured on the render, the rule occupied
      rows 230-243 while the `d = 2` label's glyphs occupied 257-519 in x on those very
      rows -- 10bp of white between them -- so the red line read as a deletion mark
      struck through the label.  It now starts a measured 20bp clear of the widest label.
    * it overran the dots.  The mean falls BETWEEN two rows, so the rule is clipped to
      the wider of those two rows; drawn to the widest row in the whole plot it ended
      64bp past any dot at its own height, which is a level line pointing at nothing.
    """
    x0, dx, ytop, dy = 176, 39, 300, 46
    lab_x = 128                                   # row labels, anchored east
    ym = ytop - (float(mean) - 1) * dy
    lo, hi = math.floor(float(mean)), math.ceil(float(mean))
    xr = max(x0 + (counts.get(d, 1) - 1) * dx for d in {lo, hi})
    xl = x0 - DOT / 2 - 4
    s, row_labels = "", {}
    for d in range(1, 7):
        y = ytop - (d - 1) * dy
        s += text(lab_x, y, f"$d={d}$", color="annot", anchor="east")
        row_labels[f"$d={d}$"] = text_box(lab_x, y, f"$d={d}$", anchor="east")
        for k in range(counts.get(d, 0)):
            s += dot(x0 + k * dx, y, "accent")
    # The rule goes on top of the discs, inside a white casing.
    #
    # It used to be drawn first, so the discs covered it -- and at a mean of 1.81 it falls
    # inside the d = 2 row, so on `apl-shortcut` it survived only in the gaps between
    # discs and read as decoration threading the row rather than as a level.  Drawing it
    # in front without the casing swaps one defect for the other the old comment feared,
    # a red line struck through a row of dots.  The casing is what makes it read as a
    # line passing in FRONT: 7bp of white either side of a 3.4bp stroke, against a 32bp
    # disc, leaves two thirds of every disc it crosses intact.  `apl-chain`'s mean is
    # 2.67 and lands in a gap, so there the casing draws over nothing and the two slides
    # keep one convention between them.
    rule = ((xl, ym), (xr + DOT / 2 + 4, ym))
    # A halo, not a corridor.  At 17bp the casing spanned 254-271 against a d = 2 disc
    # spanning 238-270, so it erased the whole top cap and the row rendered as nine
    # half-moons -- the rule was legible and the data it crossed was not.  The mean lands
    # 7bp below the disc top, so anything wider than about 8bp cuts the cap off; 7bp
    # leaves the discs whole and still gives the red enough white to be read against
    # accent blue, which it cannot be on its own.
    casing = 3.4 + 3.6
    s += seg(*rule, color="white", w=casing)
    s += seg(*rule, color="accenttwo", w=3.4, dash="dash pattern=on 10bp off 7bp")
    # The rule must not reach the row labels: red across "$d=2$" reads as a strikethrough
    # on the label, and the white casing would erase part of it outright.  Checked
    # against the labels' measured boxes, padded by the casing's own half-width, rather
    # than against a hand-picked 20bp gap that knew nothing about either.
    assert_labels_clear("dotplot mean rule", row_labels, [rule], pad=casing / 2 + 4)
    s += text(260, 12, f"dashed = mean: "
                        f"${mean.numerator}/{mean.denominator} = {float(mean):.2f}$",
              color="accenttwo", anchor="south")
    return s


def fig_apl_chain():
    return _dotplot(CNT_CHAIN, apl(G_CHAIN))


def fig_apl_shortcut():
    return _dotplot(CNT_FULL, apl(G_FULL))


def fig_chain_shortcut():
    """No occupation names: this figure draws the shortcut, and the shortcut's arc has to
    cross the row those names sit in.  See NAMED_FIGURES_MAY_NOT_DRAW -- the annotation
    carries the two letters instead, so the sentence still points at the drawing.
    """
    P = []
    s = _chain(CHAIN_EDGES + [CHORD, SHORTCUT], labels=LETTERS, hot={SHORTCUT},
               out_paths=P)
    note = "one long edge: " + _knew(SHORTCUT[::-1], "knows")
    s += text(550, 285, note, color="accenttwo", anchor="south")
    assert_labels_clear("chain-shortcut", {note: text_box(550, 285, note, anchor="south")},
                        P)
    return s


DIA_PAIR = (0, 6)
assert nx.shortest_path_length(G_FULL, *DIA_PAIR) == nx.diameter(G_FULL) == 3
DIA_ROUTE = nx.shortest_path(G_FULL, *DIA_PAIR)
# Four pairs tie at the diameter, so "THE worst pair" is wrong on its own figure -- and
# the red marks one ROUTE, which is a third thing again.
DIA_TIES = [(a, b) for a, b in itertools.combinations(range(7), 2)
            if nx.shortest_path_length(G_FULL, a, b) == nx.diameter(G_FULL)]
assert len(DIA_TIES) == 4, DIA_TIES


def fig_diameter():
    hot = set()
    for a, b in zip(DIA_ROUTE, DIA_ROUTE[1:]):
        hot.add((min(a, b), max(a, b)))
    # No occupation names, for the same reason as `chain-shortcut`: this figure draws the
    # shortcut, and the arc crossed "teacher" and "printer" at 62 and 114 red pixels.
    P = []
    s = _chain(CHAIN_EDGES + [CHORD, SHORTCUT], labels=LETTERS, hot=hot, out_paths=P)
    # No count here: worksheet A asks for the diameter on the next slide, and
    # printing it now turns one of its four questions into recall.
    note = f"one of the {len(DIA_TIES)} worst pairs"
    s += text(550, 285, note, color="accenttwo", anchor="south")
    assert_labels_clear("diameter", {note: text_box(550, 285, note, anchor="south")}, P)
    return s


# Nothing here may repeat a number the deck has already put on screen: slide 27 prints
# the mean and slide 28 draws d(A,G), so the worksheet asks for four values the students
# have not been given.  All four are computed, none is typed.
WA_PAIRS = [(0, 4), (3, 6), (1, 6)]
WA_ANS = [nx.shortest_path_length(G_FULL, a, b) for a, b in WA_PAIRS]
WA_DIA = nx.diameter(G_FULL)
assert WA_ANS == [3, 3, 2], WA_ANS
assert WA_DIA == 3, WA_DIA
WA_Q = " \\quad ".join(f"$d({LETTERS[a]},{LETTERS[b]})$?" for a, b in WA_PAIRS)
WA_A = " \\quad ".join(f"$d({LETTERS[a]},{LETTERS[b]})={v}$"
                       for (a, b), v in zip(WA_PAIRS, WA_ANS))


def fig_worksheet_a():
    s = _chain(CHAIN_EDGES + [CHORD, SHORTCUT], labels=LETTERS)
    s += text(550, 285, WA_Q + " \\quad and the diameter?", color="black", anchor="south")
    return s


WA_ROUTES = [nx.shortest_path(G_FULL, a, b) for a, b in WA_PAIRS]
# The three routes share every edge they use -- (1,5) is in two of them, (4,5) in two,
# (5,6) in two -- so they cannot be traced on one graph in one colour, and three colours
# on one graph would need a legend.  One row per pair is the only reading that works.
_WA_USED = [{frozenset(e) for e in zip(r, r[1:])} for r in WA_ROUTES]
assert any(a & b for a, b in itertools.combinations(_WA_USED, 2)), (
    "the three routes are now edge-disjoint -- they would fit on one graph, so collapse "
    "these three rows back into one figure")

# The chain is redrawn at 128bp pitch instead of 152 with shallower bows, because three
# copies of the shipped geometry stack 580bp tall against a 375bp budget.  Same graph,
# same letters, same left-to-right order; only the scale moves, which is what
# `lattice-vs-random` already does for the same reason.
WA_X0, WA_DX = 260, 128
WA_ROW_Y = (75, 190, 305)
# Signs matter and the planarity gate caught them: `bend left` is signed, so the chord
# bows up (+26) and the shortcut down (-20).  Written +20, the shortcut bowed up into the
# chord and the drawing crossed itself once per row.
WA_BENDS = {CHORD: 26, SHORTCUT: -20}


def fig_worksheet_a_answer():
    """Every answered pair's shortest route, traced, with its number beside it.

    The figure used to print four bare numbers over an unannotated graph, four slides
    after slide 28 established tracing as the device for exactly this.  A student who
    reached d(D,G) = 4 the long way round had nothing to check their route against --
    only a number contradicting theirs, which teaches that they are wrong and not where.
    """
    s = ""
    boxes = {}
    # top row first: the question slide asks the three pairs in WA_PAIRS order, and y
    # counts upward, so the rows have to be handed out in reverse or the answers read
    # bottom-to-top against a question that reads top-to-bottom
    for (a, b), route, ans, y in zip(WA_PAIRS, WA_ROUTES, WA_ANS, WA_ROW_Y[::-1]):
        pos = {i: (WA_X0 + i * WA_DX, y) for i in range(7)}
        hot = {(min(u, v), max(u, v)) for u, v in zip(route, route[1:])}
        P = []
        s += _chain(CHAIN_EDGES + [CHORD, SHORTCUT], labels=LETTERS, hot=hot, pos=pos,
                    bends=WA_BENDS, out_paths=P)
        lab = f"$d({LETTERS[a]},{LETTERS[b]}) = {ans}$"
        s += text(WA_X0 - 32, y, lab, color="accenttwo", anchor="east")
        boxes[lab] = text_box(WA_X0 - 32, y, lab, anchor="east")
        assert_labels_clear(f"worksheet-a-answer row {LETTERS[a]}{LETTERS[b]}",
                            {lab: boxes[lab]}, P)
        assert len(route) - 1 == ans, (route, ans)
    dia = f"diameter $= {WA_DIA}$: no pair in the network is further apart"
    s += text(550, 352, dia, color="accenttwo", anchor="south")
    boxes[dia] = text_box(550, 352, dia, anchor="south")
    assert_boxes_clear("worksheet-a-answer", boxes)
    return s



# --------------------------------------------------------------------------- Part 3
def ellipse_pos(n, cx, cy, rx, ry, start=90, ccw=True):
    out = {}
    for i in range(n):
        a = math.radians(start + (360 / n) * (i if ccw else -i))
        out[i] = (cx + rx * math.cos(a), cy + ry * math.sin(a))
    return out


def antiprism_pos(n, cx, cy, rx, ry, inner, start=90):
    """Positions for C_n(1,2) that draw it planar with straight edges.

    C_n(1,2) IS the (n/2)-antiprism.  Put the even nodes on an outer ellipse and the odd
    nodes on a concentric inner one and the two families of edge separate cleanly: the
    +2 edges become the two (n/2)-gons, the +1 edges the zigzag between them.  Zero
    crossings, and every triangle draws as a triangle.

    On one ellipse there is no such drawing.  Bow every skip chord inward and adjacent
    chords cross at every node -- sixteen crossings on the slide whose claim is that
    triangles are everywhere, with each triangle rendering as a lens.  Alternate the bows
    in and out instead and the crossings go, but an outward bow has to clear its disc
    from the far side, and the result is a wavy flower in which no triangle can be picked
    out at all.  The antiprism dissolves the trade rather than choosing a side.
    """
    assert n % 2 == 0, n
    step = 720.0 / n                      # even nodes sit two ring steps apart
    out = {}
    for k in range(n // 2):
        a = math.radians(start + step * k)
        out[2 * k] = (cx + rx * math.cos(a), cy + ry * math.sin(a))
        b = math.radians(start + step * k + step / 2)
        out[2 * k + 1] = (cx + inner * rx * math.cos(b), cy + inner * ry * math.sin(b))
    return out


TRI_L = {0: (55, 105), 1: (125, 255), 2: (195, 105)}
TRI_R = {0: (325, 105), 1: (395, 255), 2: (465, 105)}


def _closed_panel(p):
    s = "".join(seg(p[a], p[b], color="accenttwo", w=HEAVY_W)
                for a, b in ((0, 1), (1, 2), (0, 2)))
    return s + "".join(disc(p[i][0], p[i][1], "", fill="accent") for i in p)


def fig_triangle_only():
    """The closed panel alone: same shape, same colours, same disc size as the left half
    of `triangle-triplet`, centred and scaled so it is not a third of a canvas."""
    p = {0: (75, 105), 1: (260, 290), 2: (445, 105)}
    s = _closed_panel(p)
    s += text(260, 320, "all three edges: a triangle", color="accenttwo",
              anchor="south")
    return s


def fig_triangle_triplet():
    s = _closed_panel(TRI_L)
    for a, b in ((0, 1), (1, 2)):
        s += seg(TRI_R[a], TRI_R[b], color="black", w=EDGE_W)
    for i in TRI_R:
        s += disc(TRI_R[i][0], TRI_R[i][1], "", fill="accent")
    # 134, not the panel centre 125: the label measures 251bp and centring it on the
    # panel ran its first glyph off the left edge of the canvas
    s += ring(*TRI_L[1], color="accentthree", w=4.0)
    s += ring(*TRI_R[1], color="accentthree", w=4.0)
    s += text(134, 55, "closed", color="accenttwo", anchor="north")
    s += text(395, 55, "open", color="black", anchor="north")
    # The heading used to read "three nodes, two edges or three" -- the node-SET
    # definition, under which the windmill has 45 triplets against the 55 that slides
    # 45 and 46 print. The centre node is the whole content of the definition the deck
    # now uses, so it is ringed in both panels rather than only described.
    s += text(260, 320, "two edges, one centre node", color="annot",
              anchor="south")
    return s


TRI_C = [{0: (40 + 370 * k, 120), 1: (145 + 370 * k, 285), 2: (250 + 370 * k, 120)}
         for k in range(3)]


def fig_triplet_three_corners():
    """One triangle drawn three times, a different corner ringed each time.

    This is what makes the deck's 3 x 5 add up: a triplet is counted at its centre, so a
    triangle holds three closed triplets, one centred at each corner -- and 3 x 5 / 55 is
    the number slide 45 derives. Stating that in prose and not drawing it was how the
    windmill's 45-vs-55 contradiction survived two rounds.
    """
    s = ""
    for k, p3 in enumerate(TRI_C):
        for a, b in ((0, 1), (1, 2), (0, 2)):
            s += seg(p3[a], p3[b], color="accenttwo", w=HEAVY_W)
        for i in p3:
            s += disc(p3[i][0], p3[i][1], "", fill="accent")
        s += ring(*p3[k], color="accentthree", w=4.0)
    s += text(550, 22, "one triangle, three closed triplets --- one centred at each corner",
              color="annot", anchor="south")
    return s


EGO = ellipse_pos(5, 260, 190, 190, 150, start=18)
EGO_LINKS = [(0, 1), (2, 3)]
EGO_ALL = list(itertools.combinations(range(5), 2))
assert len(EGO_ALL) == math.comb(5, 2) == 10


def _ego(links=(), dashed=(), link_col="accenttwo"):
    s = ""
    for a, b in dashed:
        s += seg(EGO[a], EGO[b], color="annot", w=2.0,
                 dash="dash pattern=on 7bp off 6bp")
    for i in EGO:
        s += seg((260, 190), EGO[i], color="black", w=EDGE_W)
    for a, b in links:
        s += seg(EGO[a], EGO[b], color=link_col, w=HEAVY_W)
    s += disc(260, 190, "A", fill="accent")
    for i in EGO:
        s += disc(EGO[i][0], EGO[i][1], "", fill="accent")
    return s


def fig_ego_graph():
    s = _ego()
    s += text(260, 12, "A has five friends", color="black", anchor="south")
    return s


def fig_ego_pairs():
    s = _ego(dashed=EGO_ALL)
    s += text(260, 12, "how many pairs among them?", color="black", anchor="south")
    return s


def fig_ego_pairs_count():
    s = _ego(dashed=EGO_ALL)
    s += text(260, 12, "$5\\times 4/2 = 10$ possible edges", color="accenttwo",
              anchor="south")
    return s


def fig_ego_clustering():
    s = _ego(links=EGO_LINKS, dashed=[e for e in EGO_ALL if e not in EGO_LINKS])
    s += text(260, 12, "2 of the 10 exist: $C_A = 0.2$", color="accenttwo", anchor="south")
    return s


# Lifted 40bp off the floor: the $C_i$ formula under this triangle is a stacked fraction
# ~100bp tall, and with the base edge at y = 100 the accent-2 stroke ran straight through
# the numerator and crossed out the 3 in $(A^3)_{ii}$.
TRI = {0: (68, 140), 1: (452, 140), 2: (260, 320)}
TRI_EDGES = [(0, 1), (1, 2), (0, 2)]


def _triangle(cols=("black", "black", "black")):
    s = ""
    for (a, b), c in zip(((0, 1), (1, 2), (0, 2)), cols):
        s += seg(TRI[a], TRI[b], color=c, w=EDGE_W)
    for i, lab in ((0, "$i$"), (1, "$j$"), (2, "$\\ell$")):
        s += disc(TRI[i][0], TRI[i][1], lab, fill="accent")
    return s


TRI_CEN = tuple(sum(c) / 3 for c in zip(*TRI.values()))


def _walk_loop(order, t, color, w):
    """One closed walk drawn *inside* the triangle: the three edges, inset toward the
    centroid, rounded, with a single arrowhead saying which way round it goes.

    The old version drew six arcs between three nodes -- every edge twice, no arrowhead
    anywhere -- on the one slide whose job is counting."""
    pts = [tuple(TRI_CEN[k] + t * (TRI[i][k] - TRI_CEN[k]) for k in (0, 1)) for i in order]
    pts.append(pts[0])
    stop = tuple(pts[-2][k] + 0.55 * (pts[-1][k] - pts[-2][k]) for k in (0, 1))
    path = " -- ".join("(%.1f,%.1f)" % q for q in pts[:-1] + [stop])
    return (f"\\draw[line width={w}bp,draw={color},rounded corners=16bp,"
            f"-{{Stealth[length=13bp]}},postaction={{decorate,decoration={{markings,"
            f"mark=at position 0.42 with {{\\arrow{{Stealth[length=13bp]}}}}}}}}] {path};\n")


def fig_a3_walks():
    """Both walks in accent-2, nested, told apart by which way the arrows point.

    The second walk was accent-3: a 2.01:1 stroke against white where accent-2 on the
    same figure measures 5.6:1, under a caption asking the room to tell the two apart by
    colour.  Direction is the thing that differs, so direction is what carries it.
    """
    s = "".join(seg(TRI[a], TRI[b], color="black", w=EDGE_W) for a, b in TRI_EDGES)
    # the two loops break on OPPOSITE edges: written to start at the same node they both
    # opened next to node i, and two open ends 30bp apart read as one spiral rather than
    # as two closed walks
    s += _walk_loop((0, 1, 2), 0.68, "accenttwo", 3.4)     # i -> j -> l -> i, opens left
    s += _walk_loop((1, 0, 2), 0.32, "accenttwo", 3.4)     # j -> i -> l -> j, opens right
    for i, lab in ((0, "$i$"), (1, "$j$"), (2, "$\\ell$")):
        s += disc(TRI[i][0], TRI[i][1], lab, fill="accent")
    s += text(260, 20, "two ways round: $(A^3)_{ii} = 2$", color="accenttwo",
              anchor="south")
    return s


A3_FORMULA = "$C_i = \\dfrac{(A^3)_{ii}}{k_i(k_i-1)} = \\dfrac{2}{2\\cdot 1} = 1$"


def fig_a3_formula():
    s = _triangle(("accenttwo", "accenttwo", "accenttwo"))
    s += text(260, 20, A3_FORMULA, color="accenttwo", anchor="south")
    fw, fh = ink_box_bp(A3_FORMULA)
    assert_text_clear("a3-formula", (260 - fw / 2, 20, 260 + fw / 2, 20 + fh),
                      [(TRI[a], TRI[b]) for a, b in TRI_EDGES])
    return s


CBAR_FULL = sum(C_FULL, Fraction(0)) / 7
assert CBAR_FULL == Fraction(5, 21), CBAR_FULL


def fig_cbar_milgram():
    """The per-node values are gone: this slide's point is the averaging, and printing
    all seven both duplicated slide 41 and left the worksheet nothing to compute."""
    s = _chain(CHAIN_EDGES + [CHORD, SHORTCUT], labels=LETTERS)
    s += text(550, 285, f"average over the 7 nodes: $\\bar C = "
                        f"{CBAR_FULL.numerator}/{CBAR_FULL.denominator} "
                        f"= {float(CBAR_FULL):.2f}$", color="accenttwo", anchor="south")
    return s


# --- windmill: hub + 5 blades -------------------------------------------------
# ry 132, not 150: `transitivity-def` sits in a `fig tight`, whose 320px cap bound the
# scale at 285bp of blade spread.  All four windmill figures share the geometry, so they
# all shrink together and the graph does not change size between consecutive slides.
WM_HUB = (300, 190)
WM_RX, WM_RY = 245, 132
WM = {}
for _b in range(5):
    for _s2, _off in ((0, -18), (1, 18)):
        _a = math.radians(18 + 72 * _b + _off)
        WM[(_b, _s2)] = (WM_HUB[0] + WM_RX * math.cos(_a), WM_HUB[1] + WM_RY * math.sin(_a))
WM_EDGES = [((b, s2), "hub") for b in range(5) for s2 in (0, 1)] + \
           [((b, 0), (b, 1)) for b in range(5)]
WM_POS = {**WM, "hub": WM_HUB}
assert not clearance_ok(WM_EDGES, WM_POS)
assert_drawn_planar("windmill", WM_EDGES, WM_POS)


def _windmill(blade_label="", hub_label=""):
    s = ""
    for b in range(5):
        for s2 in (0, 1):
            s += seg(WM_HUB, WM[(b, s2)], color="black", w=EDGE_W)
        s += seg(WM[(b, 0)], WM[(b, 1)], color="black", w=EDGE_W)
    for b in range(5):
        for s2 in (0, 1):
            s += disc(WM[(b, s2)][0], WM[(b, s2)][1], blade_label, fill="accent")
    s += disc(WM_HUB[0], WM_HUB[1], hub_label, fill="accent")
    return s


def _hub_leader(to_x, to_y):
    """A leader that does not read as an eleventh edge.

    Started at the hub's own centre it left the disc at exactly the point the ten spokes
    leave it, so the hub drew with eleven lines coming out of it on the slide that asks
    how many pairs of the hub's neighbours are joined.  56bp out is 36bp of white past
    the disc's rim -- clearly a pointer, not a spoke.
    """
    dx, dy = to_x - WM_HUB[0], to_y - WM_HUB[1]
    L = math.hypot(dx, dy)
    start = (WM_HUB[0] + dx / L * 56, WM_HUB[1] + dy / L * 56)
    gap = 56 - NODE / 2
    assert gap >= 30, f"the hub leader starts {gap:.0f}bp off the disc -- it reads as a spoke"
    return seg((round(start[0], 1), round(start[1], 1)), (to_x, to_y),
               color="accenttwo", w=2.2)


def fig_windmill():
    s = _windmill()
    s += text(760, 240, "one hub,\\\\five closed blades", color="black", anchor="west",
              width=330)
    s += text(760, 110, "how clustered\\\\is this network?", color="accenttwo",
              anchor="west", width=330)
    return s


def fig_windmill_cbar():
    # the blade digit is explained here, by the line naming it, and nowhere else
    s = _windmill(blade_label="1")
    s += _hub_leader(700, 120)
    s += text(712, 120, "hub: $C_i = 1/9$", color="accenttwo", anchor="west")
    s += text(712, 250, "each blade node: $C_i = 1$", color="black", anchor="west")
    s += text(700, 40, "$\\bar C = 91/99 = 0.92$", color="accenttwo", anchor="west")
    return s


def fig_windmill_split():
    # no blade digit: nothing on THIS slide says what the 1 is, and an unexplained
    # number inside every node reads as a node label
    s = _windmill()
    s += _hub_leader(700, 120)
    s += text(712, 120, "the hub owns 45\\\\of the 55 triplets", color="accenttwo",
              anchor="west", width=370)
    s += text(700, 300, "node-weighted: $\\bar C = 0.92$", color="black", anchor="west")
    s += text(700, 30, "triplet-weighted: $C = 0.27$", color="accenttwo", anchor="west")
    return s


# Every number this figure prints, derived rather than asserted.  A triplet is counted at
# its CENTRE node -- the middle node of the two edges -- so a node of degree k contributes
# C(k,2) of them and one triangle contains three closed triplets.  That is the deck's own
# definition as of slide 34, and it is the only reading that produces the deck's 0.27.
WM_HUB_K = 10                                     # the hub's degree
WM_BLADE_K = 2                                    # every blade node's degree
WM_HUB_TRIPLETS = math.comb(WM_HUB_K, 2)          # 45
WM_BLADE_TRIPLETS = 10 * math.comb(WM_BLADE_K, 2)  # 10 nodes x 1
WM_TRIANGLES = sum(nx.triangles(WINDMILL).values()) // 3
WM_CLOSED = 3 * WM_TRIANGLES                      # three closed triplets per triangle
WM_T = Fraction(WM_CLOSED, WM_HUB_TRIPLETS + WM_BLADE_TRIPLETS)
assert sorted(dict(WINDMILL.degree()).values()) == [2] * 10 + [10]
assert WM_HUB_TRIPLETS + WM_BLADE_TRIPLETS == TRIPLETS == 55
assert WM_T == Fraction(3, 11) and abs(float(WM_T) - nx.transitivity(WINDMILL)) < 1e-12


def fig_transitivity_def():
    """The arithmetic, set as mathematics, next to the drawing it is counted from.

    This figure used to print "5 triangles shaded / 55 triplets in all", which asserts
    the 55 without deriving it -- and 55 is exactly the number that separates the deck's
    definition of a triplet from the wrong one, so it is the number that has to be shown
    being built.
    """
    s = ""
    for b in range(5):
        p, q = WM[(b, 0)], WM[(b, 1)]
        s += (f"\\fill[accenttwo,opacity=0.24] ({WM_HUB[0]},{WM_HUB[1]}) -- "
              f"({p[0]:.1f},{p[1]:.1f}) -- ({q[0]:.1f},{q[1]:.1f}) -- cycle;\n")
    s += _windmill()
    x, total = 620, WM_HUB_TRIPLETS + WM_BLADE_TRIPLETS
    s += text(x, 302, "each node: $\\binom{k_i}{2}$ triplets", color="black",
              anchor="west")
    s += text(x, 232, f"hub $\\binom{{{WM_HUB_K}}}{{2}} = {WM_HUB_TRIPLETS}$",
              color="black", anchor="west")
    s += text(x, 190, f"$+$ 10 blade nodes $\\times \\binom{{2}}{{2}} = "
                      f"{WM_BLADE_TRIPLETS}$", color="black", anchor="west")
    s += text(x, 132, f"${WM_HUB_TRIPLETS} + {WM_BLADE_TRIPLETS} = {total}$ triplets",
              color="black", anchor="west")
    s += text(x, 80, f"$C = \\dfrac{{3 \\times {WM_TRIANGLES}}}{{{total}}} = "
                     f"\\dfrac{{{WM_T.numerator}}}{{{WM_T.denominator}}} "
                     f"= {float(WM_T):.2f}$", color="accenttwo", anchor="west")
    return s


WB_NODES = [0, 1, 3]
WB_ANS = [C_FULL[i] for i in WB_NODES]
assert WB_ANS == [Fraction(1), Fraction(1, 3), Fraction(0)], WB_ANS


def fig_worksheet_b():
    s = _chain(CHAIN_EDGES + [CHORD, SHORTCUT], labels=LETTERS)
    s += text(550, 285, "$C_A$? \\quad $C_B$? \\quad $C_D$?", color="black", anchor="south")
    return s


def fig_worksheet_b_answer():
    """No printed value at all: the deck reveals the three answers one fragment at a
    time, and a figure that prints anything computed leads them.

    The $\\bar C$ line was worse than the three answers would have been -- it is the
    average, which the deck reveals LAST, and it was the only coloured type on the
    slide.  What the figure can carry without leading is which three nodes are being
    asked about, so it rings them.
    """
    s = _chain(CHAIN_EDGES + [CHORD, SHORTCUT], labels=LETTERS)
    for i in WB_NODES:
        s += ring(*CHAIN_POS[i])
    return s



# --------------------------------------------------------------------------- Part 4
def fig_paradox():
    """Flattened, and the cluster's caption moved from above it to the empty band below.

    The slide is a `fig tight`: the theme caps the image at 320px, and at the old spread
    the cap -- not the width -- set the scale, so every disc and every glyph on the slide
    shrank by 11% with nothing in this file able to see it.
    """
    cl = {0: (70, 222), 1: (160, 278), 2: (250, 234), 3: (150, 170), 4: (258, 138)}
    cle = [(0, 1), (1, 2), (0, 3), (1, 3), (2, 3), (3, 4), (2, 4)]
    # Eleven gray hops out to the stranger, not five.  At five the drawing quietly
    # answered its own question -- the slide asks "so why is anyone 4.74 steps away?" over
    # a picture in which the far end is five steps away, which makes local wiring look
    # perfectly capable of it.  The route has to be visibly longer than the number the
    # deck is about to produce, or there is no paradox to have.
    n_chain = 11
    chain = {5 + k: (340 + k * 68, 196 + (k % 2) * 36) for k in range(n_chain)}
    last = 5 + n_chain - 1
    pos = {**cl, **chain}
    gray = [(2, 5)] + [(5 + k, 6 + k) for k in range(n_chain - 1)]
    edges = cle + gray
    assert len(gray) == 11 and 10 <= len(gray) <= 12, len(gray)
    assert nx.shortest_path_length(nx.Graph(edges), 0, last) > 2 * 4.74, (
        "the long way out must be plainly longer than the 4.74 the deck is about to "
        "quote, or the drawing answers the question it is asking")
    assert not clearance_ok(edges, pos)
    assert_drawn_planar("paradox", edges, pos)
    s = ""
    for a, b in edges:
        s += seg(pos[a], pos[b], color="black" if (a, b) in cle else "annot", w=EDGE_W)
    for i2, q in pos.items():
        s += disc(q[0], q[1], "", fill="accenttwo" if i2 == last else "accent")
    s += text(36, 105, "friends of friends are friends", color="black",
              anchor="north west")
    s += text(1090, 160, "a stranger", color="accenttwo", anchor="north east")
    s += text(620, 42, "local wiring only --- so why is anyone 4.74 steps away?",
              color="accenttwo", anchor="north")
    return s


K6 = ellipse_pos(6, 260, 200, 200, 125, start=0)


def fig_complete_graph():
    s = ""
    for a, b in itertools.combinations(range(6), 2):
        s += seg(K6[a], K6[b], color="black", w=EDGE_W)
    for i2 in K6:
        s += disc(K6[i2][0], K6[i2][1], "", fill="accent")
    s += text(260, 20, "every pair joined: $\\bar C = 1$, $\\bar L = 1$",
              color="accenttwo", anchor="south")
    return s


ER6 = ellipse_pos(6, 260, 205, 200, 125, start=0)
ER6_EDGES = [(0, 1), (1, 3), (2, 4), (3, 4), (0, 5)]


def fig_er_coin():
    s = ""
    for a, b in itertools.combinations(range(6), 2):
        if (a, b) not in ER6_EDGES:
            s += seg(ER6[a], ER6[b], color="annot", w=1.8,
                     dash="dash pattern=on 6bp off 7bp")
    for a, b in ER6_EDGES:
        s += seg(ER6[a], ER6[b], color="accenttwo", w=HEAVY_W)
    for i2 in ER6:
        s += disc(ER6[i2][0], ER6[i2][1], "", fill="accent")
    # 531bp of type on a 520bp canvas clipped the first word; this says the same thing
    # in 426, and in the words $G(n,p)$ is introduced with two parts later
    s += text(260, 20, "one coin per pair: heads at $p$", color="accenttwo",
              anchor="south")
    return s


def fig_er_degree():
    """Slide 57's own figure. It used to borrow slide 54's `er-coin.png` -- the only
    reuse in the deck -- so the drawing said "one coin per pair" while the slide's point
    is that ONE NODE holds n-1 of those coins. Nothing in the borrowed picture singled
    out a node, and the figcaption claimed a per-node reading it did not support."""
    hub = 0
    s = ""
    for a, b in itertools.combinations(range(6), 2):
        if hub in (a, b):
            continue
        s += seg(ER6[a], ER6[b], color="annot", w=1.4,
                 dash="dash pattern=on 5bp off 8bp")
    for b in range(1, 6):
        drawn = (min(hub, b), max(hub, b)) in ER6_EDGES
        s += seg(ER6[hub], ER6[b], color="accenttwo" if drawn else "annot",
                 w=HEAVY_W if drawn else 2.2,
                 dash="" if drawn else "dash pattern=on 6bp off 7bp")
    for i2 in ER6:
        s += disc(ER6[i2][0], ER6[i2][1], "", fill="accent")
    s += ring(ER6[hub][0], ER6[hub][1], color="accentthree", w=4.0)
    s += text(260, 20, f"this node: $n-1 = {len(ER6) - 1}$ coins",
              color="accenttwo", anchor="south")
    return s


def fig_er_clustering():
    """No ring on one pair: it was bigger than every node disc and read as an extra node
    -- or as 'this pair is special', which is the opposite of the point."""
    s = _ego(dashed=EGO_ALL)
    s += text(260, 14, "10 pairs, 10 coins: $C_{\\mathrm{rand}} = p$",
              color="accenttwo", anchor="south")
    return s


# rows at 60/178/296, not 60/200/340: the slide is a `fig tight` and the 320px cap bound
# the scale at the old spread
FAN_Y = (60, 178, 296)
FAN_L1 = [340, 620, 900]
FAN_L2 = [250, 340, 430, 530, 620, 710, 810, 900, 990]


def _fanout():
    pos = {"you": (620, FAN_Y[0])}
    pos.update({("a", x): (x, FAN_Y[1]) for x in FAN_L1})
    pos.update({("b", j): (x, FAN_Y[2]) for j, x in enumerate(FAN_L2)})
    edges = [("you", ("a", x)) for x in FAN_L1]
    edges += [(("a", FAN_L1[j // 3]), ("b", j)) for j in range(len(FAN_L2))]
    assert not clearance_ok(edges, pos)
    assert_drawn_planar("fanout", edges, pos)
    s = ""
    for a, b in edges:
        s += seg(pos[a], pos[b], color="black", w=EDGE_W)
    s += disc(620, FAN_Y[0], "", fill="accenttwo")
    for x in FAN_L1:
        s += disc(x, FAN_Y[1], "", fill="accent")
    for x in FAN_L2:
        s += disc(x, FAN_Y[2], "", fill="accent")
    return s


def fig_fanout():
    s = _fanout()
    s += text(200, FAN_Y[0], "you", color="accenttwo", anchor="east")
    s += text(200, FAN_Y[1], "$\\langle k \\rangle$", color="black", anchor="east")
    s += text(200, FAN_Y[2], "$\\langle k \\rangle^2$", color="black", anchor="east")
    return s


POW = [150 ** L for L in range(1, 6)]
assert abs(math.log(8e9) / math.log(150) - 4.55) < 0.01


def fig_fanout_solve():
    """The vertical axis is logarithmic, so it has to say so: unlabelled, exponential
    fan-out renders as a straight line, which is the opposite of the slide's point.

    The axis corner moved right, from 118 to 166.  The rotated title sat at x = 38 in a
    band 22-55bp wide, and the tick labels -- anchored east at x = 100 -- reach back to
    x = 10, so "reached" shared pixels with the 1 of $10^{11}$ and "people" touched the 1
    of $10^2$.  There was no room to move the title further left: at 25bp further out its
    own ink runs off the canvas.  So the plot gives up 48bp instead, and the title's x is
    now solved from the widest tick label rather than picked.
    """
    xa, ya = 166, 100                       # axis corner
    x0, x1, y1 = 190, 1030, 292             # 292: `fig tight` caps the image at 320px
    def X(L):
        return x0 + (L - 1) / 4 * (x1 - x0)
    def Y(v):
        return ya + (math.log10(v) - 2) / 9 * (y1 - ya)

    s = seg((xa, ya), (1060, ya), color="annot", w=2.2)
    s += seg((xa, ya), (xa, y1), color="annot", w=2.2)
    ticks = {}
    for e in range(2, 12):
        y = Y(10 ** e)
        s += seg((xa - 9, y), (xa + 9, y), color="annot", w=2.0)
        if e % 3 == 2:
            lab = f"$10^{{{e}}}$"
            s += text(xa - 18, y, lab, color="annot", anchor="east")
            ticks[lab] = text_box(xa - 18, y, lab, anchor="east")

    # Solved, not placed: sit the title one gap to the left of the widest tick label.
    title = "people reached"
    tw, th = ink_box_bp(title)
    title_x = min(b[0] for b in ticks.values()) - 14 - th / 2
    assert title_x - th / 2 >= 6, (
        f"the y-axis title's ink would start at x = {title_x - th / 2:.0f} -- there is no "
        f"room beside the tick labels, so move the plot right (raise xa), never overlap")
    s += text(round(title_x, 1), (ya + y1) / 2, title, color="annot", rotate=90)
    ticks[title] = text_box(title_x, (ya + y1) / 2, title, rotate=90)
    assert_boxes_clear("fanout-solve", ticks, pad=6)

    ypop = Y(8e9)
    s += seg((xa, ypop), (1060, ypop), color="accenttwo", w=3.2,
             dash="dash pattern=on 10bp off 7bp")
    s += text(990, ypop + 6, "8 billion people", color="accenttwo", anchor="south east")

    prev = None
    for L, v in zip(range(1, 6), POW):
        pt = (X(L), Y(v))
        if prev:
            s += seg(prev, pt, color="accent", w=3.0)
        prev = pt
    for L, v in zip(range(1, 6), POW):
        s += dot(round(X(L), 1), round(Y(v), 1), "accent")
        s += text(X(L), ya - 14, str(L), color="annot", anchor="north")
    s += text(589, ya - 52, "steps from you, at 150 friends each", color="annot",
              anchor="north")
    # under the curve, not above the plot: at y = 318 this label was the tallest ink in
    # the figure and it alone pushed a `fig tight` slide past the theme's 320px cap
    s += text(600, 120, "$L = \\ln n / \\ln \\langle k \\rangle = 4.55$",
              color="accenttwo", anchor="south west")
    return s


RND12 = nx.gnm_random_graph(12, 14, seed=1)
assert sum(nx.triangles(RND12).values()) == 0, "the free-vs-not graph must be triangle-free"
assert nx.is_connected(RND12)


# The old layout put all twelve nodes on one ellipse and drew the 14 edges as chords,
# which crossed 34 times -- and every crossing reads as a node that is not there, so the
# drawing manufactured apparent triangles directly under a caption whose whole claim is
# that there are none.  The graph is planar; the drawing has to be.
#
# These coordinates are not hand-placed and not a spring layout.  `nx.spring_layout`
# draws this graph planar in 2 of 1800 tries and never with room for a 40bp disc; the
# Chrobak-Payne embedding `nx.planar_layout` returns is crossing-free but puts adjacent
# nodes 32bp apart in a 520bp column, so the discs overlap.  So the embedding was relaxed
# by coordinate descent under a hard no-crossing gate: each node in turn moves to the
# position that most reduces the total squared violation of "58bp between centres" and
# "28bp between an edge and any disc it does not end at", and any move that creates a
# crossing is rejected outright.  The four properties that makes true are re-asserted
# here on every build, so a drift fails it.
RND12_POS = {0: (59.7, 66.0), 1: (267.0, 244.2), 2: (201.9, 146.4), 3: (244.7, 186.8),
             4: (287.2, 336.0), 5: (324.8, 236.8), 6: (185.8, 221.8), 7: (466.8, 66.0),
             8: (256.0, 99.6), 9: (294.5, 142.9), 10: (183.0, 281.4), 11: (340.0, 307.2)}
assert set(RND12_POS) == set(RND12)
assert all(20 <= x <= 500 and 20 <= y <= 344 for x, y in RND12_POS.values())
assert min(math.dist(RND12_POS[a], RND12_POS[b])
           for a, b in itertools.combinations(RND12, 2)) >= NODE + 4
assert not clearance_ok(RND12.edges(), RND12_POS, r=NODE / 2 + 6)
# The farthest node FROM NODE 0 is node 0's eccentricity (3), not the diameter (4):
# eight pairs sit at distance 4, and none of them involves node 0.  Seven slides later
# the ring figure prints the same phrase and does assert it equals the diameter.
RND12_PAIR = min((p for p in itertools.combinations(RND12, 2)
                  if nx.shortest_path_length(RND12, *p) == nx.diameter(RND12)))
RND12_PATH = nx.shortest_path(RND12, *RND12_PAIR)
assert len(RND12_PATH) - 1 == nx.diameter(RND12), (RND12_PATH, nx.diameter(RND12))


def fig_free_vs_not():
    s = ""
    hot = {(min(a, b), max(a, b)) for a, b in zip(RND12_PATH, RND12_PATH[1:])}
    paths = []
    for a, b in RND12.edges():
        e = (min(a, b), max(a, b))
        s += seg(RND12_POS[a], RND12_POS[b], color="accenttwo" if e in hot else "black",
                 w=HEAVY_W if e in hot else EDGE_W)
    assert_drawn_planar("free-vs-not", RND12.edges(), RND12_POS)
    for i2 in RND12_POS:
        s += disc(RND12_POS[i2][0], RND12_POS[i2][1], "", fill="accent")
    s += text(260, 12, f"{len(RND12_PATH)-1} hops across, and no triangle",
              color="accenttwo", anchor="south")
    return s


def fig_sigma_def():
    """A number line that says what its numbers are.  The old one built three tick labels
    and emitted none of them, so sigma = 1 -- the whole point -- was an unlabelled gray
    dot; and the definition it carried is already in the slide's formula panel."""
    y = 200
    xd = 40 + 0.5 * 460
    s = seg((40, y), (500, y), color="annot", w=2.4)
    s += f"\\draw[line width=6bp,draw=accenttwo] ({xd},{y}) -- (500,{y});\n"
    for v, lab in ((0.22, "$\\sigma < 1$"), (0.5, "$\\sigma = 1$"), (0.82, "$\\sigma > 1$")):
        x = 40 + v * 460
        s += seg((x, y - 10), (x, y + 10), color="annot", w=2.0)
        s += text(x, y - 18, lab, color="annot" if v < 0.5 else
                  ("black" if v == 0.5 else "accenttwo"), anchor="north")
    s += dot(xd, y, "annot")
    s += text(155, y + 26, "anti-small-world", color="annot", anchor="south")
    s += text(400, y + 26, "small-world", color="accenttwo", anchor="south")
    return s


def _logaxis(x0, x1, y, decades, boxes=None):
    """One tick convention, not three.  This axis used to print 1, 10, then $10^2$ --
    two notations on five ticks of the same scale, which asks the room to convert.

    `boxes`, when given, collects each tick label's measured box so a caller placing
    anything else in that band can be checked against them rather than against a guess.
    """
    s = seg((x0, y), (x1, y), color="annot", w=2.2)
    for k in range(decades + 1):
        x = x0 + k / decades * (x1 - x0)
        s += seg((x, y - 9), (x, y + 9), color="annot", w=2.0)
        lab = f"{10 ** k:,}"
        s += text(x, y - 14, lab, color="annot", anchor="north")
        if boxes is not None:
            boxes[f"tick {lab}"] = text_box(x, y - 14, lab, anchor="north")
    return s


def fig_ws1998_dots():
    """Slide 60 asks students to read both ratios off this axis.  The three path-length
    dots land 1.22 / 1.51 / 1.18 -- within 17px of each other on a log axis where a decade
    is 158px -- so every dot prints its own value."""
    x0, x1, dec = 330, 1050, 4
    def X(v):
        return x0 + math.log10(v) / dec * (x1 - x0)
    boxes = {}
    s = _logaxis(x0, x1, 96, dec, boxes)
    for r, (nm, lr, cr, _) in enumerate(WS98_R):
        # 160, not 168: the two axis tags moved from above the axis to below the tick
        # labels, which costs 33bp at the bottom of a figure with 13bp of slack.  Moving
        # each dot's value from above its dot to below it hands back 37bp at the top,
        # because the top row's values were the highest ink in the drawing.
        y = 160 + (2 - r) * 70     # 70, not 78: `fig tight` caps the image at 320px
        # a hairline, and dotted: the connector only ties the row's two dots together,
        # and drawn at edge weight it read as a measured quantity of its own
        s += seg((X(lr), y), (X(cr), y), color="annot", w=1.2,
                 dash="dash pattern=on 3bp off 6bp")
        s += text(300, y, nm, color="black", anchor="east")
        boxes[nm] = text_box(300, y, nm, anchor="east")
        for v, col in ((lr, "annot"), (cr, "accenttwo")):
            lab = f"{v:.0f}" if v >= 10 else (f"{v:.1f}" if v >= 2 else f"{v:.2f}")
            s += dot(round(X(v), 1), y, col)
            s += text(round(X(v), 1), y - 20, lab, color=col, anchor="north")
            boxes[f"{nm} {lab}"] = text_box(X(v), y - 20, lab, anchor="north")
    # Below the axis line, under its tick labels -- not in the band between the axis and
    # the bottom row, where "path length" sat directly under "C. elegans" and read as a
    # fourth network name.  These two tag the two DOT COLUMNS, so they belong to the axis
    # and not to the rows.
    # y = 40, not 46: at 46 the tags cleared the tick labels by 4bp, and the gate below
    # measured it.  They are a separate row from the ticks and have to look like one.
    for x, lab, col, anc in ((345, "path length", "annot", "north west"),
                             (1050, "clustering", "accenttwo", "north east")):
        s += text(x, 40, lab, color=col, anchor=anc)
        boxes[lab] = text_box(x, 40, lab, anchor=anc)
    assert_boxes_clear("ws1998-dots", boxes, pad=6)
    return s


def fig_ws1998_sigma():
    """x1 = 940, not 1050: at the old width the film-actors label ran off the right of
    the canvas, and ink drawn outside the page does not exist -- it is simply cut."""
    x0, x1, dec = 330, 940, 4
    def X(v):
        return x0 + math.log10(v) / dec * (x1 - x0)
    s = _logaxis(x0, x1, 60, dec)
    # annotation gray, not accent-2: the dots ARE the reading and they are accent-2, so
    # a baseline in the same colour claimed to be one of them
    s += seg((x0, 60), (x0, 248), color="annot", w=3.0,
             dash="dash pattern=on 10bp off 7bp")
    s += text(x0 + 12, 238, "$\\sigma = 1$", color="annot", anchor="south west")
    for r, (nm, _, _, sg) in enumerate(WS98_R):
        y = 128 + (2 - r) * 50     # 50, not 75: `fig tight` caps the image at 320px
        s += text(300, y, nm, color="black", anchor="east")
        s += dot(round(X(sg), 1), y, "accenttwo")
        s += text(X(sg) + 26, y, f"$\\sigma \\approx {sg:.0f}$" if sg < 100
                  else "$\\sigma \\approx 2400$", color="accenttwo", anchor="west")
    return s


# --------------------------------------------------------------------------- Part 5
# 16 nodes, not 20: at 40bp discs a 20-node ring needs a 358bp circle, which fills a
# column figure's whole height and leaves the deck scaling white margin either side.
# k=4 gives C = 3(k-2)/(4(k-1)) = 0.5 whatever n is, so nothing in the story changes.
# The layout is the 8-antiprism (see antiprism_pos): rx 195 so the drawing spans the
# column, ry 124 so the whole figure clears the 364bp canvas with its caption under it.
RING_N, RING_K = 16, 4
RING_RX, RING_RY, RING_INNER = 195, 124, 0.62
RING_C = (260, 200)
RING_POS = antiprism_pos(RING_N, RING_C[0], RING_C[1], RING_RX, RING_RY, RING_INNER)
RING_EDGES = sorted({(min(i, (i + d) % RING_N), max(i, (i + d) % RING_N))
                     for i in range(RING_N) for d in (1, 2)})
assert len(RING_EDGES) == RING_N * RING_K // 2 == 32
_R16 = nx.Graph(RING_EDGES)
RING_CBAR = Fraction(nx.average_clustering(_R16)).limit_denominator(100)
assert RING_CBAR == Fraction(1, 2)
RING_DIA = nx.diameter(_R16)
RING_L = apl(_R16)
assert RING_DIA == 4, RING_DIA


# The chord of a triangle must arc clear of the disc it passes, with white left over --
# at NODE/2 + 3 the gap was 3bp and every triangle in the lattice was a hairline.
RING_CLEAR = NODE / 2 + 16


def assert_triangles_open(name, pos, paths):
    """Every edge must leave a visible interior in the triangle it closes.

    On the antiprism layout the 16 triangles are drawn with straight edges and this gate
    measures the gap between an edge and the disc it passes; it is what stops the inner
    ellipse creeping out toward the outer one until the triangles collapse into slivers.
    """
    worst = None
    for a, b, pts in paths:
        for k, q in pos.items():
            if k in (a, b):
                continue
            d = float(np.linalg.norm(pts - np.array(q, float), axis=1).min()) - NODE / 2
            if worst is None or d < worst[0]:
                worst = (d, a, b, k)
    assert worst and worst[0] >= 12, (
        f"{name}: edge {worst[1]}-{worst[2]} runs {worst[0]:.1f}bp from node {worst[3]}'s "
        f"disc -- under 12bp the triangle it closes has no visible interior")


def _lattice_edges(pos=RING_POS, edges=RING_EDGES, hot=(), name="ring lattice"):
    """The lattice itself, drawn straight, and gated three ways.

    Straight is the point: on the antiprism layout no lattice edge needs a bow to clear
    a disc, so there is nothing to bow and nothing to cross.  The three gates are the
    guarantee -- planar drawing, disc clearance, and a visible triangle interior.
    """
    s = ""
    for a, b in edges:
        h = (a, b) in hot or (b, a) in hot
        s += seg(pos[a], pos[b], color="accenttwo" if h else "black",
                 w=HEAVY_W if h else EDGE_W)
    paths = _edge_paths(edges, pos)
    assert_drawn_planar(name, edges, pos)
    assert not clearance_ok(edges, pos, r=NODE / 2 + 10), \
        clearance_ok(edges, pos, r=NODE / 2 + 10)
    assert_triangles_open(name, pos, paths)
    return s


def _ring(hot=(), pos=RING_POS, edges=RING_EDGES, ringed=(), cen=RING_C, dashed=(),
          check=True):
    s = _lattice_edges(pos, edges, hot)
    for a, b in dashed:
        s += curve_edge(a, b, pos, color="annot", w=2.2,
                        dash="dash pattern=on 8bp off 7bp", centroid=cen,
                        clear=RING_CLEAR)
    for i2 in pos:
        s += disc(pos[i2][0], pos[i2][1], "", fill="accent")
    for i2 in ringed:
        s += ring(pos[i2][0], pos[i2][1], color="accentthree", w=4.0)
    return s


def fig_ring_lattice():
    """The label carries the number the slide is FOR, not a restatement of its body.

    It read "joined to its 4 nearest neighbours", which is word for word what the body
    beside it says -- so the figure spent its one line of type saying nothing the reader
    had not just read.  The clustering coefficient is the thing this lattice is on the
    slide to have, and it is what slides 83 and 84 divide with.
    """
    s = _ring()
    # "half the pairs": each node has 4 neighbours, so 6 pairs, of which the 3 that sit
    # within 2 steps of each other are joined -- which is where the 0.50 comes from and
    # why it does not depend on n.  Asserted rather than asserted-in-prose:
    assert RING_CBAR == Fraction(1, 2) and math.comb(RING_K, 2) == 6
    s += text(260, 8, f"$\\bar C = {float(RING_CBAR):.2f}$: half the pairs closed",
              color="black", anchor="south")
    return s


RING_FAR = nx.shortest_path(_R16, 0, RING_N // 2)
assert len(RING_FAR) - 1 == RING_DIA


RING_DIST_NOTE = "the longest shortest route"


def fig_ring_distance():
    """The figure names the route and does NOT count it.

    It printed "4 hops to cross a ring of 16 nodes", and the slide's first build fragment
    reads "16 nodes: 4 hops to the far side" -- so the reveal arrived statically, beside
    the question, before the click.  That fragment has to stay: it is the first step of a
    16 -> 1000 -> "grows linearly with n" build, and cutting it would trade this Minor for
    a Major.  So the count leaves the drawing, which still traces the route the count is
    of.
    """
    hot = {(min(a, b), max(a, b)) for a, b in zip(RING_FAR, RING_FAR[1:])}
    s = _ring(hot=hot)
    assert not any(ch.isdigit() for ch in RING_DIST_NOTE), (
        f"{RING_DIST_NOTE!r} prints a number -- the deck's build reveals this count one "
        f"fragment later, and a figure that states it first has answered its own slide")
    s += text(260, 8, RING_DIST_NOTE, color="accenttwo", anchor="south")
    return s


# A TYPICAL draw, not a flattering one.  G(16,32) has p = 32/120 = 0.267, so E[C_i] = 0.267
# and a draw carries about ten triangles; over 3000 samples not one came out triangle-free.
# Both the old seed 2 (three triangles, C = 0.054) and the triangle-free seed that briefly
# replaced it sit at the 0th percentile.  Putting either on a slide labelled "a random
# graph" would teach something false about the model, and would contradict the
# C_rand = <k>/(n-1) the deck derives two parts earlier -- which predicts 0.267 at this
# size.  Seed 275 sits at the median; the figures print the number it actually has.
RND16 = nx.gnm_random_graph(RING_N, len(RING_EDGES), seed=275)
assert nx.is_connected(RND16)
RND16_TRI = sum(nx.triangles(RND16).values()) // 3
RND16_C = nx.average_clustering(RND16)
RND16_L = nx.average_shortest_path_length(RND16)
assert RND16_TRI > 0 and 0.15 < RND16_C < 0.40, (RND16_TRI, RND16_C)
assert RND16_L < float(RING_L), (RND16_L, float(RING_L))


def fig_random_graph():
    """"this draw", not "shuffled at random": two lines below this figure the deck names
    the formula $C_{\\mathrm{rand}} = \\langle k \\rangle/(n-1)$, which predicts 0.27 at
    this size, so a caption reading "at random: 0.24" reads as the formula's answer
    rather than as what one draw happened to give."""
    s = ""
    for a, b in RND16.edges():
        s += curve_edge(a, b, RING_POS, centroid=RING_C, w=2.2)
    for i2 in RING_POS:
        s += disc(RING_POS[i2][0], RING_POS[i2][1], "", fill="accent")
    s += text(260, 8, f"this draw: $\\bar C = {RND16_C:.2f}$",
              color="black", anchor="south")
    return s


# Both panels carry the same ring as the single-panel figures do -- same 1.45:1 aspect,
# same node discs -- so the eye compares edges and not shapes.  They cannot also match on
# SIZE: the slide is a `fig tight`, whose 320px cap leaves 250px for two rings and their
# labels where a column figure gives one ring 380px, so the ring here is 85% of the one
# on slides 65-67.  Aspect and disc size were the mismatches that read as encoding.
LVR_RX, LVR_RY = 181, 115
LVR_L, LVR_R = (260, 180), (840, 180)


def fig_lattice_vs_random():
    lp = antiprism_pos(RING_N, *LVR_L, LVR_RX, LVR_RY, RING_INNER)
    rp = antiprism_pos(RING_N, *LVR_R, LVR_RX, LVR_RY, RING_INNER)
    s = _lattice_edges(lp, name="lattice-vs-random (left panel)")
    for a, b in RND16.edges():
        s += curve_edge(a, b, rp, centroid=LVR_R, w=2.2)
    for p2 in (lp, rp):
        for i2 in p2:
            s += disc(p2[i2][0], p2[i2][1], "", fill="accent")
    s += text(LVR_L[0], 42, f"lattice: long routes, $\\bar C = {float(RING_CBAR):.2f}$",
              color="black", anchor="north")
    s += text(LVR_R[0], 42, f"random: short routes, $\\bar C = {RND16_C:.2f}$",
              color="black", anchor="north")
    return s


REWIRE_OLD, REWIRE_NEW = (0, 2), (0, 9)
assert REWIRE_OLD in RING_EDGES and REWIRE_NEW not in RING_EDGES


def fig_ws_rewire_step():
    """Each annotation is drawn in the colour of the thing it names, next to that thing.
    The red sentence used to name the gray edge and the gray figcaption the red one."""
    s = _lattice_edges(edges=[e for e in RING_EDGES if e != REWIRE_OLD],
                       name="ws-rewire-step")
    s += curve_edge(*REWIRE_OLD, RING_POS, color="annot", w=2.2,
                    dash="dash pattern=on 8bp off 7bp", centroid=RING_C,
                    clear=RING_CLEAR)
    s += curve_edge(*REWIRE_NEW, RING_POS, color="accenttwo", w=HEAVY_W, centroid=RING_C)
    for i2 in RING_POS:
        s += disc(RING_POS[i2][0], RING_POS[i2][1], "", fill="accent")
    s += text(254, 8, "red: the new end", color="accenttwo", anchor="south east")
    s += text(266, 8, "gray: the old one", color="annot", anchor="south west")
    return s


def _sweep_data():
    """C(p)/C(0) and L(p)/L(0) for the Watts-Strogatz sweep -- measured, not remembered.

    The low-p end expects 0.16 / 0.34 / 0.74 / 1.6 / 3.4 / 7.4 rewirings out of 1600 edges,
    so at 6 runs the sampling noise ran L/L(0) 0.964 -> 0.928 -> 0.960 and the curve read
    as "L rises with p".  Everything below p = 0.01 gets 24 runs."""
    import json
    cfg = dict(n=400, k=8, runs=6, quiet_runs=24, quiet=6,
               ps=[round(10 ** (-4 + 4 * i / 24), 6) for i in range(25)])
    cache = OUT / "_sweep.json"
    if cache.exists():
        d = json.loads(cache.read_text())
        if d.get("cfg") == cfg:
            return d
    rng = random.Random(20260805)
    out = {"cfg": cfg, "p": cfg["ps"], "C": [], "L": []}
    for i, p in enumerate(cfg["ps"]):
        cs, ls = [], []
        for _ in range(cfg["quiet_runs"] if i < cfg["quiet"] else cfg["runs"]):
            adj = _ws_adj(cfg["n"], cfg["k"], p, rng)
            cs.append(_avg_clustering(adj))
            ls.append(_apl_adj(adj))
        out["C"].append(sum(cs) / len(cs))
        out["L"].append(sum(ls) / len(ls))
    base = _ws_adj(cfg["n"], cfg["k"], 0.0, rng)
    out["C0"], out["L0"] = _avg_clustering(base), _apl_adj(base)
    cache.write_text(json.dumps(out))
    return out


def _ws_adj(n, k, p, rng):
    adj = [set() for _ in range(n)]
    edges = [(i, (i + j) % n) for i in range(n) for j in range(1, k // 2 + 1)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    for idx, (a, b) in enumerate(edges):
        if rng.random() < p:
            for _ in range(60):
                c = rng.randrange(n)
                if c != a and c not in adj[a]:
                    adj[a].discard(b)
                    adj[b].discard(a)
                    adj[a].add(c)
                    adj[c].add(a)
                    edges[idx] = (a, c)
                    break
    return [sorted(s) for s in adj]


def _apl_adj(adj):
    n = len(adj)
    tot = cnt = 0
    for s in range(n):
        d = [-1] * n
        d[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if d[v] < 0:
                    d[v] = d[u] + 1
                    q.append(v)
        for t2 in range(s + 1, n):
            if d[t2] > 0:
                tot += d[t2]
                cnt += 1
    return tot / cnt


def _avg_clustering(adj):
    n = len(adj)
    tot = 0.0
    nb_sets = [set(a) for a in adj]
    for i in range(n):
        nb = adj[i]
        k = len(nb)
        if k < 2:
            continue
        links = sum(1 for a in range(k) for b in range(a + 1, k) if nb[b] in nb_sets[nb[a]])
        tot += 2 * links / (k * (k - 1))
    return tot / n


SWEEP = _sweep_data()
assert abs(SWEEP["C0"] - 0.6428571) < 1e-4, SWEEP["C0"]
assert abs(SWEEP["L0"] - 25.4386) < 1e-3, SWEEP["L0"]


# The band is DERIVED from the measured sweep, under a criterion written down here and
# printed on the slide -- it is not two constants with an assertion that they are as far
# apart as they are.
#
# It used to be exactly that. The slide claimed "two orders of magnitude", the drawn band
# was 1.39 decades, and the fix taken in round 2 was to widen the band to p=0.001 so the
# sentence came true -- which put the band's left edge in a regime where this deck's own
# data says routes are only 22% shorter (L/L0 = 0.781 there). That is choosing the
# evidence, one level up from choosing a flattering random seed, and the assertion
# guarding it -- log10(BAND_HI/BAND_LO) >= 2 -- could only ever compare the rectangle
# with itself.
#
# Criterion: clustering still at least four fifths of the lattice's, paths at most half.
BAND_C_MIN, BAND_L_MAX = 0.80, 0.50
BAND_RULE = "paths at most half the lattice's, clustering still four fifths of it"
# Printed ON the figure, so the rectangle is never a shaded region the slide does not
# define.  Set as maths rather than as BAND_RULE's prose because 66 characters at 37pt
# measures wider than the whole 1100bp canvas -- the deck's figcaption carries the words.
BAND_NOTE = (f"both at once: $C \\geq {BAND_C_MIN:.1f}\\,C(0)$, "
             f"$L \\leq {BAND_L_MAX:.1f}\\,L(0)$")


def _band_edge(key, target):
    """Where the DRAWN curve crosses `target`, by the same linear interpolation the
    drawing itself does between samples.

    The edges are solved for, not chosen from the 13 sampled p values.  Snapping to
    samples looks more conservative and is really an artefact of where the samples fall:
    it puts the rectangle's left edge at p = 0.01 while the L curve *as drawn* has been
    under 0.5 since p = 0.0048, so the picture contradicts its own band, and the number
    moves if anyone edits `cfg["ps"]`.  Interpolating gives the band a reader with a
    ruler actually measures off the figure, which is the only band the figure can defend.
    """
    v = [x / SWEEP[key + "0"] for x in SWEEP[key]]
    lg = [math.log10(p) for p in SWEEP["p"]]
    cross = [i for i in range(len(v) - 1) if (v[i] >= target) != (v[i + 1] >= target)]
    assert len(cross) == 1, (
        f"{key}/{key}(0) crosses {target} {len(cross)} times -- the band's edge is only "
        f"well defined while the curve is monotone; re-run the sweep with more runs")
    i = cross[0]
    t = (target - v[i]) / (v[i + 1] - v[i])
    return 10 ** (lg[i] + t * (lg[i + 1] - lg[i]))


BAND_LO = _band_edge("L", BAND_L_MAX)      # routes have fallen to half the lattice's
BAND_HI = _band_edge("C", BAND_C_MIN)      # clustering has not yet fallen below four fifths
BAND_DECADES = math.log10(BAND_HI / BAND_LO)
assert BAND_LO < BAND_HI, (BAND_LO, BAND_HI)

# Assert the rectangle against the data it summarises, never against itself.  Two checks,
# and neither can pass by construction now that the edges are solved rather than selected:
#
#   1. every SAMPLED p inside the band meets the criterion and every one outside fails it.
#      This is what catches a non-contiguous qualifying set -- an edge solved from one
#      crossing would silently span a gap.
#   2. the band contains every sampled p that qualifies.  The rectangle may not be
#      narrower than the measured evidence either; understating is a defect too, it is
#      just a quieter one than the two-decade claim this replaced.
_QUALIFY = [p for p, c, l in zip(SWEEP["p"], SWEEP["C"], SWEEP["L"])
            if c / SWEEP["C0"] >= BAND_C_MIN and l / SWEEP["L0"] <= BAND_L_MAX]
assert _QUALIFY, "no sampled p meets the band criterion -- the sweep or the criterion is wrong"
for _p, _c, _l in zip(SWEEP["p"], SWEEP["C"], SWEEP["L"]):
    _inside = BAND_LO <= _p <= BAND_HI
    _meets = _c / SWEEP["C0"] >= BAND_C_MIN and _l / SWEEP["L0"] <= BAND_L_MAX
    assert _inside == _meets, (
        f"p={_p} is {'inside' if _inside else 'outside'} the drawn band but "
        f"{'meets' if _meets else 'fails'} the criterion -- the band is not the data")
assert BAND_LO <= min(_QUALIFY) and max(_QUALIFY) <= BAND_HI, (
    f"the drawn band [{BAND_LO:.5f}, {BAND_HI:.5f}] does not cover every measured p that "
    f"meets the criterion ({min(_QUALIFY)}-{max(_QUALIFY)}) -- it understates its own data")
# A tripwire, not a threshold. `assert BAND_DECADES >= 1.0` used to stand here, and its
# bound was chosen AFTER the answer first came out at 1.18 -- so if a better sweep had put
# the honest band at 0.9 the build would have broken, and the cheapest way to make it pass
# would have been to move the criterion until the number was a decade again. An assertion
# cannot say "rewrite the sentence"; it can only fail. So pin it to the value the deck was
# actually written to and let it fire in EITHER direction.
DECK_BAND_DECADES = 1.24
assert abs(BAND_DECADES - DECK_BAND_DECADES) < 0.06, (
    f"the band moved to {BAND_DECADES:.2f} decades from the {DECK_BAND_DECADES:.2f} slide 76 "
    f"is written to. Update the slide's sentence AND this constant together -- do not "
    f"satisfy this by moving the band, the criterion or the sampling")

# The clause the deck pastes. The deck must never carry a digit the sampling cannot
# defend: three significant figures on an interpolated crossing is more precision than
# 0.17-decade sampling earns, so the deck gets a phrase and the number stays here.
DECK_CLAUSE = ("the band spans more than a decade in $p$" if BAND_DECADES >= 1.0
               else "the band spans about two thirds of a decade in $p$")

print(f"band: p {BAND_LO:.5f}-{BAND_HI:.5f}  {BAND_DECADES:.2f} decades  "
      f"(factor {BAND_HI / BAND_LO:.0f})  criterion C>={BAND_C_MIN} L<={BAND_L_MAX}")
print(f'  deck sentence: "{DECK_CLAUSE}"')


_SWEEP_LABELS, _SWEEP_CURVES = {}, []


def _sweep_frame(band=False):
    """Both curves are fractions of the lattice value, so the vertical axis has to be
    ticked and named -- two slides assert how far each curve has fallen."""
    x0, x1, y0, y1 = 200, 1050, 110, 280      # y1 280: `fig tight` caps the image at 320px
    def X(p):
        return x0 + (math.log10(p) + 4) / 4 * (x1 - x0)
    def Y(v):
        return y0 + v * (y1 - y0)
    s = ""
    if band:
        s += (f"\\fill[accentthree,opacity=0.30] ({X(BAND_LO)},{y0}) rectangle "
              f"({X(BAND_HI)},{y1 + 10});\n")
    s += seg((x0 - 20, y0), (x1 + 20, y0), color="annot", w=2.2)
    s += seg((x0, y0), (x0, y1 + 10), color="annot", w=2.2)
    # one convention across the five ticks: the axis used to run $10^{-4}$, $10^{-3}$,
    # 0.01, 0.1, 1, which asks the room to convert notations mid-axis
    for k in range(5):
        x = x0 + k / 4 * (x1 - x0)
        s += seg((x, y0 - 9), (x, y0 + 9), color="annot", w=2.0)
        s += text(x, y0 - 12, ["0.0001", "0.001", "0.01", "0.1", "1"][k],
                  color="annot", anchor="north")
    s += text(625, y0 - 52, "rewiring probability $p$", color="annot", anchor="north")
    for v, lab in ((0.0, "0"), (0.5, "0.5"), (1.0, "1")):
        s += seg((x0 - 9, Y(v)), (x0 + 9, Y(v)), color="annot", w=2.0)
        s += text(x0 - 16, Y(v), lab, color="annot", anchor="east")
    # rotated onto the axis it labels, not stacked above the plot: the band annotation
    # needs that row, and a y-axis title belongs beside its own ticks anyway
    s += text(90, (y0 + y1) / 2, "fraction of the\\\\lattice value", color="annot",
              rotate=90)
    # ly 0.71 for C, not 0.84: at 0.84 the label box ran from y 234 to 271 and the C curve
    # it names descends through 260 at the label's right-hand end, so the curve struck out
    # its own name.  0.71 puts the label in the wide gap BETWEEN the two curves, which is
    # where it belongs anyway -- and the assertion below is what found it.
    curves, boxes = [], {}
    for key, col, lab, ly, lx in (("C", "accenttwo", "$C(p)/C(0)$", 0.71, 360),
                                  ("L", "accent", "$L(p)/L(0)$", 0.30, 30)):
        base = SWEEP[key + "0"]
        pts = [(X(p), Y(v / base)) for p, v in zip(SWEEP["p"], SWEEP[key])]
        curves.append((key, key, np.array(pts, float)))
        s += "\\draw[line width=3.4bp,draw=%s] %s;\n" % (
            col, " -- ".join("(%.1f,%.1f)" % q for q in pts))
        s += text(x0 + lx, Y(ly), lab, color=col, anchor="west")
        boxes[lab] = text_box(x0 + lx, Y(ly), lab, anchor="west")
    # A curve label is placed by hand against a curve whose shape comes from measured
    # data, so the two drift apart whenever the sweep is re-run.  Check the drawn
    # polylines, not the intent.
    assert_labels_clear("ws-sweep", boxes, curves, pad=8)
    assert_boxes_clear("ws-sweep", boxes)
    _SWEEP_LABELS.clear()
    _SWEEP_LABELS.update(boxes)
    _SWEEP_CURVES[:] = curves
    return s


def fig_ws_sweep():
    return _sweep_frame()


def fig_ws_band():
    """The annotation names the gold band, so it sits over the gold band and is drawn in
    annotation gray.  It was accent-2 -- which already labels the C curve in this same
    figure -- and it sat entirely to the right of the band it was naming.

    It now carries the criterion as well.  A shaded region with no stated rule is an
    assertion the reader cannot check, and the rule is the whole of what round 2 got
    wrong: the band was widened to make a sentence true, so the sentence and the shading
    now both come from BAND_C_MIN / BAND_L_MAX and neither can move without the other.
    """
    s = _sweep_frame(band=True)
    mid = (BAND_LO * BAND_HI) ** 0.5           # the band's midpoint on a log axis
    x = 200 + (math.log10(mid) + 4) / 4 * 850
    # The label follows the derived band; it is no longer pinned to a hardcoded x.
    lo_x = 200 + (math.log10(BAND_LO) + 4) / 4 * 850
    hi_x = 200 + (math.log10(BAND_HI) + 4) / 4 * 850
    assert lo_x < x < hi_x, (lo_x, x, hi_x)
    s += text(round(x, 1), 296, BAND_NOTE, color="annot", anchor="south")
    # The note is four times the band's own width, so it has to be the only thing in its
    # row -- and the two curve labels sit one row below it, placed by a different line of
    # code against data that moves.  Both boxes come from `_sweep_frame`, so there is no
    # second copy of their coordinates to fall out of step.
    note = text_box(x, 296, BAND_NOTE, anchor="south")
    assert_boxes_clear("ws-band", {BAND_NOTE: note, **_SWEEP_LABELS})
    assert_labels_clear("ws-band", {BAND_NOTE: note}, _SWEEP_CURVES, pad=8)
    return s


def fig_ws_widget():
    rng = random.Random(3)
    adj = _ws_adj(RING_N, RING_K, 0.14, rng)
    edges = sorted({(min(i, j), max(i, j)) for i, a in enumerate(adj) for j in a})
    lattice = set(RING_EDGES)
    # the surviving lattice straight, the rewired ends bowed clear of whatever they pass
    s = _lattice_edges(edges=[e for e in edges if e in lattice], name="ws-widget")
    for a, b in edges:
        if (a, b) in lattice:
            continue
        s += curve_edge(a, b, RING_POS, color="accenttwo", w=HEAVY_W, centroid=RING_C,
                        clear=NODE / 2 + 3)
    for i2 in RING_POS:
        s += disc(RING_POS[i2][0], RING_POS[i2][1], "", fill="accent")
    s += text(260, 8, "drag $p$: the red shortcuts appear",
              color="accenttwo", anchor="south")
    return s


SHORTCUT_EDGE = (0, RING_N // 2)
_RS = nx.Graph(RING_EDGES)
_RS.add_edge(*SHORTCUT_EDGE)
SHORTENED = [v for v in range(RING_N)
             if nx.shortest_path_length(_RS, 0, v) < nx.shortest_path_length(_R16, 0, v)]
assert len(SHORTENED) >= 3, SHORTENED
assert nx.average_clustering(_RS) > 0.42, nx.average_clustering(_RS)


def fig_shortcut_effect():
    """Node 0 is what the gold rings are measured *from*, so it is named and ringed too --
    unnamed, the rings encoded 'closer to' with no second term."""
    s = _lattice_edges(name="shortcut-effect")
    s += curve_edge(*SHORTCUT_EDGE, RING_POS, color="accenttwo", w=HEAVY_W,
                    centroid=RING_C)
    for i2 in RING_POS:
        s += disc(RING_POS[i2][0], RING_POS[i2][1], "0" if i2 == 0 else "", fill="accent")
    for v in [0] + SHORTENED:
        s += ring(RING_POS[v][0], RING_POS[v][1], color="accentthree", w=4.0)
    # annotation gray: the legend describes the GOLD rings, and accent-2 is already the
    # shortcut chord in this same drawing.  Not accent-3 either -- gold type is 2.0:1
    # against white where the floor is 3:1.
    s += text(260, 8, f"gold: node 0 and the {len(SHORTENED)} now closer",
              color="annot", anchor="south")
    return s


# --------------------------------------------------------------------------- Part 6
DISC_POS = {0: (80, 260), 1: (200, 320), 2: (200, 190), 3: (85, 120),
            4: (360, 250), 5: (470, 300), 6: (470, 180)}
DISC_EDGES = [(0, 1), (1, 2), (0, 2), (0, 3), (2, 3), (4, 5), (5, 6), (4, 6)]


def _twocomp(answer=False):
    s = ""
    for a, b in DISC_EDGES:
        s += seg(DISC_POS[a], DISC_POS[b], color="black", w=EDGE_W)
    for i2, q in DISC_POS.items():
        s += disc(q[0], q[1], "", fill="accenttwo" if i2 in (3, 6) else "accent")
    s += ring(*DISC_POS[3])
    s += ring(*DISC_POS[6])
    return s


def fig_disconnected():
    s = _twocomp()
    s += text(260, 40, "distance between the red nodes?", color="black",
              anchor="north")
    return s


def fig_disconnected_answer():
    """No connector.  The figure drew a line between the one pair it says has no route
    between them, which is the only claim on the slide; the gap carries it."""
    s = _twocomp()
    s += text(260, 40, "$d = \\infty$: no route at all", color="accenttwo",
              anchor="north")
    return s


D1_POS = {0: (110, 250), 1: (280, 320), 2: (280, 180), 3: (450, 250), 4: (110, 90)}
D1_EDGES = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (0, 4)]


def _degree_one(answer=False):
    s = ""
    for a, b in D1_EDGES:
        s += seg(D1_POS[a], D1_POS[b], color="black", w=EDGE_W)
    for i2, q in D1_POS.items():
        s += disc(q[0], q[1], "", fill="accenttwo" if i2 == 4 else "accent")
    s += ring(*D1_POS[4])
    return s


def fig_degree_one():
    s = _degree_one()
    s += text(260, 40, "one friend --- so no pairs at all",
              color="black", anchor="north")
    return s


def fig_degree_one_answer():
    s = _degree_one()
    s += text(260, 40, "$k(k-1)/2 = 0$: nothing to divide", color="accenttwo",
              anchor="north")
    return s


def fig_sigma_lt_1_q():
    # "high clustering" was half the answer, printed on the question slide.
    s = _ring()
    s += text(260, 8, "a ring lattice: long routes", color="black", anchor="south")
    return s


# The answer slide used to show the question slide's file unchanged -- the same ring
# under an in-figure line reading "joined to its 4 nearest neighbours", written for a
# slide eighteen earlier.  Its own arithmetic, computed from the two baselines the deck
# derives in Part Four, is the thing that settles the question.
SIGMA_LT_1 = {
    "C": float(RING_CBAR),
    "C_rand": Fraction(RING_K, RING_N - 1),          # <k>/(n-1), slide 55
    "L": float(RING_L),
    "L_rand": math.log(RING_N) / math.log(RING_K),   # ln n / ln <k>, slide 58
}
SIGMA_LT_1["sigma"] = ((SIGMA_LT_1["C"] / float(SIGMA_LT_1["C_rand"]))
                       / (SIGMA_LT_1["L"] / SIGMA_LT_1["L_rand"]))
assert abs(SIGMA_LT_1["sigma"] - 1.5625) < 1e-9, SIGMA_LT_1
assert abs(SIGMA_LT_1["L_rand"] - 2.0) < 1e-12, SIGMA_LT_1


def fig_sigma_lt_1_answer():
    """The one slide whose job is the arithmetic that settles the question, so the
    printed numbers have to divide to the printed answer.

    C_rand was shown at two decimals: the figure read "C 0.50/0.27, L 2.4/2.0,
    sigma = 1.56" and (0.50/0.27)/(2.4/2.0) is 1.543, not 1.56 -- sigma was right,
    computed from the exact 4/15, and the display rounded the one number that could not
    take it.  A student who does the division must land on the answer beside it, so the
    check below is done on the STRINGS the figure prints, not on the floats behind them.
    """
    d = SIGMA_LT_1
    # 0.267, not 0.27: three decimals is what makes the division reconcile.
    c, c_rand = f"{d['C']:.2f}", f"{float(d['C_rand']):.3f}"
    l, l_rand, sig = f"{d['L']:.1f}", f"{d['L_rand']:.1f}", f"{d['sigma']:.2f}"
    shown = (float(c) / float(c_rand)) / (float(l) / float(l_rand))
    assert f"{shown:.2f}" == sig, (
        f"the printed numbers do not divide to the printed sigma: "
        f"({c}/{c_rand})/({l}/{l_rand}) = {shown:.4f}, printed {sig} -- print another "
        f"decimal of whichever number is being rounded away, never round sigma to match")
    s = _ring()
    # both ratios as ratios, which is what sigma is -- and 482bp, which fits the column
    # where the "0.50 vs 0.27" phrasing measured 605
    s += text(260, 8, f"$C$ {c}/{c_rand}, $L$ {l}/{l_rand}, $\\sigma = {sig}$",
              color="accenttwo", anchor="south")
    return s


GRID_POS = {(c, r): (60 + c * 100, 78 + r * 82) for c in range(5) for r in range(4)}
GRID_EDGES = [((c, r), (c + 1, r)) for c in range(4) for r in range(4)] + \
             [((c, r), (c, r + 1)) for c in range(5) for r in range(3)]
_G54 = nx.Graph(GRID_EDGES)
assert nx.transitivity(_G54) == 0


GRID_HUB = (2, 1)                      # an INTERIOR intersection: degree 4
assert sum(1 for e in GRID_EDGES if GRID_HUB in e) == 4, "the ringed node must have 4 neighbours"
GRID_HUB_TRIPLETS = math.comb(4, 2)
assert GRID_HUB_TRIPLETS == 6


GRID_NBRS = sorted({b if a == GRID_HUB else a
                    for a, b in GRID_EDGES if GRID_HUB in (a, b)})
GRID_CLOSURES = list(itertools.combinations(GRID_NBRS, 2))
assert len(GRID_CLOSURES) == GRID_HUB_TRIPLETS == 6
# None of the six closing edges exists -- which is the whole claim, so it is asserted
# rather than drawn and hoped for.
assert not any(nx.Graph(GRID_EDGES).has_edge(*e) for e in GRID_CLOSURES)


def _grid(ring_hub=False, triplets=False):
    """`triplets` draws the six third-edges that WOULD close the ringed node's triplets.

    The answer half used to highlight the node's four spokes and assert "6 triplets" in
    the caption, which leaves the 4 -> C(4,2) = 6 step happening entirely in prose: a
    student counts four red edges and is told six.  The six dashed grays are that step
    made visible, and they are the same device slide 37 uses for the same idea --
    possibilities, not edges -- so "none closed" becomes something the room can check
    rather than something it is told.
    """
    s = ""
    for a, b in GRID_EDGES:
        hot = triplets and GRID_HUB in (a, b)
        s += seg(GRID_POS[a], GRID_POS[b], color="accenttwo" if hot else "black",
                 w=HEAVY_W if hot else EDGE_W)
    if triplets:
        # Two of the six run straight through the ringed disc (the north-south and
        # east-west pairs are collinear through it), so every closure is bowed by the
        # solver rather than drawn as a chord.  RING_CLEAR keeps them outside the gold
        # ring as well as outside the disc.
        for a, b in GRID_CLOSURES:
            s += curve_edge(a, b, GRID_POS, color="annot", w=2.0,
                            dash="dash pattern=on 8bp off 7bp", clear=NODE / 2 + 18)
    for q in GRID_POS.values():
        s += disc(q[0], q[1], "", fill="accent")
    if ring_hub:
        s += ring(*GRID_POS[GRID_HUB], color="accentthree", w=4.0)
    return s


def fig_grid_q():
    """The QUESTION half. One file per slide: the answer used to be burned into the single
    shared figure, printed beside the question it was asking, which killed the only
    in-class activity in Part Six.

    The ringed node is interior on purpose -- 14 of the 20 intersections have degree 2 or
    3, so a student who picks a corner counts one triplet instead of six and concludes
    they are wrong."""
    s = _grid(ring_hub=True)
    s += text(260, 8, "how many of its triplets close?", color="black",
              anchor="south")
    return s


def fig_grid_answer():
    s = _grid(ring_hub=True, triplets=True)
    s += text(260, 8, f"{GRID_HUB_TRIPLETS} triplets, none closed: $C = 0$",
              color="accenttwo", anchor="south")
    return s


# ry 84 and cy 178, not 100 and 190: the slide is a `fig tight` and the theme's 320px cap
# bound the scale at the old spread
GNM_POS = ellipse_pos(6, 250, 178, 190, 84, start=0)
GNP_POS = ellipse_pos(6, 840, 178, 190, 84, start=0)
# (1,3) forced a crossing on what is a 5-edge tree; (1,2) draws planar on the hexagon and
# the graph is the same shape of object.  Asserted below, not eyeballed.
GNM_EDGES = [(0, 1), (1, 2), (2, 4), (3, 4), (0, 5)]
assert nx.is_tree(nx.Graph(GNM_EDGES))
assert count_crossings([(a, b, np.array([GNM_POS[a], GNM_POS[b]], float))
                        for a, b in GNM_EDGES]) == 0, "G(n,m) panel draws a crossing"
assert not clearance_ok(GNM_EDGES, GNM_POS)


def _gnm_gnp(mark=False):
    s = ""
    for a, b in GNM_EDGES:
        s += seg(GNM_POS[a], GNM_POS[b], color="black", w=EDGE_W)
    for a, b in itertools.combinations(range(6), 2):
        if (a, b) in GNM_EDGES:
            s += seg(GNP_POS[a], GNP_POS[b], color="black", w=EDGE_W)
        else:
            s += seg(GNP_POS[a], GNP_POS[b], color="annot", w=1.8,
                     dash="dash pattern=on 6bp off 7bp")
    for p2 in (GNM_POS, GNP_POS):
        for i2 in p2:
            s += disc(p2[i2][0], p2[i2][1], "", fill="accent")
    s += text(250, 52, f"$G(n,m)$: deal exactly {len(GNM_EDGES)} edges", color="black",
              anchor="north")
    s += text(840, 52, "$G(n,p)$: one coin per pair", color="black", anchor="north")
    return s


def fig_gnm_gnp():
    s = _gnm_gnp()
    s += text(545, 280, "same graphs? same mathematics?", color="accenttwo",
              anchor="south")
    return s


def fig_gnm_gnp_answer():
    s = _gnm_gnp()
    s += text(250, 280, "edges are coupled", color="annot", anchor="south")
    s += text(840, 280, "edges are independent", color="accenttwo", anchor="south")
    return s


# --------------------------------------------------------------------------- wrap-up
def fig_universality():
    """The same three networks as `ws1998-sigma`, plus the one thing that figure does not
    carry: how far apart they are in size.

    This slide used to replace the network names with "social / technological /
    biological" and drop the sigma values, which made it the earlier figure with its
    information removed.  Keeping the names AND printing n = 225,226 / 4,941 / 282 is
    what turns "one signature" from an assertion into evidence: four orders of magnitude
    of size, one column of dots.
    """
    x0, x1, dec = 460, 1020, 4          # x0 = 460: the rows now carry a name AND a size
    def X(v):
        return x0 + math.log10(v) / dec * (x1 - x0)
    s = _logaxis(x0, x1, 90, dec)
    s += text(740, 36, "small-world index", color="annot", anchor="north")
    s += seg((x0, 90), (x0, 248), color="annot", w=3.0,
             dash="dash pattern=on 10bp off 7bp")
    # beside the line and BELOW the summary: at y = 300 it sat on the same baseline as
    # the accent-2 header and the two collided
    s += text(x0 + 12, 238, "$\\sigma = 1$", color="annot", anchor="south west")
    for r, (nm, _, _, sg) in enumerate(WS98_R):
        y = 128 + (2 - r) * 50
        # {,} and not a bare comma inside the math: a comma is punctuation there, so
        # $225,226$ typesets with a thin space after it
        n = f"{WS98_N[nm]:,}".replace(",", "{,}")
        s += text(430, y, f"{nm}, $n = {n}$", color="black", anchor="east")
        s += dot(round(X(sg), 1), y, "accenttwo")
    # 710: the line measures 723bp, so centring it on the plot ran it off the canvas
    s += text(710, 272, f"{WS98_ORDERS} orders of magnitude apart --- one signature",
              color="accenttwo", anchor="south")
    return s


def fig_sw_map():
    """Panel 3 is the same lattice rewired at p = 1, not a fresh random graph, so "red:
    the rewired edges" is true of it: at the far end of the p arrow every edge has moved,
    and the panel used to draw all 24 of them black."""
    cs = [(170, 210), (550, 210), (930, 210)]
    labs = ["lattice", "small world", "random"]
    # 10 nodes, not 12: the three panels share a `fig tight` slot capped at 320px, and at
    # p = 1 twelve nodes leave no bow that clears every disc -- the chords have to pass
    # through the discs, which is the m01 defect this file exists to prevent.
    n = 10
    lat = sorted({(min(i, (i + d) % n), max(i, (i + d) % n))
                  for i in range(n) for d in (1, 2)})
    mids = sorted({(min(i, j), max(i, j))
                   for i, a in enumerate(_ws_adj(n, 4, 0.12, random.Random(1))) for j in a})
    full = sorted({(min(i, j), max(i, j))
                   for i, a in enumerate(_ws_adj(n, 4, 1.0, random.Random(1))) for j in a})
    assert 2 <= sum((e not in lat) for e in mids) <= 4, "the middle panel needs a few"
    assert sum((e not in lat) for e in full) >= 14, "p = 1 must move most of the lattice"
    s, boxes = "", {}
    for k, (cx, cy) in enumerate(cs):
        # the same antiprism the 16-node lattice uses on slides 65-83: one object, one
        # drawing.  C_n(1,2) is the (n/2)-antiprism, so it is the same construction here.
        pos = antiprism_pos(n, cx, cy, 94, 94, 0.44)
        ed = (lat, mids, full)[k]
        s += _lattice_edges(pos, [e for e in ed if e in lat], name=f"sw-map panel {k}")
        for a, b in ed:
            if (a, b) in lat:
                continue
            s += curve_edge(a, b, pos, color="accenttwo", w=HEAVY_W, centroid=(cx, cy),
                            clear=NODE / 2 + 3)
        for i2 in pos:
            s += disc(pos[i2][0], pos[i2][1], "", fill="accent")
        # All three panel labels in ink.  The middle one was accent-2, which in this same
        # drawing already means "a rewired edge" -- so red said both "this edge moved" and
        # "look at this panel", and the middle panel is not the one with the most red.
        # Raised from y = 86 to 104: the rings' lowest ink is at y = 114, so the labels
        # were floating 28bp under nothing and 3bp above the annotation row.
        s += text(cx, 104, labs[k], color="black", anchor="north")
        boxes[labs[k]] = text_box(cx, 104, labs[k], anchor="north")

    # The axis label rides the arrow's own row -- this slide is a `fig tight`, and a
    # second annotation row under three rings overruns the 320px cap by 16bp.  So the
    # arrow is INTERRUPTED around the label rather than the label being parked to the
    # left of it: at x = 20 the label spanned 20-346 while the arrow it names ran
    # 360-1020, which put it under the lattice panel and read as that panel's caption.
    # A title sitting in a gap in its own axis cannot be read as anything else's.
    note = "rewiring probability $p$"
    nw, _ = ink_box_bp(note)
    ax0, ax1, ay = 200, 1040, 40
    xc = (ax0 + ax1) / 2
    gap = nw / 2 + 16
    s += text(xc, ay, note, color="annot", anchor="center")
    s += seg((ax0, ay), (xc - gap, ay), color="annot", w=2.4)
    s += seg((xc + gap, ay), (ax1, ay), color="annot", w=2.4,
             arrow="-{Stealth[length=11bp]}")
    boxes[note] = text_box(xc, ay, note, anchor="center")
    assert xc - gap - ax0 >= 120 and ax1 - xc - gap >= 120, (
        f"the label leaves {xc - gap - ax0:.0f}bp and {ax1 - xc - gap:.0f}bp of arrow -- "
        f"under 120bp either side the two stubs stop reading as one axis")
    assert_boxes_clear("sw-map", boxes)
    assert_labels_clear("sw-map", {note: boxes[note]},
                        [((ax0, ay), (xc - gap, ay)), ((xc + gap, ay), (ax1, ay))], pad=4)
    return s


RECAP_CHORDS = [(0, RING_N // 2), (4, 11)]
assert all(e not in RING_EDGES for e in RECAP_CHORDS)


def fig_recap():
    # two chords, because the caption on this slide says "a few shortcuts"
    s = _lattice_edges(name="recap")
    for a, b in RECAP_CHORDS:
        s += curve_edge(a, b, RING_POS, color="accenttwo", w=HEAVY_W, centroid=RING_C)
    for i2 in RING_POS:
        s += disc(RING_POS[i2][0], RING_POS[i2][1], "", fill="accent")
    s += text(260, 8, "triangles kept, routes short", color="accenttwo",
              anchor="south")
    return s


MARK_R = 16          # half-width of the X mark
# 8bp of white, not 3: at 3 the search was content to leave the right-hand X six points
# off the solid chord, which is 24px on the slide -- clear to an assertion and not to a
# reader.  The mark has to look unambiguously attached to one edge, not merely be so.
MARK_PAD = 8


def fig_m03_teaser():
    """The X goes on the edge it removes, and on nothing else.

    Two rounds of this.  First both X's landed where the chords crossed, so the render
    X-ed out the crossing rather than either edge.  The fix was to spread the chords and
    assert the two marks were 80bp apart -- which is a check on the marks against each
    OTHER, not against the drawing, and it passed while the right-hand X sat on the last
    26px of the solid chord the figure says survives.  Red-pixel counts inside the two
    mark boxes were 136 against 42, the difference being an edge that is not cut.

    So each mark now slides along its own chord until its box is clear of every other
    drawn path, and the assertion is that it touches exactly one -- its own.
    """
    # spread round the ring: the old three all ran close to the centre, so their midpoints
    # -- and therefore both X marks -- landed in the same 70bp of the drawing
    shortcuts = [(1, 6), (3, 13), (9, 14)]
    assert all(e not in RING_EDGES for e in shortcuts)
    chords, bodies = {}, {}
    for e in shortcuts:
        paths = []
        bodies[e] = curve_edge(*e, RING_POS, centroid=RING_C, paths=paths)
        chords[e] = _polyline(paths[0][2])
    mids = {e: q[len(q) // 2] for e, q in chords.items()}
    # which two get cut is arbitrary, so let the drawing choose: the pair whose marks are
    # furthest apart.  Picking the first two put both X's on the chords' crossing point.
    cut = max(itertools.combinations(shortcuts, 2),
              key=lambda pr: math.dist(mids[pr[0]], mids[pr[1]]))

    # Every other stroke on the page: the lattice, and the chords this mark does not mark.
    all_paths = _edge_paths(RING_EDGES, RING_POS) + [(a, b, chords[(a, b)])
                                                     for a, b in shortcuts]

    def place(e):
        """Slide the mark along its own chord, from the midpoint outward, until its box
        clears every path but this one -- and the discs, which are drawn under it."""
        q = chords[e]
        order = sorted(range(len(q)), key=lambda i: abs(i - len(q) // 2))
        for i in order:
            if not (0.22 * len(q) <= i <= 0.78 * len(q)):
                continue                       # too near an endpoint reads as a node marker
            mx, my = q[i]
            box = (mx - MARK_R, my - MARK_R, mx + MARK_R, my + MARK_R)
            if min(math.dist((mx, my), p) for p in RING_POS.values()) < NODE / 2 + MARK_R:
                continue
            if set(paths_hitting_box(box, all_paths, pad=MARK_PAD)) == {frozenset(e)}:
                return (mx, my), box
        raise AssertionError(
            f"no point on the chord {e} carries an X clear of every other drawn path -- "
            f"move the shortcut, do not plant the mark on top of an edge it does not cut")

    marks = {}
    for e in cut:
        (mx, my), box = place(e)
        marks[e] = (mx, my, box)
    sep = math.dist(marks[cut[0]][:2], marks[cut[1]][:2])
    assert sep >= 80, f"the two X marks are {sep:.0f}bp apart -- they will read as one"

    s = _lattice_edges(name="m03-teaser")
    for e in shortcuts:
        s += curve_edge(*e, RING_POS, color="accenttwo", w=HEAVY_W, centroid=RING_C,
                        dash="dash pattern=on 13bp off 10bp" if e in cut else "")
    for i2 in RING_POS:
        s += disc(RING_POS[i2][0], RING_POS[i2][1], "", fill="accent")
    for e in cut:                       # after the discs: a marker under a node is no marker
        mx, my, _ = marks[e]
        s += seg((mx - MARK_R, my - MARK_R), (mx + MARK_R, my + MARK_R), color="black", w=5.0)
        s += seg((mx - MARK_R, my + MARK_R), (mx + MARK_R, my - MARK_R), color="black", w=5.0)
    # The claim, asserted: each mark's box intersects the one chord it marks, and no other.
    assert_marks_own_edge("m03-teaser", {e: marks[e][2] for e in cut}, all_paths,
                          pad=MARK_PAD)
    s += text(260, 8, "cut two shortcuts --- then what?",
              color="accenttwo", anchor="south")
    return s



FIGURES = [
    ("milgram-map", fig_milgram_map, "col"),
    ("milgram-rule", fig_milgram_rule, "col"),
    ("milgram-arrivals", fig_milgram_arrivals, "full"),
    ("milgram-chain", fig_milgram_chain, "full"),
    ("six-degrees-timeline", fig_six_degrees_timeline, "col"),
    ("replication-yahoo", fig_replication_yahoo, "col"),
    ("replication-facebook", fig_replication_facebook, "col"),
    ("wikirace", fig_wikirace, "col"),
    ("routing-vs-existence", fig_routing_vs_existence, "full"),
    ("chain-graph", fig_chain_graph, "full"),
    ("distance-def", fig_distance_def, "col"),
    ("chain-blank", fig_chain_blank, "full"),
    ("distance-six", fig_distance_six, "full"),
    ("chain-chord", fig_chain_chord, "full"),
    ("two-routes", fig_two_routes, "col"),
    ("apl-chain", fig_apl_chain, "col"),
    ("chain-shortcut", fig_chain_shortcut, "full"),
    ("apl-shortcut", fig_apl_shortcut, "col"),
    ("diameter", fig_diameter, "full"),
    ("worksheet-a", fig_worksheet_a, "full"),
    ("worksheet-a-answer", fig_worksheet_a_answer, "full"),
    ("triangle-only", fig_triangle_only, "col"),
    ("triangle-triplet", fig_triangle_triplet, "col"),
    ("triplet-three-corners", fig_triplet_three_corners, "full"),
    ("ego-graph", fig_ego_graph, "col"),
    ("ego-pairs", fig_ego_pairs, "col"),
    ("ego-pairs-count", fig_ego_pairs_count, "col"),
    ("ego-clustering", fig_ego_clustering, "col"),
    ("a3-walks", fig_a3_walks, "col"),
    ("a3-formula", fig_a3_formula, "col"),
    ("cbar-milgram", fig_cbar_milgram, "full"),
    ("windmill", fig_windmill, "full"),
    ("windmill-cbar", fig_windmill_cbar, "full"),
    ("transitivity-def", fig_transitivity_def, "full"),
    ("windmill-split", fig_windmill_split, "full"),
    ("worksheet-b", fig_worksheet_b, "full"),
    ("worksheet-b-answer", fig_worksheet_b_answer, "full"),
    ("paradox", fig_paradox, "full"),
    ("complete-graph", fig_complete_graph, "col"),
    ("er-coin", fig_er_coin, "col"),
    ("er-degree", fig_er_degree, "col"),
    ("er-clustering", fig_er_clustering, "col"),
    ("fanout", fig_fanout, "full"),
    ("fanout-solve", fig_fanout_solve, "full"),
    ("free-vs-not", fig_free_vs_not, "col"),
    ("sigma-def", fig_sigma_def, "col"),
    ("ws1998-dots", fig_ws1998_dots, "full"),
    ("ws1998-sigma", fig_ws1998_sigma, "full"),
    ("ring-lattice", fig_ring_lattice, "col"),
    ("ring-distance", fig_ring_distance, "col"),
    ("random-graph", fig_random_graph, "col"),
    ("lattice-vs-random", fig_lattice_vs_random, "full"),
    ("ws-rewire-step", fig_ws_rewire_step, "col"),
    ("ws-sweep", fig_ws_sweep, "full"),
    ("ws-band", fig_ws_band, "full"),
    ("ws-widget", fig_ws_widget, "col"),
    ("shortcut-effect", fig_shortcut_effect, "col"),
    ("disconnected", fig_disconnected, "col"),
    ("disconnected-answer", fig_disconnected_answer, "col"),
    ("degree-one", fig_degree_one, "col"),
    ("degree-one-answer", fig_degree_one_answer, "col"),
    ("sigma-lt-1-q", fig_sigma_lt_1_q, "col"),
    ("sigma-lt-1-answer", fig_sigma_lt_1_answer, "col"),
    ("grid-q", fig_grid_q, "col"),
    ("grid-answer", fig_grid_answer, "col"),
    ("gnm-gnp", fig_gnm_gnp, "full"),
    ("gnm-gnp-answer", fig_gnm_gnp_answer, "full"),
    ("universality", fig_universality, "full"),
    ("sw-map", fig_sw_map, "full"),
    ("recap", fig_recap, "col"),
    ("m03-teaser", fig_m03_teaser, "col"),
]


def main():
    """Every failure, not the first.

    These gates fire in clusters -- raising the type size breaks a dozen figures at once --
    and stopping at figure 3 of 67 turns one round of fixes into a dozen rebuilds.
    """
    bad = []
    for name, fn, cont in FIGURES:
        try:
            emit(name, fn(), cont)
        except AssertionError as e:
            bad.append(name)
            print(f"  FAIL {name}: {e}")
    import json
    (OUT / "_generated.json").write_text(json.dumps(sorted(_built)))
    print(f"\n{len(_built)} figures written, {len(bad)} failed")
    if bad:
        print("  " + " ".join(bad))
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate every Module 02 slide figure.

Pipeline (see review/FIGURE_SPEC.md for the derivation):

    TikZ body  ->  pdflatex (page fixed to the design canvas)  ->  pdftoppm -r 288

Author at final size: **1 bp = 1 slide pixel**.  The page is pinned to the design
canvas, so the deck's own scale factor is a constant per container:

    cols column : 537 / 520  = 1.033 slide px per bp
    full width  : 1120 / 1100 = 1.018 slide px per bp

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
COL_W, FULL_W = 537, 1120    # containers, measured in a real browser render
MAX_FIG_H = 380              # network-science.css: section .fig img { max-height }

DESIGN = {"col": 520, "full": 1100}
CONTAINER = {"col": COL_W, "full": FULL_W}

NODE = 40          # disc diameter, bp  -> 40.7-41.3 px on the slide (band 26-52)
SMALLNODE = 26     # only where a figure draws dozens of dots (arrival grid, ring lattice)
FONT = 31          # pt; the cap height that lands on the slide is MEASURED, see CAP_BP
EDGE_W = 2.6
HEAVY_W = 5.0
PAD = 12           # bp of white kept around the ink when the height is cropped

NODE_MIN_PX, NODE_MAX_PX = 26, 52
TEXT_MIN_PX = 21
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


def emit(name, body, container="col", pad=PAD):
    """Compile one TikZ body to figures/<name>.png and assert what lands on the slide."""
    if _only and not any(k in name for k in _only):
        return
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
    scale = min(CONTAINER[container] / fw, MAX_FIG_H / fh, 1.0)
    factor = scale * PXBP                      # slide px per bp
    want = CONTAINER[container] / w
    assert abs(factor - want) < 1e-6, (
        f"{name}: height binds the scale ({fh/PXBP:.0f}bp tall on a {w}bp canvas) -- "
        f"the drawing must be shorter than {w * MAX_FIG_H / CONTAINER[container]:.0f}bp")

    # ink must fill the canvas width, or the deck scales white margin
    span = (xs.max() - xs.min() + 1) / fw
    assert span >= INK_FILL_MIN, (
        f"{name}: ink spans {span:.0%} of the canvas width (need {INK_FILL_MIN:.0%}) -- "
        f"widen the drawing, do not shrink the canvas")

    node_px = NODE * factor
    assert NODE_MIN_PX <= node_px <= NODE_MAX_PX, f"{name}: node disc {node_px:.0f}px"
    cap_px = CAP_BP * factor
    assert cap_px >= TEXT_MIN_PX, (
        f"{name}: text cap height {cap_px:.1f}px on the slide (floor {TEXT_MIN_PX}) -- "
        f"measured {CAP_BP:.2f}bp at {FONT}pt")

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
    print(f"  {name}.png  {fw}x{fh}  node {node_px:.0f}px  cap {cap_px:.0f}px  "
          f"discs {lo_d:.0f}-{hi_d:.0f}px  ink {span:.0%}")


# --------------------------------------------------------------------------- drawing helpers
# 26bp measured 22px on the rendered slide -- antialiasing eats ~2px a side off a small
# disc, so the band's own floor needs the headroom.
DOT = 32          # every free-standing filled dot


def dot(x, y, color="accent", d=DOT):
    return f"\\fill[{color}] ({x},{y}) circle ({d / 2}bp);\n"


def disc(x, y, label="", fill="accent", name=None, size=NODE, text="white"):
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


def _measure_cap_bp():
    """Measure the cap height the deck's own font actually renders at FONT pt.

    R1's blocker: `CAP_RATIO = 0.70` was a guess, LaTeX was silently substituting a
    24.88pt design size for the 30pt that was asked for, and the size assertion never
    noticed because it *computed* the answer from FONT instead of reading the render.
    One calibration page, measured once at import, and the guess is gone.
    """
    im = _render("cap-calibration", text(260, 100, "H"), 520, 200)
    ys, _ = np.where(np.array(im.convert("L")) < 200)
    return (ys.max() - ys.min() + 1) / PXBP


CAP_BP = _measure_cap_bp()
assert CAP_BP >= 0.66 * FONT, (
    f"cap height measures {CAP_BP:.2f}bp at {FONT}pt (ratio {CAP_BP / FONT:.3f}) -- LaTeX is "
    f"substituting a smaller design size, so every label in the deck is shrinking silently")


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
                paths.append((a, b, pts if h else np.array([pa, pb])))
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


def clearance_ok(edges, pos, r=NODE / 2 + 3):
    """No straight edge may pass through a disc it does not end at (m01's ring defect)."""
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

# Watts & Strogatz 1998, Table 1 -- transcribed once, every ratio derived.
WS98 = [
    ("Film actors", 3.65, 2.99, 0.79, 0.00027),
    ("Power grid", 18.7, 12.4, 0.080, 0.005),
    ("C. elegans", 2.65, 2.25, 0.28, 0.05),
]
WS98_R = [(n, L / Lr, C / Cr, (C / Cr) / (L / Lr)) for n, L, Lr, C, Cr in WS98]
assert [round(s) for _, _, _, s in WS98_R] == [2397, 11, 5], WS98_R

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
    for p in (om, wi):
        vx, vy = bo[0] - p[0], bo[1] - p[1]
        L = math.hypot(vx, vy)
        tip = (bo[0] - vx / L * (DOT / 2 + 4), bo[1] - vy / L * (DOT / 2 + 4))
        s += seg(p, tip, color="annot", w=2.2, dash="dashed",
                 arrow="-{Stealth[length=9bp]}")
        s += dot(round(p[0], 1), round(p[1], 1), "accent")
    s += dot(round(bo[0], 1), round(bo[1], 1), "accenttwo")   # size encodes nothing here
    s += text(om[0] - 22, om[1] + 6, "Omaha", anchor="east")
    s += text(wi[0] - 22, wi[1] - 10, "Wichita", anchor="east")
    # clear of both the disc and the 45th-parallel stretch of coastline it used to cross
    s += text(bo[0] + 16, bo[1] + 42, "Boston", color="accenttwo", anchor="south east")
    s += text(260, 30, "160 packets, one target: a stockbroker", color="annot")
    return s


def fig_milgram_rule():
    ys = 150
    xs = [60, 260, 460]
    s = ""
    for i, x in enumerate(xs):
        s += disc(x, ys, "", fill="accent" if i != 1 else "accenttwo", name=f"p{i}")
    s += edge("p0", "p1", color="annot", w=EDGE_W, arrow="-{Stealth[length=10bp]}")
    s += edge("p1", "p2", color="accenttwo", w=HEAVY_W, arrow="-{Stealth[length=12bp]}")
    s += text(260, 200, "you", color="accenttwo")
    s += text(60, 200, "sender", color="annot")
    s += text(460, 200, "next hop", color="annot")
    return s


def fig_milgram_arrivals():
    cols, rows = 20, 8
    dx, dy = 55, 40
    x0, y0 = 20, 60
    s = ""
    for i in range(160):
        r, c = divmod(i, cols)
        x, y = x0 + c * dx, y0 + (rows - 1 - r) * dy
        if i < 64:
            s += dot(x, y, "accenttwo")
        else:
            s += f"\\draw[line width=2bp,draw=annot] ({x},{y}) circle (13bp);\n"
    s += text(20, 12, "64 arrived", color="accenttwo", anchor="west")
    s += text(1080, 12, "96 never did", color="annot", anchor="east")
    return s


def _chain_row(names, y=150, x0=95, dx=152):
    return {i: (x0 + i * dx, y) for i in range(len(names))}


def fig_six_degrees_timeline():
    s = seg((60, 250), (60, 60), color="annot", w=2.4)
    for y, yr, cap, col in ((230, "1967", "Milgram mails the packets", "accent"),
                            (90, "1990", "Guare's play names it\\\\``six degrees of separation''",
                             "accenttwo")):
        s += dot(60, y, col)
        s += text(96, y, yr, color=col, anchor="west")
        s += text(210, y, cap, color="black", anchor="west", width=300)
    return s


def _numberline(dots, x0=40, x1=490, y=150, lo=0, hi=8):
    s = seg((x0, y), (x1, y), color="annot", w=2.4)
    for v in range(lo, hi + 1, 2):
        x = x0 + (v - lo) / (hi - lo) * (x1 - x0)
        s += seg((x, y - 9), (x, y + 9), color="annot", w=2.0)
        s += text(x, y - 20, str(v), color="annot", anchor="north")
    s += text((x0 + x1) / 2, y - 62, "steps between two people", color="annot")
    for v, lab, col, up in dots:
        x = x0 + (v - lo) / (hi - lo) * (x1 - x0)
        s += dot(round(x, 1), y, col)
        s += text(x, y + 28 + up, lab, color=col, anchor="south")
    return s


def fig_replication_yahoo():
    return _numberline([(6, "Milgram\\\\1967", "annot", 0), (4, "email\\\\2003", "accenttwo", 62)])


def fig_replication_facebook():
    return _numberline([(6, "Milgram\\\\1967", "annot", 0), (4, "email\\\\2003", "annot", 62),
                        (4.74, "Facebook\\\\2012", "accenttwo", 124)])


def fig_wikirace():
    # A zigzag, so every label sits on the outside of the path's turn instead of under a
    # red edge.  No extra edge either: the dotted Bagel--Chopin link made the route two
    # clicks, contradicting the figure's own caption.
    pos = {0: (60, 120), 1: (210, 270), 2: (360, 120), 3: (480, 260)}
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
    """One point: the route exists, but from `you` only the two neighbours are visible."""
    pos = {0: (70, 175), 1: (250, 280), 2: (250, 68), 3: (500, 288), 4: (500, 60),
           5: (700, 175), 6: (880, 268), 7: (880, 78), 8: (1040, 175)}
    edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5), (5, 6), (5, 7),
             (6, 8), (7, 8)]
    route = {(0, 2), (2, 4), (4, 5), (5, 7), (7, 8)}
    assert not clearance_ok(edges, pos)
    s = ("\\draw[line width=2bp,draw=annot,dash pattern=on 9bp off 7bp,"
         "rounded corners=26bp] (20,18) rectangle (340,326);\n")
    for a, b in edges:
        hot = (a, b) in route
        s += seg(pos[a], pos[b], color="accenttwo" if hot else "annot",
                 w=HEAVY_W if hot else EDGE_W)
    for i, p in pos.items():
        if i in (0, 8):
            s += disc(p[0], p[1], "", fill="accenttwo")
        elif i in (1, 2):
            s += disc(p[0], p[1], "", fill="accent")
        else:
            s += (f"\\draw[line width=2.6bp,draw=annot,fill=white] ({p[0]},{p[1]}) "
                  f"circle ({NODE / 2}bp);\n")
    s += text(70, 143, "you", color="accenttwo", anchor="north")
    s += text(1040, 143, "target", color="accenttwo", anchor="north")
    s += text(180, 330, "all you can see", color="annot", anchor="south")
    return s



# --------------------------------------------------------------------------- Part 2
CHAIN_POS = {i: (95 + i * 152, 150) for i in range(7)}   # fixed once: the graph never moves


def _chain(edges, labels=None, hot=(), hot_col="accenttwo", ringed=(), heavy_all=False,
           name_col=None, pos=CHAIN_POS, edge_num=False, curve=True):
    """The Milgram acquaintance graph. One routine, so the geometry cannot drift."""
    s = ""
    order = [e for e in edges if e in CHAIN_EDGES] + [e for e in edges if e not in CHAIN_EDGES]
    for k, (a, b) in enumerate(order):
        col = hot_col if (a, b) in hot else "black"
        w = HEAVY_W if ((a, b) in hot or heavy_all) else EDGE_W
        if curve and (b - a) > 1:
            bend = 60 if (a, b) == CHORD else -34
            s += (f"\\draw[line width={w}bp,draw={col}] ({pos[a][0]},{pos[a][1]}) "
                  f"to[bend left={bend}] ({pos[b][0]},{pos[b][1]});\n")
        else:
            s += seg(pos[a], pos[b], color=col, w=w)
    for i in pos:
        s += disc(pos[i][0], pos[i][1], labels[i] if labels else "",
                  fill="accenttwo" if i in ringed else "accent")
    if edge_num:
        for k, (a, b) in enumerate(CHAIN_EDGES):
            mx = (pos[a][0] + pos[b][0]) / 2
            s += text(mx, pos[a][1] + 14, str(k + 1), color="accenttwo", anchor="south")
    return s


def _names(pos=CHAIN_POS, col="annot", dy=-34, highlight=None):
    """`highlight` is opt-in: on every Part Two figure accent-2 is already carrying the
    chord, the shortcut, the edge counters or the diameter route, and a permanently red
    seventh name made the colour mean two things in one picture."""
    return "".join(text(pos[i][0], pos[i][1] + dy, NAMES[i],
                        color="accenttwo" if i == highlight else col, anchor="north")
                   for i in range(7))


def _knew(edge, verb="already knew"):
    """Built from NAMES and the edge tuple, so a caption can never name the wrong pair."""
    a, b = edge
    return f"the {NAMES[a]} {verb} the {NAMES[b]}"


def fig_milgram_chain():
    s = ""
    for a, b in CHAIN_EDGES:
        s += seg(CHAIN_POS[a], CHAIN_POS[b], color="annot", w=EDGE_W,
                 arrow="-{Stealth[length=11bp]}")
    for i in range(7):
        s += disc(CHAIN_POS[i][0], CHAIN_POS[i][1], "",
                  fill="accenttwo" if i == 6 else "accent")
    s += _names(highlight=6)
    s += text(CHAIN_POS[0][0], 196, "Omaha", color="annot", anchor="south")
    s += text(CHAIN_POS[6][0], 196, "Boston", color="accenttwo", anchor="south")
    s += text(550, 250, "six hands, Omaha to Boston", color="accenttwo", anchor="south")
    return s


def fig_chain_graph():
    s = _chain(CHAIN_EDGES, labels=LETTERS)
    s += _names()
    s += text(550, 240, "one person, one node --- ``knows'' is the edge",
              color="annot", anchor="south")
    return s


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
    s += text(260, 60, "$d(i,j)=2$: two edges, not two miles",
              color="black", anchor="north")
    return s


def fig_chain_blank():
    s = _chain(CHAIN_EDGES, labels=LETTERS)
    s += ring(*CHAIN_POS[0])
    s += ring(*CHAIN_POS[6])
    s += _names()
    s += text(550, 245, "how many edges from A to G?", color="accenttwo", anchor="south")
    return s


def fig_distance_six():
    s = _chain(CHAIN_EDGES, labels=LETTERS, hot=set(CHAIN_EDGES), edge_num=True)
    s += _names()
    s += text(550, 250, "$d(A,G) = 6$", color="accenttwo", anchor="south")
    return s


def fig_chain_chord():
    s = _chain(CHAIN_EDGES + [CHORD], labels=LETTERS, hot={CHORD})
    s += _names()
    s += text(550, 275, _knew(CHORD), color="accenttwo", anchor="south")
    return s


def fig_two_routes():
    """The rejected route is annotation gray, not gold: gold text measures 2.0:1 against
    white where the red on the same figure measures 5.5:1, and the floor is 3:1."""
    p = {0: (70, 120), 1: (260, 250), 2: (450, 120)}
    s = seg(p[0], p[1], color="annot", w=EDGE_W, dash="dash pattern=on 9bp off 7bp")
    s += seg(p[1], p[2], color="annot", w=EDGE_W, dash="dash pattern=on 9bp off 7bp")
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


def _dotplot(counts, mean, caption):
    """21 pairs, one dot each, laid out in rows by distance -- so the tallest column of
    the two plots (9 pairs at d=2) still fits inside a column figure.

    The mean rule is clipped to the dots it summarises: at full canvas width it ran 112bp
    past the last dot and struck through the `d = 2` row label like a deletion mark."""
    x0, dx, ytop, dy = 168, 40, 300, 46
    s = ""
    xr = x0
    for d in range(1, 7):
        y = ytop - (d - 1) * dy
        s += text(132, y, f"$d={d}$", color="annot", anchor="east")
        for k in range(counts.get(d, 0)):
            s += dot(x0 + k * dx, y, "accent")
            xr = max(xr, x0 + k * dx)
    ym = ytop - (float(mean) - 1) * dy
    s += seg((x0 - DOT / 2 - 12, ym), (xr + DOT / 2 + 12, ym), color="accenttwo", w=3.4,
             dash="dash pattern=on 10bp off 7bp")
    s += text(260, 12, caption, color="accenttwo", anchor="south")
    return s


def fig_apl_chain():
    return _dotplot(CNT_CHAIN, apl(G_CHAIN), "average over all 21 pairs: $8/3 = 2.67$")


def fig_apl_shortcut():
    return _dotplot(CNT_FULL, apl(G_FULL), "average over all 21 pairs: $38/21 = 1.81$")


def fig_chain_shortcut():
    s = _chain(CHAIN_EDGES + [CHORD, SHORTCUT], labels=LETTERS, hot={SHORTCUT})
    s += _names()
    s += text(550, 285, "one long edge: " + _knew(SHORTCUT[::-1], "knows"),
              color="accenttwo", anchor="south")
    return s


DIA_PAIR = (0, 6)
assert nx.shortest_path_length(G_FULL, *DIA_PAIR) == nx.diameter(G_FULL) == 3
DIA_ROUTE = nx.shortest_path(G_FULL, *DIA_PAIR)


def fig_diameter():
    hot = set()
    for a, b in zip(DIA_ROUTE, DIA_ROUTE[1:]):
        hot.add((min(a, b), max(a, b)))
    s = _chain(CHAIN_EDGES + [CHORD, SHORTCUT], labels=LETTERS, hot=hot)
    s += _names()
    s += text(550, 285, "worst pair in the whole network: 3 edges",
              color="accenttwo", anchor="south")
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


def fig_worksheet_a_answer():
    s = _chain(CHAIN_EDGES + [CHORD, SHORTCUT], labels=LETTERS)
    s += text(550, 285, WA_A, color="accenttwo", anchor="south")
    s += text(550, 40, f"diameter $= {WA_DIA}$: no pair in the network is further apart",
              color="accenttwo", anchor="north")
    return s



# --------------------------------------------------------------------------- Part 3
def ellipse_pos(n, cx, cy, rx, ry, start=90, ccw=True):
    out = {}
    for i in range(n):
        a = math.radians(start + (360 / n) * (i if ccw else -i))
        out[i] = (cx + rx * math.cos(a), cy + ry * math.sin(a))
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
    s += text(260, 320, "three nodes, all three edges: a triangle",
              color="accenttwo", anchor="south")
    return s


def fig_triangle_triplet():
    s = _closed_panel(TRI_L)
    for a, b in ((0, 1), (1, 2)):
        s += seg(TRI_R[a], TRI_R[b], color="black", w=EDGE_W)
    for i in TRI_R:
        s += disc(TRI_R[i][0], TRI_R[i][1], "", fill="accent")
    s += text(125, 55, "closed: a triangle", color="accenttwo", anchor="north")
    s += text(395, 55, "open", color="black", anchor="north")
    s += text(260, 320, "three nodes, at least two edges: a triplet",
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


TRI = {0: (68, 100), 1: (452, 100), 2: (260, 290)}


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
    s = "".join(seg(TRI[a], TRI[b], color="black", w=EDGE_W)
                for a, b in ((0, 1), (1, 2), (0, 2)))
    s += _walk_loop((0, 1, 2), 0.60, "accenttwo", 3.4)     # i -> j -> l -> i
    s += _walk_loop((0, 2, 1), 0.36, "accentthree", 4.4)   # i -> l -> j -> i
    for i, lab in ((0, "$i$"), (1, "$j$"), (2, "$\\ell$")):
        s += disc(TRI[i][0], TRI[i][1], lab, fill="accent")
    s += text(260, 20, "two ways round: $(A^3)_{ii} = 2$", color="accenttwo",
              anchor="south")
    return s


def fig_a3_formula():
    s = _triangle(("accenttwo", "accenttwo", "accenttwo"))
    s += text(260, 20, "$C_i = \\dfrac{(A^3)_{ii}}{k_i(k_i-1)} = \\dfrac{2}{2\\cdot 1} = 1$",
              color="accenttwo", anchor="south")
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
WM_HUB = (300, 190)
WM = {}
for _b in range(5):
    for _s2, _off in ((0, -18), (1, 18)):
        _a = math.radians(18 + 72 * _b + _off)
        WM[(_b, _s2)] = (WM_HUB[0] + 245 * math.cos(_a), WM_HUB[1] + 150 * math.sin(_a))
WM_EDGES = [((b, s2), "hub") for b in range(5) for s2 in (0, 1)] + \
           [((b, 0), (b, 1)) for b in range(5)]


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


def fig_windmill():
    s = _windmill()
    s += text(760, 240, "one hub,\\\\five closed blades", color="black", anchor="west",
              width=330)
    s += text(760, 110, "how clustered\\\\is this network?", color="accenttwo",
              anchor="west", width=330)
    return s


def fig_windmill_cbar():
    s = _windmill(blade_label="1")
    s += seg((WM_HUB[0] + 22, WM_HUB[1] - 8), (700, 120), color="accenttwo", w=2.2)
    s += text(712, 120, "hub: $C_i = 1/9$", color="accenttwo", anchor="west")
    s += text(712, 250, "each blade node: $C_i = 1$", color="black", anchor="west")
    s += text(700, 40, "$\\bar C = 91/99 = 0.92$", color="accenttwo", anchor="west")
    return s


def fig_windmill_split():
    s = _windmill(blade_label="1")
    s += seg((WM_HUB[0] + 22, WM_HUB[1] - 8), (700, 120), color="accenttwo", w=2.2)
    s += text(712, 120, "the hub owns 45\\\\of the 55 triplets", color="accenttwo",
              anchor="west", width=370)
    s += text(700, 300, "node-weighted: $\\bar C = 0.92$", color="black", anchor="west")
    s += text(700, 30, "triplet-weighted: $C = 0.27$", color="accenttwo", anchor="west")
    return s


def fig_transitivity_def():
    s = ""
    for b in range(5):
        p, q = WM[(b, 0)], WM[(b, 1)]
        s += (f"\\fill[accenttwo,opacity=0.24] ({WM_HUB[0]},{WM_HUB[1]}) -- "
              f"({p[0]:.1f},{p[1]:.1f}) -- ({q[0]:.1f},{q[1]:.1f}) -- cycle;\n")
    s += _windmill()
    s += text(700, 250, "5 triangles shaded", color="accenttwo", anchor="west")
    s += text(700, 130, "55 triplets in all", color="black", anchor="west")
    return s


WB_NODES = [0, 1, 3]
WB_ANS = [C_FULL[i] for i in WB_NODES]
assert WB_ANS == [Fraction(1), Fraction(1, 3), Fraction(0)], WB_ANS


def fig_worksheet_b():
    s = _chain(CHAIN_EDGES + [CHORD, SHORTCUT], labels=LETTERS)
    s += text(550, 285, "$C_A$? \\quad $C_B$? \\quad $C_D$?", color="black", anchor="south")
    return s


def fig_worksheet_b_answer():
    """No value row: the deck reveals the three answers one fragment at a time, and a
    figure that prints them statically above the fragments gives the game away."""
    s = _chain(CHAIN_EDGES + [CHORD, SHORTCUT], labels=LETTERS)
    s += text(550, 285, f"and over all seven nodes: $\\bar C = "
                        f"{CBAR_FULL.numerator}/{CBAR_FULL.denominator} "
                        f"= {float(CBAR_FULL):.2f}$", color="accenttwo", anchor="south")
    return s



# --------------------------------------------------------------------------- Part 4
def fig_paradox():
    cl = {0: (70, 230), 1: (160, 300), 2: (250, 245), 3: (150, 165), 4: (258, 130)}
    cle = [(0, 1), (1, 2), (0, 3), (1, 3), (2, 3), (3, 4), (2, 4)]
    chain = {5: (420, 195), 6: (570, 250), 7: (720, 195), 8: (870, 250), 9: (1030, 195)}
    pos = {**cl, **chain}
    edges = cle + [(2, 5), (5, 6), (6, 7), (7, 8), (8, 9)]
    assert not clearance_ok(edges, pos)
    s = ""
    for a, b in edges:
        s += seg(pos[a], pos[b], color="black" if (a, b) in cle else "annot", w=EDGE_W)
    for i2, q in pos.items():
        s += disc(q[0], q[1], "", fill="accenttwo" if i2 == 9 else "accent")
    s += text(36, 352, "friends of friends are friends", color="black",
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
    s += text(260, 20, "every pair: heads with probability $p$", color="accenttwo",
              anchor="south")
    return s


def fig_er_clustering():
    """No ring on one pair: it was bigger than every node disc and read as an extra node
    -- or as 'this pair is special', which is the opposite of the point."""
    s = _ego(dashed=EGO_ALL)
    s += text(260, 14, "10 pairs, 10 coins: $C_{\\mathrm{rand}} = p$",
              color="accenttwo", anchor="south")
    return s


FAN_ROWS = [(620, 60, ["you"]), (None, 200, None), (None, 340, None)]
FAN_L1 = [340, 620, 900]
FAN_L2 = [250, 340, 430, 530, 620, 710, 810, 900, 990]


def _fanout():
    s = ""
    for x in FAN_L1:
        s += seg((620, 60), (x, 200), color="black", w=EDGE_W)
    for j, x in enumerate(FAN_L2):
        s += seg((FAN_L1[j // 3], 200), (x, 340), color="black", w=EDGE_W)
    s += disc(620, 60, "", fill="accenttwo")
    for x in FAN_L1:
        s += disc(x, 200, "", fill="accent")
    for x in FAN_L2:
        s += disc(x, 340, "", fill="accent")
    return s


def fig_fanout():
    s = _fanout()
    s += text(200, 60, "you", color="accenttwo", anchor="east")
    s += text(200, 200, "$\\langle k \\rangle$", color="black", anchor="east")
    s += text(200, 340, "$\\langle k \\rangle^2$", color="black", anchor="east")
    return s


POW = [150 ** L for L in range(1, 6)]
assert abs(math.log(8e9) / math.log(150) - 4.55) < 0.01


def fig_fanout_solve():
    """The vertical axis is logarithmic, so it has to say so: unlabelled, exponential
    fan-out renders as a straight line, which is the opposite of the slide's point."""
    xa, ya = 118, 100                       # axis corner
    x0, x1, y1 = 190, 1030, 340
    def X(L):
        return x0 + (L - 1) / 4 * (x1 - x0)
    def Y(v):
        return ya + (math.log10(v) - 2) / 9 * (y1 - ya)

    s = seg((xa, ya), (1060, ya), color="annot", w=2.2)
    s += seg((xa, ya), (xa, y1), color="annot", w=2.2)
    for e in range(2, 12):
        y = Y(10 ** e)
        s += seg((xa - 9, y), (xa + 9, y), color="annot", w=2.0)
        if e % 3 == 2:
            s += text(xa - 18, y, f"$10^{{{e}}}$", color="annot", anchor="east")
    s += text(38, (ya + y1) / 2, "people reached", color="annot", rotate=90)

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
    s += text(400, 318, "$L = \\ln n / \\ln \\langle k \\rangle = 4.55$",
              color="accenttwo", anchor="south west")
    return s


RND12 = nx.gnm_random_graph(12, 14, seed=1)
assert sum(nx.triangles(RND12).values()) == 0, "the free-vs-not graph must be triangle-free"
RND12_POS = ellipse_pos(12, 260, 200, 225, 130, start=90)
RND12_PATH = nx.shortest_path(RND12, 0, max(nx.single_source_shortest_path_length(RND12, 0).items(), key=lambda kv: kv[1])[0])
assert nx.is_connected(RND12)


def fig_free_vs_not():
    s = ""
    hot = {(min(a, b), max(a, b)) for a, b in zip(RND12_PATH, RND12_PATH[1:])}
    for a, b in RND12.edges():
        e = (min(a, b), max(a, b))
        s += curve_edge(a, b, RND12_POS, color="accenttwo" if e in hot else "black",
                        w=HEAVY_W if e in hot else EDGE_W, centroid=(260, 190))
    for i2 in RND12_POS:
        s += disc(RND12_POS[i2][0], RND12_POS[i2][1], "", fill="accent")
    s += text(260, 12, f"{len(RND12_PATH)-1} hops across --- and not one triangle",
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


def _logaxis(x0, x1, y, decades):
    s = seg((x0, y), (x1, y), color="annot", w=2.2)
    for k in range(decades + 1):
        x = x0 + k / decades * (x1 - x0)
        s += seg((x, y - 9), (x, y + 9), color="annot", w=2.0)
        lab = "1" if k == 0 else (f"$10^{{{k}}}$" if k > 1 else "10")
        s += text(x, y - 14, lab, color="annot", anchor="north")
    return s


def fig_ws1998_dots():
    """Slide 60 asks students to read both ratios off this axis.  The three path-length
    dots land 1.22 / 1.51 / 1.18 -- within 17px of each other on a log axis where a decade
    is 158px -- so every dot prints its own value."""
    x0, x1, dec = 330, 1050, 4
    def X(v):
        return x0 + math.log10(v) / dec * (x1 - x0)
    s = _logaxis(x0, x1, 96, dec)
    for r, (nm, lr, cr, _) in enumerate(WS98_R):
        y = 168 + (2 - r) * 78
        s += text(300, y, nm, color="black", anchor="east")
        s += seg((X(lr), y), (X(cr), y), color="annot", w=2.0)
        for v, col in ((lr, "annot"), (cr, "accenttwo")):
            s += dot(round(X(v), 1), y, col)
            s += text(round(X(v), 1), y + 20,
                      f"{v:.0f}" if v >= 10 else (f"{v:.1f}" if v >= 2 else f"{v:.2f}"),
                      color=col, anchor="south")
    s += text(345, 112, "path length", color="annot", anchor="south west")
    s += text(1050, 112, "clustering", color="accenttwo", anchor="south east")
    return s


def fig_ws1998_sigma():
    x0, x1, dec = 330, 1050, 4
    def X(v):
        return x0 + math.log10(v) / dec * (x1 - x0)
    s = _logaxis(x0, x1, 60, dec)
    s += seg((x0, 60), (x0, 330), color="accenttwo", w=3.0,
             dash="dash pattern=on 10bp off 7bp")
    s += text(x0, 340, "$\\sigma = 1$", color="accenttwo", anchor="south")
    for r, (nm, _, _, sg) in enumerate(WS98_R):
        y = 140 + (2 - r) * 75
        s += text(300, y, nm, color="black", anchor="east")
        s += dot(round(X(sg), 1), y, "accenttwo")
        s += text(X(sg) + 26, y, f"$\\sigma \\approx {sg:.0f}$" if sg < 100
                  else "$\\sigma \\approx 2400$", color="accenttwo", anchor="west")
    return s


# --------------------------------------------------------------------------- Part 5
# 16 nodes, not 20: at 40bp discs a 20-node ring needs a 358bp circle, which fills a
# column figure's whole height and leaves the deck scaling white margin either side.
# k=4 gives C = 3(k-2)/(4(k-1)) = 0.5 whatever n is, so nothing in the story changes.
# Vertically 124: an inward chord bowed clear of the disc it passes needs 34bp of the
# ring's own radius, and the canvas is 364bp tall.  Horizontally 180, because a circle
# that short left the drawing spanning 60% of the canvas width -- below that the deck is
# scaling white margin instead of the picture.
RING_N, RING_K = 16, 4
RING_RX, RING_RY = 180, 124
RING_C = (260, 200)
RING_POS = ellipse_pos(RING_N, RING_C[0], RING_C[1], RING_RX, RING_RY, start=90)
RING_EDGES = sorted({(min(i, (i + d) % RING_N), max(i, (i + d) % RING_N))
                     for i in range(RING_N) for d in (1, 2)})
assert len(RING_EDGES) == RING_N * RING_K // 2 == 32
_R16 = nx.Graph(RING_EDGES)
assert Fraction(nx.average_clustering(_R16)).limit_denominator(100) == Fraction(1, 2)
RING_DIA = nx.diameter(_R16)
RING_L = apl(_R16)
assert RING_DIA == 4, RING_DIA


# The chord of a triangle must arc clear of the disc it passes, with white left over --
# at NODE/2 + 3 the gap was 3bp and every triangle in the lattice was a hairline.
RING_CLEAR = NODE / 2 + 16


def assert_triangles_open(name, pos, paths):
    """Every chord must leave a visible interior in the triangle it closes.

    C16(1,2) is planar and a zero-crossing drawing does exist -- alternate the chords
    inside and outside the ring and the 16 crossings go away.  It was built and rejected:
    an outward bow has to clear the disc from the far side, which needs 34bp against 14bp
    inward, and the result is a wavy flower in which not one triangle can be picked out.
    On the slide whose claim is "triangles everywhere" that trades a Major for a Blocker.
    So the chords all bow inward, deeply, and this is the invariant that protects what the
    slide actually asserts.
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


def _ring(hot=(), pos=RING_POS, edges=RING_EDGES, ringed=(), cen=RING_C, dashed=(),
          check=True):
    s = ""
    paths = []
    for a, b in edges:
        h = (a, b) in hot or (b, a) in hot
        s += curve_edge(a, b, pos, color="accenttwo" if h else "black",
                        w=HEAVY_W if h else EDGE_W, centroid=cen,
                        clear=RING_CLEAR, paths=paths)
    for a, b in dashed:
        s += curve_edge(a, b, pos, color="annot", w=2.2,
                        dash="dash pattern=on 8bp off 7bp", centroid=cen,
                        clear=RING_CLEAR)
    if check:
        assert_triangles_open("ring lattice", pos, paths)
    for i2 in pos:
        s += disc(pos[i2][0], pos[i2][1], "", fill="accent")
    for i2 in ringed:
        s += ring(pos[i2][0], pos[i2][1], color="accentthree", w=4.0)
    return s


def fig_ring_lattice():
    s = _ring()
    s += text(260, 8, f"joined to its {RING_K} nearest neighbours",
              color="black", anchor="south")
    return s


RING_FAR = nx.shortest_path(_R16, 0, RING_N // 2)
assert len(RING_FAR) - 1 == RING_DIA


def fig_ring_distance():
    hot = {(min(a, b), max(a, b)) for a, b in zip(RING_FAR, RING_FAR[1:])}
    s = _ring(hot=hot)
    s += text(260, 8, f"{RING_DIA} hops to cross a ring of {RING_N} nodes",
              color="accenttwo", anchor="south")
    return s


# seed 117541, not 2: at m = 32 a triangle-free connected draw exists but is rare (8 in the
# first 400,000 seeds), and seed 2 carried three triangles under a caption saying it had
# none.  The `< 0.10` assertion was too weak to notice; this one cannot be satisfied by a
# graph with a single closed triplet in it.
RND16 = nx.gnm_random_graph(RING_N, len(RING_EDGES), seed=117541)
assert nx.is_connected(RND16)
assert sum(nx.triangles(RND16).values()) == 0, "the shuffled graph must be triangle-free"
RND16_C = nx.average_clustering(RND16)
RND16_L = nx.average_shortest_path_length(RND16)
assert RND16_C == 0.0 and RND16_L < float(RING_L), (RND16_C, RND16_L, float(RING_L))


def fig_random_graph():
    s = ""
    for a, b in RND16.edges():
        s += curve_edge(a, b, RING_POS, centroid=RING_C, w=2.2)
    for i2 in RING_POS:
        s += disc(RING_POS[i2][0], RING_POS[i2][1], "", fill="accent")
    s += text(260, 8, "the same 16 nodes and 32 edges, shuffled",
              color="black", anchor="south")
    return s


def fig_lattice_vs_random():
    lp = ellipse_pos(RING_N, 280, 205, 118, 118, start=90)
    rp = ellipse_pos(RING_N, 820, 205, 118, 118, start=90)
    s = ""
    paths = []
    for a, b in RING_EDGES:
        s += curve_edge(a, b, lp, centroid=(280, 205), clear=RING_CLEAR, paths=paths)
    assert_triangles_open("lattice-vs-random (left panel)", lp, paths)
    for a, b in RND16.edges():
        s += curve_edge(a, b, rp, centroid=(820, 205), w=2.2)
    for p2 in (lp, rp):
        for i2 in p2:
            s += disc(p2[i2][0], p2[i2][1], "", fill="accent")
    s += text(280, 34, "lattice: triangles, long routes", color="black", anchor="north")
    s += text(820, 34, "random: short routes, no triangles", color="black", anchor="north")
    return s


REWIRE_OLD, REWIRE_NEW = (0, 2), (0, 9)
assert REWIRE_OLD in RING_EDGES and REWIRE_NEW not in RING_EDGES


def fig_ws_rewire_step():
    """Each annotation is drawn in the colour of the thing it names, next to that thing.
    The red sentence used to name the gray edge and the gray figcaption the red one."""
    s = ""
    for a, b in RING_EDGES:
        if (a, b) == REWIRE_OLD:
            continue
        s += curve_edge(a, b, RING_POS, centroid=RING_C, clear=RING_CLEAR)
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
               ps=[round(10 ** (-4 + 4 * i / 12), 6) for i in range(13)])
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


BAND_LO, BAND_HI = 0.001, 0.1
assert math.log10(BAND_HI) - math.log10(BAND_LO) >= 2.0, "the band must span two decades"


def _sweep_frame(band=False):
    """Both curves are fractions of the lattice value, so the vertical axis has to be
    ticked and named -- two slides assert how far each curve has fallen."""
    x0, x1, y0, y1 = 200, 1050, 110, 320
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
    for k in range(5):
        x = x0 + k / 4 * (x1 - x0)
        s += seg((x, y0 - 9), (x, y0 + 9), color="annot", w=2.0)
        s += text(x, y0 - 12, ["$10^{-4}$", "$10^{-3}$", "0.01", "0.1", "1"][k],
                  color="annot", anchor="north")
    s += text(625, y0 - 52, "rewiring probability $p$", color="annot", anchor="north")
    for v, lab in ((0.0, "0"), (0.5, "0.5"), (1.0, "1")):
        s += seg((x0 - 9, Y(v)), (x0 + 9, Y(v)), color="annot", w=2.0)
        s += text(x0 - 16, Y(v), lab, color="annot", anchor="east")
    s += text(x0, y1 + 20, "fraction of the lattice value", color="annot",
              anchor="south west")
    for key, col, lab, ly, lx in (("C", "accenttwo", "$C(p)/C(0)$", 0.84, 360),
                                  ("L", "accent", "$L(p)/L(0)$", 0.30, 30)):
        base = SWEEP[key + "0"]
        pts = [(X(p), Y(v / base)) for p, v in zip(SWEEP["p"], SWEEP[key])]
        s += "\\draw[line width=3.4bp,draw=%s] %s;\n" % (
            col, " -- ".join("(%.1f,%.1f)" % q for q in pts))
        s += text(x0 + lx, Y(ly), lab, color=col, anchor="west")
    return s


def fig_ws_sweep():
    return _sweep_frame()


def fig_ws_band():
    s = _sweep_frame(band=True)
    s += text(1050, 340, "both at once", color="accenttwo", anchor="south east")
    return s


def fig_ws_widget():
    rng = random.Random(3)
    adj = _ws_adj(RING_N, RING_K, 0.14, rng)
    edges = sorted({(min(i, j), max(i, j)) for i, a in enumerate(adj) for j in a})
    lattice = set(RING_EDGES)
    s = ""
    for a, b in edges:
        new = (a, b) not in lattice
        s += curve_edge(a, b, RING_POS, color="accenttwo" if new else "black",
                        w=HEAVY_W if new else EDGE_W, centroid=RING_C,
                        clear=NODE / 2 + 3 if new else RING_CLEAR)
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
    s = ""
    for a, b in RING_EDGES:
        s += curve_edge(a, b, RING_POS, centroid=RING_C, clear=RING_CLEAR)
    s += curve_edge(*SHORTCUT_EDGE, RING_POS, color="accenttwo", w=HEAVY_W,
                    centroid=RING_C)
    for i2 in RING_POS:
        s += disc(RING_POS[i2][0], RING_POS[i2][1], "0" if i2 == 0 else "", fill="accent")
    for v in [0] + SHORTENED:
        s += ring(RING_POS[v][0], RING_POS[v][1], color="accentthree", w=4.0)
    s += text(260, 8, f"gold: node 0 and the {len(SHORTENED)} now closer to it",
              color="accenttwo", anchor="south")
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
    s += text(260, 40, "distance between the two red nodes?",
              color="black", anchor="north")
    return s


def fig_disconnected_answer():
    s = _twocomp()
    s += seg((115, 105), (440, 165), color="accenttwo", w=2.4,
             dash="dash pattern=on 9bp off 8bp")
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
    s += text(260, 40, "one friend only --- what is its $C_i$?",
              color="black", anchor="north")
    return s


def fig_degree_one_answer():
    s = _degree_one()
    s += text(260, 40, "$k(k-1)/2 = 0$: nothing to divide by",
              color="accenttwo", anchor="north")
    return s


def fig_sigma_lt_1_q():
    # "high clustering" was half the answer, printed on the question slide.
    s = _ring()
    s += text(260, 8, "a ring lattice: long routes", color="black", anchor="south")
    return s


GRID_POS = {(c, r): (60 + c * 100, 78 + r * 82) for c in range(5) for r in range(4)}
GRID_EDGES = [((c, r), (c + 1, r)) for c in range(4) for r in range(4)] + \
             [((c, r), (c, r + 1)) for c in range(5) for r in range(3)]
_G54 = nx.Graph(GRID_EDGES)
assert nx.transitivity(_G54) == 0


def fig_grid_no_triangles():
    s = ""
    for a, b in GRID_EDGES:
        s += seg(GRID_POS[a], GRID_POS[b], color="black", w=EDGE_W)
    for q in GRID_POS.values():
        s += disc(q[0], q[1], "", fill="accent")
    # below the grid, where every other figure in the deck puts its annotation -- at
    # y = 340 it sat on the top row of discs
    s += text(260, 8, "a street grid: not one triangle, so $C = 0$",
              color="accenttwo", anchor="south")
    return s


GNM_POS = ellipse_pos(6, 250, 190, 190, 100, start=0)
GNP_POS = ellipse_pos(6, 840, 190, 190, 100, start=0)
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
    s += text(250, 44, "$G(n,m)$: deal exactly 5 edges", color="black", anchor="north")
    s += text(840, 44, "$G(n,p)$: one coin per pair", color="black", anchor="north")
    return s


def fig_gnm_gnp():
    s = _gnm_gnp()
    s += text(545, 330, "same graphs? same mathematics?", color="accenttwo",
              anchor="south")
    return s


def fig_gnm_gnp_answer():
    s = _gnm_gnp()
    s += text(250, 330, "edges are coupled", color="annot", anchor="south")
    s += text(840, 330, "edges are independent", color="accenttwo", anchor="south")
    return s


# --------------------------------------------------------------------------- wrap-up
def fig_universality():
    x0, x1, dec = 330, 1050, 4
    def X(v):
        return x0 + math.log10(v) / dec * (x1 - x0)
    s = _logaxis(x0, x1, 96, dec)
    s += text(690, 42, "small-world index", color="annot", anchor="north")
    s += seg((x0, 96), (x0, 296), color="annot", w=3.0,
             dash="dash pattern=on 10bp off 7bp")
    # right of the line, or it lands on the "social" row label
    s += text(x0 + 12, 300, "$\\sigma = 1$", color="annot", anchor="south west")
    for r, (dom, (_, _, _, sg)) in enumerate(zip(["social", "technological", "biological"],
                                                 WS98_R)):
        y = 160 + (2 - r) * 65
        s += text(300, y, dom, color="black", anchor="east")
        s += dot(round(X(sg), 1), y, "accenttwo")
    s += text(690, 314, "three different worlds, one signature",
              color="accenttwo", anchor="south")
    return s


def fig_sw_map():
    """Panel 3 is the same lattice rewired at p = 1, not a fresh random graph, so "red:
    the rewired edges" is true of it: at the far end of the p arrow every edge has moved,
    and the panel used to draw all 24 of them black."""
    cs = [(180, 232), (550, 232), (920, 232)]
    labs = ["lattice", "small world", "random"]
    rng = random.Random(5)
    lat = sorted({(min(i, (i + d) % 12), max(i, (i + d) % 12))
                  for i in range(12) for d in (1, 2)})
    mids = sorted({(min(i, j), max(i, j))
                   for i, a in enumerate(_ws_adj(12, 4, 0.12, rng)) for j in a})
    full = sorted({(min(i, j), max(i, j))
                   for i, a in enumerate(_ws_adj(12, 4, 1.0, random.Random(11))) for j in a})
    assert sum((e not in lat) for e in full) >= 18, "p = 1 must move most of the lattice"
    s = ""
    for k, (cx, cy) in enumerate(cs):
        pos = ellipse_pos(12, cx, cy, 92, 92, start=90)
        ed = (lat, mids, full)[k]
        for a, b in ed:
            new = k > 0 and (a, b) not in lat
            s += curve_edge(a, b, pos, color="accenttwo" if new else "black",
                            w=HEAVY_W if new else EDGE_W, centroid=(cx, cy),
                            clear=NODE / 2 + 3 if new else RING_CLEAR)
        for i2 in pos:
            s += disc(pos[i2][0], pos[i2][1], "", fill="accent")
        s += text(cx, 104, labs[k], color="accenttwo" if k == 1 else "black",
                  anchor="north")
    s += seg((80, 56), (1020, 56), color="annot", w=2.4,
             arrow="-{Stealth[length=11bp]}")
    s += text(550, 38, "rewiring probability $p$", color="annot", anchor="north")
    return s


RECAP_CHORDS = [(0, RING_N // 2), (4, 11)]
assert all(e not in RING_EDGES for e in RECAP_CHORDS)


def fig_recap():
    # two chords, because the caption on this slide says "a few shortcuts"
    s = ""
    for a, b in RING_EDGES:
        s += curve_edge(a, b, RING_POS, centroid=RING_C, clear=RING_CLEAR)
    for a, b in RECAP_CHORDS:
        s += curve_edge(a, b, RING_POS, color="accenttwo", w=HEAVY_W, centroid=RING_C)
    for i2 in RING_POS:
        s += disc(RING_POS[i2][0], RING_POS[i2][1], "", fill="accent")
    s += text(260, 8, "triangles kept, routes short: a small world",
              color="accenttwo", anchor="south")
    return s


def fig_m03_teaser():
    """The X goes on the edge it removes.  Both used to land near where the two chords
    crossed, so the render X-ed out the crossing rather than either edge -- and the cut
    edges are dashed as well, so "removed" reads without the marker at all."""
    # spread round the ring: the old three all ran close to the centre, so their midpoints
    # -- and therefore both X marks -- landed in the same 70bp of the drawing
    shortcuts = [(1, 6), (3, 13), (9, 14)]
    assert all(e not in RING_EDGES for e in shortcuts)
    mids = {}
    for e in shortcuts:
        paths = []
        curve_edge(*e, RING_POS, centroid=RING_C, paths=paths)
        q = paths[0][2]
        mids[e] = q.mean(axis=0) if len(q) == 2 else q[len(q) // 2]
    # which two get cut is arbitrary, so let the drawing choose: the pair whose marks are
    # furthest apart.  Picking the first two put both X's on the chords' crossing point.
    cut = max(itertools.combinations(shortcuts, 2),
              key=lambda pr: math.dist(mids[pr[0]], mids[pr[1]]))
    sep = math.dist(mids[cut[0]], mids[cut[1]])
    assert sep >= 80, f"the two X marks are {sep:.0f}bp apart -- they will read as one"

    s = ""
    for a, b in RING_EDGES:
        s += curve_edge(a, b, RING_POS, centroid=RING_C, clear=RING_CLEAR)
    for e in shortcuts:
        s += curve_edge(*e, RING_POS, color="accenttwo", w=HEAVY_W, centroid=RING_C,
                        dash="dash pattern=on 13bp off 10bp" if e in cut else "")
    for i2 in RING_POS:
        s += disc(RING_POS[i2][0], RING_POS[i2][1], "", fill="accent")
    for e in cut:                       # after the discs: a marker under a node is no marker
        mx, my = mids[e]
        s += seg((mx - 16, my - 16), (mx + 16, my + 16), color="black", w=5.0)
        s += seg((mx - 16, my + 16), (mx + 16, my - 16), color="black", w=5.0)
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
    ("grid-no-triangles", fig_grid_no_triangles, "col"),
    ("gnm-gnp", fig_gnm_gnp, "full"),
    ("gnm-gnp-answer", fig_gnm_gnp_answer, "full"),
    ("universality", fig_universality, "full"),
    ("sw-map", fig_sw_map, "full"),
    ("recap", fig_recap, "col"),
    ("m03-teaser", fig_m03_teaser, "col"),
]


def main():
    for name, fn, cont in FIGURES:
        emit(name, fn(), cont)
    print(f"\n{len(_built)} figures written")


if __name__ == "__main__":
    main()

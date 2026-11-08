"""Shared setup for the m08-gnn v3 figures.  Import with:  from common import *

Rule of this deck: every word and number in a figure is at least 26 pt = 35 px on the 1280 x 720
slide (the user's rule, 2026-11-08).  figkit's sizes (13 to 26 px) are raised here through a LaTeX
preamble; one figure unit is still one slide pixel.

Run any figure script with:
    cd slides/m09 && uv run --quiet --with numpy --with scipy --with networkx --with pillow \
        --with scikit-image python figures/fig_xxx.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude/skills/slide-math/figkit"))
from figkit import (P, arrow, brace, build, edge, graph, hrule_axis, label, lineplot, node,  # noqa: E402,F401
                    pin, raw, vecdots, vertex, zoom)

HERE = Path(__file__).resolve().parent          # slides/m09/figures
IMG = HERE / "img"                               # PNGs that TikZ includes
IMG.mkdir(exist_ok=True)

# ---- type sizes: all >= 35 px -------------------------------------------------------------
PRE = r"""
\renewcommand\fstick{\fontsize{35\px}{40\px}\selectfont}
\renewcommand\fssmall{\fontsize{35\px}{40\px}\selectfont}
\renewcommand\fslabel{\fontsize{35\px}{40\px}\selectfont}
\renewcommand\fsbody{\fontsize{35\px}{40\px}\selectfont}
\renewcommand\fslarge{\fontsize{40\px}{46\px}\selectfont}
\usepackage{graphicx}
\tikzset{
  vertex/.style={circle, draw=ink, line width=2\px, fill=white, minimum size=52\px, inner sep=0pt, font=\fssmall},
  vertex hl/.style={vertex, fill=hl}, vertex hlc/.style={vertex, fill=hlc}, vertex grey/.style={vertex, fill=fillgrey},
  smallbox/.style={draw=ink, line width=2\px, fill=white, inner sep=5\px, font=\fssmall, minimum width=52\px, minimum height=52\px},
  tag/.style={draw=ink, line width=2\px, fill=white, inner xsep=8\px, inner ysep=4\px, font=\fssmall},
  note/.style={font=\fssmall, align=left, inner sep=3\px},
  arr/.style={-{Stealth[length=9bp, width=7bp]}, line width=1.5bp},
}
"""

MIN_PX = 35  # nothing in a figure may be set smaller than this

# ---- colours (hex, same as the theme) --------------------------------------------------------
HL = "#F4E6FF"      # lavender: the thing the slide is about
HLC = "#E5FDFF"     # cyan: the alternative
BLUE = "#0072B2"    # s-new
VERM = "#D55E00"    # s-base
YEL = "#E69F00"
SKY = "#56B4E9"
PINK = "#CC79A7"    # no green anywhere


def B(name: str, *parts: str):
    """Build figures/<name>.svg with the large type sizes."""
    return build(name, *parts, outdir=HERE, preamble=PRE)


# ---- images (TikZ includes PNGs; no matplotlib) -------------------------------------------------
def camera():
    """The 512 x 512 grayscale cameraman image (scikit-image, public domain) as a numpy array."""
    import skimage.data as d
    return d.camera()


def save_png(arr, name: str, scale: int = 1, nearest: bool = True) -> Path:
    """Write a 2D (gray) or 3D (RGB) uint8 array to figures/img/<name>.png; returns the path."""
    import numpy as np
    from PIL import Image
    a = np.clip(arr, 0, 255).astype("uint8")
    im = Image.fromarray(a)
    if scale != 1:
        im = im.resize((im.width * scale, im.height * scale), Image.NEAREST if nearest else Image.LANCZOS)
    p = IMG / f"{name}.png"
    im.save(p)
    return p


def picture(path: Path, at, w: float, h: float, name: str | None = None, anchor: str = "center",
            border: bool = True, interpolate: bool = False) -> str:
    """Place a PNG of w x h px with its centre at `at` (px).  border=True draws a 2 px black frame."""
    nm = f"({name}) " if name else ""
    img = rf"\includegraphics[width={w*0.75:.3f}bp,height={h*0.75:.3f}bp,interpolate={'true' if interpolate else 'false'}]{{{path.as_posix()}}}"
    frame = "draw=ink, line width=2\\px" if border else "draw=none"
    return (rf"\node[inner sep=0pt, {frame}, anchor={anchor}] {nm}at {P(*at)} {{{img}}};")


# ---- the karate club (real data) ---------------------------------------------------------------
def karate_layout(w: float, h: float, seed: int = 4, margin: float = 24):
    """Return (pos, edges, club): pos maps node 1..34 -> (x, y) px in a w x h box (y up), edges a list of
    (i, j) with 1-based names, club maps node -> 0 (Mr. Hi) or 1 (Officer)."""
    import networkx as nx
    import numpy as np
    G = nx.karate_club_graph()
    p = nx.spring_layout(G, seed=seed, k=0.35, iterations=300)
    xs = np.array([p[i][0] for i in G]); ys = np.array([p[i][1] for i in G])
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    pos = {i + 1: (margin + (p[i][0] - x0) / (x1 - x0) * (w - 2 * margin),
                   margin + (p[i][1] - y0) / (y1 - y0) * (h - 2 * margin)) for i in G}
    edges = [(u + 1, v + 1) for u, v in G.edges()]
    club = {i + 1: (0 if G.nodes[i]["club"] == "Mr. Hi" else 1) for i in G}
    return pos, edges, club


def check_min_font(*texts: str):
    """Guard: raise if a figure sets a font size below MIN_PX (looks for \\fontsize{N\\px})."""
    import re
    for t in texts:
        for m in re.finditer(r"fontsize\{(\d+(?:\.\d+)?)\\px", t):
            if float(m.group(1)) < MIN_PX:
                raise ValueError(f"font size {m.group(1)} px is below {MIN_PX} px")

"""Group c: GraphSAGE, GAT, message passing.

cd slides/m09 && uv run --quiet --with numpy --with scipy --with networkx --with pillow \
    --with scikit-image python figures/fig_c.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import *  # noqa: E402,F401,F403

import numpy as np  # noqa: E402

COLORS = r"""
\definecolor{hopa}{HTML}{D9B8F5}
\definecolor{hopb}{HTML}{B88AE0}
\newcommand\fbig{\fontsize{64\px}{64\px}\selectfont}
\newcommand\foplus{\fontsize{70\px}{70\px}\selectfont}
"""


# ---- helpers ------------------------------------------------------------------------------------
def fx(v: float) -> str:
    return f"{v:.2f}"


def square(cx, cy, s, fill, pct=100, lw=2):
    """A filled square centred at (cx, cy); fill is a colour name, pct its strength (white above 0)."""
    col = fill if pct >= 100 else f"{fill}!{int(pct)}!white"
    return (rf"\filldraw[fill={col}, draw=ink, line width={lw}\px] "
            rf"{P(cx - s / 2, cy - s / 2)} rectangle {P(cx + s / 2, cy + s / 2)};")


def vec_values(n, seed, lo=25, hi=100):
    r = np.random.default_rng(seed)
    return [float(v) for v in r.uniform(lo, hi, n)]


def vec_col(cx, top, vals, col, s=40):
    """Column of squares hanging from y=top, shade by vals (percent)."""
    out = []
    for i, v in enumerate(vals):
        out.append(square(cx, top - s / 2 - i * s, s, col, v))
    return "\n".join(out)


def vec_row(left, cy, vals, col, s=30):
    out = []
    for i, v in enumerate(vals):
        out.append(square(left + s / 2 + i * s, cy, s, col, v))
    return "\n".join(out)


def N(name, at, text="", size=52, fill="white", extra=""):
    ex = f", {extra}" if extra else ""
    return rf"\node[vertex, minimum size={size}\px, fill={fill}{ex}] ({name}) at {P(*at)} {{{text}}};"


def line(p, q, w=2, color="ink", dash=False):
    d = r", dash pattern=on 6\px off 5\px" if dash else ""
    return rf"\draw[line width={fx(w)}\px, draw={color}{d}] {P(*p)} -- {P(*q)};"


def Eline(a, b, w=2, color="ink", dash=False):
    d = r", dash pattern=on 6\px off 5\px" if dash else ""
    return rf"\draw[line width={fx(w)}\px, draw={color}{d}] ({a}) -- ({b});"


def T(at, text, anchor="center", extra=""):
    ex = f", {extra}" if extra else ""
    return rf"\node[font=\fssmall, inner sep=2\px, anchor={anchor}, align=center{ex}] at {P(*at)} {{{text}}};"


# ---- c01 ----------------------------------------------------------------------------------------
def c01_sampling_tree():
    sx = 0.85
    pos = {"t": (105, 298), "a": (52, 192), "b": (157, 192), "c": (45, 390), "d": (165, 390),
           "e": (25, 80), "f": (78, 80), "g": (20, 247), "h": (130, 80), "i": (183, 80),
           "j": (190, 247), "k": (45, 496)}
    pos = {k: (17 + x * sx, y + 20) for k, (x, y) in pos.items()}
    solid = [("t", "a"), ("t", "b"), ("a", "e"), ("a", "f"), ("b", "h"), ("b", "i")]
    dashed = [("t", "c"), ("t", "d"), ("a", "g"), ("b", "j"), ("c", "k")]
    fills = {"t": "hl", "a": "hopa", "b": "hopa", "e": "hopb", "f": "hopb", "h": "hopb", "i": "hopb"}
    ns = 36
    p = [COLORS, r"\begin{scope}[on background layer]"]
    for u, v in dashed:
        p.append(line(pos[u], pos[v], 2, "muted", dash=True))
    for u, v in solid:
        p.append(line(pos[u], pos[v], 2.5))
    p.append(r"\end{scope}")
    for k, xy in pos.items():
        if k in fills:
            p.append(N(f"g{k}", xy, "", ns, fills[k]))
        else:
            p.append(N(f"g{k}", xy, "", ns, "white", extra="draw=muted"))
    # tree
    tx = {"t": 312, "a": 260, "b": 364, "e": 234, "f": 286, "h": 338, "i": 390}
    ty = {"t": 520, "a": 300, "b": 300, "e": 100, "f": 100, "h": 100, "i": 100}
    ts = 40
    tedges = [("t", "a"), ("t", "b"), ("a", "e"), ("a", "f"), ("b", "h"), ("b", "i")]
    p.append(r"\begin{scope}[on background layer]")
    for u, v in tedges:
        p.append(line((tx[u], ty[u]), (tx[v], ty[v]), 2.5))
    p.append(r"\end{scope}")
    for k in tx:
        p.append(N(f"r{k}", (tx[k], ty[k]), "", ts, fills[k]))
    p.append(rf"\draw[arr] {P(440, 100)} -- {P(440, 520)};")
    p.append(rf"\node[font=\fssmall, inner sep=2\px, anchor=west] at {P(458, 310)} {{aggregate}};")
    B("c01_sampling_tree", *p)


# ---- c02 ----------------------------------------------------------------------------------------
def c02_sage_concat():
    s = 44
    R = 552                     # right edge of every row
    a = vec_values(4, 1)
    b = vec_values(4, 2)
    xm = R - 4 * s              # centre line of the arrows (centre of the 8-square row)
    p = [COLORS]
    yself, ynbr, ycat, yW, ynew = 540, 410, 275, 170, 50
    p.append(vec_row(R - 4 * s, yself, a, "snew", s))
    p.append(vec_row(R - 4 * s, ynbr, b, "sbase", s))
    p.append(T((0, yself), "self", anchor="west"))
    p.append(T((0, ynbr), "neighbours", anchor="west"))
    for dx in (-8, 8):
        p.append(rf"\draw[ink, line width=3\px] {P(R - 2 * s + dx, yself - 44)} -- {P(R - 2 * s + dx, ynbr + 44)};")
    p.append(vec_row(R - 8 * s, ycat, a, "snew", s))
    p.append(vec_row(R - 4 * s, ycat, b, "sbase", s))
    p.append(rf"\draw[arr] {P(xm, ynbr - 34)} -- {P(xm, ycat + 34)};")
    p.append(rf"\draw[arr] {P(xm, ycat - 34)} -- {P(xm, yW + 42)};")
    p.append(rf"\node[smallbox, minimum width=90\px, minimum height=80\px, font=\fslarge] (W) at {P(xm, yW)} {{$W$}};")
    p.append(rf"\draw[arr] {P(xm, yW - 42)} -- {P(xm, ynew + 34)};")
    c = vec_values(4, 3)
    p.append(vec_row(xm - 2 * s, ynew, c, "hlink", s))
    p.append(T((0, ynew), "new", anchor="west"))
    B("c02_sage_concat", *p)


# ---- c03 ----------------------------------------------------------------------------------------
def c03_concat_vs_sum():
    s = 50
    a = vec_values(3, 11)
    b = vec_values(3, 12)
    gap = 20
    xv = 600 - 118 - 6                       # centre of the right slot (the word "neighbour" is 235 px wide)
    xu = xv - 3 * s - gap
    lc = xu - 1.5 * s
    ny = 510
    p = []
    p.append(line((xu, ny), (xv, ny), 3))
    p.append(N("u", (xu, ny), "$u$", 66, "hl"))
    p.append(N("v", (xv, ny), "$v$", 66))
    p.append(vec_row(xu - 1.5 * s, ny - 75, a, "snew", s))
    p.append(vec_row(xv - 1.5 * s, ny - 75, b, "sbase", s))
    # sum: each cell half blue, half vermillion (a diagonal split): mixed, cannot tell who is who
    ys = 290
    p.append(T((0, ys), "sum", anchor="west"))
    for i in range(3):
        x0 = lc + (3 * s + gap) / 2 + i * s
        p.append(rf"\fill[snew] {P(x0, ys - s / 2)} -- {P(x0 + s, ys - s / 2)} -- {P(x0, ys + s / 2)} -- cycle;")
        p.append(rf"\fill[sbase] {P(x0 + s, ys - s / 2)} -- {P(x0 + s, ys + s / 2)} -- {P(x0, ys + s / 2)} -- cycle;")
        p.append(rf"\draw[ink, line width=2\px] {P(x0, ys - s / 2)} rectangle {P(x0 + s, ys + s / 2)};")
    # concat: [a | b]
    yc = 160
    p.append(T((0, yc), "concat", anchor="west"))
    p.append(vec_row(lc, yc, a, "snew", s))
    p.append(vec_row(lc + 3 * s + gap, yc, b, "sbase", s))
    p.append(T((xu, yc - 68), "self"))
    p.append(T((xv, yc - 68), "neighbour"))
    B("c03_concat_vs_sum", *p)


# ---- c04 ----------------------------------------------------------------------------------------
def c04_gcn_vs_gat():
    deg_j = [2, 3, 3, 4, 4]
    d_i = 5
    gcn = [1 / math.sqrt((d_i + 1) * (d + 1)) for d in deg_j]
    gat = [0.45, 0.25, 0.15, 0.10, 0.05]
    k = 31.0
    cols = ["snew", "sbase", "sthree", "sfour", "sfive"]
    rx, ry = 125, 170
    p = []
    for name, cx, ws in (("GCN", 175, gcn), ("GAT", 525, gat)):
        cy = 190
        p.append(rf"\node[font=\fslarge, inner sep=2\px] at {P(cx, 470)} {{{name}}};")
        pts = []
        for i in range(5):
            ang = math.radians(90 + 72 * i)
            pts.append((cx + rx * math.cos(ang), cy + ry * math.sin(ang)))
        for (x, y), w in zip(pts, ws):
            p.append(line((cx, cy), (x, y), max(2, w * k)))
        p.append(N(f"c{name}", (cx, cy), "$i$", 60, "hl"))
        for (x, y), c in zip(pts, cols):
            p.append(N(f"n{name}{x:.0f}", (x, y), "", 46, c))
    B("c04_gcn_vs_gat", *p)


# ---- c05 ----------------------------------------------------------------------------------------
def c05_attention_visual():
    e = np.array([1.2, 0.1, -0.5])
    alpha = np.exp(e) / np.exp(e).sum()
    ys = [200, 105, 10]
    p = [rf"\begin{{scope}}[on background layer]"]
    for y, al in zip(ys, alpha):
        p.append(line((36, 105), (195, y), al * 20))
    p.append(r"\end{scope}")
    p.append(N("ci", (36, 105), "$i$", 66, "hl"))
    # softmax box (text rotated)
    p.append(rf"\node[draw=ink, line width=2\px, fill=white, minimum width=290\px, minimum height=66\px, "
             rf"font=\fssmall, rotate=90, inner sep=0pt] at {P(431, 105)} {{softmax}};")
    for j, (y, ej, al) in enumerate(zip(ys, e, alpha), start=1):
        p.append(N(f"cj{j}", (195, y), f"$j_{j}$", 76))
        txt = f"${ej:.1f}$".replace("-", "{-}")
        p.append(T((304, y), txt))
        p.append(rf"\draw[arr] {P(374, y)} -- {P(396, y)};")
        p.append(rf"\draw[arr] {P(467, y)} -- {P(489, y)};")
        p.append(T((556, y), f"${al:.2f}$"))
    p.append(T((304, 290), "scores"))
    p.append(T((548, 290), "weights"))
    B("c05_attention_visual", *p)


# ---- c06 ----------------------------------------------------------------------------------------
def c06_mp_flow():
    bx, bw, bh = 360, 340, 82
    ys = [445, 290, 135]
    names = [r"message $\varphi$", r"aggregate \raisebox{-12\px}{\scalebox{2.4}{$\bigoplus$}}", r"update $\psi$"]
    p = []
    js = [(44, 495), (44, 410), (44, 325)]
    for n, (x, y) in enumerate(js, start=1):
        p.append(N(f"j{n}", (x, y), f"$j_{n}$", 76))
    p.append(N("ni", (44, 135), "$i$", 76, "hl"))
    for n, y in enumerate(ys):
        p.append(rf"\node[draw=ink, line width=2\px, fill=white, minimum width={bw}\px, minimum height={bh}\px, "
                 rf"font=\fssmall] (b{n}) at {P(bx, y)} {{{names[n]}}};")
    for n, (x, y) in enumerate(js, start=1):
        p.append(rf"\draw[arr] {P(x + 40, y)} -- {P(bx - bw / 2 - 2, 445 + (2 - n) * 25)};")
    p.append(rf"\draw[arr] {P(86, 135)} -- {P(bx - bw / 2 - 2, 135)};")
    p.append(rf"\draw[arr] {P(bx, ys[0] - bh / 2)} -- {P(bx, ys[1] + bh / 2)};")
    p.append(rf"\draw[arr] {P(bx, ys[1] - bh / 2)} -- {P(bx, ys[2] + bh / 2)};")
    p.append(rf"\draw[arr] {P(bx, ys[2] - bh / 2)} -- {P(bx, 70)};")
    p.append(N("nh", (bx, 30), "$h_i'$", 76, "hl"))
    p.append(rf"\node[font=\fssmall, inner sep=2\px, anchor=east] at {P(bx - 46, 30)} {{new feature}};")
    for n, y in enumerate(ys, start=1):
        p.append(rf"\node[circle, fill=ink, text=white, minimum size=56\px, inner sep=0pt, font=\fssmall] "
                 rf"at {P(bx + bw / 2, y + bh / 2)} {{{n}}};")
    B("c06_mp_flow", *p)


# ---- c08 ----------------------------------------------------------------------------------------
def c08_readout():
    s = 24
    nodes = {1: (40, 400), 2: (170, 430), 3: (175, 310), 4: (40, 280), 5: (110, 170)}
    edges = [(1, 2), (2, 3), (3, 4), (4, 1), (4, 5), (3, 5), (1, 3)]
    p = [COLORS, r"\begin{scope}[on background layer]"]
    for u, v in edges:
        p.append(line(nodes[u], nodes[v], 2.5))
    p.append(r"\end{scope}")
    for i, (x, y) in nodes.items():
        p.append(N(f"v{i}", (x, y), "", 40, "white"))
        p.append(vec_row(x - 36, y - 38, vec_values(3, 30 + i), "snew", s))
    p.append(rf"\draw[ink, line width=2\px, fill=white] {P(310, 340)} circle ({0.75 * 34}bp);")
    p.append(rf"\draw[ink, line width=2\px] {P(276, 340)} -- {P(344, 340)};")
    p.append(rf"\draw[ink, line width=2\px] {P(310, 306)} -- {P(310, 374)};")
    p.append(rf"\draw[arr] {P(235, 340)} -- {P(268, 340)};")
    # graph vector
    gv = vec_values(4, 40)
    for i, v in enumerate(gv):
        p.append(square(490, 450 - 20 - i * 40, 40, "hlink", v))
    p.append(rf"\draw[arr] {P(352, 340)} -- {P(458, 340)};")
    p.append(rf"\node[draw=ink, line width=2\px, fill=white, minimum width=250\px, minimum height=70\px, font=\fssmall] "
             rf"(cl) at {P(430, 190)} {{classifier}};")
    p.append(rf"\draw[arr] {P(490, 282)} -- {P(490, 230)};")
    p.append(rf"\draw[arr] {P(430, 154)} -- {P(430, 90)};")
    p.append(T((430, 50), "class"))
    B("c08_readout", *p)


if __name__ == "__main__":
    c01_sampling_tree()
    c02_sage_concat()
    c03_concat_vs_sum()
    c04_gcn_vs_gat()
    c05_attention_visual()
    c06_mp_flow()
    c08_readout()

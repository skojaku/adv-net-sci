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
    pos = {"t": (105, 298), "a": (52, 192), "b": (157, 192), "c": (45, 390), "d": (165, 390),
           "e": (25, 80), "f": (78, 80), "g": (20, 247), "h": (130, 80), "i": (183, 80),
           "j": (190, 247), "k": (45, 496)}
    solid = [("t", "a"), ("t", "b"), ("a", "e"), ("a", "f"), ("b", "h"), ("b", "i")]
    dashed = [("t", "c"), ("t", "d"), ("a", "g"), ("b", "j"), ("c", "k")]
    fills = {"t": "hl", "a": "hopa", "b": "hopa", "e": "hopb", "f": "hopb", "h": "hopb", "i": "hopb"}
    ns = 34
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
    p.append(rf"\node[tag, anchor=north] at {P(95, 42)} {{uniform sample}};")
    # tree
    rows = {"target": 500, "hop 1": 290, "hop 2": 80}
    tx = {"t": 403, "a": 353, "b": 453, "e": 328, "f": 378, "h": 428, "i": 478}
    ty = {"t": 500, "a": 290, "b": 290, "e": 80, "f": 80, "h": 80, "i": 80}
    ts = 40
    tedges = [("t", "a"), ("t", "b"), ("a", "e"), ("a", "f"), ("b", "h"), ("b", "i")]
    p.append(r"\begin{scope}[on background layer]")
    for u, v in tedges:
        p.append(line((tx[u], ty[u]), (tx[v], ty[v]), 2.5))
    p.append(r"\end{scope}")
    for k in tx:
        p.append(N(f"r{k}", (tx[k], ty[k]), "", ts, fills[k]))
    for nm, y in rows.items():
        p.append(rf"\node[font=\fssmall, inner sep=2\px, anchor=west] at {P(206, y)} {{{nm}}};")
    for y0, y1 in ((80, 290), (290, 500)):
        ym = (y0 + y1) / 2
        p.append(rf"\draw[arr] {P(504, y0 + 25)} -- {P(504, y1 - 25)};")
        p.append(rf"\node[font=\fssmall, inner sep=2\px, anchor=west] at {P(516, ym)} {{aggregate}};")
    B("c01_sampling_tree", *p)


# ---- c02 ----------------------------------------------------------------------------------------
def c02_sage_concat():
    s = 50
    cy = 200
    a = vec_values(4, 1)
    b = vec_values(4, 2)
    p = [COLORS]
    p.append(vec_col(30, cy + 2 * s, a, "snew", s))
    p.append(vec_col(185, cy + 2 * s, b, "sbase", s))
    for dx in (-7, 7):
        p.append(rf"\draw[ink, line width=3\px] {P(107 + dx, cy - 32)} -- {P(107 + dx, cy + 32)};")
    p.append(T((30, cy - 2 * s - 38), "self"))
    p.append(T((185, cy - 2 * s - 55), r"neighbours\\(mean)"))
    p.append(vec_col(310, cy + 4 * s, a, "snew", s))
    p.append(vec_col(310, cy, b, "sbase", s))
    p.append(rf"\draw[arr] {P(220, cy)} -- {P(275, cy)};")
    p.append(rf"\node[smallbox, minimum width=66\px, minimum height=66\px, font=\fslarge] (W) at {P(410, cy)} {{$W$}};")
    p.append(rf"\draw[arr] {P(340, cy)} -- {P(373, cy)};")
    c = vec_values(4, 3)
    p.append(rf"\draw[arr] {P(448, cy)} -- {P(490, cy)};")
    for i, v in enumerate(c):
        p.append(square(520, cy + 2 * s - s / 2 - i * s, s, "hlink", v))
    p.append(T((520, cy - 2 * s - 38), "new"))
    B("c02_sage_concat", *p)


# ---- c03 ----------------------------------------------------------------------------------------
def c03_concat_vs_sum():
    s = 30
    a = vec_values(3, 11)
    b = vec_values(3, 12)
    centres = (113.5, 486.5)
    ny, fy = 400, 480
    p = []
    for k, c in enumerate(centres):
        xu, xv = c - 65, c + 65
        va, vb = (a, b) if k == 0 else (b, a)
        ca, cb = ("snew", "sbase") if k == 0 else ("sbase", "snew")
        p.append(line((xu, ny), (xv, ny), 3))
        p.append(N(f"u{k}", (xu, ny), "$u$", 56, "hl"))
        p.append(N(f"v{k}", (xv, ny), "$v$", 56))
        p.append(vec_row(xu - 45, fy, va, ca, s))
        p.append(vec_row(xv - 45, fy, vb, cb, s))
        # sum: three squares, each half blue half vermillion
        for i in range(3):
            x = c - 45 + s / 2 + i * s
            ys = 255
            p.append(rf"\fill[snew] {P(x - s / 2, ys)} rectangle {P(x + s / 2, ys + s / 2)};")
            p.append(rf"\fill[sbase] {P(x - s / 2, ys - s / 2)} rectangle {P(x + s / 2, ys)};")
            p.append(rf"\draw[ink, line width=2\px] {P(x - s / 2, ys - s / 2)} rectangle {P(x + s / 2, ys + s / 2)};")
        # concat [a | b] or [b | a]
        first = (va, ca) if k == 0 else (vb, cb)
        second = (vb, cb) if k == 0 else (va, ca)
        # same vectors as above: case 1 -> [a | b], case 2 -> [b | a]
        left = c - 100
        p.append(vec_row(left, 80, first[0], first[1], s))
        p.append(vec_row(left + 3 * s + 14, 80, second[0], second[1], s))
        p.append(rf"\draw[ink, line width=2\px] {P(left + 3 * s + 7, 80 - 21)} -- {P(left + 3 * s + 7, 80 + 21)};")
    # middle column
    p.append(T((300, 280), "sum"))
    p.append(rf"\node[tag] at {P(300, 230)} {{same}};")
    p.append(T((300, 105), "concat"))
    p.append(rf"\node[tag] at {P(300, 55)} {{different}};")
    B("c03_concat_vs_sum", *p)


# ---- c04 ----------------------------------------------------------------------------------------
def c04_gcn_vs_gat():
    deg_j = [2, 3, 3, 4, 4]
    d_i = 5
    gcn = [1 / math.sqrt((d_i + 1) * (d + 1)) for d in deg_j]
    gat = [0.45, 0.25, 0.15, 0.10, 0.05]
    k = 31.0
    cols = ["snew", "sbase", "sthree", "sfour", "sfive"]
    rx, ry = 124, 175
    p = []
    for name, cx, ws in (("GCN", 170, gcn), ("GAT", 530, gat)):
        cy = 195
        p.append(rf"\node[font=\fslarge, inner sep=2\px] at {P(cx, 470)} {{{name}}};")
        pts = []
        for i in range(5):
            ang = math.radians(90 + 72 * i)
            pts.append((cx + rx * math.cos(ang), cy + ry * math.sin(ang)))
        for (x, y), w in zip(pts, ws):
            p.append(line((cx, cy), (x, y), max(2, w * k)))
        p.append(N(f"c{name}", (cx, cy), "$i$", 56, "hl"))
        for (x, y), c in zip(pts, cols):
            p.append(N(f"n{name}{x:.0f}", (x, y), "", 46, c))
    B("c04_gcn_vs_gat", *p)


# ---- c05 ----------------------------------------------------------------------------------------
def c05_attention_visual():
    e = np.array([1.2, 0.1, -0.5])
    alpha = np.exp(e) / np.exp(e).sum()
    ys = [350, 215, 80]
    cols = ["snew", "sbase", "sthree"]
    p = [rf"\begin{{scope}}[on background layer]"]
    for y, al in zip(ys, alpha):
        p.append(line((35, 215), (190, y), al * 20))
    p.append(r"\end{scope}")
    p.append(N("ci", (35, 215), "$i$", 52, "hl"))
    # softmax box
    p.append(rf"\node[draw=ink, line width=2\px, fill=white, minimum width=124\px, minimum height=390\px, "
             rf"font=\fssmall] at {P(467, 215)} {{softmax}};")
    for j, (y, ej, al, c) in enumerate(zip(ys, e, alpha, cols), start=1):
        p.append(N(f"cj{j}", (190, y), f"$j_{j}$", 52))
        vals = vec_values(3, 20 + j)
        p.append(vec_col(250, y + 45, vals, c, 30))
        txt = f"${ej:.1f}$".replace("-", "{-}")
        p.append(T((345, y), txt))
        p.append(rf"\draw[arr] {P(380, y)} -- {P(403, y)};")
        p.append(rf"\draw[arr] {P(533, y)} -- {P(561, y)};")
        p.append(T((600, y), f"${al:.2f}$"))
    p.append(rf"\node[tag, align=center] at {P(345, 462)} {{scores\\$e_{{ij}}$}};")
    p.append(rf"\node[tag, align=center] at {P(595, 462)} {{weights $\alpha_{{ij}}$\\(sum to 1)}};")
    B("c05_attention_visual", *p)


# ---- c06 ----------------------------------------------------------------------------------------
def c06_mp_flow():
    bx, bw, bh = 340, 290, 82
    ys = [445, 290, 135]
    names = [r"message $\varphi$", r"aggregate $\bigoplus$", r"update $\psi$"]
    p = []
    # neighbours (left, top) and i (left, bottom)
    js = [(40, 490), (40, 415), (40, 340)]
    for n, (x, y) in enumerate(js, start=1):
        p.append(N(f"j{n}", (x, y), f"$j_{n}$", 56))
    p.append(N("ni", (40, 135), "$i$", 56, "hl"))
    for n, y in enumerate(ys):
        p.append(rf"\node[draw=ink, line width=2\px, fill=white, minimum width={bw}\px, minimum height={bh}\px, "
                 rf"font=\fssmall] (b{n}) at {P(bx, y)} {{{names[n]}}};")
    for n, (x, y) in enumerate(js, start=1):
        p.append(rf"\draw[arr] {P(x + 30, y)} -- {P(bx - bw / 2 - 2, 445 + (2 - n) * 25)};")
    p.append(rf"\draw[arr] {P(70, 135)} -- {P(bx - bw / 2 - 2, 135)};")
    p.append(rf"\draw[arr] {P(bx, ys[0] - bh / 2)} -- {P(bx, ys[1] + bh / 2)};")
    p.append(rf"\draw[arr] {P(bx, ys[1] - bh / 2)} -- {P(bx, ys[2] + bh / 2)};")
    p.append(rf"\draw[arr] {P(bx, ys[2] - bh / 2)} -- {P(bx, 70)};")
    p.append(N("nh", (bx, 40), "$h_i'$", 56, "hl"))
    p.append(rf"\node[font=\fssmall, inner sep=2\px, anchor=west] at {P(bx + 45, 40)} {{new feature}};")
    for n, y in enumerate(ys, start=1):
        p.append(rf"\node[circle, fill=ink, text=white, minimum size=46\px, inner sep=0pt, font=\fssmall] "
                 rf"at {P(bx - bw / 2, y + bh / 2)} {{{n}}};")
    B("c06_mp_flow", *p)


# ---- c07 ----------------------------------------------------------------------------------------
def c07_three_models_mini():
    k = 24.0
    ns, cs = 40, 48
    d_i = 4
    deg_j = [2, 3, 3, 4]
    gcn = [1 / math.sqrt((d_i + 1) * (d + 1)) for d in deg_j]
    gat = [0.50, 0.25, 0.15, 0.10]
    offs = [(-85, 52), (85, 52), (-85, -52), (85, -52)]
    names = ["GCN", "GraphSAGE", "GAT"]
    p = []
    for idx, nm in enumerate(names):
        y0 = 538 - 168 * (idx + 1) - 15 * idx     # bottom of the panel
        cx, cy = 315, y0 + 84
        p.append(rf"\draw[ink, line width=2\px] {P(3, y0)} rectangle {P(437, y0 + 168)};")
        p.append(rf"\node[font=\fssmall, inner sep=2\px, anchor=west] at {P(12, cy)} {{{nm}}};")
        if nm == "GCN":
            ws, dash = gcn, [False] * 4
        elif nm == "GAT":
            ws, dash = gat, [False] * 4
        else:
            ws, dash = [0.5, 0.5, 0.5, 0.5], [False, False, True, True]
        for (dx, dy), w, d in zip(offs, ws, dash):
            if d:
                p.append(line((cx, cy), (cx + dx, cy + dy), 2, "muted", dash=True))
            else:
                p.append(line((cx, cy), (cx + dx, cy + dy), max(2, w * k)))
        p.append(N(f"m{idx}c", (cx, cy), "", cs, "hl"))
        for n, ((dx, dy), d) in enumerate(zip(offs, dash)):
            if d:
                p.append(N(f"m{idx}n{n}", (cx + dx, cy + dy), "", ns, "white", extra="draw=muted"))
            else:
                p.append(N(f"m{idx}n{n}", (cx + dx, cy + dy), "", ns, "white"))
    B("c07_three_models_mini", *p)


# ---- c08 ----------------------------------------------------------------------------------------
def c08_readout():
    s = 22
    nodes = {1: (40, 360), 2: (170, 390), 3: (175, 270), 4: (40, 240), 5: (110, 130)}
    edges = [(1, 2), (2, 3), (3, 4), (4, 1), (4, 5), (3, 5), (1, 3)]
    p = [COLORS, r"\begin{scope}[on background layer]"]
    for u, v in edges:
        p.append(line(nodes[u], nodes[v], 2.5))
    p.append(r"\end{scope}")
    for i, (x, y) in nodes.items():
        p.append(N(f"v{i}", (x, y), "", 40, "white"))
        p.append(vec_row(x - 33, y - 38, vec_values(3, 30 + i), "snew", s))
    p.append(rf"\draw[ink, line width=2\px, fill=white] {P(290, 300)} circle ({0.75 * 30}bp);")
    p.append(rf"\draw[ink, line width=2\px] {P(260, 300)} -- {P(320, 300)};")
    p.append(rf"\draw[ink, line width=2\px] {P(290, 270)} -- {P(290, 330)};")
    p.append(rf"\draw[arr] {P(215, 300)} -- {P(252, 300)};")
    p.append(T((290, 205), r"sum\\mean\\max"))
    # graph vector
    gv = vec_values(4, 40)
    for i, v in enumerate(gv):
        p.append(square(480, 372 - 18 - i * 36, 36, "hlink", v))
    p.append(rf"\draw[arr] {P(328, 300)} -- {P(448, 300)};")
    p.append(rf"\node[draw=ink, line width=2\px, fill=white, minimum width=160\px, minimum height=60\px, font=\fssmall] "
             rf"(cl) at {P(480, 150)} {{classifier}};")
    p.append(rf"\draw[arr] {P(480, 224)} -- {P(480, 182)};")
    p.append(rf"\draw[arr] {P(480, 118)} -- {P(480, 70)};")
    p.append(T((480, 40), "class"))
    B("c08_readout", *p)


if __name__ == "__main__":
    c01_sampling_tree()
    c02_sage_concat()
    c03_concat_vs_sum()
    c04_gcn_vs_gat()
    c05_attention_visual()
    c06_mp_flow()
    c07_three_models_mini()
    c08_readout()

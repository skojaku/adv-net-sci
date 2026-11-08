"""Group e: spectral view.  Run from slides/m09:
    uv run --quiet --with numpy --with scipy --with networkx --with pillow --with scikit-image python figures/fig_e.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import *  # noqa: E402,F403

import networkx as nx  # noqa: E402
import numpy as np  # noqa: E402

LAV = ["#9B6BC9", "#B88AE0", "#D9B8F5", "#F4E6FF"]   # hop 0 (darkest) .. hop 3 (lightest)
GREYL = "#C9C9C9"


# ---------------------------------------------------------------- helpers
def hx(c: str):
    c = c.lstrip("#")
    return np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], float)


def rgbs(c) -> str:
    c = hx(c) if isinstance(c, str) else c
    return "{rgb,255:red,%d;green,%d;blue,%d}" % tuple(int(round(v)) for v in c)


def mix(c0, c1, t):
    t = float(np.clip(t, 0, 1))
    return (1 - t) * hx(c0) + t * hx(c1)


def seq(t):                      # white -> blue
    return mix("#FFFFFF", BLUE, t)


def div(v):                      # -1..1 : vermillion - white - blue
    return mix("#FFFFFF", BLUE, v) if v >= 0 else mix("#FFFFFF", VERM, -v)


def vtx(name, at, size, fill="#FFFFFF", text="", extra=""):
    ex = f"fill={rgbs(fill)}" + (f", {extra}" if extra else "")
    return vertex(name, at, text, size=size, extra=ex)


def eg(a, b, style="draw=" + "rule", text=None, lw=None):
    st = style + (f", line width={lw}\\px" if lw else "")
    if text is None:
        return f"\\draw[edge, {st}] ({a}) -- ({b});"
    return (f"\\draw[edge, {st}] ({a}) -- ({b}) node[midway, fill=white, inner sep=2\\px, "
            f"font=\\fssmall, text=snew] {{{text}}};")


def curve(pts, style="draw=ink, line width=2.5\\px"):
    s = " ".join(P(x, y) for x, y in pts)
    return f"\\draw[{style}] plot[smooth, tension=0.6] coordinates {{{s}}};"


def poly(pts, style="draw=ink, line width=2.5\\px"):
    return f"\\draw[{style}] " + " -- ".join(P(x, y) for x, y in pts) + ";"


def axes(x0, y0, w, h, style="line width=1.5\\px"):
    ar = "-{Stealth[length=7bp, width=6bp]}"
    return (f"\\draw[{ar}, {style}] {P(x0, y0)} -- {P(x0 + w, y0)};\n"
            f"\\draw[{ar}, {style}] {P(x0, y0)} -- {P(x0, y0 + h)};")


def lap(G):
    A = nx.to_numpy_array(G, nodelist=sorted(G.nodes()), weight=None)
    return np.diag(A.sum(1)) - A, A


def karate_spectral():
    G = nx.karate_club_graph()
    L, A = lap(G)
    lam, U = np.linalg.eigh(L)
    return G, L, A, lam, U


# ---------------------------------------------------------------- e01
def e01_khop():
    pos = {0: (270, 250), 1: (270, 345), 2: (160, 250), 3: (380, 250), 4: (270, 150),
           5: (165, 425), 6: (375, 425), 7: (50, 320), 8: (150, 110), 9: (490, 320), 10: (400, 100),
           11: (55, 465), 12: (490, 450), 13: (570, 375), 14: (530, 160), 15: (45, 150)}
    pos = {v: (x, 28 + (y - 100) * 436 / 365) for v, (x, y) in pos.items()}
    E = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 5), (1, 6), (5, 6), (2, 7), (2, 8), (4, 8), (3, 9),
         (3, 10), (4, 10), (5, 11), (6, 12), (9, 13), (12, 13), (10, 14), (8, 15)]
    G = nx.Graph(E)
    hop = nx.single_source_shortest_path_length(G, 0)
    cnt = [sum(1 for v in hop.values() if v == k) for k in range(4)]
    assert cnt == [1, 4, 6, 5], cnt
    parts = []
    for v, p in pos.items():
        parts.append(vtx(f"v{v}", p, 52, LAV[hop[v]]))
    parts.append("\\begin{scope}[on background layer]")
    parts += [eg(f"v{a}", f"v{b}", "draw=ink") for a, b in E]
    parts.append("\\end{scope}")
    # theta_k tag next to a representative node of hop k, joined by a short leader
    tagpos = {0: (338, 150), 1: (175, 330), 2: (485, 368), 3: (530, 172)}
    reps = {0: 0, 1: 1, 2: 9, 3: 14}
    for k, t in tagpos.items():
        parts.append(f"\\node[tag] (t{k}) at {P(*t)} {{$\\theta_{k}$}};")
    for k, t in tagpos.items():
        parts.append(f"\\draw[lead] (t{k}) -- (v{reps[k]});")
    parts.append(f"\\node[font=\\fsbody, anchor=south west, inner sep=2\\px] at {P(2, 4)} {{$K=3$}};")
    return B("e01_khop", *parts)


# ---------------------------------------------------------------- e02
def e02_laplacian_diff():
    pos = {1: (40, 380), 2: (40, 110), 3: (300, 250), 4: (580, 380), 5: (570, 100), 6: (390, 40)}
    x = {1: 8, 2: 1, 3: 6, 4: 3, 5: 3, 6: 4}
    E = [(1, 2), (1, 3), (1, 4), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
    parts = []
    for v, p in pos.items():
        parts.append(vtx(f"v{v}", p, 52, HL if v == 1 else "#FFFFFF", text=f"${x[v]}$"))
    parts.append("\\begin{scope}[on background layer]")
    for a, b in E:
        d = x[a] - x[b]
        parts.append(eg(f"v{a}", f"v{b}", "draw=ink" if a == 1 else "draw=muted", text=f"${d}$"))
    parts.append("\\end{scope}")
    diffs = [x[1] - x[b] for a, b in E if a == 1 for b in [b]]
    Lx1 = sum(diffs)
    s = "+".join(str(d) for d in diffs)
    parts.append(f"\\node[tag, anchor=south west, fill=hl] (call) at {P(10, 452)} {{$(Lx)_1 = {s} = {Lx1}$}};")
    parts.append("\\draw[lead] (call.south west) ++(30bp,0) -- (v1);")
    return B("e02_laplacian_diff", *parts)


# ---------------------------------------------------------------- e03
def e03_eigvecs_karate():
    G, L, A, lam, U = karate_spectral()
    pos, edges, _ = karate_layout(334, 228, seed=4, margin=14)
    panels = [(0, "$\\lambda_1 = 0$"), (1, None), (9, None), (33, None)]
    names = {0: 1, 1: 2, 9: 10, 33: 34}
    W, H, LAB = 334, 228, 40
    parts = []
    for pi, (k, _) in enumerate(panels):
        col, row = pi % 2, pi // 2
        ox = col * (W + 20)
        oy = (1 - row) * (H + LAB + 10)
        u = U[:, k].copy()
        if k == 0:
            u = np.abs(u)
        else:
            i = int(np.argmax(np.abs(u)))
            u *= np.sign(u[i])
        m = np.abs(u).max()
        lv = "0" if abs(lam[k]) < 1e-9 else f"{lam[k]:.2f}"
        lamtxt = f"$\\lambda_{{{names[k]}}} = {lv}$"
        for v, (px, py) in pos.items():
            parts.append(vtx(f"p{pi}v{v}", (ox + px, oy + LAB + py), 26, div(u[v - 1] / m),
                             extra="line width=1.5\\px"))
        parts.append("\\begin{scope}[on background layer]")
        parts += [eg(f"p{pi}v{a}", f"p{pi}v{b}", "draw=rule") for a, b in edges]
        parts.append("\\end{scope}")
        parts.append(label((ox + W / 2, oy + LAB / 2 - 2), lamtxt, size="fssmall"))
    return B("e03_eigvecs_karate", *parts)


# ---------------------------------------------------------------- e04
def e04_spectral_conv_flow():
    n = 8
    G = nx.path_graph(n)
    L, A = lap(G)
    lam, U = np.linalg.eigh(L)
    rng = np.random.default_rng(3)
    x = rng.uniform(-1, 1, n)
    xh = U.T @ x
    g = np.exp(-lam)
    gx = g * xh
    y = U @ gx
    rows = [x, xh, gx, y]
    unit = 26 / max(np.abs(r).max() for r in rows)
    names = ["$\\bm x$", "$\\hat{\\bm x}$", "$g(\\Lambda)\\hat{\\bm x}$", "$\\bm y$"]
    H0, GAP = 56, 98
    X0, STEP = 118, 68
    xc = X0 + 3.5 * STEP
    ys = [GAP * 0 + H0 / 2 + (3 - i) * (H0 + GAP) for i in range(4)]
    parts = []
    for i, r in enumerate(rows):
        yc = ys[i]
        parts.append(f"\\draw[line width=1.2\\px, draw=muted] {P(X0 - 20, yc)} -- {P(X0 + 7 * STEP + 20, yc)};")
        for j, v in enumerate(r):
            col = "ink" if i in (0, 3) else "snew"
            parts.append(f"\\fill[{col}] {P(X0 + j * STEP, yc + v * unit)} circle (6.5\\px);")
        parts.append(f"\\node[anchor=east, font=\\fssmall, inner sep=2\\px] at {P(X0 - 28, yc)} {{{names[i]}}};")
    boxes = [r"$U^{\top}$", r"$\times\, g(\lambda)$", r"$U$"]
    for i, t in enumerate(boxes):
        ya, yb = ys[i] - H0 / 2 - 6, ys[i + 1] + H0 / 2 + 6
        ym = (ya + yb) / 2
        parts.append(node(f"b{i}", (xc, ym), t, style="smallbox", w=150 if i == 1 else 90, h=52))
        parts.append(arrow((xc, ya), f"(b{i}.north)"))
        parts.append(arrow(f"(b{i}.south)", (xc, yb)))
    # g(lambda) curve beside the second box
    cx0, cy0, cw, ch = 450, 0, 100, 56
    ym = (ys[1] - H0 / 2 - 6 + ys[2] + H0 / 2 + 6) / 2
    cy0 = ym - ch / 2
    parts.append(axes(cx0, cy0, cw, ch + 6))
    ls = np.linspace(0, lam.max(), 30)
    parts.append(curve([(cx0 + l / lam.max() * (cw - 8), cy0 + np.exp(-l) * ch) for l in ls],
                       "draw=snew, line width=3\\px"))
    parts.append(f"\\node[anchor=west, font=\\fssmall, inner sep=2\\px] at {P(cx0 + cw + 2, cy0 + 4)} {{$\\lambda$}}; ")
    return B("e04_spectral_conv_flow", *parts)


# ---------------------------------------------------------------- e05
def e05_nested_models():
    from scipy.interpolate import CubicSpline
    lam = np.linspace(0, 2, 40)
    kx = np.linspace(0, 2, 6)
    free = CubicSpline(kx, [0.85, 0.3, 0.75, 0.45, 0.9, 0.4])(lam)          # free-form g(lambda)
    poly3 = np.polyval(np.polyfit(lam, 1 / (1 + (lam / 0.8) ** 3), 3), lam)  # degree-3 polynomial
    line = 1 - lam                                                            # GCN
    parts = []

    def box(x0, y0, x1, y1, fill):
        return f"\\draw[line width=2\\px, rounded corners=14\\px, fill={fill}] {P(x0, y0)} rectangle {P(x1, y1)};"

    parts.append(box(0, 0, 634, 514, "white"))
    parts.append(box(18, 18, 470, 440, "hl"))
    parts.append(box(36, 36, 316, 330, "white"))

    def lab_(x, y, t):
        return f"\\node[anchor=north west, font=\\fsbody, inner sep=2\\px] at {P(x, y)} {{{t}}};"

    parts.append(lab_(16, 510, "spectral conv"))
    parts.append(lab_(34, 436, "ChebNet"))
    parts.append(lab_(52, 326, "GCN"))

    CW, CH = 92, 120

    def plot_curve(x0, y0, f, ymin, ymax, col="ink"):
        z = (0 - ymin) / (ymax - ymin) * CH            # height of the lambda axis
        ar = "-{Stealth[length=7bp, width=6bp]}"
        out = [f"\\draw[{ar}, line width=1.5\\px] {P(x0, y0 + z)} -- {P(x0 + CW + 12, y0 + z)};",
               f"\\draw[{ar}, line width=1.5\\px] {P(x0, y0)} -- {P(x0, y0 + CH + 8)};"]
        pts = [(x0 + (l / 2) * CW, y0 + (v - ymin) / (ymax - ymin) * CH) for l, v in zip(lam, f)]
        out.append(curve(pts, f"draw={col}, line width=3.5\\px"))
        out.append(f"\\node[anchor=west, font=\\fssmall, inner sep=1\\px] at {P(x0 + CW + 14, y0 + z)} {{$\\lambda$}};")
        return "\n".join(out)

    parts.append(plot_curve(484, 200, free, 0, 1))
    parts.append(plot_curve(330, 165, poly3, -0.1, 1.1))
    parts.append(plot_curve(176, 120, line, -1, 1))
    parts.append(f"\\node[anchor=east, font=\\fssmall, inner sep=1\\px] at {P(166, 220)} {{$1-\\lambda$}};")
    return B("e05_nested_models", *parts)


# ---------------------------------------------------------------- e06
def _centrality_parts():
    G, L, A, lam, U = karate_spectral()
    c = nx.eigenvector_centrality_numpy(G, weight=None)
    x = np.array([c[i] for i in range(34)])
    x = x / np.abs(x).max()
    Uk = U[:, :5]
    low = Uk @ (Uk.T @ x)
    high = x - low
    return G, x, low, high


def e06_masks_karate():
    G, x, low, high = _centrality_parts()
    W, H, LAB = 224, 236, 44
    pos, edges, _ = karate_layout(W, H, seed=4, margin=14)
    mx = x.max()
    mh = np.abs(high).max()
    cols = [[seq(v / mx) for v in x], [seq(v / mx) for v in low], [div(v / mh) for v in high]]
    names = ["$\\bm x$", "low", "high"]
    parts = []
    for pi in range(3):
        ox = pi * (W + 14)
        for v, (px, py) in pos.items():
            parts.append(vtx(f"p{pi}v{v}", (ox + px, LAB + py), 20, cols[pi][v - 1], extra="line width=1.5\\px"))
        parts.append("\\begin{scope}[on background layer]")
        parts += [eg(f"p{pi}v{a}", f"p{pi}v{b}", "draw=rule", lw=1.2) for a, b in edges]
        parts.append("\\end{scope}")
        parts.append(label((ox + W / 2, LAB / 2 - 2), names[pi], size="fssmall"))
    return B("e06_masks_karate", *parts)


# ---------------------------------------------------------------- e07
def e07_highfreq_boundary():
    G, x, low, high = _centrality_parts()
    W, H = 690, 470
    pos, edges, club = karate_layout(W, H, seed=4, margin=26)
    mag = np.abs(high)
    t = mag / mag.max()
    cross = [(a, b) for a, b in edges if club[a] != club[b]]
    cd = {v: sum(1 for e in cross if v in e) for v in pos}
    big = 3                       # a large node with the most boundary edges (4)
    parts = []
    for v, p in pos.items():
        parts.append(vtx(f"v{v}", p, 14 + 34 * t[v - 1], seq(t[v - 1]), extra="line width=1.5\\px"))
    parts.append("\\begin{scope}[on background layer]")
    for a, b in edges:
        if (a, b) in cross:
            parts.append(eg(f"v{a}", f"v{b}", "draw=ink", lw=5))
        else:
            parts.append(eg(f"v{a}", f"v{b}", "draw=rule", lw=1.4))
    parts.append("\\end{scope}")
    CALL = (pos[big][0] - 230, pos[big][1] - 70)
    parts.append(f"\\node[tag, fill=white] (call) at {P(*CALL)} {{boundary}};")
    parts.append(f"\\draw[arr] (call) -- (v{big});")
    return B("e07_highfreq_boundary", *parts), big, pos, cross, mag


# ---------------------------------------------------------------- e08
def e08_summary_visuals():
    FW, FH, GAP = 374, 170, 14
    parts = []
    fy = [2 * (FH + GAP), (FH + GAP), 0]
    for y in fy:
        parts.append(f"\\draw[line width=2\\px, fill=white] {P(0, y)} rectangle {P(FW, y + FH)};")
    # (1) convolution
    y0 = fy[0]
    cs = 25
    gx0, gy0 = 34, y0 + 52
    rng = np.random.default_rng(1)
    for i in range(4):
        for j in range(4):
            inwin = i < 3 and j < 3
            g = 255 - int(rng.integers(0, 90)) if not inwin else None
            fillc = "hl" if inwin else rgbs(np.array([g, g, g], float))
            parts.append(f"\\draw[line width=1.5\\px, fill={fillc if inwin is False else 'hl'}] "
                         f"{P(gx0 + j * cs, gy0 + (3 - i) * cs)} rectangle {P(gx0 + (j + 1) * cs, gy0 + (4 - i) * cs)};")
    parts.append(f"\\draw[line width=3\\px] {P(gx0, gy0 + cs)} rectangle {P(gx0 + 3 * cs, gy0 + 4 * cs)};")
    parts.append(arrow((gx0 + 4 * cs + 14, gy0 + 2 * cs), (gx0 + 4 * cs + 70, gy0 + 2 * cs)))
    gp = {0: (250, y0 + 100), 1: (310, y0 + 125), 2: (320, y0 + 72), 3: (265, y0 + 55), 4: (195, y0 + 0 + 0)}
    gp = {1: (285, y0 + 100), 2: (345, y0 + 125), 3: (350, y0 + 70), 4: (310, y0 + 52), 5: (230, y0 + 78)}
    for v, p in gp.items():
        parts.append(vtx(f"s1v{v}", p, 26, HL if v == 1 else "#FFFFFF"))
    for a, b in [(1, 2), (1, 3), (1, 4), (1, 5), (4, 3)]:
        parts.append(eg(f"s1v{a}", f"s1v{b}", "draw=ink", lw=1.5))
    parts.append(label((FW / 2, y0 + 22), "convolution", size="fssmall"))
    # (2) message passing
    y0 = fy[1]
    cx, cy = 255, y0 + 100
    nb = [(120, y0 + 128), (120, y0 + 72), (255, y0 + 128 + 0)]
    nb = [(110, y0 + 130), (110, y0 + 70), (255, y0 + 138)]
    nb = [(100, y0 + 130), (100, y0 + 70), (255, y0 + 140)]
    parts.append(vtx("s2c", (cx - 40, cy - 8), 40, HL))
    ctr = (cx - 40, cy - 8)
    nbs = [(70, y0 + 135), (70, y0 + 70), (190, y0 + 150), (320, y0 + 70)]
    nbs = [(60, y0 + 135), (60, y0 + 65), (150, y0 + 150), (150, y0 + 52)]
    for i, p in enumerate(nbs):
        parts.append(vtx(f"s2n{i}", p, 28))
    parts.append(label((FW / 2, y0 + 22), "message passing", size="fssmall"))
    # (3) low-pass filter
    y0 = fy[2]
    cx0, cy0, cw, ch = 60, y0 + 74, 250, 70
    parts.append(axes(cx0, cy0, cw + 14, ch + 6))
    ls = np.linspace(0, 1, 40)
    gcurve = lambda l: 1 / (1 + (l / 0.38) ** 4)  # noqa: E731
    parts.append(curve([(cx0 + l * cw, cy0 + gcurve(l) * ch) for l in ls], "draw=snew, line width=3\\px"))
    lamp = np.linspace(0.08, 0.92, 6)
    for l in lamp:
        parts.append(f"\\fill[ink] {P(cx0 + l * cw, cy0)} circle (6\\px);")
        parts.append(f"\\fill[snew] {P(cx0 + l * cw, cy0 + gcurve(l) * ch)} circle (5\\px);")
        parts.append(f"\\draw[line width=1.2\\px, draw=muted] {P(cx0 + l * cw, cy0)} -- {P(cx0 + l * cw, cy0 + gcurve(l) * ch)};")
    parts.append(label((FW / 2, y0 + 22), "low-pass filter", size="fssmall"))
    return parts


def _e08():
    parts = e08_summary_visuals()
    # arrows into the message-passing centre need names defined; add after nodes
    y0 = 1 * (170 + 14)
    ctr = "s2c"
    for i in range(4):
        parts.append(f"\\draw[arr] (s2n{i}) -- ({ctr});")
    return B("e08_summary_visuals", *parts)


if __name__ == "__main__":
    e01_khop()
    e02_laplacian_diff()
    e03_eigvecs_karate()
    e04_spectral_conv_flow()
    e05_nested_models()
    e06_masks_karate()
    r = e07_highfreq_boundary()
    _e08()
    print("e07 biggest node:", r[1], "cross edges:", len(r[3]))

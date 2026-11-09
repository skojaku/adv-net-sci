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
        parts.append(vtx(f"v{v}", p, 40, LAV[hop[v]]))
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
    return B("e01_khop", *parts)


# ---------------------------------------------------------------- e02
def e02_laplacian_diff():
    pos = {1: (60, 135), 2: (60, 500), 3: (310, 320), 4: (560, 135), 5: (570, 420), 6: (400, 555)}
    x = {1: 8, 2: 1, 3: 6, 4: 3, 5: 3, 6: 4}
    E = [(1, 2), (1, 3), (1, 4), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
    parts = []
    for v, p in pos.items():
        parts.append(vtx(f"v{v}", p, 66, HL if v == 1 else "#FFFFFF", text=f"${x[v]}$"))
    parts.append("\\begin{scope}[on background layer]")
    for a, b in E:
        d = x[a] - x[b]
        parts.append(eg(f"v{a}", f"v{b}", "draw=ink" if a == 1 else "draw=muted", text=f"${d}$"))
    parts.append("\\end{scope}")
    diffs = [x[1] - x[b] for a, b in E if a == 1]
    Lx1 = sum(diffs)
    s = "+".join(str(d) for d in diffs)
    parts.append(f"\\node[tag, anchor=south west, fill=hl] (call) at {P(4, 6)} {{$(Lx)_i = {s} = {Lx1}$}};")
    parts.append("\\draw[lead] (call.north west) ++(40bp,0) -- (v1);")
    parts.append(f"\\node[anchor=east, font=\\fssmall, inner sep=1\\px] at {P(60 - 37, 135)} {{$i$}};")
    return B("e02_laplacian_diff", *parts)


# ---------------------------------------------------------------- e03
def e03_eigvecs_karate():
    G, L, A, lam, U = karate_spectral()
    W, H, LAB, GX = 320, 236, 58, 20
    pos, edges, _ = karate_layout(W, H, seed=4, margin=16)
    ks = [0, 1, 9, 33]
    names = {0: 1, 1: 2, 9: 10, 33: 34}
    parts = []
    for pi, k in enumerate(ks):
        col, row = pi % 2, pi // 2
        ox = col * (W + GX)
        oy = (1 - row) * (H + LAB + 6)
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
            parts.append(vtx(f"p{pi}v{v}", (ox + px, oy + py), 24, div(u[v - 1] / m),
                             extra="line width=1.5\\px"))
        parts.append("\\begin{scope}[on background layer]")
        parts += [eg(f"p{pi}v{a}", f"p{pi}v{b}", "draw=rule", lw=1.5) for a, b in edges]
        parts.append("\\end{scope}")
        parts.append(label((ox + W / 2, oy + H + LAB / 2 + 2), lamtxt, size="fssmall"))
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
    unit = 21 / max(np.abs(r).max() for r in rows)
    names = ["$\\bm x$", "$\\hat{\\bm x}$", "$g(\\Lambda)\\hat{\\bm x}$", "$\\bm y$"]
    H0, GAP = 52, 120
    X0, STEP = 262, 50
    xc = X0 + 3.5 * STEP
    ys = [H0 / 2 + (3 - i) * (H0 + GAP) for i in range(4)]
    parts = []
    for i, r in enumerate(rows):
        yc = ys[i]
        parts.append(f"\\draw[line width=1.2\\px, draw=muted] {P(X0 - 20, yc)} -- {P(X0 + 7 * STEP + 20, yc)};")
        for j, v in enumerate(r):
            col = "ink" if i in (0, 3) else "snew"
            parts.append(f"\\fill[{col}] {P(X0 + j * STEP, yc + v * unit)} circle (6.5\\px);")
        parts.append(f"\\node[anchor=east, font=\\fssmall, inner sep=2\\px] at {P(X0 - 30, yc)} {{{names[i]}}};")
    boxes = [r"$U^{\top}$", r"$\times\, g(\lambda)$", r"$U$"]
    for i, t in enumerate(boxes):
        ya, yb = ys[i] - H0 / 2 - 2, ys[i + 1] + H0 / 2 + 2
        ym = (ya + yb) / 2
        parts.append(node(f"b{i}", (xc, ym), t, style="smallbox", w=200 if i == 1 else 100, h=64))
        parts.append(arrow((xc, ya), f"(b{i}.north)"))
        parts.append(arrow(f"(b{i}.south)", (xc, yb)))
    # g(lambda) curve left of the second box
    cx0, cw, ch = 100, 130, 56
    ym = (ys[1] - H0 / 2 - 2 + ys[2] + H0 / 2 + 2) / 2
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

    parts.append(box(0, 0, 630, 520, "white"))
    parts.append(box(14, 14, 474, 430, "hl"))
    parts.append(box(28, 28, 324, 306, "white"))

    def lab_(x, y, t):
        return f"\\node[anchor=north west, font=\\fsbody, inner sep=2\\px] at {P(x, y)} {{{t}}};"

    parts.append(lab_(12, 516, "spectral"))
    parts.append(lab_(26, 426, "Cheb"))
    parts.append(lab_(42, 302, "GCN"))

    CW, CH = 76, 120

    def plot_curve(x0, y0, f, ymin, ymax, col="ink"):
        z = (0 - ymin) / (ymax - ymin) * CH            # height of the lambda axis
        ar = "-{Stealth[length=7bp, width=6bp]}"
        out = [f"\\draw[{ar}, line width=1.5\\px] {P(x0, y0 + z)} -- {P(x0 + CW + 12, y0 + z)};",
               f"\\draw[{ar}, line width=1.5\\px] {P(x0, y0)} -- {P(x0, y0 + CH + 8)};"]
        pts = [(x0 + (l / 2) * CW, y0 + (v - ymin) / (ymax - ymin) * CH) for l, v in zip(lam, f)]
        out.append(curve(pts, f"draw={col}, line width=3.5\\px"))
        out.append(f"\\node[anchor=west, font=\\fssmall, inner sep=1\\px] at {P(x0 + CW + 14, y0 + z)} {{$\\lambda$}};")
        return "\n".join(out)

    parts.append(plot_curve(488, 210, free, 0, 1))
    parts.append(plot_curve(336, 180, poly3, -0.1, 1.1))
    parts.append(plot_curve(190, 110, line, -1, 1))
    parts.append(f"\\node[anchor=east, font=\\fssmall, inner sep=1\\px] at {P(170, 170)} {{$1-\\lambda$}};")
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
    W, H, LAB, GX = 360, 270, 62, 23
    pos, edges, _ = karate_layout(W, H, seed=4, margin=18)
    mx = x.max()
    mh = np.abs(high).max()
    cols = [[seq(v / mx) for v in x], [seq(v / mx) for v in low], [div(v / mh) for v in high]]
    names = ["$\\bm x$", "low", "high"]
    parts = []
    for pi in range(3):
        ox = pi * (W + GX)
        for v, (px, py) in pos.items():
            parts.append(vtx(f"p{pi}v{v}", (ox + px, py), 26, cols[pi][v - 1], extra="line width=1.5\\px"))
        parts.append("\\begin{scope}[on background layer]")
        parts += [eg(f"p{pi}v{a}", f"p{pi}v{b}", "draw=rule", lw=1.5) for a, b in edges]
        parts.append("\\end{scope}")
        parts.append(label((ox + W / 2, H + LAB / 2 + 2), names[pi], size="fssmall"))
    return B("e06_masks_karate", *parts)


# ---------------------------------------------------------------- e07
def e07_highfreq_boundary():
    G, x, low, high = _centrality_parts()
    W, H = 636, 540
    pos, edges, club = karate_layout(W, H, seed=4, margin=34)
    mag = np.abs(high)
    t = mag / mag.max()
    cross = [(a, b) for a, b in edges if club[a] != club[b]]
    big = 3                       # a large node with the most boundary edges (4)
    sz = {v: 36 + 22 * t[v - 1] for v in pos}
    for _ in range(200):                           # push overlapping nodes apart
        moved = False
        for u in pos:
            for w in pos:
                if u < w:
                    dx, dy = pos[w][0] - pos[u][0], pos[w][1] - pos[u][1]
                    d = max(np.hypot(dx, dy), 1e-6)
                    need = (sz[u] + sz[w]) / 2 + 4
                    if d < need:
                        f = (need - d) / 2 / d
                        pos[u] = (pos[u][0] - dx * f, pos[u][1] - dy * f)
                        pos[w] = (pos[w][0] + dx * f, pos[w][1] + dy * f)
                        moved = True
        if not moved:
            break
    parts = []
    for v, p in pos.items():
        parts.append(vtx(f"v{v}", p, 36 + 22 * t[v - 1], seq(t[v - 1]), extra="line width=1.5\\px"))
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
    FW, FH, GAP = 430, 186, 14
    parts = []
    fy = [2 * (FH + GAP), (FH + GAP), 0]
    for y in fy:
        parts.append(f"\\draw[line width=2\\px, fill=white] {P(0, y)} rectangle {P(FW, y + FH)};")
    LY = 36                                   # label height above the frame bottom
    # (1) convolution: 4x4 pixel grid with the 3x3 window -> small graph
    y0 = fy[0]
    cs = 24
    gx0, gy0 = 34, y0 + 72
    rng = np.random.default_rng(1)
    for i in range(4):
        for j in range(4):
            inwin = i < 3 and j < 3
            g = 255 - int(rng.integers(0, 90))
            fillc = "hl" if inwin else rgbs(np.array([g, g, g], float))
            parts.append(f"\\draw[line width=1.5\\px, fill={fillc}] "
                         f"{P(gx0 + j * cs, gy0 + (3 - i) * cs)} rectangle {P(gx0 + (j + 1) * cs, gy0 + (4 - i) * cs)};")
    parts.append(f"\\draw[line width=3\\px] {P(gx0, gy0 + cs)} rectangle {P(gx0 + 3 * cs, gy0 + 4 * cs)};")
    parts.append(arrow((gx0 + 4 * cs + 12, gy0 + 2 * cs), (gx0 + 4 * cs + 62, gy0 + 2 * cs)))
    gp = {1: (302, y0 + 120), 2: (368, y0 + 148), 3: (372, y0 + 98), 4: (335, y0 + 72), 5: (260, y0 + 102)}
    for v, p in gp.items():
        parts.append(vtx(f"s1v{v}", p, 36, HL if v == 1 else "#FFFFFF"))
    for a, b in [(1, 2), (1, 3), (1, 4), (1, 5), (4, 3)]:
        parts.append(eg(f"s1v{a}", f"s1v{b}", "draw=ink", lw=1.5))
    parts.append(label((FW / 2, y0 + LY), "convolution", size="fssmall"))
    # (2) message passing: neighbours -> centre
    y0 = fy[1]
    ctr = (295, y0 + 116)
    parts.append(vtx("s2c", ctr, 44, HL))
    nbs = [(70, y0 + 150), (70, y0 + 80), (170, y0 + 160), (170, y0 + 72)]
    for i, p in enumerate(nbs):
        parts.append(vtx(f"s2n{i}", p, 36))
    parts.append(label((FW / 2, y0 + LY), "message passing", size="fssmall"))
    # (3) low-pass: curve and dots
    y0 = fy[2]
    cx0, cy0, cw, ch = 80, y0 + 82, 270, 56
    parts.append(axes(cx0, cy0, cw + 14, ch + 8))
    ls = np.linspace(0, 1, 40)
    gcurve = lambda l: 1 / (1 + (l / 0.38) ** 4)  # noqa: E731
    parts.append(curve([(cx0 + l * cw, cy0 + gcurve(l) * ch) for l in ls], "draw=snew, line width=3\\px"))
    lamp = np.linspace(0.08, 0.92, 6)
    for l in lamp:
        parts.append(f"\\fill[ink] {P(cx0 + l * cw, cy0)} circle (6\\px);")
        parts.append(f"\\fill[snew] {P(cx0 + l * cw, cy0 + gcurve(l) * ch)} circle (5\\px);")
        parts.append(f"\\draw[line width=1.2\\px, draw=muted] {P(cx0 + l * cw, cy0)} -- {P(cx0 + l * cw, cy0 + gcurve(l) * ch)};")
    parts.append(label((FW / 2, y0 + LY), "low-pass", size="fssmall"))
    return parts


def _e08():
    parts = e08_summary_visuals()
    for i in range(4):
        parts.append(f"\\draw[arr] (s2n{i}) -- (s2c);")
    return B("e08_summary_visuals", *parts)


# ---------------------------------------------------------------- f01
def f01_gcn_fourier():
    parts = []
    CX = [300, 866]
    parts.append(f"\\draw[line width=2\\px, draw=rule] {P(583, 10)} -- {P(583, 550)};")
    parts.append(label((CX[0], 530), "image", size="fslarge"))
    parts.append(label((CX[1], 530), "graph", size="fslarge"))
    # left: gray patch * blur kernel
    rng = np.random.default_rng(5)
    cs, ky = 30, 412
    px0 = CX[0] - 170
    py0 = ky - 2.5 * cs
    for i in range(5):
        for j in range(5):
            g = 255 - int(rng.integers(20, 150))
            parts.append(f"\\draw[line width=1.5\\px, fill={rgbs(np.array([g, g, g], float))}] "
                         f"{P(px0 + j * cs, py0 + i * cs)} rectangle {P(px0 + (j + 1) * cs, py0 + (i + 1) * cs)};")
    sx, sy = px0 + 5 * cs + 38, ky
    for ang in (90, 30, 150):
        dx, dy = 18 * np.cos(np.radians(ang)), 18 * np.sin(np.radians(ang))
        parts.append(f"\\draw[line width=5\\px, line cap=round] {P(sx - dx, sy - dy)} -- {P(sx + dx, sy + dy)};")
    ks = 38
    kx0 = px0 + 5 * cs + 76
    ky0 = ky - 1.5 * ks
    for i in range(3):
        for j in range(3):
            parts.append(f"\\draw[line width=1.5\\px, fill=hl] {P(kx0 + j * ks, ky0 + i * ks)} rectangle "
                         f"{P(kx0 + (j + 1) * ks, ky0 + (i + 1) * ks)};")
    parts.append(label((CX[0], 292), "convolution", size="fssmall"))
    # right: GCN step, three neighbours into node i
    ci = (CX[1] + 100, ky)
    parts.append(vtx("gi", ci, 56, HL, text=""))
    nb = [(CX[1] - 120, ky + 62), (CX[1] - 120, ky), (CX[1] - 120, ky - 62)]
    for k, p in enumerate(nb):
        parts.append(vtx(f"gn{k}", p, 44))
    for k in range(3):
        parts.append(f"\\draw[arr] (gn{k}) -- (gi);")
    parts.append(label((CX[1], 292), "GCN step", size="fssmall"))
    # arrows down
    for cx, t in zip(CX, ["Fourier", "?"]):
        parts.append(arrow((cx, 250), (cx, 160)))
        parts.append(label((cx + 18, 205), t, size="fssmall", anchor="west"))
    # waves (left) and a big question mark (right)
    wx0, ww = CX[0] - 150, 300
    ts = np.linspace(0, 1, 120)
    parts.append(curve([(wx0 + t * ww, 112 + 24 * np.sin(2 * np.pi * 2 * t)) for t in ts], "draw=snew, line width=3.5\\px"))
    parts.append(curve([(wx0 + t * ww, 56 + 20 * np.sin(2 * np.pi * 6 * t)) for t in ts], "draw=sbase, line width=3.5\\px"))
    parts.append(f"\\node[font=\\fontsize{{120\\px}}{{120\\px}}\\selectfont, inner sep=0pt] at {P(CX[1], 85)} {{?}};")
    return B("f01_gcn_fourier", *parts)


# ---------------------------------------------------------------- f02
def f02_smoothness():
    G, L, A, lam, U = karate_spectral()
    W, H, GX = 520, 290, 100
    pos, edges, _ = karate_layout(W, H, seed=4, margin=22)
    sigs = []
    spread = {k: np.abs(U[:, k]).max() for k in range(28, 34)}
    khi = min(spread, key=spread.get)              # most spread-out of the top 6 eigenvectors
    print("f02 top-6 max|u|:", {k + 1: round(float(v), 3) for k, v in spread.items()}, "chosen", khi + 1)
    for k, word in [(1, "low frequency"), (khi, "high frequency")]:
        u = U[:, k].copy()
        u *= np.sign(u[int(np.argmax(np.abs(u)))])
        J = float(sum(A[i, j] * (u[i] - u[j]) ** 2 for i in range(34) for j in range(34)))
        assert abs(J - 2 * lam[k]) < 1e-8
        sigs.append((u, J, word))
    parts = []
    OX = [(1166 - 2 * W - GX) / 2 + i * (W + GX) for i in range(2)]
    for pi, (u, J, word) in enumerate(sigs):
        ox = OX[pi]
        m = np.abs(u).max()
        for v, (px, py) in pos.items():
            parts.append(vtx(f"p{pi}v{v}", (ox + px, 130 + py), 28, div(u[v - 1] / m), extra="line width=1.5\\px"))
        parts.append("\\begin{scope}[on background layer]")
        parts += [eg(f"p{pi}v{a}", f"p{pi}v{b}", "draw=rule", lw=1.5) for a, b in edges]
        parts.append("\\end{scope}")
        parts.append(label((ox + W / 2, 90), f"\\textit{{J}} = {J:.1f}", size="fssmall"))
        parts.append(label((ox + W / 2, 26), word, size="fssmall"))
        print("f02", word, "lambda", round(float(lam[[1, khi][pi]]), 3), "J", round(J, 3))
    return B("f02_smoothness", *parts)


if __name__ == "__main__":
    allf = {"e01": e01_khop, "e02": e02_laplacian_diff, "e03": e03_eigvecs_karate,
            "e04": e04_spectral_conv_flow, "e05": e05_nested_models, "e06": e06_masks_karate,
            "e07": lambda: e07_highfreq_boundary()[0], "e08": _e08, "f01": f01_gcn_fourier,
            "f02": f02_smoothness}
    for k in (sys.argv[1:] or list(allf)):
        allf[k]()
        print("built", k, flush=True)

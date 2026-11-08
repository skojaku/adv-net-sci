"""Group b: image as graph, GCN.   Run from slides/m09:
uv run --quiet --with numpy --with scipy --with networkx --with pillow --with scikit-image python figures/fig_b.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import networkx as nx  # noqa: E402
import numpy as np  # noqa: E402

from common import *  # noqa: E402,F401,F403

HOPS = ["#D9B8F5", "#B88AE0", "#9B6BC9"]          # hop 1, 2, 3 (lavender step scale)
RULE = "#C9C9C9"


# ---------------------------------------------------------------- colour helpers
def col(c) -> str:
    """TikZ colour from '#RRGGBB' or an (r, g, b) tuple of 0..255 values."""
    if isinstance(c, str):
        c = c.lstrip("#")
        c = tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    return "{rgb,255:red,%d;green,%d;blue,%d}" % tuple(int(round(v)) for v in c)


def mix(c0, c1, t):
    def rgb(c):
        c = c.lstrip("#")
        return np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], float)
    t = float(min(1, max(0, t)))
    return tuple(rgb(c0) * (1 - t) + rgb(c1) * t)


def seq(t):                       # white -> blue
    return col(mix("#FFFFFF", BLUE, t))


def div(v, lim):                  # vermillion - white - blue
    t = float(max(-1, min(1, v / lim)))
    return col(mix("#FFFFFF", BLUE, t) if t >= 0 else mix("#FFFFFF", VERM, -t))


def gray(v):
    return col((v, v, v))


# ---------------------------------------------------------------- drawing helpers
def circ(name, at, fill="white", size=30, text="", lw=2):
    return vertex(name, at, text, size=size, extra=f"fill={fill}, line width={lw}\\px")


def line(a, b, color="ink", lw=2, dash=False):
    d = ", dash pattern=on 6\\px off 5\\px" if dash else ""
    return f"\\draw[draw={color}, line width={lw}\\px{d}] {P(*a)} -- {P(*b)};"


def rect(x0, y0, x1, y1, fill="white", lw=2, color="ink"):
    return f"\\draw[{color}, line width={lw}\\px, fill={fill}] {P(x0, y0)} rectangle {P(x1, y1)};"


def triangle(cx, cy, w=22, h=30):
    return f"\\fill[ink] {P(cx - w / 2, cy + h / 2)} -- {P(cx + w / 2, cy)} -- {P(cx - w / 2, cy - h / 2)} -- cycle;"


def norm_adj(G):
    A = nx.to_numpy_array(G, nodelist=sorted(G.nodes()))
    At = A + np.eye(len(A))
    d = At.sum(1)
    return A, At / np.sqrt(np.outer(d, d))


# ================================================================= b01
def b01_grid_to_graph():
    img = camera().astype(float)
    pix = img.reshape(4, 128, 4, 128).mean(axis=(1, 3))        # real 4 x 4 gray values (whole photo pooled)
    lo, hi = pix.min(), pix.max()
    pix = (pix - lo) / (hi - lo) * 215 + 20                    # stretch to 20..235 so every cell is distinct
    c = 50
    parts = []
    grid = {(r, k): (k * c + c / 2, (3 - r) * c + c / 2) for r in range(4) for k in range(4)}
    gedges = [((r, k), (r, k + 1)) for r in range(4) for k in range(3)] + \
             [((r, k), (r + 1, k)) for r in range(3) for k in range(4)]
    # stage 1: pixels
    for (r, k), (x, y) in grid.items():
        parts.append(rect(x - c / 2, y - c / 2, x + c / 2, y + c / 2, gray(pix[r, k]), lw=2))
    # stage 2: grid graph
    x2 = 242
    for a, b in gedges:
        parts.append(line((grid[a][0] + x2, grid[a][1]), (grid[b][0] + x2, grid[b][1])))
    for (r, k), (x, y) in grid.items():
        parts.append(circ(f"g{r}{k}", (x + x2, y), gray(pix[r, k]), size=30))
    # stage 3: same nodes, irregular positions
    rng = np.random.default_rng(3)
    x3 = 484
    irr = {}
    for (r, k), (x, y) in grid.items():
        jx, jy = rng.uniform(-1, 1, 2)
        ux = x + 16 * math.sin(y / 38.0) + 11 * jx
        uy = y * 1.10 + 16 * math.sin(x / 45.0 + 1.0) + 11 * jy - 6
        irr[(r, k)] = (ux + x3, uy)
    for a, b in gedges:
        parts.append(line(irr[a], irr[b]))
    for key, (x, y) in irr.items():
        parts.append(circ(f"h{key[0]}{key[1]}", (x, y), gray(pix[key]), size=30))
    # triangles and labels
    parts.append(triangle(221, 100))
    parts.append(triangle(463, 100))
    for xc, t in ((100, "pixels"), (342, "edges"), (584, "graph")):
        parts.append(label((xc, -28), t, anchor="center"))
    return B("b01_grid_to_graph", *parts)


# ================================================================= b02
def b02_pixel_vs_node():
    c = 80
    parts = []
    cols = [col(YEL), col(SKY), col(PINK), col(BLUE), col(VERM), gray(110), gray(175), gray(225)]
    ox, oy = 0, 140            # grid origin (bottom-left)
    order = [(r, k) for r in range(3) for k in range(3) if (r, k) != (1, 1)]
    ci = 0
    for r in range(3):
        for k in range(3):
            x0, y0 = ox + k * c, oy + (2 - r) * c
            if (r, k) == (1, 1):
                parts.append(rect(x0, y0, x0 + c, y0 + c, col(HL)))
            else:
                parts.append(rect(x0, y0, x0 + c, y0 + c, cols[ci]))
                ci += 1
    # node with 4 neighbours
    cx, cy = 3 * c + 55 + 100, oy + 1.5 * c
    d = 100
    nbr = [(cx, cy + d), (cx + d, cy), (cx, cy - d), (cx - d, cy)]
    for i, p in enumerate(nbr):
        parts.append(line((cx, cy), p, lw=3))
    for i, p in enumerate(nbr):
        parts.append(circ(f"n{i}", p, gray(175), size=52))
    parts.append(circ("ctr", (cx, cy), col(HL), size=60))
    parts.append(label((1.5 * c, 100), r"weight per\\position", anchor="north", extra="align=center"))
    parts.append(label((cx, 100), r"weight per\\edge", anchor="north", extra="align=center"))
    return B("b02_pixel_vs_node", *parts)


# ================================================================= b03
def gcn_out(seed):
    G = nx.karate_club_graph()
    _, Ah = norm_adj(G)
    rng = np.random.default_rng(seed)
    W1, W2, W3 = rng.standard_normal((34, 4)), rng.standard_normal((4, 4)), rng.standard_normal((4, 2))
    h = np.tanh(Ah @ np.eye(34) @ W1)
    h = np.tanh(Ah @ h @ W2)
    return Ah @ h @ W3


def pick_seed():
    """Seed whose 3-layer untrained GCN separates the clubs in 2D and fills both axes (not a line)."""
    G = nx.karate_club_graph()
    y = np.array([0 if G.nodes[i]["club"] == "Mr. Hi" else 1 for i in G])
    best, bs = None, -1
    for s in range(500):
        o = gcn_out(s)
        o = o - o.mean(0)
        sv = np.linalg.svd(o, compute_uv=False)
        if sv[1] / sv[0] < 0.45:
            continue
        a, b = o[y == 0], o[y == 1]
        m0, m1 = a.mean(0), b.mean(0)
        sp = math.sqrt(a.var(0).sum() + b.var(0).sum())
        pred = (np.linalg.norm(o - m1, axis=1) < np.linalg.norm(o - m0, axis=1)).astype(int)
        acc = (pred == y).mean()
        score = acc + 0.3 * np.linalg.norm(m0 - m1) / sp
        if score > bs:
            best, bs = s, score
    return best


def b03_untrained_gcn():
    seed = pick_seed()
    print("b03 seed", seed)
    W, Hh = 330, 290
    pos, edges, club = karate_layout(W, Hh, margin=18)
    ccol = {0: col(BLUE), 1: col(VERM)}
    parts = []
    for u, v in edges:
        parts.append(line(pos[u], pos[v], color=col(RULE), lw=2))
    for i, p in pos.items():
        parts.append(circ(f"k{i}", p, ccol[club[i]], size=22))
    # right panel
    ox = 370
    o = gcn_out(seed)
    o = o - o.mean(0)
    s = min((W - 50) / (o[:, 0].max() - o[:, 0].min()), (Hh - 50) / (o[:, 1].max() - o[:, 1].min()))
    cx, cy = ox + W / 2, Hh / 2
    mid = (o.max(0) + o.min(0)) / 2
    parts.append(f"\\draw[line width=1.5\\px, ink] {P(ox, 0)} rectangle {P(ox + W, Hh)};")
    for i in range(34):
        x = cx + (o[i, 0] - mid[0]) * s
        y = cy + (o[i, 1] - mid[1]) * s
        parts.append(circ(f"o{i}", (x, y), ccol[club[i + 1]], size=22))
    parts.append(label((W / 2, -12), r"karate club", anchor="north"))
    parts.append(label((ox + W / 2, -12), r"GCN output\\(no training)", anchor="north", extra="align=center"))
    return B("b03_untrained_gcn", *parts)


# ================================================================= b04
def b04_gcn_layer_node():
    rng = np.random.default_rng(5)
    degs = {"i": 3, "j1": 2, "j2": 1, "j3": 3}
    dt = {k: v + 1 for k, v in degs.items()}
    names = ["j1", "j2", "j3", "i"]
    feat = {k: rng.uniform(0.05, 1.0, 3) for k in names}
    w = {k: 1 / math.sqrt(dt["i"] * dt[k]) for k in names if k != "i"}
    w["i"] = 1 / dt["i"]
    s = sum(w[k] * feat[k] for k in names)
    Wm = rng.standard_normal((3, 3)) * 1.2
    new = 1 / (1 + np.exp(-(s @ Wm)))
    ys = {"j1": 400, "j2": 280, "j3": 160, "i": 40}
    sx, sy = 285, 220         # Sigma centre
    parts = []
    labs = {"j1": r"j_1", "j2": r"j_2", "j3": r"j_3", "i": r"i"}
    wl = {"j1": r"\hat A_{ij_1}", "j2": r"\hat A_{ij_2}", "j3": r"\hat A_{ij_3}", "i": r"\hat A_{ii}"}
    q = 24

    def vec(x, y, vals, bg=None):
        out = []
        if bg:
            out.append(rect(x - 4, y - 1.5 * q - 4, x + q + 4, y + 1.5 * q + 4, col(HL), lw=2))
        for t, v in enumerate(vals):
            yy = y + 1.5 * q - (t + 1) * q
            out.append(rect(x, yy, x + q, yy + q, seq(v), lw=1.5))
        return out

    for k in names:
        y = ys[k]
        fx = 78
        parts.append(circ(f"c{k}", (30, y), col(HL) if k == "i" else "white", size=52, text=f"${labs[k]}$"))
        parts += vec(fx, y, feat[k])
        a = (fx + q + 8, y)
        parts.append(f"\\draw[arr] {P(*a)} -- {P(sx - 26, sy)} node[pos=0.3, fill=white, inner sep=2\\px, "
                     f"font=\\fssmall] {{${wl[k]}$}};")
    parts.append(circ("sig", (sx, sy), "white", size=52, text=r"$\sum$"))
    bx = [360, 440]
    parts.append(f"\\draw[arr] {P(sx + 26, sy)} -- {P(bx[0] - 28, sy)};")
    parts.append(node("W", (bx[0], sy), "$W$", style="smallbox"))
    parts.append(f"\\draw[arr] {P(bx[0] + 28, sy)} -- {P(bx[1] - 28, sy)};")
    parts.append(node("sg", (bx[1], sy), r"$\sigma$", style="smallbox"))
    parts.append(f"\\draw[arr] {P(bx[1] + 28, sy)} -- {P(bx[1] + 56, sy)};")
    parts += vec(bx[1] + 64, sy, new, bg=True)
    parts.append(label((bx[1] + 64 + q / 2, sy - 62), r"$h_i'$", anchor="north"))
    return B("b04_gcn_layer_node", *parts)


# ================================================================= b05
def b05_norm_weights():
    G = nx.Graph([(0, 1), (0, 2), (0, 3), (0, 4), (1, 2)])
    pos = {0: (310, 235), 1: (95, 370), 2: (95, 100), 3: (525, 370), 4: (525, 100)}
    dt = {v: G.degree(v) + 1 for v in G}
    parts = []
    # self loops (out/in angles point away from the hub)
    away = {0: 90, 1: 150, 2: 210, 3: 30, 4: 330}
    for v, (x, y) in pos.items():
        a = math.radians(away[v])
        parts.append(f"\\draw[line width=2\\px, ink] {P(x + 46 * math.cos(a), y + 46 * math.sin(a))} circle (24\\px);")
    for u, v in G.edges():
        hub = 0 in (u, v)
        parts.append(f"\\draw[{'hlink' if hub else 'ink'}, line width={4 if hub else 2}\\px] {P(*pos[u])} -- {P(*pos[v])};")
    for u, v in G.edges():
        hub = 0 in (u, v)
        w = 1 / math.sqrt(dt[u] * dt[v])
        mx, my = (pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2
        if (u, v) == (1, 2):
            mx -= 0
        parts.append(f"\\node[fill={'hl' if hub else 'white'}, inner sep=3\\px, font=\\fssmall] at {P(mx, my)} {{${w:.2f}$}};")
    for v, p in pos.items():
        parts.append(circ(f"v{v}", p, col(HL) if v == 0 else "white", size=62, text=f"${dt[v]}$"))
    parts.append(label((310, 15), r"node $=\tilde d$", anchor="center"))
    return B("b05_norm_weights", *parts)


# ================================================================= b06
def b06_matrix_picture():
    rng = np.random.default_rng(7)
    n, d, d2 = 8, 3, 2
    G = nx.gnp_random_graph(n, 0.3, seed=11)
    A = nx.to_numpy_array(G) + np.eye(n)
    dd = A.sum(1)
    Ah = A / np.sqrt(np.outer(dd, dd))
    H = rng.uniform(0, 1, (n, d))
    W = rng.standard_normal((d, d2))
    H2 = Ah @ H @ W
    LIM = max(abs(W).max(), abs(H2).max())
    c = 29
    hl_row = 3
    gap = 44
    parts = []
    top = 240   # y of the top edge of the blocks

    def block(x0, M, kind, name, dots=False, ncol=None):
        r, k = M.shape
        out = []
        for i in range(r):
            for j in range(k):
                x, y = x0 + j * c, top - (i + 1) * c
                if kind == "A":
                    f = col(HL) if i == hl_row else "white"
                elif kind == "seq":
                    f = seq(M[i, j])
                else:
                    f = div(M[i, j], LIM)
                if kind == "seq" or kind == "div":
                    pass
                out.append(f"\\fill[fill={f}] {P(x, y)} rectangle {P(x + c, y + c)};")
        if kind in ("seq", "div") and False:
            pass
        # light cell lines
        for i in range(r + 1):
            out.append(line((x0, top - i * c), (x0 + k * c, top - i * c), color=col(RULE), lw=1))
        for j in range(k + 1):
            out.append(line((x0 + j * c, top), (x0 + j * c, top - r * c), color=col(RULE), lw=1))
        if dots:
            for i in range(r):
                for j in range(k):
                    if M[i, j] > 0:
                        out.append(f"\\fill[ink] {P(x0 + (j + .5) * c, top - (i + .5) * c)} circle (5.5\\px);")
        out.append(f"\\draw[ink, line width=2\\px] {P(x0, top)} rectangle {P(x0 + k * c, top - r * c)};")
        return out

    x = 34
    parts += block(x, Ah, "A", "A", dots=True)
    xA = x
    x += n * c + gap
    parts += block(x, H, "seq", "H")
    xH = x
    x += d * c + gap
    # W is d x d2, aligned to the top edge
    parts += block(x, W, "div", "W")
    xW = x
    x += d2 * c + gap
    parts += block(x, H2, "div", "H2")
    xH2 = x
    # highlight the row i in H and H': draw a lavender outline over that row (value cells keep their colour)
    for x0, k in ((xH, d), (xH2, d2)):
        parts.append(f"\\draw[hlink, line width=4\\px] {P(x0, top - hl_row * c)} rectangle {P(x0 + k * c, top - (hl_row + 1) * c)};")
    parts.append(f"\\draw[hlink, line width=4\\px] {P(xA, top - hl_row * c)} rectangle {P(xA + n * c, top - (hl_row + 1) * c)};")
    # operators (at the middle of the tall blocks)
    my = top - n * c / 2
    parts.append(label((xA + n * c + gap / 2, my), r"$\times$", anchor="center", size="fslarge"))
    parts.append(label((xH + d * c + gap / 2, my), r"$\times$", anchor="center", size="fslarge"))
    parts.append(label((xW + d2 * c + gap / 2, my), r"$=$", anchor="center", size="fslarge"))
    # names under the blocks
    yb = top - n * c - 14
    for xx, w_, t in ((xA, n, r"$\hat A$"), (xH, d, r"$H$"), (xH2, d2, r"$H'$")):
        parts.append(label((xx + w_ * c / 2, yb), t, anchor="north"))
    parts.append(label((xW + d2 * c / 2, top - d * c - 14), r"$W$", anchor="north"))
    # dimensions on top and left
    yt = top + 8
    for xx, w_, t in ((xA, n, "$n$"), (xH, d, "$d$"), (xW, d2, "$d'$"), (xH2, d2, "$d'$")):
        parts.append(label((xx + w_ * c / 2, yt), t, anchor="south"))
    parts.append(label((xA - 8, top - n * c / 2), "$n$", anchor="east"))
    return B("b06_matrix_picture", *parts)


# ================================================================= b07
def b07_receptive_graph():
    edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 5), (2, 6), (3, 7), (3, 8),
             (4, 9), (6, 10), (7, 10), (8, 11), (8, 12)]
    G = nx.Graph(edges)
    dist = nx.single_source_shortest_path_length(G, 0)
    assert [sum(1 for v in dist if dist[v] == h) for h in range(4)] == [1, 3, 5, 4]
    base = {0: (0, 0), 1: (-50, 25), 2: (20, 55), 3: (50, -35), 4: (-100, 62), 5: (-32, 100),
            6: (92, 78), 7: (118, -30), 8: (55, -90), 9: (-110, 5), 10: (130, 28), 11: (0, -95), 12: (110, -90)}
    xs = [p[0] for p in base.values()]; ys = [p[1] for p in base.values()]
    cxg, cyg = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    sc = 0.88
    pitch = 252
    parts = []
    gy = 375           # graph row centre
    py = 125           # grid row centre
    cell = 32
    for ci, L in enumerate((1, 2, 3)):
        cx = 125 + ci * pitch
        P_ = {v: (cx + (p[0] - cxg) * sc, gy + (p[1] - cyg) * sc) for v, p in base.items()}
        for u, v in edges:
            parts.append(line(P_[u], P_[v], lw=2))
        for v, p in P_.items():
            if v == 0:
                f = "ink"
            elif dist[v] <= L:
                f = col(HOPS[dist[v] - 1])
            else:
                f = "white"
            parts.append(circ(f"g{ci}_{v}", p, f, size=30))
        # grid
        for r in range(7):
            for k in range(7):
                dd = max(abs(r - 3), abs(k - 3))
                if dd == 0:
                    f = "ink"
                elif dd <= L:
                    f = col(HOPS[dd - 1])
                else:
                    f = "white"
                x0, y0 = cx - 3.5 * cell + k * cell, py - 3.5 * cell + (6 - r) * cell
                parts.append(rect(x0, y0, x0 + cell, y0 + cell, f, lw=2))
        parts.append(label((cx, 520), f"{L} layer" + ("s" if L > 1 else ""), anchor="north"))
    return B("b07_receptive_graph", *parts)


# ================================================================= b08
def b08_smoothing_6():
    G = nx.karate_club_graph()
    _, Ah = norm_adj(G)
    x0 = np.random.default_rng(0).uniform(0, 1, 34)
    pw, ph = 262, 168
    pos, edges, _ = karate_layout(pw, ph, margin=14)
    layers = [0, 1, 2, 3, 5, 20]
    parts = []
    # one colour scale for all panels (0 .. largest value of any panel), so that the change over layers is visible
    xmax = max((np.linalg.matrix_power(Ah, L) @ x0).max() for L in layers)
    for idx, L in enumerate(layers):
        r, k = divmod(idx, 2)
        ox = k * 345 + 80
        oy = (2 - r) * 186 + 6
        x = np.linalg.matrix_power(Ah, L) @ x0
        t = x / xmax
        for u, v in edges:
            parts.append(line((pos[u][0] + ox, pos[u][1] + oy), (pos[v][0] + ox, pos[v][1] + oy), color=col(RULE), lw=2))
        for i, p in pos.items():
            parts.append(circ(f"p{idx}_{i}", (p[0] + ox, p[1] + oy), seq(t[i - 1]), size=22, lw=1.5))
        parts.append(label((ox - 8, oy + ph / 2), f"layer\\\\{L}", anchor="east", extra="align=center"))
    return B("b08_smoothing_6", *parts)


# ================================================================= b09
def b09_explosion():
    parts = []
    ys = [445, 310, 175, 40]
    l1 = [146 + i * 112 for i in range(5)]
    root = (l1[2], ys[0])
    off = 38
    for x in l1:
        parts.append(line(root, (x, ys[1])))
        for dx in (-off, off):
            parts.append(line((x, ys[1]), (x + dx, ys[2])))
    p0 = (l1[2] + off, ys[2])
    kids = [(p0[0] - 22, ys[3]), (p0[0] + 22, ys[3])]
    for q in kids:
        parts.append(line(p0, q))
    parts.append(circ("root", root, col(HL), size=44))
    for i, x in enumerate(l1):
        parts.append(circ(f"c{i}", (x, ys[1]), "white", size=40))
        for j, dx in enumerate((-off, off)):
            parts.append(circ(f"d{i}{j}", (x + dx, ys[2]), "white", size=26))
        parts.append(label((x, ys[2] - 2), r"$\cdots$", anchor="center"))
    for j, q in enumerate(kids):
        parts.append(circ(f"e{j}", q, "white", size=20, lw=1.5))
    parts.append(label((p0[0] + 50, ys[3] - 2), r"$\cdots$", anchor="center"))
    for i, x in enumerate(l1):
        for j, dx in enumerate((-off, off)):
            if (i, j) not in ((2, 1), (3, 0)):
                parts.append(label((x + dx, ys[3] + 4), r"$\vdots$", anchor="center"))
    for y, h, n in zip(ys, range(4), (1, 5, 25, 125)):
        parts.append(label((0, y), f"hop {h}", anchor="west"))
        parts.append(label((692, y), f"${n}$", anchor="east"))
    return B("b09_explosion", *parts)


if __name__ == "__main__":
    for f in (b01_grid_to_graph, b02_pixel_vs_node, b03_untrained_gcn, b04_gcn_layer_node, b05_norm_weights,
              b06_matrix_picture, b07_receptive_graph, b08_smoothing_6, b09_explosion):
        try:
            f()
            print("built", f.__name__)
        except Exception as e:  # keep going so that one error does not hide the rest
            print("FAILED", f.__name__, e)

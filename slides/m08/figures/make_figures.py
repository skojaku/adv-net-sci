"""Build every figure of the m08 deck:  python3 figures/make_figures.py  (from slides/m08).

Real data where a figure shows a result (karate club, the growth model with a fixed seed);
hand layouts for the explanatory drawings. See ~/.claude/skills/slide-math/FIGURES.md.
"""

import math
import random
import sys
from pathlib import Path

import networkx as nx
import numpy as np

sys.path.insert(0, str(Path.home() / ".claude/skills/slide-math/figkit"))
from figkit import P, arrow, build, edge, graph, label, lineplot, node, raw, vecdots, vertex  # noqa: E402

OUT = Path(__file__).resolve().parent


# ------------------------------------------------------------------ data

def karate():
    G = nx.karate_club_graph()
    A = nx.to_numpy_array(G)
    deg = A.sum(1)
    L = np.diag(deg) - A
    w, V = np.linalg.eigh(L)
    fiedler = V[:, 1]
    order = np.argsort(fiedler)
    club = np.array([0 if G.nodes[i]["club"] == "Mr. Hi" else 1 for i in range(34)])
    lam, U = np.linalg.eigh(A)
    idx = np.argsort(-np.abs(lam))
    return A, lam[idx], U[:, idx], order, fiedler, club


A, LAM, U, ORDER, FIEDLER, CLUB = karate()
if FIEDLER[ORDER[0]] > 0:      # sign is arbitrary; put the faction of node 0 on the left
    pass


def reconstruct(d):
    return (U[:, :d] * LAM[:d]) @ U[:, :d].T


# ------------------------------------------------------------------ helpers

def rgb(c):
    return f"{{rgb,255:red,{c[0]};green,{c[1]};blue,{c[2]}}}"


def diverging(v):
    """-1 blue (snew), 0 white, +1 vermillion (sbase)."""
    v = max(-1.0, min(1.0, v))
    neg, pos, w = (0, 114, 178), (213, 94, 0), (255, 255, 255)
    tgt = pos if v >= 0 else neg
    t = abs(v)
    return tuple(round(w[i] + (tgt[i] - w[i]) * t) for i in range(3))


def heat(M, x0, y0, size, perm=None, scale=1.0, binary=False):
    """A matrix as coloured cells, top-left corner at (x0, y0) in px (y up in TikZ)."""
    n = M.shape[0]
    p = np.arange(n) if perm is None else perm
    c = size / n
    out = []
    for i in range(n):
        for j in range(n):
            v = M[p[i], p[j]]
            if binary:
                if v == 0:
                    continue
                col = "fill=ink"
            else:
                if abs(v) < 0.02 * scale:
                    continue
                col = "fill=" + rgb(diverging(v / scale))
            x, y = x0 + j * c, y0 - (i + 1) * c
            out.append(f"\\path[{col}] {P(x, y)} rectangle {P(x + c + 0.3, y + c + 0.3)};")
    out.append(f"\\draw[line width=1.2\\px] {P(x0, y0 - size)} rectangle {P(x0 + size, y0)};")
    return "\n".join(out)


def cap(x, y, text, anchor="north"):
    return label((x, y), text, anchor=anchor)


# ------------------------------------------------------------------ part 1: words and walks

def feat():
    """Hand-made node features: a small graph and the numbers computed from it."""
    G = nx.Graph([(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (3, 4), (5, 6), (5, 7), (6, 7)])
    pos = {1: (120, 110), 2: (50, 170), 3: (50, 50), 4: (190, 50), 5: (230, 150), 6: (310, 190), 7: (320, 100)}
    pos = {1: (110, 110), 2: (40, 170), 3: (40, 50), 4: (150, 20), 5: (200, 150), 6: (260, 200), 7: (270, 110)}
    deg = G.degree(1)
    tri = nx.triangles(G, 1)
    P2 = sum(1 / G.degree(j) for j in G[1]) / deg
    parts = [graph(pos, G.edges, highlight=[1]),
             cap(150, -8, r"node $i=1$")]
    rows = [(rf"degree\qquad $k_1={deg}$", 190), (rf"triangles\qquad $t_1={tri}$", 140),
            (rf"return probability\qquad $(\mathbf P^2)_{{11}}={P2:.2f}$", 90)]
    for k, (t, y) in enumerate(rows):
        parts.append(node(f"f{k}", (570, y + 20), t, style="smallbox", w=360, h=40, extra="align=left, font=\\fsbody"))
    parts.append(label((570, 250), "features chosen by hand", size="fssmall"))
    parts.append(arrow((320, 110), (385, 110), style="arr"))
    build("feat", *parts, outdir=OUT)


def pipeline():
    """Hand-made features vs learned features, as two flows."""
    def row(y, mid_text, mid_style, mid_w, vec_label=None):
        parts = [node(f"a{y}", (80, y), "network", w=120, h=54, style="box"),
                 node(f"b{y}", (445, y), mid_text, w=mid_w, h=70, style="box", extra=mid_style),
                 node(f"c{y}", (820, y), "model", w=120, h=54, style="box"),
                 node(f"d{y}", (1020, y), "prediction", w=150, h=54, style="box")]
        parts += [arrow(f"(a{y}.east)", f"(b{y}.west)"), arrow(f"(b{y}.east)", f"(c{y}.west)", text=vec_label),
                  arrow(f"(c{y}.east)", f"(d{y}.west)")]
        return parts
    parts = row(190, r"features designed by hand\\[2\px]{\fssmall degree, triangles, \dots}", "", 330, r"{\fssmall $k_i,\,t_i,\dots$}")
    parts += row(60, r"embedding trained on data\\[2\px]{\fssmall a vector for every node}", "fill=hl", 330, r"{\fssmall $\bm x_i\in\mathbb{R}^d$}")
    parts += [label((0, 245), "before", anchor="west", size="fsbody"), label((0, 115), "representation learning", anchor="west", size="fsbody")]
    build("pipeline", *parts, outdir=OUT)


def analogy():
    pts = {"man": (210, 70), "woman": (250, 190), "king": (440, 100), "queen": (480, 220)}
    parts = []
    for k, p in pts.items():
        style = "vertex hl" if k == "queen" else "vertex"
        parts.append(vertex(k, p, "", style=style, size=16))
    parts.append(arrow("(man)", "(woman)", style="arr"))
    parts.append(arrow("(king)", "(queen)", style="arr"))
    parts.append(raw(f"\\draw[arr, dash pattern=on 5\\px off 4\\px] (man) -- (king);"))
    parts.append(raw(f"\\draw[arr, dash pattern=on 5\\px off 4\\px] (woman) -- (queen);"))
    for k, (dx, dy, anc) in {"man": (-12, -2, "east"), "woman": (-12, 2, "east"), "king": (12, -2, "west"), "queen": (12, 2, "west")}.items():
        x, y = pts[k]
        parts.append(label((x + dx, y + dy), k, anchor=anc, size="fsbody"))
    parts.append(label((218, 135), r"$\bm x_{\mathrm{woman}}-\bm x_{\mathrm{man}}$", anchor="east", size="fssmall"))
    parts.append(label((462, 165), r"$\bm x_{\mathrm{queen}}-\bm x_{\mathrm{king}}$", anchor="west", size="fssmall"))
    parts.append(label((335, 62), "royalty", size="fssmall", anchor="north"))
    build("analogy", *parts, outdir=OUT)


def sentence():
    words = ["chance", "favors", "only", "the", "prepared", "mind"]
    xs = [95 + 190 * i for i in range(6)]
    parts = []
    for i, (w, x) in enumerate(zip(words, xs)):
        sty = "fill=hl" if w in ("favors", "prepared") else ""
        parts.append(node(f"w{i}", (x, 70), w, w=150, h=48, style="box", extra=sty))
    parts.append(raw(f"\\draw[arr] (w1.north) to[out=60, in=120, looseness=1.0] (w4.north);"))
    parts.append(label((xs[2] + 95, 128), r"predict the context word", size="fssmall"))
    parts.append(label((xs[1], 6), "input: query", size="fssmall", anchor="north"))
    parts.append(label((xs[4], 6), "output: key", size="fssmall", anchor="north"))
    build("sentence", *parts, outdir=OUT)


def walkgraph():
    pos = {1: (60, 160), 2: (170, 215), 3: (180, 105), 4: (290, 175), 5: (300, 70), 6: (410, 140), 7: (430, 230), 8: (160, 20)}
    E = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (4, 7), (6, 7), (5, 6), (3, 8)]
    walk = [1, 3, 4, 2, 3, 5]
    parts = [graph(pos, E, highlight=set(walk))]
    # the walk, drawn over the edges
    for a, b in zip(walk, walk[1:]):
        parts.append(raw(f"\\draw[line width=3.4\\px, hlink] (v{a}) -- (v{b});"))
    steps = {}
    for k, v in enumerate(walk):
        steps.setdefault(v, []).append(str(k + 1))
    for v, ks in steps.items():
        parts.append(raw(f"\\node[font=\\fstick, anchor=south west, inner sep=1\\px] at ($(v{v}.north east)+(1bp,0)$) {{{','.join(ks)}}};"))
    parts.append(cap(250, -6, r"walk: $1\to3\to4\to2\to3\to5$"))
    build("walkgraph", *parts, outdir=OUT)


def walks_compare():
    """A 5x4 lattice with a plain walk (drifts away) and a PPR walk (returns to s)."""
    def panel(ox, path, jumps, tag):
        pos = {(i, j): (ox + 40 + i * 60, 30 + j * 60) for i in range(5) for j in range(4)}
        names = {k: f"{k[0]}{k[1]}" for k in pos}
        out = []
        for k, p in pos.items():
            sty = "vertex hl" if k == path[0] else "vertex"
            out.append(vertex(f"n{names[k]}", p, "", style=sty, size=12))
        out.append("\\begin{scope}[on background layer]")
        for (i, j) in pos:
            for di, dj in ((1, 0), (0, 1)):
                if (i + di, j + dj) in pos:
                    out.append(f"\\draw[edge, draw=rule] (n{names[(i, j)]}) -- (n{names[(i + di, j + dj)]});")
        out.append("\\end{scope}")
        for a, b in zip(path, path[1:]):
            dashed = (a, b) in jumps
            sty = "arr, draw=sbase, dash pattern=on 4\\px off 3\\px" if dashed else "arr, draw=ink"
            bend = "bend left=25" if dashed else ""
            out.append(f"\\draw[{sty}, {bend}] (n{names[a]}) to (n{names[b]});".replace(", ]", "]"))
        out.append(label((ox + 160, -4), tag, anchor="north", size="fssmall"))
        return "\n".join(out)
    plain = [(0, 1), (1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (4, 3), (3, 3), (3, 2)]
    ppr = [(0, 1), (1, 1), (1, 2), (0, 1), (0, 2), (0, 1), (1, 1), (2, 1), (0, 1)]
    jumps = {((1, 2), (0, 1)), ((0, 2), (0, 1)), ((2, 1), (0, 1))}
    build("walks-compare", panel(0, plain, set(), "plain walk"), panel(340, ppr, jumps, r"walk with restart at $s$ (dashed: jump to $s$)"), outdir=OUT)


# ------------------------------------------------------------------ part 2: hyperbolic

def growth():
    """Popularity-similarity growth: r = ln t, theta uniform, connect to the m nodes with the smallest s * theta_st."""
    rnd = random.Random(7)
    N, m = 60, 2
    th = [0.0] + [rnd.uniform(0, 2 * math.pi) for _ in range(N)]
    links = {}
    for t in range(2, N + 1):
        cand = []
        for s in range(1, t):
            d = abs(th[s] - th[t])
            d = min(d, 2 * math.pi - d)
            cand.append((s * d, s))
        links[t] = [s for _, s in sorted(cand)[: min(m, t - 1)]]
    R = 135
    parts = []
    for fi, T in enumerate((8, 20, 60)):
        cx, cy = 190 + fi * 390, 165
        pos = lambda t: (cx + R * math.log(t) / math.log(N) * math.cos(th[t]), cy + R * math.log(t) / math.log(N) * math.sin(th[t]))
        parts.append(f"\\draw[draw=rule, line width=1.5\\px] {P(cx, cy)} circle ({R * 0.75}bp);")
        for t in range(2, T + 1):
            for s in links[t]:
                new = t == T
                parts.append(f"\\draw[{'hlink, line width=2.6\\px' if new else 'line width=1\\px, draw=muted'}] {P(*pos(s))} -- {P(*pos(t))};")
        for t in range(1, T + 1):
            x, y = pos(t)
            if t == 1:
                x, y = cx, cy
            fill = "hl" if t == T else "white"
            parts.append(f"\\draw[fill={fill}, line width=1.2\\px] {P(x, y)} circle (3.4bp);")
        parts.append(label((cx, 2), rf"$t={T}$", anchor="north", size="fsbody"))
    build("growth", *parts, outdir=OUT)


def popsim():
    """Two forces: attach to a popular node (a hub), attach to similar nodes (angular neighbours)."""
    parts = []
    # popularity: a hub with many links, a newcomer linking to it
    hx, hy = 190, 120
    parts.append(vertex("hub", (hx, hy), "", size=44))
    for i in range(9):
        a = 2 * math.pi * i / 9 + 0.4
        parts.append(vertex(f"l{i}", (hx + 95 * math.cos(a), hy + 95 * math.sin(a)), "", size=14))
        parts.append(f"\\draw[edge] (hub) -- (l{i});")
    parts.append(vertex("new1", (hx + 215, hy), "", style="vertex hl", size=18))
    parts.append(f"\\draw[arr, line width=2.4\\px] (new1) -- {P(hx + 36, hy)};")
    parts.append(label((hx + 40, -16), "popular: many links already", anchor="north", size="fssmall"))
    # similarity: nodes on a ring by angle, newcomer links to its angular neighbours
    cx, cy, R = 700, 120, 95
    n = 12
    pts = [(cx + R * math.cos(2 * math.pi * i / n), cy + R * math.sin(2 * math.pi * i / n)) for i in range(n)]
    for i, q in enumerate(pts):
        parts.append(vertex(f"s{i}", q, "", style="vertex hlc" if i in (2, 3) else "vertex", size=18))
    na = 2 * math.pi * 2.5 / n
    npos = (cx + 150 * math.cos(na), cy + 150 * math.sin(na))
    parts.append(vertex("new2", npos, "", style="vertex hl", size=18))
    parts.append("\\draw[line width=2.4\\px, hlink] (new2) -- (s2); \\draw[line width=2.4\\px, hlink] (new2) -- (s3);")
    parts.append(label((cx, -16), "similar: close in angle", anchor="north", size="fssmall"))
    build("popsim", *parts, outdir=OUT)


def communities():
    def ring(ox, n, k, tag, R):
        cx, cy = ox + 190, 140
        parts = [f"\\draw[draw=muted, dash pattern=on 5\\px off 4\\px, line width=1.5\\px] {P(cx, cy)} circle ({(R + 26) * 0.75}bp);"]
        pts = [(cx + R * math.cos(2 * math.pi * i / n + 0.3), cy + R * math.sin(2 * math.pi * i / n + 0.3)) for i in range(n)]
        for i, p in enumerate(pts):
            parts.append(vertex(f"c{ox}_{i}", p, "", style="vertex hl" if i == 0 else "vertex", size=15))
        parts.append("\\begin{scope}[on background layer]")
        targets = [int(round(1 + i * (n - 2) / (k - 1))) if n - 1 > k else i + 1 for i in range(k)]
        targets = sorted(set(targets))[:k] if n - 1 > k else list(range(1, n))
        for j in targets:
            parts.append(f"\\draw[line width=2.2\\px, hlink] (c{ox}_0) -- (c{ox}_{j});")
        parts.append("\\end{scope}")
        parts.append(label((cx, 0), tag, anchor="north", size="fssmall"))
        return "\n".join(parts)
    build("communities", ring(0, 16, 6, r"large community: 16 nodes", 105), ring(380, 8, 6, r"small community: 8 nodes", 62), outdir=OUT)


def circumference():
    xs = [i / 20 for i in range(0, 101)]
    build("circumference", lineplot(
        [{"x": xs, "y": [2 * math.pi * math.sinh(x) for x in xs], "style": "new"},
         {"x": xs, "y": [2 * math.pi * x for x in xs], "style": "draw=ink, dash pattern=on 6\\px off 4\\px"}],
        w=330, h=250, xlabel=r"radius $r$", ylabel=r"circumference $C(r)$", legend=None, xmin=0, xmax=5, ymin=0, ymax=480,
        after=r"\node[note, text=snew, anchor=south east] at (axis cs:4.9,300) {hyperbolic $2\pi\sinh r$};"
              r"\node[note, anchor=south east] at (axis cs:4.9,50) {Euclidean $2\pi r$};"), outdir=OUT)


def geodesic(a, b, n=14):
    """Points along the hyperbolic geodesic between a and b (unit-disk coordinates)."""
    (ax, ay), (bx, by) = a, b
    if abs(ax * by - ay * bx) < 1e-9:
        return [(ax + (bx - ax) * t / n, ay + (by - ay) * t / n) for t in range(n + 1)]
    r2 = ax * ax + ay * ay
    cx_, cy_ = ax / r2, ay / r2            # inverse point of a
    # circumcentre of a, b, inverse(a)
    def circ(p, q, r):
        d = 2 * (p[0] * (q[1] - r[1]) + q[0] * (r[1] - p[1]) + r[0] * (p[1] - q[1]))
        ux = ((p[0] ** 2 + p[1] ** 2) * (q[1] - r[1]) + (q[0] ** 2 + q[1] ** 2) * (r[1] - p[1]) + (r[0] ** 2 + r[1] ** 2) * (p[1] - q[1])) / d
        uy = ((p[0] ** 2 + p[1] ** 2) * (r[0] - q[0]) + (q[0] ** 2 + q[1] ** 2) * (p[0] - r[0]) + (r[0] ** 2 + r[1] ** 2) * (q[0] - p[0])) / d
        return ux, uy
    ox, oy = circ(a, b, (cx_, cy_))
    R = math.hypot(ax - ox, ay - oy)
    t0, t1 = math.atan2(ay - oy, ax - ox), math.atan2(by - oy, bx - ox)
    dt = (t1 - t0 + math.pi) % (2 * math.pi) - math.pi
    return [(ox + R * math.cos(t0 + dt * t / n), oy + R * math.sin(t0 + dt * t / n)) for t in range(n + 1)]


def tree_disk():
    """A tree in the Poincare disk: depth d at hyperbolic radius 0.9 d; edges are geodesics."""
    depth_max = 5
    nodes, edges_ = [], []
    def build_tree(d, a0, a1, parent):
        a = (a0 + a1) / 2
        idx = len(nodes)
        nodes.append((d, a))
        if parent is not None:
            edges_.append((parent, idx))
        if d == depth_max:
            return
        k = 3 if d == 0 else 2
        w = (a1 - a0) / k
        for i in range(k):
            build_tree(d + 1, a0 + i * w, a0 + (i + 1) * w, idx)
    build_tree(0, 0, 2 * math.pi, None)
    cx, cy, R = 200, 200, 190
    unit = [(math.tanh(0.45 * d) * math.cos(a), math.tanh(0.45 * d) * math.sin(a)) for d, a in nodes]
    out = [f"\\draw[line width=2\\px, draw=ink] {P(cx, cy)} circle ({R * 0.75}bp);"]
    for a, b in edges_:
        pts = geodesic(unit[a], unit[b])
        path = " -- ".join(P(cx + R * x, cy + R * y) for x, y in pts)
        out.append(f"\\draw[line width=0.9\\px, draw=ink] {path};")
    for i, (x, y) in enumerate(unit):
        r = 4.2 if nodes[i][0] <= 2 else 2.2
        out.append(f"\\draw[fill={'hl' if i == 0 else 'white'}, line width=0.9\\px] {P(cx + R * x, cy + R * y)} circle ({r * 0.75}bp);")
    build("tree-disk", *out, outdir=OUT)


def tree_plain():
    out = []
    depth_max = 4
    pos = {}
    def place(d, i, x0, x1):
        x = (x0 + x1) / 2
        pos[(d, i)] = (x, 190 - d * 44)
        if d < depth_max:
            place(d + 1, 2 * i, x0, x)
            place(d + 1, 2 * i + 1, x, x1)
    place(0, 0, 0, 360)
    for (d, i), p in pos.items():
        if d < depth_max:
            for c in (2 * i, 2 * i + 1):
                out.append(f"\\draw[line width=1.1\\px] {P(*p)} -- {P(*pos[(d + 1, c)])};")
    for (d, i), p in pos.items():
        out.append(f"\\draw[fill={'hl' if d == 0 else 'white'}, line width=1.1\\px] {P(*p)} circle ({(5 if d < 3 else 3.6) * 0.75}bp);")
    out.append(label((380, 190), r"depth 0", anchor="west", size="fstick"))
    out.append(label((380, 14), r"depth 4: $2^4=16$ nodes", anchor="west", size="fstick"))
    build("tree-plain", *out, outdir=OUT)


# ------------------------------------------------------------------ part 3: spectral

def compress():
    parts = [node("A", (90, 100), r"\fslarge$\mathbf A$", w=140, h=140),
             label((90, 10), r"$N\times N$: $N^2$ numbers", anchor="north", size="fssmall"),
             label((210, 100), r"\fslarge$\approx$"),
             node("U", (290, 100), r"\fslarge$\mathbf U$", w=60, h=140, extra="fill=hl"),
             label((290, 10), r"$N\times d$", anchor="north", size="fssmall"),
             node("UT", (445, 100), r"\fslarge$\mathbf U^{\top}$", w=140, h=60, extra="fill=hl"),
             label((445, 55), r"$d\times N$", anchor="north", size="fssmall"),
             label((560, 100), r"$d\ll N$: only $Nd$ numbers are kept", anchor="west", size="fsbody")]
    build("compress", *parts, outdir=OUT)


def layers():
    S = 225
    parts = []
    xs = [0, 285, 565, 845]
    mats = [A] + [LAM[k] * np.outer(U[:, k], U[:, k]) for k in range(3)]
    names = [r"$\mathbf A$"] + [rf"$\lambda_{k + 1}\mathbf u_{k + 1}\mathbf u_{k + 1}^{{\top}}$" for k in range(3)]
    for i, (x, M, nm) in enumerate(zip(xs, mats, names)):
        parts.append(heat(M, x, S, S, perm=ORDER, scale=1.0, binary=(i == 0)))
        extra = f",\\ \\lambda_{i}={LAM[i - 1]:.1f}" if i else ""
        parts.append(cap(x + S / 2, -6, nm if i == 0 else nm.replace("$", "$", 1)))
    for x, s in ((S + 30, r"\fslarge$=$"), (S + 310, r"\fslarge$+$"), (S + 590, r"\fslarge$+$")):
        parts.append(label((x, S / 2), s))
    parts.append(label((845 + S + 40, S / 2), r"\fslarge$+\cdots$", anchor="west"))
    for i in range(1, 4):
        parts.append(label((xs[i] + S / 2, -34), rf"$\lambda_{i}={LAM[i - 1]:.1f}$", anchor="north", size="fssmall"))
    build("layers", *parts, outdir=OUT)


def recon():
    S = 190
    parts, xs = [], [0, 245, 490]
    for x, d, nm in zip(xs, (None, 2, 6), (r"$\mathbf A$", r"$\mathbf A_{2}$", r"$\mathbf A_{6}$")):
        M = A if d is None else reconstruct(d)
        parts.append(heat(M, x, S, S, perm=ORDER, scale=1.0, binary=d is None))
        parts.append(cap(x + S / 2, -6, nm))
    parts.append(label((xs[1] - 28, S / 2), r"\fslarge$\to$"))
    parts.append(label((xs[2] - 28, S / 2), r"\fslarge$\to$"))
    build("recon", *parts, outdir=OUT)


def spectrum():
    vals = [float(v) for v in LAM[:12]]
    build("spectrum", vecdots(vals, labels=[str(i + 1) for i in range(12)], highlight=[0, 1], yticks=[-10, 0, 10, 20], unit=8, step=27, ymin=-14, ymax=23),
          label((250, 150), r"$\lambda_k$, ordered by $|\lambda_k|$", size="fssmall"), outdir=OUT)


def error_curve():
    ds = list(range(0, 35))
    err = [float(np.sum(LAM[d:] ** 2)) for d in ds]
    assert abs(err[0] - np.sum(A ** 2)) < 1e-6          # ||A||_F^2 = sum of squares of the eigenvalues
    assert abs(err[6] - np.sum((A - reconstruct(6)) ** 2)) < 1e-6
    build("error", lineplot([{"x": ds, "y": err, "style": "new"}], w=330, h=230, xlabel=r"kept terms $d$",
                            ylabel=r"$\|\mathbf A-\mathbf A_d\|_F^{\,2}$", legend=None, xmin=0, xmax=34, ymin=0,
                            extra=r"xtick={0,10,20,30}"), outdir=OUT)


def cuts():
    """Two cliques joined by one edge, plus a pendant node. Two cuts of one edge each."""
    posA = {f"a{i}": (130 + 70 * math.cos(2 * math.pi * i / 5 + 1.2), 130 + 70 * math.sin(2 * math.pi * i / 5 + 1.2)) for i in range(5)}
    posB = {f"b{i}": (430 + 70 * math.cos(2 * math.pi * i / 5 + 3.1), 130 + 70 * math.sin(2 * math.pi * i / 5 + 3.1)) for i in range(5)}
    posP = {"p": (130 + 140 * math.cos(1.2 + 2 * math.pi * 2 / 5), 130 + 140 * math.sin(1.2 + 2 * math.pi * 2 / 5))}
    pos = {**posA, **posB, **posP}
    E = [(u, v) for grp in (posA, posB) for u in grp for v in grp if u < v] + [("a4", "b0"), ("p", "a2")]
    # find which A node is nearest to p and which pair is the bridge for readability
    def panel(ox, S, cutE, tag):
        parts = []
        for k, (x, y) in pos.items():
            sty = "vertex hl" if k in S else "vertex hlc"
            parts.append(vertex(f"{k}x{ox}", (x + ox, y), "", style=sty, size=18))
        parts.append("\\begin{scope}[on background layer]")
        for u, v in E:
            cut = (u, v) in cutE or (v, u) in cutE
            sty = "line width=3\\px, draw=sbase, dash pattern=on 5\\px off 3\\px" if cut else "line width=1.2\\px, draw=ink"
            parts.append(f"\\draw[{sty}] ({u}x{ox}) -- ({v}x{ox});")
        parts.append("\\end{scope}")
        parts.append(label((ox + 260, -2), tag, anchor="north", size="fssmall"))
        return "\n".join(parts)
    bridge = {("a4", "b0")}
    pend = {("p", "a2")}
    build("cuts", panel(0, {"p"}, pend, ""), outdir=OUT)
    build("cuts-bridge", panel(0, set(posA) | {"p"}, bridge, ""), outdir=OUT)


def indicator():
    xs = [math.sqrt(5 / 6)] * 6 + [-math.sqrt(6 / 5)] * 5
    labs = ["p"] + [f"a_{i + 1}" for i in range(5)] + [f"b_{i + 1}" for i in range(5)]
    hl = {i: "hl" for i in range(6)} | {i: "hlc" for i in range(6, 11)}
    build("indicator", vecdots(xs, labels=labs, highlight=hl, yticks=[-1, 0, 1], unit=70, step=34, ymin=-1.3, ymax=1.2), outdir=OUT)


def fiedler():
    vals = [float(FIEDLER[i]) for i in ORDER]
    sign = 1 if CLUB[ORDER[0]] == 0 else -1          # put Mr. Hi's faction on the left
    vals = [sign * v for v in vals]
    labs = [str(int(i) + 1) for i in ORDER]
    hl = {k: ("hl" if CLUB[i] == 0 else "hlc") for k, i in enumerate(ORDER)}
    errors = sum(1 for k, i in enumerate(ORDER) if (vals[k] < 0) != (CLUB[i] == 0))
    print("fiedler: sign disagrees with the club for", errors, "of 34 nodes")
    build("fiedler", vecdots(vals, labels=labs, highlight=hl, yticks=[-0.2, 0, 0.2], unit=210, step=29, ymin=-0.4, ymax=0.4), outdir=OUT)


if __name__ == "__main__":
    for f in (feat, pipeline, analogy, sentence, walkgraph, walks_compare, popsim, growth, communities, circumference,
              tree_disk, tree_plain, compress, layers, recon, spectrum, error_curve, cuts, indicator, fiedler):
        print("building", f.__name__)
        f()
    print("figures written to", OUT)

"""Build every figure of the m08 deck:  python3 figures/make_figures.py  (from slides/m08).
Type is 1.45x the skill default (classroom size); the sizes are set in PRE below.

Real data where a figure shows a result (karate club, the growth model with a fixed seed);
hand layouts for the explanatory drawings. See ~/.claude/skills/slide-math/FIGURES.md.
"""

import json
import math
import random
import sys
from pathlib import Path

import networkx as nx
import numpy as np

sys.path.insert(0, str(Path.home() / ".claude/skills/slide-math/figkit"))
from figkit import P, arrow, build, edge, graph, label, lineplot, node, raw, vecdots, vertex  # noqa: E402

OUT = Path(__file__).resolve().parent

# Classroom type: figure text 1.6x the skill default, matching the deck's 34 px body.
PRE = (r"\renewcommand\fstick{\fontsize{20\px}{24\px}\selectfont}"
       r"\renewcommand\fssmall{\fontsize{25\px}{30\px}\selectfont}"
       r"\renewcommand\fslabel{\fontsize{28\px}{33\px}\selectfont}"
       r"\renewcommand\fsbody{\fontsize{34\px}{41\px}\selectfont}"
       r"\renewcommand\fslarge{\fontsize{42\px}{49\px}\selectfont}"
       r"\tikzset{arr/.style={-{Stealth[length=10bp, width=8bp]}, line width=1.8bp},"
       r" edge/.style={line width=2\px}, vertex/.append style={line width=2\px}}")


def B(name, *parts):
    return build(name, *parts, outdir=OUT, preamble=PRE)


# ------------------------------------------------------------------ data

def karate():
    G = nx.karate_club_graph()
    A = nx.to_numpy_array(G, weight=None)      # the unweighted karate club
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

WALK_POS = {1: (60, 160), 2: (170, 215), 3: (180, 105), 4: (290, 175), 5: (300, 70), 6: (410, 140), 7: (430, 230), 8: (160, 20)}
WALK_E = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (4, 7), (6, 7), (5, 6), (3, 8)]


def feat():
    """Hand-made node features: a small graph, and the vector of numbers computed from node 1."""
    G = nx.Graph([(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (3, 4), (5, 6), (5, 7), (6, 7)])
    pos = {1: (110, 140), 2: (40, 225), 3: (30, 70), 4: (125, 15), 5: (205, 150), 6: (215, 245), 7: (285, 95)}
    deg, tri = G.degree(1), nx.triangles(G, 1)
    P2 = sum(1 / G.degree(j) for j in G[1]) / deg
    parts = [graph(pos, G.edges, highlight=[1], size=42)]
    cells = [(f"{deg}", r"$k_1$"), (f"{tri}", r"$t_1$"), (f"{P2:.2f}", r"$(\mathbf P^2)_{11}$")]
    parts.append(label((420, 290), r"$\mathbf x_1$", size="fsbody"))
    for k, (val, lab) in enumerate(cells):
        y = 220 - 62 * k
        parts.append(node(f"c{k}", (420, y), f"${val}$" if k < 2 else f"${val}$", style="box", w=96, h=56, extra="font=\\fsbody"))
        parts.append(label((482, y), lab, anchor="west", size="fslabel"))
    parts.append(arrow((330, 140), (362, 140)))
    B("feat", *parts)


def pipeline():
    """Hand-made features vs learned features, as two flows."""
    def row(y, mid_text, mid_style, vec_label):
        parts = [node(f"a{y}", (70, y), "network", w=140, h=96, style="box", extra="font=\\fsbody"),
                 node(f"b{y}", (410, y), mid_text, w=470, h=118, style="box", extra=mid_style + ", font=\\fsbody"),
                 node(f"c{y}", (825, y), "model", w=130, h=96, style="box", extra="font=\\fsbody"),
                 node(f"d{y}", (1060, y), "prediction", w=200, h=96, style="box", extra="font=\\fsbody")]
        parts += [arrow(f"(a{y}.east)", f"(b{y}.west)"), arrow(f"(b{y}.east)", f"(c{y}.west)", text=vec_label),
                  arrow(f"(c{y}.east)", f"(d{y}.west)")]
        return parts
    parts = row(200, r"features designed by hand\\[4\px]{\fslabel degree, triangles, \dots}", "", r"$k_i,\,t_i,\dots$")
    parts += row(30, r"embedding trained on data\\[4\px]{\fslabel a vector for every node}", "fill=hl", r"$\mathbf x_i\in\mathbb{R}^d$")
    B("pipeline", *parts)


def analogy():
    pts = {"man": (115, 70), "woman": (175, 230), "king": (365, 95), "queen": (425, 255)}
    parts = []
    for k, p in pts.items():
        parts.append(vertex(k, p, "", style="vertex hl" if k == "queen" else "vertex", size=26))
    parts.append(arrow("(man)", "(woman)"))
    parts.append(arrow("(king)", "(queen)"))
    parts.append("\\draw[arr, dash pattern=on 5bp off 4bp] (man) -- (king);")
    parts.append("\\draw[arr, dash pattern=on 5bp off 4bp] (woman) -- (queen);")
    for k, (dx, dy, anc) in {"man": (-20, 0, "east"), "woman": (-20, 0, "east"), "king": (20, -4, "west"), "queen": (20, 0, "west")}.items():
        x, y = pts[k]
        parts.append(label((x + dx, y + dy), k, anchor=anc, size="fsbody"))
    parts.append(label((282, 168), "same\\\\direction", size="fssmall", anchor="center", extra="align=center"))
    parts.append(label((240, 60), "royalty", size="fssmall", anchor="north"))
    B("analogy", *parts)


def sentence():
    """A sentence, one input word and one output word, each with its vector."""
    words = ["chance", "favors", "only", "the", "prepared", "mind"]
    xs = [92 + 190 * i for i in range(6)]
    parts = []
    for i, (w, x) in enumerate(zip(words, xs)):
        sty = "fill=hl, " if w in ("favors", "prepared") else ""
        parts.append(node(f"w{i}", (x, 190), w, w=178, h=62, style="box", extra=sty + "font=\\fsbody"))
    parts.append("\\draw[arr] (w1.north) to[out=50, in=130, looseness=0.75] (w4.north);")
    parts.append(label(((xs[1] + xs[4]) / 2, 268), "word pair from the text", size="fssmall", anchor="south"))
    for i, lab in ((1, r"$\mathbf u_i$"), (4, r"$\mathbf v_j$")):
        for k in range(4):
            parts.append(f"\\draw[fill=hl, line width=1.5\\px] {P(xs[i] - 22, 140 - 27 * k)} rectangle {P(xs[i] + 22, 113 - 27 * k)};")
        parts.append(label((xs[i] - 36, 86), lab, anchor="east", size="fsbody") if i == 1 else label((xs[i] + 36, 86), lab, anchor="west", size="fsbody"))
    parts.append(label((xs[1], 6), "input (query)", size="fssmall", anchor="north"))
    parts.append(label((xs[4], 6), "output (key)", size="fssmall", anchor="north"))
    parts.append(arrow((xs[1] + 36, 86), (xs[4] - 36, 86), text=r"score $\mathbf u_i^\top\mathbf v_j$"))
    B("sentence", *parts)


def contrast():
    """Pull a real pair together, push a random pair apart."""
    fav, prep, water = (120, 150), (300, 260), (420, 70)
    parts = [vertex("fav", fav, "", style="vertex hl", size=34), vertex("prep", prep, "", size=34), vertex("water", water, "", size=34)]
    for k, p in enumerate([(220, 40), (500, 190), (480, 300), (60, 280), (200, 330)]):
        parts.append(vertex(f"g{k}", p, "", style="vertex grey", size=20))
    parts.append("\\draw[arr, shorten >=19bp, shorten <=19bp, line width=2.6bp] (prep) -- (fav);")
    parts.append(f"\\draw[arr, draw=sbase, line width=2.6bp] (water) -- {P(535, 30)};")
    parts.append(label((fav[0], fav[1] - 30), r"favors", anchor="north", size="fsbody"))
    parts.append(label((prep[0], prep[1] + 28), r"prepared", anchor="south", size="fsbody"))
    parts.append(label((water[0] - 8, water[1] + 28), r"water", anchor="south", size="fsbody"))
    parts.append(label((236, 190), r"label 1: pull", anchor="west", size="fssmall"))
    parts.append(label((470, 5), r"label 0: push", anchor="north", size="fssmall", extra="text=sbase"))
    B("contrast", *parts)


def walkgraph():
    """The graph with one walk drawn on it, and the walk written as a sentence."""
    walk = [1, 3, 4, 2, 3, 5]
    pos = {k: (x * 1.1 + 20, y * 1.1 + 120) for k, (x, y) in WALK_POS.items()}
    parts = [graph(pos, WALK_E, highlight=set(walk), size=40)]
    for a, b in zip(walk, walk[1:]):
        parts.append(f"\\draw[line width=5\\px, hlink] (v{a}) -- (v{b});")
    for k, v in enumerate(walk):
        parts.append(node(f"s{k}", (36 + 82 * k, 40), f"${v}$", style="box", w=62, h=58, extra="font=\\fsbody, fill=hl"))
        if k:
            parts.append(arrow(f"(s{k-1}.east)", f"(s{k}.west)"))
    B("walkgraph", *parts)


def deepwalk():
    """network -> random walks -> pairs in a window -> word2vec vectors."""
    s = 0.46
    pos = {k: (x * s + 8, y * s + 105) for k, (x, y) in WALK_POS.items()}
    parts = [graph(pos, WALK_E, size=32)]
    heads = [(105, r"\textbf{network}"), (430, r"\textbf{1  random walks}"), (755, r"\textbf{2  pairs}"), (1042, r"\textbf{3  word2vec}")]
    for x, t in heads:
        parts.append(label((x, 318), t, size="fsbody"))
    walks = [[1, 3, 4, 2, 3, 5], [4, 6, 7, 4, 2, 3], [8, 3, 5, 4, 7, 6]]
    for r, w in enumerate(walks):
        y = 235 - 68 * r
        for k, v in enumerate(w):
            fill = "fill=hl, " if (r == 0 and k == 2) else ""
            parts.append(node(f"w{r}{k}", (284 + 52 * k, y), f"${v}$", style="smallbox", w=46, h=52, extra=fill + "font=\\fslabel"))
    parts.append(f"\\draw[zoom] {P(284 + 52 - 28, 235 - 34)} rectangle {P(284 + 156 + 28, 235 + 34)};")
    parts.append(label((430, 52), "window of one step", size="fssmall", anchor="north"))
    pairs = [("4", "3", True), ("4", "2", True), ("3", "1", False), ("3", "4", False), ("2", "4", False), ("2", "3", False)]
    for k, (a, b, hl) in enumerate(pairs):
        x, y = 690 + 118 * (k % 2), 235 - 68 * (k // 2)
        fill = "fill=hl, " if hl else ""
        parts.append(node(f"p{k}", (x, y), f"$({a},{b})$", style="smallbox", w=108, h=52, extra=fill + "font=\\fslabel"))
    parts.append(label((755, 52), "(node, context)", size="fssmall", anchor="north"))
    parts.append(node("emb", (1042, 160), "", style="box", w=250, h=236))
    pts = {1: (960, 108), 2: (966, 190), 3: (1018, 148), 8: (1030, 226), 4: (1096, 108), 5: (1130, 172), 6: (1128, 238), 7: (1076, 244)}
    for k, p in pts.items():
        parts.append(vertex(f"e{k}", p, f"${k}$", size=34))
    parts.append(label((1042, 24), r"vectors $\mathbf u_i$ (schematic)", size="fssmall", anchor="north"))
    parts.append(arrow((208, 160), (258, 160)))
    parts.append(arrow((560, 160), (655, 160)))
    parts.append(arrow((862, 160), (912, 160)))
    B("deepwalk", *parts)


def walks_compare():
    """A 5x4 lattice with a plain walk (drifts away) and a walk with restart (returns to s), stacked."""
    def panel(oy, path, jumps, tag, tag_y):
        pos = {(i, j): (30 + i * 85, oy + j * 48) for i in range(5) for j in range(4)}
        names = {k: f"{k[0]}{k[1]}" for k in pos}
        out = []
        for k, p in pos.items():
            out.append(vertex(f"n{oy}{names[k]}", p, "", style="vertex hl" if k == path[0] else "vertex", size=20))
        out.append("\\begin{scope}[on background layer]")
        for (i, j) in pos:
            for di, dj in ((1, 0), (0, 1)):
                if (i + di, j + dj) in pos:
                    out.append(f"\\draw[edge, draw=rule] (n{oy}{names[(i, j)]}) -- (n{oy}{names[(i + di, j + dj)]});")
        out.append("\\end{scope}")
        for a, b in zip(path, path[1:]):
            dashed = (a, b) in jumps
            sty = "arr, draw=sbase, dash pattern=on 4bp off 3bp" if dashed else "arr, draw=ink"
            bend = ", bend left=25" if dashed else ""
            out.append(f"\\draw[{sty}{bend}] (n{oy}{names[a]}) to (n{oy}{names[b]});")
        out.append(label((0, tag_y), tag, anchor="west", size="fssmall"))
        return "\n".join(out)
    plain = [(0, 1), (1, 1), (2, 1), (2, 2), (3, 2), (4, 2), (4, 3), (3, 3), (3, 2)]
    ppr = [(0, 1), (1, 1), (1, 2), (0, 1), (0, 2), (0, 1), (1, 1), (2, 1), (0, 1)]
    jumps = {((1, 2), (0, 1)), ((0, 2), (0, 1)), ((2, 1), (0, 1))}
    B("walks-compare", panel(235, plain, set(), "plain walk", 235 + 144 + 36),
      panel(0, ppr, jumps, r"walk with restart at $s$ (dashed: jump to $s$)", 144 + 36))


def ppr_step():
    """One step of a walk with restart: jump to s with probability alpha, else move to a random neighbour."""
    cur, s = (270, 130), (70, 230)
    parts = [vertex("s", s, r"$s$", style="vertex hl", size=44), vertex("cur", cur, "", size=44)]
    for k, p in enumerate([(480, 235), (510, 130), (480, 25)]):
        parts.append(vertex(f"n{k}", p, "", size=36))
        parts.append(f"\\draw[arr, shorten >=3bp, shorten <=3bp] (cur) -- (n{k});")
    parts.append("\\draw[arr, draw=sbase, dash pattern=on 5bp off 4bp, shorten >=3bp, shorten <=3bp] (cur) -- (s);")
    parts.append(label((cur[0], cur[1] - 36), "current node", anchor="north", size="fssmall"))
    parts.append(label((100, 150), r"prob. $\alpha$", anchor="west", size="fssmall", extra="text=sbase"))
    parts.append(label((388, 186), r"prob. $1-\alpha$", anchor="center", size="fssmall", extra="fill=white, inner sep=2bp"))
    B("ppr-step", *parts)


# ------------------------------------------------------------------ lab output

def lesmis():
    """2-D PCA of the Les Miserables embedding of the lab (figures/lesmis_pca.json, made by lesmis_embed.py)."""
    d = json.loads((OUT / "lesmis_pca.json").read_text())
    xy, near = d["xy"], set(d["near_valjean"])
    xs, ys = [v[0] for v in xy.values()], [v[1] for v in xy.values()]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    W, H = 520, 390
    sx = lambda x: 20 + (x - x0) / (x1 - x0) * W
    sy = lambda y: 20 + (y - y0) / (y1 - y0) * H
    parts = [f"\\draw[line width=2\\px] {P(0, 0)} rectangle {P(W + 40, H + 40)};"]
    for k, (x, y) in xy.items():
        if k == "Valjean":
            sty = "fill=hl, line width=2\\px"
        elif k in near:
            sty = "fill=hlc, line width=2\\px"
        else:
            sty = "fill=white, line width=1.4\\px"
        parts.append(f"\\draw[{sty}] {P(sx(x), sy(y))} circle ({(8 if k == 'Valjean' else 5.5) * 0.75}bp);")
    offs = {"Valjean": (0, -15, "north"), "Javert": (8, 12, "south west"), "Marius": (-6, 12, "south"), "Cosette": (6, 12, "south west"),
            "Myriel": (0, -12, "north"), "Gavroche": (0, -12, "north"), "Fantine": (-8, 10, "south east")}
    for k, (dx, dy, a) in offs.items():
        x, y = xy[k]
        parts.append(label((sx(x) + dx, sy(y) + dy), k, anchor=a, size="fssmall"))
    B("lesmis", *parts)


# ------------------------------------------------------------------ part 2: hyperbolic

def pa_vs_ps():
    """Preferential attachment (popularity only) next to popularity and similarity."""
    def panel(ox, ps):
        out = []
        hubs = {"h1": (110, 190, 58, 7), "h2": (420, 175, 46, 5)}
        for name, (hx, hy, hs, nleaf) in hubs.items():
            out.append(vertex(f"{name}_{ox}", (ox + hx, hy), "", size=hs))
            for i in range(nleaf):
                a = 2 * math.pi * i / nleaf + (0.9 if name == "h1" else 0.2)
                r = 78 if name == "h1" else 66
                lx, ly = ox + hx + r * math.cos(a), hy + r * math.sin(a)
                out.append(vertex(f"{name}l{i}_{ox}", (lx, ly), "", size=20))
                out.append(f"\\draw[edge] ({name}_{ox}) -- ({name}l{i}_{ox});")
        out.append(vertex(f"new_{ox}", (ox + 300, 62), "", style="vertex hl", size=30))
        if not ps:
            out.append(f"\\draw[arr, line width=3.4bp, draw=hlink, shorten >=4bp] (new_{ox}) -- (h1_{ox});")
        else:
            out.append(f"\\draw[arr, line width=3.4bp, draw=hlink, shorten >=4bp] (new_{ox}) -- (h2_{ox});")
            out.append(f"\\draw[arr, line width=3.4bp, draw=hlink, shorten >=4bp] (new_{ox}) -- (h2l3_{ox});")
            out.append(f"\\draw[zoom] {P(ox + 232, -2)} rectangle {P(ox + 548, 292)};")
        return "\n".join(out)
    parts = [panel(0, False), panel(606, True)]
    for ox in (0, 606):
        parts.append(label((ox + 110, 190 + 78 + 30), "popular", anchor="south", size="fssmall"))
        parts.append(label((ox + 420, 175 + 66 + 26), "less popular", anchor="south", size="fssmall"))
        parts.append(label((ox + 300 - 24, 62), "new node", anchor="east", size="fssmall"))
    parts.append(label((280, 372), r"\textbf{preferential attachment}", size="fsbody"))
    parts.append(label((886, 372), r"\textbf{popularity and similarity}", size="fsbody"))
    parts.append(label((280, -24), "links to the most popular node", anchor="north", size="fssmall"))
    parts.append(label((886, -24), "dashed box: nodes similar to the new node", anchor="north", size="fssmall"))
    B("pa-vs-ps", *parts)


def growth():
    """Popularity-similarity growth: r = ln t, theta uniform, connect to the m nodes with the smallest s * theta_st."""
    rnd = random.Random(7)
    N, m, T = 60, 2, 40
    th = [0.0] + [rnd.uniform(0, 2 * math.pi) for _ in range(N)]
    links = {}
    for t in range(2, N + 1):
        cand = []
        for s in range(1, t):
            d = abs(th[s] - th[t])
            d = min(d, 2 * math.pi - d)
            cand.append((s * d, s))
        links[t] = [s for _, s in sorted(cand)[: min(m, t - 1)]]
    R = 190
    cx, cy = 215, 205
    rr = lambda t: R * math.log(t) / math.log(T)
    pos = lambda t: (cx + rr(t) * math.cos(th[t]), cy + rr(t) * math.sin(th[t]))
    parts = [f"\\draw[draw=rule, line width=2\\px] {P(cx, cy)} circle ({R * 0.75}bp);"]
    for t in range(2, T + 1):
        for s in links[t]:
            new = t == T
            parts.append(f"\\draw[{'hlink, line width=4\\px' if new else 'line width=1.3\\px, draw=muted'}] {P(*pos(s))} -- {P(*pos(t))};")
    for t in range(1, T + 1):
        x, y = (cx, cy) if t == 1 else pos(t)
        parts.append(f"\\draw[fill={'hl' if t == T else 'white'}, line width=1.6\\px] {P(x, y)} circle ({(8 if t == T else 5.5) * 0.75}bp);")
    ang = math.degrees(th[T])
    parts.append(f"\\draw[dash pattern=on 5bp off 4bp, line width=1.3bp] {P(cx, cy)} -- {P(cx + R + 10, cy)};")
    parts.append(f"\\draw[line width=1.3bp] {P(cx + 70, cy)} arc[start angle=0, end angle={ang}, radius={70 * 0.75}bp];")
    am = math.radians(ang / 2)
    parts.append(label((cx + 92 * math.cos(am), cy + 92 * math.sin(am)), r"$\theta_t$", size="fsbody"))
    mx, my = cx + rr(T) * 0.5 * math.cos(th[T]), cy + rr(T) * 0.5 * math.sin(th[T])
    parts.append(f"\\draw[line width=1.3bp, dash pattern=on 5bp off 4bp] {P(cx, cy)} -- {P(*pos(T))};")
    parts.append(label((mx - 10, my + 22), r"$r_t=\ln t$", size="fsbody", anchor="east", extra="fill=white, inner sep=2bp"))
    B("growth", *parts)


def communities():
    def ring(ox, n, k, tag, R):
        cx, cy = ox, 150
        parts = [f"\\draw[draw=muted, dash pattern=on 5bp off 4bp, line width=1.6bp] {P(cx, cy)} circle ({(R + 28) * 0.75}bp);"]
        pts = [(cx + R * math.cos(2 * math.pi * i / n + 0.3), cy + R * math.sin(2 * math.pi * i / n + 0.3)) for i in range(n)]
        for i, p in enumerate(pts):
            parts.append(vertex(f"c{ox}_{i}", p, "", style="vertex hl" if i == 0 else "vertex", size=22))
        parts.append("\\begin{scope}[on background layer]")
        targets = [int(round(1 + i * (n - 2) / (k - 1))) if n - 1 > k else i + 1 for i in range(k)]
        targets = sorted(set(targets))[:k] if n - 1 > k else list(range(1, n))
        for j in targets:
            parts.append(f"\\draw[line width=3.2\\px, hlink] (c{ox}_0) -- (c{ox}_{j});")
        parts.append("\\end{scope}")
        parts.append(label((cx, -(R + 28) + 150 - 10), tag, anchor="north", size="fssmall"))
        return "\n".join(parts)
    B("communities", ring(135, 16, 6, r"large community: 16 nodes", 98), ring(435, 8, 6, r"small community: 8 nodes", 64))


def circumference():
    xs = [i / 20 for i in range(0, 101)]
    B("circumference", lineplot(
        [{"x": xs, "y": [2 * math.pi * math.sinh(x) for x in xs], "style": "new"},
         {"x": xs, "y": [2 * math.pi * x for x in xs], "style": "draw=ink, dash pattern=on 6bp off 4bp"}],
        w=400, h=300, xlabel=r"radius $r$", ylabel=r"circumference $C(r)$", legend=None, xmin=0, xmax=5, ymin=0, ymax=480,
        after=r"\node[note, text=snew, anchor=south east] at (axis cs:4.9,300) {hyperbolic $2\pi\sinh r$};"
              r"\node[note, anchor=south east] at (axis cs:4.9,40) {Euclidean $2\pi r$};"))


def geodesic(a, b, n=14):
    """Points along the hyperbolic geodesic between a and b (unit-disk coordinates)."""
    (ax, ay), (bx, by) = a, b
    if abs(ax * by - ay * bx) < 1e-9:
        return [(ax + (bx - ax) * t / n, ay + (by - ay) * t / n) for t in range(n + 1)]
    r2 = ax * ax + ay * ay
    cx_, cy_ = ax / r2, ay / r2            # inverse point of a

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
    cx, cy, R = 205, 205, 200
    unit = [(math.tanh(0.45 * d) * math.cos(a), math.tanh(0.45 * d) * math.sin(a)) for d, a in nodes]
    out = [f"\\draw[line width=2.4\\px, draw=ink] {P(cx, cy)} circle ({R * 0.75}bp);"]
    for a, b in edges_:
        pts = geodesic(unit[a], unit[b])
        path = " -- ".join(P(cx + R * x, cy + R * y) for x, y in pts)
        out.append(f"\\draw[line width=1.2\\px, draw=ink] {path};")
    for i, (x, y) in enumerate(unit):
        r = 6.5 if nodes[i][0] <= 2 else 3.2
        out.append(f"\\draw[fill={'hl' if i == 0 else 'white'}, line width=1.2\\px] {P(cx + R * x, cy + R * y)} circle ({r * 0.75}bp);")
    B("tree-disk", *out)


def tree_plain():
    out = []
    depth_max = 4
    pos = {}

    def place(d, i, x0, x1):
        x = (x0 + x1) / 2
        pos[(d, i)] = (x, 300 - d * 70)
        if d < depth_max:
            place(d + 1, 2 * i, x0, x)
            place(d + 1, 2 * i + 1, x, x1)
    place(0, 0, 0, 480)
    for (d, i), p in pos.items():
        if d < depth_max:
            for c in (2 * i, 2 * i + 1):
                out.append(f"\\draw[line width=1.6\\px] {P(*p)} -- {P(*pos[(d + 1, c)])};")
    for (d, i), p in pos.items():
        out.append(f"\\draw[fill={'hl' if d == 0 else 'white'}, line width=1.6\\px] {P(*p)} circle ({(9 if d < 3 else 6) * 0.75}bp);")
    out.append(label((250, 4), r"depth $d$: $2^d$ nodes", anchor="north", size="fsbody"))
    B("tree-plain", *out)


# ------------------------------------------------------------------ part 3: spectral

def compress():
    parts = [node("A", (100, 215), r"\fslarge$\mathbf A$", w=180, h=180),
             label((100, 112), r"$N\times N$", anchor="north", size="fssmall"),
             label((100, 80), r"$N^2$ numbers", anchor="north", size="fssmall"),
             label((222, 215), r"\fslarge$\approx$"),
             node("U", (298, 215), r"\fslarge$\mathbf U$", w=76, h=180, extra="fill=hl"),
             label((298, 112), r"$N\times d$", anchor="north", size="fssmall"),
             node("UT", (444, 215), r"\fslarge$\mathbf U^{\top}$", w=180, h=76, extra="fill=hl"),
             label((444, 163), r"$d\times N$", anchor="north", size="fssmall"),
             label((371, 80), r"$Nd$ numbers, $d\ll N$", anchor="north", size="fssmall")]
    B("compress", *parts)


def layers():
    S = 175
    parts = []
    xs = [0, 230, 460, 690]
    mats = [A] + [LAM[k] * np.outer(U[:, k], U[:, k]) for k in range(3)]
    names = [r"$\mathbf A$"] + [rf"$\lambda_{k + 1}\mathbf u_{k + 1}\mathbf u_{k + 1}^{{\top}}$" for k in range(3)]
    for i, (x, M, nm) in enumerate(zip(xs, mats, names)):
        parts.append(heat(M, x, S, S, perm=ORDER, scale=1.0, binary=(i == 0)))
        parts.append(cap(x + S / 2, -8, nm))
    for x, s in ((S + 27, r"\fslarge$=$"), (S + 257, r"\fslarge$+$"), (S + 487, r"\fslarge$+$")):
        parts.append(label((x, S / 2), s))
    parts.append(label((690 + S + 28, S / 2), r"\fslarge$+\cdots$", anchor="west"))
    for i in range(1, 4):
        parts.append(label((xs[i] + S / 2, -44), rf"$\lambda_{i}={LAM[i - 1]:.1f}$", anchor="north", size="fssmall"))
    B("layers", *parts)


def recon():
    S = 150
    parts, xs = [], [0, 215, 430]
    for x, d, nm in zip(xs, (None, 2, 6), (r"$\mathbf A$", r"$\mathbf A_{2}$", r"$\mathbf A_{6}$")):
        M = A if d is None else reconstruct(d)
        parts.append(heat(M, x, S, S, perm=ORDER, scale=1.0, binary=d is None))
        parts.append(cap(x + S / 2, -8, nm))
    parts.append(label((xs[1] - 32, S / 2), r"\fslarge$\to$"))
    parts.append(label((xs[2] - 32, S / 2), r"\fslarge$\to$"))
    B("recon", *parts)


def spectrum():
    vals = [float(v) for v in LAM[:12]]
    B("spectrum", vecdots(vals, labels=[str(i + 1) for i in range(12)], highlight=[0, 1], yticks=[-10, 0, 10, 20], unit=9, step=30, ymin=-14, ymax=23, r=5.5),
      label((215, 215), r"$\lambda_k$ ordered by $|\lambda_k|$", size="fssmall"))


def error_curve():
    """The squared eigenvalues, with the dropped ones shaded, and the error as a function of d."""
    lam2 = [float(v) ** 2 for v in LAM]
    B("error-terms", vecdots(lam2, labels=[str(i + 1) if i + 1 in (1, 10, 20, 30) else r"\,"for i in range(34)],
                              highlight={i: "hl" for i in range(6, 34)}, yticks=[0, 20, 40], unit=3.6, step=15.5, r=3.6, ymin=-1, ymax=48),
      label((100, 190), r"$\lambda_k^2$", size="fsbody"),
      label((300, 100), r"dropped for $d=6$", size="fssmall"))
    ds = list(range(0, 35))
    err = [float(np.sum(LAM[d:] ** 2)) for d in ds]
    assert abs(err[0] - np.sum(A ** 2)) < 1e-6          # ||A||_F^2 = sum of squares of the eigenvalues
    assert abs(err[6] - np.sum((A - reconstruct(6)) ** 2)) < 1e-6
    after = (rf"\fill[ink] (axis cs:2,{err[2]:.4f}) circle (4.5bp); \fill[ink] (axis cs:6,{err[6]:.4f}) circle (4.5bp);"
             rf"\node[note, anchor=south west] at (axis cs:3,{err[2] + 6:.2f}) {{$d=2$}};"
             rf"\node[note, anchor=south west] at (axis cs:7,{err[6] + 8:.2f}) {{$d=6$}};")
    B("error", lineplot([{"x": ds, "y": err, "style": "new"}], w=400, h=170, xlabel=r"kept terms $d$",
                        ylabel=r"$\|\mathbf A-\mathbf A_d\|_F^{\,2}$", legend=None, xmin=0, xmax=34, ymin=0,
                        extra=r"xtick={0,10,20,30}", after=after))


def eleven():
    """Two 5-cliques joined by one edge, plus a pendant node p (the pen-and-paper example)."""
    names = ["p"] + [f"a{i}" for i in range(5)] + [f"b{i}" for i in range(5)]
    ix = {n: i for i, n in enumerate(names)}
    M = np.zeros((11, 11))
    for grp in "ab":
        for i in range(5):
            for j in range(i + 1, 5):
                M[ix[f"{grp}{i}"], ix[f"{grp}{j}"]] = M[ix[f"{grp}{j}"], ix[f"{grp}{i}"]] = 1
    for u, v in (("a4", "b0"), ("p", "a2")):
        M[ix[u], ix[v]] = M[ix[v], ix[u]] = 1
    return names, M


def cuts():
    """Two cliques joined by one edge, plus a pendant node. Two cuts of one edge each."""
    posA = {f"a{i}": (125 + 75 * math.cos(2 * math.pi * i / 5 + 1.2), 135 + 75 * math.sin(2 * math.pi * i / 5 + 1.2)) for i in range(5)}
    posB = {f"b{i}": (415 + 75 * math.cos(2 * math.pi * i / 5 + 3.1), 135 + 75 * math.sin(2 * math.pi * i / 5 + 3.1)) for i in range(5)}
    posP = {"p": (125 + 150 * math.cos(1.2 + 2 * math.pi * 2 / 5), 135 + 150 * math.sin(1.2 + 2 * math.pi * 2 / 5))}
    pos = {**posA, **posB, **posP}
    E = [(u, v) for grp in (posA, posB) for u in grp for v in grp if u < v] + [("a4", "b0"), ("p", "a2")]

    def panel(S, cutE):
        parts = []
        for k, (x, y) in pos.items():
            parts.append(vertex(f"{k}x", (x + 10, y), "", style="vertex hl" if k in S else "vertex hlc", size=34))
        parts.append("\\begin{scope}[on background layer]")
        for u, v in E:
            cut = (u, v) in cutE or (v, u) in cutE
            sty = "line width=4.5\\px, draw=sbase, dash pattern=on 6bp off 4bp" if cut else "line width=1.8\\px, draw=ink"
            parts.append(f"\\draw[{sty}] ({u}x) -- ({v}x);")
        parts.append("\\end{scope}")
        return "\n".join(parts)
    B("cuts", panel({"p"}, {("p", "a2")}))
    B("cuts-bridge", panel(set(posA) | {"p"}, {("a4", "b0")}))


def indicator():
    xs = [math.sqrt(5 / 6)] * 6 + [-math.sqrt(6 / 5)] * 5
    labs = ["p"] + [f"a_{i + 1}" for i in range(5)] + [f"b_{i + 1}" for i in range(5)]
    hl = {i: "hl" for i in range(6)} | {i: "hlc" for i in range(6, 11)}
    B("indicator", vecdots(xs, labels=labs, highlight=hl, yticks=[-1, 0, 1], unit=125, step=46, ymin=-1.3, ymax=1.2, r=6))


def relax():
    """Indicator (two values) above, relaxed solution (any real values) below, for the 11-node example."""
    names, M = eleven()
    L = np.diag(M.sum(1)) - M
    w, V = np.linalg.eigh(L)
    x = V[:, 1] * math.sqrt(11)
    x = x * (1 if x[0] > 0 else -1)
    ind = [math.sqrt(5 / 6)] * 6 + [-math.sqrt(6 / 5)] * 5
    labs = ["p"] + [f"a_{i + 1}" for i in range(5)] + [f"b_{i + 1}" for i in range(5)]
    hl = {i: "hl" for i in range(6)} | {i: "hlc" for i in range(6, 11)}
    B("relax",
      vecdots(ind, labels=labs, highlight=hl, yticks=[-1, 0, 1], unit=50, step=46, ymin=-1.4, ymax=1.4, r=6, origin=(0, 300), name="x1"),
      vecdots([float(v) for v in x], labels=labs, highlight=hl, yticks=[-1, 0, 1], unit=50, step=46, ymin=-1.4, ymax=1.4, r=6, origin=(0, 80), name="x2"),
      label((290, 412), r"two values", size="fsbody"),
      label((290, 184), r"any real values", size="fsbody"))


def fiedler():
    vals = [float(FIEDLER[i]) for i in ORDER]
    sign = 1 if CLUB[ORDER[0]] == 0 else -1          # put Mr. Hi's faction on the left
    vals = [sign * v for v in vals]
    hl = {k: ("hl" if CLUB[i] == 0 else "hlc") for k, i in enumerate(ORDER)}
    wrong = [int(i) + 1 for k, i in enumerate(ORDER) if (vals[k] < 0) != (CLUB[i] == 0)]
    print("fiedler: sign disagrees with the club for member(s)", wrong)
    B("fiedler", vecdots(vals, labels=[r"\," for _ in ORDER], highlight=hl, yticks=[-0.2, 0, 0.2], unit=410, step=20, r=5.5, ymin=-0.45, ymax=0.35))
    # the network, nodes coloured by faction
    G = nx.karate_club_graph()
    pos = nx.spring_layout(G, seed=3, iterations=300)
    xs, ys = [p[0] for p in pos.values()], [p[1] for p in pos.values()]
    sc = lambda p: (20 + (p[0] - min(xs)) / (max(xs) - min(xs)) * 330, 20 + (p[1] - min(ys)) / (max(ys) - min(ys)) * 330)
    parts = ["\\begin{scope}[on background layer]"]
    for u, v in G.edges:
        parts.append(f"\\draw[line width=1.3\\px, draw=muted] {P(*sc(pos[u]))} -- {P(*sc(pos[v]))};")
    parts.append("\\end{scope}")
    for i in G.nodes:
        col = "hl" if CLUB[i] == 0 else "hlc"
        extra = ", draw=sbase, line width=3\\px" if (i + 1) in wrong else ", line width=1.6\\px"
        parts.append(f"\\draw[fill={col}{extra}] {P(*sc(pos[i]))} circle (7.5bp);")
    B("karate-net", *parts)


def detour():
    """Where word2vec sits in the story: a detour through text, back to networks at DeepWalk."""
    parts = [node("g", (150, 260), r"vectors\\for nodes", style="box", w=250, h=110, extra="font=\\fsbody"),
             node("d", (560, 260), r"DeepWalk", style="box", w=250, h=110, extra="font=\\fsbody, fill=hl"),
             node("w", (355, 40), r"word2vec\\on text", style="box", w=250, h=110, extra="font=\\fsbody, dashed"),
             arrow("(g.east)", "(d.west)"),
             f"\\draw[arr, dashed] (g.south) |- (w.west);",
             f"\\draw[arr, dashed] (w.east) -| (d.south);",
             label((355, 190), r"\fslabel direct route", anchor="south"),
             label((355, -40), r"\fslabel detour: the same method, on text", anchor="north")]
    B("detour", *parts)


def blockmats():
    """A and x_i - x_j in the node order S | T, for the Ratio Cut indicator and the Normalized Cut indicator."""
    names, M = eleven()
    deg = M.sum(1)
    S_idx, T_idx = list(range(6)), list(range(6, 11))
    n = 11

    def one(name, xS, xT):
        parts = []
        sz, gap = 262, 70
        c = sz / n
        for k, x0 in enumerate((0, sz + gap)):
            y0 = sz
            if k == 0:
                for i in range(n):
                    for j in range(n):
                        if M[i, j]:
                            parts.append(f"\\path[fill=ink] {P(x0 + j * c, y0 - (i + 1) * c)} rectangle {P(x0 + (j + 1) * c + 0.3, y0 - i * c + 0.3)};")
                for (i, j) in ((5, 6), (6, 5)):
                    parts.append(f"\\draw[draw=sbase, line width=3.5\\px] {P(x0 + j * c, y0 - (i + 1) * c)} rectangle {P(x0 + (j + 1) * c, y0 - i * c)};")
            else:
                for i in range(n):
                    for j in range(n):
                        if (i < 6) != (j < 6):
                            v = (xS - xT) if i < 6 else (xT - xS)
                            col = rgb(diverging(0.45 if v > 0 else -0.45))
                            parts.append(f"\\path[fill={col}] {P(x0 + j * c, y0 - (i + 1) * c)} rectangle {P(x0 + (j + 1) * c + 0.3, y0 - i * c + 0.3)};")
                d = xS - xT
                parts.append(label((x0 + 8.5 * c, y0 - 3 * c), rf"${d:.2f}$", size="fsbody"))
                parts.append(label((x0 + 2.5 * c, y0 - 8.5 * c), rf"$-{d:.2f}$", size="fsbody"))
                parts.append(label((x0 + 3 * c, y0 - 3 * c), r"$0$", size="fsbody"))
                parts.append(label((x0 + 8.5 * c, y0 - 8.5 * c), r"$0$", size="fsbody"))
            parts.append(f"\\draw[line width=1.4\\px] {P(x0, y0 - sz)} rectangle {P(x0 + sz, y0)};")
            parts.append(f"\\draw[dash pattern=on 5bp off 4bp, line width=1.3bp, draw=muted] {P(x0 + 6 * c, y0)} -- {P(x0 + 6 * c, y0 - sz)};")
            parts.append(f"\\draw[dash pattern=on 5bp off 4bp, line width=1.3bp, draw=muted] {P(x0, y0 - 6 * c)} -- {P(x0 + sz, y0 - 6 * c)};")
            parts.append(label((x0 + 3 * c, y0 + 6), r"$S$", size="fsbody", anchor="south"))
            parts.append(label((x0 + 8.5 * c, y0 + 6), r"$T$", size="fsbody", anchor="south"))
            parts.append(label((x0 + sz / 2, -8), r"$\mathbf A$" if k == 0 else r"$x_i-x_j$", size="fsbody", anchor="north"))
        B(name, *parts)

    volS, volT = deg[S_idx].sum(), deg[T_idx].sum()
    one("matrices-rc", math.sqrt(5 / 6), -math.sqrt(6 / 5))
    one("matrices-ncut", math.sqrt(volT / volS), -math.sqrt(volS / volT))
    print("volumes", volS, volT, "NCut", 1 * (1 / volS + 1 / volT))


def indicator_ncut():
    names, M = eleven()
    deg = M.sum(1)
    volS, volT = deg[:6].sum(), deg[6:].sum()
    xs = [math.sqrt(volT / volS)] * 6 + [-math.sqrt(volS / volT)] * 5
    labs = ["p"] + [f"a_{i + 1}" for i in range(5)] + [f"b_{i + 1}" for i in range(5)]
    hl = {i: "hl" for i in range(6)} | {i: "hlc" for i in range(6, 11)}
    B("indicator-ncut", vecdots(xs, labels=labs, highlight=hl, yticks=[-1, 0, 1], unit=125, step=46, ymin=-1.3, ymax=1.2, r=6))


def relax_ncut():
    """Normalized Cut: indicator (two values) above, relaxed solution x = D^{-1/2} y below, for the 11-node example."""
    names, M = eleven()
    deg = M.sum(1)
    Dm = np.diag(deg ** -0.5)
    Ls = np.eye(11) - Dm @ M @ Dm
    w, V = np.linalg.eigh(Ls)
    y = V[:, 1]
    x = Dm @ y
    x = x * math.sqrt(deg.sum() / (x @ (deg * x)))          # x^T D x = vol(G)
    x = x * (1 if x[0] > 0 else -1)
    volS, volT = deg[:6].sum(), deg[6:].sum()
    ind = [math.sqrt(volT / volS)] * 6 + [-math.sqrt(volS / volT)] * 5
    labs = ["p"] + [f"a_{i + 1}" for i in range(5)] + [f"b_{i + 1}" for i in range(5)]
    hl = {i: "hl" for i in range(6)} | {i: "hlc" for i in range(6, 11)}
    B("relax-ncut",
      vecdots(ind, labels=labs, highlight=hl, yticks=[-1, 0, 1], unit=50, step=46, ymin=-1.4, ymax=1.4, r=6, origin=(0, 300), name="x1"),
      vecdots([float(v) for v in x], labels=labs, highlight=hl, yticks=[-1, 0, 1], unit=50, step=46, ymin=-1.4, ymax=1.4, r=6, origin=(0, 80), name="x2"),
      label((290, 412), r"two values", size="fsbody"),
      label((290, 184), r"any real values", size="fsbody"))


if __name__ == "__main__":
    ALL = (feat, pipeline, analogy, sentence, contrast, walkgraph, deepwalk, walks_compare, ppr_step, lesmis, pa_vs_ps, growth,
              communities, circumference, tree_disk, tree_plain, compress, layers, recon, spectrum, error_curve, cuts,
              indicator, relax, fiedler, detour, blockmats, indicator_ncut, relax_ncut)
    want = sys.argv[1:]
    for f in ALL:
        if want and f.__name__ not in want:
            continue
        print("building", f.__name__)
        f()
    print("figures written to", OUT)

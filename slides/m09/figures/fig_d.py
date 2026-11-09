"""Group d: Weisfeiler-Lehman figures (d01 ... d07).

cd slides/m09 && uv run --quiet --with numpy --with scipy --with networkx --with pillow \
    --with scikit-image python figures/fig_d.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import *  # noqa: E402,F401,F403
from common import HERE, PRE, build  # noqa: E402

EXTRA = r"""
\definecolor{gry}{HTML}{B5B5B5}
\definecolor{brn}{HTML}{8B5A2B}
\definecolor{dgy}{HTML}{4A4A4A}
\definecolor{lav}{HTML}{B79AE0}
\definecolor{gblue}{HTML}{7F93AD}
"""


def B(name, *parts):  # noqa: F811
    return build(name, *parts, outdir=HERE, preamble=PRE + EXTRA)


# ---------------------------------------------------------------- real WL -------------------------
def wl_step(adj, col):
    """One WL iteration.  adj {v: [neighbours]}, col {v: label}.  Returns the signature of each node."""
    return {v: (col[v], tuple(sorted(col[u] for u in adj[v]))) for v in adj}


def relabel(sigs_list):
    """Shared relabelling over several graphs: signature -> integer in order of first appearance."""
    table = {}
    out = []
    for sigs in sigs_list:
        d = {}
        for v in sorted(sigs):
            table.setdefault(sigs[v], len(table))
            d[v] = table[sigs[v]]
        out.append(d)
    return out, table


# ---------------------------------------------------------------- drawing helpers -----------------
def ngraph(prefix, pos, edges, fills, size=52):
    """Vertices with fill colour names (TikZ), edges behind.  Returns TikZ string."""
    out = [vertex(f"{prefix}{v}", p, "", size=size, extra=f"fill={fills[v]}") for v, p in pos.items()]
    out.append(r"\begin{scope}[on background layer]")
    out += [edge(f"{prefix}{u}", f"{prefix}{v}", style="line width=2\\px") for u, v in edges]
    out.append(r"\end{scope}")
    return "\n".join(out)


def ring(cx, cy, r, n=6, start=0.0, sy=1.0):
    return {i: (cx + r * math.cos(math.radians(start + 360 * i / n)),
                cy + sy * r * math.sin(math.radians(start + 360 * i / n))) for i in range(n)}


def triangle(cx, cy, side):
    r = side / math.sqrt(3)
    return ring(cx, cy, r, 3, start=90)


def cycle_edges(keys):
    k = list(keys)
    return [(k[i], k[(i + 1) % len(k)]) for i in range(len(k))]


def sq(at, fill, s=40, extra="line width=2\\px"):
    x, y = at
    return rf"\draw[{extra}, fill={fill}] {P(x - s / 2, y - s / 2)} rectangle {P(x + s / 2, y + s / 2)};"


def txt(at, text, anchor="center", size="fssmall", extra=""):
    return label(at, text, anchor=anchor, size=size, extra=extra)


# ---------------------------------------------------------------- d01 -------------------------------
def three_graphs(cy, rh, rt, th, hx, tx1, tx2, sy=1.0):
    """6-cycle at hx, two triangles at tx1 and tx2.  Returns (pos, edges)."""
    hexp = ring(hx, cy, rh, 6, start=0, sy=sy)
    t1 = triangle(tx1, cy + th, rt)
    t2 = triangle(tx2, cy + th, rt)
    pos = {f"h{i}": p for i, p in hexp.items()}
    pos.update({f"a{i}": p for i, p in t1.items()})
    pos.update({f"b{i}": p for i, p in t2.items()})
    edges = ([(f"h{u}", f"h{v}") for u, v in cycle_edges(range(6))]
             + [(f"a{u}", f"a{v}") for u, v in cycle_edges(range(3))]
             + [(f"b{u}", f"b{v}") for u, v in cycle_edges(range(3))])
    return pos, edges


def d01():
    cy = 190
    pos, edges = three_graphs(cy, 100, 150, 10, 150, 640, 900)
    fills = {k: "gry" for k in pos}
    B("d01_cycle_vs_triangles",
      ngraph("n", pos, edges, fills, 48),
      txt((150, 28), "6-cycle", size="fsbody"),
      txt((770, 28), "two triangles", size="fsbody"))


# ---------------------------------------------------------------- d02 -------------------------------
D2_ADJ = {1: [2], 2: [1, 3], 3: [2, 4, 5], 4: [3], 5: [3]}
D2_EDGES = [(1, 2), (2, 3), (3, 4), (3, 5)]
D2_INIT = {1: "R", 2: "B", 3: "Y", 4: "R", 5: "R"}
D2_CNAME = {"R": "sbase", "B": "snew", "Y": "sthree"}
D2_NEW = ["sfour", "sfive", "lav", "gblue"]


def wl_graph_pos(cx, cy, sp):
    """The 5-node graph: path 1-2-3-4 and node 5 above node 3, centred on cx."""
    p = {i + 1: (cx + (i - 1.5) * sp, cy) for i in range(4)}
    p[5] = (p[3][0], cy + 0.8 * sp)
    return p


def wl_graph(prefix, pos, fills, size, hl_edges=(), ringed=None):
    out = []
    if ringed is not None:
        x, y = pos[ringed]
        out.append(rf"\draw[line width=5\px, draw=hlink, fill=hl] {P(x, y)} circle ({(size / 2 + 12) * 0.75:.2f}bp);")
    out += [vertex(f"{prefix}{v}", p, "", size=size, extra=f"fill={fills[v]}") for v, p in pos.items()]
    out.append(r"\begin{scope}[on background layer]")
    for u, v in D2_EDGES:
        st = "draw=hlink, line width=6\\px" if (u, v) in hl_edges else "line width=2\\px"
        out.append(edge(f"{prefix}{u}", f"{prefix}{v}", style=st))
    out.append(r"\end{scope}")
    return "\n".join(out)


def d02_data():
    sigs = wl_step(D2_ADJ, D2_INIT)
    (new,), table = relabel([sigs])
    assert len(table) <= len(D2_NEW)
    return sigs, new, table


def mset(x0, y, colours, s=48, gap=62):
    """'{ sq sq sq }' starting at x0 (left edge of the opening brace)."""
    out = [txt((x0 + 14, y), r"$\{$", size="fslarge")]
    xs = x0 + 40
    for j, c in enumerate(colours):
        out.append(sq((xs + 24 + gap * j, y), c, s))
    xe = xs + 24 + gap * (len(colours) - 1) + 24 + 8
    out.append(txt((xe + 14, y), r"$\}$", size="fslarge"))
    return "\n".join(out), xe + 28


def d02():
    sigs, new, table = d02_data()
    cx, cyb, sp, nsz = 255, 250, 140, 72
    pos = wl_graph_pos(cx, cyb, sp)
    # a: iteration 0, node 3 and its neighbour colours
    nb = [D2_CNAME[c] for c in sigs[3][1]]
    m, xe = mset(0, 500, nb)
    w = xe
    m, xe = mset(cx - w / 2 + 0, 500, nb)
    B("d02a_wl_collect",
      wl_graph("p", pos, {v: D2_CNAME[D2_INIT[v]] for v in pos}, nsz,
               hl_edges={(2, 3), (3, 4), (3, 5)}, ringed=3),
      m,
      txt((cx, 140), "iteration 0"))
    # b: the table
    rows = sorted(table.items(), key=lambda kv: kv[1])
    parts = []
    pitch = 112
    y0 = 3 * pitch + 20
    for k, (sig, lab) in enumerate(rows):
        y = y0 - k * pitch
        own, nbs = sig
        parts.append(sq((40, y), D2_CNAME[own], 56))
        mm, xe = mset(80, y, [D2_CNAME[c] for c in nbs], s=56, gap=68)
        parts.append(mm)
        parts.append(rf"\draw[arr] {P(385, y)} -- {P(450, y)};")
        parts.append(sq((510, y), D2_NEW[lab], 56, "draw=hlink, line width=5\\px"))
    parts.append(txt((510, y0 + 80), "new"))
    B("d02b_wl_table", *parts)
    # c: iteration 1, with iteration 0 small above
    ps = wl_graph_pos(cx, 500, 64)
    B("d02c_wl_result",
      wl_graph("s", ps, {v: D2_CNAME[D2_INIT[v]] for v in ps}, 40),
      rf"\draw[arr] {P(cx, 440)} -- {P(cx, 395)};",
      wl_graph("q", pos, {v: D2_NEW[new[v]] for v in pos}, nsz),
      txt((cx, 140), "iteration 1"))


# ---------------------------------------------------------------- d03 -------------------------------
def d03():
    padj = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
    pedges = [(0, 1), (1, 2), (2, 3)]
    sadj = {0: [1, 2, 3], 1: [0], 2: [0], 3: [0]}
    sedges = [(0, 1), (0, 2), (0, 3)]
    g0 = {v: 0 for v in padj}
    (pn, sn), table = relabel([wl_step(padj, g0), wl_step(sadj, g0)])
    cols = ["sfour", "sfive", "sthree"]
    nlab = len(table)
    assert nlab == 3
    px0, psp = 40, 72
    ppos = {v: (px0 + psp * v, 0) for v in padj}
    cx = 440
    spos = {0: (cx, 0), 1: (cx, 70), 2: (cx - 62, -35), 3: (cx + 62, -35)}
    parts = []
    for row, (yc, fills_p, fills_s) in enumerate([
            (455, {v: "gry" for v in padj}, {v: "gry" for v in sadj}),
            (265, {v: cols[pn[v]] for v in padj}, {v: cols[sn[v]] for v in sadj})]):
        pp = {f"p{v}": (x, yc) for v, (x, y) in ppos.items()}
        sp = {f"s{v}": (x, yc - 15 + y) for v, (x, y) in spos.items()}
        pos = {**pp, **sp}
        edges = [(f"p{u}", f"p{v}") for u, v in pedges] + [(f"s{u}", f"s{v}") for u, v in sedges]
        fills = {**{f"p{v}": c for v, c in fills_p.items()}, **{f"s{v}": c for v, c in fills_s.items()}}
        parts.append(ngraph(f"r{row}", pos, edges, fills, 48))
        parts.append(txt((0, yc + 78), f"iteration {row}", anchor="west"))
    # histogram
    yl = 148
    parts.append(txt((0, yl), "histogram", anchor="west"))
    ys = 28
    for gx, counts in [(px0 + 1.5 * psp, [list(pn.values()).count(k) for k in range(nlab)]),
                       (cx, [list(sn.values()).count(k) for k in range(nlab)])]:
        for k in range(nlab):
            x = gx + (k - 1) * 62
            parts.append(sq((x, ys), cols[k], 44))
            for d in range(counts[k]):
                parts.append(rf"\draw[line width=1.5\px, fill=ink] {P(x, ys + 44 + 30 * d)} circle (12\px);")
    B("d03_path_star", *parts)


# ---------------------------------------------------------------- d04 -------------------------------
def d04():
    parts = []
    hx, t1x, t2x = 520, 860, 1040
    rows_y = [515, 355, 195]
    for i, yc in enumerate(rows_y):
        pos, edges = three_graphs(yc, 100, 110, 4, hx, t1x, t2x, sy=0.5)
        parts.append(ngraph(f"r{i}", pos, edges, {k: "gry" for k in pos}, 40))
        parts.append(txt((0, yc), f"iteration {i}", anchor="west"))
        parts.append(txt((712, yc), "$=$", size="fslarge"))
    yh = 45
    for x in (hx, (t1x + t2x) / 2):
        parts.append(txt((x - 22, yh), r"$6\times$", anchor="east"))
        parts.append(rf"\draw[line width=1.5\px, fill=gry] {P(x + 8, yh)} circle (17\px);")
    parts.append(txt((712, yh), "$=$", size="fslarge"))
    parts.append(txt((0, yh), "same histogram", anchor="west"))
    B("d04_wl_fail", *parts)


# ---------------------------------------------------------------- d05 -------------------------------
def d05():
    xl, xr = 140, 520
    w = 280
    rows = [(r"label $c_i$", r"feature $h_i$", 84),
            (r"neighbour\\labels", r"message $m_i$", 130),
            (r"HASH", r"update $\psi$", 84)]
    ys = [380, 230, 80]
    parts = [txt((xl, 490), "WL", size="fslarge"),
             txt((xr, 490), "GNN", size="fslarge")]
    for k, (y, (a, b, h)) in enumerate(zip(ys, rows)):
        st = "box, fill=hl" if k == 1 else "box"
        parts.append(node(f"l{k}", (xl, y), a, style=st, w=w, h=h, extra="font=\\fssmall, align=center"))
        parts.append(node(f"r{k}", (xr, y), b, style=st, w=w, h=h, extra="font=\\fssmall, align=center"))
        parts.append(rf"\draw[line width=2\px] (l{k}.east) -- (r{k}.west);")
    for k in range(2):
        parts.append(rf"\draw[arr] (l{k}.south) -- (l{k + 1}.north);")
        parts.append(rf"\draw[arr] (r{k}.south) -- (r{k + 1}.north);")
    B("d05_wl_gnn_correspondence", *parts)


# ---------------------------------------------------------------- d06 -------------------------------
def d06():
    cy = 360
    pos, edges = three_graphs(cy, 70, 90, 6, 90, 330, 475)
    mid = 225
    parts = [ngraph("g", pos, edges, {k: "gry" for k in pos}, 40),
             raw(rf"\draw[line width=4\px] {P(mid - 24, cy + 14)} -- {P(mid + 24, cy + 14)}; \draw[line width=4\px] {P(mid - 24, cy - 14)} -- {P(mid + 24, cy - 14)}; \draw[line width=4\px] {P(mid - 10, cy - 36)} -- {P(mid + 10, cy + 36)};"),
             node("wl", (265, 190), "WL: equal", w=360, h=72),
             node("gn", (265, 60), "GNN: equal", style="box, fill=hl", w=360, h=72),
             r"\draw[arr] (wl.south) -- (gn.north);"]
    B("d06_theorem", *parts)


# ---------------------------------------------------------------- d07 -------------------------------
def d07():
    import numpy as np
    A = [0, 0, 1, 1]
    Bm = [0, 1]
    onehot = lambda ms: np.eye(2)[ms]  # noqa: E731
    cols = ["sbase", "snew"]

    def fmt(x):
        s = f"{x:g}"
        return s[1:] if s.startswith("0.") else s

    def vec(v):
        return rf"$(\textcolor{{sbase}}{{{fmt(v[0])}}},\textcolor{{snew}}{{{fmt(v[1])}}})$"

    aggs = {"sum": lambda M: M.sum(0), "mean": lambda M: M.mean(0), "max": lambda M: M.max(0)}
    xa, xb, xm = 275, 540, 410
    parts = []
    yt = 345
    for x, ms in ((xa, A), (xb, Bm)):
        n = len(ms)
        wbox = 34 * n + 28 + 2 * 40
        parts.append(rf"\draw[line width=2\px, fill=white] {P(x - wbox / 2, yt - 38)} rectangle {P(x + wbox / 2, yt + 38)};")
        parts.append(txt((x - wbox / 2 + 6, yt), r"$\{\!\{$", anchor="west"))
        parts.append(txt((x + wbox / 2 - 6, yt), r"$\}\!\}$", anchor="east"))
        x0 = x - 34 * (n - 1) / 2
        for i, c in enumerate(ms):
            parts.append(rf"\draw[line width=1.5\px, fill={cols[c]}] {P(x0 + 34 * i, yt)} circle (14\px);")
    y = 235
    for name, f in aggs.items():
        va, vb = f(onehot(A)), f(onehot(Bm))
        same = bool(np.allclose(va, vb))
        if not same:
            parts.append(rf"\fill[hl] {P(0, y - 45)} rectangle {P(620, y + 45)};")
        parts.append(txt((0, y), name, anchor="west"))
        parts.append(txt((xa, y), vec(va)))
        parts.append(txt((xb, y), vec(vb)))
        parts.append(txt((xm, y), "$=$" if same else r"$\neq$", size="fslarge"))
        y -= 100
    B("d07_aggregators", *parts)


if __name__ == "__main__":
    d01()
    d02()
    d03()
    d04()
    d05()
    d06()
    d07()

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


def ring(cx, cy, r, n=6, start=0.0):
    return {i: (cx + r * math.cos(math.radians(start + 360 * i / n)),
                cy + r * math.sin(math.radians(start + 360 * i / n))) for i in range(n)}


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
def d01():
    cy = 215
    hexp = ring(167, cy, 115, 6, start=0)
    t1 = triangle(421, cy + 8, 110)
    t2 = triangle(601, cy + 8, 110)
    # keys must be unique over the whole picture
    pos = {}
    for i, p in hexp.items():
        pos[f"h{i}"] = p
    for i, p in t1.items():
        pos[f"a{i}"] = p
    for i, p in t2.items():
        pos[f"b{i}"] = p
    edges = ([(f"h{u}", f"h{v}") for u, v in cycle_edges(range(6))]
             + [(f"a{u}", f"a{v}") for u, v in cycle_edges(range(3))]
             + [(f"b{u}", f"b{v}") for u, v in cycle_edges(range(3))])
    fills = {k: "gry" for k in pos}
    B("d01_cycle_vs_triangles",
      ngraph("n", pos, edges, fills, 52),
      txt((167, 28), "6-cycle", size="fsbody", extra="font=\\fslarge"),
      txt((511, 28), "two triangles", size="fsbody", extra="font=\\fslarge"))


# ---------------------------------------------------------------- d02 -------------------------------
def d02():
    adj = {1: [2], 2: [1, 3], 3: [2, 4, 5], 4: [3], 5: [3]}
    edges = [(1, 2), (2, 3), (3, 4), (3, 5)]
    init = {1: "R", 2: "B", 3: "Y", 4: "R", 5: "R"}
    cname = {"R": "sbase", "B": "snew", "Y": "sthree"}
    sigs = wl_step(adj, init)
    (new,), table = relabel([sigs])
    newcol = ["sfive", "sfour", "brn", "dgy"]
    assert len(table) <= len(newcol)
    parts = []
    # before graph
    pos0 = {1: (45, 490), 2: (140, 490), 3: (235, 490), 4: (330, 490), 5: (235, 396)}
    parts.append(ngraph("p", pos0, edges, {v: cname[init[v]] for v in adj}, 52))
    parts.append(txt((395, 490), "iteration 0", anchor="west"))
    # after graph (smaller)
    pos1 = {1: (440, 190), 2: (493, 190), 3: (546, 190), 4: (599, 190), 5: (546, 137)}
    # (scaled to 38 px nodes)
    parts.append(ngraph("q", pos1, edges, {v: newcol[new[v]] for v in adj}, 42))
    parts.append(txt((520, 262), "iteration 1", size="fssmall"))
    # table: one row per distinct signature, in order of new label
    rows = sorted(table.items(), key=lambda kv: kv[1])
    y0 = 300
    for k, (sig, lab) in enumerate(rows):
        y = y0 - k * 78
        own, nb = sig
        parts.append(sq((30, y), cname[own], 40))
        parts.append(txt((78, y), r"$\{$", size="fslarge"))
        for j, c in enumerate(nb):
            parts.append(sq((120 + 46 * j, y), cname[c], 38, "line width=1.5\\px"))
        parts.append(txt((120 + 46 * (len(nb) - 1) + 24, y), r"$\}$", size="fslarge", anchor="west"))
        parts.append(rf"\draw[arr] {P(290, y)} -- {P(335, y)};")
        parts.append(sq((375, y), newcol[lab], 40, "draw=hlink, line width=5\\px"))
    B("d02_wl_iteration", *parts)


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
    xs = [244, 310, 376, 442]
    ppos = {v: (xs[v], 0) for v in padj}
    cx = 585
    spos = {0: (cx, 0), 1: (cx, 62), 2: (cx - 54, -31), 3: (cx + 54, -31)}
    parts = []
    for row, (yc, fills_p, fills_s) in enumerate([
            (450, {v: "gry" for v in padj}, {v: "gry" for v in sadj}),
            (295, {v: cols[pn[v]] for v in padj}, {v: cols[sn[v]] for v in sadj})]):
        pp = {f"p{v}": (x, yc) for v, (x, y) in ppos.items()}
        sp = {f"s{v}": (x, yc - 14 + y) for v, (x, y) in spos.items()}
        pos = {**pp, **sp}
        edges = [(f"p{u}", f"p{v}") for u, v in pedges] + [(f"s{u}", f"s{v}") for u, v in sedges]
        fills = {**{f"p{v}": c for v, c in fills_p.items()}, **{f"s{v}": c for v, c in fills_s.items()}}
        parts.append(ngraph(f"r{row}", pos, edges, fills, 52))
        parts.append(txt((0, yc), f"iteration {row}", anchor="west"))
    # histogram
    parts.append(txt((0, 80), "histogram", anchor="west"))
    ys = 55
    for gx, counts in [(343, [list(pn.values()).count(k) for k in range(nlab)]),
                       (cx, [list(sn.values()).count(k) for k in range(nlab)])]:
        for k in range(nlab):
            x = gx + (k - 1) * 58
            parts.append(sq((x, ys), cols[k], 40))
            for d in range(counts[k]):
                parts.append(rf"\draw[line width=1.5\px, fill=ink] {P(x, ys + 44 + 30 * d)} circle (12\px);")
    B("d03_path_star", *parts)


# ---------------------------------------------------------------- d04 -------------------------------
def d04():
    parts = []
    hx = 285
    rows_y = [440, 290, 140]
    r = 58
    nsz = 36
    for i, yc in enumerate(rows_y):
        hexp = ring(hx, yc, r, 6, 0)
        t1 = triangle(482, yc + 4, 68)
        t2 = triangle(604, yc + 4, 68)
        pos = {f"h{k}": p for k, p in hexp.items()}
        pos.update({f"a{k}": p for k, p in t1.items()})
        pos.update({f"b{k}": p for k, p in t2.items()})
        edges = ([(f"h{u}", f"h{v}") for u, v in cycle_edges(range(6))]
                 + [(f"a{u}", f"a{v}") for u, v in cycle_edges(range(3))]
                 + [(f"b{u}", f"b{v}") for u, v in cycle_edges(range(3))])
        parts.append(ngraph(f"r{i}", pos, edges, {k: "gry" for k in pos}, nsz))
        parts.append(txt((0, yc), f"iteration {i}", anchor="west"))
        parts.append(txt((393, yc + 2), "=", size="fslarge", extra="font=\\fslarge"))
    yh = 30
    for x in (hx, 543):
        parts.append(txt((x - 22, yh), r"$6\times$", anchor="east"))
        parts.append(rf"\draw[line width=1.5\px, fill=gry] {P(x - 4, yh)} circle (15\px);")
    parts.append(txt((393, yh), "=", size="fslarge", extra="font=\\fslarge"))
    B("d04_wl_fail", *parts)


# ---------------------------------------------------------------- d05 -------------------------------
def d05():
    xl, xr = 142, 556
    w, h = 280, 100
    ys = [370, 225, 80]
    rows = [(r"label $c_i$", r"feature $h_i$"),
            (r"multiset of\\neighbour labels", r"aggregated\\message $m_i$"),
            (r"HASH", r"update $\psi$")]
    parts = [txt((xl, 478), "WL", size="fslarge", extra="font=\\fslarge"),
             txt((xr, 478), "GNN", size="fslarge", extra="font=\\fslarge")]
    for k, (y, (a, b)) in enumerate(zip(ys, rows)):
        st = "box, fill=hl" if k == 1 else "box"
        parts.append(node(f"l{k}", (xl, y), a, style=st, w=w, h=h, extra="font=\\fssmall"))
        parts.append(node(f"r{k}", (xr, y), b, style=st, w=w, h=h, extra="font=\\fssmall"))
        parts.append(rf"\draw[line width=2\px] ({'l'}{k}.east) -- ({'r'}{k}.west);")
    for k in range(2):
        parts.append(rf"\draw[arr] (l{k}.south) -- (l{k + 1}.north);")
        parts.append(rf"\draw[arr] (r{k}.south) -- (r{k + 1}.north);")
    B("d05_wl_gnn_correspondence", *parts)


# ---------------------------------------------------------------- d06 -------------------------------
def d06():
    cy = 305
    hexp = ring(115, cy, 90, 6, 0)
    t1 = triangle(465, cy + 6, 74)
    t2 = triangle(585, cy + 6, 74)
    pos = {f"h{k}": p for k, p in hexp.items()}
    pos.update({f"a{k}": p for k, p in t1.items()})
    pos.update({f"b{k}": p for k, p in t2.items()})
    edges = ([(f"h{u}", f"h{v}") for u, v in cycle_edges(range(6))]
             + [(f"a{u}", f"a{v}") for u, v in cycle_edges(range(3))]
             + [(f"b{u}", f"b{v}") for u, v in cycle_edges(range(3))])
    parts = [ngraph("g", pos, edges, {k: "gry" for k in pos}, 40),
             raw(rf"\draw[line width=4\px] {P(262, cy + 12)} -- {P(318, cy + 12)}; \draw[line width=4\px] {P(262, cy - 12)} -- {P(318, cy - 12)}; \draw[line width=4\px] {P(283, cy - 32)} -- {P(297, cy + 32)};"),
             node("wl", (350, 140), "WL colours: equal", w=400, h=62, extra="font=\\fssmall"),
             node("gn", (350, 38), "GNN output: equal", style="box, fill=hl", w=400, h=62, extra="font=\\fssmall"),
             r"\draw[arr] (wl.south) -- (gn.north);"]
    B("d06_theorem", *parts)


# ---------------------------------------------------------------- d07 -------------------------------
def d07():
    import numpy as np
    # neighbour multisets: colour 0 = R (vermillion), 1 = B (blue); one-hot vectors
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
    xa, xb, xm = 235, 560, 398
    parts = []
    # multisets in boxes
    yt = 470
    for x, ms in ((xa, A), (xb, Bm)):
        n = len(ms)
        wbox = 36 * n + 40 + 2 * 28
        parts.append(rf"\draw[line width=2\px, fill=white] {P(x - wbox / 2, yt - 36)} rectangle {P(x + wbox / 2, yt + 36)};")
        parts.append(txt((x - wbox / 2 + 14, yt), r"$\{\!\{$", anchor="west"))
        parts.append(txt((x + wbox / 2 - 14, yt), r"$\}\!\}$", anchor="east"))
        x0 = x - 36 * (n - 1) / 2
        for i, c in enumerate(ms):
            parts.append(rf"\draw[line width=1.5\px, fill={cols[c]}] {P(x0 + 36 * i, yt)} circle (14\px);")
    y = 350
    for name, f in aggs.items():
        va, vb = f(onehot(A)), f(onehot(Bm))
        same = bool(np.allclose(va, vb))
        parts.append(txt((0, y), name, anchor="west"))
        parts.append(txt((xa, y), vec(va)))
        parts.append(txt((xb, y), vec(vb)))
        parts.append(txt((xm, y), "same" if same else "different",
                         extra=("font=\\fssmall\\bfseries" if not same else "")))
        y -= 135
    # thin separators
    for yy in (410, 282, 147):
        parts.append(rf"\draw[rule, line width=1.5\px] {P(0, yy)} -- {P(690, yy)};")
    B("d07_aggregators", *parts)


if __name__ == "__main__":
    d01()
    d02()
    d03()
    d04()
    d05()
    d06()
    d07()

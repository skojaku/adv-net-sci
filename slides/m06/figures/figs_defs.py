#!/usr/bin/env python3
"""Definition figures of Module 06: the two ways to count, the bowtie, the grid.

All of them are builds the lecturer steps through (frames/<name>/NN.png); every frame is one
small step, in the lecturer's style (figlib: pencil discs, brush strokes, Meslo labels).

    w5-blank, w5-walks             slides 8, 9    how far is u from v: shortest path, then walks
                                                  (col; frame 0 of w5-walks = w5-blank)
    closeness-def, bowtie-closeness slides 12, 25  the sum of distances, node by node; D smallest
    ecc-def                        slide 26       the sums give way to eccentricities
                                                  (frame 0 = bowtie-closeness)
    btw-def                        slide 33       a letter for every pair, a counter per carrier
                                                  (frame 0 = the bare bowtie)
    grid-empty/-row1/-row2/-final  slides 10, 40, 71, 81   one table in four states (full)

The bowtie figures share one canvas, one set of coordinates and one box, so the picture
does not move from slide to slide.  harmonic-def lives in figs_quiz (the CA group).
Every number is read from `smallgraphs`; the facts a figure draws are asserted at build time.
"""

import itertools
import re

import networkx as nx

import figlib as F
import smallgraphs as S


# --------------------------------------------------------------------------- helpers
def place(XY, s, ox, oy, sy=None):
    """Grid units -> bp, y up, with grid (0, 0) of the lowest-left node at (ox, oy)."""
    sy = s if sy is None else sy
    x0 = min(p[0] for p in XY.values())
    y0 = min(p[1] for p in XY.values())
    return {n: (ox + (x - x0) * s, oy + (y - y0) * sy) for n, (x, y) in XY.items()}


def adjacent(G, names):
    assert all(G.has_edge(a, b) for a, b in zip(names, names[1:])), f"{names} is not a walk"


def edges_tex(edges, pos):
    return "".join(F.seg(pos[a], pos[b]) for a, b in edges)


def discs_tex(pos, labels, hot=(), fill=None):
    fill = fill or {}
    return "".join(F.disc(x, y, labels.get(n, ""), fill="hot" if n in hot else fill.get(n, "white"))
                   for n, (x, y) in pos.items())


def route(pos, names, color="gold", w=14):
    return F.brush([pos[n] for n in names], color=color, w=w)


# =========================================================================== W5
# Module 01's five-node graph, stretched to fill the column (the picture is a diagram, only
# the adjacency matters). u top right, v bottom centre.
W5_H = 420
W5_SX, W5_SY, W5_OX, W5_OY = 400, 118, 68, 74
W5_POS = {n: (W5_OX + x * W5_SX, W5_OY + (y + 0.9) * W5_SY) for n, (x, y) in S.W5_XY.items()}
W5_CAP_Y = 24
W5_BOX = (W5_H - 326, W5_H - 6)                       # bp from the canvas top, shared by every frame
F.assert_planar_drawing(list(S.W5.edges), W5_POS, "W5 stretched")
W5_LAB = {"u": "u", "v": "v"}


def _w5_walks(k):
    """Every walk of exactly k steps from u to v, by depth-first enumeration."""
    out = []

    def go(path):
        if len(path) == k + 1:
            if path[-1] == "v":
                out.append(tuple(path))
            return
        for m in sorted(S.W5[path[-1]]):
            go(path + [m])
    go(["u"])
    return out


def _w5_facts():
    d = nx.shortest_path_length(S.W5, "u", "v")
    sp = [tuple(q) for q in nx.all_shortest_paths(S.W5, "u", "v")]
    w = {k: _w5_walks(k) for k in (2, 3, 4)}
    counts = [len(w[2]), len(w[3]), len(w[4])]
    assert d == S.dist(S.W5, "u")["v"] == 2
    assert counts == S.walk_counts(S.W5, S.W5_ORDER, "u", "v")[1:4] == [2, 1, 11], counts
    for k in w:
        for p in w[k]:
            assert len(p) == k + 1
            adjacent(S.W5, p)
    return d, sp, w


def _w5_scene(brushes="", label="", count=""):
    """The blank graph, plus brushes under the discs, plus one caption: a muted label and
    its number in hot.  Everything but the brushes and the caption is the same in every frame."""
    o = edges_tex(S.W5.edges, W5_POS) + brushes + discs_tex(W5_POS, W5_LAB)
    if label:
        o += F.text(380, W5_CAP_Y, label, color="muted", anchor="east")
        o += F.text(394, W5_CAP_Y, count, color="hot", anchor="west")
    return o


def w5_blank():
    F.emit("w5-blank", _w5_scene(), container="col", h=W5_H, box=W5_BOX)


def w5_walks():
    d, sps, walks = _w5_facts()
    a, b = ("u", "n2", "v"), ("u", "n3", "v")
    assert a in sps and b in sps
    assert a in walks[2] and b in walks[2] and len(walks[2]) == 2
    c, = walks[3]
    assert c == ("u", "n0", "n2", "v"), c
    n2, n3, n4 = len(walks[2]), len(walks[3]), len(walks[4])
    frames = [
        _w5_scene(),                                                                       # = w5-blank
        _w5_scene(route(W5_POS, a, "hot"), "shortest path:", str(d)),
        _w5_scene(route(W5_POS, a) + route(W5_POS, b), "walks of length 2:", str(n2)),
        _w5_scene(route(W5_POS, c), "walks of length 3:", str(n3)),
        _w5_scene("", "walks of length 4:", str(n4)),
    ]
    assert frames[0] == _w5_scene()
    F.emit_frames("w5-walks", frames, container="col", h=W5_H, box=W5_BOX)


# =========================================================================== BT (closeness, ecc, btw)
BT_S = 80
BT_POS = place(S.BT_XY, BT_S, 58, 118)
BT_H = 400
BT_BOX = (BT_H - 346, BT_H - 46)                     # one crop for the whole bowtie group
F.assert_planar_drawing(list(S.BT.edges), BT_POS, "BT")
BT_NODES = sorted(S.BT)
# where each node's number sits: above (+1) or below (-1); one choice, so a number never hops
BT_SIDE = {"A": 1, "B": -1, "C": 1, "D": -1, "E": 1, "F": 1, "G": -1}
BT_GAP = 36


def bt_value(n, s, color="ink"):
    x, y = BT_POS[n]
    return F.text(x, y + BT_SIDE[n] * BT_GAP, s, color=color)


def bt_scene(vals=None, colors=None, brushes="", hot=(), under=None, fill=None):
    """The bowtie with its edges, optional brushes under the discs, values beside the nodes.
    `hot`: nodes whose disc is the answer; `under`: the node whose value is underlined."""
    colors = colors or {}
    o = edges_tex(S.BT.edges, BT_POS) + brushes
    o += discs_tex(BT_POS, {n: n for n in BT_POS}, hot=hot, fill=fill)
    for n, s in (vals or {}).items():
        o += bt_value(n, s, colors.get(n, "ink"))
    if under:
        x, y = BT_POS[under]
        yy = y + BT_SIDE[under] * BT_GAP - 18
        o += F.underline(x - 22, x + 22, yy, color="hot")
    return o


def closeness_frames():
    G = S.BT
    sums = S.dsum(G)
    assert S.argbest(sums, min) == (["D"], 10) and sums["A"] == 15      # D smallest, A the example
    assert [sums[n] for n in BT_NODES] == [15, 15, 11, 10, 11, 15, 15]
    L = S.dist(G, "A")
    assert sum(L.values()) == 15 and sorted(L.values()) == [0, 1, 1, 2, 3, 4, 4]
    frames = [bt_scene()]                                                # the bare bowtie
    frames.append(bt_scene({n: str(k) for n, k in L.items() if n != "A"}, fill={"A": "cool"}))
    shown = {}
    for n in BT_NODES:
        shown[n] = str(sums[n])
        frames.append(bt_scene(dict(shown)))
    frames.append(bt_scene(dict(shown), colors={"D": "hot"}, hot=["D"], under="D"))
    return frames, sums


def closeness_def():
    frames, _ = closeness_frames()
    F.emit_frames("closeness-def", frames, container="col", h=BT_H, box=BT_BOX)
    F.emit("bowtie-closeness", frames[-1], container="col", h=BT_H, box=BT_BOX)


def ecc_def():
    G = S.BT
    ecc = S.eccentricity(G)
    assert S.argbest(ecc, min) == (["D"], 2)
    assert [ecc[n] for n in BT_NODES] == [4, 4, 3, 2, 3, 4, 4]
    closeness, sums = closeness_frames()
    sumtxt = {n: str(sums[n]) for n in BT_NODES}
    frames = [closeness[-1]]                                              # = bowtie-closeness
    muted = {n: "muted" for n in BT_NODES}
    frames.append(bt_scene(sumtxt, colors=muted))                         # the sums step back
    shown = {}
    for u in BT_NODES:
        L = S.dist(G, u)
        far = min(n for n in sorted(L) if L[n] == ecc[u])                 # the alphabetically first farthest
        path = tuple(nx.shortest_path(G, u, far))
        adjacent(G, path)
        assert len(path) - 1 == ecc[u] == L[far]
        shown[u] = str(ecc[u])
        vals = {**{n: sumtxt[n] for n in BT_NODES if n not in shown}, **shown}
        cols = {n: ("muted" if n not in shown else "ink") for n in BT_NODES}
        frames.append(bt_scene(vals, colors=cols, brushes=route(BT_POS, path)))
    frames.append(bt_scene(dict(shown), colors={"D": "hot"}, hot=["D"], under="D"))
    F.emit_frames("ecc-def", frames, container="col", h=BT_H, box=BT_BOX)


def btw_def():
    G = S.BT
    btw = S.betweenness(G)
    assert S.argbest(btw) == (["D"], 9) and btw["C"] == btw["E"] == 8
    pairs = []
    for s, t in itertools.combinations(BT_NODES, 2):
        ps = list(nx.all_shortest_paths(G, s, t))
        assert len(ps) == 1                                     # every shortest path is unique here
        if len(ps[0]) > 2:
            pairs.append((s, t, tuple(ps[0])))
    count = {n: 0 for n in G}
    for s, t, p in pairs:
        for i in p[1:-1]:
            count[i] += 1
    assert {n: count[n] for n in G} == {n: int(btw[n]) for n in G}
    assert len(pairs) == 13 and count["D"] == 9
    frames = [bt_scene()]                                       # the bare bowtie
    run = {n: 0 for n in G}
    for s, t, p in pairs:
        for i in p[1:-1]:
            run[i] += 1
        frames.append(bt_scene({n: str(c) for n, c in run.items() if c}, brushes=route(BT_POS, p)))
    assert run == count
    allc = {n: str(c) for n, c in count.items()}
    frames.append(bt_scene(allc))                               # the ends carry nothing: 0
    frames.append(bt_scene(allc, colors={"D": "hot"}, hot=["D"], under="D"))
    F.emit_frames("btw-def", frames, container="col", h=BT_H, box=BT_BOX)


# =========================================================================== the grid
GW, GH = F.FULL_W, 420
GM = 6                            # outer margin
GX0, GX1 = GM, GW - GM
LINE = int(F.FONT * 1.15)
PADY = 5
ROW1_H = 3 * LINE + 2 * PADY      # name + two lines
ROW2_H = 4 * LINE + 2 * PADY      # name + up to three lines
ROW2_Y0 = 22
ROW2_Y1 = ROW2_Y0 + ROW2_H
CAP2_Y = ROW2_Y1 + 19             # the muted caption above each row ("walks", "shortest paths")
ROW1_Y0 = CAP2_Y + 19
ROW1_Y1 = ROW1_Y0 + ROW1_H
CAP1_Y = ROW1_Y1 + 19
HEAD_Y = CAP1_Y + 42                   # the two axis headers (muted), one line
HEAD_ROUTES = "which routes count"
HEAD_NUMBER = "how they become one number"
GRID_BOX = (GH - (HEAD_Y + 22), GH - (ROW2_Y0 - 8))      # one crop for all four states

# (metric, description lines); the description of every cell is the spec's text, only broken
# into lines. Nothing is shortened.
ROW1 = [("closeness", ["sum of", "lengths"]),
        ("harmonic", ["sum of", "1/length"]),
        ("eccentricity", ["longest", "distance"]),
        ("betweenness", ["paths passing", "through"])]
ROW2 = [("degree", ["walks of", "length 1"]),
        ("Katz", ["all", "lengths,", "discounted"]),
        ("eigenvector", ["the longest", "walks"]),
        ("PageRank", ["walks that", "split the", "vote"]),
        ("HITS", ["walks that", "alternate", "direction"])]


def _cells(row, y0, y1):
    pitch = (GX1 - GX0) / (5 if row is ROW2 else 4)
    return [dict(name=name, desc=desc, x0=GX0 + i * pitch + 3, x1=GX0 + (i + 1) * pitch - 3,
                 y0=y0, y1=y1) for i, (name, desc) in enumerate(row)]


CELLS1 = _cells(ROW1, ROW1_Y0, ROW1_Y1)
CELLS2 = _cells(ROW2, ROW2_Y0, ROW2_Y1)
# geometry asserts: cells inside the canvas, no overlap, same width within a row
for _row in (CELLS1, CELLS2):
    for _a, _b in zip(_row, _row[1:]):
        assert _a["x1"] < _b["x0"]
    assert _row[0]["x0"] >= GX0 and _row[-1]["x1"] <= GX1
    assert len({round(c["x1"] - c["x0"], 6) for c in _row}) == 1
assert CELLS1[0]["x1"] - CELLS1[0]["x0"] > 200 and CELLS2[0]["x1"] - CELLS2[0]["x0"] > 170
# every line of text fits inside its cell (Meslo is 0.6 em per character), with 2 bp to spare
for _c in CELLS1 + CELLS2:
    for _t in [_c["name"]] + _c["desc"]:
        assert 0.6 * F.FONT * len(_t) + 4 <= _c["x1"] - _c["x0"], f"{_t!r} overflows its cell"
assert GRID_BOX[1] - GRID_BOX[0] <= F.FIG_H["tall"]


def _box(c, color):
    """A hand-drawn cell."""
    x0, y0, x1, y1 = c["x0"], c["y0"], c["x1"], c["y1"]
    return (F._seed(x0, y0) + f"\\draw[line width=2.0bp,draw={color},pencil] "
            f"({x0:.1f},{y0}) rectangle ({x1:.1f},{y1});\n")


def _ghost(c):
    """An empty slot of the table: a faint dashed box, so the empty table already shows its shape."""
    return (F._seed(c["x0"], c["y0"], 7) + f"\\draw[line width=2.0bp,draw=pale,pencil] "
            f"({c['x0']:.1f},{c['y0']}) rectangle ({c['x1']:.1f},{c['y1']});\n")


def _cell_tex(c, new=False):
    o = _box(c, "hot" if new else "ink")
    name = ("\\textcolor{hot}{%s}" if new else "%s") % c["name"]
    o += F.text((c["x0"] + c["x1"]) / 2, c["y1"] - PADY, "\\\\ ".join([name] + c["desc"]), anchor="north")
    return o


def _grid(row1, row2, new=()):
    """row1, row2: how many cells of each row to draw (a prefix). `new`: names of the cells
    that are new on this slide (name and box in hot, every old cell in ink). The slots not
    drawn yet are faint dashed boxes."""
    o = F.text(GM, HEAD_Y, HEAD_ROUTES, color="muted", anchor="west")
    o += F.text(GX1, HEAD_Y, HEAD_NUMBER, color="muted", anchor="east")
    o += F.text(GX0, CAP1_Y, "shortest paths", color="muted", anchor="west")
    o += F.text(GX0, CAP2_Y, "walks", color="muted", anchor="west")
    for c in CELLS1[row1:] + CELLS2[row2:]:
        o += _ghost(c)
    for c in CELLS1[:row1] + CELLS2[:row2]:
        o += _cell_tex(c, c["name"] in new)
    return o


def _grid_fig(name, row1, row2, new=()):
    F.emit(name, _grid(row1, row2, new), container="full", h=GH, hmod="tall", nodes=False, box=GRID_BOX)


def grid_empty():
    _grid_same_picture()
    _grid_fig("grid-empty", 0, 1)


def grid_row1():
    _grid_fig("grid-row1", 4, 1, new=[c[0] for c in ROW1])


def grid_row2():
    _grid_fig("grid-row2", 4, 3, new=["Katz", "eigenvector"])


def grid_final():
    _grid_fig("grid-final", 4, 5, new=["PageRank", "HITS"])


def _grid_same_picture():
    """The four states are one picture: every cell that appears is drawn at the same place."""
    plain = lambda t: re.sub(r"\\textcolor\{hot\}\{(\w+)\}", r"\1", t).replace("draw=hot", "draw=ink")
    big = set(plain(_grid(4, 5)).splitlines())
    for part in (_grid(0, 1), _grid(4, 1, [c[0] for c in ROW1]), _grid(4, 3, ["Katz", "eigenvector"])):
        for line in plain(part).splitlines():
            assert "pale" in line or line in big, f"grid state differs from the final picture: {line[:60]}"
    assert "pale" not in _grid(4, 5)                                   # the final table has no empty slot


FIGURES = [
    ("w5-blank", w5_blank),
    ("w5-walks", w5_walks),
    ("closeness-def", closeness_def),
    ("ecc-def", ecc_def),
    ("btw-def", btw_def),
    ("grid-empty", grid_empty),
    ("grid-row1", grid_row1),
    ("grid-row2", grid_row2),
    ("grid-final", grid_final),
]

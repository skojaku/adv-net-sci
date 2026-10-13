#!/usr/bin/env python3
"""Definition figures of Module 06: the two ways to count, the bowtie, the grid.

All of them are builds the lecturer steps through (frames/<name>/NN.png); every frame is one
small step, in the lecturer's style (figlib: pencil discs, brush strokes, Meslo labels).

    w5-blank, w5-walks             slides 8, 9    how far is u from v: shortest path, then walks
                                                  (col; frame 0 of w5-walks = w5-blank)
    closeness-def, bowtie-closeness slides 12, 25  the sum of distances, node by node, then c = 6/sum; D 0.60
    ecc-def                        slide 26       the sums give way to eccentricities
                                                  (frame 0 = bowtie-closeness)
    btw-def                        slide 33       one frame per source node (its paths, counters), zeros, D = 9
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


def callout(blockers, discs, text, at, target, anchor="south", gap=8.0, tip=None, bend=0):
    """F.callout, with the build-time check that the note's box touches no disc and no value
    box in `blockers` (the notes never lie on a number or a node)."""
    tikz, b = F.callout(text, at, target, anchor=anchor, gap=gap, tip=tip, bend=bend)
    for x, y in discs:
        assert not F.box_hits_disc(b, x, y, F.NODE / 2 + 3), f"callout {text!r} touches a disc"
    for o in blockers:
        assert not F.boxes_overlap(b, o), f"callout {text!r} touches a value"
    return tikz


def route(pos, names, color="gold", w=14):
    return F.brush([pos[n] for n in names], color=color, w=w)


# =========================================================================== W5
# Module 01's five-node graph, stretched to fill the column (the picture is a diagram, only
# the adjacency matters). u top right, v bottom centre.
W5_H = 420
W5_SX, W5_SY, W5_OX, W5_OY = 400, 118, 68, 74
W5_POS = {n: (W5_OX + x * W5_SX, W5_OY + (y + 0.9) * W5_SY) for n, (x, y) in S.W5_XY.items()}
W5_BOX = (W5_H - 404, W5_H - 6)                       # shared by every frame: a band above the drawing holds the callouts
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


W5_HMOD = "tall"


def _w5_scene(brushes="", note=None):
    """The blank graph, plus brushes under the discs, plus one callout (tikz).  Everything
    but the brushes and the callout is the same in every frame."""
    return edges_tex(S.W5.edges, W5_POS) + brushes + discs_tex(W5_POS, W5_LAB) + (note or "")


def _w5_note(text, at, target, anchor="south", gap=8.0):
    return callout([], W5_POS.values(), text, at, target, anchor=anchor, gap=gap)


def w5_blank():
    F.emit("w5-blank", _w5_scene(), container="col", h=W5_H, hmod=W5_HMOD, box=W5_BOX)


def w5_walks():
    d, sps, walks = _w5_facts()
    P = W5_POS
    a, b = ("u", "n2", "v"), ("u", "n3", "v")
    assert a in sps and b in sps and d == 2
    assert a in walks[2] and b in walks[2] and len(walks[2]) == 2
    c, = walks[3]
    assert c == ("u", "n0", "n2", "v"), c
    n2, n3, n4 = len(walks[2]), len(walks[3]), len(walks[4])
    assert (n2, n3, n4) == (2, 1, 11)
    e = ("u", "n0", "u", "n2", "v")                       # a length-4 walk that goes back to u
    assert e in walks[4] and e.count("u") == 2
    mid = ((P["n0"][0] + P["u"][0]) / 2, (P["n0"][1] + P["u"][1]) / 2 - 26)
    e_pts = [P["u"], P["n0"], mid, P["u"], P["n2"], P["v"]]       # the way back is bowed, so it shows
    top = 336                                              # the callout band above the drawing
    mx = lambda p, q, t=0.5: (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    frames = [
        _w5_scene(),                                                                       # = w5-blank
        _w5_scene(route(P, a, "hot"), _w5_note(f"shortest path: {d} steps", (14, 26), mx(P["n2"], P["v"], 0.45),
                                               anchor="west", gap=14)),
        _w5_scene(route(P, a) + route(P, b), _w5_note(f"length 2: {n2} walks", (523, 26), mx(P["n3"], P["v"], 0.4),
                                                      anchor="east", gap=14)),
        _w5_scene(route(P, c, "cool"), _w5_note(f"length 3: {n3} walk", (P["n0"][0] + 200, top), (P["n0"][0] + 200, P["n0"][1] + 4),
                                                gap=6)),
        _w5_scene(F.brush(e_pts, color="cool", w=9),
                  _w5_note(f"length 4: {n4} walks\\\\this one revisits u", (P["n0"][0] + 200, top - 4),
                           (P["n0"][0] + 200, P["n0"][1] + 4), gap=6)),
    ]
    assert frames[0] == _w5_scene()
    F.emit_frames("w5-walks", frames, container="col", h=W5_H, hmod=W5_HMOD, box=W5_BOX)


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
# C and E sit where an edge climbs away on one side; their numbers lean to the free side so a
# four-character value ("0.55") never lies across an edge
BT_DX = {"C": 26, "E": -26}


def bt_value(n, s, color="ink"):
    x, y = BT_POS[n]
    return F.text(x + BT_DX.get(n, 0), y + BT_SIDE[n] * BT_GAP, s, color=color)


def bt_scene(vals=None, colors=None, brushes="", hot=(), under=None, fill=None, under_w=22, note=None):
    """The bowtie with its edges, optional brushes under the discs, values beside the nodes.
    `hot`: nodes whose disc is the answer; `under`: the node whose value is underlined.
    `note`: (text, at, target, kwargs) of the muted callout; it must touch no disc and no value."""
    colors = colors or {}
    o = edges_tex(S.BT.edges, BT_POS) + brushes
    o += discs_tex(BT_POS, {n: n for n in BT_POS}, hot=hot, fill=fill)
    boxes = []
    for n, s in (vals or {}).items():
        o += bt_value(n, s, colors.get(n, "ink"))
        x, y = BT_POS[n]
        boxes.append(F.label_box(x + BT_DX.get(n, 0), y + BT_SIDE[n] * BT_GAP, s, "center", pad=2))
    if under:
        x, y = BT_POS[under]
        yy = y + BT_SIDE[under] * BT_GAP - 18
        o += F.underline(x - under_w, x + under_w, yy, color="hot")
    if note:
        text, at, target, kw = note
        kw = {"anchor": "center", **kw}
        o += callout(boxes, BT_POS.values(), text, at, target, **kw)
    return o


# the callout band: above the drawing between the two corner values, one line (or two) centred
BT_TOP = (BT_POS["D"][0], 322)                        # one-line note, centred over D
BT_TOP2 = (BT_POS["D"][0], 272)                       # two-line note, its bottom edge here
BT_ABOVE_D = (BT_POS["D"][0], BT_POS["D"][1] + 24)     # arrow stops above D's disc
LB = "\\\\"


def closeness_frames():
    """Six frames; each has a callout.  Returns the callout frames, the last frame without its
    callout (bowtie-closeness) and the closeness values."""
    G = S.BT
    sums = S.dsum(G)
    assert S.argbest(sums, min) == (["D"], 10) and sums["A"] == 15      # D smallest, A the example
    assert [sums[n] for n in BT_NODES] == [15, 15, 11, 10, 11, 15, 15]
    L = S.dist(G, "A")
    assert sum(L.values()) == 15 and sorted(L.values()) == [0, 1, 1, 2, 3, 4, 4]
    assert sorted(L[n] for n in BT_NODES if n != "A") == [1, 1, 2, 3, 4, 4]
    N = len(G)
    clo = {n: f"{(N - 1) / sums[n]:.2f}" for n in BT_NODES}               # c_i = (N-1) / sum: higher is better
    assert clo == {"A": "0.40", "B": "0.40", "C": "0.55", "D": "0.60", "E": "0.55", "F": "0.40", "G": "0.40"}, clo
    apos = BT_POS["A"]
    a15 = (apos[0], apos[1] + BT_GAP)                                     # where A's number sits
    allsum = {n: str(sums[n]) for n in BT_NODES}
    dval = (BT_POS["D"][0], BT_POS["D"][1] - BT_GAP)
    frames = [
        bt_scene(),                                                       # the bare bowtie
        bt_scene({n: str(k) for n, k in L.items() if n != "A"}, fill={"A": "cool"},
                 note=("distances from A", (270, 324), (apos[0] + 24, apos[1] + 8),
                       dict(gap=14, tip=(122, 322)))),
        bt_scene({"A": "15"}, fill={"A": "cool"},
                 note=("1+1+2+3+4+4 = 15", (290, 324), (a15[0] + 22, a15[1] - 4),
                       dict(gap=6, tip=(146, 322)))),
        bt_scene(allsum, note=("every node's sum", (BT_POS["D"][0], 64), (dval[0], dval[1] - 20),
                               dict(gap=4))),
        bt_scene({**allsum, "A": clo["A"]},
                 note=("6/15 = 0.40", (290, 324), (a15[0] + 40, a15[1] - 4), dict(gap=6, tip=(184, 322)))),
    ]
    last = dict(clo)
    kw = dict(colors={"D": "hot"}, hot=["D"], under="D", under_w=34)
    plain = bt_scene(last, **kw)
    frames.append(bt_scene(last, **kw, note=("highest: D", BT_TOP, BT_ABOVE_D, dict(gap=2))))
    return frames, plain, clo


def closeness_def():
    frames, plain, _ = closeness_frames()
    assert len(frames) == 6
    F.emit_frames("closeness-def", frames, container="col", h=BT_H, box=BT_BOX)
    F.emit("bowtie-closeness", plain, container="col", h=BT_H, box=BT_BOX)


def ecc_def():
    G = S.BT
    ecc = S.eccentricity(G)
    assert S.argbest(ecc, min) == (["D"], 2)
    assert [ecc[n] for n in BT_NODES] == [4, 4, 3, 2, 3, 4, 4]
    _, plain, _ = closeness_frames()
    L = S.dist(G, "A")
    far = min(n for n in sorted(L) if L[n] == ecc["A"])                  # the alphabetically first farthest
    path = tuple(nx.shortest_path(G, "A", far))
    adjacent(G, path)
    assert far == "F" and path == ("A", "C", "D", "E", "F") and len(path) - 1 == ecc["A"] == 4
    allecc = {n: str(ecc[n]) for n in BT_NODES}
    d = BT_POS["D"]
    frames = [
        plain,                                                            # = bowtie-closeness
        bt_scene({"A": "4"}, brushes=route(BT_POS, path),
                 note=(f"A's farthest:{LB}{ecc['A']} steps", (BT_POS["D"][0] + 52, BT_TOP2[1]),
                       (BT_POS["D"][0] + 52, BT_POS["D"][1] + 11), dict(gap=3, anchor="south"))),
        bt_scene(allecc, note=(f"every node's{LB}worst case", BT_TOP2, BT_ABOVE_D, dict(gap=2, anchor="south"))),
        bt_scene(allecc, colors={"D": "hot"}, hot=["D"], under="D",
                 note=("smallest: D", BT_TOP, BT_ABOVE_D, dict(gap=2))),
    ]
    F.emit_frames("ecc-def", frames, container="col", h=BT_H, box=BT_BOX)


def btw_def():
    G = S.BT
    btw = S.betweenness(G)
    assert S.argbest(btw) == (["D"], 9) and btw["C"] == btw["E"] == 8
    pairs = []
    for s_, t_ in itertools.combinations(BT_NODES, 2):
        ps = list(nx.all_shortest_paths(G, s_, t_))
        assert len(ps) == 1                                     # every shortest path is unique here
        if len(ps[0]) > 2:
            pairs.append((s_, t_, tuple(ps[0])))
    count = {n: 0 for n in G}
    for s_, t_, p in pairs:
        for i in p[1:-1]:
            count[i] += 1
    assert {n: count[n] for n in G} == {n: int(btw[n]) for n in G}
    assert len(pairs) == 13 and count["D"] == 9
    fromA = [(t_, p) for s_, t_, p in pairs if s_ == "A"]
    assert len(fromA) == 4
    cA = {n: 0 for n in G}
    for _t, p in fromA:
        for i in p[1:-1]:
            cA[i] += 1
    af = ("A", "C", "D", "E", "F")
    assert af in [p for _t, p in fromA]
    assert (cA["C"], cA["D"], cA["E"]) == (4, 3, 2)
    allc = {n: str(c) for n, c in count.items()}
    assert [allc[n] for n in "CDE"] == ["8", "9", "8"] and allc["A"] == allc["G"] == "0"
    one = {n: "1" for n in "CDE"}
    frames = [
        bt_scene(),                                             # the bare bowtie
        bt_scene(one, brushes=route(BT_POS, af),
                 note=("A to F passes C, D, E", BT_TOP, (BT_POS["C"][0] + 54, BT_POS["C"][1] + 9),
                       dict(gap=2, tip=(BT_POS["C"][0] + 54, 304)))),
        bt_scene({n: str(c) for n, c in cA.items() if c},
                 brushes="".join(route(BT_POS, p) for _t, p in fromA),
                 note=("all of A's letters", BT_TOP, BT_ABOVE_D, dict(gap=2))),
        bt_scene(allc, note=("every pair", BT_TOP, BT_ABOVE_D, dict(gap=2))),
        bt_scene(allc, colors={"D": "hot"}, hot=["D"], under="D",
                 note=("D carries the most", BT_TOP, BT_ABOVE_D, dict(gap=2))),
    ]
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
# Degree is in both rows: a shortest path of length 1 and a walk of length 1 are one edge.
ROW1 = [("degree", ["paths of", "length 1"]),
        ("closeness", ["sum of", "lengths"]),
        ("harmonic", ["sum of", "1/length"]),
        ("eccentricity", ["longest", "distance"]),
        ("betweenness", ["paths passing", "through"])]
ROW2 = [("degree", ["walks of", "length 1"]),
        ("Katz", ["all", "lengths,", "discounted"]),
        ("eigenvector", ["the longest", "walks"]),
        ("HITS", ["walks that", "alternate", "direction"]),
        ("PageRank", ["walks that", "split the", "vote"])]
CELL_GAP = 6                      # between two boxes
PADX = 14                         # at least this much white between the longest line and the border


def _need(cell):
    name, desc = cell
    return max(len(t) for t in [name] + desc) * 0.6 * F.FONT + 2 * PADX


DEG_W = max(_need(ROW1[0]), _need(ROW2[0]))   # the two degree cells: one width, one column


def _cells(row, y0, y1):
    """Cell widths follow the longest line (Meslo: 0.6 em per character), so a long word such as
    "eigenvector" never touches its border; the spare width is shared equally among all cells
    but the first (degree), which has the same width in both rows so the two line up."""
    need = [DEG_W] + [_need(c) for c in row[1:]]
    spare = (GX1 - GX0) - sum(need) - CELL_GAP * (len(row) - 1)
    assert spare >= 0, "the grid row does not fit"
    out, x = [], GX0
    for i, ((name, desc), w) in enumerate(zip(row, need)):
        w += spare / (len(row) - 1) if i else 0
        out.append(dict(name=name, desc=desc, x0=x, x1=x + w, y0=y0, y1=y1))
        x += w + CELL_GAP
    return out


CELLS1 = _cells(ROW1, ROW1_Y0, ROW1_Y1)
CELLS2 = _cells(ROW2, ROW2_Y0, ROW2_Y1)
assert CELLS1[0]["name"] == CELLS2[0]["name"] == "degree"
assert (CELLS1[0]["x0"], CELLS1[0]["x1"]) == (CELLS2[0]["x0"], CELLS2[0]["x1"]), "degree: one column"
# geometry asserts: cells inside the canvas, no overlap
for _row in (CELLS1, CELLS2):
    for _a, _b in zip(_row, _row[1:]):
        assert _a["x1"] < _b["x0"]
    assert _row[0]["x0"] >= GX0 and _row[-1]["x1"] <= GX1 + 1e-6
# every line of text fits inside its cell (Meslo is 0.6 em per character), with 2 bp to spare
for _c in CELLS1 + CELLS2:
    for _t in [_c["name"]] + _c["desc"]:
        assert 0.6 * F.FONT * len(_t) + 2 * PADX <= _c["x1"] - _c["x0"] + 1e-6, f"{_t!r} overflows its cell"
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
    o = F.text(GM, HEAD_Y, "\\textit{%s}" % HEAD_ROUTES, color="muted", anchor="west")
    o += F.text(GX1, HEAD_Y, "\\textit{%s}" % HEAD_NUMBER, color="muted", anchor="east")
    o += F.text(GX0, CAP1_Y, "shortest paths", anchor="west")
    o += F.text(GX0, CAP2_Y, "walks", anchor="west")
    for c in CELLS1[row1:] + CELLS2[row2:]:
        o += _ghost(c)
    for c in CELLS1[:row1] + CELLS2[:row2]:
        o += _cell_tex(c, c["name"] in new)
    return o


def _grid_fig(name, row1, row2, new=()):
    F.emit(name, _grid(row1, row2, new), container="full", h=GH, hmod="tall", nodes=False, box=GRID_BOX)


def grid_empty():
    _grid_same_picture()
    _grid_fig("grid-empty", 1, 1)


def grid_row1():
    _grid_fig("grid-row1", 5, 1, new=[c[0] for c in ROW1[1:]])


def grid_row2():
    _grid_fig("grid-row2", 5, 3, new=["Katz", "eigenvector"])


def grid_final():
    _grid_fig("grid-final", 5, 5, new=["HITS", "PageRank"])


def _grid_same_picture():
    """The four states are one picture: every cell that appears is drawn at the same place."""
    plain = lambda t: re.sub(r"\\textcolor\{hot\}\{(\w+)\}", r"\1", t).replace("draw=hot", "draw=ink")
    big = set(plain(_grid(5, 5)).splitlines())
    for part in (_grid(1, 1), _grid(5, 1, [c[0] for c in ROW1[1:]]), _grid(5, 3, ["Katz", "eigenvector"])):
        for line in plain(part).splitlines():
            assert "pale" in line or line in big, f"grid state differs from the final picture: {line[:60]}"
    assert "pale" not in _grid(5, 5)                                   # the final table has no empty slot


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

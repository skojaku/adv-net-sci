#!/usr/bin/env python3
"""Definition figures of Module 06: the two ways to count, one GIF per definition, the grid.

    w5-blank, w5-walks.gif        slides 9, 10   how far is u from v: shortest path or walks
    closeness-def.gif             slide 13       distances ring by ring, the sum, every node's sum
    harmonic-def.gif              slide 20       the same on the cut graph, 1/length, 1/inf = 0
    ecc-def.gif                   slide 24       the farthest node from each node in turn
    btw-def.gif                   slide 29       a letter for every pair, a counter on each carrier
    grid-empty/-row1/-row2/-final slides 11, 34, 57, 68   one table in four states

Every number is read from `smallgraphs`; the facts a figure draws are asserted at build time.
"""

import math

import networkx as nx

import figlib as F
import smallgraphs as S

RED, BLUE, DIM = "accenttwo", "accent", "annot"
GOLD = "accentthree"

CAP_ARROW = "-{Stealth[length=13bp,width=13bp]}"


# --------------------------------------------------------------------------- helpers
def place(XY, s, ox, oy, sy=None):
    """Grid units -> bp, y up, with grid (0, 0) of the lowest-left node at (ox, oy).
    `sy`: a different vertical scale, when the drawing needs a flatter angle for its labels."""
    sy = s if sy is None else sy
    x0 = min(p[0] for p in XY.values())
    y0 = min(p[1] for p in XY.values())
    return {n: (ox + (x - x0) * s, oy + (y - y0) * sy) for n, (x, y) in XY.items()}


def pin(box, c="black!30"):
    """Four specks at the corners of a box that the drawing must keep.

    figlib crops each figure to its ink, so two figures of one picture would otherwise be
    cropped differently and the picture would jump when the slide advances. The specks
    (1.4 bp, 30 % gray) fix the crop box and are not visible at slide size.
    """
    x0, y0, x1, y1 = box
    return "".join(f"\\fill[{c}] ({x},{y}) circle (0.7bp);\n" for x in (x0, x1) for y in (y0, y1))


def nodes_tex(pos, labels=None, fill=None):
    labels = labels if labels is not None else {n: n for n in pos}
    return "".join(F.disc(x, y, labels.get(n, ""), name=n, fill=(fill or {}).get(n, "accent"))
                   for n, (x, y) in pos.items())


def edges_tex(edges, dashed=()):
    out = ""
    for a, b in edges:
        if (a, b) in dashed or (b, a) in dashed:
            out += (f"\\draw[line width={F.EDGE_W}bp,draw={DIM},{F.DASH}] ({a}) -- ({b});\n")
        else:
            out += f"\\draw[line width={F.EDGE_W}bp,draw=black] ({a}) -- ({b});\n"
    return out


def cross_out(p, q, r=13, w=5.0):
    """A red x on the middle of the segment p--q: this road is closed."""
    cx, cy = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    return (F.seg((cx - r, cy - r), (cx + r, cy + r), color=RED, w=w)
            + F.seg((cx - r, cy + r), (cx + r, cy - r), color=RED, w=w))


def route(names, color=RED, w=6.5, arrow=True, opacity=None):
    """A walk through named nodes, centre to border: each hop stops at the discs."""
    o = [f"line width={w}bp", f"draw={color}"]
    if arrow:
        o.append(CAP_ARROW)
    if opacity is not None:
        o.append(f"opacity={opacity}")
    return f"\\draw[{','.join(o)}] " + " -- ".join(f"({n})" for n in names) + ";\n"


def adjacent(G, names):
    assert all(G.has_edge(a, b) for a, b in zip(names, names[1:])), f"{names} is not a walk"


def sides_for(names, pos, edges, bounds):
    """One side per label, chosen once on the widest text a node ever carries, so a number
    does not hop around between frames."""
    chosen, _ = F.place_labels(names, pos, [tuple(e) for e in edges], bounds=bounds)
    return chosen


SIDE = {"N": ("south", 0, 26), "S": ("north", 0, -26), "E": ("west", 26, 0), "W": ("east", -26, 0),
        "SL": ("north", -12, -30),          # below, nudged left: clear of an edge leaving to the SE
        "NE": ("south west", 20, 20), "NW": ("south east", -20, 20),
        "SE": ("north west", 20, -20), "SW": ("north east", -20, -20)}


def tight_box(x, y, s, anchor, size=F.FONT, pad=3):
    """figlib.label_box with the width of the real glyphs (digits and the slash are 0.5 em in
    Latin Modern) instead of the generous 0.55 em, for labels that are numbers only."""
    old = F.CHAR_W
    F.CHAR_W = 0.5
    try:
        return F.label_box(x, y, s, anchor, size=size, pad=pad)
    finally:
        F.CHAR_W = old


def sides_pref(names, pos, edges, bounds, pref):
    """Each label takes the first side of its preference list that collides with nothing
    (other labels, any disc, any edge, the bounds); a node with no free side is an error."""
    chosen, boxes = {}, {}
    for n in names:
        # the stated preferences first, then every other side, the one facing away from the
        # node's neighbours first
        nb = [pos[m] for m in {x for e in edges for x in e if n in e and x != n}]
        cx = sum(p[0] for p in nb) / len(nb)
        cy = sum(p[1] for p in nb) / len(nb)
        away = lambda k: -((SIDE[k][1]) * (cx - pos[n][0]) + (SIDE[k][2]) * (cy - pos[n][1]))
        rest = sorted((k for k in SIDE if k not in pref[n]), key=away, reverse=True)
        for key in list(pref[n]) + rest:
            anc, dx, dy = SIDE[key]
            b = tight_box(pos[n][0] + dx, pos[n][1] + dy, names[n], anc)
            inside = bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]
            if (inside and not any(F.box_hits_disc(b, x, y) for x, y in pos.values())
                    and not any(F.boxes_overlap(b, o) for o in boxes.values())
                    and not any(F.box_hits_segment(b, pos[a], pos[c]) for a, c in edges)):
                chosen[n], boxes[n] = SIDE[key], b
                break
        else:
            raise AssertionError(f"no free side for the label of {n}; placed so far {[(k, [round(v) for v in b]) for k, b in boxes.items()]}")
    return chosen


def values_tex(vals, pos, chosen, colors=None):
    """Print each value beside its node, on the side picked in `chosen`."""
    o = ""
    for n, s in vals.items():
        anc, dx, dy = chosen[n]
        o += F.text(pos[n][0] + dx, pos[n][1] + dy, s, color=(colors or {}).get(n, "black"),
                    anchor=anc)
    return o


def widest(*dicts):
    out = {}
    for d in dicts:
        for n, s in d.items():
            if n not in out or len(s) > len(out[n]):
                out[n] = s
    return out


def frac(x):
    """A Fraction or int as text with a slash; 'inf' never appears (a cut graph is not asked)."""
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


# =========================================================================== W5
# Module 01's five-node graph, stretched to fill the column (the picture is a diagram, only
# the adjacency matters). u top right, v bottom centre.
W5_W, W5_H = F.COL_W, 420
W5_SX, W5_SY = 380, 118
W5_POS = {n: (78 + (x - 0.0) * W5_SX, 60 + (y + 0.9) * W5_SY) for n, (x, y) in S.W5_XY.items()}
W5_CAP_Y = 358
W5_PIN = (14, 38, W5_W - 14, 390)
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


def _w5_base(highlight="", caption="", extra=""):
    return (pin(W5_PIN) + nodes_tex(W5_POS, W5_LAB) + edges_tex(S.W5.edges) + highlight + extra
            + (F.text(W5_W / 2, W5_CAP_Y, caption) if caption else ""))


def w5_blank():
    F.emit("w5-blank", _w5_base(), container="col", h=W5_H)


def w5_walks():
    d, sps, walks = _w5_facts()
    assert ("u", "n2", "v") in sps and ("u", "n3", "v") in sps
    a, b = ("u", "n2", "v"), ("u", "n3", "v")
    assert a in walks[2] and b in walks[2] and len(walks[2]) == 2
    c, = walks[3]
    assert c == ("u", "n0", "n2", "v"), c
    n2, n3, n4 = len(walks[2]), len(walks[3]), len(walks[4])
    red = lambda s: f"\\textcolor{{accenttwo}}{{{s}}}"
    final = (f"walks of length 2, 3, 4: {red(f'{n2}, {n3}, {n4}')}")
    frames = [
        _w5_base(route(a), f"shortest path: {d}"),
        _w5_base(route(a), "length 2: first walk"),
        _w5_base(route(b), "length 2: second walk"),
        _w5_base(route(a) + route(b), f"length 2: {n2} walks"),
        _w5_base(route(c), f"length 3: {n3} walk"),
        _w5_base("", final),
    ]
    ms = [1500, 800, 800, 1300, 1400, 1500]
    F.emit_gif("w5-walks", frames, container="col", h=W5_H, durations=ms, hold=3)


# =========================================================================== BT (closeness, ecc, btw)
BT_S = 76
BT_POS = place(S.BT_XY, BT_S, 78, 118)
BT_CAP_Y = 30
BT_BOUNDS = (8, 66, F.COL_W - 8, 400)
BT_H = 420
F.assert_planar_drawing(list(S.BT.edges), BT_POS, "BT")


def bt_scene(vals=None, colors=None, extra="", caption="", marks=(), chosen=None):
    o = nodes_tex(BT_POS) + edges_tex(S.BT.edges) + extra
    for n in marks:
        o += F.mark(*BT_POS[n])
    if vals:
        o += values_tex(vals, BT_POS, chosen, colors)
    if caption:
        o += F.text(F.COL_W / 2, BT_CAP_Y, caption)
    return o


def closeness_def():
    G = S.BT
    sums = S.dsum(G)
    assert S.argbest(sums, min) == (["D"], 10) and sums["A"] == 15      # D smallest, A the example
    L = S.dist(G, "A")
    assert sum(L.values()) == 15 and sorted(L.values()) == [0, 1, 1, 2, 3, 4, 4]
    rings = {k: [n for n in sorted(L) if L[n] == k] for k in range(1, 5)}
    assert rings == {1: ["B", "C"], 2: ["D"], 3: ["E"], 4: ["F", "G"]}
    names = widest({n: str(x) for n, x in sums.items()}, {n: str(x) for n, x in L.items()})
    ch = sides_for(names, BT_POS, S.BT.edges, BT_BOUNDS)
    frames, shown = [], {}
    frames.append(bt_scene(caption="distances from A", marks=["A"], chosen=ch))
    for k in range(1, 5):
        shown.update({n: str(k) for n in rings[k]})
        frames.append(bt_scene(dict(shown), caption=("1 step" if k == 1 else f"{k} steps"),
                               marks=["A"], chosen=ch))
    terms = "+".join(str(L[n]) for n in sorted(L) if n != "A")
    assert eval(terms) == 15
    frames.append(bt_scene({**shown, "A": "15"}, colors={"A": RED}, marks=["A"], chosen=ch,
                           caption=f"sum = {terms} = 15"))
    allsum = {n: str(x) for n, x in sums.items()}
    frames.append(bt_scene(allsum, colors={"D": RED}, marks=["D"], chosen=ch,
                           caption=f"smallest sum: D, {sums['D']}"))
    ms = [900, 800, 800, 800, 800, 1700, 1500]
    F.emit_gif("closeness-def", frames, container="col", h=BT_H, durations=ms, hold=3)


def ecc_def():
    G = S.BT
    ecc = S.eccentricity(G)
    assert S.argbest(ecc, min) == (["D"], 2)
    names = {n: str(x) for n, x in ecc.items()}
    ch = sides_for(names, BT_POS, S.BT.edges, BT_BOUNDS)
    frames, shown = [], {}
    for u in sorted(G):
        L = S.dist(G, u)
        far = min(n for n in sorted(L) if L[n] == ecc[u])         # the alphabetically first farthest
        path = tuple(nx.shortest_path(G, u, far))
        adjacent(G, path)
        assert len(path) - 1 == ecc[u] == L[far]
        shown[u] = str(ecc[u])
        frames.append(bt_scene(dict(shown), colors={u: RED},
                               extra=route(path, w=6.0),
                               caption=f"{u}: farthest is {far}, {ecc[u]} steps", chosen=ch))
    frames.append(bt_scene(names, colors={"D": RED}, marks=["D"], chosen=ch,
                           caption=f"smallest eccentricity: D, {ecc['D']}"))
    ms = [900] + [800] * 6 + [1700]
    F.emit_gif("ecc-def", frames, container="col", h=BT_H, durations=ms, hold=3)


def btw_def():
    G = S.BT
    btw = S.betweenness(G)
    assert S.argbest(btw) == (["D"], 9) and btw["C"] == btw["E"] == 8
    pairs = []
    import itertools
    for s, t in itertools.combinations(sorted(G), 2):
        ps = list(nx.all_shortest_paths(G, s, t))
        assert len(ps) == 1                                     # every shortest path is unique here
        if len(ps[0]) > 2:
            pairs.append((s, t, tuple(ps[0])))
    count = {n: 0 for n in G}
    for s, t, p in pairs:
        for i in p[1:-1]:
            count[i] += 1
    assert {n: count[n] for n in G} == {n: int(btw[n]) for n in G}
    assert len(pairs) == 13
    names = {n: str(int(btw[n])) for n in G}
    ch = sides_for(names, BT_POS, S.BT.edges, BT_BOUNDS)
    frames, ms = [], []
    frames.append(bt_scene(caption="a letter for every pair", chosen=ch))
    ms.append(1100)
    run = {n: 0 for n in G}
    for s, t, p in pairs:
        inner = p[1:-1]
        for i in inner:
            run[i] += 1
        vals = {n: str(c) for n, c in run.items() if c}
        frames.append(bt_scene(vals, colors={i: RED for i in inner},
                               extra=route(p, w=6.0),
                               caption=f"letter from {s} to {t}", chosen=ch))
        ms.append(700)
    assert run == count
    frames.append(bt_scene({n: str(c) for n, c in count.items()}, colors={"D": RED},
                           marks=["D"], chosen=ch,
                           caption=f"D carries the most: {count['D']}"))
    ms.append(1700)
    F.emit_gif("btw-def", frames, container="col", h=BT_H, durations=ms, hold=3)


# =========================================================================== harmonic on CA_CUT
CA_S, CA_SY = 66, 58          # horizontal, vertical bp per grid unit: flat enough that G's value
CA_POS = place(S.CA_XY, CA_S, 34, 104, CA_SY)     # fits under G between the edges G-F and G-J
CA_CAP_Y = 30
CA_BOUNDS = (8, 56, F.COL_W - 8, 380)
CA_H = 420
F.assert_planar_drawing(list(S.CA.edges), CA_POS, "CA")


def harmonic_def():
    G = S.CA_CUT
    h = S.harmonic(G)
    assert S.argbest(h) == (["G"], S.Fr(9, 2)) and h["G"] == S.Fr(9, 2)
    L = S.dist(G, "G")
    one = [n for n in sorted(L) if L[n] == 1]
    two = [n for n in sorted(L) if L[n] == 2]
    other = [n for n in sorted(G) if n not in L]
    assert one == ["F", "H", "I", "J"] and two == ["K"] and other == list("ABCDE")
    assert 4 * S.Fr(1) + S.Fr(1, 2) == h["G"]
    cut = ("E", "F")
    assert not G.has_edge(*cut) and S.CA.has_edge(*cut)
    edges = list(S.CA.edges)
    final = {n: frac(x) for n, x in h.items()}
    names = widest(final, {n: "1/1" for n in one})
    # G's value goes directly below G (nudged left to clear the edge G-J), so it sits near G
    # and not near F, which is 0.8 grid units away and carries its own value above it.
    pref = {"A": ["N", "NE", "NW"], "B": ["NW", "W"], "C": ["SW", "W"], "D": ["S", "SE", "SW"],
            "E": ["SE", "NE"], "F": ["NW", "N"], "G": ["SL", "S"], "H": ["E", "NE"], "I": ["E"],
            "J": ["S", "SW"], "K": ["E", "S"]}
    ch = sides_pref(names, CA_POS, [tuple(e) for e in edges], CA_BOUNDS, pref)

    def centre(n):                       # where the value of n is drawn
        anc, dx, dy = ch[n]
        return CA_POS[n][0] + dx, CA_POS[n][1] + dy + (-14 if dy < 0 else 14 if dy > 0 else 0)
    gx, gy = centre("G")
    assert (math.hypot(gx - CA_POS["G"][0], gy - CA_POS["G"][1])
            < 0.85 * math.hypot(gx - CA_POS["F"][0], gy - CA_POS["F"][1])), "G's value is not clearly nearer G than F"

    def scene(vals=None, colors=None, caption="", marks=()):
        o = nodes_tex(CA_POS) + edges_tex(edges, dashed=[cut]) + cross_out(CA_POS["E"], CA_POS["F"])
        for n in marks:
            o += F.mark(*CA_POS[n])
        if vals:
            o += values_tex(vals, CA_POS, ch, colors)
        if caption:
            o += F.text(F.COL_W / 2, CA_CAP_Y, caption)
        return o

    v1 = {n: "1/1" for n in one}
    v2 = {**v1, "K": "1/2"}
    v3 = {**v2, **{n: "0" for n in other}}
    frames = [
        scene(caption="the road E-F is closed", marks=["G"]),
        scene(v1, caption="one step away: 1/1", marks=["G"]),
        scene(v2, caption="two steps away: 1/2", marks=["G"]),
        scene(v3, caption="no way there: 1/$\\infty$ = 0", marks=["G"]),
        scene({**v3, "G": "9/2"}, colors={"G": RED}, marks=["G"],
              caption="sum = 1+1+1+1+1/2 = 9/2"),
        scene(final, colors={"G": RED}, marks=["G"], caption="highest: G, 9/2"),
    ]
    ms = [1100, 900, 900, 1100, 1700, 1700]
    F.emit_gif("harmonic-def", frames, container="col", h=CA_H, durations=ms, hold=3)


# =========================================================================== the grid
GW, GH = F.FULL_W, 420
GM = 14                           # outer margin
LAB_W = 111                       # width of the widest row label ("shortest")
GX0, GX1 = GM + LAB_W + 10, GW - GM
LINE = int(F.FONT * 1.15)
PADY = 5
ROW1_H = 3 * LINE + 2 * PADY      # name + two lines
ROW2_H = 4 * LINE + 2 * PADY      # name + three lines
ROW_GAP = 8
ROW2_Y0 = 22
ROW2_Y1 = ROW2_Y0 + ROW2_H
ROW1_Y0 = ROW2_Y1 + ROW_GAP
ROW1_Y1 = ROW1_Y0 + ROW1_H
HEAD_Y = ROW1_Y1 + 20                  # the two axis headers (grey, horizontal)
HEAD_ROUTES = "which routes count"
HEAD_NUMBER = "how they become one number"
GRID_PIN = (GM, ROW2_Y0 - 1, GW - GM, HEAD_Y + 14)

# (metric, description lines); the description of every cell is the spec's text, only broken
# into lines. Nothing is shortened.
ROW1 = [("closeness", ["sum of", "lengths"]),
        ("harmonic", ["sum of", "1/length"]),
        ("eccentricity", ["longest", "distance"]),
        ("betweenness", ["paths passing", "through"])]
ROW2 = [("degree", ["walks of", "length 1"]),
        ("Katz", ["all lengths,", "discounted"]),
        ("eigenvector", ["the longest", "walks"]),
        ("PageRank", ["walks that", "split the", "vote"]),
        ("HITS", ["walks that", "alternate", "direction"])]


def _cells(row, y0, y1):
    n = len(row)
    pitch = (GX1 - GX0) / 5 if row is ROW2 else (GX1 - GX0) / 4
    out = []
    for i, (name, desc) in enumerate(row):
        out.append(dict(name=name, desc=desc, x0=GX0 + i * pitch + 4, x1=GX0 + (i + 1) * pitch - 4,
                        y0=y0, y1=y1))
    return out


CELLS1 = _cells(ROW1, ROW1_Y0, ROW1_Y1)
CELLS2 = _cells(ROW2, ROW2_Y0, ROW2_Y1)
# geometry asserts: cells inside the canvas, no overlap, same width within a row
for _row in (CELLS1, CELLS2):
    for _a, _b in zip(_row, _row[1:]):
        assert _a["x1"] < _b["x0"]
    assert _row[0]["x0"] >= GX0 and _row[-1]["x1"] <= GX1
    assert len({round(c["x1"] - c["x0"], 6) for c in _row}) == 1
assert CELLS1[0]["x1"] - CELLS1[0]["x0"] > 200 and CELLS2[0]["x1"] - CELLS2[0]["x0"] > 170
assert ROW1_Y1 + 12 <= F.FIG_H[""] - 12 + ROW2_Y0                     # whole picture fits a plain figure


def _cell_tex(c, new=False):
    w = c["x1"] - c["x0"]
    o = (f"\\draw[line width=1.6bp,draw={DIM},rounded corners=9bp] "
         f"({c['x0']:.1f},{c['y0']}) rectangle ({c['x1']:.1f},{c['y1']});\n")
    s = "\\textcolor{%s}{%s}\\\\ %s" % ("accenttwo" if new else "black", c["name"],
                                          "\\\\ ".join(c["desc"]))
    o += F.text((c["x0"] + c["x1"]) / 2, c["y1"] - PADY, s, anchor="north")
    return o


def _rowlabel(text_lines, y0, y1):
    return F.text(GM, (y0 + y1) / 2, "\\\\ ".join(text_lines), color=BLUE, anchor="west")


def _grid(row1, row2, new=()):
    """row1, row2: how many cells of each row to draw (a prefix). `new`: names of the cells
    that are new on this slide; their centrality name is accent-2, every other name black."""
    o = pin(GRID_PIN)
    o += F.text(GM, HEAD_Y, HEAD_ROUTES, color=DIM, anchor="west")
    o += F.text((GX0 + GX1) / 2, HEAD_Y, HEAD_NUMBER, color=DIM)
    o += _rowlabel(["shortest", "paths"], ROW1_Y0, ROW1_Y1)
    o += _rowlabel(["walks"], ROW2_Y0, ROW2_Y1)
    for c in CELLS1[:row1] + CELLS2[:row2]:
        o += _cell_tex(c, c["name"] in new)
    return o


def _grid_fig(name, row1, row2, hmod, new=()):
    F.emit(name, _grid(row1, row2, new), container="full", h=GH, hmod=hmod, nodes=False)


def grid_empty():
    _grid_fig("grid-empty", 0, 1, "")


def grid_row1():
    _grid_fig("grid-row1", 4, 0, "", new=[c[0] for c in ROW1])


def grid_row2():
    _grid_fig("grid-row2", 4, 3, "", new=["Katz", "eigenvector"])


def grid_final():
    # The 26 px disc floor leaves no room for an icon per cell: a 3-node icon adds >= 70 bp to a
    # row, and the table is already 330 bp of the 400 bp a tall figure may have.
    _grid_fig("grid-final", 4, 5, "tall")


def _grid_same_picture():
    """The four states are one picture: every cell that appears is drawn at the same place."""
    plain = lambda t: t.replace("{accenttwo}", "{black}")          # colour aside, the same lines
    big = plain(_grid(4, 5)).splitlines()
    parts = (_grid(0, 1), _grid(4, 0, [c[0] for c in ROW1]), _grid(4, 3, ["Katz", "eigenvector"]))
    for part in parts:
        for line in plain(part).splitlines():
            assert line in big, f"grid state differs from the final picture: {line[:60]}"
    assert "accenttwo" not in _grid(4, 5)                              # the final table: all black


_grid_same_picture()

FIGURES = [
    ("w5-blank", w5_blank),
    ("w5-walks", w5_walks),
    ("closeness-def", closeness_def),
    ("ecc-def", ecc_def),
    ("btw-def", btw_def),
    ("harmonic-def", harmonic_def),
    ("grid-empty", grid_empty),
    ("grid-row1", grid_row1),
    ("grid-row2", grid_row2),
    ("grid-final", grid_final),
]

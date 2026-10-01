#!/usr/bin/env python3
"""Figures for the deck rebuilt from the lecturer's hand sketches (2026-09-30).

The sketches set the order: what a community looks like, the clique and its three
relaxations, the cut and its two balanced versions on the karate club, then modularity,
Louvain, Leiden, the resolution limit and near-equal modularity. Figures that already
existed and still fit (the small club, `karate-plain`, `rho-dense`, `k-plex`) are reused
from `figs_story.py`; everything drawn here is new.

Every number a figure prints, and every number the deck prints beside it, is computed
and asserted in this file. The karate splits in particular are searched for, not typed:
`_best_split` runs a random-restart local search and the build fails if the partition
the slide shows is not the best one it finds.
"""

import itertools
import math
import random
from fractions import Fraction as F
from functools import lru_cache

import networkx as nx
import numpy as np

import verify_numbers as V
from figlib import FONT, NODE, assert_planar_drawing, emit, label_box, seg, text

NODE_R = NODE / 2
from figs_story import SMALL_E, SMALL_LEFT, SMALL_POS
from kfig import (
    CHI, COFF, arrow, assert_boxes_clear, clique_edges, karate, ring_positions, small,
)

FIGURES = []


def fig(name, container="full", h=380, hmod=""):
    def deco(fn):
        FIGURES.append((name, lambda: emit(name, fn(), container=container, h=h, hmod=hmod)))
        return fn
    return deco


def _k(e):
    return (min(e), max(e))


# =========================================================================== Part 1
# Four groups a room sees at once: a 5-clique, a 4-clique, five people with seven of
# their ten possible friendships, and four with five of six. One edge between
# neighbouring groups.
GROUPS = [list(range(0, 5)), list(range(5, 9)), list(range(9, 14)), list(range(14, 18))]


def _groups_graph():
    pos = {}
    pos.update(ring_positions(5, 150, 165, 100, 95, start=90, order=GROUPS[0]))
    pos.update({5: (360, 225), 6: (480, 225), 7: (360, 105), 8: (480, 105)})
    pos.update(ring_positions(5, 690, 165, 100, 95, start=90, order=GROUPS[2]))
    pos.update({14: (875, 165), 15: (945, 235), 16: (945, 95), 17: (1015, 165)})
    e = clique_edges(GROUPS[0]) + clique_edges(GROUPS[1])
    e += [(9, 10), (10, 11), (11, 12), (12, 13), (13, 9), (9, 11), (9, 12)]
    e += [(14, 15), (14, 16), (15, 17), (16, 17), (15, 16)]
    bridges = [(4, 5), (8, 11), (13, 14)]
    return pos, e + bridges, bridges


def _fit_ellipse(pts, margin=30.0):
    """The smallest axis-aligned ellipse, centred on the points' box, holding every disc."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    a0 = max(1.0, (max(xs) - min(xs)) / 2)
    b0 = max(1.0, (max(ys) - min(ys)) / 2)
    s = max(math.hypot((x - cx) / a0, (y - cy) / b0) for x, y in pts)
    return cx, cy, s * a0 + margin, s * b0 + margin


def _groups(circled):
    pos, e, bridges = _groups_graph()
    g = nx.Graph(e)
    assert nx.is_connected(g), "the example network must be one network"
    inside = [g.subgraph(c).number_of_edges() for c in GROUPS]
    assert inside == [10, 6, 7, 5], inside
    assert len(bridges) == 3
    out = ""
    if circled:
        boxes = []
        for grp in GROUPS:
            cx, cy, rx, ry = _fit_ellipse([pos[n] for n in grp])
            others = [pos[n] for n in pos if n not in grp]
            assert all(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 > 1.15 for x, y in others), \
                "a group's outline must not take in somebody from another group"
            boxes.append((cx - rx, cx + rx))
            out += (f"\\draw[line width=4.2bp,draw=accenttwo,dash pattern=on 12bp off 9bp] "
                    f"({cx:.1f},{cy:.1f}) ellipse ({rx:.1f}bp and {ry:.1f}bp);\n")
        for (l1, r1), (l2, r2) in zip(boxes, boxes[1:]):
            assert r1 < l2, "two group outlines overlap"
    out += small(pos, e, node=36, planar=False, what="groups",
                 fill={n: "annot" for n in pos})
    return out


@fig("groups-plain", h=330, hmod="tight")
def _groups_plain():
    """Eighteen people, and the groups are visible before anyone defines them."""
    return _groups(False)


@fig("groups-circled", h=330, hmod="tight")
def _groups_circled():
    """The same drawing with the four groups the room just pointed at."""
    return _groups(True)


HEX = ring_positions(6, 268, 180, 205, 140, start=0)


@fig("clique-six", container="col", h=380)
def _clique_six():
    """Six people, all fifteen friendships: no edge can be added inside."""
    e = clique_edges(list(range(6)))
    assert len(e) == 15
    return small(HEX, e, planar=False, what="clique-six", fill={n: "accent" for n in HEX})


@fig("clique-miss-one", container="col", h=380)
def _clique_miss_one():
    """The same six with one friendship gone -- and by definition no longer a clique."""
    full = clique_edges(list(range(6)))
    missing = (0, 1)
    have = [x for x in full if x != missing]
    assert len(have) == 14
    return small(HEX, have, planar=False, what="clique-miss-one", dashes=[missing],
                 edges_all=full, fill={n: "accent" for n in HEX})


@fig("n-clique-two", container="col", h=380)
def _n_clique_two():
    """A ring of five: every pair is one or two steps apart, so it is a 2-clique."""
    p = ring_positions(5, 268, 180, 215, 130, start=90)
    e = [(i, (i + 1) % 5) for i in range(5)]
    g = nx.Graph(e)
    assert nx.diameter(g) == 2
    path = [(1, 0), (0, 4)]
    assert nx.shortest_path_length(g, 1, 4) == 2
    return small(p, e, heavy=path, what="n-clique-two", fill={n: "accent" for n in p})


@fig("k-plex-two", container="col", h=380)
def _kplex_two():
    """Five members; the two dashed diagonals are the only missing edges.

    Drawn planar: the member who knows everyone sits inside the rectangle, above the
    point where the diagonals cross, so neither diagonal runs through the disc.
    """
    p = {0: (60, 300), 1: (476, 300), 2: (476, 80), 3: (60, 80), 4: (268, 244)}
    missing = [(0, 2), (1, 3)]
    have = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3)]
    g = nx.Graph(have)
    s = g.number_of_nodes()
    assert min(d for _, d in g.degree()) == s - 2, "each member reaches at least s - 2"
    assert len(have) + len(missing) == s * (s - 1) // 2
    assert_planar_drawing(have, p, "k-plex-two")
    from figlib import clearance_bad
    assert not clearance_bad(missing, p, r=NODE_R + 3), "a dashed diagonal hits a disc"
    return small(p, have, dashes=missing, edges_all=have + missing, what="k-plex-two",
                 fill={n: "accent" for n in p})


# ------------------------------------------------------------------ worked examples
# Two examples after every pseudo-clique, each with small round numbers: a learner
# meeting a definition for the first time should be checking the definition, not
# dividing 8 by 15.
def _missing(nodes, edges):
    have = {_k(e) for e in edges}
    return [e for e in itertools.combinations(nodes, 2) if _k(e) not in have]


RECT4 = {0: (60, 280), 1: (476, 280), 2: (476, 100), 3: (60, 100)}
PENT = ring_positions(5, 268, 180, 215, 130, start=90)


@fig("dense-def", container="col", h=380)
def _dense_def():
    """Five members, seven of the ten possible edges: 0.7-dense."""
    e = [(0, 1), (0, 4), (1, 2), (1, 4), (2, 3), (2, 4), (3, 4)]
    assert F(len(e), 10) == F(7, 10)
    return small(PENT, e, what="dense-def", fill={n: "accent" for n in PENT})


DENSE1_E = [(0, 1), (1, 2), (2, 3)]
DENSE2_E = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2), (0, 3), (1, 4)]


@fig("dense-ex1", container="col", h=380)
def _dense_ex1():
    assert F(len(DENSE1_E), 6) == F(1, 2)
    return small(RECT4, DENSE1_E, what="dense-ex1", fill={n: "accent" for n in RECT4})


@fig("dense-ex1-answer", container="col", h=380)
def _dense_ex1a():
    miss = _missing(RECT4, DENSE1_E)
    assert len(miss) == 3
    return small(RECT4, DENSE1_E, dashes=miss, edges_all=DENSE1_E + miss, planar=False,
                 what="dense-ex1-answer", fill={n: "accent" for n in RECT4})


@fig("dense-ex2", container="col", h=380)
def _dense_ex2():
    assert F(len(DENSE2_E), 10) == F(4, 5)
    return small(PENT, DENSE2_E, planar=False, what="dense-ex2",
                 fill={n: "accent" for n in PENT})


@fig("dense-ex2-answer", container="col", h=380)
def _dense_ex2a():
    miss = _missing(PENT, DENSE2_E)
    assert len(miss) == 2
    return small(PENT, DENSE2_E, dashes=miss, edges_all=DENSE2_E + miss, planar=False,
                 what="dense-ex2-answer", fill={n: "accent" for n in PENT})


ZIG = {0: (60, 120), 1: (200, 260), 2: (340, 120), 3: (480, 260)}
ZIG_E = [(0, 1), (1, 2), (2, 3)]
STAR = {0: (268, 185), **{i + 1: p for i, p in
                          ring_positions(5, 268, 185, 215, 130, start=90).items()}}
STAR_E = [(0, i) for i in range(1, 6)]


@fig("ncl-ex1", container="col", h=380)
def _ncl1():
    assert nx.diameter(nx.Graph(ZIG_E)) == 3
    return small(ZIG, ZIG_E, what="ncl-ex1", fill={n: "accent" for n in ZIG})


@fig("ncl-ex1-answer", container="col", h=380)
def _ncl1a():
    return small(ZIG, ZIG_E, heavy=ZIG_E, what="ncl-ex1-answer",
                 fill={n: "accent" for n in ZIG})


@fig("ncl-ex2", container="col", h=380)
def _ncl2():
    assert nx.diameter(nx.Graph(STAR_E)) == 2
    return small(STAR, STAR_E, what="ncl-ex2", fill={n: "accent" for n in STAR})


@fig("ncl-ex2-answer", container="col", h=380)
def _ncl2a():
    return small(STAR, STAR_E, heavy=[(0, 2), (0, 5)], what="ncl-ex2-answer",
                 fill={n: "accent" for n in STAR})


# --------------------------------------------------------- numbers inside the discs
NUM_NODE = 46                   # a digit at 36pt needs the room; the band is 26-52px


def _numbered(pos, edges, fill, nums=None, ghosts=(), node=NUM_NODE, what="numbered",
              planar=True):
    """Discs that carry a number, and removed nodes left as dashed outlines.

    The peeling slides need both: the number is a degree that changes from frame to
    frame, and a node that has been peeled stays visible as a ghost so the room can
    see where it was.
    """
    from figlib import clearance_bad, crossings, disc
    live = {n: p for n, p in pos.items() if n not in ghosts}
    e = [x for x in edges if x[0] in live and x[1] in live]
    if planar:
        cr = crossings(e, live)
        assert not cr, f"{what}: {len(cr)} edge crossing(s) -- {cr[:3]}"
    bad = clearance_bad(e, live, r=node / 2 + 3)
    assert not bad, f"{what}: edge passes through a disc it does not end at -- {bad[:3]}"
    out = ""
    for n in ghosts:
        x, y = pos[n]
        out += (f"\\draw[line width=2.6bp,draw=annot,dash pattern=on 6bp off 5bp] "
                f"({x:.1f},{y:.1f}) circle ({node / 2}bp);\n")
    for a, b in e:
        out += seg(live[a], live[b], color="black", w=2.8)
    for n, (x, y) in live.items():
        lab = str(nums[n]) if nums and n in nums else ""
        out += disc(x, y, label=lab, fill=fill.get(n, "annot"), size=node)
    return out


def _degrees(edges, nodes):
    g = nx.Graph(edges)
    g.add_nodes_from(nodes)
    return dict(g.degree())


RECT4N = {0: (60, 280), 1: (476, 280), 2: (476, 100), 3: (60, 100)}
CYC4_E = [(0, 1), (1, 2), (2, 3), (3, 0)]
HEX6 = ring_positions(6, 268, 190, 215, 130, start=0)
CYC6_E = [(i, (i + 1) % 6) for i in range(6)]


def _plex_k(edges, nodes):
    s = len(nodes)
    return s - min(_degrees(edges, nodes).values())


@fig("kplex-ex1", container="col", h=380)
def _kp1():
    assert _plex_k(CYC4_E, RECT4N) == 2
    return _numbered(RECT4N, CYC4_E, {n: "accent" for n in RECT4N}, what="kplex-ex1")


@fig("kplex-ex1-answer", container="col", h=380)
def _kp1a():
    return _numbered(RECT4N, CYC4_E, {n: "accent" for n in RECT4N},
                     nums=_degrees(CYC4_E, RECT4N), what="kplex-ex1-answer")


@fig("kplex-ex2", container="col", h=380)
def _kp2():
    assert _plex_k(CYC6_E, HEX6) == 4
    return _numbered(HEX6, CYC6_E, {n: "accent" for n in HEX6}, what="kplex-ex2")


@fig("kplex-ex2-answer", container="col", h=380)
def _kp2a():
    return _numbered(HEX6, CYC6_E, {n: "accent" for n in HEX6},
                     nums=_degrees(CYC6_E, HEX6), what="kplex-ex2-answer")


# ------------------------------------------------------------------ the k-core
def _peel(edges, nodes, k):
    """Peel in rounds. Returns the list of rounds (nodes removed) and the k-core."""
    g = nx.Graph(edges)
    g.add_nodes_from(nodes)
    h = g.copy()
    rounds = []
    while True:
        low = sorted(n for n, d in h.degree() if d < k)
        if not low:
            break
        rounds.append(low)
        h.remove_nodes_from(low)
    assert set(h) == set(nx.k_core(g, k)), "peeling must agree with networkx's k_core"
    return rounds, set(h), h


KDEF = {0: (120, 250), 1: (300, 250), 2: (120, 90), 3: (300, 90),
        4: (210, 350), 5: (60, 350), 6: (460, 170)}
KDEF_E = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (4, 0), (4, 1), (4, 5),
          (6, 1), (6, 3)]


@fig("kcore-def", container="col", h=380)
def _kcore_def():
    """A network and its 3-core: each blue member has 3 neighbours inside blue."""
    _, core, h = _peel(KDEF_E, KDEF, 3)
    assert core == {0, 1, 2, 3}
    inside = dict(h.degree())
    fill = {n: ("accent" if n in core else "annot") for n in KDEF}
    return _numbered(KDEF, KDEF_E, fill, nums=inside, planar=False, what="kcore-def")


# The worked example. Node 5 starts with degree 3 and still does not survive: its two
# triangle partners go in round 1, and it goes in round 2.
PEEL = {0: (520, 190), 1: (190, 300), 2: (190, 80), 3: (300, 190), 4: (720, 190),
        5: (880, 190), 6: (1010, 290), 7: (1010, 90), 8: (60, 310), 9: (60, 190)}
PEEL_E = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (2, 3), (1, 4), (2, 4),
          (4, 5), (5, 6), (5, 7), (6, 7), (1, 8), (1, 9), (2, 9)]


def _peel_facts():
    rounds, core, _ = _peel(PEEL_E, PEEL, 3)
    assert rounds == [[6, 7, 8, 9], [5]] and core == {0, 1, 2, 3, 4}
    assert _degrees(PEEL_E, PEEL)[5] == 3, "the trap: node 5 starts at degree 3"
    return rounds, core


def _peel_frame(removed, red, blue=()):
    live_e = [e for e in PEEL_E if e[0] not in removed and e[1] not in removed]
    deg = _degrees(live_e, [n for n in PEEL if n not in removed])
    fill = {n: ("accenttwo" if n in red else "accent" if n in blue else "annot")
            for n in PEEL}
    return _numbered(PEEL, PEEL_E, fill, nums=deg, ghosts=removed, what="peel")


@fig("peel-0", h=380)
def _peel0():
    _peel_facts()
    return _peel_frame(removed=set(), red=set())


@fig("peel-1", h=380)
def _peel1():
    rounds, _ = _peel_facts()
    return _peel_frame(removed=set(), red=set(rounds[0]))


@fig("peel-2", h=380)
def _peel2():
    rounds, _ = _peel_facts()
    return _peel_frame(removed=set(rounds[0]), red=set(rounds[1]))


@fig("peel-3", h=380)
def _peel3():
    rounds, core = _peel_facts()
    return _peel_frame(removed=set(rounds[0]) | set(rounds[1]), red=set(), blue=core)


# Example 1: the 2-core. The branch goes one node at a time; the node on the path
# between the square and the triangle has degree 2 and stays.
KEX1 = {0: (90, 290), 1: (250, 290), 2: (250, 100), 3: (90, 100), 7: (450, 100),
        4: (650, 120), 5: (790, 260), 6: (830, 90), 8: (420, 300), 9: (580, 310),
        10: (960, 320), 11: (990, 210)}
KEX1_E = [(0, 1), (1, 2), (2, 3), (3, 0), (2, 7), (7, 4), (4, 5), (4, 6), (5, 6),
          (1, 8), (8, 9), (5, 10), (5, 11)]

# Example 2: the 3-core comes in two pieces.
KEX2 = {0: (70, 190), 1: (170, 300), 2: (170, 80), 3: (270, 190), 8: (430, 250),
        9: (650, 250), 4: (810, 190), 5: (910, 300), 6: (910, 80), 7: (1010, 190)}
KEX2_E = clique_edges([0, 1, 2, 3]) + clique_edges([4, 5, 6, 7]) + [(3, 8), (8, 9), (9, 4)]


def _kex(pos, edges, k, answer):
    rounds, core, h = _peel(edges, pos, k)
    removed = set().union(*map(set, rounds)) if rounds else set()
    if not answer:
        return _numbered(pos, edges, {n: "annot" for n in pos}, planar=False,
                         what="kcore-ex")
    fill = {n: "accent" for n in core}
    return _numbered(pos, edges, fill, nums=dict(h.degree()), ghosts=removed,
                     planar=False, what="kcore-ex-answer")


@fig("kcore-ex1", h=380)
def _kex1():
    rounds, core, _ = _peel(KEX1_E, KEX1, 2)
    assert rounds == [[9, 10, 11], [8]] and core == {0, 1, 2, 3, 4, 5, 6, 7}
    return _kex(KEX1, KEX1_E, 2, answer=False)


@fig("kcore-ex1-answer", h=380)
def _kex1a():
    return _kex(KEX1, KEX1_E, 2, answer=True)


@fig("kcore-ex2", h=380)
def _kex2():
    rounds, core, h = _peel(KEX2_E, KEX2, 3)
    assert rounds == [[8, 9]] and core == set(range(8))
    assert nx.number_connected_components(h) == 2, "the 3-core must be in two pieces"
    return _kex(KEX2, KEX2_E, 3, answer=False)


@fig("kcore-ex2-answer", h=380)
def _kex2a():
    return _kex(KEX2, KEX2_E, 3, answer=True)


CORE_COLS = {4: "accent", 3: "accenttwo", 2: "accentthree", 1: "annot"}


@fig("karate-core", h=380)
def _karate_core():
    """The club coloured by core number: the largest k whose k-core holds the member."""
    c = nx.core_number(_karate_simple())
    counts = {k: sum(1 for v in c.values() if v == k) for k in range(1, 5)}
    assert counts == {1: 1, 2: 11, 3: 12, 4: 10}, counts
    return karate(fill={n: CORE_COLS[c[n]] for n in range(34)})


# =========================================================================== Part 2
def _small_graph():
    return nx.Graph(SMALL_E)


def _squash(pos, sx=1.0, sy=1.0, x0=46.0, nx0=46.0, cy=214.0, dx=0.0):
    """The small club rescaled: `sx` about x0 (moved to nx0), `sy` about the midline."""
    return {n: (nx0 + (x - x0) * sx + dx, cy + (y - cy) * sy) for n, (x, y) in pos.items()}


def _two_sides(left):
    return {n: (CHI if n in left else COFF) for n in SMALL_POS}


def _crossing(left):
    return [e for e in SMALL_E if (e[0] in left) != (e[1] in left)]


def _vol(g, S):
    return sum(d for _, d in g.degree(S))


@lru_cache(maxsize=None)
def _small_numbers():
    """Every score the cut slides print, from the one graph."""
    g = _small_graph()
    n, m = g.number_of_nodes(), g.number_of_edges()
    L = set(SMALL_LEFT)
    lone = {9}
    out = {
        "n": n, "m": m,
        "cut_bal": V.cut_size(g, L), "cut_lone": V.cut_size(g, lone),
        "rc_bal": F(V.cut_size(g, L), len(L) * (n - len(L))),
        "rc_lone": F(V.cut_size(g, lone), 1 * (n - 1)),
        "vol_l": _vol(g, L), "vol_r": _vol(g, set(g) - L), "vol_lone": _vol(g, lone),
    }
    out["nc_bal"] = F(out["cut_bal"], out["vol_l"] * out["vol_r"])
    out["nc_lone"] = F(out["cut_lone"], out["vol_lone"] * (2 * m - out["vol_lone"]))
    assert (n, m) == (9, 15)
    assert (out["cut_bal"], out["cut_lone"]) == (2, 1)
    assert (out["rc_bal"], out["rc_lone"]) == (F(1, 10), F(1, 8))
    assert (out["vol_l"], out["vol_r"], out["vol_lone"]) == (16, 14, 1)
    assert (out["nc_bal"], out["nc_lone"]) == (F(1, 112), F(1, 29))
    # the minimum cut really is the lone node, and nothing cheaper exists
    assert nx.edge_connectivity(g) == 1
    # inside edges and the configuration-model expectation, for Part 3
    out["inside"] = m - out["cut_bal"]
    out["expected_inside"] = F(out["vol_l"] ** 2 + out["vol_r"] ** 2, 4 * m)
    out["Q"] = (out["inside"] - out["expected_inside"]) / m
    assert out["inside"] == 13 and out["expected_inside"] == F(113, 15)       # 7.53
    assert abs(float(out["Q"]) - V.unweighted_Q(g, [L, set(g) - L])) < 1e-12
    assert f"{float(out['Q']):.2f}" == "0.36"
    return out


@fig("cut-plain", h=380)
def _cut_plain():
    """Nine people. Where would you draw the line?"""
    return small(dict(SMALL_POS), list(SMALL_E), what="cut-plain",
                 fill={n: "annot" for n in SMALL_POS})


# Each half scaled by 0.8 and the right half moved left, so only the two bridges get
# shorter. Squashing the whole drawing by 0.52 left the lone node's edge 14bp long.
CUT_COL = {n: ((30 + (x - 46) * 0.8) if n in SMALL_LEFT else (507 - (960 - x) * 0.8), y)
           for n, (x, y) in SMALL_POS.items()}


@fig("cut-def-col", container="col", h=380)
def _cut_def_col():
    """Cut counts the edges that run between the two groups: two here."""
    s = _small_numbers()
    out = small(dict(CUT_COL), list(SMALL_E), what="cut-def-col",
                fill=_two_sides(SMALL_LEFT), heavy=_crossing(SMALL_LEFT), heavy_color="black")
    out += text(268, 62, f"cut = {s['cut_bal']}", color="black", anchor="north", size=FONT)
    return out


@fig("cut-works", container="col", h=380)
def _cut_works():
    """Three clear groups: the three edges between them are the smallest cut."""
    pos, e, grp = {}, [], {}
    centres = [(125, 95), (412, 95), (268, 280)]
    for gi, (cx, cy) in enumerate(centres):
        b = gi * 4
        pos.update({b: (cx - 62, cy), b + 1: (cx + 62, cy), b + 2: (cx, cy + 52),
                    b + 3: (cx, cy - 52)})
        e += [(b, b + 2), (b, b + 3), (b + 1, b + 2), (b + 1, b + 3), (b + 2, b + 3)]
        grp.update({b + i: gi for i in range(4)})
    bridges = [(1, 4), (2, 8), (6, 9)]
    e += bridges
    g = nx.Graph(e)
    parts = [{n for n in g if grp[n] == i} for i in range(3)]
    cut = sum(1 for a, b in g.edges() if grp[a] != grp[b])
    assert cut == 3 and nx.edge_connectivity(g) == 2
    # no other split into three non-empty groups cuts fewer edges
    best = min(sum(1 for a, b in g.edges() if lab[a] != lab[b])
               for lab in itertools.product(range(3), repeat=12) if len(set(lab)) == 3)
    assert best == cut, best
    assert all(nx.is_connected(g.subgraph(p)) for p in parts)
    cols = ["accent", "accenttwo", "accentthree"]
    out = small(pos, e, what="cut-works", fill={n: cols[grp[n]] for n in pos},
                heavy=bridges, heavy_color="black")
    out += text(268, 160, f"cut = {cut}", color="black", anchor="center", size=FONT)
    return out


@fig("cut-trivial", h=380)
def _cut_trivial():
    """The cheapest cut takes one person away from everyone else."""
    s = _small_numbers()
    lone = {9}
    fill = {n: (COFF if n in lone else CHI) for n in SMALL_POS}
    out = small(dict(SMALL_POS), list(SMALL_E), what="cut-trivial", fill=fill,
                heavy=_crossing(set(SMALL_POS) - lone), heavy_color="black")
    out += text(98, 62, f"cut = {s['cut_lone']}", color="black", anchor="north", size=44)
    return out


SQ = _squash(SMALL_POS, sy=0.7)


@fig("rcut-small", h=400, hmod="tight")
def _rcut():
    """Both candidate splits, each with its ratio cut: the balanced one is smaller."""
    s = _small_numbers()
    assert s["rc_bal"] < s["rc_lone"]
    out = small(dict(SQ), list(SMALL_E), what="rcut-small", fill={n: "accent" for n in SQ})
    for x, col, val in ((98, "annot", s["rc_lone"]), (550, "accenttwo", s["rc_bal"])):
        out += (f"\\draw[line width=3.6bp,draw={col},dash pattern=on 13bp off 10bp] "
                f"({x},120) -- ({x},308);\n")
        out += text(x, 318, f"{val.numerator}/{val.denominator}", color=col,
                    anchor="south", size=44)
    return out


@fig("ncut-small", h=400, hmod="tight")
def _ncut():
    """The balanced split, with each side's volume: the sum of its members' degrees."""
    s = _small_numbers()
    assert s["nc_bal"] < s["nc_lone"]
    out = small(dict(SQ), list(SMALL_E), what="ncut-small", fill=_two_sides(SMALL_LEFT),
                heavy=_crossing(SMALL_LEFT), heavy_color="black")
    out += text(216, 112, f"vol = {s['vol_l']}", color="accent", anchor="north", size=FONT)
    out += text(866, 112, f"vol = {s['vol_r']}", color="accenttwo", anchor="north", size=FONT)
    return out


# ------------------------------------------------------------------ the karate club
def _karate_simple():
    g = nx.Graph()
    g.add_nodes_from(range(34))
    g.add_edges_from(V.karate().edges())         # drop Zachary's weights: A_ij is 0 or 1
    return g


def _score(g, S, kind):
    n, m = g.number_of_nodes(), g.number_of_edges()
    c = V.cut_size(g, S)
    if kind == "cut":
        return F(c)
    if kind == "ratio":
        return F(c, len(S) * (n - len(S)))
    v = _vol(g, S)
    return F(c, v * (2 * m - v))


def _best_split(g, kind, restarts=400, seed=0):
    """Random-restart single-node local search. Returns the best score found."""
    rng = random.Random(seed)
    nodes = list(g)
    best = None
    for _ in range(restarts):
        p = rng.random()
        S = {v for v in nodes if rng.random() < p}
        if not S or len(S) == len(nodes):
            continue
        cur = _score(g, S, kind)
        moved = True
        while moved:
            moved = False
            for v in nodes:
                T = S ^ {v}
                if not T or len(T) == len(nodes):
                    continue
                t = _score(g, T, kind)
                if t < cur:
                    S, cur, moved = T, t, True
        best = cur if best is None or cur < best else best
    return best


KARATE_MIN = frozenset({11})
KARATE_RATIO = frozenset({4, 5, 6, 10, 16})
KARATE_NCUT = frozenset({0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 16, 17, 19, 21})


@lru_cache(maxsize=None)
def _karate_cuts():
    g = _karate_simple()
    hi, _ = V.factions()
    out = {}
    for kind, S in (("cut", KARATE_MIN), ("ratio", KARATE_RATIO), ("ncut", KARATE_NCUT)):
        mine = _score(g, S, kind)
        found = _best_split(g, kind)
        assert mine <= found, f"{kind}: the search found a better split ({found} < {mine})"
        out[kind] = (S, V.cut_size(g, S), mine)
    assert [out[k][1] for k in ("cut", "ratio", "ncut")] == [1, 4, 10]
    assert len(KARATE_RATIO) == 5 and len(KARATE_NCUT) == 17
    wrong = sorted(KARATE_NCUT ^ hi)
    assert wrong == [8, 9], wrong
    out["ncut_agree"] = 34 - len(wrong)
    assert out["ncut_agree"] == 32
    return out


def _karate_cut(S, rings=()):
    g = _karate_simple()
    side = S if 0 in S else frozenset(range(34)) - S          # Mr. Hi's side is blue
    fill = {n: (CHI if n in side else COFF) for n in range(34)}
    cross = [e for e in g.edges() if (e[0] in S) != (e[1] in S)]
    return karate(fill=fill, heavy=cross, heavy_color="black", rings=rings,
                  ring_color="accentthree")


@fig("karate-cut-min", h=380)
def _kmin():
    """Minimum cut on the club: one member with one friend, cut away."""
    return _karate_cut(_karate_cuts()["cut"][0])


@fig("karate-cut-ratio", h=380)
def _kratio():
    """Ratio cut on the club: five members split off."""
    return _karate_cut(_karate_cuts()["ratio"][0])


@fig("karate-cut-norm", h=380)
def _knorm():
    """Normalized cut on the club: 17 against 17; the two ringed members are swapped."""
    return _karate_cut(_karate_cuts()["ncut"][0], rings=[8, 9])


# =========================================================================== Part 3
@fig("how-dense", h=360)
def _how_dense():
    """Two cliques and two stars: all groups of a kind, and nothing alike in density."""
    pos, e = {}, []
    k4 = [0, 1, 2, 3]
    pos.update({0: (70, 245), 1: (200, 245), 2: (70, 115), 3: (200, 115)})
    e += clique_edges(k4)
    k5 = list(range(4, 9))
    pos.update(ring_positions(5, 405, 180, 100, 95, start=90, order=k5))
    e += clique_edges(k5)
    pos[9] = (675, 180)
    leaves = list(range(10, 15))
    pos.update(ring_positions(5, 675, 180, 100, 100, start=90, order=leaves))
    e += [(9, l) for l in leaves]
    pos[15] = (945, 180)
    leaves2 = list(range(16, 23))
    pos.update(ring_positions(7, 945, 180, 100, 100, start=90, order=leaves2))
    e += [(15, l) for l in leaves2]
    g = nx.Graph(e)
    dens = [round(nx.density(g.subgraph(c)), 2)
            for c in (k4, k5, [9] + leaves, [15] + leaves2)]
    assert dens == [1.0, 1.0, 0.33, 0.25], dens
    return small(pos, e, node=34, planar=False, what="how-dense",
                 fill={n: "annot" for n in pos})


def _rewired(seed_range=range(400), node=34):
    """A degree-preserving rewiring of the small club, laid out on its own.

    The club's own layout puts three people on one line, so almost every random edge
    runs through somebody's disc; the rewired network gets a spring layout of its own,
    pushed apart by `relax` until no edge crosses a stranger. Inside counts are always
    odd here (2 x inside + cut = 16 on the blue side), so the draw nearest the
    expected 7.53 is 7.
    """
    from figlib import clearance_bad
    from kfig import relax
    g = _small_graph()
    L = set(SMALL_LEFT)
    base = _squash(SMALL_POS, sx=0.505, nx0=30.0, sy=0.8)
    box = (610.0, 130.0, 1030.0, 300.0)
    for s in seed_range:
        h = g.copy()
        nx.double_edge_swap(h, nswap=30, max_tries=10_000, seed=s)
        assert dict(h.degree()) == dict(g.degree())
        inside = sum(1 for a, b in h.edges() if (a in L) == (b in L))
        if inside != 7 or not nx.is_connected(h):
            continue
        raw = nx.spring_layout(h, seed=s)
        xs = [v[0] for v in raw.values()]
        ys = [v[1] for v in raw.values()]
        pos = {n: (box[0] + (x - min(xs)) / (max(xs) - min(xs)) * (box[2] - box[0]),
                   box[1] + (y - min(ys)) / (max(ys) - min(ys)) * (box[3] - box[1]))
               for n, (x, y) in raw.items()}
        pos = relax(pos, list(h.edges()), node=node, box=box, seed=s)
        if clearance_bad(list(h.edges()), pos, r=node / 2 + 3):
            continue
        if any(math.dist(pos[a], pos[b]) < node + 8 for a, b in itertools.combinations(pos, 2)):
            continue
        return base, pos, h, inside
    raise SystemExit("no rewiring with 7 inside draws cleanly -- widen the seed range")


@fig("null-model", h=380, hmod="tight")
def _null():
    """Left: the network. Right: the same degrees, edges wired at random."""
    s = _small_numbers()
    base, right, h, inside = _rewired()
    fill = _two_sides(SMALL_LEFT)
    out = small(base, list(SMALL_E), node=34, what="null-left", fill=fill)
    out += small(right, list(h.edges()), node=34, planar=False, what="null-right", fill=fill)
    out += text(261, 95, f"{s['inside']} inside", color="black", anchor="north", size=FONT)
    out += text(821, 95, f"{inside} inside", color="black", anchor="north", size=FONT)
    return out


@fig("louvain-steps", h=330, hmod="tight")
def _louvain():
    """Step 1 groups the nodes; step 2 turns each group into one node."""
    pos, e, grp = {}, [], {}
    cy = 190
    for gi, cx in enumerate((105, 300, 495)):
        b = gi * 4
        pos.update({b: (cx - 62, cy), b + 1: (cx + 62, cy), b + 2: (cx, cy + 55),
                    b + 3: (cx, cy - 55)})
        e += [(b, b + 2), (b, b + 3), (b + 1, b + 2), (b + 1, b + 3), (b + 2, b + 3)]
        grp.update({b + i: gi for i in range(4)})
    e += [(1, 4), (5, 8)]
    g = nx.Graph(e)
    parts = [{n for n in g if grp[n] == i} for i in range(3)]
    q3 = V.unweighted_Q(g, parts)
    # the three groups are a local maximum: no single node move raises Q
    for v in g:
        for tgt in range(3):
            if tgt == grp[v]:
                continue
            alt = [set(p) for p in parts]
            alt[grp[v]].discard(v)
            alt[tgt].add(v)
            assert V.unweighted_Q(g, [p for p in alt if p]) <= q3 + 1e-12
    cols = ["accent", "accenttwo", "accentthree"]
    out = small(pos, e, node=34, what="louvain-steps", fill={n: cols[grp[n]] for n in pos})
    out += arrow((604, cy), (690, cy), color="annot", w=3.4, head=14)
    sup = {i: (770 + 130 * i, cy) for i in range(3)}
    out += small(sup, [(0, 1), (1, 2)], node=50, what="louvain-super",
                 fill={i: cols[i] for i in sup})
    labels = [(300, 100, "1. move nodes"), (900, 100, "2. merge groups")]
    assert_boxes_clear([label_box(x, y, s, "north") for x, y, s in labels], "louvain-steps")
    for x, y, s in labels:
        out += text(x, y, s, color="black", anchor="north", size=FONT)
    return out


LEIDEN_POS = {0: (60, 290), 1: (60, 120), 2: (210, 205), 3: (420, 290), 4: (420, 120),
              5: (620, 205), 6: (830, 290), 7: (830, 120), 8: (990, 205)}
LEIDEN_E = [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5),
            (5, 6), (5, 7), (6, 7), (6, 8), (7, 8)]


@fig("leiden-two", h=380, hmod="tight")
def _leiden():
    """The same network twice: Louvain's group in two pieces, and Leiden's repair."""
    g = nx.Graph(LEIDEN_E)
    red = {0, 1, 2, 6, 7, 8}
    assert not nx.is_connected(g.subgraph(red)), "Louvain's group must be in two pieces"
    fixed = [{0, 1, 2}, {6, 7, 8}, {3, 4, 5}]
    assert all(nx.is_connected(g.subgraph(p)) for p in fixed)
    assert V.unweighted_Q(g, fixed) > V.unweighted_Q(g, [red, {3, 4, 5}])
    left = _squash(LEIDEN_POS, sx=0.48, x0=60.0, nx0=35.0, sy=0.8, cy=205.0)
    right = {n: (x + 565, y) for n, (x, y) in left.items()}
    out = small(left, LEIDEN_E, node=34, what="leiden-left",
                fill={n: ("accenttwo" if n in red else "annot") for n in left})
    col2 = {0: "accenttwo", 1: "accenttwo", 2: "accenttwo",
            6: "accentthree", 7: "accentthree", 8: "accentthree"}
    out += small(right, LEIDEN_E, node=34, what="leiden-right",
                 fill={n: col2.get(n, "annot") for n in right})
    out += text(258, 95, "Louvain", color="black", anchor="north", size=FONT)
    out += text(823, 95, "Leiden", color="black", anchor="north", size=FONT)
    return out


# ------------------------------------------------------------------ resolution limit
def _ring_of_triangles(n, x0, x1, y_top=250, y_bot=130, apex=58, base=60.0):
    """n triangles joined in a ring, drawn as a racetrack: half on top pointing up, half
    below pointing down, and one vertical bridge at each end.

    Returns (pos, edges, triangles in ring order). A ring drawn on an ellipse squeezes
    the triangles at the two ends onto a tight curve; two straight rows do not.
    """
    assert n % 2 == 0
    per = n // 2
    gap = (x1 - x0 - per * base) / (per - 1) if per > 1 else 0.0
    pos, tris, e = {}, [], []
    k = 0
    for row, (y, sgn) in enumerate(((y_top, 1), (y_bot, -1))):
        slots = range(per) if row == 0 else reversed(range(per))
        for j in slots:
            xa = x0 + j * (base + gap)
            a, b, c = k, k + 1, k + 2
            k += 3
            left, right = (xa, y), (xa + base, y)
            if row == 0:
                pos[a], pos[b] = left, right
            else:
                pos[a], pos[b] = right, left
            pos[c] = (xa + base / 2, y + sgn * apex)
            e += [(a, b), (a, c), (b, c)]
            tris.append((a, b, c))
    for t in range(n):
        e.append((tris[t][1], tris[(t + 1) % n][0]))     # the bridge to the next triangle
    return pos, e, tris


def _ring_Q(n):
    pos, e, tris = _ring_of_triangles(n, 0, 1000)
    g = nx.Graph(e)
    assert g.number_of_edges() == 4 * n and nx.is_connected(g)
    apart = V.unweighted_Q(g, [set(t) for t in tris])
    pairs = V.unweighted_Q(g, [set(tris[i]) | set(tris[i + 1]) for i in range(0, n, 2)])
    assert abs(apart - (0.75 - 1 / n)) < 1e-12 and abs(pairs - (0.875 - 2 / n)) < 1e-12
    return apart, pairs


def _band(pts, width=50):
    return ("\\draw[line width=%dbp,draw=accentthree,opacity=0.45,line cap=round,"
            "line join=round] %s;\n" % (width, " -- ".join("(%.1f,%.1f)" % p for p in pts)))


@fig("ring-ten", h=380)
def _ring_ten():
    """Ten triangles in a ring. Which grouping gives the highest Q?"""
    pos, e, tris = _ring_of_triangles(10, 110, 970, y_top=262, y_bot=118, apex=72,
                                      base=90.0)
    out = small(pos, e, node=30, what="ring-ten", fill={n: "annot" for n in pos})
    out += text(540, 190, "10 triangles", color="black", anchor="center", size=FONT)
    return out


@fig("ring-four-ten", h=380)
def _ring_four_ten():
    """Four triangles: Q keeps them apart. Ten: Q merges neighbours in pairs."""
    a4, p4 = _ring_Q(4)
    a10, p10 = _ring_Q(10)
    assert a4 > p4 and p10 > a10, "4 must stay apart and 10 must merge"
    assert (round(a4, 3), round(p4, 3), round(a10, 3), round(p10, 3)) == \
        (0.5, 0.375, 0.65, 0.675)
    a8, p8 = _ring_Q(8)
    assert abs(a8 - p8) < 1e-12, "at eight triangles the two groupings tie"
    out = ""
    p_l, e_l, t_l = _ring_of_triangles(4, 70, 330)
    p_r, e_r, t_r = _ring_of_triangles(10, 470, 1040)
    for t in t_l:                                        # four groups, one per triangle
        out += _band([p_l[t[2]], p_l[t[0]], p_l[t[1]], p_l[t[2]]])
    for i in range(0, 10, 2):                            # five groups, one per pair
        a, b = t_r[i], t_r[i + 1]
        out += _band([p_r[a[2]], p_r[a[0]], p_r[a[1]], p_r[a[2]], p_r[a[1]],
                      p_r[b[0]], p_r[b[2]], p_r[b[1]], p_r[b[0]]])
    out += small(p_l, e_l, node=30, what="ring-four", fill={n: "accent" for n in p_l})
    out += small(p_r, e_r, node=30, what="ring-ten-merged", fill={n: "accent" for n in p_r})
    out += text(200, 190, "4", color="black", anchor="center", size=44)
    out += text(755, 190, "10", color="black", anchor="center", size=44)
    return out


# ------------------------------------------------------------------ near-equal Q
# Two splits of the club found by single-node local search on unweighted modularity.
# Both are local maxima (asserted below); the best known split scores 0.4198.
Q_FOUR = [[0, 1, 2, 3, 7, 11, 12, 13, 17, 19, 21], [4, 5, 6, 10, 16],
          [8, 9, 14, 15, 18, 20, 22, 30, 32, 33], [23, 24, 25, 26, 27, 28, 29, 31]]
Q_THREE = [[0, 1, 2, 3, 7, 9, 11, 12, 13, 17, 19, 21], [4, 5, 6, 10, 16],
           [8, 14, 15, 18, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]]
Q_COLS = ["accent", "accentthree", "accenttwo", "annot"]


def _assert_local_max(g, parts):
    q = V.unweighted_Q(g, parts)
    lab = {v: i for i, p in enumerate(parts) for v in p}
    for v in g:
        for tgt in range(len(parts) + 1):                # + a new group of one
            if tgt == lab[v]:
                continue
            alt = [set(p) for p in parts] + [set()]
            alt[lab[v]].discard(v)
            alt[tgt].add(v)
            assert V.unweighted_Q(g, [p for p in alt if p]) <= q + 1e-12, \
                f"moving {v} raises Q -- not a local maximum"
    return q


@lru_cache(maxsize=None)
def _near_equal():
    g = _karate_simple()
    q4, q3 = _assert_local_max(g, Q_FOUR), _assert_local_max(g, Q_THREE)
    assert (f"{q4:.3f}", f"{q3:.3f}") == ("0.407", "0.402"), (q4, q3)
    a = V.labels(Q_FOUR, 34)
    b = V.labels(Q_THREE, 34)
    assert V.ari(a, b) < 0.65
    return q4, q3


@fig("karate-q-four", h=380)
def _kq4():
    _near_equal()
    return karate(fill={n: Q_COLS[i] for i, p in enumerate(Q_FOUR) for n in p})


@fig("karate-q-three", h=380)
def _kq3():
    _near_equal()
    return karate(fill={n: Q_COLS[i] for i, p in enumerate(Q_THREE) for n in p})


if __name__ == "__main__":
    print(_small_numbers())
    print({k: v for k, v in _karate_cuts().items()})
    print(_ring_Q(4), _ring_Q(8), _ring_Q(10))
    print(_near_equal())

#!/usr/bin/env python3
"""The purpose-built small graphs: the club, the sigma demo, the broker, the star,
the path, the localized clique, and the two "what is degree / what is betweenness"
pictures.

These are the figures that carry a definition rather than a result, so each one is
one drawing of one idea:

    club-blank / club-network      the room's own network, before and with its edges
    club-king-1/-2/-3              one geometry, three questions, three different kings
    club-three-kings (col)         the same three students where the map does not fit
    degree-count                   degree counts edge ends at a node
    betweenness-idea               every left-right route crosses one node
    sigma-blank / -graph / -answer counting shortest routes, and sharing the credit
    broker                         two cliques, one two-link node, all the flow
    star-closeness (col)           the only graph where closeness is exactly 1
    star-vs-path-1 / -2            every metric agrees; no metric agrees
    same-degree-different-friends  equal degree, unequal neighbours
    localization                   the eigenvector collapses onto the dense core

Every number printed here is imported from `verify_numbers`; none is typed.  The
club layout is not hand-placed either -- a straight-line drawing of the club network
that is planar, keeps every disc clear of every edge AND leaves the label solver a
legal assignment for all thirteen names at the 36 pt floor was found by search, and
the result is frozen in CLUB_XY with the three gates re-run at import.
"""

import itertools
import math
import re
from decimal import ROUND_HALF_UP, Decimal

import networkx as nx

import figlib as F
import romelib as R
from figlib import ACCENT, ACCENT2, ACCENT3, GRAY

# figlib's palette constants are hex strings; TikZ needs the names the preamble
# defines with \definecolor, and `fill=B14434` is an undefined-colour error rather
# than a red disc. One mapping, so a colour cannot be spelled two ways.
TIKZ = {ACCENT: "accent", ACCENT2: "accenttwo", ACCENT3: "accentthree", GRAY: "annot"}
BLUE, RED, GOLD, DIM = (TIKZ[ACCENT], TIKZ[ACCENT2], TIKZ[ACCENT3], TIKZ[GRAY])
from verify_numbers import (BROKER, BROKER_C, BROKER_PAIRS, CLUB, CLUB_BROKER,
                            CLUB_CLOSE, CLUB_SPREAD, LOCAL, LOCAL_C, LOCAL_CORE,
                            LOCAL_TAIL, LOCAL_TAIL_FRACTION, METRICS, PATH,
                            PATH_CROWNS, SIG_SD, SIG_SD_THROUGH, SIGMA, SIGMA_BT,
                            SIGMA_EDGES, SIGMA_POS, STAR, STAR_C, STAR_CROWNS, crown)

# --------------------------------------------------------------------------- ink log
# `sigma-blank` and every other Your-turn figure claims to print no digits, and the
# only honest way to check that is to record what was actually drawn. m03 shipped a
# "blank" worksheet with the answer still printed in one corner.
_DRAWN = []


def T(x, y, s, **kw):
    _DRAWN.append(s)
    return F.text(x, y, s, **kw)


def start_log():
    _DRAWN.clear()


_NODE_TEXT = re.compile(r"\\node\[[^\]]*\](?:\s*\([^)]*\))?\s*at\s*\([^)]*\)\s*\{(.*?)\};")


def assert_no_digits(name, body):
    """Two independent checks, because one of them can be bypassed.

    The log only sees strings that went through T() or discs_ink(); the regex reads
    the TikZ that will actually be compiled, so a digit drawn by any other route
    still fails the build.
    """
    bad = [s for s in _DRAWN if re.search(r"[0-9]", s)]
    bad += [s for s in _NODE_TEXT.findall(body) if re.search(r"[0-9]", s)]
    assert not bad, f"{name}: draws a digit -- {bad}"


def dec(x, places):
    """Round half UP in decimal: a float 0.575 is 57.49999999999999 and prints 57."""
    return str(Decimal(repr(float(x))).quantize(Decimal("1." + "0" * places),
                                                rounding=ROUND_HALF_UP))


# --------------------------------------------------------------------------- shared ink
def crown_mark(x, y, color=RED):
    """The deck's crown: accent-2 ring plus glyph, identical to the Roman map's.

    Imported from romelib rather than redrawn so that the crown a student learns on
    slide 12 is the same shape as the crown on slide 41; two crowns drawn twice is
    how m01 ended up with two different rings meaning the same thing.
    """
    return (F.mark(x, y, color=color, size=F.NODE)
            + R._crown_glyph(x, y + F.NODE / 2 + 22, color))


CROWN_BOX_H = 34          # the glyph's footprint above a disc, for the label solver


def crown_blocker(x, y):
    return (x - 22, y + F.NODE / 2 - 2, x + 22, y + F.NODE / 2 + CROWN_BOX_H)


def edges_ink(edges, pos, color="black", w=F.EDGE_W):
    return "".join(F.seg(pos[a], pos[b], color=color, w=w) for a, b in edges)


def discs_ink(pos, fill="accent", size=F.NODE, labels=None):
    out = ""
    for n, p in pos.items():
        lab = "" if labels is None else str(labels.get(n, ""))
        if lab:
            _DRAWN.append(lab)
        out += F.disc(p[0], p[1], lab, fill=fill, size=size)
    return out


def route_ink(routes, pos, colors, gap=14.0, w=4.6):
    """Draw shortest paths so that a shared edge shows one strand per route.

    Offsetting a whole path instead draws a ghost line beside every edge it uses
    alone, and the figure reads as if the graph had doubled edges. Here the offset
    is per edge: an edge one route uses sits ON the edge, an edge two routes share
    splits into two strands, and the bundle at the node they all cross is the count
    the figure is claiming.
    """
    users = {}
    for i, r in enumerate(routes):
        for e in zip(r, r[1:]):
            users.setdefault(tuple(sorted(e)), []).append(i)
    out = ""
    for i, r in enumerate(routes):
        for u, v in zip(r, r[1:]):
            who = users[tuple(sorted((u, v)))]
            off = (who.index(i) - (len(who) - 1) / 2) * gap
            p, q = pos[u], pos[v]
            dx, dy = q[0] - p[0], q[1] - p[1]
            L = (dx * dx + dy * dy) ** 0.5 or 1.0
            nx_, ny_ = -dy / L * off, dx / L * off
            out += F.seg((p[0] + nx_, p[1] + ny_), (q[0] + nx_, q[1] + ny_),
                         color=colors[i], w=w)
    return out


# =============================================================================
# The club network -- one geometry, used by four figures
# =============================================================================
CLUB_EDGES = sorted(tuple(sorted(e)) for e in CLUB.edges)
CLUB_XY = {
    "Sarah": (160, 260),
    "Mike": (130, 60),
    "Emma": (240, 200),
    "Alex": (450, 200),
    "Olivia": (360, 60),
    "James": (480, 70),
    "Sophia": (580, 240),
    "Ethan": (720, 55),
    "Ava": (720, 140),
    "Noah": (900, 260),
    "Lily": (1000, 240),
    "Lucas": (1000, 120),
    "Henry": (810, 85),
}
CLUB_BAND = (4.0, 4.0, 1076.0, 352.0)
CLUB_MIN_SEP = 84            # bp between disc centres: 44 bp of white at NODE = 40

assert set(CLUB_XY) == set(CLUB), sorted(set(CLUB_XY) ^ set(CLUB))
assert nx.check_planarity(CLUB)[0], "the club network must be drawable without a crossing"
# ...and the drawing above must actually realise that, which is a separate fact:
# `check_planarity` says a crossing-free drawing exists, not that this one is it.
F.assert_planar_drawing(CLUB_EDGES, CLUB_XY, "club network")
assert not F.crossings(CLUB_EDGES, CLUB_XY)
_sep = min(math.dist(p, q) for p, q in itertools.combinations(CLUB_XY.values(), 2))
assert _sep >= CLUB_MIN_SEP, f"two students are only {_sep:.0f} bp apart"

# The crown is drawn ON the layout, so it is part of the layout problem: solving the
# names first and adding the glyph afterwards drew the crown straight through the
# word "Noah". Same for the note -- a corner is reserved before the names are placed
# rather than hunted for afterwards, which is why all three king figures can carry
# the note in the same spot.
CLUB_NOTE_RECT = (4.0, 294.0, 266.0, 352.0)
CLUB_NOTE_AT = (14.0, 322.0)
CLUB_NOTE_ANCHOR = "west"

CLUB_SIDES, CLUB_BOXES = F.place_labels(
    {c: c for c in CLUB_XY}, CLUB_XY, CLUB_EDGES,
    blockers=[crown_blocker(*CLUB_XY[k]) for k in (CLUB_SPREAD[0], CLUB_CLOSE[0],
                                                   CLUB_BROKER[0])] + [CLUB_NOTE_RECT],
    bounds=CLUB_BAND, gap=3.0)


def _unambiguous(xy, boxes, margin=22.0):
    """Every name must be nearest to its own disc, by a clear margin.

    `place_labels` only asks that a label collide with nothing, which in a graph
    whose discs are 100 bp apart is not the same as the label belonging to the right
    one: an earlier layout put "Ava" beside Ethan's disc and "James" beside Alex's
    triangle, both collision-free and both wrong.
    """
    bad = []
    for n, b in boxes.items():
        c = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
        d0 = math.dist(c, xy[n])
        near = [m for m, p in xy.items() if m != n and math.dist(c, p) < d0 + margin]
        if near:
            bad.append((n, near))
    return bad


_amb = _unambiguous(CLUB_XY, CLUB_BOXES)
assert not _amb, f"a club name sits nearer another student's disc: {_amb}"


def club_labels(color="black"):
    return F.draw_labels({c: c for c in CLUB_XY}, CLUB_XY, CLUB_SIDES, color=color)


def club_note(words):
    """The question this figure's crown answers, asserted inside the reserved corner."""
    b = F.label_box(*CLUB_NOTE_AT, words, CLUB_NOTE_ANCHOR)
    r = CLUB_NOTE_RECT
    assert r[0] <= b[0] and b[2] <= r[2] and r[1] <= b[1] and b[3] <= r[3], \
        (f"the note {words!r} does not fit the corner reserved for it -- shorten it "
         f"(notes carry the question; prose goes in the figcaption)")
    return T(*CLUB_NOTE_AT, words, color=RED, anchor=CLUB_NOTE_ANCHOR)


def fig_club_blank():
    """Thirteen students, no edges -- the room draws the edges itself.

    The edges are absent from the picture and present in the gate: the layout is the
    one `club-network` and the three king figures use, so it has to be crossing-free
    here even though nothing is drawn to cross.
    """
    start_log()
    assert nx.check_planarity(CLUB)[0]
    assert not F.crossings(CLUB_EDGES, CLUB_XY), \
        "the layout this figure freezes must draw the club's 17 edges without a crossing"
    body = discs_ink(CLUB_XY) + club_labels()
    F.emit("club-blank", body, container="full", h=380)


def fig_club_network():
    start_log()
    F.assert_planar_drawing(CLUB_EDGES, CLUB_XY, "club-network")
    assert len(CLUB_EDGES) == CLUB.number_of_edges() == 17
    body = edges_ink(CLUB_EDGES, CLUB_XY) + discs_ink(CLUB_XY) + club_labels()
    F.emit("club-network", body, container="full", h=380)


# The three questions Part 1 asks, and the student each one crowns. The names come
# from verify_numbers, so a change in the roster moves the crowns here too.
CLUB_KINGS = [("club-king-1", CLUB_SPREAD[0], "tell first"),
              ("club-king-2", CLUB_CLOSE[0], "closest"),
              ("club-king-3", CLUB_BROKER[0], "coordinates")]
assert [k for _, k, _ in CLUB_KINGS] == ["Noah", "Sophia", "Alex"]
assert len({k for _, k, _ in CLUB_KINGS}) == 3, "three questions, three students"

_KING_BASE = {}


def _king_body(king, words):
    """The identical drawing every time, plus this king's crown and note."""
    base = edges_ink(CLUB_EDGES, CLUB_XY) + discs_ink(CLUB_XY) + club_labels()
    _KING_BASE.setdefault("base", base)
    assert base == _KING_BASE["base"], \
        "the three king figures must be the same picture -- only the crown may differ"
    return base + crown_mark(*CLUB_XY[king]) + club_note(words)


def _make_king(name, king, words):
    def fn():
        start_log()
        body = _king_body(king, words)
        F.emit(name, body, container="full", h=380)
    return fn


# --- the column-width version: just the three students and their friend counts ----
KING_ROWS = [(CLUB_SPREAD[0], "tell first"),
             (CLUB_CLOSE[0], "closest"),
             (CLUB_BROKER[0], "coordinates")]


def fig_club_three_kings():
    start_log()
    deg = dict(CLUB.degree())
    # The figure's whole claim is that the three answers differ and that the last two
    # kings hold FEWER friends than the first -- checked, not drawn and hoped for.
    assert deg[CLUB_SPREAD[0]] == max(deg.values())
    assert deg[CLUB_CLOSE[0]] < deg[CLUB_SPREAD[0]]
    assert deg[CLUB_BROKER[0]] < deg[CLUB_SPREAD[0]]
    b = ""
    for i, (name, role) in enumerate(KING_ROWS):
        y = 300 - 90 * i
        b += F.disc(58, y, str(deg[name]), fill="accenttwo", size=52)
        _DRAWN.append(str(deg[name]))
        b += T(96, y, name, anchor="west")
        b += T(288, y, role, color=DIM, anchor="west")
    b += T(20, 42, "in the disc: how many friends", color=DIM, anchor="west")
    F.emit("club-three-kings", b, container="col", h=390)


# =============================================================================
# degree -- what the number counts
# =============================================================================
def fig_degree_count():
    """One node, five edge ends, each end ticked. Degree counts ends, not neighbours."""
    start_log()
    # The direction of each spoke is chosen in DRAWING space, with its own length,
    # rather than by putting five nodes on an ellipse: an ellipse wide enough for the
    # ink-span gate squashes 60 deg of angle down to 28, and the two left-hand ticks
    # rendered as one bracket. Here no two spokes leave the hub less than 60 deg
    # apart, so the five ticks are five ticks.
    cx, cy = 560, 175
    spokes = [(0, 460), (60, 150), (120, 150), (180, 460), (270, 130)]
    assert min((b[0] - a[0]) % 360 for a, b in zip(spokes, spokes[1:] + spokes[:1])) >= 60
    pos = {"c": (cx, cy)}
    for i, (deg, L) in enumerate(spokes):
        a = math.radians(deg)
        pos[f"n{i}"] = (cx + L * math.cos(a), cy + L * math.sin(a))
    edges = [("c", f"n{i}") for i in range(5)]
    F.assert_planar_drawing(edges, pos, "degree-count")
    k = len(edges)
    assert k == len({e[1] for e in edges}) == 5

    b = edges_ink(edges, pos)
    for _, n in edges:
        px, py = pos[n]
        dx, dy = px - cx, py - cy
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        mx, my = cx + ux * (52 / 2 + 22), cy + uy * (52 / 2 + 22)
        b += F.seg((mx - uy * 15, my + ux * 15), (mx + uy * 15, my - ux * 15),
                   color=RED, w=5.5)
    b += discs_ink({n: p for n, p in pos.items() if n != "c"})
    b += F.disc(cx, cy, "", fill="accent", size=52)
    b += T(cx, 350, f"{k} edge ends, so degree {k}", color=RED)
    F.emit("degree-count", b, container="full", h=410)


# =============================================================================
# betweenness -- the idea, before the formula
# =============================================================================
BI_POS = {"l1": (140, 280), "l2": (300, 175), "l3": (140, 70),
          "M": (540, 175),
          "r2": (780, 175), "r1": (940, 280), "r3": (940, 70)}
BI_EDGES = [("l1", "l2"), ("l2", "l3"), ("l1", "l3"), ("l2", "M"),
            ("M", "r2"), ("r1", "r2"), ("r2", "r3"), ("r1", "r3")]
BI = nx.Graph(BI_EDGES)
BI_LEFT, BI_RIGHT = ["l1", "l2", "l3"], ["r1", "r2", "r3"]
# The claim the figure makes, checked over every pair rather than the three drawn.
BI_PAIRS = [(a, b) for a in BI_LEFT for b in BI_RIGHT]
assert all(all("M" in p for p in nx.all_shortest_paths(BI, a, b)) for a, b in BI_PAIRS), \
    "every left-right shortest path must use M, or the figure's note is false"
assert BI.degree("M") == 2
BI_SHOWN = [["l1", "l2", "M", "r2", "r1"],
            ["l3", "l2", "M", "r2", "r3"],
            ["l1", "l2", "M", "r2", "r3"]]


def fig_betweenness_idea():
    start_log()
    F.assert_planar_drawing(BI_EDGES, BI_POS, "betweenness-idea")
    for p in BI_SHOWN:
        assert p in list(nx.all_shortest_paths(BI, p[0], p[-1])), \
            f"the drawn route {p} is not a shortest path"
    b = edges_ink(BI_EDGES, BI_POS, color=DIM, w=F.EDGE_W)
    b += route_ink(BI_SHOWN, BI_POS, [RED] * len(BI_SHOWN))
    b += discs_ink({n: p for n, p in BI_POS.items() if n != "M"})
    b += F.disc(*BI_POS["M"], "M", fill="accenttwo", size=52)
    _DRAWN.append("M")
    # The drawing shows three of the nine; the note says so rather than letting the
    # count of strands stand in for the count of pairs.
    b += T(540, 330, f"{len(BI_SHOWN)} of the {len(BI_PAIRS)} left-right routes; "
                     f"all of them cross M", color=RED)
    F.emit("betweenness-idea", b, container="full", h=390)


# =============================================================================
# the sigma demo -- counting shortest routes, and sharing the credit
# =============================================================================
SIG_XY = {n: (130 + 200 * p[0], 60 + 105 * p[1]) for n, p in SIGMA_POS.items()}
SIG_E = [tuple(e) for e in SIGMA_EDGES]
F.assert_planar_drawing(SIG_E, SIG_XY, "sigma demo")
assert sorted(map(tuple, map(sorted, SIG_E))) == sorted(map(tuple, map(sorted, SIGMA.edges)))


def _sigma_base():
    b = edges_ink(SIG_E, SIG_XY)
    for n in ("S", "D"):
        b += F.mark(*SIG_XY[n], color=RED)
    b += discs_ink(SIG_XY, labels={n: n for n in SIG_XY})
    return b


def fig_sigma_graph():
    start_log()
    b = _sigma_base()
    b += T(550, 330, f"S to D: {SIG_SD} shortest routes", color=RED)
    assert SIG_SD == 2
    F.emit("sigma-graph", b, container="full", h=390)


def fig_sigma_blank():
    start_log()
    b = _sigma_base()
    b += T(550, 330, "S to D: how many shortest routes?", color=RED)
    assert_no_digits("sigma-blank", b)
    F.emit("sigma-blank", b, container="full", h=390)


SIG_ROUTES = [["S", "A", "T", "D"], ["S", "B", "T", "D"]]


def fig_sigma_answer():
    start_log()
    for p in SIG_ROUTES:
        assert p in list(nx.all_shortest_paths(SIGMA, "S", "D"))
    assert len(list(nx.all_shortest_paths(SIGMA, "S", "D"))) == SIG_SD == 2
    # the share of the S-D pair each node carries, computed, never typed
    share = {n: SIG_SD_THROUGH[n] / SIG_SD for n in ("A", "B", "T")}
    assert share == {"A": 0.5, "B": 0.5, "T": 1.0}, share
    assert SIGMA_BT["A"] == SIGMA_BT["B"] and SIGMA_BT["T"] == max(SIGMA_BT.values())
    words = {n: ("1/2" if share[n] == 0.5 else "1") for n in share}
    assert words == {"A": "1/2", "B": "1/2", "T": "1"}

    b = edges_ink(SIG_E, SIG_XY, color=DIM)
    b += route_ink(SIG_ROUTES, SIG_XY, [BLUE, RED])
    b += discs_ink(SIG_XY, labels={n: n for n in SIG_XY})
    sides, boxes = F.place_labels(words, SIG_XY, SIG_E, bounds=(4, 4, 1076, 300), gap=3.0)
    amb = _unambiguous(SIG_XY, boxes)
    assert not amb, f"a share is printed nearer another node: {amb}"
    _DRAWN.extend(words.values())
    b += F.draw_labels(words, SIG_XY, sides, color=RED)
    b += F.note("each route earns 1, split where they tie", (550, 330),
                color=DIM, anchor="center", boxes=boxes)
    F.emit("sigma-answer", b, container="full", h=390)


# =============================================================================
# the broker -- two cliques, one two-link node
# =============================================================================
BR_XY = {"L1": (400, 175), "L2": (260, 275), "L3": (120, 175), "L4": (260, 75),
         "M": (540, 175),
         "R1": (680, 175), "R2": (820, 275), "R3": (960, 175), "R4": (820, 75)}
BR_ALL = [tuple(sorted(e)) for e in BROKER.edges]
# A 4-clique cannot be drawn without a crossing unless one vertex sits inside the
# triangle of the other three, and here both cliques hang off a bridge, so the two
# diagonals of each diamond must cross. That is the ONLY crossing the figure allows:
# the outer edges plus the bridge are checked for planarity, and the total crossing
# count is asserted to be exactly the two unavoidable ones.
BR_OUTER = [("L1", "L2"), ("L2", "L3"), ("L3", "L4"), ("L4", "L1"),
            ("R1", "R2"), ("R2", "R3"), ("R3", "R4"), ("R4", "R1"),
            ("L1", "M"), ("M", "R1")]
BR_DIAG = [("L1", "L3"), ("L2", "L4"), ("R1", "R3"), ("R2", "R4")]
assert sorted(tuple(sorted(e)) for e in BR_OUTER + BR_DIAG) == sorted(BR_ALL)


def fig_broker():
    start_log()
    F.assert_planar_drawing(BR_OUTER, BR_XY, "broker (outer edges)")
    assert not F.clearance_bad(BR_ALL, BR_XY), "an edge crosses a disc it does not end at"
    x = F.crossings(BR_ALL, BR_XY)
    assert len(x) == 2, f"only the two K4 diagonals may cross -- got {len(x)}: {x}"
    assert all(set(a) <= {"L1", "L2", "L3", "L4"} or set(a) <= {"R1", "R2", "R3", "R4"}
               for pair in x for a in pair), x
    assert crown(BROKER_C["betweenness"]) == ["M"]
    assert BROKER.degree("M") == 2
    assert "M" not in crown(BROKER_C["degree"])

    b = edges_ink(BR_ALL, BR_XY)
    b += discs_ink({n: p for n, p in BR_XY.items() if n != "M"})
    b += F.disc(*BR_XY["M"], "M", fill="accenttwo", size=52)
    _DRAWN.append("M")
    b += crown_mark(*BR_XY["M"])
    b += T(540, 335, f"{BROKER_PAIRS} pairs must cross M", color=RED)
    b += T(540, 30, f"and M holds only {BROKER.degree('M')} links", color=DIM)
    F.emit("broker", b, container="full", h=400)


# =============================================================================
# the star and the path
# =============================================================================
def _star_xy(cx, cy, rx, ry, n=6):
    """Hub plus n leaves on a wide ellipse.

    A circle wide enough for the ink-span gate is too tall for the height cap
    (FIGURE_GUIDE, "square figures cannot pass both gates"), and starting at 0 deg
    puts a leaf at each horizontal extreme, which is where the width comes from.
    """
    xy = {0: (cx, cy)}
    for i in range(n):
        a = math.radians(360 * i / n)
        xy[i + 1] = (cx + rx * math.cos(a), cy + ry * math.sin(a))
    return xy


STAR_E = [tuple(e) for e in STAR.edges]
assert len(STAR) == 7 and len(STAR_E) == 6


def fig_star_closeness():
    start_log()
    xy = _star_xy(268, 175, 200, 115)
    F.assert_planar_drawing(STAR_E, xy, "star-closeness")
    c = STAR_C["closeness"][0]
    assert c == 1.0, c
    assert crown(STAR_C["closeness"]) == [0]
    shown = dec(c, 1)
    assert shown == "1.0", shown
    b = edges_ink(STAR_E, xy)
    b += F.mark(*xy[0], color=RED)
    b += discs_ink(xy)
    b += T(268, 332, f"hub closeness = {shown}", color=RED)
    F.emit("star-closeness", b, container="col", h=390)


def fig_star_vs_path_1():
    start_log()
    xy = _star_xy(540, 175, 400, 125)
    F.assert_planar_drawing(STAR_E, xy, "star-vs-path-1")
    n = len(METRICS)
    assert all(STAR_CROWNS[m] == [0] for m in METRICS), STAR_CROWNS
    assert len(STAR_CROWNS) == n == 7
    b = edges_ink(STAR_E, xy) + discs_ink(xy) + crown_mark(*xy[0])
    b += T(540, 335, f"all {n} metrics crown the hub", color=RED)
    F.emit("star-vs-path-1", b, container="full", h=400)


PATH_XY = {i: (120 + 140 * i, 175) for i in range(7)}
PATH_E = [tuple(e) for e in PATH.edges]


def fig_star_vs_path_2():
    start_log()
    F.assert_planar_drawing(PATH_E, PATH_XY, "star-vs-path-2")
    deg_k, bet_k = PATH_CROWNS["degree"], PATH_CROWNS["betweenness"]
    assert deg_k == [1, 2, 3, 4, 5] and bet_k == [3], (deg_k, bet_k)
    assert len(deg_k) == 5 and len(bet_k) == 1
    b = edges_ink(PATH_E, PATH_XY)
    for i in deg_k:                       # accent-3 is a ring here, never a label
        b += F.mark(*PATH_XY[i], color=GOLD, w=6.0)
    b += discs_ink(PATH_XY, labels={i: str(i) for i in PATH_XY})
    for i in bet_k:
        b += crown_mark(*PATH_XY[i])
    b += T(540, 292, f"crown = most routes ({len(bet_k)} node)", color=RED)
    b += T(540, 72, f"ring = most friends ({len(deg_k)} nodes)", color=DIM)
    F.emit("star-vs-path-2", b, container="full", h=400)


# =============================================================================
# equal degree, unequal neighbours
# =============================================================================
# Built here rather than imported: the point is a contrast the deck's other graphs
# do not contain. U and its three friends form a 4-clique; V's three friends are
# leaves. Both focal nodes hold exactly three edges.
SD_EDGES = [("U", "a"), ("U", "b"), ("U", "c"), ("a", "b"), ("a", "c"), ("b", "c"),
            ("V", "x"), ("V", "y"), ("V", "z")]
SD = nx.Graph(SD_EDGES)
SD_XY = {"U": (100, 175), "a": (240, 270), "b": (240, 80), "c": (185, 175),
         "V": (350, 175), "x": (490, 260), "y": (490, 175), "z": (490, 90)}
assert SD.degree("U") == SD.degree("V") == 3, "the two focal degrees must be equal"
assert min(SD.degree(n) for n in SD["U"]) == 3
assert max(SD.degree(n) for n in SD["V"]) == 1, "V's friends must be leaves"


def fig_same_degree_different_friends():
    start_log()
    F.assert_planar_drawing(SD_EDGES, SD_XY, "same-degree-different-friends")
    k = SD.degree("U")
    b = edges_ink(SD_EDGES, SD_XY)
    b += discs_ink({n: p for n, p in SD_XY.items() if n not in ("U", "V")})
    for n in ("U", "V"):
        b += F.disc(*SD_XY[n], str(k), fill="accenttwo", size=52)
        _DRAWN.append(str(k))
    b += T(268, 332, f"{k} friends each", color=RED)
    F.emit("same-degree-different-friends", b, container="col", h=390)


# =============================================================================
# localization -- the eigenvector falls off the tail
# =============================================================================
LOC_XY = {}
for i in range(5):
    a = math.radians(72 * i)
    LOC_XY[LOCAL_CORE[i]] = (260 + 110 * math.cos(a), 180 + 110 * math.sin(a))
for i, t in enumerate(LOCAL_TAIL):
    LOC_XY[t] = (510 + 150 * i, 180)
LOC_ALL = [tuple(sorted(e)) for e in LOCAL.edges]
LOC_DIAG = [tuple(sorted(e)) for e in itertools.combinations(LOCAL_CORE, 2)
            if abs(LOCAL_CORE.index(e[0]) - LOCAL_CORE.index(e[1])) not in (1, 4)]
LOC_PLANAR = [e for e in LOC_ALL if e not in LOC_DIAG]


def fig_localization():
    start_log()
    # K5 is the canonical NON-planar graph, so the five chords of the pentagon must
    # cross -- five crossings, all of them core-to-core. Everything else (the rim
    # and the tail) is checked for planarity, and no edge may enter a disc.
    F.assert_planar_drawing(LOC_PLANAR, LOC_XY, "localization (rim and tail)")
    assert not F.clearance_bad(LOC_ALL, LOC_XY)
    x = F.crossings(LOC_ALL, LOC_XY)
    assert len(x) == 5 and all(set(a) <= set(LOCAL_CORE) for p in x for a in p), x

    ev = LOCAL_C["eigenvector"]
    top = max(ev.values())
    shown = dec(LOCAL_TAIL_FRACTION, 4)
    assert abs(float(shown) - ev["t4"] / top) < 5e-5, shown
    assert crown(ev)[0] in LOCAL_CORE

    b = edges_ink(LOC_ALL, LOC_XY)
    for n, p in LOC_XY.items():
        # floored at 14% so the faintest disc is still a disc and not a hole
        pctile = int(round(100 * (0.14 + 0.86 * ev[n] / top)))
        b += F.disc(p[0], p[1], "", fill=f"accent!{pctile}!white")
    b += F.mark(*LOC_XY["t4"], color=RED)
    b += T(30, 336, "shade = eigenvector score", color=DIM, anchor="west")
    b += T(30, 28, f"the far node scores {shown} of the top", color=RED, anchor="west")
    F.emit("localization", b, container="full", h=400)


# =============================================================================
FIGURES = [
    ("club-blank", fig_club_blank),
    ("club-network", fig_club_network),
    ("club-three-kings", fig_club_three_kings),
    ("degree-count", fig_degree_count),
    ("betweenness-idea", fig_betweenness_idea),
    ("sigma-graph", fig_sigma_graph),
    ("sigma-blank", fig_sigma_blank),
    ("sigma-answer", fig_sigma_answer),
    ("broker", fig_broker),
    ("star-closeness", fig_star_closeness),
    ("star-vs-path-1", fig_star_vs_path_1),
    ("star-vs-path-2", fig_star_vs_path_2),
    ("same-degree-different-friends", fig_same_degree_different_friends),
    ("localization", fig_localization),
] + [(n, _make_king(n, k, w)) for n, k, w in CLUB_KINGS]

if __name__ == "__main__":
    F.run(FIGURES)

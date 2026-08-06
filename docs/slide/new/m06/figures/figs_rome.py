#!/usr/bin/env python3
"""The Roman map and everything drawn on it — Parts 1 to 8.

Every figure in this module goes through `romelib.map_body()`, so the twelve discs
are in the same place on every slide of the deck and the only things that change
are the shading and the crown. That is the deck's central claim about itself, so
`romelib.assert_same_geometry()` is called on each one and the build fails, by
city name, if a figure moves anything.

All of them are full-width `fig tall` figures (1080 x ~420 px). They cannot be put
in a `cols` column: at 537 px the twelve Latin names do not fit at the 36 pt type
floor, and the deck therefore stacks text above the map rather than beside it.
"""

import numpy as np

import figlib as F
import romelib as R
from figlib import emit, seg, text
from verify_numbers import (ATTACK_BETWEEN, ATTACK_DEGREE, ATTACK_SURVIVORS,
                            CUT_C, CUT_EDGE, EIG_GAP_PCT, REDRAW, REDRAW_C,
                            REDRAW_CROWNS, REDRAW_IN, REDRAW_OUT, ROMA, ROMA_C,
                            ROMA_CROWNS, centralities, crown, hits, podium)

ACCENT, ACCENT2, ACCENT3, GRAY = "accent", "accenttwo", "accentthree", "annot"

# One height for every map, so no two metric slides differ in scale either.
MAP_H = 430
MAP_MOD = "tall"


def _map(name, **kw):
    emit(name, R.map_body(**kw), container="full", h=MAP_H, hmod=MAP_MOD)


# --------------------------------------------------------------------------- Part 1
def fig_milestone():
    """The Milliarium Aureum, drawn rather than photographed.

    A photograph would need a licence cleared and could not be held to the type
    floor; and the surviving object is a marble core whose gilded bronze is long
    gone, so a drawing is closer to what Augustus put up than any photograph is.
    """
    # The tikzpicture bounding box is (0,0)-(w,h) and anything drawn outside it is
    # CLIPPED silently, so the caption under the base has to start well above 0.
    cx, cy = 540.0, 120.0
    b = ""
    # stepped base
    for i, (hw, h) in enumerate(((150, 26), (124, 24), (100, 22))):
        b += (f"\\fill[{GRAY}] ({cx - hw:.0f},{cy + i * 24:.0f}) rectangle "
              f"({cx + hw:.0f},{cy + i * 24 + h:.0f});\n")
    # the column: a gilded cylinder, so accent-3 as a FILL is exactly its job
    top = cy + 3 * 24
    b += (f"\\fill[{ACCENT3}] ({cx - 46:.0f},{top:.0f}) rectangle "
          f"({cx + 46:.0f},{top + 210:.0f});\n")
    b += (f"\\draw[line width=3bp,draw=black] ({cx - 46:.0f},{top:.0f}) rectangle "
          f"({cx + 46:.0f},{top + 210:.0f});\n")
    # capital
    b += (f"\\fill[{GRAY}] ({cx - 62:.0f},{top + 210:.0f}) rectangle "
          f"({cx + 62:.0f},{top + 244:.0f});\n")
    # the inscription band, drawn as ruled lines rather than fake Latin
    for i in range(4):
        y = top + 170 - i * 34
        b += seg((cx - 30, y), (cx + 30, y), color="black", w=3.0)
    b += text(cx - 300, top + 120, "gilded\\\\bronze", color=ACCENT2, anchor="east")
    b += text(cx + 268, top + 60, "distances to\\\\every province", color="black",
              anchor="west")
    b += text(cx, cy - 18, "Milliarium Aureum, 20 BC", color=GRAY, anchor="north")
    emit("milestone", b, container="full", h=520, hmod=MAP_MOD)


def fig_milestone_radial():
    """The stone at the centre; distances outward, never across.

    The four numbers are Roman miles along the roads named, rounded to the nearest
    ten. They are constants here because they come from the road itineraries, not
    from the graph -- and they are the only hand-entered numbers in this module.
    """
    spokes = [("Gades", 20, 1650), ("Londinium", 7, 1310),
              ("Byzantium", -7, 1120), ("Alexandria", -20, 1560)]
    cx, cy, H = 96.0, 200.0, 400.0
    b = f"\\fill[{ACCENT3}] ({cx},{cy}) circle (26bp);\n"
    b += f"\\draw[line width=3bp] ({cx},{cy}) circle (26bp);\n"
    pts = []
    for place, ang, miles in spokes:
        a = np.deg2rad(ang)
        r0, r1 = 34.0, 470.0
        p = (cx + r0 * np.cos(a), cy + r0 * np.sin(a))
        q = (cx + r1 * np.cos(a), cy + r1 * np.sin(a))
        b += seg(p, q, color="black", w=2.6)
        b += text(q[0] + 16, q[1], f"{place} — {miles} miles", color="black",
                  anchor="west")
        pts.append(F.label_box(q[0] + 16, q[1], f"{place} — {miles} miles", "west"))
    b += text(cx, cy - 44, "the stone", color=ACCENT2, anchor="north")
    # "the stone" is centred under a disc that sits near the left edge, so its
    # own box is what runs off the canvas if the centre moves any further left.
    _sb = F.label_box(cx, cy - 44, "the stone", "north")
    assert _sb[0] >= 0 and _sb[2] <= 1080, _sb
    # Ink drawn outside the canvas does not exist -- assert the coordinates the
    # generator wrote rather than hoping the crop notices.
    for box in pts:
        assert 0 <= box[0] and box[2] <= 1080 and 0 <= box[1] and box[3] <= H, box
    emit("milestone-radial", b, container="full", h=H, hmod=MAP_MOD)


def fig_roma_map():
    """The map with a coastline behind it, before the abstraction step.

    The coastline is annotation gray and deliberately loose: it is scenery, and
    making it ink would give it the same weight as a road.
    """
    coast = [
        [(60, 300), (150, 330), (250, 322), (330, 336), (430, 330), (520, 318),
         (600, 300), (700, 290), (800, 300), (900, 282), (1010, 292)],
        [(70, 120), (170, 96), (280, 104), (390, 88), (500, 100), (610, 80),
         (720, 96), (830, 78), (940, 92), (1020, 76)],
    ]
    b = ""
    for line in coast:
        b += F.polyline(line, color=GRAY, w=2.2)
    b += R.map_body()
    emit("roma-map", b, container="full", h=440, hmod=MAP_MOD)


def fig_roma_graph():
    _map("roma-graph")


# --------------------------------------------------------------------------- Part 2
def fig_roma_degree():
    _map("roma-degree", scores=ROMA_C["degree"], crown_cities=ROMA_CROWNS["degree"])


def fig_degree_local():
    """What a city can see without a map: its own edges, and nothing else."""
    focus = "Roma"
    nbr = set(ROMA[focus]) | {focus}
    far = [c for c in R.CITIES if c not in nbr]
    b = ""
    for a, c in R.EDGES:
        col = "black" if (a in nbr and c in nbr) else GRAY
        w = F.EDGE_W if col == "black" else 1.4
        b += seg(R.NODE_XY[a], R.NODE_XY[c], color=col, w=w)
    for c in R.CITIES:
        fill = ACCENT if c in nbr else "white"
        b += (f"\\draw[line width=1.6bp,draw={'black' if c in nbr else GRAY},"
              f"fill={fill}] ({R.NODE_XY[c][0]:.2f},{R.NODE_XY[c][1]:.2f}) "
              f"circle ({F.NODE / 2}bp);\n")
    b += R.crowns([focus])
    b += R.labels()
    assert len(far) == ROMA.number_of_nodes() - ROMA.degree(focus) - 1
    emit("degree-local", b, container="full", h=MAP_H, hmod=MAP_MOD)


def fig_two_roads_ahead():
    """One step out, then two: the two ways past degree."""
    focus = "Roma"
    d = dict(zip(*zip(*[(n, l) for n, l in
                        __import__("networkx").single_source_shortest_path_length(
                            ROMA, focus).items()])))
    one = [c for c in R.CITIES if d[c] == 1]
    two = [c for c in R.CITIES if d[c] == 2]
    assert one and two
    b = R.edges()
    for c in R.CITIES:
        fill = {0: ACCENT2, 1: ACCENT, 2: ACCENT3}.get(d[c], "white")
        b += (f"\\draw[line width=1.6bp,draw=black,fill={fill}] "
              f"({R.NODE_XY[c][0]:.2f},{R.NODE_XY[c][1]:.2f}) "
              f"circle ({F.NODE / 2}bp);\n")
    b += R.labels()
    emit("two-roads-ahead", b, container="full", h=MAP_H, hmod=MAP_MOD)


# --------------------------------------------------------------------------- Part 3
def fig_distance_rings():
    import networkx as nx
    d = nx.single_source_shortest_path_length(ROMA, "Roma")
    scores = {c: 1.0 / (1 + d[c]) for c in R.CITIES}
    b = R.edges() + R.discs(scores)
    for c in R.CITIES:
        if d[c]:
            b += text(R.NODE_XY[c][0], R.NODE_XY[c][1] - 2, str(d[c]),
                      color="white", anchor="center")
    b += R.crowns(["Roma"])
    b += R.labels()
    emit("roma-distance-rings", b, container="full", h=MAP_H, hmod=MAP_MOD)


def _closeness_worksheet(name, show):
    import networkx as nx
    focus = "Massilia"
    d = nx.single_source_shortest_path_length(ROMA, focus)
    assert sum(v for k, v in d.items() if k != focus) == 22
    b = R.edges() + R.discs()
    for c in R.CITIES:
        if c == focus:
            continue
        b += text(R.NODE_XY[c][0], R.NODE_XY[c][1] - 2,
                  str(d[c]) if show else "?", color="white", anchor="center")
    b += R.crowns([focus])
    b += R.labels()
    emit(name, b, container="full", h=MAP_H, hmod=MAP_MOD)


def fig_closeness_one_city():
    _closeness_worksheet("closeness-one-city", True)


def fig_closeness_blank():
    _closeness_worksheet("closeness-blank", False)


def fig_roma_closeness():
    _map("roma-closeness", scores=ROMA_C["closeness"],
         crown_cities=ROMA_CROWNS["closeness"])


def fig_roma_cut():
    _map("roma-cut", broken=[CUT_EDGE])


def fig_roma_cut_closeness():
    flat = {c: 0.0 for c in R.CITIES}
    assert all(v == 0.0 for v in CUT_C["closeness"].values())
    _map("roma-cut-closeness", scores=flat, broken=[CUT_EDGE])


def fig_roma_cut_harmonic():
    h = CUT_C["harmonic"]
    assert crown(h) == ["Roma"] and h["Londinium"] == 0.0
    _map("roma-cut-harmonic", scores=h, crown_cities=crown(h), broken=[CUT_EDGE])


def fig_roma_eccentricity():
    cr = ROMA_CROWNS["eccentricity"]
    assert len(cr) == 3
    _map("roma-eccentricity", scores=ROMA_C["eccentricity"], crown_cities=cr)


# --------------------------------------------------------------------------- Part 4
def fig_roma_betweenness():
    _map("roma-betweenness", scores=ROMA_C["betweenness"],
         crown_cities=ROMA_CROWNS["betweenness"])


def fig_roma_betweenness_runnerup():
    """The runner-up, ringed. The crown stays on Rome so the two are not confused."""
    second = podium(ROMA_C["betweenness"])[1][0]
    third = podium(ROMA_C["betweenness"])[2][0]
    assert second == "Mediolanum" and ROMA.degree(second) < ROMA.degree(third)
    extra = F.ring(*R.NODE_XY[second], size=F.NODE, color=ACCENT3, w=5.0, grow=22)
    _map("roma-betweenness-runnerup", scores=ROMA_C["betweenness"],
         crown_cities=ROMA_CROWNS["betweenness"], extra=extra)


def _attack_panel(name, order, survivors, tag):
    import networkx as nx
    H = ROMA.copy()
    H.remove_nodes_from(order)
    giant = max(nx.connected_components(H), key=len)
    assert len(giant) == survivors, (name, len(giant), survivors)
    b = ""
    for a, c in R.EDGES:
        gone = a in order or c in order
        b += seg(R.NODE_XY[a], R.NODE_XY[c], color=GRAY if gone else "black",
                 w=1.4 if gone else F.EDGE_W, dash=F.DASH if gone else "")
    for c in R.CITIES:
        if c in order:
            fill, edge = "white", ACCENT2
        elif c in giant:
            fill, edge = ACCENT, "black"
        else:
            fill, edge = "white", GRAY
        b += (f"\\draw[line width=2.4bp,draw={edge},fill={fill}] "
              f"({R.NODE_XY[c][0]:.2f},{R.NODE_XY[c][1]:.2f}) "
              f"circle ({F.NODE / 2}bp);\n")
    b += R.labels()
    emit(name, b, container="full", h=MAP_H, hmod=MAP_MOD)


def fig_attack_degree():
    _attack_panel("attack-compare-1", ATTACK_DEGREE[0],
                  ATTACK_SURVIVORS["degree"], "by degree")


def fig_attack_between():
    _attack_panel("attack-compare-2", ATTACK_BETWEEN[0],
                  ATTACK_SURVIVORS["betweenness"], "by betweenness")


# --------------------------------------------------------------------------- Parts 5-7
def fig_roma_eigenvector():
    _map("roma-eigenvector", scores=ROMA_C["eigenvector"],
         crown_cities=ROMA_CROWNS["eigenvector"])


def fig_roma_katz():
    _map("roma-katz", scores=ROMA_C["katz"], crown_cities=ROMA_CROWNS["katz"])


def fig_hits_collapses():
    """Hub score and authority score on an undirected map: the same vector."""
    import networkx as nx
    A = nx.to_numpy_array(ROMA, nodelist=list(ROMA))
    hub, aut = hits(A)
    ev = np.array([ROMA_C["eigenvector"][n] for n in ROMA])
    assert np.abs(hub - ev).max() < 1e-8 and np.abs(aut - ev).max() < 1e-8
    scores = dict(zip(list(ROMA), hub))
    _map("hits-collapses", scores=scores, crown_cities=crown(scores))


# --------------------------------------------------------------------------- Part 8
CROWN_ORDER = ["degree", "closeness", "eccentricity", "betweenness",
               "eigenvector", "katz"]
CROWN_WORDS = {"degree": "most roads", "closeness": "closest on average",
               "eccentricity": "best worst case", "betweenness": "most traffic",
               "eigenvector": "best connected neighbours", "katz": "with a floor"}


def fig_crown_summary():
    """One panel per measure, identical geometry, emitted as a six-step build."""
    for i, m in enumerate(CROWN_ORDER, start=1):
        cr = ROMA_CROWNS[m]
        _map(f"crown-summary-{i}", scores=ROMA_C[m], crown_cities=cr)


def _redraw_panel(name, G, C_, tag):
    cr = crown(C_["betweenness"])
    edges = [tuple(e) for e in G.edges()]
    b = ""
    for a, c in edges:
        traded = (a, c) in (REDRAW_OUT, REDRAW_OUT[::-1]) or \
                 (a, c) in REDRAW_IN or (c, a) in REDRAW_IN
        b += seg(R.NODE_XY[a], R.NODE_XY[c],
                 color=ACCENT2 if traded else "black",
                 w=5.0 if traded else F.EDGE_W)
    b += R.discs(C_["betweenness"])
    b += R.crowns(cr)
    b += R.labels()
    emit(name, b, container="full", h=MAP_H, hmod=MAP_MOD)


def fig_redraw():
    _redraw_panel("redraw-1", ROMA, ROMA_C, "the map we drew")
    _redraw_panel("redraw-2", REDRAW, REDRAW_C, "one edge traded")
    assert REDRAW_CROWNS["betweenness"] == ["Mediolanum"]


FIGURES = [
    ("milestone", fig_milestone),
    ("milestone-radial", fig_milestone_radial),
    ("roma-map", fig_roma_map),
    ("roma-graph", fig_roma_graph),
    ("roma-degree", fig_roma_degree),
    ("degree-local", fig_degree_local),
    ("two-roads-ahead", fig_two_roads_ahead),
    ("roma-distance-rings", fig_distance_rings),
    ("closeness-one-city", fig_closeness_one_city),
    ("closeness-blank", fig_closeness_blank),
    ("roma-closeness", fig_roma_closeness),
    ("roma-cut", fig_roma_cut),
    ("roma-cut-closeness", fig_roma_cut_closeness),
    ("roma-cut-harmonic", fig_roma_cut_harmonic),
    ("roma-eccentricity", fig_roma_eccentricity),
    ("roma-betweenness", fig_roma_betweenness),
    ("roma-betweenness-runnerup", fig_roma_betweenness_runnerup),
    ("attack-compare-1", fig_attack_degree),
    ("attack-compare-2", fig_attack_between),
    ("roma-eigenvector", fig_roma_eigenvector),
    ("roma-katz", fig_roma_katz),
    ("hits-collapses", fig_hits_collapses),
    ("crown-summary", fig_crown_summary),
    ("redraw", fig_redraw),
]

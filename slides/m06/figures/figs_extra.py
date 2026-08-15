#!/usr/bin/env python3
"""Three column-width figures the deck needed after the slides were written.

They live in their own module rather than in `figs_small.py` only because that
file was being authored in parallel; there is nothing special about them.

Each is 537 bp wide, because each sits beside a formula panel or a block of text
that has to stay next to it.
"""

import math

import networkx as nx

import figlib as F
from figlib import emit, seg, text
from verify_numbers import CLUB, CLUB_BROKER, CLUB_C, CLUB_CLOSE, CLUB_SPREAD

ACCENT, ACCENT2, ACCENT3, GRAY = "accent", "accenttwo", "accentthree", "annot"

# --------------------------------------------------------------------------- the
# small graph behind the closeness definition and its harmonic repair. Six nodes,
# one focus, distances 1, 1, 2, 2, 3 -- small enough to read at a glance in a
# column, and the same shape both times so the second slide is visibly the first
# one with an edge removed.
IDEA_POS = {
    "f": (92.0, 150.0),
    "a": (250.0, 235.0),
    "b": (250.0, 65.0),
    "c": (385.0, 235.0),
    "d": (385.0, 65.0),
    "e": (488.0, 150.0),
}
IDEA_EDGES = [("f", "a"), ("f", "b"), ("a", "c"), ("b", "d"), ("c", "e")]
IDEA = nx.Graph(IDEA_EDGES)
FOCUS = "f"

_D = nx.single_source_shortest_path_length(IDEA, FOCUS)
assert sorted(v for k, v in _D.items() if k != FOCUS) == [1, 1, 2, 2, 3], _D


def _idea_body(cut_edge=None, reciprocal=False):
    G = IDEA.copy()
    if cut_edge:
        G.remove_edge(*cut_edge)
    d = nx.single_source_shortest_path_length(G, FOCUS)
    drawn = [e for e in IDEA_EDGES if not (cut_edge and set(e) == set(cut_edge))]
    F.assert_planar_drawing(drawn, IDEA_POS, "closeness idea")

    b = ""
    for u, v in IDEA_EDGES:
        if cut_edge and set((u, v)) == set(cut_edge):
            b += seg(IDEA_POS[u], IDEA_POS[v], color=GRAY, w=F.EDGE_W, dash=F.DASH)
        else:
            b += seg(IDEA_POS[u], IDEA_POS[v], color="black", w=F.EDGE_W)
    for n, (x, y) in IDEA_POS.items():
        fill = ACCENT2 if n == FOCUS else ACCENT
        b += (f"\\draw[line width=1.6bp,draw=black,fill={fill}] ({x},{y}) "
              f"circle ({F.NODE / 2}bp);\n")

    labels = {}
    for n in IDEA_POS:
        if n == FOCUS:
            continue
        if n in d:
            # Plain "1/2" rather than \tfrac: a stacked fraction is taller and
            # wider than the solver's box model expects, and at 537 bp that is
            # the difference between a solution and none.
            labels[n] = (f"1/{d[n]}" if reciprocal and d[n] > 1
                         else ("1" if reciprocal else str(d[n])))
        else:
            labels[n] = "0"
    sides, boxes = F.place_labels(labels, IDEA_POS, drawn,
                                  bounds=(6, 6, 531, 294), gap=3.0)
    b += F.draw_labels(labels, IDEA_POS, sides, color="black")
    return b, boxes


def fig_closeness_idea():
    """Distances from one node -- the numbers closeness adds up."""
    b, boxes = _idea_body()
    b += F.note("add these up", (268, 292), color=ACCENT2, anchor="center",
                boxes=boxes)
    emit("closeness-idea", b, container="col", h=340)


def fig_harmonic_idea():
    """The same graph with one node cut off, scored as reciprocals.

    The cut node contributes 0 instead of infinity, which is the whole of the
    repair -- so it is the only number on the drawing that is not a fraction.
    """
    b, boxes = _idea_body(cut_edge=("c", "e"), reciprocal=True)
    b += F.note("the island adds 0", (268, 292), color=ACCENT2, anchor="center",
                boxes=boxes)
    emit("harmonic-idea", b, container="col", h=340)


# --------------------------------------------------------------------------- the
# three crowned students, without the network. Used beside the day-one closing
# text, where there is no room for thirteen names.
def fig_club_three_kings_small():
    # Third mark is BLACK, not accent: a blue ring on a blue disc is invisible,
    # and blue text is the theme's structural colour rather than an emphasis.
    who = [(CLUB_SPREAD[0], "spreads the news fastest", ACCENT2),
           (CLUB_CLOSE[0], "closest to everyone else", ACCENT3),
           (CLUB_BROKER[0], "coordinates all the clubs", "black")]
    assert len({w[0] for w in who}) == 3
    b = ""
    y = 250.0
    for name, job, colour in who:
        deg = int(CLUB.degree(name))
        b += (f"\\draw[line width=5bp,draw={colour},fill=accent] (32,{y}) "
              f"circle ({F.NODE / 2}bp);\n")
        b += text(70, y + 14, f"{name} — {deg} friends", color="black", anchor="west")
        b += text(70, y - 20, job, color=GRAY, anchor="west")
        y -= 105
    emit("club-three-kings-small", b, container="col", h=320)


FIGURES = [
    ("closeness-idea", fig_closeness_idea),
    ("harmonic-idea", fig_harmonic_idea),
    ("club-three-kings-small", fig_club_three_kings_small),
]


# --------------------------------------------------------------------------- the
# club network with all three answers marked. `figs_small` emitted a column-width
# version of this that is really the small three-disc summary; the payoff slide of
# Part 1 needs the network itself, so it is drawn here at full width.
CLUB_XY = {
    "Sarah": (70.0, 300.0), "Mike": (70.0, 110.0), "Emma": (185.0, 205.0),
    "Alex": (325.0, 205.0), "Olivia": (325.0, 62.0), "James": (445.0, 110.0),
    "Sophia": (470.0, 275.0), "Ethan": (596.0, 392.0), "Ava": (648.0, 300.0),
    "Noah": (775.0, 265.0), "Lily": (900.0, 352.0), "Lucas": (940.0, 285.0),
    "Henry": (890.0, 175.0),
}
CLUB_MARK = None


def _assert_club_geometry():
    """Discs must not touch. The first layout put Ethan 38bp from Ava, and a 40bp
    disc 38bp from another one is two overlapping circles on both club figures."""
    import itertools
    close = [(a, b) for a, b in itertools.combinations(CLUB_XY, 2)
             if math.dist(CLUB_XY[a], CLUB_XY[b]) < F.NODE + 14]
    assert not close, f"club discs overlap or nearly touch: {close}"


def fig_club_three_answers():
    _assert_club_geometry()
    """One network, three marks, three questions -- the whole of Part 1's payoff."""
    import itertools
    edges = [tuple(e) for e in CLUB.edges()]
    assert set(CLUB_XY) == set(CLUB), sorted(set(CLUB_XY) ^ set(CLUB))
    F.assert_planar_drawing(edges, CLUB_XY, "club network")

    # Three marks, three colours, and the third one cannot be accent: a blue ring
    # on a blue disc is invisible, which is how the first version of this figure
    # shipped a mark nobody could see. Marked nodes change FILL instead, so all
    # three read at a glance, and the slide's figcaption names each colour.
    marks = [(CLUB_SPREAD[0], ACCENT2, "tell first"),
             (CLUB_CLOSE[0], ACCENT3, "closest to everyone"),
             (CLUB_BROKER[0], "black", "coordinates")]
    assert len({m[0] for m in marks}) == 3

    b = ""
    for u, v in edges:
        b += seg(CLUB_XY[u], CLUB_XY[v], color="black", w=F.EDGE_W)
    marked = {m[0]: m[1] for m in marks}
    for n, (x, y) in CLUB_XY.items():
        fill = marked.get(n, "accent")
        b += (f"\\draw[line width=1.6bp,draw=black,fill={fill}] ({x},{y}) "
              f"circle ({F.NODE / 2}bp);\n")
    # Same treatment as the Roman map: solve against discs and other labels only,
    # restricted to the four nearest sides, and halo the text so an edge behind it
    # stays readable. Solving against seventeen edges as well does not terminate
    # here -- the backtracker explores the whole tree before reporting failure.
    names = {n: n for n in CLUB_XY}
    saved = F.SIDES[:]
    F.SIDES[:] = saved[:4]
    try:
        sides, boxes = F.place_labels(names, CLUB_XY, [], bounds=(6, 6, 1074, 420),
                                      gap=3.0)
    finally:
        F.SIDES[:] = saved
    for dx, dy in [(a, c) for a in (-2, 0, 2) for c in (-2, 0, 2) if (a, c) != (0, 0)]:
        shifted = {n: (x + dx, y + dy) for n, (x, y) in CLUB_XY.items()}
        b += F.draw_labels(names, shifted, sides, color="white")
    b += F.draw_labels(names, CLUB_XY, sides, color="black")
    emit("club-three-answers", b, container="full", h=440, hmod="tall")


FIGURES.append(("club-three-answers", fig_club_three_answers))


# --------------------------------------------------------------------------- the
# blank club network with the CLUBS drawn on it. The first version of this slide
# listed the rosters as bullets beside a bare scatter of names; when the slide went
# full width the bullets went with it, and the figure was left saying "draw a line
# between two students who share a club" without anywhere showing who shares one.
# The grouping belongs in the drawing.
CLUB_BLOB_R = 36.0
# Candidate offsets for a club's name, tried in order from its members' centroid.
# Hand-assigning eight of these was tried first and the assertion below rejected
# the second one -- with thirteen student names already placed by the solver there
# is no way to guess a free spot, which is the whole reason FIGURE_GUIDE says to
# place labels with a solver rather than by hand.
CLUB_LABEL_SPOTS = [(anc, dx, dy)
                    for r in (52, 74, 96, 120)
                    for anc, ux, uy in (("south", 0, 1), ("north", 0, -1),
                                        ("west", 1, 0), ("east", -1, 0),
                                        ("south west", 0.7, 0.7), ("south east", -0.7, 0.7),
                                        ("north west", 0.7, -0.7), ("north east", -0.7, -0.7))
                    for dx, dy in ((ux * r, uy * r),)]


def _hull(pts):
    """Convex hull, counter-clockwise. Andrew's monotone chain, deduplicated."""
    pts = sorted(set((round(x, 3), round(y, 3)) for x, y in pts))
    if len(pts) <= 2:
        return pts

    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and ((out[-1][0] - out[-2][0]) * (p[1] - out[-2][1])
                                     - (out[-1][1] - out[-2][1]) * (p[0] - out[-2][0])) <= 0:
                out.pop()
            out.append(p)
        return out[:-1]

    return half(pts) + half(pts[::-1])


def fig_club_clubs():
    import itertools
    from verify_numbers import CLUBS
    assert set(CLUB_XY) == set(CLUB)

    _assert_club_geometry()
    b = ""
    # Each club is the rounded HULL of its members, not a band between every pair.
    # The pairwise version was drawn first and gave the exercise away: a spoke
    # between every two clubmates is the set of lines the student is being asked
    # to draw. A hull says "these people share a club" and nothing more.
    for members in CLUBS.values():
        pts = [CLUB_XY[m] for m in members]
        hull = _hull(pts)
        if len(hull) == 1:
            b += (f"\\fill[{ACCENT3},opacity=0.34] ({hull[0][0]},{hull[0][1]}) "
                  f"circle ({CLUB_BLOB_R}bp);\n")
        elif len(hull) == 2:
            b += (f"\\draw[line width={2 * CLUB_BLOB_R}bp,draw={ACCENT3},opacity=0.34,"
                  f"line cap=round] ({hull[0][0]},{hull[0][1]}) -- "
                  f"({hull[1][0]},{hull[1][1]});\n")
        else:
            path = " -- ".join(f"({x:.1f},{y:.1f})" for x, y in hull)
            b += (f"\\filldraw[{ACCENT3},opacity=0.34,line width={2 * CLUB_BLOB_R}bp,"
                  f"draw={ACCENT3},line join=round,line cap=round] {path} -- cycle;\n")

    for n, (x, y) in CLUB_XY.items():
        b += (f"\\draw[line width=1.6bp,draw=black,fill=accent] ({x},{y}) "
              f"circle ({F.NODE / 2}bp);\n")

    names = {n: n for n in CLUB_XY}
    saved = F.SIDES[:]
    F.SIDES[:] = saved[:4]
    try:
        sides, boxes = F.place_labels(names, CLUB_XY, [], bounds=(6, 6, 1074, 420),
                                      gap=3.0)
    finally:
        F.SIDES[:] = saved
    for dx, dy in [(a, c) for a in (-2, 0, 2) for c in (-2, 0, 2) if (a, c) != (0, 0)]:
        shifted = {n: (x + dx, y + dy) for n, (x, y) in CLUB_XY.items()}
        b += F.draw_labels(names, shifted, sides, color="white")
    b += F.draw_labels(names, CLUB_XY, sides, color="black")

    # Club names, placed by hand and then held to the same collision rule the
    # student names are: a club label that lands on a student name is worse than
    # no club label, because the room reads it as that student's.
    placed = dict(boxes)
    for club, members in CLUBS.items():
        mx = sum(CLUB_XY[m][0] for m in members) / len(members)
        my = sum(CLUB_XY[m][1] for m in members) / len(members)
        chosen = None
        for anc, dx, dy in CLUB_LABEL_SPOTS:
            cx, cy = mx + dx, my + dy
            box = F.label_box(cx, cy, club, anc)
            if not (6 <= box[0] and box[2] <= 1074 and 6 <= box[1] and box[3] <= 430):
                continue
            if any(F.boxes_overlap(box, o) for o in placed.values()):
                continue
            if any(F.box_hits_disc(box, x, y) for x, y in CLUB_XY.values()):
                continue
            chosen = (cx, cy, anc, box)
            break
        assert chosen, (f"no clear spot for the {club} label -- move a student, or "
                        f"widen the canvas; do not shrink the type")
        cx, cy, anc, box = chosen
        placed[club] = box
        b += text(cx, cy, club, color=GRAY, anchor=anc)

    emit("club-clubs", b, container="full", h=440, hmod="tall")


FIGURES.append(("club-clubs", fig_club_clubs))

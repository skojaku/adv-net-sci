#!/usr/bin/env python3
"""Three column-width figures the deck needed after the slides were written.

They live in their own module rather than in `figs_small.py` only because that
file was being authored in parallel; there is nothing special about them.

Each is 537 bp wide, because each sits beside a formula panel or a block of text
that has to stay next to it.
"""

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
    who = [(CLUB_SPREAD[0], "spreads the news fastest", ACCENT2),
           (CLUB_CLOSE[0], "closest to everyone else", ACCENT3),
           (CLUB_BROKER[0], "coordinates all the clubs", ACCENT)]
    assert len({w[0] for w in who}) == 3
    b = ""
    y = 250.0
    for name, job, colour in who:
        deg = int(CLUB.degree(name))
        b += (f"\\draw[line width=5bp,draw={colour},fill=accent] (32,{y}) "
              f"circle ({F.NODE / 2}bp);\n")
        b += text(70, y + 14, f"{name} — {deg} friends", color="black", anchor="west")
        b += text(70, y - 20, job, color=colour if colour != ACCENT3 else GRAY,
                  anchor="west")
        y -= 105
    emit("club-three-kings-small", b, container="col", h=320)


FIGURES = [
    ("closeness-idea", fig_closeness_idea),
    ("harmonic-idea", fig_harmonic_idea),
    ("club-three-kings-small", fig_club_three_kings_small),
]

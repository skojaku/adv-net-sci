#!/usr/bin/env python3
"""The one layout of Feld's eight girls, shared by every figure that draws them.

Nine figures draw this graph. If each solved its own positions the graph would change
shape and size between consecutive slides -- m01 shipped a figure whose nodes ranged
68-177px across a build for exactly that reason. One dict, imported everywhere.

Feld's own Figure 1 crosses Sue-Dale with Alice-Pam. The graph is planar, so ours does
not (rubric F2): the K5-minus-three-edges core sits on the left with Pam above the
Sue-Alice line and Dale below it, Jane hangs off Alice and Dale on the right, and the
Pam - Carol - Tina chain runs along the top right.
"""

from figlib import FULL_W, assert_planar_drawing, place_labels
from verify_numbers import FELD_EDGES, FELD_ORDER, feld_graph, friend_means, moments

G = feld_graph()
M = moments(G)
FM = friend_means(G)

# bp on the 1080bp full-width canvas; y grows upward.
#
# The vertical span is deliberately shallow. Solved names stick out roughly 50bp above
# the top disc and below the bottom one, and the CROPPED drawing has a hard budget of
# 380bp before the height binds the deck's scale and every label in the figure shrinks.
# A first layout 232bp tall measured 408bp with its names on and would have failed the
# gate; LABEL_BAND is what the solver is actually allowed to use.
POS = {
    "Betty": (118, 212),
    "Sue": (312, 212),
    "Alice": (536, 212),
    "Pam": (424, 312),
    "Dale": (424, 112),
    "Jane": (660, 118),
    "Carol": (716, 312),
    "Tina": (948, 312),
}
LABEL_BAND = (6, 20, 1074, 376)      # 356bp of ink + 24bp of crop pad = the 380bp cap

# The room reads the colours as: below the line / above it / exactly equal.
BELOW = ["Betty", "Jane", "Pam", "Dale", "Tina"]
ABOVE = ["Sue", "Alice"]
EQUAL = ["Carol"]
assert BELOW == [v for v in FELD_ORDER if FM[v][2] > G.degree(v)]
assert ABOVE == [v for v in FELD_ORDER if FM[v][2] < G.degree(v)]
assert EQUAL == [v for v in FELD_ORDER if FM[v][2] == G.degree(v)]

assert set(POS) == set(FELD_ORDER)
assert_planar_drawing(FELD_EDGES, POS, "feld layout")
assert min(x for x, _ in POS.values()) > 60, "leftmost disc is too close to the canvas"
assert max(x for x, _ in POS.values()) < FULL_W - 60, "rightmost disc is too close"


def solve_names(extra_blockers=(), size=None):
    """Place the eight names with the backtracking solver, inside the canvas."""
    from figlib import FONT
    names = {n: n for n in POS}
    return place_labels(names, POS, FELD_EDGES, blockers=extra_blockers,
                        bounds=LABEL_BAND, size=size or FONT)


def degree(v):
    return G.degree(v)


def friend_mean(v):
    """Feld's Table 1 column: the mean degree of v's friends, as a float."""
    return float(FM[v][2])

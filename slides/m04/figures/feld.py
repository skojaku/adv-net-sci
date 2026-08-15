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


# ------------------------------------------------------------ how each group is drawn
# R5 A5-1, the fourth and fifth address of one defect. The membership lists have always
# lived here and the COLOURS lived in each figure module, so every round a call site
# nobody had named kept the opposite key: accent-2 meant "above her friends' average" on
# slides 010 and 012 and "below" on 039, 040, 082 and 096, and `figs_edge.py` grew its
# own declaration with an assertion that guaranteed the inversion.
#
# Data and role are one object now. `paradox_groups()` is the only way to get the
# memberships, and it hands back the way each is drawn along with them, so a figure
# cannot take the lists and invent its own colours for them.
ABOVE_FRIENDS = "accenttwo"   # her friends average FEWER than she has -- the minority
BELOW_FRIENDS = None          # hollow: legible as "not red", carrying no second meaning
EQUAL_FRIENDS = "annot"       # exactly equal

PARADOX_ROLE = {"above": ABOVE_FRIENDS, "below": BELOW_FRIENDS, "equal": EQUAL_FRIENDS}


def paradox_groups():
    """(relation, members, role) for the three groups -- one object, never three."""
    return (("above", ABOVE, ABOVE_FRIENDS),
            ("below", BELOW, BELOW_FRIENDS),
            ("equal", EQUAL, EQUAL_FRIENDS))


def paradox_role(rel):
    """The way a girl who is above / below / exactly on her friends' average is drawn."""
    assert rel in PARADOX_ROLE, f"unknown relation {rel!r}"
    return PARADOX_ROLE[rel]


def paradox_rel(v):
    """Which of the three a girl is in, from the data rather than from a caller."""
    k, fm = G.degree(v), FM[v][2]
    return "below" if fm > k else "above" if fm < k else "equal"


assert {v: paradox_rel(v) for v in FELD_ORDER} == \
    {v: r for r, members, _ in paradox_groups() for v in members}
assert len({ABOVE_FRIENDS, BELOW_FRIENDS, EQUAL_FRIENDS}) == 3, "two groups share a role"

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

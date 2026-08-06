#!/usr/bin/env python3
"""The one Roman-map geometry that every metric figure in Module 06 reuses.

The deck's whole defence against a centrality-catalogue lecture is that the map
never changes: seven metric slides show the identical twelve discs in the
identical places, and the only things that differ are the shading and the crown
(SLIDE_RUBRIC F1). That is an invariant, so it is asserted rather than intended --
`assert_same_geometry()` names the offending city if a figure draws one elsewhere.

Positions come from the real longitude/latitude in `verify_numbers.ROMA_POS`,
mapped affinely into the drawing box. The map is stretched horizontally (the box
is 2.8:1 and the Mediterranean is 1.5:1) because the slide's height cap is hard at
380 px; an affine map cannot create or remove an edge crossing, so the topology
the deck talks about is untouched.
"""

import numpy as np

import figlib as F
# TikZ colour NAMES, as defined in figlib's preamble. The module-level hex
# constants in figlib are for computing shades, not for passing to TikZ:
# xcolor has no colour called "B14434" and a raw hex fill is a fatal error.
ACCENT, ACCENT2, ACCENT3, GRAY = "accent", "accenttwo", "accentthree", "annot"
from verify_numbers import (CUT_EDGE, ROMA, ROMA_C, ROMA_EDGES, ROMA_POS, crown)

# --------------------------------------------------------------------------- box
# Authored for the 1080 bp full-width container. The height budget is what the
# `.fig` cap allows once figlib's 12 bp crop padding is added on both sides:
# 380 - 2*12 = 356, and the labels have to live inside that with the discs.
FULL_W = 1080
# The map is emitted as a `fig tall` (420 px cap), so the ink budget is
# 420 - 2*12 bp of figlib crop padding = 396. That number is not a preference:
# at 356 (a plain `.fig`) the twelve names cannot be placed at the 36 pt floor
# at all, at 376 they still cannot, and at 396 every one of them fits on one of
# the FOUR NEAREST sides of its own disc. See `LABEL_SIDES` below.
INK_H = 396
FIG_MOD = "tall"

# Discs sit inside this; labels may use the full band.
BAND = (8.0, 8.0, FULL_W - 8.0, INK_H - 8.0)

CITIES = list(ROMA_POS)
EDGES = [(a, b) for a, b, _ in ROMA_EDGES]
WHY = {(a, b): w for a, b, w in ROMA_EDGES}


# A straight affine projection of longitude/latitude was tried first, and the label
# solver cannot place twelve names at the 36 pt type floor inside it: the projection
# puts Tarraco, Lugdunum, Massilia and Colonia inside 170 bp of width and each of
# them needs a ~170 bp label, so three cities have *zero* viable sides before any
# other label is placed. FIGURE_GUIDE's instruction in that situation is explicit --
# move a node, do not shrink the type.
#
# So these coordinates come from an annealing search (scratch script recorded in the
# commit message) with planarity, disc clearance and label-solvability as hard
# constraints and geographic faithfulness as the objective. The result is checked
# below: **longitude order is exactly preserved**, latitude order to rho = 0.96. The
# lecturer can point at it and say "the Mediterranean" without saying anything false.
_RAW = {
    "Londinium": (62.6, 375.4),
    "Colonia": (343.9, 373.1),
    "Lugdunum": (201.7, 311.1),
    "Massilia": (325.1, 211.5),
    "Tarraco": (75.3, 202.8),
    "Mediolanum": (488.5, 320.2),
    "Roma": (592.3, 207.0),
    "Carthago": (490.9, 90.2),
    "Thessalonica": (745.2, 199.2),
    "Athenae": (898.4, 193.2),
    "Byzantium": (1002.9, 309.6),
    "Alexandria": (1014.4, 89.2),
}

# Stretched into the 396 bp band. An affine map cannot create or remove a
# crossing, so the topology the deck talks about survives the rescale; the
# assertions below re-check it anyway.
_ylo, _yhi = min(p[1] for p in _RAW.values()), max(p[1] for p in _RAW.values())
_BOT, _TOP = 56.0, INK_H - 56.0
NODE_XY = {c: (p[0], _BOT + (p[1] - _ylo) / (_yhi - _ylo) * (_TOP - _BOT))
           for c, p in _RAW.items()}


def _rank(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0] * len(vals)
    for pos, i in enumerate(order):
        r[i] = pos
    return np.array(r, float)


def _spearman(a, b):
    ra, rb = _rank(a), _rank(b)
    ra, rb = ra - ra.mean(), rb - rb.mean()
    return float(ra @ rb / np.sqrt((ra @ ra) * (rb @ rb)))


# The drawing is a schematic, but it is not a rearrangement: west stays west and
# north stays north, so the lecturer can point at it and say "the Mediterranean".
_lon = [ROMA_POS[c][0] for c in CITIES]
_lat = [ROMA_POS[c][1] for c in CITIES]
GEO_RHO_X = _spearman([NODE_XY[c][0] for c in CITIES], _lon)
GEO_RHO_Y = _spearman([NODE_XY[c][1] for c in CITIES], _lat)
assert GEO_RHO_X > 0.999, f"the layout reorders east and west (rho = {GEO_RHO_X:.3f})"
assert GEO_RHO_Y > 0.94, f"the layout scrambles north and south (rho = {GEO_RHO_Y:.3f})"

# --------------------------------------------------------------------------- gates
F.assert_planar_drawing(EDGES, NODE_XY, "roman map")

_span = max(x for x, _ in NODE_XY.values()) - min(x for x, _ in NODE_XY.values())
assert _span / FULL_W > 0.70, f"the map spans only {_span / FULL_W:.0%} of the canvas"


def assert_same_geometry(name, xy):
    """Every metric figure calls this. A moved city fails the build, by name."""
    assert set(xy) == set(NODE_XY), f"{name}: draws {sorted(set(xy) ^ set(NODE_XY))}"
    off = [c for c in xy if abs(xy[c][0] - NODE_XY[c][0]) > 1e-9
           or abs(xy[c][1] - NODE_XY[c][1]) > 1e-9]
    assert not off, (f"{name}: {', '.join(off)} moved -- every metric slide must show "
                     f"the identical map, or the deck's one-map claim is false")


# --------------------------------------------------------------------------- labels
# Solved once and frozen, so two figures cannot place the same name differently.
#
# Two decisions here, both made after looking at the render rather than the code.
#
# 1. The solver runs WITHOUT the edge constraint. With eighteen edges among twelve
#    cities there is no assignment that clears the edges as well as the discs and
#    the other labels -- three cities have *zero* viable sides before any other
#    label is placed -- so a name is allowed to lie across a road.
# 2. It is then drawn with a white HALO, not on a white chip. The chip version was
#    built first and rendered a map whose roads were chopped into pieces wherever a
#    name crossed them: Londinium's road to Colonia simply stopped. A halo lets the
#    road show through between the letters, which is what an atlas does.
#
# And the solver is restricted to the four NEAREST sides, so no name ends up
# floating between two cities with nothing to say which one it belongs to. That is
# only possible because the figure is a `fig tall`; at the plain 380 px cap there
# is no solution at any distance.
_NEAR_SIDES = F.SIDES[:4]


def _solve_near():
    saved = F.SIDES[:]
    F.SIDES[:] = _NEAR_SIDES
    try:
        return F.place_labels({c: c for c in CITIES}, NODE_XY, [], bounds=BAND, gap=3.0)
    finally:
        F.SIDES[:] = saved


LABEL_SIDES, LABEL_BOXES = _solve_near()
assert all(max(abs(dx), abs(dy)) <= 26 for _, dx, dy in LABEL_SIDES.values()), \
    "a name drifted onto the far ring -- it would no longer read as that city's"

# Halo offsets: eight directions at 2 bp. `contour` is not in this TeX install, so
# the halo is drawn by hand; 2 bp at 36 pt is enough to break a 2.6 bp road line.
_HALO = [(dx, dy) for dx in (-2, 0, 2) for dy in (-2, 0, 2) if (dx, dy) != (0, 0)]


def labels(color="black"):
    """Every city name, haloed in white so a road can pass behind it."""
    out = ""
    for dx, dy in _HALO:
        shifted = {c: (NODE_XY[c][0] + dx, NODE_XY[c][1] + dy) for c in CITIES}
        out += F.draw_labels({c: c for c in CITIES}, shifted, LABEL_SIDES, color="white")
    out += F.draw_labels({c: c for c in CITIES}, NODE_XY, LABEL_SIDES, color=color)
    return out


# --------------------------------------------------------------------------- ink
def _mix(t, base=(0x39, 0x59, 0xA6)):
    """White -> accent at fraction t, as an inline TikZ colour expression.

    Returned as `{rgb,255:red,R;green,G;blue,B}` rather than a bare hex string:
    xcolor has no colour named "3959A6", and a raw hex fill is a fatal LaTeX error
    rather than a wrong colour, which is at least loud.
    """
    t = 0.0 if t is None else max(0.0, min(1.0, float(t)))
    # Floor the ramp at 0.30 so the lightest disc is still a disc: a near-white node
    # reads as a hole in the map, and check_render's node detector masks on the FILL
    # colour with a tolerance of 46, so a pale disc is not a node at all to the gate
    # and the 26-52 px band goes unenforced on that slide.
    t = 0.30 + 0.70 * t
    r, g, b = (int(round(255 + (c - 255) * t)) for c in base)
    return "{rgb,255:red,%d;green,%d;blue,%d}" % (r, g, b)


def edges(broken=(), color="black", w=F.EDGE_W):
    out = ""
    for a, b in EDGES:
        if (a, b) in broken or (b, a) in broken:
            out += F.seg(NODE_XY[a], NODE_XY[b], color=GRAY, w=w, dash=F.DASH)
        else:
            out += F.seg(NODE_XY[a], NODE_XY[b], color=color, w=w)
    return out


def discs(scores=None):
    """Twelve discs shaded by `scores` (city -> value), or all accent if none.

    The shading is the ONLY thing that differs between two metric figures, so the
    caller must state what it encodes in the slide's figcaption ("darker = higher
    closeness"). An unexplained shade is an F1 Blocker.
    """
    out = ""
    top = max(scores.values()) or 1.0 if scores else 1.0
    for c in CITIES:
        fill = "accent" if scores is None else _mix(scores[c] / top)
        out += (f"\\draw[line width=1.6bp,draw=black,fill={fill}] "
                f"({NODE_XY[c][0]:.2f},{NODE_XY[c][1]:.2f}) circle ({F.NODE / 2}bp);\n")
    return out


def crowns(cities, color=ACCENT2):
    """An accent-2 ring plus a crown glyph, on every city that holds the maximum.

    A shared crown is a real answer -- eccentricity crowns three cities -- so this
    takes a list and draws all of them. Drawing one where the data has three would
    be a false claim on the slide.
    """
    out = ""
    for c in cities:
        x, y = NODE_XY[c]
        out += F.ring(x, y, size=F.NODE, color=color, w=4.0, grow=13)
        out += _crown_glyph(x, y + F.NODE / 2 + 26, color)
    return out


def _crown_glyph(x, y, color=ACCENT2, w=44.0, h=28.0):
    """A small crown, drawn as a filled path so it reads at slide size."""
    pts = [(x - w / 2, y - h / 2), (x - w / 2, y + h / 2), (x - w / 4, y),
           (x, y + h / 2 + 3), (x + w / 4, y), (x + w / 2, y + h / 2),
           (x + w / 2, y - h / 2)]
    return "\\fill[%s] %s -- cycle;\n" % (
        color, " -- ".join(f"({a:.2f},{b:.2f})" for a, b in pts))


def map_body(scores=None, crown_cities=(), broken=(), extra="", label_color="black"):
    """The standard metric-map drawing. Every metric figure goes through here."""
    assert_same_geometry("map_body", NODE_XY)
    return (edges(broken=broken) + discs(scores) + crowns(list(crown_cities))
            + labels(color=label_color) + extra)


# Candidate anchors for an in-drawing note, tried in order. A note is pinned to a
# corner while the names are placed by the solver, so a fixed corner is a collision
# waiting to happen -- m03 drew a note straight through the word "Znojmo", and the
# first version of this module put one through "Londinium" on nineteen figures at
# once. Trying several anchors and asserting the survivor is cheaper than either.
_NOTE_SPOTS = [
    ((FULL_W - 16, 22), "east"),
    ((16, 22), "west"),
    ((FULL_W - 16, INK_H - 22), "east"),
    ((16, INK_H - 22), "west"),
    ((FULL_W / 2, 22), "center"),
    ((FULL_W / 2, INK_H - 22), "center"),
]


def note(s, color=ACCENT2, size=F.FONT):
    """A short in-drawing note, placed where it clears every name and every disc.

    Notes carry NUMBERS. Prose belongs in the deck's figcaption -- a note long
    enough to be a sentence will not fit anywhere on a map this full, and the
    assertion below says so rather than letting it overlap something.
    """
    for at, anchor in _NOTE_SPOTS:
        b = F.label_box(at[0], at[1], s, anchor, size=size)
        if not (0 <= b[0] and b[2] <= FULL_W and 0 <= b[1] and b[3] <= INK_H):
            continue
        if any(F.boxes_overlap(b, o) for o in LABEL_BOXES.values()):
            continue
        if any(F.box_hits_disc(b, x, y) for x, y in NODE_XY.values()):
            continue
        return F.text(at[0], at[1], s, color=color, anchor=anchor, size=size)
    raise AssertionError(
        f"in-drawing note {s!r} does not fit anywhere clear on the map -- shorten it "
        f"to the numbers, and put the sentence in the slide's figcaption")

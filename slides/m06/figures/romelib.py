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
# Placed by an offline search (grid of candidate centres, then a greedy pass) and frozen,
# so two figures cannot place the same name differently. The rule the search enforced,
# and `check_labels()` below re-asserts at every build:
#
#   * a name's white box never covers a road that does not end at that name's city
#     (round 2: the Thessalonica box hid the Roma-Alexandria road and the Roma box
#     hid the stubs of Roma's own roads);
#   * Roma's five roads all leave its disc in the open;
#   * no box touches a disc that is not its own, a crown zone, or another box;
#   * a name sits next to its own city: its own disc is the nearest disc to the box.
#
# One road is allowed under its own city's name, and only where no free place exists
# (Athenae, which is boxed in by three roads): see `OWN_ROAD_OK`.
#
# WH is the measured size (bp) of the white box of each name at the 36 pt floor, from a
# test render with a red fill; the box centre is the TikZ `anchor=center` point.
WH = {"Londinium": (158.8, 27.2), "Colonia": (112.2, 27.2), "Lugdunum": (158.2, 34.2),
      "Massilia": (118.8, 27.2), "Tarraco": (113.2, 27.2), "Mediolanum": (180.2, 27.2),
      "Roma": (87.8, 27.2), "Carthago": (136.2, 34.2), "Thessalonica": (185.8, 27.2),
      "Athenae": (121.8, 27.2), "Byzantium": (159.8, 34.2), "Alexandria": (159.8, 27.2)}
LABEL_AT = {
    "Athenae": (918, 119),
    "Lugdunum": (96, 266),
    "Londinium": (167, 357),
    "Colonia": (423, 366),
    "Roma": (621, 132),
    "Thessalonica": (744, 221),
    "Alexandria": (908, 37),
    "Massilia": (324, 137),
    "Carthago": (396, 41),
    "Mediolanum": (604, 284),
    "Tarraco": (75, 209),
    "Byzantium": (992, 318),
}
OWN_ROAD_OK = {"Athenae", "Thessalonica"}
CROWNED = ("Roma", "Massilia", "Mediolanum")   # the only cities any metric figure crowns
_LBL_MARGIN = 3.0          # half the fill's inner sep, doubled: a clear strip around the white box


def _label_box(c, cx, cy, m=_LBL_MARGIN):
    w, h = WH[c]
    return (cx - w / 2 - m, cy - h / 2 - m, cx + w / 2 + m, cy + h / 2 + m)


LABEL_BOXES = {c: _label_box(c, *LABEL_AT[c]) for c in CITIES}


def _gap(b, x, y):
    return float(np.hypot(max(b[0] - x, 0, x - b[2]), max(b[1] - y, 0, y - b[3])))


def check_labels():
    """No white box covers a road that is not its own city's; none hides a disc, a crown or a name."""
    assert set(LABEL_AT) == set(CITIES), "a city has no label"
    for c in CITIES:
        b = LABEL_BOXES[c]
        assert BAND[0] - 4 <= b[0] and b[2] <= BAND[2] + 4 and BAND[1] - 4 <= b[1] and b[3] <= BAND[3] + 4, \
            f"{c}: label outside the drawing"
        for o in CITIES:
            x, y = NODE_XY[o]
            assert _gap(b, x, y) >= F.NODE / 2 + 2, f"{c}: label covers the disc of {o}"
            if o != c:
                assert _gap(b, x, y) > _gap(b, *NODE_XY[c]) + (13 if c in OWN_ROAD_OK else 29), \
                    f"{c}: label sits nearer to {o} than to {c}"
        for o in CROWNED:
            x, y = NODE_XY[o]
            assert (b[2] <= x - 30 or x + 30 <= b[0] or b[3] <= y + 18 or y + 62 <= b[1]), \
                f"{c}: label sits where the crown of {o} is drawn"
        for a, d in EDGES:
            if c in (a, d):
                if c == "Roma":
                    assert not F.box_hits_segment(b, NODE_XY[a], NODE_XY[d], pad=0), \
                        f"Roma: its label hides part of the road {a}-{d}"
                continue
            assert not F.box_hits_segment(b, NODE_XY[a], NODE_XY[d], pad=1), \
                f"{c}: its label covers the road {a}-{d}, which does not end there"
        for o in CITIES:
            if o < c:
                q = LABEL_BOXES[o]
                assert (b[2] + 3 <= q[0] or q[2] + 3 <= b[0] or b[3] + 3 <= q[1] or q[3] + 3 <= b[1]), \
                    f"labels {c} and {o} touch"
    own = {c: sum(1 for a, d in EDGES if c in (a, d)
                  and F.box_hits_segment(LABEL_BOXES[c], NODE_XY[a], NODE_XY[d], pad=0))
           for c in CITIES}
    extra = {c: n for c, n in own.items() if n and c not in OWN_ROAD_OK}
    assert not extra, f"a label lies on its own city's road: {extra}"


check_labels()


def labels(color="black"):
    """Every city name on a white box, so a road ends at the box and does not run through
    the letters. Called after the roads and the discs, so the box covers whatever it overlaps."""
    out = ""
    for c in CITIES:
        out += F.text(LABEL_AT[c][0], LABEL_AT[c][1], c, color=color, anchor="center")
    return out.replace("\\node[", "\\node[fill=white,inner sep=1.5pt,")


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
    """A heavy accent-2 border plus a crown glyph, on every city holding the max.

    A shared crown is a real answer -- eccentricity crowns three cities -- so this
    takes a list and draws all of them. Drawing one where the data has three would
    be a false claim on the slide.

    A separate RING around the disc was drawn here first and had to go. The render
    gate masks node fill colours and then fills holes, so a disc sitting inside an
    accent-2 ring reads to it as one 57 px disc, and every crowned slide in the
    deck failed the 26-52 px band at once. A heavy border on the disc itself says
    exactly the same thing and leaves the disc the size it actually is.
    """
    out = ""
    for c in cities:
        x, y = NODE_XY[c]
        out += (f"\\draw[line width=5bp,draw={color}] ({x:.2f},{y:.2f}) "
                f"circle ({F.NODE / 2}bp);\n")
        out += _crown_glyph(x, y + F.NODE / 2 + 20, color)
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


# ============================================================================ col layout
# The opening trio of Module 06 (roma-basemap, roma-to-graph, roma-degree) lives in the right
# half of the slide (a 537 bp `col`), so it cannot reuse the 1080 bp drawing above. These
# figures put the twelve pins at their REAL map positions (the OpenStreetMap tile map of
# data/roma-basemap.json) and turn the pins into the discs of the graph where they stand, so
# a map and its graph are the same picture. One canvas, one crop, three figures.
import json as _json
import math as _math
from PIL import Image as _Image

COL_W = F.COL_W
COL_H = 420
COL_MOD = "tall"                 # 400 bp cap: the map is 365 bp tall plus the disc overshoot
_DATA = F.OUT / "data"
_PALE = _DATA / "roma-basemap-pale.png"
BASEMAP = _DATA / "roma-basemap-col.png"
_meta = _json.loads((_DATA / "roma-basemap.json").read_text())
IMG_W, IMG_H = _meta["image"]["width"], _meta["image"]["height"]
assert _Image.open(_PALE).size == (IMG_W, IMG_H)


def _make_col_basemap():
    """The pale OSM map, simplified for a 430 bp wide figure: land goes to near-paper (the
    raster grain leaves it clean), the sea stays a soft blue-grey, and the street labels,
    which are unreadable at this size and only add speckle, are blurred away."""
    import numpy as np
    from PIL import ImageFilter
    a = np.asarray(_Image.open(_PALE).convert("RGB").filter(ImageFilter.GaussianBlur(2.2))).astype(float)
    sea = np.clip((a[..., 2] - a[..., 0] - 6) / 14.0, 0, 1)[..., None]       # blue-ish -> 1
    sea_col = np.array([196, 209, 222], float)
    land = 255 - 0.08 * (255 - a)                                           # faint relief only
    out = sea * sea_col + (1 - sea) * land
    return _Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGB")


if not BASEMAP.exists() or BASEMAP.stat().st_mtime < _PALE.stat().st_mtime:
    _make_col_basemap().save(BASEMAP)
assert set(_meta["cities"]) == set(CITIES), "basemap cities differ from the Roman graph"

# The whole 2000 x 1826 image is shown, stretched by 10% sideways: the height cap (400 bp)
# fixes the vertical scale, and the width has to reach 76% of the column for the ink gate.
SX, SY = 0.22, 0.20
MAP_WBP, MAP_HBP = IMG_W * SX, IMG_H * SY
MAP_X0, MAP_Y0 = (COL_W - MAP_WBP) / 2, 26.0
PIN_XY = {c: (MAP_X0 + v["px"] * SX, MAP_Y0 + (IMG_H - v["py"]) * SY)
          for c, v in _meta["cities"].items()}
PIN_D = 18               # bp, a pin on the map
DISC_D = 34              # bp, a node of the graph (about 34 px on the slide)

# Straight roads between the pins must be a clean planar drawing, and no two discs may touch.
F.assert_planar_drawing(EDGES, PIN_XY, "roma pins")
for _a in CITIES:
    for _b in CITIES:
        if _a < _b:
            assert _math.dist(PIN_XY[_a], PIN_XY[_b]) > DISC_D + 6, f"discs {_a} and {_b} nearly touch"

# "Roma" sits north-east of its pin: the wedge between its roads to Mediolanum (north-west)
# and Thessalonica (east) is the only open one.
ROMA_LABEL = (PIN_XY["Roma"][0] + 14, PIN_XY["Roma"][1] + 22)


def col_map(opacity=1.0):
    """The pale OSM map with its pencil frame, `opacity` in 0..1 (0 draws nothing)."""
    if opacity <= 0:
        return ""
    op = f"opacity={opacity:.3f}," if opacity < 1 else ""
    o = (f"\\node[{op}anchor=south west,inner sep=0pt] at ({MAP_X0:.2f},{MAP_Y0:.2f}) "
         f"{{\\includegraphics[width={MAP_WBP:.2f}bp,height={MAP_HBP:.2f}bp]{{{BASEMAP}}}}};\n")
    x0, y0, x1, y1 = MAP_X0, MAP_Y0, MAP_X0 + MAP_WBP, MAP_Y0 + MAP_HBP
    for p, q in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        o += F.seg(p, q, color="muted", w=2.2, opacity=opacity if opacity < 1 else None)
    return o


def col_pins(size=PIN_D, fill="cool"):
    return "".join(F.disc(*PIN_XY[c], "", fill=fill, size=size) for c in CITIES)


def col_roads(a=0, b=None):
    """Roads a..b of EDGES as straight soft-ink lines between the pins."""
    return "".join(F.seg(PIN_XY[u], PIN_XY[v]) for u, v in EDGES[a:b])


def col_label():
    """"Roma", with a white halo so it reads on the map and is invisible on white paper."""
    x, y = ROMA_LABEL
    o = ""
    for hx in (-2.5, 0, 2.5):
        for hy in (-2.5, 0, 2.5):
            if (hx, hy) != (0, 0):
                o += F.text(x + hx, y + hy, "Roma", color="white", anchor="south west")
    return o + F.text(x, y, "Roma", anchor="south west")


def col_graph(fills=None, hot=()):
    """The finished graph: roads, white discs (or `fills` city -> fill) and the name Roma."""
    fills = fills or {}
    o = col_roads()
    for c in CITIES:
        o += F.disc(*PIN_XY[c], "", fill="hot" if c in hot else fills.get(c, "white"), size=DISC_D)
    return o + col_label()


def col_box():
    """(top, bottom) in bp from the canvas top: the map, every pin and disc, and the padding."""
    top = max(MAP_Y0 + MAP_HBP + 2.5, max(p[1] for p in PIN_XY.values()) + DISC_D / 2 + 2)
    bot = min(MAP_Y0 - 2.5, min(p[1] for p in PIN_XY.values()) - DISC_D / 2 - 2)
    return (COL_H - top - F.PAD, COL_H - bot + F.PAD)

#!/usr/bin/env python3
"""The New York State highway maps of Module 06 (all `col`, 537 bp wide).

Data: `data/ny_network.json` (289 interchanges, 433 road segments, built by `make_ny.py`).
Projection: equirectangular, longitude scaled by cos(42.5 deg).  One scale for every map,
so the seven figures overlay exactly.

Shading.  Every map shades the 289 dots white-ish to accent, and a darker dot is ALWAYS the
more central one:

    degree        1 -> 5 (a small ramp, because there are only four values)
    closeness     min-max of the value
    eccentricity  min-max of 1 / eccentricity  (the smaller the worst-case drive, the darker)
    betweenness   value / maximum
    eigenvector   value / maximum

Eccentricity is the one measure where *smaller* is better. It is shaded by 1/e so that the
slide's rule "darker = more central" holds on every map; the figcaption must say so.

The winner of a measure is a larger accent-2 dot with a white rim. Names go in blank
regions of the map (Lake Ontario, Pennsylvania, New England) with a leader line.
"""

import json
import math

import figlib as F
from figlib import emit, seg, text

ACCENT, ACCENT2, GRAY = "accent", "accenttwo", "annot"

NY = json.loads((F.OUT / "data" / "ny_network.json").read_text())
NODES, EDGES, CITIES = NY["nodes"], NY["edges"], NY["cities"]
N = len(NODES)
assert (N, len(EDGES)) == (289, 433), (N, len(EDGES))
assert all(n["id"] == i for i, n in enumerate(NODES))

# --------------------------------------------------------------------------- projection
SCALE = 72.0                        # bp per degree of latitude
X0, Y0 = 6.0, 30.0                  # lower-left of the state's bounding box on the canvas
CANVAS_H = 400
DY = 22.0                           # Y0 grew from 8 to 30 (room for the 60 km circle); hand-placed names move with the map
_ring_pts = [p for ring in NY["outline"] for p in ring]
LON0, LAT0 = min(p[0] for p in _ring_pts), min(p[1] for p in _ring_pts)
KX = math.cos(math.radians(42.5)) * SCALE


def P(lon, lat):
    return (X0 + (lon - LON0) * KX, Y0 + (lat - LAT0) * SCALE)


XY = [P(n["lon"], n["lat"]) for n in NODES]
MAP_W = max(p[0] for p in XY)
assert max(p[0] for p in map(lambda q: P(*q), _ring_pts)) < F.COL_W - 90

# --------------------------------------------------------------------------- facts
CITY_ID = dict(CITIES)
assert len(CITY_ID) == 8


def argbest(key, sign=1):
    vals = [sign * n[key] for n in NODES]
    best = max(vals)
    ties = [i for i, v in enumerate(vals) if abs(v - best) < 1e-12 * max(1, abs(best))]
    assert len(ties) == 1, f"{key}: tie between {ties}"
    return ties[0]


WIN = {"closeness": argbest("closeness"), "harmonic": argbest("harmonic"),
       "eccentricity": argbest("eccentricity", -1), "betweenness": argbest("betweenness"),
       "eigenvector": argbest("eigenvector")}
EXPECT = {                                  # measure -> (refs, nearest place)
    "closeness": ({"NY 17", "US 209"}, "Middletown"),
    "harmonic": ({"I 95", "HR", "I 295"}, "New York City"),
    "eccentricity": ({"NY 17", "NY 8", "NY 10"}, "Binghamton"),
    "betweenness": ({"NY 17", "NY 52"}, "Monticello"),
    "eigenvector": ({"CI", "I 495"}, "Hempstead"),
}
for m, (refs, near) in EXPECT.items():
    n = NODES[WIN[m]]
    assert set(n["refs"]) == refs and n["near"] == near, f"{m}: winner is {n['refs']} near {n['near']}"
assert round(NODES[WIN["eccentricity"]]["eccentricity"], 1) == 472.7
_btw8 = sorted(CITY_ID, key=lambda c: -NODES[CITY_ID[c]]["betweenness"])
assert _btw8[0] == "Binghamton", _btw8
from collections import Counter                      # noqa: E402
assert Counter(n["degree"] for n in NODES) == {3: 201, 4: 57, 1: 30, 5: 1}

# --------------------------------------------------------------------------- shading
def _norm(vals, lo=None):
    lo = min(vals) if lo is None else lo
    hi = max(vals)
    return [(v - lo) / (hi - lo) for v in vals]


SHADE = {
    "degree": [min(n["degree"], 4) / 4 for n in NODES],
    "closeness": _norm([n["closeness"] for n in NODES]),
    "eccentricity": _norm([1 / n["eccentricity"] for n in NODES]),
    "betweenness": _norm([n["betweenness"] for n in NODES], lo=0.0),
    "eigenvector": _norm([n["eigenvector"] for n in NODES], lo=0.0),
}
# degree: 1 -> 0.25 (lightest), 3 -> 0.75, 4 and 5 -> 1.0
SHADE["degree"] = [{1: 0.0, 3: 0.55, 4: 1.0, 5: 1.0}[n["degree"]] for n in NODES]


def mix(t):
    """White -> accent. The lightest dot is still visible (it carries a rim)."""
    t = 0.16 + 0.84 * max(0.0, min(1.0, t))
    r, g, b = (int(round(255 + (c - 255) * t)) for c in (0x39, 0x59, 0xA6))
    return "{rgb,255:red,%d;green,%d;blue,%d}" % (r, g, b)


# --------------------------------------------------------------------------- drawing
def base(edge_color=f"{GRAY}!45", edge_w=1.7):
    """State outline and the road segments, behind everything."""
    o = ""
    for ring in NY["outline"]:
        pts = [P(*p) for p in ring]
        o += ("\\draw[line width=1.8bp,draw=%s,line join=round] %s -- cycle;\n"
              % (GRAY, " -- ".join("(%.1f,%.1f)" % p for p in pts)))
    for e in EDGES:
        o += seg(XY[e["u"]], XY[e["v"]], color=edge_color, w=edge_w)
    return o


def shaded_dots(shade):
    """All 289 interchanges, light ones first so the dark ones sit on top."""
    o = ""
    for i in sorted(range(N), key=lambda i: shade[i]):
        t = shade[i]
        d = 6.5 + 4.5 * t
        o += ("\\draw[line width=0.8bp,draw=%s!60!black,fill=%s] (%.1f,%.1f) circle (%sbp);\n"
              % (ACCENT, mix(t), XY[i][0], XY[i][1], d / 2))
    return o


def plain_dots(color=f"{GRAY}!55", d=6.0):
    return "".join(F.dot(x, y, color=color, d=d) for x, y in XY)


def winner(i, d=20.0):
    x, y = XY[i]
    return ("\\draw[line width=2.2bp,draw=white,fill=%s] (%.1f,%.1f) circle (%sbp);\n"
            % (ACCENT2, x, y, d / 2))


class Labels:
    """Names in blank regions with leader lines.

    Asserts that labels clear each other, the canvas and the city dots, and that no leader
    crosses another label. Boxes use 0.47 em per character (measured: Latin Modern 36 pt
    "Middletown" is 168 bp, figlib's conservative CHAR_W would say 210).
    """
    CW = 0.47

    def __init__(self, name):
        self.name, self.boxes, self.out, self.leaders, self.lines = name, [], "", "", []
        self.dy = DY

    def box(self, s, x, y, anchor, cw=None):
        w = (cw or self.CW) * F.FONT * len(s) + 8
        h = 0.95 * F.FONT + 2
        ax = {"center": 0.0, "west": 0.5, "east": -0.5}[anchor]
        return (x + ax * w - w / 2, y - h / 2, x + ax * w + w / 2, y + h / 2)

    def add(self, s, x, y, anchor="center", color="black", to=None, r=0.0, lead=None,
            halo=True, avoid=(), cw=None, rel=True):
        if rel:
            y += self.dy
        b = self.box(s, x, y, anchor, cw)
        assert 2 <= b[0] and b[2] <= F.COL_W - 2 and 2 <= b[1] and b[3] <= CANVAS_H - 2, \
            f"{self.name}: label {s!r} runs off the canvas {tuple(round(v) for v in b)}"
        for k, o in self.boxes:
            assert not F.boxes_overlap(b, o), f"{self.name}: labels {s!r} and {k!r} overlap"
        for px, py in avoid:
            assert not F.box_hits_disc(b, px, py, 11), f"{self.name}: label {s!r} covers a city dot"
        self.boxes.append((s, b))
        if to is not None:
            x0, y0, x1, y1 = b
            dx = max(x0 - to[0], 0, to[0] - x1)
            dy = max(y0 - to[1], 0, to[1] - y1)
            if dx > 0 and (dx >= dy or dx >= 8):
                sx, sy = (x0 + 2 if to[0] < x0 else x1 - 2), min(max(to[1], y0 + 8), y1 - 8)
            else:
                sy, sx = (y0 + 2 if to[1] < y0 else y1 - 2), min(max(to[0], x0 + 8), x1 - 8)
            L = math.hypot(to[0] - sx, to[1] - sy)
            ex, ey = to[0] - (to[0] - sx) / L * r, to[1] - (to[1] - sy) / L * r
            self.lines.append((s, (sx, sy), (ex, ey)))
            self.leaders += seg((sx, sy), (ex, ey), color=lead or color, w=2.4)
        if halo:
            for hx in (-2, 0, 2):
                for hy in (-2, 0, 2):
                    if (hx, hy) != (0, 0):
                        self.out += text(x + hx, y + hy, s, color="white", anchor=anchor)
        self.out += text(x, y, s, color=color, anchor=anchor)

    def body(self):
        for s, p, q in self.lines:
            for k, o in self.boxes:
                assert k == s or not F.box_hits_segment(o, p, q, pad=0), \
                    f"{self.name}: the leader of {s!r} crosses the label {k!r}"
        return self.leaders + self.out


# --------------------------------------------------------------------------- the 3x inset
ZOOM = 3.0
INS_W = 156.0                                   # frame, bp
INS_X0, INS_Y0 = 377.0, 150.0                   # lower-left of the inset frame
REG_C = (322.0, 54.0)                           # centre of the NYC area on the map (map bp)
REG_H = INS_W / ZOOM / 2                        # half the side of the region the inset shows
INS_C = (INS_X0 + INS_W / 2, INS_Y0 + INS_W / 2)


def Z(p):
    """Map position -> inset position."""
    return (INS_C[0] + ZOOM * (p[0] - REG_C[0]), INS_C[1] + ZOOM * (p[1] - REG_C[1]))


def inset(dots, winners=()):
    """A framed 3x view of the NYC area (lower right). `dots(order, zoomed_xy)` draws the
    interchanges; `winners` is a list of (node, diameter) drawn on top."""
    fx0, fy0, fx1, fy1 = INS_X0, INS_Y0, INS_X0 + INS_W, INS_Y0 + INS_W
    # the region on the main map
    o = ("\\draw[line width=1.8bp,draw=%s] (%.1f,%.1f) rectangle (%.1f,%.1f);\n"
         % (GRAY, REG_C[0] - REG_H, REG_C[1] - REG_H, REG_C[0] + REG_H, REG_C[1] + REG_H))
    o += "\\begin{scope}\n\\clip (%.1f,%.1f) rectangle (%.1f,%.1f);\n" % (fx0, fy0, fx1, fy1)
    o += "\\fill[white] (%.1f,%.1f) rectangle (%.1f,%.1f);\n" % (fx0, fy0, fx1, fy1)
    for ring in NY["outline"]:
        pts = [Z(P(*p)) for p in ring]
        o += ("\\draw[line width=1.8bp,draw=%s,line join=round] %s -- cycle;\n"
              % (GRAY, " -- ".join("(%.1f,%.1f)" % p for p in pts)))
    for e in EDGES:
        o += seg(Z(XY[e["u"]]), Z(XY[e["v"]]), color=f"{GRAY}!45", w=1.7)
    inside = [i for i in range(N)
              if fx0 - 8 <= Z(XY[i])[0] <= fx1 + 8 and fy0 - 8 <= Z(XY[i])[1] <= fy1 + 8]
    o += dots(inside, {i: Z(XY[i]) for i in inside})
    for i, d in winners:
        x, y = Z(XY[i])
        assert fx0 + d / 2 < x < fx1 - d / 2 and fy0 + d / 2 < y < fy1 - d / 2, f"winner {i} not in the inset"
        o += ("\\draw[line width=2bp,draw=white,fill=%s] (%.1f,%.1f) circle (%sbp);\n"
              % (ACCENT2, x, y, d / 2))
    o += "\\end{scope}\n"
    o += ("\\draw[line width=2bp,draw=%s] (%.1f,%.1f) rectangle (%.1f,%.1f);\n"
          % (GRAY, fx0, fy0, fx1, fy1))
    return o


def _inset_shaded(shade):
    def dots(order, zxy):
        o = ""
        for i in sorted(order, key=lambda i: shade[i]):
            t = shade[i]
            o += ("\\draw[line width=0.8bp,draw=%s!60!black,fill=%s] (%.1f,%.1f) circle (%sbp);\n"
                  % (ACCENT, mix(t), zxy[i][0], zxy[i][1], (6.5 + 4.5 * t) / 2))
        return o
    return dots


def _inset_plain(order, zxy):
    return "".join(F.dot(*zxy[i], color=f"{GRAY}!50", d=6.5) for i in order)


# 60 km around Manhattan, drawn with the map's own projection (1 deg lat = 111.2 km)
MANHATTAN = P(-73.9712, 40.7831)
R60 = (60 / 111.2 * SCALE, 60 / (111.2 * math.cos(math.radians(40.7831))) * KX)   # (y, x) radii, bp


def circle60():
    return ("\\draw[line width=2bp,draw=%s,dash pattern=on 7bp off 5bp] (%.1f,%.1f) ellipse (%.2fbp and %.2fbp);\n"
            % (GRAY, MANHATTAN[0], MANHATTAN[1], R60[1], R60[0]))


def _city(c):
    return XY[CITY_ID[c]]


def _finish(name, body):
    emit(name, body, container="col", h=CANVAS_H, nodes=False)


# --------------------------------------------------------------------------- the figures
def fig_overview():
    L = Labels("ny-overview")
    b = base() + plain_dots()
    for c in CITY_ID:
        x, y = _city(c)
        b += ("\\draw[line width=2bp,draw=white,fill=%s] (%.1f,%.1f) circle (9bp);\n" % (ACCENT, x, y))
    dots = [_city(c) for c in CITY_ID]
    spec = {                                  # name: (anchor, x, y); leader only if far
        "Watertown": ("east", _city("Watertown")[0] - 6, _city("Watertown")[1] + 44 - DY, True),
        "Buffalo": ("center", 66, 146, True),
        "Rochester": ("center", 110, 250, True),
        "Syracuse": ("center", 232, 157, True),
        "Utica": ("west", 262, 214, False),
        "Albany": ("west", 346, 166, False),
        "Binghamton": ("center", 130, 70, True),
        "NYC": ("center", 398, 100, True),
    }
    for c, (anc, x, y, lead) in spec.items():
        key = "New York City" if c == "NYC" else c
        L.add(c, x, y, anchor=anc, to=_city(key) if lead else None, r=11, avoid=dots)
    _finish("ny-overview", b + L.body())


def fig_degree():
    b = base() + shaded_dots(SHADE["degree"])
    L = Labels("ny-degree")
    # a legend instead of names: the degrees that matter, drawn with the figure's own dots
    rows = [("degree 4+", 1.0), ("degree 3", 0.55), ("degree 1", 0.0)]
    for k, (s, t) in enumerate(rows):
        y = 300 - k * 50
        b += ("\\draw[line width=0.8bp,draw=%s!60!black,fill=%s] (360,%d) circle (6.5bp);\n"
              % (ACCENT, mix(t), y))
        L.add(s, 374, y, anchor="west", halo=False, cw=0.43, rel=False)
    _finish("ny-degree", b + L.body())


def _single(name, measure, labels):
    L = Labels(name)
    i = WIN[measure]
    b = base() + shaded_dots(SHADE[measure]) + winner(i)
    labels(L, i)
    _finish(name, b + L.body())


def fig_closeness():
    def lab(L, i):
        L.add("Middletown", 112, 46, color=ACCENT2, to=XY[i], r=12)
        L.add("NYC", 400, 100, to=_city("New York City"), r=3)
    _single("ny-closeness", "closeness", lab)


def fig_eccentricity():
    def lab(L, i):
        L.add("Binghamton", 115, 80, to=_city("Binghamton"), r=3)
        L.add("473 km", 215, 32, color=ACCENT2, to=XY[i], r=12)
    _single("ny-eccentricity", "eccentricity", lab)


def fig_betweenness():
    def lab(L, i):
        L.add("Binghamton", 115, 80, to=_city("Binghamton"), r=3)
        L.add("Monticello", 190, 32, color=ACCENT2, to=XY[i], r=12)
    _single("ny-betweenness", "betweenness", lab)


def fig_eigenvector():
    L = Labels("ny-eigenvector")
    i = WIN["eigenvector"]
    b = base() + circle60() + shaded_dots(SHADE["eigenvector"]) + winner(i)
    b += inset(_inset_shaded(SHADE["eigenvector"]), [(i, 20.0)])
    # "60 km" at the circle's south-west, in the blank below Pennsylvania
    ang = math.radians(225)
    L.add("60 km", MANHATTAN[0] + R60[1] * math.cos(ang) - 14, MANHATTAN[1] + R60[0] * math.sin(ang) + 3,
          anchor="east", color=GRAY, rel=False)
    zx, zy = Z(XY[i])
    L.add("Hempstead", 533, INS_Y0 - 28, anchor="east", color=ACCENT2, to=(zx, zy), r=12, cw=0.42, rel=False)
    _finish("ny-eigenvector", b + L.body())


def fig_five():
    L = Labels("ny-five")
    b = base() + plain_dots(color=f"{GRAY}!50", d=6.5)
    for m in ("eccentricity", "betweenness", "closeness", "eigenvector", "harmonic"):
        b += winner(WIN[m], d=13.0)
    b += inset(_inset_plain, [(WIN["harmonic"], 11.0), (WIN["eigenvector"], 11.0)])
    spec = {                                   # measure: (x, y), map-relative
        "eccentricity": (113, 84),
        "betweenness": (120, 38),
        "closeness": (205, 0),
    }
    for m, (x, y) in spec.items():
        L.add(m, x, y, anchor="center", color=ACCENT2, to=XY[WIN[m]], r=8)
    # the two winners that sit in the NYC inset: harmonic above the frame, eigenvector below it
    zh, ze = Z(XY[WIN["harmonic"]]), Z(XY[WIN["eigenvector"]])
    L.add("harmonic", 533, INS_Y0 + INS_W + 28, anchor="east", color=ACCENT2, to=zh, r=10, cw=0.42, rel=False)
    L.add("eigenvector", 533, INS_Y0 - 28, anchor="east", color=ACCENT2, to=ze, r=10, cw=0.42, rel=False)
    _finish("ny-five", b + L.body())


FIGURES = [("ny-overview", fig_overview), ("ny-degree", fig_degree),
           ("ny-closeness", fig_closeness), ("ny-eccentricity", fig_eccentricity),
           ("ny-betweenness", fig_betweenness), ("ny-eigenvector", fig_eigenvector),
           ("ny-five", fig_five)]

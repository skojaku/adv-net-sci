#!/usr/bin/env python3
"""The opening of Module 06: a real map of the twelve cities, then the same twelve
cities as a graph.

    roma-basemap      (col)   the OpenStreetMap tile map with a pin on each city
    roma-to-graph.gif (full)  the map fades, the roads are drawn straight between the pins,
                              and the pins slide to the Roman graph's positions

The last frame of the GIF is `romelib.map_body()`, i.e. the picture `roma-graph.png` shows,
and the position the pins slide to is asserted to be `romelib.NODE_XY`.

The basemap is a PNG from `make_basemap.py`, placed with `\\includegraphics` inside the TikZ
body. The pale PNG is nearly white, so figlib's "ink" test (luminance < 200) does not see
it: every figure here carries ink (a thin frame, pins) that spans the picture, so the crop
and the ink-width gate act on the map and not on the pins alone.
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image

import figlib as F
import romelib as R
from figlib import emit, emit_gif, text

GRAY = "annot"     # the TikZ colour name (figlib.GRAY is the hex string)

DATA = F.OUT / "data"
BASEMAP = DATA / "roma-basemap-pale.png"
BASEJSON = DATA / "roma-basemap.json"

_meta = json.loads(BASEJSON.read_text())
PX = {c: (v["px"], v["py"]) for c, v in _meta["cities"].items()}
IMG_W, IMG_H = _meta["image"]["width"], _meta["image"]["height"]
assert set(PX) == set(R.CITIES), f"basemap cities differ from romelib: {set(PX) ^ set(R.CITIES)}"
assert (Image.open(BASEMAP).size) == (IMG_W, IMG_H)

PIN = 14            # bp, accent-2 pins on the map (spec)
FRAME_W = 2.6

# The region of the 2000 x 1826 PNG that is shown. Rows 62..1795 keep every pin (rows 107 to
# 1749) with a margin; all 2000 columns are kept so the map is wide enough for the ink gate.
CROP = (0, 62, IMG_W, 1795)           # the still
CROP_GIF = (0, 30, IMG_W, 1820)       # the GIF map is shorter, so it needs more margin in px


def _cropped(crop):
    """The cropped basemap as a file; PIL once, cached on disk next to the source."""
    out = DATA / ("roma-basemap-pale-crop-%d-%d.png" % (crop[1], crop[3]))
    src_m = BASEMAP.stat().st_mtime
    if not out.exists() or out.stat().st_mtime < src_m:
        Image.open(BASEMAP).crop(crop).save(out)
    return out


def _inc(path, x, y, w, opacity=1.0):
    """The image with its lower-left corner at (x, y) and width w bp."""
    op = f"opacity={opacity:.3f}," if opacity < 1 else ""
    return (f"\\node[{op}anchor=south west,inner sep=0pt] at ({x:.2f},{y:.2f}) "
            f"{{\\includegraphics[width={w:.2f}bp]{{{path}}}}};\n")


class MapGeom:
    """Where the image and each city sit when the cropped map is `h` bp tall."""

    def __init__(self, h, x0, y0, crop=CROP):
        self.crop = crop
        cw, ch = crop[2] - crop[0], crop[3] - crop[1]
        self.s = h / ch
        self.w, self.h, self.x0, self.y0 = cw * self.s, h, x0, y0
        self.pin = {c: (x0 + (px - crop[0]) * self.s, y0 + (crop[3] - py) * self.s)
                    for c, (px, py) in PX.items()}
        for c, (x, y) in self.pin.items():
            assert x0 + 9 < x < x0 + self.w - 9 and y0 + 9 < y < y0 + h - 9, \
                f"{c}: its pin is within 9 bp of the map edge"

    def image(self, opacity=1.0):
        return _inc(_cropped(self.crop), self.x0, self.y0, self.w, opacity)

    def frame(self):
        return (f"\\draw[line width={FRAME_W}bp,draw={GRAY}] ({self.x0:.2f},{self.y0:.2f}) "
                f"rectangle ({self.x0 + self.w:.2f},{self.y0 + self.h:.2f});\n")


def _pin(x, y, d=PIN):
    return (f"\\draw[line width=1.6bp,draw=white,fill=accenttwo] ({x:.2f},{y:.2f}) "
            f"circle ({d / 2}bp);\n")


# --------------------------------------------------------------------------- the still
def fig_basemap():
    """The real map, one pin per city, only "Roma" named (the credit is in the caption)."""
    # 353 bp is just under the ink budget of a plain figure (380 - 2 * 12 crop padding). 409 bp wide at
    # that height is 76.2% of the 537 bp column, just over the 76% ink gate.
    h = 353.0
    g = MapGeom(h, x0=(F.COL_W - (CROP[2] - CROP[0]) * h / (CROP[3] - CROP[1])) / 2, y0=30.0)
    b = g.image() + g.frame()
    for c in R.CITIES:
        b += _pin(*g.pin[c])
    # "Roma" sits to the west of its pin, in the Tyrrhenian Sea, with a white halo.
    x, y = g.pin["Roma"]
    for dx in (-2, 0, 2):
        for dy in (-2, 0, 2):
            if (dx, dy) != (0, 0):
                b += text(x - 14 + dx, y + dy, "Roma", color="white", anchor="east")
    b += text(x - 14, y, "Roma", color="black", anchor="east")
    # Roma's name must stay on the map.
    assert x - 14 - 0.55 * F.FONT * 4 > g.x0, "the label Roma runs off the map"
    emit("roma-basemap", b, container="col", h=460)


# --------------------------------------------------------------------------- the GIF
def _ink_rows():
    """Rows (bp from the bottom of the canvas) of ink in the final frame."""
    im = F.render(R.map_body(), F.FULL_W, CANVAS_H)
    a = np.array(im.convert("L"))
    ys, xs = np.where(a < 200)
    return (CANVAS_H * F.PXBP - ys.max()) / F.PXBP, (CANVAS_H * F.PXBP - ys.min()) / F.PXBP


CANVAS_H = 470


def fig_to_graph():
    lo, hi = _ink_rows()
    h_map = hi - lo                       # the map is as tall as the finished graph's ink
    g = MapGeom(h_map, x0=6.0, y0=lo, crop=CROP_GIF)
    # In frame 0 the pins are at the map's cities; the last frame's discs are at NODE_XY.
    start = g.pin
    end = {c: R.NODE_XY[c] for c in R.CITIES}

    def at(t):
        return {c: (start[c][0] + t * (end[c][0] - start[c][0]),
                    start[c][1] + t * (end[c][1] - start[c][1])) for c in R.CITIES}

    assert all(abs(at(1.0)[c][0] - R.NODE_XY[c][0]) < 1e-9
               and abs(at(1.0)[c][1] - R.NODE_XY[c][1]) < 1e-9 for c in R.CITIES), \
        "the pins do not end on romelib.NODE_XY"
    R.assert_same_geometry("roma-to-graph final", at(1.0))

    def roads(pos, upto=None):
        o = ""
        for a, b in R.EDGES[:upto]:
            o += F.seg(pos[a], pos[b], color="black", w=F.EDGE_W)
        return o

    def dots(pos, t):
        """Pins turn from accent-2 into accent as they grow from 14 bp to 40 bp discs."""
        d = PIN + (F.NODE - PIN) * t
        mix = int(round(100 * (1 - t)))
        fill = "accent" if mix == 0 else f"accenttwo!{mix}!accent"
        o = ""
        for c in R.CITIES:
            x, y = pos[c]
            o += (f"\\draw[line width=1.6bp,draw={'white' if t == 0 else 'black'},fill={fill}] "
                  f"({x:.2f},{y:.2f}) circle ({d / 2}bp);\n")
        return o

    frames, dur = [], []

    def add(body, ms):
        frames.append(body)
        dur.append(ms)

    add(g.image() + g.frame() + dots(start, 0), 1800)                       # the map, with pins
    for op in (0.66, 0.33, 0.0):                                             # the map fades
        add((g.image(op) if op else "") + (g.frame() if op else "") + dots(start, 0), 450)
    half = len(R.EDGES) // 2
    add(roads(start, half) + dots(start, 0), 500)                           # roads, first half
    add(roads(start) + dots(start, 0), 900)                                 # roads, all
    for k in range(1, 7):                                                    # the pins slide
        t = k / 6
        pos = at(t)
        add(roads(pos) + dots(pos, t), 400)
    add(R.map_body(), 1600)                                                 # + names = roma-graph
    emit_gif("roma-to-graph", frames, container="full", h=CANVAS_H, hmod="tall",
             durations=dur, hold=3)


FIGURES = [("roma-basemap", fig_basemap), ("roma-to-graph", fig_to_graph)]

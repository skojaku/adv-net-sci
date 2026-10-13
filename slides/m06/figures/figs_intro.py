#!/usr/bin/env python3
"""The opening of Module 06: a real map of the twelve cities, then the same twelve cities
as a graph (all `col`, 537 bp wide, one canvas and one crop).

    roma-basemap     (col)         the OpenStreetMap map with a pin on each city, "Roma" named
    roma-to-graph    (col, frames) frame 0 = roma-basemap; the map fades in three steps, the
                                   roads are drawn five, six and seven at a time between the
                                   pins, the pins grow into white discs where they stand; the
                                   last frame is the network on white paper, only "Roma" named
    roma-degree      (figs_rome)   the last frame plus degree shading (built from romelib)

The geometry (pins at their real map positions, 10% sideways stretch, canvas, crop box) is in
`romelib` (section "col layout"). Frame 0 is built from the same function as roma-basemap, so
the two are pixel-identical.
"""

import figlib as F
import romelib as R


def _basemap_body():
    return R.col_map(1.0) + R.col_pins() + R.col_label()


def fig_basemap():
    F.emit("roma-basemap", _basemap_body(), container="col", h=R.COL_H, hmod=R.COL_MOD,
           box=R.col_box())


def fig_to_graph():
    n = len(R.EDGES)
    assert n == 18
    frames = [_basemap_body()]                                   # 0: the map (= roma-basemap)
    for op in (0.62, 0.30, 0.0):                                 # 1-3: the map fades
        frames.append(R.col_map(op) + R.col_pins() + R.col_label())
    for a, b in ((0, 5), (5, 11), (11, n)):                      # 4-6: the roads
        frames.append(R.col_roads(0, b) + R.col_pins() + R.col_label())
    frames.append(R.col_roads() + R.col_pins(size=26, fill="cool!45!white") + R.col_label())  # 7
    frames.append(R.col_graph())                                 # 8: the graph
    F.emit_frames("roma-to-graph", frames, container="col", h=R.COL_H, hmod=R.COL_MOD,
                  box=R.col_box())


FIGURES = [("roma-basemap", fig_basemap), ("roma-to-graph", fig_to_graph)]

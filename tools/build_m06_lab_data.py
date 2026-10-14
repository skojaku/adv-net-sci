#!/usr/bin/env python3
"""Pack the Module 6 lab's road map into lab.py.

    uv run --with pillow --with scipy python tools/build_m06_lab_data.py

The lab is uploaded to molab as one file and has to open on bad wifi, so the
map travels inside it, the way the stylesheet does (see LAB_NOTEBOOK_GUIDE.md).
This script is the only place it comes from:

  * the Roman road network (data/roman-roads: Harvard Dataverse, Roman Road
    Network, version 2008). Its 4,529 points are road junctions and waypoints,
    not cities: 390 of them lie within 30 km of Rome. So points that lie
    within MERGE_KM of each other (complete linkage, so no two points in a
    place are further apart than that) are merged into one place at their
    centroid, and two places are joined when any road runs between them. At
    150 km that leaves about 300 places, a size a student can read on a map.
    The cut-off is a round number chosen for the size, not for any result.
  * the terrain behind it, from OpenTopoMap (CC-BY-SA; map data (c)
    OpenStreetMap contributors, SRTM). A few dozen tiles are fetched once,
    here, stitched into one picture, washed out so that the network stays the
    loudest thing on the page, and stored as a JPEG. The lab never contacts a
    tile server.

The result is written over the one line of lab.py that ends in
`# BUILT-DATA`. Run it again to change the map; commit the result.
"""

from __future__ import annotations

import base64
import csv
import io
import json
import math
import pathlib
import re
import sys
import time
import urllib.request
import zlib

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage

from PIL import Image, ImageEnhance, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAB = ROOT / "lecture-note" / "m06-centrality" / "pen-and-paper" / "lab.py"
DATA = ROOT / "data" / "roman-roads"
DATA_LINE = re.compile(r'^(\s*ROMAN_DATA_B64 = )".*"(  # BUILT-DATA)$', re.MULTILINE)

MERGE_KM = 150
ZOOM = 5
TILE = 256
TILE_URL = "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
# OpenTopoMap asks for a descriptive agent and no bulk fetching; this is ~25 tiles.
AGENT = "adv-net-sci-course-lab/1.0 (skojaku@binghamton.edu)"
MARGIN_DEG = 1.0


def world_px(lon: float, lat: float, zoom: int = ZOOM) -> tuple[float, float]:
    """Web Mercator: the pixel of the whole-world picture at this zoom."""
    size = TILE * 2**zoom
    x = (lon + 180.0) / 360.0 * size
    s = math.sin(math.radians(lat))
    y = (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * size
    return x, y


def fetch_tile(x: int, y: int) -> Image.Image:
    url = TILE_URL.format(s="abc"[(x + y) % 3], z=ZOOM, x=x, y=y)
    req = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        return Image.open(io.BytesIO(r.read())).convert("RGB")


def wash(img: Image.Image) -> Image.Image:
    """Keep the relief and the coastline, lose the loudness: the roads are the
    point, and a green-and-brown topographic map would shout over them."""
    grey = ImageOps.autocontrast(img.convert("L"), cutoff=1)
    warm = ImageOps.colorize(grey, black=(104, 98, 88), white=(255, 253, 247))
    mixed = Image.blend(warm, img, 0.22)  # a little of the sea's blue survives
    mixed = ImageEnhance.Brightness(mixed).enhance(1.06)
    return Image.blend(mixed, Image.new("RGB", mixed.size, (255, 253, 247)), 0.38)


def main() -> int:
    with open(DATA / "node_table.csv", newline="") as f:
        nodes = [(float(r["lon"]), float(r["lat"])) for r in csv.DictReader(f)]
    with open(DATA / "edge_table.csv", newline="") as f:
        edges = [(int(r["src"]), int(r["trg"])) for r in csv.DictReader(f)]
    assert [i for i, _ in enumerate(nodes)] == list(range(len(nodes)))
    rome_point = 0  # the dataset's junction at Rome (12.506 E, 41.875 N)

    # Merge nearby points into places.
    pts = np.array(nodes)
    km = np.c_[pts[:, 0] * np.cos(np.radians(pts[:, 1])) * 111.0, pts[:, 1] * 111.0]
    label = fcluster(linkage(km, "complete"), MERGE_KM, "distance") - 1
    k = int(label.max()) + 1
    places = [tuple(pts[label == c].mean(axis=0)) for c in range(k)]
    links = sorted(
        {tuple(sorted((int(label[a]), int(label[b])))) for a, b in edges if label[a] != label[b]}
    )
    rome = int(label[rome_point])
    print(f"{len(nodes)} points -> {k} places, {len(links)} links")
    nodes, edges = places, links

    lons, lats = [p[0] for p in nodes], [p[1] for p in nodes]
    x0, y1 = world_px(min(lons) - MARGIN_DEG, min(lats) - MARGIN_DEG)
    x1, y0 = world_px(max(lons) + MARGIN_DEG, max(lats) + MARGIN_DEG)
    x0, y0, x1, y1 = int(x0), int(y0), math.ceil(x1), math.ceil(y1)
    tx0, tx1, ty0, ty1 = x0 // TILE, x1 // TILE, y0 // TILE, y1 // TILE
    print(f"crop {x1 - x0} x {y1 - y0} px, {(tx1 - tx0 + 1) * (ty1 - ty0 + 1)} tiles")

    mosaic = Image.new("RGB", ((tx1 - tx0 + 1) * TILE, (ty1 - ty0 + 1) * TILE))
    for ty in range(ty0, ty1 + 1):
        for tx in range(tx0, tx1 + 1):
            mosaic.paste(fetch_tile(tx, ty), ((tx - tx0) * TILE, (ty - ty0) * TILE))
            time.sleep(0.4)
    crop = mosaic.crop((x0 - tx0 * TILE, y0 - ty0 * TILE, x1 - tx0 * TILE, y1 - ty0 * TILE))
    out = io.BytesIO()
    wash(crop).save(out, "JPEG", quality=72, optimize=True)
    print(f"terrain jpeg {len(out.getvalue()) / 1024:.0f} KB")

    blob = {
        "nodes": [round(v * 1000) for p in nodes for v in p],  # lon, lat, lon, lat...
        "edges": [v for e in edges for v in e],
        "rome": rome,
        "merge_km": MERGE_KM,
        "terrain": {
            "jpeg": base64.b64encode(out.getvalue()).decode("ascii"),
            "zoom": ZOOM,
            "x0": x0,
            "y0": y0,
            "w": x1 - x0,
            "h": y1 - y0,
        },
    }
    packed = base64.b64encode(
        zlib.compress(json.dumps(blob, separators=(",", ":")).encode(), 9)
    ).decode("ascii")
    text = LAB.read_text(encoding="utf-8")
    new, n = DATA_LINE.subn(lambda m: f'{m.group(1)}"{packed}"{m.group(2)}', text)
    if n != 1:
        print(f"{LAB}: {n} lines end in '# BUILT-DATA', expected 1", file=sys.stderr)
        return 1
    LAB.write_text(new, encoding="utf-8")
    print(f"wrote {len(packed) / 1024:.0f} KB into {LAB.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

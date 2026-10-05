#!/usr/bin/env python3
"""Pack the Module 5 lab's data into lab.py.

    python tools/build_m05_lab_data.py

The lab is uploaded to molab as one file and has to open on bad wifi, so its
three data sets travel inside it, the way the stylesheet does (see
LAB_NOTEBOOK_GUIDE.md). This script is the only place they come from:

  * the US airport network, from OpenFlights (jpatokal/openflights, Open
    Database License). Two airports are joined when at least one scheduled
    route runs between them in either direction. Only the largest connected
    piece is kept, so every airport can be reached from every other.
  * the US airline x airport network, from the same routes: an airline is
    joined to every US airport it flies to. Airlines are the US-registered
    ones, and codeshare rows (a ticket sold by one airline on another's plane)
    are dropped, because the plane is not the seller's.
  * the outlines of the US states, from Natural Earth (public domain), for the
    map behind the dots.
  * the college football network (Girvan and Newman, 2002), from Netzschleuder:
    115 teams, an edge for every game in the Fall 2000 regular season, and the
    conference each team played in. Teams are sorted by name for the same
    reason the airports are sorted by code.

Everything is rounded hard (airports to 0.01 degree, outlines to 0.1) and
compressed: the whole blob is about 25 KB. Airports are sorted by their
three-letter code, so the order a student sees in the matrix before any
fitting is alphabetical and has nothing to do with the blocks.

The result is written over the one line of lab.py that ends in
`# BUILT-DATA`. Run it again to change the data; commit the result.
"""

from __future__ import annotations

import base64
import csv
import io
import json
import pathlib
import re
import sys
import urllib.request
import zipfile
import zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAB = ROOT / "lecture-note" / "m05-clustering" / "pen-and-paper" / "lab.py"
DATA_LINE = re.compile(r'^(\s*LAB_DATA_B64 = )".*"(  # BUILT-DATA)$', re.MULTILINE)

OPENFLIGHTS = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/{}.dat"
NATURAL_EARTH = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/"
    "geojson/ne_110m_admin_1_states_provinces.geojson"
)
FOOTBALL = "https://networks.skewed.de/net/football/files/football.csv.zip"


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def components(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Union-find; returns the member list of the biggest piece."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        parent[find(a)] = find(b)
    groups: dict[int, list[int]] = {}
    for x in range(n):
        groups.setdefault(find(x), []).append(x)
    return max(groups.values(), key=len)


def read_openflights() -> tuple[dict, dict, list]:
    airports = {}
    for r in csv.reader(fetch(OPENFLIGHTS.format("airports")).decode("utf-8").splitlines()):
        if r[3] != "United States" or r[4] in ("", "\\N"):
            continue
        lon = float(r[7])
        if lon > 0:  # the western Aleutians sit past 180 degrees
            lon -= 360
        airports[r[0]] = dict(iata=r[4], city=r[2], lat=float(r[6]), lon=lon)

    airlines = {}
    for r in csv.reader(fetch(OPENFLIGHTS.format("airlines")).decode("utf-8").splitlines()):
        if r[6] == "United States":
            airlines[r[0]] = r[1]

    routes = list(csv.reader(fetch(OPENFLIGHTS.format("routes")).decode("utf-8").splitlines()))
    return airports, airlines, routes


def airport_row(a: dict) -> list:
    return [a["iata"], a["city"], round(a["lat"], 2), round(a["lon"], 2)]


def build() -> dict:
    airports, airlines, routes = read_openflights()

    # --- airport x airport ---------------------------------------------------
    pairs = set()
    for r in routes:
        s, d = r[3], r[5]
        if s in airports and d in airports and s != d:
            pairs.add(tuple(sorted((airports[s]["iata"], airports[d]["iata"]))))
    codes = sorted({c for p in pairs for c in p})
    index = {c: i for i, c in enumerate(codes)}
    edges = [(index[a], index[b]) for a, b in pairs]
    keep = components(len(codes), edges)
    keep_set = set(keep)
    codes = [codes[i] for i in sorted(keep_set)]
    index = {c: i for i, c in enumerate(codes)}
    edges = sorted(
        (index[a], index[b]) for a, b in pairs if a in index and b in index
    )
    by_iata = {a["iata"]: a for a in airports.values()}
    net = dict(
        airports=[airport_row(by_iata[c]) for c in codes],
        edges=[list(e) for e in edges],
    )

    # --- airline x airport ---------------------------------------------------
    links = set()
    for r in routes:
        if r[6] == "Y" or r[1] not in airlines:
            continue
        s, d = r[3], r[5]
        if s in airports and d in airports and s != d:
            links.add((r[1], airports[s]["iata"]))
            links.add((r[1], airports[d]["iata"]))
    names = sorted({airlines[a] for a, _ in links})
    bcodes = sorted({c for _, c in links})
    name_ix = {n: i for i, n in enumerate(names)}
    code_ix = {c: i for i, c in enumerate(bcodes)}
    bip = dict(
        airlines=names,
        bairports=[airport_row(by_iata[c]) for c in bcodes],
        bedges=sorted([name_ix[airlines[a]], code_ix[c]] for a, c in links),
    )

    # --- outlines ------------------------------------------------------------
    rings = []
    for f in json.loads(fetch(NATURAL_EARTH))["features"]:
        if f["properties"].get("admin") != "United States of America":
            continue
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            ring = []
            for lon, lat in poly[0]:
                pt = [round(lon, 1), round(lat, 1)]
                if not ring or ring[-1] != pt:
                    ring.append(pt)
            if len(ring) > 3:
                rings.append(ring)

    return {**net, **bip, "states": rings}


def football() -> dict:
    """Teams by name, with the conference each one played in."""
    z = zipfile.ZipFile(io.BytesIO(fetch(FOOTBALL)))
    rows = [
        r
        for r in csv.reader(io.StringIO(z.read("nodes.csv").decode("utf-8")))
        if r and not r[0].startswith("#")
    ]
    # "FloridaState" -> "Florida State"; "TexasA&M" -> "Texas A&M"
    label = {int(r[0]): re.sub(r"(?<=[a-z])(?=[A-Z])", " ", r[1]) for r in rows}
    conf = {int(r[0]): int(r[2]) for r in rows}
    order = sorted(label, key=lambda i: label[i])
    index = {old: new for new, old in enumerate(order)}
    edges = []
    for r in csv.reader(io.StringIO(z.read("edges.csv").decode("utf-8"))):
        if r and not r[0].startswith("#"):
            a, b = index[int(r[0])], index[int(r[1])]
            edges.append([min(a, b), max(a, b)])
    return dict(
        fnames=[label[i] for i in order],
        fconf=[conf[i] for i in order],
        fedges=sorted(edges),
    )


def main() -> int:
    data = {**build(), **football()}
    blob = base64.b64encode(
        zlib.compress(json.dumps(data, separators=(",", ":")).encode("utf-8"), 9)
    ).decode("ascii")

    print(
        f"{len(data['airports'])} airports, {len(data['edges'])} routes; "
        f"{len(data['airlines'])} airlines x {len(data['bairports'])} airports, "
        f"{len(data['bedges'])} links; {len(data['states'])} outline rings; "
        f"{len(data['fnames'])} teams, {len(data['fedges'])} games; "
        f"{len(blob)} chars"
    )
    if not LAB.exists():
        print(f"{LAB} does not exist yet", file=sys.stderr)
        return 1
    before = LAB.read_text(encoding="utf-8")
    after, n = DATA_LINE.subn(lambda m: f'{m.group(1)}"{blob}"{m.group(2)}', before)
    if n != 1:
        print(f"{LAB}: {n} lines end in '# BUILT-DATA', expected 1", file=sys.stderr)
        return 1
    LAB.write_text(after, encoding="utf-8")
    print(f"wrote the data into {LAB.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

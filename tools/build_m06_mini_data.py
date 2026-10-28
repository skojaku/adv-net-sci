# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["numpy", "pandas", "pyshp", "shapely"]
# ///
"""Rebuild the data block of notebooks/m06-centrality/mini-project.py.

The notebook travels to molab as one file and fetches nothing at run time, so
the hospitals, their catchment populations, the two referral networks and the
two capacity vectors are written into it as literals between the markers

    # BUILT-DATA-BEGIN
    # BUILT-DATA-END

Sources (both public, no key):
  hospitals   NYS Department of Health, Health Facility General Information
              (health.data.ny.gov/resource/vn5v-hh5r), facility type HOSP, the
              five NYC counties
  population  2020 Census, centers of population by tract
              (www2.census.gov/geo/docs/reference/cenpop2020/tract)
  map         2020 Census cartographic boundaries, county subdivisions of New
              York State, clipped to the shoreline; the five boroughs, simplified

Everything else -- who refers to whom, how many beds -- is a simulation
assumption, drawn here with fixed seeds and then frozen into the notebook.

    uv run tools/build_m06_mini_data.py
"""

import io
import json
import zipfile
import re
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import shapefile
from shapely.geometry import shape

NOTEBOOK = Path(__file__).resolve().parent.parent / "notebooks/m06-centrality/mini-project.py"
COUNTIES = ["New York", "Kings", "Queens", "Bronx", "Richmond"]
COUNTY_FIPS = [5, 47, 61, 81, 85]
TIGHT = 1.08  # total capacity / total people
SIGMA = 0.45  # spread of capacity around "proportional to the catchment"
SCENARIOS = {"A": (1, 11), "B": (3, 13)}  # (referral-network seed, capacity seed)


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def hospitals():
    q = urllib.parse.urlencode(
        {
            "$where": "fac_desc_short='HOSP' AND county in("
            + ",".join(f"'{c}'" for c in COUNTIES)
            + ")",
            "$limit": 500,
        }
    )
    rows = json.loads(get(f"https://health.data.ny.gov/resource/vn5v-hh5r.json?{q}"))
    seen, out = set(), []
    for r in rows:
        if "latitude" not in r:
            continue
        key = (round(float(r["latitude"]), 3), round(float(r["longitude"]), 3))
        if key in seen:  # the same building listed twice
            continue
        seen.add(key)
        out.append((r["facility_name"].strip(), float(r["latitude"]), float(r["longitude"]), r["county"]))
    names = [o[0] for o in out]
    return [
        (n if names.count(n) == 1 else f"{n} ({c})", la, lo)
        for n, la, lo, c in out
    ]


def tracts():
    t = pd.read_csv(
        io.BytesIO(get("https://www2.census.gov/geo/docs/reference/cenpop2020/tract/CenPop2020_Mean_TR36.txt")),
        encoding="utf-8-sig",
    )
    t = t[t.COUNTYFP.isin(COUNTY_FIPS)]
    return t[["LATITUDE", "LONGITUDE"]].values.astype(float), t.POPULATION.values


def basemap(tol=0.0005):
    """The five boroughs as outlines (lon, lat) and one label point each."""
    z = zipfile.ZipFile(io.BytesIO(get("https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_36_cousub_500k.zip")))
    stem = next(n for n in z.namelist() if n.endswith(".shp"))[:-4]
    r = shapefile.Reader(
        shp=io.BytesIO(z.read(stem + ".shp")),
        shx=io.BytesIO(z.read(stem + ".shx")),
        dbf=io.BytesIO(z.read(stem + ".dbf")),
    )
    rings, labels = [], []
    for sr in r.iterShapeRecords():
        rec = sr.record.as_dict()
        if f"{int(rec['COUNTYFP']):03d}" not in [f"{c:03d}" for c in COUNTY_FIPS]:
            continue
        poly = shape(sr.shape.__geo_interface__).simplify(tol)
        parts = list(poly.geoms) if poly.geom_type == "MultiPolygon" else [poly]
        for part in parts:
            if part.area > 2e-5:  # drop specks
                rings.append([(round(x, 4), round(y, 4)) for x, y in part.exterior.coords])
        biggest = max(parts, key=lambda p: p.area)
        c = biggest.representative_point()
        labels.append((rec["NAME"], round(c.x, 4), round(c.y, 4)))
    return rings, labels


def km(a, b):
    la = np.radians((a[:, None, 0] + b[None, :, 0]) / 2)
    dx = (a[:, None, 1] - b[None, :, 1]) * 111.32 * np.cos(la)
    dy = (a[:, None, 0] - b[None, :, 0]) * 110.57
    return np.hypot(dx, dy)


def main():
    H = hospitals()
    hl = np.array([[h[1], h[2]] for h in H])
    tl, tp = tracts()
    n = len(H)
    near = km(tl, hl).argmin(1)
    pop = np.bincount(near, weights=tp, minlength=n).round(-2).astype(int)
    HH = km(hl, hl)

    def network(seed):
        rng = np.random.default_rng(seed)
        E = set()
        w = pop / pop.sum()
        for i in range(n):
            for j in np.argsort(HH[i])[1:3]:
                E.add((i, int(j)))  # the two nearest
            p = w.copy()
            p[i] = 0
            E.add((i, int(rng.choice(n, p=p / p.sum()))))  # one far, big hospitals preferred
        order = rng.permutation(n)
        for a, b in zip(order, np.roll(order, -1)):
            E.add((int(a), int(b)))  # a loop through everyone, so the network is strongly connected
        return sorted(E)

    def capacity(seed):
        c = pop * np.random.default_rng(seed).lognormal(0, SIGMA, n)
        return (c * TIGHT * pop.sum() / c.sum()).round(-2).astype(int).tolist()

    block = ["# BUILT-DATA-BEGIN"]
    block.append("HOSPITALS = [")
    for (name, la, lo), p in zip(H, pop):
        block.append(f"    ({name!r}, {la:.4f}, {lo:.4f}, {int(p)}),")
    block.append("]")
    block.append("EDGES = {")
    for k, (ns, _) in SCENARIOS.items():
        block.append(f"    {k!r}: {network(ns)!r},")
    block.append("}")
    block.append("CAPACITY = {")
    for k, (_, cs) in SCENARIOS.items():
        block.append(f"    {k!r}: {capacity(cs)!r},")
    block.append("}")
    rings, labels = basemap()
    block.append(f"BASEMAP = {rings!r}")
    block.append(f"BOROUGHS = {labels!r}")
    block.append("# BUILT-DATA-END")
    new = "\n    ".join(block)  # the markers sit inside the notebook's `with app.setup` block

    text = NOTEBOOK.read_text()
    text = re.sub(r"# BUILT-DATA-BEGIN.*?# BUILT-DATA-END", lambda m: new, text, flags=re.S)
    NOTEBOOK.write_text(text)
    print(f"{n} hospitals, {int(pop.sum()):,} people; wrote {NOTEBOOK}")


if __name__ == "__main__":
    main()

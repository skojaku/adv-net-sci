# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["osmium", "numpy", "scipy", "networkx", "pyproj", "shapely", "matplotlib"]
# ///
"""New York State highway network at the level of interchanges (Module 06 data set).

Run:  uv run slides/m06/figures/make_ny.py [--tol 3.5] [--no-preview]

Raw data (downloaded once into figures/data/, which is gitignored):
  * ny-latest.osm.pbf   Geofabrik extract of OpenStreetMap, New York State
  * ny-state.geojson    New York State boundary (glynnbird/usstatesgeojson), display only
Everything after the download runs offline from that cache.

Pipeline
  1. Read every OSM way tagged highway = motorway / motorway_link / trunk / trunk_link.
     A node is a junction if two ways share it or a way starts or ends there. The road between two
     consecutive junctions of a way is one edge whose length is the km along the road.
     (cached as data/ny_junctions.pkl)
  2. Keep the largest connected component.
  3. Consolidate: junctions are grouped by complete-linkage agglomerative clustering in a projected
     CRS (EPSG:5070). Every group has diameter <= tol km. A group becomes one node at the mean of its
     members. Single linkage (the usual "merge everything within tol") chains the dense road mesh of
     the NYC area and Buffalo into one blob of ~10,000 junctions at tol = 1 km, so complete linkage
     is used.
  4. Drop self-loops, keep the shorter of parallel edges, contract every degree-2 node (chain
     lengths add), and delete dead-end stubs shorter than tol (remnants of the consolidation) until
     nothing changes. An edge shorter than the straight-line distance between its end nodes is
     lengthened to that distance.
  5. Centralities, with shortest paths weighted by km where a distance is involved.
  6. Write data/ny_network.json and a preview PNG (matplotlib, for checking only).
"""
import argparse
import datetime
import json
import math
import os
import pickle
import time
import urllib.request
from collections import Counter, defaultdict

import networkx as nx
import numpy as np
from pyproj import Transformer
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
from scipy.spatial import cKDTree
from shapely.geometry import MultiPolygon, shape

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
PBF_URL = "https://download.geofabrik.de/north-america/us/new-york-latest.osm.pbf"
GEOJSON_URL = "https://raw.githubusercontent.com/glynnbird/usstatesgeojson/master/new%20york.geojson"
PBF = os.path.join(DATA, "ny-latest.osm.pbf")
PBF_DATE = os.path.join(DATA, "ny-latest.date")
GEOJSON = os.path.join(DATA, "ny-state.geojson")
JUNCTIONS = os.path.join(DATA, "ny_junctions.pkl")
OUT_JSON = os.path.join(DATA, "ny_network.json")
OUT_PNG = os.path.join(DATA, "ny_preview.png")

HIGHWAYS = {"motorway", "motorway_link", "trunk", "trunk_link"}
MAIN = {"motorway", "trunk"}
DEFAULT_TOL_KM = 3.5
CITY_RADIUS_KM = 6.0
EARTH_KM = 6371.0088

CITIES = {
    "Buffalo": (-78.8784, 42.8864),
    "Rochester": (-77.6088, 43.1566),
    "Syracuse": (-76.1474, 43.0481),
    "Utica": (-75.2327, 43.1009),
    "Albany": (-73.7562, 42.6526),
    "New York City": (-73.9712, 40.7831),
    "Binghamton": (-75.918, 42.0987),
    "Watertown": (-75.9108, 43.9748),
}

# (name, lon, lat): only used to describe a node as "near X" in reports.
PLACES = [
    ("Buffalo", -78.8784, 42.8864), ("Niagara Falls", -79.0377, 43.0962), ("Jamestown", -79.2353, 42.0970),
    ("Olean", -78.4297, 42.0776), ("Rochester", -77.6088, 43.1566), ("Batavia", -78.1875, 42.9981),
    ("Geneva", -76.9772, 42.8687), ("Corning", -77.0547, 42.1429), ("Elmira", -76.8077, 42.0898),
    ("Ithaca", -76.5019, 42.4440), ("Syracuse", -76.1474, 43.0481), ("Auburn", -76.5661, 42.9317),
    ("Cortland", -76.1805, 42.6012), ("Binghamton", -75.918, 42.0987), ("Utica", -75.2327, 43.1009),
    ("Rome", -75.4557, 43.2128), ("Oneonta", -75.0638, 42.4529), ("Watertown", -75.9108, 43.9748),
    ("Oswego", -76.5105, 43.4553), ("Massena", -74.8946, 44.9281), ("Ogdensburg", -75.4863, 44.6942),
    ("Malone", -74.2948, 44.8489), ("Plattsburgh", -73.4529, 44.6995), ("Glens Falls", -73.6440, 43.3095),
    ("Saratoga Springs", -73.7846, 43.0831), ("Schenectady", -73.9396, 42.8142), ("Albany", -73.7562, 42.6526),
    ("Amsterdam", -74.1882, 42.9387), ("Hudson", -73.7910, 42.2529), ("Kingston", -73.9974, 41.9270),
    ("Poughkeepsie", -73.9210, 41.7004), ("Newburgh", -74.0104, 41.5034), ("Middletown", -74.4229, 41.4459),
    ("Monticello", -74.6894, 41.6556), ("Port Jervis", -74.6918, 41.3751), ("Suffern", -74.1496, 41.1148),
    ("White Plains", -73.7629, 41.0340), ("Yonkers", -73.8987, 40.9312), ("New York City", -73.9712, 40.7831),
    ("Hempstead", -73.6187, 40.7062), ("Huntington", -73.4257, 40.8682), ("Ronkonkoma", -73.1126, 40.8154),
    ("Riverhead", -72.6620, 40.9170), ("Hamptons", -72.3, 40.88), ("Newark NJ border", -74.17, 40.65),
    ("Watkins Glen", -76.8686, 42.3803), ("Lake George", -73.7120, 43.4259), ("Lake Placid", -73.9799, 44.2795),
    ("Gouverneur", -75.4738, 44.3356), ("Carthage", -75.6107, 43.9778), ("Canandaigua", -77.2819, 42.8870),
]


def log(msg):
    print(msg, flush=True)


def hav_km(lon1, lat1, lon2, lat2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * EARTH_KM * math.asin(math.sqrt(a))


# ----------------------------------------------------------------------------- download + parse
def download():
    os.makedirs(DATA, exist_ok=True)
    if not (os.path.exists(PBF) and os.path.getsize(PBF) > 0):
        log(f"downloading {PBF_URL}")
        urllib.request.urlretrieve(PBF_URL, PBF)
        with open(PBF_DATE, "w") as f:
            f.write(datetime.date.today().isoformat() + "\n")
    if not (os.path.exists(GEOJSON) and os.path.getsize(GEOJSON) > 0):
        log(f"downloading {GEOJSON_URL}")
        urllib.request.urlretrieve(GEOJSON_URL, GEOJSON)


def parse_pbf():
    """OSM ways -> junction graph. Returns dict(xy, edges, refs)."""
    import osmium

    log("reading the pbf (a few seconds with a warm cache)")
    ways = []
    fp = (osmium.FileProcessor(PBF, osmium.osm.NODE | osmium.osm.WAY)
          .with_locations().with_filter(osmium.filter.KeyFilter("highway")))
    for o in fp:
        if o.is_way() and o.tags["highway"] in HIGHWAYS:
            try:
                pts = [(n.ref, n.lon, n.lat) for n in o.nodes]
            except osmium.InvalidLocationError:
                continue
            if len(pts) >= 2:
                ways.append((o.tags["highway"], o.tags.get("ref", ""), pts))
    log(f"{len(ways)} ways")

    use = Counter()
    for _, _, pts in ways:
        for r in {p[0] for p in pts}:
            use[r] += 1
        use[pts[0][0]] += 1
        use[pts[-1][0]] += 1
    xy, edges = {}, {}
    refs = defaultdict(Counter)  # junction -> counts of route refs on the main carriageways
    for hw, ref, pts in ways:
        toks = [t.strip() for t in ref.split(";") if t.strip()] if hw in MAIN else []
        last, acc = 0, 0.0
        for i in range(1, len(pts)):
            acc += hav_km(pts[i - 1][1], pts[i - 1][2], pts[i][1], pts[i][2])
            if use[pts[i][0]] >= 2 or i == len(pts) - 1:
                u, v = pts[last][0], pts[i][0]
                xy[u] = pts[last][1:]
                xy[v] = pts[i][1:]
                for t in toks:
                    refs[u][t] += 1
                    refs[v][t] += 1
                if u != v:
                    k = (u, v) if u < v else (v, u)
                    edges[k] = min(edges.get(k, 1e18), acc)
                last, acc = i, 0.0
    return {"xy": xy, "edges": edges, "refs": {k: dict(v) for k, v in refs.items()}}


def load_junctions():
    if os.path.exists(JUNCTIONS):
        with open(JUNCTIONS, "rb") as f:
            return pickle.load(f)
    d = parse_pbf()
    with open(JUNCTIONS, "wb") as f:
        pickle.dump(d, f)
    return d


# ----------------------------------------------------------------------------- simplify
def contract_degree2(H, total, through):
    """Contract every degree-2 node of H. Edge attributes: km (road km between the raw end junctions,
    including the straight-line hops inside contracted clusters) and ends {cluster: raw junction}.
    total(a, b, attr) adds the offsets from the raw end junctions to the cluster centres;
    through(n, r1, r2) is the km from raw junction r1 to r2 inside cluster n."""
    q = [n for n in H if H.degree(n) == 2]
    while q:
        n = q.pop()
        if n not in H or H.degree(n) != 2:
            continue
        u, v = list(H.neighbors(n))
        e1, e2 = H[n][u], H[n][v]
        attr = {"km": e1["km"] + e2["km"] + through(n, e1["ends"][n], e2["ends"][n]),
                "ends": {u: e1["ends"][u], v: e2["ends"][v]}}
        H.remove_node(n)
        if not H.has_edge(u, v) or total(u, v, attr) < total(u, v, H[u][v]):
            H.add_edge(u, v, **attr)
        q += [x for x in (u, v) if H.degree(x) == 2]


def consolidate(Xkm, tol):
    """Complete-linkage clusters of diameter <= tol (km). Returns labels."""
    n = len(Xkm)
    pr = cKDTree(Xkm).query_pairs(tol, output_type="ndarray")
    A = coo_matrix((np.ones(len(pr)), (pr[:, 0], pr[:, 1])), shape=(n, n))
    nc, comp = connected_components(A, directed=False)  # a cluster never spans two components
    lab = -np.ones(n, int)
    nxt = 0
    for c in range(nc):
        mem = np.where(comp == c)[0]
        if len(mem) == 1:
            lab[mem] = nxt
            nxt += 1
            continue
        f = fcluster(linkage(Xkm[mem], method="complete"), tol, criterion="distance")
        lab[mem] = f - 1 + nxt
        nxt += f.max()
    return lab


def build_graph(raw, tol):
    xy, refs = raw["xy"], raw["refs"]
    G = nx.Graph()
    for (u, v), km in raw["edges"].items():
        G.add_edge(u, v, km=km)
    comp = max(nx.connected_components(G), key=len)
    stats = {"junctions_all": G.number_of_nodes(), "junctions_lcc": len(comp)}
    G = G.subgraph(comp).copy()
    stats["raw_edges_lcc"] = G.number_of_edges()

    nodes = list(G.nodes())
    idx = {n: i for i, n in enumerate(nodes)}
    tf = Transformer.from_crs(4326, 5070, always_xy=True)
    P = np.array([xy[n] for n in nodes])
    X = np.column_stack(tf.transform(P[:, 0], P[:, 1])) / 1000.0
    lab = consolidate(X, tol)
    stats["clusters"] = int(lab.max() + 1)

    members = defaultdict(list)
    for n, l in zip(nodes, lab):
        members[int(l)].append(n)
    centre = {l: tuple(np.mean([xy[m] for m in ms], axis=0)) for l, ms in members.items()}

    def total(a, b, e):  # km from centre of a to centre of b along the road
        return e["km"] + hav_km(*centre[a], *xy[e["ends"][a]]) + hav_km(*centre[b], *xy[e["ends"][b]])

    def through(n, r1, r2):
        return hav_km(*xy[r1], *xy[r2])

    H = nx.Graph()
    for u, v, d in G.edges(data=True):
        a, b = int(lab[idx[u]]), int(lab[idx[v]])
        if a == b:
            continue
        attr = {"km": d["km"], "ends": {a: u, b: v}}
        if not H.has_edge(a, b) or total(a, b, attr) < total(a, b, H[a][b]):
            H.add_edge(a, b, **attr)
    contract_degree2(H, total, through)
    pruned = 0
    while True:
        stubs = [n for n in H if H.degree(n) == 1
                 and total(n, next(iter(H[n])), next(iter(H[n].values()))) < tol]
        if not stubs or H.number_of_nodes() <= 2:
            break
        H.remove_nodes_from(stubs)
        pruned += len(stubs)
        contract_degree2(H, total, through)
    stats["stubs_pruned"] = pruned

    keep = sorted(H.nodes())
    pos = {l: centre[l] for l in keep}
    node_refs = {}
    for l in keep:
        c = Counter()
        for m in members[l]:
            c.update(refs.get(m, {}))
        node_refs[l] = [r for r, _ in c.most_common(3)]
    new = {l: i for i, l in enumerate(keep)}
    out = nx.Graph()
    for l in keep:
        out.add_node(new[l], lon=pos[l][0], lat=pos[l][1], refs=node_refs[l], merged=len(members[l]))
    short = 0
    for a, b, d in H.edges(data=True):
        chord = hav_km(*pos[a], *pos[b])
        km = total(a, b, d)
        if km < chord:
            km, short = chord, short + 1
        out.add_edge(new[a], new[b], km=km)
    stats["edges_lengthened_to_chord"] = short  # road km would be below the straight line
    return out, stats


# ----------------------------------------------------------------------------- measures
def measures(G):
    n = G.number_of_nodes()
    ids = list(range(n))
    W = nx.to_scipy_sparse_array(G, nodelist=ids, weight="km", format="csr")
    D = dijkstra(W, directed=False)
    assert np.isfinite(D).all(), "graph is not connected"
    off = ~np.eye(n, dtype=bool)
    closeness = (n - 1) / D.sum(1)
    with np.errstate(divide="ignore"):
        inv = np.where(off, 1.0 / np.where(off, D, 1), 0.0)
    harmonic = inv.sum(1) / (n - 1)
    ecc = D.max(1)
    btw = nx.betweenness_centrality(G, weight="km", normalized=True)  # exact
    A = nx.to_numpy_array(G, nodelist=ids, weight=None)
    vals, vecs = np.linalg.eigh(A)
    lam = float(vals[-1])
    v = vecs[:, -1]
    v = v if v.sum() >= 0 else -v
    assert (v > -1e-12).all()
    alphas = (0.5 / lam, 0.9 / lam)
    katz = [np.linalg.solve(np.eye(n) - a * A, np.ones(n)) for a in alphas]
    pr = nx.pagerank(G, alpha=0.85, weight=None, tol=1e-12, max_iter=1000)  # teleportation r = 0.15
    deg = np.array([G.degree(i) for i in ids])
    return {
        "degree": deg, "closeness": closeness, "harmonic": harmonic, "eccentricity": ecc,
        "betweenness": np.array([btw[i] for i in ids]), "eigenvector": v,
        "katz_05": katz[0], "katz_09": katz[1], "pagerank": np.array([pr[i] for i in ids]),
    }, lam, alphas, D


def nearest_place(lon, lat):
    best = min(PLACES, key=lambda p: hav_km(lon, lat, p[1], p[2]))
    return best[0], hav_km(lon, lat, best[1], best[2])


def outline(simplify_deg=0.02):
    g = shape(json.load(open(GEOJSON))["geometry"])
    polys = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
    rings = []
    for p in polys:
        if p.area < 0.005:  # tiny islands
            continue
        s = p.simplify(simplify_deg, preserve_topology=True)
        rings.append([[round(x, 4), round(y, 4)] for x, y in s.exterior.coords])
    return rings


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tol", type=float, default=DEFAULT_TOL_KM, help="cluster diameter in km")
    ap.add_argument("--no-preview", action="store_true")
    a = ap.parse_args()

    download()
    raw = load_junctions()
    t0 = time.time()
    G, stats = build_graph(raw, a.tol)
    n, m = G.number_of_nodes(), G.number_of_edges()
    log(f"tol {a.tol} km: {stats} -> {n} nodes, {m} edges ({time.time() - t0:.0f}s)")
    assert nx.is_connected(G) and nx.number_of_selfloops(G) == 0

    meas, lam, alphas, D = measures(G)
    lon = np.array([G.nodes[i]["lon"] for i in range(n)])
    lat = np.array([G.nodes[i]["lat"] for i in range(n)])

    cities, city_info = {}, {}
    for name, (cx, cy) in CITIES.items():
        dist = np.array([hav_km(cx, cy, lon[i], lat[i]) for i in range(n)])
        near = np.where(dist <= CITY_RADIUS_KM)[0]
        if len(near):
            i = int(near[np.argmax(meas["betweenness"][near])])
            rule = f"highest betweenness among {len(near)} node(s) within {CITY_RADIUS_KM:g} km"
        else:
            i = int(np.argmin(dist))
            rule = "no node within 6 km: nearest node"
        cities[name] = i
        city_info[name] = {"node": i, "distance_km": round(float(dist[i]), 2), "rule": rule}

    nodes = []
    for i in range(n):
        d = {"id": i, "lon": round(float(lon[i]), 5), "lat": round(float(lat[i]), 5),
             "refs": G.nodes[i]["refs"], "merged": G.nodes[i]["merged"]}
        pl, pd_ = nearest_place(lon[i], lat[i])
        d["near"] = pl
        d["near_km"] = round(pd_, 1)
        for k, v in meas.items():
            d[k] = int(v[i]) if k == "degree" else float(v[i])
        nodes.append(d)
    edges = [{"u": int(u), "v": int(v), "km": round(float(d["km"]), 3)} for u, v, d in G.edges(data=True)]

    date = open(PBF_DATE).read().strip() if os.path.exists(PBF_DATE) else ""
    out = {
        "nodes": nodes, "edges": edges, "cities": cities, "city_info": city_info,
        "lambda_max": lam, "katz_alpha": {"katz_05": alphas[0], "katz_09": alphas[1]},
        "outline": outline(),
        "meta": {
            "source": PBF_URL + " (OpenStreetMap, ODbL); boundary " + GEOJSON_URL,
            "download_date": date,
            "ways": "highway in " + ", ".join(sorted(HIGHWAYS)),
            "tolerance_km": a.tol,
            "consolidation": "complete linkage, cluster diameter <= tolerance, EPSG:5070",
            "n_nodes": n, "n_edges": m, **stats,
            "edge_weight": "km along the road between the two node centres (shorter of parallel edges; chain lengths summed)",
            "closeness": "(n-1) / sum of km distances", "harmonic": "mean of 1/km over the other nodes",
            "eccentricity": "km to the farthest node", "betweenness": "exact, km-weighted, normalized",
            "eigenvector": "unweighted adjacency, unit L2 norm, positive", "katz": "(I - alpha A)^-1 1, beta = 1, unweighted",
            "pagerank": "unweighted, alpha 0.85 (teleportation r = 0.15), sums to 1",
            "city_radius_km": CITY_RADIUS_KM,
        },
    }
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, separators=(",", ":"))
    log(f"wrote {OUT_JSON} ({os.path.getsize(OUT_JSON) / 1e3:.0f} KB)")
    if not a.no_preview:
        preview(out)


def preview(out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    nodes, cities = out["nodes"], out["cities"]
    fig, ax = plt.subplots(figsize=(15, 11))
    for ring in out["outline"]:
        r = np.array(ring)
        ax.plot(r[:, 0], r[:, 1], color="#999999", lw=1)
    for e in out["edges"]:
        u, v = nodes[e["u"]], nodes[e["v"]]
        ax.plot([u["lon"], v["lon"]], [u["lat"], v["lat"]], color="#555555", lw=0.8, zorder=1)
    b = np.array([d["betweenness"] for d in nodes])
    sc = ax.scatter([d["lon"] for d in nodes], [d["lat"] for d in nodes], c=b, cmap="viridis_r", s=28, zorder=2,
                    edgecolors="k", linewidths=0.3)
    plt.colorbar(sc, ax=ax, shrink=0.6, label="betweenness")
    for name, i in cities.items():
        d = nodes[i]
        ax.scatter([d["lon"]], [d["lat"]], s=110, facecolors="none", edgecolors="red", linewidths=1.6, zorder=3)
        ax.annotate(name, (d["lon"], d["lat"]), xytext=(6, 6), textcoords="offset points", color="red", fontsize=11,
                    fontweight="bold")
    ax.set_aspect(1 / math.cos(math.radians(42.5)))
    ax.set_title(f"NY highway network: {len(nodes)} nodes, {len(out['edges'])} edges, tol {out['meta']['tolerance_km']} km")
    fig.savefig(OUT_PNG, dpi=110, bbox_inches="tight")
    log(f"wrote {OUT_PNG}")


if __name__ == "__main__":
    main()

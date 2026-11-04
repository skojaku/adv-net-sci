#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "numpy",
#     "pandas",
#     "scikit-learn",
#     "python-igraph",
# ]
# ///
"""Build the three networks of the M07 mini-project and write them into the notebook.

    uv run tools/build_m07_mini_data.py                 # rewrite the BUILT-DATA block
    uv run tools/build_m07_mini_data.py --csv-dir /tmp/m07   # also dump the CSVs
    uv run tools/build_m07_mini_data.py --summary        # print numbers, write nothing

The notebook (notebooks/m07-randomwalks/mini-project.py) travels alone to molab,
so the data is a literal between BUILT-DATA-BEGIN / BUILT-DATA-END, one
zlib+base64 CSV per table. Nothing is fetched when a student runs it.

  net1  degree-corrected stochastic block model, assortative, 5 groups
  net2  core-periphery, 2 groups
  net3  OpenFlights routes, ground truth = region (time-zone prefix)

Node ids are shuffled and group names are replaced by 0..K-1 in random order, so
neither the airport order nor a region name gives the origin away. Each network is
its largest connected component, unweighted, undirected.

BASELINE is modularity maximisation (Leiden), mean NMI over 10 seeds, because the
notebook should not need igraph.
"""

import argparse
import base64
import io
import random
import re
import urllib.request
import zlib
from pathlib import Path

import igraph
import numpy as np
import pandas as pd
from sklearn.metrics import normalized_mutual_info_score

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "notebooks" / "m07-randomwalks" / "mini-project.py"
CACHE = Path.home() / ".cache" / "adv-net-sci" / "openflights"
OPENFLIGHTS = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/"

N_BASELINE_RUNS = 10
INDENT = "    "  # the block lives inside `with app.setup`


# ---------------------------------------------------------------- generators
def dcsbm(n, sizes, mu, mean_degree, alpha, seed):
    """Assortative DC-SBM: a fraction mu of the edge weight leaves the group."""
    rng = np.random.default_rng(seed)
    k = len(sizes)
    g = np.repeat(np.arange(k), np.round(np.array(sizes) / np.sum(sizes) * n).astype(int))
    n = len(g)
    theta = np.minimum(rng.pareto(alpha, n) + 1.0, 12.0)
    omega = np.full((k, k), mu / (k - 1))
    np.fill_diagonal(omega, 1 - mu)
    w = np.outer(theta, theta) * omega[g][:, g]
    w = w / w.sum() * (n * mean_degree)
    iu = np.triu_indices(n, 1)
    keep = rng.random(len(iu[0])) < 1 - np.exp(-w[iu])
    return n, np.c_[iu[0][keep], iu[1][keep]], g


def core_periphery(n, core_frac, p_cc, p_cp, p_pp, alpha, seed):
    """Core-periphery: dense core, sparse periphery, medium links between them."""
    rng = np.random.default_rng(seed)
    n_core = int(n * core_frac)
    g = np.r_[np.zeros(n_core, int), np.ones(n - n_core, int)]
    theta = np.minimum(rng.pareto(alpha, n) + 1.0, 8.0)
    p = np.array([[p_cc, p_cp], [p_cp, p_pp]])
    w = np.outer(theta, theta) * p[g][:, g]
    iu = np.triu_indices(n, 1)
    keep = rng.random(len(iu[0])) < np.minimum(w[iu], 1.0)
    return n, np.c_[iu[0][keep], iu[1][keep]], g


def airports():
    CACHE.mkdir(parents=True, exist_ok=True)
    for name in ("airports.dat", "routes.dat"):
        if not (CACHE / name).exists():
            urllib.request.urlretrieve(OPENFLIGHTS + name, CACHE / name)
    ap = pd.read_csv(CACHE / "airports.dat", header=None, usecols=[4, 11],
                     names=["iata", "tz"], na_values="\\N").dropna()
    region = dict(zip(ap.iata, ap.tz.str.split("/").str[0]))
    rt = pd.read_csv(CACHE / "routes.dat", header=None, usecols=[2, 4],
                     names=["s", "d"], na_values="\\N").dropna()
    rt = rt[rt.s.isin(region) & rt.d.isin(region) & (rt.s != rt.d)]
    pairs = {tuple(sorted(x)) for x in zip(rt.s, rt.d)}
    names = sorted({a for p in pairs for a in p})
    ids = {a: i for i, a in enumerate(names)}
    edges = np.array([(ids[a], ids[b]) for a, b in pairs])
    labels = pd.factorize(np.array([region[a] for a in names]))[0]
    return len(names), edges, labels


# ---------------------------------------------------------------- shaping
def largest_component(n, edges, g):
    graph = igraph.Graph(n=n, edges=edges.tolist())
    cc = graph.connected_components()  # NOT .giant(): that renumbers the vertices
    keep = np.where(np.array(cc.membership) == int(np.argmax(cc.sizes())))[0]
    new = -np.ones(n, int)
    new[keep] = np.arange(len(keep))
    edges = np.array([(new[a], new[b]) for a, b in edges if new[a] >= 0 and new[b] >= 0])
    return len(keep), edges, g[keep]


def anonymise(n, edges, g, seed):
    """Shuffle node ids, edge order and edge direction; rename the groups at random."""
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)  # old id -> new id
    edges = perm[edges]
    flip = rng.random(len(edges)) < 0.5
    edges[flip] = edges[flip][:, ::-1]
    edges = edges[rng.permutation(len(edges))]
    groups = np.empty(n, int)
    groups[perm] = g
    names = rng.permutation(len(set(g)))
    groups = names[pd.factorize(groups, sort=True)[0]]
    return edges, groups


def baseline(n, edges, groups):
    graph = igraph.Graph(n=n, edges=edges.tolist())
    scores = []
    for seed in range(N_BASELINE_RUNS):
        random.seed(seed)
        found = graph.community_leiden(objective_function="modularity", n_iterations=-1).membership
        scores.append(normalized_mutual_info_score(groups, found))
    return float(np.mean(scores))


# ---------------------------------------------------------------- packing
def pack(df):
    text = df.to_csv(index=False)
    return base64.b64encode(zlib.compress(text.encode(), 9)).decode()


def build():
    raw = {
        "net1": dcsbm(800, [0.30, 0.25, 0.20, 0.15, 0.10], 0.3, 10, 2.5, seed=0),
        "net2": core_periphery(800, 0.2, 0.05, 0.03, 0.005, 2.5, seed=0),
        "net3": airports(),
    }
    out = {}
    for i, (name, (n, edges, g)) in enumerate(raw.items()):
        n, edges, g = largest_component(n, edges, g)
        edges, groups = anonymise(n, edges, g, seed=100 + i)
        out[name] = {
            "n": n,
            "m": len(edges),
            "k": len(set(groups)),
            "edges": pd.DataFrame(edges, columns=["source", "target"]),
            "groups": pd.DataFrame({"node": np.arange(n), "group": groups}),
            "baseline": baseline(n, edges, groups),
        }
    return out


def block(nets):
    lines = [
        f"{INDENT}# BUILT-DATA-BEGIN",
        f"{INDENT}# Written by tools/build_m07_mini_data.py. One zlib+base64 CSV per table.",
        f"{INDENT}NETWORKS = {{",
    ]
    for name, d in nets.items():
        lines += [
            f"{INDENT}    {name!r}: {{",
            f"{INDENT}        'edges': {pack(d['edges'])!r},",
            f"{INDENT}        'groups': {pack(d['groups'])!r},",
            f"{INDENT}    }},",
        ]
    lines += [f"{INDENT}}}"]
    lines += [f"{INDENT}BASELINE = {{{', '.join(f'{k!r}: {round(v['baseline'], 2)}' for k, v in nets.items())}}}"]
    lines += [f"{INDENT}# BUILT-DATA-END"]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", action="store_true", help="print numbers, write nothing")
    ap.add_argument("--csv-dir", type=Path, help="also write the CSV tables here")
    args = ap.parse_args()

    nets = build()
    for name, d in nets.items():
        print(f"{name}: n={d['n']} m={d['m']} K={d['k']} baseline(Leiden, mean NMI)={d['baseline']:.2f}")
    if args.csv_dir:
        args.csv_dir.mkdir(parents=True, exist_ok=True)
        for name, d in nets.items():
            d["edges"].to_csv(args.csv_dir / f"{name}_edges.csv", index=False)
            d["groups"].to_csv(args.csv_dir / f"{name}_groups.csv", index=False)
    if args.summary:
        return
    if not NOTEBOOK.exists():
        raise SystemExit(f"{NOTEBOOK} does not exist yet; nothing written")
    text = NOTEBOOK.read_text()
    pattern = re.compile(rf"^{INDENT}# BUILT-DATA-BEGIN.*?^{INDENT}# BUILT-DATA-END", re.S | re.M)
    if not pattern.search(text):
        raise SystemExit("BUILT-DATA markers not found in the notebook")
    NOTEBOOK.write_text(pattern.sub(lambda _: block(nets), text, count=1))
    print(f"wrote {NOTEBOOK.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

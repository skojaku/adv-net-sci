#!/usr/bin/env python3
"""Check a student's Quiz 6 graph: do betweenness, closeness, degree and
eigenvector centrality each have one most central node, and are the four
different?  (Brandes and Hildenbrand 2014, "BCDE" graphs.)

Usage:
    uv run --with networkx --with numpy check_bcde.py "1-2 1-3 1-4 2-6"
    uv run --with networkx --with numpy check_bcde.py --demo

The edge list is any text with pairs like 1-2 (node labels may be words or
numbers). Prints each measure's values, its center, and the verdict.
"""
import re
import sys

import networkx as nx
import numpy as np

TOL = 1e-9  # ties in betweenness and eigenvector are decided to this tolerance

DEMO = "1-2 1-3 1-4 2-6 3-5 3-8 3-12 4-6 4-7 6-11 7-8 9-10 10-11"


def parse(text):
    G = nx.Graph()
    for a, b in re.findall(r"([A-Za-z0-9_]+)\s*-\s*([A-Za-z0-9_]+)", text):
        if a == b:
            sys.exit(f"self-loop at {a}: not a simple graph")
        G.add_edge(a, b)
    return G


def unique_max(values, names):
    """The nodes within TOL of the top value; one name means a unique center."""
    top = max(values)
    tied = [nm for nm, v in zip(names, values) if v >= top - TOL]
    return tied


def main():
    arg = DEMO if (len(sys.argv) > 1 and sys.argv[1] == "--demo") else " ".join(sys.argv[1:])
    if not arg.strip():
        sys.exit(__doc__)
    G = parse(arg)
    names = sorted(G, key=lambda s: (len(s), s))
    n = len(names)
    print(f"{n} nodes, {G.number_of_edges()} edges, connected: {nx.is_connected(G)}")
    if not nx.is_connected(G):
        sys.exit("not connected: the quiz needs a connected graph")
    if n > 12:
        print(f"WARNING: {n} nodes, the limit is 12")

    deg = [G.degree(v) for v in names]
    tot = [sum(nx.single_source_shortest_path_length(G, v).values()) for v in names]
    clo = [1.0 / t for t in tot]  # the integer total decides ties, exactly
    bet_d = nx.betweenness_centrality(G, normalized=False)
    bet = [bet_d[v] for v in names]
    A = nx.to_numpy_array(G, nodelist=names)
    w, U = np.linalg.eigh(A)
    ev = np.abs(U[:, -1])
    ev = ev / ev.max()

    print(f"{'node':>6} {'deg':>4} {'sumdist':>8} {'betw':>8} {'eigvec':>8}")
    for i, v in enumerate(names):
        print(f"{v:>6} {deg[i]:>4} {tot[i]:>8} {bet[i]:>8.3f} {ev[i]:>8.4f}")

    centers = {}
    for label, vals in (("betweenness", bet), ("closeness", clo),
                        ("degree", deg), ("eigenvector", ev)):
        tied = unique_max(vals, names)
        centers[label] = tied
        status = "unique" if len(tied) == 1 else f"TIE {tied}"
        print(f"{label:>12}: center {tied[0] if len(tied) == 1 else tied}  ({status})")

    all_unique = all(len(t) == 1 for t in centers.values())
    four = {t[0] for t in centers.values() if len(t) == 1}
    ok = all_unique and len(four) == 4
    print("VERDICT:", "four different unique centers" if ok else
          ("a center is tied" if not all_unique else "centers coincide"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

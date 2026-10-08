#!/usr/bin/env python3
"""Write the M05 pitch notebook (Colab / Jupyter): community detection on the class's own seats.

    python tools/build_m05_pitch_notebook.py                          # write pitch-seats.ipynb
    python tools/build_m05_pitch_notebook.py --branch main            # the branch the data URL points at
    python tools/build_m05_pitch_notebook.py --graph knn --k 3        # how seats become a network
    python tools/build_m05_pitch_notebook.py --graph eps --eps 2.3

In class the lecturer draws the seating on paper, reads off one (x, y) per
student and commits `seats.csv` next to the notebook. The notebook reads that
file from a fixed raw.githubusercontent.com address and joins people who sit
close (an epsilon-neighbourhood graph or a k-nearest-neighbour graph). The graph
is built here, not by the students. Four groups then pitch a partition of it;
there is no ground truth.

How each group gets its partition:

  1. Shape (k-core, clique, pseudo-clique) and 2. Cut: by eye. The nodes are
     numbered in the picture; the student writes one number per node in a list,
     the notebook redraws the partition and prints the matrix of group sizes and
     edge counts, and `check` gives the values to compare with a hand calculation.
  3. Modularity: types igraph code from a paper sheet.
  4. Block model: types graph-tool code from a paper sheet.

The code on the paper is lecture-note/m05-clustering/pitch/pitch-code.tex; the
notebook has an empty cell for it. The handout is pitch-sheet.tex.

graph-tool is not on PyPI and has no Windows build. Step A installs it with
micromamba into a private conda environment in the temp folder and the fit runs
there in its own process (the way lecture-note/m05-clustering/pen-and-paper/lab.py
does it), so it needs no restart and works on Colab, Linux and macOS. condacolab
would not: it only works in Colab.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "lecture-note" / "m05-clustering" / "pitch"
REPO = "skojaku/adv-net-sci"
PATH = "lecture-note/m05-clustering/pitch"


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n").splitlines(True)}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": text.strip("\n").splitlines(True),
    }


SETUP = '''
#@title Setup. Press the play button. Nothing to type here. { display-mode: "form" }
try:
    import igraph
except ImportError:
    %pip install -q python-igraph
    import igraph

from itertools import combinations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

SEATS_URL = "__RAW__"
GRAPH, K, EPS = "__GRAPH__", __K__, __EPS__   # set by the lecturer: "knn" (k nearest) or "eps" (within EPS)

try:
    seats = pd.read_csv(SEATS_URL)
except Exception:
    seats = pd.read_csv(SEATS_URL.replace("seats.csv", "seats-example.csv"))
    print("#" * 70)
    print("REHEARSAL DATA: seats.csv is not published yet, so this is an invented room.")
    print("Run this notebook again once the lecturer says the seats are up.")
    print("#" * 70)

P = seats[["x", "y"]].to_numpy(dtype=float)
N = len(P)
D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
np.fill_diagonal(D, np.inf)
if GRAPH == "knn":
    EDGES = sorted({tuple(sorted((i, int(j)))) for i in range(N) for j in np.argsort(D[i], kind="stable")[:K]})
else:
    eps = D.min(axis=1).max() if EPS is None else EPS      # None: the smallest value that leaves nobody alone
    EDGES = [(i, j) for i, j in combinations(range(N), 2) if D[i, j] <= eps + 1e-9]
graph = igraph.Graph(n=N, edges=EDGES)
A = np.array(graph.get_adjacency().data)

PALETTE = ["#3959A6", "#B14434", "#DAB167", "#6B6B6B", "#7A5195", "#E377C2", "#8C564B", "#6BAED6", "#1A1A1A", "#BDB8AA"]


def show(labels, matrix=True):
    """Draw the partition: colour = group, dashed = edge between groups. Then print the
    matrix: the diagonal is the number of edges inside a group, the rest is the number of
    edges between two groups."""
    labels = list(labels)
    assert len(labels) == N, f"labels needs one number per node: {N} numbers, you gave {len(labels)}"
    names = sorted(set(labels))
    fig, ax = plt.subplots(figsize=(10, 4.2))
    for u, v in EDGES:
        cross = labels[u] != labels[v]
        ax.plot(P[[u, v], 0], P[[u, v], 1], color="#1A1A1A" if cross else "#BDB8AA", lw=1.2 if cross else 1.8,
                ls=(0, (4, 3)) if cross else "-", zorder=1)
    colour = [PALETTE[names.index(g) % len(PALETTE)] for g in labels]
    ax.scatter(P[:, 0], P[:, 1], s=420, c=colour, edgecolor="#1A1A1A", lw=1, zorder=2)
    for i in range(N):
        ax.text(P[i, 0], P[i, 1], str(i), ha="center", va="center", fontsize=10, fontweight="bold",
                color="#1A1A1A" if colour[i] in ("#DAB167", "#6BAED6", "#BDB8AA") else "white", zorder=3)
    ax.set_aspect("equal"); ax.axis("off"); ax.margins(0.08)
    plt.show()
    if matrix:
        M = pd.DataFrame(0, index=names, columns=names)
        for u, v in EDGES:
            M.loc[labels[u], labels[v]] += 1
            if labels[u] != labels[v]:
                M.loc[labels[v], labels[u]] += 1
        M.insert(0, "size", [labels.count(g) for g in names])
        M.index.name = "group"
        display(M)


def check(labels):
    """The values to compare with your hand calculation."""
    labels = list(labels)
    rows = []
    for g in sorted(set(labels)):
        S = [i for i in range(N) if labels[i] == g]
        inside = int(A[np.ix_(S, S)].sum()) // 2
        vol = int(A[S].sum())
        rows.append(dict(group=g, size=len(S), inside=inside,
                         density=round(inside / (len(S) * (len(S) - 1) / 2), 3) if len(S) > 1 else None,
                         fewest_inside=int(A[np.ix_(S, S)].sum(axis=1).min()),
                         leaving=vol - 2 * inside, volume=vol))
    t = pd.DataFrame(rows).set_index("group")
    display(t)
    print(f"ratio cut      = sum of leaving/size   = {sum(r.leaving / r.size for r in t.itertuples()):.4f}")
    print(f"normalized cut = sum of leaving/volume = {sum(r.leaving / r.volume for r in t.itertuples() if r.volume):.4f}")
    print(f"modularity Q   = {graph.modularity(labels):.4f}")


print(f"{N} people, numbered 0 to {N - 1}. {len(EDGES)} edges.")
'''

STEP_A = '''
#@title Step A. Group 4 only. Press the play button and wait. { display-mode: "form" }
# graph-tool is not on PyPI. It is installed from conda into a private folder, and graph_tool(fn)
# runs your function fn there. Inside fn, `gt` is graph-tool and `g` is the network.
import inspect, io, json, os, pathlib, platform, subprocess, tarfile, tempfile, textwrap, urllib.request

GT = pathlib.Path(tempfile.gettempdir()) / "graph-tool"
GT_PYTHON = GT / "env" / "bin" / "python"

if not GT_PYTHON.exists():
    kind = {"Linux": "linux-64",
            "Darwin": "osx-arm64" if platform.machine() == "arm64" else "osx-64"}.get(platform.system())
    if kind is None:
        raise SystemExit("graph-tool does not run on Windows. Open this notebook in Colab instead.")
    print("Installing graph-tool: one to three minutes. Please wait.")
    url = f"https://micro.mamba.pm/api/micromamba/{kind}/latest"
    tarfile.open(fileobj=io.BytesIO(urllib.request.urlopen(url).read()), mode="r:bz2").extract("bin/micromamba", GT)
    subprocess.run([GT / "bin" / "micromamba", "create", "-y", "-q", "-p", GT / "env", "-c", "conda-forge", "graph-tool"],
                   env={**os.environ, "MAMBA_ROOT_PREFIX": str(GT / "root")}, check=True)


def graph_tool(fn):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / "in.json").write_text(json.dumps(dict(n=N, edges=EDGES)))
        (tmp / "run.py").write_text(
            "import json\\nimport graph_tool.all as gt\\n"
            "gt.seed_rng(1); gt.openmp_set_num_threads(1)\\n"
            "d = json.load(open('in.json'))\\n"
            "g = gt.Graph(directed=False); g.add_vertex(d['n']); g.add_edge_list(d['edges'])\\n\\n"
            + textwrap.dedent(inspect.getsource(fn))
            + f"\\n\\njson.dump({fn.__name__}(g), open('out.json', 'w'))\\n")
        done = subprocess.run([GT_PYTHON, "run.py"], cwd=tmp, capture_output=True, text=True)
        if done.returncode:
            raise RuntimeError(done.stderr[-1500:])
        return json.loads((tmp / "out.json").read_text())


print("graph-tool is ready.")
'''


def cells(branch: str, graph: str, k: int, eps: float | None) -> list[dict]:
    raw = f"https://raw.githubusercontent.com/{REPO}/{branch}/{PATH}/seats.csv"
    setup = (SETUP.replace("__RAW__", raw).replace("__GRAPH__", graph)
             .replace("__K__", str(k)).replace("__EPS__", repr(eps)))
    return [
        md("""
# Pitch your partition

Everyone in this room is a node. Two people who sit close are joined by an edge. Your group makes **one** partition of these nodes and has three minutes to say why it is the one to use. There is no answer key.

Run *Setup*, then *The graph*. Then go to your group's section.
"""),
        code(setup),
        md("## The graph\nEach node has a number. `labels[i]` will be the group of node `i`."),
        code("show([0] * N, matrix=False)"),
        md("""
## Groups 1 and 2 · by eye
**Group 1:** find a k-core, a clique and a pseudo-clique. Give its members the number 1 and everyone else 0.
**Group 2:** split the nodes into groups so that the ratio cut and the normalized cut are small. One number per group.

Edit the list, run the cell, look. Work out the values by hand from the matrix below the picture, then run the check.
"""),
        code("""
labels = [0] * N   # replace by one number per node, e.g. [0, 0, 1, 1, 0, ...]
show(labels)
"""),
        code("check(labels)"),
        md("## Group 3 · igraph\nType the code from your sheet into the cell below. The network is `graph`."),
        code("# type the code from your sheet\n"),
        md("## Group 4 · graph-tool\nRun Step A, then type the code from your sheet into the cell below."),
        code(STEP_A),
        code("# type the code from your sheet\n"),
    ]


def main() -> None:
    ap = argparse.ArgumentParser()
    default_branch = subprocess.run(
        ["git", "-C", str(ROOT), "branch", "--show-current"], capture_output=True, text=True
    ).stdout.strip() or "main"
    ap.add_argument("--branch", default=default_branch,
                    help="branch the notebook's data URL points at (default: the current one)")
    ap.add_argument("--graph", choices=["knn", "eps"], default="eps", help="how seats become a network")
    ap.add_argument("--k", type=int, default=3, help="neighbours per person for --graph knn")
    ap.add_argument("--eps", type=float, default=None,
                    help="distance in seat widths for --graph eps (default: the smallest that leaves nobody alone)")
    args = ap.parse_args()
    nb = {
        "cells": cells(args.branch, args.graph, args.k, args.eps),
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }
    out = OUT / "pitch-seats.ipynb"
    out.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} (data from branch {args.branch}, graph {args.graph})")
    print(f"open in Colab: https://colab.research.google.com/github/{REPO}/blob/{args.branch}/{PATH}/pitch-seats.ipynb")


if __name__ == "__main__":
    main()

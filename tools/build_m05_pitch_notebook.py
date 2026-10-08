#!/usr/bin/env python3
"""Write the M05 pitch notebook (Colab / Jupyter): community detection on the class's own seats.

    python tools/build_m05_pitch_notebook.py                  # write pitch-seats.ipynb
    python tools/build_m05_pitch_notebook.py --branch main    # the branch the data URL points at
    python tools/build_m05_pitch_notebook.py --k 3            # the notebook's starting value of K

In class the lecturer draws the seating on paper, reads off one (x, y) per
student and commits `seats.csv` next to the notebook. The notebook reads that
file from a fixed raw.githubusercontent.com address and joins each person to
their K nearest people (an edge is kept if either end chose it). K is a variable
in the notebook that students may change: the data is not a network, and how to
define its edges is part of what the exercise is about. K = 2 can leave the
network in pieces; K = 3 usually does not.

Everything that is not the exercise is in ONE cell at the top, shown as a form so
that Colab hides its code: the loading, the drawing, and the graph-tool bridge,
which installs graph-tool on the first call so that only group 4 pays for it.

Four groups then pitch a partition; there is no ground truth.

  1. Shape (k-core, clique, pseudo-clique) and 2. Cut: by eye. The nodes are
     numbered in the picture; the student writes one number per node in a list.
     `show` redraws the partition; the adjacency matrix `A` is available. The
     student computes the values by hand. There is no checking function and no
     table of group sizes.
  3. Modularity: types igraph code from a paper sheet.
  4. Block model: types graph-tool code from a paper sheet.

The code on the paper is in the boxes of group 3 and 4 on the back of
lecture-note/m05-clustering/pitch/pitch-sheet.tex (one sheet, both sides, the
only handout); the notebook has an empty cell for it. If `show`, `graph` or
`graph_tool` change, change the sheet too.

graph-tool is not on PyPI and has no Windows build. It is installed with
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

import inspect, io, json, os, pathlib, platform, subprocess, tarfile, tempfile, textwrap, urllib.request

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SEATS_URL = "__RAW__"
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
DIST = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
np.fill_diagonal(DIST, np.inf)


def make_graph(k):
    """Join each person to their k nearest people. An edge is kept if either end chose it."""
    edges = sorted({tuple(sorted((i, int(j)))) for i in range(N) for j in np.argsort(DIST[i], kind="stable")[:k]})
    return edges, igraph.Graph(n=N, edges=edges)


PALETTE = ["#8FA8DC", "#E3877A", "#DAB167", "#B79AD6", "#9CCBE8", "#F0A8D0", "#C9A27E", "#BDB8AA", "#E5E5E5", "#F2D16B"]   # light enough for black labels


def show(labels):
    """Draw the partition with igraph (colour = group, dark edge = edge between groups)."""
    labels = np.array(labels)
    assert len(labels) == N, f"labels needs one number per node: {N} numbers, you gave {len(labels)}"
    names = np.unique(labels)
    colour = [PALETTE[int(np.where(names == g)[0][0]) % len(PALETTE)] for g in labels]
    cross = [labels[u] != labels[v] for u, v in graph.get_edgelist()]
    fig, ax = plt.subplots(figsize=(10, 4.2))
    igraph.plot(graph, target=ax, layout=igraph.Layout(P.tolist()), bbox=None,
                vertex_color=colour, vertex_size=30, vertex_label=list(range(N)),
                vertex_label_color="#1A1A1A",
                edge_color=["#1A1A1A" if c else "#BDB8AA" for c in cross],
                edge_width=[1.2 if c else 2.5 for c in cross])
    plt.show()


GT = pathlib.Path(tempfile.gettempdir()) / "graph-tool"
GT_PYTHON = GT / "env" / "bin" / "python"


def graph_tool(fn):
    """Run the function fn inside graph-tool and return what it returns. In fn, `gt` is
    graph-tool and `g` is the network. graph-tool is not on PyPI, so the first call installs
    it from conda into a private folder (one to three minutes, only group 4 pays for it)."""
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


print(f"Ready. {N} people.")
'''


def cells(branch: str, k: int) -> list[dict]:
    raw = f"https://raw.githubusercontent.com/{REPO}/{branch}/{PATH}/seats.csv"
    return [
        md("""
# Pitch your partition

Everyone in this room is a node. Each person is joined to their K nearest people. Your group makes **one** partition of these nodes and has three minutes to say why it is the one to use. There is no answer key.

Run *Setup*, then *The graph*, then go to your group's section.
"""),
        code(SETUP.replace("__RAW__", raw)),
        md("## The graph\nThe data is where people sit; it is not a network. K decides which pairs become edges. Change it and run the cell again."),
        code(f"""
K = {k}
EDGES, graph = make_graph(K)
A = np.array(graph.get_adjacency().data)   # adjacency matrix: A[i, j] = 1 when i and j are joined
show([0] * N)
print(A)
"""),
        md("""
## Groups 1 and 2 · by eye
`labels[i]` is the group of node `i`. Edit the list, run the cell, look at the picture.

**Group 1:** a k-core, a clique and a pseudo-clique: give its members the number 1 and everyone else 0.
**Group 2:** exactly two groups, numbered 0 and 1.
"""),
        code("""
labels = [0] * N   # replace by one number per node, e.g. [0, 0, 1, 1, 0, ...]
show(labels)
"""),
        md("## Group 3 · igraph\nType the code from your sheet into the cell below. The network is `graph`."),
        code("# type the code from your sheet\n"),
        md("## Group 4 · graph-tool\nType the code from your sheet into the cell below. The first run installs graph-tool and takes one to three minutes."),
        code("# type the code from your sheet\n"),
    ]


def main() -> None:
    ap = argparse.ArgumentParser()
    default_branch = subprocess.run(
        ["git", "-C", str(ROOT), "branch", "--show-current"], capture_output=True, text=True
    ).stdout.strip() or "main"
    ap.add_argument("--branch", default=default_branch,
                    help="branch the notebook's data URL points at (default: the current one)")
    ap.add_argument("--k", type=int, default=3, help="the notebook's starting value of K (nearest people per person)")
    args = ap.parse_args()
    nb = {
        "cells": cells(args.branch, args.k),
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
    print(f"wrote {out.relative_to(ROOT)} (data from branch {args.branch}, K = {args.k})")
    print(f"open in Colab: https://colab.research.google.com/github/{REPO}/blob/{args.branch}/{PATH}/pitch-seats.ipynb")


if __name__ == "__main__":
    main()

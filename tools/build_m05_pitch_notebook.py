#!/usr/bin/env python3
"""Write the M05 pitch notebook (Colab / Jupyter): community detection on the class's own seats.

    python tools/build_m05_pitch_notebook.py                 # write pitch-seats.ipynb
    python tools/build_m05_pitch_notebook.py --branch main   # the branch the data URL points at

In class the lecturer draws the seating on paper, reads off one (x, y) per
student and commits `seats.csv` next to the notebook. The notebook reads that
file from a fixed raw.githubusercontent.com address, joins people who sit close
(an epsilon-neighbourhood graph or a k-nearest-neighbour graph), and each of
four groups runs one community-detection method on that graph and pitches the
result. There is no ground truth: the point of the exercise is that the four
results differ and that each group can only defend its result from its own
definition of a community.

Group 4 runs graph-tool. condacolab only works in Colab, and the notebook may be
opened in any Jupyter, so graph-tool is installed the way the M05 pen-and-paper
lab does it (lecture-note/m05-clustering/pen-and-paper/lab.py): micromamba puts
it in a private conda environment in the temp folder and the fit runs there in
its own process. That needs no restart and works on Colab, Linux and macOS; there
is no graph-tool for Windows. The other groups never touch it.

The handout is lecture-note/m05-clustering/pitch/pitch-sheet.tex.
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


def code(text: str, title: str | None = None) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": text.strip("\n").splitlines(True),
    }


def cells(branch: str) -> list[dict]:
    raw = f"https://raw.githubusercontent.com/{REPO}/{branch}/{PATH}/seats.csv"
    return [
        md(r"""
# Pitch your result: communities among us

The lecturer has drawn where everyone in this room sits. Two people are joined by an edge when they sit close. That gives a network of about 15 nodes. Your group runs **one** community-detection method on it and has **three minutes** to say why its result is the one to trust.

There is no right answer to check against. You may only argue from your own method's definition of a community.

1. **Group 4 only:** run *Step A* now. It installs graph-tool and takes one to three minutes the first time. It works in Colab and in Jupyter on a Mac or Linux laptop. graph-tool does not run on Windows; use Colab there.
2. **Everyone:** run *Setup*, then *The graph*.
3. Go to the section with your group number. Run it, change the setting, run it again.
"""),
        md("## Step A · Group 4 only\nPress ▶ and wait. Nothing to type, and nothing restarts."),
        code("""
#@title Step A. Group 4 only. Press the play button and wait. { display-mode: "form" }
# graph-tool is not on PyPI, so it is installed from conda into a private folder, and the
# block-model fit runs there in its own process. blockmodel() is the bridge to it.
import io, json, os, pathlib, platform, subprocess, tarfile, tempfile, urllib.request

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

_SCRIPT = '''
import json
import numpy as np
import graph_tool.all as gt
d = json.load(open("in.json"))
g = gt.Graph(directed=False)
g.add_vertex(d["n"])
g.add_edge_list(d["edges"])
gt.seed_rng(d["seed"]); np.random.seed(d["seed"]); gt.openmp_set_num_threads(1)
kw = {} if d["n_groups"] is None else {"multilevel_mcmc_args": dict(B_min=d["n_groups"], B_max=d["n_groups"])}
state = gt.minimize_blockmodel_dl(g, state_args=dict(deg_corr=d["deg_corr"]), **kw)
json.dump({"labels": [int(b) for b in state.get_blocks().a], "dl": float(state.entropy())}, open("out.json", "w"))
'''


def blockmodel(n, edges, n_groups=None, deg_corr=False, seed=0):
    \"\"\"Fit graph-tool's stochastic block model. Returns (group of each person, description length).\"\"\"
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / "in.json").write_text(json.dumps(dict(n=n, edges=edges, n_groups=n_groups, deg_corr=deg_corr, seed=seed)))
        (tmp / "run.py").write_text(_SCRIPT)
        done = subprocess.run([GT_PYTHON, "run.py"], cwd=tmp, capture_output=True, text=True)
        if done.returncode:
            raise RuntimeError(done.stderr[-1500:])
        out = json.loads((tmp / "out.json").read_text())
    return out["labels"], out["dl"]


print("graph-tool is ready.")
"""),
        md("## Setup · everyone\nLoads the seat coordinates the lecturer published. Nothing to type."),
        code(f"""
#@title Setup. Press the play button. Nothing to type here. {{ display-mode: "form" }}
try:
    import igraph
except ImportError:
    %pip install -q python-igraph
    import igraph

import random
from itertools import combinations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# The lecturer replaces this file; the address stays the same.
SEATS_URL = "{raw}"

try:
    seats = pd.read_csv(SEATS_URL)
except Exception:
    # Rehearsal: the lecturer has not published the real seats yet.
    seats = pd.read_csv(SEATS_URL.replace("seats.csv", "seats-example.csv"))
    print("#" * 70)
    print("REHEARSAL DATA: seats.csv is not published yet, so this is an invented room.")
    print("Run this notebook again once the lecturer says the seats are up.")
    print("#" * 70)

IDS = list(seats["id"].astype(str))
P = seats[["x", "y"]].to_numpy(dtype=float)
N = len(IDS)
DIST = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
print(f"{{N}} people. Distances are in seat widths. Closest pair: {{np.min(DIST[np.triu_indices(N, 1)]):.2f}}, farthest pair: {{DIST.max():.2f}}.")
"""),
        code("""
#@title Helpers. Nothing to edit here. { display-mode: "form" }
PALETTE = ["#3959A6", "#B14434", "#DAB167", "#6B6B6B", "#7A5195", "#E377C2", "#8C564B", "#6BAED6", "#1A1A1A", "#BDB8AA"]


def build_graph(kind, k, eps):
    \"\"\"kind "knn": join each person to their k nearest people (an edge is kept if either end chose it).
    kind "eps": join two people when their distance is at most eps.
    eps=None: use the smallest eps at which nobody is without a neighbour.\"\"\"
    D = DIST.copy()
    np.fill_diagonal(D, np.inf)
    if kind == "knn":
        edges = {tuple(sorted((i, int(j)))) for i in range(N) for j in np.argsort(D[i], kind="stable")[:k]}
        used = None
    else:
        used = float(D.min(axis=1).max()) if eps is None else float(eps)
        edges = {(i, j) for i, j in combinations(range(N), 2) if D[i, j] <= used + 1e-9}
    return igraph.Graph(n=N, edges=sorted(edges)), used


def relabel(labels):
    seen = {}
    return [seen.setdefault(x, len(seen)) for x in labels]


def show(labels, title="", ax=None):
    \"\"\"Draw the room. Colour = group. Dashed line = an edge between two groups.\"\"\"
    lab = relabel(labels)
    own = ax is None
    if own:
        fig, ax = plt.subplots(figsize=(10, 4.2))
    for u, v in graph.get_edgelist():
        cross = lab[u] != lab[v]
        ax.plot([P[u, 0], P[v, 0]], [P[u, 1], P[v, 1]], color="#1A1A1A" if cross else "#BDB8AA",
                lw=1.2 if cross else 1.8, ls=(0, (4, 3)) if cross else "-", zorder=1)
    ax.scatter(P[:, 0], P[:, 1], s=420, c=[PALETTE[g % len(PALETTE)] for g in lab], edgecolor="#1A1A1A", lw=1, zorder=2)
    for i in range(N):
        ax.text(P[i, 0], P[i, 1], IDS[i], ha="center", va="center", fontsize=9, fontweight="bold",
                color="white" if lab[i] in (0, 1, 3, 4, 8) else "#1A1A1A", zorder=3)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.margins(0.08)
    ax.set_title(title, loc="left", fontsize=11, fontweight="bold")
    if own:
        plt.show()
    k = max(lab) + 1
    q = graph.modularity(lab) if graph.ecount() else float("nan")
    between = sum(lab[u] != lab[v] for u, v in graph.get_edgelist())
    if own:
        print(f"{k} group{'s' if k != 1 else ''}   modularity Q = {q:.4f}   {between} of {graph.ecount()} edges run between groups")
        print(pd.DataFrame({"group": range(1, k + 1),
                            "people": [sum(g == c for g in lab) for c in range(k)],
                            "members": [", ".join(IDS[i] for i in range(N) if lab[i] == c) for c in range(k)]}).to_string(index=False))


def cut_labels(kind):
    \"\"\"Best two-way split under `kind` ("cut", "ratio", "normalized"). "cut" is exact (igraph).
    The other two are searched: sweep along the second eigenvector of the Laplacian, then move
    one person at a time while the score improves. People with no neighbour cannot be split;
    they are returned as a group of their own.\"\"\"
    A = np.array(graph.get_adjacency().data, dtype=float)
    d = A.sum(axis=1)
    alone = np.where(d == 0)[0]
    keep = np.where(d > 0)[0]
    a, dk = A[np.ix_(keep, keep)], d[keep]
    n = len(keep)

    def score(S):
        k = int(S.sum())
        if k in (0, n):
            return np.inf
        c = a[S][:, ~S].sum()
        if kind == "cut":
            return c
        if kind == "ratio":
            return c / (k * (n - k))
        return c / (dk[S].sum() * dk[~S].sum())

    if kind == "ratio":
        f = np.linalg.eigh(np.diag(dk) - a)[1][:, 1]
    else:
        f = np.linalg.eigh(np.eye(n) - a / np.sqrt(np.outer(dk, dk)))[1][:, 1] / np.sqrt(dk)
    order = np.argsort(f)
    best, bestS = np.inf, None
    for i in range(1, n):
        S = np.zeros(n, dtype=bool)
        S[order[:i]] = True
        if score(S) < best:
            best, bestS = score(S), S.copy()
    moved = True
    while moved:
        moved = False
        for i in range(n):
            T = bestS.copy()
            T[i] = ~T[i]
            if score(T) < best - 1e-15:
                best, bestS, moved = score(T), T, True
    labels = [2] * N
    for pos, i in enumerate(keep):
        labels[i] = int(bestS[pos])
    return labels, best


def rand_agreement(a, b):
    \"\"\"Of all pairs of people, the share that both partitions treat the same way
    (together in both, or apart in both).\"\"\"
    pairs = list(combinations(range(N), 2))
    return sum((a[i] == a[j]) == (b[i] == b[j]) for i, j in pairs) / len(pairs)
"""),
        md(r"""
## The graph · everyone
Two ways to join people who sit close:

- **$k$-nearest-neighbour graph** (`"knn"`): each person is joined to their $k$ nearest people.
- **$\varepsilon$-neighbourhood graph** (`"eps"`): two people are joined when their distance is at most $\varepsilon$ (in seat widths). `EPS = None` takes the smallest $\varepsilon$ at which nobody is left without a neighbour.

Both are choices, and they change the network. Your group may change them; say which you used when you pitch.
"""),
        code("""
GRAPH = "eps"   # "knn" or "eps"
K = 3           # used when GRAPH = "knn"
EPS = None      # used when GRAPH = "eps". None, or a number such as 2.5

graph, eps_used = build_graph(GRAPH, K, EPS)
comps = graph.connected_components().membership
show(comps, f"{GRAPH} graph" + (f", eps = {eps_used:.2f}" if eps_used else f", k = {K}"))
print("\\nWith no method applied: every connected piece has its own colour.")
"""),
        md(r"""
## Group 1 · Shape
**Definition.** A community is a set of people who are all linked to one another through the graph, with nobody outside linked to them. A *clique* is a set in which everyone is joined to everyone else.

The groups are the connected pieces of the graph. Whether the pieces are meaningful depends on the graph above: change `GRAPH`, `K` or `EPS` there and run that cell again.
"""),
        code("""
labels_1 = graph.connected_components().membership
show(labels_1, "Group 1 · connected pieces")
cliques = [sorted(IDS[i] for i in c) for c in graph.maximal_cliques(min=3)]
print(f"Maximal cliques with at least 3 people: {len(cliques)}")
for c in cliques:
    print("  ", ", ".join(c))
"""),
        md(r"""
## Group 2 · Cut
**Definition.** A community is one side of a split into two. The split is scored by its *cut*, the number of edges between the sides, $\text{Cut}(V_1,V_2)=\sum_{i\in V_1}\sum_{j\in V_2}A_{ij}$, divided by a term for the size of the sides so that peeling off one person does not win. Ratio cut divides by $|V_1||V_2|$, normalized cut by $\text{vol}(V_1)\text{vol}(V_2)$.

The ratio and normalized objectives are searched, so the result is the best found, not a proof of the best. If the graph has several connected pieces, a cut of 0 exists (put whole pieces on either side) and the search returns one of them.
"""),
        code("""
OBJECTIVE = "normalized"   # "cut", "ratio" or "normalized"

labels_2, value = cut_labels(OBJECTIVE)
show(labels_2, f"Group 2 · {OBJECTIVE} cut, score {value:.4g}")
"""),
        md(r"""
## Group 3 · Chance
**Definition.** A community is a set of people with more edges inside it than a random network with the same degrees would put there. Modularity is $Q=\frac{1}{2m}\sum_{ij}\left[A_{ij}-\frac{k_ik_j}{2m}\right]\delta(c_i,c_j)$, and the algorithm searches for the grouping with the highest $Q$. The number of groups is not given; the score chooses it.

Louvain and Leiden start from a random order of people, so the seed can change the answer.
"""),
        code("""
ALGORITHM = "leiden"   # "leiden" or "louvain"
SEED = 0

random.seed(SEED)
part = (graph.community_leiden(objective_function="modularity", n_iterations=-1) if ALGORITHM == "leiden"
        else graph.community_multilevel())
labels_3 = part.membership
show(labels_3, f"Group 3 · {ALGORITHM}, seed {SEED}")

qs = []
for s in range(20):
    random.seed(s)
    p = (graph.community_leiden(objective_function="modularity", n_iterations=-1) if ALGORITHM == "leiden"
         else graph.community_multilevel())
    qs.append((round(p.modularity, 4), len(p)))
print(f"Over seeds 0-19: Q from {min(q for q, _ in qs)} to {max(q for q, _ in qs)}; number of groups: {sorted(set(n for _, n in qs))}")
"""),
        md(r"""
## Group 4 · Pattern (graph-tool)
**Definition.** A community is a set of people who connect to every group in the same way. Each pair of people is joined with a probability that depends only on the two people's groups (the *stochastic block model*). graph-tool chooses the grouping that gives the shortest description of the network: the description of the model plus the description of the edges given the model. A group is only kept if it pays for itself.

`N_GROUPS = None` lets graph-tool choose the number of groups. If it answers with one group, the fit found no structure worth describing at this size; set `N_GROUPS` to a number to force it, and say so when you pitch. `DEG_CORR = True` lets every person have their own degree.
"""),
        code("""
N_GROUPS = None     # None: graph-tool chooses. Or 2, 3, ...
DEG_CORR = False
SEED = 0

labels_4, dl = blockmodel(N, graph.get_edgelist(), N_GROUPS, DEG_CORR, SEED)
show(labels_4, f"Group 4 · block model, description length {dl:.1f}")
"""),
        md("""
## After the pitches · everyone
Runs all four methods with the settings above. The table gives, for each pair of results, the share of the pairs of people that both results treat the same way (together in both, or apart in both). 1 means identical.
"""),
        code("""
results = {}
results["1 · pieces"] = graph.connected_components().membership
results["2 · normalized cut"] = cut_labels("normalized")[0]
random.seed(0)
results["3 · Leiden"] = graph.community_leiden(objective_function="modularity", n_iterations=-1).membership
try:
    results["4 · block model"] = blockmodel(N, graph.get_edgelist())[0]
except NameError:
    print("Step A has not been run here, so the block model is missing; ask group 4 for their result.")

fig, axes = plt.subplots(2, 2, figsize=(14, 6.5))
for ax, (name, lab) in zip(axes.ravel(), results.items()):
    show(lab, f"{name}: {max(relabel(lab)) + 1} group{'s' if max(relabel(lab)) else ''}", ax=ax)
for ax in axes.ravel()[len(results):]:
    ax.axis("off")
plt.tight_layout(); plt.show()

names = list(results)
print(pd.DataFrame([[rand_agreement(results[a], results[b]) for b in names] for a in names],
                   index=names, columns=names).round(2).to_string())
"""),
    ]


def main() -> None:
    ap = argparse.ArgumentParser()
    default_branch = subprocess.run(
        ["git", "-C", str(ROOT), "branch", "--show-current"], capture_output=True, text=True
    ).stdout.strip() or "main"
    ap.add_argument("--branch", default=default_branch,
                    help="branch the notebook's data URL points at (default: the current one)")
    args = ap.parse_args()
    nb = {
        "cells": cells(args.branch),
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
    print(f"wrote {out.relative_to(ROOT)} (data from branch {args.branch})")
    print(f"open in Colab: https://colab.research.google.com/github/{REPO}/blob/{args.branch}/{PATH}/pitch-seats.ipynb")


if __name__ == "__main__":
    main()

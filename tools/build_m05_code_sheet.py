#!/usr/bin/env python3
"""Build the M05 code sheet's two halves from one list of boxes.

    python tools/build_m05_code_sheet.py          # notebooks + the sheet's boxes
    python tools/build_m05_code_sheet.py --test   # also run the worked notebook
    python tools/build_m05_code_sheet.py --answers  # run it and keep the results in it

The code sheet is a paper handout, separate from the pen-and-paper exercise. A
student types each framed box of code from the paper into the matching empty
cell of a Colab notebook, and looks at what comes out. The sheet is about how to
use the tools (igraph's Leiden, graph-tool's stochastic block model): its main
network is Zachary's karate club, and the US airports are for whoever finishes
early.

The paper and the notebook must say the same code, so both are written from BOXES
below:

  * boxes/boxN.tex            the framed code and the line-by-line notes, which
                              code-sheet.tex \\input's.
  * colab-lab.ipynb           what the student opens: three setup cells that are
                              only run, then one empty cell per box.
  * colab-lab-solutions.ipynb the same with every box typed in. --test runs it;
                              --answers runs it and saves the results into the file, so
                              that the answers can be read without a Colab runtime.

Everything the student does not type -- the install, the data, and the drawing
functions `show` and `show_map` -- is in the three setup cells, so that no
spell-like step stands between a student and the code on the paper.

Why graph-tool is installed with condacolab. graph-tool is a C++ library that
conda packages and pip does not. In Colab's own Python it cannot be imported: its
C++ runtime is newer than the system one (measured on molab, the same kind of
machine: GLIBCXX_3.4.36 not found). condacolab installs conda and restarts the
runtime onto conda's Python, which carries a new enough runtime, so after one
restart `import graph_tool.all as gt` is an ordinary import and the student types
ordinary code. The restart is why Setup 1 is its own cell.
"""

from __future__ import annotations

import base64
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHEET = ROOT / "lecture-note" / "m05-clustering" / "code-sheet"
LAB_PY = ROOT / "lecture-note" / "m05-clustering" / "pen-and-paper" / "lab.py"

# ---------------------------------------------------------------------------
# The boxes. `code` is exactly what the student types. `notes` explain it line
# by line, in LaTeX, for the paper: (lines, text) where lines is "3" or "2--3".
# ---------------------------------------------------------------------------
BOXES = [
    dict(
        id="karate",
        title="Build the karate club network",
        code='''import igraph as ig
karate = ig.Graph.Famous("Zachary")
print(karate.vcount(), karate.ecount())''',
        notes=[
            ("1", r"\texttt{import} loads a library: a bundle of ready-made tools. \texttt{igraph} is a library for building and studying networks. \texttt{as ig} gives it the short name \texttt{ig}, so that we type less."),
            ("2", r"\texttt{ig.Graph.Famous("+'"Zachary"'+r")} builds a network that igraph already knows: Zachary's karate club, 34 members, two of them linked when they were friends outside the club. The \texttt{=} stores the network under the name \texttt{karate}."),
            ("3", r"\texttt{vcount()} counts the nodes (the members) and \texttt{ecount()} counts the edges (the friendships). \texttt{print} shows both. You should see \texttt{34 78}."),
        ],
    ),
    dict(
        id="leiden",
        title="Find communities with Leiden",
        code='''result = karate.community_leiden("modularity", n_iterations=-1)
leiden = result.membership
print(leiden)''',
        notes=[
            ("1", r"\texttt{community\_leiden} runs the Leiden algorithm. It looks for \emph{communities}: groups with many friendships inside and few between groups. \texttt{"+'"modularity"'+r"} is the score it tries to raise: how much denser the groups are than in a random network. \texttt{n\_iterations=-1} means keep improving until nothing changes. What it returns is stored as \texttt{result}."),
            ("2", r"\texttt{result.membership} is the answer as a plain list: entry $i$ is the group number of node $i$. We store it as \texttt{leiden}."),
            ("3", r"Print the list. You should see 34 numbers. Two nodes with the same number are in the same group. The numbers are only labels, and Leiden uses chance, so your list may differ from your neighbour's."),
        ],
    ),
    dict(
        id="sbm",
        title="The stochastic block model, with graph-tool",
        code='''import graph_tool.all as gt
gt.seed_rng(1)
g = gt.Graph(directed=False)
g.add_edge_list(karate.get_edgelist())
state = gt.minimize_blockmodel_dl(g, state_args=dict(deg_corr=False))
sbm = state.get_blocks().a
print(sbm)''',
        notes=[
            ("1", r"graph-tool is a second library. It fits the stochastic block model, which you know from the lecture. \texttt{as gt} is its short name."),
            ("2", r"The fit makes random choices. \texttt{seed\_rng(1)} fixes them, so that everyone in the room gets the same answer. Change the \texttt{1} and you may get a different grouping."),
            ("3", r"graph-tool cannot read igraph's networks. It has its own kind, so we start with an empty one. \texttt{directed=False} says that a friendship goes both ways."),
            ("4", r"\texttt{karate.get\_edgelist()} asks igraph for all the friendships as pairs of node numbers. \texttt{add\_edge\_\allowbreak list} hands the pairs to graph-tool, which creates the nodes and the edges. This line is the only bridge between the two libraries."),
            ("5", r"\texttt{minimize\_blockmodel\_dl} fits the stochastic block model. \texttt{dl} stands for \emph{description length}: of all the ways to group the nodes, it picks the one that describes the network in the fewest bits. It decides the number of groups too. \texttt{state\_args=dict(deg\_corr=False)} asks for the plain model of the lecture, where the group alone decides how likely a friendship is. Graph-tool's default lets every member also have a number of friends of their own; on a network this small, that version finds one single group, which tells us nothing. The fitted model is stored as \texttt{state}."),
            ("6", r"\texttt{state.get\_blocks()} gives the group of each node, in graph-tool's own array type. \texttt{.a} turns it into a plain array of numbers, like the list in Box 2."),
            ("7", r"Print it: again one number for each of the 34 nodes."),
        ],
    ),
    dict(
        id="show",
        title="Put the results side by side",
        code='''show(karate, Real=club, Leiden=leiden, SBM=sbm)''',
        notes=[
            ("1", r"\texttt{show} was written for you in the notebook's setup. It draws the karate club once for each grouping you give it. The word before each \texttt{=} is the title printed on the picture. Each of the four biggest groups has a colour and a shape of its own, and the circles are bigger for members with more friends. Under each drawing is the adjacency matrix, with the members listed group by group: its black squares are friendships, and the strip along its top and left edges has the colour of each group. \texttt{club} is ready-made too: who really joined which side when the club split in two."),
        ],
    ),
    dict(
        id="circle",
        title="Draw the groups on a circle",
        code='''import matplotlib.pyplot as plt
import numpy as np
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
for ax, name, groups in zip(axes, ["Leiden", "SBM"], [leiden, sbm]):
    layout = karate.layout_circle(order=np.argsort(groups))
    ig.plot(
        karate, target=ax, layout=layout,
        vertex_color=colors_of(groups),
        vertex_shape=shapes_of(groups),
        vertex_label=karate.vs.indices,
        vertex_label_color="white",
        edge_color="lightgray",
    )
    group_legend(ax, groups)
    ax.set_title(name)
plt.show()''',
        notes=[
            ("1--2", r"\texttt{matplotlib} is Python's drawing library, and \texttt{numpy} is a library for lists of numbers. \texttt{plt} and \texttt{np} are their usual short names."),
            ("3", r"\texttt{plt.subplots(1, 2, ...)} makes one picture with two panels side by side (1 row, 2 columns), 10 inches wide and 5 tall. \texttt{fig} is the whole picture and \texttt{axes} holds the two panels."),
            ("4", r"A loop: the indented lines run twice, once for each panel. \texttt{zip} walks through three lists together. The first time round, \texttt{ax} is the first panel, \texttt{name} is \texttt{"+'"Leiden"'+r"} and \texttt{groups} is the list from Box 2; the second time, the SBM's."),
            ("5", r"\texttt{np.argsort(groups)} lists the node numbers sorted by group, so nodes of one group sit together. \texttt{layout\_circle(order=...)} puts the nodes on a circle in that order: each group takes one arc. The layout holds a position for every node."),
            ("6--13", r"\texttt{ig.plot} draws the network into the panel \texttt{ax}, at the positions in \texttt{layout}. \texttt{vertex\_color} and \texttt{vertex\_shape} give each node the colour and the shape of its group, so that a group never depends on colour alone (\texttt{colors\_of} and \texttt{shapes\_of} were written for you); \texttt{vertex\_label} writes the node's number inside it, in white (\texttt{karate.vs.indices} is the list of node numbers); \texttt{edge\_color} draws the friendships in light grey. Each line ends with a comma."),
            ("14", r"\texttt{group\_legend} (written for you) adds a key under the panel: the marker and the size of each group."),
            ("15--16", r"\texttt{ax.set\_title(name)} writes the title above the panel, and \texttt{plt.show()} shows the finished picture."),
        ],
    ),
    dict(
        id="airports",
        title="The same recipe on the US airports",
        code='''result_air = g_air.community_leiden("modularity", n_iterations=-1)
leiden_air = result_air.membership
g2 = gt.Graph(directed=False)
g2.add_edge_list(g_air.get_edgelist())
state2 = gt.minimize_blockmodel_dl(g2, state_args=dict(deg_corr=False))
sbm_air = state2.get_blocks().a
show_map(Leiden=leiden_air, SBM=sbm_air)''',
        notes=[
            ("1--2", r"Box 2 again. Only the network changed: \texttt{g\_air} is the US airport network (540 airports, two linked when a flight connects them), already built for you."),
            ("3--4", r"Box 3, lines 3 and 4, again, with a new graph-tool network called \texttt{g2}."),
            ("5--6", r"Box 3, lines 5 and 6, again. Nothing is printed this time, because 540 numbers are too many to read."),
            ("7", r"\texttt{show\_map} is the airport version of \texttt{show}: the airports on a map of the US, coloured by group, next to the matrix. Each of the four biggest groups is named on the map by its busiest airport."),
        ],
    ),
]

# ---------------------------------------------------------------------------
# The three setup cells. 1 and 2 are Colab-only (the notebook is not run
# with them in the local test); 3 is plain Python.
# ---------------------------------------------------------------------------
SETUP_1 = '''# Setup 1 of 3. Press the play button, then wait.
# Colab restarts by itself when this finishes. That is meant to happen.
!pip install -q condacolab
import condacolab
condacolab.install()'''

SETUP_2 = '''# Setup 2 of 3. Press the play button AFTER the restart. It takes a few minutes.
import condacolab
condacolab.check()
print("Installing graph-tool. This takes three to five minutes. Please wait.")
!mamba install -q -y -c conda-forge graph-tool python-igraph matplotlib
print("Done.")'''

SETUP_3 = r'''#@title Setup 3 of 3. Press the play button and wait for the tick. Nothing to type here.
import base64, json, math, random, zlib

import igraph
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle

# The airport data travels inside this notebook, so nothing is downloaded.
_DATA = json.loads(zlib.decompress(base64.b64decode("@@DATA@@")))

# Colour marks the group, and nothing else does. The four biggest groups take the two
# accents of the course figures (blue, vermillion) and two steps of ink, each with a
# marker shape of its own, so that no group is told apart by colour alone; every other
# group is light grey, "the rest". Blue and vermillion pass the all-pairs colour checks
# (dataviz validate_palette.js, on white): worst colour-blind separation 21.9, normal
# vision 31.2. Ink and grey carry no hue, so those checks do not apply to them.
INK, INK2, INK3 = "#1a1a1a", "#767676", "#bdbdbd"
TEXT, AXIS = "#52514e", "#c3c2b7"
STYLES = [  # colour, matplotlib marker, igraph shape: for each of the four biggest groups
    ("#0072b2", "o", "circle"),
    ("#d55e00", "s", "rectangle"),
    (INK, "^", "triangle-up"),
    (INK2, "D", "diamond"),
]
REST = (INK3, "o", "circle")
plt.rcParams.update({"figure.dpi": 100, "font.size": 9, "text.color": INK,
                     "axes.edgecolor": AXIS, "axes.labelcolor": INK})

# Who joined which side when the karate club split: 0 = Mr. Hi, 1 = the Officer.
_OFFICER = {9, 14, 15, 18, 20, 22, *range(23, 34)}
club = [1 if i in _OFFICER else 0 for i in range(34)]

# The US airport network: 540 airports, two linked when a flight connects them.
AIRPORTS = _DATA["airports"]  # [code, city, latitude, longitude]
g_air = igraph.Graph(n=len(AIRPORTS), edges=_DATA["edges"])


def _groups(blocks):
    """Number the groups 0, 1, 2 ... from the biggest. Returns the group number of
    each node, and the group sizes, biggest first."""
    blocks = np.asarray(blocks)
    ids, sizes = np.unique(blocks, return_counts=True)
    ranked = ids[np.argsort(-sizes, kind="stable")]
    rank = {b: k for k, b in enumerate(ranked)}
    return np.array([rank[b] for b in blocks]), np.sort(sizes)[::-1]


def _style(k):
    return STYLES[k] if k < len(STYLES) else REST


def colors_of(blocks):
    """The colour of the group each node is in, to draw with. The four biggest
    groups have a colour each; every other group is light grey."""
    return [_style(k)[0] for k in _groups(blocks)[0]]


def shapes_of(blocks):
    """The shape of the group each node is in, to draw with: one for each of the four
    biggest groups, so that colour is never the only way to tell them apart."""
    return [_style(k)[2] for k in _groups(blocks)[0]]


def group_legend(ax, blocks, shapes=True):
    """A key under a drawing: the marker and the size of each group. Every group
    past the fourth is counted together as "the rest"."""
    _, sizes = _groups(blocks)
    keys = []
    for k in range(min(len(sizes), len(STYLES))):
        color, marker, _ = STYLES[k]
        keys.append(ax.scatter([], [], marker=marker if shapes else "o", s=42, color=color,
                               label=f"group {k + 1}: {sizes[k]}"))
    if len(sizes) > len(STYLES):
        keys.append(ax.scatter([], [], marker="o", s=42, color=INK3,
                               label=f"the rest: {int(sizes[len(STYLES):].sum())}"))
    ax.legend(handles=keys, loc="upper center", bbox_to_anchor=(0.5, 0.03), ncol=len(keys),
              frameon=False, fontsize=8, labelcolor=TEXT, handletextpad=0.2, columnspacing=1.0)


def _matrix(ax, graph, number, title):
    """The adjacency matrix with the nodes listed group by group. The matrix is ink:
    the order already says which group is which. A thin strip in each group's colour
    along the top and the left links it to the drawing."""
    n = graph.vcount()
    degree = np.array(graph.degree())
    order = np.lexsort((-degree, number))
    place = np.empty(n, dtype=int)
    place[order] = np.arange(n)
    rows, cols = [], []
    for i, j in graph.get_edgelist():
        rows += [place[i], place[j]]
        cols += [place[j], place[i]]
    ax.scatter(cols, rows, s=max(1.3, 0.9 * (260 / n) ** 2), marker="s",
               linewidths=0, color=INK, rasterized=True)
    edges = np.concatenate([[0], np.cumsum(np.bincount(number))])
    width = max(1.2, 0.022 * n)
    for k in range(len(edges) - 1):
        length = edges[k + 1] - edges[k]
        color = _style(k)[0]
        ax.add_patch(Rectangle((-0.5 - 1.7 * width, edges[k] - 0.5), width, length,
                               color=color, linewidth=0, clip_on=False))
        ax.add_patch(Rectangle((edges[k] - 0.5, -0.5 - 1.7 * width), length, width,
                               color=color, linewidth=0, clip_on=False))
    for k in edges[1:-1]:
        ax.axvline(k - 0.5, color=INK3, lw=0.7)
        ax.axhline(k - 0.5, color=INK3, lw=0.7)
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(n - 0.5, -0.5)
    ax.set_aspect("equal")
    if n <= 40:
        ax.yaxis.tick_right()  # the strips take the left and the top
        ax.set_xticks(range(n), order, fontsize=5, rotation=90, color=TEXT)
        ax.set_yticks(range(n), order, fontsize=5, color=TEXT)
        ax.tick_params(length=0)
    else:
        ax.set_xticks([])
        ax.set_yticks([])
    for side in ax.spines.values():
        side.set_color(AXIS)
    ax.set_title(title, fontsize=9, loc="left", color=INK,
                 pad=6 + 2.7 * width * 260 / n)  # above the strip


def show(graph, **groupings):
    """Draw a small network once for each grouping, with its matrix under it.
    show(karate, Leiden=leiden): the word before = is the title of the picture."""
    where = np.array(graph.layout_kamada_kawai())  # the same picture every time
    degree = np.array(graph.degree())
    fig, axs = plt.subplots(2, len(groupings), figsize=(3.9 * len(groupings), 8.2), squeeze=False)
    for col, (name, blocks) in enumerate(groupings.items()):
        number, sizes = _groups(blocks)
        top = axs[0, col]
        for a, b in graph.get_edgelist():
            top.plot(*where[[a, b]].T, color=INK3, lw=0.8, zorder=1)
        for k in range(len(sizes) - 1, -1, -1):  # the rest first, the biggest group on top
            members = np.flatnonzero(number == k)
            color, marker, _ = _style(k)
            top.scatter(where[members, 0], where[members, 1], s=40 + 22 * degree[members],
                        marker=marker, color=color, edgecolors="white", linewidths=1.5, zorder=2)
        for v in np.argsort(-degree)[:2]:  # name the two best-connected members
            top.annotate(str(v), where[v], xytext=(0, 12), textcoords="offset points",
                         ha="center", fontsize=9, fontweight="bold", color=INK, zorder=3,
                         path_effects=[pe.withStroke(linewidth=2.4, foreground="white")])
        top.set_aspect("equal")
        top.axis("off")
        top.set_title(f"{name}: {len(sizes)} groups", fontsize=9, loc="left", color=INK)
        group_legend(top, blocks)
        _matrix(axs[1, col], graph, number, "the same nodes, group by group")
    fig.tight_layout()
    plt.show()


def _albers(lon, lat, lon0=-96.0, lat0=37.5, p1=29.5, p2=45.5):
    """The usual US map projection (Albers equal-area conic), done by hand."""
    lon, lat = np.radians(np.asarray(lon, float)), np.radians(np.asarray(lat, float))
    n = (math.sin(math.radians(p1)) + math.sin(math.radians(p2))) / 2
    c = math.cos(math.radians(p1)) ** 2 + 2 * n * math.sin(math.radians(p1))
    rho = np.sqrt(c - 2 * n * np.sin(lat)) / n
    rho0 = math.sqrt(c - 2 * n * math.sin(math.radians(lat0))) / n
    theta = n * (lon - math.radians(lon0))
    return rho * np.sin(theta), rho0 - rho * np.cos(theta)


_AIR_X, _AIR_Y = _albers([a[3] for a in AIRPORTS], [a[2] for a in AIRPORTS])


def _name_groups(ax, hubs):
    """Name each coloured group on the map by its busiest airport and its size,
    in the first spot around the airport where no earlier label is in the way."""
    renderer = ax.figure.canvas.get_renderer()
    taken = []
    spots = [(0, 10), (0, -16), (-30, 8), (30, 8), (-30, -14), (30, -14), (0, 26), (0, -32)]
    for hub, size in hubs:
        for dx, dy in spots:
            label = ax.annotate(
                f"{AIRPORTS[hub][0]} · {size}", (_AIR_X[hub], _AIR_Y[hub]),
                xytext=(dx, dy), textcoords="offset points", ha="center",
                fontsize=8, fontweight="bold", color=INK, zorder=5,
                path_effects=[pe.withStroke(linewidth=2.6, foreground="white")])
            box = label.get_window_extent(renderer)
            if not any(box.overlaps(other) for other in taken):
                taken.append(box)
                break
            label.remove()


def show_map(**groupings):
    """Airports on a map of the US, coloured by group, with the matrix beside it.
    show_map(Leiden=leiden_air): the word before = is the title of the picture."""
    graph = g_air
    degree = np.array(graph.degree())
    fig, axs = plt.subplots(len(groupings), 2, figsize=(8.6, 4.1 * len(groupings)),
                            gridspec_kw=dict(width_ratios=[1.5, 1]), squeeze=False)
    todo = []
    for (ax_map, ax_mat), (name, blocks) in zip(axs, groupings.items()):
        number, sizes = _groups(blocks)
        for ring in _DATA["states"]:
            x, y = _albers([p[0] for p in ring], [p[1] for p in ring])
            ax_map.plot(x, y, color=AXIS, lw=0.5, zorder=0)
        for k in range(len(sizes) - 1, -1, -1):  # the rest first, the biggest group on top
            members = np.flatnonzero(number == k)
            members = members[np.argsort(degree[members])]  # hubs on top
            ax_map.scatter(_AIR_X[members], _AIR_Y[members], s=7 + 3 * np.sqrt(degree[members]),
                           color=_style(k)[0], edgecolors="white", linewidths=0.5, zorder=3)
        ax_map.set_aspect("equal")
        ax_map.axis("off")
        ax_map.set_title(f"{name}: {len(sizes)} groups", fontsize=9, loc="left", color=INK)
        group_legend(ax_map, blocks, shapes=False)
        hubs = []
        for k in range(min(len(sizes), len(STYLES))):
            members = np.flatnonzero(number == k)
            hubs.append((members[np.argmax(degree[members])], len(members)))
        todo.append((ax_map, hubs))
        _matrix(ax_mat, graph, number, "the same airports, group by group")
    fig.tight_layout()
    fig.canvas.draw()
    for ax_map, hubs in todo:
        _name_groups(ax_map, hubs)
    plt.show()


try:
    import graph_tool
    print(f"✓ Ready. graph-tool {graph_tool.__version__}, igraph {igraph.__version__}.")
except ImportError:
    print("✗ graph-tool is not installed. Run Setup 2 again, or ask for help.")
'''


# ---------------------------------------------------------------------------
# Data and notebooks
# ---------------------------------------------------------------------------
def airport_blob() -> str:
    """The airports, as the lab packs them, cut down to what the sheet draws."""
    text = LAB_PY.read_text(encoding="utf-8")
    packed = re.search(r'LAB_DATA_B64 = "([^"]+)"', text).group(1)
    data = json.loads(zlib.decompress(base64.b64decode(packed)))
    keep = {k: data[k] for k in ("airports", "edges", "states")}
    raw = json.dumps(keep, separators=(",", ":")).encode()
    return base64.b64encode(zlib.compress(raw, 9)).decode("ascii")


def source(text: str) -> list[str]:
    lines = text.split("\n")
    return [l + "\n" for l in lines[:-1]] + [lines[-1]]


def cell(kind: str, text: str, n: int, **meta) -> dict:
    out = {"cell_type": kind, "id": f"c{n:02d}", "metadata": meta, "source": source(text)}
    if kind == "code":
        out |= {"execution_count": None, "outputs": []}
    return out


def notebook(solved: bool) -> dict:
    cells, n = [], 0

    def add(kind, text, **meta):
        nonlocal n
        cells.append(cell(kind, text, n, **meta))
        n += 1

    add("markdown", "# Lab · Find the blocks\n\n"
        "This notebook goes with the **code sheet**. First press ▶ on the three setup cells, in order. "
        "Then type each framed Box from the sheet into its empty cell and press ▶ (or Shift+Enter)."
        + ("\n\n*Worked copy: every box is typed in.*" if solved else ""))
    add("markdown", "## Setup 1 of 3\nThe first cell restarts Colab. That is meant to happen.")
    add("code", SETUP_1, tags=["colab-only"])
    add("markdown", "## Setup 2 of 3\nPress ▶ after the restart. It takes a few minutes.")
    add("code", SETUP_2, tags=["colab-only"])
    add("markdown", "## Setup 3 of 3\nPress ▶ and wait for the ✓.")
    add("code", SETUP_3.replace("@@DATA@@", airport_blob()), cellView="form")
    for k, box in enumerate(BOXES, 1):
        extra = "\n\n*If you have time.*" if box["id"] == "airports" else ""
        add("markdown", f"## Box {k} · {box['title']}\nType the code from Box {k} on your sheet.{extra}")
        add("code", box["code"] if solved else f"# Box {k}: type the code from your sheet here.")
    return {
        "cells": cells,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_notebooks() -> None:
    SHEET.mkdir(parents=True, exist_ok=True)
    for name, solved in (("colab-lab.ipynb", False), ("colab-lab-solutions.ipynb", True)):
        (SHEET / name).write_text(json.dumps(notebook(solved), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print("wrote", (SHEET / name).relative_to(ROOT))


# ---------------------------------------------------------------------------
# The sheet's boxes
# ---------------------------------------------------------------------------
def write_boxes() -> None:
    folder = SHEET / "boxes"
    folder.mkdir(parents=True, exist_ok=True)
    for k, box in enumerate(BOXES, 1):
        assert "\\end{codebox}" not in box["code"]
        lines = [
            "% GENERATED by tools/build_m05_code_sheet.py -- do not edit.",
            f"\\begin{{codebox}}{{Box {k}}}{{{box['title']}}}",
            box["code"],
            "\\end{codebox}",
            "\\begin{linenotes}",
            *[f"\\item[{label}] {text}" for label, text in box["notes"]],
            "\\end{linenotes}",
        ]
        (folder / f"box{k}.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", len(BOXES), "boxes in", folder.relative_to(ROOT))


# ---------------------------------------------------------------------------
# --test: run the worked notebook with graph-tool imported for real
# ---------------------------------------------------------------------------
def test() -> int:
    import nbformat
    from nbclient import NotebookClient

    nb = nbformat.read(SHEET / "colab-lab-solutions.ipynb", as_version=4)
    nb.cells = [c for c in nb.cells if "colab-only" not in c.metadata.get("tags", [])]
    NotebookClient(nb, kernel_name="gtenv", timeout=600).execute()
    shots = pathlib.Path(tempfile.gettempdir()) / "m05-code-sheet-shots"
    shots.mkdir(exist_ok=True)
    n = 0
    for c in nb.cells:
        if c.cell_type != "code":
            continue
        for out in c.outputs:
            if out.output_type == "stream":
                print(out.text.rstrip()[:300])
            elif out.output_type == "error":
                print("ERROR", out.ename, out.evalue)
                return 1
            elif "image/png" in out.get("data", {}):
                (shots / f"fig{n}.png").write_bytes(base64.b64decode(out.data["image/png"]))
                n += 1
    print(f"ran every cell; {n} pictures in {shots}")
    return 0


def answers() -> int:
    """Run the worked notebook here and keep what it printed and drew in the file.

    The two Colab-only setup cells are not run (they install conda); they stay in
    the file, empty of output, so that opened in Colab it runs as it always does.
    The results are from this machine's run: Leiden uses chance, so a run in Colab
    may count a group more or less.
    """
    import nbformat
    from nbclient import NotebookClient

    path = SHEET / "colab-lab-solutions.ipynb"
    full = nbformat.read(path, as_version=4)
    run = nbformat.v4.new_notebook(metadata=full.metadata)
    run.cells = [c for c in full.cells if "colab-only" not in c.metadata.get("tags", [])]
    NotebookClient(run, kernel_name="gtenv", timeout=600).execute()
    done = {c.id: c for c in run.cells}
    for c in full.cells:
        if c.id in done and c.cell_type == "code":
            c.outputs, c.execution_count = done[c.id].outputs, done[c.id].execution_count
    nbformat.validate(full)
    nbformat.write(full, path)
    saved = sum(1 for c in full.cells if c.cell_type == "code" and c.outputs)
    print(f"saved the results of {saved} cells into {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    write_notebooks()
    write_boxes()
    if "--test" in sys.argv:
        sys.exit(test())
    if "--answers" in sys.argv:
        sys.exit(answers())

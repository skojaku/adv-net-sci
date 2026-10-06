#!/usr/bin/env python3
"""Build the M05 code sheet's two halves from one list of boxes.

    python tools/build_m05_code_sheet.py          # notebooks + the sheet's boxes
    python tools/build_m05_code_sheet.py --test   # also run the worked notebook
    python tools/build_m05_code_sheet.py --answers  # run it and keep the results in it

The code sheet is a paper handout, separate from the pen-and-paper exercise. A
student types each framed box of code from the paper into the matching empty
cell of a Colab notebook, and looks at what comes out. The sheet is about how to
use the tools (igraph's Leiden, graph-tool's stochastic block model, and the
drawing functions of both): its main network is Zachary's karate club, and the US
airports are for whoever finishes early. Nothing is hidden behind a helper: the
student writes the drawing too, and the pictures are the libraries' own, not tidied
for comparison.

The paper and the notebook must say the same code, so both are written from BOXES
below:

  * boxes/boxN.tex            the framed code and the line-by-line notes, which
                              code-sheet.tex \\input's.
  * colab-lab.ipynb           what the student opens: three setup cells that are
                              only run, then one empty cell per box.
  * colab-lab-solutions.ipynb the same with every box typed in. --test runs it;
                              --answers runs it and saves the results into the file, so
                              that the answers can be read without a Colab runtime.

Everything the student does not type -- the install, and the data (the club's real
split, the airports and where they are) -- is in the three setup cells, so that no
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
            ("1", r"\texttt{import} loads a library: a bundle of ready-made tools. \texttt{igraph} is a library for building, studying and drawing networks. \texttt{as ig} gives it the short name \texttt{ig}, so that we type less."),
            ("2", r"\texttt{ig.Graph.Famous("+'"Zachary"'+r")} builds a network that igraph already knows: Zachary's karate club. The \texttt{=} stores it under the name \texttt{karate}."),
            ("3", r"\texttt{vcount()} counts the nodes (the members) and \texttt{ecount()} counts the edges (the friendships). \texttt{print} shows both. You should see \texttt{34 78}."),
        ],
    ),
    dict(
        id="leiden",
        title="Find communities with Leiden, and draw them",
        code='''result = karate.community_leiden("modularity", n_iterations=-1)
leiden = result.membership
print(leiden)
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ig.plot(
    karate, target=ax,
    vertex_color=[palette[g] for g in leiden],
    vertex_shape=[shapes[g] for g in leiden],
    vertex_label=karate.vs.indices,
    vertex_label_color="white",
)
ax.set_title("Leiden")
plt.show()''',
        notes=[
            ("1", r"\texttt{community\_leiden} runs the Leiden algorithm. It looks for \emph{communities}: groups with many friendships inside and few between groups. \texttt{"+'"modularity"'+r"} is the score it tries to raise: how much denser the groups are than in a random network. \texttt{n\_iterations=-1} means keep improving until nothing changes. What it returns is stored as \texttt{result}."),
            ("2", r"\texttt{result.membership} is the answer as a plain list: entry $i$ is the group number of node $i$. We store it as \texttt{leiden}."),
            ("3", r"Print the list. You should see 34 numbers. Two nodes with the same number are in the same group. The numbers are only labels, and Leiden uses chance, so your list may differ from your neighbour's."),
            ("4", r"\texttt{matplotlib.pyplot} is Python's library for drawing pictures. \texttt{plt} is its short name."),
            ("5", r"\texttt{plt.subplots()} makes an empty picture. \texttt{fig} is the picture and \texttt{ax} is the empty panel in it, which we draw into."),
            ("6--12", r"\texttt{ig.plot} is igraph's drawing function. It draws \texttt{karate} into the panel \texttt{ax}. \texttt{palette} and \texttt{shapes} are ready-made lists: group 0 is a blue circle, group 1 a vermillion square, and so on. \texttt{[palette[g] for g in leiden]} builds a list by looking up, for each group number \texttt{g} in \texttt{leiden}, the colour of that group: one colour for each node. \texttt{vertex\_shape} does the same with shapes, so that a group never depends on colour alone. \texttt{vertex\_label} writes each node's number on it (\texttt{karate.vs.indices} is the list 0 to 33), in white. Each line inside the brackets ends with a comma."),
            ("13--14", r"\texttt{ax.set\_title} writes the title above the panel, and \texttt{plt.show()} shows the picture."),
        ],
    ),
    dict(
        id="sbm",
        title="The stochastic block model, with graph-tool",
        code='''import graph_tool.all as gt
import numpy as np
gt.seed_rng(1)
g = gt.Graph(directed=False)
g.add_edge_list(karate.get_edgelist())
state = gt.minimize_blockmodel_dl(g, state_args=dict(deg_corr=False))
sbm = state.get_blocks().a
print(sbm)
groups = np.unique(sbm, return_inverse=True)[1]
colors = g.new_vertex_property("vector<double>")
for v in g.vertices():
    colors[v] = (*palette[groups[int(v)]], 1)
pos = gt.graph_draw(
    g,
    vertex_fill_color=colors,
    vertex_text=g.vertex_index,
)''',
        notes=[
            ("1", r"graph-tool is a second library. It fits the stochastic block model, which you know from the lecture. \texttt{as gt} is its short name."),
            ("2", r"\texttt{numpy} is a library for lists of numbers. \texttt{np} is its short name."),
            ("3", r"The fit makes random choices. \texttt{seed\_rng(1)} fixes them, so that everyone in the room gets the same answer. Change the \texttt{1} and you may get a different grouping."),
            ("4", r"graph-tool cannot read igraph's networks. It has its own kind, so we start with an empty one. \texttt{directed=False} says that a friendship goes both ways."),
            ("5", r"\texttt{karate.get\_edgelist()} asks igraph for all the friendships as pairs of node numbers. \texttt{add\_edge\_\allowbreak list} hands the pairs to graph-tool, which creates the nodes and the edges. This line is the only bridge between the two libraries."),
            ("6", r"\texttt{minimize\_blockmodel\_dl} fits the stochastic block model. \texttt{dl} stands for \emph{description length}: of all the ways to group the nodes, it picks the one that describes the network in the fewest bits. It decides the number of groups too. \texttt{state\_args=dict(deg\_corr=False)} asks for the plain model of the lecture, where the group alone decides how likely a friendship is. Graph-tool's default also lets every member have a number of friends of their own; on a network this small, that version finds one single group. The fitted model is stored as \texttt{state}."),
            ("7", r"\texttt{state.get\_blocks()} gives the group of each node, in graph-tool's own array type. \texttt{.a} turns it into a plain array of numbers, like the list in Box 2."),
            ("8", r"Print it: again one number for each of the 34 nodes."),
            ("9", r"graph-tool numbers its groups with gaps (say 15 and 32). \texttt{np.unique} with \texttt{return\_\allowbreak inverse=True} renumbers them 0, 1, 2, \ldots{} so that they fit the palette; the \texttt{[1]} picks that renumbered list."),
            ("10", r"graph-tool keeps what it knows about nodes in a \emph{property map}: a table with one value per node. This one will hold a list (red, green, blue) for each node."),
            ("11--12", r"A loop over the nodes \texttt{v} of the network. \texttt{groups[int(v)]} is the group of node \texttt{v} (\texttt{int} turns graph-tool's node object into its number), \texttt{palette[\ldots]} is the colour of that group, and \texttt{(*palette[\ldots], 1)} unpacks its red, green and blue and adds a 1 for fully opaque. The result goes into the table."),
            ("13--17", r"\texttt{gt.graph\_draw} is graph-tool's drawing function. \texttt{vertex\_fill\_color=colors} fills each node with its colour from the table, and \texttt{vertex\_text=g.vertex\_index} writes its number on it. The function hands back the position it gave each node; we keep that as \texttt{pos}, which also stops Colab from printing it under the picture."),
        ],
    ),
    dict(
        id="real",
        title="Draw what really happened",
        code='''fig, ax = plt.subplots()
ig.plot(
    karate, target=ax,
    vertex_color=[palette[g] for g in club],
    vertex_shape=[shapes[g] for g in club],
    vertex_label=karate.vs.indices,
    vertex_label_color="white",
)
ax.set_title("What really happened")
plt.show()''',
        notes=[
            ("1", r"A fresh empty panel, as in Box 2."),
            ("2--8", r"The drawing call of Box 2 again. The only change is the list of groups: \texttt{club} is ready-made, a \texttt{0} or a \texttt{1} for each member, for the side they joined when the club split in two."),
            ("9--10", r"A title, and show the picture."),
        ],
    ),
    dict(
        id="circle",
        title="Draw the groups on a circle",
        code='''layout = karate.layout_circle(order=np.argsort(leiden))
fig, ax = plt.subplots()
ig.plot(
    karate, target=ax, layout=layout,
    vertex_color=[palette[g] for g in leiden],
    vertex_shape=[shapes[g] for g in leiden],
    vertex_label=karate.vs.indices,
    vertex_label_color="white",
    edge_color="lightgray",
)
ax.set_title("Leiden, on a circle")
plt.show()''',
        notes=[
            ("1", r"\texttt{np.argsort(leiden)} lists the node numbers sorted by group, so that nodes of one group sit together. \texttt{layout\_circle(order=...)} puts the nodes on a circle in that order, so that each group takes one arc. The layout is a position for every node."),
            ("2", r"A fresh empty panel."),
            ("3--10", r"The drawing call of Box 2 again, with two additions: \texttt{layout=layout} uses our positions instead of igraph's own, and \texttt{edge\_color="+'"lightgray"'+r"} draws the friendships in light grey, so that they do not hide the nodes."),
            ("11--12", r"A title, and show the picture."),
        ],
    ),
    dict(
        id="airports_leiden",
        title="The US airports: Leiden, and a map",
        code='''import seaborn as sns
import pandas as pd
members = g_air.community_leiden("modularity", n_iterations=-1).membership
top = pd.Series(members).value_counts().index[:4]
sns.scatterplot(x=lon, y=lat, color="#bdbdbd", s=14)
sns.scatterplot(
    x=lon, y=lat, hue=members, hue_order=top, palette=palette[:4], s=14
)
plt.show()''',
        notes=[
            ("1--2", r"\texttt{seaborn} draws statistical pictures, and \texttt{pandas} works with tables. \texttt{sns} and \texttt{pd} are their usual short names."),
            ("3", r"Box 2, line 1, again, on the US airport network \texttt{g\_air} (540 airports, two linked when a flight connects them), which is ready-made. We keep the group of each airport as \texttt{members}."),
            ("4", r"\texttt{pd.Series(members).value\_counts()} counts how many airports each group has, biggest group first. \texttt{.index[:4]} keeps the numbers of the four biggest groups. We call them \texttt{top}."),
            ("5", r"\texttt{lon} and \texttt{lat} are the longitude and the latitude of each airport, also ready-made. \texttt{sns.\allowbreak scatterplot} puts one dot per airport at that place: a rough map of the US. This first call paints all of them light grey; \texttt{s=14} is the dot size."),
            ("6--8", r"The second call paints over the grey, but only the four groups in \texttt{top}: \texttt{hue=members} says that the colour follows the group, \texttt{hue\_order=top} limits it to those four, and \texttt{palette[:4]} is the first four colours of the palette. Every other airport stays light grey: it is ``the rest''."),
            ("9", r"Show the map."),
        ],
    ),
    dict(
        id="airports_sbm",
        title="The US airports: the block model, and a map",
        code='''g2 = gt.Graph(directed=False)
g2.add_edge_list(g_air.get_edgelist())
state2 = gt.minimize_blockmodel_dl(g2, state_args=dict(deg_corr=False))
members = state2.get_blocks().a
top = pd.Series(members).value_counts().index[:4]
sns.scatterplot(x=lon, y=lat, color="#bdbdbd", s=14)
sns.scatterplot(
    x=lon, y=lat, hue=members, hue_order=top, palette=palette[:4], s=14
)
plt.show()''',
        notes=[
            ("1--2", r"Box 3, lines 4 and 5, again, with a new graph-tool network called \texttt{g2}."),
            ("3", r"Box 3, line 6, again."),
            ("4", r"Box 3, line 7, again: the group of each airport, kept as \texttt{members}."),
            ("5--9", r"The map of the previous box, again, now coloured by the groups of the stochastic block model."),
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
!mamba install -q -y -c conda-forge graph-tool python-igraph matplotlib seaborn pandas
print("Done.")'''

SETUP_3 = r'''#@title Setup 3 of 3. Press the play button and wait for the tick. Nothing to type here.
import base64, json, zlib

import igraph
import seaborn as sns

sns.set_theme(style="white")  # a plain white background for every picture

# Colours and shapes for the groups, chosen by the course's figure rules: blue and
# vermillion (they stay apart for colour-blind readers too), then two steps of ink; the
# light grey is for "the rest". A shape goes with each colour, so that no group depends
# on colour alone.
palette = sns.color_palette(["#0072b2", "#d55e00", "#1a1a1a", "#767676", "#bdbdbd"])
shapes = ["circle", "rectangle", "triangle-up", "diamond", "circle"]

# The airport data travels inside this notebook, so nothing is downloaded.
_DATA = json.loads(zlib.decompress(base64.b64decode("@@DATA@@")))

# Who joined which side when the karate club split: 0 = Mr. Hi, 1 = the Officer.
_OFFICER = {9, 14, 15, 18, 20, 22, *range(23, 34)}
club = [1 if i in _OFFICER else 0 for i in range(34)]

# The US airport network: 540 airports, two linked when a flight connects them.
AIRPORTS = _DATA["airports"]  # [code, city, latitude, longitude]
g_air = igraph.Graph(n=len(AIRPORTS), edges=_DATA["edges"])
lon = [a[3] for a in AIRPORTS]  # where each airport is
lat = [a[2] for a in AIRPORTS]

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
    keep = {k: data[k] for k in ("airports", "edges")}
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
        extra = "\n\n*If you have time.*" if box["id"].startswith("airports") else ""
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

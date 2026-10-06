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
split and the airports) -- is in the three setup cells, so that no
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
import graph_tool.all as gt
karate = ig.Graph.Famous("Zachary")
g = gt.Graph(directed=False)
g.add_edge_list(karate.get_edgelist())
print(g.num_vertices(), g.num_edges())''',
        notes=[
            ("1", r"\texttt{import} loads a library: a bundle of ready-made tools. \texttt{igraph} is a library for networks. We use it for one thing only: Leiden. \texttt{as ig} is its short name."),
            ("2", r"\texttt{graph\_tool} is the main library of this sheet. It fits stochastic block models and draws networks. \texttt{as gt} is its short name."),
            ("3", r"\texttt{ig.Graph.Famous("+'"Zachary"'+r")} builds a network that igraph already knows: Zachary's karate club. The \texttt{=} stores it under the name \texttt{karate}."),
            ("4--5", r"graph-tool cannot read igraph's networks. It has its own kind, so we make an empty one (\texttt{directed=False} says that a friendship goes both ways) and fill it. \texttt{karate.get\_edgelist()} asks igraph for all the friendships as pairs of node numbers, and \texttt{add\_edge\_\allowbreak list} hands the pairs to graph-tool, which creates the nodes and the edges. This is the only bridge between the two libraries."),
            ("6", r"\texttt{num\_vertices()} counts the nodes (the members) and \texttt{num\_edges()} counts the edges (the friendships). You should see \texttt{34 78}."),
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
        id="paint",
        title="Draw the groups with graph-tool",
        code='''import numpy as np
def paint(groups):
    groups = np.unique(groups, return_inverse=True)[1]
    colors = g.new_vertex_property("vector<double>")
    for v in g.vertices():
        colors[v] = (*palette[groups[int(v)]], 1)
    return colors
pos = gt.graph_draw(
    g, vertex_fill_color=paint(leiden), vertex_text=g.vertex_index
)''',
        notes=[
            ("1", r"\texttt{numpy} is a library for lists of numbers. \texttt{np} is its short name."),
            ("2", r"We write a \emph{function}: a recipe we can use again. \texttt{paint} takes a list of group numbers and gives back a colour for every node. The lines indented under \texttt{def} are the recipe."),
            ("3", r"graph-tool numbers its groups with gaps (say 15 and 32). \texttt{np.unique} with \texttt{return\_\allowbreak inverse=True} renumbers them 0, 1, 2, \ldots{} so that they fit the palette; the \texttt{[1]} picks that renumbered list. (Leiden's numbers have no gaps, so for them it changes nothing.)"),
            ("4", r"graph-tool keeps what it knows about nodes in a \emph{property map}: a table with one value per node. This one will hold a list (red, green, blue) for each node. \texttt{palette} is a ready-made list of colours, one for each group."),
            ("5--6", r"A loop over the nodes \texttt{v} of the network. \texttt{groups[int(v)]} is the group of node \texttt{v} (\texttt{int} turns graph-tool's node object into its number), \texttt{palette[\ldots]} is the colour of that group, and \texttt{(*palette[\ldots], 1)} unpacks its red, green and blue and adds a 1 for fully opaque. The result goes into the table."),
            ("7", r"\texttt{return} hands the table back to whoever called \texttt{paint}."),
            ("8--10", r"\texttt{gt.graph\_draw} is graph-tool's drawing function. \texttt{vertex\_fill\_color=paint(leiden)} fills each node with the colour of its Leiden group, and \texttt{vertex\_text=g.vertex\_index} writes its number on it. The function hands back the position it gave each node; we keep it as \texttt{pos}, so that the next boxes can draw the nodes in the same places."),
        ],
    ),
    dict(
        id="sbm",
        title="The stochastic block model",
        code='''deg_corr = False
gt.seed_rng(1)
state = gt.minimize_blockmodel_dl(
    g, state_args=dict(deg_corr=deg_corr)
)
sbm = state.get_blocks().a
print(sbm)
pos = gt.graph_draw(
    g, pos=pos, vertex_text=g.vertex_index,
    vertex_fill_color=paint(sbm),
)''',
        notes=[
            ("1", r"This stores your choice of model under the name \texttt{deg\_corr}. \texttt{False} is the plain model of the lecture: the group alone decides how likely a friendship is, so the members of a group are alike in how many friends they have. \texttt{True} is the \emph{degree-corrected} model: every member may also have more or fewer friends than the others in the group. Change this one word later, to try the other model."),
            ("2", r"The fit makes random choices. \texttt{seed\_rng(1)} fixes them, so that everyone in the room gets the same answer. Change the \texttt{1} and you may get a different grouping."),
            ("3--5", r"\texttt{minimize\_blockmodel\_dl} fits the stochastic block model from the lecture. \texttt{dl} stands for \emph{description length}: of all the ways to group the nodes, it picks the one that describes the network in the fewest bits. It decides the number of groups too. \texttt{state\_args=dict(deg\_corr=deg\_corr)} hands your choice from line 1 to the model. The fitted model is stored as \texttt{state}."),
            ("6", r"\texttt{state.get\_blocks()} gives the group of each node, in graph-tool's own array type. \texttt{.a} turns it into a plain array of numbers, like the list in Box 2."),
            ("7", r"Print it: one number for each of the 34 nodes."),
            ("8--11", r"The drawing call of Box 3, with the colours of the block model's groups. \texttt{pos=pos} reuses the positions from Box 3, so that each node stays in the same place and the pictures can be compared."),
        ],
    ),
    dict(
        id="real",
        title="What really happened",
        code='''pos = gt.graph_draw(
    g, pos=pos, vertex_text=g.vertex_index,
    vertex_fill_color=paint(club),
)''',
        notes=[
            ("1--4", r"The same call once more, with \texttt{club}, which is ready-made: a \texttt{0} or a \texttt{1} for each member, for the side they joined when the club split in two."),
        ],
    ),
    dict(
        id="nested",
        title="A hierarchy of groups: the nested block model",
        code='''deg_corr = False
nested = gt.minimize_nested_blockmodel_dl(
    g, state_args=dict(deg_corr=deg_corr)
)
nested.print_summary()
groups = nested.get_bs()[0]
pos_tree = nested.draw(vertex_fill_color=paint(groups))''',
        notes=[
            ("1", r"Your choice of model, as in Box 4."),
            ("2--4", r"\texttt{minimize\_nested\_blockmodel\_dl} fits the \emph{nested} stochastic block model: the groups of nodes are themselves grouped into bigger groups, and those into still bigger ones, up to a single group. Everything else is as in Box 4. The result is stored as \texttt{nested}."),
            ("5", r"\texttt{print\_summary()} prints one line for each level of the hierarchy. For example \texttt{l: 0, N: 34, B: 2} says that level 0 has 34 nodes, put into 2 groups."),
            ("6", r"\texttt{nested.get\_bs()} gives the group of every node at every level, and \texttt{[0]} keeps the first level: the groups of the nodes themselves."),
            ("7", r"\texttt{nested.draw} draws the hierarchy on a circle: the nodes sit on the rim, the groups and the groups of groups are the squares inside, and the friendships bend along the hierarchy. \texttt{vertex\_fill\_color=paint(groups)} colours the nodes as in Box 3. It hands back positions; we keep them as \texttt{pos\_tree}."),
        ],
    ),
    dict(
        id="airports",
        title="The US airports: the hierarchy",
        code='''deg_corr = False
g2 = gt.Graph(directed=False)
g2.add_edge_list(g_air.get_edgelist())
nested_air = gt.minimize_nested_blockmodel_dl(
    g2, state_args=dict(deg_corr=deg_corr)
)
nested_air.print_summary()
pos_air = nested_air.draw()''',
        notes=[
            ("1", r"Your choice of model, as in Box 4."),
            ("2--3", r"Box 1, lines 4 and 5, again, with a new graph-tool network called \texttt{g2}. \texttt{g\_air} is the US airport network (540 airports, two linked when a flight connects them), already built for you."),
            ("4--6", r"Box 6, lines 2 to 4, again, on the airport network."),
            ("7", r"One line for each level of the hierarchy, as in Box 6."),
            ("8", r"The hierarchy on a circle. Without \texttt{vertex\_fill\_color}, graph-tool picks the colours itself; with this many groups, colour no longer says much, and the place on the circle does."),
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

# Colours for the groups, chosen by the course's figure rules: blue and vermillion (they
# stay apart for colour-blind readers too), then two steps of ink; the light grey is for
# "the rest". The node numbers in the pictures are the second channel.
palette = sns.color_palette(["#0072b2", "#d55e00", "#1a1a1a", "#767676", "#bdbdbd"])

# The airport data travels inside this notebook, so nothing is downloaded.
_DATA = json.loads(zlib.decompress(base64.b64decode("@@DATA@@")))

# Who joined which side when the karate club split: 0 = Mr. Hi, 1 = the Officer.
_OFFICER = {9, 14, 15, 18, 20, 22, *range(23, 34)}
club = [1 if i in _OFFICER else 0 for i in range(34)]

# The US airport network: 540 airports, two linked when a flight connects them.
AIRPORTS = _DATA["airports"]  # [code, city, latitude, longitude]
g_air = igraph.Graph(n=len(AIRPORTS), edges=_DATA["edges"])

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

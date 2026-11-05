#!/usr/bin/env python3
"""Write notebooks/m07-randomwalks/mini-project.py with the m07mini package embedded.

    python3 tools/embed_m07_mini.py

molab could not install m07mini from a git URL, so the data and the scoring function
sit in one hidden cell of the notebook. The package (notebooks/m07-randomwalks/m07mini)
stays the source: run tools/build_m07_mini_data.py first when the networks change, then
this script, then upload the notebook again.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG = ROOT / "notebooks" / "m07-randomwalks" / "m07mini" / "src" / "m07mini"
OUT = ROOT / "notebooks" / "m07-randomwalks" / "mini-project.py"

HEADER = '''# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6",
#     "pandas==2.3.1",
#     "scipy==1.15.3",
#     "scikit-learn==1.7.1",
# ]
# ///
#
# Mini project M07 -- design a community detection algorithm built on a random walk.
#
# The task, the requirements and the targets are on the paper handout
# (lecture-note/m07-random-walks/mini-project/handout.tex), not here. The notebook
# is a blank page with the data loaded and a scoring cell. The data and the scoring
# function sit in the hidden second cell. Do not edit that cell by hand: it is written
# by tools/embed_m07_mini.py from notebooks/m07-randomwalks/m07mini.

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    mo.md("# Mini project m07")
    return


@app.cell(hide_code=True)
def _():
    import base64
    import io
    import types
    import zlib

    import pandas as pd
    from sklearn.metrics import normalized_mutual_info_score

'''

FOOTER = '''

    def _table(name, table):
        text = zlib.decompress(base64.b64decode(_NETWORKS[name][table])).decode()
        return pd.read_csv(io.StringIO(text))


    def _load_edges():
        """Edge table of each network: columns source and target, one row per undirected edge."""
        return {name: _table(name, "edges") for name in _NETWORKS}


    def _load_groups():
        """Ground truth of each network: columns node and group."""
        return {name: _table(name, "groups") for name in _NETWORKS}


    def _evaluate(answer):
        """Normalized mutual information with the ground truth, per network."""
        unknown = sorted(set(answer) - set(_NETWORKS))
        if unknown:
            raise ValueError(f"unknown network {unknown}; the networks are {list(_NETWORKS)}")
        scores = {}
        for name, labels in answer.items():
            truth = _table(name, "groups")["group"].to_numpy()
            labels = list(labels)
            if len(labels) != len(truth):
                raise ValueError(f"{name}: expected {len(truth)} labels, got {len(labels)}")
            scores[name] = round(float(normalized_mutual_info_score(truth, labels)), 3)
        return scores


    m07mini = types.SimpleNamespace(
        load_edges=_load_edges, load_groups=_load_groups, evaluate=_evaluate
    )
    return (m07mini,)


@app.cell
def _(m07mini):
    edges = m07mini.load_edges()  # {"net1": DataFrame, "net2": ..., "net3": ...}
    groups = m07mini.load_groups()  # ground truth, same keys
    edges["net1"].head()
    return edges, groups


@app.cell
def _(edges, groups):
    # your code
    return


@app.cell
def _(m07mini):
    answer = {
        "net1": [0] * 800,  # one label per node: element i is the group of node i
        "net2": [0] * 800,
        "net3": [0] * 3169,
    }
    m07mini.evaluate(answer)
    return


if __name__ == "__main__":
    app.run()
'''


def main():
    ns = {}
    exec((PKG / "_data.py").read_text(), ns)
    networks = ns["NETWORKS"]
    lines = ["    _NETWORKS = {"]
    for name, d in networks.items():
        lines += [
            f"        {name!r}: {{",
            f"            'edges': {d['edges']!r},",
            f"            'groups': {d['groups']!r},",
            "        },",
        ]
    lines.append("    }")
    OUT.write_text(HEADER + "\n".join(lines) + FOOTER)
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

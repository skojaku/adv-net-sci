# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6",
#     "pandas==2.3.1",
#     "scipy==1.15.3",
#     "scikit-learn==1.7.1",
#     "m07mini @ git+https://github.com/skojaku/adv-net-sci@main#subdirectory=notebooks/m07-randomwalks/m07mini",
# ]
# ///
#
# Mini project M07 -- design a community detection algorithm built on a random walk.
#
# The task, the requirements and the targets are on the paper handout
# (lecture-note/m07-random-walks/mini-project/handout.tex), not here. The notebook
# is a blank page with the data loaded and a scoring cell. The data and the scoring
# function live in the package m07mini (notebooks/m07-randomwalks/m07mini), which
# tools/build_m07_mini_data.py writes. Fixing the scorer therefore needs no re-upload
# of this notebook.

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    mo.md("# Mini project m07")
    return


@app.cell
def _():
    import m07mini

    edges = m07mini.load_edges()  # {"net1": DataFrame, "net2": ..., "net3": ...}
    groups = m07mini.load_groups()  # ground truth, same keys
    edges["net1"].head()
    return edges, groups, m07mini


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

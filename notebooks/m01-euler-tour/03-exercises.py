# /// script
# dependencies = [
#     "matplotlib==3.10.3",
#     "numpy==2.3.2",
#     "pandas==2.3.1",
#     "python-igraph==0.11.9",
# ]
# [tool.marimo.display]
# default_width = "full"
# [tool.marimo.formatting]
# line_length = 120
# ///

import marimo

__generated_with = "0.14.13"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Exercises


    /// admonition | Running with Marimo

    You can run this notebook with Marimo. To do so, download the notebook (click `...` button on the top, then `Download` button) and use the following steps:

    ```bash
    marimo edit --sandbox <filename>.py
    ```

    The notebook will open in your web browser. All necessary packages will be installed automatically in a dedicated virtual environment managed by uv.
    ///



    ## Exercise 01

    1. Create a network of landmasses and bridges of Binghamton, NY.
    2. Find an Euler path that crosses all the bridges of Binghamton, NY exactly once.

    ![Binghamton Map](https://github.com/skojaku/adv-net-sci/raw/main/docs/lecture-note/figs/binghamton-map.jpg)
    """
    )
    return


@app.cell
def _():
    import numpy as np
    return (np,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Define the edges""")
    return


@app.cell
def _():
    _edges = ...
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Define the adjacnecy matrix (without for loops!)""")
    return


@app.cell
def _():
    A = ...
    return (A,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Visualize the graph""")
    return


@app.cell
def _(A, np):
    import igraph
    import matplotlib.pyplot as plt


    def visualize_graph(A, **params):
        A = np.array(A)
        src, trg = np.where(A)
        g = igraph.Graph(directed=False)
        g.add_vertices(A.shape[0])
        for s, t in zip(src, trg):
            for _ in range(A[s, t]):
                g.add_edge(s, t)

        fig, ax = plt.subplots()
        igraph.plot(g, target=ax, **params)
        return fig


    # This should work directly in marimo
    visualize_graph(A)
    return (visualize_graph,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Check if the graph has an Euler path and implement Euler's theorem""")
    return


@app.cell
def _(A, np):
    # TODO: Implement a function to check if a graph has an Euler path
    # Hint: Euler's theorem states that a graph has an Euler path if and only if:
    # - All nodes have even degree (Euler circuit), OR
    # - Exactly two nodes have odd degree (Euler path)


    def has_euler_path(degrees):
        """
        Check if a graph has an Euler path based on node degrees.
        Complete this function based on Euler's theorem.
        """
        # Your code here
        pass


    # Calculate degrees for Binghamton network
    degrees_binghamton = np.sum(A, axis=1)

    # Test your function
    # Your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ##  Exercise 02

    Let's create a network from pre-existing data and check if it has an Euler path.

    1. Select a network of your choice from [Netzschleuder](https://networks.skewed.de/). For convenience, choose a network of nodes less than 5000.
    2. Download the csv version of the data by clicking something like "3KiB" under `csv` column.
    3. Unzip the file and find "edges.csv", open it with a text editor to familiarize yourself with the format.
    4. Load the data using `pandas`.
    5. Get the source and target nodes from the data to create an edge list.
    6. Construct the adjacency matrix from the edge list.
    7. Draw the graph using `igraph`.
    8. Check if the graph has an Euler path.


    Load the data by
    """
    )
    return


@app.cell
def _():
    import pandas as pd

    df = ...  # pd.read_csv("edges.csv")  # load the data
    df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Then, get the srce and target nodes to compose an edge list""")
    return


@app.cell
def _():
    src = ...
    trg = ...
    _edges = ...
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Create the adjacency matrix from the edge list""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Get the degree of each node
    ```{code-cell} ipython3
    deg = ...
    ```

    Visualize the graph
    """
    )
    return


@app.cell
def _(A, visualize_graph):
    visualize_graph(A)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Check if the graph has an Euler path""")
    return


@app.cell
def _():
    # Use the has_euler_path function you implemented in Exercise 01
    # Your code here
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()

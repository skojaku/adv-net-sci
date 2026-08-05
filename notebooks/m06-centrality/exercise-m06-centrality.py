import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <a target="_blank" href="https://colab.research.google.com/github/skojaku/adv-net-sci/blob/main/notebooks/m06-centrality/exercise-m06-centrality.ipynb">
      <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
    </a>

    # Computing centrality with Python

    ## Network of university students

    Let's compute the centrality of the network using Python igraph.
    """)
    return


@app.cell
def _():
    # Uncomment if you use Colab
    # !sudo apt install libcairo2-dev pkg-config python3-dev
    # !pip install pycairo cairocffi
    # !pip install igraph
    return


@app.cell
def _():
    import igraph
    import numpy as np

    names = [
        "Sarah",
        "Mike",
        "Emma",
        "Alex",
        "Olivia",
        "James",
        "Sophia",
        "Ethan",
        "Ava",
        "Noah",
        "Lily",
        "Lucas",
        "Henry",
    ]
    edge_list = [
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 3),
        (3, 4),
        (3, 5),
        (3, 6),
        (4, 5),
        (6, 7),
        (6, 8),
        (6, 9),
        (7, 8),
        (7, 9),
        (8, 9),
        (9, 10),
        (9, 11),
        (9, 12),
    ]
    g = igraph.Graph()
    g.add_vertices(13)
    g.vs["name"] = names
    g.add_edges(edge_list)
    igraph.plot(g, vertex_label=g.vs["name"])
    return g, igraph, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `igraph` offers a wide range of centrality measures as methods of the `igraph.Graph` class.

    - **Degree centrality**: `igraph.Graph.degree()`
    - **Closeness centrality**: `igraph.Graph.closeness()`
    - **Betweenness centrality**: `igraph.Graph.betweenness()`
    - **Harmonic centrality**: `igraph.Graph.harmonic_centrality()`
    - **Eccentricity**: `igraph.Graph.eccentricity()`
    - **Eigenvector centrality**: `igraph.Graph.eigenvector_centrality()`
    - **PageRank centrality**: `igraph.Graph.personalized_pagerank()`

    For example, the closeness centrality is computed by
    """)
    return


@app.cell
def _(g):
    g.betweenness()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Computing Katz centrality

    Let's compute the Katz centrality without using igraph.
    Let us first define the adjacency matrix of the graph
    """)
    return


@app.cell
def _(g, np):
    A = g.get_adjacency_sparse()
    _alpha = 1
    _beta = 1
    _c = np.linalg.inv(np.eye(g.vcount()) - _alpha * A.T) @ np.ones((g.vcount(), 1)) * _beta
    _c
    return (A,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    which is the scipy CSR sparse matrix. The Katz centrality is given by

    $$

    \mathbf{c} = \beta \mathbf{1} + \alpha \mathbf{A} \mathbf{c}

    $$

    So, how do we solve this? We can use a linear solver but here we will use a simple method:

    1. Initialize $\mathbf{c}$ with a random vector.
    2. Compute the right hand side of the equation and update $\mathbf{c}$.
    3. Repeat the process until $\mathbf{c}$ converges.

    Let's implement this.
    """)
    return


@app.cell
def _(A, g, np):
    _alpha, _beta = (0.1, 0.05)
    _n_nodes = g.vcount()
    _c = np.random.rand(_n_nodes, 1)
    for _ in range(100):
        _c_next = _beta * np.ones((_n_nodes, 1)) + _alpha * A * _c
        if np.linalg.norm(_c_next - _c) < 1e-06:
            break
        _c = _c_next
    print(_c)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Does the centrality converge?
    - Change the hyperparameter and see how the result changes 😉
    If the centrality diverges, think about why it diverges.

    ### Exercise 01: PageRank centrality

    Compute the PageRank centrality of this graph
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    c_i = \frac{\beta}{N} + (1-\beta) \sum_j \frac{A_{ji}}{d^{\text{out}}_j} c_j
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    $$
    c = \beta \mathbf{1} + (1-\beta) \left(\mathbf{D}^{-1} \mathbf{A}\right)^\top \mathbf{c}
    $$
    where

    $$
    \mathbf{D} =
    \begin{bmatrix}
    d^{\text{out}}_1 & 0 & 0 & \cdots & 0 \\
    0 & d^{\text{out}}_2 & 0 & \cdots & 0 \\
    0 & 0 & d^{\text{out}}_3 & \cdots & 0 \\
    \vdots & \vdots & \vdots & \ddots & \vdots \\
    0 & 0 & 0 & \cdots & d^{\text{out}}_N \\
    \end{bmatrix}
    $$
    is the diagonal matrix of the out-degrees.
    """)
    return


@app.cell
def _(A, g, np):
    _beta = 0.25
    _deg = np.array(A.sum(axis=1)).flatten()
    D = np.diag(_deg)
    Dinv = np.diag(1.0 / _deg)
    P = Dinv @ A
    _n_nodes = g.vcount()
    _c = np.random.rand(_n_nodes, 1)
    for _ in range(100):
        _c_next = _beta * np.ones((_n_nodes, 1)) / _n_nodes + (1 - _beta) * P.T @ _c
        if np.linalg.norm(_c_next - _c) < 1e-06:
            break
        _c = _c_next
    print(_c)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Network of ancient Roman roads

    ### Load the data & construct the network
    """)
    return


@app.cell
def _():
    import pandas as pd

    root = "https://raw.githubusercontent.com/skojaku/adv-net-sci/main/data/roman-roads"
    node_table = pd.read_csv(f"{root}/node_table.csv")
    edge_table = pd.read_csv(f"{root}/edge_table.csv")
    return edge_table, node_table


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The node table:
    """)
    return


@app.cell
def _(node_table):
    node_table.head(3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The edge table:
    """)
    return


@app.cell
def _(edge_table):
    edge_table.head(3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's construct a network from the node and edge tables.
    """)
    return


@app.cell
def _(edge_table, igraph, node_table):
    src, trg = (edge_table['src'].values, edge_table['trg'].values)
    g_1 = igraph.Graph()
    g_1.add_vertices(node_table['node_id'].values)
    # Your code here
    g_1.add_edges(list(zip(src, trg)))  # create a graph from the edge list
    return (g_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    which looks like this:
    """)
    return


@app.cell
def _(g_1, igraph, node_table):
    _coord = list(zip(node_table['lon'].values, -node_table['lat'].values))
    igraph.plot(g_1, layout=_coord, vertex_size=5)
    return


@app.cell
def _(g_1, igraph, node_table, np):
    import seaborn as sns
    _coord = list(zip(node_table['lon'].values, -node_table['lat'].values))
    _deg = g_1.betweenness()
    palette = sns.color_palette('viridis', as_cmap=True)
    igraph.plot(g_1, layout=_coord, vertex_size=5, vertex_color=[palette(d / np.max(_deg)) for d in _deg])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 02 🏛️

    1. Compute the following centrality measures:
        - Degree centrality 🔢
        - Eigenvector centrality
        - PageRank centrality
        - Katz centrality
        - Betweenness centrality
        - Closeness centrality
    2. Plot the centrality measures on the map and see in which centrality Rome is the most important node. 🗺️🏛️ (as beautiful as possible!!)

    ### Exercise 03:

    A BCDE graph is a graph where the most central nodes in terms of:
    - (B) Betweenness centrality
    - (C) Closeness centrality
    - (D) Degree centrality
    - (E) Eccentricity

    are different. It is known that the smallest number of nodes of a BCDE graph is 10. Surely, it is challenging to find the smallest one. So, let's create a BCDE graph of nodes between 10 and 15 nodes. If possible, identify the smallest BCDE graph.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()

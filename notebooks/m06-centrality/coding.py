# /// script
# dependencies = [
#     "marimo",
#     "numpy",
#     "pandas",
#     "python-igraph",
# ]
# [tool.marimo.display]
# default_width = "full"
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    # Uncomment if you use Colab
    #!pip install igraph
    return


@app.cell
def _():
    import igraph

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
    return g, igraph


@app.cell
def _(g):
    g.closeness()
    return


@app.cell
def _(g):
    A = g.get_adjacency_sparse()
    return (A,)


@app.cell
def _(A, g):
    import numpy as np

    alpha, beta = 0.1, 0.05 # Hyperparameters
    n_nodes = g.vcount() # number of nodes
    c = np.random.rand(n_nodes, 1) # column random vector

    for _ in range(100):
        c_next = beta * np.ones((n_nodes, 1)) + alpha * A * c
        if np.linalg.norm(c_next - c) < 1e-6:
            break
        c = c_next
    print(c)
    return


@app.cell
def _():
    # Your code here
    return


@app.cell
def _():
    import pandas as pd

    root = "https://raw.githubusercontent.com/skojaku/adv-net-sci/main/data/roman-roads"
    node_table = pd.read_csv(f"{root}/node_table.csv")
    edge_table = pd.read_csv(f"{root}/edge_table.csv")
    return edge_table, node_table


@app.cell
def _(node_table):
    node_table.head(3)
    return


@app.cell
def _(edge_table):
    edge_table.head(3)
    return


@app.cell
def _(edge_table, igraph, node_table):
    g_1 = igraph.Graph()
    g_1.add_vertices(node_table['node_id'].values)
    g_1.add_edges(list(zip(edge_table['src'].values, edge_table['trg'].values)))  # create an empty graph  # add nodes  # add edges
    return (g_1,)


@app.cell
def _(g_1, igraph, node_table):
    coord = list(zip(node_table['lon'].values, -node_table['lat'].values))
    igraph.plot(g_1, layout=coord, vertex_size=5)
    return


if __name__ == "__main__":
    app.run()

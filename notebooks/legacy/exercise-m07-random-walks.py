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
    # Random Walks in Python

    ## Simulating Random Walks

    We will simulate random walks on a simple graph of five nodes as follows.
    """)
    return


@app.cell
def _():
    import numpy as np
    import igraph

    g = igraph.Graph()

    g.add_vertices([0, 1, 2, 3, 4])
    g.add_edges([(0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (2, 4), (3, 4)])
    igraph.plot(g, vertex_size=20, vertex_label=g.vs["name"])
    return g, igraph, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A random walk is characterized by the transition probabilities between nodes.

    $$
    P_{ij} = \frac{A_{ij}}{k_i}
    $$

    Let us first compute the transition probabilities and store them in a matrix, $\mathbf{P}$.
    """)
    return


@app.cell
def _(g, np):
    A = g.get_adjacency_sparse().toarray()
    _k = np.array(g.degree())
    n_nodes = g.vcount()
    P = np.zeros((n_nodes, n_nodes))
    # A simple but inefficient way to compute P
    for _i in range(n_nodes):
        for j in range(n_nodes):
            if _k[_i] > 0:
                P[_i, j] = A[_i, j] / _k[_i]
            else:
                P[_i, j] = 0
    P = A / _k[:, np.newaxis]
    # Alternative, more efficient way to compute P
    # or even more efficiently
    P = np.einsum('ij,i->ij', A, 1 / _k)
    return P, n_nodes


@app.cell
def _(P):
    print("Transition probability matrix:\n", P)
    return


@app.cell
def _(P):
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.heatmap(P, annot=True, cmap="YlGnBu")
    plt.show()
    return plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each row and column of $\mathbf{P}$ corresponds to a node, with entries representing the transition probabilities from the row node to the column node.

    Now, let us simulate a random walk on this graph. We represent a position of the walker by a vector, $\mathbf{x}$, with five elements, each of which represents a node. We mark the node that the walker is currently at by `1` and others as `0`.
    """)
    return


@app.cell
def _(np):
    x = np.array([0, 0, 0, 0, 0])
    x[0] = 1
    print("Initial position of the walker:\n", x)
    return (x,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This vector representation is convenient to get the probabilities of transitions to other nodes from the current node:

    $$
    \mathbf{x} \mathbf{P}
    $$

    which is translated into the following code:
    """)
    return


@app.cell
def _(P, x):
    probs = x @ P
    print("Position of the walker after one step:\n", probs)
    return (probs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can then draw the next node based on the probabilities
    """)
    return


@app.cell
def _(n_nodes, np, probs, x):
    next_node = np.random.choice(n_nodes, p=probs)
    x[:] = 0  # zero out the vector
    x[next_node] = 1  # set the next node to 1
    print("Position of the walker after one step:\n", x)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Expected behavior of random walks

    What is the expected position of the walker after multiple steps? It is easy to compute the expected position of the walker after one step from initial position $x(0)$:

    $$
    \mathbb{E}[x(1)] = x(0) P
    $$

    where $x(t)$ is the probability distribution of the walker at time $t$. In Python, the expected position of the walker at time $t=1$ is given by
    """)
    return


@app.cell
def _(P, np):
    _x_0 = np.array([1, 0, 0, 0, 0])
    x_1 = _x_0 @ P
    print('Expected position of the walker after one step:\n', x_1)
    return (x_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the second step, the expected position of the walker is given by

    $$
    \mathbb{E}[x(2)] = \mathbb{E}[x(1) P] = \mathbb{E}[x(0) P] P = x(0) P^2
    $$

    In other words,
    """)
    return


@app.cell
def _(P, x_1):
    x_2 = x_1 @ P
    print("Expected position of the walker after two steps:\n", x_2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Following the same argument, the expected position of the walker at time $t$ is given by

    $$
    \mathbb{E}[x(t)] = x(0) P^t
    $$

    ### Exercise 01

    Write a function to compute the expected position of the walker at time $t$ using the above formula:
    """)
    return


@app.function
def expected_position(A, x_0, t):
    """
    Compute the probability distribution of the walker at time t.

    Args:
        A (np.ndarray): The adjacency matrix of the graph.
        x_0 (np.ndarray): The initial position of the walker.
        t (int): The number of steps to simulate.

    Returns:
        np.ndarray: The probability distribution of the walker at time t.
    """
    # Your code here
    pass


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 02

    Plot each element of $x(t)$ as a function of $t$ for $t=0,1,2,\ldots, 1000$. Try different initial positions and compare the results!

    Steps:
    1. Define the initial position of the walker.
    2. Compute the expected position of the walker at time $t$ using the function you wrote above.
    3. Draw a line plot for each element of $x(t)$, totalling 5 lines, with the x-axis as $t$ and the y-axis as the probability of the walker being at each node.

    ## Community structure

    Random walks can capture community structure of a network.
    To see this, let us consider a network of a ring of cliques.
    """)
    return


@app.cell
def _(igraph, np, sns):
    import networkx as nx
    n_cliques = 3
    n_nodes_per_clique = 5
    G = nx.ring_of_cliques(n_cliques, n_nodes_per_clique)
    g_1 = igraph.Graph().Adjacency(nx.to_numpy_array(G).tolist()).as_undirected()
    membership = np.repeat(np.arange(n_cliques), n_nodes_per_clique)
    color_map = [sns.color_palette()[_i] for _i in membership]
    igraph.plot(g_1, vertex_size=20, vertex_color=color_map)
    return (g_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let us compute the expected position of the walker after 1 to 10 steps.

    **Compute the transition matrix**:
    """)
    return


@app.cell(hide_code=True)
def _(g_1, np):
    from scipy import sparse
    A_1 = g_1.get_adjacency_sparse()
    _k = np.array(g_1.degree())
    P_1 = sparse.diags(1 / _k) @ A_1
    return (A_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Compute the expected position of the walker after 1 to 300 steps**:
    """)
    return


@app.cell(hide_code=True)
def _(A_1, g_1, np):
    from networkx import nodes
    _x_0 = np.zeros(g_1.vcount())
    _x_0[2] = 1
    x_list = [_x_0]
    t_list = [0, 1, 3, 5, 10, 299]
    for _t in t_list:
        x_t = expected_position(A_1, _x_0, _t)
        x_list.append(x_t)
    x_list = np.array(x_list)
    return t_list, x_list


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Plot the expected position of the walker at each step**:
    """)
    return


@app.cell
def _(g_1, igraph, np, plt, sns, t_list, x_list):
    # Cell tags: hide-input
    cmap = sns.color_palette('viridis', as_cmap=True)
    sns.set_style('white')
    sns.set(font_scale=1.2)
    sns.set_style('ticks')
    fig, axes = plt.subplots(figsize=(15, 10), ncols=3, nrows=2)
    for _i, _t in enumerate(t_list):
        igraph.plot(g_1, vertex_size=20, vertex_color=[cmap(x_list[_t][j] / np.max(x_list[_t])) for j in range(g_1.vcount())], target=axes[_i // 3][_i % 3])
        axes[_i // 3][_i % 3].set_title(f'$t$ = {_t}', fontsize=25)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    where the color of each node represents the probability of the walker being at that node.

    An important observation is that the walker spends more time in the clique that it started from and then diffuse to others. Thus, the position of the walker before reaching the steady state tells us the community structure of the network.
    """)
    return


if __name__ == "__main__":
    app.run()

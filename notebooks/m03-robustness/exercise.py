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
    <a target="_blank" href="https://colab.research.google.com/github/skojaku/adv-net-sci/blob/main/notebooks/m03-robustness/exercise.ipynb">
      <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
    </a>
    """)
    return


@app.cell
def _():
    # If you are using Google Colab, uncomment the following line to install igraph
    # !sudo apt install libcairo2-dev pkg-config python3-dev
    # !pip install pycairo cairocffi
    # !pip install igraph
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Hands-on: Robustness

    We consider a small social network of 34 members in a university karate club, called Zachary's karate club network.
    """)
    return


@app.cell
def _():
    import igraph
    g = igraph.Graph.Famous("Zachary")
    igraph.plot(g, vertex_size=20)
    return (g,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's break the network 😈!
    We will remove nodes one by one and see how the connectivity of the network changes at each step.
    It is useful to create a copy of the network to keep the original network unchanged.
    """)
    return


@app.cell
def _(g):
    g_original = g.copy()
    return (g_original,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Robustness against random failures

    Let us remove a single node from the network. To this end, we need to first identify which nodes are in the network. With `igraph`, the IDs of the nodes in a graph are accessible through `Graph.vs.indices` as follows:
    """)
    return


@app.cell
def _(g):
    print(g.vs.indices)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We randomly choose a node and remove it from the network by using `Graph.delete_vertices`.
    """)
    return


@app.cell
def _(g):
    import numpy as np
    node_idx = np.random.choice(g.vs.indices)
    g.delete_vertices(node_idx)
    print("Node removed:", node_idx)
    print("Nodes remaining:", g.vs.indices)
    print("Number of nodes remaining:", g.vcount())
    return (np,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    :::{note}
    `np.random.choice(array)` takes an array `array` and returns a single element from the array.
    For example, `np.random.choice(np.array([1, 2, 3]))` returns either 1, 2, or 3 with equal probability.
    See [the documentation](https://numpy.org/doc/stable/reference/random/generated/numpy.random.choice.html) for more details.
    :::

    The connectivity of the network is the fraction of nodes in the largest connected component of the network after node removal.
    We can get the connected components of the network by using `Graph.connected_components`.
    """)
    return


@app.cell
def _(g):
    components = g.connected_components()
    return (components,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The sizes of the connected components are accessible via `Graph.connected_components.sizes`.
    """)
    return


@app.cell
def _(components):
    components.sizes()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Thus, the connectivity of the network can be computed by
    """)
    return


@app.cell
def _(g, g_original, np):
    components_1 = g.connected_components()
    _connectivity = np.max(components_1.sizes()) / g_original.vcount()
    _connectivity
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 📊 Exercise: Draw the robustness profile

    In this exercise, we'll create a robustness profile for the network.
    Follow these steps:
    1. Remove nodes randomly one by one
    2. Calculate the connectivity after each removal
    3. Plot the connectivity vs. fraction of nodes removed
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let us plot the robustness profile.
    """)
    return


@app.cell
def _(g_original):
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    _n_nodes = g_original.vcount()
    g_1 = g_original.copy()
    _results = []
    for _i in range(_n_nodes - 1):
        _connectivity = ...
        _results.append({'connectivity': _connectivity, 'node_removed': 1 - g_1.vcount() / _n_nodes})
    df_random = pd.DataFrame(_results)
    sns.set_style('white')
    sns.set(font_scale=1.2)
    sns.set_style('ticks')
    _fig, _ax = plt.subplots(figsize=(7, 5))
    _ax = sns.lineplot(data=df_random, x='node_removed', y='connectivity', ax=_ax)
    _ax.set_xlabel('Fraction of nodes removed')
    _ax.set_ylabel('Connectivity')
    sns.despine()
    return pd, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    How should we interpret the robustness profile? Consider the most robust network consisting of $N$ nodes, where all $N$ nodes are fully connected. Regardless of how many nodes are removed, there will always be a single connected component, and the size of this component will be $N-k$ if $k$ nodes are removed. Therefore, the connectivity is $(N-k)/N=1-k/N$, which corresponds to the diagonal line in the plot above.
    Hence, **a network is considered robust if its connectivity curve is close to the diagonal line**.
    On the other hand, if the curve is significantly lower than the diagonal line, the network is not robust.

    For the network we considered above, the robustness profile is close to the diagonal line, indicating that the network is robust to the random removal of nodes.

    :::{note}
    The random attack is stochastic, meaning that the robustness profile has a variation in each run. Thus, it is necessary to run the attack multiple times and average the results to get a more accurate estimate of the robustness.
    :::

    ## Targeted attack

    In a targeted attack, nodes are removed based on specific criteria rather than randomly.
    One common strategy is to remove nodes from the largest node degree to the smallest, based on the idea that removing nodes with many edges is more likely to disrupt the network connectivity.

    The degree of the nodes is accessible via `Graph.degree`.
    """)
    return


@app.cell
def _(g_original):
    print(g_original.degree())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 02:

    We compute the robustness profile by removing nodes with the largest degree and measuring the connectivity of the network after each removal. Recompute the degree of the nodes after each removal.
    """)
    return


@app.cell
def _(g_original, pd, plt, sns):
    _n_nodes = g_original.vcount()
    g_2 = g_original.copy()
    _results = []
    for _i in range(_n_nodes - 1):
        _connectivity = ...
        _results.append({'connectivity': _connectivity, 'node_removed': 1 - g_2.vcount() / _n_nodes})
    df_targeted = pd.DataFrame(_results)
    sns.set_style('white')
    sns.set(font_scale=1.2)
    sns.set_style('ticks')
    _fig, _ax = plt.subplots(figsize=(7, 5))
    _ax = sns.lineplot(data=df_targeted, x='node_removed', y='connectivity', ax=_ax)
    _ax.set_xlabel('Fraction of nodes removed')
    _ax.set_ylabel('Connectivity')
    sns.despine()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 03

    Compute the robustness index for the degree-based targetted attack and random failures
    """)
    return


@app.cell
def _():
    # Your code

    R_index_targeted = ...
    R_index_random = ...


    print(f"R-index for targeted attack: {R_index_targeted}")
    print(f"R-index for random failures: {R_index_random}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The targeted attack has a smaller $R$-index, indicating that the network is less robust to the targeted attack compared to the random attack.
    """)
    return


if __name__ == "__main__":
    app.run()

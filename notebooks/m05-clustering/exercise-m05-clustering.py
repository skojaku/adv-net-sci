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
    <a target="_blank" href="https://colab.research.google.com/github/skojaku/adv-net-sci/blob/main/notebooks/m05-clustering/exercise-m05-clustering.ipynb">
      <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
    </a>

    # Hands-on: Clustering
    """)
    return


@app.cell
def _():
    # If you are using Google Colab, uncomment the following line to install igraph
    #!sudo apt install libcairo2-dev pkg-config python3-dev
    #!pip install pycairo cairocffi
    #!pip install igraph
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Modularity maximization

    Let us showcase how to use `igraph` to detect communities with modularity. We will use the Karate Club Network as an example.
    """)
    return


@app.cell
def _():
    import igraph

    g = igraph.Graph.Famous("Zachary")
    igraph.plot(g, vertex_size=20)
    return g, igraph


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When it comes to maximizing modularity, there are a variety of algorithms to choose from.
    Two of the most popular ones are the `Louvain` and `Leiden` algorithms, both of which are implemented in `igraph`. The Louvain algorithm has been around for quite some time and is a classic choice, while the Leiden algorithm is a newer bee that often yields better accuracy. For our example, we'll be using the `Leiden` algorithm, and I think you'll find it really effective!
    """)
    return


@app.cell
def _(g):
    communities = g.community_leiden(resolution=1, objective_function="modularity")
    return (communities,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What is `resolution`? It is a parameter that helps us tackle the resolution limit of the modularity maximization algorithm {footcite}`fortunato2007resolution`!
    In simple terms, when we use the resolution parameter $\rho$, the modularity formula can be rewritten as
     follow:

    $$
    Q(M) = \frac{1}{2m} \sum_{i=1}^n \sum_{j=1}^n \left(A_{ij} - \rho \frac{k_i k_j}{2m}\right) \delta(c_i, c_j)
    $$

    Here, the parameter $\rho$ plays a crucial role in balancing the positive and negative parts of the equation.
    The resolution limit comes into play because of the diminishing effect of the negative term as the number of edges $m$ increases.
    The parameter $\rho$ can adjust this balance and allow us to circumvent the resolution limit.

    What is `communities`? This is a list of communities, where each community is represented by a list of nodes by their indices.
    """)
    return


@app.cell
def _(communities):
    print(communities.membership)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let us visualize the communities by coloring the nodes in the graph.
    """)
    return


@app.cell
def _(communities, g, igraph):
    import seaborn as sns
    community_membership = communities.membership
    _palette = sns.color_palette().as_hex()
    igraph.plot(g, vertex_color=[_palette[i] for i in community_membership])
    return (sns,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - `community_membership`: This is a list of community membership for each node.
    - `palette`: This is a list of colors to use for the communities.
    - `igraph.plot(g, vertex_color=[palette[i] for i in community_membership])`: This plots the graph 'g' with nodes colored by their community.

    ### Exercise 01 🏋️‍♀️💪🧠

    1. Select a network of your choice from [Netzschleuder](https://networks.skewed.de/). For convenience, choose a network of nodes less than 5000.
    2. Download the csv version of the data by clicking something like "3KiB" under `csv` column.
    3. Unzip the file and find "edges.csv", open it with a text editor to familiarize yourself with the format.
    4. Load the data using `pandas`.
    5. Get the source and target nodes from the data to create an edge list.
    6. Construct a graph from the edge list, either using `igraph` or `scipy`.
    7. Find communities by maximizing the modularity and visualize them.
    8. Try at least three different values of the resolution parameter and observe how the community structure changes.
    """)
    return


@app.cell
def _(igraph, sns):
    import pandas as pd
    _df = pd.read_csv('../edges.csv', header=None, usecols=[0, 1], names=['src', 'trg'], sep=',', skiprows=1)
    _src, _trg = tuple(_df.values.T)
    g_1 = igraph.Graph.TupleList([(_src[i], _trg[i]) for i in range(len(_src))], directed=False)
    g_1 = g_1.clusters().giant()
    communities_1 = g_1.community_leiden(resolution=1, objective_function='modularity')
    _palette = sns.color_palette('tab20').as_hex()
    color_map = [_palette[i] if i < len(_palette) else 'gray' for i in communities_1.membership]
    igraph.plot(g_1, vertex_size=20, vertex_color=color_map)
    return (pd,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Stochstic Block Model

    Let us turn the SBM as our community detection tool using [graph-tool](https://graph-tool.skewed.de/). This is a powerful library for network analysis, with a focus on the stochastic block model.
    """)
    return


@app.cell
def _():
    #
    # Uncomment the following code if you are using Google Colab
    #
    #!wget https://downloads.skewed.de/skewed-keyring/skewed-keyring_1.0_all_$(lsb_release -s -c).deb
    #!dpkg -i skewed-keyring_1.0_all_$(lsb_release -s -c).deb
    #!echo "deb [signed-by=/usr/share/keyrings/skewed-keyring.gpg] https://downloads.skewed.de/apt $(lsb_release -s -c) main" > /etc/apt/sources.list.d/skewed.list
    #!apt-get update
    #!apt-get install python3-graph-tool python3-matplotlib python3-cairo
    #!apt purge python3-cairo
    #!apt install libcairo2-dev pkg-config python3-dev
    #!pip install --force-reinstall pycairo
    #!pip install zstandard
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will identify the communities using the stochastic block model as follows.
    First, we will convert the graph object in igraph to that in graph-tool.
    """)
    return


@app.cell
def _(igraph):
    import graph_tool.all as gt
    import numpy as np
    g_2 = igraph.Graph.Famous('Zachary')
    np.random.seed(42)
    _edges = g_2.get_edgelist()
    _r, _c = zip(*_edges)
    g_gt = gt.Graph(directed=False)
    g_gt.add_edge_list(np.vstack([_r, _c]).T)
    return g_2, g_gt, gt, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Then, we will fit the stochastic block model to the graph.
    """)
    return


@app.cell
def _(g_gt, gt):
    # Fit the stochastic block model
    _state = gt.minimize_blockmodel_dl(g_gt, state_args={'deg_corr': False, 'B_min': 2, 'B_max': 10})
    b = _state.get_blocks()
    return (b,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - `B_min` and `B_max` are the minimum and maximum number of communities to consider.
    - `deg_corr` is a boolean flag to switch to the degree-corrected SBM {footcite}`karrer2011stochastic`.

    ```{note}
    Here's a fun fact: the likelihood maximization on its own can't figure out how many communities there should be. But `graph-tool` has a clever trick to circumvent this limitation.
    `graph-tool` actually fits multiple SBMs, each with a different number of communities. Then, it picks the most plausible one based on a model selection criterion.
    ```

    Let's visualize the communities to see what we got.
    """)
    return


@app.cell
def _(b, np):
    # Cell tags: hide-input
    # Convert the block assignments to a list
    community_membership_1 = b.get_array()
    community_membership_1 = np.unique(community_membership_1, return_inverse=True)[1]
    # The community labels may consist of non-consecutive integers, e.g., 10, 8, 1, 4, ...
    # So we reassign the community labels to be 0, 1, 2, ...
    community_membership_1
    return (community_membership_1,)


@app.cell
def _(community_membership_1, g_2, igraph, sns):
    import matplotlib.pyplot as plt
    _palette = sns.color_palette().as_hex()
    _fig, _ax = plt.subplots(figsize=(10, 8))
    igraph.plot(g_2, target=_ax, vertex_color=[_palette[i] for i in community_membership_1])
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What we're seeing here isn't a failure at all. In fact, it's the best partition according to our stochastic block model. The model has discovered something called a **core-periphery structure** {footcite}`borgatti2000models`. Let me break that down:

    - Think of a major international airport (the core) and smaller regional airports (the periphery).
    - Major international airports have many flights connecting to each other (densely connected).
    - Smaller regional airports have fewer connections among themselves (sparsely connected).
    - Many regional airports have flights to major hubs (periphery connected to the core).

    That's exactly what our model found in this network.

    If we look at the adjacency matrix, we would see something that looks like an upside-down "L". This shape is like a signature for core-periphery structures.
    """)
    return


@app.cell
def _(community_membership_1, g_2, np, plt):
    # Convert igraph Graph to adjacency matrix
    A = np.array(g_2.get_adjacency().data)
    sorted_indices = np.argsort(community_membership_1)
    # Sort nodes based on their community (core first, then periphery)
    A_sorted = A[sorted_indices][:, sorted_indices]
    plt.figure(figsize=(10, 8))
    plt.imshow(A_sorted, cmap='binary')
    # Plot the sorted adjacency matrix
    plt.title('Sorted Adjacency Matrix: Core-Periphery Structure')
    plt.xlabel('Node Index (sorted)')
    plt.ylabel('Node Index (sorted)')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 02 🏋️‍♀️💪🧠

    1. Select a network of your choice from [Netzschleuder](https://networks.skewed.de/). For convenience, choose a network of nodes less than 5000.
    2. Download the csv version of the data by clicking something like "3KiB" under `csv` column.
    3. Unzip the file and find "edges.csv", open it with a text editor to familiarize yourself with the format.
    4. Load the data using `pandas`.
    5. Get the source and target nodes from the data to create an edge list.
    6. Construct a graph from the edge list, either using `igraph` or `scipy`.
    7. Find communities by fitting the stochastic block model and visualize them.
    8. Try `deg_corr=True` and compare the results with those from `deg_corr=False`.

    ```{footbibliography}
    ```
    """)
    return


@app.cell
def _(community_membership_1, gt, igraph, np, pd, plt, sns):
    _df = pd.read_csv('../edges.csv', header=None, usecols=[0, 1], names=['src', 'trg'], sep=',', skiprows=1)
    _src, _trg = tuple(_df.values.T)
    g_3 = igraph.Graph.TupleList([(_src[i], _trg[i]) for i in range(len(_src))], directed=False)
    g_3 = g_3.clusters().giant()
    np.random.seed(42)
    _edges = g_3.get_edgelist()
    _r, _c = zip(*_edges)
    g_gt_1 = gt.Graph(directed=False)
    g_gt_1.add_edge_list(np.vstack([_r, _c]).T)
    _state = gt.minimize_blockmodel_dl(g_gt_1, state_args={'deg_corr': False, 'B_min': 2, 'B_max': 10})
    b_1 = _state.get_blocks()
    _palette = sns.color_palette().as_hex()
    _fig, _ax = plt.subplots(figsize=(10, 8))
    igraph.plot(g_3, target=_ax, vertex_color=[_palette[i] for i in community_membership_1])
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    return (g_gt_1,)


@app.cell
def _(g_gt_1, gt):
    _state = gt.minimize_nested_blockmodel_dl(g_gt_1, state_args={'deg_corr': True, 'B_min': 2, 'B_max': 10})
    _state.draw()
    return


@app.cell
def _(g_gt_1, gt):
    _state = gt.minimize_nested_blockmodel_dl(g_gt_1, state_args={'deg_corr': False, 'B_min': 2, 'B_max': 10})
    _state.draw()
    return


if __name__ == "__main__":
    app.run()

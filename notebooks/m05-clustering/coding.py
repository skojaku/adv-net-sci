# /// script
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "numpy",
#     "igraph",
#     "seaborn",
# ]
# [tool.marimo.display]
# default_width = "full"
# ///

# NOTE: this notebook also imports graph_tool, which is not installable from
# PyPI. Install it with conda, or run that cell locally.

import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import igraph
    import matplotlib.pyplot as plt
    _fig, _ax = plt.subplots(figsize=(10, 8))
    g = igraph.Graph.Famous('Zachary')
    igraph.plot(g, target=_ax, vertex_size=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    return g, igraph, plt


@app.cell
def _(g):
    communities = g.community_leiden(resolution=1, objective_function= "modularity")
    return (communities,)


@app.cell
def _(communities):
    print(communities.membership)
    return


@app.cell
def _(communities, g, igraph, plt):
    import seaborn as sns
    community_membership = communities.membership
    palette = sns.color_palette().as_hex()
    _fig, _ax = plt.subplots(figsize=(10, 8))
    igraph.plot(g, target=_ax, vertex_color=[palette[i] for i in community_membership])
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    return (sns,)


@app.cell
def _(igraph):
    import graph_tool.all as gt
    import numpy as np
    g_1 = igraph.Graph.Famous('Zachary')
    np.random.seed(42)
    # igraph object
    edges = g_1.get_edgelist()
    r, c = zip(*edges)
    # Set random seed for reproducibility
    g_gt = gt.Graph(directed=False)
    # Convert the graph object in igraph to that in graph-tool
    g_gt.add_edge_list(np.vstack([r, c]).T)
    return g_1, g_gt, gt, np


@app.cell
def _(g_gt, gt):
    # Fit the stochastic block model
    _state = gt.minimize_blockmodel_dl(g_gt, state_args={'deg_corr': False, 'B_min': 2, 'B_max': 10})
    b = _state.get_blocks()
    return (b,)


@app.cell
def _(b, np):
    # Convert the block assignments to a list
    community_membership_1 = b.get_array()
    community_membership_1 = np.unique(community_membership_1, return_inverse=True)[1]
    # The community labels may consist of non-consecutive integers, e.g., 10, 8, 1, 4, ...
    # So we reassign the community labels to be 0, 1, 2, ...
    community_membership_1
    return (community_membership_1,)


@app.cell
def _(community_membership_1, g_1, igraph, plt, sns):
    palette_1 = sns.color_palette().as_hex()
    _fig, _ax = plt.subplots(figsize=(10, 8))
    igraph.plot(g_1, target=_ax, vertex_color=[palette_1[i] for i in community_membership_1])
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    return (palette_1,)


@app.cell
def _(community_membership_1, g_1, np, plt):
    # Convert igraph Graph to adjacency matrix
    A = np.array(g_1.get_adjacency().data)
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


@app.cell
def _(g_1, g_gt, gt, igraph, np, palette_1, plt):
    _state = gt.minimize_blockmodel_dl(g_gt, state_args={'deg_corr': True, 'B_min': 2, 'B_max': 10})
    b_1 = _state.get_blocks()
    community_membership_2 = b_1.get_array()
    community_membership_2 = np.unique(community_membership_2, return_inverse=True)[1]
    _fig, _ax = plt.subplots(figsize=(10, 8))
    igraph.plot(g_1, target=_ax, vertex_color=[palette_1[i] for i in community_membership_2])
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()

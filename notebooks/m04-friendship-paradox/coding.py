# /// script
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "numpy",
#     "python-igraph",
#     "scipy",
#     "seaborn",
# ]
# [tool.marimo.display]
# default_width = "full"
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import igraph
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Create a Barabási-Albert network with 10,000 nodes
    g = igraph.Graph.Barabasi(n=10000, m=1)
    A = g.get_adjacency()
    return A, np, plt, sns


@app.cell
def _(A, np):
    # Compute degree for each node
    deg = np.sum(A, axis=1).flatten()

    # Convert to probability distribution
    p_deg = np.bincount(deg) / len(deg)
    return deg, p_deg


@app.cell
def _(np, p_deg, plt, sns):
    _fig, _ax = plt.subplots(figsize=(8, 5))
    _ax = sns.lineplot(x=np.arange(len(p_deg)), y=p_deg)
    _ax.set_xlabel('Degree')
    _ax.set_ylabel('Probability')
    _ax.set_title('Linear Scale: Most Information Hidden')
    return


@app.cell
def _(np, p_deg, plt, sns):
    _fig, _ax = plt.subplots(figsize=(8, 5))
    _ax = sns.lineplot(x=np.arange(len(p_deg)), y=p_deg)
    _ax.set_xscale('log')
    _ax.set_yscale('log')
    _ax.set_ylim(np.min(p_deg[p_deg > 0]) * 0.01, None)
    _ax.set_xlabel('Degree')
    _ax.set_ylabel('Probability')
    _ax.set_title('Log-Log Scale: Structure Revealed')
    return


@app.cell
def _(np, p_deg, plt, sns):
    # Compute CCDF: fraction of nodes with degree > k
    _ccdf_deg = 1 - np.cumsum(p_deg)[:-1]  # Exclude last element (always 0)
    _fig, _ax = plt.subplots(figsize=(8, 5))
    _ax = sns.lineplot(x=np.arange(len(_ccdf_deg)), y=_ccdf_deg)
    _ax.set_xscale('log')
    _ax.set_yscale('log')
    _ax.set_xlabel('Degree')
    _ax.set_ylabel('CCDF')
    _ax.set_title('CCDF: Smooth Power-Law Visualization')
    return


@app.cell
def _(A):
    from scipy import sparse

    # Extract all edges from the adjacency matrix
    src, trg, _ = sparse.find(A)
    print(f"Total number of edges: {len(src)}")
    print(f"First few source nodes: {src[:10]}")
    print(f"First few target nodes: {trg[:10]}")
    return (src,)


@app.cell
def _(deg, np, src):
    # Get degrees of "friends" (source nodes from edge sampling)
    deg_friend = deg[src]

    # Compute degree distribution of friends
    p_deg_friend = np.bincount(deg_friend) / len(deg_friend)

    print(f"Average degree in network: {np.mean(deg):.2f}")
    print(f"Average degree of friends: {np.mean(deg_friend):.2f}")
    print(f"Friendship paradox ratio: {np.mean(deg_friend) / np.mean(deg):.2f}")
    return (p_deg_friend,)


@app.cell
def _(np, p_deg, p_deg_friend, plt, sns):
    # Compute CCDFs for both distributions
    _ccdf_deg = 1 - np.cumsum(p_deg)[:-1]
    ccdf_deg_friend = 1 - np.cumsum(p_deg_friend)[:-1]
    _fig, _ax = plt.subplots(figsize=(10, 6))
    # Create comparison plot
    _ax = sns.lineplot(x=np.arange(len(_ccdf_deg)), y=_ccdf_deg, label='Regular nodes', linewidth=2, color='blue')
    _ax = sns.lineplot(x=np.arange(len(ccdf_deg_friend)), y=ccdf_deg_friend, label='Friends (degree-biased)', linewidth=2, color='red', ax=_ax)
    _ax.set_xscale('log')
    _ax.set_yscale('log')
    _ax.set_xlabel('Degree')
    _ax.set_ylabel('CCDF')
    _ax.set_title('Friendship Paradox: Friends Have Higher Degrees')
    _ax.legend(frameon=False)
    _ax.grid(True, alpha=0.3)
    return


if __name__ == "__main__":
    app.run()

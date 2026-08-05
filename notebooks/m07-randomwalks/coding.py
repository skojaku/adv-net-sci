# /// script
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "networkx",
#     "numpy",
#     "pandas",
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
    import numpy as np
    import igraph

    g = igraph.Graph()

    g.add_vertices([0, 1, 2, 3, 4])
    g.add_edges([(0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (2, 4), (3, 4)])
    igraph.plot(g, vertex_size=20, vertex_label=g.vs["name"])
    return g, igraph, np


@app.cell
def _(g, np):
    A = g.get_adjacency_sparse().toarray()
    _k = np.array(g.degree())
    n_nodes = g.vcount()
    P = np.zeros((n_nodes, n_nodes))
    # A simple but inefficient way to compute P
    for _i in range(n_nodes):
        for _j in range(n_nodes):
            if _k[_i] > 0:
                P[_i, _j] = A[_i, _j] / _k[_i]
            else:
                P[_i, _j] = 0
    P = A / _k[:, np.newaxis]
    # Alternative, more efficient way to compute P
    # or even more efficiently
    P = np.einsum('ij,i->ij', A, 1 / _k)
    return A, P, n_nodes


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


@app.cell
def _(np):
    x = np.array([0, 0, 0, 0, 0])
    x[0] = 1
    print("Initial position of the walker:\n", x)
    return (x,)


@app.cell
def _(P, x):
    probs = x @ P
    print("Transition probabilities from current position:\n", probs)
    return (probs,)


@app.cell
def _(n_nodes, np, probs, x):
    next_node = np.random.choice(n_nodes, p=probs)
    x[:] = 0 # zero out the vector
    x[next_node] = 1 # set the next node to 1
    print("Position after one step:\n", x)
    return


@app.cell
def _(P, np):
    _x_0 = np.array([1, 0, 0, 0, 0])
    x_1 = _x_0 @ P
    print('Expected position after one step:\n', x_1)
    return (x_1,)


@app.cell
def _(P, x_1):
    x_2 = x_1 @ P
    print("Expected position after two steps:\n", x_2)
    return


@app.cell
def _(A, np, plt):
    def plot_convergence(A, x_0, max_t=100):
        """Plot the convergence to stationary distribution."""
        _k = np.sum(A, axis=1)
        P = A / _k[:, np.newaxis]
        n_nodes = A.shape[0]
        positions = []
        x_t = _x_0.copy()
        positions.append(x_t.copy())
        for _t in range(max_t):
            x_t = x_t @ P
            positions.append(x_t.copy())
        positions = np.array(positions)
        _fig, ax = plt.subplots(figsize=(10, 6))
        for _i in range(n_nodes):
            ax.plot(range(max_t + 1), positions[:, _i], label=f'Node {_i}', linewidth=2)
        ax.set_xlabel('Time')
        ax.set_ylabel('Probability')
        ax.set_title('Random Walk Convergence to Stationary Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.show()
    starting_positions = [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 1]]
    for _i, _x_0 in enumerate(starting_positions):
        print(f'\nStarting from node {np.argmax(_x_0)}:')
        plot_convergence(A, np.array(_x_0))
    return


@app.cell
def _(np):
    import igraph as ig
    edge_list = []
    for _i in range(5):
        for _j in range(_i + 1, 5):
            edge_list.append((_i, _j))
            edge_list.append((_i + 5, _j + 5))
    edge_list.append((0, 6))
    g_1 = ig.Graph(edge_list)
    ig.plot(g_1, vertex_size=20, vertex_label=np.arange(g_1.vcount()))
    return (g_1,)


@app.cell
def _(g_1, np):
    import scipy.sparse as sparse
    A_1 = g_1.get_adjacency_sparse()
    deg = np.array(A_1.sum(axis=1)).flatten()
    Dinv = sparse.diags(1 / deg)
    P_1 = Dinv @ A_1
    return P_1, deg, sparse


@app.cell
def _(P_1, g_1, np, plt, sns):
    x_3 = np.zeros(g_1.vcount())
    x_3[1] = 1
    T = 100
    xt = []
    for _t in range(T):
        x_3 = x_3.reshape(1, -1) @ P_1
        xt.append(x_3)
    xt = np.vstack(xt)
    _fig, ax = plt.subplots(figsize=(10, 6))
    palette = sns.color_palette().as_hex()
    for _i in range(g_1.vcount()):
        sns.lineplot(x=range(T), y=xt[:, _i], label=f'Node {_i}', ax=ax, color=palette[_i % len(palette)])
    ax.set_xlabel('Time')
    ax.set_ylabel('Probability')
    ax.set_title('Stationary distribution of a random walk')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
    return (xt,)


@app.cell
def _(deg, np, xt):
    import pandas as pd

    n_edges = np.sum(deg) / 2
    expected_stationary_dist = deg / (2 * n_edges)

    pd.DataFrame({
        "Expected stationary distribution": expected_stationary_dist,
        "Observed stationary distribution": xt[-1].flatten()
    }).style.format("{:.4f}").set_caption("Comparison of Expected and Observed Stationary Distributions").background_gradient(cmap='cividis', axis=None)
    return (pd,)


@app.cell
def _(igraph, np, sns):
    import networkx as nx
    n_cliques = 3
    n_nodes_per_clique = 5
    G = nx.ring_of_cliques(n_cliques, n_nodes_per_clique)
    g_2 = igraph.Graph().Adjacency(nx.to_numpy_array(G).tolist()).as_undirected()
    membership = np.repeat(np.arange(n_cliques), n_nodes_per_clique)
    color_map = [sns.color_palette()[_i] for _i in membership]
    igraph.plot(g_2, vertex_size=20, vertex_color=color_map)
    return (g_2,)


@app.cell
def _(g_2, np, sparse):
    A_2 = g_2.get_adjacency_sparse()
    _k = np.array(g_2.degree())
    P_2 = sparse.diags(1 / _k) @ A_2
    return (P_2,)


@app.cell
def _(P_2, g_2, np):
    x_t = np.zeros(g_2.vcount())
    x_t[2] = 1
    x_list = [x_t]
    for _t in range(300):
        x_t = x_t @ P_2
        x_list.append(x_t)
    x_list = np.array(x_list)
    return (x_list,)


@app.cell
def _(g_2, igraph, np, plt, sns, x_list):
    cmap = sns.color_palette('viridis', as_cmap=True)
    sns.set_style('white')
    sns.set(font_scale=1.2)
    sns.set_style('ticks')
    _fig, axes = plt.subplots(figsize=(15, 10), ncols=3, nrows=2)
    t_list = [0, 1, 3, 5, 10, 299]
    for _i, _t in enumerate(t_list):
        igraph.plot(g_2, vertex_size=20, vertex_color=[cmap(x_list[_t][_j] / np.max(x_list[_t])) for _j in range(g_2.vcount())], target=axes[_i // 3][_i % 3])
        axes[_i // 3][_i % 3].set_title(f'$t$ = {_t}', fontsize=25)
    return


@app.cell
def _(g_2, np, sparse):
    # Using the two-clique network from before
    A_norm = g_2.get_adjacency_sparse()
    deg_1 = np.array(A_norm.sum(axis=1)).flatten()
    Dinv_sqrt = sparse.diags(1.0 / np.sqrt(deg_1))
    # Normalized adjacency matrix
    A_norm = Dinv_sqrt @ A_norm @ Dinv_sqrt
    return A_norm, deg_1


@app.cell
def _(A_norm, np):
    # Compute eigenvalues and eigenvectors
    evals, evecs = np.linalg.eigh(A_norm.toarray())
    return evals, evecs


@app.cell
def _(evals, pd):
    # Display eigenvalues
    pd.DataFrame({
        "Eigenvalue": evals
    }).T.style.background_gradient(cmap='cividis', axis = 1).set_caption("Eigenvalues of the normalized adjacency matrix")
    return


@app.cell
def _(evals, np):
    lambda_2 = -np.sort(-evals)[1]  # Second largest eigenvalue
    tau = 1 / (1 - lambda_2)  # Relaxation time
    print(f"The second largest eigenvalue is {lambda_2:.4f}")
    print(f"The relaxation time of the random walk is {tau:.4f}")
    return


@app.cell
def _(deg_1, evals, evecs, g_2, np, pd, sparse):
    _t = 5
    _x_0 = np.zeros(g_2.vcount())
    _x_0[0] = 1
    Q_L = np.diag(1.0 / np.sqrt(deg_1)) @ evecs
    Q_R = np.diag(np.sqrt(deg_1)) @ evecs
    x_t_spectral = _x_0 @ Q_L @ np.diag(evals ** _t) @ Q_R.T
    P_matrix = sparse.diags(1 / deg_1) @ g_2.get_adjacency_sparse()
    x_t_power = _x_0.copy()
    for _i in range(_t):
        x_t_power = x_t_power @ P_matrix
    pd.DataFrame({'Spectral method': x_t_spectral.flatten(), 'Power iteration': x_t_power.flatten()}).style.background_gradient(cmap='cividis', axis=None).set_caption('Comparison of Spectral and Power Iteration Methods')
    return


if __name__ == "__main__":
    app.run()

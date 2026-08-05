# /// script
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "numpy",
#     "pandas",
#     "igraph",
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

    # Create the famous Zachary's karate club network
    g = igraph.Graph.Famous('Zachary')

    # Visualize the network
    igraph.plot(g, bbox=(300, 200), vertex_size=20, vertex_label=list(range(g.vcount())))
    return g, igraph


@app.cell
def _(g):
    components = g.connected_components()
    print("Number of components:", len(components))
    print("Component sizes:", list(components.sizes()))
    print("Largest component size:", components.giant().vcount())
    return


@app.cell
def _(g):
    import numpy as np

    def network_connectivity(graph, original_size=None):
        """Calculate network connectivity as fraction of nodes in largest component"""
        if original_size is None:
            original_size = graph.vcount()

        if graph.vcount() == 0:
            return 0.0

        components = graph.connected_components()
        return max(components.sizes()) / original_size

    # Test the function
    connectivity = network_connectivity(g)
    print(f"Current connectivity: {connectivity:.3f}")
    return network_connectivity, np


@app.cell
def _():
    # If you are using Google Colab, uncomment the following line to install igraph
    # !sudo apt install libcairo2-dev pkg-config python3-dev
    # !pip install pycairo cairocffi
    # !pip install igraph
    return


@app.cell
def _(g, network_connectivity, np):
    import pandas as pd

    def simulate_random_attack(graph):
        """Simulate random node removal and measure connectivity"""
        g_test = graph.copy()
        original_size = g_test.vcount()
        results = []

        for i in range(original_size - 1):  # Remove all but one node
            # Randomly select and remove a node
            node_idx = np.random.choice(g_test.vs.indices)
            g_test.delete_vertices(node_idx)

            # Measure connectivity
            connectivity = network_connectivity(g_test, original_size)

            # Store results
            results.append({
                "connectivity": connectivity,
                "frac_nodes_removed": (i + 1) / original_size,
            })

        return pd.DataFrame(results)

    # Run the simulation
    df_random = simulate_random_attack(g)
    return df_random, pd, simulate_random_attack


@app.cell
def _(df_random):
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set(style='white', font_scale=1.2)
    sns.set_style('ticks')
    _fig, _ax = plt.subplots(figsize=(6, 5))
    _ax.plot(df_random['frac_nodes_removed'], df_random['connectivity'], 'o-', linewidth=2, markersize=4, label='Random attack')
    _ax.set_xlabel('Proportion of nodes removed')
    _ax.set_ylabel('Connectivity')
    _ax.set_xlim(0, 1)
    _ax.set_ylim(0, 1)
    sns.despine()
    plt.tight_layout()
    plt.show()
    return plt, sns


@app.cell
def _(g, network_connectivity, np, pd):
    def simulate_targeted_attack(graph, criterion="degree"):
        """Simulate targeted node removal based on specified criterion"""
        g_test = graph.copy()
        original_size = g_test.vcount()
        results = []

        for i in range(original_size - 1):
            # Remove node with highest degree
            if criterion == "degree":
                degrees = g_test.degree()
                node_idx = g_test.vs.indices[np.argmax(degrees)]

            g_test.delete_vertices(node_idx)

            # Measure connectivity
            connectivity = network_connectivity(g_test, original_size)

            # Store results
            results.append({
                "connectivity": connectivity,
                "frac_nodes_removed": (i + 1) / original_size,
            })

        return pd.DataFrame(results)

    # Run targeted attack simulation
    df_targeted = simulate_targeted_attack(g)
    return (df_targeted,)


@app.cell
def _(df_random, df_targeted, plt, sns):
    _fig, _ax = plt.subplots(figsize=(7, 5))
    _ax.plot(df_random['frac_nodes_removed'], df_random['connectivity'], 'o-', linewidth=2, markersize=4, label='Random attack', alpha=0.8)
    _ax.plot(df_targeted['frac_nodes_removed'], df_targeted['connectivity'], 's-', linewidth=2, markersize=4, label='Targeted attack', alpha=0.8)
    _ax.set_xlabel('Proportion of nodes removed')
    _ax.set_ylabel('Connectivity')
    _ax.set_xlim(0, 1)
    _ax.set_ylim(0, 1)
    _ax.legend(frameon=False)
    sns.despine()
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(g, igraph):
    import random

    # Create a weighted version of our network for MST analysis
    g_weighted = g.copy()
    g_weighted.es["weight"] = [random.randint(1, 10) for _ in g_weighted.es]

    # Visualize weighted network
    igraph.plot(g_weighted, bbox=(300, 200),
               edge_width=[w/3 for w in g_weighted.es["weight"]],
               vertex_label=list(range(g_weighted.vcount())))
    return (g_weighted,)


@app.cell
def _(g_weighted, igraph):
    # Find minimum spanning tree
    mst = g_weighted.spanning_tree(weights=g_weighted.es["weight"])

    # Visualize the MST
    igraph.plot(mst, bbox=(300, 200),
               edge_width=[w/3 for w in mst.es["weight"]],
               vertex_label=list(range(mst.vcount())))
    return


@app.cell
def _(igraph, network_connectivity, np, pd):
    def percolation_simulation(lattice_size=100, p_values=None):
        """Simulate percolation on a 2D lattice"""
        if p_values is None:
            p_values = np.linspace(0, 1, 20)

        # Create 2D lattice
        g_lattice = igraph.Graph.Lattice([lattice_size, lattice_size],
                                        nei=1, directed=False,
                                        mutual=False, circular=False)

        results = []
        for p in p_values:
            # Randomly keep nodes with probability p
            keep_nodes = np.where(np.random.rand(g_lattice.vcount()) < p)[0]

            if len(keep_nodes) > 0:
                g_sub = g_lattice.subgraph(keep_nodes)
                largest_size = network_connectivity(g_sub, g_lattice.vcount())
            else:
                largest_size = 0

            results.append({"p": p, "largest_component_fraction": largest_size})

        return pd.DataFrame(results)

    # Run percolation simulation
    df_percolation = percolation_simulation(lattice_size=50)
    return (df_percolation,)


@app.cell
def _(df_percolation, plt, sns):
    _fig, _ax = plt.subplots(figsize=(6, 5))
    _ax.plot(df_percolation['p'], df_percolation['largest_component_fraction'], 'o-', linewidth=2, markersize=4)
    critical_p = 0.593
    _ax.axvline(x=critical_p, color='red', linestyle='--', alpha=0.7, label=f'Critical point (p_c ≈ {critical_p})')
    _ax.set_xlabel('Probability (p)')
    _ax.set_ylabel('Fractional largest component size')
    # Mark theoretical critical point for 2D lattice
    _ax.set_title('Percolation on 2D Lattice')  # Theoretical value for 2D square lattice
    _ax.legend(frameon=False)
    sns.despine()
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _():
    # Your implementation here
    return


@app.cell
def _(igraph, np, pd):
    # Load airport network data
    df_airports = pd.read_csv("https://raw.githubusercontent.com/skojaku/core-periphery-detection/master/data/edge-table-airport.csv")

    # Process edge data
    edges = df_airports[["source", "target"]].to_numpy()
    edges = np.unique(edges.reshape(-1), return_inverse=True)[1]
    edges = edges.reshape(-1, 2)

    # Create network
    g_airports = igraph.Graph()
    g_airports.add_vertices(np.max(edges) + 1)
    g_airports.add_edges([tuple(edge) for edge in edges])

    print(f"Airport network: {g_airports.vcount()} nodes, {g_airports.ecount()} edges")
    return (g_airports,)


@app.cell
def _(g_airports, np):
    # Calculate degree statistics
    degrees = np.array(g_airports.degree())
    k_mean = np.mean(degrees)
    k_squared_mean = np.mean(degrees**2)

    # Molloy-Reed criterion: kappa_0 > 2 for giant component
    kappa_0 = k_squared_mean / k_mean
    print(f"κ₀ = <k²>/<k> = {kappa_0:.3f}")

    # Critical fraction for network breakdown
    f_c = 1 - 1 / (kappa_0 - 1)
    print(f"Predicted critical fraction f_c = {f_c:.3f}")
    return (f_c,)


@app.cell
def _(f_c, g_airports, np, plt, simulate_random_attack, sns):
    # Simulate and visualize (using subset for efficiency)
    n_samples = min(500, g_airports.vcount() - 1)  # Sample for computational efficiency
    sample_indices = np.linspace(0, g_airports.vcount() - 2, n_samples, dtype=int)
    df_airport_robustness = simulate_random_attack(g_airports)
    df_airport_sample = df_airport_robustness.iloc[sample_indices]
    _fig, _ax = plt.subplots(figsize=(6, 5))
    _ax.plot(df_airport_sample['frac_nodes_removed'], df_airport_sample['connectivity'], 'o-', linewidth=2, markersize=3, alpha=0.8)
    _ax.axvline(x=f_c, color='red', linestyle='--', alpha=0.7, label=f'Theoretical f_c = {f_c:.3f}')
    _ax.plot([0, 1], [1, 0], 'gray', linestyle=':', alpha=0.5, label='Linear decline')
    _ax.set_xlabel('Proportion of nodes removed')
    _ax.set_ylabel('Connectivity')
    _ax.set_title('Airport Network Robustness')
    # Add theoretical prediction
    _ax.legend(frameon=False)
    sns.despine()
    plt.tight_layout()
    # Add diagonal reference line
    plt.show()
    return


if __name__ == "__main__":
    app.run()

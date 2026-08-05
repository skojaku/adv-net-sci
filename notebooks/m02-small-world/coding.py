# /// script
# dependencies = [
#     "marimo",
#     "numpy",
#     "igraph",
# ]
# [tool.marimo.display]
# default_width = "full"
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    edge_list = [(0, 1), (1, 2), (0, 2), (0, 3)]
    return (edge_list,)


@app.cell
def _(edge_list):
    import igraph

    g = igraph.Graph() # Create an empty graph
    g.add_vertices(4) # Add 4 vertices
    g.add_edges(edge_list) # Add edges to the graph

    # Plot the graph
    igraph.plot(g, bbox=(150, 150), vertex_label=list(range(4)))
    return g, igraph


@app.cell
def _(g):
    g.get_all_simple_paths(2, to=3)
    return


@app.cell
def _(g):
    g.get_shortest_paths(2, to=3)
    return


@app.cell
def _(g):
    g.distances(2, 3)
    return


@app.cell
def _(g):
    components = g.connected_components()
    return (components,)


@app.cell
def _(components):
    print("membership: ", components.membership)  # the IDs of the component each node belongs to.
    print("sizes: ", list(components.sizes()))  # the number of nodes in each component.
    print("giant: ", components.giant())  # a subgraph of the largest connected component.
    return


@app.cell
def _(igraph):
    edge_list_1 = [(0, 1), (1, 2), (2, 1), (2, 3), (2, 5), (3, 1), (3, 4), (3, 5), (4, 5), (5, 3)]
    g_1 = igraph.Graph(directed=True)
    g_1.add_vertices(6)
    g_1.add_edges(edge_list_1)
    igraph.plot(g_1, bbox=(250, 250), vertex_label=list(range(6)))
    return (g_1,)


@app.cell
def _(g_1):
    print('From 0 to 3', g_1.get_all_simple_paths(0, to=3))
    print('From 3 to 0', g_1.get_all_simple_paths(3, to=0))
    return


@app.cell
def _(g_1):
    g_1.get_shortest_paths(4, 1)
    return


@app.cell
def _(g_1):
    print(list(g_1.connected_components(mode='strong')))
    print(list(g_1.connected_components(mode='weak')))
    return


@app.cell
def _(igraph):
    # Create a graph with some triangles
    _edges = [(0, 1), (0, 2), (1, 2), (0, 3), (3, 4), (3, 5), (4, 5), (1, 6), (6, 7)]  # Triangle: 0-1-2
    g_cluster = igraph.Graph()  # Node 3 with two neighbors (4,5)
    g_cluster.add_vertices(8)  # Triangle: 3-4-5
    g_cluster.add_edges(_edges)  # Linear extension
    # Plot the graph
    igraph.plot(g_cluster, bbox=(300, 200), vertex_label=list(range(8)))
    return (g_cluster,)


@app.cell
def _(g_cluster):
    # Local clustering coefficient for each node
    local_clustering = g_cluster.transitivity_local_undirected()
    print('Local clustering coefficients:')
    for _i, coeff in enumerate(local_clustering):
        print(f'Node {_i}: {coeff:.3f}')
    return (local_clustering,)


@app.cell
def _(g_cluster, local_clustering):
    for _node in range(g_cluster.vcount()):
        neighbors = g_cluster.neighbors(_node)
        _degree = len(neighbors)
        clustering = local_clustering[_node]
        print(f'Node {_node}: degree={_degree}, neighbors={neighbors}, clustering={clustering:.3f}')
        if _degree >= 2:
            possible_edges = _degree * (_degree - 1) // 2
            actual_edges = 0
            for _i in range(len(neighbors)):
                for j in range(_i + 1, len(neighbors)):
                    if g_cluster.are_adjacent(neighbors[_i], neighbors[j]):
                        actual_edges = actual_edges + 1
            print(f'  -> {actual_edges}/{possible_edges} neighbor pairs connected')
        print()
    return


@app.cell
def _(g_cluster, local_clustering):
    # Average local clustering (mean of local values)
    avg_local_clustering = g_cluster.transitivity_avglocal_undirected()
    print(f"Average local clustering: {avg_local_clustering:.3f}")

    # Verify by manual calculation
    import numpy as np
    manual_avg = np.nanmean(local_clustering)  # nanmean ignores NaN values
    print(f"Manual calculation: {manual_avg:.3f}")
    return


@app.cell
def _(g_cluster):
    global_clustering = g_cluster.transitivity_undirected()
    print(f'Global clustering: {global_clustering:.3f}')
    triangles_count = len(g_cluster.list_triangles())
    print(f'Number of triangles: {triangles_count}')
    print(f'Triangles in graph: {g_cluster.list_triangles()}')
    triples = 0
    for _node in range(g_cluster.vcount()):
        _degree = g_cluster.degree(_node)
        if _degree >= 2:
            triples = triples + _degree * (_degree - 1) // 2
    print(f'Connected triples: {triples}')
    print(f'Global clustering = 3 * {triangles_count} / {triples} = {3 * triangles_count / triples:.3f}')
    return


@app.cell
def _(g_cluster, igraph):
    n_complete = 6
    g_complete = igraph.Graph.Full(n_complete)
    n_random = 20
    p_random = 0.2
    g_random = igraph.Graph.Erdos_Renyi(n_random, p_random)
    n_ring = 20
    k_ring = 4
    g_ring = igraph.Graph.Lattice(dim=[n_ring], circular=True, nei=k_ring // 2)
    networks = {'Complete': g_complete, 'Random': g_random, 'Ring Lattice': g_ring, 'Our Example': g_cluster}
    print('Clustering Comparison:')
    print('-' * 60)
    print(f"{'Network':<15} {'Avg Local':<12} {'Global':<12} {'Nodes':<8} {'Edges':<8}")
    print('-' * 60)
    for name, graph in networks.items():
        avg_local = graph.transitivity_avglocal_undirected()
        global_clust = graph.transitivity_undirected()
        nodes = graph.vcount()
        _edges = graph.ecount()
        print(f'{name:<15} {avg_local:<12.3f} {global_clust:<12.3f} {nodes:<8} {_edges:<8}')
    return


@app.cell
def _(igraph):
    # Create a small-world network (Watts-Strogatz model)
    # Start with ring lattice, then rewire some edges randomly
    n_ws = 30
    k_ws = 6
    p_rewire = 0.1

    g_smallworld = igraph.Graph.Watts_Strogatz(dim=1, size=n_ws, nei=k_ws//2, p=p_rewire)

    print("Small-World Network Analysis:")
    print(f"Nodes: {g_smallworld.vcount()}, Edges: {g_smallworld.ecount()}")
    print(f"Average local clustering: {g_smallworld.transitivity_avglocal_undirected():.3f}")
    print(f"Global clustering: {g_smallworld.transitivity_undirected():.3f}")
    print(f"Average path length: {g_smallworld.average_path_length():.3f}")

    # Compare with random graph of same size and density
    g_random_compare = igraph.Graph.Erdos_Renyi(n_ws, g_smallworld.ecount() * 2 / (n_ws * (n_ws - 1)))

    print("\nCompared to random graph with same density:")
    print(f"Random avg local clustering: {g_random_compare.transitivity_avglocal_undirected():.3f}")
    print(f"Random global clustering: {g_random_compare.transitivity_undirected():.3f}")
    print(f"Random average path length: {g_random_compare.average_path_length():.3f}")
    return


if __name__ == "__main__":
    app.run()

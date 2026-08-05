# /// script
# dependencies = [
#     "marimo",
#     "numpy",
#     "scipy",
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
    from scipy import sparse

    # Create a small example network
    # Let's represent the same 5-node network from earlier
    dense_matrix = np.array([
        [0, 1, 1, 0, 0],  # Node 0 connects to nodes 1, 2
        [1, 0, 1, 1, 0],  # Node 1 connects to nodes 0, 2, 3
        [1, 1, 0, 0, 1],  # Node 2 connects to nodes 0, 1, 4
        [0, 1, 0, 0, 1],  # Node 3 connects to nodes 1, 4
        [0, 0, 1, 1, 0]   # Node 4 connects to nodes 2, 3
    ])

    # Convert to CSR format
    csr_matrix = sparse.csr_matrix(dense_matrix)

    print("Dense matrix shape:", dense_matrix.shape)
    print("CSR matrix shape:", csr_matrix.shape)
    print("Non-zero entries:", csr_matrix.nnz)
    print("Memory saved: {:.1f}%".format((1 - csr_matrix.nnz / dense_matrix.size) * 100))
    return csr_matrix, np, sparse


@app.cell
def _(csr_matrix):
    print("CSR internal arrays:")
    print("data (non-zero values):", csr_matrix.data)
    print("indices (column positions):", csr_matrix.indices)
    print("indptr (row pointers):", csr_matrix.indptr)

    # Let's trace through how CSR works
    print("\nDecoding CSR structure:")
    for i in range(len(csr_matrix.indptr) - 1):
        start = csr_matrix.indptr[i]
        end = csr_matrix.indptr[i + 1]
        row_data = csr_matrix.data[start:end]
        row_indices = csr_matrix.indices[start:end]
        print(f"Row {i}: values {row_data} at columns {row_indices}")
    return


@app.cell
def _(np, sparse):
    # Define our network as an edge list
    edges = [
        (0, 1), (0, 2),  # Node 0 connections
        (1, 2), (1, 3),  # Node 1 connections
        (2, 4),          # Node 2 connections
        (3, 4)           # Node 3 connections
    ]

    # Extract source and target nodes
    sources = [edge[0] for edge in edges]
    targets = [edge[1] for edge in edges]

    # For undirected graphs, add reverse edges
    all_sources = sources + targets
    all_targets = targets + sources

    # Create data array (all ones for unweighted graph)
    data_values = np.ones(len(all_sources))

    # Create CSR matrix directly from edge list
    n_nodes = 5
    csr_from_edges = sparse.csr_matrix(
        (data_values, (all_sources, all_targets)),
        shape=(n_nodes, n_nodes)
    )

    print("CSR from edge list:")
    print(csr_from_edges.toarray())
    return


@app.cell
def _(csr_matrix, np):
    # Node degrees - sum each row
    degrees = np.array(csr_matrix.sum(axis=1)).flatten()
    print("Node degrees:", degrees)

    # Find neighbors of node 1
    node_1_neighbors = csr_matrix.indices[csr_matrix.indptr[1]:csr_matrix.indptr[2]]
    print("Node 1 neighbors:", node_1_neighbors)

    # Matrix multiplication for 2-hop paths
    two_hop_matrix = csr_matrix @ csr_matrix
    print("Two-hop connections (shows paths of length 2):")
    print(two_hop_matrix.toarray())
    return (degrees,)


@app.cell
def _(np, sparse):
    # Create a larger sparse network
    n = 1000
    density = 0.01  # Only 1% of edges exist

    # Generate random sparse matrix
    np.random.seed(42)
    large_dense = sparse.random(n, n, density=density, format='csr')

    print(f"Network size: {n} × {n} = {n**2:,} potential edges")
    print(f"Actual edges: {large_dense.nnz:,}")
    print(f"Sparsity: {(1 - large_dense.nnz / (n*n)) * 100:.1f}% zeros")
    print(f"CSR memory usage: ~{(large_dense.nnz * 2 + n) * 4 / 1024:.1f} KB")
    print(f"Dense memory usage: ~{n*n * 4 / 1024:.1f} KB")
    print(f"Memory savings: {((n*n * 4) - (large_dense.nnz * 2 + n) * 4) / (n*n * 4) * 100:.1f}%")
    return


@app.cell
def _(csr_matrix, np):
    def is_walk_sparse(sequence, csr_matrix):
        """
        Check if a sequence forms a valid walk using sparse CSR matrix.
        """
        if len(sequence) < 2:
            return True

        sequence = np.array(sequence)
        current_nodes = sequence[:-1]
        next_nodes = sequence[1:]

        # Use CSR matrix indexing - still works with advanced indexing!
        edges_exist = csr_matrix[(current_nodes, next_nodes)]

        # Convert sparse result to array and check
        return np.all(edges_exist == 1)

    # Test with our CSR matrix
    test_walk = [0, 1, 2, 4, 3, 1]
    print(f"Walk {test_walk} is valid: {is_walk_sparse(test_walk, csr_matrix)}")
    return


@app.cell
def _(csr_matrix, degrees, np):
    # Submatrix extraction - get connections for subset of nodes
    subset_nodes = [0, 1, 2]
    subgraph = csr_matrix[subset_nodes][:, subset_nodes]
    print("Subgraph for nodes [0, 1, 2]:")
    print(subgraph.toarray())

    # Efficient boolean operations
    # Find nodes with degree > 2
    high_degree_nodes = np.where(degrees > 2)[0]
    print("High degree nodes (> 2 connections):", high_degree_nodes)

    # Matrix powers for path counting
    paths_3 = csr_matrix ** 3  # Counts 3-step paths
    print("3-step path counts:")
    print(paths_3.toarray())
    return


if __name__ == "__main__":
    app.run()

# /// script
# dependencies = [
#     "marimo",
#     "numpy",
# ]
# [tool.marimo.display]
# default_width = "full"
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    # Each row represents one edge (connection between two nodes)
    edges = [
        (0, 1),  # Node 0 connects to Node 1
        (0, 2),  # Node 0 connects to Node 2
        (1, 2),  # Node 1 connects to Node 2
        (1, 3),  # Node 1 connects to Node 3
        (2, 4),  # Node 2 connects to Node 4
        (3, 4)   # Node 3 connects to Node 4
    ]

    print(f"Network has {len(edges)} edges")
    print("Edge list:", edges)
    return (edges,)


@app.cell
def _():
    # Define adjacency list directly as a dictionary
    neighbors = {
        0: [1, 2],     # Node 0 connects to nodes 1 and 2
        1: [0, 2, 3],  # Node 1 connects to nodes 0, 2, and 3
        2: [0, 1, 4],  # Node 2 connects to nodes 0, 1, and 4
        3: [1, 4],     # Node 3 connects to nodes 1 and 4
        4: [2, 3]      # Node 4 connects to nodes 2 and 3
    }

    print("Adjacency list representation:")
    for node, neighbor_list in neighbors.items():
        print(f"Node {node}: {neighbor_list}")
    return (neighbors,)


@app.cell
def _():
    # Define adjacency matrix directly
    import numpy as np

    matrix = np.array([
        [0, 1, 1, 0, 0],  # Node 0 connects to nodes 1, 2
        [1, 0, 1, 1, 0],  # Node 1 connects to nodes 0, 2, 3
        [1, 1, 0, 0, 1],  # Node 2 connects to nodes 0, 1, 4
        [0, 1, 0, 0, 1],  # Node 3 connects to nodes 1, 4
        [0, 0, 1, 1, 0]   # Node 4 connects to nodes 2, 3
    ])

    print("Adjacency matrix:")
    print(matrix)
    return matrix, np


@app.cell
def _(edges):
    _degrees = [0] * 5
    for node1, node2 in edges:
        _degrees[node1] += 1
        _degrees[node2] += 1
    print("Degrees from edge list:", _degrees)
    return


@app.cell
def _(neighbors):
    _degrees = [len(neighbors[i]) for i in range(5)]
    print("Degrees from adjacency list:", _degrees)
    return


@app.cell
def _(matrix):
    _degrees = matrix.sum(axis=1)  # Sum rows
    print("Degrees from adjacency matrix:", _degrees)
    return


@app.cell
def _(matrix, np):
    def is_walk(sequence, adjacency_matrix):
        """
        Check if a sequence of nodes forms a valid walk.

        Args:
            sequence: List of node indices [v0, v1, v2, ...]
            adjacency_matrix: 2D numpy array representing the graph

        Returns:
            bool: True if sequence is a valid walk, False otherwise
        """
        if len(sequence) < 2:
            return True  # Single node or empty sequence is trivially a walk

        # Use NumPy vectorized operations for efficient edge checking
        sequence = np.array(sequence)
        current_nodes = sequence[:-1]  # All nodes except the last
        next_nodes = sequence[1:]      # All nodes except the first

        # Simple but slower: for loop version (slower but more explicit)
        # for i, j in zip(current_nodes, next_nodes):
        #     if adjacency_matrix[i, j] == 0:
        #         return False
        # return True

        # Check all edges at once using advanced indexing
        edges_exist = adjacency_matrix[current_nodes, next_nodes]

        # All edges must exist (all values must be 1)
        return np.all(edges_exist == 1)


    # Test with our sample network
    test_sequence = [0, 1, 2, 4, 3, 1]
    print(f"Sequence {test_sequence} is a valid walk: {is_walk(test_sequence, matrix)}")

    # Test an invalid walk
    invalid_sequence = [0, 3]  # No direct edge between 0 and 3
    print(f"Sequence {invalid_sequence} is a valid walk: {is_walk(invalid_sequence, matrix)}")
    return (is_walk,)


@app.cell
def _(is_walk, matrix, np):
    def is_trail(sequence, adjacency_matrix):
        """
        Check if a sequence of nodes forms a valid trail.

        Args:
            sequence: List of node indices [v0, v1, v2, ...]
            adjacency_matrix: 2D numpy array representing the graph

        Returns:
            bool: True if sequence is a valid trail, False otherwise
        """
        if not is_walk(sequence, adjacency_matrix):
            return False  # Must be a valid walk first

        if len(sequence) < 2:
            return True

        # Convert to numpy for efficient operations
        sequence = np.array(sequence)
        current_nodes = sequence[:-1]
        next_nodes = sequence[1:]

        # Use complex numbers to represent edges!
        # For undirected graph: smaller_node + 1j * larger_node
        # This ensures edge (1,2) and (2,1) both become 1+2j
        edge_starts = np.minimum(current_nodes, next_nodes)  # Real part
        edge_ends = np.maximum(current_nodes, next_nodes)    # Imaginary part
        complex_edges = edge_starts + 1j * edge_ends

        # Check uniqueness directly with NumPy
        return len(complex_edges) == len(np.unique(complex_edges))

        # Alternative: Original for loop version (slower but more explicit)
        # used_edges = set()
        # for i in range(len(sequence) - 1):
        #     current_node = sequence[i]
        #     next_node = sequence[i + 1]
        #     # Create edge tuple (smaller index first for undirected graphs)
        #     edge = (min(current_node, next_node), max(current_node, next_node))
        #     if edge in used_edges:
        #         return False  # Edge already used
        #     used_edges.add(edge)
        # return True

    # Test trail verification
    trail_sequence = [0, 1, 3, 4, 2]
    print(f"Sequence {trail_sequence} is a valid trail: {is_trail(trail_sequence, matrix)}")

    # Test invalid trail (reuses edge 1-2)
    invalid_trail = [0, 1, 2, 1, 3]
    print(f"Sequence {invalid_trail} is a valid trail: {is_trail(invalid_trail, matrix)}")
    return


@app.cell
def _(is_walk, matrix, np):
    def is_path(sequence, adjacency_matrix):
        """
        Check if a sequence of nodes forms a valid path.

        Args:
            sequence: List of node indices [v0, v1, v2, ...]
            adjacency_matrix: 2D numpy array representing the graph
            allow_cycle: If True, allows start node = end node (cycle)

        Returns:
            bool: True if sequence is a valid path, False otherwise
        """
        if not is_walk(sequence, adjacency_matrix):
            return False  # Must be a valid walk first

        if len(sequence) < 2:
            return True

        sequence = np.array(sequence)

        return len(sequence) == len(np.unique(sequence))

    # Test path verification
    path_sequence = [0, 1, 3, 4]
    print(f"Sequence {path_sequence} is a valid path: {is_path(path_sequence, matrix)}")

    # Test invalid path (repeats node 1)
    invalid_path = [0, 1, 2, 1, 3]
    print(f"Sequence {invalid_path} is a valid path: {is_path(invalid_path, matrix)}")
    return


@app.cell
def _(matrix, np):
    def connected_components(adjacency_matrix):
        """
        Find connected components in an undirected graph using adjacency matrix.

        Args:
            adjacency_matrix: 2D numpy array (square)

        Returns:
            List of lists, each sublist contains node indices in a component
        """
        import numpy as np
        n = adjacency_matrix.shape[0]
        visited = np.zeros(n, dtype=bool)
        components = []

        def dfs(node, component):
            """Depth-first search to explore a component"""
            # Mark the current node as visited and add it to current component
            visited[node] = True
            component.append(node)

            # Find all neighbors of the current node using vectorized operation
            neighbors = np.where(adjacency_matrix[node] > 0)[0]

            # Recursively visit unvisited neighbors
            for neighbor in neighbors:
                if not visited[neighbor]:
                    dfs(neighbor, component)

        # Main algorithm: iterate through all nodes
        for v in range(n):
            if not visited[v]:  # Found a new component
                component = []
                dfs(v, component)  # Explore entire component
                components.append(component)

        return components

    # Test with our original connected graph
    print("Testing with connected graph:")
    components = connected_components(matrix)
    print("Connected components:", components)
    print(f"Number of components: {len(components)}")

    # Create a disconnected graph to demonstrate multiple components
    disconnected_matrix = np.array([
        [0, 1, 0, 0, 0],  # Component 1: nodes 0,1,2
        [1, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1],  # Component 2: nodes 3,4
        [0, 0, 0, 1, 0]
    ])

    print("\nTesting with disconnected graph:")
    disconnected_components = connected_components(disconnected_matrix)
    print("Connected components:", disconnected_components)
    print(f"Number of components: {len(disconnected_components)}")
    return connected_components, disconnected_matrix


@app.cell
def _(connected_components, disconnected_matrix, matrix, np):
    def has_euler_path_complete(adjacency_matrix):
        """
        Complete Euler path checker with connectivity verification.

        Args:
            adjacency_matrix: 2D numpy array representing the graph

        Returns:
            bool: True if graph has an Euler path, False otherwise
        """
        # Check if graph is connected (ignoring isolated nodes)
        components = connected_components(adjacency_matrix)

        # Find nodes with at least one edge (degree > 0)
        degrees = adjacency_matrix.sum(axis=1)
        non_isolated_nodes = np.where(degrees > 0)[0]

        if len(non_isolated_nodes) == 0:
            return True  # Empty graph has Euler path trivially

        # Check if all non-isolated nodes are in the same component
        component_with_edges = None
        for component in components:
            if non_isolated_nodes[0] in component:
                component_with_edges = set(component)
                break

        # All nodes with edges must be in the same component
        if not all(node in component_with_edges for node in non_isolated_nodes):
            return False  # Graph is disconnected

        # Count nodes with odd degrees (among non-isolated nodes)
        non_isolated_degrees = degrees[non_isolated_nodes]
        odd_degree_count = np.sum(non_isolated_degrees % 2)

        # Euler's theorem: exactly 0 or 2 nodes with odd degrees
        return odd_degree_count == 0 or odd_degree_count == 2

    # Test with connected graph
    print("Connected graph has Euler path:", has_euler_path_complete(matrix))

    # Test with disconnected graph
    print("Disconnected graph has Euler path:", has_euler_path_complete(disconnected_matrix))

    # Test the classic Königsberg bridge problem (all odd degrees)
    konigsberg = np.array([
        [0, 1, 1, 1],  # Landmass 0 connects to all others (degree 3)
        [1, 0, 1, 1],  # Landmass 1 connects to all others (degree 3)
        [1, 1, 0, 1],  # Landmass 2 connects to all others (degree 3)
        [1, 1, 1, 0]   # Landmass 3 connects to all others (degree 3)
    ])
    print("Königsberg bridges have Euler path:", has_euler_path_complete(konigsberg))
    return


if __name__ == "__main__":
    app.run()

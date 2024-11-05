# %%
import numpy as np
from typing import List, Dict, Tuple
import networkx as nx
from collections import defaultdict


class WL2Test:
    def __init__(self):
        """Initialize the 2-WL test"""
        self.color_map = {}  # Maps color patterns to unique color IDs
        self.next_color = 0  # Counter for generating unique color IDs

    def get_unique_color(self, pattern) -> int:
        """Get a unique color ID for a pattern. If pattern is new, assign a new color."""
        if pattern not in self.color_map:
            self.color_map[pattern] = self.next_color
            self.next_color += 1
        return self.color_map[pattern]

    def create_initial_coloring(self, adj_matrix: np.ndarray) -> np.ndarray:
        """Create initial coloring matrix based on edge connections.

        Args:
            adj_matrix: Adjacency matrix of the graph

        Returns:
            Initial coloring matrix where each cell (i,j) contains the color of tuple (i,j)
        """
        n = len(adj_matrix)
        color_matrix = np.zeros((n, n), dtype=int)

        # Assign initial colors:
        # 1 for connected pairs (edges)
        # 0 for non-connected pairs
        for i in range(n):
            for j in range(n):
                # Convert to tuple for hashing
                pattern = (0, bool(adj_matrix[i, j]))  # (is_same_node, is_connected)
                color_matrix[i, j] = self.get_unique_color(pattern)

        return color_matrix

    def get_neighbor_colors(
        self, color_matrix: np.ndarray, i: int, j: int
    ) -> Tuple[List[int], List[int]]:
        """Get sorted colors of neighbors for position i and j.

        Args:
            color_matrix: Current coloring matrix
            i, j: Indices of the tuple (i,j)

        Returns:
            Two sorted lists of neighbor colors (first_position_colors, second_position_colors)
        """
        n = len(color_matrix)
        # Get neighbors sharing first position (i,*)
        first_pos_colors = sorted(color_matrix[i, :])
        # Get neighbors sharing second position (*,j)
        second_pos_colors = sorted(color_matrix[:, j])

        return first_pos_colors, second_pos_colors

    def refine_coloring(self, color_matrix: np.ndarray) -> np.ndarray:
        """Refine the coloring based on neighborhood colors.

        Args:
            color_matrix: Current coloring matrix

        Returns:
            New coloring matrix
        """
        n = len(color_matrix)
        new_color_matrix = np.zeros((n, n), dtype=int)

        for i in range(n):
            for j in range(n):
                # Get sorted neighbor colors
                first_pos_colors, second_pos_colors = self.get_neighbor_colors(
                    color_matrix, i, j
                )

                # Create pattern from current color and neighbor colors
                pattern = (
                    color_matrix[i, j],
                    tuple(first_pos_colors),
                    tuple(second_pos_colors),
                )

                # Assign new color based on pattern
                new_color_matrix[i, j] = self.get_unique_color(pattern)

        return new_color_matrix

    def are_matrices_equal(self, matrix1: np.ndarray, matrix2: np.ndarray) -> bool:
        """Check if two coloring matrices represent the same coloring up to color renaming."""
        # Get unique colors and their counts in both matrices
        colors1 = defaultdict(int)
        colors2 = defaultdict(int)

        for color in matrix1.flatten():
            colors1[color] += 1
        for color in matrix2.flatten():
            colors2[color] += 1

        # Compare color frequency distributions
        return sorted(colors1.values()) == sorted(colors2.values())

    def visualize_coloring(
        self, color_matrix: np.ndarray, node_labels: List[str] = None
    ) -> None:
        """Visualize the coloring matrix with node labels."""
        n = len(color_matrix)
        if node_labels is None:
            node_labels = [str(i) for i in range(n)]

        # Print column headers
        print("   ", end="")
        for j in range(n):
            print(f"{node_labels[j]:4}", end="")
        print("\n   " + "----" * n)

        # Print matrix with row labels
        for i in range(n):
            print(f"{node_labels[i]:2}|", end=" ")
            for j in range(n):
                print(f"{color_matrix[i,j]:3}", end=" ")
            print()
        print()

        # Print color counts
        color_counts = defaultdict(int)
        for color in color_matrix.flatten():
            color_counts[color] += 1
        print("Color counts:", dict(color_counts))

    def test_isomorphism(self, G1: nx.Graph, G2: nx.Graph, max_iter: int = 10) -> bool:
        """Test if two graphs might be isomorphic using 2-WL test.

        Args:
            G1, G2: Input graphs
            max_iter: Maximum number of iterations

        Returns:
            True if graphs might be isomorphic, False if definitely not isomorphic
        """
        if G1.number_of_nodes() != G2.number_of_nodes():
            return False

        # Convert graphs to adjacency matrices
        adj1 = nx.adjacency_matrix(G1).toarray()
        adj2 = nx.adjacency_matrix(G2).toarray()

        # Get initial colorings
        colors1 = self.create_initial_coloring(adj1)
        colors2 = self.create_initial_coloring(adj2)

        # Check if initial colorings are different
        if not self.are_matrices_equal(colors1, colors2):
            return False

        # Refine colorings until stabilization or max iterations
        for _ in range(max_iter):
            new_colors1 = self.refine_coloring(colors1)
            new_colors2 = self.refine_coloring(colors2)

            # Check if new colorings are different
            if not self.are_matrices_equal(new_colors1, new_colors2):
                return False

            # Check if colorings have stabilized
            if self.are_matrices_equal(
                new_colors1, colors1
            ) and self.are_matrices_equal(new_colors2, colors2):
                break

            colors1, colors2 = new_colors1, new_colors2

        return True


# Example usage
def test_path_graph():
    # Create path graph n1-n2-n3-n4
    G = nx.path_graph(4)

    # Initialize 2-WL test
    wl = WL2Test()

    # Get adjacency matrix
    adj_matrix = nx.adjacency_matrix(G).toarray()

    # Run the test
    node_labels = ["n1", "n2", "n3", "n4"]

    print("Original adjacency matrix:")
    wl.visualize_coloring(adj_matrix, node_labels)

    print("\nInitial coloring:")
    colors = wl.create_initial_coloring(adj_matrix)
    wl.visualize_coloring(colors, node_labels)

    print("\nAfter first refinement:")
    new_colors = wl.refine_coloring(colors)
    wl.visualize_coloring(new_colors, node_labels)

    print("\nAfter second refinement:")
    final_colors = wl.refine_coloring(new_colors)
    wl.visualize_coloring(final_colors, node_labels)


if __name__ == "__main__":
    test_path_graph()
# %%
import numpy as np
from scipy import sparse


def weisfeiler_lehman_test(A, num_iterations):
    n_nodes = A.shape[0]
    labels = np.zeros(n_nodes, dtype=int)
    color_map = {}
    hash_fn = lambda x: color_map.setdefault(x, len(color_map))
    for _ in range(num_iterations):

        # Go through each node
        labels_old = labels.copy()
        for i in range(n_nodes):

            # Collect the labels of all neighbors
            neighbors = A[i].nonzero()[1]
            neighbor_labels = labels_old[neighbors]

            # Count the frequency of each label
            unique, counts = np.unique(neighbor_labels, return_counts=True)

            # Create a hash key by converting the frequency dictionary to a string
            hash_key = str({unique[j]: counts[j] for j in range(len(unique))})

            # Create a new label by hashing the frequency dictionary
            label = hash_fn(hash_key)
            labels[i] = label

        # Check convergence
        unique, counts = np.unique(labels, return_counts=True)
        unique_old, counts_old = np.unique(labels_old, return_counts=True)
        if np.array_equal(np.sort(counts), np.sort(counts_old)):
            break
    return labels


edge_list = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]

A = sparse.csr_matrix(
    ([1] * len(edge_list), ([e[0] for e in edge_list], [e[1] for e in edge_list])),
    shape=(6, 6),
)
A = A + A.T
A.sort_indices()

weisfeiler_lehman_test(A, A.shape[0])
# %%

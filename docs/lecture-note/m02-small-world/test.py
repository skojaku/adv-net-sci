# %%
import igraph as ig
import numpy as np

def small_worldness(graph, n_trials=100):
  """
  Calculates the small-world-ness of a graph.

  Args:
    graph: An igraph Graph object.
    n_trials: Number of random graphs to generate for averaging.

  Returns:
    A float representing the small-world-ness of the graph.
  """

  n_nodes = graph.vcount()
  n_edges = graph.ecount()

  # Calculate clustering coefficient
  clustering_coefficient = graph.transitivity_undirected()

  # Calculate average shortest path length
  shortest_path_length = graph.average_path_length()

  # Generate random graphs and calculate their average
  random_clustering_coefficients = []
  random_shortest_path_lengths = []

  for _ in range(n_trials):
    # Generate an Erdos-Renyi random graph
    p = 2.0 * n_edges / (n_nodes * (n_nodes - 1))
    random_graph = ig.Graph.Erdos_Renyi(n_nodes, p=p)

    clustering_coefficient_rand = random_graph.transitivity_undirected()
    shortest_path_length_rand = random_graph.average_path_length()

    random_clustering_coefficients.append(clustering_coefficient_rand)
    random_shortest_path_lengths.append(shortest_path_length_rand)

  clustering_coefficient_rand_avg = np.mean(random_clustering_coefficients)
  shortest_path_length_rand_avg = np.mean(random_shortest_path_lengths)

  # Handle potential division by zero
  if shortest_path_length_rand_avg == 0 or clustering_coefficient_rand_avg == 0:
    return 0  # Or raise an exception, depending on desired behavior

  # Calculate small-world-ness
  gamma = clustering_coefficient / clustering_coefficient_rand_avg
  lambda_val = shortest_path_length / shortest_path_length_rand_avg

  # Small worldness calculation (Watts and Strogatz: gamma / lambda)
  small_world = gamma / lambda_val

  return small_world

# Example usage:
# Create a sample graph (e.g., a Watts-Strogatz graph)
graph = ig.Graph.Watts_Strogatz(dim=1, size=100, nei=4, p=0)

# Calculate small-world-ness
sw = small_worldness(graph)
print(f"Small-world-ness: {sw}")
# %%

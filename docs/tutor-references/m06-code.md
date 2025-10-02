# Module 06: Centrality - Coding Implementation

This reference guide provides code examples for computing, visualizing, and analyzing various centrality measures using Python with the `igraph` library. The examples are aligned with the concepts and datasets discussed in the lecture notes.

## Setup

First, let's import the necessary libraries.

```python
import igraph
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

## 1. University Student Network Example

We'll start with the simple network of university students from the lecture to demonstrate how to compute various centrality measures.

### Creating the Network

```python
# Define the network structure
names = [
    "Sarah", "Mike", "Emma", "Alex", "Olivia", "James",
    "Sophia", "Ethan", "Ava", "Noah", "Lily", "Lucas", "Henry"
]
edge_list = [
    (0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (3, 5), (3, 6),
    (4, 5), (6, 7), (6, 8), (6, 9), (7, 8), (7, 9), (8, 9),
    (9, 10), (9, 11), (9, 12)
]

# Create the graph
g_student = igraph.Graph()
g_student.add_vertices(len(names))
g_student.vs["name"] = names
g_student.add_edges(edge_list)

# Plot the network
igraph.plot(g_student, vertex_label=g_student.vs["name"], bbox=(300, 300))
```

### Computing Centrality with `igraph`

`igraph` provides built-in functions for most standard centrality measures.

```python
# Compute various centrality measures
centralities = {
    'Degree': g_student.degree(),
    'Closeness': g_student.closeness(),
    'Harmonic': g_student.harmonic_centrality(),
    'Betweenness': g_student.betweenness(),
    'Eigenvector': g_student.eigenvector_centrality(),
    'PageRank': g_student.pagerank(),
    'Personalized PageRank (from Noah)': g_student.personalized_pagerank(reset_vertices=['Noah']),
    'Eccentricity': g_student.eccentricity()
}

# Display the results for a few nodes
for name, values in centralities.items():
    print(f"--- {name} Centrality ---")
    for i in range(5): # Print top 5 for brevity
        node_name = g_student.vs[i]['name']
        print(f"  {node_name}: {values[i]:.3f}")
    print()
```

## 2. Manual Katz Centrality Implementation

While `igraph` has a function for Katz centrality, implementing it manually helps in understanding the underlying algorithm. Here, we use the power iteration method from the lecture.

$$
\mathbf{c} = \beta \mathbf{1} + \alpha \mathbf{A} \mathbf{c}
$$

```python
def katz_centrality_manual(graph, alpha=0.1, beta=1.0, max_iter=100, tol=1e-6):
    """
    Computes Katz centrality using power iteration.
    
    Args:
        graph (igraph.Graph): The input graph.
        alpha (float): Attenuation factor. Must be less than 1 / largest eigenvalue of A.
        beta (float): Constant bias.
        max_iter (int): Maximum number of iterations.
        tol (float): Tolerance for convergence.
        
    Returns:
        numpy.ndarray: The Katz centrality scores for each node.
    """
    n_nodes = graph.vcount()
    A = graph.get_adjacency_sparse()
    c = np.ones((n_nodes, 1))  # Start with an initial guess

    for i in range(max_iter):
        c_next = beta * np.ones((n_nodes, 1)) + alpha * A @ c
        
        # Check for convergence
        if np.linalg.norm(c_next - c) < tol:
            print(f"Converged after {i+1} iterations.")
            return c_next.flatten()

        c = c_next
        
    print("Warning: Did not converge within max_iter.")
    return c.flatten()

# Calculate and display Katz centrality for the student network
# Note: alpha must be smaller than 1/lambda_max. For this graph, lambda_max is ~3.0.
katz_scores = katz_centrality_manual(g_student, alpha=0.1, beta=1.0)
print("\n--- Manual Katz Centrality ---")
for i, score in enumerate(katz_scores):
    print(f"  {g_student.vs[i]['name']}: {score:.3f}")
```

## 3. Case Study: Ancient Roman Roads

Now, let's apply these concepts to a real-world dataset: the network of ancient Roman roads.

### Load and Construct the Network

```python
# Load data from the web
root = "https://raw.githubusercontent.com/skojaku/adv-net-sci/main/data/roman-roads"
node_table = pd.read_csv(f"{root}/node_table.csv")
edge_table = pd.read_csv(f"{root}/edge_table.csv")

# Construct the graph
g_roman = igraph.Graph()
g_roman.add_vertices(node_table["node_id"].values)
g_roman.vs["name"] = node_table["label"].values
g_roman.add_edges(list(zip(edge_table["src"].values, edge_table["trg"].values)))

# Store coordinates for plotting
coord = list(zip(node_table["lon"].values, -node_table["lat"].values)) # Use negative lat for correct orientation
```

### Visualizing Centrality on the Map

A powerful way to interpret centrality is to visualize it geographically.

```python
def plot_centrality_on_map(graph, layout, scores, title, ax):
    """Helper function to plot centrality scores on a map."""
    
    # Normalize scores for color mapping
    min_score, max_score = np.min(scores), np.max(scores)
    if min_score == max_score:
        normalized_scores = np.ones_like(scores)
    else:
        normalized_scores = (np.array(scores) - min_score) / (max_score - min_score)

    cmap = plt.cm.magma
    vertex_color = [cmap(s) for s in normalized_scores]
    
    igraph.plot(
        graph,
        target=ax,
        layout=layout,
        vertex_size=15,
        vertex_color=vertex_color,
        vertex_label=None,
        edge_width=0.5,
        edge_color="#777777"
    )
    ax.set_title(title, fontsize=12)
    ax.set_axis_off()

# Compute centralities for the Roman network
roman_centralities = {
    'Degree': g_roman.degree(),
    'Betweenness': g_roman.betweenness(),
    'Closeness': g_roman.closeness(),
    'Eigenvector': g_roman.eigenvector_centrality()
}

# Create a comparison plot
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

for i, (name, scores) in enumerate(roman_centralities.items()):
    plot_centrality_on_map(g_roman, coord, scores, f"{name} Centrality", axes[i])

plt.tight_layout()
plt.show()
```

### Correlation Analysis

Let's analyze how different centrality measures correlate on the Roman roads network.

```python
def analyze_centrality_correlations(df_centralities):
    """Plots a heatmap of the correlation matrix."""
    corr_matrix = df_centralities.corr()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Centrality Measure Correlations (Roman Roads)')
    plt.tight_layout()
    plt.show()
    
    return corr_matrix

# Create a DataFrame from the computed centralities
df_roman_cent = pd.DataFrame(roman_centralities)
df_roman_cent['name'] = g_roman.vs['name']
df_roman_cent = df_roman_cent.set_index('name')

# Analyze and display correlation matrix
corr_matrix_roman = analyze_centrality_correlations(df_roman_cent)
print("\nCorrelation Matrix (Roman Roads):")
print(corr_matrix_roman.round(3))
```
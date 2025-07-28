# Preparation: Distance and Path Analysis Prerequisites

## Required Knowledge from Module 1

Before studying small-world networks, you should understand these concepts from the Euler Tour module:
- Basic graph representations (adjacency matrix, edge lists)
- Node degree calculations 
- Graph connectivity fundamentals

## Distance Measures in Networks

Small-world networks are fundamentally about distances between nodes. You'll need to understand:

### Shortest Path Distance
The **shortest path distance** between two nodes is the minimum number of edges in any path connecting them.

```python
import networkx as nx

# Calculate shortest path distances
G = nx.Graph()
G.add_edges_from([(1, 2), (2, 3), (3, 4), (1, 4)])
distance = nx.shortest_path_length(G, 1, 3)  # Returns 2
```

### Average Path Length
For network analysis, we often compute the average shortest path length across all pairs of nodes:

$$\langle d \rangle = \frac{1}{N(N-1)} \sum_{i \neq j} d_{ij}$$

where $d_{ij}$ is the shortest path distance between nodes $i$ and $j$.

## Clustering Concepts

### Local Clustering Coefficient
The clustering coefficient measures how densely connected a node's neighbors are:

$$C_i = \frac{2E_i}{k_i(k_i-1)}$$

where $E_i$ is the number of edges between neighbors of node $i$, and $k_i$ is the degree of node $i$.

### Global Clustering
The average clustering coefficient across all nodes provides a measure of local connectivity.

## Statistical Analysis Prerequisites

### Probability Distributions
You'll need basic understanding of:
- **Random variables** and their distributions
- **Expected values** and variance
- **Comparing observed vs. expected values**

### Network Models
Understanding of **random graphs** where edges are placed randomly with some probability will help contextualize small-world properties.

## Computational Prerequisites

### Algorithm Complexity
Basic understanding of computational complexity (O(n), O(n²)) for evaluating network analysis algorithms.

### Data Structures
Familiarity with:
- Lists and dictionaries for graph representations
- Efficient storage and retrieval of network data

These foundations will help you understand how small-world networks achieve the remarkable property of short average distances despite high local clustering.
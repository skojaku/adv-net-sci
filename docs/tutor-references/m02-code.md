# Module 02: Small-World Networks - Coding Implementation

## Network Analysis Libraries

### Primary Choice: igraph
```python
import igraph

# Installation
# pip install igraph cairocffi
# conda install -c conda-forge igraph cairocffi
```

**Advantages over NetworkX**:
- More reliable algorithm implementations
- Better performance (optimized C core)
- Comprehensive built-in functions

**Alternative**: scipy.csgraph for advanced users
```python
from scipy.sparse import csgraph
```

## Basic Graph Operations

### Creating Graphs
```python
# From edge list
edge_list = [(0, 1), (1, 2), (0, 2), (0, 3)]
g = igraph.Graph()
g.add_vertices(4)
g.add_edges(edge_list)

# Plot
igraph.plot(g, bbox=(150, 150), vertex_label=list(range(4)))
```

### Shortest Paths
```python
# All simple paths (expensive for large networks)
g.get_all_simple_paths(2, to=3)

# Shortest paths only
g.get_shortest_paths(2, to=3)

# Just distances (more efficient)
g.distances(2, 3)

# Average path length for entire network
g.average_path_length()
```

### Connected Components
```python
components = g.connected_components()

# Useful attributes
print("Membership:", components.membership)  # Component ID per node
print("Sizes:", list(components.sizes()))    # Nodes per component
print("Giant:", components.giant())          # Largest component subgraph
```

### Directed Networks
```python
# Create directed graph
g_directed = igraph.Graph(directed=True)
g_directed.add_vertices(6)
g_directed.add_edges(edge_list)

# Different connectivity types
strong_components = g.connected_components(mode="strong")
weak_components = g.connected_components(mode="weak")
```

## Clustering Coefficient Implementation

### Local Clustering
```python
# For each node
local_clustering = g.transitivity_local_undirected()

# Analyze specific nodes
for node in range(g.vcount()):
    neighbors = g.neighbors(node)
    degree = len(neighbors)
    clustering = local_clustering[node]
    
    print(f"Node {node}: degree={degree}, clustering={clustering:.3f}")
```

### Average Local Clustering
```python
# Direct calculation
avg_local_clustering = g.transitivity_avglocal_undirected()

# Manual verification
import numpy as np
manual_avg = np.nanmean(local_clustering)  # Ignores NaN values
```

### Global Clustering
```python
# Global clustering coefficient
global_clustering = g.transitivity_undirected()

# Understanding the calculation
triangles_count = len(g.list_triangles())
print(f"Triangles: {g.list_triangles()}")

# Count connected triples
triples = 0
for node in range(g.vcount()):
    degree = g.degree(node)
    if degree >= 2:
        triples += degree * (degree - 1) // 2

print(f"Global clustering = 3 * {triangles_count} / {triples}")
```

## Network Generators for Comparison

### Built-in Generators
```python
# Complete graph
g_complete = igraph.Graph.Full(n=6)

# Random graph (Erdős–Rényi)
g_random = igraph.Graph.Erdos_Renyi(n=20, p=0.2)

# Regular ring lattice
g_ring = igraph.Graph.Lattice(dim=[20], circular=True, nei=2)

# Small-world (Watts-Strogatz)
g_smallworld = igraph.Graph.Watts_Strogatz(
    dim=1, size=30, nei=3, p=0.1
)
```

### Network Comparison
```python
networks = {
    "Complete": g_complete,
    "Random": g_random,
    "Ring Lattice": g_ring,
    "Small-World": g_smallworld
}

print(f"{'Network':<15} {'Avg Local':<12} {'Global':<12} {'Path Length':<12}")
print("-" * 55)

for name, graph in networks.items():
    avg_local = graph.transitivity_avglocal_undirected()
    global_clust = graph.transitivity_undirected()
    avg_path = graph.average_path_length()
    
    print(f"{name:<15} {avg_local:<12.3f} {global_clust:<12.3f} {avg_path:<12.3f}")
```

## Small-World Index Calculation

### Reference Values for Random Networks
```python
def calculate_small_world_index(graph):
    # Actual network properties
    C_actual = graph.transitivity_avglocal_undirected()
    L_actual = graph.average_path_length()
    
    # Network parameters
    n = graph.vcount()
    k_avg = 2 * graph.ecount() / n  # Average degree
    
    # Random network reference values
    C_random = k_avg / (n - 1)
    L_random = np.log(n) / np.log(k_avg)
    
    # Small-world index
    sigma = (C_actual / C_random) / (L_actual / L_random)
    
    return sigma, C_actual, L_actual, C_random, L_random

# Example usage
sigma, C_act, L_act, C_rand, L_rand = calculate_small_world_index(g_smallworld)
print(f"Small-world index σ: {sigma:.3f}")
print(f"Clustering ratio: {C_act/C_rand:.3f}")
print(f"Path length ratio: {L_act/L_rand:.3f}")
```

## Watts-Strogatz Model Implementation

### Manual Implementation
```python
import numpy as np
import random

def watts_strogatz_manual(n, k, p):
    """
    Generate Watts-Strogatz small-world network
    
    n: number of nodes
    k: each node connected to k nearest neighbors  
    p: rewiring probability
    """
    g = igraph.Graph()
    g.add_vertices(n)
    
    # Step 1: Create ring lattice
    edges = []
    for i in range(n):
        for j in range(1, k//2 + 1):
            neighbor = (i + j) % n
            edges.append((i, neighbor))
    
    g.add_edges(edges)
    
    # Step 2: Rewire edges with probability p
    if p > 0:
        edges_to_rewire = list(g.get_edgelist())
        random.shuffle(edges_to_rewire)
        
        for edge in edges_to_rewire:
            if random.random() < p:
                # Remove original edge
                g.delete_edges([edge])
                
                # Rewire to random node
                start_node = edge[0]
                
                # Find valid targets (avoid self-loops and duplicates)
                possible_targets = set(range(n)) - {start_node}
                existing_neighbors = set(g.neighbors(start_node))
                valid_targets = list(possible_targets - existing_neighbors)
                
                if valid_targets:
                    new_target = random.choice(valid_targets)
                    g.add_edge(start_node, new_target)
    
    return g
```

### Using Built-in Function
```python
# Much simpler and more efficient
g_ws = igraph.Graph.Watts_Strogatz(dim=1, size=100, nei=4, p=0.1)
```

## Performance Analysis

### Path Length Estimation for Large Networks
```python
def estimate_average_path_length(graph, sample_size=1000):
    """
    Estimate average path length by sampling node pairs
    (Full calculation is O(n³), prohibitive for large networks)
    """
    n = graph.vcount()
    distances = []
    
    for _ in range(sample_size):
        # Sample two random nodes
        node1 = random.randint(0, n-1)
        node2 = random.randint(0, n-1)
        
        if node1 != node2:
            try:
                dist = graph.shortest_paths(node1, node2)[0][0]
                if dist != float('inf'):  # If connected
                    distances.append(dist)
            except:
                pass
    
    return np.mean(distances) if distances else float('inf')

# Usage for large networks
estimated_L = estimate_average_path_length(large_graph, sample_size=5000)
```

## Real-World Network Analysis

### Loading External Data
```python
import pandas as pd

# Load edge list from CSV
df = pd.read_csv('network_edges.csv')
edges = list(zip(df['source'], df['target']))

# Create graph
g_real = igraph.Graph()
g_real.add_vertices(max(max(edges)) + 1)  # Ensure enough vertices
g_real.add_edges(edges)

# Analyze small-world properties
sigma = calculate_small_world_index(g_real)
print(f"Real network small-world index: {sigma:.3f}")
```
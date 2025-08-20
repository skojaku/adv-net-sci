# Module 05: Clustering/Community Detection - Coding Implementation

## Basic Community Detection with igraph

### Modularity-Based Methods
```python
import igraph
import numpy as np

# Load or create network
g = igraph.Graph.Famous('Zachary')

# Louvain algorithm (fast modularity optimization)
communities_louvain = g.community_multilevel()

# Leiden algorithm (improved modularity optimization) 
communities_leiden = g.community_leiden()

# Print results
print(f"Louvain: {len(communities_louvain)} communities")
print(f"Leiden: {len(communities_leiden)} communities")
print(f"Louvain modularity: {communities_louvain.modularity:.3f}")
print(f"Leiden modularity: {communities_leiden.modularity:.3f}")
```

### Other Community Detection Algorithms
```python
# Label propagation
communities_lp = g.community_label_propagation()

# Edge betweenness (Girvan-Newman)
communities_eb = g.community_edge_betweenness()

# Spectral clustering
communities_spectral = g.community_leading_eigenvector()

# Compare results
methods = {
    'Louvain': communities_louvain,
    'Leiden': communities_leiden, 
    'Label Prop': communities_lp,
    'Spectral': communities_spectral
}

for name, comm in methods.items():
    print(f"{name}: {len(comm)} communities, Q={comm.modularity:.3f}")
```

## Modularity Calculation
```python
def calculate_modularity_manual(graph, communities):
    """Manual modularity calculation for understanding"""
    A = np.array(graph.get_adjacency().data)
    m = graph.ecount()
    degrees = np.array(graph.degree())
    
    modularity = 0
    for community in communities:
        for i in community:
            for j in community:
                expected = (degrees[i] * degrees[j]) / (2 * m)
                modularity += (A[i][j] - expected)
    
    return modularity / (2 * m)

# Verify against igraph calculation
manual_Q = calculate_modularity_manual(g, communities_louvain)
igraph_Q = communities_louvain.modularity
print(f"Manual Q: {manual_Q:.3f}, igraph Q: {igraph_Q:.3f}")
```

## Visualization
```python
import matplotlib.pyplot as plt

# Plot network with community colors
def plot_communities(graph, communities, title="Communities"):
    # Assign colors to communities
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    node_colors = []
    
    for node in range(graph.vcount()):
        for i, community in enumerate(communities):
            if node in community:
                node_colors.append(colors[i % len(colors)])
                break
    
    # Create layout
    layout = graph.layout_fruchterman_reingold()
    
    # Plot
    igraph.plot(graph, 
                bbox=(400, 400),
                layout=layout,
                vertex_color=node_colors,
                vertex_size=20,
                edge_width=0.5)

plot_communities(g, communities_louvain, "Louvain Communities")
```

## Evaluation Metrics
```python
def evaluate_communities(communities1, communities2):
    """Compare two community detections using NMI and ARI"""
    from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score
    
    # Convert to membership vectors
    n = max(max(comm) for comm in communities1) + 1
    
    membership1 = [0] * n
    for i, comm in enumerate(communities1):
        for node in comm:
            membership1[node] = i
    
    membership2 = [0] * n  
    for i, comm in enumerate(communities2):
        for node in comm:
            membership2[node] = i
    
    nmi = normalized_mutual_info_score(membership1, membership2)
    ari = adjusted_rand_score(membership1, membership2)
    
    return nmi, ari

# Compare methods
nmi, ari = evaluate_communities(communities_louvain, communities_leiden)
print(f"Louvain vs Leiden - NMI: {nmi:.3f}, ARI: {ari:.3f}")
```
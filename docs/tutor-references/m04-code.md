# Module 04: Node Degree - Coding Implementation

## Computing and Visualizing Degree Distributions

This section follows the narrative from the lecture notes, using a Barabási-Albert scale-free network to demonstrate best practices for visualizing heavy-tailed degree distributions.

### 1. Generating Network Data and Computing Degrees

We start by creating a scale-free network and calculating its degree distribution.

```python
import igraph
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import sparse

# Create a Barabási-Albert network with 10,000 nodes
g = igraph.Graph.Barabasi(n=10000, m=1)
A = g.get_adjacency()

# Compute degree for each node
deg = np.sum(A, axis=1).flatten()

# Convert to probability distribution (PDF)
p_deg = np.bincount(deg) / len(deg)
```

### 2. The Problem with Linear-Scale Histograms

A standard histogram on a linear scale fails to reveal the structure of the degree distribution because most nodes have very low degrees, hiding the long tail of high-degree hubs.

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax = sns.lineplot(x=np.arange(len(p_deg)), y=p_deg)
ax.set_xlabel('Degree')
ax.set_ylabel('Probability')
ax.set_title('Linear Scale: Most Information Hidden')
```

### 3. Using Log-Log Plots to Reveal Structure

Switching to logarithmic scales on both axes (a log-log plot) makes the underlying power-law structure visible. Power-law relationships appear as straight lines in log-log space.

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax = sns.lineplot(x=np.arange(len(p_deg)), y=p_deg)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylim(np.min(p_deg[p_deg>0])*0.01, None)
ax.set_xlabel('Degree')
ax.set_ylabel('Probability')
ax.set_title('Log-Log Scale: Structure Revealed')
```
While better, the plot is noisy in the tail due to statistical fluctuations.

### 4. The CCDF: The Standard for Visualizing Degree Distributions

The **Complementary Cumulative Distribution Function (CCDF)** is the preferred method. It plots the fraction of nodes with a degree *greater than* k. This smooths the data without arbitrary binning and provides a clear view of the distribution's tail.

```python
# Compute CCDF: fraction of nodes with degree > k
ccdf_deg = 1 - np.cumsum(p_deg)[:-1]  # Exclude last element (always 0)

fig, ax = plt.subplots(figsize=(8, 5))
ax = sns.lineplot(x=np.arange(len(ccdf_deg)), y=ccdf_deg)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Degree')
ax.set_ylabel('CCDF (Fraction of nodes with degree > k)')
ax.set_title('CCDF: Smooth Power-Law Visualization')
```
The CCDF produces a clean, interpretable curve, making it the standard for analyzing heavy-tailed distributions in network science.

## Implementing the Friendship Paradox

This section demonstrates the friendship paradox computationally using an efficient, edge-based sampling method as shown in the lecture.

### 1. Edge-Based Sampling to Find "Friends"

To correctly sample "friends," we sample edges uniformly at random. The endpoints of these edges represent the friends. High-degree nodes are part of more edges, so they are naturally overrepresented in this sample, which is the source of the paradox.

```python
# Extract all edges from the adjacency matrix
src, trg, _ = sparse.find(A)
print(f"Total number of edges: {len(src)}")

# Get degrees of "friends" (source nodes from the edge list)
deg_friend = deg[src]

# Compare average degrees
print(f"Average degree in network: {np.mean(deg):.2f}")
print(f"Average degree of friends: {np.mean(deg_friend):.2f}")
print(f"Friendship paradox ratio: {np.mean(deg_friend) / np.mean(deg):.2f}")
```

### 2. Visualizing the Degree Bias with CCDF

A side-by-side CCDF plot of the node degree distribution and the friend degree distribution provides the clearest visualization of the friendship paradox.

```python
# Compute degree distribution of friends
p_deg_friend = np.bincount(deg_friend) / len(deg_friend)

# Compute CCDFs for both distributions
ccdf_deg = 1 - np.cumsum(p_deg)[:-1]
ccdf_deg_friend = 1 - np.cumsum(p_deg_friend)[:-1]

# Create comparison plot
fig, ax = plt.subplots(figsize=(10, 6))
ax = sns.lineplot(x=np.arange(len(ccdf_deg)), y=ccdf_deg,
                  label='All Nodes (Uniform Sampling)', linewidth=2, color='blue')
ax = sns.lineplot(x=np.arange(len(ccdf_deg_friend)), y=ccdf_deg_friend,
                  label='Friends (Edge-Based Sampling)', linewidth=2, color='red', ax=ax)

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Degree')
ax.set_ylabel('CCDF')
ax.set_title('Friendship Paradox: Friends Have Higher Degrees')
ax.legend(frameon=False)
ax.grid(True, alpha=0.3)
```
The plot shows that the friend distribution (red) is shifted towards higher degrees compared to the general node population (blue), visually confirming the paradox.

## High-Degree Node Analysis

### Identify Hubs
```python
def identify_hubs(graph, method='top_k', k=5, threshold=None):
    """Identify high-degree nodes (hubs) in the network"""
    degrees = graph.degree()
    
    if method == 'top_k':
        # Top k highest degree nodes
        sorted_indices = np.argsort(degrees)[::-1]
        hub_indices = sorted_indices[:k]
    elif method == 'threshold':
        # Nodes above threshold
        hub_indices = [i for i, d in enumerate(degrees) if d >= threshold]
    elif method == 'percentile':
        # Nodes above percentile threshold
        threshold = np.percentile(degrees, threshold or 90)
        hub_indices = [i for i, d in enumerate(degrees) if d >= threshold]
    
    hubs = [{'node': i, 'degree': degrees[i]} for i in hub_indices]
    return sorted(hubs, key=lambda x: x['degree'], reverse=True)

# Find hubs
hubs = identify_hubs(g, method='top_k', k=5)
print("Top 5 hubs:")
for hub in hubs:
    print(f"Node {hub['node']}: degree {hub['degree']}")
```

### Hub Impact Analysis
```python
def analyze_hub_impact(graph, hub_nodes):
    """Analyze the impact of removing hub nodes"""
    original_components = len(graph.connected_components())
    original_largest = graph.connected_components().giant().vcount()
    
    results = []
    
    for hub in hub_nodes:
        # Create copy and remove hub
        g_test = graph.copy()
        g_test.delete_vertices(hub['node'])
        
        # Analyze impact
        new_components = len(g_test.connected_components())
        if g_test.vcount() > 0:
            new_largest = g_test.connected_components().giant().vcount()
        else:
            new_largest = 0
        
        results.append({
            'hub_node': hub['node'],
            'hub_degree': hub['degree'],
            'components_change': new_components - original_components,
            'largest_component_change': original_largest - new_largest,
            'connectivity_loss': (original_largest - new_largest) / graph.vcount()
        })
    
    return results

# Analyze hub removal impact
hub_impact = analyze_hub_impact(g, hubs)
for impact in hub_impact:
    print(f"Removing node {impact['hub_node']} (degree {impact['hub_degree']}): "
          f"{impact['connectivity_loss']:.2%} connectivity loss")
```

## Degree-Based Network Generation

### Scale-Free Network (Barabási-Albert Model)
```python
def generate_scale_free_network(n, m):
    """Generate scale-free network using preferential attachment"""
    g_sf = igraph.Graph.Barabasi(n, m)  # n nodes, m edges per new node
    return g_sf

# Generate and compare networks
g_random = igraph.Graph.Erdos_Renyi(100, 0.05)
g_scale_free = generate_scale_free_network(100, 2)

# Compare degree distributions
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.hist(g_random.degree(), alpha=0.7, label='Random')
ax1.set_title('Random Network')
ax1.set_xlabel('Degree')
ax1.set_ylabel('Count')

ax2.hist(g_scale_free.degree(), alpha=0.7, label='Scale-free', color='orange')
ax2.set_title('Scale-Free Network')
ax2.set_xlabel('Degree')
ax2.set_ylabel('Count')

plt.tight_layout()
```

## Degree Correlations

### Assortativity Measurement
```python
def calculate_degree_assortativity(graph):
    """Calculate degree assortativity coefficient"""
    return graph.assortativity_degree()

# Compare assortativity across networks
networks = {
    'Zachary': igraph.Graph.Famous('Zachary'),
    'Random': igraph.Graph.Erdos_Renyi(50, 0.1),
    'Scale-Free': igraph.Graph.Barabasi(50, 2)
}

print("Degree Assortativity:")
for name, graph in networks.items():
    assortativity = calculate_degree_assortativity(graph)
    print(f"{name}: {assortativity:.3f}")
```

## Performance Optimization

### Efficient Degree Calculations for Large Networks
```python
def efficient_degree_analysis(graph):
    """Efficient analysis for large networks"""
    # Vectorized degree calculation
    degrees = np.array(graph.degree())
    
    # Use numpy for statistics
    stats = {
        'mean': degrees.mean(),
        'std': degrees.std(),
        'percentiles': np.percentile(degrees, [25, 50, 75, 90, 95, 99])
    }
    
    return stats, degrees

# For very large networks, consider sampling
def sample_based_friendship_paradox(graph, sample_size=1000):
    """Sample-based friendship paradox analysis for large networks"""
    n = graph.vcount()
    sampled_nodes = np.random.choice(n, min(sample_size, n), replace=False)
    
    results = []
    for node in sampled_nodes:
        node_degree = graph.degree(node)
        if node_degree > 0:
            neighbors = graph.neighbors(node)
            avg_friend_degree = np.mean([graph.degree(neighbor) for neighbor in neighbors])
            results.append((node_degree, avg_friend_degree))
    
    if results:
        own_degrees, friend_degrees = zip(*results)
        return np.mean(own_degrees), np.mean(friend_degrees)
    return 0, 0
```
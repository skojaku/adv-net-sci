# Module 04: Node Degree - Coding Implementation

## Degree Calculation and Analysis

### Basic Degree Computation
```python
import igraph
import numpy as np
import matplotlib.pyplot as plt

# Create or load network
g = igraph.Graph.Famous('Zachary')

# Get degrees
degrees = g.degree()
print("Node degrees:", degrees)
print("Max degree:", max(degrees))
print("Min degree:", min(degrees))
print("Average degree:", np.mean(degrees))
```

### Degree Distribution Analysis
```python
from collections import Counter

def analyze_degree_distribution(graph):
    """Comprehensive degree distribution analysis"""
    degrees = graph.degree()
    
    # Basic statistics
    degree_stats = {
        'mean': np.mean(degrees),
        'std': np.std(degrees),
        'min': min(degrees),
        'max': max(degrees),
        'median': np.median(degrees)
    }
    
    # Degree distribution
    degree_counts = Counter(degrees)
    degree_values = sorted(degree_counts.keys())
    degree_frequencies = [degree_counts[k] for k in degree_values]
    degree_probabilities = [f/len(degrees) for f in degree_frequencies]
    
    return {
        'stats': degree_stats,
        'degree_values': degree_values,
        'frequencies': degree_frequencies,
        'probabilities': degree_probabilities,
        'raw_degrees': degrees
    }

# Analysis
dist_analysis = analyze_degree_distribution(g)
print("Degree statistics:", dist_analysis['stats'])
```

## Degree Distribution Visualization

### Basic Histogram
```python
def plot_degree_histogram(degrees, title="Degree Distribution"):
    """Plot degree distribution as histogram"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.hist(degrees, bins=range(min(degrees), max(degrees) + 2), 
            alpha=0.7, edgecolor='black')
    ax.set_xlabel('Degree')
    ax.set_ylabel('Number of Nodes')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
    return fig

plot_degree_histogram(g.degree())
```

### Log-Log Plot for Scale-Free Detection
```python
def plot_degree_distribution_loglog(graph, title="Degree Distribution (Log-Log)"):
    """Plot degree distribution on log-log scale to detect power laws"""
    degrees = graph.degree()
    degree_counts = Counter(degrees)
    
    # Filter out zero degrees for log scale
    degrees_nonzero = [k for k in degree_counts.keys() if k > 0]
    probabilities = [degree_counts[k]/len(degrees) for k in degrees_nonzero]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.loglog(degrees_nonzero, probabilities, 'bo', markersize=6)
    ax.set_xlabel('Degree (log scale)')
    ax.set_ylabel('P(degree) (log scale)')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
    return fig, degrees_nonzero, probabilities

plot_degree_distribution_loglog(g)
```

### Complementary Cumulative Distribution
```python
def plot_ccdf(degrees, title="Complementary Cumulative Distribution"):
    """Plot complementary cumulative distribution function"""
    sorted_degrees = np.sort(degrees)[::-1]  # Sort in descending order
    ccdf_values = np.arange(1, len(sorted_degrees) + 1) / len(sorted_degrees)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.loglog(sorted_degrees, ccdf_values, 'r-', linewidth=2)
    ax.set_xlabel('Degree (log scale)')
    ax.set_ylabel('P(Degree ≥ k) (log scale)')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
    return fig

plot_ccdf(g.degree())
```

## Friendship Paradox Implementation

### Calculate Friend Degrees
```python
def friendship_paradox_analysis(graph):
    """Analyze the friendship paradox in a network"""
    results = []
    
    for node in range(graph.vcount()):
        node_degree = graph.degree(node)
        neighbors = graph.neighbors(node)
        
        if neighbors:  # If node has neighbors
            neighbor_degrees = [graph.degree(neighbor) for neighbor in neighbors]
            avg_friend_degree = np.mean(neighbor_degrees)
        else:
            avg_friend_degree = 0
        
        results.append({
            'node': node,
            'degree': node_degree,
            'avg_friend_degree': avg_friend_degree,
            'paradox_difference': avg_friend_degree - node_degree
        })
    
    return results

# Analyze friendship paradox
fp_results = friendship_paradox_analysis(g)

# Summary statistics
own_degrees = [r['degree'] for r in fp_results if r['degree'] > 0]
friend_degrees = [r['avg_friend_degree'] for r in fp_results if r['degree'] > 0]

print(f"Average own degree: {np.mean(own_degrees):.2f}")
print(f"Average friend degree: {np.mean(friend_degrees):.2f}")
print(f"Friendship paradox holds: {np.mean(friend_degrees) > np.mean(own_degrees)}")
```

### Visualize Friendship Paradox
```python
def plot_friendship_paradox(results):
    """Visualize the friendship paradox"""
    # Filter nodes with degree > 0
    filtered = [r for r in results if r['degree'] > 0]
    own_degrees = [r['degree'] for r in filtered]
    friend_degrees = [r['avg_friend_degree'] for r in filtered]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Scatter plot
    ax1.scatter(own_degrees, friend_degrees, alpha=0.6)
    ax1.plot([0, max(own_degrees)], [0, max(own_degrees)], 'r--', label='y=x line')
    ax1.set_xlabel('Own Degree')
    ax1.set_ylabel('Average Friend Degree')
    ax1.set_title('Friendship Paradox')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Distribution comparison
    ax2.hist(own_degrees, alpha=0.5, label='Own degrees', bins=15)
    ax2.hist(friend_degrees, alpha=0.5, label='Friend degrees', bins=15)
    ax2.axvline(np.mean(own_degrees), color='blue', linestyle='--', label=f'Mean own: {np.mean(own_degrees):.1f}')
    ax2.axvline(np.mean(friend_degrees), color='orange', linestyle='--', label=f'Mean friend: {np.mean(friend_degrees):.1f}')
    ax2.set_xlabel('Degree')
    ax2.set_ylabel('Count')
    ax2.set_title('Degree Distributions')
    ax2.legend()
    
    plt.tight_layout()
    return fig

plot_friendship_paradox(fp_results)
```

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
# Module 07: Random Walks - Coding Implementation

## Basic Random Walk Simulation

### Simple Random Walk
```python
import igraph
import numpy as np
import matplotlib.pyplot as plt

def simulate_random_walk(graph, start_node, steps):
    """Simulate a single random walk"""
    walk = [start_node]
    current = start_node
    
    for _ in range(steps):
        neighbors = graph.neighbors(current)
        if neighbors:  # If node has neighbors
            current = np.random.choice(neighbors)
            walk.append(current)
        else:  # Dead end
            break
    
    return walk

# Example usage
g = igraph.Graph.Famous('Zachary')
walk = simulate_random_walk(g, start_node=0, steps=20)
print(f"Random walk: {walk[:10]}...")  # Show first 10 steps
```

### Multiple Random Walks
```python
def simulate_multiple_walks(graph, start_node, steps, num_walks):
    """Simulate multiple random walks from the same starting node"""
    walks = []
    for _ in range(num_walks):
        walk = simulate_random_walk(graph, start_node, steps)
        walks.append(walk)
    return walks

# Generate multiple walks
walks = simulate_multiple_walks(g, start_node=0, steps=100, num_walks=1000)

# Analyze visit frequencies
visit_counts = {}
for walk in walks:
    for node in walk:
        visit_counts[node] = visit_counts.get(node, 0) + 1

# Normalize to get empirical stationary distribution
total_visits = sum(visit_counts.values())
empirical_stationary = {node: count/total_visits for node, count in visit_counts.items()}
```

## Stationary Distribution Analysis

### Theoretical vs Empirical Comparison
```python
def analyze_stationary_distribution(graph):
    """Compare theoretical and empirical stationary distributions"""
    # Theoretical stationary distribution (degree/2m)
    degrees = np.array(graph.degree())
    total_degree = degrees.sum()
    theoretical_stationary = degrees / total_degree
    
    # Empirical distribution from random walks
    all_visits = {}
    num_walks = 1000
    walk_length = 1000
    
    for start_node in range(min(10, graph.vcount())):  # Sample starting nodes
        walks = simulate_multiple_walks(graph, start_node, walk_length, num_walks//10)
        for walk in walks:
            for node in walk[walk_length//2:]:  # Skip burn-in period
                all_visits[node] = all_visits.get(node, 0) + 1
    
    total_visits = sum(all_visits.values())
    empirical_stationary = np.zeros(graph.vcount())
    for node, count in all_visits.items():
        empirical_stationary[node] = count / total_visits
    
    return theoretical_stationary, empirical_stationary

# Compare distributions
theoretical, empirical = analyze_stationary_distribution(g)

print("Stationary Distribution Comparison (first 5 nodes):")
for i in range(5):
    print(f"Node {i}: Theoretical={theoretical[i]:.3f}, Empirical={empirical[i]:.3f}")
```

## Random Walk-Based Centrality

### Random Walk Betweenness
```python
def random_walk_betweenness(graph, num_walks=1000, walk_length=100):
    """Compute random walk betweenness centrality"""
    visit_counts = np.zeros(graph.vcount())
    
    # Generate random walks from all nodes
    for start_node in range(graph.vcount()):
        for _ in range(num_walks // graph.vcount()):
            walk = simulate_random_walk(graph, start_node, walk_length)
            for node in walk:
                visit_counts[node] += 1
    
    # Normalize
    total_visits = visit_counts.sum()
    rw_betweenness = visit_counts / total_visits
    
    return rw_betweenness

# Compute and compare with standard betweenness
rw_betweenness = random_walk_betweenness(g)
std_betweenness = np.array(g.betweenness())
std_betweenness = std_betweenness / std_betweenness.max()  # Normalize

print("Centrality Comparison (top 3 nodes by random walk betweenness):")
top_nodes = np.argsort(rw_betweenness)[-3:][::-1]
for node in top_nodes:
    print(f"Node {node}: RW={rw_betweenness[node]:.3f}, Std={std_betweenness[node]:.3f}")
```

## PageRank Implementation

### Basic PageRank
```python
def pagerank_power_iteration(graph, damping=0.85, max_iter=100, tol=1e-6):
    """Implement PageRank using power iteration"""
    n = graph.vcount()
    
    # Create transition matrix
    A = np.array(graph.get_adjacency().data, dtype=float)
    degrees = np.array(graph.degree(), dtype=float)
    
    # Handle degree-zero nodes
    degrees[degrees == 0] = 1
    
    # Create column-stochastic transition matrix
    T = A / degrees.reshape(1, -1)
    
    # PageRank matrix
    M = damping * T + (1 - damping) / n * np.ones((n, n))
    
    # Power iteration
    pr = np.ones(n) / n  # Initial distribution
    
    for iteration in range(max_iter):
        pr_new = M @ pr
        
        # Check convergence
        if np.linalg.norm(pr_new - pr) < tol:
            print(f"Converged after {iteration + 1} iterations")
            break
            
        pr = pr_new
    
    return pr

# Compare with igraph implementation
manual_pr = pagerank_power_iteration(g)
igraph_pr = np.array(g.pagerank())

print("PageRank Comparison (first 5 nodes):")
for i in range(5):
    print(f"Node {i}: Manual={manual_pr[i]:.4f}, igraph={igraph_pr[i]:.4f}")
```

## Community Detection via Random Walks

### Walktrap Algorithm Concept
```python
def compute_walk_similarities(graph, walk_length=4):
    """Compute similarity between nodes based on random walk distributions"""
    n = graph.vcount()
    similarities = np.zeros((n, n))
    
    # For each node, compute where random walks end up
    for start_node in range(n):
        end_distributions = {}
        
        # Generate many short walks
        for _ in range(1000):
            walk = simulate_random_walk(graph, start_node, walk_length)
            end_node = walk[-1]
            end_distributions[end_node] = end_distributions.get(end_node, 0) + 1
        
        # Normalize to get distribution
        total = sum(end_distributions.values())
        for end_node in end_distributions:
            end_distributions[end_node] /= total
        
        # Store as vector
        distribution = np.zeros(n)
        for end_node, prob in end_distributions.items():
            distribution[end_node] = prob
        
        # Compute similarities with all other nodes
        for other_node in range(n):
            if other_node != start_node:
                # This would require computing distribution for other_node too
                # Simplified version - just use walk ending probabilities
                pass
    
    return similarities

# Use igraph's built-in walktrap
communities_walktrap = g.community_walktrap()
print(f"Walktrap found {len(communities_walktrap)} communities")
print(f"Modularity: {communities_walktrap.modularity:.3f}")
```

## Visualization and Analysis

### Walk Trajectory Visualization
```python
def visualize_random_walk(graph, walk, title="Random Walk Path"):
    """Visualize a random walk path on the network"""
    layout = graph.layout_fruchterman_reingold()
    
    # Create edge list for walk path
    walk_edges = [(walk[i], walk[i+1]) for i in range(len(walk)-1)]
    
    # Count edge usage
    edge_counts = {}
    for edge in walk_edges:
        edge_key = tuple(sorted(edge))  # Undirected
        edge_counts[edge_key] = edge_counts.get(edge_key, 0) + 1
    
    # Set edge widths based on usage
    edge_widths = []
    for edge in graph.get_edgelist():
        edge_key = tuple(sorted(edge))
        width = edge_counts.get(edge_key, 0) + 1
        edge_widths.append(width)
    
    # Plot
    igraph.plot(graph,
                layout=layout,
                vertex_size=15,
                vertex_color='lightblue',
                edge_width=edge_widths,
                bbox=(400, 400))
    
    return walk_edges

# Visualize a random walk
long_walk = simulate_random_walk(g, start_node=0, steps=50)
walk_edges = visualize_random_walk(g, long_walk)
print(f"Walk visited {len(set(long_walk))} unique nodes out of {g.vcount()} total")
```
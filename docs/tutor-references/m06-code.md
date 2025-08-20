# Module 06: Centrality - Coding Implementation

## Computing Centrality Measures with igraph

### Basic Centrality Measures
```python
import igraph
import numpy as np
import matplotlib.pyplot as plt

# Create or load network
g = igraph.Graph.Famous('Zachary')

# Compute various centrality measures
centralities = {
    'degree': g.degree(),
    'closeness': g.closeness(),
    'betweenness': g.betweenness(),
    'eigenvector': g.eigenvector_centrality(),
    'pagerank': g.pagerank(),
    'katz': g.authority_score()  # Similar to Katz centrality
}

# Display top nodes for each measure
for name, values in centralities.items():
    top_nodes = np.argsort(values)[-3:][::-1]  # Top 3 nodes
    print(f"{name.capitalize()} centrality top 3:")
    for i, node in enumerate(top_nodes):
        print(f"  {i+1}. Node {node}: {values[node]:.3f}")
    print()
```

### Centrality Correlation Analysis
```python
import pandas as pd
import seaborn as sns

def analyze_centrality_correlations(graph):
    """Analyze correlations between different centrality measures"""
    centralities = {
        'Degree': graph.degree(),
        'Closeness': graph.closeness(),
        'Betweenness': graph.betweenness(),
        'Eigenvector': graph.eigenvector_centrality(),
        'PageRank': graph.pagerank()
    }
    
    # Create DataFrame
    df = pd.DataFrame(centralities)
    
    # Compute correlation matrix
    corr_matrix = df.corr()
    
    # Plot heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Centrality Measure Correlations')
    plt.tight_layout()
    
    return df, corr_matrix

df_cent, corr_matrix = analyze_centrality_correlations(g)
print("Correlation Matrix:")
print(corr_matrix.round(3))
```

### Custom Centrality Implementation
```python
def closeness_centrality_manual(graph):
    """Manual implementation of closeness centrality"""
    n = graph.vcount()
    closeness = []
    
    for node in range(n):
        # Get shortest paths from this node to all others
        distances = graph.shortest_paths(source=node)[0]
        
        # Filter out infinite distances (disconnected nodes)
        finite_distances = [d for d in distances if d != float('inf') and d > 0]
        
        if finite_distances:
            closeness_val = (len(finite_distances)) / sum(finite_distances)
        else:
            closeness_val = 0.0
        
        closeness.append(closeness_val)
    
    return closeness

# Compare with igraph implementation
manual_closeness = closeness_centrality_manual(g)
igraph_closeness = g.closeness()

print("Manual vs igraph closeness (first 5 nodes):")
for i in range(5):
    print(f"Node {i}: Manual={manual_closeness[i]:.3f}, igraph={igraph_closeness[i]:.3f}")
```

## Centrality Visualization
```python
def plot_centrality_comparison(graph, centrality_dict):
    """Plot network with different centrality measures"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    layout = graph.layout_fruchterman_reingold()
    
    for idx, (name, values) in enumerate(centrality_dict.items()):
        if idx >= 6:  # Only plot first 6 measures
            break
            
        # Normalize values for visualization
        norm_values = np.array(values)
        if norm_values.max() > 0:
            norm_values = norm_values / norm_values.max()
        
        # Create vertex sizes based on centrality
        vertex_sizes = 10 + 40 * norm_values
        
        # Plot on subplot
        igraph.plot(graph,
                    target=axes[idx],
                    layout=layout,
                    vertex_size=vertex_sizes,
                    vertex_color='lightblue',
                    edge_width=0.5,
                    bbox=(200, 200))
        axes[idx].set_title(f'{name.capitalize()} Centrality')
    
    # Hide unused subplots
    for idx in range(len(centrality_dict), 6):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    return fig

plot_centrality_comparison(g, centralities)
```

## Advanced Applications
```python
def identify_key_players(graph, top_k=5):
    """Identify key players using multiple centrality measures"""
    measures = {
        'degree': graph.degree(),
        'betweenness': graph.betweenness(),
        'eigenvector': graph.eigenvector_centrality(),
        'pagerank': graph.pagerank()
    }
    
    # Rank nodes for each measure
    rankings = {}
    for name, values in measures.items():
        rankings[name] = np.argsort(values)[::-1]  # Descending order
    
    # Find nodes that appear in top-k for multiple measures
    top_nodes = set()
    node_scores = {}
    
    for node in range(graph.vcount()):
        score = 0
        for name, ranking in rankings.items():
            if node in ranking[:top_k]:
                score += 1
        node_scores[node] = score
        if score >= 2:  # Appears in top-k of at least 2 measures
            top_nodes.add(node)
    
    # Sort by score
    key_players = sorted(node_scores.items(), key=lambda x: x[1], reverse=True)
    
    return key_players[:top_k], rankings

key_players, rankings = identify_key_players(g)
print("Key players (appearing in multiple top-5 lists):")
for node, score in key_players:
    print(f"Node {node}: appears in {score} top-5 lists")
```
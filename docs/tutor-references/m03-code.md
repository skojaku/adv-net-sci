# Module 03: Network Robustness - Coding Implementation

## Core Libraries for Robustness Analysis

### Primary Choice: igraph
```python
import igraph
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Installation: pip install igraph cairocffi
# or: conda install -c conda-forge igraph cairocffi
```

**Advantages**: Reliable connected component algorithms, efficient graph operations, comprehensive network analysis functions.

**Alternative**: scipy.sparse.csgraph for high-performance connectivity analysis.

## Connectivity Measurement

### Basic Connectivity Function
```python
def network_connectivity(graph, original_size=None):
    """Calculate network connectivity as fraction of nodes in largest component"""
    if original_size is None:
        original_size = graph.vcount()
    
    if graph.vcount() == 0:
        return 0.0
    
    components = graph.connected_components()
    return max(components.sizes()) / original_size
```

### Connected Components Analysis
```python
# Create test network (Zachary's karate club)
g = igraph.Graph.Famous('Zachary')

# Analyze components
components = g.connected_components()
print("Number of components:", len(components))
print("Component sizes:", list(components.sizes()))
print("Largest component size:", components.giant().vcount())

# Current connectivity
connectivity = network_connectivity(g)
print(f"Current connectivity: {connectivity:.3f}")
```

## Random Attack Simulation

### Basic Random Attack
```python
def simulate_random_attack(graph):
    """Simulate random node removal and measure connectivity"""
    g_test = graph.copy()
    original_size = g_test.vcount()
    results = []
    
    for i in range(original_size - 1):  # Remove all but one node
        # Randomly select and remove a node
        node_idx = np.random.choice(g_test.vs.indices)
        g_test.delete_vertices(node_idx)
        
        # Measure connectivity
        connectivity = network_connectivity(g_test, original_size)
        
        # Store results
        results.append({
            "connectivity": connectivity,
            "frac_nodes_removed": (i + 1) / original_size,
        })
    
    return pd.DataFrame(results)

# Run simulation
df_random = simulate_random_attack(g)
```

### Multiple Random Attack Runs
```python
def simulate_multiple_random_attacks(graph, n_runs=100):
    """Run multiple random attack simulations for statistical reliability"""
    all_results = []
    
    for run in range(n_runs):
        df_run = simulate_random_attack(graph)
        df_run['run'] = run
        all_results.append(df_run)
    
    return pd.concat(all_results, ignore_index=True)

# Statistical analysis
df_random_multi = simulate_multiple_random_attacks(g, n_runs=50)

# Calculate mean and confidence intervals
stats = df_random_multi.groupby('frac_nodes_removed')['connectivity'].agg([
    'mean', 'std', 'count'
]).reset_index()
```

## Targeted Attack Simulation

### High-Degree Attack Strategy
```python
def simulate_targeted_attack(graph, strategy='degree'):
    """Simulate targeted node removal based on various strategies"""
    g_test = graph.copy()
    original_size = g_test.vcount()
    results = []
    
    for i in range(original_size - 1):
        # Select target based on strategy
        if strategy == 'degree':
            # Target highest degree node
            degrees = g_test.degree()
            target_idx = np.argmax(degrees)
        elif strategy == 'betweenness':
            # Target highest betweenness centrality node
            betweenness = g_test.betweenness()
            target_idx = np.argmax(betweenness)
        elif strategy == 'closeness':
            # Target highest closeness centrality node
            closeness = g_test.closeness()
            target_idx = np.argmax(closeness)
        
        # Remove target node
        g_test.delete_vertices(target_idx)
        
        # Measure connectivity
        connectivity = network_connectivity(g_test, original_size)
        
        results.append({
            "connectivity": connectivity,
            "frac_nodes_removed": (i + 1) / original_size,
            "strategy": strategy
        })
    
    return pd.DataFrame(results)

# Run targeted attacks with different strategies
df_degree = simulate_targeted_attack(g, 'degree')
df_betweenness = simulate_targeted_attack(g, 'betweenness')
df_closeness = simulate_targeted_attack(g, 'closeness')
```

### Advanced Targeting Strategies
```python
def simulate_adaptive_attack(graph):
    """Adaptive attack: recalculate centrality after each removal"""
    g_test = graph.copy()
    original_size = g_test.vcount()
    results = []
    
    for i in range(original_size - 1):
        # Recalculate degrees after each removal
        degrees = g_test.degree()
        target_idx = np.argmax(degrees)
        
        g_test.delete_vertices(target_idx)
        connectivity = network_connectivity(g_test, original_size)
        
        results.append({
            "connectivity": connectivity,
            "frac_nodes_removed": (i + 1) / original_size,
            "strategy": "adaptive_degree"
        })
    
    return pd.DataFrame(results)
```

## Robustness Profile Visualization

### Basic Plotting
```python
import seaborn as sns

def plot_robustness_profiles(dataframes, labels, title="Network Robustness"):
    """Plot multiple robustness profiles for comparison"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    
    for i, (df, label) in enumerate(zip(dataframes, labels)):
        ax.plot(df["frac_nodes_removed"], df["connectivity"], 
                'o-', linewidth=2, markersize=4, 
                label=label, color=colors[i % len(colors)])
    
    ax.set_xlabel("Fraction of nodes removed")
    ax.set_ylabel("Connectivity")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# Compare strategies
dataframes = [df_random, df_degree, df_betweenness]
labels = ['Random Attack', 'Degree Attack', 'Betweenness Attack']
plot_robustness_profiles(dataframes, labels)
```

### Statistical Visualization with Confidence Intervals
```python
def plot_statistical_robustness(df_multi, title="Robustness with Confidence Intervals"):
    """Plot robustness profile with confidence intervals"""
    # Calculate statistics
    stats = df_multi.groupby('frac_nodes_removed')['connectivity'].agg([
        'mean', 'std', 'count'
    ]).reset_index()
    
    # Calculate confidence intervals
    confidence = 0.95
    t_value = 1.96  # Approximate for large samples
    stats['ci'] = t_value * stats['std'] / np.sqrt(stats['count'])
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot mean line
    ax.plot(stats['frac_nodes_removed'], stats['mean'], 
            'o-', linewidth=2, label='Mean', color='blue')
    
    # Fill confidence interval
    ax.fill_between(stats['frac_nodes_removed'],
                    stats['mean'] - stats['ci'],
                    stats['mean'] + stats['ci'],
                    alpha=0.3, color='blue', label=f'{confidence*100}% CI')
    
    ax.set_xlabel("Fraction of nodes removed")
    ax.set_ylabel("Connectivity") 
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig
```

## R-Index Calculation

### Robustness Index Implementation
```python
def calculate_r_index(connectivity_series):
    """Calculate R-index (area under robustness curve)"""
    # R-index is the normalized area under the curve
    return np.trapz(connectivity_series) / len(connectivity_series)

# Calculate R-indices for different attack strategies
r_random = calculate_r_index(df_random['connectivity'])
r_degree = calculate_r_index(df_degree['connectivity'])
r_betweenness = calculate_r_index(df_betweenness['connectivity'])

print("R-Index Comparison:")
print(f"Random attack: {r_random:.3f}")
print(f"Degree attack: {r_degree:.3f}")
print(f"Betweenness attack: {r_betweenness:.3f}")
```

### Comprehensive Robustness Analysis
```python
def comprehensive_robustness_analysis(graph, n_random_runs=50):
    """Complete robustness analysis with multiple strategies"""
    results = {}
    
    # Random attack (multiple runs for statistics)
    print("Running random attacks...")
    df_random_multi = simulate_multiple_random_attacks(graph, n_random_runs)
    df_random_mean = df_random_multi.groupby('frac_nodes_removed')['connectivity'].mean().reset_index()
    results['random'] = df_random_mean
    
    # Targeted attacks
    strategies = ['degree', 'betweenness', 'closeness']
    for strategy in strategies:
        print(f"Running {strategy} attack...")
        df_targeted = simulate_targeted_attack(graph, strategy)
        results[strategy] = df_targeted
    
    # Calculate R-indices
    r_indices = {}
    for name, df in results.items():
        r_indices[name] = calculate_r_index(df['connectivity'])
    
    return results, r_indices

# Run comprehensive analysis
results, r_indices = comprehensive_robustness_analysis(g)

# Display results
print("\nR-Index Rankings (higher = more robust):")
for strategy, r_value in sorted(r_indices.items(), key=lambda x: x[1], reverse=True):
    print(f"{strategy:12}: {r_value:.3f}")
```

## Network Comparison

### Multi-Network Robustness Comparison
```python
def compare_network_robustness(networks, network_names):
    """Compare robustness across different network types"""
    comparison_results = {}
    
    for name, graph in zip(network_names, networks):
        print(f"Analyzing {name}...")
        
        # Quick robustness analysis
        df_random = simulate_random_attack(graph)
        df_degree = simulate_targeted_attack(graph, 'degree')
        
        comparison_results[name] = {
            'random': calculate_r_index(df_random['connectivity']),
            'degree_attack': calculate_r_index(df_degree['connectivity']),
            'size': graph.vcount(),
            'edges': graph.ecount(),
            'avg_degree': 2 * graph.ecount() / graph.vcount()
        }
    
    return pd.DataFrame(comparison_results).T

# Example: Compare different network types
networks = [
    igraph.Graph.Famous('Zachary'),
    igraph.Graph.Erdos_Renyi(50, 0.1),
    igraph.Graph.Barabasi(50, 2)
]
names = ['Zachary Karate', 'Random Network', 'Scale-Free']

comparison_df = compare_network_robustness(networks, names)
print("Network Robustness Comparison:")
print(comparison_df.round(3))
```

## Performance Optimization

### Efficient Large Network Analysis  
```python
def efficient_robustness_sample(graph, n_removals=100):
    """Sample-based robustness analysis for large networks"""
    original_size = graph.vcount()
    
    # Sample removal fractions
    removal_fractions = np.linspace(0.01, 0.99, n_removals)
    
    results = []
    for frac in removal_fractions:
        g_test = graph.copy()
        
        # Remove fraction of nodes randomly
        n_remove = int(frac * original_size)
        nodes_to_remove = np.random.choice(
            g_test.vs.indices, size=n_remove, replace=False
        )
        
        g_test.delete_vertices(nodes_to_remove)
        connectivity = network_connectivity(g_test, original_size)
        
        results.append({
            'frac_nodes_removed': frac,
            'connectivity': connectivity
        })
    
    return pd.DataFrame(results)
```
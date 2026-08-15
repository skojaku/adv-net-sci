# Module 01: Euler Tour - Coding Implementation

## Network Representations

Three fundamental ways to represent networks computationally:

### 1. Edge Table (Edge List)
Direct listing of connections as pairs - most intuitive for data storage:
```python
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4)]
```

### 2. Adjacency List
Dictionary storing each node's neighbors - optimal for graph algorithms:
```python
neighbors = {
    0: [1, 2],     # Node 0 connects to nodes 1 and 2
    1: [0, 2, 3],  # Node 1 connects to nodes 0, 2, and 3
    2: [0, 1, 4],  # etc.
    3: [1, 4],
    4: [2, 3]
}
```

### 3. Adjacency Matrix
Grid where entry (i,j) = 1 if nodes connected - enables matrix operations:
```python
import numpy as np
matrix = np.array([
    [0, 1, 1, 0, 0],  # Node 0 connects to nodes 1, 2
    [1, 0, 1, 1, 0],  # Node 1 connects to nodes 0, 2, 3
    [1, 1, 0, 0, 1],  # etc.
    [0, 1, 0, 0, 1],
    [0, 0, 1, 1, 0]
])
```

## Computing Node Degrees

### From Adjacency Matrix (Vectorized)
```python
degrees = matrix.sum(axis=1)  # Sum rows for undirected graphs
```

### From Edge List
```python
degrees = [0] * num_nodes
for node1, node2 in edges:
    degrees[node1] += 1
    degrees[node2] += 1
```

### From Adjacency List
```python
degrees = [len(neighbors[i]) for i in range(num_nodes)]
```

## Verification Algorithms

### Walk Verification
```python
def is_walk(sequence, adjacency_matrix):
    if len(sequence) < 2:
        return True
    
    sequence = np.array(sequence)
    current_nodes = sequence[:-1]
    next_nodes = sequence[1:]
    
    # Check all edges exist using vectorized operations
    edges_exist = adjacency_matrix[current_nodes, next_nodes]
    return np.all(edges_exist == 1)
```

### Trail Verification (No Repeated Edges)
```python
def is_trail(sequence, adjacency_matrix):
    if not is_walk(sequence, adjacency_matrix):
        return False
    
    if len(sequence) < 2:
        return True
    
    sequence = np.array(sequence)
    current_nodes = sequence[:-1]
    next_nodes = sequence[1:]
    
    # Use complex numbers to represent edges efficiently
    edge_starts = np.minimum(current_nodes, next_nodes)
    edge_ends = np.maximum(current_nodes, next_nodes)
    complex_edges = edge_starts + 1j * edge_ends
    
    # Check uniqueness
    return len(complex_edges) == len(np.unique(complex_edges))
```

### Path Verification (No Repeated Nodes)
```python
def is_path(sequence, adjacency_matrix):
    if not is_walk(sequence, adjacency_matrix):
        return False
    
    sequence = np.array(sequence)
    return len(sequence) == len(np.unique(sequence))
```

## Connected Components

### Depth-First Search Algorithm
```python
def connected_components(adjacency_matrix):
    n = adjacency_matrix.shape[0]
    visited = np.zeros(n, dtype=bool)
    components = []
    
    def dfs(node, component):
        visited[node] = True
        component.append(node)
        
        # Find neighbors using vectorized operation
        neighbors = np.where(adjacency_matrix[node] > 0)[0]
        
        for neighbor in neighbors:
            if not visited[neighbor]:
                dfs(neighbor, component)
    
    for v in range(n):
        if not visited[v]:
            component = []
            dfs(v, component)
            components.append(component)
    
    return components
```

## Complete Euler Path Implementation

```python
def has_euler_path_complete(adjacency_matrix):
    # Check connectivity
    components = connected_components(adjacency_matrix)
    
    # Find nodes with edges (degree > 0)
    degrees = adjacency_matrix.sum(axis=1)
    non_isolated_nodes = np.where(degrees > 0)[0]
    
    if len(non_isolated_nodes) == 0:
        return True  # Empty graph has Euler path
    
    # Verify all non-isolated nodes are in same component
    component_with_edges = None
    for component in components:
        if non_isolated_nodes[0] in component:
            component_with_edges = set(component)
            break
    
    if not all(node in component_with_edges for node in non_isolated_nodes):
        return False  # Disconnected
    
    # Check degree conditions
    non_isolated_degrees = degrees[non_isolated_nodes]
    odd_degree_count = np.sum(non_isolated_degrees % 2)
    
    # Euler's theorem: exactly 0 or 2 odd-degree nodes
    return odd_degree_count == 0 or odd_degree_count == 2
```

## Performance Optimization Tips

- **Avoid Python loops**: Use NumPy vectorized operations when possible
- **Complex numbers for edges**: Represent undirected edges as `min_node + 1j * max_node`
- **Advanced indexing**: Use `matrix[rows, cols]` for batch edge checking
- **Memory efficiency**: Choose representation based on network density

## Computational Complexity

- **Degree calculation**: O(n²) for adjacency matrix, O(E) for edge list
- **Walk verification**: O(k) where k is sequence length  
- **Connected components**: O(n²) using DFS with adjacency matrix
- **Complete Euler check**: O(n²) dominated by connectivity verification
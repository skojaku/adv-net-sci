---
title: Preparation - Python and Graph Basics
---

## Necessary Python Libraries

```python
# Core library for high-performance graph analysis
import igraph as ig

# Supporting libraries for computation and visualization
import numpy as np
from scipy import sparse
```

### Library Explanations

**igraph**: High-performance graph analysis library written in C with Python bindings. Offers 10-100x better performance than NetworkX for graph operations - crucial when working with complex algorithms like Euler tour detection.

**NumPy**: The foundation of scientific computing in Python. Provides:
- **Efficient arrays**: Fast operations on large datasets
- **Mathematical functions**: Linear algebra, statistics, and array operations
- **Memory efficiency**: Dense arrays stored contiguously in memory
- *For graphs*: Stores adjacency matrices, degree sequences, and numerical computations

**SciPy Sparse**: Specialized for handling sparse matrices where most elements are zero. Essential for large graphs because:
- **Memory savings**: Real networks are typically sparse (few edges relative to possible connections)
- **Speed**: Operations only computed on non-zero elements
- **Graph applications**: Adjacency matrices of large networks (social media, web graphs) are naturally sparse

::: {#fig-sparse-example}
```python
# Example: 1000x1000 adjacency matrix with only 5000 edges
# Dense matrix: 1,000,000 elements stored
# Sparse matrix: only 5000 non-zero elements stored (99.5% memory savings!)

import numpy as np
from scipy import sparse

# Dense matrix (memory intensive)
dense_adj = np.zeros((1000, 1000))

# Sparse matrix (memory efficient) 
edges = [(0, 1), (1, 2), (2, 999)]  # Few connections
sparse_adj = sparse.csr_matrix((1000, 1000))
```

**Key insight**: Real-world networks are sparse - Facebook users aren't friends with everyone, web pages don't link to every other page, proteins don't interact with all others.
:::

### How These Libraries Work Together

::: {#fig-library-integration}
```python
import igraph as ig
import numpy as np
from scipy import sparse

# Create a graph with igraph
g = ig.Graph([(0, 1), (1, 2), (2, 3), (0, 3)])

# Get adjacency matrix as NumPy array (for small graphs)
adj_dense = np.array(g.get_adjacency().data)
print("Dense adjacency matrix:")
print(adj_dense)

# For large graphs, use sparse representation
adj_sparse = sparse.csr_matrix(adj_dense)
print(f"\nMemory usage - Dense: {adj_dense.nbytes} bytes")
print(f"Memory usage - Sparse: {adj_sparse.data.nbytes + adj_sparse.indices.nbytes + adj_sparse.indptr.nbytes} bytes")

# Compute degrees using NumPy (sum rows of adjacency matrix)
degrees_numpy = np.sum(adj_dense, axis=1)
degrees_igraph = g.degree()
print(f"\nDegrees (NumPy): {degrees_numpy}")
print(f"Degrees (igraph): {degrees_igraph}")
```

This integration is powerful for Euler tour algorithms where you need fast degree calculations and efficient graph traversals.
:::

## Quick igraph Reference

### Basic Graph Creation

```python
# Create from edge list (most common)
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
g = ig.Graph(edges)

# Create empty graph and add elements
g = ig.Graph()
g.add_vertices(4)
g.add_edges([(0, 1), (1, 2), (2, 3), (3, 0)])

# Create with attributes
g = ig.Graph(edges=[(0, 1), (1, 2)],
             vertex_attrs={'name': ['A', 'B', 'C', 'D']})
```

### Essential Graph Properties

```python
# Basic properties
print(f"Vertices: {g.vcount()}")
print(f"Edges: {g.ecount()}")
print(f"Connected: {g.is_connected()}")

# Degree analysis (crucial for Euler tours!)
degrees = g.degree()
print(f"Degrees: {degrees}")
print(f"Odd degree vertices: {sum(1 for d in degrees if d % 2 == 1)}")
```

### Useful Operations for Euler Tours

```python
# Check if vertex has odd/even degree
vertex_id = 0
is_odd_degree = g.degree(vertex_id) % 2 == 1

# Get neighbors of a vertex
neighbors = g.neighbors(vertex_id)

# Remove an edge (useful for algorithm implementation)
edge_id = g.get_eid(0, 1)  # Get edge ID between vertices 0 and 1
g.delete_edges([edge_id])

# Copy graph for experimentation
g_copy = g.copy()
```

### Data Structures You'll Need

```python
# Stack for DFS-based algorithms
stack = []
stack.append(vertex)
current = stack.pop()

# Set for tracking visited elements
visited = set()
visited.add(vertex)

# List for building paths
path = []
path.append(vertex)
```

## Quick Test: Can You Find an Euler Tour?

```python
# Create a simple graph
g = ig.Graph([(0, 1), (1, 2), (2, 0)])

# Check degrees
degrees = g.degree()
odd_vertices = [v for v in range(g.vcount()) if degrees[v] % 2 == 1]

print(f"Degrees: {degrees}")
print(f"Odd degree vertices: {len(odd_vertices)}")
print(f"Has Euler cycle: {len(odd_vertices) == 0}")
print(f"Has Euler path: {len(odd_vertices) in [0, 2]}")
```

::: {.column-margin}
**Remember Euler's rule**: A graph has an Euler cycle if all vertices have even degree, and an Euler path if exactly 0 or 2 vertices have odd degree.
:::

## What's Next?

You're now equipped with the essential tools for Euler tour algorithms. In the next sections, you'll:

1. **Learn** the historical Königsberg bridge problem that started it all
2. **Understand** the mathematical theory behind Eulerian paths
3. **Implement** algorithms to find Euler tours in any graph
4. **Apply** these concepts to real-world problems

The beauty of Euler's insight was seeing that complex geometric problems could be solved with simple rules about connections. Let's discover how this 18th-century breakthrough still powers modern algorithms today.
---
title: Preparation - Python and Graph Basics
---

## Getting Ready for Euler Tours

This module explores one of mathematics' most elegant problems - finding paths that visit every connection exactly once. Before diving into the historical puzzle and algorithms, let's set up the computational tools you'll need to implement and experiment with Eulerian path algorithms.

## Essential Python Setup

### Required Libraries

```python
# Core library for high-performance graph analysis
import igraph as ig

# Supporting libraries for computation and visualization  
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, deque
```

::: {.column-margin}
**Why igraph?** Written in C with Python bindings, igraph offers 10-100x better performance than NetworkX for graph operations - crucial when working with complex algorithms like Euler tour detection.
:::

### Installing igraph

```bash
# Install igraph for Python
pip install python-igraph

# For visualization support (optional)
pip install matplotlib numpy
```

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
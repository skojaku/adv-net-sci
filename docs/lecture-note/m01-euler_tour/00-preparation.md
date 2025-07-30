---
title: Preparation: Python and Graph Basics
---

## The Seven Bridges of Königsberg: A Problem That Changed Mathematics

In 1736, the residents of Königsberg faced a delightful puzzle. Their city was built around the Pregel River, with seven bridges connecting four landmasses. The question everyone wondered: **Could you take a walk that crosses each bridge exactly once and return to your starting point?**

::: {#fig-konigsberg}
![The seven bridges of Königsberg](https://upload.wikimedia.org/wikipedia/commons/5/5d/Konigsberg_bridges.png)

The original seven bridges of Königsberg. Each bridge must be crossed exactly once - is this possible?
:::

Leonhard Euler, one of history's greatest mathematicians, realized something profound: the specific layout of the bridges didn't matter. What mattered was the **abstract structure** - which landmasses connected to which others. By representing the problem as nodes (landmasses) connected by edges (bridges), Euler created the field of graph theory and proved that such a path was impossible.

::: {.column-margin}
This problem led to the concept of an **Eulerian path** - a path that visits every edge exactly once. We'll explore this thoroughly in our module.
:::

Today, this same mathematical framework powers Google's PageRank, helps epidemiologists track disease spread, enables GPS navigation, and guides drug discovery. **The art of representing real-world problems as graphs remains one of the most powerful tools in computational science.**

Before diving into the Euler Tour problem, let's master the foundational knowledge you'll need.

## Python Essentials for Graph Analysis

Just as Euler abstracted bridges into mathematical objects, we'll use Python's data structures to represent and manipulate graphs efficiently.

### Data Structures: The Building Blocks

For graph algorithms, you'll rely on three core Python data structures:

::: {layout-ncol=3}

**Lists** store sequences of nodes or edges:
```python
nodes = [1, 2, 3, 4]
edges = [(1, 2), (2, 3), (3, 4)]
```

**Dictionaries** create adjacency lists:
```python
graph = {
    1: [2, 4], 
    2: [1, 3],
    3: [2, 4],
    4: [3, 1]
}
```

**Sets** track visited nodes:
```python
visited = set()
visited.add(1)
```

:::

### Essential Libraries

::: {#fig-python-libraries}

```python
import igraph as ig       # Fast graph creation and analysis
import numpy as np        # Numerical operations and matrices  
import matplotlib.pyplot as plt  # Graph visualization
```

These three libraries form the trinity of graph analysis in Python.
:::

::: {.column-margin}
**igraph** offers superior performance compared to NetworkX, especially for large graphs. Written in C with Python bindings, it's the preferred choice for computational efficiency.
:::

## Graph Representations: Three Ways to See the Same Network

Just as the Königsberg bridges could be viewed as a physical map or an abstract graph, we can represent the same network in multiple ways. Each representation has its strengths - choose wisely based on your problem.

### Adjacency List: The Memory Champion

::: {#fig-adjacency-list}

Most memory-efficient for sparse graphs (few connections relative to possible connections):

```python
# Undirected graph: connections go both ways
graph = {
    'A': ['B', 'D'],
    'B': ['A', 'C'], 
    'C': ['B', 'D'],
    'D': ['A', 'C']
}

# Directed graph: one-way streets
directed_graph = {
    'A': ['B', 'D'],
    'B': ['C'],
    'C': ['D'], 
    'D': []
}

# Weighted graph: connections have costs
weighted_graph = {
    'A': [('B', 2), ('D', 1)],
    'B': [('A', 2), ('C', 3)],
    'C': [('B', 3), ('D', 2)],
    'D': [('A', 1), ('C', 2)]
}
```

For most real-world networks (social networks, web graphs, transportation), adjacency lists are the gold standard.
:::

### Adjacency Matrix: The Speed Demon

::: {#fig-adjacency-matrix}

Best for dense graphs and lightning-fast edge lookups:

```python
# For a 4-node graph (A=0, B=1, C=2, D=3)
adj_matrix = np.array([
    [0, 1, 0, 1],  # Node A connections
    [1, 0, 1, 0],  # Node B connections
    [0, 1, 0, 1],  # Node C connections
    [1, 0, 1, 0]   # Node D connections
])

# Weighted adjacency matrix (0 means no edge)
weighted_adj_matrix = np.array([
    [0, 2, 0, 1],  # Node A: edge to B (weight 2), D (weight 1)
    [2, 0, 3, 0],  # Node B: edge to A (weight 2), C (weight 3)  
    [0, 3, 0, 2],  # Node C: edge to B (weight 3), D (weight 2)
    [1, 0, 2, 0]   # Node D: edge to A (weight 1), C (weight 2)
])
```

Perfect for mathematical operations and algorithms that need to check "Is there an edge between nodes i and j?" frequently.
:::

::: {.column-margin}
**Quick check**: `adj_matrix[i][j] == 1` tells you instantly if nodes i and j are connected. Try doing that with an adjacency list!
:::

### Edge List: The Minimalist

::: {#fig-edge-list}

Simplest representation for basic operations and data storage:

```python
# List of tuples (source, target)
edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')]

# Weighted edge list: add weight as third element
weighted_edges = [('A', 'B', 2), ('B', 'C', 3), ('C', 'D', 2), ('D', 'A', 1)]
```

This is how most graph datasets are stored in files - one edge per line.
:::

## Practical Graph Construction with igraph

### igraph Basics: Performance Meets Simplicity

::: {#fig-igraph-basics}

```python
# Creating different types of graphs
g_undirected = ig.Graph()                    # Empty undirected graph
g_directed = ig.Graph(directed=True)         # Empty directed graph

# Creating from edge list (most common approach)
g = ig.Graph([(0, 1), (1, 2), (2, 3), (3, 0)])

# Adding vertices and edges dynamically
g = ig.Graph()
g.add_vertices(4)                            # Add vertices 0, 1, 2, 3
g.add_edges([(0, 1), (1, 2), (2, 3), (3, 0)])

# Creating with vertex names and attributes
g = ig.Graph(n=4, edges=[(0, 1), (1, 2)], 
             vertex_attrs={'name': ['A', 'B', 'C', 'D']},
             edge_attrs={'weight': [1.0, 2.0]})

# Basic graph properties
print(f"Vertices: {g.vcount()}, Edges: {g.ecount()}")
print(f"Degree of vertex 0: {g.degree(0)}")
print(f"Neighbors: {g.neighbors(0)}")
print(f"Is connected: {g.is_connected()}")
```

**Performance advantage**: igraph operations are 10-100x faster than NetworkX due to C implementation.
:::

### Converting Between Representations

::: {#fig-igraph-conversions}

```python
# igraph to adjacency list dictionary
adj_list = {v: g.neighbors(v) for v in range(g.vcount())}

# igraph to adjacency matrix (as numpy array)
adj_matrix = g.get_adjacency().data  # Returns as list of lists
import numpy as np
adj_matrix = np.array(g.get_adjacency().data)  # As numpy array

# From adjacency matrix to igraph
g = ig.Graph.Adjacency(adj_matrix.tolist())

# From edge list to igraph (multiple ways)
edges = [(0, 1), (1, 2), (2, 3)]
g = ig.Graph(edges)                    # Direct construction
g = ig.Graph(edges=edges)              # Explicit parameter

# Loading from files
g = ig.Graph.Read_Edgelist('graph.txt')
g = ig.Graph.Read_GraphML('graph.graphml')
g = ig.Graph.Read_GML('graph.gml')
```

**Fast conversions**: igraph handles format conversions efficiently with built-in methods.
:::

### Common Graph Construction Patterns

::: {#fig-igraph-patterns}

```python
# Classic graph structures for testing
complete_graph = ig.Graph.Full(5)            # K5: every vertex connected
cycle_graph = ig.Graph.Ring(6)               # C6: vertices in a circle
path_graph = ig.Graph.Path(10)               # P10: linear chain
star_graph = ig.Graph.Star(9)                # 1 center + 8 outer vertices
tree_graph = ig.Graph.Tree(15, 2)            # Binary tree with 15 vertices

# Grid and lattice structures
lattice_2d = ig.Graph.Lattice([4, 4])        # 4x4 grid
lattice_3d = ig.Graph.Lattice([3, 3, 3])     # 3D cube lattice

# Random graph models
erdos_renyi = ig.Graph.Erdos_Renyi(100, 0.1)      # Random edges
barabasi_albert = ig.Graph.Barabasi(100, 3)       # Preferential attachment
watts_strogatz = ig.Graph.Watts_Strogatz(1, 100, 4, 0.1)  # Small world

# Famous graphs from literature
zachary = ig.Graph.Famous('Zachary')          # Karate club network
petersen = ig.Graph.Famous('Petersen')        # Petersen graph
```

**Rich library**: igraph includes generators for most standard graph families and models.
:::

## Graph Traversal Fundamentals

Understanding graph traversal is essential for implementing Euler tour algorithms.

### Depth-First Search (DFS)

```python
def dfs_recursive(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(f"Visiting: {start}")
    
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)
    
    return visited

def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            print(f"Visiting: {node}")
            
            # Add neighbors to stack (reverse order for consistent traversal)
            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return visited
```

### Breadth-First Search (BFS)

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        node = queue.popleft()
        print(f"Visiting: {node}")
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return visited
```

### igraph Traversal: Built-in and Optimized

::: {#fig-igraph-traversal}

```python
# Depth-First Search: returns [vertices, parents]
vertices, parents = g.dfs(0)                 # DFS from vertex 0
vertices_only = g.dfs(0)[0]                  # Just the vertex order

# Breadth-First Search: returns [vertices, layers, parents]  
vertices, layers, parents = g.bfs(0)         # BFS from vertex 0
vertices_only = g.bfs(0)[0]                  # Just the vertex order

# Lazy iterators for large graphs (memory efficient)
dfs_iterator = g.dfsiter(0)                  # Lazy DFS traversal
bfs_iterator = g.bfsiter(0)                  # Lazy BFS traversal

# Path finding algorithms
shortest_path = g.get_shortest_path(0, 3)    # Single shortest path  
all_shortest = g.get_shortest_paths(0, 3)    # All shortest paths
distances = g.distances(0, 3)                # Distance matrix

# Random walks for sampling
random_path = g.random_walk(0, steps=10)     # 10-step random walk
```

**Optimized performance**: igraph's C implementation makes traversals extremely fast.
:::

## Performance Considerations

### Time and Space Complexity

| Representation | Space | Add Edge | Remove Edge | Check Edge | Neighbors |
|---------------|-------|----------|-------------|------------|-----------|
| Adjacency List | O(V + E) | O(1) | O(degree) | O(degree) | O(degree) |
| Adjacency Matrix | O(V²) | O(1) | O(1) | O(1) | O(V) |
| Edge List | O(E) | O(1) | O(E) | O(E) | O(E) |

### Choosing the Right Representation

```python
# For sparse graphs (few edges): Use adjacency list
if num_edges < num_vertices**2 / 4:
    representation = "adjacency_list"

# For dense graphs (many edges): Use adjacency matrix  
elif num_edges > num_vertices**2 / 2:
    representation = "adjacency_matrix"

# For simple operations on small graphs: Use edge list
else:
    representation = "edge_list"
```

### Memory-Efficient Patterns

```python
# Use generators for large graphs
def get_neighbors(graph, node):
    """Generator for neighbors to save memory"""
    for neighbor in graph.get(node, []):
        yield neighbor

# Use defaultdict to avoid key errors
from collections import defaultdict

graph = defaultdict(list)
graph['A'].append('B')  # No KeyError if 'A' doesn't exist

# For very large graphs, consider using numpy arrays
import numpy as np
large_adj_matrix = np.zeros((10000, 10000), dtype=np.int8)  # Use smallest dtype
```

### Quick Reference

::: {#fig-quick-reference}

```python
# Essential imports for graph processing
import igraph as ig
import numpy as np
from collections import defaultdict, deque
import matplotlib.pyplot as plt

# Common graph properties
def analyze_graph(g):
    print(f"Vertices: {g.vcount()}")
    print(f"Edges: {g.ecount()}")
    print(f"Density: {g.density():.3f}")
    print(f"Connected: {g.is_connected()}")
    print(f"Average degree: {np.mean(g.degree()):.2f}")
    print(f"Diameter: {g.diameter()}")
```

Your toolkit for efficient graph analysis is now complete.
:::

## From Bridges to Algorithms: What's Next?

Just as Euler transformed a walking puzzle into mathematical theory, you now have the tools to represent and analyze any network computationally. The Seven Bridges of Königsberg couldn't be solved with a simple walk, but **Euler's insight - that structure matters more than physical layout - revolutionized how we think about connectivity**.

::: {.column-margin}
**Historical note**: The original bridges were destroyed during World War II, but two were rebuilt. Today, Königsberg (now Kaliningrad) has an Eulerian path through its bridges - you can complete the tour that eluded 18th-century residents!
:::

**What you've mastered:**
- **Data structures** that capture network relationships efficiently
- **Multiple representations** (adjacency lists, matrices, edge lists) for different algorithmic needs  
- **igraph** for high-performance graph analysis
- **Traversal algorithms** (DFS, BFS) that explore network structure systematically

**What's coming next:** You'll apply these tools to solve Euler tour problems - finding paths that visit every edge exactly once. This seemingly simple puzzle connects to circuit design, DNA sequencing, mail delivery optimization, and even solving mazes. 

The mathematical elegance that Euler discovered in 1736 still powers algorithms solving 21st-century problems. **Your journey from bridges to bits begins now.**
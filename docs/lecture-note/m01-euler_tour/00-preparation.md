---
title: Preparation - From Visual to Computational
filters:
  - marimo-team/marimo
  - tikz
tikz:
  cache: false
  save-tex: true  # Enable saving intermediate .tex files
  tex-dir: tikz-tex  # Optional: Specify directory to save .tex files
---

## From Picture to Code

Consider this network with 5 nodes and 6 edges:

```{.tikz}
%%| caption: A graph of five nodes

\begin{tikzpicture}[scale=1.8, font=\Large]
  % Define vertices
  \node[circle, draw, fill=white, minimum size=1.2cm] (0) at (0,2) {\textbf{0}};
  \node[circle, draw, fill=white, minimum size=1.2cm] (1) at (-1.5,0.5) {\textbf{1}};
  \node[circle, draw, fill=white, minimum size=1.2cm] (2) at (1.5,0.5) {\textbf{2}};
  \node[circle, draw, fill=white, minimum size=1.2cm] (3) at (-1,-1.5) {\textbf{3}};
  \node[circle, draw, fill=white, minimum size=1.2cm] (4) at (1,-1.5) {\textbf{4}};

  % Draw edges
  \draw[thick, black] (0) -- (1);
  \draw[thick, black] (0) -- (2);
  \draw[thick, black] (1) -- (2);
  \draw[thick, black] (1) -- (3);
  \draw[thick, black] (2) -- (4);
  \draw[thick, black] (3) -- (4);

\end{tikzpicture}
```

How do we represent this graph in a format that a computer can understand and manipulate? Let's explore three fundamental approaches.

## 1. Edge Table

The edge table is the most intuitive representation because it directly mirrors how we naturally describe a network: as a list of connections. Each row captures one relationship between two nodes, making it conceptually straightforward and human-readable. This representation excels in storage efficiency for sparse networks where most nodes are not connected to each other, which describes most real-world networks. It also makes adding or removing connections trivial since you simply add or delete rows.

However, the edge table becomes cumbersome when you need to answer questions about a specific node's relationships. Finding all neighbors of a particular node requires scanning the entire list, making operations like "show me all friends of person X" computationally expensive for large networks.

```python
# Each row represents one edge (connection between two nodes)
edges = [
    (0, 1),  # Node 0 connects to Node 1
    (0, 2),  # Node 0 connects to Node 2  
    (1, 2),  # Node 1 connects to Node 2
    (1, 3),  # Node 1 connects to Node 3
    (2, 4),  # Node 2 connects to Node 4
    (3, 4)   # Node 3 connects to Node 4
]

print(f"Total edges: {len(edges)}")  # 6
```

## 2. Adjacency List

The adjacency list reorganizes the same information by grouping connections around each node, creating a node-centric view of the network. This representation mirrors how we might naturally think about social relationships: each person maintains their own contact list. The key benefit lies in its efficiency for node-focused operations since finding all neighbors of any node takes constant time rather than requiring a full search.

The adjacency list also maintains the storage efficiency of edge tables for sparse networks while dramatically speeding up common graph algorithms that need to explore a node's immediate neighborhood. However, determining whether two specific nodes are connected requires scanning through one node's neighbor list, making edge-existence queries slower than in matrix representations.

```python
# Define adjacency list directly as a dictionary
neighbors = {
    0: [1, 2],     # Node 0 connects to nodes 1 and 2
    1: [0, 2, 3],  # Node 1 connects to nodes 0, 2, and 3
    2: [0, 1, 4],  # Node 2 connects to nodes 0, 1, and 4
    3: [1, 4],     # Node 3 connects to nodes 1 and 4
    4: [2, 3]      # Node 4 connects to nodes 2 and 3
}

print("Adjacency List:")
for node, adj in neighbors.items():
    print(f"Node {node}: {adj}")

# Output:
# Node 0: [1, 2]
# Node 1: [0, 2, 3] 
# Node 2: [0, 1, 4]
# Node 3: [1, 4]
# Node 4: [2, 3]
```

## 3. Adjacency Matrix

The adjacency matrix transforms the network into a mathematical grid where every possible relationship is explicitly represented, either as present (1) or absent (0). This representation embodies a complete, symmetric view of all potential connections in the network. Its greatest strength lies in instant edge lookups: determining whether any two nodes are connected requires only a single array access, making it exceptionally fast for connectivity queries.

The matrix format also enables powerful mathematical operations, allowing entire classes of network algorithms to leverage linear algebra for dramatic speed improvements. However, this completeness comes at a significant cost in memory usage, especially for sparse networks where most entries remain zero. A network with a million nodes requires a trillion matrix entries regardless of how few actual connections exist, making this representation impractical for large, sparse real-world networks.

```python
import numpy as np

# Initialize 5x5 matrix with zeros
matrix = np.zeros((5, 5), dtype=int)

# Fill in connections from edge table
for node1, node2 in edges:
    matrix[node1][node2] = 1  # Mark connection
    matrix[node2][node1] = 1  # Since graph is undirected

print("Adjacency Matrix:")
print(matrix)

# Output:
# [[0 1 1 0 0]
#  [1 0 1 1 0]
#  [1 1 0 0 1]
#  [0 1 0 0 1]
#  [0 0 1 1 0]]
```

You now understand how to represent networks computationally!
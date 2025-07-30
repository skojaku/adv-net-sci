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

The edge table directly lists connections as pairs. It's memory-efficient for sparse networks and makes adding/removing edges simple. However, finding a node's neighbors requires scanning the entire list.

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

The adjacency list stores each node's neighbors in a dictionary. It allows instant neighbor lookup and remains memory-efficient for sparse networks. However, checking if two specific nodes are connected requires scanning a neighbor list.

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

The adjacency matrix uses a grid where entry (i,j) = 1 if nodes are connected. It enables instant edge lookups and supports fast linear algebra operations. However, it uses excessive memory for sparse networks since it stores every possible connection.

```python
import numpy as np

# Define adjacency matrix directly
matrix = np.array([
    [0, 1, 1, 0, 0],  # Node 0 connects to nodes 1, 2
    [1, 0, 1, 1, 0],  # Node 1 connects to nodes 0, 2, 3
    [1, 1, 0, 0, 1],  # Node 2 connects to nodes 0, 1, 4
    [0, 1, 0, 0, 1],  # Node 3 connects to nodes 1, 4
    [0, 0, 1, 1, 0]   # Node 4 connects to nodes 2, 3
])

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
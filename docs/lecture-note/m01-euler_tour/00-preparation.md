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

The most direct translation: list every connection as a pair of nodes.

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

For each node, store a list of its neighbors.

```python
# Build adjacency list from edge table
neighbors = {}
for i in range(5):  # Initialize empty lists for nodes 0-4
    neighbors[i] = []

# Add each edge to both nodes' neighbor lists
for node1, node2 in edges:
    neighbors[node1].append(node2)
    neighbors[node2].append(node1)

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

Create a 5×5 grid where entry (i,j) = 1 if nodes i and j are connected.

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
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

### Edge Table

The edge table directly lists connections as pairs.

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

```

### Adjacency List

The adjacency list stores each node's neighbors in a dictionary.

```python
# Define adjacency list directly as a dictionary
neighbors = {
    0: [1, 2],     # Node 0 connects to nodes 1 and 2
    1: [0, 2, 3],  # Node 1 connects to nodes 0, 2, and 3
    2: [0, 1, 4],  # Node 2 connects to nodes 0, 1, and 4
    3: [1, 4],     # Node 3 connects to nodes 1 and 4
    4: [2, 3]      # Node 4 connects to nodes 2 and 3
}
```

### Adjacency Matrix

The adjacency matrix uses a grid where entry (i,j) = 1 if nodes are connected.

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
```

## Counting Node Degrees

The degree of a node is the number of edges connected to it. Here's how to compute degrees using each representation:

### From Edge Table

Count how many times each node appears in the edge list.

```python
# Count degrees from edge table
degrees = {}
for i in range(5):
    degrees[i] = 0

for node1, node2 in edges:
    degrees[node1] += 1
    degrees[node2] += 1

print("Degrees:", [degrees[i] for i in range(5)])  # [2, 3, 3, 2, 2]
```

### From Adjacency List

Count the length of each node's neighbor list.

```python
# Count degrees from adjacency list
degrees = [len(neighbors[i]) for i in range(5)]
print("Degrees:", degrees)  # [2, 3, 3, 2, 2]
```

### From Adjacency Matrix

Sum each row (or column) of the matrix.

```python
# Count degrees from adjacency matrix
degrees = matrix.sum(axis=1)  # Sum rows
print("Degrees:", degrees)  # [2 3 3 2 2]
```

You now understand how to represent networks computationally!
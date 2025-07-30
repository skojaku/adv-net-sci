---
title: Preparation - Python and Graph Basics
filters:
  - marimo-team/marimo
  - tikz
tikz:
  cache: false
  save-tex: true  # Enable saving intermediate .tex files
  tex-dir: tikz-tex  # Optional: Specify directory to save .tex files
---

## Required Libraries

```python
import igraph as ig
import numpy as np
```

**igraph**: High-performance C library with Python interface - essential for Euler tour algorithms.

## Basic Graph Creation

```{.tikz}
%%| caption: Triangle Graph - Our working example with vertices 0, 1, 2

\begin{tikzpicture}[scale=1.5]
  % Define vertices
  \node[circle, draw, fill=lightblue, minimum size=1cm] (0) at (0,1.5) {0};
  \node[circle, draw, fill=lightgreen, minimum size=1cm] (1) at (-1,0) {1};
  \node[circle, draw, fill=lightcoral, minimum size=1cm] (2) at (1,0) {2};
  
  % Draw edges
  \draw[thick, blue] (0) -- (1);
  \draw[thick, blue] (1) -- (2);
  \draw[thick, blue] (2) -- (0);
  
  % Add degree labels
  \node[above] at (0,2) {degree: 2};
  \node[below left] at (-1,-0.5) {degree: 2};
  \node[below right] at (1,-0.5) {degree: 2};
\end{tikzpicture}
```
```python
# Create triangle graph
g = ig.Graph([(0, 1), (1, 2), (2, 0)])

# Basic properties
print(f"Vertices: {g.vcount()}")
print(f"Edges: {g.ecount()}")
print(f"Degrees: {g.degree()}")
```

## Euler Tour Check

```python
# Check if Euler tour exists
degrees = g.degree()
odd_count = sum(1 for d in degrees if d % 2 == 1)

if odd_count == 0:
    print("✓ Euler cycle exists")
elif odd_count == 2:
    print("✓ Euler path exists")
else:
    print("✗ No Euler tour")
```

## Essential Operations

```python
# Get neighbors
neighbors = g.neighbors(0)

# Copy graph
g_copy = g.copy()

# Data structures for algorithms
path = []
visited = set()
```

## Quick Test

```python
# Test the triangle graph
g = ig.Graph([(0, 1), (1, 2), (2, 0)])
degrees = g.degree()
odd_count = sum(1 for d in degrees if d % 2 == 1)
print(f"Degrees: {degrees}, Odd vertices: {odd_count}")
# Output: Degrees: [2, 2, 2], Odd vertices: 0
# → Has Euler cycle!
```

You're now ready to implement Euler tour algorithms!
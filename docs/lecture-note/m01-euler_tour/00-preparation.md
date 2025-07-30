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
%%| caption: 5-node Graph - Mix of even and odd degrees for Euler tour analysis

\begin{tikzpicture}[scale=1.8, font=\Large]
  % Define vertices
  \node[circle, draw, fill=blue!20, minimum size=1.2cm] (0) at (0,2) {\textbf{0}};
  \node[circle, draw, fill=green!20, minimum size=1.2cm] (1) at (-1.5,0.5) {\textbf{1}};
  \node[circle, draw, fill=red!20, minimum size=1.2cm] (2) at (1.5,0.5) {\textbf{2}};
  \node[circle, draw, fill=orange!20, minimum size=1.2cm] (3) at (-1,-1.5) {\textbf{3}};
  \node[circle, draw, fill=purple!20, minimum size=1.2cm] (4) at (1,-1.5) {\textbf{4}};

  % Draw edges
  \draw[thick, blue] (0) -- (1);
  \draw[thick, blue] (0) -- (2);
  \draw[thick, blue] (1) -- (2);
  \draw[thick, blue] (1) -- (3);
  \draw[thick, blue] (2) -- (4);
  \draw[thick, blue] (3) -- (4);

  % Add degree labels
  \node[above, font=\Large] at (0,2.7) {\textbf{degree: 2}};
  \node[left, font=\Large] at (-2.2,0.5) {\textbf{degree: 3}};
  \node[right, font=\Large] at (2.2,0.5) {\textbf{degree: 3}};
  \node[below left, font=\Large] at (-1.5,-2.2) {\textbf{degree: 2}};
  \node[below right, font=\Large] at (1.5,-2.2) {\textbf{degree: 2}};
\end{tikzpicture}
```

```python
# Create 5-node graph
g = ig.Graph([(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4)])

# Basic properties
print(f"Vertices: {g.vcount()}")  # 5
print(f"Edges: {g.ecount()}")    # 6
print(f"Degrees: {g.degree()}")  # [2, 3, 3, 2, 2]
```

## Euler Tour Check

```python
# Check if Euler tour exists
degrees = g.degree()  # [2, 3, 3, 2, 2]
odd_count = sum(1 for d in degrees if d % 2 == 1)  # Count odd degrees

print(f"Degrees: {degrees}")
print(f"Odd degree vertices: {odd_count}")

if odd_count == 0:
    print("✓ Euler cycle exists")
elif odd_count == 2:
    print("✓ Euler path exists")
else:
    print("✗ No Euler tour")
# Output: Euler path exists (exactly 2 odd vertices: 1 and 2)
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
# Test the 5-node graph
g = ig.Graph([(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4)])
degrees = g.degree()
odd_count = sum(1 for d in degrees if d % 2 == 1)
print(f"Degrees: {degrees}, Odd vertices: {odd_count}")
# Output: Degrees: [2, 3, 3, 2, 2], Odd vertices: 2
# → Has Euler path! (Must start at vertex 1 or 2, end at the other)
```

You're now ready to implement Euler tour algorithms!
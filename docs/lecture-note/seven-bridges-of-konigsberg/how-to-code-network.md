---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .Rmd
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.3
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---


# How to describe a network using mathematics and code

So far we worked out the network of bridges of Konigsberg by illustrating the network with points and lines.
From now, we will work with the mathematical description of the network.

An atomic element of a network is a node, i.e., a network is a collection of edges which are pairs of nodes.
We *label* a unique integer as an identifier for each node. For instance, the bridges of Konigsberg has 4 nodes, and we assign the number 0 to 3 to the nodes. An edge can be represented by a pair of nodes. For instance, the edge between node 0 and node 1 can be represented by the pair `(0, 1)`.


:::{figure-md} numbered-koningsberg-graph

<img src= "./figs/labeled-koningsberg.jpg" width="30%">

Labeled Knigsberg graph

:::

:::{note}
:name: node-labeling
We label nodes starting from 0 with consecutive numbers, which is convenient for Python. However, this is *not the only way* to label nodes.
:::

The Konigsberg graph can be represented by a list of edges.

```{code-cell} python
edges = [(0,1), (0, 1), (0, 3), (1, 2), (1, 2), (1, 3), (2, 3)]
```

This list is a complete description of the network. However, it is inconvenient to work with mathematically.
Another, more convenient format is the *adjacency matrix*.
In this form, one regard the node index as a coordinate in the matrix. For instance, edge $(1,3)$ is represented by the entry in the second row and fourth column. The entry of the matrix represents the number of edges between two nodes. Thus, the zeros in the matrix represent the absence of edges.

```{code-cell} ipython3
A = [[0, 2, 0, 1],
     [2, 0, 2, 1],
     [0, 2, 0, 1],
     [1, 1, 1, 0]]
```

or equivalently, using for loops:
```{code-cell} ipython3
import numpy as np

A = np.zeros((4, 4))
for i, j in edges:
    A[i][j] += 1
```
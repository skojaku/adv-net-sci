---
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

<a target="_blank" href="https://colab.research.google.com/github/skojaku/adv-net-sci/blob/main/docs/lecture-note/m01-euler_tour/how-to-code-network.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

# Compute with networks

So far we worked out the network of bridges of Konigsberg by illustrating the network with points and lines.
From now, we will work with a representation of the network that can be easily computed with code.

## Network representation

An atomic element of a network is a node, i.e., a network is a collection of edges which are pairs of nodes.
We *label* a unique integer as an identifier for each node. For instance, the bridges of Konigsberg has 4 nodes, and we assign the number 0 to 3 to the nodes. An edge can be represented by a pair of nodes. For instance, the edge between node 0 and node 1 can be represented by the pair `(0, 1)`.


```{figure-md} numbered-koningsberg-graph

![file](https://github.com/skojaku/adv-net-sci/blob/gh-pages/_images/labeled-koningsberg.jpg?raw=true)

Labeled Knigsberg graph

```

```{note}
:name: node-labeling
We label nodes starting from 0 with consecutive numbers, which is convenient for Python. However, this is *not the only way* to label nodes.
```

The Konigsberg graph can be represented by a list of edges.

```{code-cell} python
edges = [(0,1), (0, 1), (0, 3), (1, 2), (1, 2), (1, 3), (2, 3)]
```

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
    A[j][i] += 1
```

:::{note}
In the Konigsberg graph, the edges are *undirected*, meaning edge (i,j) is the same as edge (j,i), which is why we increment both entries $(i,j)$ and $(j,i)$ in the for loop. If the edges are *directed*, we treat (i,j) and (j,i) as two different edges, and increment only (i,j).
:::

## Edge counting

Let us showcase the convenience of the adjacency matrix by counting the number of edges in the network.

The total number of edges in the network is the sum of the entities in the
```{code-cell} ipython3
np.sum(A) / 2
```
We divide by 2 because an edge corresponds to two entries in the matrix. Now, let us consider

It is also easy to compute the number of edges pertained to individual nodes by taking the row or column sum of the matrix.
```{code-cell} ipython3
np.sum(A, axis = 1)
```
The result is an array of length 4, where the i-th entry is the number of edges connected to node i.

:::{important}
The number of edges connected to a node is called the ***degree*** of the node.
:::
:::{tip}
The `np.sum(A, axis = 1)` is the column sum of `A`. Alternatively, `np.sum(A, axis = 0)` is the row sum of `A`.
Check out the numpy [documentation](https://numpy.org/doc/stable/reference/generated/numpy.sum.html) for more details.
:::
:::{tip}
If the adjacency matrix is `scipy` CSR format (or CSC format), you can instead use `A_csr.sum(axis=1)`, `A_csr.sum(axis=0)`, and `A_csr.sum()`.
Check out the [scipy documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html#scipy.sparse.csr_matrix) for more details.
:::

We can check the number of nodes with odd degree by taking the modulus of the degree by 2.
```{code-cell} ipython3
deg = np.sum(A, axis = 1)
is_odd = deg % 2 == 1
is_odd
```
```{code-cell} ipython3
if np.sum(is_odd) == 2 or np.sum(is_odd) == 0:
    print("The graph has a Euler path.")
else:
    print("The graph does not have a Euler path.")
```

```{admonition} Exercise
:class: tip

1. Create a network of landmasses and bridges of Binghamton, NY.
2. Find an Euler path that crosses all the bridges of Binghamton, NY exactly once.

![](../../lecture-note/figs/binghamton-map.jpg)

```
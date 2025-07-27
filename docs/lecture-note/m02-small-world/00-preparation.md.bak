# Preparation: Graph Theory Fundamentals

## Overview

Before diving into small-world networks, let's review the fundamental concepts from graph theory that will be essential for understanding distance, paths, and connectivity in networks.

## Historical Foundation: The Seven Bridges of Königsberg

Back in 18th century, there was a city called *Königsberg* situated on the Pregel River in a historical region of Germany. The city had two large islands connected to each other and the mainland by seven bridges. The citizens of Königsberg pondered a puzzle during their Sunday walks:

::: {.callout-note title="Problem"}
How could one walk through the city and cross each bridge exactly once?
:::

![alt text](https://99percentinvisible.org/wp-content/uploads/2022/02/bridges-with-water-600x418.png){#fig-seven-bridges fig-alt="The seven bridges of Königsberg"}

: The seven bridges of Königsberg {#fig-seven-bridges}

Leonard Euler worked out the solution to this puzzle in 1736. He first simplified the city into *a network of landmasses connected by bridges*, by noting that the landareas, the positions of the islands and the bridges are nothing to do with the puzzle, and that the only thing that matters is the connections between the landmasses.

![](https://lh3.googleusercontent.com/-CYxppcJBwe4/W2ndkci9bVI/AAAAAAABX-U/K6SNM8gAhg0oNsnWNgQbH3uKNd5Ba10wwCHMYCw/euler-graph-bridges2?imgmax=1600){#fig-euler-graph fig-alt="Euler's graph of the bridges of Knigsberg"}

: Euler's graph of the bridges of Knigsberg {#fig-euler-graph}

## Euler's Solution

Euler consider two cases:
- a node has an even number of edges, or
- a node has an odd number of edges.

When a node has an even number $2k$ of edges, one can enter and leave the node $k$ times by crossing different edges.

When a node has an odd number $2k+1$ of edges, one can enter and leave the node $k$ times by crossing different edges but leave one last edge to cross. The only way to cross this last edge is that one starts or ends at the node.

Based up on the above reasoning, Euler leads to the following necessary (and later shown as sufficient) conditions:

::: {.callout-note title="Euler's path"}

There exists a walk that crosses all edges exactly once if and only if all nodes have even number of edges, or exactly two nodes have an odd number of edges.
:::

![alt text](https://lh3.googleusercontent.com/-CYxppcJBwe4/W2ndkci9bVI/AAAAAAABX-U/K6SNM8gAhg0oNsnWNgQbH3uKNd5Ba10wwCHMYCw/euler-graph-bridges2?imgmax=1600)

Back to the Konigsberg bridge problem, every node has an odd number of edges, meaning that there is no way to cross all edges exactly once. What a sad story for the citizens of Konigsberg. But the problem was solved during World War II, where Koingberg was bombarded by Soviet Union, losing two of the seven bridges 🫠.

![](../figs/seven-bridge-bombared.png){#fig-markdown-fig fig-alt="Two bridges were bombed by Soviet Union, which allows the Euler path to exist."}

: Two bridges were bombed by Soviet Union, which allows the Euler path to exist. {#fig-markdown-fig}

## Network Representation

An atomic element of a network is a node, i.e., a network is a collection of edges which are pairs of nodes. We *label* a unique integer as an identifier for each node. For instance, the bridges of Konigsberg has 4 nodes, and we assign the number 0 to 3 to the nodes. An edge can be represented by a pair of nodes. For instance, the edge between node 0 and node 1 can be represented by the pair `(0, 1)`.

::: {.callout-note}
We label nodes starting from 0 with consecutive numbers, which is convenient for Python. However, this is *not the only way* to label nodes.
:::

The Konigsberg graph can be represented by a list of edges:

```python
edges = [(0,1), (0, 1), (0, 3), (1, 2), (1, 2), (1, 3), (2, 3)]
```

Another, more convenient format is the *adjacency matrix*. In this form, one regard the node index as a coordinate in the matrix. For instance, edge $(1,3)$ is represented by the entry in the second row and fourth column. The entry of the matrix represents the number of edges between two nodes. Thus, the zeros in the matrix represent the absence of edges.

```python
A = [[0, 2, 0, 1],
     [2, 0, 2, 1],
     [0, 2, 0, 1],
     [1, 1, 1, 0]]
```

or equivalently, using for loops:
```python
import numpy as np

A = np.zeros((4, 4))
for i, j in edges:
    A[i][j] += 1
    A[j][i] += 1
```

::: {.callout-note}
In the Konigsberg graph, the edges are *undirected*, meaning edge (i,j) is the same as edge (j,i), which is why we increment both entries $(i,j)$ and $(j,i)$ in the for loop. If the edges are *directed*, we treat (i,j) and (j,i) as two different edges, and increment only (i,j).
:::

## Edge Counting and Degree

Let us showcase the convenience of the adjacency matrix by counting the number of edges in the network.

The total number of edges in the network is the sum of the entities in the matrix divided by 2:
```python
np.sum(A) / 2
```
We divide by 2 because an edge corresponds to two entries in the matrix.

It is also easy to compute the number of edges pertained to individual nodes by taking the row or column sum of the matrix:
```python
np.sum(A, axis = 1)
```
The result is an array of length 4, where the i-th entry is the number of edges connected to node i.

::: {.callout-important}
The number of edges connected to a node is called the ***degree*** of the node.
:::

::: {.callout-tip}
The `np.sum(A, axis = 1)` is the column sum of `A`. Alternatively, `np.sum(A, axis = 0)` is the row sum of `A`.
Check out the numpy [documentation](https://numpy.org/doc/stable/reference/generated/numpy.sum.html) for more details.
:::

We can check the number of nodes with odd degree by taking the modulus of the degree by 2:
```python
deg = np.sum(A, axis = 1)
is_odd = deg % 2 == 1
is_odd
```
```python
if np.sum(is_odd) == 2 or np.sum(is_odd) == 0:
    print("The graph has a Euler path.")
else:
    print("The graph does not have a Euler path.")
```

## Graph Algorithms Fundamentals

Before we explore small-world networks, it's important to understand several key algorithmic concepts:

### Path Finding
- **Path**: A sequence of nodes where each adjacent pair is connected by an edge
- **Shortest Path**: The path between two nodes with the minimum number of edges (unweighted) or minimum total weight (weighted)
- **Dijkstra's Algorithm**: Finds shortest paths from a source node to all other nodes in weighted graphs
- **Breadth-First Search (BFS)**: Finds shortest paths in unweighted graphs

### Graph Traversal
- **Depth-First Search (DFS)**: Explores as far as possible along each branch before backtracking
- **Breadth-First Search (BFS)**: Explores neighbors at the current depth before moving to nodes at the next depth

### Connectivity
- **Connected Component**: A maximal set of nodes such that every pair is connected by a path
- **Strongly Connected Component**: In directed graphs, a maximal set where every node can reach every other node
- **Weakly Connected Component**: In directed graphs, connected when edge directions are ignored

These concepts will be crucial for understanding how small-world networks maintain short paths between nodes while preserving local clustering.

## Keywords
- **Network**, **Graph**
- **Node**, **Vertex** 
- **Edge**, **Link**
- **Degree**
- **Adjacency Matrix**
- **Path**, **Walk**
- **Euler Path**
- **Connected Component**
- **Graph Algorithms**
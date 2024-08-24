---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

<a target="_blank" href="https://colab.research.google.com/github/skojaku/adv-net-sci/blob/main/notebooks/exercise-m06-centrality.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

# Computing centrality with Python

## Network of university students

Let's compute the centrality of the network using Python igraph.

```{code-cell} ipython
import igraph
names  = ['Sarah', 'Mike', 'Emma', 'Alex', 'Olivia', 'James', 'Sophia', 'Ethan', 'Ava', 'Noah', 'Lily', 'Lucas', 'Henry']
edge_list = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (3, 5), (3, 6), (4, 5), (6, 7), (6, 8), (6, 9), (7, 8), (7, 9), (8, 9), (9, 10), (9, 11), (9, 12)]
g = igraph.Graph()
g.add_vertices(13)
g.vs["name"] = names
g.add_edges(edge_list)
igraph.plot(g, vertex_label=g.vs["name"])
```

`igraph` offers a wide range of centrality measures as methods of the `igraph.Graph` class.

- **Degree centrality**: `igraph.Graph.degree()`
- **Closeness centrality**: `igraph.Graph.closeness()`
- **Betweenness centrality**: `igraph.Graph.betweenness()`
- **Harmonic centrality**: `igraph.Graph.harmonic_centrality()`
- **Eccentricity**: `igraph.Graph.eccentricity()`
- **Eigenvector centrality**: `igraph.Graph.eigenvector_centrality()`
- **PageRank centrality**: `igraph.Graph.personalized_pagerank()`

For example, the closeness centrality is computed by
```{code-cell} ipython
g.closeness()
```

### Computing Katz centrality

Let's compute the Katz centrality without using igraph.
Let us first define the adjacency matrix of the graph

```{code-cell} ipython
A = g.get_adjacency()
A
```
which is the scipy CSR sparse matrix. The Katz centrality is given by

$$

\mat{c} = \beta \mathbb{1} + \alpha \mat{A} \mat{c}+

$$

So, how do we solve this? We can use a linear solver but here we will use a simple method:

1. Initialize $\mat{c}$ with a random vector.
2. Compute the right hand side of the equation and update $\mat{c}$.
3. Repeat the process until $\mat{c}$ converges.

Let's implement this.
```{code-cell} ipython

alpha, beta = 0.1, 0.05 # Hyperparameters
n_nodes = g.vcount() # number of nodes
c = np.random.rand(n_nodes, 1) # column random vector

for _ in range(100):
    c_next = beta * np.ones((n_nodes, 1)) + alpha * A * c
    if np.linalg.norm(c_next - c) < 1e-6:
        break
    c = c_next
print(c)
```

Change the hyperparameter and see how the result changes 😉
If the centrality diverges, think about why it diverges.

*Hint*: Katz centrality can be analytically computed by

$$

\mat{c} = \beta \left(\mathbb{I} -  \alpha \mat{A} \right)^{-1} \mathbb{1}

$$

### Exercise (Optional)

Compute the PageRank centrality of this graph

```{code-cell} ipython

```


## Network of ancient Roman roads

### Load the data & construct the network

```{code-cell} ipython
import pandas as pd

root = "https://raw.github.com/skojaku/adv-net-sci/main/data/roman-roads"
node_table = pd.read_csv(f"{root}/node_table.csv")
edge_table = pd.read_csv(f"{root}/edge_table.csv")
```

The node table:
```{code-cell} ipython
node_table
```

The edge table:
```{code-cell} ipython
edge_table
```

Let's construct a network from the node and edge tables.
```{code-cell} ipython
import igraph

g = igraph.Graph() # create an empty graph
g.add_vertices(node_table["node_id"].values) # add nodes
g.add_edges(list(zip(edge_table["src"].values, edge_table["trg"].values))) # add edges
```

which looks like this:
```{code-cell} ipython
coord = list(zip(node_table["long"].values, node_table["lat"].values))
igraph.plot(g, layout = coord)
```

### Exercise 🏛️

1. Compute the following centrality measures:
    - Degree centrality 🔢
    - Eigenvector centrality
    - PageRank centrality
    - Katz centrality
    - Betweenness centrality
    - Closeness centrality
2. Plot the centrality measures on the map and see in which centrality Rome is the most important node. 🗺️🏛️


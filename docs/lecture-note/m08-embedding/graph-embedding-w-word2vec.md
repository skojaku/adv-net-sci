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

# Graph embedding with word2vec

How can we apply word2vec to graph data? There is a critical challenge: word2vec takes sequence of words as input, while graph data are discrete and unordered. A solution to fill this gap is *random walk*, which transforms graph data into a sequence of nodes. Once we have a sequence of nodes, we can treat it as a sequence of words and apply word2vec.


## DeepWalk

DeepWalk is one of the pioneering works to apply word2vec to graph data {footcite}`perozzi2014deepwalk`. It views the nodes as words and the nodes random walks on the graph as sentences, and applies word2vec to learn the node embeddings.

More specifically, the method contains the following steps:

1. Sample multiple random walks from the graph.
2. Treat the random walks as sentences and apply skip-gram with negative sampling to learn the node embeddings.

## Exercise 01: Implement DeepWalk

Let's implement DeepWalk step by step. First, we need a function to sample random walks from a given network.

```{code-cell} ipython3
import numpy as np

def random_walk(net, start_node, walk_length):
    """
    Sample a random walk starting from start_node.

    Parameters
    ----------
    net : scipy.sparse.csr_matrix
        Adjacency matrix of the network.
    start_node : int
        The node to start the random walk from.
    walk_length : int
        The length of the random walk.

    Returns
    -------
    walk : list
        A list containing the nodes in the random walk, starting from start_node.
    """
    # TODO: Implement the random walk sampling here
    pass
```

Next, let us generate the training data for the word2vec model by generating multiple random walks starting from each node in the network. We consider Les Miserables network as an example.

```{code-cell} ipython3
import pandas as pd
from scipy import sparse


data_url = "https://raw.githubusercontent.com/skojaku/adv-net-sci/refs/heads/main/docs/lecture-note/assets/data/lesmiserable/"
node_table = pd.read_csv(data_url + "node_table.csv")
edge_table = pd.read_csv(data_url + "edge_table.csv")

rows, cols = edge_table["src"].values, edge_table["trg"].values
weight = edge_table["weight"].values
nrows, ncols = node_table.shape[0], node_table.shape[0]
A = sparse.csr_matrix(
    (weight, (rows, cols)),
    shape=(nrows, ncols),
)
A = A + A.T
```

```{code-cell} ipython3
n_walkers_per_node = 10
walk_length = 50
walks = []
for i in range(nrows):
    walks.append(random_walk(A, i, walk_length))
```

Then, we feed the random walks to the word2vec model.

```{code-cell} ipython3
from gensim.models import Word2Vec

model = Word2Vec(walks, vector_size=128, window=5, min_count=1, sg=0, hs = 1)
```

Let's visualize the node embeddings using UMAP.

```{code-cell} ipython3
:tags: [hide-input]
import umap
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource, HoverTool


reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=5, metric="cosine")
xy = reducer.fit_transform(model.wv.vectors)

output_notebook()

# Calculate the degree of each node
degrees = A.sum(axis=1).A1

source = ColumnDataSource(data=dict(
    x=xy[:, 0],
    y=xy[:, 1],
    name=node_names,
    size=np.sqrt(degrees / np.max(degrees)) * 30

))

p = figure(title="Node Embeddings from Word2Vec", x_axis_label="X", y_axis_label="Y")
p.scatter('x', 'y', size='size', source=source)

hover = HoverTool()
hover.tooltips = [("Node", "@name"), ("Degree", "@size")]
p.add_tools(hover)

show(p)
```

## node2vec

node2vec is a sibling of DeepWalk proposed by {cite:t}`grover2016node2vec`. While DeepWalk uses random walks, node2vec uses biased random walks that can move in different directions.

The bias walk is parameterized by two parameters, $p$ and $q$:

$$
P(v_{t+1} = x | v_t = v, v_{t-1} = t) \propto
\begin{cases}
\frac{1}{p} & \text{if } d(v,t) = 0 \\
1 & \text{if } d(v,t) = 1 \\
\frac{1}{q} & \text{if } d(v,t) = 2 \\
\end{cases}
$$

where $d(v,x)$ is the shortest path distance between node $v$ and $x$.

- A smaller $p$ leads to more biased towards the previous node, $v_{t-1} = t$.
- A smaller $q$ leads to more biased towards the nodes that are further away from the previous node, $v_{t-1} = t$.

By controlling these parameters, we can bias the walk to be more like breadth-first sampling (BFS) or depth-first sampling (DFS).

![](https://www.researchgate.net/publication/354654762/figure/fig3/AS:1069013035655173@1631883977008/A-biased-random-walk-procedure-of-node2vec-B-BFS-and-DFS-search-strategies-from-node-u.png)

The results are the embeddings that capture communities (with breadth-first sampling) and the structural equivalence (with depth-first sampling).


![](https://miro.medium.com/v2/resize:fit:1138/format:webp/1*nCyF5jFSU5uJVdAPdf-0HA.png)

```{note}
Structural equivalence refers to the concept where two nodes in a network are considered equivalent if they share the same neighbors. In other words, structurally equivalent nodes have identical connections to other nodes in the network.
```

### Exercise 02: Implement node2vec

<start from here>


```{footbibliography}

```
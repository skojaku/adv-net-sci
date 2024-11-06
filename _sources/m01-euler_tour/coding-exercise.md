---
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

<a target="_blank" href="https://colab.research.google.com/github/skojaku/adv-net-sci/blob/main/notebooks/exercise-m01-euler-tour.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

#  Exercise


## Exercise 01

1. Create a network of landmasses and bridges of Binghamton, NY.
2. Find an Euler path that crosses all the bridges of Binghamton, NY exactly once.

![](../figs/binghamton-map.jpg)


```{code-cell} ipython3
# If you are using colab, uncomment the following line
# !sudo apt install libcairo2-dev pkg-config python3-dev
# !pip install pycairo cairocffi
# !pip install igraph

```

Define the edges
```{code-cell} ipython3
# This is a placeholder for your code for the exercise
edges = ...
```


Define the adjacnecy matrix (without for loops!)
```{code-cell} ipython3
A = ...
```

Visualize the graph
```{code-cell} ipython3
import igraph
import matplotlib.pyplot as plt
import numpy as np

def visualize_graph(A, **params):
  A = np.array(A)
  src, trg = np.where(A)
  g = igraph.Graph(directed=False)
  g.add_vertices(A.shape[0])
  for s, t in zip(src, trg):
    for _ in range(A[s, t]):
      g.add_edge(s, t)
  return igraph.plot(g, **params)

visualize_graph(A)
```

Check if the graph has an Euler path
```{code-cell} ipython3

```


##  Exercise 02

Let's create a network from pre-existing data and check if it has an Euler path.

1. Select a network of your choice from [Netzschleuder](https://networks.skewed.de/). For convenience, choose a network of nodes less than 5000.
2. Download the csv version of the data by clicking something like "3KiB" under `csv` column.
3. Unzip the file and find "edges.csv", open it with a text editor to familiarize yourself with the format.
4. Load the data using `pandas`.
5. Get the source and target nodes from the data to create an edge list.
6. Construct the adjacency matrix from the edge list.
7. Draw the graph using `igraph`.
8. Check if the graph has an Euler path.


Load the data by
```{code-cell} ipython3
import pandas as pd
df = pd.read_csv('edges.csv') # load the data
display(df)
```

Then, get the srce and target nodes to compose an edge list
```{code-cell} ipython3
src = ...
trg = ...
edges = ...
```

Create the adjacency matrix from the edge list
```{code-cell} ipython3
```

Get the degree of each node
```{code-cell} ipython3
deg = ...
```

Visualize the graph
```{code-cell} ipython3
visualize_graph(A)
```

Check if the graph has an Euler path
```{code-cell} ipython3
```
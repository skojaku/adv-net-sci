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

<a target="_blank" href="https://colab.research.google.com/github/skojaku/adv-net-sci/blob/main/notebooks/exercise-m03-robustness.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

```{code-cell} ipython3
# If you are using Google Colab, uncomment the following line to install igraph
# !sudo apt install libcairo2-dev pkg-config python3-dev
# !pip install pycairo cairocffi
# !pip install igraph
```

# Hands-on: Robustness (Random attack)

We consider a small social network of 34 members in a university karate club, called Zachary's karate club network.
```{code-cell} ipython3
import igraph
g = igraph.Graph.Famous("Zachary")
igraph.plot(g, vertex_size=20)
```

Let's break the network 😈!
We will remove nodes one by one and see how the connectivity of the network changes at each step.
It is useful to create a copy of the network to keep the original network unchanged.

```{code-cell} ipython3
g_original = g.copy()
```

## Robustness against random failures

Let us remove a single node from the network. To this end, we need to first identify which nodes are in the network. With `igraph`, the IDs of the nodes in a graph are accessible through `Graph.vs.indices` as follows:
```{code-cell} ipython3
print(g.vs.indices)
```

We randomly choose a node and remove it from the network by using `Graph.delete_vertices`.

```{code-cell} ipython3
import numpy as np
node_idx = np.random.choice(g.vs.indices)
g.delete_vertices(node_idx)
print("Node removed:", node_idx)
print("Nodes remaining:", g.vs.indices)
```

:::{note}
`np.random.choice(array)` takes an array `array` and returns a single element from the array.
For example, `np.random.choice(np.array([1, 2, 3]))` returns either 1, 2, or 3 with equal probability.
See [the documentation](https://numpy.org/doc/stable/reference/random/generated/numpy.random.choice.html) for more details.
:::

The connectivity of the network is the fraction of nodes in the largest connected component of the network after node removal.
We can get the connected components of the network by using `Graph.connected_components`.
```{code-cell} ipython3
components = g.connected_components()
```
The sizes of the connected components are accessible via `Graph.connected_components.sizes`.
```{code-cell} ipython3
components.sizes()
```
Thus, the connectivity of the network can be computed by
```{code-cell} ipython3
components = g.connected_components()
connectivity = np.max(components.sizes()) / g_original.vcount()
connectivity
```

Putting together the above code, let us compute the robustness profile of the network.

```{code-cell} ipython3
import pandas as pd

g = g_original.copy() # restore the network
n_nodes = g.vcount()  # Number of nodes

results = []
for i in range(n_nodes -1):  # Loop if the network has at least one node

    # Remove a randomly selected node
    node_idx = np.random.choice(g.vs.indices)
    g.delete_vertices(node_idx)

    # Evaluate the connectivity
    components = g.connected_components()
    connectivity = np.max(components.sizes()) / g_original.vcount()

    # Save the results
    results.append(
        {
            "connectivity": connectivity,
            "frac_nodes_removed": (i + 1) / n_nodes,
        }
    )

df_robustness_profile = pd.DataFrame(results)
```

Let us plot the robustness profile.

```{code-cell} ipython3
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='white', font_scale=1.2)
sns.set_style('ticks')

ax = df_robustness_profile.plot(
    x="frac_nodes_removed",
    y="connectivity",
    kind="line",
    figsize=(5, 5),
    label="Random attack",
)
plt.xlabel("Proportion of nodes removed")
plt.ylabel("Connectivity")
plt.legend().remove()
plt.show()
```

## Targeted attack

In a targeted attack, nodes are removed based on specific criteria rather than randomly.
One common strategy is to remove nodes from the largest node degree to the smallest, based on the idea that removing nodes with many edges is more likely to disrupt the network connectivity.

The degree of the nodes is accessible via `Graph.degree`.
```{code-cell} ipython3
print(g_original.degree())
```

We compute the robustness profile by removing nodes with the largest degree and measuring the connectivity of the network after each removal.

```{code-cell} ipython3
g = g_original.copy() # restore the network
n_nodes = g.vcount()  # Number of nodes

results = []
for i in range(n_nodes -1):  # Loop if the network has at least one node

    # Remove the nodes with thelargest degree
    node_idx = g.vs.indices[np.argmax(g.degree())]
    g.delete_vertices(node_idx)

    # Evaluate the connectivity
    components = g.connected_components()
    connectivity = np.max(components.sizes()) / g_original.vcount()

    # Save the results
    results.append(
        {
            "connectivity": connectivity,
            "frac_nodes_removed": (i + 1) / n_nodes,
        }
    )

df_robustness_profile_targeted = pd.DataFrame(results)
```

```{code-cell} ipython3
sns.set(style='white', font_scale=1.2)
sns.set_style('ticks')

sns.set(style="white", font_scale=1.2)
sns.set_style("ticks")

ax = df_robustness_profile.plot(
    x="frac_nodes_removed",
    y="connectivity",
    kind="line",
    figsize=(5, 5),
    label="Random attack",
)
ax = df_robustness_profile_targeted.plot(
    x="frac_nodes_removed",
    y="connectivity",
    kind="line",
    label="Targeted attack",
    ax=ax,
)
ax.set_xlabel("Proportion of nodes removed")
ax.set_ylabel("Connectivity")
ax.legend(frameon=False)
plt.show()
```

While the network is robust against the random attacks, it is vulnerable to the degree-based targeted attack.
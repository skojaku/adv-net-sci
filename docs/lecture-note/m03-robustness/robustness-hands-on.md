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

# Hands-on: Robustness

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

How should we interpret the robustness profile? Consider the most robust network consisting of $N$ nodes, where all $N$ nodes are fully connected. Regardless of how many nodes are removed, there will always be a single connected component, and the size of this component will be $N-k$ if $k$ nodes are removed. Therefore, the connectivity is $(N-k)/N=1-k/N$, which corresponds to the diagonal line in the plot above.
Hence, **a network is considered robust if its connectivity curve is close to the diagonal line**.
On the other hand, if the curve is significantly lower than the diagonal line, the network is not robust.

For the network we considered above, the robustness profile is close to the diagonal line, indicating that the network is robust to the random removal of nodes.

:::{note}
The random attack is stochastic, meaning that the robustness profile has a variation in each run. Thus, it is necessary to run the attack multiple times and average the results to get a more accurate estimate of the robustness.
:::

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

The **$R$-index** is the area under the connectivity curve, which can be computed by

```{code-cell} ipython3
rindex = df_robustness_profile["connectivity"].mean()
rindex_targeted = df_robustness_profile_targeted["connectivity"].mean()
print(f"R-index (random): {rindex:.3f}")
print(f"R-index (targeted): {rindex_targeted:.3f}")
```

The targeted attack has a smaller $R$-index, indicating that the network is less robust to the targeted attack compared to the random attack.
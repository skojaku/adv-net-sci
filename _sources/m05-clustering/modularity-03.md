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

# Modularity maximization with Python

Let us showcase how to use `igraph` to detect communities with modularity. We will use the Karate Club Network as an example.


```{code-cell} ipython3
import igraph
g = igraph.Graph.Famous("Zachary")
igraph.plot(g, vertex_size=20)
```

When it comes to maximizing modularity, there are a variety of algorithms to choose from.
Two of the most popular ones are the `Louvain` and `Leiden` algorithms, both of which are implemented in `igraph`. The Louvain algorithm has been around for quite some time and is a classic choice, while the Leiden algorithm is a newer bee that often yields better accuracy. For our example, we'll be using the `Leiden` algorithm, and I think you'll find it really effective!

```{code-cell} ipython3
communities = g.community_leiden(resolution=1, objective_function= "modularity")
```

What is `resolution`? It is a parameter that helps us tackle the resolution limit of the modularity maximization algorithm {cite:p}`fortunato2007resolution`!
In simple terms, when we use the resolution parameter $\rho$, the modularity formula can be rewritten as
 follow:

$$
Q(M) = \frac{1}{2m} \sum_{i=1}^n \sum_{j=1}^n \left(A_{ij} - \rho \frac{k_i k_j}{2m}\right) \delta(c_i, c_j)
$$

Here, the parameter $\rho$ plays a crucial role in balancing the positive and negative parts of the equation.
The resolution limit comes into play because of the diminishing effect of the negative term as the number of edges $m$ increases.
The parameter $\rho$ can adjust this balance and allow us to circumvent the resolution limit.

What is `communities`? This is a list of communities, where each community is represented by a list of nodes by their indices.

```{code-cell} ipython3
print(communities)

```
Let us visualize the communities by coloring the nodes in the graph.

```{code-cell} ipython3
import seaborn as sns
community_membership = communities.membership
palette = sns.color_palette().as_hex()
igraph.plot(g, vertex_color=[palette[i] for i in community_membership])
```

- `community_membership`: This is a list of community membership for each node.
- `palette`: This is a list of colors to use for the communities.
- `igraph.plot(g, vertex_color=[palette[i] for i in community_membership])`: This plots the graph 'g' with nodes colored by their community.

```{admonition} Exercise
:class: tip

Let's try out different values of the resolution parameter and observe how the community structure changes.

```
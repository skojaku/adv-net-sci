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

# Graph cut

Another approach from computer science is to treat a community detection problem as an *optimization* problem.
An early example is the **graph cut** problem, which asks to find the minimum number of edges to cut the graph into two disconnected components.

Specifically, let us consider cutting the network into two communities. Let $V_1$ and $V_2$ be the set of nodes in the two communities.
Then, the cut is the number of edges between the two communities, which is given by

$$
\begin{align}
\text{Cut}(V_1, V_2) = \sum_{i \in V_1} \sum_{j \in V_2} A_{ij}
\end{align}
$$

Now, the community detection problem is translated into **an optimization problem**, with the goal of finding a cut $V_1, V_2$ that minimizes $\text{Cut}(V_1, V_2)$.

The description of this problem is not complete 😈. Let's find out what is missing by playing with the optimization problem.

```{admonition} Exercise
:class: tip

Can you identify what is missing in the description of the graph cut problem? Without this, the best cut is trivial. {{ "<a href='BASE_URL/vis/community-detection/index.html?scoreType=graphcut&numCommunities=2&randomness=1&dataFile=two-cliques.json'>Graph Cut Problem 🎮</a>".replace('BASE_URL', base_url) }}

```{dropdown} Click to reveal the answer!

The missing element is a constraint: each community must contain at least one node. Without this, the trivial solution of placing all nodes in a single community would always yield a cut of zero.
```
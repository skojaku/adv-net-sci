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
An early example is the **graph cut** problem, which asks to find the minimum number of edges to cut in a graph into two disconnected components.

Specifically, let us first represent a binary label for each node, $x_i \in \{0, 1\}$, where nodes with the same label are in the same community.
The number of edges between the two communities is given by

$$
\begin{align}
\text{Cut}(x)
&= \frac{1}{2}\sum_{i=1}^{N} \sum_{j=1}^{N} A_{ij} \cdot \left( 1- \delta(x_i, x_j) \right)
\end{align}
$$
-  $\delta(x_i, x_j)$ is *the Kronecker delta function*, which is 1 if $x_i = x_j$ and 0 otherwise.
- The factor $1/2$ corrects for double counting of edges due to the double summation.

Now, the community detection problem is translated into **an optimization problem**, with the goal being to find a cut $x$ that minimizes $\text{Cut}(x)$.


The description of this problem is not complete 😈. Let's find out what is missing by playing with the optimization problem.

- **Interactive Demo**: Can you identify what is missing in the description of the graph cut problem? Without this, the best cut is trivial. {{ "<a href='BASE_URL/vis/community-detection/index.html?scoreType=graphcut&numCommunities=2&randomness=1&dataFile=two-cliques.json'>Graph Cut Problem 🎮</a>".replace('BASE_URL', base_url) }}
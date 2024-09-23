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

# Random Walk and Centrality

Random walkers make a random decision at every step. However, they visit some nodes more freuquently than others. These nodes often have many edges in the network. Is this a coincidence?

There are two factors that determine the behavior of a random walker.

The first factor is the dependence of the random walk on the starting node. Namely, for the first few steps, the walker is localized around the node where it starts.
However, this dependence decays as the walker makes more steps, and eventually the walker's position becomes independent of the starting node.
We call the distribution of the walker after infinite steps as the **stationary state** or **steady-state**.

The second factor is the friendship paradox: "Your friends have more friends than you do." This explains why random walkers tend to visit nodes with many edges. Namely, a walker traverses an edge from you, it is likely to reach someone with more edges on average, because of the friendship paradox. Consequently, despite the random decision at every step, the walker is biased to visit nodes with many edges.

An important consequence of these two factors is the following.

$$
\pi_i \propto d_i, \; \text{or equivalently} \; \pi_i \propto \frac{d_i}{2m}
$$

where $\pi_i$ is the probability of visiting node $i$ in the stationary state, $d_i$ is the degree of node $i$, and $m$ is the number of edges in the network.

This result shows that, in a network, nodes with many edges are visited more frequently than nodes with few edges.
This is because the number of edges a node has is a good proxy for the node's importance.

Another important observation is the dependence of the random walk on the starting node.
For the first few steps, the walker is concentrated around the node where it starts. But, after many steps, the walker walks away from where it starts.
Ultimately, the walker's position after sufficiently many steps is independent of the starting node.
The position
the walker's position is determined by the network structure, not the initial node.
At the begining of the walk, the walker is concentrated around the node where it starts. But, after many steps

> In a social network, most individuals have more friends than the average friend count of their friends.
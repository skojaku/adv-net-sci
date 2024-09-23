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


# Characteristics of random walks

## Stationary state

Let's dive into the math behind random walks in a way that's easy to understand.

Imagine you're at a node $i$ at time $t$. You randomly choose one of the neighboring nodes to move to, let's call it node $j$. The chance of moving from node $i$ to node $j$ is called the transition probability $p_{ij}$:

$$
p_{ij} = \frac{A_{ij}}{k_i},
$$

Here, $A_{ij}$ is part of the adjacency matrix (which tells us if there's a connection between nodes $i$ and $j$), and $k_i$ is the number of connections (degree) node $i$ has. If our network has $N$ nodes, we have $N \times N$ transition probabilities, which we can put together in a *transition probability matrix* $P$.

$$
\mathbf{P} = \begin{pmatrix}
p_{11} & p_{12} & \cdots & p_{1N} \\
p_{21} & p_{22} & \cdots & p_{2N} \\
\vdots & \vdots & \ddots & \vdots \\
p_{N1} & p_{N2} & \cdots & p_{NN}
\end{pmatrix}
$$

This matrix $P$ tells us everything about the random walk process. Using $P$, we can figure out how often we expect to visit each node after taking $T$ steps. For example, the chance of visiting node $j$ after one step from node $i$ is simply:

$$
P_{ij} = p_{ij}.
$$

If we want to know the chance of visiting node $j$ after **two steps** from node $i$, we use:

$$
\left(\mathbf{P}^{2}\right)_{ij} = \sum_{k} P_{ik} P_{kj}.
$$

Let's break this down:
- The sum is over all possible intermediate nodes $k$.
- $P_{ik}P_{kj}$ is the chance of moving from node $i$ to node $k$, and then from node $k$ to node $j$.
- By adding up all these probabilities, we get the total chance of moving from node $i$ to node $j$ in two steps.

Similarly, the chance of visiting node $j$ after **$T$ steps** from node $i$ is:

$$
\left(\mathbf{P}^{T}\right)_{ij}
$$

Armed with this, let us consider the long-term behavior of the random walk. We represent $\mathbf{x}(t) = [x_1(t), \ldots, x_N(t)]^\top$ as the probability distribution of being at each node at time $t$. As $T$ becomes very large, $\left(\mathbf{P}^{T}\right)_{ij}$ settles down to a constant value such that:

$$
\mathbf{x}(t) = \mathbf{P} \mathbf{x}(t+1).
$$

This is an eigenvector equation, and the solution is given by the Perron-Frobenius theorem. For undirected networks, such vector always exists and is called the **stationary distribution** of the random walk. According to the Perron-Frobenius theorem, the solution is:


$$
\mathbf{x}(\infty) = \mathbb{\pi}, \; \mathbf{\pi} = [\pi_1, \ldots, \pi_N]
$$

Here, $\mathbb{\pi} = [\pi_1, \ldots, \pi_N]$ is the stationary distribution. This means $\pi_j$ is the long-term probability of being at node $j$. This is an eigenvector equation, and $\pi_j$ is the left eigenvector of $P$ with eigenvalue 1. For undirected networks, this vector $\pi$ always exists and is given by:

$$
\pi_j = \frac{k_j}{\sum_{\ell} k_\ell} \propto k_j.
$$

This means the probability of being at node $j$ in the long run is proportional to the degree of node $j$. The normalization ensures that the sum of all probabilities is 1, i.e., $\sum_{j=1}^N \pi_j = 1$.

## Mixing time

How fast does a random walker converges to the stationary state? The speed of convergence depends on the edge density and the community structure of the network because a walker tends to stay within its community where it started from, and takes more steps to explore the network if the network is sparse.

Mixing time is the number of steps it takes for the random walker to approach the stationary state, up to a certain error margin $\delta$.

$$
\sum_j \left|\pi_j - x_j(t)\right| < \delta,
$$

Random walkers converge to the stationary state quickly if the network is well-connected and does not have strong community structure.
On the other hand, it takes longer to converge if the network is sparse or has dense communities sparsely connected across.

Mixing time is the number of steps it takes for the random walker to reach the stat

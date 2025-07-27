# Random walks unify centrality and communities

## Modularity: Interpretation from random walk perspective

Modularity can be intepreted as a random walk perspective. Modularity is given by

$$
Q = \frac{1}{2m} \sum_{ij} \left( A_{ij} - \frac{d_i d_j}{2m} \right) \delta(c_i, c_j)
$$

where $m$ is the number of edges in the network, $A_{ij}$ is the adjacency matrix, $d_i$ is the degree of node $i$, $c_i$ is the community of node $i$, and $\delta(c_i, c_j)$ is the Kronecker delta function (which is 1 if $c_i = c_j$ and 0 otherwise).

We can rewrite the modularity using the language of random walks as follows.

$$
\begin{aligned}
Q &= \sum_{ij} \left(\frac{A_{ij}}{2m}  - \frac{d_i}{2m} \frac{d_j}{2m} \right) \delta(c_i, c_j) \\
&= \sum_{ij} \left(\pi_i P_{ij}  - \pi_i \pi_j \right) \delta(c_i, c_j)
\end{aligned}
$$
where $\pi_i$ is the stationary distribution of the random walk given by

$$
\pi_i = \frac{d_i}{2m}
$$

and $P_{ij}$ is the transition probability between nodes $i$ and $j$.

```{note}
Let's break down this derivation step by step:

1. We start with the original modularity formula:

   $$Q = \frac{1}{2m} \sum_{ij} \left( A_{ij} - \frac{d_i d_j}{2m} \right) \delta(c_i, c_j)$$

2. First, we move the constant $1/(2m)$ to the inside of the parentheses:

   $$Q = \sum_{ij} \left(\frac{A_{ij}}{2m} - \frac{d_i d_j}{2m^2} \right) \delta(c_i, c_j)$$

3. Now, we recognize that $\frac{A_{ij}}{2m}$ can be rewritten as:

   $$\frac{A_{ij}}{2m} = \frac{d_i}{2m} \cdot \frac{A_{ij}}{d_i} = \pi_i P_{ij}$$

4. We also recognize that $\frac{d_i}{2m}$ is the stationary distribution of the random walk, which we denote as $\pi_i$:

   $$\frac{d_i}{2m} = \pi_i$$

5. Substituting these into our equation:

   $$Q = \sum_{ij} \left(\pi_i P_{ij} - \pi_i \pi_j \right) \delta(c_i, c_j)$$

```

The expression suggests that:

1. The first term, $\pi_i P_{ij} \delta(c_i, c_j)$, represents the probability that a walker is at node $i$ and moves to node $j$ within the same community **by one step**.
2. The second term, $\pi_i \pi_j$, represents the probability that a walker is at node $i$ and moves to another node $j$ within the same community **after long steps**.

In summary, modularity compares short-term and long-term random walk probabilities. High modularity indicates that a random walker is more likely to stay within the same community after one step than after many steps.

```{note}
Building on this perspective from random walks, Delvenne et al. {footcite}`delvenne2010stability` extends the modularity by comparing multi-step and long-step transition probabilities of a random walk. This approach, known as "Markov stability", shows that the number of steps acts as a "resolution parameter" that determines the scale of detectable communities.
```


## PageRank: Interpretation from random walk perspective

PageRank can be interpreted from a random walk perspective:

$$
c_i = (1-\beta) \sum_j P_{ji} c_j + \beta \cdot \frac{1}{N}
$$

Where:
- $c_i$ is the PageRank of node $i$
- $P_{ji}$ is the transition probability from node $j$ to node $i$
- $\beta$ is the teleportation probability
- $N$ is the total number of nodes

This equation represents a random walk where:
1. With probability $(1-\beta)$, the walker follows a link to the next node.
2. With probability $\beta$, the walker *teleports* to a random node in the network.

The PageRank $c_i$ is the stationary distribution of this random walk, representing the long-term probability of finding the walker at node $i$.

```{note}
This sounds odd at first glance. But it makes sense when you think about what PageRank was invented for, i.e., Web search. It characterizes a web surfer as a random walker that chooses the next page by randomly jumping to a random page with probability $\beta$ or by following a link to a page with probability $1-\beta$. The web page with the largest PageRank means that the page is most likely to be visited by this random web surfer.
```


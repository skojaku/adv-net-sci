# Robustness Analysis - Exercises

## Percolation Theory and Network Connectivity

Consider a random network of $N$ nodes, where every pair of nodes are connected by an edge with a certain probability. The degree $k$ of a node follows a binomial distribution, which we approximate by a Poisson random variable with mean $\langle k \rangle$ and variance $\langle k \rangle$.

1. Derive $\langle k^2 \rangle$ using $\langle k \rangle$.
   - Hint: Variance is defined as $\text{Var}(k) = \langle (k-\langle k \rangle)^2 \rangle$.
2. Compute the ratio $\frac{\langle k^2 \rangle}{\langle k \rangle}$.
3. Check when the network satisfies the Molloy-Reed criterion.

::: {.callout collapse="true"}
## Solution

**Solution for Q1**:
To derive $\langle k^2 \rangle$, we start with the definition of variance

$$\text{Var}(k) = \langle (k - \langle k \rangle)^2 \rangle$$

Expanding the square, we get

$$\text{Var}(k) = \langle k^2 \rangle - 2\langle k \rangle \langle k \rangle + \langle k \rangle^2$$

Since $\text{Var}(k) = \langle k \rangle$ for a Poisson distribution, we can substitute and rearrange

$$\langle k \rangle = \langle k^2 \rangle - \langle k \rangle^2$$

Solving for $\langle k^2 \rangle$, we obtain

$$\langle k^2 \rangle = \langle k \rangle + \langle k \rangle^2$$

**Solution for Q2**:
$\frac{\langle k^2 \rangle}{\langle k \rangle} = 1 + \langle k \rangle$

**Solution for Q3**:
$\langle k \rangle >1$. In other words, if a node has on average more than one neighbor, the random network is likely to have a giant component.
:::

## Robust Network Design

Design strategies for networks that must withstand both random failures and targeted attacks present unique challenges. Consider the trade-offs between different network topologies and their resilience properties.

**Challenge**: What design strategy makes a network robust against targeted attacks? Design a network that is robust against both random failures and targeted attacks.

{{ '[🚀 Interactive Demo]( BASE_URL/vis/network-robustness.html)'.replace('BASE_URL', base_url) }}

::: {.callout collapse="true"}
## Design Strategy

A bimodal degree distribution can enhance network robustness against both random failures and targeted attacks. In this setup, $(1-r)$ portion of nodes have a degree of 1, while $r$ portion of nodes have a high degree, $k_{\text{max}}$.

This structure ensures that the network remains connected even if a hub is removed, as other hubs maintain the connectivity. It also withstands random failures due to its heterogeneous degree distribution.
:::

## Power Grid Network Design

Real-world infrastructure design requires balancing multiple objectives: cost efficiency, reliability, and robustness. Power grids exemplify this challenge perfectly.

**Challenge**: Design a cost-effective power grid network using minimum spanning tree concepts. Consider the trade-offs between cost minimization and network robustness.

- ✍️ [Pen and Paper Exercise](./pen-and-paper/exercise.pdf)

This exercise bridges theoretical network concepts with practical engineering constraints, demonstrating how robustness analysis guides infrastructure investment decisions.
# Exercises

## Exercise 1: Percolation Theory

Consider a random network of $N$ nodes, where every pair of nodes are connected by an edge with a certain probability.
Then, the degree $k$ of a node is a binomial random variable, which we approximate by a Poisson random variable with mean $\langle k \rangle$. The variance of the Poisson random variable is also $\langle k \rangle$.

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

## Exercise 2: Network Design

What is the design strategy to make a network robust against targeted attacks?
Design a network that is robust against both random failures and targeted attacks.

{{ '[🚀 Interactive Demo]( BASE_URL/vis/network-robustness.html)'.replace('BASE_URL', base_url) }}

::: {.callout collapse="true"}
## An answer

A bimodal degree distribution can enhance network robustness against both random failures and targeted attacks.
In this setup, $(1-r)$ portion of nodes have a degree of 1, while $r$ portion of nodes have a high degree, $k_{\text{max}}$.
This structure ensures that the network remains connected even if a hub is removed, as other hubs maintain the connectivity. It also withstands random failures due to its heterogeneous degree distribution.
:::

## Exercise 3: Power Grid Network

- ✍️ [Pen and Paper](./pen-and-paper/exercise.pdf)

Design a cost-effective power grid network using minimum spanning tree concepts. Consider the trade-offs between cost minimization and network robustness.
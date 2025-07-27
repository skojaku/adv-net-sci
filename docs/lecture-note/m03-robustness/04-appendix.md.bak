# Appendix

## Derivation of the Molloy-Reed criterion

Molloy and Reed derived the following criterion for an existence of a giant component in a network with an arbitrary degree distribution {footcite}`molloy1995critical`.
It is based on a simple heuristic argument: the network has a giant component when a random node $i$ with neighbor $j$ has, on average, is connected to at least one other node. We write the condition as

$$
\langle k_i \vert i \leftrightarrow j \rangle = \sum_{k} k P(k \vert i \leftrightarrow j) > 2
$$

where $\langle k_i \vert i \leftrightarrow j \rangle$ is the conditional average degree of node $i$ given that it is connected to node $j$. From Bayes' theorem, we have

$$
P(k_i \vert i \leftrightarrow j) = \frac{P(i \leftrightarrow j \vert k_i) P(k_i)}{P(i \leftrightarrow j)}
$$

Assuming that the network is uncorrelated and sparse (meaning, we neglect loops), then $P(i \leftrightarrow j \vert k_i) = k_i / (N-1)$ and $P(i \leftrightarrow j) = \langle k \rangle / (N-1)$. Substituting these into the above equation, we get

$$
P(k_i \vert i \leftrightarrow j) = \frac{k_i P(k_i)}{\langle k \rangle}
$$

Thus, the condition for the existence of a giant component is

$$
\frac{1}{\langle k \rangle} \sum_{k_i} k_i^2 P(k_i) = \frac{\langle k^2 \rangle}{\langle k \rangle} > 2
$$


## Derivation of the percolation threshold for a random attack.

Assume a fraction $p$ of nodes are removed independently from the network. The removal of nodes reduces the connectivity of the network and the degree of the remaining nodes.
The probability that a node with initial degree $k_0$ reduces its degree to $k$ follows
a binomial distribution,

$$
P(k \vert k_0, p) = \binom{k_0}{k} (1-p)^k p^{k_0-k}
$$

Considering all nodes, the new degree distribution is given by

$$
P'(k) = \sum_{k_0 = k}^{\infty} P(k_0) \binom{k_0}{k} (1-p)^k p^{k_0-k}
$$

To connect with the Molloy-Reed criterion, we need to compute the first and second moments, denoted by $\langle k \rangle'$ and $\langle k^2 \rangle'$, of the new degree distribution.

$$
\begin{align}
\langle k \rangle' &= \sum_{k} k P'(k_0) \\
&= \sum_{k} \sum_{k_0=k}^{\infty} k \binom{k_0}{k} (1-p)^k p^{k_0-k} P(k_0) \\
&= \sum_{k_0=0}^\infty P(k_0) \underbrace{\sum_{k} k \binom{k_0}{k} (1-p)^k p^{k_0-k}}_{\text{Expected value of $k$ for a binomial distribution}} \\
&= \sum_{k_0=0}^\infty P(k_0) k_0 (1-p) \\
&= \langle k_0 \rangle (1-p)
\end{align}
$$

Similarly, we can compute the second moment, which is given by

$$
\langle k^2 \rangle' = \langle k_0^2 \rangle (1-p)^2 + \langle k_0 \rangle p (1-p)
$$

By substituting these into the Molloy-Reed criterion, we get

$$
\frac{\langle k^2 \rangle'}{\langle k \rangle'}  = \frac{\langle k_0^2 \rangle (1-p)^2 + \langle k_0 \rangle p (1-p)}{\langle k_0 \rangle (1-p)} = \frac{\langle k_0^2 \rangle (1-p) + \langle k_0 \rangle p}{\langle k_0 \rangle} > 2
$$

By solving the inequality for $p$, we get the percolation threshold for a random attack,

$$
1-p < \frac{1}{\langle k_0 ^2 \rangle / \langle k_0 \rangle - 1}
$$

which is the condition for the existence of a giant component.

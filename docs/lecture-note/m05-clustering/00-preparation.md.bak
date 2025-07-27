# Module 5 Preparation: Clustering Foundations

## Recap from Module 4: Friendship Paradox and Degree Distributions

### Friendship Paradox

The friendship paradox arises not because of the way we form friendships, but because of measurement! A person with 100 friends generates 100 cards, while a person with 1 friend generates only 1 card. If we average friend counts over the cards, popular people are counted more. This is where the friendship paradox comes from.

In network terms, cards represent edges and people represent nodes. The friendship paradox arises because we measure at different levels: nodes or edges. The average friend count at the node level is lower than at the edge level because popular people are counted more often at the edge level.

### Degree Distribution Fundamentals

Understanding degree distribution is the first key step to understand networks! The degree of a node $i$, denoted by $d_i$, is the number of edges connected to it. With the adjacency matrix $A$, the degree of node $i$ is given by:

$$
k_i = \sum_{j=1}^N A_{ij}.
$$

The degree distribution $p(k)$ can be computed by counting the number of nodes with each degree and dividing by the total number of nodes. For visualization, we often use the complementary cumulative distribution function (CCDF):

$$
\text{CCDF}(k) = P(k' > k) = \sum_{k'=k+1}^\infty p(k')
$$

The slope of the CCDF tells us the heterogeneity of the degree distribution:
- Steep slope: more **homogeneous** degree distribution (similar degrees)
- Flat slope: more **heterogeneous** degree distribution (wide range of degrees)

### Degree Distribution of Friends

When we sample edges uniformly at random, the degree distribution of a friend is given by:

$$
p'(k) = \frac{k}{\langle k \rangle} p(k)
$$

This biased sampling leads to the friendship paradox, where the average degree of a friend is:

$$
\langle k' \rangle = \frac{\langle k^2 \rangle}{\langle k \rangle} \geq \langle k \rangle
$$

## Linear Algebra Foundations for Clustering

### Adjacency Matrix

The adjacency matrix $A$ is fundamental to network analysis. For an undirected network with $N$ nodes:
- $A_{ij} = 1$ if nodes $i$ and $j$ are connected
- $A_{ij} = 0$ if nodes $i$ and $j$ are not connected
- $A$ is symmetric: $A_{ij} = A_{ji}$

### Degree Matrix

The degree matrix $D$ is a diagonal matrix where:
$$
D_{ii} = \sum_{j=1}^N A_{ij} = k_i
$$

All off-diagonal elements are zero: $D_{ij} = 0$ for $i \neq j$.

### Graph Laplacian

The graph Laplacian $L$ is defined as:
$$
L = D - A
$$

Properties of the Laplacian:
- Symmetric matrix for undirected graphs
- All row sums are zero: $\sum_{j} L_{ij} = 0$
- Positive semidefinite: all eigenvalues are non-negative
- The number of zero eigenvalues equals the number of connected components

### Normalized Graph Laplacian

The normalized Laplacian is defined as:
$$
\mathcal{L} = D^{-1/2} L D^{-1/2} = I - D^{-1/2} A D^{-1/2}
$$

where $I$ is the identity matrix. This normalization is crucial for spectral clustering algorithms.

### Eigenvalues and Eigenvectors

For a matrix $M$, an eigenvector $v$ and eigenvalue $\lambda$ satisfy:
$$
M v = \lambda v
$$

Key properties:
- For symmetric matrices, eigenvalues are real and eigenvectors are orthogonal
- The smallest eigenvalues of the Laplacian are most informative for clustering
- The second smallest eigenvalue (algebraic connectivity) indicates how well-connected the graph is

### Matrix Norms and Cuts

The **cut** between two sets of nodes $S$ and $T$ is:
$$
\text{cut}(S, T) = \sum_{i \in S} \sum_{j \in T} A_{ij}
$$

This can be expressed in matrix form using indicator vectors. If $\mathbf{x}$ is an indicator vector where $x_i = 1$ if node $i \in S$ and $x_i = -1$ if node $i \in T$, then:
$$
\text{cut}(S, T) = \frac{1}{4} \mathbf{x}^T L \mathbf{x}
$$

This matrix formulation connects graph cuts to quadratic optimization problems, which forms the basis for spectral clustering algorithms.

## Why These Concepts Matter for Clustering

1. **Matrix Representations**: Adjacency and Laplacian matrices encode network structure in a form amenable to linear algebra techniques.

2. **Spectral Properties**: Eigenvalues and eigenvectors of the Laplacian reveal the natural clustering structure of networks.

3. **Optimization Framework**: Many clustering problems can be formulated as matrix optimization problems.

4. **Degree Bias Understanding**: Knowledge of degree distributions helps us understand why certain normalization schemes (ratio cut, normalized cut) are necessary.

This mathematical foundation will be essential as we explore different clustering methods in the following sections.
# Preparation: Random Walks and Linear Algebra Foundations

## Overview from Module 7: Random Walks

### What is a Random Walk?

A random walk in undirected networks is the following process:
1. Start at a node $i$
2. Randomly choose an edge to traverse to a neighbor node $j$
3. Repeat step 2 until you have taken $T$ steps.

Suppose you walk in a city. You are drunk and your feet have no idea where to go. You just take a step wherever your feet take you. At every intersection, you make a random decision and take a step. This is the core idea of a random walk.

While your feet are taking you to a random street, after making many steps and looking back, you will realize that you have been to certain places more frequently than others. If you were to map the frequency of your visits to each street, you will end up with a distribution that tells you about salient structure of the street network.

### Mathematical Foundation: Transition Probabilities

The probability of moving from node $i$ to node $j$, called the transition probability $p_{ij}$, is:

$$p_{ij} = \frac{A_{ij}}{k_i}$$

where $A_{ij}$ is an element of the adjacency matrix, and $k_i$ is the degree of node $i$. For a network with $N$ nodes, we can represent all transition probabilities in a transition probability matrix $\mathbf{P}$.

The probability distribution after $t$ steps is:
$$\mathbf{x}(t) = \mathbf{x}(0) \mathbf{P}^t$$

### Stationary Distribution

As $T$ becomes very large, the probability distribution approaches a constant value called the stationary distribution:

$$\mathbf{x}(\infty) = \boldsymbol{\pi}, \; \boldsymbol{\pi} = [\pi_1, \ldots, \pi_N]$$

For undirected networks, this stationary distribution is proportional to the degree of each node:

$$\pi_j = \frac{k_j}{\sum_{\ell} k_\ell} \propto k_j$$

## Essential Linear Algebra: Eigenvalues and Eigenvectors

### Matrix Diagonalization

A diagonalizable matrix $\mathbf{S}$ can be written as:
$$\mathbf{S} = \mathbf{Q} \boldsymbol{\Lambda} \mathbf{Q}^{-1}$$

where $\boldsymbol{\Lambda}$ is a diagonal matrix of eigenvalues and $\mathbf{Q}$ is a matrix of eigenvectors. This is useful because:

$$\mathbf{S}^t = \mathbf{Q} \boldsymbol{\Lambda}^t \mathbf{Q}^{-1}$$

### Spectral Properties of Networks

For network analysis, we work with the normalized adjacency matrix:
$$\overline{\mathbf{A}} = \mathbf{D}^{-\frac{1}{2}} \mathbf{A} \mathbf{D}^{-\frac{1}{2}}$$

where $\mathbf{D}$ is the diagonal degree matrix. This matrix is symmetric and can be diagonalized as:
$$\overline{\mathbf{A}} = \mathbf{Q} \boldsymbol{\Lambda} \mathbf{Q}^\top$$

### Connection to Random Walks

The transition matrix can be expressed using the normalized adjacency matrix:
$$\mathbf{P} = \mathbf{D}^{-\frac{1}{2}} \overline{\mathbf{A}} \mathbf{D}^{\frac{1}{2}}$$

This allows us to compute:
$$\mathbf{P}^t = \mathbf{Q}_L \boldsymbol{\Lambda}^t \mathbf{Q}_R^\top$$

where $\mathbf{Q}_L = \mathbf{D}^{-\frac{1}{2}} \mathbf{Q}$ and $\mathbf{Q}_R = \mathbf{D}^{\frac{1}{2}} \mathbf{Q}$.

### Eigenvalue Interpretation

The probability distribution after $t$ steps can be written as:

$$\mathbf{x}(t) = \sum_{\ell=1}^N \lambda_\ell^t \mathbf{q}^{(L)}_{\ell} \langle\mathbf{q}^{(R)}_{\ell}, \mathbf{x}(0) \rangle$$

Key insights:
- The largest eigenvalue is always $\lambda_1 = 1$
- The second largest eigenvalue $\lambda_2$ determines convergence speed
- As $t \to \infty$, all terms decay except the first, leading to the stationary distribution

### Mixing Time

The mixing time $t_{\text{mix}}$ is the time needed to reach the stationary distribution and is bounded by:

$$t_{\text{mix}} \leq \frac{1}{1-\lambda_2}$$

where $\lambda_2$ is the second largest eigenvalue of the normalized adjacency matrix.

## Why This Matters for Embedding

Understanding random walks and spectral properties is crucial for embedding methods because:

1. **Spectral Embedding**: Uses eigenvectors of graph matrices to create node representations
2. **Neural Embeddings**: Methods like Word2Vec can be understood through random walk processes
3. **Convergence Properties**: Eigenvalues determine how well embedding methods will work
4. **Structural Information**: Eigenvectors capture important network structural properties

The concepts from random walks provide the mathematical foundation for understanding how both classical spectral methods and modern neural embedding approaches extract meaningful representations from network structure.
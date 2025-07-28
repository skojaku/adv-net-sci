# Preparation: Markov Chain Theory Prerequisites

## Required Knowledge from Previous Modules

Before studying random walks, ensure you understand:
- **From M01-M06**: Network representations, eigenvalue theory, matrix operations
- **From M06**: Advanced concepts like matrix series convergence and spectral properties

## Probability Theory for Stochastic Processes

### Discrete Probability Basics
Foundation for understanding random processes:
- **Probability distributions**: Discrete probability mass functions
- **Conditional probability**: $P(A|B) = \frac{P(A \cap B)}{P(B)}$
- **Independence**: When events don't influence each other
- **Law of total probability**: $P(A) = \sum_i P(A|B_i)P(B_i)$

### Stochastic Processes
Understanding time-dependent random systems:
- **Random variable sequences**: $X_0, X_1, X_2, \ldots$
- **State space**: Set of possible values for each $X_t$
- **Transition probabilities**: $P(X_{t+1} = j | X_t = i)$

## Markov Chain Fundamentals

### Markov Property
The defining characteristic of Markov chains:
$$P(X_{t+1} = j | X_t = i, X_{t-1} = i_{t-1}, \ldots, X_0 = i_0) = P(X_{t+1} = j | X_t = i)$$

**Interpretation**: Future state depends only on present state, not on history.

### Transition Matrix Theory
Matrix representation of state transitions:
- **Stochastic matrix**: Rows sum to 1, all entries non-negative
- **Chapman-Kolmogorov equation**: $P^{(n+m)} = P^{(n)} \cdot P^{(m)}$
- **n-step transition probabilities**: $(P^n)_{ij} = P(X_n = j | X_0 = i)$

### Classification of States
Understanding different types of states:
- **Accessible**: State $j$ is accessible from state $i$ if $P^{(n)}_{ij} > 0$ for some $n$
- **Communicating**: States $i$ and $j$ communicate if each is accessible from the other
- **Irreducible**: All states communicate with each other
- **Periodic**: State $i$ has period $d$ if returns are only possible at multiples of $d$ steps

## Limit Behavior and Convergence

### Stationary Distributions
Probability distributions that don't change over time:
- **Definition**: $\pi P = \pi$ where $\pi$ is a row vector
- **Existence**: Guaranteed for finite, irreducible chains
- **Uniqueness**: Unique for irreducible chains

### Convergence Theorems
When and how chains reach equilibrium:
- **Ergodic theorem**: For irreducible, aperiodic chains: $\lim_{n \to \infty} P^{(n)}_{ij} = \pi_j$
- **Rate of convergence**: How quickly the chain approaches stationary distribution
- **Mixing time**: Time needed to get close to stationary distribution

## Linear Algebra for Markov Chains

### Eigenvalue Structure
Connection between eigenvalues and chain behavior:
- **Dominant eigenvalue**: Always equals 1 for stochastic matrices
- **Subdominant eigenvalue**: Controls convergence rate
- **Spectral gap**: Difference between largest and second-largest eigenvalues

### Perron-Frobenius for Stochastic Matrices
Special properties of transition matrices:
- **Principal eigenvalue**: Always 1
- **Principal eigenvector**: Corresponds to stationary distribution
- **Non-negative entries**: All eigenvector entries are non-negative

## Applications Context

### Random Walks on Graphs
Specific application of Markov chains to networks:
- **State space**: Nodes of the graph
- **Transition probabilities**: Based on edge structure
- **Uniformity**: Equal probability to each neighbor

### Information Propagation
Understanding how information spreads:
- **Diffusion processes**: How properties spread through networks
- **Equilibrium**: Long-term distribution of walkers or information

These probability and linear algebra foundations are essential for understanding how random walks reveal network structure through their stationary distributions and convergence properties.
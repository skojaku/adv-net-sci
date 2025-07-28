# Preparation: Advanced Linear Algebra for Network Analysis

## Required Knowledge from Previous Modules

Before studying centrality measures, ensure you understand:
- **From M01-M05**: Network representations, eigenvalue concepts from clustering
- **Linear algebra**: Matrix operations, eigenvalue decomposition from M05

## Advanced Matrix Theory

### Matrix Powers and Series

#### Matrix Powers
Understanding powers of matrices:
- $A^k$ represents $k$-step relationships in networks
- Interpretation: $A^k_{ij}$ = number of walks of length $k$ from node $i$ to $j$
- **Convergence**: How $A^k$ behaves as $k \to \infty$

#### Matrix Series
Infinite series involving matrices:
- **Geometric series**: $(I - \alpha A)^{-1} = I + \alpha A + \alpha^2 A^2 + \ldots$
- **Convergence conditions**: When does the series converge?
- **Spectral radius**: Determines convergence: series converges if $|\alpha| < 1/\rho(A)$

### Spectral Properties

#### Perron-Frobenius Theorem
For non-negative matrices (like adjacency matrices):
- **Largest eigenvalue**: Is real and positive
- **Principal eigenvector**: Has all non-negative entries
- **Uniqueness**: Principal eigenvector is unique (up to scaling)
- **Dominance**: Largest eigenvalue strictly dominates others for irreducible matrices

#### Spectral Radius
- **Definition**: $\rho(A) = \max_i |\lambda_i|$ (magnitude of largest eigenvalue)
- **Significance**: Controls convergence of matrix powers and series
- **Computation**: Can be found using power iteration method

## Normalization Techniques

### Vector Normalization
Different ways to normalize vectors:
- **L1 norm**: $||v||_1 = \sum_i |v_i|$ (sum to 1 for probability distributions)
- **L2 norm**: $||v||_2 = \sqrt{\sum_i v_i^2}$ (unit length vectors)
- **Max norm**: $||v||_\infty = \max_i |v_i|$ (scale largest element to 1)

### Matrix Normalization
- **Row stochastic**: Each row sums to 1 (transition matrices)
- **Column stochastic**: Each column sums to 1  
- **Doubly stochastic**: Both rows and columns sum to 1

## Iterative Methods

### Power Iteration
Algorithm for finding largest eigenvalue and eigenvector:
1. Start with random vector $v^{(0)}$
2. Iterate: $v^{(k+1)} = \frac{Av^{(k)}}{||Av^{(k)}||}$
3. Converges to principal eigenvector

#### Convergence Rate
- Depends on ratio $|\lambda_2|/|\lambda_1|$
- Faster convergence when this ratio is small
- **Acceleration techniques**: Methods to improve convergence

### Matrix Decompositions

#### Similarity Transformations
- **Diagonalization**: $A = PDP^{-1}$ where $D$ is diagonal
- **Applications**: Computing matrix powers efficiently: $A^k = PD^kP^{-1}$

## Applications to Network Analysis

### Network Properties via Eigenvalues
- **Connectivity**: Related to eigenvalue gaps
- **Mixing time**: How quickly random walks converge
- **Expansion**: How well-connected different parts of the network are

### Computational Considerations
- **Sparse matrices**: Most real networks are sparse
- **Efficient algorithms**: Exploiting sparsity for large networks
- **Numerical stability**: Avoiding computational errors

These advanced linear algebra concepts provide the mathematical foundation for understanding how centrality measures capture different notions of node importance through matrix operations.
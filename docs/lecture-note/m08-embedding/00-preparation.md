# Preparation: Dimensionality Reduction and Optimization Prerequisites

## Required Knowledge from Previous Modules

Before studying network embedding, ensure you understand:
- **From M01-M07**: Network representations, linear algebra, eigenvalue theory, and Markov chain concepts
- **From M07**: Stationary distributions and spectral properties of random walks

## Matrix Decomposition Theory

### Singular Value Decomposition (SVD)
Essential decomposition for dimensionality reduction:
- **Definition**: For matrix $A$: $A = U \Sigma V^T$
- **Components**: $U$ (left singular vectors), $\Sigma$ (singular values), $V$ (right singular vectors)
- **Properties**: Provides optimal low-rank approximation in Frobenius norm
- **Truncated SVD**: Using only top-k singular values/vectors for compression

### Low-Rank Approximation
Mathematical foundation for embedding:
- **Frobenius norm**: $||A||_F = \sqrt{\sum_{ij} A_{ij}^2}$
- **Optimal approximation**: SVD minimizes $||A - A_k||_F$ for rank-k matrix $A_k$
- **Information preservation**: How much structure is retained in low dimensions

### Principal Component Analysis (PCA)
Classical dimensionality reduction technique:
- **Objective**: Find directions of maximum variance
- **Covariance matrix**: $C = \frac{1}{n-1}X^TX$ for centered data matrix $X$
- **Solution**: Eigenvectors of covariance matrix
- **Connection to SVD**: PCA eigenvectors are SVD right singular vectors

## Optimization Fundamentals

### Objective Functions
Understanding what we optimize in embedding:
- **Reconstruction error**: How well embeddings recreate original data
- **Preservation metrics**: Maintaining distances, similarities, or other properties
- **Regularization**: Preventing overfitting and ensuring generalization

### Gradient-Based Optimization
Essential for neural embedding methods:
- **Gradient descent**: $\theta_{t+1} = \theta_t - \alpha \nabla_\theta L(\theta_t)$
- **Stochastic gradient descent**: Using random samples for efficiency
- **Learning rate scheduling**: Adaptive step sizes
- **Convergence criteria**: When to stop optimization

### Constrained Optimization
For embedding problems with constraints:
- **Orthogonality constraints**: When embedding vectors must be orthogonal
- **Norm constraints**: Limiting embedding vector magnitudes
- **Lagrange multipliers**: Mathematical tool for handling constraints

## Distance and Similarity Measures

### Metric Properties
Understanding what makes a good distance measure:
- **Non-negativity**: $d(x,y) \geq 0$
- **Symmetry**: $d(x,y) = d(y,x)$
- **Triangle inequality**: $d(x,z) \leq d(x,y) + d(y,z)$
- **Identity**: $d(x,y) = 0$ if and only if $x = y$

### Common Distance Functions
- **Euclidean distance**: $||x - y||_2$
- **Cosine similarity**: $\frac{x \cdot y}{||x|| ||y||}$
- **Manhattan distance**: $||x - y||_1$
- **Jaccard similarity**: For set-based comparisons

### Embedding Quality Metrics
How to evaluate if embeddings preserve important properties:
- **Distance preservation**: Do similar nodes remain close?
- **Neighborhood preservation**: Are local structures maintained?
- **Global structure**: Are long-range relationships captured?

## High-Dimensional Data Analysis

### Curse of Dimensionality
Understanding challenges with high-dimensional spaces:
- **Distance concentration**: All points become equidistant in high dimensions
- **Sparsity**: High-dimensional spaces are mostly empty
- **Visualization challenges**: Difficulty interpreting high-dimensional data

### Manifold Learning
Assumption underlying many embedding methods:
- **Manifold hypothesis**: High-dimensional data lies on lower-dimensional manifolds
- **Local linearity**: Small neighborhoods can be approximated linearly
- **Intrinsic dimensionality**: True degrees of freedom in the data

## Computational Considerations

### Scalability Issues
Challenges with large networks:
- **Matrix operations**: O(n³) complexity for eigenvalue decomposition
- **Memory requirements**: Storing large adjacency matrices
- **Approximation methods**: Trading accuracy for computational efficiency

### Sparse Matrix Techniques
Essential for large network analysis:
- **Sparse storage**: Only storing non-zero entries
- **Iterative methods**: Lanczos algorithm for eigenvalues
- **Random sampling**: Approximating matrix operations

These mathematical foundations provide the theoretical basis for understanding how embedding methods transform high-dimensional network structures into meaningful low-dimensional representations.
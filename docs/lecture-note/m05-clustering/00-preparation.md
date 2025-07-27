# Preparation: Linear Algebra and Optimization Prerequisites

## Required Knowledge from Previous Modules

Before studying clustering methods, ensure you understand:
- **From M01-M04**: Basic network representations, degree distributions, and sampling bias concepts
- **Mathematical foundations**: Sampling theory and statistical bias from M04

## Linear Algebra Fundamentals

### Matrix Operations
Essential matrix operations for clustering algorithms:

#### Basic Operations
- **Matrix multiplication**: $C = AB$ where $C_{ij} = \sum_k A_{ik}B_{kj}$
- **Matrix transpose**: $(A^T)_{ij} = A_{ji}$
- **Identity matrix**: $I$ where $I_{ii} = 1$ and $I_{ij} = 0$ for $i \neq j$

#### Symmetric Matrices
- **Symmetric**: $A = A^T$ (important for undirected graphs)
- **Positive semidefinite**: All eigenvalues are non-negative
- **Spectral theorem**: Symmetric matrices can be diagonalized with real eigenvalues

### Eigenvalue Decomposition

#### Eigenvalue Problem
For matrix $M$ and vector $v$:
$$Mv = \lambda v$$
where $\lambda$ is an eigenvalue and $v$ is the corresponding eigenvector.

#### Key Properties
- **Orthogonality**: Eigenvectors of symmetric matrices are orthogonal
- **Real eigenvalues**: Symmetric matrices have real eigenvalues
- **Eigenvector basis**: Eigenvectors form a basis for the vector space

### Quadratic Forms
Expression $x^T M x$ for vector $x$ and matrix $M$:
- **Interpretation**: Measures how vector $x$ interacts with matrix $M$
- **Optimization**: Many clustering problems minimize quadratic forms
- **Geometric meaning**: Related to distances and similarities

## Optimization Prerequisites

### Constrained Optimization
Basic understanding of optimization with constraints:
- **Objective function**: What we want to minimize or maximize
- **Constraints**: Restrictions on feasible solutions
- **Lagrange multipliers**: Method for handling equality constraints

### Relaxation Techniques
- **Discrete vs. continuous**: Converting integer problems to real-valued problems
- **Approximation quality**: Understanding when relaxations provide good solutions

## Graph Theory Prerequisites

### Cut Problems
Understanding graph partitioning:
- **Cut**: Set of edges between two groups of nodes
- **Minimum cut**: Finding the smallest cut between node groups
- **Balanced cuts**: Ensuring groups are roughly equal in size

### Spectral Graph Theory Basics
- **Graph spectrum**: Set of eigenvalues of graph matrices
- **Connectivity and eigenvalues**: How eigenvalues relate to graph structure
- **Fiedler vector**: Second smallest eigenvector and its clustering properties

## Computational Prerequisites

### Algorithm Analysis
- **Time complexity**: Understanding O(n²), O(n³) for matrix operations
- **Space complexity**: Memory requirements for large matrices
- **Numerical stability**: Issues with floating-point computations

### Data Structures
- **Sparse matrices**: Efficient storage for large, sparse adjacency matrices
- **Priority queues**: For optimization algorithms

These mathematical foundations are essential for understanding how clustering algorithms transform network structure problems into linear algebra problems that can be solved efficiently.
# Module 06 Preparation: Community Detection and Matrix Operations

## Review from Module 5: Community Detection

### What is community?

**Communities** in networks are groups of nodes that share similar connection patterns. These communities do not always mean densely-connected nodes. Sometimes, a community can be nodes that are not connected to each other, but connect similarly to other groups.

Communities reflect underlying mechanisms of network formation and underpin the dynamics of information propagation. Examples include:

1. **Homophily**: The tendency of similar nodes to form connections.
2. **Functional groups**: Nodes that collaborate for specific purposes.
3. **Hierarchical structure**: Smaller communities existing within larger ones.
4. **Information flow**: The patterns of information, influence, or disease propagation through the network.

### Modularity

**Modularity** is by far the most widely used method for community detection. Modularity measures assortativity *relative* to *a null model*.

**Assortativity** is a measure of the tendency of nodes to connect with nodes of the same attribute. The attribute, in our case, is the community that the node belongs to, and we say that a network is assortative if nodes of the same community are more likely to connect with each other than nodes of different communities.

Unlike graph cut methods that aim to maximize assortativity directly, modularity measures assortativity relative to a null model by comparing our original network to a "random" version where we mix up all the connections.

### Stochastic Block Model

The **Stochastic Block Model (SBM)** flips the idea of modularity maximization on its head! Instead of starting with a network and looking for communities, we start with the communities and ask, *"What kind of network would we get if the nodes form these communities?"*.

In stochastic block model, we describe a network using probabilities given a community structure. Specifically, let us consider two nodes $i$ and $j$ who belong to community $c_i$ and $c_j$. Then, the probability of an edge between $i$ and $j$ is given by their community membership:

$$
P(A_{ij}=1|c_i, c_j) = p_{c_i,c_j}
$$

where $p_{c_i,c_j}$ is the probability of an edge between nodes in community $c_i$ and $c_j$, respectively.

## Essential Matrix Operations for Centrality

### Adjacency Matrix Fundamentals

The **adjacency matrix** $A$ is the foundation for most centrality calculations:
- $A_{ij} = 1$ if there is an edge between nodes $i$ and $j$
- $A_{ij} = 0$ otherwise
- For undirected networks: $A_{ij} = A_{ji}$ (symmetric matrix)

### Key Matrix Operations

#### Matrix Powers
Powers of the adjacency matrix reveal important network properties:
- $A^2_{ij}$ = number of walks of length 2 between nodes $i$ and $j$
- $A^k_{ij}$ = number of walks of length $k$ between nodes $i$ and $j$

#### Eigenvalues and Eigenvectors
For a matrix $A$ and vector $v$:
$$Av = \lambda v$$
where $\lambda$ is an eigenvalue and $v$ is the corresponding eigenvector.

**Key properties:**
- The **largest eigenvalue** $\lambda_1$ (spectral radius) determines many network properties
- The **principal eigenvector** $v_1$ (corresponding to $\lambda_1$) forms the basis of eigenvector centrality
- For connected networks, $\lambda_1 > 0$ and $v_1$ has all positive entries

#### Matrix Norms
The **matrix norm** measures the "size" of a matrix:
- **Spectral norm**: $||A||_2 = \lambda_1$ (largest eigenvalue)
- Used in normalizing centrality measures

#### Matrix Inversion and Pseudo-inverse
- **Matrix inverse** $A^{-1}$: exists only for square, non-singular matrices
- **Moore-Penrose pseudo-inverse** $A^+$: generalization for any matrix
- Used in advanced centrality measures like Katz centrality

### Connection to Centrality

These matrix operations directly connect to centrality measures we'll study:

1. **Degree centrality**: Uses row/column sums of $A$
2. **Eigenvector centrality**: Uses the principal eigenvector of $A$
3. **Katz centrality**: Uses matrix series $(I - \alpha A)^{-1}$
4. **PageRank**: Uses modified adjacency matrix with damping

Understanding these matrix fundamentals will be crucial as we explore how different centrality measures capture different aspects of node importance in networks.
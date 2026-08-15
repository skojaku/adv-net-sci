# Module 06: Centrality - Core Concepts

## What is Centrality?

**Centrality** measures the importance of a node in a network. The concept of "importance" is context-dependent, and different situations call for different centrality measures. The core question is: in what sense is a node important?

## Degree-Based Centrality

### Degree Centrality
The simplest centrality measure is to count a node's direct connections (its degree).

$$
c_i = d_i = \sum_{j} A_{ij}
$$

**Interpretation**: A node is important if it has many direct connections.
**Applications**: Useful for understanding immediate influence, social popularity, and viral spread.

## Distance-Based Centrality

This family of measures is inspired by the Roman *Milliarium Aureum* (Golden Milestone), the central point from which all distances were measured in the Roman Empire. A node is considered central if it is "close" to other nodes.

### Closeness Centrality
Measures how close a node is to all other nodes in the network on average.

$$
c_i = \frac{N - 1}{\sum_{j=1}^N d(i,j)}
$$

where $d(i,j)$ is the shortest path length from node $i$ to node $j$.

**Interpretation**: A node is important if it can reach other nodes quickly.
**Limitation**: Fails in disconnected networks, as infinite distances make the centrality zero for all nodes in smaller components.

### Harmonic Centrality
An adjustment to closeness centrality that works for disconnected networks.

$$
c_i = \sum_{j \neq i} \frac{1}{d(i,j)}
$$

**Advantage**: Infinite distances contribute zero to the sum, making it robust for disconnected graphs.

### Eccentricity Centrality
Measures a node's importance based on the longest shortest path from it to any other node.

$$
c_i = \frac{1}{\max_{j} d(i,j)}
$$

**Interpretation**: A node is important if its maximum distance to any other node is small. It optimizes for the worst-case scenario, making it useful for placing emergency services or distribution centers.

### Betweenness Centrality
Measures how often a node lies on the shortest paths between other pairs of nodes.

$$
c_i = \sum_{j < k} \frac{\sigma_{jk}(i)}{\sigma_{jk}}
$$

where:
- $\sigma_{jk}$ is the total number of shortest paths between nodes $j$ and $k$.
- $\sigma_{jk}(i)$ is the number of those paths that pass through node $i$.

**Interpretation**: A node is important if it acts as a "bridge" and controls the flow of information or resources.

## Walk-Based Centrality

This family of measures is based on the idea that "a man is known by the company he keeps." A node's importance is determined by the importance of its neighbors.

### Eigenvector Centrality
A node is important if it is connected to other important nodes. This circular definition is resolved using linear algebra.

$$
\lambda c_i = \sum_{j} A_{ij} c_j \quad \text{or in matrix form,} \quad \lambda \mathbf{c} = \mathbf{A} \mathbf{c}
$$

The solution, $\mathbf{c}$, is the eigenvector of the adjacency matrix $\mathbf{A}$ corresponding to the largest eigenvalue, $\lambda$. The Perron-Frobenius theorem guarantees this eigenvector is unique and has all positive entries.

**Interpretation**: Captures influence that extends beyond direct connections.

### Katz Centrality
Extends eigenvector centrality by giving each node a small amount of base centrality, $\beta$. This helps address limitations where eigenvector centrality can over-emphasize a few well-connected nodes.

$$
c_i = \beta + \lambda \sum_{j} A_{ij} c_j \quad \text{or in matrix form,} \quad \mathbf{c} = \beta \mathbf{1} + \lambda \mathbf{A} \mathbf{c}
$$

The solution can be found by solving the linear system:
$$
\mathbf{c} = \beta (\mathbf{I} - \lambda \mathbf{A})^{-1} \mathbf{1}
$$

**Interpretation**: Measures influence by counting all walks, with shorter walks weighted more heavily.

### HITS (Hyperlink-Induced Topic Search)
Designed for directed networks, HITS distinguishes between two types of importance:
- **Authority**: A node is a good authority if it is pointed to by many good hubs.
- **Hub**: A node is a good hub if it points to many good authorities.

$$
\mathbf{x} = \lambda_x \mathbf{A}^T \mathbf{y} \quad (\text{Hubs})
$$
$$
\mathbf{y} = \lambda_y \mathbf{A} \mathbf{x} \quad (\text{Authorities})
$$

These equations can be solved by finding the principal eigenvectors of $\mathbf{A}^T\mathbf{A}$ for hubs and $\mathbf{A}\mathbf{A}^T$ for authorities.

**Applications**: Web search, identifying influential papers in citation networks.

### PageRank
The algorithm that powered Google Search. It simulates a random walker on the network. A node is important if it is likely to be visited.

$$
c_i = (1-\beta) \sum_j A_{ji}\frac{c_j}{d^{\text{out}}_j} + \beta \cdot \frac{1}{N}
$$

The formula has two parts:
1.  **Random walk from neighbors**: A node receives a share of its neighbors' importance.
2.  **Teleportation**: With probability $\beta$, the walker jumps to a random node in the network. This ensures the walk doesn't get stuck in dead ends.

**Interpretation**: A node is important if many important pages link to it.

### Personalized PageRank
Extends PageRank by making the "teleportation" step biased towards a specific starting node or set of nodes.

$$
c_i = (1-\beta) \sum_j A_{ji}\frac{c_j}{d^{\text{out}}_j} + \beta \cdot p_{\ell}
$$

where $p_{\ell}$ is a vector that is 1 for the starting node $\ell$ and 0 otherwise. Instead of jumping to any random node, the walker jumps back to the starting node $\ell$.

**Interpretation**: Ranks nodes based on their proximity to a specific "focal" node, making it ideal for personalized recommendations (e.g., "find movies similar to this one").

## Choosing the Right Centrality

### Context-Dependent Selection

| Goal                     | Recommended Centrality                               |
| ------------------------ | ---------------------------------------------------- |
| **Find popular nodes**   | Degree                                               |
| **Find efficient nodes** | Closeness, Harmonic                                  |
| **Find critical nodes**  | Betweenness, Eccentricity                            |
| **Find influential nodes** | Eigenvector, PageRank, Katz                          |
| **Personalized search**  | Personalized PageRank                                |

### Computational Considerations

| Centrality  | Time Complexity       | Notes                               |
| ----------- | --------------------- | ----------------------------------- |
| Degree      | $O(m)$                | Very fast.                          |
| Closeness   | $O(nm)$               | Moderate, requires all-pairs paths. |
| Betweenness | $O(nm)$               | Can be slow on large, dense graphs. |
| Eigenvector | Iterative             | Moderate, depends on convergence.   |

## Centrality Correlations

Centrality measures are often correlated, but the strength of the correlation depends on the network's structure.
- **Degree** and **Eigenvector** centrality are often strongly correlated.
- In a **star network**, the central node dominates Degree and Betweenness scores.
- In a **path network**, Betweenness peaks in the middle, while Degree is uniform (except at the ends).

## Applications and Implications

- **Network Robustness**: Identify critical nodes to protect or target.
- **Epidemic Modeling**: Find super-spreaders and optimal vaccination targets.
- **Social Dynamics**: Uncover leaders, influencers, and bridges between communities.
- **Economic Networks**: Detect systemic risks and supply chain vulnerabilities.
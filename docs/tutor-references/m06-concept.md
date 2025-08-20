# Module 06: Centrality - Core Concepts

## What is Centrality?

**Centrality** measures node importance in a network. The concept of "importance" is context-dependent - different situations require different centrality measures.

Key question: In what sense is a node important?

## Degree-Based Centrality

### Degree Centrality
The simplest centrality measure: count direct connections.

```
c_i = d_i = Σⱼ A_ij
```

**Interpretation**: Nodes with many direct connections are most important.

**Applications**: Social influence, viral spread, immediate reach.

## Distance-Based Centrality

Inspired by the Roman *Milliarium Aureum* (Golden Milestone) - the central point from which all distances were measured in the Roman Empire.

### Closeness Centrality
Measures how close a node is to all other nodes.

```
c_i = (N-1) / Σⱼ d(i,j)
```

Where d(i,j) is shortest path length from i to j.

**Interpretation**: Nodes that can reach others quickly are most important.

### Harmonic Centrality  
Handles disconnected networks by using reciprocal distances.

```
c_i = Σⱼ≠ᵢ 1/d(i,j)
```

**Advantage**: Works even when network is disconnected.

### Eccentricity Centrality
Based on the farthest distance from a node.

```
c_i = 1/max_j d(i,j)
```

**Interpretation**: Nodes with small maximum distances are most central.

### Betweenness Centrality
Measures how often a node lies on shortest paths between other nodes.

```
c_i = Σⱼ<ₖ σⱼₖ(i)/σⱼₖ
```

Where:
- σⱼₖ = number of shortest paths between j and k
- σⱼₖ(i) = number of those paths passing through i

**Interpretation**: Nodes controlling information flow are most important.

## Walk-Based Centrality

Based on Aesop's principle: "A man is known by the company he keeps."

### Eigenvector Centrality
A node is important if connected to other important nodes.

```
c_i = λ Σⱼ A_ij c_j
```

**Circular definition** resolved through eigenvalue decomposition:
- **λ** = largest eigenvalue of adjacency matrix
- **c** = corresponding eigenvector

**Interpretation**: Importance comes from connections to other important nodes.

### PageRank
Google's famous algorithm, adding damping factor to eigenvector centrality.

```
PR(i) = (1-d)/N + d Σⱼ PR(j)/L(j)
```

Where:
- d = damping parameter (typically 0.85)
- L(j) = number of outbound links from j
- N = total number of nodes

**Interpretation**: Importance with random jump probability.

### Katz Centrality
Weighted sum of all walks starting from a node.

```
c_i = Σₖ₌₁^∞ Σⱼ αᵏ(Aᵏ)ⱼᵢ
```

Where α < 1/λ₁ (largest eigenvalue) for convergence.

**Interpretation**: More walks leading to a node = higher centrality.

### HITS Algorithm
Separates **authorities** (pointed to) from **hubs** (pointing to authorities).

**Authority score**: 
```
a_i = Σⱼ A_ji h_j
```

**Hub score**:
```
h_i = Σⱼ A_ij a_j
```

**Applications**: Web search, citation analysis.

## Random Walk Centrality

### Random Walk Betweenness
Expected number of times a random walk passes through a node.

### Current Flow Betweenness  
Based on electrical current flow through network resistors.

**Advantage**: Considers all paths, not just shortest paths.

## Choosing the Right Centrality

### Context-Dependent Selection

**Information Spread**:
- Initial spread: Degree centrality
- Efficient broadcast: Closeness centrality
- Control bottlenecks: Betweenness centrality

**Social Networks**:
- Popular individuals: Degree centrality
- Opinion leaders: Eigenvector centrality
- Bridges between groups: Betweenness centrality

**Infrastructure**:
- Critical failures: Betweenness centrality
- Service efficiency: Closeness centrality
- Load distribution: Random walk centrality

### Computational Considerations

**Time Complexity**:
- Degree: O(m) - very fast
- Closeness: O(nm) - moderate for small networks
- Betweenness: O(nm + n²log n) - slow for large networks
- Eigenvector: O(n³) or iterative methods - moderate

**Memory Requirements**:
- Degree: O(n) - minimal
- Distance-based: O(n²) - all-pairs distances
- Walk-based: O(n) - iterative computation

## Centrality Correlations

### Positive Correlations
- Degree and eigenvector centrality (usually strong)
- Closeness and betweenness (in many networks)

### Network-Dependent Patterns
- **Star networks**: Degree = betweenness at center
- **Path networks**: Betweenness peaks at center, degree uniform
- **Clique networks**: All centralities nearly equal

## Applications and Implications

### Network Robustness
- Target high-centrality nodes for maximum disruption
- Protect high-centrality nodes for resilience

### Epidemic Modeling
- Patient zero identification
- Vaccination strategies
- Containment protocols

### Social Dynamics
- Leadership emergence
- Innovation diffusion  
- Social capital measurement

### Economic Networks
- Systemic risk identification
- Supply chain vulnerabilities
- Financial contagion pathways
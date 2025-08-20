# Module 07: Random Walks - Core Concepts

## What Are Random Walks?

A **random walk** on a network is a stochastic process where a walker moves from node to node by randomly selecting among available edges. At each step, the walker chooses one of the current node's neighbors with some probability (often uniform).

### Basic Process
1. Start at a node
2. Move to a randomly chosen neighbor
3. Repeat indefinitely

### Mathematical Foundation
**Transition probability**: P(i→j) = A_ij / k_i
- A_ij = 1 if nodes i,j are connected, 0 otherwise  
- k_i = degree of node i

## The Markov Property

Random walks are **Markov processes**: the next step depends only on the current position, not the path history.

**Transition matrix**: T_ij = probability of moving from i to j
- Row-stochastic: each row sums to 1
- T_ij = A_ij / k_i for simple random walks

## Stationary Distribution

### Definition
The **stationary distribution** π satisfies: π = πT

In steady state, the probability of being at each node remains constant.

### For Simple Random Walks
π_i = k_i / (2m)

Where:
- k_i = degree of node i
- m = total number of edges

**Key insight**: Stationary probability is proportional to degree - high-degree nodes are visited more often.

## Types of Random Walks

### Simple Random Walk
- Uniform probability among neighbors
- Most basic form

### Biased Random Walks
- **Degree-biased**: Higher probability to high-degree neighbors
- **Distance-biased**: Preference based on previous step
- **Attribute-biased**: Based on node features

### Random Walks with Restart
- With probability α, restart at original node
- With probability (1-α), continue random walk
- Used in PageRank algorithm

### Self-Avoiding Random Walks
- Cannot revisit already visited nodes
- More complex but useful for certain applications

## Key Properties

### Mixing Time
Time required to reach stationary distribution from any starting point.

**Fast mixing**: Networks where random walks quickly forget starting position
**Slow mixing**: Networks with bottlenecks or strong community structure

### Return Probability
Probability of returning to starting node after t steps.

**Expected return time** for node i: 1/π_i = 2m/k_i

### Cover Time
Expected time to visit all nodes at least once.

## Applications of Random Walks

### Centrality Measures

**Random Walk Betweenness**: Expected number of times a random walk passes through a node

**Random Walk Closeness**: Based on expected hitting times between nodes

### Community Detection
- **Infomap**: Uses random walk compression to find communities
- **Walktrap**: Exploits the tendency of random walks to stay within communities

### Recommendation Systems
- Random walks on user-item bipartite graphs
- Collaborative filtering through walk-based similarity

### Web Search
- **PageRank**: Random walks with restart on web graphs
- Link analysis and authority ranking

## Mathematical Analysis

### Hitting Times
**Hitting time** h_ij: Expected number of steps to reach j starting from i

**Commute time**: h_ij + h_ji (round trip time)

### Resistance Distance
Connection to electrical networks: random walk hitting times relate to effective resistance between nodes.

### Spectral Properties
Random walk properties connect to graph Laplacian eigenvalues:
- **Mixing time**: Related to spectral gap (difference between largest and second-largest eigenvalues)
- **Return probabilities**: Expressed through spectral decomposition

## Random Walks on Different Network Types

### Regular Networks
- Uniform stationary distribution
- Predictable mixing behavior
- Symmetric hitting times

### Scale-Free Networks  
- High-degree hubs dominate stationary distribution
- Fast mixing due to hub connectivity
- Asymmetric hitting times

### Small-World Networks
- Faster mixing than regular lattices
- Long-range connections accelerate exploration
- Balanced local and global exploration

### Community Networks
- Slow mixing between communities
- Random walks get "trapped" within communities
- Useful for community detection algorithms

## Extensions and Variants

### Multiple Random Walkers
- Multiple simultaneous walks
- Collision and interaction models
- Parallel exploration strategies

### Random Walks on Directed Networks
- Asymmetric transition probabilities
- Different in-degree and out-degree effects
- Teleportation for handling dead ends

### Temporal Random Walks
- Networks changing over time
- Time-dependent transition probabilities
- Non-stationary processes

### Random Walks on Multilayer Networks
- Walks across different network layers
- Inter-layer transition probabilities
- Complex system modeling

## Computational Aspects

### Simulation Methods
- Monte Carlo simulation for individual walks
- Matrix powers for multi-step probabilities
- Iterative methods for stationary distributions

### Convergence Detection
- Total variation distance to stationarity
- Mixing time estimation
- Convergence diagnostics

### Scalability
- Sparse matrix operations for large networks
- Approximation methods for very large systems
- Parallel and distributed algorithms

## Connection to Other Network Concepts

### Unifying Framework
Random walks provide a unifying perspective connecting:
- **Centrality measures**: Walk-based importance
- **Community structure**: Trapping and escape dynamics  
- **Network distances**: Effective resistance and commute times
- **Spreading processes**: Diffusion and epidemic models

This makes random walks one of the most versatile tools in network analysis.
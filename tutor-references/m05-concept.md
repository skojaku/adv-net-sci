# Module 05: Clustering/Community Detection - Core Concepts

## Understanding Communities in Networks

**Community structure** refers to groups of nodes that share similar connection patterns. Communities represent the tendency of nodes to form clusters based on:

1. **Homophily**: Similar nodes forming connections
2. **Functional groups**: Nodes collaborating for specific purposes  
3. **Hierarchical structure**: Nested community organization
4. **Information flow patterns**: Shared pathways for propagation

Communities don't always mean densely connected groups - they can be nodes with similar connection patterns to other groups.

## Pattern Matching Approach

### Cliques: The Strictest Communities
A **clique** is a group of nodes all connected to each other (complete subgraph).
- Examples: triangles (3-cliques), fully-connected squares (4-cliques)
- **Problem**: Too rigid for real-world networks

### Pseudo-Cliques: Relaxed Community Definitions

**Relaxing degree requirements**:
- **k-plex**: Each node connects to all but k others in the group
- **k-core**: Each node connects to at least k others in the group

**Relaxing density requirements**:
- **ρ-dense subgraphs**: Minimum edge density of ρ

**Relaxing distance requirements**:
- **n-clique**: All nodes within n steps of each other

**Combined approaches**:
- **k-truss**: All edges participate in at least k-2 triangles
- **n-clan** and **n-club**: Distance and diameter constraints

## Graph Cut Optimization Approach

Transform community detection into an **optimization problem**:

```
Cut(V₁, V₂) = Σᵢ∈V₁ Σⱼ∈V₂ Aᵢⱼ
```

**Goal**: Minimize edges between communities (minimize cut)

**Problem**: Without constraints, trivial solution is one giant community
**Solution**: Require each community to have minimum size

## Modularity: The Gold Standard

**Modularity** measures community quality by comparing actual connections within communities to expected connections in a random graph.

### Key Concepts

**Assortativity**: Tendency of similar nodes to connect
**Null model**: Random graph with same degree sequence
**Modularity score**: Actual internal connections - Expected internal connections

### Mathematical Formulation
```
Q = (1/2m) Σᵢⱼ [Aᵢⱼ - (kᵢkⱼ/2m)] δ(cᵢ, cⱼ)
```

Where:
- m = total number of edges
- Aᵢⱼ = adjacency matrix
- kᵢ = degree of node i  
- δ(cᵢ, cⱼ) = 1 if nodes i,j in same community, 0 otherwise

### Properties
- **Range**: [-1, 1]
- **Higher values**: Better community structure
- **Q > 0.3**: Often considered significant community structure
- **Optimization**: NP-hard problem

## Community Detection Algorithms

### Modularity Optimization
- **Greedy algorithms**: Local modularity improvements
- **Louvain algorithm**: Hierarchical modularity optimization
- **Leiden algorithm**: Improved version addressing Louvain limitations

### Other Approaches
- **Label propagation**: Nodes adopt majority label of neighbors
- **Spectral methods**: Use graph Laplacian eigenstructure
- **Stochastic block models**: Generative probabilistic approach
- **Random walks**: Community detection via diffusion processes

## Limitations and Challenges

### Resolution Limit
Modularity optimization has **resolution limit**: cannot detect communities smaller than certain size, even if they're well-defined.

### Degeneracy Problem
Many different community structures can have similar (near-optimal) modularity scores, leading to instability.

### Null Model Assumptions
Configuration model assumptions may not match real network formation processes.

### Parameter Selection
Many algorithms require parameter tuning (resolution, number of communities, etc.)

## Evaluation Metrics

### Internal Measures (No Ground Truth)
- **Modularity**: Most common quality measure
- **Conductance**: Measures community isolation
- **Density**: Internal vs. external edge ratios

### External Measures (With Ground Truth)
- **Normalized Mutual Information (NMI)**: Information-theoretic similarity
- **Adjusted Rand Index (ARI)**: Corrected for chance agreement
- **F1-score**: Precision-recall trade-off

## Applications

### Social Networks
- Friend groups, interest communities
- Echo chambers, political polarization
- Viral marketing, influence propagation

### Biological Networks  
- Protein complexes, metabolic pathways
- Disease modules, drug target identification
- Brain network modules

### Infrastructure Networks
- Internet autonomous systems
- Transportation hub clusters
- Power grid control areas

### Information Networks
- Citation communities, research fields
- Web page clusters, topic groups
- Recommendation system user segments
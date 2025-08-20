# Module 04: Node Degree - Core Concepts

## The Fundamental Concept: Node Degree

**Node degree** is the number of edges connected to a node - the most basic yet powerful measure in network analysis. While simple to define, degree reveals network structure and drives many collective behaviors.

### Individual vs. Network Level
- **Individual level**: Degree measures visibility and influence - high-degree nodes spread information quickly
- **Network level**: The collection of degrees (degree distribution) reveals centralization patterns

## Degree Distribution

The **degree distribution** shows the fraction of nodes with each degree value. It answers: "How common is each degree?"

### Why It Matters
Degree distribution shapes network behavior:
- **Robustness**: Heavy-tailed distributions tolerate random failures but are vulnerable to targeted hub attacks
- **Small-world effects**: Hub-dominated distributions create shortcuts that reduce path lengths
- **Spreading processes**: High-degree nodes accelerate information/disease transmission

## The Friendship Paradox

**Statement**: "Your friends have more friends than you do, on average"

This is not an insult but a mathematical consequence discovered by Scott Feld (1991).

### Mechanism
- High-degree nodes (popular people) are more likely to be counted as friends
- Low-degree nodes are less likely to be referenced
- Creates **sampling bias** where average degree of friends exceeds your own degree

### Mathematical Formulation
For any node i with degree k_i and neighbors j:
```
Average degree of i's friends = Σ(k_j) / k_i
```

This typically exceeds both:
- Node i's own degree (k_i)
- Network's average degree

### Example
Simple 4-node network:
- Bob (degree 3): connected to Alex, Carol, David (all degree 1)
- Alex, Carol, David (degree 1): each connected only to Bob (degree 3)
- Network average degree: 1.5
- Average friend degree: 2.25

## Degree Bias and Its Implications

### Sampling Bias
When sampling nodes through their connections (neighbor sampling):
- High-degree nodes are overrepresented
- Low-degree nodes are underrepresented
- Leads to biased estimates of network properties

### Practical Applications

#### Public Health
- **Early detection**: Monitor high-degree individuals for disease outbreaks
- **Intervention strategies**: Vaccinate social hubs for maximum impact
- **Contact tracing**: Focus on nodes with many connections

#### Social Networks
- **Influence maximization**: Target high-degree users for viral marketing
- **Information spread**: Understand how news/rumors propagate
- **Network effects**: Explain why people perceive trends as more popular than they are

#### Infrastructure
- **Robustness planning**: Protect critical high-degree nodes
- **Attack strategies**: Target hubs for maximum network disruption
- **Resource allocation**: Prioritize maintenance of critical connection points

## Degree-Based Network Classification

### Types of Degree Distributions

#### Random Networks (Poisson)
- Most nodes have similar degrees around the mean
- Few very high or very low degree nodes
- Bell-curve-like distribution

#### Scale-Free Networks (Power-law)
- Heavy-tailed distribution: P(k) ~ k^(-γ)
- Many low-degree nodes, few high-degree hubs
- No characteristic scale

#### Regular Networks
- All nodes have identical or very similar degrees
- Narrow degree distribution
- Common in lattices and grid structures

## Mathematical Properties

### Degree Sum Formula
For any network: Σ(degrees) = 2 × (number of edges)

### Handshaking Lemma
In any network, the number of nodes with odd degree is even.

### Degree Correlations
- **Assortative**: High-degree nodes connect to other high-degree nodes
- **Disassortative**: High-degree nodes connect to low-degree nodes
- **Neutral**: No degree correlation

These correlation patterns affect network resilience, spreading dynamics, and structural properties.
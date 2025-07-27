# M04 Preparation: Prerequisites and Foundation

## Review: Network Robustness (from M03)

Before diving into the friendship paradox, let's review key concepts from M03 that will be relevant:

### Minimum Spanning Tree
- **Definition**: A tree that connects all vertices in a graph with the minimum total edge weight
- **Algorithms**: 
  - Kruskal's algorithm: Build MST by adding edges in order of increasing weight
  - Prim's algorithm: Build MST by growing from a starting vertex
- **Applications**: Network connectivity, infrastructure design

### Network Robustness
- **Random attacks**: Removing nodes/edges randomly
- **Targeted attacks**: Removing highest-degree nodes first
- **Robustness index**: Measures how well a network maintains connectivity under attacks
- **Key insight**: Scale-free networks are robust to random failures but vulnerable to targeted attacks

## Probability Theory Basics

The friendship paradox relies on fundamental probability concepts:

### Expected Value
For a discrete random variable X:
$$E[X] = \sum_{i} x_i P(X = x_i)$$

### Sampling Bias
- **Population vs. Sample**: What we measure may not represent the true population
- **Selection bias**: Some individuals are more likely to be selected than others
- **Example**: Airport surveys overrepresent frequent travelers

### Degree Distribution
In networks, the degree distribution P(k) gives the probability that a randomly chosen node has degree k:
- **Mean degree**: $\langle k \rangle = \sum_{k} k P(k)$
- **Degree variance**: Important for understanding network structure

### Weighted Sampling
When sampling is not uniform:
- Probability of selecting node i is proportional to some weight w_i
- Expected degree under degree-weighted sampling differs from uniform sampling
- This is the mathematical foundation of the friendship paradox

## Connection to Friendship Paradox

These concepts prepare us to understand:
1. Why your friends have more friends than you (on average)
2. How sampling bias creates this apparent paradox
3. Applications in epidemiology and social network analysis
4. The role of degree heterogeneity in network phenomena

## Learning Objectives

By the end of this module, you should be able to:
- Explain the friendship paradox mathematically
- Identify when and why the paradox occurs
- Apply the concept to vaccination strategies
- Calculate expected degrees under different sampling schemes
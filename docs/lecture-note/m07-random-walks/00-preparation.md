# Preparation: From Centrality to Random Walks

## Overview

Before diving into random walks, let's review the key concepts from Module 6 (Centrality) that will form the foundation for understanding how random walks relate to network structure and centrality measures.

## Review: Eigenvector Centrality and Spectral Methods

### Eigenvector Centrality

"A man is known by the company he keeps" is a quote from Aesop who lived in the ancient Greece, a further back in time from the Roman Empire.
It suggests that a person's character is reflected by the people this person is friends with.
This idea can be applied to define the *centrality* of a node in a network.

One considers that a node is important if it is connected to other important nodes. Yes, it sounds like circular! But it is actually computable! Let us define it more precisely by the following equation.

$$
c_i = \lambda \sum_{j} A_{ij} c_j
$$

where $\lambda$ is a constant. It suggests that the centrality of a node ($c_i$) is the sum of the centralities of its neighbors ($A_{ij} c_j$; note that $A_{ij}=1$ if $j$ is a neighbor, and otherwise $A_{ij}=0$), normalized by $\lambda$.

Using vector notation, we can rewrite the equation as:

$$
\mathbf{c} = \lambda \mathbf{A} \mathbf{c}
$$

This is actually the eigenvector equation! The solution is the eigenvector of the adjacency matrix, $\mathbf{A}$. We choose the eigenvector associated with the largest eigenvalue, which by the Perron-Frobenius theorem guarantees that all elements are positive.

### PageRank

PageRank, the celebrated idea behind Google Search, is like a cousin of Katz centrality:

$$
c_i = (1-\beta) \sum_j A_{ji}\frac{c_j}{d^{\text{out}}_j} + \beta \cdot \frac{1}{N}
$$

where $d^{\text{out}}_j$ is the out-degree of node $j$. The term $c_j/d^{\text{out}}_j$ represents that the score of node $j$ is divided by the number of nodes to which node $j$ points. This is based on an idea of traffic, where viewers of a web page are evenly transferred to the linked web pages.

## Introduction to Markov Chains

### What is a Markov Chain?

A Markov chain is a mathematical system that experiences transitions from one state to another according to certain probabilistic rules. The defining property is that the next state depends only on the current state, not on the sequence of events that preceded it. This is called the **Markov property** or "memorylessness."

### Key Components

1. **State Space**: A set of possible states $S = \{1, 2, ..., n\}$
2. **Transition Matrix**: A matrix $P$ where $P_{ij}$ is the probability of transitioning from state $i$ to state $j$
3. **Initial Distribution**: The probability distribution over states at time $t=0$

### Transition Matrix Properties

For a valid transition matrix:
- All entries are non-negative: $P_{ij} \geq 0$
- Each row sums to 1: $\sum_j P_{ij} = 1$ (stochastic matrix)

### Stationary Distribution

A key concept is the **stationary distribution** $\pi$, which satisfies:

$$
\pi = \pi P
$$

This means that if the system reaches the stationary distribution, it will remain in that distribution over time. The stationary distribution is the left eigenvector of the transition matrix corresponding to eigenvalue 1.

### Connection to Random Walks

Random walks on networks are a special case of Markov chains where:
- **States** are the nodes of the network
- **Transitions** follow the edges of the network
- **Transition probabilities** are typically uniform among neighbors

For an unweighted, undirected network, the transition probability from node $i$ to node $j$ is:

$$
P_{ij} = \frac{A_{ij}}{d_i}
$$

where $d_i$ is the degree of node $i$.

### Why This Matters for Random Walks

The concepts from eigenvector centrality and Markov chains come together in random walks:

1. **PageRank** is actually the stationary distribution of a specific random walk on the network
2. **Eigenvector centrality** relates to the stationary distribution of random walks on undirected networks
3. The **transition matrix** of a random walk encodes the local structure of the network
4. The **long-term behavior** of random walks reveals global network properties

This foundation will help us understand how random walks can unify concepts of centrality and community detection in the following sections.
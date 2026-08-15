---
marp: true
theme: default
paginate: true
size: 4:3
---

The city planning department of Smalltown is analyzing its bridge system. The town has 5 distinct areas connected by bridges, where:
- Area A connects to B with 2 bridges
- Area B connects to C with 3 bridges
- Area C connects to D with 1 bridge
- Area D connects to E with 2 bridges
- Area E connects to A with 2 bridges


Based on Euler's theorem, which statement is correct about the possibility of creating a walking tour that crosses each bridge exactly once?

---

Given the following Python code for representing a network:

```python
edges = [(0,1), (0,2), (1,2), (1,3), (2,3)]
import numpy as np
A = np.zeros((4, 4))
for i, j in edges:
    A[i][j] += 1
    A[j][i] += 1
```

What is the degree of node 1 in this network?

---

A social network researcher is analyzing a small community where each person is represented by a node and friendships by edges. They've created this adjacency matrix:

```python
A = [[0, 1, 0, 1],
     [1, 0, 1, 1],
     [0, 1, 0, 1],
     [1, 1, 1, 0]]
```

What is the total number of unique friendships (edges) in this network?

---

In the context of network representation, which of the following correctly describes the relationship between edge lists and adjacency matrices?

---

Given the following Python code to analyze a walking trail system:

```python
def can_complete_trail(edges):
    A = np.zeros((4, 4))
    for i, j in edges:
        A[i][j] += 1
        A[j][i] += 1
    deg = np.sum(A, axis=1)
    odd_count = np.sum(deg % 2)
    return odd_count in [0, 2]
```

Which modification would make this function correctly handle a directed trail system (where trails can only be walked in one direction)?

---

In analyzing the bridges of Königsberg, which statement correctly describes Euler's approach to solving the puzzle?

---

A network analysis student needs to store a large social network with 100,000 nodes where most nodes are connected to only a few others. Which data structure would be least efficient?

---


In a directed network, what is the key difference between strongly connected and weakly connected components?

---

During Milgram's small-world experiment, what was the key finding regarding social connections?

---

Given a network path (0,1,2,1,3), which statement is correct?

---

In Facebook's 2012 analysis of their social network with 721 million users, what was discovered about the average shortest path length between users?

---

What is the main characteristic of an Euler path in a network?

---


A research team is analyzing a social media network with directed connections (where user A following user B doesn't necessarily mean B follows A). They find that every user can reach every other user when ignoring direction of connections, but this isn't true when considering direction. They conclude:

---

A power company needs to build a new electrical grid connecting 5 cities. The cost of connecting each pair of cities varies based on distance and terrain.

Which algorithm would be most appropriate for finding the most cost-effective way to connect all cities?

---

In a network with degree distribution P(k) ~ k^-γ where γ = 2.5, what happens to the critical fraction fc as the network size N increases?



---

An airport network has an average degree $<k> = 5$ and average squared degree $<k^2> = 75$. What is the critical fraction $f_c$ of airports that need to be removed to break down the network?



---

What distinguishes Kruskal's algorithm from Prim's algorithm in finding a minimum spanning tree?



---

Which network structure would be most vulnerable to targeted attacks but robust against random failures?



---

For a Poisson random network with average degree <k>, what is the condition for the existence of a giant component according to the Molloy-Reed criterion?



---

What best describes a first-order phase transition in network percolation?



---

In designing a robust network against both random and targeted attacks, which degree distribution would be most effective?



---

For a scale-free network with γ > 3, what primarily determines the critical fraction fc?



---

When using the R-index to measure network robustness, what is its maximum possible value?



---

Which of the following best represents how the complementary cumulative distribution function (CCDF) changes when plotting the degree distribution of friends versus regular nodes in a network?



---

In a network where every node has exactly the same degree, what would be true about the friendship paradox?



---

What is the mathematical relationship between the average degree of a friend ⟨k'⟩ and the network's degree moments?



---

When visualizing degree distributions in networks, why is the CCDF preferred over a regular histogram?



---

In the context of the Molloy-Reed condition for giant components, what is the critical threshold?



---

When sampling friends in a network, why does sampling via edges (rather than nodes) create a bias?



---

What is the relationship between the power-law exponent γ and the heterogeneity of a network's degree distribution?



---

For a node with degree $k$, how many times more likely is it to be sampled as a friend compared to a node with degree 1?



---

What is the probability density function p'(k) for the degree distribution of a friend in terms of the original degree distribution p(k)?



---

In the context of network visualization, why is a log-log plot typically used for degree distributions?


---

In a social network with 1000 nodes, you find that the modularity maximization algorithm detects communities even though the edges were randomly generated with equal probability between all node pairs. What does this observation most likely indicate?



---

When analyzing a network using the Stochastic Block Model (SBM), you observe that the probability of connections between communities (p_out) is higher than within communities (p_in). This network structure is best described as:



---

A researcher is analyzing a large social network and discovers that modularity fails to detect small but densely connected communities. This phenomenon is known as:



---

In the context of balanced graph cuts, which statement best explains why normalized cut might be preferred over ratio cut?




---

Which of the following is NOT a valid pseudo-clique definition?



---

In a Stochastic Block Model, what does the presence of clear diagonal blocks in the adjacency matrix typically indicate?



---

When applying community detection to a real network, you notice that increasing the resolution parameter results in:



---

In the context of modularity maximization, why might comparing modularity scores between different networks be misleading?

---

In a social network study of a high school, which centrality measure would be most appropriate to identify students who are best positioned to spread information to all students by a small number of hops?



---

Consider a directed network representing scientific paper citations. Which centrality measure would best identify foundational papers that influenced many other important papers in the field?



---

In a directed network, the PageRank centrality of node i is calculated as $c_i = (1-\beta)\sum(A_ji * c_j/d^out_j) + \beta/N$. What does $d^out_j$ represent?



---

Which centrality measure was specifically designed to address the limitation of closeness centrality in disconnected networks?



---

In an undirected network, if a node has an eccentricity centrality of 0.25, what is the maximum shortest path length from this node to any other node in the network?



---

The Katz centrality was developed to address which limitation of eigenvector centrality?



---

In a transportation network, which centrality measure would be most appropriate for identifying critical junctions whose removal would most disrupt the flow of traffic between different parts of the network?



---

What distinguishes HITS centrality from other centrality measures?



---

The eigenvector centrality of a node is:



---

When computing PageRank, what is the primary purpose of the term β/N?


---

In a network of three connected communities, a random walker starts in assortative community A of 1000 nodes and takes two steps. Which statement is most likely to be true?



---

What is the key mathematical property of a transition probability matrix P for a random walk?

---

If λ₁ and λ₂ are the largest and second-largest eigenvalues of a normalized adjacency matrix respectively, which property indicates faster convergence to the stationary distribution?



---

In the context of PageRank, what is the primary purpose of the teleportation probability β?



---

How does modularity relate to random walks?



---

In a network where all nodes have equal degree, what will be true about the stationary distribution?



---

Given a directed network, which condition might prevent a random walk from reaching a stationary distribution?



---

What does the mixing time of a random walk indicate?



---

In an undirected network, how does the stationary probability πᵢ relate to node degree kᵢ?



---

When analyzing community structure using random walks, what indicates a strong community?

---

A network scientist is analyzing a large social network and needs to choose between spectral embedding and neural embedding approaches. The primary concern is the ability to mathematically prove and understand the method's properties. Which approach would be most suitable?



---

Given a social network, which of the following statements about the first eigenvector of the adjacency matrix spectral embedding is correct?



---

In Laplacian Eigenmap, why do we typically discard the eigenvector corresponding to the smallest eigenvalue?



---

What is the main reason behind using random walks in graph embedding methods like DeepWalk?



---

When using word2vec for network embedding, what is the significance of the window size parameter?



---
What is the primary difference between DeepWalk and node2vec in terms of their random walk strategy?


---

What is the main objective of the Laplacian Eigenmap method?


---

Which of the following best describes the relationship between convolution in the spatial domain and the frequency domain according to the convolution theorem?


---

In GraphSAGE, what is the primary advantage of neighborhood sampling over using all neighbors?



---

What is the main limitation of the Weisfeiler-Lehman (WL) test?



---

What distinguishes Graph Attention Networks (GAT) from previous GNN architectures?



---

When applying a Prewitt operator to an image in the frequency domain, what type of filter is it considered?



---

In the context of spectral graph convolution, what does the eigenvalue λ of the Laplacian matrix represent?



---

What is the key difference between ChebNet and traditional spectral GCNs?



---

What is the main contribution of Graph Isomorphism Network (GIN) to GNN architectures?



---

In image processing, what happens when you apply a low-pass filter in the frequency domain?



---

What is the primary difference between GCN by Kipf and Welling and Bruna's spectral GCN?


---

In analyzing a social network, a researcher finds that removing nodes with high betweenness centrality quickly breaks down the network into disconnected components, but removing nodes with high degree centrality has less impact. This network most likely has:



---

If a network shows clear community structure via modularity maximization and has a stationary random walk distribution highly skewed toward certain nodes, this most likely indicates:



---

In a citation network where papers are nodes and citations are directed edges, which combination of metrics would best identify influential papers that bridge different research fields?



---

A social network exhibits both the friendship paradox and high modularity. What can we conclude?



---

If a network shows high robustness against random failures but clear communities via spectral embedding, this suggests:



---

In a transportation network, what would be the relationship between the Euler path existence and the betweenness centrality distribution?


---

In a network where GCN performs well for node classification but spectral embedding shows no clear structure, what is most likely true?



---

If a network shows both the small-world property and clear core-periphery structure via stochastic block modeling, what can we conclude about its degree distribution?

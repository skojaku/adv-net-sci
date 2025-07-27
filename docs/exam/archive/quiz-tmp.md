---

The city planning department of Smalltown is analyzing its bridge system. The town has 5 distinct areas connected by bridges, where:
- Area A connects to B with 2 bridges
- Area B connects to C with 3 bridges
- Area C connects to D with 1 bridge
- Area D connects to E with 2 bridges
- Area E connects to A with 2 bridges

Based on Euler's theorem, which statement is correct about the possibility of creating a walking tour that crosses each bridge exactly once?

A) A walking tour is possible because all areas have an even number of bridges
B) A walking tour is impossible because there are more than two areas with an odd number of bridges
C) A walking tour is possible because there are exactly two areas with an odd number of bridges
D) A walking tour is impossible because the total number of bridges is odd


<correct_answer>B</correct_answer>

Explanation:
To determine if an Euler path exists, we need to count the number of bridges (degree) for each area:
- Area A: 4 bridges (even)
- Area B: 5 bridges (odd)
- Area C: 4 bridges (even)
- Area D: 3 bridges (odd)
- Area E: 4 bridges (even)

According to Euler's theorem, a path crossing each bridge exactly once exists if and only if all nodes have even degree or exactly two nodes have odd degree. In this case, we have two areas (B and D) with odd degree, making an Euler path impossible.

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

A) 2
B) 3
C) 4
D) 5

<correct_answer>B</correct_answer>

Explanation:
To find the degree of node 1, we need to:
1. Count all edges connected to node 1 in the edge list
2. From the edges list, node 1 connects to:
   - node 0 once: (0,1)
   - node 2 once: (1,2)
   - node 3 once: (1,3)
Therefore, node 1 has 3 connections, making its degree 3. This can also be verified by summing row 1 or column 1 in the adjacency matrix A.

---

A social network researcher is analyzing a small community where each person is represented by a node and friendships by edges. They've created this adjacency matrix:

```python
A = [[0, 1, 0, 1],
     [1, 0, 1, 1],
     [0, 1, 0, 1],
     [1, 1, 1, 0]]
```

What is the total number of unique friendships (edges) in this network?

A) 13
B) 10
C) 6
D) 5

<correct_answer>D</correct_answer>

Explanation:
To find the total number of unique edges:
1. The adjacency matrix is symmetric (undirected graph)
2. Each edge is counted twice in the matrix (once for each direction)
3. Sum of matrix = 13 (2+1+2+1+1+2+1+1+2)
4. Total unique edges = sum/2 = 13/2 ≈ 6
The value in each cell represents the number of edges between two nodes. Since this is an undirected graph, we divide by 2 to avoid counting each edge twice.

---

In the context of network representation, which of the following correctly describes the relationship between edge lists and adjacency matrices?

A) Edge lists are more memory efficient for sparse networks, but adjacency matrices provide faster access to edge existence
B) Edge lists always require more memory than adjacency matrices regardless of network density
C) Adjacency matrices are always more memory efficient than edge lists
D) Edge lists and adjacency matrices require the same amount of memory for all networks

<correct_answer>A</correct_answer>

Explanation:
This question tests understanding of data structure trade-offs:
- Edge lists store only existing edges (E entries)
- Adjacency matrices store N² entries where N is number of nodes
- For sparse networks (E << N²), edge lists use less memory
- Adjacency matrices allow O(1) edge lookup vs O(E) for edge lists
The correct answer reflects this fundamental trade-off in network representations.

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

A) Remove the line A[j][i] += 1
B) Change axis=1 to axis=0
C) Change odd_count in [0, 2] to odd_count == 0
D) Add A = A.transpose() before calculating degrees

---

1. In analyzing the bridges of Königsberg, which statement correctly describes Euler's approach to solving the puzzle?

A) He focused on the exact geographical locations of the bridges and islands
B) He simplified the problem by only considering landmasses and their connections
C) He calculated the physical distances between each bridge
D) He analyzed the water flow patterns between the bridges

<correct_answer>B</correct_answer>

---

2. A network analysis student needs to store a large social network with 100,000 nodes where most nodes are connected to only a few others. Which data structure would be least efficient?

A) Dense adjacency matrix
B) Full edge list in Python dictionary
C) Compressed Sparse Row (CSR) format
D) Adjacency list format

<correct_answer>CA/correct_answer>

---

3. In a directed network, what is the key difference between strongly connected and weakly connected components?

A) Strongly connected components have more edges than weakly connected ones
B) Weakly connected components ignore edge directions while strongly connected ones follow them
C) Strongly connected components must form complete subgraphs
D) Weakly connected components must have bidirectional edges

<correct_answer>B</correct_answer>

---

4. During Milgram's small-world experiment, what was the key finding regarding social connections?

A) All packets reached their targets within exactly six steps
B) Most successful deliveries occurred through approximately six intermediaries
C) Every person knew the target directly within their social circle
D) The experiment failed to show any meaningful connection patterns

<correct_answer>B</correct_answer>

---

5. Given a network path (0,1,2,1,3), which statement is correct?

A) This sequence represents both a trail and a path
B) This sequence represents a trail but not a path
C) This sequence represents a walk but neither a trail nor a path
D) This sequence represents a path but not a trail

<correct_answer>C</correct_answer>


---

7. In Facebook's 2012 analysis of their social network with 721 million users, what was discovered about the average shortest path length between users?

A) It was exactly 6, confirming Milgram's original hypothesis
B) The average shortest path length was deceased
C) It was over 10 connections
D) It varied significantly by geographical region

<correct_answer>B</correct_answer>

---

8. What is the main characteristic of an Euler path in a network?

A) It must start and end at the same node
B) It must cross each edge exactly once
C) It must visit each node exactly once
D) It must be the shortest possible path between two nodes

<correct_answer>B</correct_answer>

A research team is analyzing a social media network with directed connections (where user A following user B doesn't necessarily mean B follows A). They find that every user can reach every other user when ignoring direction of connections, but this isn't true when considering direction. They conclude:

A) The network contains no connected components
B) The network is strongly connected but not weakly connected
C) The network is weakly connected but not strongly connected
D) The network must contain at least one cycle

<correct_answer>C</correct_answer>

---

A power company needs to build a new electrical grid connecting 5 cities. The cost of connecting each pair of cities varies based on distance and terrain.

Which algorithm would be most appropriate for finding the most cost-effective way to connect all cities?

A) Kruskal's algorithm
B) Molloy-Reed criterion
C) Phase transition analysis
D) Percolation theory

<correct_answer>A</correct_answer>

---

In a network with degree distribution P(k) ~ k^-γ where γ = 2.5, what happens to the critical fraction fc as the network size N increases?

A) fc approaches 0
B) fc approaches 0.5
C) fc approaches 1
D) fc remains constant

<correct_answer>C</correct_answer>

---

An airport network has an average degree <k> = 5 and average squared degree <k^2> = 75. What is the critical fraction fc of airports that need to be removed to break down the network?

A) 0.93
B) 0.85
C) 0.77
D) 0.66

<correct_answer>A</correct_answer>

---

What distinguishes Kruskal's algorithm from Prim's algorithm in finding a minimum spanning tree?

A) Kruskal's sorts edges globally while Prim's sorts locally
B) Kruskal's works on directed graphs while Prim's works on undirected
C) Kruskal's finds multiple trees while Prim's finds one
D) Kruskal's is faster but less accurate than Prim's

<correct_answer>A</correct_answer>

---

Which network structure would be most vulnerable to targeted attacks but robust against random failures?

A) Regular lattice
B) Random network
C) Star network
D) Complete graph

<correct_answer>C</correct_answer>

---

For a Poisson random network with average degree <k>, what is the condition for the existence of a giant component according to the Molloy-Reed criterion?

A) <k> > 0
B) <k> > 1
C) <k> > 2
D) <k> > 3

<correct_answer>B</correct_answer>

---

What best describes a first-order phase transition in network percolation?

A) A gradual, continuous change in connectivity
B) A discontinuous jump in connectivity at the critical point
C) Multiple critical points
D) No change in connectivity

<correct_answer>B</correct_answer>

---

In designing a robust network against both random and targeted attacks, which degree distribution would be most effective?

A) Power-law distribution
B) Poisson distribution
C) Bimodal distribution
D) Uniform distribution

<correct_answer>C</correct_answer>

---

For a scale-free network with γ > 3, what primarily determines the critical fraction fc?

A) Maximum degree kmax
B) Minimum degree kmin
C) Average degree <k>
D) Network size N

<correct_answer>B</correct_answer>

---

When using the R-index to measure network robustness, what is its maximum possible value?

A) 1
B) 0.5
C) 2
D) Depends on network size

<correct_answer>B</correct_answer>

---

Which of the following best represents how the complementary cumulative distribution function (CCDF) changes when plotting the degree distribution of friends versus regular nodes in a network?

A) The CCDF of friends has a steeper slope than regular nodes
B) The CCDF of friends has a flatter slope than regular nodes
C) The CCDF of friends and regular nodes have identical slopes
D) The CCDF of friends shows no clear relationship to regular nodes

<correct_answer>B</correct_answer>

---

In a network where every node has exactly the same degree, what would be true about the friendship paradox?

A) The paradox would be stronger than in heterogeneous networks
B) The paradox would still exist but be weaker
C) The paradox would not exist at all
D) The paradox would only exist for nodes with high degrees

<correct_answer>C</correct_answer>

---

What is the mathematical relationship between the average degree of a friend ⟨k'⟩ and the network's degree moments?

A) ⟨k'⟩ = ⟨k⟩
B) ⟨k'⟩ = ⟨k²⟩
C) ⟨k'⟩ = ⟨k²⟩/⟨k⟩
D) ⟨k'⟩ = ⟨k⟩/⟨k²⟩

<correct_answer>C</correct_answer>

---

When visualizing degree distributions in networks, why is the CCDF preferred over a regular histogram?

A) CCDF requires less computational power to calculate
B) CCDF shows the tail of the distribution more clearly without binning
C) CCDF only works for scale-free networks
D) CCDF eliminates all noise in the data

<correct_answer>B</correct_answer>

---

In the context of the Molloy-Reed condition for giant components, what is the critical threshold?

A) ⟨k²⟩/⟨k⟩ > 1
B) ⟨k²⟩/⟨k⟩ > 2
C) ⟨k²⟩/⟨k⟩ > 3
D) ⟨k²⟩/⟨k⟩ > 4

<correct_answer>B</correct_answer>

---

When sampling friends in a network, why does sampling via edges (rather than nodes) create a bias?

A) Edge sampling excludes isolated nodes
B) Edge sampling favors nodes with higher degrees
C) Edge sampling only works in directed networks
D) Edge sampling reduces network connectivity

<correct_answer>B</correct_answer>

---

What is the relationship between the power-law exponent γ and the heterogeneity of a network's degree distribution?

A) Larger γ indicates more heterogeneous distribution
B) Larger γ indicates more homogeneous distribution
C) γ has no relationship to network heterogeneity
D) γ only affects the minimum degree

<correct_answer>B</correct_answer>

---

For a node with degree k, how many times more likely is it to be sampled as a friend compared to a node with degree 1?

A) k/2 times more likely
B) k times more likely
C) k² times more likely
D) 2k times more likely

<correct_answer>B</correct_answer>

---

What is the probability density function p'(k) for the degree distribution of a friend in terms of the original degree distribution p(k)?

A) p'(k) = k·p(k)
B) p'(k) = k·p(k)/⟨k⟩
C) p'(k) = p(k)/⟨k⟩
D) p'(k) = k²·p(k)/⟨k⟩

<correct_answer>B</correct_answer>

---

In the context of network visualization, why is a log-log plot typically used for degree distributions?

A) To make the plot more visually appealing
B) To reduce computational complexity
C) To better visualize both small and large values simultaneously
D) To eliminate outliers in the data

<correct_answer>C</correct_answer>

---

1) In a social network with 1000 nodes, you find that the modularity maximization algorithm detects communities even though the edges were randomly generated with equal probability between all node pairs. What does this observation most likely indicate?

A) The network actually has meaningful community structure
B) The modularity algorithm is malfunctioning
C) High modularity scores don't necessarily indicate real community structure
D) The random network is too small for reliable community detection

<correct_answer>C</correct_answer>

---

2) When analyzing a network using the Stochastic Block Model (SBM), you observe that the probability of connections between communities (p_out) is higher than within communities (p_in). This network structure is best described as:

A) Assortative mixing
B) Random mixing
C) Disassortative mixing
D) Core-periphery structure

<correct_answer>C</correct_answer>

---

3) A researcher is analyzing a large social network and discovers that modularity fails to detect small but densely connected communities. This phenomenon is known as:

A) The resolution limit
B) The density paradox
C) The small community effect
D) The modularity ceiling

<correct_answer>A</correct_answer>

---

4) In the context of balanced graph cuts, which statement best explains why normalized cut might be preferred over ratio cut?

A) Normalized cut always produces fewer communities
B) Normalized cut balances communities based on edge count rather than node count
C) Normalized cut is computationally less expensive
D) Normalized cut produces more balanced community sizes

<correct_answer>B</correct_answer>


---

7) Which of the following is NOT a valid pseudo-clique definition?

A) k-plex: each node connects to all but k others in the group
B) k-core: each node connects to k others in the group
C) n-clique: all nodes are within n steps of each other
D) m-dense: exactly m nodes must be connected to each other

<correct_answer>D</correct_answer>

---

8) In a Stochastic Block Model, what does the presence of clear diagonal blocks in the adjacency matrix typically indicate?

A) Random mixing between communities
B) Strong assortative mixing within communities
C) Negative assortativity between communities
D) Equal-sized communities

<correct_answer>B</correct_answer>

---

9) When applying community detection to a real network, you notice that increasing the resolution parameter results in:

A) Fewer but larger communities
B) More but smaller communities
C) No change in community structure
D) More balanced community sizes

<correct_answer>B</correct_answer>

---

10) In the context of modularity maximization, why might comparing modularity scores between different networks be misleading?

A) Modularity scores are always network-size dependent
B) Different networks have different null models
C) Modularity scores can be high even for random networks
D) The resolution limit affects each network differently

<correct_answer>A and C</correct_answer>

---

1) In a social network study of a high school, which centrality measure would be most appropriate to identify students who are best positioned to spread information to all students by a small number of hops?

A) Degree centrality
B) Closeness centrality
C) Betweenness centrality
D) Eigenvector centrality

<correct_answer>B</correct_answer>

---

2) Consider a directed network representing scientific paper citations. Which centrality measure would best identify foundational papers that influenced many other important papers in the field?

A) Eccentricity centrality
B) Degree centrality
C) HITS authority score
D) Betweenness centrality

<correct_answer>C</correct_answer>

---

3) In a directed network, the PageRank centrality of node i is calculated as c_i = (1-β)∑(A_ji * c_j/d^out_j) + β/N. What does d^out_j represent?

A) The in-degree of node j
B) The total degree of node j
C) The out-degree of node j
D) The eigenvector centrality of node j

<correct_answer>C</correct_answer>

---

4) Which centrality measure was specifically designed to address the limitation of closeness centrality in disconnected networks?

A) Betweenness centrality
B) Harmonic centrality
C) Katz centrality
D) Eigenvector centrality

<correct_answer>B</correct_answer>

---

5) In an undirected network, if a node has an eccentricity centrality of 0.25, what is the maximum shortest path length from this node to any other node in the network?

A) 0.25
B) 2
C) 4
D) 0.5

<correct_answer>C</correct_answer>

---

6) The Katz centrality was developed to address which limitation of eigenvector centrality?

A) Its inability to handle directed networks
B) Its overemphasis on well-connected nodes
C) Its computational complexity
D) Its sensitivity to network size

<correct_answer>B</correct_answer>

---

7) In a transportation network, which centrality measure would be most appropriate for identifying critical junctions whose removal would most disrupt the flow of traffic between different parts of the network?

A) Closeness centrality
B) Degree centrality
C) Betweenness centrality
D) Eigenvector centrality

<correct_answer>C</correct_answer>

---

8) What distinguishes HITS centrality from other centrality measures?

A) It only works on undirected networks
B) It assigns two different scores to each node
C) It requires the network to be connected
D) It only considers immediate neighbors

<correct_answer>B</correct_answer>

---

9) The eigenvector centrality of a node is:

A) Always equal to its degree centrality
B) The sum of its neighbors' centralities
C) Proportional to the sum of its neighbors' centralities
D) Independent of its neighbors' centralities

<correct_answer>C</correct_answer>

---

10) When computing PageRank, what is the primary purpose of the term β/N?

A) To normalize the centrality scores
B) To prevent the algorithm from converging
C) To ensure scores sum to 1
D) To prevent nodes from having nearly zero centrality

<correct_answer>D</correct_answer>

---

1) In a network of three connected communities, a random walker starts in assortative community A of 1000 nodes and takes two steps. Which statement is most likely to be true?

A) The walker will spend equal time in all communities
B) The walker will spend more time in communities with higher node degrees
C) The walker will remain exclusively in community A
D) The walker's location will be completely random with no pattern

<correct_answer>B</correct_answer>

---

2) What is the key mathematical property of a transition probability matrix P for a random walk?

A) All diagonal elements must be zero
B) All elements must be positive!
C) The sum of each row must equal 1
D) The matrix must be symmetric

<correct_answer>C</correct_answer>

---

3) If λ₁ and λ₂ are the largest and second-largest eigenvalues of a normalized adjacency matrix respectively, which property indicates faster convergence to the stationary distribution?

A) λ₁ - λ₂ is small
B) λ₁ - λ₂ is large
C) λ₁ + λ₂ is large
D) λ₁ × λ₂ is large

<correct_answer>B</correct_answer>

---

4) In the context of PageRank, what is the primary purpose of the teleportation probability β?

A) To speed up the computation
B) To ensure convergence by avoiding dead ends
C) To reduce the importance of hub nodes
D) To increase the importance of leaf nodes

<correct_answer>B</correct_answer>

---

5) How does modularity relate to random walks?

A) It compares one-step and infinite-step transition probabilities
B) It only considers infinite-step transition probabilities
C) It only considers one-step transition probabilities
D) It compares two-step and three-step transition probabilities

<correct_answer>A</correct_answer>

---

6) In a network where all nodes have equal degree, what will be true about the stationary distribution?

A) It will be proportional to node centrality
B) It will be uniform across all nodes
C) It will depend on the starting position
D) It will oscillate between nodes

<correct_answer>B</correct_answer>

---

7) Given a directed network, which condition might prevent a random walk from reaching a stationary distribution?

A) The presence of self-loops
B) High clustering coefficient
C) The presence of dead ends
D) High average degree

<correct_answer>C</correct_answer>

---

8) What does the mixing time of a random walk indicate?

A) The average time to visit all nodes
B) The time to reach the steady state
C) The time between community switches
D) The average return time to starting node

<correct_answer>B</correct_answer>

---

9) In an undirected network, how does the stationary probability πᵢ relate to node degree kᵢ?

A) πᵢ = kᵢ
B) πᵢ = kᵢ/2m where m is total edges
C) πᵢ = kᵢ²
D) πᵢ = 1/kᵢ

<correct_answer>B</correct_answer>

---

10) When analyzing community structure using random walks, what indicates a strong community?

A) Large mixing time within the community
B) Small return probability to the community
C) Equal transition probabilities to all communities
D) Higher within-community transition probabilities

<correct_answer>D</correct_answer>

---

A network scientist is analyzing a large social network and needs to choose between spectral embedding and neural embedding approaches. The primary concern is the ability to mathematically prove and understand the method's properties. Which approach would be most suitable?

A) Neural embedding using DeepWalk
B) Neural embedding using node2vec
C) Spectral embedding using eigendecomposition
D) Word2vec with random walks

<correct_answer>C</correct_answer>

---

Given a social network, which of the following statements about the first eigenvector of the adjacency matrix spectral embedding is correct?

A) It represents the community structure
B) It corresponds to the eigenvector centrality
C) It captures structural holes
D) It identifies bridge nodes

<correct_answer>B</correct_answer>

---

In Laplacian Eigenmap, why do we typically discard the eigenvector corresponding to the smallest eigenvalue?

A) It contains too much noise
B) It's computationally expensive
C) It's always the all-one vector (trivial solution)
D) It represents negative relationships

<correct_answer>C</correct_answer>

---

What is the main reason behind using random walks in graph embedding methods like DeepWalk?

A) To reduce computational complexity
B) To transform discrete graph data into sequential data
C) To identify important nodes
D) To calculate node centrality

<correct_answer>B</correct_answer>

---

When using word2vec for network embedding, what is the significance of the window size parameter?

A) It determines the embedding dimension
B) It controls the number of negative samples
C) It defines the context range for node relationships
D) It sets the number of random walks

<correct_answer>C</correct_answer>

---
What is the primary difference between DeepWalk and node2vec in terms of their random walk strategy?

A) DeepWalk uses longer random walks
B) node2vec uses biased random walks with parameters p and q
C) DeepWalk uses multiple random walks per node
D) node2vec only walks to immediate neighbors
<correct_answer>B</correct_answer>

---

What is the main objective of the Laplacian Eigenmap method?

A) Maximize the distance between connected nodes
B) Minimize the distance between connected nodes
C) Maximize the modularity of communities
D) Minimize the number of edges cut

<correct_answer>B</correct_answer>

---

Which of the following best describes the relationship between convolution in the spatial domain and the frequency domain according to the convolution theorem?

A) They are completely independent operations with no mathematical relationship
B) Convolution in spatial domain equals multiplication in frequency domain
C) Convolution in frequency domain equals addition in spatial domain
D) They are identical operations in both domains

<correct_answer>B</correct_answer>

---

In GraphSAGE, what is the primary advantage of neighborhood sampling over using all neighbors?

A) It improves the accuracy of the model
B) It reduces the computational complexity
C) It allows handling dynamic, growing networks
D) It increases the model's depth

<correct_answer>C</correct_answer>

---

What is the main limitation of the Weisfeiler-Lehman (WL) test?

A) It cannot process large graphs
B) It requires excessive computational power
C) It cannot distinguish regular graphs with same number of nodes and edges
D) It only works on directed graphs

<correct_answer>C</correct_answer>

---

What distinguishes Graph Attention Networks (GAT) from previous GNN architectures?

A) It uses random sampling of neighbors
B) It learns attention weights for different neighbors
C) It only processes edge features
D) It requires fewer parameters

<correct_answer>B</correct_answer>

---

When applying a Prewitt operator to an image in the frequency domain, what type of filter is it considered?

A) Low-pass filter
B) Band-pass filter
C) High-pass filter
D) All-pass filter

<correct_answer>C</correct_answer>

---

In the context of spectral graph convolution, what does the eigenvalue λ of the Laplacian matrix represent?

A) The number of nodes in the graph
B) The total variation for the corresponding eigenvector
C) The graph's diameter
D) The number of edges in the graph

<correct_answer>B</correct_answer>

---

What is the key difference between ChebNet and traditional spectral GCNs?

A) ChebNet uses attention mechanisms
B) ChebNet approximates filters using Chebyshev polynomials
C) ChebNet only works on regular graphs
D) ChebNet requires more parameters

<correct_answer>B</correct_answer>

---

What is the main contribution of Graph Isomorphism Network (GIN) to GNN architectures?

A) It introduces attention mechanisms
B) It maximizes discriminative power based on WL test
C) It reduces computational complexity
D) It handles dynamic graphs better

<correct_answer>B</correct_answer>

---

In image processing, what happens when you apply a low-pass filter in the frequency domain?

A) Edges become sharper
B) High-frequency noise is amplified
C) The image becomes smoother
D) Colors become more vivid

<correct_answer>C</correct_answer>

---

What is the primary difference between GCN by Kipf and Welling and Bruna's spectral GCN?

A) GCN uses attention mechanisms
B) GCN employs first-order approximation of spectral convolutions
C) GCN only works on regular graphs
D) GCN requires more parameters

<correct_answer>B</correct_answer>

# Multiple

 In analyzing a social network, a researcher finds that removing nodes with high betweenness centrality quickly breaks down the network into disconnected components, but removing nodes with high degree centrality has less impact. This network most likely has:

A) A scale-free degree distribution
B) A bridge-and-cluster structure
C) A random configuration
D) A core-periphery structure

<correct_answer>B</correct_answer>

---

2) If a network shows clear community structure via modularity maximization and has a stationary random walk distribution highly skewed toward certain nodes, this most likely indicates:

A) The network has negative assortativity
B) Communities are connected through high-degree hubs
C) The network is randomly configured
D) The network has uniform degree distribution

<correct_answer>B</correct_answer>

---

3) In a citation network where papers are nodes and citations are directed edges, which combination of metrics would best identify influential papers that bridge different research fields?

A) PageRank and modularity
B) Degree centrality and HITS
C) Betweenness centrality and community detection
D) Eigenvector centrality and clustering coefficient

<correct_answer>C</correct_answer>

---

4) A social network exhibits both the friendship paradox and high modularity. What can we conclude?

A) The network is randomly connected
B) The network has heterogeneous degree distribution within communities
C) The network must be fully connected
D) The network has uniform degree distribution

<correct_answer>B</correct_answer>

---

5) If a network shows high robustness against random failures but clear communities via spectral embedding, this suggests:

A) The network has a uniform degree distribution
B) The network has strong disassortative mixing
C) The network has hierarchical community structure
D) The network has scale-free properties within communities

<correct_answer>D</correct_answer>

---

6) In a transportation network, what would be the relationship between the Euler path existence and the betweenness centrality distribution?

A) High betweenness nodes must have even degrees
B) There is no direct relationship
C) All nodes must have equal betweenness
D) The network cannot have an Euler path if any node has high betweenness

<correct_answer>B</correct_answer>
---

8) In a network where GCN performs well for node classification but spectral embedding shows no clear structure, what is most likely true?

A) The network has high clustering coefficient
B) Node features contain important information
C) The network is randomly connected
D) The network has clear communities

<correct_answer>B</correct_answer>

---

9) If a network shows both the small-world property and clear core-periphery structure via stochastic block modeling, what can we conclude about its degree distribution?

A) It must be uniform
B) It must be power-law
C) It can be heterogeneous but not necessarily power-law
D) It must be Poisson

<correct_answer>C</correct_answer>


d

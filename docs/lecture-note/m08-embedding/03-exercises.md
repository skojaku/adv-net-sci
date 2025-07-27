# Exercises

## Pen and Paper Exercises

- [✍️ Pen and paper exercises](pen-and-paper/exercise.pdf)

## Programming Exercises

### Exercise 01: Implement DeepWalk

In this exercise, we implement DeepWalk step by step. This exercise is covered in detail in the [02-coding.qmd](02-coding.qmd#exercise-01-implement-deepwalk) file.

**Objectives:**
- Understand how to generate random walks from a graph
- Learn how to apply word2vec to graph data
- Practice extracting and visualizing node embeddings
- Apply clustering methods to embedded representations

**Key Steps:**
1. **Data preparation**: Load the karate club network
2. **Generate random walks**: Implement random walk sampling function
3. **Train word2vec model**: Apply word2vec to the random walks
4. **Clustering**: Use K-means clustering on the embeddings

### Exercise 02: Implement node2vec

In this exercise, we implement the biased random walk mechanism that makes node2vec different from DeepWalk. This exercise is covered in detail in the [02-coding.qmd](02-coding.qmd#exercise-02-implement-node2vec) file.

**Objectives:**
- Understand the biased random walk mechanism in node2vec
- Learn about the parameters p and q and their effects
- Implement the alias sampling method for biased walks
- Compare node2vec results with DeepWalk

**Key Steps:**
1. **Implement biased random walk**: Create functions for node2vec random walks
2. **Understand p and q parameters**: Learn how they control walk behavior
3. **Train node2vec model**: Apply word2vec with biased random walks
4. **Compare results**: Analyze differences between node2vec and DeepWalk

### Additional Practice Exercises

#### Exercise 03: Spectral Embedding Comparison

**Objective**: Compare different spectral embedding methods on the same network.

**Tasks**:
1. Implement spectral embedding using the adjacency matrix
2. Implement modularity embedding
3. Implement Laplacian Eigenmap
4. Compare the resulting embeddings visually
5. Analyze which method best captures community structure

#### Exercise 04: Parameter Sensitivity Analysis

**Objective**: Understand how different parameters affect embedding quality.

**Tasks**:
1. Vary the embedding dimension (d) in spectral methods
2. Test different window sizes in word2vec-based methods
3. Experiment with different p and q values in node2vec
4. Compare clustering performance across parameter settings

#### Exercise 05: Real Network Analysis

**Objective**: Apply embedding methods to a real-world network.

**Tasks**:
1. Choose a real network dataset (e.g., social network, citation network)
2. Apply both spectral and neural embedding methods
3. Evaluate embeddings using downstream tasks (clustering, classification)
4. Compare computational efficiency and embedding quality

## Evaluation Questions

1. **Conceptual Understanding**:
   - What is the main difference between spectral and neural embedding methods?
   - How do random walks help bridge the gap between word2vec and graph data?
   - What role do eigenvalues and eigenvectors play in spectral embedding?

2. **Technical Implementation**:
   - Why do we exclude the first eigenvector in Laplacian Eigenmap?
   - How does the window size in word2vec affect the final embeddings?
   - What is the computational complexity of different embedding methods?

3. **Practical Applications**:
   - When would you choose spectral methods over neural methods?
   - How do the p and q parameters in node2vec affect the type of structure captured?
   - What are the trade-offs between embedding dimension and computational cost?

## Additional Resources

- **Software Packages**: Refer to the [01-concepts.md](01-concepts.md#software-for-network-embedding) for recommended implementations
- **Mathematical Details**: See [04-appendix.md](04-appendix.md) for formal proofs and derivations
- **Preparation Material**: Review [00-preparation.md](00-preparation.md) for background on random walks and linear algebra
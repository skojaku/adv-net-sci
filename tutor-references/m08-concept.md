# Module 08: Graph Embedding - Core Concepts

## What is Graph Embedding?

**Graph embedding** is the process of mapping nodes (and sometimes edges) from a network to low-dimensional vector representations while preserving network structural information.

**Goal**: Transform discrete graph structure into continuous vector space where:
- Similar nodes have similar embeddings
- Network relationships are preserved
- Machine learning algorithms can be applied

## Why Embedding Networks?

### Limitations of Raw Networks
- **Discrete structure**: Hard to apply standard ML algorithms
- **High dimensionality**: Adjacency matrices are n×n (sparse but large)
- **Complex relationships**: Non-Euclidean structure difficult to process

### Benefits of Embeddings
- **Continuous representation**: Enable gradient-based optimization
- **Dimensionality reduction**: From n×n to n×d where d << n
- **Feature learning**: Automatic discovery of relevant node features
- **Downstream tasks**: Classification, clustering, link prediction

## Spectral Embedding Methods

### Principal Component Analysis (PCA)
Apply PCA directly to adjacency matrix or derived matrices.

**Process**:
1. Compute adjacency matrix A
2. Perform eigendecomposition: A = UΛU^T
3. Use top k eigenvectors as embeddings

**Limitations**: Doesn't capture non-linear relationships

### Laplacian Eigenmap
Use graph Laplacian for embedding.

**Graph Laplacian**: L = D - A
- D = degree matrix (diagonal)
- A = adjacency matrix

**Process**:
1. Compute normalized Laplacian: L_norm = D^(-1/2) L D^(-1/2)
2. Find smallest eigenvalues and eigenvectors
3. Use eigenvectors as node embeddings

**Property**: Preserves local neighborhood structure

### Spectral Clustering Connection
Spectral embedding naturally leads to spectral clustering - eigenvectors reveal community structure.

## Neural Network Embedding Methods

### Word2Vec Inspiration
Borrowed from natural language processing where words are embedded based on context.

**Key insight**: Treat random walks on graphs as "sentences" and nodes as "words"

### Node2Vec
Extends Word2Vec to networks using biased random walks.

**Algorithm**:
1. Generate biased random walks from each node
2. Treat walks as sentences, nodes as words
3. Apply Skip-gram model to learn embeddings

**Biased Walk Parameters**:
- **p** (return parameter): Controls likelihood of returning to previous node
- **q** (in-out parameter): Controls exploration vs exploitation
  - q < 1: Prefer outward exploration (BFS-like)
  - q > 1: Prefer local exploration (DFS-like)

### DeepWalk
Uses uniform random walks instead of biased walks.

**Process**:
1. Generate uniform random walks
2. Apply Word2Vec Skip-gram model
3. Learn node embeddings that predict walk context

### Other Neural Methods
- **LINE**: Large-scale information network embedding
- **GraphSAGE**: Inductive representation learning
- **Graph Neural Networks**: End-to-end learning with graph structure

## Matrix Factorization Approaches

### Basic Idea
Factorize network-related matrices into low-rank components.

### Methods
- **Adjacency matrix factorization**: A ≈ UV^T
- **Laplacian factorization**: Factorize graph Laplacian
- **Transition matrix factorization**: Random walk probabilities

### Advantages
- Computational efficiency
- Theoretical guarantees
- Interpretable factors

## Embedding Quality Evaluation

### Intrinsic Evaluation
**Reconstruction accuracy**: How well can embeddings reconstruct original network?

**Metrics**:
- Mean squared error for adjacency matrix reconstruction
- Precision/recall for edge prediction
- Ranking metrics for node similarity

### Extrinsic Evaluation
**Downstream task performance**: How well do embeddings work for specific applications?

**Tasks**:
- **Node classification**: Predicting node labels
- **Link prediction**: Predicting missing edges  
- **Graph clustering**: Community detection
- **Graph visualization**: 2D/3D network layout

### Embedding Visualization
- t-SNE: Non-linear dimensionality reduction for visualization
- UMAP: Uniform Manifold Approximation and Projection
- Direct 2D embedding methods

## Applications

### Social Networks
- **User profiling**: Learning user representations from social connections
- **Friend recommendation**: Link prediction using embeddings
- **Community detection**: Clustering in embedding space
- **Influence analysis**: Measuring user similarity and reach

### Biological Networks
- **Protein function prediction**: Using protein interaction networks
- **Drug discovery**: Drug-target interaction prediction
- **Disease analysis**: Disease-gene association networks
- **Pathway analysis**: Biological pathway embeddings

### Knowledge Graphs
- **Entity embeddings**: Learning representations of entities and relations
- **Knowledge completion**: Predicting missing facts
- **Question answering**: Using embeddings for reasoning
- **Semantic search**: Finding related concepts

### Recommendation Systems
- **Collaborative filtering**: User-item bipartite graph embeddings
- **Content recommendation**: Item similarity in embedding space
- **Hybrid approaches**: Combining multiple embedding types
- **Cold start problems**: Handling new users/items

## Challenges and Limitations

### Scalability Issues
- **Memory requirements**: Storing embeddings for large networks
- **Computational complexity**: Training time for million-node networks
- **Distributed computing**: Parallel embedding algorithms

### Parameter Sensitivity
- **Embedding dimension**: Trade-off between expressiveness and efficiency
- **Walk parameters**: Choosing p, q in Node2Vec
- **Training hyperparameters**: Learning rate, epochs, window size

### Evaluation Difficulties
- **Ground truth**: Often unclear what "good" embedding means
- **Task dependence**: Different tasks may require different embeddings
- **Stability**: Embeddings may vary across training runs

### Preservation Trade-offs
- **Local vs global structure**: Cannot preserve all network properties
- **Static snapshots**: Most methods assume static networks
- **Directed vs undirected**: Different approaches needed

## Recent Developments

### Dynamic Graph Embeddings
- **Temporal networks**: Evolving network embeddings over time
- **Online learning**: Updating embeddings incrementally
- **Time-aware methods**: Incorporating temporal information

### Heterogeneous Graph Embeddings
- **Multiple node types**: Different types of entities
- **Multiple edge types**: Different types of relationships
- **Meta-path based**: Using meta-paths to define context

### Graph Neural Networks
- **End-to-end learning**: Learning embeddings and task jointly
- **Inductive methods**: Generalizing to unseen nodes
- **Attention mechanisms**: Learning importance weights
- **Graph Transformer**: Attention-based graph processing
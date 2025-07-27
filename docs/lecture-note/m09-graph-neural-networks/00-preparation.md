# Preparation: Machine Learning Basics for Graph Neural Networks

## From Module 8: Network Embedding Foundations

Graph Neural Networks build upon the foundational concepts of network embedding that we learned in Module 8. Before diving into GNNs, let's review these essential machine learning concepts.

## Spectral Embedding: Matrix Decomposition Approach

Networks are high-dimensional discrete data that can be difficult to analyze with traditional machine learning methods that assume continuous and smooth data. Spectral embedding is a technique to embed networks into low-dimensional spaces.

Let us approach the spectral embedding from the perspective of network compression. Suppose we have an adjacency matrix $\mathbf{A}$ of a network. The adjacency matrix is a high-dimensional data, i.e., a matrix has size $N \times N$ for a network of $N$ nodes. We want to compress it into a lower-dimensional matrix $\mathbf{U}$ of size $N \times d$ for a user-defined small integer $d < N$. A good $\mathbf{U}$ should preserve the network structure and thus can reconstruct the original data $\mathbf{A}$ as closely as possible. This leads to the following optimization problem:

$$
\min_{\mathbf{U}} J(\mathbf{U}),\quad J(\mathbf{U}) = \| \mathbf{A} - \mathbf{U}\mathbf{U}^\top \|_F^2
$$

where $\mathbf{U}\mathbf{U}^\top$ is the outer product of $\mathbf{U}$ and represents the reconstructed network, $\|\cdot\|_F$ is the Frobenius norm, and $J(\mathbf{U})$ is the loss function that measures the difference between the original network $\mathbf{A}$ and the reconstructed network $\mathbf{U}\mathbf{U}^\top$. By minimizing the Frobenius norm with respect to $\mathbf{U}$, we obtain the best low-dimensional embedding of the network.

Consider the spectral decomposition of $\mathbf{A}$:

$$
\mathbf{A} = \sum_{i=1}^N \lambda_i \mathbf{u}_i \mathbf{u}_i^\top
$$

where $\lambda_i$ are weights and $\mathbf{u}_i$ are column vectors. Each term $\lambda_i \mathbf{u}_i \mathbf{u}_i^\top$ is a rank-one matrix that captures a part of the network's structure. The larger the weight $\lambda_i$, the more important that term is in describing the network. To compress the network, we can select the $d$ terms with the largest weights $\lambda_i$. By combining the corresponding $\mathbf{u}_i$ vectors into a matrix $\mathbf{U}$, we obtain a good low-dimensional embedding of the network.

## Laplacian Eigenmap: Graph-Aware Embedding

Laplacian Eigenmap is another approach to compress a network into a low-dimensional space. The fundamental idea behind this method is to position connected nodes close to each other in the low-dimensional space. This approach leads to the following optimization problem:

$$
\min_{\mathbf{U}} J_{LE}(\mathbf{U}),\quad J_{LE}(\mathbf{U}) = \frac{1}{2}\sum_{i,j} A_{ij} \| u_i - u_j \|^2
$$

In this equation, $\| u_i - u_j \|^2$ represents the squared distance between nodes $i$ and $j$ in the low-dimensional space. The goal is to minimize this distance for connected nodes (where $A_{ij} = 1$).

This can be rewritten using the Laplacian matrix:

$$
J_{LE}(\mathbf{U}) = \text{Tr}(\mathbf{U}^\top \mathbf{L} \mathbf{U})
$$

where the Laplacian matrix $\mathbf{L}$ is defined as:

$$
L_{ij} = \begin{cases}
k_i & \text{if } i = j \\
-A_{ij} & \text{if } i \neq j
\end{cases}
$$

The solution is the $d$ eigenvectors associated with the $d$ smallest eigenvalues of $\mathbf{L}$.

## Neural Embedding: word2vec Fundamentals

Neural embedding methods like word2vec provide another perspective on learning representations. word2vec is a neural network model that learns word embeddings in a continuous vector space, operating on the principle: "You shall know a word by the company it keeps."

Key concepts from word2vec include **Context Windows** (word2vec identifies a word's context by examining the words within a fixed window around it), **Neural Architecture** (word2vec uses a neural network that looks like a bow tie - two layers of vocabulary size coupled with a much smaller hidden layer), **Dimensionality Reduction** (word2vec can be considered as a dimensionality reduction technique that reduces the dimensionality based on the co-occurrence of words within a short distance), and **Dense Vector Representations** (with word2vec, words are represented as dense vectors, enabling exploration of relationships using simple linear algebra).

## Essential Machine Learning Concepts for GNNs

Graph Neural Networks rely on optimization techniques similar to those used in spectral embedding. Key concepts include **Loss Functions and Optimization** (reconstruction loss for measuring how well learned representations can reconstruct original graph structure, supervised loss when node labels are available for classification tasks, and gradient descent for iterative optimization methods for training neural networks).

Traditional spectral methods require explicit eigenvalue decomposition, while neural methods learn representations through **Feature Learning vs. Feature Engineering**. This includes end-to-end learning where features are learned jointly with the task objective, parameterized functions where neural networks provide flexible function approximation, and backpropagation for automatic differentiation enabling efficient gradient computation.

The distinction between **Inductive vs. Transductive Learning** is crucial: spectral methods typically require the full graph during training (transductive), while neural methods can generalize to unseen nodes and graphs (inductive).

**Nonlinear Transformations** represent a key advantage of neural approaches over spectral methods. While spectral methods are fundamentally linear, neural networks introduce nonlinearity through activation functions (ReLU, sigmoid, tanh enable complex mappings), multiple layers (deep architectures can learn hierarchical representations), and attention mechanisms (dynamic weighting of different graph components).

## Connection to Graph Neural Networks

Graph Neural Networks extend these embedding concepts by:

1. **Combining Spectral and Neural Approaches**: Using spectral graph theory to design neural architectures
2. **Message Passing**: Generalizing convolution operations to irregular graph structures  
3. **Learnable Filters**: Replacing fixed spectral filters with trainable neural networks
4. **Multi-task Learning**: Jointly learning node representations and downstream tasks

This foundation prepares us to understand how GNNs build upon both the mathematical rigor of spectral methods and the flexibility of neural networks to create powerful graph learning architectures.
# Network Embedding Concepts

## What to Learn in This Module

In this module, we will learn how to embed networks into low-dimensional spaces. We will learn:
- Spectral embedding
- Neural embedding
- **Keywords**: Laplacian EigenMap, Normalized Spectral Embedding, DeepWalk, Node2Vec

## Spectral vs Neural Embedding

We have learned two types of graph embedding methods: spectral methods and neural embedding methods. But which one is better than the other? We will compare the two types of methods from multiple aspects as follows.

### 1. Analytical Tractability

**Spectral methods** are more analytically tractable and thus are easier to understand using linear algebra. It is even possible to derive the capability and limitation of the spectral methods. For example, spectral methods based on adjacency matrices and normalized laplacian matrices are shown to be optimal for detecting communities in the stochastic block model {footcite}`nadakuditi2012graph`. 

**Neural embedding methods** are less analytically tractable. But still possible to analyze the theoretical properties by using an equivalence between a spectral embedding and a neural embedding under a very specific condition {footcite}`qiu2018network,kojaku2023network`. These theoretical results have demonstrated that DeepWalk, node2vec, and LINE are in fact an optimal embedding methods for community detection for the stochatic block model.

### 2. Scalability

A key limitation of the **spectral embedding** is the computational cost. While efficient methods exist like randomized singular value decomposition (implemented in scikit learn package as `TruncatedSVD`), they might be unstable depending on the spectrum distribution of the matrix to be decomposed. 

**Neural embedding methods** are often more stable and scalable.

### 3. Flexibility

**Neural embeddings** are more flexible than spectral embeddings. It is easy to change the objective functions of neural embeddings using the same training procedure. For example, the proximity of nodes in both embedding spaces are inherently dot similarity, but one can train neural embeddings to optimize for other metrics to embed the network in a non-Euclidean space. An interesting example of this is the Poincaré embeddings {footcite}`nickel2017poincare` for embedding networks in hyperbolic space.

![](https://pbs.twimg.com/media/DUUj0sxU8AACV50.jpg)

## Software for Network Embedding

There are various software packages for network embeddings. But due to technical complexity, some of them do not faithfully implement the algorithms in the paper. We provide a list of software packages for network embeddings below.

- [fastnode2vec](https://github.com/louisabraham/fastnode2vec). This is a very fast implementation of node2vec. However, it uses a uniform probability distribution for the negative sampling, which is different from the original node2vec paper that uses a different distribution. This leads to some degeneracy of the embedding quality in community detection tasks.
- [pytorch-geometric](https://github.com/pyg-team/pytorch_geometric). This is a very popular package for graph neural networks. It also uses a uniform probability distribution for the negative sampling, potentially having the same issue as `fastnode2vec`.
- [gnn-tools](https://github.com/skojaku/gnn-tools). This is a collection of my experiments on network embedding methods.
- [My collection](https://github.com/skojaku/graphvec). This is a lighter version of the `gnn-tools` collection.

## Exercises

- [✍️ Pen and paper exercises](pen-and-paper/exercise.pdf)
# Module 08: Graph Embedding - Coding Implementation

## Spectral Embedding Methods

### Laplacian Eigenmap
```python
import igraph
import numpy as np
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt

def laplacian_eigenmap(graph, dimensions=2):
    """Compute Laplacian eigenmap embedding"""
    # Get adjacency matrix
    A = np.array(graph.get_adjacency().data)
    
    # Compute degree matrix
    degrees = np.array(graph.degree())
    D = np.diag(degrees)
    
    # Compute normalized Laplacian
    D_sqrt_inv = np.diag(1.0 / np.sqrt(degrees))
    L_norm = np.eye(len(degrees)) - D_sqrt_inv @ A @ D_sqrt_inv
    
    # Compute smallest eigenvalues and eigenvectors
    eigenvalues, eigenvectors = eigsh(L_norm, k=dimensions+1, which='SM')
    
    # Use eigenvectors (skip the first trivial one)
    embedding = eigenvectors[:, 1:dimensions+1]
    
    return embedding, eigenvalues[1:]

# Example usage
g = igraph.Graph.Famous('Zachary')
embedding, eigenvals = laplacian_eigenmap(g, dimensions=2)

# Plot embedding
plt.figure(figsize=(8, 6))
plt.scatter(embedding[:, 0], embedding[:, 1], s=50, alpha=0.7)
for i in range(len(embedding)):
    plt.annotate(str(i), (embedding[i, 0], embedding[i, 1]), 
                xytext=(5, 5), textcoords='offset points', fontsize=8)
plt.title('Laplacian Eigenmap Embedding')
plt.xlabel('First Eigenvector')
plt.ylabel('Second Eigenvector')
plt.grid(True, alpha=0.3)
plt.show()
```

### PCA on Adjacency Matrix
```python
from sklearn.decomposition import PCA

def adjacency_pca_embedding(graph, dimensions=2):
    """PCA embedding of adjacency matrix"""
    A = np.array(graph.get_adjacency().data)
    
    # Apply PCA
    pca = PCA(n_components=dimensions)
    embedding = pca.fit_transform(A)
    
    return embedding, pca.explained_variance_ratio_

# Compare with Laplacian embedding
pca_embedding, explained_var = adjacency_pca_embedding(g, dimensions=2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Laplacian embedding
ax1.scatter(embedding[:, 0], embedding[:, 1], s=50, alpha=0.7)
ax1.set_title('Laplacian Eigenmap')
ax1.grid(True, alpha=0.3)

# PCA embedding
ax2.scatter(pca_embedding[:, 0], pca_embedding[:, 1], s=50, alpha=0.7, color='red')
ax2.set_title(f'PCA Embedding (Explained var: {explained_var.sum():.2f})')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
```

## Node2Vec-style Implementation

### Random Walk Generation
```python
def generate_biased_walks(graph, num_walks=10, walk_length=20, p=1.0, q=1.0):
    """Generate biased random walks for node2vec-style embedding"""
    walks = []
    
    for start_node in range(graph.vcount()):
        for _ in range(num_walks):
            walk = [start_node]
            
            if len(graph.neighbors(start_node)) == 0:
                walks.append(walk)
                continue
                
            # First step is uniform random
            current = np.random.choice(graph.neighbors(start_node))
            walk.append(current)
            
            # Subsequent steps use bias
            for _ in range(walk_length - 2):
                neighbors = graph.neighbors(current)
                if not neighbors:
                    break
                
                # Compute transition probabilities
                probabilities = []
                for neighbor in neighbors:
                    if neighbor == walk[-2]:  # Return to previous
                        prob = 1.0 / p
                    elif graph.are_adjacent(neighbor, walk[-2]):  # Close to previous
                        prob = 1.0
                    else:  # Farther from previous
                        prob = 1.0 / q
                    probabilities.append(prob)
                
                # Normalize probabilities
                probabilities = np.array(probabilities)
                probabilities = probabilities / probabilities.sum()
                
                # Sample next node
                current = np.random.choice(neighbors, p=probabilities)
                walk.append(current)
            
            walks.append(walk)
    
    return walks

# Generate walks with different parameters
walks_bfs = generate_biased_walks(g, num_walks=5, walk_length=10, p=1.0, q=0.5)
walks_dfs = generate_biased_walks(g, num_walks=5, walk_length=10, p=1.0, q=2.0)

print(f"Generated {len(walks_bfs)} BFS-like walks")
print(f"Generated {len(walks_dfs)} DFS-like walks")
print(f"Example walk: {walks_bfs[0]}")
```

### Skip-gram Style Training (Conceptual)
```python
from collections import defaultdict, Counter

def create_training_data(walks, window_size=5):
    """Create training pairs from random walks"""
    training_pairs = []
    
    for walk in walks:
        for i, center_node in enumerate(walk):
            # Define context window
            start = max(0, i - window_size)
            end = min(len(walk), i + window_size + 1)
            
            for j in range(start, end):
                if i != j:  # Don't pair node with itself
                    context_node = walk[j]
                    training_pairs.append((center_node, context_node))
    
    return training_pairs

def simple_embedding_learning(training_pairs, num_nodes, embed_dim=64, 
                             learning_rate=0.01, epochs=100):
    """Simplified embedding learning (conceptual implementation)"""
    # Initialize embeddings randomly
    embeddings = np.random.normal(0, 0.1, (num_nodes, embed_dim))
    
    # Count co-occurrences for simplified training
    cooccurrence = defaultdict(int)
    for center, context in training_pairs:
        cooccurrence[(center, context)] += 1
    
    # Simple update rule (not full skip-gram)
    for epoch in range(epochs):
        for (center, context), count in cooccurrence.items():
            # Simplified gradient update
            center_emb = embeddings[center]
            context_emb = embeddings[context]
            
            # Simple similarity-based update
            similarity = np.dot(center_emb, context_emb)
            target = 1.0  # Want high similarity for co-occurring nodes
            
            error = target - similarity
            gradient = error * learning_rate
            
            embeddings[center] += gradient * context_emb * 0.1
            embeddings[context] += gradient * center_emb * 0.1
    
    return embeddings

# Create embeddings from walks
training_pairs = create_training_data(walks_bfs + walks_dfs)
embeddings = simple_embedding_learning(training_pairs, g.vcount(), embed_dim=2)

# Visualize learned embeddings
plt.figure(figsize=(8, 6))
plt.scatter(embeddings[:, 0], embeddings[:, 1], s=50, alpha=0.7)
for i in range(len(embeddings)):
    plt.annotate(str(i), (embeddings[i, 0], embeddings[i, 1]), 
                xytext=(5, 5), textcoords='offset points', fontsize=8)
plt.title('Simple Walk-based Embeddings')
plt.grid(True, alpha=0.3)
plt.show()
```

## Matrix Factorization Approach

### Simple Matrix Factorization
```python
from sklearn.decomposition import NMF

def matrix_factorization_embedding(graph, dimensions=2):
    """Embed using non-negative matrix factorization of adjacency matrix"""
    A = np.array(graph.get_adjacency().data, dtype=float)
    
    # Add self-loops to make diagonal positive
    A_self = A + np.eye(A.shape[0])
    
    # Apply NMF
    nmf = NMF(n_components=dimensions, random_state=42, max_iter=1000)
    embedding = nmf.fit_transform(A_self)
    
    return embedding, nmf.reconstruction_err_

# Compare different embedding methods
methods = {
    'Laplacian': embedding,
    'PCA': pca_embedding, 
    'Matrix Factorization': matrix_factorization_embedding(g)[0]
}

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, (name, emb) in enumerate(methods.items()):
    axes[idx].scatter(emb[:, 0], emb[:, 1], s=50, alpha=0.7)
    axes[idx].set_title(f'{name} Embedding')
    axes[idx].grid(True, alpha=0.3)

plt.tight_layout()
```

## Embedding Evaluation

### Link Prediction Evaluation
```python
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

def evaluate_embedding_link_prediction(graph, embedding):
    """Evaluate embedding quality using link prediction task"""
    
    # Create positive examples (existing edges)
    edges = graph.get_edgelist()
    positive_pairs = [(i, j) for i, j in edges]
    
    # Create negative examples (non-existing edges)
    negative_pairs = []
    num_negatives = len(positive_pairs)
    
    while len(negative_pairs) < num_negatives:
        i = np.random.randint(0, graph.vcount())
        j = np.random.randint(0, graph.vcount())
        if i != j and not graph.are_adjacent(i, j):
            negative_pairs.append((i, j))
    
    # Compute edge scores using embedding similarity
    def edge_score(i, j, embedding):
        return np.dot(embedding[i], embedding[j])
    
    positive_scores = [edge_score(i, j, embedding) for i, j in positive_pairs]
    negative_scores = [edge_score(i, j, embedding) for i, j in negative_pairs]
    
    # Create labels and scores
    y_true = [1] * len(positive_scores) + [0] * len(negative_scores)
    y_scores = positive_scores + negative_scores
    
    # Compute AUC
    auc = roc_auc_score(y_true, y_scores)
    return auc

# Evaluate different embeddings
for name, emb in methods.items():
    auc = evaluate_embedding_link_prediction(g, emb)
    print(f"{name} embedding AUC: {auc:.3f}")
```

## Visualization and Analysis

### t-SNE Visualization for Higher Dimensions
```python
from sklearn.manifold import TSNE

def high_dim_embedding_visualization(graph, dimensions=10):
    """Create high-dimensional embedding and visualize with t-SNE"""
    
    # Create higher-dimensional Laplacian embedding
    high_dim_embedding, _ = laplacian_eigenmap(graph, dimensions=dimensions)
    
    # Apply t-SNE for 2D visualization
    tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, graph.vcount()-1))
    tsne_embedding = tsne.fit_transform(high_dim_embedding)
    
    # Plot
    plt.figure(figsize=(10, 8))
    plt.scatter(tsne_embedding[:, 0], tsne_embedding[:, 1], s=60, alpha=0.7)
    
    for i in range(len(tsne_embedding)):
        plt.annotate(str(i), (tsne_embedding[i, 0], tsne_embedding[i, 1]), 
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.title(f'{dimensions}D Laplacian Embedding → t-SNE Visualization')
    plt.grid(True, alpha=0.3)
    return high_dim_embedding, tsne_embedding

high_dim_emb, tsne_emb = high_dim_embedding_visualization(g, dimensions=5)
```
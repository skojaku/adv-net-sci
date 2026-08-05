# /// script
# dependencies = [
#     "bokeh",
#     "gensim",
#     "marimo",
#     "matplotlib",
#     "numpy",
#     "pandas",
#     "python-igraph",
#     "scikit-learn",
#     "seaborn",
#     "umap-learn",
# ]
# [tool.marimo.display]
# default_width = "full"
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import igraph
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Load the karate club network
    g = igraph.Graph.Famous("Zachary")
    A = g.get_adjacency_sparse()

    # Get community labels (Mr. Hi = 0, Officer = 1)
    labels = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    g.vs["label"] = labels

    # Visualize the network
    palette = sns.color_palette().as_hex()
    igraph.plot(g, vertex_color=[palette[label] for label in labels], bbox=(300, 300))
    return A, g, igraph, labels, np, palette, plt, sns


@app.cell
def _(A):
    # Convert to dense array for eigendecomposition
    A_dense = A.toarray()
    return (A_dense,)


@app.cell
def _(A_dense, labels, np, plt, sns):
    # Compute the spectral decomposition
    _eigvals, _eigvecs = np.linalg.eig(A_dense)
    d = 2
    # Find the top d eigenvectors
    _sorted_indices = np.argsort(_eigvals)[::-1][:d]
    _eigvals = _eigvals[_sorted_indices]
    _eigvecs = _eigvecs[:, _sorted_indices]
    _fig, _ax = plt.subplots(figsize=(7, 5))
    sns.scatterplot(x=_eigvecs[:, 0], y=_eigvecs[:, 1], hue=labels, ax=_ax)
    # Plot the results
    _ax.set_title('Spectral Embedding')
    _ax.set_xlabel('Eigenvector 1')
    _ax.set_ylabel('Eigenvector 2')
    plt.show()
    return (d,)


@app.cell
def _(A_dense, d, labels, np, plt, sns):
    deg = np.sum(A_dense, axis=1)
    m = np.sum(deg) / 2
    Q = A_dense - np.outer(deg, deg) / (2 * m)
    Q = Q / (2 * m)
    _eigvals, _eigvecs = np.linalg.eig(Q)
    _sorted_indices = np.argsort(-_eigvals)[:d]
    _eigvals = _eigvals[_sorted_indices]
    _eigvecs = _eigvecs[:, _sorted_indices]
    _fig, _ax = plt.subplots(figsize=(7, 5))
    sns.scatterplot(x=_eigvecs[:, 0], y=_eigvecs[:, 1], hue=labels, ax=_ax)
    _ax.set_title('Modularity Embedding')
    _ax.set_xlabel('Eigenvector 1')
    _ax.set_ylabel('Eigenvector 2')
    plt.show()
    return


@app.cell
def _(A_dense, d, labels, np, plt, sns):
    D = np.diag(np.sum(A_dense, axis=1))
    L = D - A_dense
    _eigvals, _eigvecs = np.linalg.eig(L)
    _sorted_indices = np.argsort(_eigvals)[1:d + 1]
    _eigvals = _eigvals[_sorted_indices]
    # Sort the eigenvalues and eigenvectors
    _eigvecs = _eigvecs[:, _sorted_indices]  # Exclude the first eigenvector
    _fig, _ax = plt.subplots(figsize=(7, 5))
    sns.scatterplot(x=_eigvecs[:, 0], y=_eigvecs[:, 1], hue=labels, ax=_ax)
    _ax.set_title('Laplacian Eigenmap')
    # Plot the results
    _ax.set_xlabel('Eigenvector 2')
    _ax.set_ylabel('Eigenvector 3')
    plt.show()
    return


@app.cell
def _():
    import gensim
    import gensim.downloader
    from gensim.models import Word2Vec
    # Load pre-trained word2vec model from Google News
    model = gensim.downloader.load('word2vec-google-news-300')
    return Word2Vec, model


@app.cell
def _(model):
    # Example usage
    word = "king"
    similar_words = model.most_similar(word)
    print(f"Words most similar to '{word}':")
    for similar_word, similarity in similar_words:
        print(f"{similar_word}: {similarity:.4f}")
    return


@app.cell
def _(model):
    # We solve the puzzle by
    #
    #  vec(king) - vec(man) + vec(woman)
    #
    # To solve this, we use the model.most_similar function, with positive words being "king" and "woman" (additive), and negative words being "man" (subtractive).
    #
    model.most_similar(positive=['woman', "king"], negative=['man'], topn=5)
    return


@app.cell
def _(model, np, plt, sns):
    import pandas as pd
    from sklearn.decomposition import PCA
    countries = ['Germany', 'France', 'Italy', 'Spain', 'Portugal', 'Greece']
    capital_words = ['Berlin', 'Paris', 'Rome', 'Madrid', 'Lisbon', 'Athens']
    country_embeddings = np.array([model[country] for country in countries])
    capital_embeddings = np.array([model[capital] for capital in capital_words])
    pca = PCA(n_components=2)
    embeddings = np.vstack([country_embeddings, capital_embeddings])
    embeddings_pca = pca.fit_transform(embeddings)
    df = pd.DataFrame(embeddings_pca, columns=['PC1', 'PC2'])
    df['Label'] = countries + capital_words
    df['Type'] = ['Country'] * len(countries) + ['Capital'] * len(capital_words)
    plt.figure(figsize=(12, 10))
    scatter_plot = sns.scatterplot(data=df, x='PC1', y='PC2', hue='Type', style='Type', s=200, palette='deep', markers=['o', 's'])
    for _i in range(len(df)):
        plt.text(df['PC1'][_i], df['PC2'][_i] + 0.08, df['Label'][_i], fontsize=12, ha='center', va='bottom', bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
    for _i in range(len(countries)):
        plt.arrow(df['PC1'][_i], df['PC2'][_i], df['PC1'][_i + len(countries)] - df['PC1'][_i], df['PC2'][_i + len(countries)] - df['PC2'][_i], color='gray', alpha=0.6, linewidth=1.5, head_width=0.02, head_length=0.03)
    plt.legend(title='Type', title_fontsize='13', fontsize='11')
    plt.title('PCA of Country and Capital Word Embeddings', fontsize=16)
    plt.xlabel('Principal Component 1', fontsize=14)
    plt.ylabel('Principal Component 2', fontsize=14)
    _ax = plt.gca()
    _ax.set_axis_off()
    return


@app.cell
def _(np):
    def random_walk(net, start_node, walk_length):
        """
        Generate a random walk starting from start_node.

        Parameters:
        -----------
        net : sparse matrix
            Adjacency matrix of the network
        start_node : int
            Starting node for the walk
        walk_length : int
            Length of the walk

        Returns:
        --------
        walk : list
            List of node indices representing the random walk
        """
        walk = [start_node]

        while len(walk) < walk_length:
            cur = walk[-1]
            cur_nbrs = list(net[cur].indices)

            if len(cur_nbrs) > 0:
                # Randomly choose one of the neighbors
                walk.append(np.random.choice(cur_nbrs))
            else:
                # Dead end - terminate the walk
                break

        return walk

    return (random_walk,)


@app.cell
def _(A, g, random_walk):
    n_nodes = g.vcount()
    n_walkers_per_node = 10
    walk_length = 50
    walks = []
    for _i in range(n_nodes):
        for _ in range(n_walkers_per_node):
            walks.append(random_walk(A, _i, walk_length))
    print(f'Generated {len(walks)} random walks')
    print(f'Example walk: {walks[0][:10]}...')  # Show first 10 nodes of first walk
    return n_nodes, n_walkers_per_node, walk_length, walks


@app.cell
def _(Word2Vec, walks):
    model_1 = Word2Vec(walks, vector_size=32, window=3, min_count=1, sg=1, hs=1, workers=1)  # Dimension of the embedding vectors  # Maximum distance between current and predicted node  # Minimum frequency for a node to be included  # Use skip-gram model (vs CBOW)  # Use hierarchical softmax for training,
    return (model_1,)


@app.cell
def _(model_1, n_nodes, np):
    embedding = np.array([model_1.wv[_i] for _i in range(n_nodes)])
    print(f'Embedding matrix shape: {embedding.shape}')
    print(f'First node embedding (first 5 dimensions): {embedding[0][:5]}')
    return (embedding,)


@app.cell
def _(A, embedding, g, np, palette):
    import umap
    from bokeh.plotting import figure, show
    from bokeh.io import output_notebook
    from bokeh.models import ColumnDataSource, HoverTool
    reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=15, metric='cosine')
    # Reduce embeddings to 2D
    xy = reducer.fit_transform(embedding)
    output_notebook()
    _degrees = A.sum(axis=1).A1
    source = ColumnDataSource(data=dict(x=xy[:, 0], y=xy[:, 1], size=np.sqrt(_degrees / np.max(_degrees)) * 30, community=[palette[label] for label in g.vs['label']]))
    _p = figure(title='DeepWalk Node Embeddings (UMAP projection)', x_axis_label='UMAP 1', y_axis_label='UMAP 2')
    # Calculate node degrees for visualization
    _p.scatter('x', 'y', size='size', source=source, line_color='black', color='community')
    # Create interactive plot
    show(_p)
    return ColumnDataSource, HoverTool, figure, output_notebook, show, umap


@app.cell
def _(embedding):
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    def find_optimal_clusters(embedding, n_clusters_range=(2, 10)):
        """
        Find the optimal number of clusters using silhouette score.

        The silhouette score measures how well each node fits within its cluster
        compared to other clusters. Scores range from -1 to 1, where higher is better.
        """
        silhouette_scores = []

        for n_clusters in range(*n_clusters_range):
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(embedding)
            score = silhouette_score(embedding, cluster_labels)
            silhouette_scores.append((n_clusters, score))
            print(f"k={n_clusters}: silhouette score = {score:.3f}")

        # Select the number of clusters with highest silhouette score
        optimal_k = max(silhouette_scores, key=lambda x: x[1])[0]
        print(f"\nOptimal number of clusters: {optimal_k}")

        # Perform final clustering with optimal k
        kmeans = KMeans(n_clusters=optimal_k, random_state=42)
        return kmeans.fit_predict(embedding)

    # Find clusters
    cluster_labels = find_optimal_clusters(embedding)
    return cluster_labels, find_optimal_clusters


@app.cell
def _(cluster_labels, g, igraph, sns):
    # Visualize the clustering results
    cmap = sns.color_palette().as_hex()
    igraph.plot(
        g,
        vertex_color=[cmap[label] for label in cluster_labels],
        bbox=(500, 500),
        vertex_size=20
    )
    return


@app.cell
def _(np):
    def node2vec_random_walk(net, start_node, walk_length, p, q):
        """
        Generate a biased random walk for node2vec.

        Parameters:
        -----------
        net : sparse matrix
            Adjacency matrix of the network
        start_node : int
            Starting node for the walk
        walk_length : int
            Length of the walk
        p : float
            Return parameter (controls likelihood of returning to previous node)
        q : float
            In-out parameter (controls BFS vs DFS behavior)

        Returns:
        --------
        walk : list
            List of node indices representing the biased random walk
        """
        walk = [start_node]
        while len(walk) < walk_length:
            cur = walk[-1]
            cur_nbrs = list(net[cur].indices)
            if len(cur_nbrs) > 0:
                if len(walk) == 1:
                    walk.append(np.random.choice(cur_nbrs))
                else:
                    prev = walk[-2]  # First step: uniform random choice
                    next_node = biased_choice(net, cur_nbrs, prev, _p, q)
                    walk.append(next_node)
            else:  # Subsequent steps: biased choice based on p and q
                break
        return walk

    def biased_choice(net, neighbors, prev, p, q):
        """
        Choose the next node with bias controlled by p and q.

        The transition probability is:
        - 1/p if returning to the previous node
        - 1   if moving to a neighbor of the previous node (distance 1)
        - 1/q if moving away from the previous node (distance 2)
        """
        unnormalized_probs = []
        for neighbor in neighbors:
            if neighbor == prev:
                unnormalized_probs.append(1 / _p)
            elif neighbor in net[prev].indices:
                unnormalized_probs.append(1.0)
            else:
                unnormalized_probs.append(1 / q)
        norm_const = sum(unnormalized_probs)
        normalized_probs = [prob / norm_const for prob in unnormalized_probs]  # Returning to previous node
        return np.random.choice(neighbors, p=normalized_probs)  # Moving to a common neighbor (BFS-like)  # Moving away from previous node (DFS-like)  # Normalize probabilities  # Sample next node

    return (node2vec_random_walk,)


@app.cell
def _(A, n_nodes, n_walkers_per_node, node2vec_random_walk, walk_length):
    # Generate biased random walks
    _p = 1.0  # Return parameter
    q = 0.1  # In-out parameter (q < 1 means DFS-like)
    walks_node2vec = []
    for _i in range(n_nodes):
        for _ in range(n_walkers_per_node):
            walks_node2vec.append(node2vec_random_walk(A, _i, walk_length, _p, q))
    print(f'Generated {len(walks_node2vec)} biased random walks')
    print(f'Example walk: {walks_node2vec[0][:10]}...')
    return (walks_node2vec,)


@app.cell
def _(Word2Vec, n_nodes, np, walks_node2vec):
    # Train node2vec model
    model_node2vec = Word2Vec(walks_node2vec, vector_size=32, window=3, min_count=1, sg=1, hs=1)
    embedding_node2vec = np.array([model_node2vec.wv[_i] for _i in range(n_nodes)])
    # Extract embeddings
    print(f'Node2vec embedding shape: {embedding_node2vec.shape}')
    return (embedding_node2vec,)


@app.cell
def _(
    A,
    ColumnDataSource,
    HoverTool,
    embedding_node2vec,
    figure,
    g,
    n_nodes,
    np,
    output_notebook,
    palette,
    show,
    umap,
):
    # Reduce node2vec embeddings to 2D
    reducer_n2v = umap.UMAP(n_components=2, random_state=42, n_neighbors=15, metric='cosine')
    xy_n2v = reducer_n2v.fit_transform(embedding_node2vec)
    output_notebook()
    _degrees = A.sum(axis=1).A1
    source_n2v = ColumnDataSource(data=dict(x=xy_n2v[:, 0], y=xy_n2v[:, 1], size=np.sqrt(_degrees / np.max(_degrees)) * 30, community=[palette[label] for label in g.vs['label']], name=[str(_i) for _i in range(n_nodes)]))
    p_n2v = figure(title='Node2vec Embeddings (UMAP projection)', x_axis_label='UMAP 1', y_axis_label='UMAP 2')
    p_n2v.scatter('x', 'y', size='size', source=source_n2v, line_color='black', color='community')
    hover = HoverTool()
    hover.tooltips = [('Node', '@name'), ('Community', '@community')]
    p_n2v.add_tools(hover)
    show(p_n2v)
    return


@app.cell
def _(embedding_node2vec, find_optimal_clusters, g, igraph, n_nodes, palette):
    # Find optimal clusters for node2vec embeddings
    cluster_labels_n2v = find_optimal_clusters(embedding_node2vec)
    # Visualize the clustering results
    igraph.plot(g, vertex_color=[palette[label] for label in cluster_labels_n2v], bbox=(500, 500), vertex_size=20, vertex_label=[str(_i) for _i in range(n_nodes)])
    return


if __name__ == "__main__":
    app.run()

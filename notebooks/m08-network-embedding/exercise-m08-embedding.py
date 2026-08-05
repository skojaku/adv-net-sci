import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/skojaku/adv-net-sci/blob/main/notebooks/exercise-m08-embedding.ipynb)

    # M09: Embedding

    ## Data
    """)
    return


@app.cell
def _():
    import numpy as np
    import networkx as nx
    import matplotlib.pyplot as plt
    import seaborn as sns
    G = nx.karate_club_graph()
    # Create a small example network
    A = nx.adjacency_matrix(G).toarray()
    labels = np.unique([_d[1]['club'] for _d in G.nodes(data=True)], return_inverse=True)[1]
    _cmap = sns.color_palette()
    nx.draw(G, with_labels=False, node_color=[_cmap[_i] for _i in labels])
    return A, G, labels, np, nx, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Section 1: Compute the eigenvectors and eigenvalues of A

    To compute the eigenvectors and eigenvalues of the adjacency matrix A, we can use the `np.linalg.eig` function from NumPy.

    ```python
    import numpy as np
    eigvals, eigvecs = np.linalg.eig(A)
    ```

    This function returns two arrays:
    - `eigvals`: An array of eigenvalues
    - `eigvecs`: An array where each column is an eigenvector

    To find the $d$ largest eigenvalues, we sort the eigenvectors by their corresponding eigenvalues in descending order:
    ```python
    idx = eigvals.argsort()[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]
    ```

    Now you have the eigenvectors and eigenvalues of A, which can be used for spectral embedding.
    """)
    return


@app.cell
def _(A, np):
    # Compute the spectral decomposition
    _eigvals, eigvecs = np.linalg.eig(A)
    _d = 2
    # Find the top d eigenvectors
    _sorted_indices = np.argsort(_eigvals)[::-1][:_d]
    _eigvals = _eigvals[_sorted_indices]
    eigvecs = eigvecs[:, _sorted_indices]
    return


@app.cell
def _(labels, plt, sns):
    _x = ...
    _y = ...
    _fig, _ax = plt.subplots(figsize=(7, 5))
    sns.scatterplot(x=_x, y=_y, hue=labels, ax=_ax)
    _ax.set_title('Spectral Embedding')
    _ax.set_xlabel('Eigenvector 1')
    _ax.set_ylabel('Eigenvector 2')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Section 2: Compute the Laplacian matrix and its eigenvectors

    1. Define the Laplacian matrix as

    $$
    \mathbf{L} = \begin{bmatrix}
    k_1 & -A_{12} & \cdots & -A_{1n} \\
    -A_{21} & k_2 & \cdots & -A_{2n} \\
    \vdots & \vdots & \ddots & \vdots \\
    -A_{n1} & -A_{n2} & \cdots & k_n
    \end{bmatrix}
    $$

    $$
    L = D - A
    $$

    where $D$ is the degree matrix.

    $$
    D = \begin{bmatrix}
    k_1 & 0 & \cdots & 0 \\
    0 & k_2 & \cdots & 0 \\
    \vdots & \vdots & \ddots & \vdots \\
    0 & 0 & \cdots & k_n
    \end{bmatrix}
    $$

    2. Compute the smallest, second smallest, and third smallest eigenvalues and their corresponding eigenvectors.

    3. Confirm that the smallest eigenvector is parallel to the all-ones vector.

    4. Confirm that the second smallest eigenvector is orthogonal to the all-ones vector.

    5. Form a 2D embedding using the second and third smallest eigenvectors and plot it.
    """)
    return


@app.cell
def _(A, np):
    deg = np.sum(A, axis=1).ravel()
    D = np.diag(deg)
    L = D - A
    _eigvals, eigvecs_1 = np.linalg.eig(L)
    _d = 3
    _sorted_indices = np.argsort(_eigvals)[:_d]
    _eigvals = _eigvals[_sorted_indices]
    eigvecs_1 = eigvecs_1[:, _sorted_indices]
    return (eigvecs_1,)


@app.cell
def _(A, eigvecs_1, np):
    import pandas as pd
    N = A.shape[0]
    # Confirm that the smallest eigenvector is parallel to the all-ones vector (i.e., x1.T @ np.ones(N) == 0)
    v = np.ones(N)
    v = v / np.linalg.norm(v)
    pd.DataFrame({'eigvec': eigvecs_1[:, 0], 'v': v})
    return pd, v


@app.cell
def _(eigvecs_1, v):
    # Confirm that the second smallest eigenvector is orthogonal to the all-ones vector (i.e., x2.T @ x1 = 0)
    eigvecs_1[:, 1].T @ v
    return


@app.cell
def _(eigvecs_1, labels, plt, sns):
    _x = eigvecs_1[:, 1]
    _y = eigvecs_1[:, 2]
    _fig, _ax = plt.subplots(figsize=(7, 5))
    sns.scatterplot(x=_x, y=_y, hue=labels, ax=_ax)
    _ax.set_title('Spectral Embedding')
    _ax.set_xlabel('Eigenvector 1')
    _ax.set_ylabel('Eigenvector 2')
    plt.show()
    return


@app.cell
def _(G, kmeans, nx, sns):
    from sklearn.cluster import KMeans
    _cmap = sns.color_palette()
    # kmeans = KMeans(n_clusters=4, n_init = 100)
    # kmeans.fit(eigvecs[:, 1:2])
    # kmeans.labels_
    # sns.scatterplot(x = x, y = y, hue=kmeans.labels_, palette = cmap)
    nx.draw(G, with_labels=False, node_color=[_cmap[_i] for _i in kmeans.labels_])
    return (KMeans,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Section 3: Generate an embedding based on the normalized cut

    1. Express the normalized cut objective function in terms of vector $x$ and a matrix $M$ (Hint: $M$ is something we already learned)

    2. Compute the eigenvectors and eigenvalues of $M$

    3. Form a 2D embedding and plot it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Section 4: Modularity-based embedding

    1. Compute the modularity matrix $Q$

    2. Compute the eigenvectors and eigenvalues of $Q$

    3. Form a 2D embedding and plot it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Section 5: Word2Vec
    """)
    return


@app.cell
def _():
    import gensim
    import gensim.downloader
    from gensim.models import Word2Vec
    import urllib.request
    # Load pre-trained word2vec model from Google News
    # Load a smaller pre-trained model for faster loading
    import os
    model_path = 'GoogleNews-vectors-negative300-SLIM.bin.gz'
    if not os.path.exists(model_path):
    # Download the model if it doesn't exist
        url = 'https://github.com/eyaler/word2vec-slim/raw/master/GoogleNews-vectors-negative300-SLIM.bin.gz'
        print('Downloading model...')
        urllib.request.urlretrieve(url, model_path)
        print('Download complete')
    # Load the model using gensim
    # model = gensim.downloader.load('word2vec-google-news-300')  # Higher quality 300-dim embeddings trained on Google News
    model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
    return Word2Vec, model


@app.cell
def _(model):
    # Example usage
    word = "bank"
    similar_words = model.most_similar(word)
    print(f"Words most similar to '{word}':")
    for similar_word, similarity in similar_words:
        print(f"{similar_word}: {similarity:.4f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A cool (yet controversial) application of word embeddings is analogy solving. Let us consider the following puzzle:

    > man is to woman as king is to ___ ?
    """)
    return


@app.cell
def _(model):
    # We solve the puzzle by
    #
    #  vec(king) - vec(man) + vec(woman)
    #
    # To solve this, we use the model.most_similar function, with positive words being "king" and "woman" (additive), and negative words being "man" (subtractive).
    #
    model.most_similar(positive=["usd", "us"], negative=["usa"], topn=5)
    return


@app.cell
def _(model, np, pd, plt, sns):
    from sklearn.decomposition import PCA
    word_group_A = ['Germany', 'France', 'Italy', 'Spain', 'Portugal', 'Greece']
    word_group_B = ['Berlin', 'Paris', 'Rome', 'Madrid', 'Lisbon', 'Athens']
    country_embeddings = np.array([model[country] for country in word_group_A])
    capital_embeddings = np.array([model[capital] for capital in word_group_B])
    pca = PCA(n_components=2)
    embeddings = np.vstack([country_embeddings, capital_embeddings])
    embeddings_pca = pca.fit_transform(embeddings)
    df = pd.DataFrame(embeddings_pca, columns=['PC1', 'PC2'])
    df['Label'] = word_group_A + word_group_B
    df['Type'] = ['Country'] * len(word_group_A) + ['Capital'] * len(word_group_B)
    plt.figure(figsize=(12, 10))
    scatter_plot = sns.scatterplot(data=df, x='PC1', y='PC2', hue='Type', style='Type', s=200, palette='deep', markers=['o', 's'])
    for _i in range(len(df)):
        plt.text(df['PC1'][_i], df['PC2'][_i] + 0.08, df['Label'][_i], fontsize=12, ha='center', va='bottom', bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))
    for _i in range(len(word_group_A)):
        plt.arrow(df['PC1'][_i], df['PC2'][_i], df['PC1'][_i + len(word_group_A)] - df['PC1'][_i], df['PC2'][_i + len(word_group_A)] - df['PC2'][_i], color='gray', alpha=0.6, linewidth=1.5, head_width=0.02, head_length=0.03)
    plt.legend(title='Type', title_fontsize='13', fontsize='11')
    plt.title('PCA of Country and Capital Word Embeddings', fontsize=16)
    plt.xlabel('Principal Component 1', fontsize=14)
    plt.ylabel('Principal Component 2', fontsize=14)
    _ax = plt.gca()
    _ax.set_axis_off()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Section 6:

    ## Preparation: DeepWalk

    Let us implement DeepWalk from scratch based on the following steps:

    1. Generate random walks of length l per node
    2. Feed walks to Word2Vec
    3. Use skip-gram with hierarchical softmax

    Let's implement the above steps in the following cell.
    """)
    return


@app.cell
def _(A, np):
    from scipy import sparse

    def random_walk(net, start_node, walk_length):
        walk = [start_node]
        while len(walk) < _walk_length:
            cur = walk[-1]
            cur_nbrs = list(net[cur].indices)
            if len(cur_nbrs) > 0:
                walk.append(np.random.choice(cur_nbrs))
            else:
                break
        return walk
    A_1 = sparse.csr_matrix(A)
    random_walk(A_1, 0, 5)
    return A_1, random_walk, sparse


@app.cell
def _(A_1, random_walk):
    n_nodes = A_1.shape[0]
    _n_walkers_per_node = 10
    _walk_length = 50
    walks = []
    for _i in range(n_nodes):
        for _ in range(_n_walkers_per_node):
            walks.append(random_walk(A_1, _i, _walk_length))
    return n_nodes, walks


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Then, we feed the random walks to the word2vec model.
    """)
    return


@app.cell
def _(Word2Vec, walks):
    model_1 = Word2Vec(walks, vector_size=32, window=3, min_count=1, sg=1, hs=1)
    return (model_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here,

    - `vector_size` is the dimension of the embedding vectors.
    - `window` indicates the maximum distance between a word and its context words. For example, in the random walk `[0, 1, 2, 3, 4, 5, 6, 7]`, the context words of node 2 are `[0, 1, 3, 4, 5]` when `window=3`.
    - `min_count` is the minimum number of times a word must appear in the training data to be included in the vocabulary.

    Two parameters `sg=1` and `hs=1` indicate that we are using the skip-gram model with negative sampling. If you are interested in the details, please refer to the lecture note.

    Let's get the embeddings of the nodes.
    """)
    return


@app.cell
def _(model_1, n_nodes, np):
    embedding = []
    for _i in range(n_nodes):
        embedding.append(model_1.wv[_i])
    embedding = np.array(embedding)
    embedding[:3]
    return (embedding,)


@app.cell
def _(model_1):
    model_1
    return


@app.cell
def _():
    # ! pip install umap-learn # uncomment this if you are running this notebook on colab
    return


@app.cell
def _(A_1, embedding, labels, np, sns):
    import umap
    from bokeh.plotting import figure, show
    from bokeh.io import output_notebook
    from bokeh.models import ColumnDataSource, HoverTool
    _reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=15, metric='cosine')
    _xy = _reducer.fit_transform(embedding)
    output_notebook()
    _degrees = A_1.sum(axis=1).A1
    _palette = sns.color_palette().as_hex()
    _source = ColumnDataSource(data=dict(x=_xy[:, 0], y=_xy[:, 1], size=np.sqrt(_degrees / np.max(_degrees)) * 30, community=[_palette[label] for label in labels]))
    _p = figure(title='Node Embeddings from Word2Vec', x_axis_label='X', y_axis_label='Y')
    _p.scatter('x', 'y', size='size', source=_source, line_color='black', color='community')
    show(_p)
    return ColumnDataSource, figure, output_notebook, show, umap


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One of the interesting applications with node embeddings is clustering. While we have good community detection methods, like the modularity maximization and stochastic block model, we can use clustering methods from machine learning, such as $K$-means and Gaussian mixture model. Let's see what we can get from the node embeddings.
    """)
    return


@app.cell
def _(KMeans):
    from sklearn.metrics import silhouette_score

    def Kmeans_with_silhouette(embedding, n_clusters_range=(2, 10)):
        silhouette_scores = []
        for n_clusters in range(*n_clusters_range):
            kmeans = KMeans(n_clusters=n_clusters)
            kmeans.fit(embedding)
            score = silhouette_score(embedding, kmeans.labels_)
            silhouette_scores.append((n_clusters, score))
        optimal_n_clusters = max(silhouette_scores, key=lambda x: _x[1])[0]
        kmeans = KMeans(n_clusters=optimal_n_clusters)
        kmeans.fit(embedding)
        return kmeans.labels_

    return (Kmeans_with_silhouette,)


@app.cell
def _(G, Kmeans_with_silhouette, embedding, nx, plt, sns):
    _detected_labels = Kmeans_with_silhouette(embedding)
    _cmap = sns.color_palette().as_hex()
    plt.figure(figsize=(8, 8))
    nx.draw(G, node_color=[_cmap[label] for label in _detected_labels], with_labels=False, node_size=100)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercise: Node2Vec

    Implement Node2Vec from scratch based on the following steps:

    1. Generate biased random walks of length l per node
    2. Feed walks to Word2Vec
    3. Use skip-gram with negative sampling by setting `sg=1` and `hs=0` for the Word2Vec model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    node2vec uses biased random walks that can move in different directions. The bias walk is parameterized by two parameters, $p$ and $q$:

    $$
    P(v_{t+1} = x | v_t = v, v_{t-1} = t) \propto
    \begin{cases}
    \frac{1}{p} & \text{if } d(v,t) = 0 \\
    1 & \text{if } d(v,t) = 1 \\
    \frac{1}{q} & \text{if } d(v,t) = 2 \\
    \end{cases}
    $$
    """)
    return


@app.cell
def _(A_1, np, sparse):
    def node2vec_random_walk(net, start_node, walk_length, p, q):
        """
        Sample a random walk starting from start_node.
        """
        walk = [start_node]
        prev = -1
        while len(walk) < _walk_length:
            cur = walk[-1]
            cur_nbrs = list(net[cur].indices)
            if prev == -1:
                next_node = np.random.choice(cur_nbrs)
                walk.append(next_node)
                prev = cur
                continue
            prev_nbrs = list(net[prev].indices)
            common_nbrs = list(set(cur_nbrs) & set(prev_nbrs))
            non_common_nbrs = list(set(cur_nbrs) - set(prev_nbrs))
            neighbors = [prev] + common_nbrs + non_common_nbrs
            prob = [1 / _p] + [1] * len(common_nbrs) + [1 / q] * len(non_common_nbrs)
            prob = np.array(prob) / sum(prob)
            next_node = np.random.choice(neighbors, p=prob)
            walk.append(next_node)
            prev = cur
        return walk
    A_2 = sparse.csr_matrix(A_1)
    node2vec_random_walk(A_2, 0, 5, p=1, q=0.1)
    return A_2, node2vec_random_walk


@app.cell
def _(A_2, Word2Vec, node2vec_random_walk, np):
    walks_1 = []
    _p = 0.1
    q = 2
    n_nodes_1 = A_2.shape[0]
    _n_walkers_per_node = 10
    _walk_length = 50
    walks_1 = []
    for _i in range(n_nodes_1):
        for _ in range(_n_walkers_per_node):
            walks_1.append(node2vec_random_walk(A_2, _i, _walk_length, _p, q))
    model_2 = Word2Vec(walks_1, vector_size=32, window=3, min_count=1, sg=1, hs=1)
    embedding_1 = []
    for _i in range(n_nodes_1):
        embedding_1.append(model_2.wv[_i])
    embedding_1 = np.array(embedding_1)
    return (embedding_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Plot the node embeddings using UMAP.
    """)
    return


@app.cell
def _(
    A_2,
    ColumnDataSource,
    embedding_1,
    figure,
    labels,
    np,
    output_notebook,
    show,
    sns,
    umap,
):
    _reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=15, metric='cosine')
    _xy = _reducer.fit_transform(embedding_1)
    output_notebook()
    _degrees = A_2.sum(axis=1).A1
    _palette = sns.color_palette().as_hex()
    _source = ColumnDataSource(data=dict(x=_xy[:, 0], y=_xy[:, 1], size=np.sqrt(_degrees / np.max(_degrees)) * 30, community=[_palette[label] for label in labels]))
    _p = figure(title='Node Embeddings from Word2Vec', x_axis_label='X', y_axis_label='Y')
    _p.scatter('x', 'y', size='size', source=_source, line_color='black', color='community')
    show(_p)
    return


@app.cell
def _(G, Kmeans_with_silhouette, embedding_1, nx, plt, sns):
    _detected_labels = Kmeans_with_silhouette(embedding_1)
    _cmap = sns.color_palette().as_hex()
    plt.figure(figsize=(8, 8))
    nx.draw(G, node_color=[_cmap[label] for label in _detected_labels], with_labels=False, node_size=100)
    plt.show()
    return


if __name__ == "__main__":
    app.run()

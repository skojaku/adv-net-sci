# /// script
# dependencies = ["cairocffi", "fastnode2vec @ git+https://github.com/skojaku/fastnode2vec.git", "igraph", "pycairo", "python-igraph"]
# ///

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
    <a href="https://colab.research.google.com/github/skojaku/adv-net-sci/blob/main/notebooks/m08-network-embedding/node2vec_demo.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
    """)
    return


@app.cell
def _():
    # packages added via marimo's package management: git+https://github.com/skojaku/fastnode2vec.git !pip install git+https://github.com/skojaku/fastnode2vec.git
    # Using pip (with plotting support)
    # packages added via marimo's package management: igraph cairocffi pycairo python-igraph !pip install igraph cairocffi pycairo python-igraph
    return


@app.cell
def _():
    import gensim
    import igraph as ig
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    return ig, np, plt, sns


@app.cell
def _(ig, np, sns):
    # Load the karate club network
    g = ig.Graph.Famous('Zachary')
    A = g.get_adjacency_sparse()
    labels = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    # Get community labels (Mr. Hi = 0, Officer = 1)
    g.vs['label'] = labels
    _palette = sns.color_palette().as_hex()
    # Visualize the network
    ig.plot(g, vertex_color=[_palette[label] for label in labels], bbox=(300, 300))
    return g, labels


@app.cell
def _():
    emb = ...
    return (emb,)


@app.cell
def _(emb):
    emb
    return


@app.cell
def _(emb, labels, plt, sns):
    from sklearn.decomposition import PCA

    pca = PCA(n_components=2)
    xy = pca.fit_transform(emb)

    sns.set_style("white")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax = sns.scatterplot(x=xy[:, 0], y=xy[:, 1], s=100, hue=labels)
    ax.set_xticks([])
    ax.set_yticks([])
    sns.despine()
    return


@app.cell
def _(emb, g, ig, labels, sns):
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=3, random_state=0).fit(emb)
    detected_labels = kmeans.labels_
    _palette = sns.color_palette().as_hex()
    # Visualize the network
    ig.plot(g, vertex_color=[_palette[label] for label in detected_labels], vertex_label=list(labels), bbox=(300, 300))
    return


@app.cell
def _(ig):
    import networkx as nx

    h = ig.Graph.from_networkx(nx.les_miserables_graph())
    A_lesmis = h.get_adjacency_sparse()
    return


if __name__ == "__main__":
    app.run()

# %%
import numpy as np
from scipy import sparse

def random_walk(net, start_node, walk_length):
    """
    Sample a random walk starting from start_node.

    Parameters
    ----------
    net : scipy.sparse.csr_matrix
        Adjacency matrix of the network.
    start_node : int
        The node to start the random walk from.
    walk_length : int
        The length of the random walk.

    Returns
    -------
    walk : list
        A list containing the nodes in the random walk, starting from start_node.
    """
    walk = [start_node]
    current_node = start_node
    for _ in range(walk_length - 1):
        current_node = np.random.choice(net.indices[net.indptr[current_node]:net.indptr[current_node + 1]])
        walk.append(current_node)
    return walk
# %%
import pandas as pd
from scipy import sparse

data_url = "https://raw.githubusercontent.com/skojaku/adv-net-sci/refs/heads/main/docs/lecture-note/assets/data/lesmis/"
node_table = pd.read_csv(data_url + "node_table.csv")
edge_table = pd.read_csv(data_url + "edge_table.csv")

# Get the names of the nodes
node_names = node_table["name"].values

rows, cols = edge_table["src"].values, edge_table["trg"].values
weight = edge_table["weight"].values
nrows, ncols = node_table.shape[0], node_table.shape[0]
A = sparse.csr_matrix(
    (weight, (rows, cols)),
    shape=(nrows, ncols),
)
A = A + A.T
n_walkers_per_node = 10
walk_length = 50
walks = []
for i in range(nrows):
    walks.append(random_walk(A, i, walk_length))
# %%
from gensim.models import Word2Vec

model = Word2Vec(walks, vector_size=32, window=5, min_count=1, sg=0, hs = 1)
# %%
import umap

reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=5, metric="cosine")
xy = reducer.fit_transform(model.wv.vectors)
# %%
import matplotlib.pyplot as plt
import seaborn as sns
fig, ax = plt.subplots(figsize=(5, 5))
sns.scatterplot(x=xy[:, 0], y=xy[:, 1], ax=ax)
ax.axis("off")

# %%# Bokeh
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource, HoverTool

output_notebook()

# Calculate the degree of each node
degrees = A.sum(axis=1).A1

source = ColumnDataSource(data=dict(
    x=xy[:, 0],
    y=xy[:, 1],
    name=node_names,
    size=np.sqrt(degrees / np.max(degrees)) * 30

))

p = figure(title="Node Embeddings from Word2Vec", x_axis_label="X", y_axis_label="Y")
p.scatter('x', 'y', size='size', source=source)

hover = HoverTool()
hover.tooltips = [("Node", "@name"), ("Degree", "@size")]
p.add_tools(hover)

show(p)

# %%

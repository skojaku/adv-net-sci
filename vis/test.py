# %%
import networkx as nx
import numpy as np
G = nx.karate_club_graph()
A = nx.adjacency_matrix(G)
labels = np.unique([d[1]['club'] for d in G.nodes(data=True)], return_inverse=True)[1]
print(labels)

# %%

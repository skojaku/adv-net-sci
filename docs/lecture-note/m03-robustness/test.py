# %%
from scipy import sparse
import numpy as np

A = [
    [0, 2, 8, 12, 4, 10, 14, 6, 16],
    [2, 0, 3, 2, 1, 5, 11, 15, 7],
    [8, 3, 0, 4, 10, 14, 6, 12, 16],
    [12, 9, 4, 0, 5, 11, 15, 7, 13],
    [4, 13, 10, 5, 0, 6, 12, 16, 8],
    [10, 5, 14, 11, 6, 0, 7, 13, 9],
    [14, 11, 6, 15, 12, 7, 0, 8, 10],
    [6, 15, 12, 7, 16, 13, 8, 0, 11],
    [16, 7, 16, 13, 8, 9, 10, 11, 0]
]

A = np.array(A)
A = np.triu(A)
A = sparse.csr_matrix(A + A.T)
Tcsr = sparse.csgraph.minimum_spanning_tree(A).toarray()
print(Tcsr + Tcsr.T)
import networkx as nx

G = nx.from_numpy_array(A)
T = nx.minimum_spanning_tree(G)
print(T.size(weight="weight"))
nx.draw(T, with_labels=True)
# %%
print(A.toarray())

# %%

# %%
import networkx as nx
import numpy as np
G = nx.karate_club_graph()
A = nx.adjacency_matrix(G)
labels = np.unique([d[1]['club'] for d in G.nodes(data=True)], return_inverse=True)[1]

# Probability matrix
deg = np.sum(A, axis=1)
P = np.diag(1/deg) @ A

# Normalized adjacency matrix
A_norm = np.diag(1/np.sqrt(deg)) @ A @ np.diag(1/np.sqrt(deg))

# Eigenvalues and eigenvectors
evals= np.linalg.eigvals(P)
evals_norm = np.linalg.eigvals(A_norm)
print(evals)
print(evals_norm)
# %%

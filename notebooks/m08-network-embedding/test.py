#%% Loading
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt
import seaborn as sns 


A = ig.Graph.Famous("Zachary").get_adjacency_sparse()

#%% Compute the Laplacian and normalized Laplacian -----------
n_nodes = A.shape[0]
deg = np.array(A.sum(axis=1)).reshape(-1)
D = np.diag(deg)  # Degree matrix
Dsqrt_inv = np.diag(1.0 / np.sqrt(deg + 1e-10))

# Laplacian
L = D - A

# Normalized Laplacian
Ln = np.eye(n_nodes) - Dsqrt_inv @ A.toarray() @ Dsqrt_inv

#%% Eigenvalue decomposition -----------
eigvals_L, eigvecs_L = np.linalg.eig(L)
eigvals_Ln, eigvecs_Ln = np.linalg.eig(Ln)

# Keep only real parts
eigvals_L, eigvecs_L = np.real(eigvals_L), np.real(eigvecs_L) 
eigvals_Ln, eigvecs_Ln = np.real(eigvals_Ln), np.real(
    eigvecs_Ln
)

# Sort eigenvalues and eigenvectors
order = np.argsort(eigvals_L)
eigvals_L, eigvecs_L = eigvals_L[order], eigvecs_L[:, order]

order = np.argsort(eigvals_Ln)
eigvals_Ln, eigvecs_Ln = eigvals_Ln[order], eigvecs_Ln[:, order]


#%% Visualize the eigenvectors -----------
%%matplotlib

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
sns.heatmap(eigvecs_L, cmap="coolwarm", center =0, ax=axes[0])
sns.heatmap(eigvecs_Ln, cmap="coolwarm", center =0, ax=axes[1])

axes[0].set_title("Eigenvectors of Laplacian L")
axes[1].set_title("Eigenvectors of Normalized Laplacian Ln")


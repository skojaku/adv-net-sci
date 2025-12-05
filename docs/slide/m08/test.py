# %% Import a graph
import numpy as np 
import igraph as ig 

A = ig.Graph.Famous("Zachary").get_adjacency_sparse()
A = A.toarray()

# %% Compute the eigenvectors and eigenvalues

eigvals, eigvecs = np.linalg.eig(A)
eigvals, eigvecs = np.real(eigvals), np.real(eigvecs)

# %% Compute the reconstructed adjacency matrix and the error 

Arecon = np.zeros_like(A)
error_list = []
basis_matrices = []

for i in range(5): 
    # Take the i-th eigenvalue and eigenvector
    u = eigvecs[:, i].reshape((-1,1))
    s = eigvals[i]

    # Compute the basis matrix 
    B = u @ u.T

    # Update the reconstructed adjacency matrix
    Arecon = Arecon + s * B 
    error = np.linalg.norm(A - Arecon, ord='fro')
    error_list.append(error)

    basis_matrices.append(B)

# %% Plot the error decay 
%matplotlib 
import matplotlib.pyplot as plt
import seaborn as sns 

fig, ax = plt.subplots(figsize=(6,4))

sns.lineplot(x = np.arange(1, len(error_list)+1), y = error_list, marker='o', ax=ax)
ax.set_xlabel("Number of basis matrices")
ax.set_ylabel("Reconstruction error (Frobenius norm)")


# %% Plot the reconstructed adjacency matrix 
n_matrices = len(basis_matrices)
n_cols = 3
fig, axes = plt.subplots(n_matrices // n_cols + 1, n_cols, figsize=(12, 12))

for i in range(n_matrices):
    ax = axes.flatten()[i]
    sns.heatmap(basis_matrices[i], ax=ax, cbar=False, center = 0, cmap ='coolwarm')
    ax.set_title(f"Basis Matrix {i+1}")

plt.tight_layout()

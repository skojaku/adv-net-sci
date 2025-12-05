# %% Construct a graph
import matplotlib.pyplot as plt
import numpy as np
import igraph as ig

A = ig.Graph.Famous("Zachary").get_adjacency_sparse()


# %% Compute the eigenvalues and eigenvectors

eigvals, eigvecs = np.linalg.eig(A.toarray())
eigvals, eigvecs = np.real(eigvals), np.real(eigvecs)

# %%

reconstruction_errors = []
reconstruction_matrices = []
reconstructed = np.zeros(A.shape)
for i in range(len(eigvals)):
    basisMatrix = eigvecs[:, i].reshape((-1, 1)) @ eigvecs[:, i].reshape((1, -1))

    reconstructed = reconstructed + eigvals[i] * basisMatrix

    # Compute the error
    error = np.linalg.norm(A.toarray() - reconstructed) ** 2

    reconstruction_errors.append(error)
    reconstruction_matrices.append(reconstructed.copy())

# %% Plot the results

import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(8, 5))

sns.lineplot(x=range(1, len(reconstruction_errors) + 1), y=reconstruction_errors, ax=ax)

# %% Plot the reconstructed matrices

fig, axes = plt.subplots(len(reconstruction_matrices) // 4, 4, figsize=(12, 15))

for i, ax in enumerate(axes.flatten()):

    sns.heatmap(reconstruction_matries[i], ax=ax, cbar=False, cmap="coolwarm", center=0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Using top {i} eigenvalues")

plt.tight_layout()
fig

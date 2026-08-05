# /// script
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "networkx",
#     "numpy",
#     "igraph",
#     "scipy",
#     "seaborn",
#     "torch",
#     "torch-geometric",
# ]
# [tool.marimo.display]
# default_width = "full"
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import igraph as ig
    import seaborn as sns
    import numpy as np
    from scipy import sparse
    import matplotlib.pyplot as plt
    import matplotlib as mpl

    G = ig.Graph.Famous("Zachary")
    A = G.get_adjacency_sparse()
    return A, G, ig, mpl, np, plt, sns, sparse


@app.cell
def _(A, np, sparse):
    # Compute Laplacian matrix
    _deg = np.array(A.sum(axis=1)).reshape(-1)
    D = sparse.diags(_deg)
    L = D - A
    evals, evecs = np.linalg.eigh(L.toarray())
    # Compute eigendecomposition
    order = np.argsort(evals)
    evals = evals[order]
    # Sort eigenvalues and eigenvectors
    evecs = evecs[:, order]
    return evals, evecs


@app.cell
def _(evals, evecs, np):
    alpha = 2
    L_low = evecs @ np.diag(1 / (1 + alpha * evals)) @ evecs.T
    L_high = evecs @ np.diag(alpha * evals / (1 + alpha * evals)) @ evecs.T

    print("Size of low-pass filter:", L_low.shape)
    print("Size of high-pass filter:", L_high.shape)
    return L_high, L_low


@app.cell
def _(A, L_high, L_low, np):
    # Random feature vector
    x = np.random.randn(A.shape[0], 1)

    # Convolve with low-pass filter
    x_low = L_low @ x

    # Convolve with high-pass filter
    x_high = L_high @ x
    return (x,)


@app.cell
def _(G, L_high, L_low, ig, mpl, np, plt, sns, x):
    _fig, _axes = plt.subplots(1, 3, figsize=(15, 5))
    _palette = sns.color_palette('viridis', as_cmap=True)
    _norm = mpl.colors.Normalize(vmin=-0.3, vmax=0.3)
    _values = x.reshape(-1)
    _values = _values / np.linalg.norm(_values)
    ig.plot(G, vertex_color=[_palette(_norm(x)) for x in _values], bbox=(0, 0, 500, 500), vertex_size=20, target=_axes[0])
    _axes[0].set_title('Original')
    _values = L_low @ x
    _values = _values / np.linalg.norm(_values)
    _values = _values.reshape(-1)
    ig.plot(G, vertex_color=[_palette(_norm(x)) for x in _values], bbox=(0, 0, 500, 500), vertex_size=20, target=_axes[1])
    _axes[1].set_title('Low-pass filter')
    _values = L_high @ x
    _values = _values / np.linalg.norm(_values)
    _values = _values.reshape(-1)
    ig.plot(G, vertex_color=[_palette(_norm(x)) for x in _values], bbox=(0, 0, 500, 500), vertex_size=20, target=_axes[2])
    _axes[2].set_title('High-pass filter')
    _fig.tight_layout()
    return


@app.cell
def _(G, L_high, L_low, ig, mpl, np, plt, sns):
    eigen_centrality = np.array(G.eigenvector_centrality()).reshape(-1, 1)
    low_pass_eigen = L_low @ eigen_centrality
    high_pass_eigen = L_high @ eigen_centrality
    _fig, _axes = plt.subplots(1, 3, figsize=(15, 5))
    _palette = sns.color_palette('viridis', as_cmap=True)
    _norm = mpl.colors.Normalize(vmin=-0, vmax=0.3)
    _values = eigen_centrality.reshape(-1)
    _values = _values / np.linalg.norm(_values)
    _values = _values.reshape(-1)
    ig.plot(G, vertex_color=[_palette(_norm(x)) for x in _values], bbox=(0, 0, 500, 500), vertex_size=20, target=_axes[0])
    _axes[0].set_title('Original')
    _values = low_pass_eigen.reshape(-1)
    _values = _values / np.linalg.norm(_values)
    _values = _values.reshape(-1)
    ig.plot(G, vertex_color=[_palette(_norm(x)) for x in _values], bbox=(0, 0, 500, 500), vertex_size=20, target=_axes[1])
    _axes[1].set_title('Low-pass filter')
    _values = high_pass_eigen.reshape(-1)
    _values = _values / np.linalg.norm(_values)
    ig.plot(G, vertex_color=[_palette(_norm(x)) for x in _values], bbox=(0, 0, 500, 500), vertex_size=20, target=_axes[2])
    _axes[2].set_title('High-pass filter')
    _fig.tight_layout()
    return


@app.cell
def _():
    import torch
    import torch.nn.functional as F
    from torch_geometric.nn import GCNConv
    from torch_geometric.data import Data

    return Data, F, GCNConv, torch


@app.cell
def _(np):
    import networkx as nx
    G_1 = nx.karate_club_graph()
    # Load the Karate Club network
    A_1 = nx.adjacency_matrix(G_1)
    membership = np.unique([d[1]['club'] for d in G_1.nodes(data=True)], return_inverse=True)[1]
    n_nodes = A_1.shape[0]
    # Get true community labels
    print(f'Number of nodes: {n_nodes}')
    print(f'Membership: {membership}')
    return A_1, membership, n_nodes


@app.cell
def _(A_1, n_nodes, np, sparse):
    _deg = np.array(A_1.sum(axis=1)).reshape(-1)
    D_inv_sqrt = sparse.diags(1.0 / np.sqrt(_deg))
    L_norm = sparse.eye(n_nodes) - D_inv_sqrt @ A_1 @ D_inv_sqrt
    evals_1, evecs_1 = np.linalg.eigh(L_norm.toarray())
    k = 5
    node_features = evecs_1[:, 1:k + 1]
    print(f'Node feature shape: {node_features.shape}')
    print(f'Feature matrix:\n{node_features[:5]}')
    return (node_features,)


@app.cell
def _(A_1, Data, membership, node_features, np, torch):
    # Convert adjacency matrix to edge list (COO format)
    edge_index = torch.tensor(np.array(A_1.nonzero()), dtype=torch.long)
    x_1 = torch.tensor(node_features, dtype=torch.float)
    # Convert node features to tensor
    y = torch.tensor(membership, dtype=torch.long)
    # Convert labels to tensor
    # Create PyTorch Geometric Data object
    data = Data(x=x_1, edge_index=edge_index, y=y)
    return (data,)


@app.cell
def _(data, membership, n_nodes, np, torch):
    # Create train/test masks
    # We'll label only 4 nodes (2 from each community) for training
    train_mask = torch.zeros(n_nodes, dtype=torch.bool)
    test_mask = torch.zeros(n_nodes, dtype=torch.bool)

    # Select 4 nodes from each class for training
    for label in [0, 1]:
        label_indices = np.where(membership == label)[0]
        train_indices = np.random.choice(label_indices, size=4, replace=False)
        train_mask[train_indices] = True

    # All other nodes are for testing
    test_mask = ~train_mask

    data.train_mask = train_mask
    data.test_mask = test_mask

    print(f"Number of training nodes: {train_mask.sum().item()}")
    print(f"Number of test nodes: {test_mask.sum().item()}")
    print(f"Training node indices: {torch.where(train_mask)[0].numpy()}")
    return (train_mask,)


@app.cell
def _(F, GCNConv, data, torch):
    class GCN(torch.nn.Module):
        def __init__(self, num_features, hidden_channels, num_classes):
            super(GCN, self).__init__()
            # First GCN layer: input features -> hidden dimension
            self.conv1 = GCNConv(num_features, hidden_channels)
            # Second GCN layer: hidden dimension -> output classes
            self.conv2 = GCNConv(hidden_channels, num_classes)

        def forward(self, x, edge_index):
            # First layer with ReLU activation
            x = self.conv1(x, edge_index)
            x = F.relu(x)
            x = F.dropout(x, p=0.5, training=self.training)

            # Second layer (no activation, we'll use softmax later)
            x = self.conv2(x, edge_index)
            return x

    # Initialize the model
    model = GCN(
        num_features=data.num_node_features,
        hidden_channels=16,
        num_classes=2
    )

    print(model)
    print(f"\nTotal parameters: {sum(p.numel() for p in model.parameters())}")
    return (model,)


@app.cell
def _(data, model, torch):
    # Set up optimizer and loss function
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    criterion = torch.nn.CrossEntropyLoss()

    # Training function
    def train():
        model.train()
        optimizer.zero_grad()

        # Forward pass
        out = model(data.x, data.edge_index)

        # Compute loss only on training nodes
        loss = criterion(out[data.train_mask], data.y[data.train_mask])

        # Backward pass
        loss.backward()
        optimizer.step()

        return loss.item()

    # Evaluation function
    def test():
        model.eval()
        with torch.no_grad():
            out = model(data.x, data.edge_index)
            pred = out.argmax(dim=1)

            # Calculate accuracy on train and test sets
            train_correct = pred[data.train_mask] == data.y[data.train_mask]
            test_correct = pred[data.test_mask] == data.y[data.test_mask]

            train_acc = int(train_correct.sum()) / int(data.train_mask.sum())
            test_acc = int(test_correct.sum()) / int(data.test_mask.sum())

        return train_acc, test_acc

    # Train the model
    losses = []
    train_accs = []
    test_accs = []

    for epoch in range(200):
        loss = train()
        train_acc, test_acc = test()

        losses.append(loss)
        train_accs.append(train_acc)
        test_accs.append(test_acc)

        if (epoch + 1) % 20 == 0:
            print(f'Epoch {epoch+1:03d}, Loss: {loss:.4f}, '
                  f'Train Acc: {train_acc:.4f}, Test Acc: {test_acc:.4f}')

    print(f'\nFinal Test Accuracy: {test_accs[-1]:.4f}')
    return losses, test_accs, train_accs


@app.cell
def _(losses, plt, test_accs, train_accs):
    _fig, _axes = plt.subplots(1, 2, figsize=(12, 4))
    _axes[0].plot(losses)
    # Plot loss
    _axes[0].set_xlabel('Epoch')
    _axes[0].set_ylabel('Loss')
    _axes[0].set_title('Training Loss')
    _axes[0].grid(True, alpha=0.3)
    _axes[1].plot(train_accs, label='Train')
    _axes[1].plot(test_accs, label='Test')
    # Plot accuracy
    _axes[1].set_xlabel('Epoch')
    _axes[1].set_ylabel('Accuracy')
    _axes[1].set_title('Train vs Test Accuracy')
    _axes[1].legend()
    _axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(data, ig, membership, model, n_nodes, np, plt, torch, train_mask):
    model.eval()
    with torch.no_grad():
        out = model(data.x, data.edge_index)
        predictions = out.argmax(dim=1).numpy()
    _fig, _axes = plt.subplots(1, 2, figsize=(14, 6))
    colors_true = ['#FF6B6B', '#4ECDC4']
    colors_pred = ['#FF6B6B', '#4ECDC4']
    vertex_colors_true = [colors_true[label] for label in membership]
    vertex_shapes = ['circle' if not train_mask[i] else 'square' for i in range(n_nodes)]
    vertex_sizes = [15 if not train_mask[i] else 25 for i in range(n_nodes)]
    G_2 = ig.Graph.Famous('Zachary')
    ig.plot(G_2, vertex_color=vertex_colors_true, vertex_shape=vertex_shapes, vertex_size=vertex_sizes, bbox=(0, 0, 500, 500), target=_axes[0])
    _axes[0].set_title('True Labels\n(Squares = Training Nodes)', fontsize=12, fontweight='bold')
    vertex_colors_pred = [colors_pred[pred] for pred in predictions]
    ig.plot(G_2, vertex_color=vertex_colors_pred, vertex_size=20, bbox=(0, 0, 500, 500), target=_axes[1])
    _axes[1].set_title('Predicted Labels', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.show()
    misclassified = np.where(predictions != membership)[0]
    print(f'\nMisclassified nodes: {misclassified}')
    print(f'Number of misclassified nodes: {len(misclassified)}')
    return


if __name__ == "__main__":
    app.run()

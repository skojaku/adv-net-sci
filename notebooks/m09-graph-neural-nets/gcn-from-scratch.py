# /// script
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "networkx",
#     "numpy",
#     "scikit-learn",
#     "scipy",
#     "seaborn",
#     "torch",
# ]
# [tool.marimo.display]
# default_width = "full"
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import scipy.sparse as sp
    import torch
    import torch.nn as nn
    import scipy.sparse.linalg as slinalg

    class BrunaGraphConv(nn.Module):
        """
        Bruna's Spectral Graph Convolution Layer

        This implementation follows the original formulation by Joan Bruna et al.,
        using the eigendecomposition of the graph Laplacian for spectral convolution.
        """

        def __init__(self, in_features, out_features, n_nodes):
            """
            Initialize the Bruna Graph Convolution layer

            Args:
                in_features (int): Number of input features
                out_features (int): Number of output features
            """
            super(BrunaGraphConv, self).__init__()
            self.in_features = in_features
            self.out_features = out_features
            self.weight = nn.Parameter(torch.FloatTensor(in_features, out_features, _n_nodes - 1))
            self.reset_parameters()

        def reset_parameters(self):
            """Initialize weights using Glorot initialization"""
            nn.init.xavier_uniform_(self.weight)

        @staticmethod
        def get_laplacian_eigenvectors(adj):
            """
            Compute eigendecomposition of the normalized graph Laplacian

            Args:
                adj: Adjacency matrix

            Returns:
                eigenvalues, eigenvectors of the normalized Laplacian
            """
            adj = adj + sp.eye(adj.shape[0])
            deg = np.array(adj.sum(axis=1))
            Dsqrt_inv = sp.diags(1.0 / np.sqrt(deg).flatten())
            laplacian = sp.eye(adj.shape[0]) - Dsqrt_inv @ adj @ Dsqrt_inv
            eigenvals, eigenvecs = slinalg.eigsh(laplacian.tocsc(), k=adj.shape[0] - 1, which='SM', tol=1e-06)
            return (torch.FloatTensor(eigenvals), torch.FloatTensor(eigenvecs))

        def forward(self, x, eigenvecs):
            """  # Compute normalized Laplacian
            Forward pass implementing Bruna's spectral convolution  # Add self-loops

            Args:
                x: Input features [num_nodes, in_features]  # Compute degree matrix
                eigenvecs: Eigenvectors of the graph Laplacian [num_nodes, num_nodes-1]

            Returns:
                Output features [num_nodes, out_features]  # Compute normalized Laplacian: D^(-1/2) A D^(-1/2)
            """
            x_spectral = torch.matmul(eigenvecs.t(), x)
            out = torch.zeros(x.size(0), self.out_features, device=x.device)
            for i in range(self.in_features):
                for j in range(self.out_features):
                    filtered = x_spectral[:, i] * self.weight[i, j, :]
                    out[:, j] = out[:, j] + torch.matmul(eigenvecs, filtered)
            return out

    return BrunaGraphConv, nn, np, sp, torch


@app.cell
def _(torch):
    import networkx as nx
    import matplotlib.pyplot as plt
    G = nx.karate_club_graph()
    adj = nx.to_scipy_sparse_array(G)
    # Load karate club network
    features = torch.eye(G.number_of_nodes())
    labels = torch.tensor([G.nodes[i]['club'] == 'Officer' for i in G.nodes()], dtype=torch.long)
    return G, adj, features, labels, nx, plt


@app.cell
def _(BrunaGraphConv, nn):
    # Define a simple GCN model
    class SimpleGCN(nn.Module):

        def __init__(self, in_features, out_features, hidden_features, n_nodes):
            super(SimpleGCN, self).__init__()
            self.conv1 = BrunaGraphConv(in_features, _hidden_features, _n_nodes)
            self.relu = nn.ReLU()
            self.conv2 = BrunaGraphConv(_hidden_features, out_features, _n_nodes)

        def forward(self, x, eigenvecs):
            x = self.conv1(x, eigenvecs)
            x = self.relu(x)
            x = self.conv2(x, eigenvecs)
            return x

    return (SimpleGCN,)


@app.cell
def _(BrunaGraphConv, G, SimpleGCN, adj, features, labels, nn, np, torch):
    import torch.optim as optim
    from sklearn.model_selection import train_test_split
    eigenvals, eigenvecs = BrunaGraphConv.get_laplacian_eigenvectors(adj)
    # Get eigenvectors of the Laplacian
    _hidden_features = 10
    _input_features = features.shape[1]
    # Initialize the model
    _output_features = 2
    _n_nodes = G.number_of_nodes()
    model = SimpleGCN(_input_features, _output_features, _hidden_features, _n_nodes)
    _optimizer = optim.Adam(model.parameters(), lr=0.01)
    _criterion = nn.CrossEntropyLoss()
    _train_idx, _test_idx = train_test_split(np.arange(G.number_of_nodes()), test_size=0.2, random_state=42)
    # Train the model
    _train_features = features[_train_idx]
    _train_labels = labels[_train_idx]
    _test_features = features[_test_idx]
    # Split the data into training and testing sets
    _test_labels = labels[_test_idx]
    _n_train = 100
    for _epoch in range(_n_train):
        model.train()
        _optimizer.zero_grad()
        _output = model(_train_features, eigenvecs[_train_idx, :])
        _loss = _criterion(_output, _train_labels)
        _loss.backward()
        _optimizer.step()
        if _epoch == 0 or (_epoch + 1) % 25 == 0:
            model.eval()
            with torch.no_grad():
                _output = model(_test_features, eigenvecs[_test_idx, :])
                _, _predicted = torch.max(_output, 1)
                _accuracy = (_predicted == _test_labels).float().mean()
                print(f'Epoch {_epoch + 1}/{_n_train}, Loss: {_loss.item():.4f}, Accuracy: {_accuracy.item():.4f}')  # Evaluate the model
    return eigenvecs, model, optim, train_test_split


@app.cell
def _(eigenvecs, features, labels, model, plt):
    import seaborn as sns
    from sklearn.manifold import TSNE
    embeddings = model.conv1(features, eigenvecs).detach().numpy()
    # Visualize the learned embeddings
    _xy = TSNE(n_components=2).fit_transform(embeddings)
    _fig, _ax = plt.subplots(figsize=(5, 5))
    sns.scatterplot(x=_xy[:, 0].reshape(-1), y=_xy[:, 1].reshape(-1), hue=labels.numpy(), palette='tab10', ax=_ax)
    _ax.set_title('Learned Node Embeddings')
    plt.show()
    return TSNE, sns


@app.cell
def _(nn, np, sp, torch):
    from typing import Optional

    def sparse_mx_to_torch_sparse(sparse_mx):
        """Convert scipy sparse matrix to torch sparse tensor."""
        sparse_mx = sparse_mx.tocoo()
        indices = torch.from_numpy(np.vstack((sparse_mx.row, sparse_mx.col)).astype(np.int64))
        values = torch.from_numpy(sparse_mx.data.astype(np.float32))
        shape = torch.Size(sparse_mx.shape)
        return torch.sparse_coo_tensor(indices, values, shape)

    class ChebConv(nn.Module):
        """
        Chebyshev Spectral Graph Convolutional Layer
        """

        def __init__(self, in_channels: int, out_channels: int, K: int, bias: bool=True):
            super(ChebConv, self).__init__()
            self.in_channels = in_channels
            self.out_channels = out_channels
            self.K = K
            self.weight = nn.Parameter(torch.Tensor(K, in_channels, out_channels))
            if bias:
                self.bias = nn.Parameter(torch.Tensor(out_channels))
            else:
                self.register_parameter('bias', None)
            self.reset_parameters()

        def reset_parameters(self):
            """Initialize parameters."""
            nn.init.xavier_uniform_(self.weight)
            if self.bias is not None:  # Trainable parameters
                nn.init.zeros_(self.bias)

        def _normalize_laplacian(self, adj_matrix):
            """
            Compute normalized Laplacian L = I - D^(-1/2)AD^(-1/2)
            """
            if not sp.isspmatrix(adj_matrix):
                adj_matrix = sp.csr_matrix(adj_matrix)
            adj_matrix = adj_matrix.astype(float)
            rowsum = np.array(adj_matrix.sum(1)).flatten()
            d_inv_sqrt = np.power(rowsum, -0.5)
            d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.0
            d_mat_inv_sqrt = sp.diags(d_inv_sqrt)
            n = adj_matrix.shape[0]
            L = sp.eye(n) - d_mat_inv_sqrt @ adj_matrix @ d_mat_inv_sqrt
            return L

        def _scale_laplacian(self, L):
            """  # Convert to scipy if it's not already
            Scale Laplacian eigenvalues to [-1, 1] interval
            L_scaled = 2L/lambda_max - I
            """
            try:
                eigenval, _ = sp.linalg.eigsh(L, k=1, which='LM', return_eigenvectors=False)
                lambda_max = eigenval[0]  # Compute degree matrix D
            except:
                lambda_max = 2.0
            n = L.shape[0]
            L_scaled = 2.0 / lambda_max * L - sp.eye(n)
            return L_scaled
      # Compute L = I - D^(-1/2)AD^(-1/2)
        def chebyshev_basis(self, L_sparse: torch.sparse.Tensor, X: torch.Tensor):
            """
            Compute Chebyshev polynomials basis up to order K.
            """
            cheb_polynomials = []
            cheb_polynomials.append(X)
            if self.K > 1:
                X_1 = torch.sparse.mm(L_sparse, X)
                cheb_polynomials.append(X_1)
            for k in range(2, self.K):
                X_k = 2 * torch.sparse.mm(L_sparse, cheb_polynomials[k - 1]) - cheb_polynomials[k - 2]  # Compute largest eigenvalue
                cheb_polynomials.append(X_k)
            return torch.stack(cheb_polynomials, dim=0)

        def forward(self, X: torch.Tensor, adj_matrix: sp.spmatrix):  # Approximate lambda_max = 2 if eigenvalue computation fails
            """
            Forward pass.

            Args:
                X: Node features tensor of shape [num_nodes, in_channels]
                adj_matrix: Adjacency matrix in scipy sparse format

            Returns:
                Output tensor of shape [num_nodes, out_channels]
            """
            L_norm = self._normalize_laplacian(adj_matrix)  # List to store Chebyshev polynomials
            L_scaled = self._scale_laplacian(L_norm)
            L_scaled = sparse_mx_to_torch_sparse(L_scaled).to(X.device)
            Tx = self.chebyshev_basis(L_scaled, X)  # T_0(L) = I
            out = torch.einsum('kni,kio->no', Tx, self.weight)
            if self.bias is not None:
                out = out + self.bias
            return out  # T_1(L) = L  # Recurrence T_k(L) = 2L·T_{k-1}(L) - T_{k-2}(L)  # [K, num_nodes, in_channels]  # Compute normalized and scaled Laplacian  # Convert to torch sparse tensor  # Compute Chebyshev polynomials basis  # [K, num_nodes, in_channels]  # Perform convolution using learned weights

    return (ChebConv,)


@app.cell
def _(ChebConv, nn, sp, torch):
    class ChebNet(nn.Module):
        """
        ChebNet model for node classification
        """

        def __init__(
            self,
            in_channels: int,
            hidden_channels: int,
            out_channels: int,
            K: int,
            num_layers: int,
            dropout: float = 0.5,
        ):
            super(ChebNet, self).__init__()

            self.convs = nn.ModuleList()

            # First layer
            self.convs.append(ChebConv(in_channels, hidden_channels, K))

            # Hidden layers
            for _ in range(num_layers - 2):
                self.convs.append(ChebConv(hidden_channels, hidden_channels, K))

            # Output layer
            self.convs.append(ChebConv(hidden_channels, out_channels, K))

            self.dropout = nn.Dropout(dropout)
            self.activation = nn.ReLU()

        def forward(self, X: torch.Tensor, adj_matrix: sp.spmatrix):
            """
            Forward pass through all layers
            """
            for i, conv in enumerate(self.convs[:-1]):
                X = conv(X, adj_matrix)
                X = self.activation(X)
                X = self.dropout(X)

            # Output layer
            X = self.convs[-1](X, adj_matrix)
            return X

    return (ChebNet,)


@app.cell
def _(ChebNet, nn, np, nx, optim, torch, train_test_split):
    G_1 = nx.karate_club_graph()
    adj_1 = nx.to_scipy_sparse_array(G_1)
    features_1 = torch.eye(G_1.number_of_nodes())
    labels_1 = torch.tensor([G_1.nodes[i]['club'] == 'Officer' for i in G_1.nodes()], dtype=torch.long)
    _hidden_features = 10
    _input_features = features_1.shape[1]
    _output_features = 2
    _n_nodes = G_1.number_of_nodes()
    K = 3
    num_layers = 2
    dropout = 0.5
    model_1 = ChebNet(_input_features, _hidden_features, _output_features, K, num_layers, dropout)
    _optimizer = optim.Adam(model_1.parameters(), lr=0.01)
    _criterion = nn.CrossEntropyLoss()
    _train_idx, _test_idx = train_test_split(np.arange(G_1.number_of_nodes()), test_size=0.2, random_state=42)
    _train_features = features_1[_train_idx]
    _train_labels = labels_1[_train_idx]
    _test_features = features_1[_test_idx]
    _test_labels = labels_1[_test_idx]
    _n_train = 100
    for _epoch in range(_n_train):
        model_1.train()
        _optimizer.zero_grad()
        _output = model_1(features_1, adj_1)
        _loss = _criterion(_output[_train_idx], _train_labels)
        _loss.backward()
        _optimizer.step()
        if _epoch == 0 or (_epoch + 1) % 25 == 0:
            model_1.eval()
            with torch.no_grad():
                _output = model_1(features_1, adj_1)
                _, _predicted = torch.max(_output[_test_idx], 1)
                _accuracy = (_predicted == _test_labels).float().mean()
                print(f'Epoch {_epoch + 1}/{_n_train}, Loss: {_loss.item():.4f}, Accuracy: {_accuracy.item():.4f}')
    return adj_1, features_1, labels_1, model_1


@app.cell
def _(TSNE, adj_1, features_1, labels_1, model_1, plt, sns, torch):
    model_1.eval()
    with torch.no_grad():
        X_hidden = features_1
        for conv in model_1.convs[:-1]:
            X_hidden = conv(X_hidden, adj_1)
            X_hidden = model_1.activation(X_hidden)
    _xy = TSNE(n_components=2).fit_transform(X_hidden.numpy())
    _fig, _ax = plt.subplots(figsize=(5, 5))
    sns.scatterplot(x=_xy[:, 0].reshape(-1), y=_xy[:, 1].reshape(-1), hue=labels_1.numpy(), palette='tab10', ax=_ax)
    _ax.set_title('Learned Node Embeddings')
    plt.show()
    return


if __name__ == "__main__":
    app.run()

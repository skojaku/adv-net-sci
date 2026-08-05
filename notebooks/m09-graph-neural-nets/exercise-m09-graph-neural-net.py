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
    # [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/skojaku/adv-net-sci/blob/main/notebooks/m09-graph-neural-nets/exercise-m09-graph-neural-net.ipynb)

    # Exercise M09: Graph Neural Networks

    ## Image Processing

    Let's perform the Fourier transform on an image.
    For an image $X$ with size $H \times W$, the Fourier transform of $X$ is:

    $$
    \begin{aligned}
    \mathcal{F}(X)[h, w] &= \sum_{k=0}^{H-1} \sum_{\ell=0}^{W-1} X[k, \ell] \cdot e^{-2\pi i \frac{hk}{H}} \cdot e^{-2\pi i \frac{w\ell}{W}} \\
    &= \sum_{k=0}^{H-1} \sum_{\ell=0}^{W-1} X[k, \ell] e^{-2\pi i \left(\frac{hk}{H} + \frac{w\ell}{W}\right)}
    \end{aligned}
    $$

    The exponential term $e^{-2\pi i \left(\frac{hk}{H} + \frac{w\ell}{W}\right)}$ represents a 2D wave with frequency $(h, w)$, which looks like the following:
    """)
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt

    def basis_function(img_size=256, u=0, v=0):
        """
        img_size : square size of image f(x,y)
        u,v : spatial space indice
        """
        N = img_size
        x = np.linspace(0, N - 1, N)
        y = np.linspace(0, N - 1, N)
        x_, y_ = np.meshgrid(x, y)
        bf = np.exp(-1j * 2 * np.pi * (u * x_ / N + v * y_ / N))
        if u == 0 and v == 0:
            bf = np.round(bf)
        real = np.real(bf)
        _imag = np.imag(bf)
        return (real, _imag)
    size = 16
    _bf_arr_real = np.zeros((size * size, size, size))
    _bf_arr_imag = np.zeros((size * size, size, size))
    _ind = 0
    for _col in range(size):
        for _row in range(size):
            _re, _imag = basis_function(img_size=size, u=_row, v=_col)
            _bf_arr_real[_ind] = _re
            _bf_arr_imag[_ind] = _imag
            _ind = _ind + 1
    _, _axs = plt.subplots(size, size, figsize=(4, 4))
    _axs = _axs.flatten()
    for _img, _ax in zip(_bf_arr_real, _axs):
        _ax.set_axis_off()
        _ax.imshow(_img, cmap='gray')
    return basis_function, np, plt, size


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Note 🤔**: It is common to reorder the basis functions such that the lowest frequency components are at the center, which looks like this:
    """)
    return


@app.cell
def _(basis_function, np, plt, size):
    _bf_arr_real = np.zeros((size * size, size, size))
    _bf_arr_imag = np.zeros((size * size, size, size))
    _ind = 0
    for _col in range(-size // 2, size // 2):
        for _row in range(-size // 2, size // 2):
            _re, _imag = basis_function(img_size=size, u=_row, v=_col)
            _bf_arr_real[_ind] = _re
            _bf_arr_imag[_ind] = _imag
            _ind = _ind + 1
    _fig, _axs = plt.subplots(size, size, figsize=(4, 4))
    _axs = _axs.flatten()
    for _img, _ax in zip(_bf_arr_real, _axs):
        _ax.set_axis_off()
        _ax.imshow(_img, cmap='gray')
    _fig.suptitle('Real Part of Basis Functions')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, let's perform the Fourier transform on an image.
    """)
    return


@app.cell
def _(np, plt):
    from PIL import Image
    import requests
    from io import BytesIO

    def read_jpeg_from_url(url):
        response = requests.get(url)
        _img = Image.open(BytesIO(response.content))
        if _img.mode != 'RGB':
            _img = _img.convert('RGB')
        return _img

    def image_to_numpy(img):
        return np.array(_img)

    def to_gray_scale(img_np):
        return np.mean(img_np, axis=2)
    url = 'https://www.binghamton.edu/news/images/uploads/features/20180815_peacequad02_jwc.jpg'
    _img = read_jpeg_from_url(url)
    img_np = image_to_numpy(_img)
    img_gray = to_gray_scale(img_np)
    plt.imshow(img_gray, cmap='gray')
    return (img_gray,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Take the Fourier transform of the image.
    """)
    return


@app.cell
def _(img_gray, np):
    ft_img_gray = np.fft.fft2(img_gray)
    return (ft_img_gray,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This decomposes the image into a sum of basis waves. Let's see the weights of the basis waves.
    """)
    return


@app.cell
def _(ft_img_gray, np, plt):
    import matplotlib
    weight = np.abs(ft_img_gray)
    fig1, ax1 = plt.subplots(figsize=(5, 5))
    ax1.imshow(weight, cmap='gray', norm=matplotlib.colors.LogNorm(), aspect='equal')
    # real part
    _cbar = fig1.colorbar(ax1.images[0], ax=ax1, orientation='horizontal')
    _cbar.set_label('Fourier transform magnitude')
    ax1.axis('off')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The pixel’s brightness indicates the strength of its associated basis wave: a brighter pixel means that wave plays a more dominant role in the image. We can see that there are some high‑frequency components, which correspond to the image’s edges.

    **Your task 🧑‍💻**

    Now, let's see the convolution of the image with a Prewitt operator.

    The Prewitt operator is a type of edge detection filter that highlights regions of an image with high spatial derivatives.

    An example of the Prewitt operator for detecting horizontal edges is:

    $$
    K = \begin{bmatrix}
        1 & 1 & 1 \\
        0 & 0 & 0 \\
       -1 & -1 & -1
    \end{bmatrix}
    $$

    Implement the Prewitt operator, and see the result of the convolution.
    """)
    return


@app.cell
def _(np):
    K = np.zeros((3, 3))  # Change this to the Prewitt operator
    return (K,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This operator is used to detect the horizontal edges of the image.
    Let's compute the Fourier transform of the Prewitt operator.
    """)
    return


@app.cell
def _(K, img_gray, np):
    K_padd = np.zeros((img_gray.shape[0], img_gray.shape[1]))
    K_padd[: K.shape[0], : K.shape[1]] = K  # We put K in the corner of the padded matrix

    # convolution
    FK = np.fft.fft2(K_padd)
    return (FK,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Note 🤔**: We have padded the operator to the same size as the image, which is required to perform the convolution. Now, let's see the weights of the basis waves.
    """)
    return


@app.cell
def _(FK, np, plt):
    plt.imshow(np.abs(FK), cmap='gray')
    _cbar = plt.colorbar()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Observe that the low frequency components are suppressed, and the high frequency components are enhanced. This is because the Prewitt operator is a high-pass filter that only allows high-frequency components to pass through.

    We now perform the convolution of the image with the Prewitt operator.
    """)
    return


@app.cell
def _(FK, img_gray, np, plt):
    FX = np.fft.fft2(img_gray)
    conv_img_gray = np.real(np.fft.ifft2(FX * FK))
    plt.imshow(conv_img_gray, cmap="gray")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1 🏋️:

    Design your own kernel to:
    1. Detect the vertical edges of the image.
    2. Smooth the image.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **1. Kernel to detect the vertical edges of the image.**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **2. Kernel to smooth the image.**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Spectral Graph Convolutional Networks

    We can think of a convolution of an image from the perspective of networks.
    In the convolution of an image, a pixel is convolved with its *neighbors*. We can regard each pixel as a node, and each node is connected to its neighboring nodes (pixels) that are involved in the convolution.

    ![](https://av-eks-lekhak.s3.amazonaws.com/media/__sized__/article_images/conv_graph-thumbnail_webp-600x300.webp)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Suppose that each node has a variable $x_i \in \mathbb{R}$, just like each pixel has a value in a grey image. Consider a network of $N$ such nodes.

    In this example, we use the karate club network and set $x$ by a random gaussian variable.
    """)
    return


@app.cell
def _(np):
    import igraph as ig
    from scipy import sparse
    import matplotlib as mpl
    G = ig.Graph.Famous('Zachary')
    A = G.get_adjacency_sparse()
    x = np.random.randn(G.vcount())
    return A, G, ig, mpl, sparse, x


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We define the *total variation* of ${\mathbf x}$ as the sum of the squared differences between connected nodes:

    $$
    J = \frac{1}{2}\sum_{i=1}^N\sum_{j=1}^N A_{ij}(x_i - x_j)^2 = {\bf x}^\top {\bf L} {\bf x},
    $$

    where ${\bf L}$ is the Laplacian matrix of the graph given by

    $$
    L_{ij} = \begin{cases}
    -1 & \text{if } i \text{ and } j \text{ are connected} \\
    k_i & \text{if } i = j \\
    0 & \text{otherwise}
    \end{cases}.
    $$

    and ${\bf x} = [x_1,x_2,\ldots, x_N]^\top$ is a column vector of feature variables.
    """)
    return


@app.cell
def _(A, G, sparse, x):
    J = 0
    for _i in range(G.vcount()):
        for j in range(G.vcount()):
            if A[_i, j] != 0:
                J = J + (x[_i] - x[j]) ** 2
    J = J / 2
    _deg = A.sum(axis=1).A1
    L = sparse.diags(_deg) - A
    J_by_laplacian = x.T @ L @ x
    print(f'J: {J}, J_by_laplacian: {J_by_laplacian}')
    return J, L


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We decompose the total variation into high-frequency and low-frequency components by using the eigenvectors ${\bf u}_i$ and the eigenvalues $\lambda_i$ of the Laplacian matrix:

    $$
    J = \sum_{i=1}^N \lambda_i  {\bf x}^\top {\mathbf u}_i {\mathbf u}_i^\top {\bf x} = \sum_{i=1}^N \lambda_i  ||{\bf x}^\top {\mathbf u}_i||^2.
    $$

    The term $({\bf x}^\top {\mathbf u}_i)$ is a dot-product between the feature vector ${\bf x}$ and the eigenvector ${\mathbf u}_i$, measuring how much ${\bf x}$ aligns with ${\mathbf u}_i$, similar to Fourier coefficients with sinusoids. Each $||{\bf x}^\top {\mathbf u}_i||^2$ represents the ''strength'' of ${\bf x}$ with respect to ${\mathbf u}_i$, making the total variation $J$ a weighted sum of these strengths.
    """)
    return


@app.cell
def _(J, L, np, x):
    # Compute the eigenvalues and eigenvectors of the Laplacian matrix
    eigvals, eigvecs = np.linalg.eigh(L.toarray())
    sorted_indices = np.argsort(eigvals)
    # Sort the eigenvalues and eigenvectors
    eigvals = eigvals[sorted_indices]
    eigvecs = eigvecs[:, sorted_indices]
    strength = []
    for _i in range(len(eigvals)):
        strength.append(np.sum((x.T @ eigvecs[:, _i]) ** 2))
    J_by_eig = np.sum(strength * eigvals)
    print(f'J: {J}, J_by_eig: {J_by_eig}')
    return eigvals, eigvecs, strength


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here is the "frequency" of each component in increasing order of eigenvalues (frequency).
    """)
    return


@app.cell
def _(eigvals, plt, strength):
    import seaborn as sns
    _fig, _ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=range(len(eigvals)), y=strength)
    _ax.set_xlabel('Eigenvalue index')
    _ax.set_ylabel('Strength')
    sns.despine()
    plt.show()
    return (sns,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The eigenvalues $\lambda_i$ are then multipled by the strength of the corresponding component, and the total is the total variation $J$.
    """)
    return


@app.cell
def _(eigvals, plt, sns, strength):
    _fig, _ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=range(len(eigvals)), y=strength * eigvals)
    _ax.set_xlabel('Eigenvalue index')
    _ax.set_ylabel('Strength * Eigenvalue')
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, we can consider "eigenvals" as a filter that controls which frequency components pass through 😉. For example, if we want to keep the low-frequency components, we can set the high-frequency components to zero.
    """)
    return


@app.cell
def _(eigvals, plt, sns, strength):
    _eigvals_filtered = eigvals.copy()
    _eigvals_filtered[:-10] = 0
    _eigvals_filtered[-10:] = 10
    _fig, _ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=range(len(eigvals)), y=strength * _eigvals_filtered)
    _ax.set_xlabel('Eigenvalue index')
    _ax.set_ylabel('Strength * Filtered Eigenvalue')
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using this filter, we reconstruct the Laplacian matrix.
    """)
    return


@app.cell
def _(eigvals, eigvecs, np):
    L_filtered = eigvecs @ np.diag(eigvals) @ eigvecs.T
    return (L_filtered,)


@app.cell
def _(L, L_filtered, plt, sns):
    _fig, _axes = plt.subplots(1, 2, figsize=(10, 5))
    _axes[0].set_title('Original Laplacian')
    _axes[1].set_title('Reconstructed Laplacian from filtered eigenvalues')
    sns.heatmap(L.toarray(), cmap='viridis', ax=_axes[0])
    sns.heatmap(L_filtered, cmap='viridis', ax=_axes[1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We now have a new "convolution" matrix $L_{\text{filtered}}$ with which to generate a new feature vector ${\bf x}'$.
    """)
    return


@app.cell
def _(L_filtered, x):
    x_prime = L_filtered @ x
    return (x_prime,)


@app.cell
def _(G, ig, mpl, plt, sns, x, x_prime):
    _fig, _axes = plt.subplots(1, 2, figsize=(10, 5))
    _palette = sns.color_palette('viridis', as_cmap=True)
    _norm = mpl.colors.Normalize(vmin=-0.8, vmax=0.8)
    ig.plot(G, vertex_color=[_palette(_norm(_x)) for _x in x], bbox=(0, 0, 500, 500), vertex_size=20, target=_axes[0])
    _axes[0].set_title('Original')
    ig.plot(G, vertex_color=[_palette(_norm(_x)) for _x in x_prime], bbox=(0, 0, 500, 500), vertex_size=20, target=_axes[1])
    _axes[1].set_title('High-pass filter')
    _fig.tight_layout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Observe that the values of the nodes are smoothed out, since the high-frequency components are suppressed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2 🏋️:

    Design your own filter to detect the high-frequency components of the graph. And apply the filter to:

    1. Random gaussian variables
    2. Eigenvector centrality of the graph.

    Then, compare the results with the original ones.

    **Construct your own filter**
    """)
    return


@app.cell
def _(eigvals, eigvecs, np):
    _eigvals_filtered = eigvals.copy()
    alpha = 3
    high_pass_filter = alpha * eigvals / (1 + alpha * eigvals)
    L_filtered_1 = eigvecs @ np.diag(high_pass_filter) @ eigvecs.T
    return (L_filtered_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Apply the filter to random gaussian variables**
    """)
    return


@app.cell
def _(G, L_filtered_1, ig, mpl, np, plt, sns):
    x_1 = np.random.randn(G.vcount())
    x_prime_1 = L_filtered_1 @ x_1
    _fig, _axes = plt.subplots(1, 2, figsize=(10, 5))
    _palette = sns.color_palette('viridis', as_cmap=True)
    _norm = mpl.colors.Normalize(vmin=-0.8, vmax=0.8)
    ig.plot(G, vertex_color=[_palette(_norm(_x)) for _x in x_1], bbox=(0, 0, 500, 500), vertex_size=20, target=_axes[0])
    _axes[0].set_title('Original')
    ig.plot(G, vertex_color=[_palette(_norm(_x)) for _x in x_prime_1], bbox=(0, 0, 500, 500), vertex_size=20, target=_axes[1])
    _axes[1].set_title('High-pass filter')
    _fig.tight_layout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Apply the filter to eigenvector centrality**
    """)
    return


@app.cell
def _(G, L_filtered_1, ig, mpl, plt, sns):
    x_2 = G.eigenvector_centrality()
    x_prime_2 = L_filtered_1 @ x_2
    _fig, _axes = plt.subplots(1, 2, figsize=(10, 5))
    _palette = sns.color_palette('viridis', as_cmap=True)
    _norm = mpl.colors.Normalize(vmin=0, vmax=0.5)
    ig.plot(G, vertex_color=[_palette(_norm(_x)) for _x in x_2], bbox=(0, 0, 500, 500), vertex_size=20, target=_axes[0])
    _axes[0].set_title('Original')
    ig.plot(G, vertex_color=[_palette(_norm(_x)) for _x in x_prime_2], bbox=(0, 0, 500, 500), vertex_size=20, target=_axes[1])
    _axes[1].set_title('High-pass filter')
    _fig.tight_layout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Graph Convolutional Networks

    Let's implement a simple Graph Convolutional Network (GCN) by Kipf & Welling. We will use the karate club network again. To this end, we will use PyTorch.
    """)
    return


@app.cell
def _():
    import torch

    return (torch,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's work with multiple features for each node.
    """)
    return


@app.cell
def _(G, torch):
    X = torch.randn(G.vcount(), 5)  # one-hot encoding of the node indices
    X.shape
    return (X,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    GCN updates node features by:

    $$
    x' = \sigma\left( \tilde {\mathbf A} X \Theta\right)
    $$

    where
    1. $X$ is the feature matrix of the graph,
    2. $\sigma$ is an activation function, and
    3. $\Theta$ is a learnable parameter matrix.
    4. $\tilde {\mathbf A}$ is the normalized adjacency matrix of the graph (with self-loops).

    Let's break down the formula. First, we will compute $\tilde {\mathbf A}$

    $$
    \tilde A = A + I
    $$

    $$
    \tilde A' = D^{-\frac{1}{2}} \tilde A D^{-\frac{1}{2}}
    $$

    where $D$ is the degree matrix of the graph.
    """)
    return


@app.cell
def _(A, np, sparse):
    A_hat = A + sparse.eye(A.shape[0])
    _deg = np.array(A.sum(axis=1)).flatten()
    D_inv = sparse.diags(1.0 / np.sqrt(_deg))
    A_hat_norm = D_inv @ A_hat @ D_inv
    return (A_hat_norm,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, we will multiply it by feature matrix $X$ and learnable parameter matrix $\Theta$.
    """)
    return


@app.cell
def _(A_hat_norm, X, plt, sns):
    A_hat_norm_X = A_hat_norm @ X
    sns.set_style('white')
    sns.set(font_scale=1.2)
    sns.set_style('ticks')
    _fig, _ax = plt.subplots(figsize=(7, 5), ncols=2)
    sns.heatmap(A_hat_norm_X, ax=_ax[0])
    _ax[0].set_title("$\tilde A' X$")
    sns.heatmap(X, ax=_ax[1])
    _ax[1].set_title('$X$')
    _fig.tight_layout()
    return (A_hat_norm_X,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, let's prepare the learnable parameters and apply it to the feature matrix. We initialize the learnable parameters by random gaussian variables.
    """)
    return


@app.cell
def _(X, torch):
    Theta = torch.nn.Parameter(
        torch.randn(X.shape[1], 5), requires_grad=True
    )  # The new feature x' has 5 dimensions.
    return (Theta,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And multiply it by $\tilde {\mathbf A} X$, and apply the activation function $\sigma$. We will use the sigmoid function as the activation function.
    """)
    return


@app.cell
def _(A_hat_norm_X, Theta, torch):
    A_hat_norm_X_Theta = torch.FloatTensor(A_hat_norm_X) @ Theta
    return (A_hat_norm_X_Theta,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, let's visualize the updated feature matrix. Each row is a new feature vector of a node.
    """)
    return


@app.cell
def _(A_hat_norm_X_Theta):
    A_hat_norm_X_Theta
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's visualize the updated feature matrix in 2D space using PCA.
    """)
    return


@app.cell
def _(A_hat_norm_X_Theta, np, plt, sns):
    _fig, _ax = plt.subplots(figsize=(5, 5))
    from sklearn.decomposition import PCA
    _xy = PCA(n_components=2).fit_transform(A_hat_norm_X_Theta.detach().numpy())
    import networkx as nx
    Gnx = nx.karate_club_graph()
    labels = np.unique([d[1]['club'] for d in Gnx.nodes(data=True)], return_inverse=True)[1]
    # We color the nodes by the membership of the karate club members.
    sns.scatterplot(x=_xy[:, 0], y=_xy[:, 1], hue=labels, ax=_ax)
    return PCA, labels


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We observe that the nodes are separated into two clusters, despite the fact that the GCN is **untrained!**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, let's train the GCN to predict the membership of the karate club. Namely, the GCN is given the feature matrix $X$ and the adjacency matrix $A$, and it learns the parameter matrix $\Theta$ to predict the membership of the karate club. We will split the nodes into the training and testing sets, and evaluate the accuracy of the model using the testing set.
    """)
    return


@app.cell
def _(A, G, labels, np, sparse, torch):
    from sklearn.model_selection import train_test_split
    from tqdm import tqdm

    class GCN(torch.nn.Module):

        def __init__(self, in_features, out_features, A):
            super(GCN, self).__init__()
            self.linear = torch.nn.Parameter(torch.randn(in_features, out_features), requires_grad=True)
            A_hat = A + sparse.eye(A.shape[0])
            _deg = A_hat.sum(axis=1).A1
            D_hat = sparse.diags(_deg)
            D_hat_inv = sparse.diags(1 / _deg)
            self.A_hat_norm = D_hat_inv @ A_hat

        def forward(self, x):
            Ax = torch.tensor(self.A_hat_norm @ x, dtype=torch.float32)
            return torch.nn.functional.sigmoid(Ax @ self.linear)
    model = GCN(in_features=A.shape[0], out_features=2, A=A)
    X_1 = torch.eye(A.shape[0])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = torch.nn.CrossEntropyLoss()
    train_idx, test_idx = train_test_split(np.arange(G.vcount()), test_size=0.2, random_state=42)
    labels_1 = torch.tensor(labels)
    train_features = X_1[train_idx]
    train_labels = labels_1[train_idx]
    test_features = X_1[test_idx]
    test_labels = labels_1[test_idx]
    n_train = 200
    pbar = tqdm(range(n_train))
    loss_history = []
    for epoch in pbar:
        model.train()
        optimizer.zero_grad()
        output = model(X_1)
        loss = criterion(output[train_idx], train_labels)
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            output = model(X_1)
            _, predicted = torch.max(output, 1)
            accuracy = (predicted[test_idx] == test_labels).float().mean()
            loss_history.append(loss.item())
            pbar.set_postfix(loss=loss.item(), accuracy=accuracy.item())
    return X_1, labels_1, loss_history, model, n_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The loss decreases as the training progresses, which indicates that the model is learning.
    """)
    return


@app.cell
def _(loss_history, n_train, plt, sns):
    _fig, _ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=range(n_train), y=loss_history, ax=_ax)
    _ax.set_xlabel('Epoch')
    _ax.set_ylabel('Loss')
    sns.despine()
    plt.show()
    return


@app.cell
def _(PCA, X_1, labels_1, model, plt, sns):
    Xprime = model(X_1)
    _fig, _ax = plt.subplots(figsize=(5, 5))
    _xy = PCA(n_components=2).fit_transform(Xprime.detach().numpy())
    sns.scatterplot(x=_xy[:, 0], y=_xy[:, 1], hue=labels_1, ax=_ax, legend=False)
    _ax.set_title('Learned feature matrix')
    sns.despine()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3 🏋️:

    1. Build a two-layer GCN and train it to predict the membership of the karate club.
    2. Compare the performance of the two-layer GCN with the one-layer GCN.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()

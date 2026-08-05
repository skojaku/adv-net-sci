# /// script
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "numpy",
#     "igraph",
#     "seaborn",
# ]
# [tool.marimo.display]
# default_width = "full"
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App()


@app.cell
def _():
    import igraph
    import matplotlib.pyplot as plt
    _fig, _ax = plt.subplots(figsize=(10, 8))
    g = igraph.Graph.Famous('Zachary')
    igraph.plot(g, target=_ax, vertex_size=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    return g, igraph, plt


@app.cell
def _(g):
    communities = g.community_leiden(resolution=1, objective_function= "modularity")
    return (communities,)


@app.cell
def _(communities):
    print(communities.membership)
    return


@app.cell
def _(communities, g, igraph, plt):
    import seaborn as sns
    community_membership = communities.membership
    palette = sns.color_palette().as_hex()
    _fig, _ax = plt.subplots(figsize=(10, 8))
    igraph.plot(g, target=_ax, vertex_color=[palette[i] for i in community_membership])
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    return (sns,)


@app.cell
def _():
    # We fit the stochastic block model ourselves, in numpy. Everything below is
    # the derivation from the concepts chapter turned into code, so there is no
    # black box and no compiled dependency to install.
    import numpy as np

    def _blocks(A, labels, B):
        """One-hot membership, block edge counts, and block sizes."""
        N = A.shape[0]
        Z = np.zeros((N, B))
        Z[np.arange(N), labels] = 1.0
        return Z, Z.T @ A @ Z, Z.sum(0)

    def sbm_loglik(A, labels, B):
        """Bernoulli SBM log-likelihood, evaluated at the maximum-likelihood p.

        The concepts chapter shows p_rs = m_rs / (number of pairs between r and
        s), so we never optimise p — we substitute it and search over labels.
        """
        _, m, n_r = _blocks(A, labels, B)
        m = m / 2.0                                   # each edge counted twice
        n = np.outer(n_r, n_r)
        np.fill_diagonal(n, n_r * (n_r - 1) / 2.0)    # pairs inside a block
        iu = np.triu_indices(B)
        m_e, n_e = m[iu], n[iu]
        keep = n_e > 0
        m_e, n_e = m_e[keep], n_e[keep]
        p = np.clip(m_e / n_e, 1e-12, 1 - 1e-12)
        return float(np.sum(m_e * np.log(p) + (n_e - m_e) * np.log(1 - p)))

    def sbm_loglik_dc(A, labels, B):
        """Degree-corrected SBM objective (Karrer & Newman 2011).

            L = sum_rs  m_rs log( m_rs / (kappa_r kappa_s) )

        kappa_r is the total degree of block r, so a node's own degree is
        explained away and the blocks are free to capture something else.
        """
        k = A.sum(1)
        Z, m, _ = _blocks(A, labels, B)
        kappa = Z.T @ k
        with np.errstate(divide="ignore", invalid="ignore"):
            term = m * np.log(m / np.outer(kappa, kappa))
        return float(np.nansum(np.where(m > 0, term, 0.0)))

    def fit_sbm(A, B, degree_corrected=False, n_init=5, max_sweeps=50, seed=0):
        """Greedy search: move one node at a time, keep any move that helps."""
        score = sbm_loglik_dc if degree_corrected else sbm_loglik
        rng = np.random.default_rng(seed)
        N = A.shape[0]
        best_labels, best = None, -np.inf
        for _ in range(n_init):
            labels = rng.integers(0, B, size=N)
            labels[rng.permutation(N)[:B]] = np.arange(B)   # use every block
            ll = score(A, labels, B)
            for _sweep in range(max_sweeps):
                improved = False
                for i in rng.permutation(N):
                    cur = labels[i]
                    for b in range(B):
                        if b == cur:
                            continue
                        labels[i] = b
                        cand = score(A, labels, B)
                        if cand > ll + 1e-9:
                            ll, cur, improved = cand, b, True
                        else:
                            labels[i] = cur
                if not improved:
                    break
            if ll > best:
                best, best_labels = ll, labels.copy()
        return best_labels, best

    def description_length(A, labels, B):
        """Lower is better. Likelihood alone always prefers more blocks, so we
        charge for the parameters: one probability per block pair, one label
        per node. graph-tool implements a more principled version of this."""
        N = A.shape[0]
        return (-sbm_loglik(A, labels, B)
                + 0.5 * (B * (B + 1) / 2) * np.log(N * (N - 1) / 2)
                + N * np.log(B))

    def select_blocks(A, B_min=2, B_max=6, **kw):
        """Fit every B in range and keep the one with the smallest description length."""
        results = []
        for B in range(B_min, B_max + 1):
            labels, _ll = fit_sbm(A, B, **kw)
            results.append((description_length(A, labels, B), B, labels))
        best_dl, best_B, best_labels = min(results, key=lambda t: t[0])
        table = [(B, round(dl, 1)) for dl, B, _ in sorted(results, key=lambda t: t[1])]
        return best_labels, best_B, table

    return fit_sbm, np, select_blocks


@app.cell
def _(igraph, np):
    g_1 = igraph.Graph.Famous("Zachary")
    A_karate = np.array(g_1.get_adjacency().data, dtype=float)
    return A_karate, g_1


@app.cell
def _(A_karate, np, select_blocks):
    # Fit the plain (not degree-corrected) SBM, letting the description length
    # pick the number of communities.
    community_membership_1, B_selected, dl_by_B = select_blocks(
        A_karate, B_min=2, B_max=6, n_init=5, seed=42
    )
    community_membership_1 = np.unique(community_membership_1, return_inverse=True)[1]
    print("selected number of blocks:", B_selected)
    print("description length by B:  ", dl_by_B)
    return (community_membership_1,)


@app.cell
def _(community_membership_1, g_1, igraph, plt, sns):
    palette_1 = sns.color_palette().as_hex()
    _fig, _ax = plt.subplots(figsize=(10, 8))
    igraph.plot(g_1, target=_ax, vertex_color=[palette_1[i] for i in community_membership_1])
    plt.axis("off")
    plt.tight_layout()
    plt.show()
    return (palette_1,)


@app.cell
def _(A_karate, community_membership_1, np, plt):
    sorted_indices = np.argsort(community_membership_1)
    A_sorted = A_karate[sorted_indices][:, sorted_indices]
    plt.figure(figsize=(10, 8))
    plt.imshow(A_sorted, cmap="binary")
    plt.title("Adjacency matrix, rows and columns sorted by block")
    plt.xlabel("Node index (sorted)")
    plt.ylabel("Node index (sorted)")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(A_karate, fit_sbm, g_1, igraph, np, palette_1, plt):
    # Now the degree-corrected version, on the same network.
    community_membership_2, _ = fit_sbm(A_karate, 2, degree_corrected=True, n_init=10, seed=7)
    community_membership_2 = np.unique(community_membership_2, return_inverse=True)[1]

    # Zachary recorded which faction each member joined after the split.
    faction = np.array([0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,0,1,0,1,1,
                        1,1,1,1,1,1,1,1,1,1])
    _agree = max((community_membership_2 == faction).sum(),
                 (1 - community_membership_2 == faction).sum())
    print(f"degree-corrected SBM agrees with the real split: {_agree}/34 = {_agree/34:.0%}")

    _fig, _ax = plt.subplots(figsize=(10, 8))
    igraph.plot(g_1, target=_ax, vertex_color=[palette_1[i] for i in community_membership_2])
    plt.axis("off")
    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()

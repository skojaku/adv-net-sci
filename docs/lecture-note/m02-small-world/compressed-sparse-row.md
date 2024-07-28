---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .Rmd
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.3
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---



# Efficient representation for large sparse networks

We will first load the network data as the adjacency matrix into memory.
A challenge is that the adjacency matrix can be too large to fit in memrory.
For example, a network with $10^5$ nodes requires a $10^5 \times 10^5$ matrix, totaling $10$ billion entries!
A good news is that we do not need to hold all these entries in memory, if we know the network is *sparse*.

Many networks in real-world are sparse, meaning most nodes connect to only a few others.
The result is that the adjacency matrix often contains many zeros.
This is where we can save significant memory by storing only the non-zero entries.

**Compressed Sparse Row (CSR)** representation offers the same convenience as the adjacency matrix while being more efficient.
This representation keeps the indices of the non-zero entries in the adjacency matrix, together with the values in the entries.
Sounds simple! But the way it stores the indices and values is slightly complicated. Interested readers can find more details in the [Appendix](./appendix.md).


:::{figure-md} csr_matirx

<img src="https://miro.medium.com/v2/resize:fit:1100/format:webp/0*zWhtdW4nYTSO3nya.gif" width="100%">

Compressed Sparse Row (CSR) matrix. Source: [Medium: Sparse GEMM and Tensor Core’s Structured Sparsity](https://medium.com/@hxu296/exploring-spgemm-and-nvidias-leap-in-deep-neural-network-efficiency-d367adc68791)
:::

The CSR format is implemented in the [scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html) library. It is straightforward to convert the CSR matrix from the *dense* adjacency matrix.
```{code-cell} ipython3
from scipy.sparse import csr_matrix

A = [[0, 2, 0, 1],
     [2, 0, 2, 1],
     [0, 2, 0, 1],
     [1, 1, 1, 0]]

A_csr = csr_matrix(A)
A_csr
```

If you have an *edge list*, you can directly generate the CSR matrix without creating the dense matrix first.
```{code-cell} ipython3
from scipy.sparse import csr_matrix

edges = [(0,1), (0, 1), (0, 3), (1, 2), (1, 2), (1, 3), (2, 3)]

src = [edge[0] for edge in edges]
trg = [edge[1] for edge in edges]
values = [1 for _ in edges]
A_csr = csr_matrix((values, (src, trg)), shape=(4, 4))
A_csr
```
where `src`, `trg`, and `values` are lists of the source nodes, target nodes, and edge weights, respectively.

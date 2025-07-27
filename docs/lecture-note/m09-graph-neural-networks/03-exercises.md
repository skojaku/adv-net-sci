# Exercises: Graph Neural Networks

## Theoretical Exercises

## Pen and Paper Exercises

- [✍️ Pen and paper exercises](pen-and-paper/exercise.pdf)

The pen and paper exercises cover fundamental concepts including spectral graph theory (understanding eigenvalues and eigenvectors of graph matrices), fourier analysis on graphs (extending classical signal processing to graph domains), convolution operations (defining convolution for irregular graph structures), message passing (mathematical formulation of information aggregation in graphs), and network architecture design (principles for designing effective GNN architectures).

## Programming Exercises

**Coding Exercise: GCN Implementation**

::: {.callout-note title="Exercise"}
:class: note

Let's implement a simple GCN model for node classification.
[Coding Exercise](../../../notebooks/exercise-m09-graph-neural-net.ipynb)
:::

This coding exercise will guide you through building a GCN from scratch (implementing the basic GCN layer), node classification (training GCN for semi-supervised node classification), spectral filtering (understanding how GCNs relate to spectral graph theory), and comparison with other methods (benchmarking against traditional approaches).

**Key Learning Objectives:** Through these exercises, you will understand the mathematics (connect spectral graph theory to practical GNN implementations), implement core algorithms (build GCN, GraphSAGE, GAT, and GIN from fundamental principles), apply to real problems (use GNNs for node classification, graph classification, and link prediction), analyze performance (compare different GNN architectures and understand their strengths/weaknesses), and debug and optimize (learn common pitfalls and optimization strategies for GNNs).

**Exercise Topics:** The exercises cover basic GCN implementation (implement the GCN layer forward pass, add self-loops and normalization, train on Cora dataset for node classification), spectral analysis (visualize graph spectra and eigenvectors, implement spectral filtering, compare low-pass vs high-pass filters), advanced architectures (implement GraphSAGE with different aggregators, build GAT with attention visualization, create GIN and test on graph isomorphism), and practical applications (social network analysis, citation network node classification, molecular property prediction).

These exercises bridge theory and practice, ensuring you understand both the mathematical foundations and practical implementation details of Graph Neural Networks.
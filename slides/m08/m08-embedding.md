---
marp: true
theme: math
paginate: true
footer: "Sadamori Kojaku, 2026"
---

<!-- MOCK (2026-11-02). Figures marked "placeholder" are boxes to be replaced; the animation slide is a
     static three-frame version. Wireframe: review/WIREFRAME.md. Build: python3 figures/make_figures.py;
     python3 ~/.claude/skills/slide-math/tools/check.py m08-embedding.md -->

<!-- _class: title -->
<!-- _paginate: false -->
<!-- _footer: "" -->

# Embedding

## from words to <span class="hot">networks</span>

Module 8: word2vec, hyperbolic and spectral embeddings

<p class="by">Sadamori Kojaku</p>

---

<!-- _class: agenda -->

## Outline

1. From words to nodes
2. Hyperbolic embedding
3. Spectral embedding

---

<!-- _class: divider -->

<p class="crumb">Embedding</p>

## From words to nodes

---

## Hand-made node features

A prediction model needs a vector of numbers for every node, and for networks these numbers have been computed by hand.

<div class="cols c12 mid">
<div>

- degree $k_i$
- number of triangles $t_i$
- return probability of a random walk, $(\mathbf P^t)_{ii}$
- <span class="key">each task needs its own choice of features</span>

</div>
<div class="fig">

![](figures/feat.svg)

</div>
</div>

---

## Representation learning

Representation learning trains the node vectors $\vb x_i \in \R^d$ on data instead of designing them by hand.

<div class="fig">

![](figures/pipeline.svg)

</div>

- the vectors go into any standard model: a classifier, a clustering method, a link predictor
- the training signal comes from the network itself, without labels

---

## word2vec: words as vectors

word2vec (Mikolov et al. 2013) gives every word a vector so that words used in similar contexts get close vectors.

<div class="cols c11 mid">
<div>

<div class="box" data-tab="Vector arithmetic">

$$\vb x_{\text{king}} - \vb x_{\text{man}} + \vb x_{\text{woman}} \approx \vb x_{\text{queen}}$$

<div class="note">

The offset man $\to$ woman has the same direction as king $\to$ queen.

</div>
</div>

- a relation between words is a direction in the space
- comparing meanings reduces to linear algebra

</div>
<div class="fig">

![w:560](figures/analogy.svg)

</div>
</div>

<div class="ref">Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). Efficient estimation of word representations in vector space. arXiv:1301.3781.</div>

---

## Prediction from context

word2vec predicts a word from a nearby word; every word has a query vector $\vb u$ and a key vector $\vb v$.

<div class="fig">

![](figures/sentence.svg)

</div>

<div class="cols c11">
<div class="box tight" data-tab="Query">

$\vb u_i$ represents word $i$ when it is the input

</div>
<div class="box tight" data-tab="Key">

$\vb v_j$ represents word $j$ when it is the word to predict

</div>
</div>

---

## Training by contrast

A real pair is pulled together and a random pair is pushed apart, which is logistic regression on $\vb u_i^\top \vb v_j$.

<div class="cols c11 mid">
<div>

| input $i$ | other word $j$ | label $y$ |
|---|---|---|
| <mark>favors</mark> | <mark>prepared</mark> | 1 |
| favors | water | 0 |
| only | mind | 1 |
| only | stone | 0 |

<div class="note">

Label 1: a pair from the text. Label 0: the second word is drawn at random.

</div>
</div>
<div class="box" data-tab="Objective for one real pair">

$$\Pr(y=1 \mid i, j) = \sigma(\vb u_i^\top \vb v_j)$$

$$\ell = -\log \sigma(\vb u_i^\top \vb v_j) - \log \sigma(-\vb u_i^\top \vb v_{j'})$$

<div class="note">

$j'$ is a random word; $\sigma(z) = 1/(1+e^{-z})$.

</div>
</div>
</div>

---

## Walks as sentences

A random walk on a network is a sequence of nodes, in the same way that a sentence is a sequence of words.

<div class="cols c11 mid">
<div class="fig">

![](figures/walkgraph.svg)

</div>
<div class="kv">

| text | network |
|---|---|
| word | node |
| sentence | random walk |
| neighbors | nodes close together in a walk |

</div>
</div>

---

## DeepWalk (Perozzi et al. 2014)

DeepWalk trains word2vec on random walks, with nodes in place of words.

<div class="cols flow c111 stretch">
<div class="box" data-tab="1  Walks">

Start walkers from every node and record the visited nodes:

$3 \to 1 \to 4 \to 2 \to 3 \to \cdots$

</div>

<span class="tri"></span>

<div class="box" data-tab="2  Pairs">

Pair each node with the nodes within $w$ steps in the same walk:

$(3,1),\ (3,4),\ (1,4),\ \dots$

</div>

<span class="tri"></span>

<div class="box" data-tab="3  word2vec">

Train $\vb u_i, \vb v_j$ so that these pairs are real and random pairs are fake

</div>
</div>

- the vector of node $i$ is $\vb u_i$

<div class="ref">Perozzi, B., Al-Rfou, R., & Skiena, S. (2014). DeepWalk: online learning of social representations. KDD.</div>

---

## The walk rule sets what is close

Nodes that appear together in walks get close vectors, so a different walk rule gives a different embedding.

<div class="fig">

![](figures/walks-compare.svg)

</div>

<div class="cols c11 stretch">
<div class="box tight" data-tab="Plain walk">

$$\Pr(i \to j) = \frac{A_{ij}}{k_i}$$

</div>
<div class="box tight" data-tab="Walk with restart (personalized PageRank)">

$$\Pr(i \to j) = \alpha\,[\,j = s\,] + (1-\alpha)\frac{A_{ij}}{k_i}$$

</div>
</div>

- node2vec biases the step with two parameters, $p$ and $q$ (Grover & Leskovec 2016)

---

## Lab: character embeddings

In the lab notebook, walkers run on the Les Misérables co-appearance network and word2vec embeds the characters.

<div class="cols c11">
<div>

- the walk simulator and the word2vec call are given
- choose a character and list the closest vectors
- plot the 77 characters in two dimensions

</div>
<div>

<div class="box grey" data-tab="Notebook">

QR code and short link <span class="tag">placeholder</span>

</div>
<div class="box grey" data-tab="Output">

Two-dimensional map of the characters <span class="tag">placeholder</span>

</div>
</div>
</div>

---

## Lab task: personalized PageRank walk

Implement a walk that returns to a favourite character $s$ with probability $\alpha$ at every step, then compare the embeddings.

<div class="cols c32">
<div>

```python
def ppr_walk(G, start, length, alpha, rng):
    walk = [start]
    # TODO: with probability alpha, return to `start`;
    #       otherwise move to a uniformly chosen neighbour
    return walk
```

</div>
<div>

- which characters are closest to $s$ for $\alpha = 0.05$ and for $\alpha = 0.5$?
- how do they differ from the closest characters under the plain walk?

</div>
</div>

---

<!-- _class: divider -->

<p class="crumb">Embedding</p>

## Hyperbolic embedding

---

## Popularity and similarity

Papadopoulos et al. (2012) grow a network with two forces: a new node attaches to popular nodes and to similar nodes.

<div class="fig">

![](figures/popsim.svg)

</div>

- popularity: a node that arrived earlier has had more time to collect links
- similarity: nodes that are alike are placed close to each other

<div class="ref">Papadopoulos, F., Kitsak, M., Serrano, M. Á., Boguñá, M., & Krioukov, D. (2012). Popularity versus similarity in growing networks. Nature, 489, 537–540.</div>

---

## Growth rule of the model

Node $t$ gets a radius from its arrival time and an angle at random, and links to the $m$ existing nodes closest to it in the hyperbolic disk.

<div class="cols c11 stretch">
<div class="box tight" data-tab="Coordinates of node t">

$$r_t = \ln t \qquad \theta_t \sim \mathrm{Uniform}[0, 2\pi)$$

</div>
<div class="box tight" data-tab="Links of node t">

the $m$ nodes $s < t$ with the smallest $s\,\theta_{st}$

</div>
</div>

<div class="fig">

![](figures/growth.svg)

<div class="cap">

Simulation with $m=2$, 60 nodes; the newest node and its links are marked. <span class="tag">animation planned</span>

</div>

</div>

---

## Observed degree mixes two effects

Degree is the one quantity that can be observed, and in it popularity and similarity are mixed.

<div class="parts eq-lg">
<div class="part">

$$k_i \;\propto$$

</div>
<div class="part" data-tag="popularity">

$$\hl{\kappa_i}$$

<div class="pin">

hidden degree

</div>
</div>
<div class="part">

$$\times$$

</div>
<div class="part" data-tag="similarity">

$$\hlc{n_i}$$

<div class="pin">

community size

</div>
</div>
</div>

- the same $k_i$ can come from a large $\kappa_i$ with few similar nodes or a small $\kappa_i$ with many
- $\kappa_i$ cannot be read from $k_i$ alone

---

## Same degree, different hidden degree

Two nodes with degree 6 have different hidden degrees when their communities differ in size.

<div class="cols c21 mid">
<div class="fig">

![](figures/communities.svg)

</div>
<div>

- large community: many similar nodes, so a small $\kappa$ gives $k = 6$
- small community: few similar nodes, so $k = 6$ needs a large $\kappa$
- <span class="key">the node in the small community attracts links more strongly</span>

</div>
</div>

---

## Exponential growth of hyperbolic space

In the hyperbolic plane of curvature $-1$, the circumference of a circle grows exponentially with its radius.

<div class="cols c32 mid">
<div>

<div class="box" data-tab="Circle of radius r">

$$C_{\text{hyp}}(r) = 2\pi \sinh r \approx \pi e^{r}$$

$$C_{\text{Euclid}}(r) = 2\pi r$$

</div>

- the area $2\pi(\cosh r - 1)$ also grows as $e^{r}$
- the radius is the logarithm of the number of nodes that fit

</div>
<div class="fig">

![](figures/circumference.svg)

</div>
</div>

---

## Hyperbolic space as a continuous tree

A tree with branching factor $b$ has $b^d$ nodes at depth $d$, and hyperbolic space has room that grows in the same way.

<div class="cols flow c11 mid">
<div class="fig">

![](figures/tree-plain.svg)

</div>

<span class="tri"></span>

<div class="fig">

![](figures/tree-disk.svg)

<div class="cap">

Poincaré disk; depth $d$ at hyperbolic distance $0.9\,d$ from the center; edges are geodesics.

</div>
</div>
</div>

- distances grow with the logarithm of the number of nodes: a log scale in space

---

## WordNet in the Poincaré disk

In a Poincaré embedding of WordNet, general words lie near the center and specific words near the boundary.

<div class="fig">

<div class="panel">

![h:470](../legacy/m08/figs/wordnet-hyperbolic-embedding.png)

</div>
<p class="cap">Poincaré embedding of the WordNet noun hierarchy (Nickel & Kiela 2017).</p>
</div>

---

<!-- _class: divider -->

<p class="crumb">Embedding</p>

## Spectral embedding

---

## Compressing a matrix

The adjacency matrix has $N^2$ entries, and a spectral embedding keeps an $N \times d$ matrix $\mathbf U$ that rebuilds it as closely as possible.

<div class="fig">

![](figures/compress.svg)

</div>

<div class="box" data-tab="Objective">

$$\min_{\mathbf U \in \R^{N \times d}} \ \| \mathbf A - \mathbf U \mathbf U^{\top} \|_F$$

<div class="note">

PCA compresses a data matrix in the same way; here the matrix is $\mathbf A$ and the vectors are its eigenvectors.

</div>
</div>

---

## Eigendecomposition

A symmetric matrix is a weighted sum of outer products of its eigenvectors.

<div class="box" data-tab="Eigendecomposition">

$$\mathbf A = \sum_{k=1}^{N} \lambda_k \, \mathbf u_k \mathbf u_k^{\top}$$

<div class="note">

$\mathbf u_k$ is a unit eigenvector with eigenvalue $\lambda_k$; $\mathbf u_k \mathbf u_k^{\top}$ is an $N \times N$ matrix.

</div>
</div>

<div class="fig">
<div class="figtitle">

Zachary's karate club: $\mathbf A$ and its first three terms

</div>

![](figures/layers.svg)

</div>

---

## Keeping the large terms

Keeping the $d$ terms with the largest $|\lambda_k|$ gives the rank-$d$ approximation $\mathbf A_d$.

<div class="cols c32">
<div>

<div class="box" data-tab="Rank-d approximation">

$$\mathbf A_d = \sum_{k=1}^{d} \lambda_k \, \mathbf u_k \mathbf u_k^{\top}$$

<div class="note">

Eigenvalues are ordered so that $|\lambda_1| \ge |\lambda_2| \ge \cdots$.

</div>
</div>

<div class="fig">

![](figures/recon.svg)

</div>
</div>
<div>

<div class="fig">
<p class="figtitle">Eigenvalues</p>

![](figures/spectrum.svg)

</div>
</div>
</div>

---

## Optimality of the truncation

Among all matrices of rank at most $d$, $\mathbf A_d$ is the closest to $\mathbf A$ in the Frobenius norm.

<div class="def">

Frobenius norm: $\| \mathbf M \|_F = \sqrt{\sum_{i,j} M_{ij}^2}$

</div>

<div class="cols c11 mid">
<div class="box" data-tab="Eckart–Young–Mirsky">

$$\mathbf A_d = \arg\min_{\operatorname{rank}(\mathbf B) \le d} \| \mathbf A - \mathbf B \|_F$$

$$\| \mathbf A - \mathbf A_d \|_F^{\,2} = \sum_{k > d} \lambda_k^2$$

</div>
<div class="fig">
<p class="figtitle">Karate club</p>

![](figures/error.svg)

</div>
</div>

<div class="ref">Eckart, C., & Young, G. (1936). The approximation of one matrix by another of lower rank. Psychometrika, 1, 211–218.</div>

---

## Matrices that represent a network

The matrix to decompose is a choice, and the Laplacian and the normalized Laplacian both come from graph cuts.

<div class="kv">

| name | definition |
|---|---|
| adjacency matrix | $\mathbf A$, with $A_{ij} = 1$ if $i$ and $j$ are linked |
| degree matrix | $\mathbf D = \operatorname{diag}(k_1, \dots, k_N)$ |
| Laplacian | $\mathbf L = \mathbf D - \mathbf A$ |
| normalized Laplacian | $\mathbf L_{\mathrm{sym}} = \mathbf I - \mathbf D^{-1/2} \mathbf A \mathbf D^{-1/2}$ |

</div>

- for $\mathbf A$, keep the eigenvectors with the largest eigenvalues
- for $\mathbf L$ and $\mathbf L_{\mathrm{sym}}$, keep those with the smallest eigenvalues

---

## Cutting a network in two

A cut splits the nodes into $S$ and $T$, and Ratio Cut divides the cut size by the group sizes so that a single node is not a good cut.

<div class="box eq-sm" data-tab="Ratio Cut">

$$\mathrm{cut}(S,T) = \sum_{i \in S} \sum_{j \in T} A_{ij} \qquad \mathrm{RatioCut}(S,T) = \mathrm{cut}(S,T) \left( \frac{1}{|S|} + \frac{1}{|T|} \right)$$

</div>

<div class="cols c11">
<div class="fig">
<div class="figtitle">

$S = \{p\}$

</div>

![](figures/cuts.svg)

<div class="cap">

$\mathrm{cut} = 1$, $\mathrm{RatioCut} = 1 \times (1 + \tfrac{1}{10}) = 1.10$

</div>
</div>
<div class="fig">
<div class="figtitle">

$S$ = the left clique and $p$

</div>

![](figures/cuts-bridge.svg)

<div class="cap">

$\mathrm{cut} = 1$, $\mathrm{RatioCut} = 1 \times (\tfrac{1}{6} + \tfrac{1}{5}) = 0.37$

</div>
</div>
</div>

---

## Group indicator vector

A cut is encoded by a vector $\vb x$ that takes one value on $S$ and another on $T$.

<div class="cols c11 mid">
<div class="box" data-tab="Indicator of (S, T)">

$$x_i = \begin{cases} \ \ \sqrt{|T|/|S|} & i \in S \\ -\sqrt{|S|/|T|} & i \in T \end{cases}$$

<div class="note">

Here $N = |S| + |T|$.

</div>
</div>
<div>

- $\sum_i x_i = 0$
- $\sum_i x_i^2 = N$

</div>
</div>

<div class="fig">
<div class="figtitle">

$\vb x$ for the second cut: $|S| = 6$, $|T| = 5$

</div>

![](figures/indicator.svg)

</div>

---

## Ratio Cut as a quadratic form

With the indicator $\vb x$, the Ratio Cut is $\vb x^\top \mathbf L \vb x / N$, where $\mathbf L = \mathbf D - \mathbf A$ is the Laplacian.

<div class="box eq-lg" data-tab="Result">

$$\mathrm{RatioCut}(S,T) = \frac{1}{N}\, \vb x^\top \mathbf L \vb x$$

</div>

<div class="box eq-sm" data-tab="Derivation: pen and paper, Q2 and Q3">

$$
\begin{aligned}
\vb x^\top \mathbf L \vb x &= \sum_i k_i x_i^2 - \sum_{i,j} A_{ij} x_i x_j = \tfrac{1}{2} \sum_{i,j} A_{ij} (x_i - x_j)^2 && \why{(Q2)}\\
&= \mathrm{cut}(S,T)\,(x_S - x_T)^2 = \mathrm{cut}(S,T)\,\frac{N^2}{|S|\,|T|} && \why{(Q3)}\\
&= N \,\mathrm{RatioCut}(S,T)
\end{aligned}
$$

</div>

---

## Relaxation to real values

Dropping the two-value constraint turns an NP-hard problem into an eigenvalue problem.

<div class="box eq-sm" data-tab="Discrete problem (NP-hard)">

$$\min_{\vb x} \ \vb x^\top \mathbf L \vb x \quad \text{s.t.} \quad x_i \in \left\{ \sqrt{|T|/|S|},\ -\sqrt{|S|/|T|} \right\},\ \ \vb x^\top \mathbf 1 = 0,\ \ \vb x^\top \vb x = N$$

</div>

<div class="darrow r"></div>

<div class="box eq-sm" data-tab="Relaxed problem">

$$\min_{\vb x \in \R^N} \ \vb x^\top \mathbf L \vb x \quad \text{s.t.} \quad \vb x^\top \mathbf 1 = 0,\ \ \vb x^\top \vb x = N \qquad\Longrightarrow\qquad \mathbf L \vb x = \lambda \vb x, \quad \vb x^\top \mathbf L \vb x = \lambda N$$

</div>

- the smallest eigenvalue is 0, with $\vb x \propto \mathbf 1$, which $\vb x^\top \mathbf 1 = 0$ excludes
- <span class="key">the solution is the eigenvector with the second smallest eigenvalue</span>

---

## Second eigenvector of the Laplacian

On Zachary's karate club, the entries of the second eigenvector of $\mathbf L$ separate the two factions, and the sign gives the cut.

<div class="fig">
<p class="figtitle">Entries of the second eigenvector, sorted; <mark>Mr. Hi's faction</mark> and <mark class="alt">the officer's faction</mark></p>

![](figures/fiedler.svg)

</div>

- the sign matches the faction for 33 of the 34 members

---

## Normalized Cut

Normalized Cut replaces group sizes with group volumes, and the same steps apply.

<div class="def">

Volume: $\mathrm{vol}(S) = \sum_{i \in S} k_i$ <span class="gap"></span> $\mathrm{vol}(G) = \sum_{i} k_i = 2m$

</div>

<div class="cols c11 stretch">
<div class="box eq-sm" data-tab="Normalized Cut">

$$\mathrm{NCut}(S,T) = \mathrm{cut}(S,T) \left( \frac{1}{\mathrm{vol}(S)} + \frac{1}{\mathrm{vol}(T)} \right)$$

</div>
<div class="box eq-sm" data-tab="Indicator">

$$x_i = \begin{cases} \ \ \sqrt{\mathrm{vol}(T)/\mathrm{vol}(S)} & i \in S \\ -\sqrt{\mathrm{vol}(S)/\mathrm{vol}(T)} & i \in T \end{cases}$$

</div>
</div>

<div class="box" data-tab="Properties (pen and paper, Q4)">

$$\vb x^\top \mathbf D \mathbf 1 = 0 \qquad \vb x^\top \mathbf D \vb x = \mathrm{vol}(G) \qquad \vb x^\top \mathbf L \vb x = \mathrm{vol}(G)\, \mathrm{NCut}(S,T)$$

</div>

---

## Relaxation of Normalized Cut

Relaxing $\vb x$ to real values gives $\mathbf L \vb x = \lambda \mathbf D \vb x$, an eigenvalue problem of the normalized Laplacian.

<div class="box eq-sm" data-tab="Relaxed problem">

$$\min_{\vb x \in \R^N} \ \vb x^\top \mathbf L \vb x \quad \text{s.t.} \quad \vb x^\top \mathbf D \mathbf 1 = 0,\ \ \vb x^\top \mathbf D \vb x = \mathrm{vol}(G)$$

</div>

<div class="darrow r"></div>

<div class="box eq-sm" data-tab="Solution (pen and paper, Q5)">

$$\mathbf L \vb x = \lambda \mathbf D \vb x \qquad \overset{\vb y = \mathbf D^{1/2} \vb x}{\Longleftrightarrow} \qquad \mathbf L_{\mathrm{sym}} \vb y = \lambda \vb y, \quad \mathbf L_{\mathrm{sym}} = \mathbf I - \mathbf D^{-1/2} \mathbf A \mathbf D^{-1/2}$$

</div>

- the solution is the eigenvector with the second smallest eigenvalue, as for Ratio Cut

---

## Pen and paper: from the cut to the Laplacian

Derive the Ratio Cut result and the Normalized Cut counterpart on paper (10 minutes).

<div class="kv">

| question | task |
|---|---|
| Q1 | check $\sum_i x_i = 0$ and $\sum_i x_i^2 = N$ for the indicator of Ratio Cut |
| Q2 | show $\vb x^\top \mathbf L \vb x = \tfrac{1}{2} \sum_{i,j} A_{ij} (x_i - x_j)^2$ |
| Q3 | show $\vb x^\top \mathbf L \vb x = N\, \mathrm{RatioCut}(S,T)$ |
| Q4 | repeat Q1 to Q3 for Normalized Cut |
| Q5 | derive $\mathbf L_{\mathrm{sym}} \vb y = \lambda \vb y$ from $\mathbf L \vb x = \lambda \mathbf D \vb x$ |

</div>

---

<!-- _class: roomy -->

## Summary

- word2vec learns a vector per word from word pairs; DeepWalk applies it to random walks
  - the walk rule decides which nodes are close
- hyperbolic embedding places nodes by popularity (radius) and similarity (angle)
  - the space grows exponentially, as a tree does
- spectral embedding keeps the eigenvectors with the largest terms of $\mathbf A$
  - the Laplacian comes from the continuous relaxation of Ratio Cut; the normalized Laplacian, from Normalized Cut

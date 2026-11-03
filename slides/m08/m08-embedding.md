---
marp: true
theme: math
paginate: true
footer: "Sadamori Kojaku, 2026"
---

<style>
/* Classroom size: type about 1.5x the skill default (body 34 px instead of 21 px). */
section {
  --fs: 34px;
  --fs-lead: 32px;
  --fs-title: 44px;
  --fs-small: 24px;
  --fs-code: 26px;
  padding: 92px 50px 52px 57px;
}
section > h2 { top: 15px; line-height: 54px; }
section > h2::before { height: 54px; width: 12px; left: -26px; }
section > h2 + p { line-height: 1.36; margin: 0 0 12px -8px; max-width: 1180px; }
section .box { padding: 18px 28px; margin: 0 0 16px; }
section .box[data-tab] { margin-top: 30px; padding-top: 38px; }
section .box[data-tab]::before { font-size: 28px; height: 48px; line-height: 48px; top: -25px; }
section .tag, section .part[data-tag]::before { font-size: 24px; }
section .figtitle { font-size: 24px; margin-bottom: 8px; }
section .ref { font-size: 15px; bottom: 30px; }
section > footer, section::after { font-size: 14px; }
section .tri { border-width: 15px 0 15px 22px; }
section .cols.flow { grid-template-columns: minmax(0, 1fr) 30px minmax(0, 1fr); }
section .parts { margin: 64px 0 140px; }
section .part[data-tag]::before { bottom: calc(100% + 10px); }
section .pin { padding-top: 56px; }
section .pin::before { height: 44px; }
section pre { padding: 14px 26px; line-height: 1.55; flex-shrink: 0; }
section th, section td { padding: 6px 18px; }
section table { margin-bottom: 14px; }
section.divider > h2 { font-size: 56px; }
section.divider .crumb { font-size: 26px; }
section.agenda ol > li { font-size: 52px; }
</style>

<!-- MOCK v2 (2026-11-03). Classroom-size type, two columns (text left, figure right). The lab QR is a placeholder; the
     growth slide is one frame of the planned animation. Wireframe: review/WIREFRAME.md. Build: python3 figures/make_figures.py;
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

Prediction models need a vector of numbers for every node, and for networks these numbers have been designed by hand.

<div class="cols c11 mid">
<div>

- degree $k_i$
- number of triangles $t_i$
- return probability $(\mathbf P^t)_{ii}$ of a random walk
- <span class="key">each task needs a new choice of features</span>

</div>
<div class="fig">

![w:569](figures/feat.svg)

</div>
</div>

---

## Representation learning

Representation learning trains the node vectors $\vb x_i \in \R^d$ on data instead of designing them by hand.

<div class="fig">

![](figures/pipeline.svg)

</div>

- the vectors feed any model: a classifier, a clustering method, a link predictor
- the training signal comes from the network itself, without labels

---

## word2vec: words as vectors

word2vec (Mikolov et al. 2013) gives every word a vector, so that words used in similar contexts get close vectors.

<div class="cols c11 mid">
<div>

<div class="box eq-sm">

$$\begin{aligned} & \vb x_{\text{king}} - \vb x_{\text{man}} + \vb x_{\text{woman}} \\ & \approx \vb x_{\text{queen}} \end{aligned}$$

</div>

- a relation between words is a direction
- meaning is compared by linear algebra

</div>
<div class="fig">

![w:569](figures/analogy.svg)

</div>
</div>

<div class="ref">Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). Efficient estimation of word representations in vector space. arXiv:1301.3781.</div>

---

## Prediction from context

word2vec predicts a word from a nearby word; every word has a query vector $\vb u$ and a key vector $\vb v$.

<div class="fig">

![](figures/sentence.svg)

</div>

- a pair $(i, j)$ that appears in the text gets a high score $\vb u_i^\top \vb v_j$

---

## Training by contrast

A real pair (label 1) is pulled together and a random pair (label 0) is pushed apart.

<div class="cols c11 mid">
<div>

| input $i$ | other $j$ | label $y$ |
|---|---|---|
| <mark>favors</mark> | <mark>prepared</mark> | 1 |
| favors | water | 0 |
| only | mind | 1 |
| only | stone | 0 |

</div>
<div class="fig">

![](figures/contrast.svg)

</div>
</div>

<div class="box eq-sm">

$$\Pr(y=1 \mid i, j) = \sigma(\vb u_i^\top \vb v_j) \quad \ell = -\log \sigma(\vb u_i^\top \vb v_j) - \log \sigma(-\vb u_i^\top \vb v_{j'})$$

</div>

---

## Walks as sentences

A random walk on a network is a sequence of nodes, in the same way that a sentence is a sequence of words.

<div class="cols c11 mid">
<div>

| text | network |
|---|---|
| word | node |
| sentence | random walk |
| nearby words | nodes close together in a walk |

</div>
<div class="fig">

![](figures/walkgraph.svg)

</div>
</div>

---

## DeepWalk (Perozzi et al. 2014)

DeepWalk trains word2vec on random walks, with nodes in place of words.

<div class="fig">

![](figures/deepwalk.svg)

</div>

- every node $i$ gets a query vector $\vb u_i$ and a key vector $\vb v_i$; $\vb u_i$ is its embedding
- settings: walks per node, walk length, window size; node2vec biases the walk with $p$ and $q$

<div class="ref">Perozzi, B., Al-Rfou, R., & Skiena, S. (2014). DeepWalk: online learning of social representations. KDD.</div>

---

## The walk rule sets what is close

Nodes that appear together in walks get close vectors, so a different walk rule gives a different embedding.

<div class="cols c32">
<div>

<div class="box">

**Plain walk**: move to a random neighbor

$$\Pr(i \to j) = A_{ij} / k_i$$

</div>

Another rule is a **walk with restart** (personalized PageRank): return to the start node $s$ with probability $\alpha$.

<div class="eq-sm">

$$\Pr(i \to j) = \alpha\,[\,j = s\,] + (1-\alpha)\,A_{ij} / k_i$$

</div>

</div>
<div class="fig">

![](figures/walks-compare.svg)

</div>
</div>

---

## Lab: character embeddings

In the lab notebook, walkers run on the Les Misérables co-appearance network and word2vec embeds the characters.

<div class="cols c11">
<div>

- the walk simulator and the word2vec call are given
- choose a character and list the closest vectors
- plot the 77 characters in two dimensions

<div class="box grey">

QR code and short link <span class="tag">placeholder</span>

</div>
</div>
<div class="fig">

![w:520](figures/lesmis.svg)

<div class="cap">

Valjean (lavender) and his 10 closest characters (cyan).

</div>
</div>
</div>

---

## Lab task: personalized PageRank walk

Implement a walk that restarts at the start node with probability $\alpha$.

```python
def ppr_walk(G, start, length, alpha, rng):
    walk = [start]
    # TODO: with probability alpha, go back to `start`;
    #       otherwise move to a random neighbor
    return walk
```

<div class="cols c11 mid">
<div>

- closest characters to $s$ for $\alpha = 0.05$ and $\alpha = 0.5$?
- how do they differ from the plain walk?

</div>
<div class="fig">

![](figures/ppr-step.svg)

</div>
</div>

---

<!-- _class: divider -->

<p class="crumb">Embedding</p>

## Hyperbolic embedding

---

## Popularity and similarity

Papadopoulos et al. (2012) add similarity to preferential attachment.

<div class="fig">

![w:960](figures/pa-vs-ps.svg)

</div>

- popularity: an earlier node has had more time to collect links
- similarity: nodes that are alike are placed close to each other

<div class="ref">Papadopoulos, F. et al. (2012). Popularity versus similarity in growing networks. Nature, 489, 537–540.</div>

---

## Growth rule of the model

Node $t$ gets a radius from its arrival time and a random angle, and links to the $m$ closest existing nodes.

<div class="cols c11 mid">
<div>

<div class="box eq-sm">

$$r_t = \ln t$$

$$\theta_t \sim \mathrm{Uniform}[0, 2\pi)$$

link to the $m$ nodes $s < t$ with the smallest $s\,\theta_{st}$

</div>

- $\theta_{st}$: angle between $s$ and $t$

</div>
<div class="fig">

![w:450](figures/growth.svg)

<div class="cap">

$m=2$, newest node $t=40$ (animation planned).

</div>
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

- the same $k_i$ can come from a large $\kappa_i$ with few similar nodes, or a small $\kappa_i$ with many
- $\kappa_i$ cannot be read from $k_i$ alone

---

## Same degree, different hidden degree

Two nodes with degree 6 have different hidden degrees when their communities differ in size.

<div class="cols c11 mid">
<div>

- large community: many similar nodes, so a small $\kappa$ gives $k = 6$
- small community: few similar nodes, so $k = 6$ needs a large $\kappa$
- <span class="key">the node in the small community attracts links more strongly</span>

</div>
<div class="fig">

![](figures/communities.svg)

</div>
</div>

---

## Exponential growth of hyperbolic space

In the hyperbolic plane of curvature $-1$, the circumference of a circle grows exponentially with its radius.

<div class="cols c11 mid">
<div>

<div class="box eq-sm">

$$C_{\text{hyp}}(r) = 2\pi \sinh r \approx \pi e^{r}$$

$$C_{\text{Euclid}}(r) = 2\pi r$$

</div>

- the area $2\pi(\cosh r - 1)$ also grows as $e^{r}$
- the radius is the logarithm of the number of nodes that fit

</div>
<div class="fig">

![w:569](figures/circumference.svg)

</div>
</div>

---

## Hyperbolic space as a continuous tree

Hyperbolic space is the continuous version of a tree.

<div class="cols flow c11 mid">
<div class="fig">

![w:460](figures/tree-plain.svg)

</div>

<span class="tri"></span>

<div class="fig">

![w:370](figures/tree-disk.svg)

<div class="cap">

Poincaré disk, depth $d$ at distance $0.9\,d$.

</div>
</div>
</div>

- depth $d$ of a tree holds $b^d$ nodes; hyperbolic space grows in the same way

---

## WordNet in the Poincaré disk

General words lie near the center and specific words near the boundary.

<div class="cols c11 mid">
<div>

- center: general words
- boundary: specific words
- the hierarchy of 80,000 nouns fits in a disk of two dimensions

</div>
<div class="fig">

![h:505](../legacy/m08/figs/wordnet-hyperbolic-embedding.png)

</div>
</div>

<div class="ref">Image: Poincaré embedding of WordNet nouns (Nickel & Kiela 2017; source to be confirmed).</div>

---

<!-- _class: divider -->

<p class="crumb">Embedding</p>

## Spectral embedding

---

## Compressing a matrix

A spectral embedding keeps an $N \times d$ matrix $\mathbf U$ that rebuilds the $N \times N$ adjacency matrix as closely as possible.

<div class="cols c11 mid">
<div>

<div class="box eq-sm" data-tab="Objective">

$$\min_{\mathbf U \in \R^{N \times d}} \ \| \mathbf A - \mathbf U \mathbf U^{\top} \|_F$$

</div>

- PCA compresses a data matrix in the same way
- here the matrix is $\mathbf A$ and the vectors are its eigenvectors

</div>
<div class="fig">

![w:569](figures/compress.svg)

</div>
</div>

---

## Eigendecomposition

A symmetric matrix is a weighted sum of outer products of its eigenvectors.

<div class="box">

$$\mathbf A = \sum\nolimits_{k=1}^{N} \lambda_k \, \mathbf u_k \mathbf u_k^{\top}$$

<div class="note">

$\mathbf u_k$: unit eigenvector with eigenvalue $\lambda_k$; $\mathbf u_k \mathbf u_k^{\top}$ is an $N \times N$ matrix.

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

$$\mathbf A_d = \sum\nolimits_{k=1}^{d} \lambda_k \, \mathbf u_k \mathbf u_k^{\top}$$

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

<div class="cols c11">
<div>

<div class="def">

$\| \mathbf M \|_F = \sqrt{\sum_{i,j} M_{ij}^2}$

</div>

<div class="box eq-sm" data-tab="Eckart–Young–Mirsky">

$$\mathbf A_d = \arg\min_{\operatorname{rank}(\mathbf B) \le d} \| \mathbf A - \mathbf B \|_F$$

$$\| \mathbf A - \mathbf A_d \|_F^{\,2} = \sum_{k > d} \lambda_k^2$$

</div>

- <mark>the error is the sum of the squared eigenvalues that are dropped</mark>

</div>
<div class="fig">

![](figures/error-terms.svg)

![](figures/error.svg)

</div>
</div>

<div class="ref">Eckart, C., & Young, G. (1936). The approximation of one matrix by another of lower rank. Psychometrika, 1, 211–218.</div>

---

## Matrices that represent a network

The matrix to decompose is a choice, and the Laplacian and the normalized Laplacian both come from graph cuts.

| name | definition |
|---|---|
| adjacency matrix | $\mathbf A$, with $A_{ij} = 1$ if $i$ and $j$ are linked |
| degree matrix | $\mathbf D = \operatorname{diag}(k_1, \dots, k_N)$ |
| Laplacian | $\mathbf L = \mathbf D - \mathbf A$ |
| normalized Laplacian | $\mathbf L_{\mathrm{sym}} = \mathbf I - \mathbf D^{-1/2} \mathbf A \mathbf D^{-1/2}$ |

- for $\mathbf A$, keep the eigenvectors with the largest eigenvalues
- for $\mathbf L$ and $\mathbf L_{\mathrm{sym}}$, keep those with the smallest eigenvalues

---

## Cutting a network in two

A cut splits the nodes into $S$ and $T$; Ratio Cut divides the cut size by the group sizes.

<div class="box eq-sm">

$$\mathrm{cut}(S,T) = \sum_{i \in S} \sum_{j \in T} A_{ij}$$

$$\mathrm{RatioCut}(S,T) = \mathrm{cut}(S,T) \left( \frac{1}{|S|} + \frac{1}{|T|} \right)$$

</div>

<div class="cols c11">
<div class="fig">

![w:470](figures/cuts.svg)

<div class="cap">

$S = \{p\}$: $1 \times (1 + \tfrac{1}{10}) = 1.10$

</div>
</div>
<div class="fig">

![w:470](figures/cuts-bridge.svg)

<div class="cap">

$S$ = left clique and $p$: $1 \times (\tfrac{1}{6} + \tfrac{1}{5}) = 0.37$

</div>
</div>
</div>

---

## Group indicator vector

A cut is encoded by a vector $\vb x$ that takes one value on $S$ and another on $T$.

<div class="cols c11 mid">
<div>

<div class="box eq-sm">

$$x_i = \begin{cases} \ \ \sqrt{|T|/|S|} & i \in S \\ -\sqrt{|S|/|T|} & i \in T \end{cases}$$

</div>

- $N = |S| + |T|$
- $\sum_i x_i = 0$
- $\sum_i x_i^2 = N$

</div>
<div class="fig">
<div class="figtitle">

$\vb x$ for the second cut: $|S| = 6$, $|T| = 5$

</div>

![](figures/indicator.svg)

</div>
</div>

---

## Ratio Cut as a quadratic form

With the indicator $\vb x$, the Ratio Cut is $\vb x^\top \mathbf L \vb x / N$, where $\mathbf L = \mathbf D - \mathbf A$ is the Laplacian.

<div class="box">

<div class="eq-lg">

$$\mathrm{RatioCut}(S,T) = \frac{1}{N}\, \vb x^\top \mathbf L \vb x$$

</div>

<hr>

<div class="eq-sm">

$$
\begin{aligned}
\vb x^\top \mathbf L \vb x &= \tfrac{1}{2} \sum_{i,j} A_{ij} (x_i - x_j)^2 && \why{(Q2)}\\
&= \mathrm{cut}(S,T)\,(x_S - x_T)^2 = \mathrm{cut}(S,T)\,\frac{N^2}{|S|\,|T|} && \why{(Q3)}\\
&= N \,\mathrm{RatioCut}(S,T)
\end{aligned}
$$

</div>
</div>

---

## Relaxation to real values

Dropping the two-value constraint turns an NP-hard problem into an eigenvalue problem.

<div class="cols c11">
<div>

<div class="box eq-sm">

$$
\begin{aligned}
& \min_{\vb x \in \R^N} \ \vb x^\top \mathbf L \vb x \\
& \text{s.t. } \vb x^\top \mathbf 1 = 0, \ \ \vb x^\top \vb x = N \\
& \Longrightarrow \ \mathbf L \vb x = \lambda \vb x
\end{aligned}
$$

</div>

- $\lambda = 0$: $\vb x \propto \mathbf 1$, excluded
- <span class="key">the solution is the eigenvector with the second smallest eigenvalue</span>

</div>
<div class="fig">

![w:520](figures/relax.svg)

</div>
</div>

---

## Second eigenvector of the Laplacian

On Zachary's karate club, the sign of the second eigenvector of $\mathbf L$ gives the two factions.

<div class="cols c12 mid">
<div class="fig">

![](figures/karate-net.svg)

</div>
<div class="fig">
<p class="figtitle">Entries of the second eigenvector, sorted; <mark>Mr. Hi's faction</mark> and <mark class="alt">the officer's faction</mark></p>

![](figures/fiedler.svg)

</div>
</div>

- the sign matches the faction for 32 of the 34 members (outlined: 3 and 9)

---

## Normalized Cut

Normalized Cut replaces the group sizes with the group volumes, and the same steps apply.

<div class="def">

Volume: $\mathrm{vol}(S) = \sum_{i \in S} k_i$ <span class="gap"></span> $\mathrm{vol}(G) = \sum_{i} k_i = 2m$

</div>

| | Ratio Cut | Normalized Cut |
|---|---|---|
| objective | $\mathrm{cut}\,\bigl(\frac{1}{\lvert S\rvert} + \frac{1}{\lvert T\rvert}\bigr)$ | $\mathrm{cut}\,\bigl(\frac{1}{\mathrm{vol}(S)} + \frac{1}{\mathrm{vol}(T)}\bigr)$ |
| value on $S$ | $\sqrt{\lvert T\rvert / \lvert S\rvert}$ | $\sqrt{\mathrm{vol}(T) / \mathrm{vol}(S)}$ |
| value on $T$ | $-\sqrt{\lvert S\rvert / \lvert T\rvert}$ | $-\sqrt{\mathrm{vol}(S) / \mathrm{vol}(T)}$ |
| constraints | $\vb x^\top \mathbf 1 = 0$, $\vb x^\top \vb x = N$ | $\vb x^\top \mathbf D \mathbf 1 = 0$, $\vb x^\top \mathbf D \vb x = \mathrm{vol}(G)$ |
| $\vb x^\top \mathbf L \vb x$ | $N \cdot \mathrm{RatioCut}$ | $\mathrm{vol}(G) \cdot \mathrm{NCut}$ |

---

## Relaxation of Normalized Cut

Relaxing $\vb x$ to real values gives $\mathbf L \vb x = \lambda \mathbf D \vb x$, an eigenvalue problem of the normalized Laplacian.

<div class="box">

$$
\begin{aligned}
& \min_{\vb x \in \R^N} \ \vb x^\top \mathbf L \vb x \quad \text{s.t. } \vb x^\top \mathbf D \mathbf 1 = 0, \ \ \vb x^\top \mathbf D \vb x = \mathrm{vol}(G) \\
& \Longrightarrow \ \mathbf L \vb x = \lambda \mathbf D \vb x \ \ \overset{\vb y = \mathbf D^{1/2} \vb x}{\Longleftrightarrow} \ \ \mathbf L_{\mathrm{sym}} \vb y = \lambda \vb y
\end{aligned}
$$

</div>

- $\mathbf L_{\mathrm{sym}} = \mathbf I - \mathbf D^{-1/2} \mathbf A \mathbf D^{-1/2}$; the change of variable is pen and paper Q5
- the solution is the eigenvector with the second smallest eigenvalue, as for Ratio Cut

---

## Pen and paper: from the cut to the Laplacian

Derive the Ratio Cut result and the Normalized Cut counterpart on paper (10 minutes).

<div class="cols c32 mid">
<div>

| question | task |
|---|---|
| Q1 | $\sum_i x_i = 0$ and $\sum_i x_i^2 = N$ |
| Q2 | $\vb x^\top \mathbf L \vb x = \tfrac{1}{2} \sum_{i,j} A_{ij} (x_i - x_j)^2$ |
| Q3 | $\vb x^\top \mathbf L \vb x = N\, \mathrm{RatioCut}$ |
| Q4 | Q1 to Q3 for Normalized Cut |
| Q5 | $\mathbf L \vb x = \lambda \mathbf D \vb x \Rightarrow \mathbf L_{\mathrm{sym}} \vb y = \lambda \vb y$ |

</div>
<div class="fig">

![w:455](figures/cuts-bridge.svg)

</div>
</div>

---

## Summary

- word2vec learns a vector per word from word pairs; DeepWalk applies it to random walks
  - the walk rule decides which nodes are close
- hyperbolic embedding places nodes by popularity (radius) and similarity (angle)
  - the space grows exponentially, as a tree does
- spectral embedding keeps the eigenvectors with the largest terms of $\mathbf A$
  - the Laplacian comes from the continuous relaxation of Ratio Cut; the normalized Laplacian, from Normalized Cut

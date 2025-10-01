---
marp: true
theme: default
paginate: true
---

<style>
img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
</style>


Check list
- [ ] Microphone turned on
- [ ] Zoom room open
- [ ] Recording on
- [ ] Mouse cursor visible
- [ ] Sound Volume on

---

# Advanced Topics in Network Science

Lecture 07: Random Walks
Sadamori Kojaku


---

## What to Learn 📚

- 🎲 Random walks as a powerful tool in network analysis
- 🧮 Characterization of random walks in networks
- 🌟 Steady state distribution, and dynamic behavior
- 🔗 Connection to centrality measures and community detection

---

# Have you ever played this game? 🎮

![bg right:70% width:90%](https://livedoor.blogimg.jp/yoursong1982/imgs/6/d/6d6f0b43.jpg)

---

# Ladder Lottery Game 🪜

- Choose a line.
- Move along the line, cross the horizontal lines if you hit them.
- Stop at the end of the line.
- You'll win if you hit a treasure at the end of the line.

Suppose you know where is the treasure is located. Think a strategy to maximize your winning probability 🤔.

[Interactive demo 👾](https://skojaku.github.io/adv-net-sci/vis/amida-kuji.html)

![bg right:40% width:90%](https://upload.wikimedia.org/wikipedia/commons/6/64/Amidakuji_2022-05-10.gif)


---

## Answer
- Choose the line above the treasure.

## Why?

- Suppose that there is no horizontal line. You'll win if you choose the line above the treasure.
- Now, consider adding few horizontal lines. You'll only move other lines few times, and you'll end up with being on the line centered around the treasure with high probability.
- The chance of winning "diffuses" as the number of horizontal lines increases, with limit close to uniform.

---

# This is a network!

![bg right:40% width:90%](https://upload.wikimedia.org/wikipedia/commons/6/64/Amidakuji_2022-05-10.gif)

---

## Random Walks in Networks 🌐

- 🚶‍♀️ Simple process: Start at a node, randomly move to neighbors
- 🏙️ Analogy: Drunk person walking in a city
- Interestingly, this random process captures many important properties of networks
- Unifies different concepts in network science, e.g., centrality, community structure

![bg right:40% width:90%](../../lecture-note/figs/random-walk.png)

---

# Interactive Demo: Random Walk

[Random Walk Simulator](https://skojaku.github.io/adv-net-sci/vis/random-walks/index.html?)

1. When the random walker makes many steps, where does it tend to visit most frequently?
2. When the walker makes only a few steps, where does it tend to visit?
3. Does the behavior of the walker inform us about centrality of the nodes?
4. Does the behavior of the walker inform us about communities in the network?

---

## Pen and Paper (and a bit of coding) Exercises ✍️

[Pen and Paper Exercise (and a bit of coding)](https://skojaku.github.io/adv-net-sci/m07-random-walks/pen-and-paper.html)

---

# Mathematical Foundations of Random Walks 🧮

---

## Transition Probability Matrix 📊

- $P_{ij} = \frac{A_{ij}}{k_i}$
  - $A_{ij}$: Adjacency matrix element
  - $k_i$: Degree of node $i$

- $\mathbf{P} = \mathbf{D}^{-1}\mathbf{A}$
  - $\mathbf{D}$: Diagonal matrix of node degrees

![bg right:50% width:90%](https://miro.medium.com/v2/resize:fit:970/1*UJCtt-ZviWVb6zEKEwgXQA.png)

---



## Stationary Distribution 📈

- Let us consider a random walk on an undirected network starting from a node. After sufficiently many steps, where will the walker be?

- Let $x_i(t)$ be the probability that a random walker is at node $i$ at time $t$.

- After many steps, $\lim_{t\to\infty} x_i(t) = \pi_i$, which is *time invariant*,  $\pi_i$ is called the stationary distribution

- At stationary state,

    $$
    {\bf \pi} = {\bf \pi P}
    $$

  What is the solution?

---

This is the eigenvector problem.

$$
{\bf \pi} = {\bf \pi P}
$$

One of the **left**-eigenvector of ${\bf P}$ is the stationary distribution

**Question**:
- There are $N$ left-eigenvectors for a network with $N$ nodes. Which one represents the stationary distribution?

---

# Coding Exercise:

- Create a karate-club graph.

    ```python
    import igraph as ig
    import numpy as np

    g = ig.Graph.Famous("Zachary") # Load the Zachary's karate club network
    A = g.get_adjacency_sparse() # Get the adjacency matrix
    ```

- Compute the stationary distribution  by computing $x(t)$ for a large $t$ or solving the eigenvector problem ${\bf \pi} = {\bf \pi P}$.

- Check if the sum of the stationary probabilities are 1.

- Compare the stationary distribution with the degree distribution.
---

# [Stationary distribution coding exercise](https://skojaku.github.io/adv-net-sci/m07-random-walks/random-walks-math.html)


---

## Mixing Time ⏱️

- Time to reach stationary distribution

- $t_{\text{mix}} = \min\{t : \max_{{\bf x}(0)} \|{\bf x}(t) - {\bf \pi}\|_{1} \leq \epsilon\}$

- Bound: $t_{\text{mix}} < \tau \log \left( \frac{1}{\epsilon \min_{i} \pi_i} \right)$
  - $\tau = \frac{1}{1-\lambda_2}$ (Relaxation time)
  - $\lambda_2$: Second smallest eigenvalue of the normalized laplacian

---

## Mixing Time (2)

- Let us express $x(t)$ as

  $$
    {\bf x}(t) = {\bf x}(0) \mathbf{P}^t.
  $$

- The mixing time depends on the initial state $x(0)$ and ${\bf P}^t$.
- However, it is not trivial to analytically compute ${\bf P}^t$ for a large $t$.

---

## Diagonalizability

- It is easy if ${\bf P}$ is **diagonalizable**. What does this mean?

- **Diagonalizable matrix**: A matrix $\mathbf{S}$ is diagonalizable if ${\bf S}$ can be represented as $\mathbf{S} = \mathbf{Q}\mathbf{\Lambda}\mathbf{Q}^{-1}$, where $\mathbf{Q}$ is an invertible matrix and $\mathbf{\Lambda}$ is a diagonal matrix of eigenvalues.

- It is easy to compute a power of a diagonalizable matrix.

- **Exercise**: Compute the power ${\bf S}^2$ of diagonalizable matrix ${\bf S} = \mathbf{Q}\mathbf{\Lambda}\mathbf{Q}^{-1}$.

---

## Power of Diagonalizable Matrix

- ${\bf S}^2 = \mathbf{Q}\mathbf{\Lambda}\mathbf{Q}^{-1} \mathbf{Q}\mathbf{\Lambda}\mathbf{Q}^{-1} = \mathbf{Q}\mathbf{\Lambda}^2\mathbf{Q}^{-1}$

- In general, ${\bf S}^t = \mathbf{Q}\mathbf{\Lambda}^t\mathbf{Q}^{-1}$

![bg right:50% width:100%](https://skojaku.github.io/adv-net-sci/_images/diagonalizable-squared.jpg)

---

## Mixing Time

- Is the transition matrix diagonalizable? Yes!

- Let's introduce a new matrix $\mathbf{\overline A}$ called the normalized adjacency matrix.

  $$
  \mathbf{\overline A} = \mathbf{D}^{-\frac{1}{2}} \mathbf{A} \mathbf{D}^{-\frac{1}{2}}
  $$
  - ${\bf D}$ is a diagonal matrix of node degrees.

- Express the transition matrix $\mathbf{P} = {\bf D}^{-1}{\bf A}$ using $\mathbf{\overline A}$ and $\mathbf{D}$.

---

## Mixing time

The transition matrix $\mathbf{P}$ can be rewritten as
  $$
    \begin{aligned}
    \mathbf{P} &= \mathbf{D}^{-1} \mathbf{A}
    = \mathbf{D}^{-\frac{1}{2}} \underbrace{\left( \mathbf{D}^{-1/2} \mathbf{A} \mathbf{D}^{-1/2} \right)}_{\mathbf{\overline A}} \mathbf{D}^{\frac{1}{2}} \\
    &= \mathbf{D}^{-\frac{1}{2}} \mathbf{\overline A} \mathbf{D}^{\frac{1}{2}}
    \end{aligned}
  $$

Matrix $\mathbf{\overline A}$ is diagonalizable as follows:

$$
\mathbf{\overline A} = \mathbf{Q} \mathbf{\Lambda} \mathbf{Q}^{\top}
$$
- $\mathbf{\Lambda}$ is a diagonal matrix of eigenvalues; $\mathbf{Q}$ is a matrix of eigenvectors of $\mathbf{\overline A}$.

- **Question**: Express $\mathbf{P}^2$ using $\mathbf{D}$, $\mathbf{Q}$, and $\mathbf{\Lambda}$ in the simplest form.

---

## Mixing Time

$$
\begin{aligned}
\mathbf{P}^2 &= \left( \mathbf{D}^{-\frac{1}{2}} {\bf \overline A} \mathbf{D}^{\frac{1}{2}} \right)^2 \\
&= \mathbf{D}^{-\frac{1}{2}} \mathbf{\overline A} \mathbf{D}^{\frac{1}{2}} \mathbf{D}^{-\frac{1}{2}} \mathbf{\overline A} \mathbf{D}^{\frac{1}{2}} \\
& = \mathbf{D}^{-\frac{1}{2}} {\bf \overline A}^2 \mathbf{D}^{\frac{1}{2}} \\
&= \underbrace{\mathbf{D}^{-\frac{1}{2}} \mathbf{Q}}_{{\bf Q}_L} {\bf \Lambda}^2 \underbrace{\mathbf{Q}^\top \mathbf{D}^{\frac{1}{2}}}_{{\bf Q}^\top _R}\\
\end{aligned}
$$

Now, let's focus on the matrices:
$$
{\bf Q}_L = \mathbf{D}^{-\frac{1}{2}} \mathbf{Q}, \quad {\bf Q} _R = \mathbf{D}^{\frac{1}{2}} \mathbf{Q}
$$

Compute the product of ${\bf Q}_L ^\top {\bf Q}_R$

---

## Mixing Time

$$
{\bf Q}_L ^\top {\bf Q}_R = \mathbf{I}
$$

What does this tell you? How can we use this to compute ${\bf P}^t$?

---

$$
{\bf Q}_L ^\top {\bf Q}_R = \mathbf{I}
$$

What does this tell you? How can we use this to compute ${\bf P}^t$?

**Hint**: What is the property of the diagonizable matrix?

---

## Mixing Time

Transition probability matrix $\mathbf{P}$ is diagonalizable as follows:

$$
\mathbf{P} = \mathbf{Q}_L \mathbf{\Lambda} \mathbf{Q}_R
$$

where

$$
{\bf Q}_L = \mathbf{D}^{-\frac{1}{2}} \mathbf{Q}, \quad {\bf Q} _R = \mathbf{D}^{\frac{1}{2}} \mathbf{Q}
$$

**Question**: Express the transition matrix ${\bf P}^t$ using ${\bf Q}_L$, ${\bf \Lambda}$, and ${\bf Q}_R$.

---

## Mixing Time

Going back to the original question on the mixing time, we have

$$
\begin{aligned}
{\bf x}(t) &= {\bf x}(0) \mathbf{P}^t \\
&= {\bf x}(0) \mathbf{Q}_L \mathbf{\Lambda} \mathbf{Q}_R
\end{aligned}
$$

In element-wise, we have

$$
\begin{pmatrix}
x_1(t) \\
x_2(t) \\
\vdots \\
x_N(t)
\end{pmatrix}
 =
 \sum_{\ell=1}^N
 \left[
 \lambda_\ell^t
 \begin{pmatrix}
 q^{(L)}_{\ell 1} \\
 q^{(L)}_{\ell 2} \\
 \vdots \\
 q^{(L)}_{\ell N}
 \end{pmatrix}
 \langle\mathbf{q}^{(R)}_{\ell},  \mathbf{x}(0) \rangle
 \right]
$$

---


$$
\begin{aligned}
{\bf x}(t) &= {\bf x}(0) \mathbf{P}^t \\
&= {\bf x}(0) \mathbf{Q}_L \mathbf{\Lambda} \mathbf{Q}_R
\end{aligned}
$$

In element-wise, we have

$$
\begin{pmatrix}
x_1(t) \\
x_2(t) \\
\vdots \\
x_N(t)
\end{pmatrix}
 =
 \sum_{\ell=1}^N
 \left[
 \lambda_\ell^t
 \begin{pmatrix}
 q^{(L)}_{\ell 1} \\
 q^{(L)}_{\ell 2} \\
 \vdots \\
 q^{(L)}_{\ell N}
 \end{pmatrix}
 \langle\mathbf{q}^{(R)}_{\ell},  \mathbf{x}(0) \rangle
 \right]
$$


![bg right:55% width:90%](https://skojaku.github.io/adv-net-sci/_images/diagonalizable-sum.jpg)

---


## Mixing Time

$$
\begin{pmatrix}
x_1(t) \\
x_2(t) \\
\vdots \\
x_N(t)
\end{pmatrix}
 =
 \sum_{\ell=1}^N
 \left[
 \lambda_\ell^t
 \begin{pmatrix}
 q^{(L)}_{\ell 1} \\
 q^{(L)}_{\ell 2} \\
 \vdots \\
 q^{(L)}_{\ell N}
 \end{pmatrix}
 \langle\mathbf{q}^{(R)}_{\ell},  \mathbf{x}(0) \rangle
 \right]
$$

- $\lambda_i \leq 1$ (the blue balls) with equality holds for the largest eigenvalue $\lambda_1 = 1$.
- When $t \rightarrow \infty$, only the largest eigenvalue $\lambda_1$ survives
- Other eigenvalues $\lambda_i$ decay exponentially as $t$ increases
- The second largest eigenvalue $\lambda_2$ most significantly affects the mixing time.

![bg right:35% width:100%](https://skojaku.github.io/adv-net-sci/_images/diagonalizable-sum.jpg)

---

## Bound for the Mixing Time

- The mixing time $t_{\text{mix}}$ is bounded by

$$
t_{\text{mix}} < \tau \log \left( \frac{1}{\epsilon \min_{i} \pi_i} \right)
$$

- $\tau = \frac{1}{1-\lambda_2}$ (Relaxation time)

---

# Coding Exercise:

1. Using the Zachary's karate club network, construct the normalized adjacency matrix of a network ${\bf \overline A} = \mathbf{D}^{-\frac{1}{2}} \mathbf{A} \mathbf{D}^{-\frac{1}{2}}$, where $\mathbf{D}$ is the degree matrix, and $\mathbf{A}$ is the adjacency matrix.

2. Eigendecompose the normalized adjacency matrix using `np.linalg.eigh`.

3. Using the eigenvectors ${\bf Q}$ and the eigenvalues $\mathbf{\Lambda}$, compute the transition matrix ${\bf P} = {\bf Q} \mathbf{\Lambda} \mathbf{Q}^\top$.  Confirm the equality ${\bf P} = {\bf D}^{-1} {\bf A}$.

4. Compute the multi-step transition matrix ${\bf P}^t$ using the diagonalizable property of ${\bf P}$. Confirm that ${\bf P}^t$ is equivalent to the matrix power of ${\bf P}$.

5. Compute the stationary distribution using the eigenvector corresponding to the largest eigenvalue.

6. Compute the relaxation time $\tau$ using the second largest eigenvalue $\lambda_2$ by $\tau = \frac{1}{1-\lambda_2}$.

---

# Relationship between Random Walks, Modularity, and Centrality 🌟

https://skojaku.github.io/adv-net-sci/m07-random-walks/unifying-centrality-and-communities.html
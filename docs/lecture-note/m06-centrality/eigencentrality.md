# Centralities based on centralities

"A man is known by the company he keeps" is a quote from Aesop who lived in the ancient Greece, a further back in time from the Roman Empire.
It suggests that a person's character is reflected by the people this person is friends with.
This idea can be applied to define the *centrality* of a node in a network.

## Eigenvector centrality

One considers that a node is important if it is connected to other important nodes. Yes, it sounds like circular! But it is actually computable! Let us define it more precisely by the following equation.

$$
c_i = \lambda \sum_{j} A_{ij} c_j
$$

where $\lambda$ is a constant. It suggests that the centrality of a node ($c_i$) is the sum of the centralities of its neighbors ($A_{ij} c_j$; note that $A_{ij}=1$ if $j$ is a neighbor, and otherwise $A_{ij}=0$), normalized by $\lambda$.
Using vector notation, we can rewrite the equation as

$$
\begin{bmatrix}
c_1 \\
c_2 \\
\vdots \\
c_n
\end{bmatrix} = \lambda
\begin{bmatrix}
A_{11} & A_{12} & \cdots & A_{1n} \\
A_{21} & A_{22} & \cdots & A_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
A_{n1} & A_{n2} & \cdots & A_{nn}
\end{bmatrix}
\begin{bmatrix}
c_1 \\
c_2 \\
\vdots \\
c_n
\end{bmatrix}
$$

or equivalently,

$$
\mathbf{c} = \lambda \mathbf{A} \mathbf{c}
$$

Okay, but how do we solve this? Well, this is actually the eigenvector equation! And the solution to this equation is the eigenvector of the adjacency matrix, $\mathbf{A}$. But here's the tricky part - there are multiple eigenvectors. So which one should we choose?

Let's think about it for a moment. We want our centrality measure to be positive. It wouldn't make much sense to have negative importance! So, we're looking for an eigenvector where all the elements are positive. And a good news is that there's a special eigenvector that fits the bill perfectly.
Perron-Frobenius theorem guarantees that the eigenvector associted with the largest eigenvalue always has all positive elements.

This centrality is called **Eigenvector centrality**.


## Hyperlink-Induced Topic Search (HITS) centrality

Eigenvector centrality has several problems. One is that it does not handle directed networks very well.
A natural extension of eigenvector centrality to directed networks is the HITS centrality.
It introduces two notions of importance: *hub* and *authority*. A node is an important hub if it points to many important *authorities*. A node is an important authority if it is pointed by many important *hubs*.

Let's put on a math hat to concretely define the hub and authority centralities.
We introduce two vectors, $x_i$ and $y_i$, to denote the hub and authority centralities of node $i$, respectively. Following the idea of eigenvector centrality, we can define the hub and authority centralities as follows:

$$
x_i = \lambda_x \sum_j A_{ji} y_j, \quad y_i = \lambda_y \sum_j A_{ij} x_j
$$

Or equivalently,

$$
\mathbf{x} = \lambda_x \mathbf{A}^T \mathbf{y}, \quad \mathbf{y} = \lambda_y \mathbf{A} \mathbf{x}
$$

Substituting $\mathbf{y} = \lambda_y \mathbf{A} \mathbf{x}$ into the first equation and similar for $\mathbf{x}$, we get

$$
\mathbf{x} = \lambda_x \mathbf{A}^T \mathbf{A} \mathbf{x}, \quad \mathbf{y} = \lambda_y \mathbf{A} \mathbf{A}^T \mathbf{y}
$$

Again, we obtain the eigenvector equations whose solutions are the eigenvectors of $\mathbf{A}^T \mathbf{A}$ and $\mathbf{A} \mathbf{A}^T$ for $\mathbf{x}$ and $\mathbf{y}$, respectively.

::: {.callout-note title="Exercise"}
:class: tip

If the original network is *undirected*, is the HITS centrality equivalent to the eigenvector centrality? If so or not, explain why.

:::{dropdown} Click to see the answer
If the graph is undirected, the hub and authority centralities are equivalent. And the solution is given by the eigenvector of $\mathbf{A} \mathbf{A}^T$. Now, let us consider the eigenvector equation for the adjacency matrix $\mathbf{A}$.

$$
\mathbf{c} = \lambda \mathbf{A} \mathbf{c}
$$

By multiplying $\mathbb{A}$ on the both sides, we get

$$
\begin{aligned}
\mathbf{A} \mathbf{c} &= \lambda \mathbf{A} \mathbf{A} \mathbf{c} \\
\iff \mathbf{A}^\top \mathbf{A} \mathbf{c} &= \lambda \mathbf{A}^\top \mathbf{c} \\
\iff \mathbf{A}^\top \mathbf{A} \mathbf{c} &= \lambda^2 \mathbf{c}
\end{aligned}
$$

where we used the fact that $\mathbf{A}$ is symmetric. It suggests that the eigenvector of $\mathbf{A}^\top \mathbf{A}$ is the same as that of $\mathbf{A}$, and that the eigenvalue of $\mathbf{A}^\top \mathbf{A}$ is the square of that of $\mathbf{A}$.
Thus, the eigenvector centrality is equivalent to the HITS centrality if the network is undirected.

```

::: {.callout-note title="Exercise"}
:class: tip

Consider the case where the graph is undirected and we normalize the hub centrality by the degree $d_j$ of the authority, namely

$$
x_i = \sum_j \frac{A_{ji}}{d_j} y_j,\quad y_i = \sum_j A_{ij} x_j
$$


Then we will get the hub centrality equivalent to the degree centrality. Confirm this by substituting $x_i = d_i$.
:::

## Katz centrality

Eigenvector centrality tends to pay too much attention to a small number of nodes that are well connected to the network while under-emphasizing the importance of the rest of the nodes. A solution is to add a little bit of score to all nodes.

$$
c_i = \beta + \lambda \sum_{j} A_{ij} c_j
$$

::: {.callout-note title="Exercise"}
:class: tip

Derive the solution of the Katz centrality.

:::{dropdown} Click to see the answer

The equation can be solved by

$$
\mathbf{c} = \beta \mathbf{1} + \lambda \mathbf{A} \mathbf{c}
$$

where $\mathbf{1}$ is the vector of ones. By rewriting the equation, we get

$$
\left( \mathbf{I} - \lambda \mathbf{A} \right) \mathbf{c} = \beta \mathbf{1}
$$

By taking the inverse of $\mathbf{I} - \lambda \mathbf{A}$, we get

$$
\mathbf{c} = \beta \left( \mathbf{I} - \lambda \mathbf{A} \right)^{-1} \mathbf{1}
$$
```

## PageRank

You've probably heard PageRank, a celebrated idea behind Google Search. It is like a cousin of Katz centrality.

$$
c_i = (1-\beta) \sum_j A_{ji}\frac{c_j}{d^{\text{out}}_j} + \beta \cdot \frac{1}{N}
$$

where $d^{\text{out}}_j$ is the out-degree of node $j$ (the number of edges pointing out from node $j$).
The term $c_j/d^{\text{out}}_j$ represents that the score of node $j$ is divided by the number of nodes to which node $j$ points. In Web, this is like a web page distributes its score to the web pages it points to. It is based on an idea of traffic, where the viewers of a web page are evenly transferred to the linked web pages. A web page is important if it has a high traffic of viewers.


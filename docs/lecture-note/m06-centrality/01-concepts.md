# Module 6: Centrality Concepts

## What to learn in this module

In this module, we will learn centrality, one of the most widely-used yet controversial techniques in network analysis. We will learn:
- What is centrality in networks?
- How to operationalize centrality?
- How to find centrality in networks?
- Limitations of centrality
- **Keywords**: degree centrality, closeness centrality, betweenness centrality, eigenvector centrality, PageRank, Katz centrality, HITS, random walk

## What is centrality?

Have you ever wondered who the most popular person in your school is? Or which idea is the most important in a subject? Or maybe which movie everyone's talking about right now?
These questions are all about finding out what's important in a network of people, ideas, or things. In network science, we call this *centrality.*

Centrality or *importance* is a question of how important a node is in a network.
But the notion of *importance* is somewhat vague.
In what sense we say a node is important?
Answering this question needs a specific *context*, and there are many contexts in which the *importance* is defined.

![](../figs/centrality.jpg)

## Degree-based centrality

The simplest approach to measuring centrality is to count the connections of each node. This gives us *degree centrality*, which considers a node important if it has many direct connections.

**Degree centrality** is just the count of the number of edges connected to a node (i.e., the number of neighbors, or *degree* in network science terminology). The most important node is thus the one with the highest degree.

$$
c_i = d_i = \sum_{j} A_{ij}
$$

where $A_{ij}$ is the adjacency matrix of the network, and $d_i$ is the degree of node $i$.

## Distance-based centrality

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Milliarium_Aureum_op_het_Forum_Romanum_te_Rome_Columna_Miliaria_in_Foro_Romano_%28titel_op_object%29_Antieke_monumenten_%28serietitel%29_Antiquae_Urbis_Splendor_%28serietitel%29%2C_RP-P-2016-345-28-1.jpg/1546px-thumbnail.jpg?20191217151048" alt="Roma Foro Romano Miliarium Aureum" width="80%" style="display: block; margin-left: auto; margin-right: auto;">

Let's talk about an ancient Roman monument called the *Milliarium Aureum*, also known as the *Golden Milestone*.
It was the starting point for measuring distances on all major roads in the Roman Empire.
Emperor Augustus built it when Rome changed from a republic to an empire.
The monument not only marked the distances but also represent a centralization of power, where Rome transitioned from a Republic to an Empire.
Perhaps the Romans understood the importance of being central in terms of distance, and this concept can be applied to define *centrality* in networks.

This family of centrality measures is based on shortest path distances between nodes. They consider a node important if it has short distances to other nodes or if it lies on many shortest paths.

**Closeness centrality** measures how close a node is to all other nodes in the network. A node is central if it is close to all other nodes, which is operationally defined as

$$
c_i = \frac{N - 1}{\sum_{j = 1}^N \text{shortest path length from } j \text{ to } i}
$$

where $N$ is the number of nodes in the network. The numerator, $N - 1$, is the normalization factor to make the centrality have a maximum value of 1.

::: {.callout-note title="Exercise"}
:class: tip

Create a graph where a node has the maximum closeness centrality of value 1.

::: {.callout collapse="true"}
## Click to see the answer

The simplest example is a star graph, where one node is connected to all other nodes. The node at the center has the highest closeness centrality.

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Star_network_7.svg/1920px-Star_network_7.svg.png" alt="Star graph S7" width="50%" style="display: block; margin-left: auto; margin-right: auto;">
:::

**Harmonic centrality** adjusts closeness centrality to work even in disconnected networks. The problem with closeness centrality is that it cannot handle disconnected networks. When a network is disconnected, some nodes can't reach others, making their distance infinite. This causes all centrality values to become zero, which isn't very helpful! To fix this, Beauchamp {footcite:p}`beauchamp1965improved` came up with a clever solution called *harmonic centrality*. It works even when the network is disconnected.

$$
c_i = \sum_{j\neq i} \frac{1}{\text{shortest path length from } j \text{ to } i}
$$

**Eccentricity centrality** is based on the farthest distance from a node to any other node. The eccentricity centrality is defined as

$$
c_i = \frac{1}{\max_{j} \text{shortest path length from } i \text{ to } j}
$$

**Betweenness centrality** considers that a node is important if it lies on many shortest paths between other nodes.

$$
c_i = \sum_{j < k} \frac{\sigma_{jk}(i)}{\sigma_{jk}}
$$

where $\sigma_{jk}$ is the number of shortest paths between nodes $j$ and $k$, and $\sigma_{jk}(i)$ is the number of shortest paths between nodes $j$ and $k$ that pass through node $i$.

## Walk-based centrality

"A man is known by the company he keeps" is a quote from Aesop who lived in the ancient Greece, a further back in time from the Roman Empire.
It suggests that a person's character is reflected by the people this person is friends with.
This idea can be applied to define the *centrality* of a node in a network.

This family of centrality measures considers that a node is important if it is connected to other important nodes, or if it receives many "walks" or "votes" from other nodes in the network. These measures often use recursive definitions and are computed using linear algebra techniques.

**Eigenvector centrality** considers that a node is important if it is connected to other important nodes. Yes, it sounds like circular! But it is actually computable! Let us define it more precisely by the following equation.

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
Perron-Frobenius theorem guarantees that the eigenvector associated with the largest eigenvalue always has all positive elements.

**Hyperlink-Induced Topic Search (HITS) centrality**

extends eigenvector centrality to directed networks. It introduces two notions of importance: *hub* and *authority*. A node is an important hub if it points to many important *authorities*. A node is an important authority if it is pointed by many important *hubs*.

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

::: {.callout-note collapse="true" title="Click to see the answer"}
If the graph is undirected, the hub and authority centralities are equivalent. And the solution is given by the eigenvector of $\mathbf{A} \mathbf{A}^T$. Now, let us consider the eigenvector equation for the adjacency matrix $\mathbf{A}$.

$$
\mathbf{c} = \lambda \mathbf{A} \mathbf{c}
$$

By multiplying $\mathbf{A}$ on the both sides, we get

$$
\begin{aligned}
\mathbf{A} \mathbf{c} &= \lambda \mathbf{A} \mathbf{A} \mathbf{c} \\
\iff \mathbf{A}^\top \mathbf{A} \mathbf{c} &= \lambda \mathbf{A}^\top \mathbf{c} \\
\iff \mathbf{A}^\top \mathbf{A} \mathbf{c} &= \lambda^2 \mathbf{c}
\end{aligned}
$$

where we used the fact that $\mathbf{A}$ is symmetric. It suggests that the eigenvector of $\mathbf{A}^\top \mathbf{A}$ is the same as that of $\mathbf{A}$, and that the eigenvalue of $\mathbf{A}^\top \mathbf{A}$ is the square of that of $\mathbf{A}$.
Thus, the eigenvector centrality is equivalent to the HITS centrality if the network is undirected.
:::

::: {.callout-note title="Exercise"}
:class: tip

Consider the case where the graph is undirected and we normalize the hub centrality by the degree $d_j$ of the authority, namely

$$
x_i = \sum_j \frac{A_{ji}}{d_j} y_j,\quad y_i = \sum_j A_{ij} x_j
$$

Then we will get the hub centrality equivalent to the degree centrality. Confirm this by substituting $x_i = d_i$.
:::

**Katz centrality** addresses a limitation of eigenvector centrality, which tends to pay too much attention to a small number of nodes that are well connected to the network while under-emphasizing the importance of the rest of the nodes. The solution is to add a little bit of score to all nodes.

$$
c_i = \beta + \lambda \sum_{j} A_{ij} c_j
$$

::: {.callout-note title="Exercise"}
:class: tip

Derive the solution of the Katz centrality.

::: {.callout collapse="true"}
## Click to see the answer

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
:::

**PageRank** is the celebrated idea behind Google Search and can be seen as a cousin of Katz centrality.

$$
c_i = (1-\beta) \sum_j A_{ji}\frac{c_j}{d^{\text{out}}_j} + \beta \cdot \frac{1}{N}
$$

where $d^{\text{out}}_j$ is the out-degree of node $j$ (the number of edges pointing out from node $j$).
The term $c_j/d^{\text{out}}_j$ represents that the score of node $j$ is divided by the number of nodes to which node $j$ points. In the Web, this is like a web page distributes its score to the web pages it points to. It is based on an idea of traffic, where the viewers of a web page are evenly transferred to the linked web pages. A web page is important if it has a high traffic of viewers.

## Pen and paper exercises

- [School exercises](./pen-and-paper/exercise.pdf)
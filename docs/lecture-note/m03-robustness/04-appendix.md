# Appendix

## Derivation of the Molloy-Reed criterion

Molloy and Reed derived the following criterion for an existence of a giant component in a network with an arbitrary degree distribution {footcite}`molloy1995critical`.
It is based on a simple heuristic argument: the network has a giant component when a random node $i$ with neighbor $j$ has, on average, is connected to at least one other node. We write the condition as

$$
\langle k_i \vert i \leftrightarrow j \rangle = \sum_{k} k P(k \vert i \leftrightarrow j) > 2
$$

where $\langle k_i \vert i \leftrightarrow j \rangle$ is the conditional average degree of node $i$ given that it is connected to node $j$. From Bayes' theorem, we have

$$
P(k_i \vert i \leftrightarrow j) = \frac{P(i \leftrightarrow j \vert k_i) P(k_i)}{P(i \leftrightarrow j)}
$$

Assuming that the network is uncorrelated and sparse (meaning, we neglect loops), then $P(i \leftrightarrow j \vert k_i) = k_i / (N-1)$ and $P(i \leftrightarrow j) = \langle k \rangle / (N-1)$. Substituting these into the above equation, we get

$$
P(k_i \vert i \leftrightarrow j) = \frac{k_i P(k_i)}{\langle k \rangle}
$$

Thus, the condition for the existence of a giant component is

$$
\frac{1}{\langle k \rangle} \sum_{k_i} k_i^2 P(k_i) = \frac{\langle k^2 \rangle}{\langle k \rangle} > 2
$$


## Derivation of the percolation threshold for a random attack.

Assume a fraction $p$ of nodes are removed independently from the network. The removal of nodes reduces the connectivity of the network and the degree of the remaining nodes.
The probability that a node with initial degree $k_0$ reduces its degree to $k$ follows
a binomial distribution,

$$
P(k \vert k_0, p) = \binom{k_0}{k} (1-p)^k p^{k_0-k}
$$

Considering all nodes, the new degree distribution is given by

$$
P'(k) = \sum_{k_0 = k}^{\infty} P(k_0) \binom{k_0}{k} (1-p)^k p^{k_0-k}
$$

To connect with the Molloy-Reed criterion, we need to compute the first and second moments, denoted by $\langle k \rangle'$ and $\langle k^2 \rangle'$, of the new degree distribution.

$$
\begin{align}
\langle k \rangle' &= \sum_{k} k P'(k_0) \\
&= \sum_{k} \sum_{k_0=k}^{\infty} k \binom{k_0}{k} (1-p)^k p^{k_0-k} P(k_0) \\
&= \sum_{k_0=0}^\infty P(k_0) \underbrace{\sum_{k} k \binom{k_0}{k} (1-p)^k p^{k_0-k}}_{\text{Expected value of $k$ for a binomial distribution}} \\
&= \sum_{k_0=0}^\infty P(k_0) k_0 (1-p) \\
&= \langle k_0 \rangle (1-p)
\end{align}
$$

Similarly, we can compute the second moment, which is given by

$$
\langle k^2 \rangle' = \langle k_0^2 \rangle (1-p)^2 + \langle k_0 \rangle p (1-p)
$$

By substituting these into the Molloy-Reed criterion, we get

$$
\frac{\langle k^2 \rangle'}{\langle k \rangle'}  = \frac{\langle k_0^2 \rangle (1-p)^2 + \langle k_0 \rangle p (1-p)}{\langle k_0 \rangle (1-p)} = \frac{\langle k_0^2 \rangle (1-p) + \langle k_0 \rangle p}{\langle k_0 \rangle} > 2
$$

By solving the inequality for $p$, we get the percolation threshold for a random attack,

$$
1-p < \frac{1}{\langle k_0 ^2 \rangle / \langle k_0 \rangle - 1}
$$

which is the condition for the existence of a giant component.

## Lecture Notes: Network Resilience & Attacks (Part 1) - Random Failure

### 1. Core Question: Network Robustness

How much damage can a network sustain before it breaks? How does the structure of a network (e.g., a road grid vs. a social network) affect its resilience to attack?

**Attack**: Any process that removes nodes or links from a network, threatening its structural integrity and connectivity.

**Random Failure**: A type of attack where nodes or links are removed randomly and uniformly, without regard to their properties (e.g., fallen trees in a storm, random vaccination).

### 2. Recap: Generating Functions

We use generating functions to analyze the properties of networks with a given degree distribution $p_k$ (the probability that a randomly chosen node has degree $k$).

**Degree Generating Function $G(x)$:**

$$G(x) = \sum_{k=0}^{\infty} p_k x^k$$

**Excess Degree Generating Function $Q(x)$:**

$$Q(x) = \sum_{k=0}^{\infty} q_k x^k = \frac{G'(x)}{G'(1)}$$

(Describes the distribution of the remaining degrees of a node reached by following a random link).

**Mean Degree ($z$) and Mean Excess Degree ($q$):**

$$z = G'(1)$$

$$q = Q'(1)$$

### 3. Modeling Random Link Removal (Link Percolation)

This models scenarios where connections fail randomly (e.g., blocked roads, dropped calls).

#### A. Derivation:

**Define the Attack**: Let each link in the network have a probability $c$ of surviving and a probability $r$ of being removed, where $c + r = 1$.

**The "Attack" or "Pruning" Generating Function, $A(x)$**: We can model this removal process with its own generating function. A single link can either become 0 links (with probability $r$) or remain 1 link (with probability $c$).

$$A(x) = r \cdot x^0 + c \cdot x^1 = r + cx$$

**Composition Rule ("Dice-of-Dice")**: To find the new state of the network, we compose the functions. The new degree of a node is the result of its original degree (a random process described by $G(x)$) where each of its links is subjected to the removal process (described by $A(x)$).

**New Degree Generating Function ($G_a$):**

$$G_a(x) = G(A(x))$$

**New Excess Degree Generating Function ($Q_a$):**

$$Q_a(x) = Q(A(x))$$

**Mean Excess Degree After Attack ($q_a$)**: We can find the new critical threshold by calculating the new mean excess degree.

$$q_a = Q_a'(1)$$

Using the chain rule: $Q_a'(x) = Q'(A(x)) \cdot A'(x)$

Evaluate at $x=1$: $q_a = Q'(A(1)) \cdot A'(1)$

We know:
- $A(1) = r + c(1) = 1$
- $A'(x) = c \Rightarrow A'(1) = c$

Substituting these back gives:

$$q_a = Q'(1) \cdot c$$

**Key Finding 1**: The mean excess degree after random link removal is simply the original mean excess degree multiplied by the probability of a link surviving.

$$q_a = q \cdot c$$

#### B. Application: The Road Network Example

**Model**: A 4-regular grid (all intersections have 4 roads). So, $z = 4$ and $q = 3$.

**Attack**: 20% of roads are blocked, so $r = 0.2$ and $c = 0.8$.

**Result**: $q_a = q \times c = 3 \times 0.8 = 2.4$.

**Conclusion**: Since $q_a = 2.4 > 1$, a giant connected component of roads still exists. The network is largely intact.

### 4. Modeling Random Node Removal (Node Percolation)

This models scenarios where individuals are removed (e.g., vaccination, quarantine).

#### A. The Two-Step Process:

1. **Node Removal**: A fraction $r$ of nodes is randomly removed. The degree distribution of the remaining $cN$ nodes is unchanged.

2. **Stub Removal**: The links that used to connect to the removed nodes are now dangling "stubs". These stubs must also be removed. Since the nodes were removed randomly, this is equivalent to randomly removing the endpoints of links.

#### B. Key Finding 2: 
The process of removing stubs from random node removal is mathematically identical to random link removal, where the probability of a link being removed is $r$ (the probability its neighbor was removed).

#### C. Comparison of Random Attacks:
The table below summarizes the effect of removing a proportion $r$ of links or nodes, where $c = 1 - r$.

| Property | Before Attack | Random Node Removal | Random Link Removal |
|----------|---------------|---------------------|---------------------|
| Total Nodes (N) | N | cN | N |
| Mean Degree (z) | z | cz | cz |
| Mean Excess Degree (q) | q | cq | cq |
| Degree Gen. Func. | G(x) | G(A(x)) | G(A(x)) |
| Excess Degree Gen. Func. | Q(x) | Q(A(x)) | Q(A(x)) |

The mathematical effect on connectivity metrics ($q$, $G(x)$, $Q(x)$) is identical. The only difference is the total number of surviving nodes.

### 5. Resilience of Different Network Structures

The impact of an attack depends heavily on the network's structure, particularly its heterogeneity.

**Homogeneous Networks (e.g., 3-regular graph):**
- Low mean excess degree ($q=2$ for $z=3$).
- **Hard but Brittle**: Very robust against a small number of random failures. The giant component size $s$ barely decreases.
- Experiences a sharp percolation transition. Once a critical proportion of nodes/links is removed, the network rapidly disintegrates.

**Heterogeneous Networks (e.g., scale-free):**
- High mean excess degree (e.g., $q=6$ for $z=3$).
- **Soft but Resilient**: The giant component size begins to decrease immediately with any attack.
- Does not have a sharp transition point. It is extremely difficult to destroy the giant component entirely through random failure, as the highly connected hubs maintain connectivity.

### 6. Conclusion & Outlook

- Generating functions provide a powerful and elegant framework for calculating the effect of random attacks on network integrity.
- The resilience of a network is not just about its average connectivity ($z$) but crucially about its structure, captured by the mean excess degree ($q$).
- Heterogeneous networks are surprisingly robust to random failures, while homogeneous networks are brittle.
- **Next Steps**: What happens if the attack is not random? The next lecture will explore targeted attacks, which focus on removing the most important nodes first.

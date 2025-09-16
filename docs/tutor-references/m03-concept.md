## Power Grid Design Challenge

In the aftermath of World War I, the newly formed Czechoslovakia faced massive reconstruction challenges. Cities and towns across [Moravia](https://en.wikipedia.org/wiki/Moravia) needed electricity, but the young nation had limited resources. Every resources spent on unnecessary infrastructure was a resource not available for hospitals, schools, or economic recovery. Engineers at the West Moravian Power Company faced a critical question: How do you connect every town and village to the electrical grid while using the minimum length of cable?

The problem reached mathematician Otakar Borůvka through his friend at the power company. Borůvka's 1926 solution gave us the first systematic approach to what we now call **the minimum spanning tree problem**: finding the cheapest way to connect all locations in a network.

#### Minimum Spanning Tree

A **minimum spanning tree (MST)** of a weighted network is a tree that:

- **Spans** all nodes (connects every location in the network)
- Is a **tree** (connected with no cycles - no redundant loops)
- Has **minimum total weight** among all possible spanning trees

Otakar Borůvka delivered the first algorithm to solve this problem: **Borůvka's algorithm**. But it is not the only algorithm to find the minimum spanning tree.
In fact, there are several algorithms. We will cover two algorithms: **Kruskal's algorithm** and **Prim's algorithm**, which are easier to understand and implement.

#### Kruskal's Algorithm

**Kruskal's algorithm** embodies a remarkably simple yet powerful intuition: always choose the cheapest available option, but never create wasteful loops. While sounds heuristic, this algorithm in fact leads to the global optimial solution!

The algorithm works by first sorting every possible connection from cheapest to most expensive like arranging all the cable segments by cost. Then, it examines each connection in order, asking a crucial question: "If I add this cable, will it create a redundant loop?" If the answer is no, the cable joins the growing network. If adding it would create a cycle---meaning the two locations are already connected through some other path---the algorithm skips it as wasteful. This process continues until every location is connected, guaranteeing both minimum cost and complete coverage.

#### Prim's Algorithm

**Prim's algorithm** takes a fundamentally different approach, embodying the intuition of organic growth from a single starting point. Picture an engineer beginning at the central power plant and asking: "What's the cheapest way to connect one more location to our existing grid?" This local growth strategy builds the network incrementally, always expanding from what's already been constructed.

The algorithm begins by selecting any location as its starting point, often the power plant in our analogy. From this initial seed, it repeatedly identifies the cheapest connection that would bring a new, unconnected location into the growing network. Unlike Kruskal's global view, Prim's algorithm maintains a clear distinction between locations already in the network and those still waiting to be connected. At each step, it finds the minimum-cost bridge between these two groups, gradually expanding the connected region until it encompasses every location.

Two algorithms find the same minimum spanning tree when all connection costs are different. If there are connections with the same cost, there are multiple minimum spanning trees of the same cost, and which tree to find depends on the algorithm. In particular, Prim's algorithm finds different trees when starting from different locations.

### Measuring Network Damage

While there can be many metrics to quantify network damage, we will focus on a purely topological metric: the fraction of nodes remaining in the largest connected component after removal.

$$
\text{Connectivity} = \frac{\text{Size of largest component after removal}}{\text{Original network size}}
$$

The **robustness profile** plots connectivity against the fraction of nodes removed, revealing how networks fragment. Crucially, the shape of this profile depends entirely on the **order** in which nodes are removed - random removal creates one pattern, while strategic targeting creates dramatically different patterns.

To compare networks with a single metric, we use the **R-index** - the area under this curve:

$$
R = \frac{1}{N} \sum_{k=1}^{N-1} y_k
$$

The robustness index is a measure of how robust a network is to under a sequential failure of nodes. The higher the R-index, the more robust the network is.

Networks can exhibit different robustness profiles under different attack strategies. One form of an attack is a **random failure**, where nodes are removed randomly. Another form of an attack is a **targeted attack**, where nodes are removed strategically.

Random failures are like earthquakes or equipment malfunctions; they strike unpredictably. In power grids, generators might fail due to technical problems. In computer networks, servers might crash randomly.

Even if a network survives random failures beautifully, it might crumble under **targeted attacks**. Adversaries strategically choose which nodes to attack for maximum damage. The most intuitive strategy targets **high-degree nodes** (hubs) first, i.e., like targeting the busiest airports to disrupt air travel.

## Theoretical Framework for Network Robustness

To understand these patterns mathematically, we can view network attacks as the **reverse process of percolation**. **Percolation theory** studies phase transitions in connectivity by asking: as we randomly add nodes to a grid, when does a giant connected component emerge? Network robustness asks the opposite: as we remove nodes, when does the giant component disappear?

::: {.column-margin}
**Percolation vs. Robustness: Two Sides of the Same Coin**

Percolation theory asks: *"Starting from isolation, how many nodes must we connect to form a giant component?"* - increasing connectivity from $p = 0$ to $p = 1$.

Robustness analysis asks: *"Starting from full connectivity, how many nodes must we remove to fragment the network?"* - decreasing connectivity from $p = 1$ to $p = 0$.

These are mathematically equivalent processes, just viewed in opposite directions along the same connectivity parameter.
:::

### The Molloy-Reed Criterion

For networks with arbitrary degree distributions, the **Molloy-Reed criterion** determines whether a **giant component** exists - that is, whether the network contains a single large connected component that includes most of the nodes:

$$
\kappa = \frac{\langle k^2 \rangle}{\langle k \rangle} > 2
$$

where $\langle k \rangle$ is the average degree and $\langle k^2 \rangle$ is the average of squared degrees. The ratio $\kappa$ measures **degree heterogeneity** - networks with hubs have high $\kappa$, while degree homogeneous networks have low $\kappa$. When $\kappa > 2$, a giant component forms that dominates the network connectivity. See the Appendix for the proof of the Molloy-Reed criterion.

Derivation: 
Suppose $p(k)$ is the fraction of nodes with $k$ hands. Altogether, nodes with $k$ hands contribute $k p(k)$ hands to the network.

If I randomly pick a hand, I would handshake with a node with $k$ hands with probability proportional to $k p(k)$. That is

$$
q(k) = \frac{k p(k)}{\sum_{k=1}^{\infty} k p(k)} = \frac{k}{\langle k \rangle } p(k),
$$

where $\langle k \rangle = \sum_{k=1}^{\infty} k p(k)$ is the average degree. Now, the average number of hands that my friends would have on average is

$$
\langle k \rangle_{q(k)} = \sum_{k=1}^{\infty} k q(k) = \sum_{k=1}^{\infty} k^2 / \langle k \rangle p(k) = \frac{\langle k^2 \rangle}{\langle k \rangle}.
$$

The Molloy-Reed criterion is a powerful tool to predict the existence of a giant component in a network and allows us to find the critical fraction of nodes that must be **removed** to break the network. This critial fraction depends on the strategy of the attack, along with the degree distribution. For simplicity, let us restrict ourselves into the random failures. For the random failure case, the critical fraction is given by:

$$
f_c = 1 - \frac{1}{\kappa - 1}
$$

The value of $\kappa$ depends on the degree distribution, and below, we showcase two examples of degree distributions.

Derivation: 
- After removing fraction $f$, my friend who initially has---$\kappa$ friends on average---have $(1-f)(\kappa -1)$ friends on average.
- It's $\kappa-1$ not $\kappa$ because one of the friends is me.
- Thus, the network breaks when $(1-f)(\kappa - 1) = 1$
- Solving for $f$, we get $$f_c = 1 - \frac{1}{\kappa - 1}$$

#### Degree homogeneous network

In case of a degree homogeneous network like a random network considered in the exercise above, the critical fraction is given by:

$$
f_c = 1 - \frac{1}{\langle k \rangle}
$$

given that $\langle k^2 \rangle = \langle k \rangle^2$ and thus $\kappa = \langle k \rangle$. This suggests that the threshold is determined by the average degree $\langle k \rangle$. A large $\langle k \rangle$ results in a larger $f_c$, meaning that the network is more robust against random failures.

Derivation: 
For a Poisson distribution with mean $\lambda$:

- The first moment (mean degree) is $\langle k \rangle = \lambda$
- The second moment is $\langle k^2 \rangle = \lambda^2 + \lambda$

Now, we can calculate $\kappa$:

$$
\kappa = \frac{\langle k^2 \rangle}{\langle k \rangle} = \frac{\lambda^2 + \lambda}{\lambda} = \lambda + 1
$$

Finally, we can find the critical fraction $f_c$:
$$
f_c = 1 - \frac{1}{\kappa - 1} = 1 - \frac{1}{(\lambda + 1) - 1} = 1 - \frac{1}{\lambda} 
$$


#### Degree heterogeneous network

Most real-world networks are degree heterogeneous, i.e., the degree distribution $P(k) \sim k^{-\gamma}$ follows a power law (called *scale-free* network).
The power-law degree distribution has infinite second moment, i.e., $\langle k^2 \rangle = \infty$ and thus $f_c = 1.0$, which means that all nodes must be removed to break the network into disconnected components.
This is the case where the number of nodes is infinite (i.e., so that a node has a very large degree for the degree distribution to be a valid power law). When restricting the maximum degree to be finite, the critical fraction is given by:

$$
f_c =
\begin{cases}
1 - \dfrac{1}{\frac{\gamma-2}{3-\gamma} k_{\text{min}} ^{\gamma-2} k_{\text{max}}^{3-\gamma} -1} & \text{if } 2 < \gamma < 3 \\
1 - \dfrac{1}{\frac{\gamma-2}{\gamma-3} k_{\text{min}} - 1} & \text{if } \gamma > 3 \\
\end{cases}
$$

where $k_{\text{min}}$ and $k_{\text{max}}$ are the minimum and maximum degree, respectively.
The variable $\gamma$ is the exponent of the power law degree distribution, controlling the degree heterogeneity, where a lower $\gamma$ results in a more degree heterogeneous network.

- For regime $2 < \gamma < 3$, the critical threshold $f_c$ is determined by the extreme values of the degree distribution, $k_{\text{min}}$ and $k_{\text{max}}$.
And $f_c \rightarrow 1$ when the maximum degree $k_{\text{max}} \in [k_{\text{min}}, N-1]$ increases.
Notably, in this regime, the maximum degree $k_{\text{max}}$ increases as the network size $N$ increases, and this makes $f_c \rightarrow 1$.

- For regime $\gamma > 3$, the critical threshold $f_c$ is influenced by the minimum degree $k_{\text{min}}$. In contrast to $k_{\text{max}}$, $k_{\text{min}}$ remains constant as the network size $N$ grows. Consequently, the network disintegrates when a finite fraction of its nodes are removed.

### Robustness Under Attack

While scale-free networks show remarkable robustness against random failures, they exhibit a fundamental vulnerability to targeted attacks that deliberately target high-degree nodes (hubs). 

Rather than removing nodes randomly, an adversary with knowledge of the network structure can systematically remove the highest-degree nodes first, followed by the next highest-degree nodes, and so on. Under this targeted hub removal strategy, scale-free networks fragment rapidly and dramatically. The critical threshold for attacks, $f_c^{\text{attack}}$, is dramatically lower than for random failures. While random failures require $f_c^{\text{random}} \approx 1$ (nearly all nodes must be removed), targeted attacks need only $f_c^{\text{attack}} \ll 1$ (a small fraction of hubs) to fragment the network.

To understand how networks fragment under targeted attacks, we must consider two key effects that occur when the highest-degree nodes are systematically removed. First, the removal of hub nodes changes the maximum degree of the remaining network from $k_{\max}$ to a new lower value $k'_{\max}$. Second, since these removed hubs had many connections, their elimination also removes many links from the network, effectively changing the degree distribution of the surviving nodes.

The mathematical analysis of this process relies on mapping the attack problem back to the random failure framework through careful accounting of these structural changes. When we remove an $f$ fraction of the highest-degree nodes in a scale-free network, the new maximum degree becomes $k'_{\max} = k_{\min} f^{1/(1-\gamma)}$, where the power-law exponent $\gamma$ determines how rapidly the degree sequence declines.

For scale-free networks with degree exponent $\gamma$, the critical attack threshold $f_c$ satisfies:

$$
f_c^{\frac{2-\gamma}{1-\gamma}} = \frac{2 + 2^{-\gamma}}{3-\gamma} k_{\min} \left(f_c^{\frac{3-\gamma}{1-\gamma}} - 1\right)
$$

The fractional exponents $(2-\gamma)/(1-\gamma)$ and $(3-\gamma)/(1-\gamma)$ arise from the power-law degree distribution and determine how quickly the network fragments as hubs are removed. For networks with $\gamma < 3$ (highly heterogeneous degree distributions), these exponents are negative, leading to extremely small values of $f_c$, i.e., meaning just a tiny fraction of hub removal can destroy network connectivity.

How do we design networks that resist both random failures and targeted attacks? Key principles include:

1. **Balanced Degree Distribution**: Avoid both extreme homogeneity and extreme hub concentration
2. **Multiple Redundant Pathways**: Ensure removing any single node doesn't isolate large portions
3. **Strategic Hub Protection**: In hub-based networks, invest heavily in protecting critical nodes
4. **Hierarchical Design**: Combine local clusters with hub connections and redundant backbones
5. **Adaptive Responses**: Design systems that can reconfigure when attacks are detected

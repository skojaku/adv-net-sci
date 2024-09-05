---
marp: true
theme: default
paginate: true
---

Check list
- [ ] Microphone turned on
- [ ] Zoom room open
- [ ] Recording on
- [ ] Mouse cursor visible
- [ ] Sound Volume on


---

# Advanced Topics in Network Science

Lecture 03: Network Robustness
Sadamori Kojaku

---

![bg right:100% width:70%](../enginet-intro-slide/enginet-01.png)

---

![bg right:100% width:70%](../enginet-intro-slide/enginet-02.png)

---

![bg right:100% width:70%](../enginet-intro-slide/enginet-03.png)

---

![bg right:100% width:70%](../enginet-intro-slide/enginet-04v2.png)



# Module 3: Network Robustness 🛡️

- 📚 Learning objectives:
  - Minimum spanning tree (MST) 🌳
  - Network robustness against attacks 💥
  - Random vs. targeted attacks 🎯
  - Robustness metrics: Connectivity and R-index 📊

---

# Power Grid Exercise ⚡

- 📝 Pen and paper task: Design a cost-effective power grid
- Considerations:
  - Minimize total cable length 📏
  - Ensure all stations are connected 🔌
  - Balance cost and reliability 💰

---

# Minimum Spanning Tree (MST) 🌲

- Tree connecting all nodes with minimum total edge weight
- **Tree**: Connected network without cycles.  **Spanning**: Includes all nodes

<div style="text-align: center;">
    <img src="https://github.com/skojaku/adv-net-sci/raw/gh-pages/_images/minimum-spanning-tree.jpg" width="80%">
</div>

---

# MST Algorithms 🧮

1. Kruskal's Algorithm:
   - Sort edges by weight
   - Add smallest edge that doesn't create a cycle
   - Repeat until all nodes connected

2. Prim's Algorithm:
   - Start with a single node
   - Add smallest edge connecting to unconnected node
   - Repeat until all nodes connected

- [🚀 Try the interactive demo](https://skojaku.github.io/adv-net-sci/vis/kruskal-vs-prime.html)

---

# Network Robustness

- Network's ability to maintain connectivity after failures
- Types of failures/attacks:
  - **Random failures** 🎲
  - **Targeted attacks** 🎯
- Measure: Fraction of nodes in the largest connected component

![bg right:50% width:87%](https://skojaku.github.io/adv-net-sci/_images/single-node-failure.jpg)

---

# Robustness Profile 📈

- Plot of connectivity vs. fraction of nodes removed
- Interpretation:
  - Closer to diagonal line = more robust
- Metric:
  - R-index (higher is better)
  - $R = \frac{1}{N} \sum_{k=1}^{N-1} y_k$
  - $y_k$: connectivity when $k$ nodes are removed


![bg right:50% width:100%](https://skojaku.github.io/adv-net-sci/_images/robustness-profile.jpg)

---

# Hands-on: Zachary's Karate Club 🥋

- [🚀 Hands-on: Zachary's Karate Club](https://github.com/skojaku/adv-net-sci/blob/main/notebooks/exercise-m03-robustness.ipynb)



---

# Random Failure Simulation 🎲

```python
g = g_original.copy()
n_nodes = g.vcount()

for i in range(n_nodes - 1):
    node_idx = np.random.choice(g.vs.indices)
    g.delete_vertices(node_idx)

    components = g.connected_components()
    connectivity = np.max(components.sizes()) / g_original.vcount()

    # Save results...
```

---

# Targeted Attack Simulation 🎯

```python
g = g_original.copy()
n_nodes = g.vcount()

for i in range(n_nodes - 1):
    node_idx = g.vs.indices[np.argmax(g.degree())]
    g.delete_vertices(node_idx)

    components = g.connected_components()
    connectivity = np.max(components.sizes()) / g_original.vcount()

    # Save results...
```

---

# Robustness Results 📊

- Plot robustness profiles for both attack types
- Compare R-$index values:
- Interpret results: Network more vulnerable to targeted attacks


```python
rindex = df_robustness_profile["connectivity"].mean()
rindex_targeted = df_robustness_profile_targeted["connectivity"].mean()
```

---

# Game

[🚀 Network Robustness Game](https://skojaku.github.io/adv-net-sci/vis/network-robustness.html)

---

# Theoretical Basis of Network Robustness

---

# Percolation Theory

- A mathematical framework to describe the behavior of connected clusters in a graph.
- Lattice: Regular grid of points
- A puddle appears with probability $p$ at each point
- Cluster: A group of connected puddles
- How does the size of the largest cluster grow as $p$ increases 🤔?

![bg right:50% width:100%](https://jamesmccaffrey.wordpress.com/wp-content/uploads/2021/07/percolation.jpg)

---

# Numerical percolation experiments

- Cluster size increases as $p$ increases
- Not gradual, but sudden
- At a critical point $p_c\simeq 0.598$, the largest cluster goes from small to huge

![bg right:50% width:100%](https://skojaku.github.io/adv-net-sci/_images/6c27325c48214dca671f17b6a1f27814647f9f08d86af7502457c53e060adbff.png)


---


# How does this relate to failures?

- Percolation: Each node has a puddle with probability $p$
- Failures: Each node is removed with probability $1-p$

![bg right:50% width:100%](https://skojaku.github.io/adv-net-sci/_images/6c27325c48214dca671f17b6a1f27814647f9f08d86af7502457c53e060adbff.png)

---

# Condition for Giant Component Formation

**Molloy-Reed Criterion**: A network forms a giant component if:

$$
\kappa_0 := \frac{\langle k^2 \rangle}{\langle k \rangle} > 2
$$

- $k$: Node degree; $\langle k \rangle$: Average degree; $\langle k^2 \rangle$: Second moment of degree distribution


![right:50% width:100%](https://skojaku.github.io/adv-net-sci/_images/f28296706832972715a363f1a51a5bded3072589739f7b99e87362f1c384a6ee.png)

---

# Exercise

Consider a random network of $N$ nodes, where every pair of nodes are connected by an edge with a certain probability. Then, the degree $k$ of a node is a binomial random variable, which we approximate by a Poisson random variable with mean $\langle k \rangle$. The variance of the Poisson random variable is also $\langle k \rangle$.

1. Derive $\langle k^2 \rangle$ using $\langle k \rangle$.
  - Hint: Variance is defined as $\text{Var}(k) = \langle (k-\langle k \rangle)^2 \rangle$.
2. Compute the ratio $\frac{\langle k^2 \rangle}{\langle k \rangle}$.
3. Check when the network satisfies the Molloy-Reed criterion.


---

**Solution for Q1**:
To derive $\langle k^2 \rangle$, we start with the definition of variance

$$\text{Var}(k) = \langle (k - \langle k \rangle)^2 \rangle$$

Expanding the square, we get

$$\text{Var}(k) = \langle k^2 \rangle - 2\langle k \rangle \langle k \rangle + \langle k \rangle^2$$

Since $\text{Var}(k) = \langle k \rangle$ for a Poisson distribution, we can substitute and rearrange

$$\langle k \rangle = \langle k^2 \rangle - \langle k \rangle^2$$

Solving for $\langle k^2 \rangle$, we obtain

$$\langle k^2 \rangle = \langle k \rangle + \langle k \rangle^2$$

---

**Solution for Q2**:
$\frac{\langle k^2 \rangle}{\langle k \rangle} = 1 + \langle k \rangle$

**Solution for Q3**:
$\langle k \rangle >1$. In other words, if a node has on average more than one neighbor, the random network is likely to have a giant component.

---

# Critical Fraction

The critical fraction of nodes $f_c$ at which the giant component disappears:

$$
f_c = 1 - \frac{1}{\frac{\langle k^2 \rangle}{\langle k \rangle} - 1}
$$

**Degree homogeneous network**:

For a random network in the previous exercise, by substituting $\frac{\langle k^2 \rangle}{\langle k \rangle} = 1 + \langle k \rangle$:

$$
f_c = 1 - \frac{1}{\langle k \rangle}
$$

- $f_c$ is only determined by the average degree $\langle k \rangle$.
- A larger $\langle k \rangle$ results in a larger $f_c$, making the network more robust against random failures.

---

**Degree heterogeneous network**:

For a power-law degree distribution $P(k) \sim k^{-\gamma}$,

$$
f_c =
\begin{cases}
1 - \dfrac{1}{\frac{\gamma-2}{3-\gamma} k_{\text{min}} ^{\gamma-2} k_{\text{max}}^{3-\gamma} -1} & \text{if } 2 < \gamma < 3 & \text{ (Degree heterogeneous)} \\
1 - \dfrac{1}{\frac{\gamma-2}{3-\gamma} k_{\text{min}} - 1} & \text{if } \gamma > 3 & \text{ (Degree homogeneous)} \\
\end{cases}
$$

- $k_{\text{min}}$ and $k_{\text{max}}$: the minimum and maximum degrees.
- $\gamma$: the exponent of the power law degree distribution.
- The critical fraction is determined by $k_{\text{min}}$ and $k_{\text{max}}$.
- As the number of nodes increases, $k_{\text{max}}$ also increases. Thus, in large degree heterogeneous networks, $f_c$ approaches 1 as the network size grows 🤯.

---

# Attack tolerance

- We can use the same framework to analyze the tolerance to targeted attacks.
  - **Step 1**: Remove a node.
  - **Step 2**: Check the Molloy-Reed criterion.
  - **Step 3**: Find the fraction of nodes removed when the criterion is violated.
- Effective attack: Remove nodes that most reduce $\kappa_0$ (degree heterogeneity).


![bg right:40% width:100%](https://skojaku.github.io/adv-net-sci/_images/bdfb8d2caae07ea9c24e54daa9637ff2c55f7916a6e8bb91615ab2b38f366ec7.png)

---

# Design robust networks


**Molloy-Reed criterion**:

$$
\kappa_0 := \frac{\langle k^2 \rangle}{\langle k \rangle} > 2
$$

## What does this tell you about designing networks that are robust against random and targeted attacks 🤔?

- [Interactive demo](https://skojaku.github.io/adv-net-sci/vis/network-robustness.html)

---

# Key Takeaways 🗝️

1. MST is key for efficient network design
2. Robustness depends on attack type
3. Targeted attacks are more damaging than random ones
4. R-index measures network robustness
5. Percolation theory explains network robustness based on degree heterogeneity
6. Degree heterogeneity makes networks robust against random attacks but weak to targeted ones

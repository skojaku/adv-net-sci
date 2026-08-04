---
title: "Appendix: Proof of the Molloy-Reed Criterion"
---

In the main text we used two results without proving them:

1. A giant component exists when $\kappa = \dfrac{\langle k^2 \rangle}{\langle k \rangle} > 2$.
2. Under random failures the network falls apart once a fraction $f_c = 1 - \dfrac{1}{\kappa - 1}$ of nodes is removed.

This appendix derives both. The only tool we need is a careful answer to one question: **if I follow a random edge, what do I find at the other end?**

## Setup: what kind of network are we talking about?

The criterion applies to a network that is *randomly wired subject to a given degree sequence* — the configuration model. Picture giving node $i$ exactly $k_i$ half-edges ("hands"), throwing all the hands into a bag, and pairing them up at random.

::: {.column-margin}
This is the same null model we meet again in Module 5, where it supplies the $k_ik_j/2m$ term in modularity. There it answers "how many edges would I expect by chance?"; here it answers "does the network hold together?"
:::

The important consequence of random wiring is that the network is **locally tree-like**: starting from a node and walking outward, you almost never return to where you have already been, because short cycles are vanishingly rare in a large sparse random network. This is what lets us treat the exploration as a branching process.

## Step 1: following an edge is biased toward high degree

Let $p(k)$ be the fraction of nodes with degree $k$. If we pick a node *uniformly at random*, we get degree $k$ with probability $p(k)$, and the average degree is

$$
\langle k \rangle = \sum_{k} k \, p(k).
$$

But that is **not** how the exploration works. We arrive at nodes by following edges, and a node with many hands is many times more likely to be at the end of the hand we happened to grab.

Nodes of degree $k$ contribute $k \, p(k)$ hands to the bag, out of $\sum_{k} k\,p(k) = \langle k \rangle$ hands in total. So the probability that a randomly chosen hand belongs to a node of degree $k$ is

$$
q(k) = \frac{k \, p(k)}{\sum_{k'} k'\, p(k')} = \frac{k}{\langle k \rangle} p(k).
$$

::: {.callout-note title="This is the friendship paradox"}
$q(k)$ is exactly the mechanism behind the friendship paradox in Module 4: the person at the other end of a friendship tie is not an average person. Here it decides whether the network survives; there it decides whom to vaccinate. Same bias, two uses.
:::

The average degree of the node we land on is therefore

$$
\langle k \rangle_{q} = \sum_{k} k \, q(k) = \sum_{k} k \cdot \frac{k}{\langle k \rangle} p(k) = \frac{\langle k^2 \rangle}{\langle k \rangle} = \kappa.
$$

So $\kappa$ is not an abstract ratio: **it is the average degree of the node you reach by following a random edge.** Because it involves $\langle k^2 \rangle$, it is large whenever the degree distribution has a heavy tail — which is exactly the "degree heterogeneity" reading used in the main text.

## Step 2: the branching argument

Now explore the network outward from a randomly chosen starting node.

Arrive at some node by following an edge. On average it has $\kappa$ edges — but one of them is the edge we came in on, and that one leads backward. The number of *new* edges leading onward is on average

$$
\kappa - 1 = \frac{\langle k^2 \rangle}{\langle k \rangle} - 1.
$$

This quantity — the average number of onward edges from a node reached by an edge — is the **branching factor** of the exploration, and its value is the whole story:

- If $\kappa - 1 < 1$, each layer of the exploration is smaller than the last. The frontier shrinks geometrically and dies out after a few steps. Every component is small.
- If $\kappa - 1 > 1$, each layer is *larger* than the last. The frontier grows geometrically and reaches a finite fraction of the network. A giant component exists.

The transition sits exactly at $\kappa - 1 = 1$:

$$
\boxed{\;\kappa = \frac{\langle k^2 \rangle}{\langle k \rangle} > 2 \iff \text{a giant component exists.}\;}
$$

This is the **Molloy-Reed criterion**.

::: {.column-margin}
Molloy and Reed originally stated it as $\mathbb{E}[k(k-2)] > 0$. The two forms say the same thing: $\langle k^2 \rangle - 2\langle k \rangle > 0$, then divide through by $\langle k \rangle > 0$.
:::

::: {.callout-tip title="Sanity-check it on networks you know"}
- **A ring**, where every node has degree exactly 2: $\langle k^2\rangle = 4$, $\langle k \rangle = 2$, so $\kappa = 2$. Exactly at the threshold — and indeed a ring is a single cycle, connected but with nothing to spare. Cut one edge and it is a path; the structure is marginal.
- **Isolated pairs**, every node of degree 1: $\kappa = 1 < 2$. No giant component, as expected.
- **A Poisson network with $\langle k \rangle = 1$**: we show below that $\kappa = \langle k \rangle + 1 = 2$. This reproduces the classic Erdős-Rényi result that the giant component appears exactly at average degree 1.
:::

## Step 3: what random failure does to $\kappa$

Now remove nodes at random, keeping each with probability $p$ (so a fraction $f = 1-p$ is removed). The result is still a randomly wired network, so the criterion still applies — we only need its new $\kappa$.

Take a node that survives and originally had degree $k_0$. Each of its neighbors independently survives with probability $p$, so its new degree $k$ follows $\text{Binomial}(k_0, p)$. Using $\mathbb{E}[k \mid k_0] = p k_0$ and $\text{Var}(k \mid k_0) = k_0\, p (1-p)$:

$$
\begin{aligned}
\langle k \rangle_p &= p \, \langle k \rangle_0 \\[4pt]
\langle k^2 \rangle_p &= \mathbb{E}\left[\text{Var}(k \mid k_0) + \mathbb{E}[k \mid k_0]^2\right] = p(1-p)\langle k \rangle_0 + p^2 \langle k^2 \rangle_0
\end{aligned}
$$

Dividing gives a pleasantly simple result:

$$
\kappa_p = \frac{\langle k^2 \rangle_p}{\langle k \rangle_p} = \frac{p^2 \langle k^2 \rangle_0 + p(1-p)\langle k \rangle_0}{p \langle k \rangle_0} = p \, \kappa_0 + (1 - p).
$$

Random removal therefore drags $\kappa$ linearly from its original value $\kappa_0$ (at $p=1$) down toward $1$ (as $p \rightarrow 0$).

## Step 4: the critical fraction

The network disintegrates when $\kappa_p$ falls to the threshold value $2$:

$$
p_c \kappa_0 + (1 - p_c) = 2 \quad \Longrightarrow \quad p_c (\kappa_0 - 1) = 1 \quad \Longrightarrow \quad p_c = \frac{1}{\kappa_0 - 1}.
$$

Here $p_c$ is the fraction that must **remain**. Converting to the fraction **removed**, $f_c = 1 - p_c$:

$$
\boxed{\;f_c = 1 - \frac{1}{\kappa_0 - 1}\;}
$$

which is the formula used in the main text. Note that it depends on the original network only through $\kappa_0$ — a single number summarizing the entire degree distribution.

::: {.callout-note title="The same answer, without the algebra"}
The heuristic in the main text gets here in one line. After removing a fraction $f$, a node you reach still has $(1-f)(\kappa - 1)$ onward edges on average, and the exploration dies out when that branching factor falls to $1$:

$$(1-f_c)(\kappa - 1) = 1 \;\Longrightarrow\; f_c = 1 - \frac{1}{\kappa - 1}.$$

The derivation above is the same argument done carefully, and it confirms that treating the diluted network as a fresh configuration model is legitimate.
:::

## Step 5: reading off the two regimes

**Degree-homogeneous (Poisson) networks.** For a Poisson distribution with mean $\lambda = \langle k \rangle$, the second moment is $\langle k^2 \rangle = \lambda^2 + \lambda$. Hence

$$
\kappa_0 = \frac{\lambda^2 + \lambda}{\lambda} = \lambda + 1 = \langle k \rangle + 1,
\qquad
f_c = 1 - \frac{1}{(\langle k \rangle + 1) - 1} = 1 - \frac{1}{\langle k \rangle}.
$$

A denser random network is harder to break, but $f_c$ stays strictly below $1$: remove enough nodes and it always fragments.

::: {.callout-warning title="A common slip"}
It is tempting to write $\langle k^2 \rangle = \langle k \rangle^2$ here. That would say the degree variance is zero, which describes a *regular* graph, not a Poisson one — a Poisson distribution has variance equal to its mean, which is precisely the extra $+\lambda$ term. Dropping it gives $\kappa_0 = \langle k \rangle$ and the wrong threshold $1 - 1/(\langle k \rangle - 1)$.
:::

**Degree-heterogeneous (scale-free) networks.** For $P(k) \sim k^{-\gamma}$ with $2 < \gamma < 3$, the second moment $\langle k^2 \rangle$ diverges as the network grows. Then $\kappa_0 \rightarrow \infty$ and

$$
f_c = 1 - \frac{1}{\kappa_0 - 1} \rightarrow 1.
$$

Essentially every node must be removed before the giant component dies. This is the mathematical content of the claim that scale-free networks are extraordinarily robust to random failure — and, as the main text shows, it says nothing at all about targeted attack, where those same hubs become the network's weakness.

## What the proof assumes

Two assumptions are doing real work, and both can fail:

- **Local tree-likeness.** Real networks contain many triangles (Module 2), and clustering makes the exploration revisit nodes, which slows growth. The criterion is a good approximation for sparse, weakly clustered networks and degrades as clustering rises.
- **Randomness beyond the degree sequence.** If high-degree nodes preferentially attach to other high-degree nodes (assortativity, Module 4), the branching factor along an edge is no longer $\kappa - 1$ and the threshold shifts.

## References

- Molloy, M., & Reed, B. (1995). A critical point for random graphs with a given degree sequence. *Random Structures & Algorithms*, 6(2-3), 161-180.
- Cohen, R., Erez, K., ben-Avraham, D., & Havlin, S. (2000). Resilience of the Internet to random breakdowns. *Physical Review Letters*, 85(21), 4626-4629.
- Newman, M. E. J. (2018). *Networks* (2nd ed.), Chapter 11. Oxford University Press.

---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Modularity

**Modularity** is by far the most widely used method for community detection.
Modularity can be derived in many ways, but we will follow the one derived from assortativity.

## Assortativity

**Assortativity** is a measure of the tendency of nodes to connect with nodes of the same attribute.
The attribute, in our case, is the community that the node belongs to, and we say that a network is assortative if nodes of the same community are more likely to connect with each other than nodes of different communities.

Let's think about assortativity by using color balls and strings! 🎨🧵

Imagine we're playing a game as follows:

1. Picture each connection in our network as two colored balls joined by a piece of string. 🔴🟢--🔵🟡
2. The color of each ball shows which community it belongs to.
3. Now, let's toss all these ball-and-string pairs into a big bag.
4. We'll keep pulling out strings with replacement and checking if the balls on each end match colors.

The more color matches we find, the more assortative our network is. But, there's a catch!
What if we got lots of matches just by luck? For example, if all our balls were the same color, we'd always get a match. But that doesn't tell us much about our communities.
So, to be extra clever, we compare our results to a "random" version (null model):

1. We snip all the strings and mix up all the balls.
2. Then we draw pairs of balls at random *with replacement* and see how often the colors match.

By comparing our original network to this mixed-up version, we can see if our communities are really sticking together more than we'd expect by chance.
This comparison against the random version is the heart of modularity. Unlike graph cut methods that aim to maximize assortativity directly, modularity measures assortativity *relative* to *a null model*.

:::{figure-md} fig-modularity-game

<img src="../figs/modularity.jpg" alt="Single node failure" width="100%">

Illustration of how modularity measures assortativity relative to a null model.
:::

## Deriving Modularity

Now, let's put on our math hats and make this colorful game a bit more precise.

Let's introduce some helpful symbols to describe our network:
- $N$: This is our total number of nodes (or balls in our game)
- $M$: The number of edges (or strings) connecting our nodes
- $A_{ij}$: Adjacency matrix. If $A_{ij} = 1$, it means node $i$ and node $j$ are connected. If $A_{ij} = 0$, they're not connected.
- $k_i$: Degree of node $i$, i.e., how many edges a node has.
- $c_i$: Community of node $i$, i.e., which community a node belongs to.
- $\delta(c_i, c_j)$: Kronecker delta function. It gives us 1 if nodes $i$ and $j$ are the same color, and 0 if they're different.

```{admonition} Exercise
:class: tip

What is the probability of color matches for a given network? Derive the probability by using $\sum, M, A_{ij}, \delta(c_i, c_j)$.

```{dropdown} Hint
Let's think about our colorful bag of balls and strings! 🎨🧵
First, ask yourself:
1. How many strings do we have in total? (This is our M!)
2. Now, out of all these strings, how many are the same color on both ends?
```

```{admonition} Exercise
:class: tip

What is the probability of color matches for the random version? Derive the probability by using $\sum, M, \delta(c_i, c_j), k_i,k_j$.

```{dropdown} Hint
1. Imagine a big bag full of colorful balls, but this time without any strings. 🔴🟢🔵🟡
2. Now, think about picking one ball out of the bag. What are the chances of picking a specific color?
3. Then, put that ball back and pick another one. What are the odds this second ball matches the color of the first one?

```

The full modularity formula is on the next page 😉.
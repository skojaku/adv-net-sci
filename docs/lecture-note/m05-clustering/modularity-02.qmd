# Modularity (Cont.)

::: {#fig-fig-modularity-game}

<img src="../figs/modularity.jpg" alt="Single node failure" width="100%">

Illustration of how modularity measures assortativity relative to a null model.
:::

Let's dive into the modularity formula! To put modularity into math terms, we need a few ingredients:
- $m$: The total number of strings (edges) in our bag
- $n$: The total number of balls (nodes) we have
- $A_{ij}$: This tells us if ball $i$ and ball $j$ are connected by a string
- $\delta(c_i,c_j)$: This is our color-checker. It gives us a 1 if balls $i$ and $j$ are the same color (same community), and 0 if they're different.

Now, the probability of pulling out a string out of $m$ string and finding matching colors on both ends is:

$$
\frac{1}{m} \sum_{i=1}^n \sum_{j=i+1}^n A_{ij} \delta(c_i,c_j) = \frac{1}{2m} \sum_{i=1}^n \sum_{j=1}^n A_{ij} \delta(c_i,c_j)
$$

We set $A_{ii} = 0$ by assuming our network doesn't have any "selfie strings" (where a ball is connected to itself). Also, we changed our edge counting a bit. Instead of counting each string once (which gave us $m$), we're now counting each string twice (once from each end). That's why we use $2m$ in the equation.

Now, imagine we've cut all the strings, and we're going to draw two balls at random with replacement.
Here's how our new bag looks:
- We have $2m$ balls in total ($1$ string has $2$ balls, and thus $m$ strings have $2m$ balls in total).
- A node with $k$ edges correspond to the $k$ of $2m$ balls in the bag.
- The color of each ball in our bag matches the color (or community) of its node in the network.

Now, what's the chance of pulling out two balls of the same color?

$$
\sum_{c=1}^C \left( \frac{1}{2m}\sum_{i=1}^n k_i \delta(c, c_i) \right)^2
$$

where $k_i$ is the degree (i.e., the number of edges) of node $i$, and $C$ is the total number of communities (i.e., colors).

Here's what it means in simple terms:
- We look at each color ($c$) one by one (the outer sum).
- For each color, we figure out how many balls of that color are in our bag ($\frac{1}{2m}\sum_{i=1}^n k_i \delta(c, c_i)$).
- We divide by $2m$ to get the probability of drawing a ball of that color.
- We then calculate the chance of grabbing that color twice in a row ($\left( \frac{1}{2m}\sum_{i=1}^n k_i \delta(c, c_i) \right)^2$).
- Finally, we add up these chances for all $C$ colors.

Putting altogether, the modularity is defined by

$$
\begin{align}
Q &=\frac{1}{2m} \sum_{i=1}^n \sum_{j=1}^n A_{ij} \delta(c_i,c_j) - \sum_{c=1}^C \left( \frac{1}{2m}\sum_{i=1}^n k_i \delta(c, c_i) \right)^2
\end{align}
$$

Equivalently, a standard expression is given by

$$
Q =\frac{1}{2m} \sum_{i=1}^n \sum_{j=1}^n \left[ A_{ij} -  \frac{k_ik_j}{2m} \right]\delta(c_i,c_j)
$$

```{note}

Are the two forms of modularity the same formula? Let's see how we can transform one into the other:

1. We start with our first form of modularity:

   $$
   Q =\frac{1}{2m} \sum_{i=1}^n \sum_{j=1}^n A_{ij} \delta(c_i,c_j) - \sum_{c=1}^C \left( \frac{1}{2m}\sum_{i=1}^n k_i \delta(c, c_i) \right)^2
   $$

2. First, let's factor out $\frac{1}{2m}$ from both terms:

   $$
   Q =\frac{1}{2m} \left[ \sum_{i=1}^n \sum_{j=1}^n A_{ij} \delta(c_i,c_j) - \frac{1}{2m}\sum_{c=1}^C \left( \sum_{i=1}^n k_i \delta(c, c_i) \right)^2 \right]
   $$

3. Now, here's a neat trick: $(\sum_i a_i)^2 = (\sum_i a_i)( \sum_j a_j)$. We can use this to expand the squared term:

   $$
   Q =\frac{1}{2m} \left[ \sum_{i=1}^n \sum_{j=1}^n A_{ij} \delta(c_i,c_j) - \frac{1}{2m}\sum_{c=1}^C \left( \sum_{i=1}^n k_i \delta(c, c_i) \right) \left( \sum_{j=1}^n k_j \delta(c, c_j) \right)\right]
   $$

4. And here is another trick $(\sum_i a_i)( \sum_j a_j) = \sum_i a_i \sum_j a_j = \sum_i \sum_j a_ia_j$

   $$
   Q =\frac{1}{2m} \left[ \sum_{i=1}^n \sum_{j=1}^n A_{ij} \delta(c_i,c_j) - \frac{1}{2m}\sum_{c=1}^C \left( \sum_{i=1}^n \sum_{j=1}^n k_i k_j  \delta(c, c_i)  \delta(c, c_j) \right)\right]
   $$

5. Here's yet another cool trick, $\delta(c,c_i) \delta(c, c_j) = \delta(c_i,c_j)$. This means we can simplify our expression:

   $$
   Q =\frac{1}{2m} \left[ \sum_{i=1}^n \sum_{j=1}^n A_{ij} \delta(c_i,c_j) -  \frac{1}{2m} \sum_{i=1}^n \sum_{j=1}^n k_i k_j  \delta(c_i,c_j) \right]
   $$

6. Finally, we can factor out the common parts:

   $$
   Q =\frac{1}{2m} \sum_{i=1}^n \sum_{j=1}^n \left[ A_{ij} -  \frac{k_ik_j}{2m} \right]\delta(c_i,c_j)
   $$
```


## Modularity Demo

Let's learn how the modularity works by playing with a community detection game!

::: {.callout-note title="Exercise 1"}
:class: tip

Find communities by maximizing the modularity. {{ "<a href='BASE_URL/vis/community-detection/index.html?scoreType=modularity&numCommunities=2&randomness=1&dataFile=two-cliques.json'>Modularity maximization (two communities) 🎮</a>".replace('BASE_URL', base_url) }}

:::

One of the good things about modularity is that it can figure out how many communities there should be all by itself! 🕵️‍♀️ Let's have some fun with this idea. We're going to play the same game again, but this time, we'll start with a different number of communities. See how the modularity score changes as we move things around.

::: {.callout-note title="Exercise 2"}
:class: tip

Find communities by maximizing the modularity. {{ "<a href='BASE_URL/vis/community-detection/index.html?scoreType=modularity&numCommunities=4&randomness=1&dataFile=two-cliques.json'>Modularity maximization (four communities) 🎮</a>".replace('BASE_URL', base_url) }}
:::

Now, let's take our modularity maximization for a real-world example! 🥋 We're going to use the famous karate club network. This network represents friendships between members of a university karate club. It's a classic in the world of network science, and it's perfect for seeing how modularity works in practice.

::: {.callout-note title="Exercise 3"}
:class: tip

Find communities by maximizing the modularity. {{ "<a href='BASE_URL/vis/community-detection/index.html?scoreType=modularity&numCommunities=4&randomness=0.25&dataFile=net_karate.json'>Modularity maximization (four communities) 🎮</a>".replace('BASE_URL', base_url) }}

:::

## Limitation of Modularity

Like many other community detection methods, modularity is not a silver bullet. Thanks to extensive research, we know many limitations of modularity. Let's take a look at a few of them.

### Resolution limit

The modularity finds two cliques connected by a single edge as two separate communities.
But what if we add another community to this network?
Our intuition tells us that, because communities are *local* structure, the two cliques should remain separated by the modularity. But is this the case?

::: {.callout-note title="Exercise 4"}
:class: tip

Find communities by maximizing the modularity. {{ "<a href='BASE_URL/vis/community-detection/index.html?scoreType=modularity&numCommunities=3&randomness=0.9&dataFile=two-cliques-big-clique.json'>Modularity maximization (four communities) 🎮</a>".replace('BASE_URL', base_url) }}

::: {.callout-note collapse="true" title="Click here to see the solution"}

The best modularity score actually comes from merging our two cliques into one big community. This behavior is what we call the **Resolution limit** {footcite}`fortunato2007resolution`. Modularity can't quite make out communities that are smaller than a certain size!

Think of it like this: modularity is trying to see the big picture, but it misses the little details. In network terms, the number of edges $m_c$ in a community $c$ has to be bigger than a certain size. This size is related to the total number of edges $m$ in the whole network. We write this mathematically as ${\cal O}(m)$.
```

### Spurious communities

What if the network does not have any communities at all? Does the modularity find no communities? To find out, let's run the modularity on a random network, where each pair of nodes is connected randomly with the same probability.

::: {.callout-note title="Exercise 5"}
:class: tip

Find communities by maximizing the modularity. {{ "<a href='BASE_URL/vis/community-detection/index.html?scoreType=modularity&numCommunities=3&randomness=0.8&dataFile=random-net.json'>Modularity maximization (four communities) 🎮</a>".replace('BASE_URL', base_url) }}

::: {.callout collapse="true"}
## Click here to see the solution

Surprise, surprise! 😮 Modularity finds communities even in our random network, and with a very high score too! It's like finding shapes in clouds - sometimes our brains (or algorithms) see patterns where there aren't any.

The wild thing is that the modularity score for this random network is even higher than what we saw for our network with two clear cliques!

This teaches us two important lessons:
1. We can't compare modularity scores between different networks. It's like comparing apples and oranges! 🍎🍊
2. A high modularity score doesn't always mean we've found communities.

Interested readers can read more about this in [this tweet by Tiago Peixoto](https://twitter.com/tiagopeixoto/status/1466352013856358400) and the discussion [here](https://reticular.hypotheses.org/1924).

<blockquote class="twitter-tweet" style="max-width: 550px;"><p lang="en" dir="ltr">Modularity maximization is not a reliable method to find communities in networks. Here&#39;s a simple example showing why:<br><br>1. Generate an Erdős-Rényi random graph with N nodes and average degree &lt;k&gt;.<br><br>2. Find the maximum modularity partition. <a href="https://t.co/MTt5DdFXSX">pic.twitter.com/MTt5DdFXSX</a></p>&mdash; Tiago Peixoto (@tiagopeixoto) <a href="https://twitter.com/tiagopeixoto/status/1466352013856358400?ref_src=twsrc%5Etfw">December 2, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
```


## So should we avoid modularity?

The simple answer is no. Modularity is still a powerful tool for finding communities in networks. Like any other method, it has its limitations. And knowing these limitations is crucial for using it effectively. There is "free lunch" in community detection {footcite}`peel2017ground`.

When these implicit assumptions are met, modularity is in fact a very powerful method for community detection. For example, it is in fact an "optimal" method for a certain class of networks {footcite}`nadakuditi2012graph`.

So, keep modularity in your toolbox. Just remember to use it wisely!


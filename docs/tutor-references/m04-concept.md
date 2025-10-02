# Module 04: Node Degree - Core Concepts

## The Fundamental Concept: Node Degree

**Node degree** is the number of edges connected to a node - the most basic yet powerful measure in network analysis. While simple to define, degree reveals network structure and drives many collective behaviors.

### Individual vs. Network Level
- **Individual level**: Degree measures visibility and influence - high-degree nodes spread information quickly
- **Network level**: The collection of degrees (degree distribution) reveals centralization patterns

## Degree Distribution

The **degree distribution** shows the fraction of nodes with each degree value. It answers: "How common is each degree?"

### Why It Matters
Degree distribution shapes network behavior:
- **Robustness**: Heavy-tailed distributions tolerate random failures but are vulnerable to targeted hub attacks
- **Small-world effects**: Hub-dominated distributions create shortcuts that reduce path lengths
- **Spreading processes**: High-degree nodes accelerate information/disease transmission

## The Friendship Paradox

The **Friendship Paradox** (Scott Feld, 1991) states that *your friends have more friends than you do on average*. This is not an insult — it is a statistical consequence of how connections are counted in most social networks. This counterintuitive phenomenon emerges from the mathematical properties of networks and has profound implications for how we understand social structures, information flow, and even public health interventions.

At its core, the Friendship Paradox reveals a fundamental asymmetry in social networks: high-degree nodes (popular individuals) are more likely to be counted as friends by others, while low-degree nodes are less likely to be referenced. This creates a sampling bias where the average degree of your friends tends to be higher than your own degree, and indeed higher than the average degree of the entire network.

```{dot}
//| fig-width: 4
//| fig-height: 3
//| fig-cap: "Friendship paradox example — node labels show degrees"
//| label: fig-friendship-dot
graph G {
  layout=neato
  Alex  [label="Alex\n(1)",  shape=circle, style=filled, fillcolor="#f5cbcc"];
  Bob   [label="Bob\n(3)",   shape=circle, style=filled, fillcolor="#ffd9a6"];
  Carol [label="Carol\n(1)", shape=circle];
  David [label="David\n(1)", shape=circle];
  Alex -- Bob;
  Carol -- Bob;
  David -- Bob;
}
```

The network diagram above illustrates the Friendship Paradox with a simple four-node network.
The average degree in this network is (1+3+1+1)/4 = 1.5, but when we look at the average degree of each person's friends, we get a different story.

Let us list all the friendship ties in adjacency list format, along with the degree of each node in parentheses:

- Bob: Alex (1), Carol (1), David (1)
- Alex: Bob (3)
- Carol: Bob (3)
- David: Bob (3)

Now, let's compute the average degree of a friend.

$$
\frac{\overbrace{1 + 1 + 1}^{\text{Bob's friends}} + \overbrace{3 + 3 + 3}^{\text{The friends of Alex, Carol, and David}}}{\underbrace{6}_{\text{\# of friends}}} = 2
$$

which confirms the friendship paradox, i.e., a someone's friend tends to have more friends than that someone.

Why this produces the paradox? Notice that high-degree nodes like Bob are referenced multiple times when computing the average degree of a friend. This is because Bob are a friend of many friends! On the other hand, low-degree nodes are referenced less often.
This bias towards high-degree nodes is what makes the friendship paradox a paradox.

Beyond a fun trivia, the friendship paradox has practical implications. In social networks, most people will find that their friends have more friends than they do, not because they're unpopular, but because of this statistical bias. The same principle applies to many other networks: in scientific collaboration networks, your coauthors tend to have more collaborators than you do; in the internet, the websites you link to tend to have more incoming links than your website.

### The friendship paradox in public health

This observation has profound practical consequences, especially in public health and epidemiology. To slow an epidemic you can use the friendship paradox to find better targets, called **acquaintance immunization** [@cohen2003efficient], which goes as follows:

1. Pick a random sample of individuals.
2. Ask each to nominate one friend.
3. Vaccinate the nominated friends (who tend to be better connected).

This works because when people nominate a friend, they're more likely to name someone with many social connections. By targeting these nominated friends, public health officials can reach the most connected individuals in a network without needing to map the entire social structure.

## Visualizing degree distributions

The very first step to understand degree distribution is to visualize it. But visualizing degree distribution is not as simple as it seems. For a real-world network, most nodes have a very small degree, so they are all crammed into the first few bins on the left. The long tail of high-degree nodes---which hold most edges in the network---is invisible because there are very few of them. This is a **fat-tailed distribution**, which is a common characteristics of real-world networks.

To solve this, we can plot the same histogram but with both axes on a logarithmic scale. This is called a **log–log plot**. A log–log plot makes both low- and high-degree nodes visible, revealing heavy-tailed patterns. If the tail is roughly linear, it suggests a power-law degree distribution: the probability a node has degree $k$ falls off as $k^{-\gamma}$. The slope of the line shows how quickly high-degree nodes become rare. A steeper slope (higher $\gamma$) means fewer hubs; a shallower slope means more.

The log-log plot above shows *probability density function* (PDF) of the degree distribution. It is defined as the fraction of nodes with degree exactly $k$.

$$
p(k) = \frac{\text{number of nodes with degree } k}{N}
$$

where $N$ is the total number of nodes in the network.

The PDF is useful but often noisy, especially in the tail where there are few observations. A better, more stable choice is the *complementary cumulative distribution function* (CCDF), which is useful for plotting heavy-tailed distributions.

$$
\text{CCDF}(k) = P(k' > k) = \sum_{k'=k+1}^\infty p(k')
$$

CCDF represents the fraction of nodes with degree greater than $k$, or equivalently, the fraction of nodes that survive the degree cutoff $k$. It is also known as the *survival function* of the degree distribution. A nice feature of the CCDF compared to the PDF is that it does not require any binning of the data. When calculating the PDF, we need to bin the data into a finite number of bins, which is subject to the choice of bin size. CCDF does not require any binning of the data.

### Interpreting the CCDF for Power-Law Distributions

For networks whose degree distribution follows a power law, the CCDF offers a direct path to estimating the power-law exponent, $\gamma$. Let's walk through the derivation to see how.

A continuous power-law distribution is defined by the probability density function (PDF):
$$
p(k) = Ck^{-\gamma}
$$
where $C$ is a normalization constant ensuring the total probability is 1.

The CCDF, which we denote as $P(k)$, is the probability that a node's degree $k'$ is greater than some value $k$. We calculate this by integrating the PDF from $k$ to infinity:
$$
P(k) = \int_{k}^{\infty} p(k') dk' = \int_{k}^{\infty} Ck'^{-\gamma} dk'
$$
Performing the integration gives us:
$$
P(k) = C \left[ \frac{k'^{-\gamma+1}}{-\gamma+1} \right]_{k}^{\infty}
$$
Assuming $\gamma > 1$, which is typical for real-world networks, the term $k'^{-\gamma+1}$ approaches zero as $k'$ approaches infinity. The expression simplifies to:
$$
P(k) = -C \left( \frac{k^{-\gamma+1}}{-\gamma+1} \right) = \frac{C}{\gamma-1} k^{-(\gamma-1)}
$$
This result shows that the CCDF itself follows a power law, $P(k) \propto k^{-(\gamma-1)}$.

To see what this means for a log-log plot, we take the logarithm of both sides:
$$
\log P(k) = \log\left(\frac{C}{\gamma-1}\right) - (\gamma-1)\log(k)
$$
This equation is in the form of a straight line, $y = b + mx$, where:

- $y = \log P(k)$
- $x = \log(k)$
- The y-intercept $b = \log\left(\frac{C}{\gamma-1}\right)$
- The slope $m = -(\gamma-1) = 1-\gamma$

::: {.callout-important title="Key Relationship"}
**For a power-law distribution, the slope of the CCDF on a log-log plot is $1 - \gamma$.**

This is a crucial point for accurately estimating the scaling exponent from empirical data. For example, if you measure the slope of the CCDF plot to be -1.3, the estimated power-law exponent $\gamma$ is $2.3$, not $1.3$ (since $-1.3 = 1 - 2.3$).
:::

## Degree Bias and Its Implications

### Sampling Bias
When sampling nodes through their connections (neighbor sampling):
- High-degree nodes are overrepresented
- Low-degree nodes are underrepresented
- Leads to biased estimates of network properties

### Practical Applications

#### Public Health
- **Early detection**: Monitor high-degree individuals for disease outbreaks
- **Intervention strategies**: Vaccinate social hubs for maximum impact
- **Contact tracing**: Focus on nodes with many connections

#### Social Networks
- **Influence maximization**: Target high-degree users for viral marketing
- **Information spread**: Understand how news/rumors propagate
- **Network effects**: Explain why people perceive trends as more popular than they are

#### Infrastructure
- **Robustness planning**: Protect critical high-degree nodes
- **Attack strategies**: Target hubs for maximum network disruption
- **Resource allocation**: Prioritize maintenance of critical connection points

## Degree-Based Network Classification

### Types of Degree Distributions

#### Random Networks (Poisson)
- Most nodes have similar degrees around the mean
- Few very high or very low degree nodes
- Bell-curve-like distribution

#### Scale-Free Networks (Power-law)
- Heavy-tailed distribution: P(k) ~ k^(-γ)
- Many low-degree nodes, few high-degree hubs
- No characteristic scale

#### Regular Networks
- All nodes have identical or very similar degrees
- Narrow degree distribution
- Common in lattices and grid structures

## Mathematical Properties

### Degree Sum Formula
For any network: Σ(degrees) = 2 × (number of edges)

### Handshaking Lemma
In any network, the number of nodes with odd degree is even.

### Degree Correlations
- **Assortative**: High-degree nodes connect to other high-degree nodes
- **Disassortative**: High-degree nodes connect to low-degree nodes
- **Neutral**: No degree correlation

These correlation patterns affect network resilience, spreading dynamics, and structural properties.
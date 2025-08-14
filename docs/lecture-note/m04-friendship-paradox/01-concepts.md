# M04 Concepts: The Friendship Paradox

## What We Learn in This Module

In this module, we will learn about the friendship paradox. Specifically:
- Friendship paradox: what is it, why it's important, and what are the consequences?
- **Keywords**: friendship paradox, degree bias

## In-Class Experiment

"Your friends have more friends than you" is a well-known phenomenon in social networks. It appears everywhere from physical social networks to online social networks, and even random networks!
OK. Let's do not "think" but "feeeeel" this paradox through the following in-class experiment.

## Experiment Materials and Procedure

**Materials:**
- [📇 Friendship card](./friendship-cards.pdf)
- 🖊️ Pen

**Friendship Network Experiment:**

```
┌─────────────────────────────────────────────────────────────┐

   1. [📇] Receive Your Card
      Get a card with a unique letter

   2. [🤝] Meet and Greet (5 mins)
      Move around, exchange cards with at least one friend

   3. [🧮] Count Connections (2 mins)
      Count received cards, write number, return cards

   4. [📈] Calculate Average (2 mins)
      Calculate average 'friend count' of your friends

   5. [📝] Fill Form
      Write your average and your own friend count
      in a separate sheet

└─────────────────────────────────────────────────────────────┘

❗ Important Notes:
  • This is a fun experiment, not a popularity contest
  • Be respectful and inclusive during the meet and greet
  • If you finish early, wait patiently for further instructions
```

## The Friendship Paradox Explained

## The Origin of the Friendship Paradox

The paradox arises not because of the way we form friendships. It's about measurement! For example a person with 100 friends generates 100 cards, while a person with 1 friend generates only 1 card. If we average friend counts over the cards, popular people are counted more. This is where the friendship paradox comes from.

In network terms, cards represent edges and people represent nodes. The friendship paradox arises because we measure at different levels: nodes or edges. The average friend count at the node level is lower than at the edge level because popular people are counted more often at the edge level.

## Key Questions to Consider

- **🎉 Fun Challenge**: Can you create a network where your friends have the most friends? 🤔💡 Give it a try in this [Friendship Paradox Game! 🎮✨](../assets/vis/friendship-paradox-game.html)

- **Question**: Can you create a network where the friendship paradox is absent? In other words, can you create a graph, where your friends have the same number of friends as you?

## Practical Applications: Vaccination Game

Beyond an interesting trivia, the friendship paradox has many practical utilities.

## Strategic Vaccination

The friendship paradox has important implications for public health strategies. By understanding that highly connected individuals are more likely to be selected through their connections, we can develop more effective vaccination strategies.

- **🎉 Fun Challenge**: Can you control the spread of a virus by strategically vaccinating individuals? 🤔💡 Give it a try in this [Vaccination Game! 🎮✨](../assets/vis/vaccination-game.html)

## Why Vaccination Strategy Works

When we vaccinate people chosen through the friendship paradox principle:
1. We're more likely to vaccinate highly connected individuals
2. Highly connected people are more likely to spread diseases
3. Vaccinating them creates a disproportionate impact on disease spread
4. This strategy is more effective than random vaccination

## Mathematical Foundation

The friendship paradox can be understood through the concept of degree bias:

- **Node sampling**: Selecting people randomly gives equal weight to everyone
- **Edge sampling**: Selecting people through their connections gives higher weight to popular people
- **Result**: Edge sampling systematically overrepresents high-degree nodes

### Mathematical Proof of the Friendship Paradox

When we sample friends through edge-based sampling (selecting an edge and then a node), the sampling is biased toward high-degree nodes. A person with $k$ edges is $k$ times more likely to be sampled than someone with 1 edge.

The degree distribution $p'(k)$ of a friend is given by:

$$
p'(k) = \frac{k}{\langle k \rangle} p(k)
$$

where $\langle k \rangle$ is the average degree. The average degree of a friend is:

$$
\langle k' \rangle = \sum_{k} k \cdot p'(k) = \frac{\langle k^2 \rangle}{\langle k \rangle}
$$

which is always larger than $\langle k \rangle$:

$$
\langle k' \rangle = \frac{\langle k^2 \rangle}{\langle k \rangle} \geq \langle k \rangle
$$

This mathematical proof confirms: **your friends have more friends than you, on average!**

## Data Visualization Fundamentals

### Understanding Histograms: Area vs. Height

When plotting degree distributions, it's crucial to understand that in a proper histogram representing probability density:

- **Area represents probability**, not height
- Each bar's area = width × height = probability for that interval
- Total area under all bars = 1 (for probability distributions)
- Height = density = probability/bin_width

For discrete distributions like degree distributions:
- Bar width typically = 1 (for integer degrees)
- Height = probability mass = p(k)
- Area = height × width = p(k) × 1 = p(k)

### Logarithmic Scale Fundamentals

Logarithmic scales are essential for analyzing heavy-tailed distributions:

**Why use log scales?**
- **Compress large ranges**: Display data spanning several orders of magnitude
- **Reveal patterns**: Power-law relationships appear as straight lines
- **Highlight tails**: Makes rare, high-degree nodes visible

**Log-log plots**: Both axes use logarithmic scales
- Power-law: $y = ax^b$ becomes $\log y = \log a + b \log x$ (straight line)
- Slope = power-law exponent

**Semi-log plots**: Only one axis uses logarithmic scale
- Exponential decay appears as straight line

**Key considerations**:
- Cannot plot zero values (log(0) is undefined)
- Small values become very negative
- Relative differences become absolute differences

### Complementary Cumulative Distribution Function (CCDF)

CCDF is particularly useful for heavy-tailed distributions:

$$
\text{CCDF}(k) = P(k' > k) = \sum_{k'=k+1}^\infty p(k')
$$

**Advantages over PDF**:
- Monotonically decreasing (smoother visualization)
- No binning required
- Contains full information of the distribution
- Better visualization of tails in log-log plots

## Trivia: Benford's Law Connection

The friendship paradox relates to a fascinating phenomenon called **Benford's Law**, which states that in many naturally occurring datasets, the leading digit "1" appears about 30% of the time, "2" about 17.6%, and so on.

### What is Benford's Law?

Benford's Law describes the frequency distribution of leading digits in many datasets:

$$
P(d) = \log_{10}\left(1 + \frac{1}{d}\right)
$$

where $d$ is the leading digit (1, 2, ..., 9).

**Expected frequencies**:
- 1: 30.1%, 2: 17.6%, 3: 12.5%, 4: 9.7%, 5: 7.9%
- 6: 6.7%, 7: 5.8%, 8: 5.1%, 9: 4.6%

### Connection to Network Phenomena

Both Benford's Law and the friendship paradox involve **sampling bias**:

- **Benford's Law**: Scale-invariant distributions naturally produce this digit pattern
- **Friendship Paradox**: Edge-based sampling overrepresents high-degree nodes

**Common thread**: When data spans multiple orders of magnitude (like network degrees), sampling methods matter tremendously.

Benford's Law appears in:
- Network degree sequences (sometimes)
- Financial data, population sizes
- Scientific measurements, social media metrics

Just as the friendship paradox reveals hidden structure in social networks, Benford's Law reveals hidden patterns in naturally occurring data!

This mathematical insight has applications beyond friendships, including:
- Social network analysis
- Epidemiology and disease control
- Marketing and influence strategies
- Network robustness and vulnerability assessment
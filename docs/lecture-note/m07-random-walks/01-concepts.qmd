# Random Walks: Core Concepts

## What to learn in this module

In this module, we will learn random walks, one of the most fundamental techniques in network analysis. We will learn:
- What is a random walk?
- How to simulate a random walk on a network?
- What is the behavior of a random walk on a network?
- Implicit connections to community detection and network centralities
- **Keywords**: random walk, community detection, network centralities

## Introduction through Games: Ladder Lottery

::: {.callout-note title="Ladder Lottery"}
:class: tip

Ladder Lottery is a fun East Asian game, also known as "鬼腳圖" (Guijiaotu) in Chinese, "阿弥陀籤" (Amida-kuzi) in Japanese, "사다리타기" (Sadaritagi) in Korean, and "Ladder Lottery" in English. The game is played as follows:
1. A player is given a board with a set of vertical lines.
2. The player chooses a line and starts to move along the line
3. When hitting a horizontal line, the player must move along the horizontal line and then continue to move along the next vertical line.
4. The player wins if the player can hit a marked line at the bottom of the board.
5. You cannot see the horizontal lines in advance!

Play the {{ '[Ladder Lottery Game! 🎮✨]( BASE_URL/vis/amida-kuji.html?)'.replace('BASE_URL', base_url) }} and try to answer the following questions:

1. Is there a strategy to maximize the probability of winning?
2. How does the probability of winning change as the number of horizontal lines increases?

![](https://upload.wikimedia.org/wikipedia/commons/6/64/Amidakuji_2022-05-10.gif)

:::

### Connection to Random Walks

The Ladder Lottery game is actually a perfect introduction to random walks! In this game:
- **States** are the vertical lines
- **Transitions** happen when you encounter horizontal connections
- **Randomness** comes from not knowing where the horizontal lines are placed
- **Long-term behavior** determines your probability of winning

This simple game illustrates many key concepts we'll explore in random walks on networks.

## Fundamental Concepts

### What is a Random Walk?

Suppose you walk in a city. You are drunk and your feet have no idea where to go. You just take a step wherever your feet take you. At every intersection, you make a random decision and take a step. This is the core idea of a random walk.

While your feet are taking you to a random street, after making many steps and looking back, you will realize that you have been to certain places more frequently than others. If you were to map the frequency of your visits to each street, you will end up with a distribution that tells you about salient structure of the street network.

### Random Walks in Networks

A random walk in undirected networks is the following process:
1. Start at a node $i$
2. Randomly choose an edge to traverse to a neighbor node $j$
3. Repeat step 2 until you have taken $T$ steps.

```{note}
In case of directed networks, a random walker can only move along the edge direction, and it can be that the random walker is stuck in a so-called "dead end" that does not have any outgoing edges.
```

### Key Questions to Consider

When studying random walks, we want to understand:

1. **Short-term behavior**: Where does the walker go in the first few steps?
2. **Long-term behavior**: After many steps, where does the walker spend most of its time?
3. **Structural insights**: What does the walker's behavior tell us about the network?
4. **Applications**: How can we use random walks for centrality and community detection?

## Pen and Paper Exercises

Before diving into the mathematical details and coding, it's important to work through some fundamental concepts by hand.

- [✍️ Pen and paper exercises](pen-and-paper/exercise.pdf)

These exercises will help you:
- Understand the basic mechanics of random walks
- Calculate transition probabilities manually
- Explore simple examples of stationary distributions
- Connect random walk concepts to network properties

## Preview: What's Coming Next

In the following sections, we will:
1. **Dive into the mathematics** behind random walks and their connection to Markov chains
2. **Implement random walks in code** and visualize their behavior on real networks
3. **Explore applications** including centrality measures and community detection
4. **Work through practical exercises** to solidify your understanding

The journey from this simple concept to powerful network analysis tools is both fascinating and practical!
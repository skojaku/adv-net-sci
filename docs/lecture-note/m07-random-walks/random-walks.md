# Random Walks

Suppose you walk in a city. You are drunk and your feet have no idea where to go. You just take a step wherever your feet take you. At every intersection, you make a random decision and take a step. This is the core idea of a random walk.

While your feet are taking you to a random street, after making many steps and looking back, you will realize that you have been to certain places more frequently than others. If you were to map the frequency of your visits to each street, you will end up with a distribution that tells you about salient structure of the street network. It is surprising that this seemingly random, brainless behavior can tell us something deep about the structure of the city.


<img src="../figs/random-walk.png" alt="Random walk on a network" width="50%" style="display: block; margin-left: auto; margin-right: auto;">

## Random walks in a network

A random walk in undirected networks is the following process:
1. Start at a node $i$
2. Randomly choose an edge to traverse to a neighbor node $j$
3. Repeat step 2 until you have taken $T$ steps.





```{note}
In case of directed networks, a random walker can only move along the edge direction, and it can be that the random walker is stuck in a so-called ``dead end'' that does not have any outgoing edges.
```

How does this simple process tell us something about the network structure? To get some insights, let us play with a simple interactive visualization.

::: {.callout-note title="Random Walk Simulation"}
:class: tip

Play with the {{ '[Random Walk Simulator! 🎮✨]( BASE_URL/vis/random-walks/index.html?)'.replace('BASE_URL', base_url) }} and try to answer the following questions:

1. When the random walker makes many steps, where does it tend to visit most frequently?
2. When the walker makes only a few steps, where does it tend to visit?
3. Does the behavior of the walker inform us about centrality of the nodes?
3. Does the behavior of the walker inform us about communities in the network?

:::

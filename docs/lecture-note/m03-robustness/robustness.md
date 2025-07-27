# Network Robustness

Nodes and edges can fail or be attacked, which disrupt the connectivity of a network.
Roughly speaking, we say a network is robust if it maintain most of its connectivity after failures or attacks.
There are different types of attacks, together with how we quantify the damage they cause. So let us first showcase a case study with code.

## Random node failures

Nodes can fail and disconnect from networks, such as power station closures in power grids. This is modeled as a **random failure**, where randomly chosen nodes are removed from the network. When a node fails, it and its edges are removed.

The damage varies depending on the node to be removed. The damage to the network can be measued in many different ways, but an accepted measure is the loss of **connectivity**, defined as the fraction of nodes left in the largest connected part of the network after the failure.

![](../figs/single-node-failure.jpg){#fig-single-node-failure fig-alt="The impact of removing a single node varies based on which node is removed."}

: The impact of removing a single node varies based on which node is removed. {#fig-single-node-failure}

Multiple nodes can fail simultaneously, e.g., due to natural disasters like earthquakes or tsunamis.
Thus it is often useful to assess the robustness of the network against such failures.
**Robustness profile** is a plot of the connectivity drop as a function of the number of nodes removed. It provides a visual summary of the robustness of the network against *a given sequential failure of nodes*.
In random failure, the order of nodes removed is random.

![](../figs/robustness-profile.jpg){#fig-multiple-node-failure fig-alt="Robustness profile of a network for a sequential failure of nodes."}

: Robustness profile of a network for a sequential failure of nodes. {#fig-multiple-node-failure}

Beyond the qualitative observation, it is useful to quantify the robustness of the network.
The **$R$-index** is a single number that summarizes the robustness of the network.
It is defined as the area under the connectivity curve with integral approximation.

$$
R = \frac{1}{N} \sum_{k=1}^{N-1} y_k
$$

where $y_k$ is the connectivity at fraction $k/N$ of nodes removed, where $N$ is the total number of nodes in the network. A higher value indicates that the network is robust against the attack. The $R$-index has a maximum value of 1/2 (i.e., which corresponds to a diagonal line in the plot above).


## Targeted attack

A network robust against random failures can still be fragmented by **targeted attacks**.
In targeted attacks, nodes are removed based on specific criteria rather than randomly.
For example, nodes can be removed in order of their degree, starting with the largest degree to the smallest degree. The rationale for this attack strategy is that large-degree nodes have many connections, so removing them disrupts the network more significantly.

Degree-based attack is not the only form of targeted attacks. Other forms of targeted attacks include removing nodes based on their centrality (closeness centrality, betweenness centrality) and those based on proximity.

## What's next?

In the next section, we will code up a simple example to compute the robustness profile of a network using Python.

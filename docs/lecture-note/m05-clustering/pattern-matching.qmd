# Community detection (pattern matching)

Community detection is an abstract unsupervised problem. It is abstract because there is no clear-cut definition or ground truth to compare against. The concept of a community in a network is subjective and highly context-dependent.

A classical approach to community detection is based on *pattern matching*.
Namely, we first explicitly define a community by a specific connectivity pattern of its members. Then, we search for these communities in the network.

::: {#fig-clique}

<img src="https://pythonhosted.org/trustedanalytics/R_images/k-clique_201508281155.png" alt="Clique graph" width="80%">

Cliques of different sizes. Taken from [https://pythonhosted.org/trustedanalytics/python_api/graphs/graph-/kclique_percolation.html](https://pythonhosted.org/trustedanalytics/python_api/graphs/graph-/kclique_percolation.html)
:::

Perhaps, the strictest definition of a community is a *clique*: a group of nodes all connected to each other. Examples include triangles (3-node cliques) and fully-connected squares (4-node cliques).
However, cliques are often too rigid for real-world networks. In social networks, for instance, large groups of friends rarely have every member connected to every other, yet we want to accept such "in-perfect" social circles as communities.
This leads to the idea of relaxed versions of cliques, called **pseudo-cliques**.

Pseudo-cliques are defined by relaxing at least one of the following three dimensions of strictness:

1. Degree: Not all nodes need to connect to every other node.
   - **$k$-plex**: each node connects to all but $k$ others in the group {footcite}`seidman1978graph`.
   - **$k$-core**: each node connects to $k$ others in the group {footcite}`seidman1983network`.
2. Density: The overall connection density can be lower.
   - **$\rho$-dense subgraphs**, with a minimum edge density of $\rho$ {footcite}`goldberg1984finding`.
3. Distance: Nodes can be further apart.
   - **$n$-clique**, where all nodes are within n steps of each other {footcite}`luce1950connectivity`.
4. Combination of the above:
   - **n-clan** and **n-club** {footcite}`mokken1979cliques`
   - **$k$-truss**, a maximal subgraph where all edges participate in at least $k-2$ triangles {footcite}`saito2008extracting,cohen2009graph,wang2010triangulation`.
   - **$\rho$-dense core**, a subgraph with minimum conductance $\rho$ {footcite}`koujaku2016dense`.

::: {#fig-clique-pattern}

<img src="https://ars.els-cdn.com/content/image/1-s2.0-S0378873315000520-gr1.jpg" alt="Pseudo-clique patterns" width="80%" style="display: block; margin-left: auto; margin-right: auto;">


Illustation of different pseudo cliques. Taken from {footcite}`koujaku2016dense`.

:::




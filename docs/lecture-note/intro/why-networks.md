---
title: Networks
---

## Networks are everywhere and they matter

In 2009, the H1N1 influenza pandemic started in Mexico and spread around the world. Dirk Brockmann and Dirk Helbing tracked how the disease reached different countries and made a surprising discovery that would revolutionize how we understand spreading processes.

The most natural way to think about disease spread is through geographic distance.
If you looked at a traditional world map, you might expect the disease to spread in expanding circles - first to nearby countries like Guatemala and the United States, then gradually to more distant places. But look at what the data actually shows:

::: {#fig-geo-vs-arrival-time}

![](https://www.science.org/cms/10.1126/science.1245200/asset/59290a15-76de-4a0f-9107-259201f98bcf/assets/graphic/342_1337_f1.jpeg)

Geographic distance shows only weak correlation with disease arrival times for simulated pandemics (C), H1N1 2009 (D), and SARS 2003 (E).

:::


Distance does explain the arrival time to some extent - there's a rough trend where farther places tend to be infected later (C, D, E). But it doesn't tell the whole story. At the same distances, some cities experienced early arrival while others experienced much later arrival. What explains this variation?

This mystery was solved by Dirk Brockmann and his colleagues, who realized that disease spread follows the hidden geometry of mobility networks - not geographic maps. Air travel connections, not physical distance, determined how quickly the pandemic reached different parts of the world.

::: {#fig-network-distance-vs-arrival-time}

![](https://www.science.org/cms/10.1126/science.1245200/asset/66d5a7ec-a683-4135-af2f-149c91007e48/assets/graphic/342_1337_f2.jpeg)

Effective distance (based on mobility networks) shows strong correlation with disease arrival times (R² = 0.973) for simulated pandemics (C), H1N1 2009 (D), and SARS 2003 (E).
:::

::: {.column-margin}
See [@brockmann2013hidden] for more details.
:::

The H1N1 example above reveals a fundamental truth: ***network structure determines how things spread***. Geographic distance became irrelevant once we understood the underlying mobility network. This principle extends far beyond disease outbreaks.

Networks are everywhere. Look around you: plants depend on pollinators in ecological networks, predators and prey form intricate food webs, your brain operates through neural networks, and modern medicine maps drug interactions. At the molecular level, proteins interact in complex networks that sustain life. Socially, we're connected through friendship networks, while globally, financial institutions form interconnected webs that can trigger worldwide crises. Every flight you take follows airport networks, every light switch connects to power grids, and every river flows through branching networks to the sea. Even the internet connecting you to this text and the knowledge graphs organizing human understanding - all are networks.


::: {layout-nrow=4}

![Plant pollinator network](https://mlurgi.github.io/networks_for_r/lesson-images/plant-pollinator.png)

![Food web](https://mlurgi.github.io/networks_for_r/images/food-web.png)

![Brain network](https://assets.thehansindia.com/h-upload/2020/03/08/952035-brain.webp)

![Medicine network](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41746-019-0141-x/MediaObjects/41746_2019_141_Fig1_HTML.png)

![Protein-protein interaction](https://upload.wikimedia.org/wikipedia/commons/5/56/1dfj_RNAseInhibitor-RNAse_complex.jpg)

![Social network](https://miro.medium.com/v2/resize:fit:1400/1*4MXaZGRjWL_X-LgDNjd-9w.png)

![International financial network](https://www.researchgate.net/profile/Douglas-White-4/publication/26692139/figure/fig1/AS:652592984096773@1532601700652/A-sample-of-the-international-financial-network-where-the-nodes-represent-major.png)

![US airport network](https://www.researchgate.net/profile/Victor-Eguiluz/publication/287325801/figure/fig1/AS:613998437363713@1523400043126/Map-of-the-US-airport-network-for-July-13-Airports-are-represented-as-nodes-and-edges-as.png)

![Power grid network](https://www.sciencenews.org/wp-content/uploads/2020/02/021520_power_inline-1_680.png)

![River network](https://www.treehugger.com/thmb/ScAa4BnU5Ld_rzGNo0IIZNv91U4=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8747607969_65098e4af6_o-f3ebcfa0d1894613995f1c086d1442ac.png)

![Internet network](https://www.researchgate.net/profile/Quan-Nguyen-123/publication/325794369/figure/fig2/AS:639787606220801@1529548660141/Example-of-large-and-complex-networks-Visualization-of-the-Internet-graph-by-the-Opte.png)

![Knowledge graph](https://miro.medium.com/v2/resize:fit:617/1*chWX0v67nJ0JUzbGiN8ulQ.png)

:::

## How to represent a network

Although networks come from vastly different fields, **we can represent them all using the same universal language** 😉. Whether we're studying brain connections, protein interactions, or social relationships, the mathematical representation remains identical. This abstraction is what makes network science so interdisciplinary.

A network is simply a collection of *nodes* connected by *edges*. Despite this simplicity, it's one of the most powerful abstractions we have for understanding complex systems.


We can represent any network in two equivalent ways. **Schematically**, we draw them as *dots and lines* - nodes connected by edges, as shown in this network diagram:


::: {layout-ncol=2}

![Schematic network](https://memgraph.com/images/blog/graph-algorithms-list/memgraph-graph-algorithms-image14.png)

![A network of penguins in the Kyoto Aquarium.](https://www.kyoto-aquarium.com/sokanzu/assets/img/img_sokanzu_2022.jpg)

:::

While the schematic representation is useful, things can get complicated as soon as the network becomes large. Also, we want to represent data quantitatively to obtain a quantitative understanding of network properties and behaviors.

**Tables** are a natural way to represent networks. The idea is to list the pairs of nodes that are connected by an edge. For example:

| Source | Target |
|--------|--------|
| Node1 | Node2 |
| Node1 | Node3 |
| Node2 | Node3 |
| Node2 | Node4 |
| Node3 | Node5 |

This is called an ***edge table***. Each row represents a connection between two nodes. Once we write down networks in this **tabular format**, we can apply the ***same analytical tools*** regardless of the domain - whether it's routers, people, neurons, or molecules.

## Why networks are hard to understand

For centuries, science has been dominated by reductionist thinking - the belief that we can understand complex systems by breaking them down into their fundamental components. This approach has been extraordinarily successful: we understand chemistry by studying atoms, biology by examining cells, and physics by analyzing particles and forces. From Galileo's mechanical view of the universe to Darwin's focus on individual organisms, scientists have consistently found that understanding the parts leads to understanding the whole.

This reductionist paradigm worked so well because most natural phenomena could indeed be decomposed into independent units. A gas can be understood by studying individual molecules, a machine by examining its components, and even many biological processes by focusing on individual cells or biochemical reactions. The mathematical tools developed over centuries - calculus, differential equations, statistical mechanics - were designed specifically for systems where the behavior of the whole could be predicted from the behavior of the parts.

However, scientists began to realize that not all systems can be decomposed into units that provide sufficient understanding of the system as a whole. Networks represent a fundamental challenge to reductionist thinking because their most important properties emerge from the *interactions* between components, not from the components themselves. You can understand every individual neuron in the brain, but this won't tell you how consciousness emerges. You can analyze every person in a social movement, but this won't predict how ideas spread through the population. You can study every computer on the internet, but this won't explain how global information patterns form.

The difficulty lies not in the individual nodes or edges, but in how they combine to create system-level behaviors that are genuinely novel. Scale overwhelms intuition - while you can mentally track relationships between three people, the same intuition fails completely with three million. Small changes can have massive consequences - removing one connection might fragment an entire network, while removing another has no effect at all. The structural properties that matter most - communities, bottlenecks, influence patterns - are hidden in the data and require sophisticated mathematical analysis to uncover. This is why network science exists as a distinct field: the traditional reductionist toolkit, powerful as it is, simply isn't sufficient for understanding interconnected systems where the connections themselves are the source of complexity.

## Building the right mathematical toolkit

So how do we make sense of complex networks? We need mathematical tools specifically designed for interconnected systems:

**From calculus to graph theory**: Traditional mathematics deals with continuous functions and smooth changes. But networks are discrete - you either have a connection or you don't. This requires *graph theory*, which gives us precise ways to talk about nodes, edges, paths, and connectivity patterns.

**From individual statistics to structural measures**: Traditional statistics studies properties of individual data points. But in networks, the interesting properties are *relational*. How clustered are the connections? How central is a particular node? How long are the shortest paths? These require entirely new kinds of measurements.

**From equilibrium to dynamics**: Much of physics assumes systems reach equilibrium. But networks constantly change - information spreads, opinions influence each other, failures cascade. We need mathematical models that handle these *dynamic processes*.

**From analytical to computational**: Many network problems can't be solved analytically. Finding the most influential nodes in a million-node network requires sophisticated algorithms. This creates a tight coupling between theory and computation.

This toolkit transforms qualitative questions like "How resilient is this system?" into precise, quantitative problems we can solve with algorithms and data.

## Beyond simple connections

Real networks exhibit complex structural properties that affect system behavior:

- **Degree heterogeneity**: Not all nodes are equal. Some become *hubs* with many connections, others remain peripheral. This creates both efficiency and vulnerability.

- **Clustering**: Nodes tend to connect to their neighbors' neighbors, creating local redundancy that affects how information flows through the system.

- **Small-world effects**: Even in large networks, surprisingly short paths connect any two nodes - the "six degrees of separation" is a universal network property.

- **Community structure**: Networks naturally organize into *modules* that are internally well-connected but have fewer connections between them.

## Network effects and emergent phenomena

The most fascinating aspect of networks is how they create system-level behaviors from simple local rules:

- **Cascading failures**: One failure triggers failures in neighbors, which trigger more failures, creating system-wide collapse
- **Collective intelligence**: Distributed systems can solve problems that individual components cannot
- **Resilience**: Redundant connections allow systems to function even when components fail
- **Synchronization**: Components spontaneously coordinate their behavior through network interactions
- **Phase transitions**: Networks can suddenly shift between different states as connections are added or removed

These phenomena emerge from the network structure itself - they are properties of the connections, not the individual nodes.

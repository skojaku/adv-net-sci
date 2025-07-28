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

While the schematic representation is useful, things can get complicated as soon as the network becomes large. Also, we want to represent data quantitatively to perform quantitative understanding of network properties and behaviors.

For analyzing networks, we represent them as **tables** with *source and target* columns. Consider this network:

| Source | Target |
|--------|--------|
| Node1 | Node2 |
| Node1 | Node3 |
| Node2 | Node3 |
| Node2 | Node4 |
| Node3 | Node5 |

This ***edge list*** completely describes the same network structure. Each row represents a connection between two nodes. Once we write down networks in this **tabular format**, we can apply the ***same analytical tools*** regardless of the domain - whether it's routers, people, neurons, or molecules.

**The power of abstraction**: The same tabular representation works for any networked system:

- **Social networks**: People connected by friendships
- **Brain networks**: Neurons connected by synapses
- **The Internet**: Web pages connected by hyperlinks
- **Citation networks**: Papers connected by citations
- **Food webs**: Species connected by predator-prey relationships

Whether your edge list contains "Node1 → Node2" or "Alice → Bob" or "Neuron_A → Neuron_B", the mathematical analysis is identical. This is ***the power of abstraction*** that makes network science versatile and broadly applicable across domains - once we write down any network as a table, we can apply the same analytical tools regardless of what the nodes and edges represent. 🔧

# Why should we care about networks?

System-level behavior emerges from component interactions, but networks take this to another level entirely. The 2003 Northeast blackout started with a single overloaded line in Ohio and cascaded through network connections to affect 55 million people. COVID factory closures created global shortages through supply chain networks. A single tweet can reach millions through social media cascades.

Here's the key insight: in networked systems, *local events can have global consequences*, and *global properties emerge from local interactions*. You can't understand these systems by studying individual components - you need to understand the network structure itself.

## Zoo of networks

Can you find networks around you? Find out what networks are like in nature and society.

[Zoo 🐆🐘🦆 of networks](./zoo-of-networks.md)

## Why networks are hard to understand

If networks are just tables of connections, why do we need sophisticated mathematical tools to understand them? The answer lies in the complexity that emerges from simplicity.

Traditional reductionist thinking works well for systems where you can understand the whole by understanding the parts. But networks break this approach in fundamental ways:

- **Scale overwhelms intuition**: You can mentally track relationships between 3 people. But what about 3 million? At massive scales, simple rules create complex patterns that defy intuition.

- **Small changes, big consequences**: Remove one connection and nothing happens. Remove a different connection and the entire network fragments. This *non-linearity* makes networks unpredictable.

- **Hidden structure**: A table with millions of rows reveals nothing about communities, bottlenecks, or influence patterns. The important structural properties are buried in the data and require sophisticated analysis to uncover.

- **Dynamic evolution**: Networks constantly change - nodes join, leave, reconnect. Understanding these *temporal dynamics* requires mathematical tools that go far beyond static snapshots.

This is why network science exists as a field: traditional mathematical tools aren't sufficient for interconnected systems.

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

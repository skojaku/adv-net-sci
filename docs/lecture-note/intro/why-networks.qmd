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

## Are we done with networks?

If we can represent a network in a table---a familiar data format that can be analyzed by statistical methods, machine learning, and other tools---can we just use these tools to analyze networks? Why do we need to learn network science?

**Long story short, a network is not just a collection of nodes and edges. They work in tandem to create a complex system**. And this view---that a system is not just a collection of parts---represents a critical shift in science.

For centuries, scientists believed in **reductionism**. If you could create modules that function like duck organs and assemble them together, the machine would eventually behave like a duck. Vaucanson's 18th century [Digesting Duck](https://en.wikipedia.org/wiki/Digesting_Duck) seemed to prove this approach worked remarkably well: break down complex systems into fundamental components, understand each part, then reassemble them to understand the whole.

::: {.column-margin}

![Vaucanson's Digesting Duck](https://upload.wikimedia.org/wikipedia/commons/8/8f/Digesting_Duck.jpg)

Find more details in [Wikipedia](https://en.wikipedia.org/wiki/Digesting_Duck)

:::

However, scientists began to realize that not all systems can be decomposed into units that provide sufficient understanding of the system as a whole. Networks represent a fundamental challenge to reductionist thinking because their most important properties emerge from the *interactions* between components, not from the components themselves. You can understand every individual neuron in the brain, but this won't tell you how consciousness emerges. You can analyze every person in a social movement, but this won't predict how ideas spread through the population. You can study every computer on the internet, but this won't explain how global information patterns form.

The difficulty lies not in the individual nodes or edges, but in how they combine to create system-level behaviors that are genuinely novel. Scale overwhelms intuition; while you can mentally track relationships between three people, the same intuition fails completely with three million. Small changes can have massive consequences; removing one connection might fragment an entire network, while removing another has no effect at all. This is why network science exists as a distinct field: the traditional reductionist toolkit simply isn't sufficient for understanding interconnected systems where the connections themselves are the source of complexity!

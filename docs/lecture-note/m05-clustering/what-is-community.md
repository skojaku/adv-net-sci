---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# What is community?

## Birds of a feather flock together

![Birds of a feather](https://t4.ftcdn.net/jpg/08/10/89/17/360_F_810891701_xy4NsqgdqllMfKDfV6V27ycrw8FLFqrw.jpg)

Birds of a feather flock together, and so do many other things.
For instance, we have a group of friends with similar interests who hang out together frequently but may not interact as much with other groups.

In networks, communities are groups of nodes that share similar connection patterns. These communities do not always mean densely-connected nodes. Sometimes, a community can be nodes that are not connected to each other, but connect similarly to other groups. For instance, in a user-movie rating network, a community might be users with similar movie tastes, even if they don't directly connect to each other.

![Community structure in a social network](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Network_Community_Structure.svg/220px-Network_Community_Structure.svg.png)

Communities reflect underlying mechanisms of network formation and underpin the dynamics of information propagation. Examples include:

1. Homophily: The tendency of similar nodes to form connections.
2. Functional groups: Nodes that collaborate for specific purposes.
3. Hierarchical structure: Smaller communities existing within larger ones.
4. Information flow: The patterns of information, influence, or disease propagation through the network.

This is why network scientists are sooo obsessed with community structure in networks. See {cite:p}`fortunato2010community,fortunato2016community,peixoto2019bayesian` for comprehensive reviews on network communities.

## References

```{bibliography}
:style: unsrt
:filter: docname in docnames
```

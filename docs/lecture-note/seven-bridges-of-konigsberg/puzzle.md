---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# A puzzle

In this module, we will learn an historical example that leads to the genesis of graph theory in mathematics and modern network science. Through this example, we will learn:
- How to describe a network using mathematical language
- Path, walks, circuits, cycles, connectedness


Back in 18th century, there was a city called Knigsberg situated on the Pregel River in a historical region of Germany. The city had two large islands connected to each other and the mainland by seven bridges.
During their Sunday walks, the citizens pondered a puzzle:


```{Problem}
How could one walk through the city and cross each bridge exactly once?
```

Leonard Euler worked out the solution to this puzzle in 1736. So let's see what he found out.

![alt text](https://99percentinvisible.org/app/uploads/2022/02/bridges-with-water.png)

Euler's key insight was to simplify the city into *a network of landmasses connected by bridges*, focusing on the connections rather than the geography.
In fact, the landareas, the positions of the islands and the bridges are nothing to do with the puzzle.

![alt text](https://lh3.googleusercontent.com/-CYxppcJBwe4/W2ndkci9bVI/AAAAAAABX-U/K6SNM8gAhg0oNsnWNgQbH3uKNd5Ba10wwCHMYCw/euler-graph-bridges2?imgmax=1600)


## Pen-and-paper worksheet

Let's follow the worksheet to solve the puzzle step by step.

- [Worksheet](http://estebanmoro.org/pdf/netsci_for_kids/the_konisberg_bridges.pdf) {cite:p}`esteban-moro-worksheet`


```{bibliography}
:style: unsrt
```
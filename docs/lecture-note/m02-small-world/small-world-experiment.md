---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .Rmd
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.3
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---


# Small-world experiment

How far are two people in a social network? Milgram and his colleagues conducted a series of expriment to find out in the 1960s.

:::{figure-md} milgram-small-world-experiment

<img src="../figs/milgram-small-world-experiment.png" width="70%">

Milgram's small world experiment.

:::


The experiment went as follows:
1. Milgram first sent out packets to randomly selected people in Omaha, Nebraska, and Wichita, Kansas.
2. The recipient was asked to send the packet to the target person in Boston if they knew them. If not, they were to forward it to someone they knew on a first-name basis who might know the target.
3. The recipient continued to forward the packet to their acquaintances until it reached the target.

The results were surprising: out of the 160 letters sent, 64 successfully reached the target person by the chain of nearly six people, which was later called **six degrees of separation**.
The results imply that, despite the fact that there were hundreds of millions of people in the United States, their social network was significantly compact, with two random people being connected to each other in only a few steps.

:::{tip}
The term "Six degrees of separation" is commonly associated with Milgram's experiment, but Milgram never used it. John Guare coined the term for his 1991 play and movie ["Six Degrees of Separation."](https://en.wikipedia.org/wiki/Six_Degrees_of_Separation_(film))
:::

The results were later confirmed independently.

-  Yahoo research replicate the Milgram's experiment by using emails. Started from more than 24,000 people, only 384 people reached the one of the 18 target person in 13 countries. Among the successful ones, the average length of the chain was about 4. When taken into account the broken chain, the average length was estimated between 5 and 7.{footcite}`goel2009social`

- Researchers in Facebook and University of Milan analyzed the social network n Facebook, which consisted of 721 million active users and 69 billion friendships. The average length of the shortest chain was found to be 4.74. {footcite}`backstrom2012four`

```{footbibliography}
```
---
title: "Appendix"
---

## Derivation of modularity formula

In the main text, we derived the modularity formula as follows:

$$
\begin{align}
Q &=\frac{1}{2m} \sum_{i=1}^n \sum_{j=1}^n A_{ij} \delta(c_i,c_j) - \sum_{c=1}^C \left( \frac{1}{2m}\sum_{i=1}^n k_i \delta(c, c_i) \right)^2
\end{align}
$$

By rearranging the terms, we get the standard expression for modularity as follows:

$$
Q =\frac{1}{2m} \sum_{i=1}^n \sum_{j=1}^n \left[ A_{ij} -  \frac{k_ik_j}{2m} \right]\delta(c_i,c_j)
$$

But are the two forms of modularity the same? Let's see how we can transform one into the other:

We start with our first form of modularity:

$$
Q =\frac{1}{2m} \sum_{i=1}^n \sum_{j=1}^n A_{ij} \delta(c_i,c_j) - \sum_{c=1}^C \left( \frac{1}{2m}\sum_{i=1}^n k_i \delta(c, c_i) \right)^2
$$

First, let's factor out $\frac{1}{2m}$ from both terms:

$$
Q =\frac{1}{2m} \left[ \sum_{i=1}^n \sum_{j=1}^n A_{ij} \delta(c_i,c_j) - \frac{1}{2m}\sum_{c=1}^C \left( \sum_{i=1}^n k_i \delta(c, c_i) \right)^2 \right]
$$

Now, here's a neat trick: $(\sum_i a_i)^2 = (\sum_i a_i)( \sum_j a_j)$. We can use this to expand the squared term:

$$
Q =\frac{1}{2m} \left[ \sum_{i=1}^n \sum_{j=1}^n A_{ij} \delta(c_i,c_j) - \frac{1}{2m}\sum_{c=1}^C \left( \sum_{i=1}^n k_i \delta(c, c_i) \right) \left( \sum_{j=1}^n k_j \delta(c, c_j) \right)\right]
$$

And here is another trick $(\sum_i a_i)( \sum_j a_j) = \sum_i a_i \sum_j a_j = \sum_i \sum_j a_ia_j$

$$
Q =\frac{1}{2m} \left[ \sum_{i=1}^n \sum_{j=1}^n A_{ij} \delta(c_i,c_j) - \frac{1}{2m}\sum_{c=1}^C \left( \sum_{i=1}^n \sum_{j=1}^n k_i k_j  \delta(c, c_i)  \delta(c, c_j) \right)\right]
$$

Here's yet another cool trick, $\delta(c,c_i) \delta(c, c_j) = \delta(c_i,c_j)$. This means we can simplify our expression:

$$
Q =\frac{1}{2m} \left[ \sum_{i=1}^n \sum_{j=1}^n A_{ij} \delta(c_i,c_j) -  \frac{1}{2m} \sum_{i=1}^n \sum_{j=1}^n k_i k_j  \delta(c_i,c_j) \right]
$$

Finally, we can factor out the common parts:

$$
Q =\frac{1}{2m} \sum_{i=1}^n \sum_{j=1}^n \left[ A_{ij} -  \frac{k_ik_j}{2m} \right]\delta(c_i,c_j)
$$
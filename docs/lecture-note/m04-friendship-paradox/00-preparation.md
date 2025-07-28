# Preparation: Statistical Sampling and Probability Prerequisites

## Required Knowledge from Previous Modules

Before studying the friendship paradox, ensure you understand:
- **From M01-M03**: Basic network concepts (degree, adjacency matrix, connectivity)
- **General math**: Basic calculus and linear algebra

## Probability Theory Fundamentals

### Random Variables and Distributions
Understanding of discrete probability distributions:
- **Probability mass function**: $P(X = k)$ for discrete random variable $X$
- **Expected value**: $E[X] = \sum_{k} k \cdot P(X = k)$  
- **Variance**: $\text{Var}(X) = E[X^2] - (E[X])^2$

### Conditional Probability
Essential for understanding biased sampling:
- **Conditional probability**: $P(A|B) = \frac{P(A \cap B)}{P(B)}$
- **Law of total expectation**: $E[X] = E[E[X|Y]]$

## Sampling Theory

### Population vs. Sample
- **Population parameters**: True values in the complete dataset
- **Sample statistics**: Measured values from a subset
- **Sampling bias**: When sample doesn't represent population

### Types of Sampling
- **Simple random sampling**: Each individual has equal probability of selection
- **Weighted sampling**: Selection probability proportional to some attribute
- **Size-biased sampling**: Larger items more likely to be selected

### Jensen's Inequality
For convex functions and random variables:
$$E[f(X)] \geq f(E[X])$$

This inequality is fundamental to understanding why averages of friends differ from friends of averages.

## Mathematical Prerequisites

### Basic Statistical Moments
- **First moment**: Mean $\mu = E[X]$
- **Second moment**: $E[X^2]$  
- **Relationship**: $E[X^2] \geq (E[X])^2$ with equality only when $X$ is constant

### Linear Algebra Basics
- **Matrix operations**: For adjacency matrix manipulations
- **Vector operations**: For degree calculations

## Applications Context

### Survey Methodology
Understanding how data collection methods can introduce bias:
- **Response bias**: Who is more likely to participate in surveys
- **Selection effects**: How sampling frames affect results

### Network Effects in Epidemiology
Basic concepts about disease spread:
- **Contact networks**: How diseases spread through social connections
- **Vaccination strategies**: Targeting high-contact individuals

These mathematical foundations will help you understand the counterintuitive but mathematically precise friendship paradox phenomenon.
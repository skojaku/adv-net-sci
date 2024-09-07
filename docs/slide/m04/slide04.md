---
marp: true
theme: default
paginate: true
---

Check list
- [ ] Microphone turned on
- [ ] Zoom room open
- [ ] Recording on
- [ ] Mouse cursor visible
- [ ] Sound Volume on


---

# Advanced Topics in Network Science

Lecture 04: Friendship Paradox
Sadamori Kojaku

---

![bg right:100% width:70%](../enginet-intro-slide/enginet-01.png)

---

![bg right:100% width:70%](../enginet-intro-slide/enginet-02.png)

---

![bg right:100% width:70%](../enginet-intro-slide/enginet-03.png)

---

![bg right:100% width:70%](../enginet-intro-slide/enginet-04v2.png)


---

# Module 4: Friendship Paradox 🤝

## Learning Objectives

- 📚 Understand the friendship paradox
- 🔍 Explore its importance and consequences
- 📊 How to plot degree distribution? (not as easy as it seems!)
  - Histogram
  - CDF
  - CCDF
  - Log-log plot
- 🧠 Excess degree distribution

---

# In-class Experiment 🔬

1. 📇 Receive a card with a unique letter
2. 🤝 Meet & greet: exchange cards with at least one friend (5 mins)
3. 🧮 Count received cards, write number, return cards (2 mins)
4. 📈 Calculate average 'friend count' of your friends (

![bg right:40% width:100%](https://www.quantamagazine.org/wp-content/uploads/2018/08/Fat-Tail_Network_2880x1620.jpg)


---

# What is the average number of friends that...

- ...you have?
- ...your friends have?

![bg right:40% width:100%](https://www.quantamagazine.org/wp-content/uploads/2018/08/Fat-Tail_Network_2880x1620.jpg)


---

# Friendship Paradox

## Your friends have more friends than you, on average

---
# Friendship Paradox Explained 🤔

- 📊 It's about measurement, not friendship formation!
- Average # of friends of you = Average over nodes
- Average # of friends of your friends = Average over edges

![bg right:40% width:90%](../../lecture-note/figs/nodes-vs-edges.jpg)

---

# Let's put on our mathematician hat 🎓

- Let $P_0(k)$ be the probability of a node having degree $k$
- Let $P_1(k)$ be the probability of a friend having degree $k$
- How does $P_1(k)$ look like?
- Hint:
  - Nodes with $k$ edges appear $k$ times more likely as a friend of someone than a person with $1$ edge. Thus, $P_1(k) \propto \; ????$. To get the actual distribution, you will need $\langle k \rangle = \sum_{k} k P_0(k)$
- Compute the average degree of friends over edges

---

# Degree distribution of friends

- $P_1(k) = \frac{k}{\langle k \rangle} P_0(k)$

- Average degree of friends
  - $\langle k_f \rangle = \sum_{k} k P_1(k) = \sum_{k} \frac{k^2}{\langle k \rangle} P_0(k) = \frac{\langle k^2 \rangle}{\langle k \rangle}$
---

# How is it useful?

## The Challenge
- 🦠 Control virus spread through strategic vaccination
- 🎯 Utilize the friendship paradox for effective strategies

## The Game
- 🎮 Play the [Vaccination Game](BASE_URL/vis/vaccination-game.html)
- 💉 Vaccinate strategically to halt virus spread
- 🧠 Think about how the friendship paradox influences your strategy

---

# Degree is crucial for network science!

- Network Robustness
- Epidemic Spreading and Controlling
- Community Detection
- ...

Understanding degree distribution is crucial for network analysis. But how do we plot it? 🤔 (it's not as easy as it seems!)

![bg right:50% width:100%](https://barabasi.com/img/6/159.png)

---

# It's not as easy as it seems!


![bg right:65% width:100%](https://hongtaoh.com/en/blog/2020-08-19-igraph-distribution_files/figure-html/unnamed-chunk-16-1.png)


---

# Exercise: Basic visualization techniques

- [TODO] Past link

---

# Data Visualization: CDF and CCDF 📉

## Definitions
- CDF: $F(x) = P(X \leq x)$
- CCDF: $\bar{F}(x) = P(X > x) = 1 - F(x)$

![bg right:60% width:90%](https://nap.nationalacademies.org/openbook/0309054915/xhtml/images/img00034.jpg)

---

# Visualization of Degree Distribution: Hands-on 🧠

1. Create Barabási-Albert network
3. Compute degree of each node
4. Calculate degree distribution

## Visualization
- Use log-log plots
- CCDF for clearer tail visualization

---

# CCDF in Log-Log Plot 📉

## Interpretation
- Slope indicates heterogeneity
- Steep slope: more homogeneous
- Flat slope: more heterogeneous

## Power-Law Relation
$\log [\text{CCDF}(d)] = (-\gamma + 1) \cdot \log d + \text{const.}$

---

# Excess Degree Distribution 🔍

## Definition
$q(d) = \frac{d + 1}{\langle d \rangle} p(d+1)$

## Interpretation
- Represents additional connections of a randomly chosen friend
- Excludes the link to the focal node

## Comparison
- Degree distribution of a node vs its friend
- Demonstrates the friendship paradox mathematically

---

# Key Takeaways 🗝️

- 🤝 Friendship paradox is universal in social networks
- 📊 Proper data visualization is crucial for understanding
- 🧮 Degree distributions provide insights into network structure
- 💉 Practical applications include disease control strategies
- 🧠 Critical thinking about network structures and their implications
---
title: "M01: Introduction & Seven Bridges of Königsberg"
author: "Sadamori Kojaku"
format:
  revealjs:
    slide-number: true
    chalkboard:
      buttons: false
    preview-links: auto
    theme: simple
    css: css/style.css
---

# Check list

- [ ] Microphone turned on
- [ ] Zoom room open
- [ ] MyBinder launched
- [ ] Sound Volume on

# Introduction
:::: {.columns}

::: {.column width="50%"}
Advanced Topics in Network Science

Sadamori Kojaku

skojaku@binghamton.edu

:::

::: {.column width="50%"}

![](https://newmedialab.cuny.edu/wp-content/uploads/2014/01/Internet.gif)

:::

::::



## Enginet

![](../enginet-intro-slide/enginet-01.png)

## Enginet

![](../enginet-intro-slide/enginet-02.png)

## Enginet

![](../enginet-intro-slide/enginet-03.png)

## Course Overview

- **Instructor:** Sadamori Kojaku (幸若完壮)
- **Email:** skojaku@binghamton.edu
- **Office Hours:** Monday 10:00-14:00
- **Course Website:** [https://skojaku.github.io/adv-net-sci](https://skojaku.github.io/adv-net-sci)


## Let's start with a story... 🦠

::: {.callout-note title = "Question:"}

2009: H1N1 pandemic spreads globally

Do you remember which countries were infected first and second?

:::

Think about it... discuss with your neighbor for 30 seconds

::: {.incremental}

- **Your predictions:**

  - Geographic distance matters?
  - Nearby countries first?
  - Then spreading outward in circles?

- *Let's hear some thoughts...*

:::

## Answer

::: {.callout-tip title = "Answer:"}

- First: United States

- Second: **Spain**

:::

## Here's what actually happened...

<img src="https://www.science.org/cms/10.1126/science.1245200/asset/59290a15-76de-4a0f-9107-259201f98bcf/assets/graphic/342_1337_f1.jpeg" style="width: 100%; max-width: none; margin-bottom: 20px;">

**Question:** What do you notice? Does this match your prediction?

---

**Key insight:** Network structure (air travel) determined spread, not geography!

<img src="https://www.science.org/cms/10.1126/science.1245200/asset/66d5a7ec-a683-4135-af2f-149c91007e48/assets/graphic/342_1337_f2.jpeg" style="width: 100%; max-width: none; margin-bottom: 20px;">


## Quick Exercise: Spot the Networks! 👀

::: {.callout-note title = "Challenge:"}
**Look around you right now...**

What networks do you interact with daily?

*Take 1 minute - list as many networks as you can*
:::

## Let's Share! 🗣️

**What did you come up with?**

*I'll collect a few examples from the class...*

## Here Are Some You Might Have Missed:

:::: {.columns}

::: {.column width="50%"}

**Plant-Pollinator Networks** 🌼

![](../lecture-note/m01-euler_tour/tikz-tex/a108d4489f34112ee70fef7ca6f1554f2e57d915/a108d4489f34112ee70fef7ca6f1554f2e57d915.svg){width=100% fig-align="center"}

**Question:** How is this a network? What are the connections?

:::

::: {.column width="50%"}

**Your Brain Right Now!** 🧠

![](../lecture-note/m01-euler_tour/tikz-tex/6a788908a035eb1698d3687e22ba1d7ba1f09473/6a788908a035eb1698d3687e22ba1d7ba1f09473.svg){width=100% fig-align="center"}

*As you're listening, billions of neurons are connecting...*

:::

::::

## Social Networks (Obviously!) 📱

:::: {.columns}

::: {.column width="50%"}

![](../lecture-note/m01-euler_tour/tikz-tex/75f54874400531f4c141183cee9db4c3f565b7e8/75f54874400531f4c141183cee9db4c3f565b7e8.svg){width=100% fig-align="center"}

:::

::: {.column width="50%"}

::: {.callout-note title = "Question:"}
**How do ideas spread through social networks?**

Same as diseases? Different?
:::

*Turn to your neighbor - what do you think?*

:::

::::

## How Did You Get to Class Today? 🚗

![](../lecture-note/m01-euler_tour/tikz-tex/28526e308c66f1bd530d20eb6e1c8fe995d4fada/28526e308c66f1bd530d20eb6e1c8fe995d4fada.svg){width=80% fig-align="center"}

**Transportation networks shape our daily choices!**

## Wait - Isn't This Just Graph Theory? 🤔

::: {.callout-note title = "Question:"}
**Who has taken a math course with graphs before?**

*Raise your hands... what did you study?*
:::

## Traditional Graph Theory 📐

:::: {.columns}

::: {.column width="50%"}

![](../lecture-note/m01-euler_tour/tikz-tex/d9f4eadf2f331510ed85e73fc38e092c54e7c85f/d9f4eadf2f331510ed85e73fc38e092c54e7c85f.svg){width=100% fig-align="center"}

:::

::: {.column width="50%"}

::: {.callout-note title = "Question:"}
**What do you notice about this pattern?**

*Perfect, regular, predictable...*
:::

:::

::::

## Real-World Networks Look Like This:

:::: {.columns}

::: {.column width="60%"}

![](../lecture-note/m01-euler_tour/tikz-tex/78b7681da140ca96461631cf5a72d03a36c3d906/78b7681da140ca96461631cf5a72d03a36c3d906.svg){width=100% fig-align="center"}

:::

::: {.column width="40%"}

::: {.callout-note title = "Question:"}
**What's different here?**

Why does this "messiness" matter?
:::

*Discuss with your neighbor - what makes real networks "messy"?*

:::

::::

## Thought Experiment 🤔

:::: {.columns}

::: {.column width="70%"}

::: {.callout-note title = "Question:"}
**Imagine you're an Alien scientist (like von Neumann!) studying humans...**

You understand every single neuron in the human brain perfectly.

**Can you predict what a human will say next? What they'll dream about?**
:::

*What do you think? Turn to your neighbor and discuss...*

:::

::: {.column width="30%"}

![](https://upload.wikimedia.org/wikipedia/commons/5/5e/JohnvonNeumann-LosAlamos.gif){width=50% fig-align="center"}

:::

::::

## The Reductionist Approach 🧩

:::: {.columns}

::: {.column width="40%"}

::: {.callout-note title = "Method:"}
*Break it down → Understand parts → Reassemble*
:::

**When does this work well?**

*Give me an example...*

:::

::: {.column width="60%"}

![](../lecture-note/m01-euler_tour/tikz-tex/stick-figure/stick-figure.svg){width=80% fig-align="center"}

:::

::::

## But Sometimes... 🌐

:::: {.columns}

::: {.column width="50%"}

::: {.callout-tip title = "Network Science:"}
*The whole > sum of parts*
:::

::: {.callout-note title = "Question:"}
**Why can't we predict consciousness from individual neurons?**

*What's missing in the reductionist approach?*
:::

:::

::: {.column width="50%"}

![](../lecture-note/m01-euler_tour/tikz-tex/6a788908a035eb1698d3687e22ba1d7ba1f09473/6a788908a035eb1698d3687e22ba1d7ba1f09473.svg){width=100% fig-align="center"}

:::

::::



## Course Objectives

:::: {.columns}

::: {.column width="40%"}

We will:

- 🔍 Analyze networks
- 🧠 Learn key concepts
- 🤖 Apply AI to networks

:::


::: {.column width="60%"}

After this course, you'll be able to:

- 📖 Understand network science papers
- 🛠️ Do advanced network analysis
- 📝 Design network research
- 🔗 Connect Systems Science and networks

:::

::::

---


:::: {.columns}

::: {.column width="50%"}

### Core Learning Philosophy

- Learning by doing


- *Doing it wrong, and learning from it!*

- There are many traps to make you fail!
(not in the sense of failing the course)


:::

::: {.column width="50%"}

![](https://media1.tenor.com/m/-LDi5jsgk_8AAAAd/bruce-lee-dont-think.gif){width=70% fig-align="center" style="display:block; margin-left:auto; margin-right:auto;"}

![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_NZxWrYf1VvFyG5we1DtkTZOkbsVkbUFtAg&s){width=80% fig-align="center"}

:::

::::


## Trap \#1

:::: {.columns}

::: {.column width="60%"}

**Pen & Paper Exercise**

All modules start with an in-class pen & paper exercise.

- Bring your pen to class
- You solve it by yourself
- Then, discuss with your mates

:::

::: {.column width="40%"}

![](https://static1.xdaimages.com/wordpress/wp-content/uploads/wm/2024/09/why-i-use-pen-and-paper-with-note-taking-apps.jpg)

:::

::::

## Trap \#2

:::: {.columns}

::: {.column width="60%"}

**Interactive Visualization**

Most modules have an interactive game to play

- Wining the game requires Network Science knowledge
- You don't have the knowledge initially but play the game
- You will learn Network Science by learning how to win the game

:::

::: {.column width="40%"}

Link: [Vaccination Game](https://skojaku.github.io/adv-net-sci/assets/vis/vaccination-game.html)

<iframe src="https://skojaku.github.io/adv-net-sci/assets/vis/vaccination-game.html" width="100%" height="500" frameborder="0"></iframe>

:::

::::

## Trap \#3

**Weekly Quiz**

Every class begins with a weekly quiz to review the previous week's topics.

- Written quiz
- Only few questions
- Graded and reviewed during the class
- You can resubmit the quiz (one time)
- (Enginet students will submit via Brightspace)

::::

## Trap \#4

:::: {.columns}

::: {.column width="60%"}

**Assignment**

- Most modules have coding assignments

- Distributed via GitHub Classroom

- Unlimited attempts until deadline

- Autograded


:::

::: {.column width="40%"}



<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vTDkP2xHhQHiAYDwy6k1KJ2HuQ6JoanN91Atdp9Wbfq8_1zvX2VKOx07xvLru4HvekNEzYC_WoUINRy/pubembed?start=false&loop=false&delayms=3000" frameborder="0" width="480" height="299" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>

We'll cover assignment submission in class. Find the detailed instruction on the lecture note.
:::

::::

## Trap \#5

::: {.columns}

::: {.column width="40%"}

**LLM Dojo**


- You'll create challenging questions for LLMs.

- You'll win if you can create one that stumps LLMs.

- Every module has a LLM Dojo exercise

- Collected & Graded on GitHub

:::

::: {.column width="60%"}

You'll create a quiz & answer for LLMs.

```toml
[[questions]]
question = """
    When is the global clustering not a
    good representation of the network?
    """
answer = """
    When the network is degree
    heterogeneous. This is because
    a single hub can create
    substantially many triangles
    in the network, not
    representing the number of
    triangles typical nodes
    in the network form.
    """
```

:::

::::

## Trap \#6

**Network of the Week**

- You'll pick a paper on network science of your interest

- You'll present the paper in the class
  - roughly 10 minutes
  - 5 mins for Q&A

- The instructor can help you find a paper

## Grading items

- Quiz (10%)
- Network of the Week Presentation (10%)
- Assignments (20%)
- Exam (30%)
- Project (30%)

::: {.incremental}
- ✨ Bonus (30%)
  - 10% bonus for the best project (one team)
  - 10% for the excellent Network of the Week Presentation
  - 10% bonus for excellent question-answer assignment
:::

## Exam

- **Final exam on all topics**
- During exam week (Dec 8-12)
- All multiple choice questions
- Take home exam
- Brightspace will be used for submission

## Final Project 🎓

- Individual project (30% of grade) 📊
- Timeline 📅
  - Proposal: Sept 30; Paper: Dec 5; Presentations: Dec 9

- Requirements 📋
  - About Network Science
  - Develop a new method, new visualization, literature review, case study, etc.

## Example Project 01

Analysing the network of scientific topics

![](sci-topic-net.png)


## Example Project 02

Correlation between the neural activities of the brain

![](ecog.png)

## Example Project 03

Tesla Supercharger Network

![](super-charger.png)

# Lecture note

- 📚 [Online Lecture Note](https://skojaku.github.io/adv-net-sci)
- See [The course GitHub repo](https://github.com/skojaku/adv-net-sci/) for details

## AI Tutor 🤖

:::: {.columns}

::: {.column width="50%"}


![](minidora.png)

**Minidora**, an AI tutor for this course available 24/7 through Discord


:::

::: {.column width="50%"}

- You can chat, ask questions, and take quizzes with Minidora.
- Sign up for the course on Discord to get access
- Demo: `/ask What is an Euler tour?`

:::

::::

## Policy

- 📚 3-credit course: 6.5+ hours of work/week outside class
- 🤖 AI tools allowed for learning, but cite if used in assignments
- 💾 Back up all data and code (loss not an excuse for late work)
- ♿ Accommodations available for students with disabilities
- 🚫 Zero tolerance for academic dishonesty

# Questions?

## Module 01: Königsberg Bridge Puzzle

:::: {.columns}

::: {.column width="50%"}
**Advanced Topics in Network Science**

Sadamori Kojaku

:::

::: {.column width="50%"}

![](https://newmedialab.cuny.edu/wp-content/uploads/2014/01/Internet.gif)

:::

::::


# The Königsberg Bridge Puzzle 🌉

![](https://99percentinvisible.org/app/uploads/2022/02/bridges-with-water.png)

- 18th century puzzle in Königsberg, Prussia (now Kaliningrad, Russia) 🇩🇪
- City had 7 bridges connecting 2 islands and mainland 🏙️
- **Challenge**: Find a route that crosses each bridge exactly once and returns to start 🚶‍♂️

##

## Your turn! 🧩

:::: {.columns}

::: {.column width="60%"}

::: {.callout-note title = "Challenge:"}
**Find a route that crosses each bridge exactly once and returns to start**

How would YOU approach this?
:::

*Take 30 seconds - think about your strategy*

::: {.incremental}
- **Your approaches:**
  - Trial and error?
  - Start from a specific place?
  - Look for patterns?
  - Something mathematical?
- *Let's hear 2-3 different strategies...*
:::

:::

::: {.column width="40%"}
![](https://99percentinvisible.org/app/uploads/2022/02/bridges-with-water.png){width=100% fig-align="center"}
:::

::::

##

## Euler's Revolutionary Approach 🧠

:::: {.columns}

::: {.column width="50%"}

::: {.callout-note title = "Question:"}
**What if we ignore all the physical details?**

What do you see in this transformation?
:::

*Turn to your neighbor - what's the key insight?*

:::

::: {.column width="50%"}
![](../lecture-note/m01-euler_tour/tikz-tex/c39860e7fa7562ba1d021b22b78e66cba5a9f51d/c39860e7fa7562ba1d021b22b78e66cba5a9f51d.svg){width=100% fig-align="center"}
:::

::::

## The Breakthrough Insight ✨

::: {.callout-tip title = "Answer:"}
**Euler realized:** Only connections matter, not physical details!

- Landmasses → **dots** (nodes)
- Bridges → **lines** (edges)
:::

**Why is this abstraction so powerful?**

*This was the birth of graph theory and network science!*

##

# Pen and Paper Exercise 📝

- Let's work on a pen-and-paper [exercise](http://estebanmoro.org/pdf/netsci_for_kids/the_konisberg_bridges.pdf) 📄
- Let's form a group of 3-4 people and discuss the solution together.

**Try to discover Euler's insights yourself first!**

##

## Euler's Degree-Based Reasoning 🧮

:::: {.columns}

::: {.column width="60%"}

::: {.callout-note title = "Question:"}
**Count with me:** How many bridges connect to each landmass?

*Point to each area - let's count together...*
:::

::: {.incremental}
- A: **3** bridges
- B: **5** bridges
- C: **3** bridges
- D: **3** bridges
- *What do you notice about these numbers?*
:::

:::

::: {.column width="40%"}
![](../lecture-note/figs/labeled-koningsberg.jpg){width=100% fig-align="center"}
:::

::::

## The Walking Logic 🚶‍♂️

:::: {.columns}

::: {.column width="70%"}

::: {.callout-note title = "Think About It:"}
**If you walk through a node, what happens?**

You enter on one edge, leave on another...
:::

::: {.incremental}
- **Even number of edges**: Enter/leave perfectly ✅
- **Odd number**: One edge "left over" ❌
- **Question:** Where can those "leftover" edges be?
- *Only at start/end points!*
:::

:::

::: {.column width="30%"}
![](../lecture-note/m01-euler_tour/tikz-tex/097b29e3d4bb2e92f6dc166bd54c00e7491be467/097b29e3d4bb2e92f6dc166bd54c00e7491be467.svg){width=100% fig-align="center"}
:::

::::

##

## The Moment of Truth 🏆

::: {.callout-note title = "Question:"}
**We found that Königsberg has 4 odd-degree nodes...**

But Euler's theorem says:
- **0 odd nodes** → Euler circuit possible ✅
- **2 odd nodes** → Euler path possible ✅
- **More than 2** → ?

**What does this mean for Königsberg?**
:::

*What's your verdict?*

## Euler's Path Theorem 🏆

::: {.callout-tip title = "Answer:"}
**An Euler path/circuit exists if and only if:**

1. **Graph is connected**, **AND**
2. **Either:**
   - All nodes have even degree (**Euler circuit**)
   - Exactly two nodes have odd degree (**Euler path**)

**Königsberg verdict**: 4 odd-degree nodes → **IMPOSSIBLE!** 🙅‍♂️
:::

**How do you think the townspeople reacted to this news?**

##

## Network Terminology 📚

::: {.callout-note title = "Question:"}
**What's the difference between these terms?**

Which one did Königsberg citizens actually want?
:::

::: {.incremental}
- **Walk**: Any sequence of connected nodes (can repeat)
- **Trail**: Walk without repeating edges (Euler trail) ← *This is key!*
- **Path**: Walk without repeating nodes
- **Circuit**: Closed trail (starts/ends at same node)
- **Cycle**: Closed path
:::

::: {.callout-tip title = "Answer:"}
**Königsberg sought an Euler circuit!**

A closed trail that uses every edge exactly once.
:::

##

## Tragic Irony: The Bridges' Fate 🏙️💣

:::: {.columns}

::: {.column width="60%"}

::: {.callout-note title = "Historical Twist:"}
**During WWII, Allied forces bombarded Königsberg**

Two of the seven bridges were destroyed 💥
:::

::: {.incremental}
- **The irony**: This destruction finally made an Euler path possible! ✅
- **The city**: Renamed Kaliningrad, now Russian territory 🇷🇺
- **The math**: Sometimes tragedy solves puzzles 😢
:::

**What does this teach us about real-world networks?**

:::

::: {.column width="40%"}
![After WWII bombing - bridges destroyed](../lecture-note/figs/seven-bridge-bombared.png){width=100% fig-align="center"}
:::

::::

##

## 💻 Coding Time: Networks in Code! 🌐

::: {.callout-note title = "Next Steps:"}
[Let's represent networks with Python!](https://skojaku.github.io/adv-net-sci/m01-euler_tour/how-to-code-network.html) 🐍

We'll learn how computers store and analyze networks
:::

## Key Takeaways 🎯

::: {.incremental}
- **Mathematical abstraction**: Focus on structure, not physical details
- **Euler's theorem**: Degree constraints determine network traversability
- **Network terminology**: Walks, trails, paths, circuits, and cycles
- **Historical impact**: From recreational puzzle to foundation of network science
- **Modern relevance**: GPS navigation, internet routing, social networks
:::

##

# Any questions?
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

# Introduction & Seven Bridges of Königsberg
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

2009: H1N1 pandemic spreads globally

**Question for you:** If a disease starts in Mexico, which countries do you think would be infected first?

*Think about it... discuss with your neighbor for 30 seconds*

## What would you expect?

**Your predictions:**
- Geographic distance matters?
- Nearby countries first?
- Then spreading outward in circles?

*Let's hear some thoughts...*

## Here's what actually happened...

<img src="https://www.science.org/cms/10.1126/science.1245200/asset/59290a15-76de-4a0f-9107-259201f98bcf/assets/graphic/342_1337_f1.jpeg" style="width: 100%; max-width: none; margin-bottom: 20px;">

**Question:** What do you notice? Does this match your prediction?

## The real pattern was this:

<img src="https://www.science.org/cms/10.1126/science.1245200/asset/66d5a7ec-a683-4135-af2f-149c91007e48/assets/graphic/342_1337_f2.jpeg" style="width: 100%; max-width: none; margin-bottom: 20px;">

**Key insight:** Network structure (air travel) determined spread, not geography!

##

## Quick exercise: Spot the networks! 👀

**Look around you right now...**

What networks do you interact with daily?

*Take 1 minute - list 3 networks you used today*

## Let's share!

**What did you come up with?**

*I'll collect a few examples from the class...*

## Here are some you might have missed:

<img src="../lecture-note/m01-euler_tour/tikz-tex/a108d4489f34112ee70fef7ca6f1554f2e57d915/a108d4489f34112ee70fef7ca6f1554f2e57d915.svg" style="width: 100%; max-width: none; margin-bottom: 20px;">

**Question:** How is this a network? What are the connections?

## Your brain right now!

<img src="../lecture-note/m01-euler_tour/tikz-tex/6a788908a035eb1698d3687e22ba1d7ba1f09473/6a788908a035eb1698d3687e22ba1d7ba1f09473.svg" style="width: 80%; max-width: none; margin-bottom: 20px;">

**As you're listening to me, billions of neurons are connecting...**

## Social networks (obviously!)

<img src="../lecture-note/m01-euler_tour/tikz-tex/75f54874400531f4c141183cee9db4c3f565b7e8/75f54874400531f4c141183cee9db4c3f565b7e8.svg" style="width: 100%; max-width: none; margin-bottom: 20px;">

**Question:** How do ideas spread through social networks? Same as diseases?

## How did you get to class today?

<img src="../lecture-note/m01-euler_tour/tikz-tex/28526e308c66f1bd530d20eb6e1c8fe995d4fada/28526e308c66f1bd530d20eb6e1c8fe995d4fada.svg" style="width: 100%; max-width: none; margin-bottom: 20px;">

**Transportation networks shape our daily choices!**

##


## Wait - isn't this just graph theory? 🤔

**Question for the class:** Who has taken a math course with graphs before?

*Raise your hands... what did you study?*

## Traditional Graph Theory

<img src="../lecture-note/m01-euler_tour/tikz-tex/d9f4eadf2f331510ed85e73fc38e092c54e7c85f/d9f4eadf2f331510ed85e73fc38e092c54e7c85f.svg" style="width: 80%; max-width: none; margin-bottom: 20px;">

**What do you notice about this pattern?**

*Perfect, regular, predictable...*

## Real-world networks look like this:

<img src="../lecture-note/m01-euler_tour/tikz-tex/78b7681da140ca96461631cf5a72d03a36c3d906/78b7681da140ca96461631cf5a72d03a36c3d906.svg" style="width: 80%; max-width: none; margin-bottom: 20px;">

**Question:** What's different here? Why does this matter?

*Discuss with your neighbor - what makes real networks "messy"?*

##

## Thought experiment 🤔

**Imagine you're a Martian scientist studying humans...**

You understand every single neuron in the human brain perfectly.

**Question:** Can you predict what a human will say next? What they'll dream about?

*What do you think? Turn to your neighbor and discuss...*

## The reductionist approach

<img src="../lecture-note/m01-euler_tour/tikz-tex/stick-figure/stick-figure.svg" style="width: 60%; max-width: none; margin-bottom: 20px;">

*Break it down → Understand parts → Reassemble*

**Question:** When does this work well? Give me an example...

## But sometimes...

<img src="../lecture-note/m01-euler_tour/tikz-tex/6a788908a035eb1698d3687e22ba1d7ba1f09473/6a788908a035eb1698d3687e22ba1d7ba1f09473.svg" style="width: 80%; max-width: none; margin-bottom: 20px;">

*The whole > sum of parts*

**Question:** Why can't we predict consciousness from individual neurons?

*What's missing in the reductionist approach?*

##

# Course Objectives

We will:
- 📊 Analyze networks
- 🧠 Learn key concepts
- 🤖 Apply AI to networks

After this course, you'll be able to:
- 📚 Understand network science papers
- 💻 Do advanced network analysis
- 🔬 Design network research
- 🔗 Connect Systems Science and networks


##

# Philosophy of Learning in this course

[![bg right:50% width:90% Drive: The surprising truth about what motivates us](https://img.youtube.com/vi/RQaW2bFieo8/0.jpg)](https://www.youtube.com/watch?v=RQaW2bFieo8 "Drive: The surprising truth about what motivates us")
https://www.youtube.com/watch?v=RQaW2bFieo8

##

![bg width:80% right:100%](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_NZxWrYf1VvFyG5we1DtkTZOkbsVkbUFtAg&s)

##

# Course Structure

"Don't think! Feeeeeel" - Bruce Lee

- 🎓 Lectures
- 🛠️ Hands-on exercises
- 📝 Weekly quizzes
- 💻 Biweekly coding assignments
- 🎓 Final project
- 📝 Exam

![bg right:50% width:80%](https://media1.tenor.com/m/-LDi5jsgk_8AAAAd/bruce-lee-dont-think.gif)


##

# Final Project 🎓

- Individual project (30% of grade) 📊
- Timeline 📅
  - Proposal: Sept 29; Paper: Dec 4; Presentations: Dec 8

- Requirements 📋
  - Apply concepts to real problem 🌍
  - Analyze network dataset 🔬
  - Show course integration 🧠
  - Clear presentation 🗣️

##

# Example Project 01

![](sci-topic-net.png)

##

# Example Project 02

![width:100%](ecog.png)

##

# Example Project 03

Tesla Supercharger Network

![bg right:50% width:90%](super-charger.png)


## Exam

- 📚 **(Final exam on all topics (weight: 30%)**
- 📅 During exam week (Dec 9-13)
- 📝 Theory + practical problems
- 🌍 Apply concepts to real scenarios
- 📚 Review sessions before exam


##

# Weekly Quiz on Brightspace

- 📊 Quizzes: A tool to identify misconceptions (weight: 20%)
- 🧠 Covers previous week's topics
- 🏁 Deadline: before final exam
- 🔄 Unlimited attempts until correct

##

# Assignment

- 📅 Roughly bi-weekly (weight: 20%)
- 💻 Coding exercises
- 🤖 Autograded assignments
- 🏁 Deadline: before final exam
- 🔄 Unlimited attempts until correct

##

# Lecture note

- 📚 [Interactive Jupyter book](https://skojaku.github.io/adv-net-sci)
- 💻 Run code directly on the page
  - ⏳ First-time loading may take 2-3 mins
- 🔄 Or download as Jupyter notebook
  - ☁️ Use on cloud (Google Colab, Kaggle) or locally
  - 📦 Install packages from `environment.yml` for local use
  - See [The course GitHub repo](https://github.com/skojaku/adv-net-sci/) for details

##

# Meet Minidora - Your AI Tutor 🤖

- 🎓 **Personal AI tutor** available 24/7 through Discord
- 💬 **Ask questions**: `/ask What is an Euler tour? m01`
- 🗣️ **Chat naturally**: `/chat I'm confused about networks`
- 📝 **Take quizzes**: `/quiz m01 multiple-choice`
- 📊 **Track progress**: `/status summary`

**Get help mastering network science concepts anytime!**

##

# Policy

- 📚 3-credit course: 6.5+ hours of work/week outside class
- 🤖 AI tools allowed for learning, but cite if used in assignments
- 💾 Back up all data and code (loss not an excuse for late work)
- ♿ Accommodations available for students with disabilities
- 🚫 Zero tolerance for academic dishonesty


##

# Questions?

##

# Before we start
What motivates you to take this course (if you want to)?

[![Drive: The surprising truth about what motivates us](https://img.youtube.com/vi/u6XAPnuFjJc/0.jpg)](https://www.youtube.com/watch?v=u6XAPnuFjJc "Drive: The surprising truth about what motivates us")
https://www.youtube.com/watch?v=u6XAPnuFjJc

~8:23

##

# M01: Seven Bridges of Königsberg

![bg right:50% width:90% Königsberg Bridges](https://99percentinvisible.org/app/uploads/2022/02/bridges-with-water.png)

##

# The Königsberg Bridge Puzzle 🌉

![bg right:50% width:90% Königsberg Bridges](https://99percentinvisible.org/app/uploads/2022/02/bridges-with-water.png)

- 18th century puzzle in Königsberg, Prussia (now Kaliningrad, Russia) 🇩🇪
- City had 7 bridges connecting 2 islands and mainland 🏙️
- **Challenge**: Find a route that crosses each bridge exactly once and returns to start 🚶‍♂️

##

## Your turn! 🧩

**Challenge:** Find a route that crosses each bridge exactly once and returns to start

![bg right:60% width:90%](https://physics.weber.edu/carroll/honors_images/bridges_of_konigsberg.jpg)

**Before we dive in:** How would YOU approach this?

*Take 30 seconds - what's your strategy?*

## Let's hear your approaches!

**What strategies did you come up with?**

*I want to hear 2-3 different approaches...*

- Trial and error?
- Start from a specific place?
- Look for patterns?
- Something else?

##

## Here's what Euler did differently...

**Question:** What if we ignore all the physical details?

<img src="../lecture-note/m01-euler_tour/tikz-tex/c39860e7fa7562ba1d021b22b78e66cba5a9f51d/c39860e7fa7562ba1d021b22b78e66cba5a9f51d.svg" style="width: 90%; max-width: none; margin-bottom: 20px;">

**What do you see here? What did Euler focus on?**

*Turn to your neighbor - what's the key insight?*

## The breakthrough insight

**Euler realized:** Only connections matter, not physical details!

- Landmasses → **dots** (nodes)
- Bridges → **lines** (edges)

**Question:** Why is this abstraction so powerful?

*This was the birth of graph theory and network science!*

##

# Pen and Paper Exercise 📝

- Let's work on a pen-and-paper [exercise](http://estebanmoro.org/pdf/netsci_for_kids/the_konisberg_bridges.pdf) 📄
- Let's form a group of 3-4 people and discuss the solution together.

**Try to discover Euler's insights yourself first!**

##

# Euler's Degree-Based Reasoning 🧮

![bg right:40% width:90%](../../lecture-note/figs/labeled-koningsberg.jpg)

- **Even degree nodes (2k edges)**: Enter/leave k times perfectly
- **Odd degree nodes (2k+1 edges)**: One "leftover" edge
- **Key insight**: Leftover edges can only be at start/end points

##

# Euler's Path Theorem 🏆

**An Euler path/circuit exists if and only if:**

1. **Graph is connected** (can reach any node from any other), **AND**
2. **Either:**
   - All nodes have even degree (**Euler circuit**)
   - Exactly two nodes have odd degree (**Euler path**)

**Königsberg verdict**: 4 nodes with odd degree → **impossible!**

##

# Network Terminology 📚

- **Walk**: Any sequence of connected nodes (can repeat)
- **Trail**: Walk without repeating edges (Euler trail)
- **Path**: Walk without repeating nodes
- **Circuit**: Closed trail (starts/ends at same node)
- **Cycle**: Closed path

**Königsberg sought an Euler circuit!**

##

# Aftermath: The Bridges' Fate 🏙️💣

- 🇷🇺 During WWII, Allied forces bombarded Königsberg
- 💥 Two of the seven bridges were destroyed
- ✅ Ironically, this destruction made an Euler path possible!
- 🏙️ City renamed Kaliningrad, now Russian territory

![bg right:50% width:80%](../../lecture-note/figs/seven-bridge-bombared.png)

##

# 💻 Coding Time: Networks in Code! 🌐

[Let's represent networks with Python!](https://skojaku.github.io/adv-net-sci/m01-euler_tour/how-to-code-network.html) 🐍


##


# Key Takeaways

- **Mathematical abstraction**: Focus on structure, not physical details
- **Euler's theorem**: Degree constraints determine network traversability
- **Network terminology**: Walks, trails, paths, circuits, and cycles
- **Historical impact**: From recreational puzzle to foundation of network science
- **Modern relevance**: GPS navigation, internet routing, social networks

##

# Any questions?
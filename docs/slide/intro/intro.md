---
marp: true
theme: network-science
paginate: true
math: katex
---

<!-- _class: mid -->

## Before we start

<hr>

- Microphone on
- Zoom room open
- Recording started
- Sound volume up

---

<!-- _class: lead -->

<div class="eyebrow">Advanced Topics in Network Science · Session 01</div>

# Networks

<hr>

<div class="sub">A flu, a bank and the login program on your server fail in the same way, and that is not a coincidence</div>

<div class="credit">Sadamori Kojaku · Binghamton University</div>

<!--
Open on the outbreak, not on definitions. The whole first part is one story.
-->

---

## Roadmap

<hr>

<div class="steps-list">

<div><div class="i">01</div><div>An outbreak and a map</div></div>
<div><div class="i">02</div><div>The same story, everywhere</div></div>
<div><div class="i">03</div><div>What makes a network a network</div></div>
<div><div class="i">04</div><div>How this course works</div></div>

</div>

---

<!-- _class: lead -->

<div class="eyebrow">Binghamton University</div>

# EngiNet™

<hr>

<div class="sub">State University of New York</div>

---

<!-- _class: mid -->

## Course materials: all rights reserved

<hr>

No part of the course materials used in the instruction of this course may be reproduced
in any form or by any electronic or mechanical means, including the use of information
storage and retrieval systems, without written approval from the copyright owner.

© Binghamton University, State University of New York

---

<!-- _class: mid -->

## EngiNet: who to contact

<hr>

- EngiNet office: Janice Kinzer, enginet@binghamton.edu
- EngiNet by phone: 1-800-478-0718, or 607-777-4965
- Media production: Rafia Rahman
- Instructor: Sadamori Kojaku, skojaku@binghamton.edu, 607-777-5039

---

<!-- _class: mid -->

## Course overview

<hr>

- Instructor: Sadamori Kojaku
- Email: skojaku@binghamton.edu
- Office hours: Friday 10:00–14:00
- Course site: <a href="https://skojaku.github.io/adv-net-sci">skojaku.github.io/adv-net-sci</a>

---

<!-- _class: part -->

<div class="band">
  <div>Part 1: An outbreak and a map</div>
  <div class="count">01 / 04</div>
</div>

## April 2009: a new flu leaves Mexico

Nobody has immunity, and every border is a guess about where it goes next.

---

<!-- _class: mid -->

## Where does it surface first?

<hr>

The 2009 H1N1 pandemic starts in Mexico. Name the first country outside Mexico with a confirmed case, and the second one.

* Neighbours first, then outward in rings?
* The largest countries first?
* Something else?
* *Turn to your neighbour. Thirty seconds.*

---

<!-- _class: mid -->

## First the United States. Then Spain.

<hr>

Spain is nine thousand kilometres from Mexico City. Guatemala shares a border with Mexico, and was reached later.

---

## Kilometres are the wrong ruler

<hr>

Ask instead: how many people fly this route in a day?

<div class="fig">

![](figures/flightpath.png)
<figcaption>Guatemala City is next door and hard to reach; Madrid is far away and one flight away.</figcaption>

</div>

---

## The ruler that works

<hr>

<div class="fig">

![](figures/airline_routes.jpg)
<figcaption>Every scheduled airline route on Earth. Measure the distance along these lines and the 2009 arrival times line up (Brockmann and Helbing, Science, 2013).</figcaption>

</div>

---

<!-- _class: part -->

<div class="band">
  <div>Part 2: The same story, everywhere</div>
  <div class="count">02 / 04</div>
</div>

## Epidemics are not a special case

The same question, who is connected to whom, decides outcomes in systems that share nothing else.

---

## 15 September 2008

<hr>

<div class="cols">
<div>

Lehman Brothers files for bankruptcy. One firm, out of thousands.

* Within days, banks stop lending to each other worldwide.
* Why should one failure do that?
* *Thirty seconds with your neighbour.*

</div>
<div class="fig">

![](figures/lehman.jpg)

</div>
</div>

---

## Banks are a network

<hr>

Each dot is a bank; each line is money one bank owes another, often due tomorrow morning.

<div class="fig">

![](figures/interbank_1.png)
<figcaption>A bank is only as solvent as the promises pointing into it, and it cannot see past its own neighbours.</figcaption>

</div>

---

## One default, eight lenders short

<hr>

Everyone who lent to the failed bank is now missing money, and may fail in turn: **cascading default**.

<div class="fig">

![](figures/interbank_2.png)
<figcaption>Red is the default and the losses leaving it. The damage travels the same links the money did.</figcaption>

</div>

---

<!-- _class: mid -->

## 29 March 2024

<hr>

A hobby project compresses files. It is maintained by one person, unpaid, for years.

* How does a backdoor in that project reach the login program of nearly every Linux server on Earth?
* *Take thirty seconds.*

---

## What a compression library touches

<hr>

xz compresses files. Nothing about it is security-critical until you follow what links against it.

<div class="fig">

![](figures/xz_1.png)
<figcaption>Each arrow reads "is built into". Four steps separate a compression library from the program that authenticates every remote login.</figcaption>

</div>

---

## Two years, one volunteer

<hr>

Whoever maintains the first box in that chain controls everything downstream of it.

<div class="fig">

![](figures/xz_2.png)
<figcaption>A new contributor helped for about two years, became a maintainer, and shipped hidden code in version 5.6.0 that reached sshd on Fedora and Debian test builds.</figcaption>

</div>

---

## It was caught by half a second

<hr>

<div class="fig">

![](figures/xz_3.png)
<figcaption>Andres Freund noticed logins to a test machine had slowed, went looking, and found the backdoor before it reached a stable release. Nobody had audited the trust; a stopwatch caught it.</figcaption>

</div>

<a href="https://www.youtube.com/watch?v=aoag03mSuXQ">How the xz backdoor worked (video)</a>

---

## Same shape, three worlds

<hr>

Different material, one question: **who is connected to whom?**

<div class="fig">

![](figures/same_shape.png)
<figcaption>A virus travels the first, a loss the second, a backdoor the third. The reasoning that works on one works on the others.</figcaption>

</div>

---

<!-- _class: mid -->

## Your turn: name a network

<hr>

* Write down three networks you are part of right this minute.
* For each one, write one way it could fail.
* *One minute, on paper.*

---

<!-- _class: mid -->

## Let's collect a few

<hr>

* Which of your failures stay local?
* Which one spreads to everybody?
* *What made the difference?*

---

## Ones that are easy to miss

<hr>

<div class="cols">
<div>

Remove one insect and the plants only it visits go with it.

Which plant here is safest? Which is one extinction away from trouble?

</div>
<div class="fig">

![](figures/pollinator.png)
<figcaption>A line means that insect visits that plant.</figcaption>

</div>
</div>

---

## The network you are using right now

<hr>

<div class="cols">
<div>

Eighty-six billion neurons. What you are following this sentence with is the wiring between them.

</div>
<div class="fig">

![](figures/brain_tracts.jpg)
<figcaption>Long-distance fibre tracts of one human brain, reconstructed from diffusion MRI.</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band">
  <div>Part 3: What makes a network a network</div>
  <div class="count">03 / 04</div>
</div>

## Dots and lines are three centuries old

So what is new, and why does it need its own field?

---

## Isn't this just graph theory?

<hr>

<div class="cols">
<div>

* Mathematicians have studied dots and lines since Euler.
* Their favourite objects are regular: every node alike, every neighbourhood alike.
* *So what is left for us to do?*

</div>
<div class="fig">

![](figures/regular_graph.png)
<figcaption>Every node here has the same neighbourhood, so one proof covers all of them.</figcaption>

</div>
</div>

---

## Real networks are not like that

<hr>

<div class="cols">
<div>

A handful of nodes carry an enormous share of the links. Most carry very few.

No two neighbourhoods look alike, so one proof no longer covers all of them.

</div>
<div class="fig">

![](figures/internet_map.jpg)
<figcaption>Routed paths across the Internet, drawn by the Opte Project.</figcaption>

</div>
</div>

---

## For 2500 years, the same move

<hr>

Water, number, atoms, method: four attempts to reduce the world to something simpler.

<div class="fig">

![](figures/philosophers.jpg)
<figcaption>Two millennia apart, one shared instinct: cut the world into its simplest parts.</figcaption>

</div>

---

## The reductionist bet

<hr>

<div class="cols">
<div>

* Break the system into parts.
* Understand each part.
* Reassemble, and you understand the whole.

</div>
<div class="fig">

![](figures/digesting_duck.jpg)
<figcaption>Inside Vaucanson's duck, 1739: an automaton built to prove that digestion is clockwork.</figcaption>

</div>
</div>

---

## A thought experiment

<hr>

<div class="cols">
<div>

* You are an alien scientist studying humans.
* You know every neuron and every synapse, exactly.
* *Can you say what this person will dream tonight?*

</div>
<div class="fig">

![](figures/von_neumann.jpg)
<figcaption>John von Neumann, who was fond of this kind of question.</figcaption>

</div>
</div>

---

## Knowing the parts is not knowing the system

<hr>

<div class="cols">
<div>

* Every neuron, but not the dream.
* Every person, but not the protest.
* Parts never act alone; they act on each other.
* **The relationships are the object of study.**

</div>
<div class="fig">

![](figures/parts_vs_relations.png)
<figcaption>Same four parts in both rows. Only the lower row can carry anything between them.</figcaption>

</div>
</div>

---

## Who studied relationships first?

<hr>

<div class="cols">
<div>

In 1736 Euler was handed a puzzle about a walk through a city, and answered it by throwing the city away, keeping only what was connected to what.

</div>
<div class="fig">

![](figures/euler.jpg)
<figcaption>Leonhard Euler, 1707–1783.</figcaption>

</div>
</div>

---

## Seven bridges, one walk

<hr>

<div class="cols">
<div>

Königsberg had four landmasses joined by seven bridges.

* Can you cross every bridge exactly once?
* *Two minutes, on paper.*

</div>
<div class="fig">

![](figures/konigsberg.png)
<figcaption>Four landmasses, seven bridges, and nothing else about the city.</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band">
  <div>Part 4: How this course works</div>
  <div class="count">04 / 04</div>
</div>

## The rest of this hour is logistics

How the course is built, and why it is built that way.

---

<!-- _class: mid -->

## What you will be able to do

<hr>

* Analyse real networks at real size.
* Use the concepts the field is built on.
* Apply AI tools to network problems, and check their answers.
* Read a network science paper, and design your own study.

---

## Learning is training

<hr>

<div class="cols">
<div>

* Nobody gets stronger by watching someone else lift.
* You get stronger by lifting, badly at first.
* Class is the gym: paper, pair programming, code that runs.
* **Train until you can feel a concept**, not just define it.

</div>
<div class="fig">

![](figures/deadlift.jpg)
<figcaption>The part that builds strength is the part that is hard.</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Every module opens on paper

<hr>

<div class="cols">
<div>

* You solve it alone first.
* Then you compare with the person beside you.
* Bring a pen.

</div>
<div class="fig">

![](figures/pen_paper.jpg)
<figcaption>No laptop for the first fifteen minutes: the mistake has to be yours before the fix means anything.</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Play it before you learn it

<hr>

* Most modules ship an interactive game.
* Winning it needs the concept you have not been taught yet.
* You learn the concept by learning to win.

<a href="https://skojaku.github.io/adv-net-sci/assets/vis/vaccination-game.html">Open the vaccination game</a>

---

<!-- _class: mid -->

## Weekly quiz

<hr>

* Every class opens with a short written quiz on last week.
* A few questions, graded and reviewed during class.
* One resubmission allowed.
* Online students submit through Brightspace.

---

<!-- _class: mid -->

## Assignments

<hr>

* Most modules have a coding assignment.
* Handed out through GitHub Classroom.
* Autograded, unlimited attempts until the deadline.

---

<!-- _class: mid -->

## Student Lecture

<hr>

* I publish a list of topics; you pick the one you like.
* You build a 15 to 20 minute lecture on it.
* **An interactive part is required**: a worksheet, an exercise the room does, live coding.
* A slide presentation on its own does not count.

---

## Where the grade comes from

<hr>

One square is one percent.

<div class="fig">

![](figures/grading.png)
<figcaption>There are no bonus points this year: the hundred squares on this slide are the whole grade.</figcaption>

</div>

---

<!-- _class: mid -->

## Exam

<hr>

* One final exam covering all topics.
* Multiple choice, take-home.
* Submitted through Brightspace.
* Exam week: **TBD**.

---

<!-- _class: mid -->

## Final project

<hr>

* Individual, thirty percent of the grade.
* Anything in network science: a new method, a visualization, a case study, a literature review.
* Proposal **TBD** · paper **TBD** · presentations **TBD**.

---

<!-- _class: mid -->

## Three projects from previous years

<hr>

* A map of research topics: which fields cite each other, and which papers sit on the bridge between two of them.
* Brain recordings as a network: electrodes are the nodes, and a link means two signals rise and fall together.
* The Tesla supercharger network: chargers are the nodes, drivable hops the links, and the question was where one more charger helps most.

---

<!-- _class: mid -->

## Where everything lives

<hr>

- Lecture notes: <a href="https://skojaku.github.io/adv-net-sci">skojaku.github.io/adv-net-sci</a>
- Everything else: <a href="https://github.com/skojaku/adv-net-sci/">github.com/skojaku/adv-net-sci</a>

---

<!-- _class: mid -->

## Attendance

<hr>

- Attendance is taken every class.
- Residential students: on paper, in the room.
- Online students: the assignment submission in each module counts as your attendance.

---

<!-- _class: mid -->

## Policy

<hr>

- Three credits means 6.5 or more hours of work a week outside class.
- AI tools are allowed for learning; cite them when you use them in an assignment.
- Back up your code; a lost laptop is not an extension.
- Accommodations are available; academic dishonesty is not.

---

<!-- _class: mid -->

## Before you go

<hr>

Earlier you each wrote down three networks you belong to.

* Which of them would you want to study for the project?
* What would you have to measure before you could say anything about it?
* *Bring one answer to the next class.*

---

<!-- _class: lead -->

# Questions?

<hr>

<div class="sub">Next time: Euler, seven bridges, and the first proof about a network</div>

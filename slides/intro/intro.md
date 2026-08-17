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

<div><div class="i">01</div><div>Introduction</div></div>
<div><div class="i">02</div><div>The same story, everywhere</div></div>
<div><div class="i">03</div><div>What makes a network a network</div></div>
<div><div class="i">04</div><div>How this course works</div></div>

</div>

---

<!-- _class: mid -->

## Course overview

<hr>

- Instructor: Sadamori Kojaku, skojaku@binghamton.edu
- Class: Tuesday and Thursday, 9:45–11:15, J01 Engineering
- Office hours: Friday, roughly 13:00–15:00
- Course site: <a href="https://skojaku.github.io/adv-net-sci">skojaku.github.io/adv-net-sci</a>

---

<!-- _class: part -->

<div class="band">
  <div>Part 1: Introduction</div>
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
* *Form a group and discuss. Thirty seconds.*

---

<!-- _class: mid -->

## First the United States. Then Spain.

<hr>

Spain is nine thousand kilometres from Mexico City. Guatemala shares a border with Mexico, and was reached later.

---

## Kilometres predict nothing

<hr>

Arrival time against distance in kilometres. One dot per country.

<div class="fig">

![](figures/flue-01.png)
<figcaption>A cloud, not a line, in all three panels (Brockmann and Helbing, Science, 2013).</figcaption>

</div>

---

## Flights predict it exactly

<hr>

The same arrival times, with distance now counted along air routes.

<div class="fig">

![](figures/flue-02.png)
<figcaption>Same three panels, one axis changed, and every country falls on a line.</figcaption>

</div>

---

## Drag the ruler yourself

<hr>

<figure class="anim-stage" id="h1n1-ruler">
  <div class="anim-bar">
    <div class="anim-step" data-anim-step></div>
    <div class="anim-dots" data-anim-dots></div>
    <button class="anim-btn" type="button" data-anim-prev aria-label="Previous step">◀</button>
    <button class="anim-btn" type="button" data-anim-play>⏸ Pause</button>
    <button class="anim-btn" type="button" data-anim-next aria-label="Next step">▶</button>
    <button class="anim-btn" type="button" data-anim-replay>↻ Replay</button>
  </div>
  <div class="h1-col" data-anim-canvas>
    <div data-anim-clear data-h1-plot></div>
    <div class="h1-side" data-anim-clear data-h1-side></div>
  </div>
  <figcaption class="anim-note" data-anim-note></figcaption>
</figure>

<script src="../../lecture-note/assets/anim/h1n1-ruler.js"></script>
<script src="../../lecture-note/assets/anim.js"></script>

---

<!-- _class: part -->

<div class="band">
  <div>Part 2: The same story, everywhere</div>
  <div class="count">02 / 04</div>
</div>

## Epidemics are not a special case

---

## 15 September 2008

<hr>

<div class="cols">
<div>

Lehman Brothers files for bankruptcy. One firm, out of thousands.

* Within days, banks stop lending to each other worldwide.
* Why should one failure do that?
* *Form a group and discuss. Thirty seconds.*

</div>
<div class="fig">

![](figures/lehman.jpg)

</div>
</div>

---

## Banks are a network

<hr>

Each dot is a bank; each line is money one bank owes another, due tomorrow morning.

<div class="fig">

![](figures/interbank_1.png)
<figcaption>Your bank never lent Lehman a cent, and sees only its own neighbours.</figcaption>

</div>

---

## The default walks

<hr>

Whoever lent to a failed bank is now missing money, and may fail in turn: **cascading default**.

<div class="fig">

![](figures/interbank_2.png)
<figcaption>Red has failed. Nobody on the path saw the loss coming from four steps away.</figcaption>

</div>

---

## 29 March 2024

<hr>

<div class="cols">
<div>

A hobby project compresses files. One person maintains it, unpaid, for years.

* How does a backdoor in that project reach the login program of nearly every Linux server on Earth?
* *Form a group and discuss. Thirty seconds.*

</div>
<div class="fig">

![](figures/xkcd_dependency.png)
<figcaption>xkcd 2347, "Dependency".</figcaption>

</div>
</div>

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

---

## How the backdoor actually worked

<hr>

<div class="cols">
<div>

A walk through the payload itself, if you want the detail.

<a href="https://www.youtube.com/watch?v=aoag03mSuXQ">youtube.com/watch?v=aoag03mSuXQ</a>

</div>
<div class="fig">

![](figures/xz_video_thumb.jpg)
<figcaption>Click the link, or paste the id into YouTube.</figcaption>

</div>
</div>

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

Two failures, very different reach:

* Your home router dies. You are offline; nobody else notices.
* Your bank's card processor dies. Every shop in town stops taking cards.
* *Which of yours is the router, and which is the processor?*

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

<!-- _class: mid -->

## Four more, with their failures

<hr>

- The power grid: one line sags into a tree in Ohio, and 50 million people lose power (2003).
- Your gut: a few hundred bacterial species trading chemicals, and an antibiotic deletes nodes.
- Shipping: one ship wedged in the Suez Canal, and European factories stop (2021).
- Words: which word follows which, which is the only thing a language model ever sees.

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

* Every class opens with a short written quiz on last week. Online students submit through Brightspace.
* You work it out on paper, then submit through the course quiz form: the answers go in directly, and you photograph your working into the same form.
* Sign in with your Binghamton account. That is how the answer reaches your name.
* You may retake it, and your best attempt is the one that counts.

---

<!-- _class: mid -->

## Everything is handed in through GitHub

<hr>

* You need a **GitHub account**, and you need to accept the invitation to the course organization. Until you do, no grade can reach you.
* Each assignment hands you a **private repository** of your own, through **Classroom 50**.
* You clone it, work in it, and **push** it back. Nothing is emailed and nothing is uploaded by hand.
* Two of them, from Module 2 on: one you do alone, one you do in a team.

---

<!-- _class: mid -->

## Pair Notebook: hand in the conversation

<hr>

* One per module for modules 2 to 6, on your own.
* A module taught as a tutoring session: an **AI tutor** in your terminal, and a **marimo** notebook filling up beside it in your browser.
* Sixty to ninety minutes. Stop anywhere and pick it up later.
* What is read is how you reasoned, not whether your code ran. Needing hints is not penalized.

---

<!-- _class: mid -->

## Group Mini-Project: the same ideas, on real data

<hr>

<div class="note">

Exactly one person accepts the assignment. Everybody else waits to be invited.

</div>

* Teams of up to three, in class, for modules 2 to 6.
* One shared repository, **autograded** on every push, and one score for the whole team.
* Three teammates each clicking accept makes three one-person repositories that cannot be merged afterwards.
* Sort out who accepts before anyone clicks.

---

<!-- _class: mid -->

## Set up your machine, once

<hr>

Twenty minutes, before the second week: <a href="https://skojaku.github.io/adv-net-sci/course/setup.html">skojaku.github.io/adv-net-sci/course/setup.html</a>

* **git** keeps the history of your work, and is what hands it in. On Windows, install **Git for Windows**: it brings Git Bash, a terminal that understands the same commands as a Mac.
* **uv** fetches Python and runs the notebooks, so you never install Python yourself.
* **Node.js** is what your AI tutor runs on.
* Your **course API key** arrives by email in the first week and goes in your shell profile.

---

<!-- _class: mid -->

## Student Lecture

<hr>

* Thirty-five topics, on the course site: <a href="https://skojaku.github.io/adv-net-sci/course/student-lecture.html">skojaku.github.io/adv-net-sci/course/student-lecture.html</a>
* You claim one, and build a 15 to 20 minute lecture on it.
* An interactive part is required: a worksheet, an exercise the room works through, live coding.
* A talk with no activity does not count, however good the talk is.

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
* Exam week: **10 to 16 December 2026**.

---

<!-- _class: mid -->

## Final project

<hr>

* Individual, thirty percent of the grade.
* Anything in network science: a new method, a visualization, a case study, a literature review.
* Proposal **Sun 27 Sep** · presentations **1 and 3 Dec** · paper **Sun 6 Dec**.

---

## From a previous year: a map of research topics

<hr>

<div class="cols">
<div>

Papers are the nodes; a citation is a link.

Clusters are fields. The interesting papers are the ones sitting on a bridge between two of them.

</div>
<div class="fig">

![](figures/sci-topic-net.png)
<figcaption>Each blob is a research community that nobody labelled in advance.</figcaption>

</div>
</div>

---

## From a previous year: a brain, wired by correlation

<hr>

<div class="cols">
<div>

Electrodes are the nodes. A link means two signals rise and fall together.

Nothing here is a physical wire; the network is inferred from the recording.

</div>
<div class="fig">

![](figures/ecog.png)
<figcaption>Electrocorticography: electrodes resting directly on the cortex.</figcaption>

</div>
</div>

---

## From a previous year: where to put the next charger

<hr>

<div class="cols">
<div>

Chargers are the nodes; a drivable hop is a link.

The question was which single new charger shortens the most journeys.

</div>
<div class="fig">

![](figures/super-charger.png)
<figcaption>Tesla superchargers, with the road network as the thing that connects them.</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Where everything lives

<hr>

- Lecture notes: <a href="https://skojaku.github.io/adv-net-sci">skojaku.github.io/adv-net-sci</a>
- Everything else: <a href="https://github.com/skojaku/adv-net-sci/">github.com/skojaku/adv-net-sci</a>

---

<!-- _class: mid -->

## Discord

<hr>

* Questions about lectures, assignments and setup; announcements; finding teammates.
* Four channels: welcome, network-science, artifacts, random.
* Nothing on Discord is graded. Ask half-formed questions there; that is what it is for.
* The invitation link comes through Brightspace.

---

<!-- _class: mid -->

## Attendance

<hr>

- Attendance is taken every class.
- Residential students: on paper, in the room.
- Online students: the assignment submission in each module counts as your attendance.

---

<!-- _class: mid -->

## Missing a class

<hr>

Two things, and you need both:

- Submit the absence form: <a href="https://forms.gle/yhzHoMSaKCRJXdGm7">forms.gle/yhzHoMSaKCRJXdGm7</a>
- Email me as well, ideally the day before.

**An absence that is not on the form is not counted**, however good the reason was.

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

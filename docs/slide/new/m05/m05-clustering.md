---
marp: true
theme: network-science
paginate: true
math: katex
---

<!-- _class: lead -->

<div class="eyebrow">Advanced Topics in Network Science · Module 05</div>

# The Club That Broke in Two

<hr>

<div class="sub">thirty-four friends, and the line nobody could agree on</div>

<div class="credit">Sadamori Kojaku · Binghamton University</div>

<!--
Open with a karate club in 1970, not with a definition of community. Everything in this module is one real split, pushed until it stops answering.
-->

---

## Roadmap

<hr>

<div class="steps-list">

<div><div class="i">01</div><div>A karate club, 1970, and a line nobody agrees on</div></div>
<div><div class="i">02</div><div>What counts as a group?</div></div>
<div><div class="i">03</div><div>Zachary's answer — cut between them</div></div>
<div><div class="i">04</div><div>More than chance — balls, strings, modularity</div></div>
<div><div class="i">05</div><div>Climbing Q — Louvain and Leiden</div></div>
<div><div class="i">06</div><div>Turn it around — communities first</div></div>
<div><div class="i">07</div><div>Three ways modularity lies</div></div>
<div><div class="i">08</div><div>How would you know? And where this lands</div></div>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 09</span></div>

## The club that broke in two

1970, and an anthropologist with a notebook

---

## Someone wrote the friendships down

<hr>

In 1970 an anthropologist named **Wayne Zachary** started watching a karate club at an American university.

For two years he recorded which members met each other **outside the dojo** — at bars, at tournaments, in classes.

<div class="fig tight">

![w:1080](figures/timeline-1970.png)
<figcaption>two years of watching, one paper</figcaption>

</div>

<!--
Zachary 1977, Journal of Anthropological Research 33(4): 452-473. Observed 1970-1972. He was studying conflict, not networks; the network was his instrument.
-->

---

## Two men who could not agree

<hr>

**Mr. Hi** taught the class and wanted the fees raised. **John A.** ran the business and wanted them held. Thirty-four members were caught between.

<div class="fig">

![w:1080](figures/the-dispute.png)
<figcaption>the instructor, the administrator, and everybody else</figcaption>

</div>

<!--
Both names are Zachary's own pseudonyms. The dispute ran for two years before anything happened.
-->

---

## Thirty-four people, seventy-eight friendships

<hr>

<div class="fig">

![w:1080](figures/karate-plain.png)
<figcaption>a line joins two members who met outside the dojo</figcaption>

</div>

No colour yet. Nobody is labelled. This is everything Zachary had.

<!--
Give them a moment to just look at it. Do not name anyone on the picture yet.
-->

---

<!-- _class: mid -->

## Point at the two groups

<hr>

<div class="formula">

Two groups. Where does the line go?

</div>

<!--
Do not answer. Do not hint. Do not say which side anyone is on. The next slide is the activity; the answer is two slides away.
-->

---

## Your turn

<hr>

Draw the line on paper — thirty seconds. Then hands up: **whose line cut more than fifteen friendships?**

<div class="fig">

![w:1080](figures/karate-three-guesses.png)
<figcaption>three lines this room will draw — and they are three different clubs</figcaption>

</div>

<!--
Actually take the hands. The room splitting is the point of the exercise, not a rhetorical device. None of the three drawn lines is the historical answer -- the figure asserts that.
-->

---

## In 1972 the club actually split

<hr>

The dispute ended in a fight over a fee increase. Mr. Hi started his own club. Every member had to choose.

<div class="fig">

![w:1080](figures/karate-split.png)
<figcaption>seventeen went with Mr. Hi (blue), seventeen stayed with the officers (red)</figcaption>

</div>

<!--
17 against 17. This is the ground truth for the rest of the module, and it is one of very few networks that has one.
-->

---

## Eleven friendships crossed the line

<hr>

<div class="fig">

![w:1080](figures/karate-crossing.png)
<figcaption>thirty-five friendships inside one club, thirty-two inside the other, eleven torn</figcaption>

</div>

Eleven of seventy-eight. The split ran almost exactly where the network was thinnest.

<!--
35 + 32 + 11 = 78. That "almost" is doing work: it is the whole of Part Eight.
-->

---

<!-- _class: mid -->

## Why should a network have groups at all?

<hr>

<div class="formula">

Nobody organised this club into two halves. Where did the halves come from?

</div>

<!--
Take two or three answers before moving on. "They were friends already" is the beginning of the right answer.
-->

---

## Four reasons, and they are not the same reason

<hr>

* People befriend people **like themselves**
* The **same work** puts people together
* Organisations are built in **layers**
* Information runs down **shared channels**

<div class="fig stack">

![w:1080](figures/why-groups.png)
<figcaption>four groups, four different things that made them</figcaption>

</div>

<!--
Homophily, shared function, hierarchy, shared information pathways. Different causes, and they leave different traces -- which is why one definition of "community" will not fit all four.
-->

---

## The only club whose answer really happened

<hr>

Almost every network you will ever cluster has **no answer key**. You find groups and nobody can tell you whether they are the right ones.

<div class="fig">

![w:1080](figures/ground-truth-or-not.png)
<figcaption>a recorded outcome on the left; the usual situation on the right</figcaption>

</div>

<!--
There is a trophy called the Zachary Karate Club Club, handed to whoever uses this network first at a network science conference. The joke is affectionate and it is also a complaint: the field leans on one small data set because so little else has a recorded answer. Do not quote the year -- I could not re-verify it.
-->

---

<!-- _class: mid -->

## Today's question

<hr>

<div class="formula">

What is a community — and how would you know the one you found is real?

</div>

The first half takes until lunch. The second half takes the rest of the module.

<!--
Big question, straight out of the curriculum. Both halves get answered; only one of them gets answered comfortably.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 09</span></div>

## What counts as a group?

the first instinct, and how it fails

---

## Everyone knows everyone

<hr>

<div class="cols">
<div>

The strictest possible answer: a group where **every** member is friends with **every** other.

That is a **clique**.

<div class="note">

One missing friendship and the whole thing is disqualified.

</div>

</div>
<div class="fig">

![w:537](figures/clique-def.png)
<figcaption>four mutual friends, and four one friendship short</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## How large is the biggest clique in this club?

<hr>

<div class="formula">

Thirty-four people. Seventy-eight friendships. Everyone knows everyone — how many can manage it?

</div>

Shout a number.

<!--
Take guesses. People say eight, ten, twelve. Do not correct them yet.
-->

---

## Five people. And only two such groups

<hr>

<div class="fig">

![w:1080](figures/karate-max-clique.png)
<figcaption>the largest all-know-all group in the club: five members</figcaption>

</div>

Both of them contain Mr. Hi. Neither contains John A.

<!--
Two maximum cliques, both of size 5, and they overlap in four people. Thirty-four members and the strictest definition finds five of them.
-->

---

<!-- _class: mid -->

## One missing friendship, and the group is disqualified?

<hr>

<div class="formula">

Two people in a group of eight never happened to meet. Is that group not a group?

</div>

<!--
Obviously not. The next four slides are four different ways of saying "obviously not", and they do not agree with each other.
-->

---

## Relax the head count

<hr>

<div class="cols">
<div>

A **k-plex**: every member may be missing at most **k** of the others.

At k = 1 you may miss one person. At k = 2, two.

<div class="note">

The clique is the k-plex with k = 0.

</div>

</div>
<div class="fig">

![w:537](figures/k-plex.png)
<figcaption>five members, each missing at most one of the others</figcaption>

</div>
</div>

---

## Relax it from the other side

<hr>

A **k-core**: keep at least **k** friends *inside* the group. Peel away anyone who cannot, repeat, and count with me.

<div class="fig">

![w:1080](figures/kcore-peel.gif)
<figcaption>peel away anyone below k, and it stops at the 4-core: ten people</figcaption>

</div>

<!--
Run the peel out loud. Ask what happens at k=5: the core empties. Ten people is a third of the club, and it is not two groups.
-->

---

## Relax the density

<hr>

<div class="cols">
<div>

Forget counting per person. Ask only that the group has at least a **fraction ρ** of the friendships it could have.

</div>
<div class="fig">

![w:537](figures/rho-dense.png)
<figcaption>eight of the fifteen possible friendships</figcaption>

</div>
</div>

---

## Relax the distance

<hr>

<div class="cols">
<div>

An **n-clique**: every member is within **n steps** of every other.

At n = 1 that is a clique again. At n = 2, a friend of a friend counts.

<div class="note">

Two cousins of this — n-clan and n-club — constrain where those paths may run. They are in the notes.

</div>

</div>
<div class="fig">

![w:537](figures/n-clique.png)
<figcaption>two steps from one end to the other</figcaption>

</div>
</div>

---

## Mix the axes

<hr>

<div class="cols">
<div>

A **k-truss**: every *friendship* has to sit inside at least **k − 2** triangles.

Not a rule about people — a rule about the links themselves.

</div>
<div class="fig">

![w:537](figures/k-truss.png)
<figcaption>every link with a triangle around it</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Did any of those split the club in two?

<hr>

<div class="formula">

Five definitions. Thirty-four people. Where are the two halves?

</div>

<!--
Nowhere. Wait for someone to say it.
-->

---

## They overlap, they multiply, and they do not partition

<hr>

Each definition is a different answer to *what counts as a group*, so the problem is **ill-posed** — there is no fact of the matter to be right about.

<div class="fig">

![w:1080](figures/patterns-overlap.png)
<figcaption>three definitions, three groups, overlapping — and two people in none of them</figcaption>

</div>

<!--
This is m05.c03 and it is the sentence the rest of the module keeps returning to. The move now is: stop defining, start optimising.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 09</span></div>

## Cut it

Zachary stopped looking for groups

---

## Stop looking for groups. Look at what runs between them

<hr>

<div class="fig">

![w:1080](figures/cut-idea.png)
<figcaption>do not ask what a group is — ask where the network is thinnest</figcaption>

</div>

<!--
Nine members from here to the end of the part -- small enough to follow by hand. Two groups of four who all know each other, plus one person on the edge.
-->

---

## Count what you cut

<hr>

<div class="fig">

![w:1080](figures/cut-def.png)
<figcaption>two friendships cross the line, so this cut costs two</figcaption>

</div>

<div class="formula">

$$\text{Cut}(V_1, V_2) = \sum_{i \in V_1} \sum_{j \in V_2} A_{ij}$$

</div>

<!--
Just a count of crossing edges. The sum is the same statement written for a computer.
-->

---

<!-- _class: mid -->

## So find the smallest cut 😈

<hr>

<div class="formula">

This problem is incompletely stated. What is missing?

</div>

Thirty seconds with your neighbour.

<!--
Do NOT say the word "size" or "balance". Let the demo find it for them.
-->

---

## Live demo

<hr>

Two groups of five, one friendship between them. Drag the solver and watch where it goes.

<div class="fig">

![w:1080](figures/two-cliques.png)
<figcaption>the network the demo starts from</figcaption>

</div>

<!--
skojaku.github.io/adv-net-sci/assets/vis/community-detection/index.html?scoreType=graphcut&numCommunities=2&randomness=1&dataFile=two-cliques.json
Let it run to the cheap answer before saying anything.
-->

---

## The cheapest cut peels one person off

<hr>

<div class="fig">

![w:1080](figures/karate-trivial-cut.png)
<figcaption>the club's only member with a single friend — cutting him away costs one</figcaption>

</div>

Nothing is wrong with the answer. It is genuinely the fewest crossing friendships. The **question** was wrong.

<!--
Node 12 in Zachary's numbering. A minimum cut with no constraint always finds a leaf, or an isolated corner. This is m05.c12.
-->

---

## So divide by the sizes

<hr>

<div class="fig">

![w:1080](figures/ratio-cut.png)
<figcaption>peeling one person scores 1/8; splitting the club scores 1/10 — and lower wins</figcaption>

</div>

<div class="formula">

$$\text{Ratio cut}(V_1, V_2) = \frac{\text{Cut}(V_1, V_2)}{|V_1| \cdot |V_2|}$$

</div>

<!--
Now the balanced split beats the trivial one. The normalizer did all the work.
-->

---

## What the normalizer does

<hr>

<div class="fig">

![w:1080](figures/normalizer-curve.png)
<figcaption>the product of the two group sizes, against how many people are on the smaller side</figcaption>

</div>

Biggest at equal halves, smallest when one side holds a single person. Dividing by it **punishes lopsided answers**.

---

## Balance by friendships instead of by heads

<hr>

<div class="fig">

![w:1080](figures/norm-cut.png)
<figcaption>seven friendships inside the left group, six inside the right</figcaption>

</div>

<div class="formula">

$$\text{Normalized cut}(V_1, V_2) = \frac{\text{Cut}(V_1, V_2)}{|E_1| \cdot |E_2|}$$

</div>

<!--
2/(7x6) = 1/21. And notice: a lone person has NO friendships inside, so normalized cut cannot even score the trivial answer. It rules it out rather than penalising it.
-->

---

## More than two groups

<hr>

<div class="fig">

![w:1080](figures/k-way-cut.png)
<figcaption>each group's escaping friendships, counted against its own size</figcaption>

</div>

Add up, over each group, its escaping friendships divided by its own size. Same idea, **K** times.

<!--
m05.c39. The formula is in the notes; the picture is the point.
-->

---

## Zachary ran his own club through it

<hr>

<div class="fig">

![w:1080](figures/karate-mincut.png)
<figcaption>the cut's prediction — and it agrees with what happened for thirty-three of the thirty-four</figcaption>

</div>

A method that knows nothing but who drank with whom, predicting a fight about money.

<!--
This is reproduced, not quoted: a weighted max-flow between the two leaders gives exactly Zachary's 1977 result. Thirty-three out of thirty-four.
-->

---

<!-- _class: mid -->

## One person it got wrong

<hr>

<div class="fig">

![w:1080](figures/karate-node9-ring.png)
<figcaption>the one member the structure did not predict</figcaption>

</div>

I am not going to tell you who he is today. We come back to him in the last session.

<!--
Node 9. Do not name the reason. It is the closing beat of Part Eight and it lands much harder if it waits three weeks.
-->

---

<!-- _class: mid -->

## But the cut wants you to know K first

<hr>

<div class="formula">

How many groups? The method will not tell you — it demands the number as input.

</div>

It also prefers equal halves, and finding the best cut is **NP-hard**.

<!--
End of day one. m05.c40, c41, c42. Leave the question hanging: what do you do when the number of groups is exactly what you do not know?
-->

---

<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 09</span></div>

## More than chance

a second opinion about what a group is

---

## Not "cheap to cut" — "more inside than chance"

<hr>

<div class="fig">

![w:1080](figures/chance-idea.png)
<figcaption>the same two friendships crossing, in two very different networks</figcaption>

</div>

Two crossing friendships out of thirty is remarkable. Two out of ten is Tuesday.

<!--
m05.c15. The cut counts crossings; it never asks how many crossings you SHOULD have expected.
-->

---

## Every friendship is two coloured balls on a string

<hr>

Give everybody a colour — that colour is their group. Now each friendship is a string with a ball at each end.

<div class="fig">

![w:1080](figures/balls-strings.gif)
<figcaption>pull a string, cut the strings, tip the balls into the bag, draw two</figcaption>

</div>

<!--
The whole of modularity is this game. Play it slowly. The GIF runs the four stages; the next five slides walk them one at a time.
-->

---

## Pull a string. Do the ends match?

<hr>

<div class="fig">

![w:1080](figures/observed.png)
<figcaption>six of the seven strings have the same colour at both ends</figcaption>

</div>

<div class="formula">

$$\text{observed} = \frac{\text{friendships inside a group}}{m}$$

</div>

<!--
Six out of seven. That is the observed side of the ledger and nothing more.
-->

---

<!-- _class: mid -->

## Paint everyone the same colour

<hr>

<div class="formula">

Now every string matches. Have you found anything?

</div>

<!--
No. Wait for them to say it. Do not say the word "chance" first.
-->

---

## So we need what chance would have given

<hr>

Cut every string. Tip the balls into a bag. Now the colours are loose and nobody is anybody's friend.

<div class="fig">

![w:1080](figures/bag-2m.png)
<figcaption>every friendship contributes two balls</figcaption>

</div>

<!--
This destroys the network and keeps exactly one thing: how many balls each person contributed. That is the null model, and it is a choice.
-->

---

## The bag holds 2m balls

<hr>

<div class="fig">

![w:1080](figures/bag-2m.png)
<figcaption>the ringed member has three friends, so three of the balls are hers</figcaption>

</div>

A member with **k** friends puts in **k** balls. So the chance of pulling out her colour is $k / 2m$ — and that is where the degree enters everything that follows.

<!--
m05.c44. This is the slide that makes k_i k_j / 2m stop being an incantation.
-->

---

## Draw two balls. Do *those* match?

<hr>

<div class="fig">

![w:1080](figures/expected.png)
<figcaption>seven balls of each colour, drawn twice</figcaption>

</div>

<div class="formula">

$$\text{expected} = \sum_{c} \left(\frac{\sum_{i \in c} k_i}{2m}\right)^{2}$$

</div>

<!--
Half and half here, so the expected match rate is 1/2. Any grouping has such a number.
-->

---

<!-- _class: mid -->
## Modularity is the gap

<hr>

<div class="fig">

![w:1080](figures/modularity-gap.png)
<figcaption>what the network did, against what the bag would have done</figcaption>

</div>

<div class="formula">

$$Q = \text{observed} - \text{expected}$$

</div>

<!--
6/7 minus 1/2 is 5/14. That is the whole definition; everything else is bookkeeping.
-->

---

## The same thing, written the usual way

<hr>

<div class="formula">

$$Q = \frac{1}{2m}\sum_{ij}\left[A_{ij} - \frac{k_i k_j}{2m}\right]\delta(c_i, c_j)$$

</div>

<div class="fig">

![w:1080](figures/modularity-matrix.png)
<figcaption>one pair of members: what happened, against what chance predicted</figcaption>

</div>

<!--
Go pair by pair instead of group by group. The algebra that turns one into the other is in the appendix -- expand the square, use delta(c,c_i)delta(c,c_j) = delta(c_i,c_j).
-->

---

## What "chance" actually is

<hr>

<div class="fig">

![w:1080](figures/configuration-model.png)
<figcaption>rewired at random, and every member keeps exactly the friends she had</figcaption>

</div>

The bag is the **configuration model**: shuffle every friendship, preserve every count. Change the null model and you change what counts as a community.

<!--
m05.c16. Worth saying out loud: this is a modelling choice, not a law. Part Seven is what it costs.
-->

---

## Your turn: compute Q by hand

<hr>

Two triangles, one friendship between them, seven friendships in all. Score the grouping that splits them.

<div class="fig">

![w:1080](figures/worksheet-q.png)
<figcaption>the number beside each member is how many friends she has</figcaption>

</div>

<!--
Two minutes, in pairs. Observed first, then expected. Do not put the answer on the board until most hands are down.
-->

---

## Five fourteenths

<hr>

<div class="fig">

![w:1080](figures/worksheet-q-answer.png)
<figcaption>splitting them scores five fourteenths; calling them one group scores exactly zero</figcaption>

</div>

Q lives between −1 and 1. People quote **0.3** as the threshold for real structure.

<!--
Remember that 0.3. Part Seven kills it, on this same club.
-->

---

## What the cut could not do

<hr>

<div class="fig">

![w:1080](figures/q-picks-k.png)
<figcaption>the same twelve people scored at one, two, three, four and five groups</figcaption>

</div>

Cut scores are not comparable across different K. **Q is.** So the number of groups falls out of the optimisation instead of going into it.

<!--
m05.c46. This is the reason modularity took over the field.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Five</span><span class="count">05 / 09</span></div>

## Climbing Q

and why every method here is a guess

---

<!-- _class: mid -->

## How many ways can you split thirty-four people?

<hr>

<div class="formula">

Any number of groups, any sizes. How many groupings are there?

</div>

Order of magnitude will do.

<!--
People guess thousands, or millions. Let them be wrong by twenty orders of magnitude.
-->

---

## About two followed by twenty-eight zeros

<hr>

<div class="fig">

![w:1080](figures/bell-growth.png)
<figcaption>groupings of n people, on a log scale, up to the club's thirty-four</figcaption>

</div>

Maximising Q is **NP-hard**. Everything after this slide is a heuristic with no guarantee whatsoever.

<!--
B(34) = 2.1e28. Do NOT say "more than atoms in the universe" -- that is about 1e80 and the comparison is false.
-->

---

## Louvain, phase one

<hr>

Everyone starts alone. Move each member into whichever neighbouring group raises Q the most, until no move helps.

<div class="fig">

![w:1080](figures/louvain.gif)
<figcaption>one move at a time, on the club</figcaption>

</div>

<!--
This is greedy local search, and it is the whole of phase one. The GIF ends on the four communities the deck uses later.
-->

---

## Louvain, phase two

<hr>

Collapse each group into one node, run phase one again, repeat. The **hierarchy is a by-product**.

<div class="fig">

![w:1080](figures/louvain.gif)
<figcaption>local moves, then the groups themselves become nodes</figcaption>

</div>

<!--
Fast enough for millions of nodes. Every round is cheap because the network shrinks.
-->

---

<!-- _class: mid -->

## Must a group Louvain returns be connected inside?

<hr>

<div class="formula">

It hands you a set of people and calls them a community. Can you walk from any one of them to any other without leaving the set?

</div>

<!--
Almost everybody says yes. It is not true, and the reason is worth the beat.
-->

---

## No — and Leiden fixes it

<hr>

<div class="fig">

![w:1080](figures/leiden-fix.png)
<figcaption>one group Louvain returned, in two pieces that do not touch</figcaption>

</div>

Move a broker out early and the people she was connecting stay behind, in one group, in two pieces. **Leiden** adds a refinement step that guarantees this cannot happen.

<!--
m05.c22. A real defect of a real algorithm, found years after everyone had adopted it.
-->

---

## Every method answers a different question

<hr>

<div class="fig">

![w:1080](figures/four-answers.png)
<figcaption>one network, and four different things the word "community" can mean</figcaption>

</div>

Cheap to cut. More than chance. Where a random walk gets stuck (Module 07). What the eigenvectors say (Module 08). Or: **what would generate this**.

<!--
The last one is Part Six and it is a genuinely different way to think.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Six</span><span class="count">06 / 09</span></div>

## Turn it around

communities first, network second

---

## Build the network from the groups

<hr>

<div class="fig">

![w:1080](figures/sbm-flip.png)
<figcaption>give everybody a group, look up the odds, roll for every pair</figcaption>

</div>

Give every member a group. Then join **i** and **j** with a probability that depends on nothing but their two groups.

<!--
m05.c29, the stochastic block model. Every other method in this module reads a network and guesses; this one writes a network and then asks which guess would have written it.
-->

---

## Sort by group, and blocks appear

<hr>

<div class="fig">

![w:1080](figures/sbm-blocks.png)
<figcaption>the same ten members, and who is joined to whom, ordered by group</figcaption>

</div>

<!--
Rows and columns are members; a filled cell is a friendship. Nothing changed but the order.
-->

---

## One small matrix decides everything

<hr>

<div class="fig">

![w:1080](figures/block-matrix.png)
<figcaption>the chance of a friendship, for each pair of groups</figcaption>

</div>

Two groups, four numbers. Ten groups, a hundred. That matrix **is** the model.

---

## Inside more likely than outside

<hr>

<div class="fig">

![w:1080](figures/sbm-assortative.png)
<figcaption>a high diagonal, and the communities you already recognise</figcaption>

</div>

<!--
This is the ordinary case and it reproduces exactly what modularity looks for.
-->

---

<!-- _class: mid -->

## What would you see if you flipped it?

<hr>

<div class="formula">

Make friendships *between* the groups more likely than inside them. What does the network look like?

</div>

<!--
Let them describe it before showing it. Some will say "no communities". That is the interesting wrong answer.
-->

---

## Groups that connect outward

<hr>

<div class="fig">

![w:1080](figures/sbm-three-cases.png)
<figcaption>inside more likely; outside more likely; and no difference at all</figcaption>

</div>

<!--
m05.c52. Predator and prey; buyers and sellers; men and women in a dating network. Modularity would score these near zero and report nothing.
-->

---

## A community is a shared *pattern*

<hr>

<div class="fig">

![w:1080](figures/sbm-pattern.png)
<figcaption>eight people, two groups, and not one friendship inside either group</figcaption>

</div>

Not a dense lump — a set of people who **connect to the rest of the world the same way**. That is the wide definition from Part One, and this is the model that can express it.

<!--
m05.c31. Worth pausing on: by every definition in Part Two, neither of these groups is a group at all.
-->

---

## Detection becomes inference

<hr>

<div class="fig">

![w:1080](figures/sbm-inference.png)
<figcaption>five candidate groupings, scored by how likely each makes the network you saw</figcaption>

</div>

Pick the grouping that makes the observed network **most probable**. Now "how many groups?" is model selection, not a rule of thumb.

<!--
m05.c32. The likelihood, its concavity, and the closed form for the block probabilities are all in the appendix.
-->

---

## Your turn: find the blocks

<hr>

Here is the same network in the order you happened to receive it. Swap rows and columns until you can see the groups.

<div class="fig">

![w:1080](figures/sbm-shuffled.png)
<figcaption>same members, same friendships, no order</figcaption>

</div>

<!--
Three minutes. Some will sort by degree and get close. The point is that the blocks were always there.
-->

---

<!-- _class: mid -->

## You have the tools. Next week you run them

<hr>

<div class="formula">

Louvain, on real networks, with your own hands.

</div>

Pen and paper first, then the Module 05 notebook. Bring the questions you cannot answer from the slides.

<!--
End of day two. The hands-on session is where they generate the Q > 0.3 that opens Part Seven, so make sure they actually do it.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Seven</span><span class="count">07 / 09</span></div>

## Three ways modularity lies

last week you pulled Q above 0.3 out of a random graph

---

<!-- _class: mid -->

## Two groups of five, one friendship between them

<hr>

<div class="fig">

![w:1080](figures/two-cliques.png)
<figcaption>ten people, and one link holding them together</figcaption>

</div>

Does modularity separate them?

<!--
Everyone says yes. They are right. Say nothing about scores yet.
-->

---

## Yes — and it is not close

<hr>

<div class="fig">

![w:1080](figures/two-cliques-split.png)
<figcaption>split, this scores 0.45; called one group, it scores exactly zero</figcaption>

</div>

Two obvious groups, and the score is emphatic about it.

---

<!-- _class: mid -->

## Now add a third, much larger group

<hr>

<div class="formula">

Forty more people, somewhere else in the network, with nothing to do with these ten. What happens to the two groups of five?

</div>

<!--
Nobody expects anything to happen. That is the trap and it is worth walking into slowly.
-->

---

## Live demo

<hr>

The same two groups of five. Untouched. Plus forty people who know each other.

<div class="fig">

![w:1080](figures/big-clique-net.png)
<figcaption>nothing about the two small groups has changed</figcaption>

</div>

<!--
skojaku.github.io/adv-net-sci/assets/vis/community-detection/index.html?scoreType=modularity&numCommunities=3&randomness=0.9&dataFile=two-cliques-big-clique.json
Ask for three communities. Watch it refuse.
-->

---

## The two groups get merged

<hr>

<div class="fig">

![w:1080](figures/resolution-limit.png)
<figcaption>alone, two groups; in company, modularity insists they are one</figcaption>

</div>

Merging them **raises** Q — 0.1410 against 0.1404. Not a bug in the algorithm. The definition prefers it.

<!--
m05.c26, the resolution limit. Fortunato and Barthelemy 2007. The cliques are identical in both networks -- that is the whole argument.
-->

---

## The threshold is the square root of 2m

<hr>

<div class="fig">

![w:1080](figures/sqrt2m.png)
<figcaption>the same ten internal friendships, on either side of the line</figcaption>

</div>

Alone, the network has 21 friendships and the threshold is 6.5 — a group with ten survives. In company it has 274, the threshold is 23.4, and the same ten no longer clear it.

<!--
sqrt(2L) is Fortunato and Barthelemy's own statement. The lecture note says O(m); that is loose and it is being fixed.
-->

---

## A group's fate is decided somewhere else

<hr>

<div class="fig">

![w:1080](figures/non-local.png)
<figcaption>the same two groups, and a crowd that has never met either of them</figcaption>

</div>

Nothing inside those ten people changed. The **whole network's** size decided whether they exist.

<!--
Non-locality. This is why "just tune the resolution parameter" is a patch and not a fix.
-->

---

<!-- _class: mid -->

## Is there one best grouping?

<hr>

<div class="formula">

You maximise Q and get an answer. Run it again. Same answer?

</div>

<!--
They ran it last week with different seeds, so somebody in the room already knows.
-->

---

## The landscape is rugged

<hr>

<div class="fig">

![w:1080](figures/degeneracy.png)
<figcaption>one grouping after another, and a great many of them nearly tie</figcaption>

</div>

Best on this club: 0.4198. Runner-up: 0.4151 — one percent apart, and the two disagree about **thirty-two pairs** of members.

<!--
m05.c27. "Near-optimal" means almost nothing when the optimum is a plateau with exponentially many nearly-equal peaks.
-->

---

<!-- _class: mid -->

## What does it return on a network with no groups at all?

<hr>

<div class="formula">

Forty people, wired together at random. No groups were put in. What comes out?

</div>

<!--
Half the room will say "about zero". They did this experiment last week and it did not say about zero.
-->

---

## Live demo

<hr>

<div class="fig">

![w:1080](figures/random-net.png)
<figcaption>forty people, forty-one friendships, no structure whatsoever</figcaption>

</div>

<!--
skojaku.github.io/adv-net-sci/assets/vis/community-detection/index.html?scoreType=modularity&numCommunities=4&randomness=1&dataFile=random-net.json
-->

---

## Q = 0.66 — higher than the two obvious groups scored

<hr>

<div class="fig">

![w:1080](figures/random-q-dots.png)
<figcaption>two hundred random networks, each with the club's thirty-four people and seventy-eight friendships</figcaption>

</div>

Every one of them clears 0.3. Their average is **0.354**; the split that really happened scores **0.358**.

<!--
m05.c28 and c47. The rule of thumb dies here, on this club, by four thousandths. Q cannot be compared across networks, and a high score alone is not evidence of anything.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Eight</span><span class="count">08 / 09</span></div>

## How would you know?

three methods, three answers

---

## Three methods gave three different clubs

<hr>

The cut said two groups of seventeen. Modularity says **four**. Which is right?

<div class="fig">

![w:1080](figures/karate-louvain-four.png)
<figcaption>colour marks Louvain's four groups here, not the two clubs</figcaption>

</div>

<!--
The honest answer is "it depends what you have to compare against", and that splits the rest of this part in two.
-->

---

## Without an answer key: conductance

<hr>

<div class="cols">
<div>

Count the friendships that **escape** the group. Divide by everything the group is attached to.

Low means a group that keeps to itself.

</div>
<div class="fig">

![w:537](figures/conductance-def.png)
<figcaption>two friendships escape; the group has eight link-ends in all</figcaption>

</div>
</div>

---

## It scores one group at a time

<hr>

<div class="fig">

![w:1080](figures/conductance-karate.png)
<figcaption>the split that happened scores about 0.15 — eleven escaping out of seventy-five</figcaption>

</div>

Unlike Q, this is a score **per group**, so you can ask about one community without committing to the whole grouping.

<!--
m05.c34. Internal-versus-external density is the same idea in its crudest form.
-->

---

## Every internal score just rewrites a definition

<hr>

<div class="fig">

![w:1080](figures/scores-disagree.png)
<figcaption>0.147 against 0.23–0.42 on the left; 0.3582 against 0.4198 on the right</figcaption>

</div>

They do not disagree about the facts. They disagree about **what a group is** — and neither failed an exam.

<!--
Conductance: real split 0.147 against Louvain's four groups at 0.23 to 0.42. Modularity: 0.4198 against 0.3582. Same network, same two candidates, opposite verdicts.
-->

---

## With an answer key, the unit is the pair

<hr>

<div class="fig">

![w:1080](figures/pairs-15.png)
<figcaption>six people make fifteen pairs</figcaption>

</div>

Two groupings agree about a pair when both put them together, or both keep them apart. That is what every score below counts.

---

## How much does one grouping tell you about the other?

<hr>

<div class="fig">

![w:1080](figures/mutual-information.png)
<figcaption>where each person belonged, and where the method put her — the colours are not comparable</figcaption>

</div>

Treat the two labellings as two random variables. Their **mutual information** is how much knowing one tells you about the other.

<!--
m05.c35, first half. If the method were perfect, knowing its label would tell you the true label exactly.
-->

---

<!-- _class: mid -->
## Divide by how much there was to know

<hr>

<div class="fig">

![w:1080](figures/nmi-formula.png)
<figcaption>what the two share, against everything there was to share</figcaption>

</div>

<div class="formula">

$$\text{NMI} = \frac{2\,I(X;Y)}{H(X) + H(Y)}$$

</div>

<!--
Normalising by the entropies puts it on [0,1]: 1 is identical, 0 is no information at all.
-->

---

## Your turn: score this

<hr>

Six people. Three and three, really. The method put one of them in the wrong group.

<div class="fig">

![w:1080](figures/worksheet-nmi.png)
<figcaption>the truth on top, what the method said underneath</figcaption>

</div>

<!--
Ask for a guess first -- what fraction out of one? Most people say "about 0.8, it only got one wrong". Then have them count the pairs.
-->

---

## One person wrong, and the two scores disagree about how bad that is

<hr>

<div class="fig">

![w:1080](figures/worksheet-nmi-answer.png)
<figcaption>shared information says 0.48; counting pairs says ten of the fifteen agree</figcaption>

</div>

Ten out of fifteen is 0.67. That is the **Rand index**, and it feels generous for one person in six.

<!--
It is generous. The next slide is why.
-->

---

<!-- _class: mid -->

## A coin-flip grouping already scores two thirds

<hr>

<div class="formula">

Assign all six people at random and the Rand index still comes out high. How do you fix a score like that?

</div>

<!--
Somebody will say "subtract what you would get by chance". That is exactly right and it is the same move as modularity's null model.
-->

---

<!-- _class: mid -->
## Subtract what chance would have given

<hr>

<div class="fig">

![w:1080](figures/ari.png)
<figcaption>counting pairs gives 0.67; taking chance out leaves 0.32</figcaption>

</div>

That is the **adjusted Rand index**. Zero means you did as well as coin-flipping. Negative means worse.

<!--
m05.c36. Same correction, same spirit, as the k_i k_j / 2m in modularity. Comparing to chance is the recurring idea of this whole module.
-->

---

## Report both

<hr>

<div class="fig">

![w:1080](figures/nmi-vs-ari.png)
<figcaption>one grouping, one answer key, two verdicts: 0.48 and 0.32</figcaption>

</div>

Shared information is generous to methods that make many small groups; pair counting is conservative. Report both.

---

## The best score is not what happened

<hr>

<div class="fig">

![w:1080](figures/best-vs-real.png)
<figcaption>four groups scoring 0.4198 — and the dashed line is where the club really broke</figcaption>

</div>

The split that actually happened — seventeen against seventeen, in 1972, over money — scores **0.3582**.

<!--
Let that sit. Maximising the score does not find the event. The optimum is not the truth, and on the one network where we can check, it is not even close to the truth.
-->

---

<!-- _class: mid -->
## And it matches reality less well than the 1977 answer

<hr>

<div class="fig">

![w:1080](figures/nmi-comparison.png)
<figcaption>scored against what really happened: 0.84 for the 1977 cut, 0.59 for the best-scoring grouping</figcaption>

</div>

Fifty years of better algorithms, and the higher score is the worse answer.

<!--
Not a criticism of Louvain -- it maximised exactly what it was asked to maximise. The objective was never "predict the split".
-->

---

## And that one person

<hr>

<div class="fig">

![w:1080](figures/node9.png)
<figcaption>structurally an officer; he joined Mr. Hi's club anyway</figcaption>

</div>

He was **three weeks from his black-belt test**. Switching would have cost him his rank, because Mr. Hi was the instructor.

<!--
This is the man from Part Three. The structure was not wrong about his friendships -- it was right. It simply cannot see a belt test.
-->

---

## Metadata is not ground truth

<hr>

<div class="fig">

![w:1080](figures/no-free-lunch.png)
<figcaption>three methods, three answers, and no umpire in the picture</figcaption>

</div>

A low score can mean the method failed — or that the labels have nothing to do with the wiring. Nothing in the score tells you which. And **no method is best on every network**: each encodes assumptions, and the job is knowing when they hold.

<!--
Peel, Larremore and Clauset 2017, "The ground truth about metadata and community detection in networks". m05.c48, no free lunch.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Nine</span><span class="count">09 / 09</span></div>

## Where this lands

---

## Four fields already asking this exact question

<hr>

<div class="fig">

![w:1080](figures/applications.png)
<figcaption>the same question, four times over</figcaption>

</div>

Echo chambers in political networks. Protein complexes and disease modules. Autonomous systems on the Internet. Research fields in citation data.

<!--
m05.c37. In every one of them the ground-truth problem from the last slide is live and unsolved.
-->

---

<!-- _class: mid -->
## Module 05 in one picture

<hr>

<div class="fig">

![w:1080](figures/recap.png)
<figcaption>the club, the cut, the null model, and the doubt</figcaption>

</div>

<!--
Four moves. Story, then the maths of that story, then the general case, then everything that goes wrong with it.
-->

---

## Coming up in Module 06

<hr>

<div class="fig">

![w:1080](figures/m06-teaser.png)
<figcaption>the club broke cleanly because two people were holding it together</figcaption>

</div>

Mr. Hi had **16** friends. John A. had **17**. Today we asked which *group* somebody was in. Next we ask which *person* matters.

<!--
Centrality. The two hubs are exactly why this network splits so cleanly, and they are the bridge into the next module.
-->

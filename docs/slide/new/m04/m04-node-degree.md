---
marp: true
theme: network-science
paginate: true
math: katex
---

<!-- _class: lead -->

<div class="eyebrow">Advanced Topics in Network Science · Module 04</div>

# Count Your Friends

<hr>

<div class="sub">then count theirs</div>

<div class="credit">Sadamori Kojaku · Binghamton University</div>

<!--
Open with eight girls in a 1961 high school, not with a definition of degree. The whole module is one observation pushed until it becomes a distribution.
-->

---

<!-- _class: mid -->

## The question for today

<hr>

<div class="formula">

Why do your friends have more friends than you do?

</div>

Take the insult first, and we will take it apart afterwards.

<!--
Do not answer this. Part Three answers it exactly, in one line. Do not say the word "variance" yet.
-->

---

## Roadmap for today

<hr>

<div class="steps-list">

<div><div class="i">01</div><div>Marketville, 1961 — eight girls, and a number that offends everyone</div></div>
<div><div class="i">02</div><div>Counting ends — degree, the handshake, and how common each is</div></div>
<div><div class="i">03</div><div>The exact gap — how much more, in one line</div></div>
<div><div class="i">04</div><div>Using the bias — coauthors, Facebook, and finding hubs blindfolded</div></div>
<div><div class="i">05</div><div>Reading the tail — linear axes fail, log axes talk</div></div>
<div><div class="i">06</div><div>Where hubs come from — growth, and preference</div></div>
<div><div class="i">07</div><div>Four awkward questions</div></div>
<div><div class="i">08</div><div>Do you believe that line?</div></div>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 08</span></div>

## Marketville, 1961

Eight girls, and a number that offends everyone

---

## Someone wrote the friendships down

<hr>

In 1961 **James Coleman** published *The Adolescent Society* — friendship surveys from twelve American high schools.

Thirty years later **Scott Feld** reopened one of them.

<div class="fig">

![w:1080](figures/timeline-1961.png)
<figcaption>one survey, and the paper that made it famous</figcaption>

</div>

<!--
Coleman asked students to name their friends. Feld 1991, American Journal of Sociology. The school is the one Feld called Marketville — he puts it in quotes and does not say whose pseudonym it is.
-->

---

## Eight of them

<hr>

<div class="fig">

![w:1080](figures/feld-names.png)
<figcaption>a line joins two girls who named each other</figcaption>

</div>

Feld's own words about the names: *they are fictitious*.

<!--
Nothing but the shape yet. Do not put numbers on the board.
-->

---

<!-- _class: mid -->

## Count them

<hr>

<div class="formula">

How many friends does each girl have — and what is the average across the eight?

</div>

Thirty seconds. Call the number out.

<!--
Let them count. Do not confirm anything until the next slide.
-->

---

## Two and a half

<hr>

<div class="cols">
<div>

Twenty friendships end at these eight girls, so the average girl has **2.5 friends**.

Betty and Tina have one. Sue and Alice have four.

<div class="note">

Nobody has 2.5 friends. It is an average, and it is about to be compared with another one.

</div>

</div>
<div class="fig">

![w:537](figures/feld-degrees.png)
<figcaption>each girl carrying her own count</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Now count theirs

<hr>

<div class="formula">

Pick one girl. How many friends does *each of her friends* have — and what is the average of those?

</div>

Same eight girls. Same ten lines. A different question.

<!--
This is the whole module in one slide. Do not answer it, do not hint, and do not say the number 3.
-->

---

## Your turn

<hr>

Take one girl each — count her friends, then count *their* friends, and divide.

<div class="fig">

![w:1080](figures/feld-worksheet.png)
<figcaption>one girl each; write her friends' average on the line</figcaption>

</div>

<!--
Assign round the room: Betty, Sue, Alice, Jane, Pam, Dale, Carol, Tina. Collect all eight before showing the next slide. Ask each student, out loud, whether their girl came out above or below her own count.
-->

---

## Five of eight

<hr>

<div class="fig">

![w:1080](figures/feld-friendmeans.png)
<figcaption>red: her friends average more than she has. Blue: fewer. Gray: exactly equal</figcaption>

</div>

Five girls are below their own friends. Two are above. Carol lands exactly on it.

<!--
The two above are Sue and Alice — the two with four friends each. Note that out loud; it comes back in Part Seven.
-->

---

## Feld's number

<hr>

<div class="cols">
<div>

The eight girls average **2.5** friends.

Their friends average **3.0**.

<div class="note">

This is not an insult and it is not about being unpopular. Every one of those twenty friendships was counted from both ends.

</div>

</div>
<div class="fig">

![w:537](figures/feld-two-numbers.png)
<figcaption>two averages over the same ten friendships</figcaption>

</div>
</div>

---

## Eight girls could be a fluke

<hr>

So Feld ran it on every girl in the survey with at least one friend — all 146 of them.

<div class="fig">

![w:1080](figures/marketville-146.png)
<figcaption>146 girls: 80 below their friends, 41 above, 25 exactly equal</figcaption>

</div>

<!--
2.7 friends each; 3.4 friends per friend. Nearly twice as many below as above. And it is the same school and the same survey — not a new example.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 08</span></div>

## Counting ends

Before we explain it, we have to be able to count it

---

## Degree

<hr>

<div class="cols">
<div>

A node's **degree** is the number of edges attached to it.

For one person it measures exposure. For the whole network, the spread of degrees says how centralised the thing is.

</div>
<div class="fig">

![w:537](figures/degree-def.png)
<figcaption>four edges attached, so degree four</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Add them all up

<hr>

<div class="formula">

Add every girl's degree together. What do you get — and is it a coincidence?

</div>

<!--
Let them add: 1 + 4 + 4 + 2 + 3 + 3 + 2 + 1. Ask for the number before you ask for the reason.
-->

---

## Twenty, and never odd

<hr>

<div class="fig">

![w:1080](figures/sum-ends.png)
<figcaption>a tick at every end of every line: twenty ticks, ten lines</figcaption>

</div>

Every edge has two ends, so the degrees add up to **twice the number of edges**: $\sum_i k_i = 2M$.

<!--
Ten friendships, twenty ends. This is the whole content of the degree sum formula, and the 2M comes back in Part Three as the denominator of q(k).
-->

---

## So the average falls out

<hr>

<div class="cols">
<div>

<div class="formula">

$$\langle k\rangle = \frac{2M}{N} = \frac{20}{8} = 2.5$$

</div>

You never have to count degrees one by one. Count the edges and double them.

</div>
<div class="fig">

![w:537](figures/mean-degree.png)
<figcaption>twenty ends shared out among eight girls</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## Try to build this

<hr>

<div class="formula">

Draw me a network in which **exactly three** people have an odd number of friends.

</div>

Any size, any shape. Two minutes.

<!--
Let them try. Walk round. Somebody will get to four odd, or two, and be unable to land on three. Do not say why yet.
-->

---

## You cannot

<hr>

<div class="fig">

![w:1080](figures/handshake.png)
<figcaption>odd degrees pair off; one is always left holding a loose end</figcaption>

</div>

The degrees sum to an even number, so the **odd** ones must come in pairs — the handshaking lemma.

<!--
And this is the thing that was quietly doing the work in Module 01: Euler's condition said zero or two odd-degree nodes, never one, never three, and this is why.
-->

---

## How common is each degree?

<hr>

<div class="cols">
<div>

$p(k)$ is the fraction of nodes whose degree is exactly $k$ — the **degree distribution**.

One number per degree, and it describes the whole network without naming anybody.

</div>
<div class="fig">

![w:537](figures/pk-def.png)
<figcaption>sort the nodes into piles by their count</figcaption>

</div>
</div>

---

## The eight girls, sorted

<hr>

<div class="fig">

![w:1080](figures/feld-pk.png)
<figcaption>two girls at each of one, two, three and four friends</figcaption>

</div>

A quarter of them at every degree — about as flat as a degree distribution gets.

<!--
Flat and narrow. Hold that thought: this is why the gap in this network turns out to be small. Real networks are not this polite, and Part Five shows one.
-->

---

<!-- _class: mid -->

## Why should friends have more?

<hr>

<div class="formula">

Nothing about these girls is unusual. So where does the extra friend come from?

</div>

Turn to your neighbour. One sentence.

<!--
Fish for "popular people get counted more". Do not supply it.
-->

---

## Hubs are on everybody's list

<hr>

<div class="fig">

![w:1080](figures/rosters.png)
<figcaption>Sue and Alice appear on four lists each; Betty and Tina on one</figcaption>

</div>

When you average over *friends*, you are averaging over the lists — and a popular girl is on many lists.

<!--
This is the mechanism. Everything after this is turning it into a number.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 08</span></div>

## The exact gap

Not "more" — how much more

---

<!-- _class: mid -->

## How much more?

<hr>

<div class="formula">

We know *why* friends have more friends. Can we say **how many** more, for any network at all?

</div>

<!--
The answer is one line long and it holds for every graph that has ever existed. Build to it.
-->

---

## Picking a friend is picking an end

<hr>

<div class="cols">
<div>

To pick a friend at random you do not pick a *person* — you pick one **end of one edge** and see who is holding it.

There are $2M = 20$ ends in this network.

</div>
<div class="fig">

![w:537](figures/bag-of-hands.png)
<figcaption>twenty hands in the bag, and whose they are</figcaption>

</div>
</div>

<!--
The same bag we used in Module 03 to follow an edge. Say so — this is the second time this bias has done real work.
-->

---

## A hub has more hands in the bag

<hr>

<div class="cols">
<div>

A girl with degree $k$ owns $k$ of the ends, so the chance of drawing her is proportional to $k$:

<div class="formula">

$$q(k) = \frac{k\,p(k)}{\langle k\rangle}$$

</div>

</div>
<div class="fig">

![w:537](figures/qk-formula.png)
<figcaption>four hands out of twenty belong to Sue</figcaption>

</div>
</div>

<!--
q(k), not p(k). This is the whole trick, and it is the same q(k) that told us which node an attack finds in Module 03.
-->

---

## The average friend

<hr>

<div class="fig">

![w:1080](figures/derivation-1.png)
<figcaption>average over ends, not over people</figcaption>

</div>

$$\langle k\rangle_{\text{friend}} = \sum_k k\,q(k) = \frac{\langle k^2\rangle}{\langle k\rangle}$$

<!--
Second moment over first moment. One line so far.
-->

---

## Put the variance in

<hr>

<div class="fig">

![w:1080](figures/derivation-2.png)
<figcaption>the second moment, rewritten</figcaption>

</div>

$$\langle k^2\rangle = \mathrm{Var}(k) + \langle k\rangle^2$$

<!--
Nothing new here — it is the definition of variance, rearranged. Substitute it on the next slide.
-->

---

## The whole paradox, in one line

<hr>

<div class="fig">

![w:1080](figures/derivation-3.png)
<figcaption>mean friend degree equals mean degree plus variance over mean</figcaption>

</div>

$$\langle k\rangle_{\text{friend}} = \langle k\rangle + \frac{\mathrm{Var}(k)}{\langle k\rangle}$$

<!--
Feld writes this out himself on page 1470, and it closes on his full 146-girl data too: 2.6575 + 0.6981 = 3.3557.
-->

---

## Which is why it never fails

<hr>

<div class="cols">
<div>

A variance cannot be negative. So the gap cannot be negative either.

**Every network** on earth has this property, and the only way to get equality is for every single node to have the same degree.

</div>
<div class="fig">

![w:537](figures/gap-nonneg.png)
<figcaption>the gap sits at zero or above, never below</figcaption>

</div>
</div>

<!--
This is the strongest sentence in the module. It is not a tendency, it is an identity.
-->

---

## Check it against the counting

<hr>

<div class="fig">

![w:1080](figures/feld-check.png)
<figcaption>variance one and a quarter, mean two and a half, gap one half</figcaption>

</div>

$2.5 + 0.5 = 3.0$ — and counting the sixty friends of the twenty friends by hand gave exactly the same.

<!--
Two completely different routes, one number. That is the moment to pause.
-->

---

## Careful: which average?

<hr>

<div class="fig">

![w:1080](figures/two-averages.png)
<figcaption>draw an edge end, and you get three point zero; draw a person, and you get two point nine nine</figcaption>

</div>

The theorem is about **friendships**, not about people. Averaging person by person gives a slightly different number.

<!--
3.0 versus 2.99 is nothing here, but the distinction is exactly what Part Seven's first question turns on. Flag it now.
-->

---

## Your turn

<hr>

Work out $\mathrm{Var}(k)/\langle k\rangle$ for both, and **predict the gap before you count**.

<div class="fig">

![w:1080](figures/worksheet-star-ring.png)
<figcaption>a star of four, and a ring of six</figcaption>

</div>

<!--
Star: degrees 3, 1, 1, 1. Ring: 2, 2, 2, 2, 2, 2. Make them predict first — the ring is the interesting one and half the room will expect a gap.
-->

---

## The gap *is* the variance

<hr>

<div class="fig">

![w:1080](figures/worksheet-answer.png)
<figcaption>star: gap one half. Ring: gap zero</figcaption>

</div>

Spread the degrees out and the paradox grows. Flatten them and it disappears entirely.

<!--
And now the obvious next question, which is the cliffhanger for the whole of day two: how spread out are the degrees in a real network?
-->

---

<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 08</span></div>

## Using the bias

It is not a curiosity. It is a tool

---

<!-- _class: mid -->

## Only about friendship?

<hr>

<div class="formula">

Does this happen anywhere else — or did we just find something odd about teenagers?

</div>

<!--
Take three suggestions from the room before moving on.
-->

---

## Your coauthors have more coauthors

<hr>

<div class="fig">

![w:1080](figures/coauthor-gap.png)
<figcaption>23,133 physicists: eight coauthors each, and their coauthors have twenty-two</figcaption>

</div>

Nearly **83%** of these authors are below their own coauthors' average.

<!--
arXiv condensed-matter coauthorship. Same identity, same reason: prolific collaborators appear on many author lists.
-->

---

## Seven hundred million people

<hr>

<div class="fig">

![w:1080](figures/fb-twitter.png)
<figcaption>Facebook 2011 and Twitter 2013, measured on the whole graph</figcaption>

</div>

On Facebook **92.7%** of users have fewer friends than their friends average. On Twitter it is over **98%**.

<!--
Ugander et al. 2011: 721 million active users, 68.7 billion friendships. Median friend count 99; mean friend count at the end of a random edge, 635. Hodas et al. 2013 for Twitter.
-->

---

<!-- _class: mid -->

## So what does that do to your data?

<hr>

<div class="formula">

Suppose you built your dataset by crawling — start somewhere, follow the links, keep going. What have you collected?

</div>

<!--
Almost every large network dataset that is not a full census was built this way. Let that land before answering.
-->

---

## Everything tilts

<hr>

<div class="fig">

![w:1080](figures/sampling-bias.png)
<figcaption>sample people at random and the hub turns up rarely; follow edges and it turns up constantly</figcaption>

</div>

Follow edges and you oversample hubs — so your average degree, your clustering, your everything comes out wrong.

<!--
This is why "we crawled 100,000 users" is not the same as "we sampled 100,000 users". It biases in a known direction, which is at least something.
-->

---

<!-- _class: mid -->

## Now use it on purpose

<hr>

<div class="formula">

An epidemic is starting. You have vaccine for one person in ten, and no map of who knows whom. Who do you vaccinate?

</div>

In Module 03 we took out the hubs — but that needed the whole network.

<!--
Let them flounder. Somebody will suggest asking people. That is the answer.
-->

---

## Ask them to name a friend

<hr>

<div class="fig">

![w:1080](figures/acquaintance.png)
<figcaption>pick at random, ask for one friend, vaccinate the friend</figcaption>

</div>

You never see the network. The bias finds the hubs for you, because a hub is on everybody's list.

<!--
Cohen, Havlin and ben-Avraham 2003. Nobody is asked to reveal anything except one name.
-->

---

## Try it

<hr>

<div class="cols">
<div>

Immunise one node in ten of the Internet's autonomous systems.

At random, **88%** of it stays connected. By naming a friend, **2%**.

<div class="note">

For Thursday: the gap is the variance. So how big is the variance in a real network?

</div>

</div>
<div class="fig">

![w:537](figures/immunization-curves.png)
<figcaption>random, nominated, and the fully-informed strategy that needs the map</figcaption>

</div>
</div>

<!--
Live demo: docs/lecture-note/assets/vis/vaccination-game.html. Let two students play random against nomination on the same network before showing the curves.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Five</span><span class="count">05 / 08</span></div>

## Reading the tail

We left off asking how spread out degrees really are

---

## Here is that variance

<hr>

<div class="fig">

![w:1080](figures/linear-axes.png)
<figcaption>every one of 23,133 authors, plotted by how many coauthors they have</figcaption>

</div>

Same coauthorship network as Tuesday, now with every degree on the axis.

<!--
Do not editorialise yet — let them look at it and be disappointed on the next slide.
-->

---

<!-- _class: mid -->

## What can you read off that?

<hr>

<div class="formula">

Where are the hubs? How fast do they thin out? Is there a typical number of coauthors?

</div>

<!--
None of these are answerable from that picture, which is the point.
-->

---

## Nothing — and here is why

<hr>

<div class="fig">

![w:1080](figures/fat-tail-reveal.png)
<figcaption>78% of authors sit in the first ten columns; 28 of them run out past a hundred</figcaption>

</div>

Almost everybody is tiny and a handful are enormous. That is a **fat tail**, and a linear axis cannot show both ends at once.

<!--
The tail runs to 279. On this axis those 28 authors are less than a pixel tall each.
-->

---

## Change the axes, not the data

<hr>

<div class="fig">

![w:1080](figures/loglog.png)
<figcaption>identical data, identical bins — both axes now logarithmic</figcaption>

</div>

<!--
Nothing has been recomputed. Only the ruler changed.
-->

---

## A line appears

<hr>

<div class="fig">

![w:1080](figures/loglog-line.png)
<figcaption>roughly straight over two decades of degree</figcaption>

</div>

Not perfectly straight, and not straight everywhere — but straight enough to be worth a name.

<!--
Remember the word "roughly". Part Eight comes back for it.
-->

---

## A straight line means a power law

<hr>

<div class="cols">
<div>

<div class="formula">

$$p(k) \sim k^{-\gamma}$$

</div>

A **power law**. Take logs of both sides and you get a straight line whose slope is $-\gamma$.

$\gamma$ is the one number that says how fast hubs become rare.

</div>
<div class="fig">

![w:537](figures/powerlaw-def.png)
<figcaption>steeper means hubs die out faster</figcaption>

</div>
</div>

---

<!-- _class: mid -->

## One awkward question

<hr>

<div class="formula">

That plot had bins. What happens to the picture if I choose different ones?

</div>

<!--
Nobody ever asks this and it changes everything downstream.
-->

---

## The tail changes shape

<hr>

<div class="fig">

![w:1080](figures/binning.png)
<figcaption>the same tail at three bin widths</figcaption>

</div>

Out in the tail each bin holds a handful of nodes, so the noise — and the apparent shape — is a choice you made.

<!--
None of the three is wrong. That is what makes it a problem.
-->

---

## A quantity with no bins in it

<hr>

<div class="cols">
<div>

<div class="formula">

$$\mathrm{CCDF}(k) = P(k' > k)$$

</div>

The fraction of nodes with **more** than $k$ edges. Every node contributes to it, so there is nothing to choose.

Also called the survival function.

</div>
<div class="fig">

![w:537](figures/ccdf-def.png)
<figcaption>count everybody above the line</figcaption>

</div>
</div>

---

## The same data, no choices

<hr>

<div class="fig">

![w:1080](figures/ccdf-condmat.png)
<figcaption>one point per distinct degree, and every author counted</figcaption>

</div>

<!--
Smooth where the histogram was ragged, and it did not cost anything.
-->

---

## Why not the CDF?

<hr>

<div class="fig">

![w:1080](figures/cdf-vs-ccdf.png)
<figcaption>the CDF flattens against one, and the tail vanishes into the ceiling</figcaption>

</div>

The CDF counts everybody *below* $k$ — which is almost everybody, so the interesting part is squashed against the top.

<!--
One-slide aside. Both contain the same information; only one of them shows the part you care about.
-->

---

<!-- _class: mid -->

## Is that slope $\gamma$?

<hr>

<div class="formula">

You measure a slope on the CCDF. Is that the same exponent as the one in $p(k) \sim k^{-\gamma}$?

</div>

<!--
Half the room will say yes. It is the single most common error in this material.
-->

---

## Integrate and see

<hr>

<div class="fig">

![w:1080](figures/slope-derivation.png)
<figcaption>integrating k to the minus gamma raises the exponent by one</figcaption>

</div>

$$\int_k^{\infty} x^{-\gamma}\,dx \propto k^{-(\gamma-1)} \quad\Rightarrow\quad \text{slope} = 1-\gamma$$

<!--
The CCDF is the integral of the PDF, so its exponent is one smaller. On a log-log plot that is a slope of 1 - gamma.
-->

---

## Your turn

<hr>

You measure a CCDF slope of $-1.3$. What is $\gamma$?

<div class="fig">

![w:1080](figures/slope-worksheet.png)
<figcaption>the measured slope, drawn on the data</figcaption>

</div>

<!--
Hands up for 1.3, hands up for 2.3. Count both before revealing.
-->

---

## 2.3, not 1.3

<hr>

<div class="fig">

![w:1080](figures/slope-answer.png)
<figcaption>slope minus one point three, so gamma is two point three</figcaption>

</div>

$1 - \gamma = -1.3$, so $\gamma = 2.3$. Off by one, and your network changes character completely.

<!--
Between gamma = 2 and gamma = 3 the variance diverges. That is not a rounding error, that is a different physics — and Module 03's f_c depended on it.
-->

---

## Paper exercise

<hr>

<div class="cols">
<div>

**Data Visualization** — the same distribution, drawn four ways, and one of them is lying.

Work in pairs. Twenty minutes.

</div>
<div class="fig">

![w:537](figures/exercise-card.png)
<figcaption>the handout for this part</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Six</span><span class="count">06 / 08</span></div>

## Where hubs come from

A tail that long has to be built by something

---

## Hubs

<hr>

<div class="fig">

![w:1080](figures/hubs-share.png)
<figcaption>the top 1% of Internet nodes hold 34% of all connections</figcaption>

</div>

The few nodes at the far end of the tail. They decide how fast things spread, what breaks the network, and what your crawler finds.

<!--
Sixty-five machines out of six thousand. That is what Module 03's targeted attack was aiming at.
-->

---

## Everywhere you look

<hr>

<div class="fig">

![w:1080](figures/universality.png)
<figcaption>physicists, Internet routers, and yeast proteins on one pair of axes</figcaption>

</div>

Barabási and Albert made this the founding claim of the field in 1999: unrelated systems, the same shape.

<!--
Different sizes, different mechanisms, same qualitative tail. Hold on to the word "qualitative" until Part Eight.
-->

---

<!-- _class: mid -->

## Does every network do this?

<hr>

<div class="formula">

If I wire a network up completely at random, do I get hubs?

</div>

<!--
Module 02's random graph. Ask them to predict the shape before answering.
-->

---

## Not a random one

<hr>

<div class="fig">

![w:1080](figures/poisson-ccdf.png)
<figcaption>a random network with the same average: nothing lives past a handful</figcaption>

</div>

Random wiring gives a **Poisson** distribution — everybody bunched around the mean, and hubs effectively impossible.

<!--
Same mean degree as before. The tail is not smaller, it is absent: the largest degree in that network is fifteen.
-->

---

## And a lattice is narrower still

<hr>

<div class="fig">

![w:1080](figures/three-ccdfs.png)
<figcaption>power law, random, and a lattice, on the same axes</figcaption>

</div>

Regular structures give every node the same degree — a distribution one value wide.

<!--
Module 02's ring lattice. Three networks, three shapes, and the shape is the whole difference.
-->

---

<!-- _class: mid -->

## So where do the real ones come from?

<hr>

<div class="formula">

Real networks have hubs and random ones do not. What is real networks doing that randomness is not?

</div>

<!--
Fish for "they grow" and for "popular things get more popular". You need both.
-->

---

## First ingredient: growth

<hr>

<div class="fig">

![w:1080](figures/ba-growth.png)
<figcaption>a node arrives, brings two edges, and stays</figcaption>

</div>

Networks are not wired all at once. Nodes keep arriving, and each brings a few edges with it.

<!--
Growth alone is not enough — that is the quiz in two slides' time.
-->

---

## Second ingredient: preference

<hr>

<div class="fig">

![w:1080](figures/ba-growth.gif)
<figcaption>attachment proportional to degree: the early node runs away with it</figcaption>

</div>

$$\Pi(k_i) = \frac{k_i}{\sum_j k_j}$$

<!--
Barabási-Albert, 1999. Rich get richer. Run the loop twice. The exponent that comes out is gamma = 3, which we are taking as a result rather than deriving.
-->

---

## Which is which?

<hr>

<div class="fig">

![w:1080](figures/quiz.png)
<figcaption>two networks, same size, same average degree — and their two tails</figcaption>

</div>

One grew with preference and one grew without. Vote.

<!--
Do not let anyone off with "the left one looks clumpier". Ask what in the tail tells them.
-->

---

## Preference is the whole difference

<hr>

<div class="fig">

![w:1080](figures/quiz-answer.png)
<figcaption>largest degree 315 with preference, 29 without</figcaption>

</div>

Same growth, same average degree. Take preference away and the tail is gone.

<!--
And neither ingredient works alone: uniform growth gives an exponential tail, preference on a fixed set of nodes ends up connecting everything to everything. Module 08 asks whether degree is even the right thing to prefer.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Seven</span><span class="count">07 / 08</span></div>

## Four awkward questions

Each one breaks something we just said

---

<!-- _class: mid -->

## Does it hold for **you**?

<hr>

<div class="formula">

The theorem says friends have more friends on average. Does that mean *your* friends have more friends than you?

</div>

<!--
The honest answer is no, and the gap between "on average" and "for you" is worth five minutes.
-->

---

## "On average" is not "for you"

<hr>

<div class="fig">

![w:1080](figures/individual-vs-average.png)
<figcaption>five of the eight girls below, two above, one equal — and Facebook's two percentages</figcaption>

</div>

If you are a hub it runs the other way. And whether you compare against your friends' **mean** or their **median** changes the answer for millions of people.

<!--
92.7% below the mean of their friends, but 83.6% below the median. Nine million Facebook users sit in that gap.
-->

---

<!-- _class: mid -->

## Can you kill it?

<hr>

<div class="formula">

Build me a network where nobody's friends have more friends than they do.

</div>

Open the builder and try. Two minutes.

<!--
docs/lecture-note/assets/vis/friendship-paradox-game.html. Let them fail a few times first — every irregular attempt has a positive gap.
-->

---

## Only when everyone is equal

<hr>

<div class="fig">

![w:1080](figures/vanishing.png)
<figcaption>ring, complete graph, lattice — every node the same degree, so the variance is zero</figcaption>

</div>

$\mathrm{Var}(k)=0$ is the *only* escape, and it means a network with no structure worth the name.

<!--
Which is why no real social network escapes it. Regularity is the price.
-->

---

<!-- _class: mid -->

## What about followers?

<hr>

<div class="formula">

Following on Twitter is not mutual. Does the paradox even make sense when the edges have arrows?

</div>

<!--
Two degrees now, in and out. Ask which one they think tilts.
-->

---

## Both directions tilt

<hr>

<div class="fig">

![w:1080](figures/directed.png)
<figcaption>in-degree and out-degree, counted separately on the same network</figcaption>

</div>

The accounts you follow are followed more than you are — and so are the accounts that follow you.

<!--
Hodas et al. 2013 confirm all four versions of this on Twitter. Same mechanism: you reach an account by traversing an edge, so you reach popular ones more often.
-->

---

<!-- _class: mid -->

## Same $p(k)$, same network?

<hr>

<div class="formula">

Two networks have identical degree distributions. Must they behave the same way?

</div>

<!--
Most of the room will say yes, because we have spent an hour treating p(k) as the description of a network.
-->

---

## $p(k)$ counts hubs, not who they touch

<hr>

<div class="fig">

![w:1080](figures/assortativity.png)
<figcaption>the same degrees wired three ways: hubs together, hubs apart, hubs indifferent</figcaption>

</div>

**Assortativity** measures whether high-degree nodes attach to each other. The degree distribution says nothing about it.

<!--
Same p(k) for all three. Completely different networks.
-->

---

## And it changes Module 03's answer

<hr>

<div class="fig">

![w:1080](figures/assortativity-real.png)
<figcaption>social networks positive, technological and biological negative</figcaption>

</div>

Social networks put their hubs in a core that holds together. The Internet and the cell hang leaves off hubs, so removing a hub sheds everything under it.

<!--
Facebook +0.226, coauthorship +0.134, Internet -0.182, yeast proteins -0.210. The robustness we computed in Module 03 assumed no correlation at all.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Eight</span><span class="count">08 / 08</span></div>

## Do you believe that line?

The most important slide of the module is a doubt

---

<!-- _class: mid -->

## Show of hands

<hr>

<div class="formula">

We drew a straight line through those points an hour ago and called it a power law. Does a straight line on log-log axes **prove** one?

</div>

Hands up for yes.

<!--
Count the hands. Say you are counting them. Then show the next slide.
-->

---

## This one is not a power law

<hr>

<div class="fig">

![w:1080](figures/lognormal-trap.png)
<figcaption>a power law and a log-normal, drawn on top of each other</figcaption>

</div>

One of these has no exponent at all. Straight to $R^2 = 0.99$ over three decades, and the wrong answer.

<!--
The log-normal. It arises from multiplying random factors — which is at least as plausible a story for a real network as preferential attachment.
-->

---

## So it takes a test, not an eye

<hr>

<div class="fig">

![w:1080](figures/scale-free-debate.png)
<figcaption>1999, 2011, 2019 — the claim, the doubt, and the audit</figcaption>

</div>

The paper that gave us Facebook's 92.7% also says its own degree distribution shows *substantial curvature* on these axes.

<!--
Ugander et al. 2011, in the same section we quoted for the paradox. Broido and Clauset 2019 fit 927 networks properly and find strong scale-free evidence in about 4% of them. This argument is live.
-->

---

## The shape still decides everything

<hr>

<div class="fig">

![w:1080](figures/consequences.png)
<figcaption>one distribution, three results we have already proved</figcaption>

</div>

Whatever we call the tail, how heavy it is drives robustness, distance and speed — one distribution running through the whole course.

<!--
Module 03's critical fraction, Module 02's small-world distances, and spreading speed all came out of the second moment. That is why we spent a day on it.
-->

---

## Module 04 in one page

<hr>

<div class="fig">

![w:1080](figures/recap.png)
<figcaption>eight girls, one identity, one distribution, one doubt</figcaption>

</div>

<!--
Walk it: the observation, the mechanism, the identity, the distribution, the doubt. Five sentences.
-->

---

## Coming up in Module 05

<hr>

<div class="cols">
<div>

Assortativity started asking **who** connects to whom, not just how many.

Push that far enough and the network breaks into clumps.

So: what is a community, and how would you know a real one from an accident?

</div>
<div class="fig">

![w:537](figures/m05-teaser.png)
<figcaption>two clumps, or one network and some wishful thinking?</figcaption>

</div>
</div>

<!--
Next: community detection, modularity, and the resolution limit.
-->

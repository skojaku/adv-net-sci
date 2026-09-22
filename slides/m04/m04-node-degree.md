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

<div><div class="i">01</div><div>Eight students — and a number that offends everyone</div></div>
<div><div class="i">02</div><div>Counting ends — degree, and how common each one is</div></div>
<div><div class="i">03</div><div>The exact gap — how much more, in one line</div></div>
<div><div class="i">04</div><div>Using the bias — crawlers, and finding hubs blindfolded</div></div>
<div><div class="i">05</div><div>Reading the tail — linear axes fail, log axes talk</div></div>
<div><div class="i">06</div><div>Where hubs come from — growth, and preference</div></div>
<div><div class="i">07</div><div>Three doubts — including one about the line itself</div></div>

</div>

---

<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 07</span></div>

## Eight students

And a number that offends everyone

---

## Count their friends

<hr>

How many friends does each girl have? And the average? Thirty seconds.

<div class="fig">

![w:1080](figures/feld-names.png)
<figcaption>a line joins two girls who named each other; 1961 survey, names fictitious</figcaption>

</div>

<!--
Coleman's survey asked students to name their friends; Feld 1991 reopened it. Do not confirm any number until the next slide.
-->

---

## Two and a half

<hr>

* The eight counts average **2.5 friends**.
* Betty and Tina have one. Sue and Alice have four.
* Nobody has 2.5 friends. It is an average, and another one is coming.

<div class="fig">

![w:1080](figures/feld-degrees.png)

</div>

---

## Now count theirs

<hr>

Same eight girls. Same ten lines. A different question.

Take one girl each — count her friends, then count *their* friends, and divide.

<div class="fig">

![w:1080](figures/feld-worksheet.png)

</div>

<!--
This is the whole module in one instruction. Do not answer it, do not hint, and do not say the number 3. Assign round the room: Betty, Sue, Alice, Jane, Pam, Dale, Carol, Tina. Collect all eight before showing the next slide, and ask each student out loud whether their girl came out above or below her own count.
-->

---

## Only two come out ahead

<hr>

**Red**: she beats her friends' average — only Sue and Alice. Hollow: below. Gray: equal. The eight average **2.5**, their friends **3.0**.

<div class="fig">

![w:1080](figures/feld-friendmeans.png)
<figcaption>her own count in the disc, her friends' average beside it</figcaption>

</div>

<!--
The two above are Sue and Alice — the two with four friends each. Note that out loud; it comes back in Part Seven. Feld ran the same count on all 146 girls in that school and the gap held: eighty below, forty-one above, twenty-five equal.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 07</span></div>

## Counting ends

Before we explain it, we have to be able to count it

---

<!-- _class: mid -->

## Degree

<hr>

<div class="cols">
<div>

A node's **degree** is the number of edges attached to it. *Now add all eight degrees together — shout the total.*

</div>
<div class="fig">

![w:537](figures/degree-def.png)
<figcaption>every other node in this drawing has degree one</figcaption>

</div>
</div>

<!--
Let them add: 1 + 4 + 4 + 2 + 3 + 3 + 2 + 1 = 20. Ask for the number before you ask for the reason.
-->

---

## Count the ends instead

<hr>

<div class="fig">

![w:1080](figures/sum-ends.png)

</div>

* Two ends per edge: $\sum_i k_i = 2M$, so $\langle k\rangle = 2M/N = 20/8 = 2.5$.
* An even total means **odd** degrees come in pairs — never exactly three.

<!--
Ten friendships, twenty ends, and 2M comes back in Part Three as the denominator of q(k). The last bullet is the handshaking lemma, and it is what was quietly doing the work in Module 01: Euler's condition said zero or two odd-degree nodes, never one, never three.
-->

---

<!-- _class: mid -->

## How common is each degree?

<hr>

<div class="cols">
<div>

$p(k)$ is the fraction of nodes whose degree is exactly $k$ — the **degree distribution**.

One number per degree, and it describes the whole network without naming anybody.

</div>
<div class="fig">

![w:537](figures/pk-def.png)
<figcaption>the fractions add to one, and always will</figcaption>

</div>
</div>

<!--
Our eight girls sit two at each of one, two, three and four friends — about as flat as a degree distribution gets, which is why the gap here is small. Real networks are not this polite; Part Five shows one.
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

## Hubs are on everybody’s list

<hr>

**Red**: Sue and Alice, on four lists each. <span class="accent">Blue</span>: Betty and Tina, on one.

<div class="fig">

![w:1080](figures/rosters.png)
<figcaption>eight lists, twenty names between them</figcaption>

</div>

* When you average over *friends*, you are averaging over the lists — and a popular girl is on many lists.

<!--
This is the mechanism. Everything after this is turning it into a number.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 07</span></div>

## The exact gap

Not “more” — how much more

---

<!-- _class: mid -->

## How much more?

<hr>

<div class="formula">

We know *why* friends have more friends. Can we say **how many** more, for any network at all?

</div>

Thirty seconds with your neighbour first.

<!--
The answer is one line long and it holds for every graph that has ever existed. Build to it.
-->

---

<!-- _class: mid -->

## A hub has more hands in the bag

<hr>

<div class="cols">
<div>

You pick a friend by picking one of the $2M = 20$ **ends**, not a person — so the chance it belongs to a girl of degree $k$ goes like $k\,p(k)$:

<div class="formula">

$$q(k) = \frac{k\,p(k)}{\langle k\rangle}$$

</div>

</div>
<div class="fig">

![w:537](figures/qk-formula.png)
<figcaption>q(k) is a share of hands, not a share of girls</figcaption>

</div>
</div>

<!--
q(k), not p(k). This is the whole trick, and it is the same q(k) that told us which node an attack finds in Module 03.
-->

---

## The whole paradox, in one line

<hr>

<div class="fig">

![w:1080](figures/derivation-4.png)
<figcaption>nothing in these four lines is an approximation</figcaption>

</div>

* $\mathrm{Var}(k) \ge 0$, so the gap is never negative — **every network** has it.

<!--
Line two names the second moment, and line three splits it into the mean squared plus the variance. Say "second moment" out loud; it comes back in Part Five as the thing that diverges. The non-negativity is the strongest sentence in the module: not a tendency, an identity — equality needs every node at the same degree. Feld writes the last line out himself, on page 1470, and it closes on his full 146-girl data: 2.6575 + 0.6981 = 3.3557.
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
<figcaption>predict before you count — half the room expects a gap on the ring</figcaption>

</div>

Spread the degrees out and the paradox grows. Flatten them and it disappears entirely.

<!--
And now the obvious next question, which is the cliffhanger for the whole of day two: how spread out are the degrees in a real network?
-->

---

<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 07</span></div>

## Using the bias

It is not a curiosity. It is a tool

---

## Only about friendship?

<hr>

<div class="fig">

![w:1080](figures/coauthor-gap.png)
<figcaption>23,133 physicists, and the same identity as the eight girls</figcaption>

</div>

No. Prolific collaborators appear on many author lists — same identity, same reason.

<!--
Ask for three examples from the room before you show the figure. arXiv condensed-matter coauthorship. It holds at planetary scale too: Ugander et al. 2011, 721 million Facebook users, median friend count 99 against 635 at the end of a random edge; Hodas et al. 2013 for Twitter.
-->

---

## Everything tilts

<hr>

You built your dataset by crawling — start somewhere, follow the links, keep going. What did you collect?

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

Thirty seconds with your neighbour: you cannot see the network, so what *can* you ask?

<!--
Let them flounder. Somebody will suggest asking people. That is the answer.
-->

---

## Vaccinate the friend, not the volunteer

<hr>

<div class="fig">

![w:1080](figures/acquaintance-3.png)
<figcaption>pick at random, ask for one name, immunise the name</figcaption>

</div>

* The bias finds the hubs for you — a hub is on everybody's list.
* *Hands up: random, or nominated? And by how much?*

<!--
Cohen, Havlin and ben-Avraham 2003. Nobody reveals anything except one name. Live demo: lecture-note/assets/vis/vaccination-game.html — let two students play random against nomination before you show the curves, and make the room commit to a margin out loud.
-->

---

## Nominated wins, and not by a little

<hr>

<div class="cols">
<div>

Immunise one node in ten of the Internet's autonomous systems.

* The whole difference is one question per person, and nobody names more than one friend.
* *The gap is the variance — so how big is the variance in a real network?*

</div>
<div class="fig">

![w:537](figures/immunization-curves.png)
<figcaption>the third strategy needs the whole map; nomination needs one question</figcaption>

</div>
</div>

<!--
Compare the curves against whatever margin the room guessed. The third curve needs the full map, and nomination gets most of the way there for one question per person.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Five</span><span class="count">05 / 07</span></div>

## Reading the tail

We left off asking how spread out degrees really are

---

## Here is that gap

<hr>

<div class="fig">

![w:1080](figures/linear-axes.png)
<figcaption>a fat tail, before we knew to call it one</figcaption>

</div>

* *Where are the hubs? Is there a typical number of coauthors? Thirty seconds.*

<!--
The same coauthorship network, now with every degree on the axis. None of those questions is answerable from this picture, which is the point — let them be disappointed before the next slide says why.
-->

---

## Nothing — and here is why

<hr>

<div class="fig">

![w:1080](figures/fat-tail-reveal.png)
<figcaption>everything interesting is squashed into the first inch</figcaption>

</div>

Almost everybody is tiny and a handful are enormous. That is a **fat tail**, and a linear axis cannot show both ends at once.

<!--
The tail runs to 279. On this axis those 28 authors are less than a pixel tall each.
-->

---

## A line appears

<hr>

<div class="fig">

![w:1080](figures/loglog-line.png)
<figcaption>identical data on logarithmic axes — roughly straight over two decades</figcaption>

</div>

* A straight line here means a **power law**, $p(k) \sim k^{-\gamma}$, of slope $-\gamma$.

<!--
Nothing was recomputed; only the ruler changed. Gamma is the one number that says how fast hubs become rare. Remember the word "roughly" — Part Seven comes back for it.
-->

---

## Every point came out of a bin

<hr>

<div class="fig">

![w:1080](figures/binning-1.png)
<figcaption>the choice we made without noticing we were making it</figcaption>

</div>

* One bucket per degree — a width nobody chose. *What if I pick another?*

<!--
Out in the tail most bins hold one author, or none, which is where the scatter comes from. Nobody ever asks this and it changes everything downstream.
-->

---

## The shape was a choice

<hr>

<div class="fig">

![w:1080](figures/binning-3.png)
<figcaption>same data, same window, a bin width that moves the fitted slope</figcaption>

</div>

* Widen the bins and the scatter cleans up, because each bucket holds more nodes — divide by the width and the heights stay comparable.
* The fitted slope moves with the width. Out in the tail the apparent shape is a choice you made, and neither choice is wrong.

<!--
Bin width alone moves this network across the gamma = 3 boundary. None of the widths is wrong, and that is what makes it a problem.
-->

---

<!-- _class: mid -->

## The same data, no choices

<hr>

The fraction of nodes **above** $k$: $\mathrm{CCDF}(k) = P(k' > k)$. No bins.

<div class="fig">

![w:1080](figures/ccdf-condmat.png)
<figcaption>every node counted at every k; also called the survival function</figcaption>

</div>

<!--
Smooth where the histogram was ragged, and it did not cost anything. The CDF counts everybody below k, which is almost everybody, so its tail squashes against the ceiling — that is why we plot the complement.
-->

---

<!-- _class: mid -->

## Integrate and see

<hr>

<div class="fig">

![w:1080](figures/slope-derivation.png)
<figcaption>integrating k to the minus gamma raises the exponent by one</figcaption>

</div>

* *Hands up: a CCDF slope of $-1.3$ — is $\gamma$ 1.3, or 2.3?* It is **2.3**.

<!--
Integrating k^-gamma gives k^(1-gamma): the exponent moves UP by one, which is the shallower slope you measure. Count both sets of hands before you reveal. The exponent you report is not the slope you measured, and off by one your network changes character: between gamma = 2 and gamma = 3 the variance diverges — not a rounding error, a different physics, and Module 03's f_c depended on it.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Six</span><span class="count">06 / 07</span></div>

## Where hubs come from

A tail that long has to be built by something

---

## Everywhere you look

<hr>

<div class="fig">

![w:1080](figures/universality.png)
<figcaption>hold on to the word qualitative until Part Seven</figcaption>

</div>

Barabási and Albert made this the founding claim of the field in 1999: unrelated systems, the same shape.

<!--
Different sizes, different mechanisms, same qualitative tail. Hold on to the word "qualitative" until Part Seven.
-->

---

## Not a random one

<hr>

<div class="fig">

![w:1080](figures/poisson-ccdf.png)
<figcaption>the tail is not smaller here — it is absent</figcaption>

</div>

Random wiring gives a **Poisson** distribution — everybody bunched around the mean, and hubs effectively impossible.

<!--
Wire a network up completely at random — Module 02's graph — and ask them to predict the shape before you reveal it. Same mean degree as before. The tail is not smaller, it is absent: the largest degree in that network is twenty-eight, against the physicists' 279.
-->

---

<!-- _class: mid -->

## So where do the real ones come from?

<hr>

<div class="formula">

Real networks have hubs and random ones do not. What are real networks doing that randomness is not?

</div>

Thirty seconds with your neighbour, then shout your best guess.

<!--
Fish for "they grow" and for "popular things get more popular". You need both.
-->

---

## Growth, then preference

<hr>

<div class="fig">

![w:1080](figures/ba-growth.gif)
<figcaption>attachment proportional to degree: the early node runs away with it</figcaption>

</div>

$$\Pi(k_i) = \frac{k_i}{\sum_j k_j}$$

<!--
Networks are not wired all at once: nodes keep arriving, each bringing a few edges, and each new edge prefers a node that already has many. Barabási-Albert, 1999. Rich get richer. Run the loop twice. The exponent that comes out is gamma = 3, which we take as a result rather than deriving. Neither ingredient works alone: uniform growth gives an exponential tail, and preference on a fixed set of nodes ends up connecting everything to everything.
-->

---

## Which is which?

<hr>

<div class="fig">

![w:1080](figures/quiz.png)
<figcaption>two networks, same average degree, and their two tails</figcaption>

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
<figcaption>same growth, same average degree, and only one of them has hubs</figcaption>

</div>

Take preference away and the tail is gone.

<!--
And neither ingredient works alone: uniform growth gives an exponential tail, preference on a fixed set of nodes ends up connecting everything to everything. Module 08 asks whether degree is even the right thing to prefer.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Seven</span><span class="count">07 / 07</span></div>

## Three doubts

Each one breaks something we just said

---

## “On average” is not “for you”

<hr>

*Hands up if your friends have more friends than you do.* If you are a hub it runs the other way: Sue and Alice beat theirs.

<div class="fig">

![w:1080](figures/individual-vs-average.png)
<figcaption>the theorem is about the average, and Sue is not the average</figcaption>

</div>

* It also matters whether you score yourself against your friends' **mean** or their **median**: on Facebook, 92.7% are below the mean and 83.6% below the median — 66 million people sit between the two.

<!--
The theorem is a statement about the average, not about any one person. The two above the line are the two with four friends each — name them. Ugander et al. 2011, 721 million users: one hub in your friend list drags the mean up and leaves the median alone.
-->

---

## $p(k)$ counts hubs, not who they touch

<hr>

<div class="fig">

![w:1080](figures/assortativity.png)
<figcaption>swap two edges and r moves; p(k) does not</figcaption>

</div>

* *Same $p(k)$?* **Assortativity** $r$ says whether hubs attach to each other.

<!--
Same p(k) for all three, completely different networks. Social hubs sit in a core that holds together (Facebook +0.226, coauthorship +0.134); technological and biological hubs carry leaves (Internet -0.182, yeast proteins -0.210), so removing one takes the leaves with it. The robustness we computed in Module 03 assumed all four were zero.
-->

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
<figcaption>multiply enough random factors together and you get the red one</figcaption>

</div>

One of these has no exponent at all. Straight to $R^2 = 0.99$ across 2.3 decades, and the wrong answer.

<!--
The log-normal. It arises from multiplying random factors — which is at least as plausible a story for a real network as preferential attachment.
-->

---

<!-- _class: mid -->

## So it takes a test, not an eye

<hr>

<div class="fig">

![w:1080](figures/scale-free-debate.png)
<figcaption>twenty years on, and the argument is still open</figcaption>

</div>

Facebook’s own paper calls its tail *substantially curved*.

* And so does ours: $p(k)$ gives $\gamma = 2.44$, so the rule predicts a CCDF slope of $-1.44$. It measures $-2.57$. One tail, two answers.

<!--
Ugander et al. 2011, in the same section we quoted for the paradox. Broido and Clauset 2019 fit 927 networks properly and find strong scale-free evidence in about 4% of them. This argument is live.

The two exponents are the point of the fragment, so be ready for "which one is right?": neither. A clean power law returns the same gamma whichever curve you fit, and the +1 rule from Part Five is exactly the statement that it should. -2.44 is the slope printed on "A line appears"; the CCDF fit is -2.5715 over 10 <= k <= 200 (R^2 = 0.976), so the rule predicts the two slopes differ by one and they differ by about 0.13. Part of that is the fit window moving, which is itself the tell: a real power law has no preferred window.
-->

---

<!-- _class: mid -->

## Module 04 in one page

<hr>

<div class="fig">

![w:1080](figures/recap.png)
<figcaption>left to right, the order we met them</figcaption>

</div>

One observation about eight girls, pushed until it became a distribution — and whatever we call that tail, how heavy it is drives robustness, distance and speed.

<!--
Walk it: the observation, the mechanism, the identity, the distribution, the doubt. Module 03's critical fraction, Module 02's small-world distances, and spreading speed all came out of the second moment.
-->

---

<!-- _class: mid -->

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

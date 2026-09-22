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

<div class="sub">one number per node, and the shape they make</div>

<div class="credit">Sadamori Kojaku · Binghamton University</div>

<!--
The paradox is done; this half is the distribution it turned into. Two reminder slides, then the vaccine game.
-->

---
## Roadmap for today

<hr>

<div class="steps-list">

<div><div class="i">01</div><div>Where we left off — degree, and the paradox in one line</div></div>
<div><div class="i">02</div><div>Using the bias — the vaccine game, and what it finds</div></div>
<div><div class="i">03</div><div>Reading the tail — how a distribution is drawn, and how it misleads</div></div>
<div><div class="i">04</div><div>Where hubs come from — growth, and preference</div></div>
<div><div class="i">05</div><div>Three doubts — including one about the line itself</div></div>

</div>

---
<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 05</span></div>

## Where we left off

Two slides, and then we move on

---
<!-- _class: mid -->

## Degree

<hr>

<div class="cols">
<div>

A node's **degree** $k_i$ is the number of edges attached to it.

Every edge has two ends, so $\sum_i k_i = 2M$ and $\langle k\rangle = 2M/N$.

</div>
<div class="fig">

![w:537](figures/degree-def.png)
<figcaption>every other node in this drawing has degree one</figcaption>

</div>
</div>

---
## Why a friend's degree beats yours

<hr>

<div class="fig">

![w:1080](figures/derivation-4.png)
<figcaption>q(k) is the chance an edge end belongs to a node of degree k</figcaption>

</div>

<!--
Read the four lines out. Nothing on this slide is new: Module 04's first half derived it. Line 1 substitutes q(k) = k p(k) / <k>, line 2 names the second moment, line 3 is the definition of variance rearranged, line 4 is the theorem. Var(k) >= 0, so the gap is never negative.
-->

---
<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 05</span></div>

## Using the bias

It is not a curiosity. It is a tool

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
## The vaccine game

<hr>

<div class="formula">

lecture-note/assets/vis/vaccination-game.html

</div>

<!--
Vaccine for one node in ten, and no map of who knows whom. Two students play it on the same network: one immunises people picked at random, the other picks somebody at random, asks for the name of one friend, and immunises the friend. Do not name acquaintance sampling before they find it. Cohen, Havlin and ben-Avraham 2003. Make the room commit to a margin out loud before the next slide.
-->

---
## Nominated wins, and not by a little

<hr>

<div class="fig">

![w:1080](figures/immunization-curves.png)
<figcaption>one node in ten of the Internet's autonomous systems</figcaption>

</div>

---
<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 05</span></div>

## Reading the tail

First, how a distribution gets drawn at all

---
## Twenty nodes

<hr>

<div class="fig">

![w:1080](figures/hist-degrees.png)
<figcaption>small enough to count, and we keep them for the rest of this part</figcaption>

</div>

* *Draw me the picture. Two minutes, on paper.*

---
## A bar for each degree

<hr>

Divide every height by 20 and this is $p(k)$, the **degree distribution**.

<div class="fig">

![w:1080](figures/hist-bars.png)
<figcaption>bars touch: nothing lives between k = 3 and k = 4</figcaption>

</div>

---
## Now the bins are not equal

<hr>

<div class="fig">

![w:1080](figures/hist-rebin.png)
<figcaption>one bin of width 1, one of width 2, one of width 4</figcaption>

</div>

* *Is $k = 4$ really almost as common as $k = 1$? Hands up.*

---
## Area, not height

<hr>

Divide each count by its bin width, and the bar's **area** is the count again.

<div class="fig">

![w:1080](figures/hist-area.png)
<figcaption>same twenty nodes, same bins, two readings</figcaption>

</div>

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
Nothing was recomputed; only the ruler changed. Gamma is the one number that says how fast hubs become rare. Remember the word "roughly" — Part Five comes back for it.
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
## Count upward instead

<hr>

<div class="fig">

![w:1080](figures/hist-cumulative.png)
<figcaption>twenty nodes is one, so a running total is a share</figcaption>

</div>

* Nothing here has a width: every node is counted at every $k$.

---
## Or count from the top

<hr>

<div class="fig">

![w:1080](figures/ccdf-def.png)
<figcaption>the same twenty nodes, cut at k = 3</figcaption>

</div>

* $\mathrm{CCDF}(k) = P(k' > k)$: the fraction **above** $k$, and no bins at all.

---
<!-- _class: mid -->

## The same data, no choices

<hr>

The same quantity, on all 23,133 authors.

<div class="fig">

![w:1080](figures/ccdf-condmat.png)
<figcaption>every node counted at every k; also called the survival function</figcaption>

</div>

<!--
Smooth where the histogram was ragged, and it did not cost anything — the same construction as the twenty toy nodes, 23,133 times over. The CDF counts everybody below k, which is almost everybody, so its tail squashes against the ceiling; that is why we plot the complement.
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

<div class="band"><span>Part Four</span><span class="count">04 / 05</span></div>

## Where hubs come from

A tail that long has to be built by something

---
## Everywhere you look

<hr>

<div class="fig">

![w:1080](figures/universality.png)
<figcaption>hold on to the word qualitative until Part Five</figcaption>

</div>

Barabási and Albert made this the founding claim of the field in 1999: unrelated systems, the same shape.

<!--
Different sizes, different mechanisms, same qualitative tail. Hold on to the word "qualitative" until Part Five.
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

<div class="band"><span>Part Five</span><span class="count">05 / 05</span></div>

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

The two exponents are the point of the fragment, so be ready for "which one is right?": neither. A clean power law returns the same gamma whichever curve you fit, and the +1 rule from Part Three is exactly the statement that it should. -2.44 is the slope printed on "A line appears"; the CCDF fit is -2.5715 over 10 <= k <= 200 (R^2 = 0.976), so the rule predicts the two slopes differ by one and they differ by about 0.13. Part of that is the fit window moving, which is itself the tell: a real power law has no preferred window.
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

---
marp: true
theme: network-science
paginate: true
math: katex
---

<!-- _class: lead -->

<div class="eyebrow">Graduate Lecture · Fall 2026</div>

# Network Science

---

<div class="sub">Structure, dynamics, and the mathematics of connected systems</div>

<div class="credit">Instructor name · Course code</div>

<!--
Welcome. One long lecture, six parts: graphs as a language, random models, small worlds, scale-free structure, position and groups, then dynamics on top of structure.
-->

---

## Roadmap for the lecture

---

<div class="cols">

<div>

**01 Graphs as a language**
<div class="note">Degree, paths, components, clustering</div>

</div>
<div>

**02 Random networks**
<div class="note">The null model and its failures</div>

</div>
<div>

**03 Small worlds**
<div class="note">Short paths with high clustering</div>

</div>
<div>

**04 Scale-free networks**
<div class="note">Power laws, hubs, preferential attachment</div>

</div>
<div>

**05 Position and groups**
<div class="note">Centrality, PageRank, communities</div>

</div>
<div>

**06 Robustness and spreading**
<div class="note">Percolation, epidemics, immunization</div>

</div>

</div>

<!--
Six parts. The first three are the classical models; the last three are what you do with a network once you have one.
-->

---

<!-- _class: part -->

<div class="band"><span>Part One</span><span class="count">01 / 06</span></div>

## Graphs as a language

The handful of definitions every later result is built out of

<!--
Part one is vocabulary, but the vocabulary does real work: each quantity we define is a hypothesis about what matters in a system.
-->

---

## What counts as a network

---

| System | Node | Link | Directed |
| --- | --- | --- | --- |
| Internet | Router | Physical cable | No |
| World Wide Web | Page | Hyperlink | <span class="accent-2">Yes</span> |
| Cell | Protein | Binding interaction | No |
| Science | Paper | Citation | <span class="accent-2">Yes</span> |
| Power grid | Station | Transmission line | No |

<div class="note">

The same system admits several encodings. Choosing one is a modeling decision, and it is usually the decision that determines the answer.

</div>

<!--
The move is always the same: decide what a node is, decide what a link means. Most of the difficulty in applied work is right here, not in the math.
-->

---

## Nodes, links, and the adjacency matrix

---

<div class="cols">
<div>

A graph is a node set and a link set. Store it as a matrix and all of linear algebra becomes available to you.

<div class="formula">

$$ A_{ij} = \begin{cases} 1 & \text{if } i \sim j \\ 0 & \text{otherwise} \end{cases} $$

</div>

<div class="note">

Undirected graphs give a symmetric matrix with a zero diagonal. Powers of the matrix count walks: $(A^n)_{ij}$ is the number of walks of length $n$ from $i$ to $j$.

</div>

</div>
<div class="fig">

![w:520](figures/adjacency.svg)
<figcaption>a five-node graph and its matrix</figcaption>

</div>
</div>

---

## Degree, average degree, density

---

<div class="formula">

$$ k_i = \sum_{j} A_{ij} \qquad \langle k \rangle = \frac{2L}{N} \qquad d = \frac{2L}{N(N-1)} $$

</div>

<div class="cols">
<div>

The factor of two is the whole trick: every link contributes to two degrees, so the degree sum double-counts the links.

</div>
<div>

Real networks sit at the very bottom of the density range. The web has billions of pages and an average degree in the tens.

</div>
</div>

<!--
Average degree is the first number you compute. Density says how far from complete the graph is; real networks are overwhelmingly sparse, which is why we can compute on them at all.
-->

---

## Directed and weighted networks

---

<div class="cols">
<div>

### Directed

The matrix is no longer symmetric. Every node carries two degrees, and the two averages coincide.

<div class="formula">

$$ \langle k^{in} \rangle = \langle k^{out} \rangle = \frac{L}{N} $$

</div>

<div class="note">

Reachability splits into in- and out-components, which is why the web has a bow-tie shape rather than one blob.

</div>

</div>
<div>

### Weighted

Entries become strengths: call volume, traffic, synaptic efficacy.

<div class="formula">

$$ s_i = \sum_{j} w_{ij} $$

</div>

<div class="note">

Weights are broadly distributed too, so thresholding a weighted network into a binary one throws away most of the signal.

</div>

</div>
</div>

---

## Paths, distance, and diameter

---

<div class="cols">
<div>

The distance $d_{ij}$ is the number of links on a shortest path. Average over all pairs and you get the characteristic path length.

<div class="formula">

$$ \langle d \rangle = \frac{1}{N(N-1)} \sum_{i \neq j} d_{ij} $$

</div>

<div class="note">

The diameter $d_{max}$ is the largest of these distances. Both come out of one breadth-first search per node.

</div>

</div>
<div class="fig">

![w:560](figures/shortest-path.svg)
<figcaption>d = 3 between i and j</figcaption>

</div>
</div>

<!--
Distance is measured in hops. Diameter is the worst case; average path length is the number people quote. Breadth-first search gives you both.
-->

---

## Connected components

---

A component is a maximal set of mutually reachable nodes. Real networks almost always show one giant component plus a scatter of small isolates.

<div class="fig">

![w:1000](figures/components.svg)
<figcaption>one giant component, several small ones</figcaption>

</div>

<!--
Most real networks have one giant component holding the large majority of nodes, plus a scatter of small ones. That is not an accident, and part two explains why.
-->

---

## Clustering coefficient

---

<div class="cols">
<div>

Of the links that could exist among node $i$'s neighbours, what fraction do exist?

<div class="formula">

$$ C_i = \frac{2 L_i}{k_i (k_i - 1)} $$

</div>

<div class="note">

Here $L_i$ counts links among the $k_i$ neighbours. Averaging over nodes gives $\langle C \rangle$, which in social networks lands between 0.1 and 0.6 and stays roughly independent of size.

</div>

</div>
<div class="fig">

![w:460](figures/clustering.svg)
<figcaption>C = 2/6 = 0.33</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Two</span><span class="count">02 / 06</span></div>

## Random networks

The null model, and the specific ways it fails

<!--
The random graph is wrong about almost every real network, which is exactly what makes it useful: deviations from it are the findings.
-->

---

## The Erdős–Rényi model

---

Take $N$ labelled nodes and connect each of the $\binom{N}{2}$ possible pairs independently with probability $p$. Nothing else is specified, so anything the model produces is a consequence of randomness alone.

<div class="cols">
<div class="formula">

<span class="hand">expected links</span>

$$ \langle L \rangle = p \binom{N}{2} $$

</div>
<div class="formula">

<span class="hand">expected degree</span>

$$ \langle k \rangle = p (N-1) $$

</div>
</div>

<div class="note">

To hold $\langle k \rangle$ fixed as the network grows, $p$ must shrink like $1/N$. Sparseness is built into the limit we care about.

</div>

---

## From binomial to Poisson

---

<table class="steps">
<tr><td>Exact</td><td>

$$ p_k = \binom{N-1}{k} p^k (1-p)^{N-1-k} $$

</td></tr>
<tr><td>Sparse limit</td><td>

$$ p_k = e^{-\langle k \rangle} \frac{\langle k \rangle^k}{k!} $$

</td></tr>
<tr><td>Spread</td><td>

$$ \sigma_k = \langle k \rangle^{1/2} $$

</td></tr>
</table>

The relative width falls off as $\langle k \rangle^{-1/2}$, so large random networks are strikingly uniform: nodes many times the average degree are effectively impossible.

<!--
The exact answer is binomial; in the sparse large-N limit it collapses to a Poisson with a single parameter. The key consequence is the narrow peak.
-->

---

## The giant component

---

<div class="cols">
<div>

Let $S$ be the fraction of nodes in the largest component. Self-consistency gives an implicit equation with a transition at one link per node.

<div class="formula">

$$ S = 1 - e^{-\langle k \rangle S} $$

</div>

<div class="note">

Below $\langle k \rangle = 1$ the only solution is $S = 0$. Above it a positive branch appears, and by $\langle k \rangle = \ln N$ essentially every node is absorbed.

</div>

</div>
<div class="fig">

![w:560](figures/giant-component.svg)
<figcaption>a phase transition at &lt;k&gt; = 1</figcaption>

</div>
</div>

---

## Where the random model breaks down

---

| Property | Random graph | Real networks | Verdict |
| --- | --- | --- | --- |
| Path length | Logarithmic in $N$ | Logarithmic or shorter | Close |
| Degree spread | Poisson, narrow | Heavy-tailed, hubs | <span class="accent-2">Wrong</span> |
| Clustering | $C = \langle k \rangle / N \to 0$ | Large, size-independent | <span class="accent-2">Wrong</span> |
| Growth | Fixed $N$ | Nodes arrive over time | <span class="accent-2">Missing</span> |

<div class="note">

Two of these failures set the agenda: clustering leads to small-world models, degree spread leads to scale-free ones.

</div>

---

<!-- _class: part -->

<div class="band"><span>Part Three</span><span class="count">03 / 06</span></div>

## Small worlds

How a network can be both locally dense and globally shallow

---

## Six degrees of separation

---

<div class="stats">
<div>
<div class="n">5.2</div>
<div class="cap">median chain length in Milgram's completed letter experiment, 1967</div>
</div>
<div>
<div class="n">4.7</div>
<div class="cap">average distance among 721 million Facebook users, 2011</div>
</div>
<div>
<div class="n">19</div>
<div class="cap">estimated diameter of the reachable web, measured on directed links</div>
</div>
</div>

<div class="note">

The striking part is not the size of the number but its stability. Multiply the population by a thousand and the distance grows by roughly one hop.

</div>

---

## Why random graphs are small

---

Walk outward from any node. At distance $d$ you have reached roughly $\langle k \rangle^d$ nodes, so the whole network is covered once that product reaches $N$.

<div class="cols">
<div class="formula">

<span class="hand">reach at distance d</span>

$$ N(d) \approx 1 + \langle k \rangle + \cdots + \langle k \rangle^d $$

</div>
<div class="formula">

<span class="hand">set equal to N</span>

$$ \langle d \rangle \approx \frac{\ln N}{\ln \langle k \rangle} $$

</div>
</div>

A logarithm is a very slow function. With $\langle k \rangle = 100$, going from a thousand nodes to a billion moves the average distance from about 1.5 to about 4.5.

---

## The Watts–Strogatz model

---

Begin with a ring lattice, which has high clustering and long paths. Rewire each link with probability $p$ and interpolate toward a random graph.

<div class="cols3">
<div class="fig">

![w:250](figures/ws-p0.svg)
<figcaption>p = 0 · high C, long paths</figcaption>

</div>
<div class="fig">

![w:250](figures/ws-pmid.svg)
<figcaption>small p · high C, short paths</figcaption>

</div>
<div class="fig">

![w:250](figures/ws-p1.svg)
<figcaption>p = 1 · low C, short paths</figcaption>

</div>
</div>

<!--
Start from a ring lattice, rewire a small fraction of links at random. A handful of shortcuts destroys the long paths while leaving local structure intact.
-->

---

## Clustering and path length together

---

<div class="cols">
<div>

Path length falls off at a much smaller rewiring probability than clustering does. Between the two curves lies a wide band where the network is simultaneously clustered and shallow.

<div class="note">

The model does not, however, produce hubs. Its degree distribution stays narrow, which is what part four takes up.

</div>

</div>
<div class="fig">

![w:520](figures/ws-curves.svg)
<figcaption>C(p) and L(p)</figcaption>

</div>
</div>

---

<!-- _class: part -->

<div class="band"><span>Part Four</span><span class="count">04 / 06</span></div>

## Scale-free networks

Why hubs appear, and why the average degree stops being a useful summary

---

## Power-law degree distributions

---

<div class="cols">
<div>

<div class="formula">

$$ p_k \sim k^{-\gamma} $$

</div>

Most measured networks land in the range $2 < \gamma < 3$. The tail decays slowly enough that a node with a thousand times the average degree is unremarkable.

<div class="note">

In the Poisson case the factorial in the denominator makes such a node impossible.

</div>

</div>
<div class="fig">

![w:560](figures/power-law.svg)
<figcaption>power law vs Poisson</figcaption>

</div>
</div>

---

## Reading a log-log plot

---

<div class="cols">
<div>

<div class="formula">

$$ \ln p_k = -\gamma \ln k + c $$

</div>

A straight line on log axes, with slope $-\gamma$. That is the entire diagnostic.

<div class="note">

Two cautions: use logarithmic binning or the cumulative distribution, and fit by maximum likelihood rather than by eye.

</div>

</div>
<div class="fig">

![w:520](figures/loglog.svg)
<figcaption>a measured degree distribution</figcaption>

</div>
</div>

---

## Divergent moments

---

<div class="formula">

$$ \langle k^n \rangle = \int_{k_{min}}^{\infty} k^{n} k^{-\gamma} \, dk = \frac{k_{max}^{n-\gamma+1} - k_{min}^{n-\gamma+1}}{n - \gamma + 1} $$

</div>

<div class="cols">
<div>

The integral converges only when $n < \gamma - 1$. For $2 < \gamma < 3$ the mean is finite but the second moment grows without bound as the network grows.

</div>
<div>

A distribution with no finite variance has no characteristic scale, which is where the name comes from. Reporting an average degree is then close to meaningless.

</div>
</div>

<div class="note">

Keep this result in your pocket. It is the reason scale-free networks resist random damage and the reason epidemic thresholds vanish on them.

</div>

---

## Growth and preferential attachment

---

<div class="cols">
<div>

### Growth

At every step one node arrives with $m$ links. The network has a history, and early nodes have more time to accumulate links.

</div>
<div>

### Preferential attachment

The new node picks targets in proportion to their current degree.

<div class="formula">

$$ \Pi(k_i) = \frac{k_i}{\sum_j k_j} $$

</div>

</div>
</div>

<div class="note">

Neither ingredient works alone. Growth with uniform attachment produces an exponential tail; preferential attachment on a fixed node set eventually funnels every link into a single hub.

</div>

---

## Deriving the exponent

---

<table class="steps">
<tr><td>Rate equation</td><td>

$$ \frac{dk_i}{dt} = m \frac{k_i}{\sum_j k_j} = \frac{k_i}{2t} $$

</td></tr>
<tr><td>Integrate</td><td>

$$ k_i(t) = m \left( \frac{t}{t_i} \right)^{1/2} $$

</td></tr>
<tr><td>Invert</td><td>

$$ p_k \sim k^{-3} $$

</td></tr>
</table>

<!--
Continuum derivation. Degrees grow as the square root of time, and the exponent comes out at three independently of m. Real networks show a range of exponents, so treat this as a mechanism rather than a fit.
-->

---

## The ultra-small world

---

Hubs are shortcuts. Routing through them makes distances shorter than the random-graph logarithm, with the scaling depending on the exponent.

| | | |
| --- | --- | --- |
| $\gamma = 2$ | $\langle d \rangle \sim \text{const}$ | a single hub touches nearly everything |
| $2 < \gamma < 3$ | $\langle d \rangle \sim \ln \ln N$ | ultra-small: the regime most real networks occupy |
| $\gamma = 3$ | $\langle d \rangle \sim \ln N / \ln \ln N$ | the Barabási–Albert borderline |
| $\gamma > 3$ | $\langle d \rangle \sim \ln N$ | hubs too rare to matter; back to small-world scaling |

---

<!-- _class: part -->

<div class="band"><span>Part Five</span><span class="count">05 / 06</span></div>

## Position and groups

Centrality, ranking, and the intermediate scale between node and network

---

## Four centrality measures

---

| Measure | Definition | Answers |
| --- | --- | --- |
| Degree | $k_i$ | how many direct contacts |
| Closeness | $\left( \sum_j d_{ij} \right)^{-1}$ | how fast something reaches everyone |
| Betweenness | $\sum \sigma_{st}(i) / \sigma_{st}$ | how much traffic must pass through |
| Eigenvector | $\lambda x_i = \sum_j A_{ij} x_j$ | how well connected the contacts are |

<div class="note">

These rankings routinely disagree, and the disagreement is informative: a low-degree node with high betweenness is a broker.

</div>

---

## Betweenness and bridges

---

<div class="cols">
<div>

Degree is local; betweenness is not. A node with two links can still carry every path between two dense regions.

<div class="note">

Removing the bridge here leaves every node's degree nearly unchanged and disconnects the network. This is the gap between local and structural importance.

</div>

</div>
<div class="fig">

![w:560](figures/bridge.svg)
<figcaption>k = 2, highest betweenness</figcaption>

</div>
</div>

---

## PageRank

---

<div class="formula">

$$ x_i = \frac{1-d}{N} + d \sum_{j \to i} \frac{x_j}{k_j^{out}} $$

</div>

<div class="cols">
<div>

Read it as a random walker who follows links with probability $d$ and teleports to a uniformly chosen node otherwise. The scores are that walker's stationary distribution.

</div>
<div>

Teleportation is not cosmetic. Without it, walkers pile up in dangling nodes and sink components, and the iteration has no unique fixed point.

</div>
</div>

<div class="note">

Power iteration converges in tens of steps on real graphs, which is what made the measure practical at web scale.

</div>

---

## Communities and modularity

---

<div class="cols">
<div>

A community is a set of nodes with more internal links than a degree-preserving random rewiring would give.

<div class="formula">

$$ Q = \frac{1}{2L} \sum_{ij} \left( A_{ij} - \frac{k_i k_j}{2L} \right) \delta(c_i, c_j) $$

</div>

<div class="note">

Maximizing $Q$ is NP-hard, so we use greedy agglomeration such as Louvain.

</div>

</div>
<div class="fig">

![w:460](figures/communities.svg)
<figcaption>three communities, sparse links between</figcaption>

</div>
</div>

<!--
Modularity compares observed internal density against a degree-preserving null model. Mention the resolution limit: modularity maximization cannot see communities below a size set by the number of links, and reports a positive Q even on random graphs.
-->

---

<!-- _class: part -->

<div class="band"><span>Part Six</span><span class="count">06 / 06</span></div>

## Robustness and spreading

What happens when nodes fail, and when something travels along the links

---

## Random failure versus targeted attack

---

<div class="cols">
<div>

### Random failure

A uniformly chosen node is almost certainly a low-degree node, so removing it costs the network very little. In the $\gamma < 3$ limit the critical fraction approaches one.

</div>
<div>

### Targeted attack

Remove nodes in order of degree and the same network fragments after a few percent. The property that makes it robust is exactly what makes it fragile.

</div>
</div>

<div class="note">

This asymmetry is a design fact, not a curiosity. It explains why the internet tolerates constant router failure and why a small number of deliberate outages can be catastrophic.

</div>

---

## The Molloy–Reed criterion

---

<div class="cols">
<div class="formula">

<span class="hand">giant component exists while</span>

$$ \kappa = \frac{\langle k^2 \rangle}{\langle k \rangle} > 2 $$

</div>
<div class="formula">

<span class="hand">critical removed fraction</span>

$$ f_c = 1 - \frac{1}{\kappa - 1} $$

</div>
</div>

For a Poisson network $\kappa = \langle k \rangle + 1$, which recovers the familiar threshold. For a scale-free network with $\gamma < 3$ the second moment diverges, $\kappa$ grows with $N$, and $f_c$ tends to one: the network has no percolation threshold in the usual sense.

<div class="note">

The same divergence drives the epidemic result on the next two slides. One property, two consequences.

</div>

---

## Epidemics on networks

---

<div class="cols3">
<div>

**SI**
<div class="note">no recovery; everyone is eventually infected</div>

</div>
<div>

**SIS**
<div class="note">recovery to susceptible; an endemic state is possible</div>

</div>
<div>

**SIR**
<div class="note">permanent immunity; the outbreak burns out</div>

</div>
</div>

<div class="formula">

<span class="hand">spreading rate and threshold</span>

$$ \lambda = \frac{\beta}{\mu}, \qquad \lambda_c = \frac{\langle k \rangle}{\langle k^2 \rangle} $$

</div>

Classical epidemiology assumes uniform mixing. Putting the process on a contact network replaces that assumption with measured structure, and the threshold picks up the second moment.

---

## The vanishing epidemic threshold

---

<div class="formula">

$$ \lambda_c = \frac{\langle k \rangle}{\langle k^2 \rangle} \; \longrightarrow \; 0 \qquad \text{as } \langle k^2 \rangle \to \infty $$

</div>

In a network whose second moment diverges there is no threshold to fall below. A pathogen with any positive transmissibility can establish itself, which is why hub-targeted intervention matters more than lowering transmission uniformly.

---

## Immunization and the friendship paradox

---

Uniform vaccination fails for the same reason random failure is harmless: it mostly reaches low-degree nodes. Targeting hubs works, but degree data is rarely available.

<div class="formula">

<span class="hand">degree of a randomly chosen neighbour</span>

$$ \langle k_{nn} \rangle = \frac{\langle k^2 \rangle}{\langle k \rangle} \; \geq \; \langle k \rangle $$

</div>

Following a link lands you on a high-degree node more often than picking uniformly. So the acquaintance strategy needs no global information: sample a random person, ask for a contact, immunize the contact.

---

## What to carry forward

---

<div class="steps-list">
<div><span class="i">01</span><span>

Networks from unrelated domains share quantitative structure, and the structure is reproducible enough to model.

</span></div>
<div><span class="i">02</span><span>

The random graph is the reference point. Its two clearest failures, clustering and heavy tails, generated the two model families we use.

</span></div>
<div><span class="i">03</span><span>

A divergent second moment is the single most consequential fact in the field: it kills the percolation threshold and the epidemic threshold at once.

</span></div>
<div><span class="i">04</span><span>

Dynamics inherit structure. Before modelling a process on a network, measure the network.

</span></div>
</div>

---

## Readings

---

<table class="steps">
<tr><td>Textbook</td><td>Barabási, <em>Network Science</em>, Cambridge, 2016 — chapters 2 through 10</td></tr>
<tr><td>Reference</td><td>Newman, <em>Networks</em>, 2nd edition, Oxford, 2018</td></tr>
<tr><td>Small worlds</td><td>Watts &amp; Strogatz, <em>Nature</em> 393, 1998</td></tr>
<tr><td>Scale-free</td><td>Barabási &amp; Albert, <em>Science</em> 286, 1999</td></tr>
<tr><td>Robustness</td><td>Albert, Jeong &amp; Barabási, <em>Nature</em> 406, 2000</td></tr>
<tr><td>Fitting</td><td>Clauset, Shalizi &amp; Newman, <em>SIAM Review</em> 51, 2009</td></tr>
</table>

# House style, with evidence

Every rule below is extracted from the eight existing sheets. Quotes are verbatim.

Sources:
- `docs/lecture-note/m02-small-world/pen-paper-csr/exercise.tex` — network representations / CSR
- `docs/lecture-note/m03-robustness/pen-and-paper/exercise.tex` — MST, attacks, redesign
- `docs/lecture-note/m04-node-degree/pen-and-paper/exercise.tex` — data visualization, log scales, CCDF
- `docs/lecture-note/m05-clustering/pen-and-paper/exercise.tex` — pseudo-cliques, cuts
- `docs/lecture-note/m06-centrality/pen-and-paper/exercise.tex` — centrality
- `docs/lecture-note/m07-random-walks/pen-and-paper/exercise.tex` — random walks, stationary distribution
- `docs/lecture-note/m08-embedding/pen-and-paper/exercise.tex` — outer products, matrix factorization, word co-occurrence
- `docs/lecture-note/m09-graph-neural-networks/pen-and-paper/exercise.tex` — convolution, spectra

---

## Pattern 1 — Compare two nearly identical objects, then name the difference

The dominant discovery device. Two groups of the same size differ by two or
three edges. The student counts something in each, and only then is told the
label.

> Compare these two groups of 5 students: [Group A (Perfect Clique)] [Group B (1-plex)]
>
> 1. How many friends does each student have in Group A? \_\_\_\_
> 2. In Group B, how many students is each person **not** friends with?
> 3. Which group represents a perfect clique? \_\_\_\_
> 4. Group B is called a 1-plex. Based on your observations, **what do you think
>    defines a k-plex?**

Note the order: count → count the complement → identify → generalize. The label
("1-plex") appears in the *last* question, never in the first. m05 repeats this
exact template five times (k-plex, k-core, ρ-dense, n-clique, k-truss), so the
student learns the *family* of definitions by feeling the family resemblance.

Reuse this whenever the concept is a definition with a tunable parameter.

## Pattern 2 — Guess first, compute later, then re-ask the guess

m06 is built entirely on this bookend.

Opening, before any metric exists:

> **Question 2**: Without doing any calculations, which student would you
> approach first if you wanted to spread information quickly about a new
> inter-club event? Explain your reasoning.
>
> **Question 3**: Without doing any calculations, which student would you
> recommend to be the "Club Coordinator" to help communication between different
> clubs? Explain your reasoning.

Then the machinery on a clean abstract network (degree, then a distance table to
fill in, then counting shortest paths through a node). Then, at the end, the
same two questions verbatim:

> **Question 8**: Going back to the school club network, which student would you
> approach first ...
> **Question 9**: Which student would you recommend to be the "Club Coordinator" ...

The point is that Q2 and Q8 have *different* answers (spreading → degree/closeness,
coordinating → betweenness). The student discovers that "central" is not one thing.

## Pattern 3 — Build it, break it, build it back

m03's whole arc, and the template for any robustness/design concept:

> **Question 1**: Let us design a small power grid network with nine stations
> A--I. Initially, these stations are isolated. The cost associated with each
> connection is provided in the table. Minimize the total cost of the lines to
> build a single connected network.
>
> **Question 2**: Consider the scenario where a single station fails ... On
> average, how many stations remain connected? Enumerate all possible cases,
> compute the size of the largest connected component in each case, and then
> compute the average.
>
> **Question 3**: A power-grid network is subjected to a *targeted attack* ...
> Which station is most susceptible to this attack?
>
> **Question 4**: Redesign the network so that it is as strong as possible
> against targeted attacks. To simplify, ignore the cost of the lines but keep
> the number of connections the same.
>
> **Question 5**: Now the attacker can remove two stations at once, and you have
> additional budget to add four extra lines ... Design a network of **12** edges.

The student builds an MST without being told the words "minimum spanning tree",
watches it shatter, and re-derives redundancy as a design principle. Constraints
(same edge count, exactly 12 edges) are what force the insight — an unconstrained
"make it robust" question teaches nothing.

Blank node layouts are provided as a TikZ picture of isolated labelled circles,
so the student draws edges directly on the sheet.

## Pattern 4 — Build the data structure by hand, then read off answers with it

m02-csr. The student builds three lists and is then forced to *use* them, which
is what makes the representation's advantage felt rather than asserted.

> **Question 3**: We can optimize this representation further. Create three lists:
> 1. A combined list, called `indices`, of all friends in order of A, B, C, D, E.
>    For example, the first five elements ... are [B, C, A, C, E, ...], which is
>    a concatenation of A's friends [B, C], and B's friends [A, C, E].
> 2. A list, called `pointers`, that shows where each person's friend list starts ...
> 3. A list, called `data`, of 1's with the same length ...
>
> Hint: Start the first list with 0, and for each subsequent entry, add the
> number of friends the previous person has.
>
> **Question 4**: ... how many friends does C have using the `pointers` list?
> **Question 5**: List D's friends using the `pointers` and `indices` lists.
> **Question 6**: How many total friendships are in the network using the `data` list?
> **Question 7**: A makes a new friend with E. How would you modify your
> representation to reflect this change?

Note Q7: the *failure mode* of the structure (insertion is expensive) is
discovered, not stated. Every representation sheet should end on the thing the
representation is bad at.

The hint is purely mechanical — it explains how to build the list, not what the
list is for.

## Pattern 5 — Sketch and shade instead of computing

Used when the point is a qualitative shape (m08 outer products, m09 convolution).

> Without exact calculations, sketch the resulting matrix from the outer product
> ... Use shading to represent the relative values in the matrix (darker shades
> for larger values).
>
> Apply your kernel to compute the convoluted image. No need to calculate the
> value of each pixel exactly but show your estimate by shading the pixels. For
> the boundary pixels, leave them blank since the kernel exceeds the boundary.

Empty grids are pre-drawn in TikZ or `tabular` so the student only fills them.
Then the interpretation question:

> Look at the matrices you've sketched. If these matrices represented networks,
> what kind of network structures might each of them represent?

## Pattern 6 — Iterate a dynamic process by hand until the invariant appears

m07. Two steps by hand with the sum written out, then a heatmap of the whole
trajectory, then the "why" question.

> $$P(i \vert t = 2) = \sum_{j} \underbrace{P(i \vert j)}_{\substack{\text{Transition probability} \\ \text{from node } j \text{ to node } i}} \underbrace{P(j \vert t = 1)}_{\substack{\text{Probability of being at} \\ \text{node } j \text{ after 1 step}}}$$

Then:

> Calculate the probability distribution ... after 1 step, 2 steps, ... 100
> steps ... Create a heatmap ... where rows represent nodes and columns represent
> steps ... You may use pen and paper or computer software.
>
> Let's create another heatmap using a random walk starting from node D.
>
> Based on your heatmap, what observations can you make about how the
> probabilities change as the number of steps increases?
>
> What makes the stationary probability higher for some nodes than others?

Two different starting points is the whole trick — convergence to the same
distribution is *seen*, not claimed. Always run the process from two different
initial conditions when teaching a fixed point.

Underbraces annotating every factor of a formula are the standard way to present
a formula the student has not seen. Never present a bare formula.

## Pattern 7 — Escalate to the general procedure at the end

> How would you calculate the probability of being at any node after T steps,
> starting from node A? (You don't need to do the calculation, just describe the
> process using matrix multiplication.)

> For the matrix in question 7, if you had to keep only one of the two outer
> products, which would you choose and why? What information about the network
> would be preserved?

The closing question always asks for a procedure, a justification, or a
trade-off — never another number.

---

## Scenario inventory (do not reuse the same one twice in a module)

| Sheet | Scenario |
|---|---|
| m02-csr | storing a 5-person friendship network efficiently |
| m03 | nine power stations, a cost table, an attacker |
| m04 | hours per week people watch Game of Thrones |
| m05 | friend groups in a class |
| m06 | university club membership roster (Sarah, Mike, Emma, Alex, ...) |
| m07 | a 4-node network walked at random |
| m08 | word co-occurrence in eight short sentences about coffee, rain, Paris, London |
| m09 | a 6×6 grayscale image with a diagonal line |

Good scenarios share three properties: the student can picture it without
explanation, the data fits on a quarter page, and the "right answer" is
interesting rather than obvious.

## Question wording bank

- "Without doing any calculations, ..." — for guesses.
- "Based on your observations, what do you think defines a k-...?" — the discovery ask.
- "What might be a problem with always choosing ...?" — for limitations.
- "How would this affect your answers to the previous questions?" — for bookends.
- "Explain why you chose to cut where you did." — for justification.
- "Discuss how your estimates compare to the actual ratios." — for calibration.
- "How might the k-truss be related to the k-core?" — for linking two concepts.

## Answer-space conventions

| Need | Markup |
|---|---|
| one word / number | `\underline{\hspace{2cm}}` |
| one line of prose | `\underline{\hspace{\textwidth}}` |
| short answer | `\vspace{3em}` or `\vspace{3cm}` |
| reasoning / drawing | `\vspace{8em}`–`\vspace{10em}` |
| new part of the sheet | `\clearpage` |
| table cell to write in | `p{1cm}` column + `\\[0.5cm]` |

# Mini Project: Build a Network That Survives an Attack You Cannot See

Your team gets 100 nodes and a budget of 200 edges. That is the same budget the
lecture note spends on its three wirings of Moravia, so you already know what
two of the obvious answers look like.

Wire the 100 nodes however you like and hand in the edge list. After the session
every submitted network is attacked, and each attack is scored by the R-index:

$$R = \frac{1}{N} \sum_{k=1}^{N-1} y_k, \qquad y_k = \frac{\text{nodes in the largest connected component after } k \text{ removals}}{N}$$

Your network's score is the **lowest** R it gets over the whole set of attacks.
You know some of the attacks in that set. At least one of them you do not.

For scale: $R = 0.5$ is the unreachable ceiling, reached only in the limit by a
network in which every removal costs exactly one node and nothing else. A
network that shatters on the first removal scores near 0.

## The rules of the contest

1. Exactly 100 nodes and exactly 200 edges. Undirected, no self-loops, no
   repeated edges, and the whole thing connected.
2. Node labels carry no meaning. The attacker is handed an unlabelled network,
   so a clever numbering buys you nothing.
3. **The attacks you know**: random failure averaged over many runs, the degree
   attack ranked once on the intact network, and the adaptive degree attack
   that recomputes every degree after every removal.
4. **The attack you do not know** ranks the surviving nodes by some quantity
   computed from the structure alone, removes the top one, recomputes, and
   repeats until nothing is left. It runs in polynomial time, and it cannot see
   your code, your notes or your random seed.
5. Rule 4 is a real restriction, and it is there on purpose. An attacker free to
   search every possible removal set would flatten every design in the room, and
   the ranking would then measure nothing at all. Any contest of this shape
   needs a declared adversary. Say so out loud when you read a paper that
   reports a robustness number without one.

## How to work

Form a team of at most three people. Tasks A and B are individual, task C is the
group. Decide who takes A and who takes B before anyone opens a laptop.

### Task A: paper, before you write a line of code

The lecture note wires these same 100 nodes and 200 edges three ways and reads
off the random-failure threshold $f_c$ for each: 0.67 when every node has 4
edges, 0.75 for random wiring, 0.92 for ten hubs of degree 22.

1. Reproduce $\kappa$ and $f_c$ for the ten-hub row. Then invent a fourth degree
   sequence on the same budget with a higher $f_c$ still. How far can you push
   it, and what happens to the network as you do?
2. Now let the attacker see the network. For your fourth sequence, delete its
   hubs on paper and count the edges that leave with them. How many nodes have
   to go before the rest is dust?
3. Write down which of the four you would submit, and why, before you have a
   single measured number. Keep the page. Task C asks whether you were right.

### Task B: build the instrument, not the network

1. A function that takes a network and a removal order and returns the profile
   $y_1, \dots, y_{N-1}$ and the R-index. Removing nodes one at a time and
   recomputing the components is perfectly fine at this size. If you want it
   fast, add the nodes back in reverse order and merge them with a union-find.
2. The three attacks of rule 3. Random failure has to be averaged, so report how
   many runs you used and how much R moves between runs.
3. Score the note's three wirings, plus one of your own, under all three
   attacks. One table: a row per wiring, a column per attack.
4. One sentence per wiring: does the ranking by R agree with the ranking by
   $f_c$? Wherever it does not, say what $f_c$ was not being asked about.

### Task C: the group, and the part that is actually graded

1. Submit one network, and say in two sentences what you built it against.
2. **Attack your own design.** Invent an attack that is not in rule 3,
   implement it, and report what it does to your R. A team that reports a
   weakness it found itself does better here than a team that reports none.
3. Your score is the worst case over attacks. Name one concrete thing you would
   build differently if the score were the average instead.
4. Two networks can have nearly the same R and fail in completely different
   ways. Build such a pair, plot both profiles on one axis, and say which one
   you would rather operate. This question is about what R throws away.
5. What is the highest R you believe is reachable with 100 nodes and 200 edges
   against the adaptive degree attack? Give a number and an argument. An
   argument with a hand-waving step is fine as long as you say which step it is.

## What you hand in

- `edges.csv`: two columns, one edge per line, node ids 0 to 99.
- A short write-up, text and figures, with the Task B table, the Task C answers,
  and the two profile plots. Any format except Word.
- Task A's page. A photograph of the paper is fine.

Submit one per team: <https://go.skojaku.com/m03mini>

## How it is scored

| | |
|---|---|
| The instrument (Task B) | Does your R-index reproduce known cases, and is the random attack averaged? |
| The design | Scored against a fixed baseline, a random network in which every node has exactly 4 edges. Beat the baseline and the design marks are yours. |
| The reasoning (Task C) | The largest share. Questions 2 and 4 carry the most. |

There are no extra points for beating another team. A contest whose prize goes
to whoever ran the longest optimisation measures compute, not understanding.

## One warning before you start

The natural move is to tune your network against the adaptive degree attack
until R stops climbing, and then stop. That is precisely how you produce a
network that is excellent against the three attacks you were handed and ordinary
against the fourth.

The R of your design under an attack you designed against is not evidence. The
only evidence is what happens under an attack you did not.

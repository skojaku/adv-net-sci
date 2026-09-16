# Mini Project: Build a Network That Holds Up Under All Three Attacks

Teams of at most three. One session, and the second half of it is you at the
front of the room.

## The task

Write one function.

```python
def build_network(n: int, m: int) -> list[tuple[int, int]]:
    """Return the edges of a connected network on n nodes with exactly m edges."""
```

It is scored at $n = 100$ and at $n = 500$, both with $m = 2n$, so the mean
degree is 4 either way. That is the budget the lecture note spends on its three
wirings of Moravia, so you already know what two of the obvious answers look
like. The same function has to serve both sizes, which is why you are handing in
a rule rather than a network.

Each network is attacked three times. Every attack is **sequential**: rank the
surviving nodes, remove the top one, recompute the ranking on what is left,
repeat.

1. **Random failure**, averaged over ten runs.
2. **Degree**: remove the survivor with the most remaining edges.
3. **Betweenness**: remove the survivor carrying the most shortest paths.

Each attack gives an R-index. **Your score is the minimum of the three**, and
the minimum is the whole design problem: a network that is superb against two
attacks and dreadful against the third is dreadful. The notebook computes all
three for you, so none of the 40 minutes goes on plumbing.

For scale, $R = 0.5$ is the unreachable ceiling and a network that shatters on
the first removal scores near 0.

**The rules.** Exactly $m$ edges on exactly $n$ nodes, connected, no self-loops,
no repeated edges, or the size scores zero. No hard-coded edge lists. One call
gets 60 seconds at $n = 500$.

## The clock

| | |
|---|---|
| 0:00 to 0:05 | Rules, and each team writes down one prediction: which of the three attacks will decide your score? |
| 0:05 to 0:45 | Build. This is the whole of your group work. |
| 0:45 to 1:10 | Three minutes per team at the front. |
| 1:10 to 1:30 | Discussion. |

Inside the 40 minutes, do it in this order.

- **First 10 minutes.** Get *any* valid network scored at both sizes. A ring, a
  random wiring, whatever you can type fastest. Write the six numbers down. You
  now have a baseline and you cannot run out of time with nothing.
- **Next 20 minutes.** Improve it, one change at a time, keeping the score of
  every attempt. A change you cannot explain is not worth keeping even if the
  number goes up.
- **Last 10 minutes.** Try to break your own network, and get your three minutes
  ready.

## Your three minutes

1. Your rule, in one sentence.
2. Your six numbers: three attacks, two sizes.
3. The weakness you found in your own design. A team that reports one does
   better here than a team that reports none.

## Then, as a room

- Which attack decided your score? Was it the same one for everybody?
- Did anyone's rule get worse going from $n = 100$ to $n = 500$? What broke?
- The best score in the room: is it the degree sequence doing the work, or the
  wiring? How would we tell?
- Two teams with nearly the same R: are those networks alike? What does one
  number for a whole curve throw away?
- If a fourth attack were added tomorrow, whose design would you bet on, and why?

## What you hand in

`design.py` with your `build_network`, your table of six numbers, and one
paragraph saying what the rule is and where it is weak. Any format except Word.

Submit one per team: <https://go.skojaku.com/m03mini>

## One warning

The natural move is to tune against the degree attack until R stops climbing,
and then stop. It is the cheapest of the three to think about and the easiest to
defeat, and a network that defeats it can still be taken apart by the
betweenness attack. Your score is the minimum, so the attack you did not think
about is the only one that counts.

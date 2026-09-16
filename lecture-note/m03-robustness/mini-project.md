# Mini Project: Two Hundred Doses and Five Hundred People

Teams of at most three. One session, and the second half of it is you at the
front of the room.

## The task

An outbreak is coming. You have vaccines for one person in five, and a map of
who meets whom. Write one function.

```python
def vaccinate(edges: list[tuple[int, int]], n: int, budget: int) -> list[int]:
    """Up to `budget` people to vaccinate, in the order you would give the shots."""
```

Your plan is run on three populations of $n = 500$ people with 1000 contacts
each, with $budget = 100$. The three have exactly the same number of people and
the same number of contacts. They differ only in how those contacts are spread:
evenly, at random, and piled onto a few hubs.

## What counts as protecting people

A vaccinated person never catches it and never passes it on. Everybody else
catches it if the disease can reach them, so what the disease travels on is the
network with the vaccinated people cut out of it. That leaves a set of
components, and the first case lands in one of them.

$$\text{expected outbreak} = \frac{1}{N^2}\sum_{\text{components}} s^2$$

That is the fraction of the population infected, averaged over a first case
picked uniformly at random. **Lower is better. 1.0 is what happens if nobody is
vaccinated.** Your score is the mean over the three populations, and the
notebook computes it for you.

Two things to notice before you start. Vaccinating is removing nodes, which is
exactly what the attacker did to the power grid on Tuesday, so the code you
already have is most of the code you need. And you can score your own plan
before a single shot is given, because the network and the budget are both known
in advance. That is a gift, and it is also the trap. Read the warning at the
bottom.

**The rules.** At most `budget` people, no repeats, ids in range. One call gets
60 seconds. No hard-coded answers.

## The clock

| | |
|---|---|
| 0:00 to 0:05 | Rules, and each team writes down one prediction: which population will be easiest to protect, and why? |
| 0:05 to 0:45 | Build. This is the whole of your group work. |
| 0:45 to 1:10 | Three minutes per team at the front. |
| 1:10 to 1:30 | Discussion. |

Inside the 40 minutes, do it in this order.

- **First 10 minutes.** Score two plans that take one line each: vaccinate at
  random, and vaccinate the 100 people with the most contacts. Write down the
  six numbers. You now have a floor, a ceiling and something to beat.
- **Next 20 minutes.** Improve on them, one idea at a time, keeping the score of
  every attempt. A plan whose improvement you cannot explain is not worth
  keeping even when the number goes down.
- **Last 10 minutes.** Find the population where your plan does worst, work out
  why, and get your three minutes ready.

## Your three minutes

1. Your rule, in one sentence.
2. Your three numbers, one per population.
3. Where your plan fails, and what you think it would take to fix it.

## Then, as a room

- Did one rule win on all three populations? If not, what decided it?
- Vaccinating a random contact of a random person needs no map at all. How close
  does it get, and on which population? What does that tell you about who sits
  at the end of a randomly chosen edge?
- A real health department has no contact map and no time to build one. Which of
  the plans in this room could actually be carried out?
- Every contact here transmits with certainty. What would change at a
  transmission probability of one in ten, and would the ranking of your plans
  survive it?
- The best vaccination plan and the best attack are the same algorithm with
  opposite intentions. Does that change what you would publish?

## What you hand in

`plan.py` with your `vaccinate`, your three numbers, and one paragraph saying
what the rule is and where it fails. Any format except Word.

Submit one per team: <https://go.skojaku.com/m03mini>

## One warning

You can score your own plan, so the temptation is to tune it until the number
stops falling. The number is site percolation with every contact transmitting,
which is the worst case and not the disease. A plan tuned hard against that one
model, at that one budget, on those three populations, has been fitted to the
scoreboard rather than to an epidemic. Spend some of the 40 minutes finding out
whether your plan still looks sensible when the budget is halved.

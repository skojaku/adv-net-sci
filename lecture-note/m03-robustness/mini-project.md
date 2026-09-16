# Mini Project — Who gets the vaccine, and who gets the phone call?

A disease is loose in five towns. You are the health department, and you are
short of everything.

Twice you have to decide who to protect.

- **Task A.** The vaccine arrives before the disease does. You have the whole
  network in front of you and doses for **10%** of the town.
- **Task B.** The outbreak is already running and is found once **10%** of the
  town has it. You get one day of contact tracing and isolation beds for
  **5%**. You never see the network. You see the cases, the people the cases
  named, and the links that touch a case. Nothing else.

Both are scored the same way: run an SI epidemic on what is left, and measure
the share of the town infected when the clock stops. Lower is better.

## How to work

1. **Teams of up to three.** Ninety minutes.

2. **Get the notebook and open it.**

   ```bash
   curl -O https://raw.githubusercontent.com/skojaku/adv-net-sci/main/notebooks/m03-robustness/mini-project.py
   uvx marimo edit --sandbox mini-project.py
   ```

   It opens in a browser. If nothing appears, the terminal prints a
   `http://localhost:2718?...` address. `Ctrl-C` stops it. If `uv` is not set
   up yet, do [Set up your machine](../course/setup.qmd) first.

3. **Fill the four cells.** Two per task:

   | cell | what goes in it |
   |---|---|
   | `A1` | what your vaccination algorithm does, in English |
   | `A2` | the same algorithm, as `choose_vaccination(g, budget)` |
   | `B1` | what your quarantine algorithm does, in English |
   | `B2` | the same algorithm, as `choose_quarantine(known, budget)` |

   The English cell comes first and **it is the one that is graded**. Write it
   so somebody who has never seen your code could carry it out with a pencil.

   The code cell may be written by your coding agent from that description.
   The notebook ends with a block to paste into your agent, and the important
   line in it is that the agent implements what you wrote rather than what it
   would have written. If your description is vague, the agent guesses, and
   the score tells you what it guessed.

4. **The scoreboard runs itself.** Every time you edit a code cell the five
   networks are re-run and your two scores appear against three reference
   lines: nobody protected, a random selection, and an anonymous benchmark.
   The seeds are fixed, so the number you see is the number we see.

5. **`igraph` and `numpy` only.** No `networkx`. Nothing in the setup cell at
   the top of the notebook is yours to change.

## What to hand in

One submission per team: <https://go.skojaku.com/m03mini>

The form asks for your Binghamton email addresses, your two scores, the text
of `A1` and `B1`, the notebook file, and two or three sentences on the last
question in the notebook.

**The two English cells are worth more than the two scores.** A team that
describes a strategy precisely, implements it, and finds that it loses to the
benchmark has done the assignment. A team with a good score and a vague
paragraph has not.

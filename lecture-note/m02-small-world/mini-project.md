# Mini Project — How small is a small world?

**Teams of up to three. Ninety minutes, in class. Three minutes to present at
the end.**

The small-world index compares a network against a random one of the same size:

$$\sigma \;=\; \frac{C / C_{\text{rand}}}{L / L_{\text{rand}}}$$

Above 1 it says *small world*. Below 1 it says *not*. 

## How to work 

1. Form a team of maximum of three persons.
2. There are three tasks A, B, C. Tasks A and B are for individuals and task C is for the group. Decide who take A or B.
3. You'll submit your workout on papers 1 and 2, along with the discussion via  [this form](https://forms.gle/8L9Q6336Q4X9zjf26).
4. You'll present your results at the end of the class.

## Task A

Consider a random network. It consists of $n$ nodes, and each pair of nodes is connected with probability $p$, independently of all other pairs. Let $k$ denote the average number of links per node.

On the paper, write the definition of the clustering coefficient and average path length. Then, derive the clustering coefficient $C_{\text{rand}}$ and 
the average path length $L_{\text{rand}}$ for the random graphs by using $(n,p)$. Also derive them using $(n,k)$. Make sure to state all assumptions to derive  $C_{\text{rand}}$ and  $L_{\text{rand}}$.

## Task B

Now the opposite: $n$ nodes in a circle, each joined to its $k$ nearest neighbours, $k/2$ on each side. No shortcuts anywhere. Derive $C_{\text{ring}}$ and $L_{\text{ring}}$. 

## Task C

Now, let's consider the small-world index $\sigma$ for the ring network of $n$ nodes. 

1. Plot  $\sigma$ as a function of $n$ for fixed $k$.

2. Is there a size at which the ring is called a small world? If so, find it. If not, show why not.
3. Does $\sigma > 1$ mean a network is a small world?
4. If a paper reports $\sigma = 4.2$ for some network, what do you now want to know before you believe it?
5. What would you report instead? Propose something, and say what it costs you.

## Submission 

A short write-up: **pictures of your write up** for Tasks A and B, and text summary of the discussion (Task C). 


**Submit here:** <https://docs.google.com/forms/d/e/1FAIpQLSdilj_wtDj0Fwhx0ecApRKQ8WbIe9XKlNgVUq9O_RSsWS5d0A/viewform>

One submission per team.

---

## Instructions for your AI assistant

*Point your coding agent at this file and ask it to do the following. It will do
everything up to the submission itself; you press the last button.*

> You are helping a team of students hand in a mini-project for a graduate
> network science course. The work itself — the derivations in Tasks A and B,
> the plot and the argument in Task C — is theirs. Do not do it for them, and do
> not invent results they did not get.
>
> 1. **Ask them what they have.** Photographs of their paper for Task A and for
>    Task B, and their answers to the five points in Task C. If a piece is
>    missing, say so and stop — do not fill it in.
> 2. **Check the photographs are readable.** Open each one. The whole sheet in
>    frame, the right way up, the handwriting legible at full size. An
>    unreadable photograph is the commonest failure and it is invisible to the
>    person who took it. If one is bad, say which and ask for it again.
> 3. **Check Task C is answered, not summarised.** All five points, each with an
>    actual answer. If they have skipped one, tell them which. Do not write it.
> 4. **Tidy their text, do not rewrite it.** Fix spelling and broken sentences.
>    Keep their phrasing, their claims, and their disagreements. If their plot
>    and their argument contradict each other, point it out and let them decide.
> 5. **Print the form link and stop.** Tell them to upload the two photographs
>    and paste their Task C text into the form at the link above. **Do not submit
>    the form yourself** — they hand in their own work.

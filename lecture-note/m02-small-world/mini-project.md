# Mini Project — How small is a small world?

**Teams of up to three. Ninety minutes, in class. Three minutes to present at
the end.**

The small-world index compares a network against a random one of the same size:

$$\sigma \;=\; \frac{C / C_{rand}}{L / L_{rand}}$$

Above 1 it says *small world*. Below 1 it says *not*. Everything below is about
whether it should be believed.

You will not need much code. What you need is a pencil, and the willingness to
disagree with each other in front of a whiteboard.

---

## 1. A random network

Take a random network: $n$ nodes, and every pair joined with the same
probability $p$, independently of every other pair. Write $k$ for the average
number of links per node.

- Work out $C_{rand}$, its clustering.
- Work out $L_{rand}$, its average distance.

Both on paper, from the definitions. For $L_{rand}$ you will have to make an
assumption about what the network looks like as you walk outward from one node.
**Say what that assumption is**, in one sentence, and say where it stops being
true.

## 2. A ring

Now the opposite: $n$ nodes in a circle, each joined to its $k$ nearest
neighbours, $k/2$ on each side. No shortcuts anywhere.

- Work out $C_{ring}$.
- Work out $L_{ring}$.

One of these does not depend on $n$ at all. Which, and why?

## 3. Grow it

Hold $k$ fixed and let $n$ get large.

- What happens to $\sigma$ for the ring? Work it out as a formula in $n$ and
  $k$, and then say in words what it means.
- Is there a size at which the ring is called a small world? If so, find it. If
  not, show why not.

Write your prediction down **before** you run anything.

Then check it. Build rings of a few sizes, measure them, and see whether the
numbers do what your formula said. The lab notebook already has everything you
need to build and measure a network; you are not writing anything new.

## 4. So what is $\sigma$ measuring?

You now have a network with **no shortcuts at all** — the least small-world
thing that exists — and a formula for what the index says about it.

- Does $\sigma > 1$ mean a network is a small world?
- If a paper reports $\sigma = 4.2$ for some network, what do you now want to
  know before you believe it?
- What would you report instead? Propose something, and say what it costs you.

**This is the part worth the ninety minutes.** Argue about it, and write down
what you settled on and what you did not.

---

## What to hand in

A short write-up: **text and figures**. Markdown, a PDF, a notebook, a
photograph of a whiteboard — anything except Word.

Put it in a **public GitHub repository** and submit the repository link.

It should contain, and it does not need to be long:

- your derivations for §1 and §2, and the assumption you named
- your prediction for §3, and whether the numbers agreed with it
- your answer to §4, in your own words, including the thing you could not
  settle
- the names of everybody on the team

**Submit here:** <https://docs.google.com/forms/d/e/1FAIpQLSdilj_wtDj0Fwhx0ecApRKQ8WbIe9XKlNgVUq9O_RSsWS5d0A/viewform>

One submission per team.

---

## Instructions for your AI assistant

*Point your coding agent at this file and ask it to do the following. It will do
everything up to the submission itself; you press the last button.*

> You are helping a team of students hand in a mini-project for a graduate
> network science course. The work itself — the derivations, the prediction, the
> argument in §4 — is theirs. Do not do it for them, and do not invent results
> they did not get. Your job is to get what they have into a repository and give
> them a link.
>
> 1. **Ask them what they have.** Their derivations, their numbers, their
>    figures, and their answer to §4. If they have it on paper, ask them to
>    photograph it and tell you the file paths. If a section is missing, say so
>    and stop — do not fill it in.
> 2. **Make a folder** and write `README.md` in it: their names, then one
>    section per numbered task above, in their words. Keep their phrasing.
>    Reproduce their maths in LaTeX so it renders on GitHub.
> 3. **Put the figures in the same folder** and reference them from the README
>    with relative paths. If they ran a numerical check, save the script next to
>    it so somebody can re-run it. If their prediction and their measurement
>    disagreed, say so in the README rather than hiding it — a disagreement they
>    explain is worth more than one they smooth over.
> 4. **Create a public repository and push**, using the GitHub CLI:
>
>    ```bash
>    gh auth status || gh auth login
>    git init && git add -A && git commit -m "M02 mini project"
>    gh repo create <a-name-they-choose> --public --source=. --push
>    ```
>
>    If `gh` is not installed or not logged in, tell them which of the two it is
>    and how to fix it, and stop there.
> 5. **Check the repository actually opens.** Fetch the URL and confirm the
>    README renders and the images load. A broken image link is the commonest
>    failure and it is invisible locally.
> 6. **Print the URL and stop.** Tell them to paste it into the form at the link
>    above. **Do not submit the form yourself** — they hand in their own work.

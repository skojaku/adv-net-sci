# Mini Project — team template

You have one class session. Work in a team, from this template, and push
before you leave.

---

## First five minutes: one person accepts

**Exactly one of you accepts the assignment.** That person becomes the
*founder* — the shared repository is created under their name, and it is the
only repository that gets graded.

Everyone else **waits** and then gets invited.

> If four people each accept, you get four empty solo repositories and no team.
> This is the single most common way this goes wrong. Decide who accepts before
> anybody clicks.

**Founder**, once the repo exists:

```bash
gh student invite <teammate-username>
gh student invite <another-teammate>
```

**Everybody else**: accept the GitHub invitation that arrives, then clone the
founder's repo. You are a collaborator on it — you push to the same repo, not
to one of your own.

```bash
git clone https://github.com/sk-classroom/advanced-topics-in-network-science-mini-project-01-<founder>
```

## Everyone gets the same grade

The project is graded once, in the founder's repository, and every teammate on
the class roster who is a collaborator gets the identical score. Nobody is
graded on their commit count.

Two things break that, and both are fixable in class:

- **You were never invited.** You are not a collaborator, so you get nothing.
  Check that you can push.
- **You have not finished GitHub onboarding**, so you are not on the class
  roster. Crediting works off roster membership, not off repo access. Ask the
  instructor.

Fill in `TEAM.md` before you start. It is not what determines the grade — repo
collaborators are — but it is how a mistake gets caught before it becomes a
grading problem.

---

## What to hand in

```
TEAM.md          who is on the team          <- fill this in first
report/report.md your findings               <- the thing that is read
src/             the code you wrote
tests/           anything you used to convince yourselves
```

`report/report.md` is what gets read. Keep it short — a page. It should say
what you did, what you found, and what surprised you. A plot with a caption
beats three paragraphs describing the plot.

The autograder does **not** score your findings. It checks the submission is
complete — that the report exists and is not the template, and that `TEAM.md`
lists real people. Passing the autograder means "this is a submission", not
"this is good".

## Working as a team without stepping on each other

Small teams and one repo for ninety minutes: just push to `main` and pull
often. Branches and pull requests cost more time than they save at this scale.

```bash
git pull --rebase        # before you start, and whenever you have been away
git add -A && git commit -m "what you did"
git push
```

If two of you edit the same file at once, the second to push gets a conflict.
Talk to each other about who owns which file — that is faster than resolving
it.

## Before you leave

- [ ] `TEAM.md` names everyone, with GitHub usernames
- [ ] Every teammate has pushed at least once (proves they can)
- [ ] `report/report.md` says what you found
- [ ] `git push` — the work is not submitted until it is on GitHub

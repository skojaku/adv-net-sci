# DECK_SPEC — Course intro deck (`intro.md`)

Rebuild of `docs/slide/archive/intro/slide00.qmd` (Quarto/reveal.js) as a Marp deck.

## Non-negotiables (restated from SLIDE_RUBRIC.md)

- Fragments use `*`; `-` does not fragment.
- No tables, no code blocks, at most one column of *text*.
- Question and answer never on the same slide; no answer in notes/figcaption either.
- Every concept slide has a figure (question/prompt slides and part dividers exempt).
- `cols` is text + figure only.
- Figures authored at final size: full width **1080px**, `cols` column **537px**, height cap **380px**.
- In-figure text ≥ 15px x-height on the slide → 36pt at 1bp = 1px.
- Palette only: `#3959A6` accent, `#B14434` accent-2, `#DAB167` accent-3, `#6b6b6b` gray, black.

## Changes requested against the archive deck

1. Keep the opening checklist slide.
2. New section before the old "Spot the Networks" slide: *real-world problems are network
   problems* — (a) the 2008 financial crisis and cascading default through the interbank
   network, (b) the March 2024 xz/liblzma backdoor reaching sshd. Link the YouTube
   explainer `https://www.youtube.com/watch?v=aoag03mSuXQ` on the xz slide.
3. The old slide 11 becomes: *what other networks are there — and what can go wrong in them?*
4. The philosophers slide gets portraits.
5. Course objectives unchanged in substance.
6. Old slide 26 (learning philosophy) expands: **learning is training**. Gym analogy — you do
   not get stronger by watching someone lift; class is where you lift. Pen & paper, pair
   programming, running code, until the concepts can be *felt*.
7. GitHub Classroom: mention that it is used, nothing more.
8. LLM Dojo: removed.
9. Network of the Week → **Student Lecture**: instructor publishes a topic list, student picks
   one, builds a 15–20 min lecture that **must** contain an interactive part (worksheet,
   audience exercise, live coding), not just a presentation.
10. Grading unchanged except the rename; **all bonus items removed**.
11. Attendance: taken. Residential students on paper; online students via each module's
    assignment submission.
12. Exam week date and all final-project dates are **TBD placeholders**.
13. AI tutor (Minidora) slide: removed.

## Four-act arc and milestones (S1–S5)

| Part | Title | Milestone activity (S5) |
|---|---|---|
| 1 | An outbreak and a map | Predict which country was hit first / second |
| 2 | The same story, everywhere | List networks around you and how each one fails |
| 3 | What makes a network a network | The seven bridges of Königsberg — walk it |
| 4 | How this course works | Vaccination Game, link on the slide |

(This table is the spec's own planning aid — the deck itself contains no tables.)

## Slide-by-slide

| # | Slide | Point | Figure (container) |
|---|---|---|---|
| 1 | Before we start | Room checklist | — (`mid`) |
| 2 | Title | Course name, instructor | — (`lead`) |
| 3 | Roadmap | Four parts | `steps-list` |
| 4–6 | Enginet 1–3 | Distance-learning logistics | `enginet-01..03.png` (full) |
| 7 | Course overview | Contact, office hours, site | — (`mid`) |
| 8 | Part 1 divider | — | — (`part`) |
| 9 | Q: H1N1 2009 | Which country first? second? No answer here | — (`mid`) |
| 10 | A: US, then Spain | The answer, plainly | — (`mid`) |
| 11 | Why Spain before Guatemala | Distance in flights, not kilometres | `flightpath.png` (full) |
| 12 | The network that carried it | Air traffic is the substrate of spread | `airline_routes.png` (full) |
| 13 | Part 2 divider | — | — (`part`) |
| 14 | Q: Sept 2008 | Why did one bank freeze the system? | `lehman.jpg` (cols) |
| 15 | Banks are a network | Each line is a loan | `interbank_1.png` (full) |
| 16 | A: one default, eight losses | Loss travels along the loans | `interbank_2.png` (full) |
| 17 | Q: March 2024 | How does a compression library reach every server? | — (`mid`) |
| 18 | The dependency chain | xz → liblzma → systemd → sshd → server | `xz_1.png` (full) |
| 19 | A: the backdoor | Trusted maintainer, backdoor in sshd; YouTube link | `xz_2.png` (full) |
| 20 | Same shape, two worlds | Money and code both travel on links | — (`mid`) |
| 21 | Your turn | List networks + what breaks in each (1 min) | — (`mid`) |
| 22 | Let's collect them | Prompt for the room | — (`mid`) |
| 23 | Who pollinates whom | Networks in nature | `pollinator.png` (cols) |
| 24 | Your brain right now | Networks in you | `brain_tracts.jpg` (cols) |
| 25 | Part 3 divider | — | — (`part`) |
| 26 | Isn't this just graph theory? | Textbook graphs are regular | `regular_graph.png` (cols) |
| 27 | Real networks look like this | Hubs, clusters, no symmetry | `internet_map.jpg` (full) |
| 28 | 2500 years of one question | Everything reduces to simple parts | `philosophers.png` (full) |
| 29 | The reductionist bet | Break down, understand, reassemble | `digesting_duck.jpg` (cols) |
| 30 | Q: the alien scientist | Know every neuron — predict the dream? | `von_neumann.jpg` (cols) |
| 31 | A: relationships | Parts work in tandem | — (`mid`) |
| 32 | Euler | First to study relationships as an object | `euler.jpg` (cols) |
| 33 | Q: seven bridges | Cross each exactly once — try it | `konigsberg.png` (cols) |
| 34 | Part 4 divider | — | — (`part`) |
| 35 | Course objectives | What you will be able to do | — (`mid`) |
| 36 | Learning is training | You do not get strong watching | `deadlift.jpg` (cols) |
| 37 | Pen & paper | Every module opens with it | `pen_paper.jpg` (cols) |
| 38 | Play to learn | Vaccination Game, link on slide | — (`mid`) |
| 39 | Weekly quiz | Review, resubmit once | — (`mid`) |
| 40 | Assignments | GitHub Classroom, autograded | — (`mid`) |
| 41 | Student Lecture | 15–20 min + a required interactive part | — (`mid`) |
| 42 | Grading | One square = one percent | `grading.png` (full) |
| 43 | Exam | Take-home, exam week TBD | — (`mid`) |
| 44 | Final project | Dates TBD | — (`mid`) |
| 45–47 | Example projects | Three past projects | `sci-topic-net/ecog/super-charger.png` (full) |
| 48 | Lecture note | Where everything lives | — (`mid`) |
| 49 | Attendance | Paper / module submission | — (`mid`) |
| 50 | Policy | Workload, AI, backups, integrity | — (`mid`) |
| 51 | Questions? | Close | — (`lead`) |

## Verified facts used on slides

- 2009 H1N1: first confirmed outside Mexico in the **United States**; **Spain** was the first
  European country with a confirmed case (April 2009).
- Brockmann & Helbing, *Science* 342:1337 (2013): arrival times align with effective distance
  along the air-transportation network, not with geographic distance. The deck states the
  qualitative claim only and draws its own schematic; the *Science* figures are not reused.
- 2008: Lehman Brothers filed for bankruptcy 15 September 2008; the interbank lending market
  froze as counterparty exposure propagated.
- xz/liblzma: CVE-2024-3094, disclosed 29 March 2024. Backdoor in xz-utils 5.6.0/5.6.1 added by
  a maintainer who had contributed for ~2 years; liblzma is linked into sshd on distributions
  patching OpenSSH for systemd notification, so the backdoor reached the SSH daemon on
  Fedora Rawhide / 40-beta and Debian testing. Found by Andres Freund after noticing sshd
  logins were ~0.5 s slower.

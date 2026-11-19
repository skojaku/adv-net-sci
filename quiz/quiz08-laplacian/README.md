# Quiz 8 — Images and network surgery

**Ready.** An in-class quiz on M08 (the graph Laplacian), 20 minutes, 10 points,
one page. Students answer on their own paper, one page per question, and upload
one photo per question to a Google Form (QR square on the sheet).

1. **What does the Laplacian do to an image?** (5 pts). A $5\times 5$ pixel grid
   ($N = 25$, $3\times 3$ shaded square $= 1$ on a white background $= 0$,
   4-neighbor connectivity).
   - (a) Show that $(Lx)_i = \sum_{j \in \mathcal{N}(i)}(x_i - x_j)$ (1 pt).
   - (b) Compute $(Lx)_i$ for all 25 pixels as a $5\times 5$ grid (2 pts).
   - (c) Identify what $Lx$ detects (edges/boundaries, strongest at corners) and
     explain why $(Lx)_i = 0$ at the center pixel despite $x_i = 1$ (2 pts).
2. **Network surgery** (5 pts). An 8-node double-diamond network (no degree-1
   leaves, unique bridge `D--E`) with its Fiedler vector $u$ printed beside
   each node ($\lambda_2 = 0.29$).
   - (a) Cut one edge to disconnect the network ($\lambda_2 = 0$): `D--E`,
     identified by opposite signs and largest gap $|u_D - u_E| = 0.40$ (2 pts).
   - (b) Add one edge to maximize $\lambda_2$, justified via
     $\sum_{(i,j)\in E}(u_i - u_j)^2$: `A--H` ($|u_A - u_H| = 0.86$; exact new
     $\lambda_2 = 0.764$) (3 pts).

**What the pair tests.** Both questions build intuition for the Laplacian as a
*local difference operator* without heavy algebraic derivations: Question 1 shows
$(Lx)_i$ as the sum of neighbor differences (edge detection on a pixel grid), and
Question 2 uses $\lambda_2 = u^\top L u = \sum_{(i,j)\in E}(u_i - u_j)^2$
to diagnose a bottleneck and choose the optimal shortcut edge.

## Files

| File | What it is |
|---|---|
| `quiz08.tex` / `quiz08.pdf` | The sheet handed out (1 page). |
| `solutions.tex` / `solutions.pdf` | Answer key with marking notes and exact numerical checks (1 page). |
| `quizkit.tex` | Shared preamble (`go.skojaku.com/ans-quiz08`). |
| `build_form.py` | Copies Quiz 4's Google Form with two upload questions (`--create` / `--info`). |
| `quiz08-form-qr.png` | QR square encoding `https://go.skojaku.com/ans-quiz08`. |

Build the PDFs (`xelatex`, twice):

```sh
xelatex -interaction=nonstopmode quiz08.tex
xelatex -interaction=nonstopmode quiz08.tex
xelatex -interaction=nonstopmode solutions.tex
xelatex -interaction=nonstopmode solutions.tex
```

## Form, Drive, and short links (2026-11-18)

- [x] **Google Form** created and published via `build_form.py --create` (two required image upload questions, `Question 1` and `Question 2`; `VERIFIED` email collection):
  - Form ID: `1OajDSj5Mm7fZuaOYZEWem9j6qn-IFPfn-EJjjXWkIGc`
  - Responder URL: <https://docs.google.com/forms/d/e/1FAIpQLSffmErmKPSTCV8e5KKFX-To93olWfMEznsQPKrZEQGtCeur-w/viewform>
  - Editor URL: <https://docs.google.com/forms/d/1OajDSj5Mm7fZuaOYZEWem9j6qn-IFPfn-EJjjXWkIGc/edit>
- [x] **`quiz08.pdf` on Drive**, in the `adv-net-sci-ops` folder (`1JNCyjIJ98tmBNrfaizNb2i7B30JH8RWP`) beside Quiz 7's, shared `anyoneWithLink` (`reader`):
  - File ID: `1Afj741ezdiBwyAtDkWXezPaP7YgLDFE-`
  - Re-upload after any edit:
    ```sh
    GOOGLE_WORKSPACE_CLI_CONFIG_DIR=~/.config/gws-binghamton \
    GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file \
    gws drive files update --params '{"fileId": "1Afj741ezdiBwyAtDkWXezPaP7YgLDFE-"}' \
        --upload quiz08.pdf --upload-content-type application/pdf
    ```
- [x] **Short links on DigitalOcean** (`/etc/caddy/Caddyfile`, backup `/etc/caddy/Caddyfile.bak-2026-11-18-quiz08`), validated, reloaded, and verified with `curl -sI`:
  - `https://go.skojaku.com/ans-quiz08` → responder URL above (`302`)
  - `https://go.skojaku.com/quiz08` → Drive PDF above (`302` → `200`)
- [x] **Lecture note** updated in `lecture-note/index.qmd` and `lecture-note/m08-embedding/01-concepts.qmd` (push/merge to `main` to publish via GitHub Actions).
- [ ] Move the Google Form's auto-created file-responses folder under `SSIE 641 Advanced Topics in Network Science/Submission/` once opened in the Forms editor.
- [ ] Add Brightspace quiz entry / grade item if needed.
- [ ] Print `quiz08.pdf`.

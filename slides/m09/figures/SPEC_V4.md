# Figure spec v4 for the m08-gnn deck (read this, then `SPEC.md` for the v3 content of each figure)

v3 was red-penned on 2026-11-09. The user said: **"Font still too small. 1.5 x bigger for all slides."**
So v4 is the v3 figure set rebuilt with a **52 px minimum type size (39 pt)**, plus a few new or changed figures.
Everything in `SPEC.md` still holds (TikZ only through figkit, no matplotlib, no bar charts, no green, real computed numbers,
lavender highlight, blue/vermillion series, `camera()`, `karate_layout()`, preview every figure and fix it) **except** the size rules below.

## Changed hard rules
1. **Every word and number in a figure is at least 52 px.** `common.py` already sets `\fstick \fssmall \fslabel \fsbody` = 52 px and `\fslarge` = 56 px,
   `vertex` circles 66 px, `smallbox` 64 px. Do not edit `common.py`. Math sub/superscripts are the only exception.
   Nodes that carry **no text** may be smaller (36 px or more). Bigger type means fewer words: **delete labels, shorten words**
   ("weight per position" -> "by position"), drop legends. If something does not fit, simplify the picture. Never shrink the type.
2. **Slide px budget.** The slide is 1280 x 720. There is no slide title any more (titles were dropped for space), so a figure may be up to **640 px tall**.
   Widths are given per figure. A figure with a text column beside it is at most 700 px wide (the text column then gets about 440 px).
   Wide figures (up to 1166 px) are alone on their slide.
3. Check every figure: `python3 figures/check_size.py NAME W H` (run it with the system python) and look at the PNG from `figures/preview.py NAME`.
4. The same run command as before: `cd slides/m09 && uv run --quiet --with numpy --with scipy --with networkx --with pillow --with scikit-image python figures/fig_<group>.py`.
5. Only edit your own `figures/fig_<group>.py` and the files it writes. No git. If you need a helper that `common.py` lacks, write it in your file.
6. **Convolution is true convolution** now (the user caught that v3 drew cross-correlation): use `scipy.signal.convolve2d(x, K, mode="valid" or "same")`, i.e. `Y[i,j] = sum_{a,b} K[a,b] X[i-a, j-b]`. Recompute every output (a02, a03, a04).
   Kernels: Sobel "vertical edge" [[1,0,-1],[2,0,-2],[1,0,-1]], "horizontal edge" [[1,2,1],[0,0,0],[-1,-2,-1]], blur = ones/9. Show the kernel as written; the output is the true convolution.
7. Keep function names of v3 figures where a figure continues (the deck refers to `figures/<name>.svg`). Delete nothing that other groups use.

## Figures by group (box = max W x H in px)

### fig_a1.py
- **a01_pixels** 700x560. Same content as v3. Photo about 220 px with the 4x4 lavender patch, arrow, the patch as a matrix of its real 3-digit gray values (cells about 90x58 px, brackets). Labels "image", "4 × 4 pixels".
- **a02_conv_window** 1166x520 (alone on its slide). Input 6x6 integers (cells about 70 px), the 3x3 window in lavender, "∗", kernel 3x3, "=", output 4x4 with the cell of this window lavender. All numbers real (true convolution). Labels "input", "kernel", "output". Numbers 52 px, so cells must be at least 66 px wide.
- **a03_kernel_outputs** 1166x600 (alone). Photo (about 280 px) at left; three rows to its right: row label ("vertical edge" / "horizontal edge" / "blur" at 52 px), kernel matrix, arrow, output image (about 170 px). True convolution. Rows must fit in 600 px of height.
- **a04_playground** 1166x420 (alone, centred). Three panels "Image", "Kernel", "Output": photo 230 px, editable-looking 3x3 grid (kernel [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]], lavender frame), output 230 px (true convolution), arrows; a tag "interactive". Labels 52 px.
- **a06_waves_1d** 560x600. Same as v3 with 52 px labels ("$c_1$", "$c_3$", "$c_7$", "+" and "=" signs, "f(t)" and "t").
- **a13_image_row** (NEW) 700x600. The photo (about 300 px) with one row highlighted as a thin lavender band across the image; an arrow down; below it the real gray values along that row as a smooth black curve (resample the row to about 200 points, 2 px line), axis "t", curve label "f(t)". Labels "image" and "one row". This slide says: a row of pixels is a signal.

### fig_a2.py
- **a07_time_freq** 700x600. Same content as v3, 52 px labels ("time domain", "frequency domain", "slow", "fast", tick numbers 0..8 may be reduced to 0, 4, 8 if crowded, `|c_k|`).
- **a08_conv_theorem** 700x600. Two rows x three columns of small curves / dot plots with "∗", "=", "×", "=" signs and the label "Fourier transform" on the arrows. Row labels "spatial" and "spectral" at 52 px (put them above-left of each row if the left side is too narrow). Curves about 160 px wide.
- **a09_wave_2d** 700x560. Stripes image 250 px at the left; at the right a frequency plane with axes "u", "v", a lavender dot at (3, 2), a vector from the origin to the dot. Labels: "length = frequency" on the vector (write "length" only near the vector and "frequency" in the text on the slide if no room), "angle = direction"; add the word "phase" as a short note (phase = a shift of the stripes), e.g. a second small stripes image shifted by half a period with the label "phase". Keep it clear and sparse.
- **a10_fft_interactive** (NEW; the old a10_fft_image may stay) 1166x520 (alone). Three panels: image X (270 px), its log-magnitude centred 2D spectrum (270 px) with one selected point drawn as a lavender ring and a short cursor/click mark, then an arrow to the wave of that point (270 px stripes). Labels "image X", "spectrum", "wave". A tag "interactive". The selected point must be computed so the wave panel really shows that (u, v).
- **a14_wave_interactive** (NEW) 1166x520 (alone). Left: the stripes image (about 420 px) for u=3, v=2, phase 0. Right: three slider rows labelled "u", "v", "phase" with the values "3", "2", "0" (52 px); a slider is a thin line with a lavender dot at the value. A tag "interactive". Looks like a UI mock but stays black/white/lavender.
- **a11_masks** 1166x600 (alone). Three columns "original", "keep low", "keep high". Top row spectra, bottom row images, images about 230 px, arrows between, column labels 52 px above. Total height at most 600.
- **a12_kernel_response** 1166x600 (alone). Three columns: kernel matrix (3x3 at 52 px; for blur write the prefix "1/9" at its left) over its frequency response image (about 230 px), column names "blur", "vertical edge", "horizontal edge" under; a tag "bright = passed".

### fig_b.py
- **b01_grid_to_graph** 1166x420 (alone). Three stages "pixels" -> "edges" -> "graph" with black triangles. Nodes carry no text, so they may be 36-44 px. Labels 52 px.
- **b02_pixel_vs_node** 560x520. A pixel with its 8 neighbours (colour per position) and a node with 4 equal neighbours. Labels "by position" and "by edge".
- **b03_untrained_gcn** 1166x520 (alone). Two panels about 520x400: karate club (clubs coloured) and the untrained GCN output (same colours). Keep the same seed as v3. Labels "karate club" and "GCN output" (52 px).
- **b04_gcn_layer_node** 600x560. Same flow as v3 with 52 px labels ("$\hat A_{ij}$" on the arrows, "$W$", "$\sigma$", "Σ").
- **b05_norm_weights** 640x560. Hub node with 4 neighbours, self-loops, degree $\tilde d$ inside each node (66 px circles), every edge labelled with its weight (2 decimals, 52 px with white background). Hub edges lavender. Make it big enough that no label touches a node or another label. Caption "node = $\tilde d$" may be dropped (the slide says it).
- **b06_matrix_picture** 700x420. $\hat A$ (n x n, sparse black dots, one lavender row) × $H$ (n x d tall) × $W$ (d x d' small) = $H'$ (n x d'). Letters n, d, d' and the names $\hat A$, $H$, $W$, $H'$ at 52 px.
- **b07_receptive_graph** 1166x440 (alone). Only the graph row now (the pixel-grid row is deleted): the same 13-node graph three times, centre node black; nodes within 1, 2, 3 hops lavender steps. Column labels "1 layer", "2 layers", "3 layers" (52 px). Nodes carry no text (36-44 px).
- **b08_smoothing_4** (renamed from b08_smoothing_6; write `b08_smoothing_4.svg`) 660x620. Four karate panels in 2x2 (layers 0, 1, 3, 20), global colour scale as in v3, label "layer l" (52 px) inside each panel. Panels about 320x290.
- **b09_explosion** 640x600. Computation tree, root lavender, level counts at the right ("1", "5", "25", "125"), level names at the left ("hop 0".."hop 3"), 52 px. 2-3 grandchildren drawn in full and "…" for the rest. Nodes carry no text.

### fig_c.py
- **c01_sampling_tree** 700x600. Left the small graph with target, sampled (solid) and unsampled (dashed grey) neighbours; right the computation tree with upward arrows labelled "aggregate" (once). Drop the level names and the "uniform sample" tag. Nodes without text may be 36-44 px.
- **c02_sage_concat** 560x560. Self (blue squares), neighbours (mean) (vermillion squares), "‖", concatenated vector, arrow, box $W$, new vector (lavender). Labels "self", "neighbours" (mean in the slide text), 52 px.
- **c03_concat_vs_sum** 600x560 (CHANGED, simpler). The user said the two-case figure was not clear and only the left part is fine, so show **one case**: nodes u (lavender ring, feature a in blue) and v (feature b in vermillion) joined by an edge. Under it two rows: "sum" -> one vector with two stacked colours mixed (draw it as two half-width stripes blended: use a hatched / two-colour square so that it reads as "mixed, can't tell who is who"); "concat" -> a two-slot vector [blue | vermillion] with the left slot marked "self" and the right "neighbour". Words: "sum", "concat", "self", "neighbour" only.
- **c04_gcn_vs_gat** 700x520. Two panels "GCN" and "GAT" with a centre node and 5 coloured neighbours, line widths as in SPEC.md.
- **c05_attention_visual** 640x400 (CHANGED; the slide also holds a formula below). Node i with 3 neighbours j1..j3; at each neighbour the score $e_{ij}$ (1.2, 0.1, -0.5), arrow "softmax", weight $\alpha_{ij}$ (real softmax: 0.66, 0.22, 0.12), edge width by weight. Tags "scores" and "weights" (52 px; "weights sum to 1" goes in the slide text). Make it compact in height.
- **c06_mp_flow** 560x600. Neighbours -> message $\varphi$ -> aggregate $\bigoplus$ -> update $\psi$ -> new feature; step numbers 1, 2, 3 in black discs; 52 px labels.
- **c08_readout** 560x480. Five-node graph with feature vectors, arrow to $\bigoplus$, graph vector (lavender), arrow to a box "classifier", output "class".
- (c07_three_models_mini is dropped.)

### fig_d.py
- **d01_cycle_vs_triangles** 1166x330 (alone, text below it on the slide). 6-cycle and two triangles, all nodes the same grey, labels "6-cycle" and "two triangles" (52 px). Nodes carry no text (44-52 px).
- **d02a_wl_collect**, **d02b_wl_table**, **d02c_wl_result** (NEW, replace d02_wl_iteration; the user asked for an animation, so build three key-frames of the same 5-node graph, same layout, same colours, each 640x580):
  - d02a: iteration 0 colours (3 colours: vermillion, blue, yellow); one node ringed lavender; next to it its neighbour colours as a multiset of coloured squares inside braces, e.g. "{■ ■}". Word: "iteration 0".
  - d02b: the table, one row per distinct (own colour, neighbour multiset) with a coloured square for own colour, braces with neighbour squares, arrow, the NEW colour square (a new colour per distinct row; use sky, pink, lavender, grey-blue; no green). All rows real from the WL step. No words except maybe "new".
  - d02c: iteration 1: the same graph recoloured with the new colours (real), and the iteration 0 graph small on the left (nodes 36 px) with an arrow. Word: "iteration 1".
- **d03_path_star** 700x600. Path of 4 and star of 4, rows "iteration 0", "iteration 1", "histogram" (52 px; the row labels may be rotated or above the rows), histogram = dot columns above colour swatches.
- **d04_wl_fail** 1166x600 (alone). Rows "iteration 0", "1", "2": 6-cycle and two triangles (about 220 px wide), all grey, "=" between; under: "6 ×" and a grey dot as the histogram. No bullets on the slide, so make this figure carry the message: put "same histogram" as one label.
- **d05_wl_gnn_correspondence** 700x560. Two columns "WL" and "GNN", three rows joined by lines: "label $c_i$" - "feature $h_i$"; "neighbour labels" (two lines) - "message $m_i$" (shorter than v3); "HASH" - "update $\psi$". Middle row lavender.
- **d06_theorem** 600x560. The 6-cycle and the two triangles (about 200 px) with "≠" between them; under: boxes "WL: equal" and "GNN: equal" with an arrow. Sparse.
- **d07_aggregators** 640x420 (CHANGED, shared with the GIN formula on one slide). Two multisets in boxes ({R,R,B,B} and {R,B}); rows "sum" -> (2,2) | (1,1) "different"; "mean" -> (.5,.5) | (.5,.5) "same"; "max" -> (1,1) | (1,1) "same". At 52 px this is tall: use a compact layout (two columns of results). Height at most 420.

### fig_e.py
- **e01_khop** 600x560. 16-node graph, hop shading in the lavender scale, tags $\theta_0..\theta_3$ (52 px), no "K = 3" if it does not fit (the slide says it). Nodes carry no text (36-44 px).
- **f01_gcn_fourier** (NEW) 1166x560 (alone). Two columns, "image" at the left and "graph" at the right (52 px headings). Left: a small gray image patch with a 3x3 blur kernel, label "convolution"; an arrow down labelled "Fourier" to a small picture of waves (a sine curve). Right: a small graph with node i (lavender) and 3 neighbours with arrows into i, label "GCN step"; an arrow down labelled "?" to a question mark where the waves would be ("waves on a graph?" is too long: use the big "?" only). A thin vertical divider between the columns.
- **f02_smoothness** (NEW) 1166x440 (alone). Two karate panels (about 420x330) with a real signal on the nodes: the left x = the Fiedler vector (smallest nonzero Laplacian eigenvalue, unit norm), the right x = the eigenvector of the LARGEST eigenvalue (unit norm); colours on the diverging scale. Under each panel its real smoothness $J = \sum_{i,j} A_{ij}(x_i - x_j)^2$ rounded to 1 decimal (it equals $2\lambda$), as "J = 0.9" style text, and the words "low frequency" / "high frequency" (52 px). Edges light grey.
- **e02_laplacian_diff** 640x600. 6-node graph with integers x_i in the nodes (66 px circles), each edge labelled with $x_i - x_j$ (52 px, white background), one lavender node with the callout $(Lx)_i = 7 + 2 + 5 = 14$ (real) placed where it fits; the other nodes' values must keep it readable. It is allowed to enlarge the graph to the full 640 x 600.
- **e03_eigvecs_karate** 660x620. 2x2 karate panels for $\lambda_1 = 0$, $\lambda_2$, $\lambda_{10}$, $\lambda_{34}$; labels (52 px) inside the panels' top-left or above them.
- **e04_spectral_conv_flow** 640x600. Vertical flow $x$ -> $U^\top$ -> $\hat x$ -> "× $g(\lambda)$" (with a tiny low-pass curve) -> $g(\Lambda)\hat x$ -> $U$ -> $y$, dots for the signals (8 dots, real). 52 px labels. Use a two-column layout of the flow if one column is too tall.
- **e05_nested_models** 640x560. Nested boxes "spectral conv" > "ChebNet" > "GCN" with curves; 52 px labels (use "spectral", "Cheb", "GCN" if the long names do not fit).
- **e06_masks_karate** 1166x400 (alone). Three karate panels (about 340 px) "x", "low", "high" (52 px).
- **e07_highfreq_boundary** 700x600. Karate club, node size/colour by the high-frequency part, between-club edges thick black, a callout "boundary" at a large node. Same verified numbers as v3.
- **e08_summary_visuals** 380x600. Three stacked icons with labels "convolution", "message passing", "low-pass" (52 px: shorten "low-pass filter" to "low-pass"); frames 2 px black, 14 px gap.

## Report back (short)
For each figure: file, px size, changes from this spec and why, problems left. Do not run git.

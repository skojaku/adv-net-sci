---
marp: true
theme: math
paginate: true
---

<style>
/* v3 (2026-11-08): minimum type size 26 pt = 35 px for everything but the page number.
   Figure left, explanation right. Titles are short; there is no lead sentence. */
section { justify-content: center; --fs: 35px; --fs-lead: 35px; --fs-title: 40px; --fs-small: 35px; --fs-code: 35px; padding: 84px 56px 40px 57px; line-height: 1.35; }
section > h2 { top: 16px; font-size: 40px; line-height: 48px; }
section > h2::before { height: 48px; }
section::after { font-size: 22px; bottom: 10px; right: 24px; }
section .katex-display { font-size: 1.15em; margin: 0.25em 0 0.25em 0.2em; }
section .eq-sm .katex-display { font-size: 1em; }
section .eq-lg .katex-display { font-size: 1.35em; }
section .katex { font-size: 1.05em; }
section .box[data-tab] { margin-top: 24px; padding-top: 30px; }
section .box[data-tab]::before { font-size: 35px; height: 46px; line-height: 46px; top: -24px; }
section .box { padding: 12px 22px; margin: 0 0 12px; }
section ul, section ol { margin: 0 0 0.3em; padding-left: 1.1em; }
section li { margin: 0 0 0.25em; }
section table { font-size: 35px; }
section .cols { gap: 28px; align-items: center; }
section .cols.fig560 { grid-template-columns: 560px minmax(0, 1fr); }
section .cols.fig600 { grid-template-columns: 600px minmax(0, 1fr); }
section .cols.fig620 { grid-template-columns: 620px minmax(0, 1fr); }
section .cols.fig640 { grid-template-columns: 640px minmax(0, 1fr); }
section .cols.fig700 { grid-template-columns: 700px minmax(0, 1fr); }
section .cols.fig720 { grid-template-columns: 720px minmax(0, 1fr); }
section .cols.fig760 { grid-template-columns: 760px minmax(0, 1fr); }
section .cols > div > p > img, section > p > img { display: block; max-width: none; }
section .cols > div > p { margin: 0; }
section.title .by { font-size: 35px; margin-top: 30px; }
section.title > h2 + p { font-size: 38px; }
section.divider { padding: 72px 80px 72px 78px; }
section.divider > h2 { font-size: 76px; line-height: 1.15; margin: 0; }
section .vid { margin-top: 10px; }
</style>

<!-- _class: title -->
<!-- _paginate: false -->

# GNN

## <span class="hot">Graph</span> neural networks

From convolution to message passing

<p class="by">Sadamori Kojaku</p>

---

<!-- _class: divider -->

## Convolution and the Fourier transform on images

---

## Images are arrays of pixels

<div class="cols fig700">
<div>

![](figures/a01_pixels.svg)

</div>
<div>

- gray image: a matrix $X \in \mathbb{R}^{H \times W}$
- color image: three matrices $R$, $G$, $B$

</div>
</div>

---

## Convolution with a kernel

<div class="cols fig720">
<div>

![](figures/a02_conv_window.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Convolution">

$$Y_{ij} = \sum_{a,b=-1}^{1} K_{ab}\, X_{i+a,\, j+b}$$

</div>

sum over the $3 \times 3$ window

</div>
</div>

---

## The kernel sets the pattern

<div class="cols fig700">
<div>

![](figures/a03_kernel_outputs.svg)

</div>
<div>

- each kernel responds to one pattern
- blur: the mean of 9 pixels

</div>
</div>

---

## Try your own kernel

<div class="cols fig760">
<div>

![](figures/a04_playground.svg)

</div>
<div>

- change the 9 numbers
- predict the output

</div>
</div>

---

## The kernel is local and shared

<div class="cols fig700">
<div>

![](figures/a05_receptive_planes.svg)

</div>
<div>

- <mark>local</mark>: only neighbors enter
- <mark>shared</mark>: the same $K$ everywhere
- $L$ layers: $(2L+1)^2$ pixels

</div>
</div>

---

<!-- one dimension first, then two (the lecturer's note) -->

## A signal is a sum of waves

<div class="cols fig560">
<div>

![](figures/a06_waves_1d.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Fourier series">

$$f(t) = \sum_{k} c_k\, e^{2\pi i k t / T}$$

$$c_k = \frac{1}{T} \int_0^T f(t)\, e^{-2\pi i k t / T}\, dt$$

</div>

$c_k$: the weight of wave $k$

</div>
</div>

---

## Time domain and frequency domain

<div class="cols fig700">
<div>

![](figures/a07_time_freq.svg)

</div>
<div>

- low $k$: slow wave
- high $k$: fast wave
- $(c_k)$ describes $f$ as completely as $f(t)$

</div>
</div>

---

## Convolution becomes multiplication

<div class="cols fig700">
<div>

![](figures/a08_conv_theorem.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Convolution theorem">

$$\widehat{f * g}_k = \hat f_k \, \hat g_k$$

</div>

- $\hat f_k = c_k$: the Fourier transform of $f$
- $g$ is a filter: it scales frequency $k$ by $\hat g_k$

</div>
</div>

---

## Waves in two dimensions

<div class="cols fig640">
<div>

![](figures/a09_wave_2d.svg)

</div>
<div>

<div class="box eq-sm" data-tab="2D wave">

$$e^{2\pi i (ux + vy)}$$

</div>

- direction: the angle of $(u, v)$
- frequency: $\sqrt{u^2 + v^2}$

<p class="vid">Video: 3Blue1Brown, <a href="https://www.youtube.com/watch?v=spUNpyF58BY">But what is the Fourier Transform?</a></p>

</div>
</div>

---

## The 2D Fourier transform of an image

<div class="cols fig640">
<div>

![](figures/a10_fft_image.svg)

</div>
<div>

<div class="box eq-sm" data-tab="2D Fourier transform">

$$\hat X_{uv} = \sum_{x,y} X_{xy}\, w_{uv}(x, y)$$

$$w_{uv}(x, y) = e^{-2\pi i (ux/H + vy/W)}$$

</div>

$w_{uv}$: the wave $(u, v)$; $\hat X_{uv}$: its weight

</div>
</div>

---

## Keeping low or high frequencies

<div>

![](figures/a11_masks.svg)

</div>

---

## Kernels are filters on frequencies

<div>

![](figures/a12_kernel_response.svg)

</div>

---

<!-- _class: divider -->

## From image to graph

---

## An image is a graph

<div class="cols fig700">
<div>

![](figures/b01_grid_to_graph.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Adjacency">

$$A_{pq} = \begin{cases} 1 & p, q \text{ neighbors} \\ 0 & \text{otherwise} \end{cases}$$

</div>

any graph: the same rule

</div>
</div>

---

## Convolution is a sum over neighbors

<div class="cols fig560">
<div>

![](figures/b02_pixel_vs_node.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Image">

$$Y_p = \sum_{q \in N(p) \cup \{p\}} K_{q-p}\, X_q$$

</div>
<div class="box eq-sm" data-tab="Graph">

$$h_i' = \sum_{j \in N(i) \cup \{i\}} w_{ij}\, h_j$$

</div>
</div>
</div>

---

<!-- _class: divider -->

## Graph convolutional network (GCN)

---

## An untrained GCN groups the nodes

<div class="cols fig700">
<div>

![](figures/b03_untrained_gcn.svg)

</div>
<div>

- no training
- random weights
- same club: close together

</div>
</div>

---

## The GCN layer

<div class="cols fig560">
<div>

![](figures/b04_gcn_layer_node.svg)

</div>
<div>

<div class="box eq-sm" data-tab="GCN layer">

$$h_i^{(l+1)} = \sigma\Big(\sum_{j} \hat A_{ij}\, h_j^{(l)} W^{(l)}\Big)$$

</div>

- $j \in N(i) \cup \{i\}$
- $W$: learned, $\sigma$: ReLU

</div>
</div>

---

## GCN weights neighbors by degree

<div class="cols fig620">
<div>

![](figures/b05_norm_weights.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Normalized adjacency">

$$\hat A = \tilde D^{-1/2}\, (A + I)\, \tilde D^{-1/2}$$

</div>

- $\hat A_{ij} = 1/\sqrt{\tilde d_i \tilde d_j}$
- many neighbors: small weight
- a hub does not dominate

</div>
</div>

---

## The GCN layer in matrix form

<div class="cols fig640">
<div>

![](figures/b06_matrix_picture.svg)

</div>
<div>

<div class="box eq-sm" data-tab="GCN layer">

$$H^{(l+1)} = \sigma\big(\hat A\, H^{(l)} W^{(l)}\big)$$

</div>

one row per node

</div>
</div>

---

## Stacking layers widens the view

<div class="cols fig760">
<div>

![](figures/b07_receptive_graph.svg)

</div>
<div>

- $L$ layers: nodes within $L$ hops
- image: $(2L+1)^2$ pixels

</div>
</div>

---

## Neighbor averaging smooths the signal

<div class="cols fig700">
<div>

![](figures/b08_smoothing_6.svg)

</div>
<div>

- $\hat A$ acts like a blur kernel
- many layers: over-smoothing
- the values end up set by the degrees

</div>
</div>

---

<!-- _class: divider -->

## GraphSAGE and GAT

---

## A full neighborhood grows too fast

<div class="cols fig700">
<div>

![](figures/b09_explosion.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Cost">

$$\text{nodes} \approx d^{L}$$

</div>

- $d$: average degree
- $L$: number of layers

</div>
</div>

---

## GraphSAGE samples a neighborhood

<div class="cols fig700">
<div>

![](figures/c01_sampling_tree.svg)

</div>
<div>

- $s$ neighbors per node
- sampled uniformly at random
- aggregate from leaves to root

</div>
</div>

---

## The GraphSAGE layer

<div class="cols fig560">
<div>

![](figures/c02_sage_concat.svg)

</div>
<div>

<div class="box eq-sm" data-tab="GraphSAGE layer">

$$h_i^{(l+1)} = \sigma\big([\, h_i^{(l)} \,\|\, m_i \,]\, W\big)$$

$$m_i = \mathrm{AGG}_{j \in S(i)}\, h_j^{(l)}$$

</div>

- $\|$: concatenation
- AGG: mean

</div>
</div>

---

## Concatenation keeps the node's own feature

<div class="cols fig600">
<div>

![](figures/c03_concat_vs_sum.svg)

</div>
<div>

<div class="box eq-sm" data-tab="GCN">

$$(h_i + h_j)\, W$$

</div>
<div class="box eq-sm" data-tab="GraphSAGE">

$$h_i W_1 + h_j W_2$$

</div>
</div>
</div>

---

## Neighbors differ in importance

<div class="cols fig700">
<div>

![](figures/c04_gcn_vs_gat.svg)

</div>
<div>

- GCN: weight from degrees
- GAT: weight learned from features

</div>
</div>

---

## The attention coefficient

<div class="box" data-tab="GAT layer">

$$e_{ij} = \mathrm{LeakyReLU}\big(a^\top [\, h_i W \,\|\, h_j W \,]\big)$$

$$\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k \in N(i) \cup \{i\}} \exp(e_{ik})}, \qquad h_i' = \sigma\Big(\sum_j \alpha_{ij}\, h_j W\Big)$$

</div>

- $e_{ij}$: score of the edge, from the two features
- $\alpha_{ij}$: softmax of the scores over the neighbors

---

## Attention in one neighborhood

<div class="cols fig700">
<div>

![](figures/c05_attention_visual.svg)

</div>
<div>

- score each edge
- softmax: weights sum to 1
- larger weight, larger share

</div>
</div>

---

<!-- _class: divider -->

## GCN, GraphSAGE, GAT as message passing

---

## The message passing framework

<div class="cols fig560">
<div>

![](figures/c06_mp_flow.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Message passing">

$$m_i = \bigoplus_{j \in N(i)} \varphi\big(h_i, h_j\big)$$

$$h_i' = \psi\big(h_i, m_i\big)$$

</div>

$\bigoplus$: sum, mean or max

</div>
</div>

---

## Each model chooses $\varphi$, $\bigoplus$, $\psi$

<div class="cols" style="grid-template-columns: minmax(0, 1fr) 440px;">
<div>

| | $\varphi$ | $\bigoplus$ | $\psi$ |
|---|---|---|---|
| GCN | $\hat A_{ij} h_j$ | sum | $\sigma(m_i W)$ |
| GraphSAGE | $h_j$ | mean | $\sigma([h_i \Vert m_i] W)$ |
| GAT | $\alpha_{ij} h_j W$ | sum | $\sigma(m_i)$ |

</div>
<div>

![](figures/c07_three_models_mini.svg)

</div>
</div>

---

## Readout for a whole graph

<div class="cols fig560">
<div>

![](figures/c08_readout.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Readout">

$$h_G = \bigoplus_{i \in V} h_i^{(L)}$$

</div>

- sum, mean or max
- the node order does not matter

</div>
</div>

---

<!-- _class: divider -->

## Message passing ≈ WL test

---

## Can a GNN tell them apart?

<div class="cols fig700">
<div>

![](figures/d01_cycle_vs_triangles.svg)

</div>
<div>

- 6 nodes each
- every node: degree 2
- every node: same feature

</div>
</div>

---

## The Weisfeiler–Lehman test

<div class="cols fig620">
<div>

![](figures/d02_wl_iteration.svg)

</div>
<div>

<div class="box eq-sm" data-tab="WL iteration">

$$c_i^{(t+1)} = \mathrm{HASH}\big(c_i^{(t)},\, M_i^{(t)}\big)$$

$$M_i^{(t)} = \{\!\{ c_j^{(t)} : j \in N(i) \}\!\}$$

</div>

$M_i$: the multiset of neighbor labels

</div>
</div>

---

## WL separates a path from a star

<div class="cols fig700">
<div>

![](figures/d03_path_star.svg)

</div>
<div>

- path: 2 + 2
- star: 1 + 3
- histograms differ: not isomorphic

</div>
</div>

---

## WL cannot separate a 6-cycle from two triangles

<div class="cols fig700">
<div>

![](figures/d04_wl_fail.svg)

</div>
<div>

- same label, same neighbor labels
- the histogram never changes
- the graphs are not isomorphic

</div>
</div>

---

## WL steps correspond to GNN modules

<div class="cols fig700">
<div>

![](figures/d05_wl_gnn_correspondence.svg)

</div>
<div>

each WL step has a counterpart in a message passing layer

</div>
</div>

---

## Correspondence in formulas

<div class="box" data-tab="WL">

$$c_i^{(t+1)} = \hl{\mathrm{HASH}}\big(c_i^{(t)},\ \{\!\{ c_j^{(t)} \}\!\}_{j \in N(i)}\big)$$

</div>
<div class="box" data-tab="Message passing">

$$h_i^{(l+1)} = \hl{\psi}\big(h_i^{(l)},\ \bigoplus_{j \in N(i)} \varphi(h_i^{(l)}, h_j^{(l)})\big)$$

</div>

---

## A GNN is at most as strong as the WL test

<div class="cols fig700">
<div>

![](figures/d06_theorem.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Theorem">

$$c_u^{(t)} = c_v^{(t)} \Rightarrow h_u^{(t)} = h_v^{(t)}$$

</div>

Xu et al. 2019, Morris et al. 2019

</div>
</div>

---

## Mean and max lose information that sum keeps

<div class="cols fig700">
<div>

![](figures/d07_aggregators.svg)

</div>
<div>

- sum keeps the counts
- mean and max lose them

</div>
</div>

---

## GIN reaches the WL limit

<div class="box" data-tab="GIN layer">

$$h_i^{(l+1)} = \mathrm{MLP}\Big((1 + \epsilon)\, h_i^{(l)} + \sum_{j \in N(i)} h_j^{(l)}\Big)$$

</div>

- sum aggregation
- injective update (MLP)
- separates exactly what WL separates (Xu et al. 2019)

---

<!-- _class: divider -->

## The spectral view of GCN

---

## One layer can look more than one hop

<div class="cols fig600">
<div>

![](figures/e01_khop.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Polynomial filter">

$$y = \sum_{k=0}^{K} \theta_k\, \hat A^{k} x$$

</div>
<div class="box eq-sm" data-tab="ChebNet">

$$y = \sum_{k=0}^{K} \theta_k\, T_k(\tilde L)\, x$$

</div>

$T_k$: Chebyshev polynomial

</div>
</div>

---

## The Laplacian measures differences

<div class="cols fig620">
<div>

![](figures/e02_laplacian_diff.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Laplacian">

$$(Lx)_i = \sum_{j \in N(i)} (x_i - x_j)$$

$$x^\top L x = \sum_{(i,j) \in E} (x_i - x_j)^2$$

</div>

small: $x$ is smooth, low frequency

</div>
</div>

---

## Eigenvectors of the Laplacian are waves on a graph

<div class="cols fig700">
<div>

![](figures/e03_eigvecs_karate.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Eigenvector">

$$L u_k = \lambda_k u_k$$

</div>

- $\lambda_k$: the frequency
- small: neighbors alike
- large: neighbors differ

</div>
</div>

---

## Spectral convolution

<div class="cols fig640">
<div>

![](figures/e04_spectral_conv_flow.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Graph Fourier transform">

$$\hat x = U^\top x$$

$$y = U\, g(\Lambda)\, \hat x$$

</div>

- $L = U \Lambda U^\top$
- $g$: a filter on frequencies

</div>
</div>

---

## ChebNet and GCN are special cases

<div class="cols fig640">
<div>

![](figures/e05_nested_models.svg)

</div>
<div>

<div class="box eq-sm" data-tab="ChebNet">

$$g(\lambda) = \sum_{k=0}^{K} \theta_k \lambda^k$$

</div>
<div class="box eq-sm" data-tab="GCN">

$$g(\lambda) = 1 - \tilde\lambda$$

</div>
</div>
</div>

---

## Masking frequencies on the karate club

<div class="cols fig700">
<div>

![](figures/e06_masks_karate.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Frequency mask">

$$x_{\mathrm{low}} = U\, \mathrm{diag}(m)\, U^\top x$$

</div>

$m_k = 1$ for $\lambda_k \le c$

</div>
</div>

---

## The high-frequency part on the karate club

<div class="cols fig700">
<div>

![](figures/e07_highfreq_boundary.svg)

</div>
<div>

- largest: nodes 34, 1, 33 and 3
- node 3: 4 of the 11 edges between the clubs

</div>
</div>

---

## Summary

<div class="cols" style="grid-template-columns: minmax(0, 1fr) 380px; align-items: center;">
<div>

- convolution: a sum over neighbors
- GCN, GraphSAGE, GAT: message passing
- GNN $\le$ WL test; GIN reaches it
- GCN: a low-pass filter on the eigenvalues of $L$

</div>
<div>

![](figures/e08_summary_visuals.svg)

</div>
</div>

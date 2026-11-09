---
marp: true
theme: math
paginate: true
---

<style>
/* v4 (2026-11-09): minimum type size 39 pt = 52 px for everything but the page number (1.5 x v3).
   No slide titles (the user allowed dropping them for space). Figure on one side, explanation on the other. */
section { justify-content: center; --fs: 52px; --fs-lead: 52px; --fs-title: 56px; --fs-small: 52px; --fs-code: 52px; padding: 36px 57px 36px 57px; line-height: 1.3; }
section::after { font-size: 22px; bottom: 10px; right: 24px; }
section .katex-display { font-size: 1em; margin: 0.2em 0 0.2em 0.1em; }
section .eq-sm .katex-display { font-size: 1em; }
section .eq-lg .katex-display { font-size: 1.2em; }
section .katex { font-size: 1em; }
section .box[data-tab] { margin-top: 36px; padding-top: 40px; }
section .box[data-tab]::before { font-size: 52px; height: 62px; line-height: 62px; top: -33px; }
section .box { padding: 10px 22px; margin: 0 0 12px; }
section ul, section ol { margin: 0 0 0.3em; padding-left: 1em; }
section li { margin: 0 0 0.2em; }
section table { font-size: 52px; margin: 0 auto; }
section p { margin: 0 0 0.3em; }
section .cols { gap: 28px; align-items: center; }
section .cols.fig560 { grid-template-columns: 560px minmax(0, 1fr); }
section .cols.fig600 { grid-template-columns: 600px minmax(0, 1fr); }
section .cols.fig640 { grid-template-columns: 640px minmax(0, 1fr); }
section .cols.fig660 { grid-template-columns: 660px minmax(0, 1fr); }
section .cols.fig700 { grid-template-columns: 700px minmax(0, 1fr); }
section .cols > div > p > img, section > p > img, section .c > p > img { display: block; max-width: none; }
section .cols > div > p { margin: 0; }
section .c { text-align: center; }
section .c > p > img { margin: 0 auto; }
section .under { text-align: center; margin: 8px 0 0; }
section .cite { color: #555; margin-top: 10px; }
section .vid { margin-top: 14px; }
section.title > h2 { font-size: 112px; line-height: 1.1; }
section.title > h2 + p { font-size: 52px; }
section.title .by { font-size: 52px; margin-top: 36px; }
section.divider { padding: 72px 80px 72px 78px; }
section.divider > h2 { font-size: 88px; line-height: 1.15; margin: 0; }
</style>

<!-- _class: title -->
<!-- _paginate: false -->

## <span class="hot">Graph</span> neural networks

From convolution to message passing

<p class="by">Sadamori Kojaku</p>

---

<!-- _class: divider -->

## Convolution and the Fourier transform on images

---

<div class="cols fig700">
<div>

![](figures/a01_pixels.svg)

</div>
<div>

- gray image: a matrix $X$
- color image: three matrices

</div>
</div>

---

<div class="c">

![](figures/a02_conv_window.svg)

</div>

---

<div class="box" data-tab="Convolution">

$$Y_{ij} = \sum_{a,b=-1}^{1} K_{ab}\, X_{i-a,\, j-b}$$

</div>

- sum over the $3 \times 3$ window
- the kernel is flipped

---

<div class="c">

![](figures/a03_kernel_outputs.svg)

</div>

---

<div class="c">

![](figures/a04_playground.svg)

<p class="under">change the 9 numbers, predict the output</p>

</div>

---

<div class="cols fig700">
<div>

![](figures/a13_image_row.svg)

</div>
<div>

- a row of pixels is a signal
- a signal is a sum of waves

</div>
</div>

---

<div class="cols fig560">
<div>

![](figures/a06_waves_1d.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Fourier series">

$$f(t) = \sum_k c_k\, e^{2\pi i k t / T}$$

</div>

$c_k$: the weight of wave $k$

<p class="vid">▶ 3Blue1Brown, <a href="https://www.youtube.com/watch?v=r6sGWTCMz2k">But what is a Fourier series?</a></p>

</div>
</div>

---

<div class="cols fig700">
<div>

![](figures/a07_time_freq.svg)

</div>
<div>

- low $k$: slow wave
- high $k$: fast wave
- $(c_k)$ describes $f$

</div>
</div>

---

<div class="cols fig700">
<div>

![](figures/a08_conv_theorem.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Theorem">

$$\widehat{f * g}_k = \hat f_k \, \hat g_k$$

</div>

- $g$: a filter
- it scales frequency $k$

</div>
</div>

---

<div class="c">

![](figures/a14_wave_interactive.svg)

</div>

---

<div class="cols fig700">
<div>

![](figures/a09_wave_2d.svg)

</div>
<div>

<div class="box eq-sm" data-tab="2D wave">

$$e^{2\pi i (ux + vy)}$$

</div>

- direction: the angle of $(u, v)$
- frequency: the length of $(u, v)$
- phase: a shift

</div>
</div>

---

<div class="c">

![](figures/a10_fft_interactive.svg)

</div>

---

<div class="box" data-tab="2D Fourier transform">

$$\hat X_{uv} = \sum_{x,y} X_{xy}\, w_{uv}(x, y)$$

$$w_{uv}(x, y) = e^{-2\pi i (ux/H + vy/W)}$$

</div>

- $w_{uv}$: the wave $(u, v)$
- $\hat X_{uv}$: its weight

---

<div class="c">

![](figures/a11_masks.svg)

</div>

---

<div class="c">

![](figures/a12_kernel_response.svg)

</div>

---

<!-- _class: divider -->

## From image to graph

---

<div class="c">

![](figures/b01_grid_to_graph.svg)

</div>

---

<div class="box" data-tab="Adjacency">

$$A_{pq} = \begin{cases} 1 & p, q \text{ neighbors} \\ 0 & \text{otherwise} \end{cases}$$

</div>

any graph: the same rule

---

<div class="cols fig560">
<div>

![](figures/b02_pixel_vs_node.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Image">

$$Y_p = \sum_{q} K_{p-q}\, X_q$$

</div>

<div class="box eq-sm" data-tab="Graph">

$$h_i' = \sum_{j} w_{ij}\, h_j$$

</div>

</div>
</div>

---

<!-- _class: divider -->

## Graph convolutional network (GCN)

---

<div class="c">

![](figures/b03_untrained_gcn.svg)

<p class="under">random weights, no training</p>

</div>

---

<div class="cols fig600">
<div>

![](figures/b04_gcn_layer_node.svg)

</div>
<div>

- sum over the neighbors
- multiply by $W$
- apply $\sigma$

</div>
</div>

---

<div class="box" data-tab="GCN layer">

$$h_i^{(l+1)} = \sigma\Big(\sum_j \hat A_{ij}\, h_j^{(l)} W^{(l)}\Big)$$

</div>

<div class="box" data-tab="Normalization">

$$\hat A = \tilde D^{-1/2} (A + I)\, \tilde D^{-1/2}$$

</div>

<p class="cite">Kipf & Welling 2017</p>

---

<div class="cols fig640">
<div>

![](figures/b05_norm_weights.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Weight">

$$\hat A_{ij} = \frac{1}{\sqrt{\tilde d_i \tilde d_j}}$$

</div>

- many neighbors: small weight
- a hub does not dominate

</div>
</div>

---

<div class="cols fig700">
<div>

![](figures/b06_matrix_picture.svg)

</div>
<div>

<div class="box eq-sm" data-tab="GCN layer">

$$H' = \sigma(\hat A\, H\, W)$$

</div>

one row per node

</div>
</div>

---

<div class="c">

![](figures/b07_receptive_graph.svg)

<div class="under">

$L$ layers: nodes within $L$ hops

</div>

</div>

---

<div class="cols fig660">
<div>

![](figures/b08_smoothing_4.svg)

</div>
<div>

- $\hat A$ blurs the signal
- many layers: over-smoothing
- the values end up set by the degrees

</div>
</div>

---

<!-- _class: divider -->

## GraphSAGE and GAT

---

<div class="cols fig640">
<div>

![](figures/b09_explosion.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Cost">

$$\text{nodes} \approx d^{L}$$

</div>

- $d$: average degree
- $L$: layers

</div>
</div>

---

<div class="cols fig700">
<div>

![](figures/c01_sampling_tree.svg)

</div>
<div>

- $s$ neighbors per node
- uniform at random
- aggregate leaves to root

<p class="cite">Hamilton et al. 2017</p>

</div>
</div>

---

<div class="cols fig560">
<div>

![](figures/c02_sage_concat.svg)

</div>
<div>

<div class="box eq-sm" data-tab="GraphSAGE layer">

$$h_i' = \sigma\big([\, h_i \,\|\, m_i \,]\, W\big)$$

$$m_i = \mathrm{AGG}_{j \in S(i)}\, h_j$$

</div>

- $\|$: concatenation
- AGG: mean

</div>
</div>

---

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

<div class="cols fig700">
<div>

![](figures/c04_gcn_vs_gat.svg)

</div>
<div>

- GCN: weights from degrees
- GAT: weights learned

<p class="cite">Veličković et al. 2018</p>

</div>
</div>

---

<div class="cols fig640">
<div>

![](figures/c05_attention_visual.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Attention">

$$\alpha_{ij} = \mathrm{softmax}_j(e_{ij})$$

$$h_i' = \sigma\big(\textstyle\sum_j \alpha_{ij}\, h_j W\big)$$

</div>

</div>
</div>

<div class="box eq-sm" data-tab="Score">

$$e_{ij} = \mathrm{LeakyReLU}\big(a^\top [\, h_i W \,\|\, h_j W \,]\big)$$

</div>

---

<!-- _class: divider -->

## GCN, GraphSAGE, GAT as message passing

---

<div class="cols fig560">
<div>

![](figures/c06_mp_flow.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Message passing">

$$m_i = \bigoplus_{j \in N(i)} \varphi(h_i, h_j)$$

$$h_i' = \psi(h_i, m_i)$$

</div>

$\bigoplus$: sum, mean or max

</div>
</div>

---

| | $\varphi$ | $\bigoplus$ | $\psi$ |
|---|---|---|---|
| GCN | $\hat A_{ij} h_j$ | sum | $\sigma(m_i W)$ |
| GraphSAGE | $h_j$ | mean | $\sigma([h_i \Vert m_i] W)$ |
| GAT | $\alpha_{ij} h_j W$ | sum | $\sigma(m_i)$ |

---

<div class="cols fig560">
<div>

![](figures/c08_readout.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Readout">

$$h_G = \bigoplus_{i \in V} h_i^{(L)}$$

</div>

- sum, mean or max
- node order does not matter

</div>
</div>

---

<!-- _class: divider -->

## Message passing ≈ WL test

---

<div class="c">

![](figures/d01_cycle_vs_triangles.svg)

<p class="under">every node has the same feature</p>

<p class="under">can a GNN tell them apart?</p>

</div>

---

<div class="cols fig640">
<div>

![](figures/d02a_wl_collect.svg)

</div>
<div>

- look at the neighbors' colors

<p class="cite">Weisfeiler & Lehman 1968</p>

</div>
</div>

---

<div class="cols fig640">
<div>

![](figures/d02b_wl_table.svg)

</div>
<div>

- same colors: same new color
- new color for each pair

</div>
</div>

---

<div class="cols fig640">
<div>

![](figures/d02c_wl_result.svg)

</div>
<div>

- repeat until nothing changes

</div>
</div>

---

<div class="cols fig700">
<div>

![](figures/d03_path_star.svg)

</div>
<div>

- path: 2 + 2
- star: 1 + 3
- histograms differ

</div>
</div>

---

<div class="c">

![](figures/d04_wl_fail.svg)

</div>

---

<div class="cols fig700">
<div>

![](figures/d05_wl_gnn_correspondence.svg)

</div>
<div>

WL step = GNN layer

</div>
</div>

---

<div class="box" data-tab="WL">

$$c_i^{(t+1)} = \hl{\mathrm{HASH}}\big(c_i^{(t)},\ \{\!\{ c_j^{(t)} \}\!\}_{j \in N(i)}\big)$$

</div>

<div class="box" data-tab="Message passing">

$$h_i^{(l+1)} = \hl{\psi}\big(h_i^{(l)},\ \bigoplus_{j \in N(i)} \varphi(h_i^{(l)}, h_j^{(l)})\big)$$

</div>

---

<div class="cols fig600">
<div>

![](figures/d06_theorem.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Theorem">

$$c_u = c_v \Rightarrow h_u = h_v$$

</div>

<p class="cite">Xu et al. 2019, Morris et al. 2019</p>

</div>
</div>

---

<div class="cols fig640">
<div>

![](figures/d07_aggregators.svg)

</div>
<div>

- sum keeps the counts
- mean and max lose them

</div>
</div>

---

<div class="box" data-tab="GIN layer">

$$h_i' = \mathrm{MLP}\Big((1 + \epsilon)\, h_i + \sum_{j \in N(i)} h_j\Big)$$

</div>

- sum + MLP: reaches the WL limit

<p class="cite">Xu et al. 2019</p>

---

<!-- _class: divider -->

## The spectral view of GCN

---

<div class="cols fig600">
<div>

![](figures/e01_khop.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Polynomial filter">

$$y = \sum_{k=0}^{K} \theta_k\, \hat A^{k} x$$

</div>

$K$ hops in one layer

</div>
</div>

---

<div class="c">

![](figures/f01_gcn_fourier.svg)

</div>

---

<div class="c">

$$J(x) = \sum_{i,j} A_{ij}\, (x_i - x_j)^2$$

![](figures/f02_smoothness.svg)

</div>

---

<div class="cols fig640">
<div>

![](figures/e02_laplacian_diff.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Laplacian">

$$(Lx)_i = \sum_{j} (x_i - x_j)$$

</div>

$j$: the neighbors of $i$

</div>
</div>

---

<div class="box" data-tab="Laplacian">

$$x^\top L x = \sum_{(i,j) \in E} (x_i - x_j)^2$$

</div>

- $J = 2\, x^\top L x$
- small: $x$ is smooth, low frequency

---

<div class="cols fig660">
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

<div class="cols fig640">
<div>

![](figures/e04_spectral_conv_flow.svg)

</div>
<div>

<div class="box eq-sm" data-tab="Spectral conv">

$$\hat x = U^\top x$$

$$y = U\, g(\Lambda)\, \hat x$$

</div>

- $L = U \Lambda U^\top$
- $g$: a filter

</div>
</div>

---

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

<p class="cite">Defferrard et al. 2016</p>

</div>
</div>

---

<div class="c">

![](figures/e06_masks_karate.svg)

</div>

<div class="box eq-sm" data-tab="Frequency mask">

$$x_{\text{low}} = U\, \mathrm{diag}(m)\, U^\top x, \qquad m_k = 1 \text{ for } \lambda_k \le c$$

</div>

---

<div class="cols fig700">
<div>

![](figures/e07_highfreq_boundary.svg)

</div>
<div>

- largest: nodes 34, 1, 33 and 3
- node 3: 4 of 11 cross-club edges

</div>
</div>

---

<div class="cols" style="grid-template-columns: minmax(0, 1fr) 440px; align-items: center;">
<div>

- convolution: a sum over neighbors
- GCN, GraphSAGE, GAT: message passing
- GNN $\le$ WL test; GIN reaches it
- GCN: a low-pass filter

</div>
<div>

![](figures/e08_summary_visuals.svg)

</div>
</div>

---
marp: true
theme: math
paginate: true
footer: "Sadamori Kojaku, 2026"
---

<style>
/* MOCK: figure and animation placeholders. A dashed grey box with a tag and a Japanese description of the planned figure. */
section .ph { border: 2px dashed #9a9a9a; background: #f1f1f1; padding: 14px 22px; margin: 0 0 12px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; flex: 1 1 auto; min-height: 240px; position: relative; }
section .ph::before { content: attr(data-tag); background: #111; color: #fff; font-size: 14px; font-weight: 700; padding: 3px 10px; margin-bottom: 10px; }
section .ph p { margin: 0 0 6px; font-size: 17px; line-height: 1.4; color: #444; }
section .ph.live::before { background: #d0006f; }
section .ph .txt { font-size: 14px; font-style: italic; color: #777; border-top: 1px solid #bbb; padding-top: 6px; margin-top: 8px; }
section .ph.tall { min-height: 330px; }
section .ph.wide { min-height: 190px; }
</style>

<!-- MOCK v1 (2026-11-08). Skeleton + text + exact formulas; every figure is a placeholder (dashed box) with a description.
     Plan: plan.md. Two lectures: Lecture 1 = parts 1-4 (to the end of GCN), Lecture 2 = parts 5-9.
     Build: ~/.agents/skills/slide-math/tools/render.sh m08-gnn.md all -->

<!-- _class: title -->
<!-- _paginate: false -->
<!-- _footer: "" -->

# GNN

## from <span class="hot">convolution</span> to graphs

Convolution, Fourier transform, message passing and the Weisfeiler–Lehman limit

<p class="by">Sadamori Kojaku</p>

---

<!-- _class: agenda -->

## Outline

1. Convolution, the Fourier transform and graphs
2. Graph convolutional network (GCN)
3. GraphSAGE, GAT and message passing
4. The Weisfeiler–Lehman test
5. Subgraph GNN
6. The spectral view of GCN

---

<!-- _class: divider -->

<p class="crumb">Lecture 1</p>

## Convolution and the Fourier transform on images

---

## Images as arrays of pixels

A grayscale image is a matrix $X \in \mathbb{R}^{H \times W}$; a color image has three such matrices, one each for red, green and blue.

<div class="cols c32">
<div class="ph" data-tag="FIG 1 · Pixel zoom">

写真(顔や建物)の一部を拡大し、画素の格子と各画素の値(0〜255)を表示。右に R・G・B の3枚の行列を重ねて並べる。

<p class="txt">text in figure: pixel, R, G, B, H rows, W columns</p>

</div>
<div class="box" data-tab="Color image">

$$X \in \mathbb{R}^{H \times W \times 3}$$

$$X_{ij} = (R_{ij},\, G_{ij},\, B_{ij})$$

<div class="note">

$X_{ij}$ is the pixel in row $i$, column $j$.

</div>
</div>
</div>

---

## Convolution with a kernel

A $3 \times 3$ window slides over the image; each output pixel is the weighted sum of the nine pixels under the window.

<div class="cols c32">
<div class="ph live" data-tag="ANIM 1 · Sliding window">

左: 入力画像(8×8 程度の画素格子)。3×3 の窓が1画素ずつ走査し、窓の下の9画素とカーネルの9個の重みを掛けて足す様子を表示。右: 出力画像に値が1つずつ埋まる。

<p class="txt">text in figure: input X, kernel K, output Y, window</p>

</div>
<div class="box" data-tab="Convolution">

$$Y_{ij} = \sum_{a=-1}^{1} \sum_{b=-1}^{1} K_{ab}\, X_{i+a,\, j+b}$$

<div class="note">

CNNs compute this correlation and call it convolution. Flipping $K$ gives the textbook definition.

</div>
</div>
</div>

---

## The kernel sets the pattern

A vertical-edge kernel responds to vertical lines, a horizontal-edge kernel to horizontal lines, and a uniform kernel blurs.

<div class="cols c111">
<div class="box" data-tab="Vertical edge">

$$K = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}$$

</div>
<div class="box" data-tab="Horizontal edge">

$$K = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$$

</div>
<div class="box" data-tab="Blur">

$$K = \tfrac{1}{9}\begin{bmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end{bmatrix}$$

</div>
</div>

<div class="ph wide" data-tag="FIG 2 · One image, three outputs">

同じ写真(建物など縦横の線が多いもの)に3つのカーネルを適用し、出力画像を上の各カーネルの真下に並べる。入力画像は左端に小さく置く。

<p class="txt">text in figure: input, output Y</p>

</div>

---

## Try your own kernel

The nine weights decide what the output shows; change them and watch the output.

<div class="ph live tall" data-tag="INTERACTIVE 1 · Kernel playground">

左: 入力画像(選択式: 建物、顔、文字)。中: 3×3 のカーネルの9個の数値入力欄(プリセット: 縦線、横線、ぼかし、輪郭、鮮鋭化)。右: 出力画像がリアルタイムに更新される。授業では学生が数値を変えて何が見えるかを予想する。

<p class="txt">text in figure: input, kernel K (editable), output Y, presets</p>

</div>

---

## The kernel is local and shared

The same nine weights are used at every position, and each output pixel depends only on nearby pixels.

<div class="cols c32">
<div class="ph" data-tag="FIG 3 · Receptive field">

1層目: 出力1画素が入力の 3×3 を見る。2層目: 出力1画素が入力の 5×5 を見る。同じ画素を中心に、色の濃さで範囲の広がりを示す。

<p class="txt">text in figure: 1 layer: 3×3, 2 layers: 5×5</p>

</div>
<div>

- <mark>local</mark>: only neighbors enter the sum
- <mark>shared</mark>: one kernel for all positions
- stacking $L$ layers widens the window to $(2L+1) \times (2L+1)$

</div>
</div>

---

## A signal is a sum of waves

Any periodic signal $f(t)$ with period $T$ is a weighted sum of sines and cosines whose frequencies are multiples of $1/T$.

<div class="cols c32">
<div class="ph live" data-tag="ANIM 2 · 1D Fourier decomposition">

手前: 時間軸上の1本の波(複数の正弦波の和)。視点を回転させ、奥行き方向に周波数軸を出す。各周波数 k に対応する1本の正弦波と、その重み(高さ)が奥に並ぶ。

<p class="txt">text in figure: time t, frequency k, f(t), weight c_k</p>

</div>
<div class="box" data-tab="Fourier series">

$$f(t) = \sum_{k} c_k\, e^{2\pi i k t / T}$$

$$c_k = \frac{1}{T} \int_0^T f(t)\, e^{-2\pi i k t / T}\, dt$$

<div class="note">

$e^{i\theta} = \cos\theta + i \sin\theta$. $c_k$ is the weight of the wave with frequency $k/T$.

</div>
</div>
</div>

---

## The weights are the signal in the frequency domain

Low $k$ is a slow wave and high $k$ is a fast wave; the list $(c_k)$ describes $f$ as completely as the list of values $f(t)$.

<div class="ph tall" data-tag="FIG 4 · Time domain and frequency domain">

上: 時間領域の波 f(t)。下: 周波数領域の |c_k|(棒ではなく点で表示)。低周波の成分を薄紫で強調し、対応する正弦波を上の図に重ねる。

<p class="txt">text in figure: f(t), |c_k|, slow, fast, k = 1, 3, 7</p>

</div>

---

## Convolution becomes multiplication

Convolving two signals multiplies their Fourier coefficients one frequency at a time.

<div class="cols c32">
<div class="ph" data-tag="FIG 5 · Convolution theorem">

上段: 時間領域で f、g、f*g の3つの波(f*g は f をなめらかにしたもの)。下段: それぞれのスペクトル。g のスペクトルは低周波だけが大きく、f のスペクトルに掛けると高周波が消える。

<p class="txt">text in figure: f, g (kernel), f * g, ×, low-pass</p>

</div>
<div class="box" data-tab="Convolution theorem">

$$\widehat{(f * g)}_k = \hat f_k \cdot \hat g_k$$

<div class="note">

A kernel $g$ is a filter: it scales each frequency $k$ by $\hat g_k$.

</div>
</div>
</div>

---

## Waves in two dimensions

A 2D wave has a direction and a frequency, both given by the pair $(u, v)$.

<div class="cols c32">
<div class="ph live" data-tag="ANIM 3a · 2D wave">

左: 縞模様(2次元の波)。右: 周波数平面(横 u、縦 v)に点が1つ。点を動かすと、縞の向きが点の方向に、縞の細かさが原点からの距離に対応して変わる。実部と虚部を2つの縞で示す。

<p class="txt">text in figure: u, v, direction, frequency, real part, imaginary part</p>

</div>
<div class="box" data-tab="2D wave">

$$e^{2\pi i (ux + vy)}$$

- direction: the angle of $(u, v)$
- frequency: $\sqrt{u^2 + v^2}$

</div>
</div>

---

## The 2D Fourier transform of an image

The transform writes an image as a weighted sum of 2D waves; the weights fill a frequency plane.

<div class="cols c23">
<div class="ph" data-tag="FIG 6 · Image and spectrum">

左: 写真。右: その 2D スペクトル(強度の対数)。中心が低周波、端が高周波。縦線の多い画像だと横方向に伸びるスペクトルになる例も並べる。

<p class="txt">text in figure: image, spectrum, low frequency, high frequency, u, v</p>

</div>
<div class="box eq-sm" data-tab="2D Fourier transform">

$$\hat X_{uv} = \sum_{x=0}^{H-1} \sum_{y=0}^{W-1} X_{xy}\, e^{-2\pi i (ux/H + vy/W)}$$

</div>
</div>

---

## Masking frequencies changes the image

Removing high frequencies blurs the image; removing low frequencies leaves only the edges.

<div class="ph live tall" data-tag="ANIM 3b · Frequency masks">

3列。左: 元の画像とそのスペクトル。中: スペクトルの外側を黒く塗る(低周波だけ残す)と、ぼやけた画像。右: 中心を黒く塗る(高周波だけ残す)と、輪郭だけの画像。マスクの半径をスライダで動かす。

<p class="txt">text in figure: original, keep low frequencies, keep high frequencies, mask</p>

</div>

---

## Kernels are filters on frequencies

A blur kernel keeps low frequencies and an edge kernel keeps high frequencies.

<div class="ph tall" data-tag="FIG 7 · Kernel and its frequency response">

3列(ブラー、縦エッジ、横エッジ)。各列: カーネルの 3×3 行列 → その 2D 周波数応答(明るい所が通す周波数)。ブラーは中心だけ明るく、エッジは周辺が明るい。

<p class="txt">text in figure: blur: low-pass, vertical edge, horizontal edge</p>

</div>

---

<!-- _class: divider -->

<p class="crumb">Lecture 1</p>

## From image to graph

---

## An image is a graph

A pixel grid is a graph: pixels are nodes and neighboring pixels are joined by edges.

<div class="cols c32">
<div class="ph live" data-tag="ANIM 4 · Grid to graph">

画素の格子(各画素に色)から始め、隣り合う画素を辺で結ぶ。次に格子の位置を崩し、ノードを自由な位置へ動かして一般のグラフにする。辺が保たれていれば、同じ「隣の値を足す」操作が定義できることを示す。

<p class="txt">text in figure: pixels, edges between neighbors, any graph</p>

</div>
<div class="box" data-tab="Adjacency">

$$A_{pq} = \begin{cases} 1 & p, q \text{ neighbors} \\ 0 & \text{otherwise} \end{cases}$$

<div class="note">

For a general graph, $A$ is its adjacency matrix.

</div>
</div>
</div>

---

## Convolution is a sum over neighbors

A $3 \times 3$ kernel sums a pixel and its neighbors with one weight per direction; on a graph the neighbors are $N(i)$ and there is no direction.

<div class="cols c11 stretch">
<div class="box" data-tab="Image">

$$Y_p = \sum_{q \in N(p) \cup \{p\}} K_{q-p}\, X_q$$

<div class="note">

$K_{q-p}$: a weight for each relative position.

</div>
</div>
<div class="box" data-tab="Graph">

$$h_i' = \sum_{j \in N(i) \cup \{i\}} w_{ij}\, h_j$$

<div class="note">

$w_{ij}$: a weight for each edge.

</div>
</div>
</div>

<div class="ph wide" data-tag="FIG 8 · Same neighborhood, two views">

画素と周囲8画素(位置ごとに別の重み K_ab)と、ノードと隣接ノード(辺ごとに w_ij)を左右に並べる。グラフ側には位置の区別がないことを、重みの色が全て同じであることで示す。

<p class="txt">text in figure: weight per position, weight per edge</p>

</div>

---

<!-- _class: divider -->

<p class="crumb">Lecture 1</p>

## Graph convolutional network (GCN)

---

## An untrained GCN already groups the nodes

Karate club network: with random weights and no training, the 2D features of a 3-layer GCN put members of the same club close together.

<div class="cols c32">
<div class="ph live tall" data-tag="FIG 9 · Untrained GCN on the karate club">

左: 空手クラブネットワーク(2つのクラブを色分け)。右: 未学習の3層GCNが出力した各頂点の2次元特徴の散布図。同じクラブの点が近く、異なるクラブの点が離れて分かれる。入力特徴は単位行列(全頂点が別々のone-hot)。ランダム重みを引き直すボタンで何度でも同様になることを見せる。

<p class="txt">text in figure: club 1, club 2, layer 0 (input), layer 3 (output)</p>

</div>
<div>

- no training, no labels
- random weights $W^{(l)}$
- the graph structure alone separates the clubs

<span class="callout">Why? The next slides show what a layer computes.</span>

</div>
</div>

---

## Convolution on a graph: the GCN layer

A GCN layer replaces each node's feature with a weighted sum over itself and its neighbors, then applies a linear map and a nonlinearity.

<div class="ph wide" data-tag="FIG 10 · One node in one layer">

中心ノードとその隣接ノード3つ。各ノードに特徴ベクトル(短い色付き棒)。隣の特徴が矢印で中心に集まり、足し合わされ、W を通って新しい特徴になる。

<p class="txt">text in figure: h_j, sum, W, σ, h_i'</p>

</div>

<div class="box" data-tab="GCN layer (node form)">

$$h_i^{(l+1)} = \sigma\Big(\sum_{j \in N(i) \cup \{i\}} \hat A_{ij}\, h_j^{(l)} W^{(l)}\Big)$$

<div class="note">

$h_i^{(l)} \in \mathbb{R}^{1 \times d_l}$ is a row vector; $W^{(l)} \in \mathbb{R}^{d_l \times d_{l+1}}$ is learned; $\sigma$ is a nonlinearity such as ReLU.

</div>
</div>

---

## GCN weights neighbors by degree

Each neighbor $j$ of node $i$ is weighted by $1/\sqrt{\tilde d_i \tilde d_j}$, so that a node with many neighbors does not dominate the sum.

<div class="cols c32">
<div class="ph" data-tag="FIG 11 · Normalized weights">

5ノードの小さなグラフ(ハブが1つ)。各辺の隣に重み 1/√(d̃_i d̃_j) の値を実計算で表示。自己ループも描く。ハブにつながる辺の重みが小さいことが分かる配置にする。

<p class="txt">text in figure: self-loops, weights on edges, "degree + 1" at nodes</p>

</div>
<div class="box" data-tab="Normalized adjacency">

$$\tilde A = A + I, \qquad \tilde d_i = \sum_j \tilde A_{ij}$$

$$\hat A = \tilde D^{-1/2}\, \tilde A\, \tilde D^{-1/2}$$

<div class="note">

$\hat A_{ij} = 1/\sqrt{\tilde d_i \tilde d_j}$ for $j \in N(i) \cup \{i\}$, else $0$.

</div>
</div>
</div>

---

## The GCN layer in matrix form

With one row per node, the whole layer is $\hat A H W$ followed by $\sigma$.

<div class="cols c32">
<div class="ph" data-tag="FIG 12 · Matrix picture">

行列の積を図にする: Â (n×n、疎)× H (n×d_l) × W (d_l×d_{l+1}) → H' (n×d_{l+1})。Â の1行が H の隣接ノードの行を選んで足す様子を、1行ぶん薄紫で示す。

<p class="txt">text in figure: Â, H, W, H', n nodes, one row per node</p>

</div>
<div class="box" data-tab="GCN layer (matrix form)">

$$H^{(l+1)} = \sigma\big(\hat A\, H^{(l)} W^{(l)}\big)$$

<div class="note">

Kipf & Welling (2017). $H^{(0)} = X$, the input node features.

</div>
</div>
</div>

---

## Example: one layer on a small graph

Numbers for the 4-node path $1 - 2 - 3 - 4$ with 2-dimensional features, computed by the layer above.

<div class="cols c12">
<div class="ph" data-tag="FIG 13 · Worked example">

4ノードの経路グラフ。各ノードの入力特徴(2次元)と、Â H W の計算結果(ReLU の前後)を数値つきで表示。1ノードについて、足し算の中身を分解して見せる。数値は実計算。

<p class="txt">text in figure: h_1 ... h_4, Â, W, output</p>

</div>
<div>

```python
A_hat = D_inv_sqrt @ (A + np.eye(4)) @ D_inv_sqrt
H0 = np.array([[1, 0], [0, 1], [1, 1], [0, 0]])
W0 = np.array([[1, -1], [0.5, 1]])
H1 = np.maximum(A_hat @ H0 @ W0, 0)
print(np.round(H1, 2))
```

<div class="out" id="out">

```output
[[0.7  0.  ]
 [1.07 0.  ]
 [0.67 0.33]
 [0.61 0.  ]]
```

</div>
</div>
</div>

---

## Stacking layers widens the view

After $L$ layers, the feature of node $i$ depends on the nodes within $L$ hops of $i$.

<div class="ph tall" data-tag="FIG 14 · Receptive field on a graph">

中心ノードを決め、1層目は1ホップ以内、2層目は2ホップ以内、3層目は3ホップ以内を色の濃さで示す3枚。画像の 3×3 → 5×5 → 7×7 と並べて対応を見せる。

<p class="txt">text in figure: 1 layer, 2 layers, 3 layers, image: 3×3, 5×5, 7×7</p>

</div>

---

## Neighbor averaging smooths the signal

Averaging over neighbors makes connected nodes similar and removes features that change quickly along edges; this is the graph version of a blur kernel.

<div class="cols c32">
<div class="ph" data-tag="FIG 15 · Smoothing on the karate club">

空手クラブネットワーク上で、ノードごとのランダムな値(色)。Â を1回、2回、5回かけると色がなめらかになり、同じクラブの色がそろっていく。

<p class="txt">text in figure: layer 0, 1, 2, 5</p>

</div>
<div>

- $\hat A$ acts like the blur kernel
- many layers: all features become alike (over-smoothing)
- the spectral view (Part 6) makes this exact

</div>
</div>

---

## Exercise: one layer by hand

On paper: compute $\hat A$ and $H^{(1)}$ for the 3-node path $1 - 2 - 3$ with $H^{(0)} = [1, 0, 0]^\top$, $W = 1$, no $\sigma$.

<div class="ph wide" data-tag="EXERCISE 1 · Paper (2 min)">

3ノードの経路グラフ 1-2-3 を大きく描く。ノード1だけ値が 1、他は 0。次の順に紙で計算: Ã、d̃、Â、Â H。2回かけた Â² H も求め、値がどこに広がるかを見る。

</div>

---

<!-- _class: divider -->

<p class="crumb">Lecture 2</p>

## GraphSAGE and GAT

---

## A full neighborhood grows too fast

An $L$-layer GCN needs the $L$-hop neighborhood of every node it updates, and a hub pulls in a large part of the graph.

<div class="cols c32">
<div class="ph" data-tag="FIG 16 · Neighborhood explosion">

1ノードの計算木。1ホップ目で5本、2ホップ目で各5本(25)、3ホップ目で125...と増える。ハブをたどると木が急に広がる様子を、小さなグラフと並べて示す。

<p class="txt">text in figure: hop 1, hop 2, hop 3, hub</p>

</div>
<div class="box" data-tab="Cost">

$$\text{nodes touched} \approx d^{L}$$

<div class="note">

$d$: average degree. The count is an upper bound, and it reaches the whole graph for a large $L$.

</div>
</div>
</div>

---

## GraphSAGE samples a neighborhood

For each target node, GraphSAGE builds a computation tree from a fixed number of sampled neighbors per level.

<div class="ph tall" data-tag="FIG 17 · Sampled computation tree">

左: グラフ全体(対象ノードを強調)。右: 対象ノードを根とする計算木。各レベルで s=3 本だけ隣接ノードを選ぶ(選ばれた辺は太く、選ばれない辺は薄く)。ランダムウォークで選ぶ場合も同じ図で示す。

<p class="txt">text in figure: target node, sampled neighbors, s = 3 per level</p>

</div>

---

## Messages move from the leaves to the root

Features of the leaves are aggregated into their parents, then into the root, one level per layer.

<div class="ph tall" data-tag="ANIM 5 · Aggregation up the tree">

計算木のアニメーション。葉の特徴が親に集約され、次に根に集約される。1段ごとに色が混ざる。ミニバッチ内の他の対象ノードの木も薄く並べ、大きなグラフでもメモリが一定であることを示す。

<p class="txt">text in figure: layer 2, layer 1, root</p>

</div>

---

## The GraphSAGE layer

The feature of the node itself is concatenated with the aggregated neighbor feature before the linear map.

<div class="box" data-tab="GraphSAGE layer">

$$h_i^{(l+1)} = \sigma\Big( \big[\, h_i^{(l)} \,\|\, \mathrm{AGG}\big(\{ h_j^{(l)} : j \in S(i) \}\big) \,\big]\, W^{(l)} \Big)$$

<div class="note">

$S(i) \subseteq N(i)$ is a sample of $s$ neighbors; $\|$ is concatenation; AGG is the mean, an LSTM or a max pool (Hamilton et al. 2017).

</div>
</div>

<div class="ph wide" data-tag="FIG 18 · Concatenate, then transform">

自分の特徴ベクトル(青)と集約した隣接の特徴ベクトル(橙)を横に並べて1本につなぎ、W を通して新しい特徴になる。足し算(GCN)とのちがいを横に小さく併記。

<p class="txt">text in figure: self, neighbors, ‖, W, new feature</p>

</div>

---

## Concatenation keeps the node's own feature

GCN mixes the node with its neighbors in one sum; GraphSAGE gives the node and its neighbors separate weights.

<div class="cols c11 stretch">
<div class="box" data-tab="GCN">

$$h_i W \cdot \hat A_{ii} + \sum_{j \in N(i)} \hat A_{ij}\, h_j W$$

<div class="note">

the node and its neighbors share $W$

</div>
</div>
<div class="box" data-tab="GraphSAGE">

$$h_i W_1 + \mathrm{AGG}_{j \in S(i)}(h_j)\, W_2$$

<div class="note">

$W = [W_1; W_2]$: separate weights, so the node can be told apart from its neighbors

</div>
</div>
</div>

<div class="ph wide" data-tag="FIG 19 · A case where the sum fails">

小さな例: ノード u(特徴 a)の隣接が特徴 b の1ノードのときと、u 自身が特徴 b で隣接が a のときを並べる。GCN の足し算では同じ値になるが、連結では区別される。

</div>

---

## Neighbors differ in importance

GCN weights depend only on degrees; GAT learns a weight $\alpha_{ij}$ for each edge from the features of its two ends.

<div class="ph tall" data-tag="FIG 20 · Attention on a neighborhood">

中心ノードと隣接5ノード。辺の太さが α_ij を表す。GCN(次数だけで決まるのでほぼ均一)と GAT(特徴で決まるので不均一)を左右に並べる。

<p class="txt">text in figure: GCN: fixed by degree, GAT: learned from features</p>

</div>

---

## The attention coefficient

GAT scores each edge from the two transformed features, then normalizes the scores over the neighbors of $i$ with a softmax.

<div class="box" data-tab="GAT layer">

$$e_{ij} = \mathrm{LeakyReLU}\big(a^\top [\, h_i W \,\|\, h_j W \,]\big), \qquad \alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k \in N(i) \cup \{i\}} \exp(e_{ik})}$$

$$h_i' = \sigma\Big(\sum_{j \in N(i) \cup \{i\}} \alpha_{ij}\, h_j W\Big)$$

<div class="note">

Veličković et al. (2018). $a$ is a learned vector; $\alpha_{ij} \ge 0$ and $\sum_j \alpha_{ij} = 1$.

</div>
</div>

---

## GCN, GraphSAGE and GAT compared

The three layers differ in how the weight of each neighbor is chosen and in how the node's own feature enters.

<div>

| | neighbors used | weight of a neighbor | own feature |
|---|---|---|---|
| GCN | all | $1/\sqrt{\tilde d_i \tilde d_j}$, fixed | summed in |
| GraphSAGE | a sample of $s$ | set by AGG (mean) | concatenated |
| GAT | all | $\alpha_{ij}$, learned | summed in |

</div>

---

<!-- _class: divider -->

<p class="crumb">Lecture 2</p>

## Message passing

---

## The message passing framework

GCN, GraphSAGE and GAT compute a message on each edge, aggregate the messages at a node, and update the node.

<div class="ph wide" data-tag="FIG 21 · Three steps of message passing">

1ノードを中心に3段の流れ図。(1) 各辺でメッセージ φ を作る、(2) 隣接から届いたメッセージを集約 ⨁ する(順序に依らない)、(3) 自分の特徴と集約結果から ψ で新しい特徴を作る。

<p class="txt">text in figure: message φ, aggregate ⨁, update ψ</p>

</div>

<div class="box" data-tab="Message passing layer">

$$m_i = \bigoplus_{j \in N(i)} \varphi\big(h_i^{(l)}, h_j^{(l)}\big), \qquad h_i^{(l+1)} = \psi\big(h_i^{(l)}, m_i\big)$$

<div class="note">

$\bigoplus$ is a permutation-invariant function of a multiset: sum, mean or max. Gilmer et al. (2017).

</div>
</div>

---

## Each model is a choice of $\varphi$, $\bigoplus$ and $\psi$

The three layers fit the framework with different functions.

<div>

| | $\varphi(h_i, h_j)$ | $\bigoplus$ | $\psi(h_i, m_i)$ |
|---|---|---|---|
| GCN | $\hat A_{ij}\, h_j$ | sum | $\sigma(m_i W)$ |
| GraphSAGE | $h_j$ | mean over $S(i)$ | $\sigma([h_i \,\|\, m_i]\, W)$ |
| GAT | $\alpha_{ij}\, h_j W$ | sum | $\sigma(m_i)$ |

</div>

---

## Readout for a whole graph

A graph-level prediction pools the final node features into one vector.

<div class="cols c32">
<div class="ph" data-tag="FIG 22 · Readout">

グラフの全ノードの最終特徴(色付き棒)を、足し合わせて1本のベクトルにし、分類器に渡す。

<p class="txt">text in figure: node features, pool, graph vector</p>

</div>
<div class="box" data-tab="Readout">

$$h_G = \bigoplus_{i \in V} h_i^{(L)}$$

<div class="note">

Sum, mean or max over nodes; the result does not depend on the node order.

</div>
</div>
</div>

---

<!-- _class: divider -->

<p class="crumb">Lecture 2</p>

## The Weisfeiler–Lehman test and the limit of GNNs

---

## Can a GNN tell these two graphs apart?

Both graphs have 6 nodes, every node has degree 2, and all nodes carry the same feature.

<div class="ph tall" data-tag="FIG 23 · Two graphs">

左: 6頂点の閉路(6-cycle)。右: 2つの三角形。全ノードが同じ色。「GNN で見分けられるか?」とだけ書く(答えは載せない)。

<p class="txt">text in figure: 6-cycle, two triangles, same feature</p>

</div>

---

## The Weisfeiler–Lehman test

The WL test repeatedly relabels each node by its own label and the multiset of its neighbors' labels.

<div class="cols c32">
<div class="ph live" data-tag="ANIM 6 · One WL iteration">

小さなグラフ。各ノードに色(ラベル)。各ノードについて「自分の色 + 隣接の色の集合」を並べて表にし、同じ組に同じ新しい色を割り当て、全ノードを塗り替える。これを繰り返す。

<p class="txt">text in figure: old color, neighbor colors, new color</p>

</div>
<div class="box" data-tab="WL iteration">

$$c_i^{(t+1)} = \mathrm{HASH}\big(c_i^{(t)},\ \{\!\{ c_j^{(t)} : j \in N(i) \}\!\}\big)$$

<div class="note">

$\{\!\{\cdot\}\!\}$ is a multiset. Two graphs are reported as different when their color histograms differ.

</div>
</div>
</div>

---

## WL separates a path from a star

After one iteration the colors of the path and the star differ, so the test reports that the graphs are not isomorphic.

<div class="ph tall" data-tag="FIG 24 · WL on a path and a star">

4ノードの経路と4ノードのスター。初期色は全て同じ。1回の反復後、経路は端と中の2種類(2+2)、スターは中心と葉の2種類(1+3)で、色のヒストグラムが異なる。

<p class="txt">text in figure: iteration 0, iteration 1, histogram</p>

</div>

---

## Exercise: run the WL test by hand

On paper: run the WL test on the path $G_1$ and the T-shaped tree $G_2$ and find the first iteration at which the color histograms differ.

<div class="ph tall" data-tag="EXERCISE 2 · Paper (5 min)">

2つのグラフを大きく描く。G1: 5頂点の経路 1-2-3-4-5。G2: 5頂点で、1頂点に3本の枝がつき、うち1本が2頂点の長さ(T字形)。全ノードの初期色は同じ。紙に「自分の色 + 隣接の色の集合」の表を書き、反復1回後と2回後の色のヒストグラムを比べて、区別できるか、何回目で区別できるかを答える。

</div>

---

## WL cannot separate a 6-cycle from two triangles

Every node has the same label and the same neighbor multiset at every iteration, so the color histograms of the two graphs stay equal.

<div class="ph tall" data-tag="FIG 25 · WL fails">

6頂点の閉路と2つの三角形。反復0、1、2で全ノードが同じ色のまま。ヒストグラムは「全部同じ色 6個」で変わらない。それでも2つのグラフは同型ではない(連結成分の数が違う)。

<p class="txt">text in figure: iteration 0, 1, 2, same histogram, not isomorphic</p>

</div>

---

## WL steps correspond to GNN modules

Each part of a WL iteration has a counterpart in a message passing layer.

<div class="ph tall" data-tag="FIG 26 · WL and GNN side by side">

左右2列の対応図。左: WL の1反復(ラベル c_i → 隣接ラベルの多重集合 → HASH → 新ラベル)。右: GNN の1層(特徴 h_i → 隣接特徴の集約 ⨁ → 更新 ψ → 新特徴)。同じ段を線で結ぶ。

<p class="txt">text in figure: label ↔ feature, multiset ↔ aggregation ⨁, HASH ↔ update ψ</p>

</div>

---

## Correspondence in formulas

The WL update and the message passing update have the same shape.

<div class="cols c11 stretch">
<div class="box" data-tab="WL">

$$c_i^{(t+1)} = \mathrm{HASH}\big(c_i^{(t)},\ \{\!\{ c_j^{(t)} \}\!\}_{j \in N(i)}\big)$$

</div>
<div class="box" data-tab="Message passing">

$$h_i^{(l+1)} = \psi\big(h_i^{(l)},\ \bigoplus_{j \in N(i)} \varphi(h_i^{(l)}, h_j^{(l)})\big)$$

</div>
</div>

<div class="kv">

| WL | GNN |
|---|---|
| node label $c_i$ | node feature $h_i$ |
| multiset of neighbor labels | aggregated message $m_i$ |
| HASH (injective) | update $\psi$ (a neural network) |

</div>

---

## A GNN is at most as strong as the WL test

If WL gives two nodes the same label after $t$ iterations, a $t$-layer message passing GNN gives them the same feature.

<div class="box" data-tab="Theorem (Xu et al. 2019, Morris et al. 2019)">

$$c_u^{(t)} = c_v^{(t)} \;\Longrightarrow\; h_u^{(t)} = h_v^{(t)}$$

<div class="note">

So if the WL test cannot separate two non-isomorphic graphs, no message passing GNN can: their readouts are equal.

</div>
</div>

<div class="ph wide" data-tag="FIG 27 · Limit of GNNs">

6頂点の閉路と2つの三角形を再掲。「WL が区別できない ⇒ どんな重みでも GNN の出力は同じ」と矢印で示す。

</div>

---

## Mean and max lose information that sum keeps

For one-hot node labels, mean and max give the same output for different multisets of neighbors; sum does not.

<div class="ph wide" data-tag="FIG 28 · Aggregators compared">

隣接の多重集合を2つ並べる: {赤, 赤, 青, 青} と {赤, 青}。sum は (2,2) と (1,1) で異なる。mean は (0.5, 0.5) で同じ。max は (1, 1) で同じ。

<p class="txt">text in figure: sum, mean, max, same / different</p>

</div>

---

## GIN reaches the WL limit

With sum aggregation and an injective update, a GNN separates exactly the graphs that the WL test separates.

<div class="box" data-tab="GIN layer (Xu et al. 2019)">

$$h_i^{(l+1)} = \mathrm{MLP}^{(l)}\Big( (1 + \epsilon)\, h_i^{(l)} + \sum_{j \in N(i)} h_j^{(l)} \Big)$$

<div class="note">

An MLP can approximate an injective function on a finite set of inputs, so the update does not lose information that the sum keeps.

</div>
</div>

---

<!-- _class: divider -->

<p class="crumb">Lecture 2</p>

## Subgraph GNN

---

## Mark one node, run the GNN, repeat for every node

A subgraph GNN gives one node an identifying feature, runs a GNN on that marked graph, and repeats this for every node.

<div class="ph tall" data-tag="FIG 29 · Marked copies of a graph">

6頂点の閉路から n=6 個のコピーを作る。コピー v では頂点 v だけに印(色を変える)をつけ、各コピーで GNN を走らせて各頂点の特徴を得る。得られた特徴を、頂点ごとにコピー全体で集約して最終特徴にする。

<p class="txt">text in figure: copy 1 ... copy n, marked node, GNN, aggregate over copies</p>

</div>

---

## The subgraph GNN in formulas

Node features are computed per marked copy and then aggregated over the marks; edge and graph features follow from node features.

<div class="box" data-tab="Subgraph GNN (node marking)">

$$h_i^{(v)} = \mathrm{GNN}\big(G,\ X + \mathbb{1}_v\big)_i, \qquad h_i = \rho\big(\{\!\{ h_i^{(v)} : v \in V \}\!\}\big)$$

<div class="note">

$\mathbb{1}_v$ adds a distinct feature to node $v$ only. $\rho$ aggregates over the $n$ copies (sum or mean). Examples: ID-GNN (You et al. 2021), ESAN (Bevilacqua et al. 2022).

</div>
</div>

---

## Marking separates the 6-cycle from two triangles

With node $s$ marked, the nodes of the 6-cycle receive three different distances from $s$; in the two triangles, one triangle is never reached from $s$.

<div class="ph tall" data-tag="FIG 30 · Marking breaks the symmetry">

6頂点の閉路と2つの三角形のそれぞれで、1頂点 s に印をつけ、メッセージが伝わる様子(s からの距離で色分け)。閉路は距離 0,1,1,2,2,3 の分布、三角形は距離 0,1,1 と「届かない」3頂点となり、ヒストグラムが異なる。

<p class="txt">text in figure: marked s, distance 0, 1, 2, 3, not reached</p>

</div>

---

## Cost and choice of subgraphs

Using all $n$ marked copies multiplies the cost of one GNN by $n$, so practical models use a sample of subgraphs.

<div>

| subgraph family | copies | cost |
|---|---|---|
| node marking, all nodes | $n$ | $n \times$ one GNN |
| node deletion | $n$ | $n \times$ one GNN |
| a random sample | $k \ll n$ | $k \times$ one GNN |

</div>

<div class="note">

More expressive than the WL test, and still not complete: some graph pairs stay equal.

</div>

---

<!-- _class: divider -->

<p class="crumb">Lecture 2</p>

## The spectral view of GCN

---

## One layer can look more than one hop

A layer can combine $\hat A^0 x, \hat A^1 x, \dots, \hat A^K x$ and so see nodes up to $K$ hops away.

<div class="cols c32">
<div class="ph" data-tag="FIG 31 · K-hop in one layer">

中心ノードから 0, 1, 2, 3 ホップのノードを色分け。1層で x, Âx, Â²x, Â³x を重み θ_0..θ_3 で足し合わせる。

<p class="txt">text in figure: θ_0, θ_1, θ_2, θ_3, K hops</p>

</div>
<div class="box" data-tab="Polynomial filter">

$$y = \sum_{k=0}^{K} \theta_k\, \hat A^{k} x$$

<div class="note">

$\theta_k$ are learned. $K = 1$ is a GCN layer.

</div>
</div>
</div>

---

## ChebNet: a polynomial in the Laplacian

ChebNet uses Chebyshev polynomials of the Laplacian, which are stable to compute and need only $K$ sparse matrix products.

<div class="box" data-tab="ChebNet (Defferrard et al. 2016)">

$$y = \sum_{k=0}^{K} \theta_k\, T_k(\tilde L)\, x, \qquad \tilde L = \frac{2L}{\lambda_{\max}} - I$$

<div class="note">

$L = D - A$ is the graph Laplacian. $T_0 = 1$, $T_1(x) = x$, $T_k(x) = 2x\,T_{k-1}(x) - T_{k-2}(x)$. The output at a node depends on nodes within $K$ hops.

</div>
</div>

---

## Eigenvectors of the Laplacian are waves on a graph

The eigenvectors of $L$ play the role of the sines and cosines; the eigenvalue is the frequency.

<div class="box" data-tab="Frequency of an eigenvector">

$$L u_k = \lambda_k u_k, \qquad u_k^\top L\, u_k = \sum_{(i,j) \in E} \big(u_{k,i} - u_{k,j}\big)^2 = \lambda_k$$

<div class="note">

Small $\lambda_k$: neighbors have similar values (low frequency). Large $\lambda_k$: neighbors differ (high frequency).

</div>
</div>

<div class="ph wide" data-tag="FIG 32 · Eigenvectors of the karate club">

空手クラブネットワーク上に、固有ベクトル(小さい固有値のものから順に4本)を色で表示。λ が小さいと辺の両端で値がほぼ等しい(ゆるやかな波)。大きいと辺の両端で符号が反転する(細かい波)。

<p class="txt">text in figure: λ_1 = 0, λ_2, λ_10, λ_34</p>

</div>

---

## The graph Fourier transform

Writing a signal in the eigenvector basis gives its weights on each frequency, as in the Fourier transform of Part 1.

<div class="cols c11 stretch">
<div class="box" data-tab="Graph Fourier transform">

$$\hat x = U^\top x, \qquad x = U \hat x$$

<div class="note">

$L = U \Lambda U^\top$, columns of $U$ are the eigenvectors $u_k$, $\Lambda = \mathrm{diag}(\lambda_1, \dots, \lambda_n)$.

</div>
</div>
<div class="box" data-tab="Image Fourier transform">

$$\hat f_k = \tfrac{1}{T}\textstyle\int f(t)\, e^{-2\pi i k t/T}\, dt$$

<div class="note">

the weight of the wave $k$: an inner product of $f$ with the wave

</div>
</div>
</div>

---

## Spectral convolution learns a function of the eigenvalues

The eigenvectors are fixed; the filter $g$ rescales the weight of each frequency, as a kernel does for an image.

<div class="box" data-tab="Spectral convolution">

$$y = U\, g(\Lambda)\, U^\top x, \qquad g(\Lambda) = \mathrm{diag}\big(g(\lambda_1), \dots, g(\lambda_n)\big)$$

<div class="note">

Bruna et al. (2014): learn $g(\lambda_1), \dots, g(\lambda_n)$ directly. Cost: an eigendecomposition of $L$.

</div>
</div>

<div class="ph wide" data-tag="FIG 33 · Spectral convolution">

3段の流れ図。x → (U^T) → 周波数ごとの重み x̂_k → (g(λ_k) を掛ける) → (U) → y。中段で g の形(低周波を通す曲線、高周波を通す曲線)を小さく示す。

<p class="txt">text in figure: x, U^T, g(λ), U, y, low-pass, high-pass</p>

</div>

---

## ChebNet and GCN are special cases

A polynomial $g(\lambda) = \sum_k \theta_k \lambda^k$ is spectral convolution restricted to $K$ hops; $K=1$ with tied weights is GCN.

<div class="ph wide" data-tag="FIG 34 · Family of models">

3段の入れ子図。外側: spectral convolution(g が任意、n 個の自由度)。中: ChebNet(g が K 次の多項式、K+1 個の自由度、K ホップ)。内側: GCN(K=1 で重みを共有)。各段の g の曲線を添える。

<p class="txt">text in figure: spectral conv, ChebNet, GCN, g(λ)</p>

</div>

<div class="box" data-tab="GCN as a low-pass filter">

$$\hat A = I - \tilde L_{\mathrm{sym}} \quad\Rightarrow\quad g(\lambda) = 1 - \tilde\lambda$$

<div class="note">

$\tilde\lambda$ is an eigenvalue of the normalized Laplacian of $\tilde A$; $g$ is largest for small $\tilde\lambda$, so a GCN layer keeps low frequencies and damps high ones.

</div>
</div>

---

## Masking frequencies on the karate club

Keep only the low-frequency or only the high-frequency components of the eigenvector centrality, as the mask on the image did.

<div class="cols c32">
<div class="ph live tall" data-tag="FIG 35 · Eigenvector centrality, low and high">

空手クラブネットワークの固有ベクトル中心性 x を3枚で表示: 元の x、低周波成分(U_low U_low^T x)、高周波成分(U_high U_high^T x)。スライダでカットオフを動かす。

<p class="txt">text in figure: x, low-frequency part, high-frequency part, cutoff</p>

</div>
<div class="box" data-tab="Frequency mask">

$$x_{\mathrm{low}} = U\, \mathrm{diag}(m)\, U^\top x$$

<div class="note">

$m_k = 1$ for $\lambda_k \le c$, else $0$ (low-pass). Swap to keep $\lambda_k > c$ (high-pass).

</div>
</div>
</div>

---

## The high-frequency part marks the community boundary

The high-frequency part is large on nodes next to a node of a different value, which are the nodes at the boundary between the two clubs, and small on nodes surrounded by high-centrality nodes.

<div class="ph tall" data-tag="FIG 36 · High-frequency component">

空手クラブネットワーク上の高周波成分(色)。コミュニティの境界のノードで値が大きく、中心性の高いノードに囲まれたノード(ハブの近く)で値が小さい。境界の辺を太線で示す。

<p class="txt">text in figure: boundary nodes (large), surrounded nodes (small)</p>

</div>

---

## Summary

<div class="vcenter">

- convolution sums a pixel and its neighbors; a graph does the same with the neighbors $N(i)$
- GCN: degree-normalized sum; GraphSAGE: sample + concatenation; GAT: learned weights
- all of them are message passing: $\varphi$, $\bigoplus$, $\psi$
- message passing GNNs are at most as strong as the WL test; sum aggregation (GIN) reaches the limit
- subgraph GNNs mark nodes to go beyond it
- spectral view: a GCN layer is a filter on the eigenvalues of the Laplacian

</div>

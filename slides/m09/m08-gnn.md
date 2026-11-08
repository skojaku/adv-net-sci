---
marp: true
theme: math
paginate: true
footer: "Sadamori Kojaku, 2026"
---

<style>
/* Wireframe pieces. Dashed box = a figure not drawn yet. Remove when the real figures replace them. */
section .wf { border: 2.5px dashed #000; background: #F1F1F1; box-sizing: border-box; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 10px 22px; gap: 8px; }
section .wf p { margin: 0; }
section .wfk { background: #000; color: #fff; font-weight: 700; font-size: 16px; padding: 2px 12px; letter-spacing: 0; }
section .wfd { font-size: 17px; line-height: 1.4; color: #222; }
section .wft { font-size: 16px; line-height: 1.35; color: #000; font-style: italic; border-top: 1px solid #C9C9C9; padding-top: 6px; }
section { --fs: 21px; }
</style>

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

1. Convolution and the Fourier transform on images
2. Graph convolutional network (GCN)
3. GraphSAGE and GAT
4. Message passing and the Weisfeiler–Lehman test
5. Subgraph GNN
6. The spectral view of GCN

---

<!-- _class: divider -->

<p class="crumb">GNN: from convolution to graphs</p>

## Convolution and the Fourier transform on images

---

## Images as arrays of pixels

A grayscale image is a matrix $X \in \mathbb R^{H \times W}$; a color image has three such matrices, one each for red, green and blue.

<div class="cols c32 mid">
<div class="wf" style="height:460px">
<p class="wfk">FIG 1 · Pixel zoom</p>
<p class="wfd">写真(顔や建物)の一部を拡大し、画素の格子と各画素の値(0〜255)を表示。右に R・G・B の3枚の行列を重ねて並べる。</p>
<p class="wft">Text in figure: "pixel", "R", "G", "B", "H rows", "W columns", values 0–255</p>
</div>
<div>
<div class="box" data-tab="Color image">

$$X \in \mathbb R^{H \times W \times 3}$$

$$X_{ij} = (R_{ij},\, G_{ij},\, B_{ij})$$

<div class="note">

$X_{ij}$ is the pixel in row $i$, column $j$.

</div>
</div>
</div>
</div>

---

## Convolution with a kernel

A $3\times3$ window slides over the image, and each output pixel is a weighted sum of the pixels under the window.

<div class="cols c32 mid">
<div class="wf" style="height:470px">
<p class="wfk">ANIM 1 · Sliding window</p>
<p class="wfd">左:入力画像(8×8 程度の画素格子)。3×3 の窓が1画素ずつ走査する。窓の下の9画素と、カーネルの9個の重みを掛けて足す様子を表示。右:出力画像に値が1つずつ埋まる。</p>
<p class="wft">Text in figure: "input X", "kernel K", "output Y", "window"</p>
</div>
<div>
<div class="box" data-tab="Convolution">

$$Y_{ij} = \sum_{a=-1}^{1}\sum_{b=-1}^{1} K_{ab}\, X_{i+a,\,j+b}$$

<div class="note">

CNNs compute this correlation and call it convolution. Flipping $K$ gives the textbook definition.

</div>
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

$$K = \tfrac19 \begin{bmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end{bmatrix}$$

</div>
</div>

<div class="wf" style="height:250px">
<p class="wfk">FIG 2 · One image, three outputs</p>
<p class="wfd">同じ写真(建物など縦横の線が多いもの)を入力にして、3つのカーネルを適用した出力画像を上のカーネルの真下に並べる。入力画像は左端に小さく置く。</p>
<p class="wft">Text in figure: "input", "output Y"</p>
</div>

---

## The kernel is local and shared

The same nine weights are used at every position, and each output pixel depends only on nearby pixels.

<div class="cols c32 mid">
<div class="wf" style="height:450px">
<p class="wfk">FIG 3 · Receptive field</p>
<p class="wfd">1層目:出力1画素が入力の 3×3 を見る。2層目:出力1画素が入力の 5×5 を見る。同じ画素を中心に、色の濃さで範囲の広がりを示す。</p>
<p class="wft">Text in figure: "1 layer: 3×3", "2 layers: 5×5", "same kernel at every position"</p>
</div>
<div>

- <mark>local</mark>: only neighbors enter the sum
- <mark>shared</mark>: one kernel for all positions
- stacking $L$ layers widens the window to $(2L+1)\times(2L+1)$

</div>
</div>

---

## A signal is a sum of waves

Any periodic signal $f(t)$ with period $T$ is a weighted sum of sines and cosines whose frequencies are multiples of $1/T$.

<div class="cols c32 mid">
<div class="wf" style="height:470px">
<p class="wfk">ANIM 2 · 1D Fourier decomposition</p>
<p class="wfd">手前:時間軸上の1本の波(複数の正弦波の和)。視点を回転させ、奥行き方向に周波数軸を出す。各周波数 k に対応する1本の正弦波と、その重み(高さ)が奥に並ぶ。</p>
<p class="wft">Text in figure: "time t", "frequency k", "f(t)", "weight c_k"</p>
</div>
<div>
<div class="box eq-sm" data-tab="Fourier series">

$$f(t) = \sum_{k} c_k\, e^{2\pi i k t / T}$$

$$c_k = \frac1T \int_0^T f(t)\, e^{-2\pi i k t / T}\, dt$$

<div class="note">

$e^{i\theta} = \cos\theta + i\sin\theta$. $c_k$ is the weight of the wave with frequency $k/T$.

</div>
</div>
</div>
</div>

---

## The weights are the signal in the frequency domain

Low $k$ is a slow wave and high $k$ is a fast wave; the list $(c_k)$ describes $f$ as completely as the list of values $f(t)$.

<div class="wf" style="height:470px">
<p class="wfk">FIG 4 · Time domain and frequency domain</p>
<p class="wfd">上:時間領域の波 f(t)。下:周波数領域の |c_k|(棒ではなく点で表示)。低周波の成分を薄紫で強調し、対応する正弦波を上の図に重ねる。</p>
<p class="wft">Text in figure: "f(t)", "|c_k|", "slow", "fast", "k = 1, 3, 7 ..."</p>
</div>

---

## Convolution becomes multiplication

Convolving two signals multiplies their Fourier coefficients one frequency at a time.

<div class="cols c32 mid">
<div class="wf" style="height:450px">
<p class="wfk">FIG 5 · Convolution theorem</p>
<p class="wfd">上段:時間領域で f、g、f*g の3つの波(f*g は f をなめらかにしたもの)。下段:それぞれのスペクトル。g のスペクトルは低周波だけが大きく、f のスペクトルに掛けると高周波が消える。</p>
<p class="wft">Text in figure: "f", "g (kernel)", "f * g", "×", "low-pass"</p>
</div>
<div>
<div class="box" data-tab="Convolution theorem">

$$\widehat{(f * g)}_k = \hat f_k \cdot \hat g_k$$

<div class="note">

A kernel $g$ is a filter: it scales each frequency $k$ by $\hat g_k$.

</div>
</div>
</div>
</div>

---

## Waves in two dimensions

A 2D wave has a direction and a frequency, both given by the pair $(u, v)$.

<div class="cols c32 mid">
<div class="wf" style="height:460px">
<p class="wfk">ANIM 3a · 2D wave</p>
<p class="wfd">左:縞模様(2次元の波)。右:周波数平面(横 u、縦 v)に点が1つ。点を動かすと、縞の向きが点の方向に、縞の細かさが原点からの距離に対応して変わる。実部と虚部(複素数)を2つの縞で示す。</p>
<p class="wft">Text in figure: "u", "v", "direction", "frequency", "real part", "imaginary part"</p>
</div>
<div>
<div class="box" data-tab="2D wave">

$$e^{2\pi i (u x + v y)}$$

- direction: the angle of $(u, v)$
- frequency: $\sqrt{u^2 + v^2}$

</div>
</div>
</div>

---

## The 2D Fourier transform of an image

The transform writes an image as a weighted sum of 2D waves; the weights fill a frequency plane.

<div class="cols c32 mid">
<div class="wf" style="height:450px">
<p class="wfk">FIG 6 · Image and spectrum</p>
<p class="wfd">左:写真。右:その 2D スペクトル(強度の対数)。中心が低周波、端が高周波。縦線の多い画像なら横方向に伸びるスペクトルになる例を並べて示す。</p>
<p class="wft">Text in figure: "image", "spectrum", "low frequency", "high frequency", "u", "v"</p>
</div>
<div>
<div class="box eq-sm" data-tab="2D Fourier transform">

$$\hat X_{uv} = \sum_{x=0}^{H-1}\sum_{y=0}^{W-1} X_{xy}\, e^{-2\pi i (ux/H + vy/W)}$$

</div>
</div>
</div>

---

## Masking frequencies changes the image

Removing high frequencies blurs the image; removing low frequencies leaves only the edges.

<div class="wf" style="height:470px">
<p class="wfk">ANIM 3b · Frequency masks</p>
<p class="wfd">3列。左:元の画像とそのスペクトル。中:スペクトルの外側を黒く塗る(低周波だけ残す)と、ぼやけた画像。右:中心を黒く塗る(高周波だけ残す)と、輪郭だけの画像。マスクの半径をスライダで動かす。</p>
<p class="wft">Text in figure: "original", "keep low frequencies", "keep high frequencies", "mask"</p>
</div>

---

## JPEG discards high frequencies

JPEG splits an image into $8\times8$ blocks, applies a cosine transform to each block and rounds the high-frequency coefficients to 0.

<div class="cols c32 mid">
<div class="wf" style="height:450px">
<p class="wfk">FIG 7 · JPEG</p>
<p class="wfd">8×8 ブロックの切り出し → 64個の係数(左上が低周波)→ 右下を0にした係数表 → 復元ブロック。下に品質 90 / 30 / 10 の画像とファイルサイズを並べる。</p>
<p class="wft">Text in figure: "8×8 block", "DCT coefficients", "set to 0", "quality 90 / 30 / 10"</p>
</div>
<div>

- the cosine transform is the real-valued form of the Fourier transform
- the eye is less sensitive to fast changes
- the file stores only the nonzero coefficients

</div>
</div>

---

## Kernels are filters on frequencies

A blur kernel keeps low frequencies and an edge kernel keeps high frequencies.

<div class="wf" style="height:470px">
<p class="wfk">FIG 8 · Kernel and its frequency response</p>
<p class="wfd">3列(ブラー、縦エッジ、横エッジ)。各列:カーネルの 3×3 行列 → その 2D 周波数応答(明るい所が通す周波数)。ブラーは中心だけ明るく、エッジは周辺が明るい。</p>
<p class="wft">Text in figure: "blur: low-pass", "vertical edge: high-pass in u", "horizontal edge: high-pass in v"</p>
</div>

---

<!-- _class: divider -->

<p class="crumb">GNN: from convolution to graphs</p>

## Graph convolutional network (GCN)

---

## An image is a graph

A pixel grid is a graph: pixels are nodes and neighboring pixels are joined by edges.

<div class="cols c32 mid">
<div class="wf" style="height:460px">
<p class="wfk">ANIM 4 · Grid to graph</p>
<p class="wfd">画素の格子(各画素に色)から始め、隣り合う画素を辺で結ぶ。次に格子の位置を崩し、ノードを自由な位置へ動かして一般のグラフにする。辺が保たれていれば、同じ「隣の値を足す」操作が定義できることを示す。</p>
<p class="wft">Text in figure: "pixels", "edges between neighbors", "any graph"</p>
</div>
<div>
<div class="box" data-tab="Adjacency">

$$A_{pq} = \begin{cases} 1 & p, q \text{ neighbors} \\ 0 & \text{otherwise} \end{cases}$$

<div class="note">

For a general graph, $A$ is its adjacency matrix.

</div>
</div>
</div>
</div>

---

## Convolution is a sum over neighbors

A $3\times3$ kernel sums a pixel and its neighbors with one weight per direction; on a graph, the neighbors are $\mathcal N(i)$ and there is no direction.

<div class="cols flow c11 mid">
<div class="box" data-tab="Image">

$$Y_p = \sum_{q \in \mathcal N(p) \cup \{p\}} K_{q-p}\, X_q$$

<div class="note">

$K_{q-p}$: a weight for each relative position.

</div>
</div>

<span class="tri"></span>

<div class="box" data-tab="Graph">

$$\mathbf h_i' = \sum_{j \in \mathcal N(i) \cup \{i\}} w_{ij}\, \mathbf h_j$$

<div class="note">

$w_{ij}$: a weight for each edge.

</div>
</div>
</div>

<div class="wf" style="height:210px">
<p class="wfk">FIG 9 · Same neighborhood, two views</p>
<p class="wfd">画素と周囲8画素(位置ごとに別の重み K_ab)と、ノードと隣接ノード(辺ごとに w_ij)を左右に並べる。グラフ側には位置の区別がないことを、重みの色が全て同じであることで示す。</p>
<p class="wft">Text in figure: "weight per position", "weight per edge"</p>
</div>

---

## GCN weights neighbors by degree

Each neighbor $j$ of node $i$ is weighted by $1/\sqrt{\tilde d_i \tilde d_j}$, so that a node with many neighbors does not dominate the sum.

<div class="cols c32 mid">
<div class="wf" style="height:450px">
<p class="wfk">FIG 10 · Normalized weights</p>
<p class="wfd">5ノードの小さなグラフ(ハブが1つ)。各辺の隣に重み 1/√(d̃_i d̃_j) の値を表示(実計算)。自己ループも描く。ハブにつながる辺の重みが小さいことが分かる配置にする。</p>
<p class="wft">Text in figure: self-loops, weights on edges, "degree + 1" at nodes</p>
</div>
<div>
<div class="box eq-sm" data-tab="Normalized adjacency">

$$\tilde A = A + I, \qquad \tilde d_i = \sum_j \tilde A_{ij}$$

$$\hat A = \tilde D^{-1/2}\, \tilde A\, \tilde D^{-1/2}$$

<div class="note">

$\hat A_{ij} = 1 / \sqrt{\tilde d_i \tilde d_j}$ for $j \in \mathcal N(i) \cup \{i\}$.

</div>
</div>
</div>
</div>

---

## The GCN layer

A layer sums the neighbor features with weights $\hat A_{ij}$, applies a linear map $W$, then a nonlinearity $\sigma$.

<div class="def">

Features: $\mathbf h_i^{(l)} \in \mathbb R^{1 \times d_l}$ (row vector) <span class="gap"></span> Weights: $W^{(l)} \in \mathbb R^{d_l \times d_{l+1}}$

</div>

<div class="box eq-lg" data-tab="GCN layer">

$$\mathbf h_i^{(l+1)} = \sigma\Big(\sum_{j \in \mathcal N(i) \cup \{i\}} \hat A_{ij}\, \mathbf h_j^{(l)}\, W^{(l)}\Big)$$

<div class="note">

Matrix form with one row per node: $H^{(l+1)} = \sigma(\hat A\, H^{(l)} W^{(l)})$ (Kipf & Welling 2017).

</div>
</div>

<div class="wf" style="height:170px">
<p class="wfk">FIG 11 · Layer as a diagram</p>
<p class="wfd">横一列のフロー図:H(l) → Â を掛ける(集約)→ W を掛ける(線形変換)→ σ(非線形)→ H(l+1)。各箱の下に式の該当部分。</p>
<p class="wft">Text in figure: "aggregate", "linear map", "nonlinearity"</p>
</div>

---

## One layer in three steps

For node $i$: sum the weighted neighbor features, multiply by $W$, apply $\sigma$.

<div class="cols c32 mid">
<div class="wf" style="height:470px">
<p class="wfk">ANIM 6 · Aggregation, step by step</p>
<p class="wfd">着目ノード i と3つの隣接ノード。各ノードの特徴ベクトル(3次元の縦棒ではなく数値の並び)が i に集まり、重みを掛けて足されて1本のベクトル a_i になる(1)。W を掛けて次元が変わる(2)。σ(ReLU)で負の値が0になる(3)。新しい h_i が i に置かれる。3ステップは3枚のスライドに分ける。</p>
<p class="wft">Text in figure: "neighbors", "weighted sum", "× W", "ReLU", "new feature"</p>
</div>
<div>
<div class="box eq-sm" data-tab="Three steps">

$$\begin{aligned}
\mathbf a_i &= \sum_{j} \hat A_{ij}\, \mathbf h_j^{(l)} && \why{(aggregate)}\\
\mathbf z_i &= \mathbf a_i\, W^{(l)} && \why{(linear map)}\\
\mathbf h_i^{(l+1)} &= \sigma(\mathbf z_i) && \why{(nonlinearity)}
\end{aligned}$$

</div>
</div>
</div>

---

## Example: one layer on a small graph

Numbers for a 4-node graph with 2-dimensional features, computed by the layer above.

<div class="cols c11 mid">
<div class="wf" style="height:460px">
<p class="wfk">FIG 12 · Worked example</p>
<p class="wfd">4ノードのグラフ(パスに1辺足したもの)。各ノードに2次元の特徴ベクトルの数値。Â の値、集約後の a_i、W(2×2)、z_i、ReLU 後の h_i を、ノードの横に実計算で書く。1ノード(i=2)だけ計算過程を展開。</p>
<p class="wft">Text in figure: all numbers computed by the script</p>
</div>
<div class="wf" style="height:460px">
<p class="wfk">TABLE · Same example</p>
<p class="wfd">右に i=2 の計算式を縦に並べる:a_2 = Σ Â_2j h_j、z_2 = a_2 W、h_2' = ReLU(z_2)。数値を代入した形。</p>
<p class="wft">Text in figure: numbers, "ReLU"</p>
</div>
</div>

---

## Stacking layers widens the view

After $L$ layers, the feature of node $i$ depends on the nodes within $L$ hops of $i$.

<div class="cols c32 mid">
<div class="wf" style="height:460px">
<p class="wfk">FIG 13 · Hops</p>
<p class="wfd">空手クラブのネットワーク。着目ノード i を中心に、1ホップ以内、2ホップ以内、3ホップ以内を濃淡で塗る。画像の 3×3 → 5×5 の図(FIG 3)と同じ色使い。</p>
<p class="wft">Text in figure: "1 hop", "2 hops", "3 hops", node i</p>
</div>
<div>
<div class="box" data-tab="Receptive field">

$$\mathbf h_i^{(L)} = f\big(\{\mathbf x_j : d(i, j) \le L\}\big)$$

<div class="note">

$d(i,j)$ is the shortest-path distance.

</div>
</div>
</div>
</div>

---

## An untrained GCN groups similar nodes

With random weights and no training, a 3-layer GCN places members of the same karate club near each other.

<div class="cols c32 mid">
<div class="wf" style="height:470px">
<p class="wfk">ANIM 5 · Random GCN on the karate club</p>
<p class="wfd">左:空手クラブのネットワーク(2つのクラブを2色)。右:3層 GCN(入力は単位行列、重みは乱数、学習なし)の2次元出力の散布図、同じ色。重みの乱数シードを変えるたびに点の配置が変わるが、同じクラブの点が近くに集まる様子をアニメーションで示す。</p>
<p class="wft">Text in figure: "Mr. Hi's club", "Officer's club", "random weights", "no training"</p>
</div>
<div>

- input: one-hot node IDs
- weights: random, never trained
- output: 2D

</div>
</div>

---

## Neighbor averaging smooths the signal

Averaging over neighbors makes connected nodes similar and removes features that change quickly along edges.

<div class="cols c32 mid">
<div class="wf" style="height:460px">
<p class="wfk">FIG 14 · Repeated averaging</p>
<p class="wfd">パスグラフ上の信号(ギザギザの値)を横軸にノード、縦軸に値の折れ線で表示。Â を 0回、1回、3回、10回かけた結果を4段に重ね、ギザギザが消えてなだらかになる様子を示す。</p>
<p class="wft">Text in figure: "0 steps", "1 step", "3 steps", "10 steps", "node"</p>
</div>
<div>
<div class="box" data-tab="Repeated averaging">

$$\mathbf x^{(k)} = \hat A^k \mathbf x$$

<div class="note">

Here $\mathbf x \in \mathbb R^{n}$ is one feature over all nodes. Part 6 makes "smooth" precise.

</div>
</div>
</div>
</div>

---

<!-- _class: divider -->

<p class="crumb">GNN: from convolution to graphs</p>

## GraphSAGE and GAT

---

## A full neighborhood grows too fast

An $L$-layer GCN needs the $L$-hop neighborhood of every node it updates, and a hub pulls in a large part of the graph.

<div class="cols c32 mid">
<div class="wf" style="height:450px">
<p class="wfk">FIG 15 · Neighborhood size</p>
<p class="wfd">実ネットワーク(ロードマップや引用ネットワークなど)で、1ホップ・2ホップ・3ホップの近傍の大きさを、次数の低いノードとハブについて点で比較(実計算)。ハブの2ホップ近傍がグラフの何%になるかを示す。</p>
<p class="wft">Text in figure: "hop", "number of nodes", "typical node", "hub"</p>
</div>
<div>

- memory grows with the number of hops
- GCN needs the whole graph in memory
- GraphSAGE bounds the cost per node

</div>
</div>

---

## GraphSAGE samples a neighborhood

For each target node, GraphSAGE builds a computation tree from a fixed number of sampled neighbors per level.

<div class="cols c32 mid">
<div class="wf" style="height:470px">
<p class="wfk">ANIM 7a · Sampling</p>
<p class="wfd">左:グラフ上に着目ノード(赤)。右:そのノードを根とする計算木。1段目:近傍から S₁=3 個をサンプル、2段目:それぞれから S₂=2 個。サンプルされなかった近傍は薄く表示。サンプルは一様、またはランダムウォークの訪問(PinSAGE)。</p>
<p class="wft">Text in figure: "target node", "sampled neighbors", "not sampled", "level 1", "level 2"</p>
</div>
<div>
<div class="box" data-tab="Sampled neighbors">

$$S(v) \subseteq \mathcal N(v), \qquad |S(v)| = S_l$$

<div class="note">

$S_l$ is fixed per level, so the tree has at most $S_1 S_2$ leaves.

</div>
</div>
</div>
</div>

---

## Messages move from the leaves to the root

Features of the leaves are aggregated into their parents, then into the root, one level per layer.

<div class="cols c32 mid">
<div class="wf" style="height:470px">
<p class="wfk">ANIM 7b · Aggregation on the tree</p>
<p class="wfd">ANIM 7a と同じ計算木。まず葉から2段目へ矢印と共に特徴が集まり(層1)、次に2段目から根へ(層2)。各段で「集約」→「自分の特徴と結合(concatenate)」→「W と σ」を表示。</p>
<p class="wft">Text in figure: "layer 1", "layer 2", "aggregate", "concatenate", "root"</p>
</div>
<div>
<div class="box eq-sm" data-tab="Aggregate">

$$\mathbf h_{\mathcal N(v)}^{(l)} = \mathrm{AGG}\big(\{\mathbf h_u^{(l)} : u \in S(v)\}\big)$$

<div class="note">

$\mathrm{AGG}$: mean or element-wise max.

</div>
</div>
</div>
</div>

---

## The GraphSAGE layer

The feature of the node itself is concatenated with the aggregated neighbor feature before the linear map.

<div class="box eq-lg" data-tab="GraphSAGE layer">

$$\mathbf h_v^{(l+1)} = \sigma\Big(\big[\,\mathbf h_v^{(l)} \,\Vert\, \mathbf h_{\mathcal N(v)}^{(l)}\,\big]\, W^{(l)}\Big)$$

<div class="note">

$\Vert$ joins two row vectors into one longer row vector (Hamilton et al. 2017).

</div>
</div>

<div class="wf" style="height:260px">
<p class="wfk">FIG 16 · Concatenation</p>
<p class="wfd">2本の横長のベクトル(自分の特徴、近傍の集約)が連結されて1本になり、W(縦長の行列)を掛けて新しい特徴になる。ベクトルは数値の並びの箱で描く。</p>
<p class="wft">Text in figure: "self", "neighbors", "concatenate", "× W", "σ"</p>
</div>

---

## Concatenation keeps the node's own feature

GCN mixes the node with its neighbors in one sum; GraphSAGE gives the node and its neighbors separate weights.

<div class="cols c11 stretch">
<div class="box" data-tab="GCN">

$$\sigma\Big(\sum_{j} \hat A_{ij}\, \mathbf h_j\, W\Big)$$

<div class="note">

The same $W$ for the node and its neighbors.

</div>
</div>
<div class="box" data-tab="GraphSAGE">

$$\sigma\big(\hl{\mathbf h_v W_{\text{self}}} + \hlc{\mathbf h_{\mathcal N(v)} W_{\text{nbr}}}\big)$$

<div class="note">

$[\mathbf h_v \Vert \mathbf h_{\mathcal N}]\, W = \mathbf h_v W_{\text{self}} + \mathbf h_{\mathcal N} W_{\text{nbr}}$, where $W$ is split into two blocks.

</div>
</div>
</div>

<div class="wf" style="height:200px">
<p class="wfk">FIG 17 · Weights per role</p>
<p class="wfd">左(GCN):着目ノードと隣接ノードが同じ色の矢印で足される。右(GraphSAGE):着目ノードからの矢印は薄紫、隣接ノードからの矢印は薄水色で、別々の重みを持つ。</p>
<p class="wft">Text in figure: "same weight", "separate weights"</p>
</div>

---

## Neighbors differ in importance

GCN weights depend only on degrees; GAT learns a weight $\alpha_{ij}$ for each edge from the features of its two ends.

<div class="wf" style="height:470px">
<p class="wfk">FIG 18 · Fixed and learned weights</p>
<p class="wfd">左(GCN):着目ノード i と4つの隣接ノード。辺の太さは次数だけで決まり、ほぼ同じ。右(GAT):同じ配置で辺の太さが特徴に応じて異なる(1本が太く、1本が細い)。</p>
<p class="wft">Text in figure: "GCN: fixed by degree", "GAT: learned from features", "α_ij"</p>
</div>

---

## The attention coefficient

GAT scores each edge from the two transformed features, then normalizes the scores over the neighbors of $i$ with a softmax.

<div class="cols c32 mid">
<div class="wf" style="height:470px">
<p class="wfk">ANIM 8 · Attention (GAT v1)</p>
<p class="wfd">ノード i と隣接ノード j₁, j₂, j₃。各ノードの特徴に W を掛け、(i, j) ごとに連結 → ベクトル a との内積 → LeakyReLU でスコア e_ij。3つのスコアに softmax をかけて α_ij(合計1)。α に比例する太さの辺で、加重和が i に集まる。</p>
<p class="wft">Text in figure: "score e_ij", "softmax over neighbors", "α_ij sum to 1", "weighted sum"</p>
</div>
<div>
<div class="box eq-sm" data-tab="GAT layer">

$$\begin{aligned}
e_{ij} &= \mathrm{LeakyReLU}\big([\mathbf h_i W \,\Vert\, \mathbf h_j W]\,\mathbf a\big)\\
\alpha_{ij} &= \frac{\exp e_{ij}}{\sum_{k \in \mathcal N(i)} \exp e_{ik}}\\
\mathbf h_i' &= \sigma\Big(\sum_{j \in \mathcal N(i)} \alpha_{ij}\, \mathbf h_j W\Big)
\end{aligned}$$

<div class="note">

$W$ and $\mathbf a$ are learned. $\mathcal N(i)$ includes $i$ (Veličković et al. 2018).

</div>
</div>
</div>
</div>

---

## GCN, GraphSAGE and GAT compared

The three layers differ in how the weight of each neighbor is chosen and in how the node's own feature enters.

| | weight of neighbor $j$ | own feature | neighbors used |
|---|---|---|---|
| GCN | $1/\sqrt{\tilde d_i \tilde d_j}$, fixed | in the sum (self-loop) | all |
| GraphSAGE | equal (mean) or max | concatenated | sampled subset |
| GAT | $\alpha_{ij}$, learned from $\mathbf h_i, \mathbf h_j$ | in the sum (self-loop) | all |

<div class="wf" style="height:210px">
<p class="wfk">FIG 19 · Three layers, one picture</p>
<p class="wfd">同じ小さなグラフの着目ノードに対し、3つの手法で辺の太さ・矢印の色を並べる(GCN:次数で決まる細さ、SAGE:サンプルされた辺だけ濃い、GAT:太さがばらばら)。</p>
<p class="wft">Text in figure: "GCN", "GraphSAGE", "GAT"</p>
</div>

---

<!-- _class: divider -->

<p class="crumb">GNN: from convolution to graphs</p>

## Message passing and the Weisfeiler–Lehman test

---

## The message passing framework

GCN, GraphSAGE and GAT compute a message on each edge, aggregate the messages at a node, and update the node.

<div class="cols c32 mid">
<div class="wf" style="height:460px">
<p class="wfk">FIG 20 · Message, aggregate, update</p>
<p class="wfd">着目ノード i と隣接ノード3つ。(1) 各辺に載る「メッセージ m_ij」、(2) 受け取ったメッセージを「集約 ⊕」して a_i、(3) 自分の h_i と a_i から「更新 ψ」して新しい h_i。3段階を色分けした3枚のスライドに分けて構築する(ビルド)。</p>
<p class="wft">Text in figure: "message", "aggregate", "update"</p>
</div>
<div>
<div class="box eq-sm" data-tab="Message passing">

$$\begin{aligned}
\mathbf m_{ij} &= \phi(\mathbf h_i, \mathbf h_j) \\
\mathbf a_i &= \bigoplus_{j \in \mathcal N(i)} \mathbf m_{ij} \\
\mathbf h_i' &= \psi(\mathbf h_i, \mathbf a_i)
\end{aligned}$$

<div class="note">

$\bigoplus$ is permutation-invariant (Gilmer et al. 2017).

</div>
</div>
</div>
</div>

---

## Each model is a choice of $\phi$, $\bigoplus$ and $\psi$

The three layers of Part 2 and Part 3 fit the framework with different functions.

| | message $\phi(\mathbf h_i, \mathbf h_j)$ | aggregate $\bigoplus$ | update $\psi(\mathbf h_i, \mathbf a_i)$ |
|---|---|---|---|
| GCN | $\hat A_{ij}\, \mathbf h_j$ | sum over $\mathcal N(i)\cup\{i\}$ | $\sigma(\mathbf a_i W)$ |
| GraphSAGE | $\mathbf h_j$ | mean over $S(i)$ | $\sigma([\mathbf h_i \Vert \mathbf a_i]\,W)$ |
| GAT | $\alpha_{ij}\, \mathbf h_j W$ | sum over $\mathcal N(i)\cup\{i\}$ | $\sigma(\mathbf a_i)$ |

---

## Readout for a whole graph

A graph-level prediction pools the final node features into one vector.

<div class="cols c32 mid">
<div class="wf" style="height:440px">
<p class="wfk">FIG 21 · Graph classification</p>
<p class="wfd">グラフ → L 層のメッセージパッシング(各層は同じ箱の積み重ね)→ ノードごとの特徴 → 集約(readout)→ 1本のベクトル → 分類器 → ラベル(例:分子が毒性を持つか)。</p>
<p class="wft">Text in figure: "L layers", "node features", "readout", "graph feature", "classifier"</p>
</div>
<div>
<div class="box" data-tab="Readout">

$$\mathbf h_G = \rho\big(\{\!\{\mathbf h_v^{(L)} : v \in V\}\!\}\big)$$

<div class="note">

$\{\!\{\cdot\}\!\}$ is a multiset. $\rho$ is sum or mean.

</div>
</div>
</div>
</div>

---

## Can a GNN tell these two graphs apart?

Both graphs have 6 nodes, every node has degree 2, and all nodes carry the same feature.

<div class="wf" style="height:470px">
<p class="wfk">FIG 22 · 6-cycle and two triangles</p>
<p class="wfd">左:6角形(6ノードの環)。右:三角形が2つ(互いに離れている)。ノードはすべて同じ灰色。中央に「=?」。</p>
<p class="wft">Text in figure: "G₁: one cycle of 6", "G₂: two triangles", "same node features"</p>
</div>

<p class="muted">Take a minute.</p>

---

## The Weisfeiler–Lehman test

The WL test repeatedly relabels each node by its own label and the multiset of its neighbors' labels.

<div class="box" data-tab="WL iteration">

$$c_v^{(0)} = \text{initial label of } v, \qquad c_v^{(t+1)} = \mathrm{HASH}\Big(c_v^{(t)},\ \{\!\{c_u^{(t)} : u \in \mathcal N(v)\}\!\}\Big)$$

<div class="note">

Two graphs are non-isomorphic if their multisets of labels $\{\!\{c_v^{(t)}\}\!\}$ differ at some $t$ (Weisfeiler & Lehman 1968).

</div>
</div>

<div class="wf" style="height:260px">
<p class="wfk">FIG 23 · Algorithm as a loop</p>
<p class="wfd">ループ図:ラベルのリスト → 各ノードで「自分のラベル+隣のラベルの集合」を作る → ハッシュで新しいラベル(色)に置き換える → 変化がなくなるまで繰り返す → 色のヒストグラムを2つのグラフで比べる。</p>
<p class="wft">Text in figure: "own label", "neighbor labels (multiset)", "HASH", "new label", "compare histograms"</p>
</div>

---

## WL separates a path from a star

After one iteration the colors of the path and the star differ, so the test reports that the graphs are not isomorphic.

<div class="wf" style="height:470px">
<p class="wfk">FIG 24 · WL run, 4 nodes</p>
<p class="wfd">上段:パス(4ノード)と星(中心1+葉3)、全ノード同色。下段:1回の反復後。パスは端2ノード=色A、内側2ノード=色B。星は中心=色C、葉3=色A。色ヒストグラム(点で表示)が異なる。ハッシュの対応表(ラベル→色)を右に表示。</p>
<p class="wft">Text in figure: "iteration 0", "iteration 1", "histogram", "HASH table"</p>
</div>

---

## WL cannot separate a 6-cycle from two triangles

Every node has the same label and the same neighbor multiset at every iteration, so the color histograms of the two graphs stay equal.

<div class="cols c32 mid">
<div class="wf" style="height:450px">
<p class="wfk">FIG 25 · WL run, 6-cycle and two triangles</p>
<p class="wfd">FIG 22 と同じ2つのグラフ(同じ位置)。反復 0 と反復 1 を並べ、全ノードが同じ色のまま。色ヒストグラムは「6ノード×色A」で一致。</p>
<p class="wft">Text in figure: "iteration 0", "iteration 1", "same histogram"</p>
</div>
<div>
<div class="box eq-sm" data-tab="Why">

$$c_v^{(1)} = \mathrm{HASH}\big(c,\ \{\!\{c, c\}\!\}\big)\quad \text{for all } v$$

<div class="note">

Each node has two neighbors with label $c$, in both graphs.

</div>
</div>
</div>
</div>

---

## WL steps correspond to GNN modules

Each part of a WL iteration has a counterpart in a message passing layer.

<div class="wf" style="height:490px">
<p class="wfk">FIG 26 · Correspondence</p>
<p class="wfd">左右2列、対応を矢印で結ぶ。左 WL、右 GNN。(1) 初期ラベル c⁽⁰⁾ ↔ 入力特徴 x_v(特徴がなければ全ノード同じ)。(2) 隣のラベルの集合 {{c_u}} ↔ 集約 ⊕(順序に依らない)。(3) ハッシュ HASH ↔ 更新 ψ(MLP)。(4) 1回の反復 ↔ 1層。(5) 色のヒストグラム ↔ readout ρ。同じ色で対応を示す。</p>
<p class="wft">Text in figure: "WL test", "message passing GNN", "initial label ↔ input feature", "multiset ↔ aggregate", "HASH ↔ update", "iteration ↔ layer", "histogram ↔ readout"</p>
</div>

---

## A GNN is at most as strong as the WL test

If WL gives two nodes the same label after $t$ iterations, a $t$-layer message passing GNN gives them the same feature.

<div class="box" data-tab="Theorem (Xu et al. 2019; Morris et al. 2019)">

$$c_u^{(t)} = c_v^{(t)} \;\Longrightarrow\; \mathbf h_u^{(t)} = \mathbf h_v^{(t)}$$

<div class="note">

Therefore the 6-cycle and the two triangles get the same graph feature from any message passing GNN, whatever its weights.

</div>
</div>

<div class="wf" style="height:210px">
<p class="wfk">FIG 27 · Theorem as a picture</p>
<p class="wfd">WL の色(c)と GNN の特徴(h)の「分け方」を2つの円(集合)で描く。GNN が分ける分割は WL の分割より粗い(WL の円の内側に GNN の円)。FIG 22 の2つのグラフは円の外では区別できないことを点で示す。</p>
<p class="wft">Text in figure: "partition by WL", "partition by GNN", "GNN ≤ WL"</p>
</div>

---

## Mean and max lose information that sum keeps

For one-hot node labels, mean and max give the same output for different multisets of neighbors; sum does not.

<div class="wf" style="height:470px">
<p class="wfk">FIG 28 · Aggregators on multisets</p>
<p class="wfd">3行の表。行1:{赤, 青} と {赤, 赤, 青, 青}:mean は同じ (½, ½)、sum は (1,1) と (2,2) で異なる。行2:{赤, 青, 青} と {赤, 赤, 青}:max は同じ (1,1)、sum は (1,2) と (2,1)。行3:別の例。丸の色で多重集合を描く。</p>
<p class="wft">Text in figure: "mean", "max", "sum", "same output", "different output"</p>
</div>

---

## GIN reaches the WL limit

With sum aggregation and an injective update, a GNN separates exactly the graphs that the WL test separates.

<div class="box eq-lg" data-tab="Graph isomorphism network (GIN)">

$$\mathbf h_v^{(l+1)} = \mathrm{MLP}^{(l)}\Big((1 + \epsilon)\, \mathbf h_v^{(l)} + \sum_{u \in \mathcal N(v)} \mathbf h_u^{(l)}\Big)$$

<div class="note">

Xu et al. 2019. The MLP stands for the injective update, the sum for the injective aggregation.

</div>
</div>

- GCN and GraphSAGE (mean, max) are at most as strong as GIN
- no choice of $\phi$, $\bigoplus$, $\psi$ goes beyond WL

---

<!-- _class: divider -->

<p class="crumb">GNN: from convolution to graphs</p>

## Subgraph GNN

---

## Mark one node, run the GNN, repeat for every node

A subgraph GNN gives one node an identifying feature, runs a GNN on that marked graph, and repeats this for every node.

<div class="wf" style="height:470px">
<p class="wfk">FIG 29 · Subgraph GNN pipeline</p>
<p class="wfd">左:6角形。中:6つのコピー、それぞれ別の1ノードが赤(印)。右:各コピーに同じ GNN をかけ、ノードごとに特徴を得る。最後に6コピーの特徴をノードごとに集約して1つにする(矢印)。</p>
<p class="wft">Text in figure: "graph G", "marked copies G_s", "GNN on each copy", "aggregate over s"</p>
</div>

---

## The subgraph GNN in formulas

Node features are computed per marked copy and then aggregated over the marks; edge and graph features follow from node features.

<div class="cols c11 stretch">
<div>
<div class="box eq-sm" data-tab="Marked copy and GNN">

$$\mathbf x_v^{(s)} = \big[\,\mathbf x_v \,\Vert\, \mathbb 1[v = s]\,\big]$$

$$\mathbf h_v^{(s)} = \mathrm{GNN}\big(G,\ \mathbf X^{(s)}\big)_v$$

</div>
<div class="box eq-sm" data-tab="Aggregate over marks">

$$\mathbf h_v = \mathrm{AGG}_{s \in V}\, \mathbf h_v^{(s)}$$

</div>
</div>
<div>
<div class="box eq-sm" data-tab="Edge and graph features">

$$\mathbf h_{uv} = \mathrm{MLP}\big([\mathbf h_u \Vert \mathbf h_v]\big)$$

$$\mathbf h_G = \rho\big(\{\!\{\mathbf h_v : v \in V\}\!\}\big)$$

<div class="note">

$\mathrm{AGG}$ and $\rho$: sum. Bevilacqua et al. 2022; Cotta et al. 2021.

</div>
</div>
</div>
</div>

---

## Marking separates the 6-cycle from two triangles

With node $s$ marked, the nodes of the cycle receive three different distances from $s$; in the two triangles, one triangle is never reached.

<div class="wf" style="height:470px">
<p class="wfk">FIG 30 · Marked WL on FIG 22</p>
<p class="wfd">上:6角形で1ノード s を印(赤)にして WL を2反復。s からの距離 0, 1, 1, 2, 2, 3 に応じて色が分かれる(4色)。下:三角形2つ。s のある三角形は距離 0, 1, 1、もう一方の三角形は3ノードとも色が変わらない(2色+1色)。色ヒストグラム(点)が異なる。</p>
<p class="wft">Text in figure: "marked node s", "distance 0/1/2/3", "histogram differs"</p>
</div>

---

## Cost and choice of subgraphs

Using all $n$ marked copies multiplies the cost of one GNN by $n$, so practical models use a sample of subgraphs.

<div class="cols c32 mid">
<div class="wf" style="height:430px">
<p class="wfk">FIG 31 · Subgraph policies</p>
<p class="wfd">同じグラフに対する3種類のサブグラフ集合を並べる:(1) ノードに印(全ノード分)、(2) ノードを1つ削除、(3) 着目ノードのエゴネット(k ホップ)。それぞれ3〜4コピーだけ描く。</p>
<p class="wft">Text in figure: "node-marked", "node-deleted", "ego network"</p>
</div>
<div>

- cost: $n$ GNN runs per graph
- sample a few subgraphs per graph
- more expressive than WL

</div>
</div>

---

<!-- _class: divider -->

<p class="crumb">GNN: from convolution to graphs</p>

## The spectral view of GCN

---

## One layer can look more than one hop

A layer can combine $\hat A^0 \mathbf x, \hat A^1 \mathbf x, \dots, \hat A^K \mathbf x$ and so see nodes up to $K$ hops away.

<div class="cols c32 mid">
<div class="wf" style="height:460px">
<p class="wfk">FIG 32 · Hops in one layer</p>
<p class="wfd">空手クラブ上で着目ノードを中心に、0ホップ、1ホップ、2ホップ、3ホップの寄与を、4枚の小さな図(同じネットワーク、同じ位置)で並べる。各図の下に重み θ_k。</p>
<p class="wft">Text in figure: "k = 0", "k = 1", "k = 2", "k = 3", "θ_k"</p>
</div>
<div>
<div class="box" data-tab="Polynomial filter">

$$\mathbf y = \sum_{k=0}^{K} \theta_k\, \hat A^k\, \mathbf x$$

<div class="note">

$\mathbf x \in \mathbb R^n$: one feature over all nodes. $\theta_k$ are learned.

</div>
</div>
</div>
</div>

---

## Eigenvectors of the Laplacian are waves on a graph

The eigenvectors $\mathbf u_k$ of $L = D - A$ play the role of sines and cosines, and the eigenvalue $\lambda_k$ is the frequency.

<div class="cols c32 mid">
<div class="wf" style="height:470px">
<p class="wfk">ANIM 10 · Graph Fourier basis</p>
<p class="wfd">空手クラブのネットワーク。スライダまたはボタンで k を選ぶと、ノードの色が u_k の値(青〜赤)に変わる。k=1(定数)、k=2(2クラブの符号が分かれる)、k=34(隣同士で正負が交互)。下に λ_k の点の並び。スライド上のインタラクティブ、PDF は3コマ。</p>
<p class="wft">Text in figure: "u_k", "λ_k", "low frequency", "high frequency"</p>
</div>
<div>
<div class="box eq-sm" data-tab="Graph Fourier transform">

$$L = U \Lambda U^{\top}, \qquad \hat{\mathbf x} = U^{\top} \mathbf x$$

$$\mathbf x^{\top} L\, \mathbf x = \sum_{(i,j) \in E} (x_i - x_j)^2 = \sum_k \lambda_k\, \hat x_k^2$$

<div class="note">

A small $\lambda_k$ means $\mathbf u_k$ changes little across edges.

</div>
</div>
</div>
</div>

---

## Spectral convolution filters frequencies

A spectral filter multiplies the component of each frequency by $g(\lambda_k)$, in the same way as a kernel does for an image.

<div class="cols c32 mid">
<div class="wf" style="height:450px">
<p class="wfk">FIG 33 · Low-pass and high-pass on a graph</p>
<p class="wfd">2段。上:低域通過 g(λ)(λ が小さいほど1)。下:高域通過。各段:g(λ) の曲線(34個の固有値を曲線上の点で表示)→ 入力信号と出力信号をネットワーク上の色で。画像の FIG 8 と同じ見せ方。</p>
<p class="wft">Text in figure: "g(λ)", "low-pass", "high-pass", "input", "output"</p>
</div>
<div>
<div class="box" data-tab="Spectral convolution">

$$\mathbf y = U\, g(\Lambda)\, U^{\top} \mathbf x$$

<div class="note">

Image: $\hat Y = \hat K \cdot \hat X$ (FIG 5). Graph: $\hat y_k = g(\lambda_k)\,\hat x_k$.

</div>
</div>
</div>
</div>

---

## ChebNet and GCN are polynomial filters

A degree-$K$ polynomial of $L$ filters without an eigendecomposition and uses only nodes within $K$ hops.

<div class="cols c32 mid">
<div class="wf" style="height:440px">
<p class="wfk">FIG 34 · Filter response</p>
<p class="wfd">横軸 λ、縦軸 g(λ)。K=1(GCN)、K=3、K=8 の3本の曲線と、空手クラブの固有値の点。K が大きいほど細かい形の g が作れることを示す。</p>
<p class="wft">Text in figure: "λ", "g(λ)", "K = 1 (GCN)", "K = 3", "K = 8"</p>
</div>
<div>
<div class="box eq-sm" data-tab="ChebNet">

$$\mathbf y = \sum_{k=0}^{K} \theta_k\, T_k(\tilde L)\, \mathbf x$$

$$\tilde L = \tfrac{2}{\lambda_{\max}} L - I$$

<div class="note">

$T_k$: Chebyshev polynomial. $K=1$ with $\theta_0 = -\theta_1$ gives GCN (Kipf & Welling 2017).

</div>
</div>
</div>
</div>

---

## High frequencies mark the border between the clubs

The high-frequency part of the eigenvector centrality is larger on the 13 nodes with a neighbor in the other club (mean $|\cdot|$ 0.080) than on the other 21 nodes (0.024).

<div class="cols c32 mid">
<div class="wf" style="height:450px">
<p class="wfk">FIG 35 · Karate club, high-frequency component</p>
<p class="wfd">左:空手クラブ。ノードの色=固有ベクトル中心性(ハブ0と33が濃い)。右:同じネットワークで、固有ベクトルの周波数が高い方の半分(34個中17個)だけで再構成した成分。クラブの境界のノードの絶対値が大きく、中心性の高いノードに囲まれたノードは小さい。</p>
<p class="wft">Text in figure: "eigenvector centrality", "high-frequency part", "border nodes", "interior nodes"</p>
</div>
<div>
<div class="box eq-sm" data-tab="High-frequency part">

$$\mathbf x_{\text{high}} = \sum_{k \ge 18} \hat x_k\, \mathbf u_k$$

<div class="note">

$\mathbf x$ is the eigenvector centrality. Border: a node with a neighbor in the other club.

</div>
</div>
</div>
</div>

---

<!-- _class: roomy -->

## Summary

- Convolution sums a window of neighbors with shared weights; the Fourier transform shows it as a filter on frequencies
- GCN, GraphSAGE and GAT replace the pixel window by the neighbors of a node
  - GCN: fixed weights; GraphSAGE: sampled neighbors and concatenation; GAT: learned weights
- All three are message passing, so they are at most as strong as the WL test
  - Subgraph GNNs mark nodes to go beyond it
- A GCN layer is a polynomial filter on the graph Laplacian's frequencies

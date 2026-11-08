# m08 GNN スライド・モック v1(2026-11-08)

`m08-gnn.md`(slide-math スタイル、英語、58枚)。plan.md の流れに沿った骨組み。
図は点線の枠で、枠内に「図の説明(日本語)」と「図に入れる文字(英語、斜体)」を書いた。式は本物。
アニメーションは ANIM 1〜8, 10 の札を付けた(plan の番号と同じ。9 は FIG 20〜28 のメッセージパッシングと WL)。

PDF: `m08-gnn.pdf`(Git には入れない。`~/.claude/skills/slide-math/tools/render.sh m08-gnn.md pdf` で作る)。
チェック: `python3 ~/.claude/skills/slide-math/tools/check.py m08-gnn.md`(エラー0、警告0)。

## 配分(1枚1分、授業は2回)

| 回 | 部 | スライド | 枚数 |
|---|---|---|---|
| 1 | 1 画像の畳み込みとフーリエ変換 | 3–15 | 13 |
| 1 | 2 GCN | 16–25 | 10 |
| 1 | 3 GraphSAGE と GAT | 26–34 | 9 |
| 2 | 4 メッセージパッシングと WL テスト | 35–46 | 12 |
| 2 | 5 サブグラフ GNN | 47–51 | 5 |
| 2 | 6 スペクトルの見方 | 52–57 | 6 |
| | 要約 | 58 | 1 |

第1回は 34 枚、第2回は 24 枚(式が重いので第2回は1枚あたりの時間が長い)。境界は部 3 と部 4 の間。

## スライド一覧

| # | タイトル | 図(札) | 式 |
|---|---|---|---|
| 4 | Images as arrays of pixels | FIG 1 画素の拡大と RGB | $X\in\mathbb R^{H\times W\times 3}$ |
| 5 | Convolution with a kernel | **ANIM 1** 窓の走査 | $Y_{ij}=\sum K_{ab}X_{i+a,j+b}$ |
| 6 | The kernel sets the pattern | FIG 2 同じ画像に3カーネル | 3つの 3×3 行列 |
| 7 | The kernel is local and shared | FIG 3 受容野 3×3→5×5 | |
| 8 | A signal is a sum of waves | **ANIM 2** 時間軸→周波数軸への回転 | フーリエ級数 |
| 9 | The weights are the signal in the frequency domain | FIG 4 時間領域と周波数領域 | |
| 10 | Convolution becomes multiplication | FIG 5 畳み込み定理 | $\widehat{f*g}=\hat f\hat g$ |
| 11 | Waves in two dimensions | **ANIM 3a** 2D の波と周波数平面 | $e^{2\pi i(ux+vy)}$ |
| 12 | The 2D Fourier transform of an image | FIG 6 画像とスペクトル | 2D フーリエ変換 |
| 13 | Masking frequencies changes the image | **ANIM 3b** 低周波/高周波マスク | |
| 14 | JPEG discards high frequencies | FIG 7 JPEG | |
| 15 | Kernels are filters on frequencies | FIG 8 カーネルと周波数応答 | |
| 17 | An image is a graph | **ANIM 4** 格子→グラフ | 隣接行列 |
| 18 | Convolution is a sum over neighbors | FIG 9 | 画像の式 ▶ グラフの式 |
| 19 | GCN weights neighbors by degree | FIG 10 重み付き5ノード | $\hat A=\tilde D^{-1/2}\tilde A\tilde D^{-1/2}$ |
| 20 | The GCN layer | FIG 11 層のフロー | GCN 層(行ベクトル規約) |
| 21 | One layer in three steps | **ANIM 6** 集約→W→ReLU(実際は3枚に分ける) | 3行の式 |
| 22 | Example: one layer on a small graph | FIG 12 数値例(計算は図スクリプトで) | |
| 23 | Stacking layers widens the view | FIG 13 ホップ | |
| 24 | An untrained GCN groups similar nodes | **ANIM 5** 乱数 GCN の出力(空手クラブ) | |
| 25 | Neighbor averaging smooths the signal | FIG 14 繰り返し平均 | $\hat A^k\mathbf x$ |
| 27 | A full neighborhood grows too fast | FIG 15 近傍の大きさ(実データ) | |
| 28 | GraphSAGE samples a neighborhood | **ANIM 7a** 計算木のサンプリング | $S(v)\subseteq\mathcal N(v)$ |
| 29 | Messages move from the leaves to the root | **ANIM 7b** 葉→根の集約 | AGG |
| 30 | The GraphSAGE layer | FIG 16 連結 | $[\mathbf h_v\Vert\mathbf h_{\mathcal N}]W$ |
| 31 | Concatenation keeps the node's own feature | FIG 17 | GCN と SAGE の対比(薄紫/薄水色) |
| 32 | Neighbors differ in importance | FIG 18 固定/学習の重み | |
| 33 | The attention coefficient | **ANIM 8** GAT v1 | $e_{ij},\alpha_{ij},\mathbf h_i'$ |
| 34 | GCN, GraphSAGE and GAT compared | FIG 19 | 比較表 |
| 36 | The message passing framework | FIG 20(3ビルド) | $\phi,\bigoplus,\psi$ |
| 37 | Each model is a choice of φ, ⊕ and ψ | | 対応表 |
| 38 | Readout for a whole graph | FIG 21 | $\rho$ |
| 39 | Can a GNN tell these two graphs apart? | FIG 22 6角形 vs 三角形2つ(質問、答えなし) | |
| 40 | The Weisfeiler–Lehman test | FIG 23 アルゴリズム | WL の更新式 |
| 41 | WL separates a path from a star | FIG 24 | |
| 42 | WL cannot separate a 6-cycle from two triangles | FIG 25(答え) | |
| 43 | WL steps correspond to GNN modules | FIG 26 対応図 | |
| 44 | A GNN is at most as strong as the WL test | FIG 27 | 定理 |
| 45 | Mean and max lose information that sum keeps | FIG 28 | |
| 46 | GIN reaches the WL limit | | GIN の式 |
| 48 | Mark one node, run the GNN, repeat for every node | FIG 29 | |
| 49 | The subgraph GNN in formulas | | 4つの式 |
| 50 | Marking separates the 6-cycle from two triangles | FIG 30 | |
| 51 | Cost and choice of subgraphs | FIG 31 | |
| 53 | One layer can look more than one hop | FIG 32 | 多項式フィルタ |
| 54 | Eigenvectors of the Laplacian are waves on a graph | **ANIM 10** 基底を選ぶと色が変わる | グラフフーリエ変換 |
| 55 | Spectral convolution filters frequencies | FIG 33 | $U g(\Lambda)U^\top\mathbf x$ |
| 56 | ChebNet and GCN are polynomial filters | FIG 34 | ChebNet |
| 57 | High frequencies mark the border between the clubs | FIG 35 空手クラブの高周波成分 | |

## 数値で確かめたこと(スクリプトは未コミット。図のスクリプトで再計算する)

1. **空手クラブの高周波成分(スライド 57)。** 組合せラプラシアン $L=D-A$ の固有ベクトルのうち周波数が高い方の17本で固有ベクトル中心性を再構成した。
   - 境界ノード(別のクラブに隣接する13人)の $|\cdot|$ の平均は 0.080、残り21人は 0.024。境界で大きいという主張は成り立つ。
   - ただし最大値は境界ノードのうち中心性が最大のハブ(33、0、32)。「中心性の高いノードに囲まれたノードが低い」は、絶対値としては成り立つ(内側の平均が低い)。
   - 正規化ラプラシアンで同じ計算をすると 0.019 と 0.013 で差が小さい。**どちらの $L$ を使うか、先生の意図を確認したい。**
2. **未学習 GCN(スライド 24)。** 3層、入力は単位行列、tanh、2次元出力、乱数200回。2クラブを分ける方向(ラベルで当てはめた)での正解率は平均 0.77。0.9 を超えるシードは26%。グラフなし(Â = I)の同じ構成は 0.58。
   - 傾向はあるが毎回きれいに分かれない。アニメーションは複数のシードを見せ、「毎回ではない」と言う方が正直。

## 確認したいこと

1. 授業の境界を部 3 と部 4 の間にしてよいか。
2. 空手クラブの高周波(スライド 57)で使うラプラシアンと、図に出す量(絶対値か符号付きか)。
3. スライド 49 のサブグラフ GNN の式は、全ノードに印を付けた版(DS-GNN 型、独立に実行して和)にした。層ごとに印の間で情報を混ぜる版(DSS 型)は入れていない。
4. 参考文献は記憶による。公開前に確認する:Kipf & Welling 2017、Hamilton et al. 2017、Veličković et al. 2018、Gilmer et al. 2017、Xu et al. 2019、Morris et al. 2019、Bevilacqua et al. 2022、Cotta et al. 2021、Weisfeiler & Lehman 1968。サブグラフ GNN が 3-WL を超えないという上界(Frasca et al. 2022)はスライドに書いていない。
5. 画像の例(スライド 4, 6, 12–14)に使う写真。著作権の問題がないもの(自作、またはパブリックドメイン)を使う。
6. 画像のフーリエ変換は 6 枚(11–15 と 8–10)あり、第1回の約 3 分の 1。多ければ JPEG(14)を削る。

## 文言のチェック(N9)

タイトルはすべて名詞句か事実の文。比喩、擬人化、命令なし(例:"WL cannot separate…" は検証できる事実)。

# m08 埋め込み(スライド・モック v1)

2026-11-02。`m08-embedding.md`(slide-math スタイル、英語、36枚、1枚1分で約36分)。
図は `python3 figures/make_figures.py` で作ります(PNG/SVG はコミットしません)。チェック:`python3 ~/.claude/skills/slide-math/tools/check.py m08-embedding.md`(エラー0、警告0)。画像:`~/.claude/skills/slide-math/tools/render.sh m08-embedding.md png`。

## スライド一覧

| # | タイトル | 主張(リード) | 中身 | 状態 |
|---|---|---|---|---|
| 1-2 | Title / Outline | 3部構成 | | |
| 3 | (divider) From words to nodes | | | |
| 4 | Hand-made node features | 手作りの特徴量(次数、三角形、戻り確率) | 小さいグラフと特徴量の表 | 図は実計算(戻り確率 0.42) |
| 5 | Representation learning | 特徴量を設計せず学習する | 手作り/学習の2行フロー | |
| 6 | word2vec: words as vectors | 単語がベクトルになり、類推が線形代数になる | king − man + woman ≈ queen、平行四辺形の図 | 図は手描きの概念図(実データではない) |
| 7 | Prediction from context | 近くの単語を予測する。query と key の2ベクトル | CCS2027 の例文 *chance favors only the prepared mind* | CCS2027 スライド 46〜52 から再構成 |
| 8 | Training by contrast | 本物のペアは近づけ、ランダムなペアは離す(ロジスティック回帰) | ラベル表 + 目的関数 | CCS2027 スライド 53〜58 から再構成 |
| 9 | Walks as sentences | ウォークは文、ノードは単語 | 8ノードのグラフ、対応表 | |
| 10 | DeepWalk | walks → pairs → word2vec | 3つの箱+三角 | |
| 11 | The walk rule sets what is close | 歩き方が変われば埋め込みが変わる | 格子上の通常ウォークと再起ウォーク、2式 | node2vec は1行だけ |
| 12 | Lab: character embeddings | ラボの流れ | QR とラボ出力の**プレースホルダ** | ノートブックは作成済み(下) |
| 13 | Lab task: personalized PageRank walk | 学生が `ppr_walk` を実装 | コードの骨格、2つの問い | |
| 14 | (divider) Hyperbolic embedding | | | |
| 15 | Popularity and similarity | 新しいノードは人気と類似性で選ぶ | 2枚の図(ハブ、円周上の角度) | Papadopoulos 2012 |
| 16 | Growth rule of the model | $r_t=\ln t$、角度は一様、$s\,\theta_{st}$ が小さい $m$ 個に接続 | **成長の3コマ(t=8,20,60)**、実シミュレーション | **ここをアニメーションにする**(下の案) |
| 17 | Observed degree mixes two effects | 次数 = 人気(隠れ次数)× 類似ノードの数 | 部品付きの式 | **要確認**(下) |
| 18 | Same degree, different hidden degree | 同じ次数 6 でも、小さなコミュニティのノードは隠れ次数が大きい | 16ノードと8ノードのコミュニティ | **要確認** |
| 19 | Exponential growth of hyperbolic space | 円周が $2\pi\sinh r$ で指数的に増える | 式と曲線(実計算) | |
| 20 | Hyperbolic space as a continuous tree | 木の連続版。対数的に伸びる空間 | 二分木 → ポアンカレ円板(測地線で描画) | |
| 21 | WordNet in the Poincaré disk | 中心が抽象、端が具体 | 旧デッキの画像を大きく置いただけ | **出典要確認**(下) |
| 22 | (divider) Spectral embedding | | | |
| 23 | Compressing a matrix | $\mathbf A\approx\mathbf U\mathbf U^\top$、PCA との対応 | 行列の形の図 | |
| 24 | Eigendecomposition | $\mathbf A=\sum\lambda_k\mathbf u_k\mathbf u_k^\top$ | カラテクラブの A と最初の3項(ヒートマップ、実計算) | |
| 25 | Keeping the large terms | $|\lambda_k|$ の大きい $d$ 項を残す | $\mathbf A,\mathbf A_2,\mathbf A_6$ と固有値の点図 | |
| 26 | Optimality of the truncation | フロベニウスノルムで最適(Eckart–Young–Mirsky)、誤差 $=\sum_{k>d}\lambda_k^2$ | 誤差曲線(実計算、スクリプト内で式を検算) | |
| 27 | Matrices that represent a network | $\mathbf A,\mathbf D,\mathbf L,\mathbf L_{\mathrm{sym}}$ | 定義表 | |
| 28 | Cutting a network in two | Ratio Cut の定義 | 11ノードのグラフと2つのカット(Ratio Cut 1.10 と 0.37) | 数値は検算済み |
| 29 | Group indicator vector | 指示ベクトル $\mathbf x$ | 式と $\mathbf x$ の点図 | |
| 30 | Ratio Cut as a quadratic form | RatioCut $=\mathbf x^\top\mathbf L\mathbf x/N$ | 結果と導出(導出は P&P Q2, Q3) | |
| 31 | Relaxation to real values | 連続緩和で固有値問題、2番目に小さい固有ベクトル | 離散(NP困難)→ 緩和の2つの箱 | |
| 32 | Second eigenvector of the Laplacian | 符号が派閥を分ける | カラテクラブ、34人中33人が一致(実計算) | |
| 33 | Normalized Cut | 体積に置き換え | NCut、指示ベクトル、3つの性質(P&P Q4) | 検算済み(NCut 1.02 と 0.09) |
| 34 | Relaxation of Normalized Cut | $\mathbf L\mathbf x=\lambda\mathbf D\mathbf x\Leftrightarrow\mathbf L_{\mathrm{sym}}\mathbf y=\lambda\mathbf y$ | 2つの箱(P&P Q5) | |
| 35 | Pen and paper | 5問(10分) | 一覧表 | 下の計画を参照 |
| 36 | Summary | | | |

## 先生に確認したいこと

1. **隠れ次数(スライド 17、18)**。「小さいコミュニティと大きいコミュニティで同じ次数のノードを比べると、小さいコミュニティのほうが隠れ次数が大きい」と読みました。理由は、同じ次数に必要な「類似ノードの数」が少ないので、その分を人気で補う、という次数補正ブロックモデル型の議論です(次数 $k_i\approx\kappa_i\times$ 類似ノードへの接続量)。式 $k_i\propto\kappa_i\times n_i$ は私が定性的に書いた略記で、論文の式ではありません。使いたい式(あるいは元の論文)を教えてください。
2. **WordNet の図(スライド 21)**。旧デッキ(`slides/legacy/m08/figs/wordnet-hyperbolic-embedding.png`)の画像です。ポアンカレ埋め込みの原論文(Nickel & Kiela 2017)の図かどうか、私には確認できていません(中心が Entity で、Gauss や Hyperbolic Geometry のラベルがあります)。出典が決まるまで、キャプションは Nickel & Kiela 2017 と書いてあります。
3. **成長のアニメーション(スライド 16)**。今は静止画3コマです。案:①この3コマを t=8、20、60 の3枚のビルドにする(PDF でも使える)、②HTML のアニメーションを別に作り(`lecture-note/assets/anim.js` のキット)、QR で見せる。どちらにしますか。
4. **スライドのスタイル**。依頼どおり slide-math(英語、ハンドアウト風)で作りました。いつもの講義デッキ(house style、日本語なし)と見た目が違います。このまま進めてよいか教えてください。
5. **Part 1 の枚数**。word2vec(6〜8)を3枚にしました。時間が押しているので、7 と 8 を1枚にまとめる案もあります。

## ノートブック(ラボ)

`notebooks/m08-network-embedding/lab-walks.py`(学生用)、`lab-walks-solution.py`(解答つき)。marimo、約13セル。内容は、レ・ミゼラブルの読み込み、`random_walk` と `simulate_walks`、`embed`(gensim の Word2Vec)、キャラクターのドロップダウンと PCA の散布図、最近傍表、`ppr_walk`(学生の課題、スタブは通常のウォークを返す)、$\alpha$ のスライダー、通常のウォークとの比較です。Python は `>=3.10,<3.14` に固定。molab へのアップロード、短縮リンク、QR は未作業です(スライド 12 はプレースホルダ)。

# M08 ペン＆ペーパー 計画 v1(モック)

2026-11-02。スライド 28〜35(`slides/m08/m08-embedding.md`)の後に使う、Ratio Cut → ラプラシアン、Normalized Cut → 正規化ラプラシアンの導出シート。10分、紙1〜2ページ。LaTeX はまだ書いていません。現在の `exercise.tex`(外積と行列の分解)は、承認までそのまま残します。

スライドには式を載せてあり、導出はこのシートでやります。順序は「講義で式を見る → 自分の手で通す」です(`pen-and-paper` スキルの「名前が付く前に作る」とは逆なので、問いは「見た式を最後まで通す」形にしました)。

## 設定

11人のネットワーク(スライド 28 と同じ図):5人の完全グラフ2つを1本の辺で結び、片方に次数1の人 $p$ をつなぐ。$S$ = {$p$} と $S$ = 左の5人と $p$ の2通りのカット。数値はすべて計算で確認済みです。

## 問い

| 問 | 内容 | 答え |
|---|---|---|
| Q1 | $S$ = {$p$}、$|T|=10$ について、指示ベクトルの値 $\sqrt{|T|/|S|}$ と $-\sqrt{|S|/|T|}$ を書き、$\sum_i x_i=0$ と $\sum_i x_i^2=N$ を確かめる(一般の $S,T$ でも示す) | $\sqrt{10}$ と $-1/\sqrt{10}$。$\sqrt{|S||T|}-\sqrt{|S||T|}=0$、$|S|\frac{|T|}{|S|}+|T|\frac{|S|}{|T|}=N$ |
| Q2 | $\mathbf x^\top\mathbf L\mathbf x=\sum_i k_ix_i^2-\sum_{ij}A_{ij}x_ix_j=\frac12\sum_{ij}A_{ij}(x_i-x_j)^2$ を示す | $k_i=\sum_jA_{ij}$ を使って $\frac12\sum_{ij}A_{ij}(x_i^2+x_j^2)=\sum_ik_ix_i^2$ |
| Q3 | $\frac12\sum_{ij}A_{ij}(x_i-x_j)^2=\mathrm{cut}(S,T)(x_S-x_T)^2=N\,\mathrm{RatioCut}$ を示す。11人の例で両側を計算する | $S$ 内、$T$ 内の項は 0。$(x_S-x_T)^2=N^2/(|S||T|)=N(1/|S|+1/|T|)$。例:$\mathbf x^\top\mathbf L\mathbf x/N$ は 1.10 と 0.37(スライド 28 の RatioCut と一致) |
| Q4 | 同じ手順を Normalized Cut で行う:$x_S=\sqrt{\mathrm{vol}(T)/\mathrm{vol}(S)}$、$x_T=-\sqrt{\mathrm{vol}(S)/\mathrm{vol}(T)}$ について $\mathbf x^\top\mathbf D\mathbf 1=0$、$\mathbf x^\top\mathbf D\mathbf x=\mathrm{vol}(G)$、$\mathbf x^\top\mathbf L\mathbf x=\mathrm{vol}(G)\,\mathrm{NCut}$ | $\mathrm{vol}(S)\sqrt{\mathrm{vol}(T)/\mathrm{vol}(S)}-\mathrm{vol}(T)\sqrt{\mathrm{vol}(S)/\mathrm{vol}(T)}=0$ など。例:NCut = 1.02($S$={$p$})と 0.091(左のクリーク+$p$)、$\mathrm{vol}(G)=44$ |
| Q5 | 緩和した問題の解が $\mathbf L\mathbf x=\lambda\mathbf D\mathbf x$ を満たすことと、$\mathbf y=\mathbf D^{1/2}\mathbf x$ で $\mathbf L_{\mathrm{sym}}\mathbf y=\lambda\mathbf y$ になることを示す。最小の固有値 0 の固有ベクトルは何か | 両辺に $\mathbf D^{-1/2}$ を掛ける。固有値 0 の $\mathbf y\propto\mathbf D^{1/2}\mathbf 1$ は制約 $\mathbf x^\top\mathbf D\mathbf 1=0$(= $\mathbf y\perp\mathbf D^{1/2}\mathbf 1$)で除かれ、答えは2番目に小さい固有値 |

## 先生に決めてほしいこと

1. 「クイズ」は、この紙のペン＆ペーパーのことと読みました。Brightspace などの小テスト(`quiz/` の Google フォーム形式)にもするなら教えてください。
2. 問いの数と時間(5問・10分)。Q4 は Q1〜Q3 の繰り返しなので、時間が足りなければ Q4 を宿題にします。
3. 11人の例(数値の確認用の Q3、Q4 の末尾)を入れるか、一般の式だけにするか。

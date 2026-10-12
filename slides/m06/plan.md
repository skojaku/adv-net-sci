# m06 "All Roads Lead to Rome" — スライド計画 v2

2026-10-12、講師のレビュー(旧デッキ102枚への指摘)を受けて作り直し。旧計画 v1 (2026-08-05) は git 履歴にある。
実装は DECK_BUILD_GUIDE.md の Order of work に従う:本計画 → review/DECK_SPEC.md → review/FIGURE_SPEC.md →
figures → デッキ → check_render → /slide-review。

## 決定事項

| 論点 | 決定 |
|---|---|
| 形式 | **Marp のまま改修**(m06-centrality.md)。動きは GIF(make_animations.py)、操作する部品は lecture-note のアニメーションキットの stage(`--html` 書き出しで動く。ヘッドレス Chrome で実際に操作して確認する) |
| 日程 | シラバスどおり **10/20(火)・10/22(木)**、各90分。10/27 は Mini Project。(v1 の 10/14・10/16 は秋休みで誤り) |
| 枚数 | **1枚1分、各日45枚以内**。本計画は1日目 35枚、2日目 33枚 |
| 1枚の情報量 | 本文は2行まで。説明は動き(GIF)と口頭に回す。同じことを言うスライドは統合する |
| ローマ | **導入だけ**。写真1枚・実地図1枚・ネットワーク化1枚、次数の1枚まで。以降の指標はローマ網を使わない(ローマ網は演習で学生が触る) |
| 作業グラフ | 指標ごとに**小さな例**を作る。「簡単な例 → 2つの例で問う」の順 |
| 問いの例の条件 | 簡単すぎない。各指標について2つのグラフを並べ、(A) 一見中心に見えるノード(次数最大または図の真ん中)とは**別のノード**が1位になるもの、(B) 中心に見える2ノードのどちらが上か**計算しないと分からない**もの(差は最小単位1つ分)。全数値は verify_numbers.py でアサートする |
| 実データ | **NY州のハイウェイ網**(OSM の motorway/trunk)。**交差点(インターチェンジ)単位**に簡略化し、頂点は約150〜300、主要都市だけ地名を付ける。距離系の指標は道路の km で測る。右に地図、左に箇条書き |
| つかみ | NY州の8都市(Buffalo, Rochester, Syracuse, Utica, Albany, NYC, Watertown, Binghamton)のうち媒介中心性が最も高いのはどこか。答え(Binghamton)は媒介中心性のパートで出す。簡略化した網でも Binghamton が1位になるかは計算して確認する。ならなければ講師に報告する |
| 二つの軸 | 中心性は二つの選択で決まる、を全体の背骨にする。**軸1: どの経路を数えるか**(最短パス / ウォーク)、**軸2: 経路をどう数値にまとめるか**(和・逆数の和・最大値・通過数・長さで割り引いた本数)。最後のスライドでこの分類に全指標を並べる(旧89枚目 purpose-5 の形式) |
| 実演(操作) | 2つ。**べき乗法のステップボタン**(押すたびに A を1回掛ける)、**Katz の α スライダー**(0 から 1/λ_max の先まで) |
| 記法 | 講義ノート 01-concepts.qmd に合わせる。Katz の減衰パラメータは **α**(固有値の λ と区別するため。講師の指示では λ と書かれていたが、固有値分解のスライドで λ_k と衝突する)、PageRank のテレポート確率は r |
| 固有値分解の図 | lecture-note/figs/spectral-decomposition.jpg と同じ表し方:固有値 = 丸(大きさ = |λ|)、固有ベクトル = 縦長の長方形、その転置 = 横長の長方形、行列 = 正方形 |
| 色 | 固有ベクトルの符号は 青(+)/ オレンジ(−)、濃さで大きさ。緑は使わない。赤は強調文字だけ |
| 削除 | 旧93枚目以降(地図の描き直しによる頑健性、計算コスト、星とパス、応用3題、Module 07 予告)。旧10〜12枚目(クラブ網の3つの答え)。旧42〜43枚目(M03 の攻撃比較)。旧44枚目の配布物の案内 |
| 残すクイズ | 「次数・近接・離心・媒介の1位がすべて別のノードになるグラフを作れ」を最後に置く |

## 1日目 (10/20) — 最短パスで測る

旧デッキの枚数は「旧N」で示す(レンダリングしたページ番号)。

### 導入(5枚)

1. **タイトル** All Roads Lead to Rome
2. **20 BC, the Forum Romanum**(旧5・6 → 1枚)。写真を3枚並べる:カエサルの胸像、アウグストゥス像(プリマ・ポルタ)、
   ミリアリウム・アウレウム(フォロ・ロマーノに残る基部)。箇条書きで:アウグストゥスが紀元前20年に建てた金張りの柱 /
   帝国の主要都市とそこまでの距離(マイル)が刻まれていたとされる / 帝国の道はここから始まるとされた。
   刻まれていた内容は文献で確認し、確かでない点は "said to" と書く。写真はウィキメディア・コモンズから、クレジットをスライドに入れる
3. **The roads themselves**(旧7)。OpenStreetMap の実際の地図の上に、12都市の位置にピン
4. **Keep the roads, drop the map**(旧8・9 → 1枚)。GIF:地図が消え、ピンがノードに、街道が辺になる。最後の絵の上に
   問い「どの都市が一番重要か?」
5. **Today's question, at home**。NY州のハイウェイ網(右)と8都市。「媒介中心性が一番高い都市は?」(答えは33枚目)

### 次数(3枚)

6. **Degree centrality**(旧13〜16 → 1枚)。左に式と1行「隣のノードしか見ない」、右にローマ網と次数、1位に王冠。GIF で辺を数える
7. **Degree sees one step**(旧17〜19 → 1枚)。次数が同じで、2歩先の広がりが違う2ノード
8. **NY: degree tells interchanges apart?** NY網を次数で色分け。ほぼ全部が3か4で、区別がつかない

### 二つの軸(3枚)

9. **How far is u from v?** 6ノードほどの小さなネットワークで問う
10. **Two ways to count**。GIF:最短パス(長さ2、一本の数)→ 長さ2, 3, 4 のウォークを順に数える(本数は A^k から計算)
11. **Two choices make a centrality**。空の分類表(行 = 最短パス/ウォーク、列 = 和・逆数の和・最大値・通過数・割引した本数)。
    次数だけ「長さ1」の位置に置く。以降、パートの終わりで埋めていく

### 近接(6枚)

12. パート扉 **Close to everything**
13. **Closeness centrality**。GIF:1つのノードから距離の輪が広がり、各ノードに距離が書かれ、合計 → 式 (N−1)/Σ ℓ_ij
14. **Why N−1?**(旧25・26 → 1枚)。星グラフの中心でちょうど1
15. **Q: which node is closest to everything?** 2つのグラフ。(A) 真ん中に描かれた次数最大のノードが1位ではない、(B) 2候補が僅差
16. **A**。各ノードの横に距離の合計、1位に王冠
17. **NY: closeness**。右にNY網(道路 km で計算)、左に箇条書き(1位の場所と、なぜそこか)

### 非連結と調和(5枚)

18. **Q: what if a bridge closes?** 小さなグラフを2つに切る。近接中心性はどうなるか
19. **A: every score dies**。距離 ∞ → 全ノードの近接中心性が0
20. **Take the reciprocal first**。GIF:各距離を 1/ℓ に、1/∞ = 0。調和中心性の式
21. **Q: harmonic** 2つのグラフ(片方は非連結)。近接と調和で順位が入れ替わる例を含める
22. **A**

### 離心(4枚)

23. **Would you site a fire station on the average?**(旧31を維持)
24. **Eccentricity**。式 e_i = max_j ℓ_ij、中心性 1/e_i。GIF:各ノードから一番遠いノードに線が伸びる
25. **Q: eccentricity** 2つのグラフ。近接の1位と離心の1位が違う例
26. **A**

### 媒介(9枚)

27. パート扉 **The broker**
28. **Trace a letter**。簡単な例。GIF:手紙が最短パスを通り、各ノードの通過数が増えていく
29. **Betweenness centrality**。式 Σ σ_st(i)/σ_st
30. **Two routes, so a half each**。σ の割り算を小さな絵で
31. **Q: betweenness** 2つのグラフ。(A) 次数の低いノードが1位、(B) 2つのブローカー候補が僅差
32. **A**
33. **NY: betweenness**。右にNY網を媒介中心性で色分け、左に5枚目の答え:8都市中 Binghamton が1位(I-81、I-86/NY-17、I-88 が交わる)
34. **The shortest-path row, filled**。分類表の最短パスの行を埋める
35. **A question to sleep on**。「重要な隣を持つ都市は重要か?」

1日目:35枚(余裕約10枚。講師の判断で例や問いを足せる)

## 2日目 (10/22) — ウォークで測る

### 固有ベクトル(6枚)

1. パート扉 **Known by the company you keep**。イソップの絵(ベラスケス「イソップ」1638年)と "A man is known by the company he keeps"
2. **Importance you inherit**(旧47〜49 → 1枚)。GIF:隣のスコアが流れ込む。式 λ c_i = Σ_j A_ij c_j
3. **It is an eigenvector equation**(旧50の図を維持。小さな例のグラフに合わせて描き直す)
4. **Q: N eigenvectors. Which one?**
5. **All the eigenvectors**。小さなグラフ(7ノード)を固有ベクトルの数だけ並べ、ノードを符号(青 +、オレンジ −)と大きさ(濃さ)で塗る。
   固有値は数直線上に点と値、各グラフへ矢印。全ノードが青になるのは最大固有値の1つだけ
6. **Perron–Frobenius**。定理の文:連結な無向グラフでは、最大固有値の固有ベクトルだけが全要素正

### 線形代数の寄り道(4枚)

7. **Eigendecomposition**。A = Σ λ_k u_k u_kᵀ を丸と長方形で。GIF で項を1つずつ足す。各項はランク1の行列
8. **The eigenvectors are orthogonal**。u_kᵀ u_ℓ = 0(k≠ℓ)、= 1(k=ℓ)を長方形の掛け算で
9. **Square it**。A² = Σ λ_k² u_k u_kᵀ。GIF:2つの和を掛け、交差項が直交性で消え、丸が2乗になる
10. **Keep multiplying**。A^t:丸が λ_k^t で大きくなり、最大固有値の丸だけが残る((λ_2/λ_1)^t の値を図中に)

### べき乗法と局在化(6枚)

11. **Power iteration**【実演】ボタンを押すたびに x ← A x / ‖x‖。ノードの色と値が更新され、収束する
12. **Step one is degree**。A·1 = 次数
13. **Q: where does this break?** 4つのクリークがリング状につながった網
14. **Localization**。GIF:1つのクリークを 5 → 6 → 7 → 8 と大きくすると、固有ベクトル中心性がそのクリークに集中する(合計スコアに占める割合を図中に)
15. **NY: eigenvector centrality**。右にNY網(局在化が起きるかを計算して確認。起きればNYC周辺への集中を示す)、左に箇条書き
16. (予備)

### Katz(7枚)

17. パート扉 **Everyone gets a floor**
18. **Give everybody a baseline**。式 c_i = β + α Σ_j A_ij c_j → c = β (I − αA)⁻¹ 1
19. **What is that inverse?** 1/(1−x) = 1 + x + x² + …(|x| < 1)
20. **The same series for matrices**。(I − αA)⁻¹ = I + αA + α²A² + …。A^k は長さ k のウォークの数 → 長さで割り引いたウォーク
21. **Turn the dial**【実演】α スライダー。4クリークのリング網で、α = 0(全員同じ)→ 次数に近い → 固有ベクトルに近い(局在化)→ 1/λ_max を超えると意味を失う
22. **Why 1/λ_max?**(旧67)。丸の図で (I − αA)⁻¹ = Σ_k 1/(1 − αλ_k) u_k u_kᵀ。α → 1/λ_1 で最初の丸が膨らみ、超えると符号が反転する
23. **The walk row, filled**。分類表のウォークの行(次数 = 長さ1、Katz = 割引した全長、固有ベクトル = α → 1/λ_max の極限)

### HITS(3枚、旧68〜76 の9枚から短縮)

24. パート扉 **The Web has direction**。道は両向き、リンクは片向き
25. **Hubs and authorities**。左に箇条書きと2本の式、右に小さな有向グラフ(王冠2つ)
26. **On a road map, HITS is eigenvector centrality**。Aᵀ A の固有ベクトル。無向なら Aᵀ A = A²

### PageRank(5枚)

27. **The same equation, six times**(旧77の系譜図を維持)
28. **Divide the vote**。左に箇条書きと式 c_i = Σ_j A_ji c_j / d_j^out、右に小さな有向グラフ(5〜6ページ。旧より小さく)
29. **Q: the walker reaches a dead end**。左右の配置は28と同じ
30. **Teleportation**。式 c_i = (1−r) Σ_j A_ji c_j / d_j^out + r/N。左右の配置は同じ
31. **Personalized PageRank**。テレポート先を偏らせる。左右の配置は同じ

### まとめ(2枚)

32. **Two choices, every centrality**。分類表を完成させる(旧89 purpose-5 と同じく、小さなグラフのアイコンと名前で並べる)
33. **Quiz**。次数・近接・離心・媒介の1位がすべて別のノードになるグラフを作れ

2日目:33枚

## 実装メモ

- 旧デッキから流用:verify_numbers.py の仕組み、figlib.py(TikZ → PNG)、romelib.py(導入の4枚だけ)、旧50・77・89 の図
- 新規データ:NY網は Geofabrik の New York 抽出(または Overpass)から motorway/trunk を取り、ランプを含む近接ノードを1つのインターチェンジにまとめ、
  次数2の頂点を除く。手順は rochester-betweenness(GitHub)の betweenness.py を参照。生成物はコミットしない
- 写真:カエサル、アウグストゥス、ミリアリウム・アウレウム、イソップ(ベラスケス)をウィキメディア・コモンズから。ライセンスとクレジットを FIGURE_SPEC に記録
- 地図:OpenStreetMap のタイルで静的画像を作る。"© OpenStreetMap contributors" を図中に入れる
- 実演の2つは `lecture-note/assets/anim/power-step.js` と `katz-dial.js` に scene array として置き、講義ノートからも使えるようにする

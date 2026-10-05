# m05 Remotion スライド案 (DECK_SPEC)

2026-10-05。実装前の設計表。承認後に実装する。Remotion の土台は手順書どおり
`~/Downloads/fourier-slides` (展開済み、`npm install` 済み) を使う。

## 何を作るか

Marp デッキ `../m05-clustering.md` のモジュラリティの導出まで (「Game: where Q goes wrong」まで)
は今のまま使う。そのあとを Remotion のクリック式アニメーションに置き換え、次の3つを教える。

1. モジュラリティの限界 (解像度限界、ほぼ同点の別の分割、ノイズでも高い Q)
2. 2つの分割の比べ方 (Rand 指数、調整 Rand 指数 ARI、正規化相互情報量 NMI)
3. 確率的ブロックモデル (SBM)

| Marp の今のスライド | この案 |
| --- | --- |
| A ring of triangles / Q merges neighbors | S02 から S04 |
| Similar Q, different groups (2枚) | S05 |
| (なし。デッキを作り直したときに落ちた) | S06 から S07 (ノイズ)、S08 から S16 (NMI と ARI) |
| Turn it around から Finding the groups is inference まで (8枚) | S17 から S23 |

スライドの文字は英語にする。Marp デッキと同じで、手順書が前提にしている日本語ではない。
この文書の説明は日本語、`like this` の引用がスライド上の文字。

## 先に決めてほしいこと

1. **置き換えの範囲。** 上の表のとおりでよいか。Marp 側の「Turn it around」以降は、Remotion 版が
   できたあとで消す。
2. **順序。** 限界 → 比較 (Rand、ARI、NMI の順) → SBM。ノートは NMI を先に書いているが、
   組を数えるだけの Rand のほうが具体的なので先にした。限界の最後の「Q が同点でも分割は別」から
   「では2つの分割はどれだけ違うか」へ自然につながる。
3. **任意の3枚。** S06 から S07 (ノイズで Q が高い、2枚) と S15 (全員ひとりの分割、1枚) は
   入れなくても話は通る。外すと 23 枚 68 段階が 20 枚 59 段階になる。外すかどうか。
   S06 から S07 は、Marp の直前にある「Game: where Q goes wrong」の第 2 タブ (2024 年のゲーム。
   40 節点 41 辺の無作為ネットワークで、3 色で Q = 0.57、Louvain で 0.66) の解説と重なる。
   残す場合、ゲームの網そのものを使うか (数字を入れ替える)、クラブと同じ大きさ (34 節点 78 辺) で
   比べる今の案のままにするか。後者だと、ゲームの 0.57 と、ここの 0.35 が違う理由 (ゲームの網のほうが
   疎い) を一言添えることになる。

## スタイル (Marp デッキに合わせる)

Marp は 1280 x 720、Remotion は 1920 x 1080。サイズは Marp の値の 1.5 倍にする。

| 要素 | Marp | Remotion (1920 x 1080) |
| --- | --- | --- |
| 余白 | 上 40、左右 80、下 60 | 上 60、左右 120、下 90 |
| 見出し | 40px 太字、字間 -0.02em | 60px |
| 見出しの下の線 | 2px `#dddddd` | 3px、y = 154 |
| 本文 | 30px | 45px |
| 灰色の注 | 27px `#6b6b6b` | 40px |
| 図のラベル | Caveat 30px | Caveat 45px |
| 式のパネル | `#f7f4f1` | `#f7f4f1`、余白 33 / 42 |
| 節点の円 | 直径 26 から 52px | 直径 39 から 78px |
| ページ番号 | 16px `#b3b3b3` 右下 | 24px、右 120、下 36 |
| 章の扉 | 青い帯 `#3959A6`、見出し 67px | 見出し 100px |

- 背景は白 (`#ffffff`)、文字は黒。手順書の `theme.ts` (クリーム色の紙) は使わない。
- 色: 青 `#3959A6` は構造 (線、帯、リストの印)、赤 `#B14434` は強調 (用語、「高いほう」)、
  金 `#DAB167` は塗りと輪だけ (高い確率、重なり)、灰 `#6b6b6b` は注。群の色は青、金、赤、灰の順。
  5 色目が要る図 (S07) だけ紫 `#593196` (ノートのアニメ部品の色)。**緑は使わない。棒グラフは使わない。**
- 書体: 本文は Libre Baskerville (見出しは太字)、手書きの注は Caveat。式は KaTeX。
  フォントは Marp と同じく Google Fonts から読む。教室がオフラインならファイルを同梱する (実装時に決める)。
- 見出しは `Frame` から kicker を外し、見出し 1 行と線だけにする。フッターは右のページ番号だけ。
- 声: 言葉は少なく、1 枚に絵は 1 つ。「Let's ...」「We ...」。直接的で簡潔な英語、修辞なし。
  **em ダッシュは使わない。**
- 太字は用語だけ (赤になる)。強調のための太字は使わない。
- **問いのスライドには答えを一切置かない。** 答えは次のスライド。
- 10 個以上の群を色で塗り分けない。群は帯 (影) で囲む。2 つの分け方は帯の形で区別する (S02 から S04)。
- 動く時計 `useIdle()` は使わない。止まっている間に動くものはない。乱数は固定シード。

## 設計表

「段階」は手順書のとおり。段階 0 はスライドを開くと自動で再生される。標準の長さは 45 フレーム
(30 fps で 1.5 秒)、全組を順に処理する場面だけ 60 フレーム。段階の終わりまでに動きを終え、
最後の段階は完成した絵にする (戻ったときにその絵が出る)。

### 1. Limits of modularity

| スライド | 段階 | 見せるもの | 段階の終わりに残る絵 |
| --- | --- | --- | --- |
| S01 `Limits of modularity` (扉) | 0 | 青い帯、見出し、`Q is only a score. Let's see where it misleads us.` | 扉 |
| S02 `A ring of triangles` | 0 | 4 つの三角形が 1 つずつ現れ、隣どうしが 1 本の辺でつながって輪になる | 灰色の節点の輪 (n = 4) |
| | 1 | 三角形ごとに帯がかかる。札 `Q = 0.500` | + 4 つの帯、札 |
| | 2 | 右に同じ輪が現れ、隣 2 つずつを 1 本の帯で囲む。札 `Q = 0.375`。左の 0.500 が赤。字幕 `Each triangle alone has the higher Q.` | 左 0.500 (赤)、右 0.375 |
| S03 `Add triangles to the ring` (問い) | 0 | 三角形が 1 つずつ割り込み、輪が n = 4 から n = 10 へ広がる。数字 `n = 4 ... 10` | n = 10 の輪 (帯なし) |
| | 1 | 輪の下に 2 つの分け方の見本 (三角形ごと / 2 つずつ) が小さく並ぶ。問い `Which grouping has the higher Q now?` | 輪 + 見本 2 つ + 問い。Q の値はどこにも出さない |
| S04 `Q merges neighbors: the resolution limit` | 0 | n = 10 の輪を 2 通りの帯で左右に並べる。`Q = 0.650` と `Q = 0.675`。高い右が赤 | 輪 2 つ + 値 |
| | 1 | 隣り合う 2 つの三角形だけを拡大。間の辺に `observed: 1 edge`。その下に `expected by chance: 8 x 8 / 2m = 64 / 80 = 0.8 edges` (8 は三角形の次数の和)。`1 > 0.8: merging raises Q` | 拡大図 + 観測と期待 |
| | 2 | n を 4, 6, ..., 16 と動かす。輪が描き直され、期待値の数字が 2.0 から 0.5 へ減る。右の折れ線 (`3/4 - 1/n` と `7/8 - 2/n`) の上を点が動く。n = 8 の交点で帯が「三角形ごと」から「2 つずつ」に切り替わる | n = 16 の輪 (2 つずつ) + 折れ線 (点は n = 16) |
| | 3 | 交点に `n = 8 = sqrt(2m)`。字幕 `The two triangles did not change. The rest of the network got bigger.` と `Q depends on the size of the whole network: the resolution limit.` (resolution limit は太字) | 折れ線 + 交点の注 + 字幕 2 行 |
| S05 `Similar Q, different groups` | 0 | カラテクラブ (34 人、78 本) を 4 グループで塗る。字幕 `Q = 0.407: four groups` | クラブ (4 色) |
| | 1 | 色が 3 グループに変わる。灰が赤に合流し、1 人が青へ移る (変わった節点に一瞬輪)。字幕 `Q = 0.402: three groups` | クラブ (3 色) |
| | 2 | クラブが消え、Q の数直線 (0.38 から 0.42) に 16 個の点が並ぶ (Louvain を種を変えて 400 回走らせた結果の 16 通り)。字幕 `Louvain, 400 seeds: 16 different splits, Q from 0.385 to 0.420.` と `Q cannot tell us which split is right.` | 数直線 + 16 点 + 字幕 |
| S06 `A network with no groups` (問い、任意) | 0 | 34 節点、78 辺の無作為ネットワーク。辺が 1 本ずつ現れる。灰色の節点。字幕 `34 nodes, 78 edges, chosen at random.` | 灰色のネットワーク |
| | 1 | 問い `We run Louvain on this network. What Q do we expect?` | + 問い。答えは出さない |
| S07 `Q finds groups in noise` (任意) | 0 | Louvain が走る。節点の色が数回に分けて塗り替わり、5 グループになる。札 `Q = 0.346` | 5 色のネットワーク + 札 |
| | 1 | 右に Q の数直線 (0.30 から 0.42)。同じ大きさの無作為ネットワーク 200 個の結果が点で並ぶ。0.3 に縦線 `rule of thumb: Q > 0.3`。200 点すべてが線の右 | 数直線 + 200 点 |
| | 2 | クラブの 0.420 が赤い縦線で入る。点群の右外に出る。字幕 `Every random network passes the 0.3 rule. We compare Q with random networks of the same size.` | + 赤い線 |
| | 3 | 2 段目の数直線に、節点 100 個 (平均次数 約 5) の無作為ネットワーク 100 個の点。平均 0.417 で、赤い線がこの点群の中を通る。字幕 `A random network with 100 nodes scores as high as the club.` | 2 段の数直線 + 赤い線が両方を貫く |

### 2. Comparing two splits

| スライド | 段階 | 見せるもの | 段階の終わりに残る絵 |
| --- | --- | --- | --- |
| S08 `Comparing two splits` (扉) | 0 | 帯、見出し、`Let's compare two splits with a number.` | 扉 |
| S09 `Two splits of eight nodes` | 0 | 8 節点が横一列に現れる。節点 1 から 4 が青、5 から 8 が赤。字幕 `true groups` | 色つきの 8 節点 |
| | 1 | 下の段に同じ 8 節点と、枠が 2 つ (A = 節点 1 から 5、B = 節点 6 から 8)。字幕 `found groups`。A に入った赤の節点 5 に輪 | 上: 真の色、下: 枠、5 番に輪 |
| | 2 | 節点が 1 つずつ、(真の色 x 枠) の 2 x 2 の升に飛び込む。升の数: 青 A = 4、青 B = 0、赤 A = 1、赤 B = 3 | 節点列 (縮小) + 升目 |
| S10 `Rand index: count the pairs` | 0 | 上下 2 段の絵はそのまま。`8 nodes make 28 pairs` | + 数字 |
| | 1 | 節点 1 と 2 の組。両方の段で 2 点を線で結ぶ。どちらでも同じ群なので `agree` (青のチェック) | 1 組が agree |
| | 2 | 節点 4 と 5 の組。真では別の群、found では同じ枠なので `disagree` (赤の x) | 1 組が disagree |
| | 3 | 28 組が全部、4 つの山に分かれて入る: 両方で同じ 9、真だけ同じ 3、found だけ同じ 4、両方で別 12。`agree` は 9 + 12 | 2 x 2 の山 + 数 |
| | 4 | `Rand index = agreeing pairs / all pairs = 21 / 28 = 0.75` | 山 + 分数 |
| S11 `Shuffle the labels` (問い) | 0 | 30 個の点が 5 色 (各 6 個) にまとまる。字幕 `true groups: 5 groups of 6` | 5 色の点 |
| | 1 | 点の色が一度シャッフルされ、別の色分けが下の段に現れる (`random labels`、群の大きさは同じ)。問い `What Rand index do we expect for random labels?` | 上下 2 段 + 問い。答えは出さない |
| S12 `Adjusted Rand index` | 0 | シャッフルが 40 回、速く繰り返され、毎回の Rand 指数が数直線 (0 から 1) に点で積もる。点群は 0.71 付近。字幕 `Random labels score about 0.71.` | 数直線 + 40 点 |
| | 1 | 理由。`360 of 435 pairs are apart in the true split. A random split also puts most pairs apart, so they agree.` | + 字幕 |
| | 2 | 式 `ARI = (Rand - expected Rand) / (1 - expected Rand)`、`expected Rand = 0.715`。目盛りが Rand から ARI に切り替わり、点群が 0 のまわりへ、1 は右端。字幕 `0: no better than chance. 1: identical.` | ARI の数直線 + 式 |
| | 3 | 8 節点の例に戻る: `Rand 0.75, expected 0.51, ARI 0.49` | 数字 3 つ |
| S13 `Mutual information: questions saved` | 0 | 8 節点を灰色にして 1 つを光らせる。「真の群は青か赤か」。同数の 2 群なので 1 回の yes/no。`entropy: the average number of yes/no questions to name the group`。`H(true) = 1.000` | 光った節点 + 定義 + 1.000 |
| | 1 | 光った節点の found の枠を明かす。A なら青 4・赤 1 でまだ迷う (平均 0.722 回)。B なら全員赤で 0 回。`H(true given found) = 5/8 x 0.722 + 3/8 x 0 = 0.451` | 2 つの場合 + 式 |
| | 2 | `mutual information I = 1.000 - 0.451 = 0.549`。字幕 `questions saved by the found groups` | + I |
| S14 `Normalized mutual information` | 0 | 円が 2 つ離れて現れる。面積が各エントロピー: 真 1.000、found 0.954 | 円 2 つ |
| | 1 | 円が重なる。重なりの面積が `I = 0.549` (金)。真の円の重ならない部分が `H(true given found) = 0.451` | 重なった円 |
| | 2 | `NMI = 2I / (H(true) + H(found)) = 2 x 0.549 / (1.000 + 0.954) = 0.562`。重なりを両方の円から数えて、2 つの円の面積の和で割る | + 式 |
| | 3 | 両端を並べる: 同じ分け方は円が一致して `NMI = 1`、無関係な分け方は円が離れて `NMI = 0`。真ん中がこの例の 0.562 | 3 つの状態 |
| S15 `Many tiny groups` (任意) | 0 | found を「全員ひとり」(8 個の枠) にする。真の 2 色はそのまま | 8 個の枠 |
| | 1 | `Rand 0.57, NMI 0.50, ARI 0.00`。字幕 `This split says nothing about the groups.` | + 数字 3 つ |
| | 2 | S12 のシャッフル (30 点、5 群) に戻る: ランダムな色分けの平均 `NMI 0.215, ARI about 0`。字幕 `NMI is not zero for random labels. We report ARI with NMI.` | + 字幕 |
| S16 `Which split is closer to the real one?` | 0 | カラテクラブを実際の分裂 (17 人と 17 人、青と赤) で塗る。字幕 `the real split: 17 and 17` | クラブ (2 色) |
| | 1 | 色が 4 グループの分け方 (Q = 0.407) に変わる。右に升目 (行: 実際の青と赤、列: 見つけた 4 群): 青 [11, 5, 1, 0]、赤 [0, 0, 9, 8]。その下に `NMI 0.586, ARI 0.450` | クラブ (4 色) + 升目 + 数字 |
| | 2 | 色が 3 グループの分け方 (Q = 0.402) に変わる。升目: 青 [11, 5, 1]、赤 [1, 0, 16]。`NMI 0.568, ARI 0.591`。4 群の行は小さく残る | クラブ (3 色) + 2 行 |
| | 3 | 2 行を比べる。NMI は 4 群が高く (0.586 > 0.568)、ARI は 3 群が高い (0.591 > 0.450)。高いほうを赤。字幕 `NMI and ARI can disagree. We report both.` | 2 行 + 赤 |
| | 4 | S05 の問いに答える行が加わる: `four groups vs three groups: NMI 0.768, ARI 0.626` | 3 行 |

### 3. Turn it around (SBM)

8 節点 (青 4、赤 4、28 組) で通す。確率は群内 0.9 と群間 0.1。組ごとに乱数 u を 1 つ固定し、
`u < p` なら辺が出る。そのため確率を変えると辺が足されるか消えるかだけで、別の網に入れ替わらない。

| スライド | 段階 | 見せるもの | 段階の終わりに残る絵 |
| --- | --- | --- | --- |
| S17 `Turn it around` (扉) | 0 | 帯、見出し、`Let's build a network from the groups` | 扉 |
| S18 `Groups first, then edges` | 0 | 8 節点が 2 群 (青 4、赤 4) で現れる。辺はない | 2 群の節点 |
| | 1 | 右に 2 x 2 の確率表: 青青 0.9、赤赤 0.9、青赤 0.1 (高い升は金)。式 `p_{c_i c_j}`、字幕 `one probability for each pair of groups` | + 確率表 |
| | 2 | 節点 1 と 2 (どちらも青) を選ぶ。升は 0.9。乱数 `u = 0.72` を引く。`u < 0.9` なので辺が引かれる | 辺が 1 本 |
| | 3 | 節点 1 と 6 (青と赤) を選ぶ。升は 0.1。`u = 0.59`。`u >= 0.1` なので辺は引かれない | 辺は 1 本のまま、1-6 に x |
| | 4 | 残りの組が順に処理され、ネットワークができる (12 辺。群内 11、群間 1) | 完成したネットワーク |
| S19 `Can we see the groups?` (問い) | 0 | 同じネットワークを色なしで円形に置く (左)。右に隣接行列 (8 x 8、辺は塗り)、行と列は乱れた順。問い `Where are the two groups?` | 灰色の網 + 乱れた行列 |
| S20 `Sort by group, and blocks appear` | 0 | S19 と同じ絵 | 乱れた行列 |
| | 1 | 行と列が同時に群の順へ滑って並び替わる。対角に 4 x 4 の濃いブロックが 2 つ現れる | 並び替えた行列 |
| | 2 | ブロックに赤い枠。左の節点が群の色に塗られる。字幕 `Nothing changed but the order.` | 行列 + 枠 + 色つきの網 |
| S21 `What if edges between groups are more likely?` (問い) | 0 | 確率表が入れ替わる (青青 0.1、赤赤 0.1、青赤 0.9)。節点は 2 群で辺はない。問い `What does the network look like?` | 確率表 + 辺のない節点 |
| S22 `Groups can also connect outward` | 0 | 群内が高い (0.9 / 0.1) の確率表と網 (12 辺、群内 11)。字幕 `Q of the true groups: 0.413` | 表 + 網 |
| | 1 | ダイヤルが 0.1 / 0.9 へ回る。表の色が入れ替わり、群内の辺が消えて群間の辺が現れる (15 辺、群内 1)。字幕 `Q of the true groups: -0.436` | 表 + 網 |
| | 2 | ダイヤルが 0.45 / 0.45 へ。表が一色になる (12 辺、群内 6)。字幕 `no difference: a random network. Q of the true groups: 0.000` | 表 + 網 |
| | 3 | 3 つの状態が横に 3 枚並ぶ (各: 確率表 + 網)。字幕 `One model: a table of probabilities. Members of a group connect to the rest in the same way. They need not connect to each other.` | 3 枚 |
| S23 `Finding the groups is inference` | 0 | 左に観測されたネットワーク (色なし、12 辺)。1 つ目の推測 (奇数番と偶数番の縞) で節点が塗られ、2 x 2 の升に `edges / pairs` が入る。各升の確率はその割り算 | 網 + 推測 + 升 |
| | 1 | その推測のもとで、この網がそのまま生まれる確率の対数 (`score`) を数直線 (-20 から -5) に点で置く: -17.5。`score: the log of the probability of this exact network (higher is better)` | 数直線 + 点 1 つ |
| | 2 | 推測を 3 つ足す: 1 人だけ動かした -15.5、2 人動かした -18.4、全員 1 群 -19.1 | 点 4 つ |
| | 3 | 真の分け方 (青 4、赤 4)。升は 5/6、6/6、1/16 で、score は -6.4 と最高。赤い点。字幕 `We choose the grouping with the highest score.` | 点 5 つ、最高が赤 |

## 検算した数字

`scripts/verify_numbers.py` が、この文書の数字をすべて計算し直して assert する
(`uv run slides/m05/remotion/scripts/verify_numbers.py`、全部通った)。実装では、同じ値を出す
データ生成スクリプトを書き、図の数字はそこから読む。

- **リング** (n 個の三角形、辺 4n 本): 三角形ごとの Q = 3/4 - 1/n、2 つずつの Q = 7/8 - 2/n。
  n = 4 で 0.500 と 0.375、n = 10 で 0.650 と 0.675、n = 8 で同点 (0.625)。三角形の次数の和は 8。
  隣の三角形の間の期待辺数は 8 x 8 / 2m = 8/n。2 つずつにするので n は偶数だけ動かす。
- **8 節点の例** (真: 1 から 4 と 5 から 8、found: 1 から 5 と 6 から 8): 組 28。両方で同じ 9、
  真だけ同じ 3、found だけ同じ 4、両方で別 12。Rand 21/28 = 0.75。偶然の期待値 0.505。ARI 0.495。
  H(true) 1.000、H(found) 0.954、I 0.549、H(true given found) 0.451、NMI 0.562。
  全員ひとりの found: Rand 0.571、NMI 0.500、ARI 0.000。
- **30 点のシャッフル** (5 群 x 6、種 0、2000 回): Rand の平均 0.714、期待値 (式) 0.7146、
  ARI の平均 -0.001、NMI の平均 0.215。真で別の群の組は 435 組中 360。
- **カラテクラブ**: **重みなしの辺 78 本で計算する。** `nx.karate_club_graph()` は辺に重みを持ち、
  `nx.community.modularity()` は既定でそれを使うので、そのままだと 0.434 / 0.432 / 0.445 になる。
  デッキの 0.407 / 0.402 / 0.420 は重みなしの値。実際の分裂の Q は 0.358。4 群は NMI 0.586、ARI 0.450。
  3 群は NMI 0.568、ARI 0.591。4 群と 3 群どうしは NMI 0.768、ARI 0.626。
  Louvain 400 回で 16 通り、Q は 0.385 から 0.420 (networkx 3.7)。
  `plan.md` の 0.4439 と 0.3914 は重み付きの値なので使わない。
- **ノイズ**: 34 節点 78 辺の無作為ネットワーク 200 個で Louvain の Q は平均 0.354 (0.305 から 0.402)、
  全部 0.3 より上で、クラブの 0.420 より下。種 0 は 5 群で Q = 0.346。100 節点 (確率 0.05) 100 個は
  平均 0.417 (0.362 から 0.471) で、クラブの 0.420 はこの範囲の中。ゲームと同じ大きさの 40 節点 41 辺
  (平均次数 2.05) は 200 個で平均 0.592 (0.465 から 0.681)。疎い網ほど Q は高くなる。
- **SBM** (8 節点、固定乱数の種 901): 辺は 12 本 (群内 11)、15 本 (群内 1)、12 本 (群内 6)。
  真の分け方の Q は 0.413、-0.436、0.000。確率 0.9 / 0.1 の網の升は 5/6、6/6、1/16。
  対数尤度は真 -6.4、1 人動かす -15.5、縞 -17.5、2 人動かす -18.4、全員 1 群 -19.1。
  `u` は節点 1 と 2 が 0.72、節点 1 と 6 が 0.59。

## 話すときの注 (スライドには出さない)

- S04: Fortunato と Barthelemy (2007)。しきい値は √(2m) で、群の運命が、その群ではなく網全体の辺数 m で決まる。
- S07: 「Q > 0.3 を意味のある構造の目安とする」は講義ノートの記述と同じ。
- S16: 実際の分裂の Q は 0.358 で、上の 2 つの分け方 (0.407、0.402) より低い。Q を最大にしても
  実際に起きたことには戻らない。属性は必ずしも正解ではない (Peel, Larremore, Clauset 2017)。
- S23: 最良の分け方を探すのは Q を最大にするのと同じくらい難しく、実際の手法も発見的。
  尤度なら群の数も比べられる。式の詳細は講義ノートと付録。

## 承認後の実装の順序

1. `~/Downloads/fourier-slides` を `slides/m05/remotion/` に展開 (`node_modules` と `dist` はコミットしない)。
   `package.json` の name と `index.html` の title を直す。
2. `theme.ts` と `Frame.tsx` を上のスタイルに変える。`Slide1.tsx` から `Slide7.tsx` と `index.ts` の配列を消す。
3. データ生成スクリプト (Python) が `src/data/*.ts` を書く。そこで上の数字を assert する。
4. 最初に **S04** を作る (輪、折れ線、期待値の数字を持つ最も重い 1 枚)。手順書 9 の確認を丁寧に行い、
   スタイルが Marp に合っているかをここで決める。
5. 残りを表の順に作る。節ごとに `npm run build` を通し、`npm run review` の静止画でレビューを回す。

## 確認できたこと、できていないこと

- 確認できた: 上の数字 (すべて `verify_numbers.py` で assert)。Marp デッキの該当スライドの文面と
  数字との整合。
- 確認できていない: 見た目と動き (まだ何も作っていない)。Remotion の土台の動作確認。
  節点の円の大きさや文字の大きさが Marp の基準 (図の円 26 から 52px) を満たすか。
  S16 のカラテクラブ 1 つに升目を並べたときの収まり。S04 の折れ線と輪が 1 枚に収まるか。

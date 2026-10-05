# m05 Remotion スライド案 (DECK_SPEC)

2026-10-05。設計表。

**改訂 (同日、講師の指摘のあと)**: 41 枚 (最初の案は 23 枚)。

- Rand 指数は、ノードの組を **行列のセル** で見せる (S09, S10)。ノード 2 つを線で結ぶ絵は、ネットワークの辺に見えるので使わない。
  2 つの分け方を並べ、見つけた分け方の段を 90 度回して行列の左辺にする (S09)。Rand 指数は、2 つの行列が同じ答えのセルにチェック、違う答えのセルに ×
  をつけた行列で数える (S10。違う色の組も、両方で別々なら「一致」として数える)。そのあと ARI (S12) に進み、「組でなくノードでもよいのでは」(S13) から
  ノードの分割表、対角を数えられない理由 (ラベルは任意の名前で順序もない、S14)、NMI (S15 から S19) の順に進む。
- 相互情報量は、質問の数 (エントロピー) ではなく **確率の式** で説明する (S15 から S19)。
  同時確率を分子に、周辺確率どうしの積を分母にした比で決まる。
- **群の色は、青、オレンジ、茶色、紫、濃い灰色。赤は文字だけ。** ストライプ (茶色) は、帯と円の重なりにだけ使う。
- 乱数 u は見せない (S23)。確率は 10 枚のくじで説明する。
- 最後に、SBM の推定を数式で積み上げる (S29 から S31。p_rs は与えず、一般の形の尤度から対数尤度、最大化、c を固定して p を求め、c だけの式に戻す)、
  尤度が K とともに増えること (S32)、次数補正つき SBM (S33 から S38)、Peixoto のベイズ流 SBM (S39)、graph-tool (S40)、オチの空手クラブ (S41) を足した。
- **次数補正つき SBM (Karrer and Newman, Phys. Rev. E 83, 016107, 2011; arXiv:1008.3926)** は、ベイズ流 SBM の前に置く。政治ブログの図 (論文の Fig. 2、
  講師が取り込んだ画像を `public/` に 2 枚に切って置いた) で動機づけ (S33)、次数と群は別の量だという説明 (S34)、モデル (S35)、
  c を固定して θ と ω を決める (S36)、戻して c だけの式にして最大化 (S37)、最後にもう一度ブログ (S38)。式の記号と因子は論文の本文で確かめた (下の「検算した数字」)。
- 字幕は 1 段階に短いもの 1 つまで。数える単位 (ノードの組か、ノード 1 つか) を明示する。
- **見出しは付けない** (扉の S01, S08, S22 を除く)。内容に必要な語は本文に入れた (S06 `no groups`、S18 `mutual information`、
  S19 `normalized mutual information`、S39 `Bayesian SBM`、S40 `graph-tool`)。見出しがない分、内容を上へ寄せて拡大し (既定は 1.08 倍)、
  **下の 160 px (y = 920 から) は後で付ける字幕のために空ける**。`Frame` の `zoom` と `top` で調整し、
  `npm run review` のあと `python3 scripts/check_bottom.py` で、どの段階の静止画も y = 920 より下に絵がないことと、
  端 40 px に絵がかかっていないことを確かめる (今は全 120 枚で最下部は y = 918)。

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
| (なし。デッキを作り直したときに落ちた) | S06 から S07 (ノイズ)、S08 から S21 (Rand、ARI、NMI) |
| Turn it around から Finding the groups is inference まで (8枚) | S22 から S28。そのあとに S29 から S41 を追加 |

スライドの文字は英語にする。Marp デッキと同じで、手順書が前提にしている日本語ではない。
この文書の説明は日本語、`like this` の引用がスライド上の文字。

## 先に決めてほしいこと

1. **置き換えの範囲。** 上の表のとおりでよいか。Marp 側の「Turn it around」以降は、Remotion 版が
   できたあとで消す。
2. **順序。** 限界 → 比較 (Rand、ARI、NMI の順) → SBM。ノートは NMI を先に書いているが、
   組を数えるだけの Rand のほうが具体的なので先にした。限界の最後の「Q が同点でも分割は別」から
   「では2つの分割はどれだけ違うか」へ自然につながる。
3. **任意の3枚。** S06 から S07 (ノイズで Q が高い、2枚) と S20 (全員ひとりの分割、1枚) は
   入れなくても話は通る。外すと 35 枚が 32 枚になる。外すかどうか。
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
- **色は、白、黒、青 `#3959A6` を基本にする。** 描くものの既定は青、小さな注は灰 `#6b6b6b`。
  **赤 `#B14434` は強調する文字だけ** (用語、「高いほう」、「disagree」)。塗りにも群にも線にも使わない。緑は使わない。棒グラフは使わない。
- **群 (コミュニティ) の塗り分けは色で行う**: 青 `#3959A6`、オレンジ `#E69F00`、茶色 `#8B5E34`、紫 `#6A3D9A`、
  濃い灰色 `#3a3a3a` の順。赤は使わない。群に属さないノードや不明のノード (`?`) は黒。
- **ストライプは茶色** で、群の塗り分けには使わない。群を囲む帯 (S02 から S04) と、NMI の円の重なり (S19) にだけ使う。
  群を囲む帯は、淡い青のべたか、淡い茶色のストライプ。プロット上で強調する点や線は黒、その名札は赤い文字。
- 書体: 本文は Libre Baskerville (見出しは太字)、手書きの注は Caveat。式は KaTeX。
  フォントは Marp と同じく Google Fonts から読む。教室がオフラインならファイルを同梱する (実装時に決める)。
- 見出しは `Frame` から kicker を外し、見出し 1 行と線だけにする。フッターは右のページ番号だけ。
- 声: 言葉は少なく、1 枚に絵は 1 つ。「Let's ...」「We ...」。直接的で簡潔な英語、修辞なし。
  **em ダッシュは使わない。**
- 太字は用語だけ (赤になる)。強調のための太字は使わない。
- **字幕は 1 段階に短いもの 1 つ** (8 語ほど、多くても 12 語)。同じ文を 2 か所に書かない。文より記号、数、絵。
- **単位を書く。** 群にするものは **ノード** (「node」と書く。dot や vertex や member とは書かない)。
  Rand 指数と ARI は **ノードの組** を数え、NMI は **ノード 1 つ** を見る。数える単位を、字幕と絵 (組は 2 つのノードを線で結ぶ、
  1 つは 1 つのノードを光らせる) の両方で示す。
- **問いのスライドには答えを一切置かない。** 答えは次のスライド。
- 10 個以上の群を塗り分けない。群は帯で囲む。2 つの分け方は帯の形と塗り (べた / ストライプ) で区別する (S02 から S04)。
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
| | 2 | クラブが消え、Q の数直線 (0.38 から 0.42) に 16 個の点が並ぶ (Louvain を種を変えて 400 回走らせた結果の 16 通り)。字幕 `400 Louvain runs, 16 different splits` と `Different splits, almost the same Q.` (Q は 0.385 から 0.420 で、軸で読める) | 数直線 + 16 点 + 字幕 |
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
| S09 `Two splits of eight nodes` | 0 | 8 ノードが横一列に現れる。ノード 1 から 4 が青、5 から 8 がオレンジ。字幕 `true groups` | 色つきの 8 ノード |
| | 1 | 下の段に同じ 8 ノードと、枠が 2 つ (A = ノード 1 から 5、B = ノード 6 から 8)。A に入ったオレンジのノード 5 に輪。字幕 `found groups` | 上: 真の色、下: 枠 |
| | 2 | 下の段 (見つけた分け方) が 90 度回って 8 x 8 の行列の左辺になり、上の段 (真の分け方) が上辺になる。`One cell is one pair of nodes.` | 空の 8 x 8 行列 |
| S10 `Rand index` | 0 | 行列 1: 真の分け方で、同じ色の 2 ノードのセルを塗る (対角も塗る)。`true` | 真の行列 |
| | 1 | 行列 2: 見つけた分け方で、同じ箱のセルを塗る。`found` | 行列 2 つ |
| | 2 | 右に 3 つ目の行列 `agree?`: 2 つの行列が同じ答えのセル (どちらも塗られている、またはどちらも白) に青のチェック、違う答えのセル (片方だけ塗られている) に黒の ×。先にチェックが、そのあと × が出る。対角 (ノード自身) は灰色のチェックで数えない。`Agree: 21 pairs. Disagree: 7 pairs.` | 行列 3 つ (右はチェックと ×) |
| | 3 | `Rand index = agreeing pairs of nodes / all pairs of nodes = 21 / 28 = 0.75` (21 = 両方で一緒の 9 組 + 両方で別々の 12 組。組は対角と下三角を除いた 28 組) | 式 |
| S11 `Shuffle the labels` (問い) | 0 | 30 ノードが 5 群 (各 6) にまとまる。字幕 `true groups` | 5 色のノード |
| | 1 | ノードの色が一度シャッフルされ、別の色分けが下の段に現れる。問い `What Rand index do we expect for random labels?` | 上下 2 段 + 問い。答えは出さない |
| S12 `Adjusted Rand index` | 0 | シャッフルが 40 回、速く繰り返され、毎回の Rand 指数が数直線に点で積もる。`Random labels: about 0.71` | 数直線 + 40 点 |
| | 1 | `ARI = (Rand - expected Rand) / (1 - expected Rand)`、`expected Rand = 0.715`。目盛りが ARI に切り替わり、点群が 0 のまわりへ。`0 = chance, 1 = identical` | ARI の数直線 + 式 |
| | 2 | 8 ノードの例に戻る: `Rand 0.75, expected 0.51, ARI 0.49` | 数字 3 つ |
| S13 `Nodes or pairs?` | 0 | S12 の最後の絵 (上: 真の色の 8 ノード、下: 見つけた箱 A と B の中の 8 ノード) からそのまま始まり、`Rand 0.75 / expected 0.51 / ARI 0.49` の札が消える。箱に A, B の名前。ノード 3 に輪。`Why not count nodes, one at a time?` ("NMI" の語は出さない) | 2 段の 8 ノード |
| | 1 | 上の段が消え、下の段 (箱ごと) が下がって、上に 2 x 2 の表が出る。下の段のノード (色 = 真の群、箱 = 見つけた群) が 1 つずつ表の升 (色, 箱) へ飛び込んで積もる (青 A に 1 から 4、オレンジ A に 5、オレンジ B に 6 から 8、青 B には 0)。空になった箱は消える。積もったノードが数 4, 0, 1, 3 に替わる。`Count the nodes in each cell.` 表は S14 の始まりと同じ大きさと位置で終わる | ノード数の表 |
| S14 `Can we count the diagonal?` | 0 | S13 の表がそのまま (開いた時からある) 出ていて、A を青に、B をオレンジに対応させると対角が色づく。4 + 3 = 7 of 8 nodes | 升目 + 対角 |
| | 1 | 列の並びだけ入れ替える (B, A)。対角は 0 + 1 = 1 of 8 nodes。`same split, columns in another order` | 入れ替えた升目 |
| | 2 | 見つけた群が 3 つ (2 x 3 の表)。`3 found groups, 2 true groups`、`no diagonal to count` | 2 x 3 の表 |
| | 3 | `We need a score that ignores the names and the order.` (次の NMI へつなぐ) | 同上 + 1 行 |
| S15 `Joint probability` | 0 | 表 (行: 真の群、列: 見つけた群) に、セルごとのノード数 4, 0, 1, 3。`Count the nodes in each cell.` | ノード数の表 |
| | 1 | 8 で割る。0.5, 0, 0.125, 0.375。`Divide by 8: joint probability` | 同時確率の表 |
| S16 `Marginal probability` | 0 | 行を足す: 右の余白に 0.5, 0.5。`Add up each row: marginal probability` | + 行の和 |
| | 1 | 列を足す: 下の余白に 0.625, 0.375。`Add up each column: marginal probability` | + 列の和 |
| S17 `Joint against marginals` | 0 | 余白の周辺確率を残し、セルに 2 つの周辺確率の積 (0.3125, 0.1875, ...)。`Unrelated splits: joint = marginal x marginal` | 積の表 |
| | 1 | セルが比 `joint / (marginal x marginal)` に変わる: 1.6, 0, 0.4, 2。1 より大きいセルを囲む。`above 1: more often than chance. below 1: less often.` | 比の表 |
| S18 `Mutual information` | 0 | セルに比。式 `I = sum p(t, f) log2 [ p(t, f) / (p(t) p(f)) ]` | 比の表 + 式 |
| | 1 | セルが、同時確率 x 比の対数に変わる: 0.339, 0, -0.165, 0.375 | 各セルの寄与 |
| | 2 | `I = 0.339 + 0 - 0.165 + 0.375 = 0.549`。`unrelated splits: every ratio is 1, log 1 = 0, so I = 0` | 和 |
| S19 `Normalized mutual information` | 0 | 円が 2 つ離れて現れる。面積が H (その分け方の、自分自身との相互情報量): 真 1.000、found 0.954 | 円 2 つ |
| | 1 | 円が重なる。重なりの面積が `I = 0.549` (茶色のストライプ) | 重なった円 |
| | 2 | `NMI = 2I / (H(true) + H(found)) = 2 x 0.549 / (1.000 + 0.954) = 0.562` | + 式 |
| | 3 | 両端を並べる: 同じ分け方は `NMI = 1`、無関係な分け方は `NMI = 0`、真ん中がこの例の 0.562 | 3 つの状態 |
| S20 `Many tiny groups` (任意) | 0 | found を「全員ひとり」にする | 8 個の枠 |
| | 1 | `Rand 0.57, NMI 0.50, ARI 0.00`。字幕 `This split says nothing about the groups.` | + 数字 3 つ |
| | 2 | S11 のシャッフル (30 ノード、5 群): `average NMI 0.215, average ARI about 0`。`NMI is not zero for random labels.` | + 字幕 |
| S21 `Which split is closer to the real one?` | 0 | カラテクラブを実際の分裂 (17 人と 17 人) で塗る。左のスロット。`the real split` と凡例 | クラブ 1 つ |
| | 1 | 中央に 4 グループの分け方 (Q = 0.407) が並ぶ。下に `NMI 0.586`、`ARI 0.450` | クラブ 2 つ |
| | 2 | 右に 3 グループの分け方 (Q = 0.402)。下に `NMI 0.568`、`ARI 0.591` | クラブ 3 つ |
| | 3 | NMI は 4 群が高く (0.586 > 0.568)、ARI は 3 群が高い (0.591 > 0.450)。高いほうを赤い文字に。`NMI and ARI can disagree` | 3 つ + 赤 |
| | 4 | `four vs three groups: NMI 0.768, ARI 0.626` | + 1 行 |

### 3. Turn it around (SBM)

8 ノード (青 4、オレンジ 4、28 組) で通す。確率は群内 0.9 と群間 0.1。組ごとに乱数を 1 つ固定し、
その乱数が確率より小さければ辺が出る (スライドには出さない)。確率を変えても、辺が足されるか消えるかだけで、別の網に入れ替わらない。

| スライド | 段階 | 見せるもの | 段階の終わりに残る絵 |
| --- | --- | --- | --- |
| S22 `Turn it around` (扉) | 0 | 帯、見出し、`Let's build a network from the groups` | 扉 |
| S23 `Groups first, then edges` | 0 | 8 ノードが 2 群で現れる。辺はない | 2 群のノード |
| | 1 | 右に 2 x 2 の確率表 (青青 0.9、オレンジオレンジ 0.9、青オレンジ 0.1)。`Nodes i and j connect with probability p_{c_i c_j}`、`one probability per block` | + 確率表 |
| | 2 | ノード 1 と 2 (どちらも青)。升は 0.9。10 枚のくじのうち 9 枚が青 (edge)。1 枚引く。`9 of 10 tickets say edge`、`Draw one ticket: edge`。辺が引かれる | 辺が 1 本 |
| | 3 | ノード 1 と 6。升は 0.1。10 枚のうち 1 枚だけが青。引いた 1 枚は白。`Draw one ticket: no edge` | 辺は 1 本のまま、1-6 に x |
| | 4 | 残りの組が順に処理され、ネットワークができる。`12 edges` | 完成した網 |
| S24 `Can we see the groups?` (問い) | 0 | 同じ網を色なしで円形に置く (左)。右に隣接行列 (8 x 8)、行と列は乱れた順。問い `Where are the two groups?` | 網 + 乱れた行列 |
| S25 `Sort by group, and blocks appear` | 0 | S24 と同じ絵 | 乱れた行列 |
| | 1 | 行と列が 1 ノードずつ群の順へ並び替わる。対角に 4 x 4 の濃いブロックが 2 つ現れる | 並び替えた行列 |
| | 2 | ブロックに黒い枠。左のノードが群の色に塗られる。`Nothing changed but the order.` | 行列 + 枠 |
| S26 `What if edges between groups are more likely?` (問い) | 0 | 確率表が入れ替わる (群内 0.1、群間 0.9)。辺のない節点。問い `What does the network look like?` | 確率表 + 辺のないノード |
| S27 `Groups can also connect outward` | 0 | 群内が高い (0.9 / 0.1) の確率表と網 (12 辺、群内 11)。`Q of the true groups: 0.413` | 表 + 網 |
| | 1 | ダイヤルが 0.1 / 0.9 へ。群内の辺が消え、群間の辺が現れる (15 辺、群内 1)。`Q of the true groups: -0.436` | 表 + 網 |
| | 2 | ダイヤルが 0.45 / 0.45 へ (12 辺、群内 6)。`A random network. Q of the true groups: 0.000` | 表 + 網 |
| | 3 | 3 つの状態が横に並ぶ。`One model: a table of probabilities.` | 3 枚 |
| S28 `Finding the groups is inference` | 0 | 観測されたネットワーク (色なし) に 1 つ目の推測 (奇数番と偶数番)。2 x 2 の升に `edges / pairs of nodes` | 網 + 推測 + 升 |
| | 1 | その推測のもとで、この網がそのまま生まれる確率の対数 (`score`) を数直線に置く: -17.5 | 点 1 つ |
| | 2 | 推測を 3 つ足す: 1 ノード動かした -15.5、他 2 つ、全員 1 群 -19.1 | 点 4 つ |
| | 3 | 真の分け方 (5/6、6/6、1/16): -6.4 で最高。黒い点、赤い文字 | 点 5 つ |
| S29 `The likelihood of a network` | 0 | 左の列に記号の定義 (`A_ij`、`c_i`、`p_rs`)。右に `L(c, p) = P(A given c, p)`。**p_rs の値は与えない** | 定義 + L の定義 |
| | 1 | 1 組のノード (i, j): 辺があれば確率 p_{c_i c_j}、なければ 1 - p_{c_i c_j} (場合分けの式) | + 場合分け |
| | 2 | 1 つの式にまとめる: `p^{A_ij} (1 - p)^{1 - A_ij}`。この式の `=` は、1 つ上の式の `=` の真下に揃える (TeX の `\phantom` で左辺と同じ幅をあける) | + べき乗の式 |
| | 3 | すべての組の積: `L(c, p) = product over i < j of p^{A_ij} (1 - p)^{1 - A_ij}` (尤度) | + 積 |
| | 4 | ブロック (r, s) ごとにまとめる: `L(c, p) = product over r <= s of p_rs^{m_rs} (1 - p_rs)^{n_rs - m_rs}`。左の列に m_rs と n_rs の定義が加わる | + ブロックの式 |
| | 5 | 対数をとる: `log L(c, p) = sum over r <= s of [m_rs log p_rs + (n_rs - m_rs) log(1 - p_rs)]` (2 行に分ける) | + 対数尤度。式はどれも消さず、最後まで残す。**一番新しい式を大きく (50px)、古い式を少し小さく (40px)** 。印の青い縦線は付けない (S30, S31 も同じ)。2 行目と 3 行目は 1 つの段階として同時に大小が変わる |
| S30 `Fix c, find p` | 0 | 上の帯に前の式 (L と log L) を小さく残す。`(c-hat, p-hat) = argmax of log L(c, p)` (尤度の最大化) | 帯 + 最大化の式 |
| | 1 | c を固定する: ネットワークが c の色に塗られ、ブロックごとの m / n の表が出る。`fix c: p-hat = argmax over p of log L(c, p)` | 色つきの網 + 表 (5/6、1/16、6/6) |
| | 2 | log L を p_rs で微分して 0 とおく: `m / p - (n - m) / (1 - p) = 0` | + 微分の式 |
| | 3 | `p-hat_rs = m_rs / n_rs`。表が p-hat (0.83、0.06、1.00) に変わる | + 結果 |
| S31 `Back to c` | 0 | 上の帯に log L(c, p) と p-hat を小さく残す。p-hat を戻すと c だけの式: `log L(c) = sum over r <= s of [m log(m / n) + (n - m) log(1 - m / n)]` | 帯 + c だけの式 |
| | 1 | `a formula in c alone`。この c の値: 表に -2.70、-3.74、0。`log L = -2.70 - 3.74 + 0 = -6.44` | + 数値 |
| | 2 | `c-hat = argmax over c of log L(c)`。`all that is left: maximize over c` | 結び |
| S32 `More groups always fit better` | 0 | グループ数 K = 1 から 8 の、最良の log L: -19.1, -6.4, -3.0, -1.4, 0, 0, 0, 0 の折れ線。`log L never decreases as K grows` | 折れ線 |
| | 1 | `More groups, more parameters, a better fit`。K = 5 から 8 は 0 (完全に当てはまる) | + 破線 |
| | 2 | K = 8 (全員ひとり) に輪。`A large K overfits: the groups mean nothing`、`K = 8: every node alone, a perfect fit` | 結び |
| S33 `Political blogs` | 0 | 論文の Fig. 2(a) (普通の SBM、2 群)。`Political blogs, split in two by a plain SBM`、`node size: degree`、問い `What separates the two groups?` (答えは出さない)。出典 `Karrer and Newman (2011)` | 画像 + 問い |
| | 1 | 青 = `the high-degree blogs`、黄 = `the others`。`The groups follow degree, not politics.` (色は画像の青 #3880E5 と黄 #E6E679) | + 凡例と答え |
| S34 `Hubs` | 0 | カラテクラブの次数の点の図 (34 点。次数 1 から 17、最大 17)。`karate club` | 点の図 1 つ |
| | 1 | 右に S06、S07 の無作為ネットワーク (同じ 34 節点 78 辺) の次数 (2 から 8)。`random network, the same numbers of nodes and edges` | 点の図 2 つ |
| | 2 | `In an SBM, every node of a group has the same expected degree.`、`To fit the hubs, the SBM makes a group of hubs.` | + 2 行 |
| S35 `Degree-corrected model` | 0 | SBM: `P(A_ij = 1 given c, p) = p_{c_i c_j}` (ラベル `SBM`) | 式 1 |
| | 1 | `A_ij ~ Poisson(theta_i theta_j omega_{c_i c_j})` (ラベル `degree-corrected SBM`)。新しい式を大きく、古い式を少し小さく。定義: `A_ij` (i と j の間の辺の数)、`theta_i` (節点 i が辺を作りやすい度合い)、`omega_rs` | + 式 2 と定義 |
| | 2 | 同じ群の 3 組の節点 (円の面積 = θ、ω = 1): `2 x 2 x 1 = 4`、`2 x 1/2 x 1 = 1`、`1/2 x 1/2 x 1 = 1/4`。`expected edges between the two nodes` | + 3 組 |
| S36 `Fix c (degree-corrected)` | 0 | 8 ノードの網 (白抜き)。`log L(c, theta, omega) = sum_i k_i log theta_i + 1/2 sum_{r,s} (m_rs log omega_rs - omega_rs theta_r theta_s)` (2 行)。定義 `k_i`、`m_rs` (群内の辺は 2 回数える)、`theta_r` (群の θ の和、1 に固定) | 式 + 定義 |
| | 1 | c を固定: 網が c の色に塗られる。`fix c: (theta-hat, omega-hat) = argmax over theta, omega of log L(c, theta, omega)` | + 式 |
| | 2 | `theta-hat_i = k_i / kappa_{c_i}`、`omega-hat_rs = m_rs`、`kappa_r` (群の次数の和)。節点の大きさが θ-hat に。`node size: its share of the group's degree` | + 結果 |
| S37 `Back to c (degree-corrected)` | 0 | 戻すと c だけの式: `log L(c) = 1/2 sum_{r,s} m_rs log (m_rs / (kappa_r kappa_s)) + const`。左に 2 つの表: `seen` 10, 1, 1, 12 と `expected` 5.04, 5.96, 5.96, 7.04 (kappa_r kappa_s / 2m、次数だけから期待される辺)。`more edges inside the groups than expected` | 式 + 表 2 つ |
| | 1 | `= m I(c) + const`: m 掛ける、辺の両端の群の相互情報量 (= の位置は 1 行目の = の真下) | + 式 |
| | 2 | `I(c) = sum p(r, s) log [p(r, s) / (p(r) p(s))]`、`p(r, s) = m_rs / 2m`、`p(r) = kappa_r / 2m` (同時確率を周辺確率の積で割る。S15 から S19 と同じ形) | + I の式 |
| | 3 | `c-hat = argmax over c of log L(c)`。`all that is left: maximize over c` | 結び |
| S38 `Back to the blogs` | 0 | 論文の Fig. 2(a) と (b) を並べる。`plain SBM`、`degree-corrected SBM` | 画像 2 つ |
| | 1 | `Degree correction finds the groups despite heterogeneous degrees.`。`NMI with the known labels: 0.0001` と `NMI with the known labels: 0.72` (論文の値。後者を赤) | + NMI |
| S39 `Bayesian SBM` | 0 | 左: 最尤 `max log P(A given c, p)` ("more groups always fit better")。右: 記述長 `Sigma(c) = -log P(A given c) - log P(c)` (注釈 `the network, given the groups`、`the groups`)、`a shorter description is a better grouping` | 2 つの式 |
| | 1 | K ごとの最良の分け方の記述長 (nats) の折れ線: 22.68、18.21、20.33、21.85、22.60、22.91、23.09、21.49。K = 2 が最短。`The shortest description: K = 2` | 谷のある折れ線 + 輪 |
| | 2 | `K is inferred: Bayesian SBM`、`groups within groups: nested SBM`、`uneven degrees: degree-corrected SBM`、`Tiago Peixoto (2014, 2017, 2019)` | 3 行 |
| S40 `graph-tool` | 0 | `graph-tool: a Python library by Tiago Peixoto`、`The Bayesian SBM: nested, degree-corrected` | 2 行 |
| | 1 | 関数名 `minimize_nested_blockmodel_dl`、`graph-tool.skewed.de` | 結び |
| S41 `The karate club, once more` | 0 | 左にカラテクラブを実際の分裂 (青とオレンジ) で。`the groups so far` | クラブ 1 つ |
| | 1 | 右に同じクラブを 1 色で。`graph-tool: 1 group` | クラブ 2 つ |
| | 2 | オチ: `The two groups are no stronger than in a random network.`、`degree-corrected SBM, the shortest description` | 結び |

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
- **SBM の K ごと** (S30、S31): 8 ノードの網で、全 4140 通りの分け方のうち K 個の群への最良値。最尤の log L は
  K = 1 から 8 で -19.121、-6.444、-3.014、-1.386、0、0、0、0 (K とともに減らない)。簡単なベイズ流の記述長 (nats。各ブロックの確率に
  一様な事前分布を置いて積分し、P(K) = 1/8、P(c | K) は K 個の群への分け方の上で一様。符号を反転した量が事後確率の対数) は
  22.68、18.21、20.33、21.85、22.60、22.91、23.09、21.49 で、K = 2 で最短。
- **確率の表** (S15 から S18): 同時確率 0.5, 0, 0.125, 0.375。周辺確率は真 0.5, 0.5、found 0.625, 0.375。
  積 0.3125, 0.1875。比 1.6, 0, 0.4, 2。寄与 0.339, 0, -0.165, 0.375。和 0.549。
- **SBM** (8 節点、固定乱数の種 901): 辺は 12 本 (群内 11)、15 本 (群内 1)、12 本 (群内 6)。
  真の分け方の Q は 0.413、-0.436、0.000。確率 0.9 / 0.1 の網の升は 5/6、6/6、1/16。
  対数尤度は真 -6.4、1 人動かす -15.5、縞 -17.5、2 人動かす -18.4、全員 1 群 -19.1。
  `u` は節点 1 と 2 が 0.72、節点 1 と 6 が 0.59。

- **次数補正つき SBM** (`scripts/verify_dcsbm.py`、標準ライブラリだけ): カラテクラブの次数は最大 17、S06 の無作為ネットワークは最大 8
  (どちらも 34 節点 78 辺で次数の和 156)。8 ノードの網の次数は 2, 3, 2, 4, 3, 3, 4, 3。真の分け方で m_rs = [[10, 1], [1, 12]]
  (群内の辺は 2 回数える。群内 5 本と 6 本、群間 1 本)、kappa = (11, 13)、2m = 24、次数だけから期待される辺は 5.04, 5.96, 5.96, 7.04。
  ポアソンの対数尤度を θ-hat_i = k_i / kappa_{c_i}、ω-hat_rs = m_rs で計算した値が、`1/2 sum m_rs log(m_rs / (kappa_r kappa_s)) + sum k_i log k_i - m`
  と一致し (3 群までの全 6051 通りの分け方で)、また `m I(c) - m log 2m + 定数` とも一致する。
  **論文の式 (17)、(21)、(23) は、ここで使う対数尤度の 2 倍の形** (式 (16) の対数をとると 1/2 が付く)。式 (23) は「正規化していない対数尤度」で、
  c で最大化する答えは変わらない。論文の式 (24) が、この目的関数を辺の両端の群の相互情報量 (同時確率 m_rs / 2m と周辺確率 kappa_r / 2m の積) と書いている。
  8 ノードの網で、次数補正つきの対数尤度が最大になる 2 群への分け方は真の分け方。I(真の分け方) = 0.4032 nats (スライドには出さない)。
  政治ブログの NMI 0.72 (次数補正) と 0.0001 (補正なし) は論文の本文の値 (最大連結成分 1222 節点、Adamic and Glance のラベルとの NMI)。

## 話すときの注 (スライドには出さない)

- S33 から S38: 論文はカラテクラブも同じ方法 (K = 2 の最尤) で示している (Fig. 1)。補正なしは高次数の群と低次数の群に分け、補正ありは実際の分裂を
  1 人の誤りを除いて見つける。S41 のベイズ流 (K も推定する) の結果と食い違って見えるが、問いが違う (K = 2 を与えた最尤か、2 群を支持する証拠があるか)。
- 論文の内容を使う画像 (図 2) は Karrer and Newman の出版物のもの。授業で使う権利は講師の判断。

- S04: Fortunato と Barthelemy (2007)。しきい値は √(2m) で、群の運命が、その群ではなく網全体の辺数 m で決まる。
- S07: 「Q > 0.3 を意味のある構造の目安とする」は講義ノートの記述と同じ。
- S21: 実際の分裂の Q は 0.358 で、上の 2 つの分け方 (0.407、0.402) より低い。Q を最大にしても
  実際に起きたことには戻らない。属性は必ずしも正解ではない (Peel, Larremore, Clauset 2017)。
- S27: 最良の分け方を探すのは Q を最大にするのと同じくらい難しく、実際の手法も発見的。
  尤度なら群の数も比べられる。式の詳細は講義ノートと付録。

## 実装の順序 (この順に作った)

1. `~/Downloads/fourier-slides` を `slides/m05/remotion/` に展開 (`node_modules` と `dist` はコミットしない)。
   `package.json` の name と `index.html` の title を直す。
2. `theme.ts` と `Frame.tsx` を上のスタイルに変える。`Slide1.tsx` から `Slide7.tsx` と `index.ts` の配列を消す。
3. データ生成スクリプト (Python) が `src/data/*.ts` を書く。そこで上の数字を assert する。
4. 最初に **S04** を作る (輪、折れ線、期待値の数字を持つ最も重い 1 枚)。手順書 9 の確認を丁寧に行い、
   スタイルが Marp に合っているかをここで決める。
5. 残りを表の順に作る。節ごとに `npm run build` を通し、`npm run review` の静止画でレビューを回す。

## 確認できたこと、できていないこと

- 確認できた (2026-10-05):
  - 上の数字。すべて `scripts/verify_numbers.py` で assert が通った (K ごとの SBM のスコアを含む)。
  - `npm run build` (型チェックとビルド)。
  - 41 枚の全段階の静止画 (120 枚)。`npm run review` で作り、全部を目で見て、重なり、欠け、文字の切れがないことを確かめた。
  - headless Chrome でキーボード操作 (→ で進む、← で戻る) を最後の段階まで通し、段階の表示が正しく進むこと、
    スクリプトのエラーがないことを確かめた (27 枚の版で。その後に追加した分は静止画だけ)。
- 確認できていない:
  - 動きの滑らかさ。静止画 (各段階の終点と途中の数枚) だけを見ている。
  - 段階が切り替わる約 10 フレームの間、前の絵が薄く重なる (S15 など)。
  - 実際の Chrome で全画面にしたときの文字の見え方、投影したときの色の見分けやすさ。
  - 動画の書き出し (`npx remotion render`)。
  - Remotion のライセンス (営利企業は有料になりうる。教育目的の扱いは公式の License ページで確認)。
  - Peixoto の文献と graph-tool の関数名、URL は手元の記憶で書いた。授業の前に原典で確認すること。
  - S41 の「graph-tool で空手クラブは 1 群」は、手元で graph-tool を実行して確かめてはいない。graph-tool のメーリングリスト
    (Inference for the "karate network") の `minimize_blockmodel_dl(G, deg_corr=True)` の結果と、Peixoto の
    Bayesian stochastic blockmodeling (arXiv:1705.10225) の記述による。**次数補正つきの場合**で、2 群以上の分け方も合わせると
    事後確率の約半分を占めるので、「群の構造がない」ではなく「2 群を支持する証拠が、同じ次数列のランダムなネットワークと変わらない」
    と読むこと。次数補正なしの SBM の結果は確かめていない。

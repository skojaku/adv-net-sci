# モジュラリティ最大化 Remotion スライド案 (DECK_SPEC)

2026-10-06。この文書の説明は日本語、`like this` の引用がスライド上の文字 (英語)。
講師の依頼: モジュラリティの動画。前半はモジュラリティとは何か、後半は Louvain (と Leiden)。授業の説明がうまくいかなかったので、別の道筋で説明する。
M05 の Remotion デッキ (`../remotion`) は「モジュラリティの限界」から始まる。このデッキはその前に入る。

講師が決めたこと:
- 前半の道筋: 群の内側の辺を数える → その割合は「辺を 1 本無作為に選んだとき両端が同じ色の確率」 → これを最大にすると全員 1 群が勝つ (使えない)
  → 無作為な網で期待される分を引く (全員 1 群なら 0) → 辺を半分に切って無作為につなぎ直す (次数も辺の数も変わらない。コンセントの数は同じで配線を組み替える)
  → ノード i, j の間の期待辺数 k_i k_j / 2M (順序を入れ替えても同じ、の説明を丁寧に) → 最後まで「期待される辺の本数」と呼び、確率とは呼ばない (講師の指示。疎な網やハブの注意書きのスライドは削った)
  → 行列 3 枚を順に: A、k_i k_j / 2M、その差 Q_ij (モジュラリティ行列。講師の指示で B_ij でなく Q_ij) → メンバーシップ c_i、δ(c_i, c_j)、足し合わせ → 空手クラブで Q。群の数は入力でなく、最大化の途中で決まる。
- 後半: ラベル切り替えを空手クラブで少しずつ → 止まる (小さい群を合体すれば Q は上がるのに、1 ノードずつでは動けない) → 群をスーパーノードにして再び最適化、Q が上がらなくなるまで繰り返す = Louvain
  → Leiden。
- Louvain の欠点は、**つながらない群** (Leiden 論文が直した問題) として語る (講師が選んだ)。「まとまりすぎる」(解像度限界) は Q の性質で Leiden でも直らず、M05 デッキ S01 から S04 の話。まとめで一言だけふれる。
- 行列の例は、小さい例 (6 ノード) で数字を見せ、そのあと空手クラブ (講師が選んだ)。
- Newman and Girvan (2004, Phys. Rev. E 69, 026113) は、Q の式の完成 (S12) で札として出す。Girvan and Newman 2002 (PNAS) は辺の媒介中心性の論文で、モジュラリティではない。
- 解釈の確認 (講師に伝え済み): 「ラベルスイッチング」は Q を使う貪欲な 1 ノード移動 (Louvain の第 1 段階)。「kj-1」は 2M-1。「Mr.」は Mr. Hi と Officer の 2 派。

## 全体のきまり (M05 デッキと同じ。最終)

- 解説は英語 (スライドの文字)。見出しは付けない (`Frame` に `title` を渡さない)。章の扉はない。
- 一言一句、少ない語で。em dash (—) を使わない。修辞を使わない (たとえ話の見出し、盛り上げ、「実は」)。1 文 1 つの考え。数える単位 (ノードの組か、ノード 1 つか、辺か、端か) を明示する。
- **文は `Box` / `Cap` / `Tag` に、式は `Tex` に書く。** 5 語以上で式を含まない `Box` / `Cap` / `Tag` は、動画では画面から消えてチャットに打たれる。
  ラベル (5 語未満)、数字、図、式は画面に残る。画面に残したい説明は 5 語未満にする。
- 問いのスライドに答えは出さない。
- 赤 `#B14434` は強調する文字だけ (`Term`、`Tag hot`)。塗り、群の色、線には使わない。緑は使わない。棒グラフは使わない (点・折れ線)。
- 群の色は `LOOK[0..4]` (青、オレンジ、茶、紫、濃い灰)。1 つのノードだけの群・ラベルが一人だけのノードは `HOLLOW` (白に青い縁)。
- ノードの組を「2 つのノードを線で結ぶ絵」で描かない (辺に見える)。組は行列のセル、またはセルの格子で描く。行列は対角を含めて全部描く。
- 式は 1 つずつ積み上げる (`FormulaStack`)。導く前にパラメータを与えない。新しい式は大きく、古い式は小さく。式を消さない。
- 数字は `src/data/data.ts` から読む (`scripts/make_data.py` が書く。**編集しない**)。スライドに出る数字で、そこから来ないものは作らない (小さな割り算は TS で計算してよい)。
  Q などは小数 3 桁 (`q3()` in `src/lib/club.ts`、真のマイナス記号 U+2212)。
- 乱数を使わない。スライドは `useCurrentFrame()` だけの純関数。
- `Frame n={N}`、既定の `zoom` 1.08、`top` 190。**y = 920 より下は空ける** (字幕と話し手のため)。端 40 px に絵をかけない。`npm run review` のあと `python3 scripts/check_bottom.py`。
- `export const marks = [...]`: `marks[i]` は段階 i が終わるフレーム。段階 0 は 0 から始まる。**段階の最後のフレームは完成した絵。** 1 段階は 50 から 120 フレーム (動いている部分があれば、その長さ + 余白)。
- 前のスライドの終わりの絵で次のスライドが始まる (座標を共有: `CLUB_L` など `src/lib/club.ts`)。次のスライドの冒頭に、前の絵がフェードインしてはいけない。
- 部品: `Frame`, `Canvas` / `Fade` / `FadeG` (`components/Fade`), `Box`, `Cap`, `Tag`, `Term` (`components/Text`), `Tex`, `FormulaStack`, `Network` / `toCanvas` / `mix` (`lib/network`), `LOOK` / `HOLLOW` (`lib/look`),
  `prog` / `smooth` / `stageStart` / `fromStage` / `betweenStages` / `piecewise` / `stepped` (`lib/anim`)。色 `C` とフォント `F` は `src/theme.ts`。
  共有ファイル (`network.tsx`, `Frame.tsx`, `index.ts`, `data.ts`, `club.ts`, `theme.ts`) は編集しない。必要なら、スライドのファイルの中に自分の部品を書く (他のスライドと共有する部品は `src/lib/` に新しいファイルを作る)。
- 見方: `node scripts/review.mjs --only=1-8` (自分のスライドだけ。`out/review/S01-s1.png` ...)。その静止画を **全部見る**。`npx tsc --noEmit`。

## 数字 (`data.ts`、検算済み: `scripts/verify_numbers.py`)

空手クラブ: 34 ノード、M = 78 辺、2M = 156。2 派 (REAL): 群の内側 67 辺、外 11 辺。内側の割合 0.859。無作為なら 0.5007 (= (81/156)^2 + (75/156)^2)。Q = 0.358。
全員 1 群 Q = 0.000。全員別々 Q = −0.050。ノード 0 と 33 の次数は 16 と 17: 16 × 17 / 156 = 1.74 (1 を超える)。
列 `ORDER` の順にノードを訪ね、`MOVES` 36 手で 5 群 (`STUCK`)、Q = 0.399。群 1 と 2 (`MERGE_PAIR`) を合体すると Q = 0.420 (`Q_MERGED`)。ノード 5 (`MOVE_NODE`) を群 2 から群 1 へ動かすと Q = 0.386 (下がる)。
5 つのスーパーノードの大きさ `AGG_SIZE` = 11, 2, 3, 12, 6、重み `AGG_W` (対角は群の内側の辺数の 2 倍)。2 段目の移動 `L1_MOVES` = スーパーノード 1 が 2 のラベルを取る。4 群 (`FINAL`)、Q = 0.420 (= 0.4198)。3 段目は何も動かない。
段ごとの Q: −0.050, 0.399, 0.420。通り数 `BELL_34` = 2.1e+28 (Bell 数)。
小さい例 `TOY_*` (2026-10-06 に替えた。講師: ノードの次数がみな同じだと、期待辺数の行列が例にならない): 星 {0,1,2} (ハブ 0、葉 1, 2) と三角形 {3,4,5} を辺 0-3 でつなぐ。6 ノード 6 辺、次数 3, 1, 1, 3, 2, 2 (2M = 12)。
2 派 {0,1,2} {3,4,5} の Q = 0.319 (内側 5 辺)。ノード 1 と 5 (番号は 1 から) の k_i k_j / 2M = 3 × 2 / 12 = 0.50 (S06, S07, S09)。ノード 1 と 2 は 3 × 1 / 12 = 0.25 で、辺がある (S10)。期待辺数は 0.08 から 0.75 まで開く。
つなぎ直し: 12 個の端 `TOY_STUB_NODE` (端 s はノード TOY_STUB_NODE[s] のもの)、組 `TOY_STUB_PAIRS` (端の番号の組 6 つ)、新しい辺 `TOY_REWIRED`。群の内側は 6 辺中 3 辺 (元は 5 辺。無作為なら 6 × 0.514 = 3.1 辺で、典型的な結果)。
つながらない群の例 `BR_*`: 10 ノード 14 辺。三角形 {0,1,2} と {3,4,5}、橋のノード 6 (2 と 3 につながる)、三角形 {7,8,9} (6 から 7, 8, 9 へ)。
`BR_S0`: 群 C = {0..6}、群 D = {7,8,9}、Q = 0.222。`BR_S1`: 橋 6 が D に移る、Q = 0.357、C = {0..5} は 2 つの三角形で辺がない。`BR_S2`: 2 つの三角形を分ける、Q = 0.482。
**これは作った例で、Louvain の実行ではない。** 各状態の Q は計算した。Louvain がこのような状態になりうることは Leiden 論文 (Traag, Waltman, van Eck 2019) が示している。スライドで「Louvain がこう動いた」と書かない。

## スライド

担当 A: S01 から S08。担当 B: S09 から S14。担当 C: S15 から S23。(最初の割り当て。のちに S08 と S23 を削り、全 21 枚)

### 前半: モジュラリティとは

**S01 club-two-colours** (2 段階)。`CLUB_L` に空手クラブ (`Network`、ノード 46 前後)。
0: ノードが現れる (白に青い縁 `HOLLOW`)、そのあと辺。`34 nodes, 78 edges` (Cap、右)。
1: ノードが 2 派の色になる (REAL: 青とオレンジ)。右に問い: `Is each colour a strong community?` (Box 右、問いのみ。答えを出さない)。

**S02 count-inside** (3 段階)。S01 の最終の絵で始まる (同じ座標、同じ色)。
0: 同じ色どうしの辺 (内側) が群の色で太くなる (`edgeLook`、幅 7)。色の違う辺 (外側) は薄い灰色 (幅 3)。
1: 右に数: `inside: 67`、`between: 11`、そのあと式 `\frac{67}{78}=0.859`。`M = 78 edges` (label)。
2: 内側の 1 辺と外側の 1 辺に輪をつけ、`same colour` と `different colours` (label)。文: `Pick one edge at random. Its two ends have the same colour with probability 0.859.`

**S03 maximize-inside** (3 段階)。S02 の左の club を同じ場所に。
0: クラブ (2 色)。Tag `67 / 78 = 0.859`。
1: オレンジのノードが `FLIP_ORDER` の順に 1 つずつ青になる (1 つ 5 フレーム)。Tag の分子が `FLIP_INSIDE[k]` に変わる (途中 61 まで下がり、78 まで上がる)。辺の色も追従。
2: 全員青。Tag `78 / 78 = 1.000` (hot)。文: `Everyone in one group gives the highest score. The score says nothing about the network.`

**S04 subtract-chance** (3 段階)。左に `FormulaStack`、式だけ。
0: `\text{inside fraction}=\dfrac{\text{edges inside groups}}{M}` (note: `M is the number of edges`)。
1: `Q=\text{inside fraction}-\text{inside fraction expected in a random network}`。文: `The random network has the same number of edges and the same degree for every node.`
2: `\text{everyone in one group: }\ 1-1=0`。文: `Now we need that random network.`

**S05 cut-edges** (4 段階)。小さい例 (`TOY_*`) を大きく (幅 700 ほど)。ノードは 1 から 6 の番号 (`a+1`) の円。
0: 小さい例が現れる。各ノードの横に次数 (`k = 2` など。label)。`6 edges, 12 edge ends` (Cap)。
1: 辺が真ん中で切れて、各ノードから短い線 (端、stub) が出る。`12 stubs` (label)。
2: 端が `TOY_STUB_PAIRS` の組に無作為につなぎ直される (端が伸びて出会う)。新しい網 `TOY_REWIRED`。各ノードの次数は同じ (label を残す)。文: `Every node keeps its degree. The number of edges stays 6.`
3: 元の網 (左、2 派を青とオレンジ) と、つなぎ直した網 (右、同じ色) を並べる。数: `5 of 6 edges inside` と `3 of 6 edges inside` (label)。文: `Like a power strip: the number of sockets on each device is fixed and only the wiring is shuffled.`

**S06 one-stub** (2 段階。講師の指示 2026-10-06: 導出は一本の筋で簡潔に。弧と 2M−1 は使わない)。14 個の端を 1 列に (小さい円)、ノードごとにまとめて、下にノード番号。ノード i = 1 (ハブ)、j = 5 (インデックス 0, 4) に `i`, `j` の札。
0: 端の列。`2M = 12 stubs` (label)。文: `Every stub is equally likely to join any other stub.`
1: i の端 3 つと j の端 3 つに括弧と `k_i`, `k_j`。文: `So the expected edges between i and j are proportional to their stubs.` 式 `\text{expected edges}\ \propto\ k_i\,k_j`。

**S07 stub-pairs** (2 段階)。k_i × k_j (3 × 2) のセルの格子 (行 = i の端 1 から 3、列 = j の端 1 から 2)。
0: 格子が現れる。式 `k_i\times k_j=3\times2=6\ \text{pairs}`。文: `Each cell is one pair of stubs: one of i, one of j.`
1: 各セルに `1/2M`。式 `\dfrac{k_ik_j}{2M}=\dfrac{3\times2}{12}=0.50`。文: `Each pair of stubs contributes 1/2M edges on average.` label `expected number of edges`
(行と列から数えて同じ 9 セルになる段階は削った。「j の側からも k_j k_i / 2M で同じ」は、ナレーションの 1 行で言う。)

### 前半の続き: 行列 (担当 B)

行列のマスの大きさ: 小さい例 78 px 前後、空手クラブ 13 px。群の側線 (行と列の外側) は 2 派の色。正の値は青、負の値は茶色 (`mix` で白から)。緑・赤を使わない。

**S08 matrix-a** (2 段階)。左に小さい例の網、右に 6 × 6 の行列 (対角を含む)。行と列にノード番号の円。
0: 網と空の格子。ラベル `A_{ij}` (Tex)。
1: セルが埋まる: 辺があるセルは `1` (青)、ないセルは `0` (灰色の字)。文: `A_ij is 1 if nodes i and j share an edge, and 0 if not.`

**S09 matrix-e** (3 段階)。S08 と同じ配置。
0: 各ノードの横に次数 k。行列の格子と、行・列の端に次数。ラベル `E_{ij}`。
1: セルが 1 行ずつ埋まる (`k_i k_j / 12`、小数 2 桁、値の大きさで青の濃さ)。セル (ノード 1, ノード 5) を強調して、式 `\dfrac{3\times2}{12}=0.50`。
2: 文: `A random network with the same degrees has this many edges between each pair, on average.`

**S10 matrix-b** (4 段階)。A、E、B の 3 つを横に並べる (演算子 − と =)。
0: A と E が並ぶ (`-`)。
1: `=` と B が現れる。Q_ij = A_ij − E_ij の数字、正は青、負は茶色の濃さ。式 `Q_{ij}=A_{ij}-\dfrac{k_ik_j}{2M}`。
2: 文: `Positive: more edges than expected. Negative: fewer.` (青・茶の凡例は label)。
3: B の右に、各行の和 (すべて 0)。文: `Each row of Q_ij sums to 0.`

**S11 club-matrices** (3 段階)。空手クラブの A、E、B、34 × 34、ノードは派ごとに並べる (REAL = 0 の 17 ノード、次に REAL = 1)。外側に 2 色の線。演算子 − と =。
0: A (辺 78 本、セル 156 個が青)。1: E (濃淡)。2: B (青と茶)。文: `The same three matrices for the karate club, with the nodes sorted by group.`

**S12 q-formula** (4 段階)。左に B (空手クラブ、セル 13 px) と、外側にメンバーシップの色の線。右に `FormulaStack`。
0: メンバーシップ。式 `c_i=\text{group of node }i`。
1: 同じ群のセル (δ = 1) だけが残り、他は薄くなる (2 つの対角ブロックが残る)。式 `\delta(c_i,c_j)=1\text{ if }c_i=c_j\text{, else }0`。
2: 残ったセルの B を足す。式 `Q=\dfrac{1}{2M}\sum_{i,j}Q_{ij}\,\delta(c_i,c_j)`。
3: Tag `Q = 0.358`。札 `Newman and Girvan, 2004` と `Phys. Rev. E 69, 026113` (label)。文: `Q is the fraction of edges inside groups minus the fraction expected in a random network.`

**S13 club-q-values** (5 段階)。空手クラブ 4 つを横に (幅 380 前後)、各 Tag に Q と群の数。
0: 全員別々 (`HOLLOW`)、`34 groups`、Q = −0.050。1: 全員 1 群、`1 group`、Q = 0.000。2: 2 派、`2 groups`、Q = 0.358。3: 4 群 (`FINAL`)、`4 groups`、Q = 0.420 (hot)。
4: 文: `We did not choose the number of groups. Maximizing Q chooses it.`

### 後半: アルゴリズム (担当 C)

**S14 too-many** (2 段階)。0: 数 `2.1\times10^{28}` (Tex、大)。文: `ways to split 34 nodes into groups.` 1: 文: `We cannot try them all. We improve one partition step by step.`

**S15 label-switching** (4 段階)。`CLUB_L` に空手クラブ、右に Q の折れ線 (横軸 move、縦軸 Q。点と線、棒でない)。
ノードの見え方: 自分だけのラベルのノードは `HOLLOW` に番号、2 つ以上でラベルを共有したら群の色 (最終の 5 つのラベルに `LOOK[0..4]`、ほかのラベルは `LOOK[label % 5]`)。群の内側の辺は太く、外側は薄く。移っているノードに輪。
0: 全員が自分のラベル、Tag `Q = −0.050`。文: `Every node starts with its own label.`
1: `MOVES` の 1 手目から 12 手目 (1 手 4 フレーム)。文: `A node takes the label of the neighbouring group that raises Q the most.`
2: 13 手目から 36 手目。Q = 0.399、5 群。
3: 文: `No single move raises Q any more.`

**S16 stuck** (3 段階)。`STUCK` の 5 群、Tag `Q = 0.399`。
0: 5 群。文: `No node can move to raise Q.`
1: ノード `MOVE_NODE[0]` が群 `MOVE_NODE[1]` へ動く。Tag `Q = 0.386` (hot でなく、下がった)。そして元に戻る。
2: 群 2 の 3 ノード全部が群 1 へ。Tag `Q = 0.420` (hot)。文: `Merging two whole groups raises Q. One node at a time cannot see it.`

**S17 supernodes** (3 段階)。S16 の最終と同じ座標で始まる (5 群、2 の 3 ノードは元の位置。`STUCK`)。
0: 群の周りに薄い帯。1: 各群が 1 つの円 (群の重心、大きさは `AGG_SIZE`、数字をラベル) に縮む。群の内側の辺は円の自己ループ (辺数 `AGG_W[i][i]/2`)、群どうしの辺は 1 本の太い線 (太さは辺数 `AGG_W[i][j]`、数字をラベル)。
2: Tag `Q = 0.399`、前と同じ。文: `The network of groups has the same Q.`

**S18 second-level** (3 段階)。S17 の最終の絵で始まる。
0: 5 つのスーパーノードの網。1: `L1_MOVES`: スーパーノード 1 が 2 に合流 (円が合体)、Tag `Q = 0.420`。
2: 元の 34 ノードが現れ、`FINAL` の 4 色になる。文: `4 groups. Q = 0.420.`

**S19 louvain-loop** (3 段階)。0: ループの図 (箱 3 つ): `Move nodes` → `Merge groups into nodes` → `Repeat until Q stops rising` (矢印で戻る)。
1: 右に点の折れ線 (棒でない): 段 0 −0.050、段 1 0.399、段 2 0.420、`level 3: no change`。2: Tag `Louvain` と `Blondel, Guillaume, Lambiotte, Lefebvre, 2008`。

**S20 bridge-leaves** (4 段階)。作った例 `BR_*`。青 = 群 C、オレンジ = 群 D。
0: `BR_S0` (橋 6 は青)。Tag `Q = 0.222`。1: 橋が D に移って橋がオレンジに、Tag `Q = 0.357` (hot)。
2: 青い群が 2 つの三角形に分かれ、間に辺がないことを強調 (間に破線の輪や空白)。文: `The blue group is now in two pieces with no edge between them.`
3: 文: `Louvain moves a node only to a neighbouring group. It cannot split them.` と、`Traag, Waltman, van Eck, 2019` と `up to 25% of communities badly connected, up to 16% disconnected` (その論文の要旨のとおり)。

**S21 leiden-refine** (4 段階)。`BR_S1` で始まる (S20 の終わり)。
0: 同じ絵。Tag `Q = 0.357`。1: 青い群が 2 つの三角形に割れる (別の色)。Tag `Q = 0.482` (hot)。文: `Leiden splits each group into well-connected parts before it merges them.`
2: ループの図 (S19 と同じ形): `Move nodes` → `Split groups into connected parts` → `Merge parts into nodes`。
3: 文: `Every group stays connected.` と `Leiden: Traag, Waltman, van Eck, 2019`。

(まとめのスライド (旧 S23) は削った。講師: Louvain と Leiden の復習は余分。「まとまりすぎるのは Q 自身の性質で、Leiden は直さない」は最後のスライド (S21) の最後のナレーションに移した。)

(旧 S08 の「確率でなく本数」スライドも削った。講師: 情報が散って分からない。「これは本数です」で通す。S07 の式に label `expected number of edges` を付けた。全 21 枚。)

## 作り方の順

1. `python3 scripts/make_data.py` (数字) と `python3 scripts/verify_numbers.py` (検算)。
2. スライド (3 人で分担)。3. 全体の `npm run review` と `check_bottom.py`。4. 動画: `port_video.mjs` (M05 の手順書) → 導入、ナレーション、`moods.ts`。

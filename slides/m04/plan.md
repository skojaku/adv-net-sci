# m04 "Count Your Friends" — スライド計画

2026-08-05、講師との相談で確定。実装は DECK_BUILD_GUIDE.md の Order of work に従い、
本計画 → review/DECK_SPEC.md → review/FIGURE_SPEC.md → figures → デッキ → check_render → /slide-review。

デッキ: `slides/m04/m04-node-degree.md` ・ セッション 09/16, 09/18 ・ 約78枚。

## 決定事項(相談ログ)

| 論点 | 決定 |
|---|---|
| 背骨 | **Feld 1991 の Marketville 高校**一本槍。8人の女子生徒 → 同校146人 → Facebook/Twitter → 共著網、とスケールだけを上げて同じ現象に戻り続ける |
| タイトル | **Count Your Friends**(サブタイトル: then count theirs) |
| 全体の順序 | **パラドックス先行**。第2幕で $\mathrm{Var}(k)/\langle k\rangle$ まで導き、「ではその分散は実際いくつ?」を橋にして第3幕の次数分布へ。次数分布は「パラドックスを測るために必要になった道具」として登場する |
| 数学の深さ | **両方フル導出**。(1) $q(k) \to \langle k^2\rangle/\langle k\rangle \to \langle k\rangle + \mathrm{Var}(k)/\langle k\rangle$、(2) power-law PDF の積分 → CCDF の傾き $1-\gamma$。どちらも1行ずつビルドする |
| 規模・日割り | m03 並み約78枚。1日目 (09/16) = Part 1–4(第1〜2幕+応用)、2日目 (09/18) = Part 5–8(第3〜4幕) |
| 友情カード実験 | **やめる**(curriculum.yml の hook は不採用)。第1幕のマイルストーンは Feld の網を手で数える Your turn に置き換え |
| 応用の位置 | 第2幕直後の独立パート (Part 4)。知人免疫 → ワクチンゲームで1日目を締める |
| BA モデル (c21) | 短いパート (Part 6)。成長+優先的選択 → GIF → $\gamma=3$ は結果として提示。導出なし。M08 (popularity vs similarity) へ伏線 |
| scale-free 論争 (c26) | **終幕直前の山場** (Part 8)。Poisson 混合でも直線が出る図を見せ「さっきの直線、信じますか?」で閉じる |
| エッジケース | 4題すべて採用: あなた個人にも成り立つ? / パラドックスが消える網 / 有向網 / 分布が同じでも繋ぎ方は違う (assortativity) |
| 一般化パラドックス | 入れない(Eom & Jo 2014 は不採用。1つのエッジケースに2つ新概念は入らない) |
| $\Sigma k = 2M$ と握手補題 | Part 2「端点を数える」に置く。$2M$ がそのまま Part 3 の $q(k)$ の分母になるのでトリビアにならない。握手補題は M01 のオイラー条件の回収として問い形式で |
| 2つの平均 | Part 3 で1枚使って区別する。3.0 = 友人関係20本についての平均 = $\langle k^2\rangle/\langle k\rangle$(定理はこちらだけを主張する)、2.99 = 8人それぞれの平均を人単位で平均したもの。この区別が Part 7「あなた個人にも成り立つ?」の伏線 |
| 146人データ | Part 1 末に入れる。「8人はたまたまでは?」に同じ学校の同じデータで答える |
| 実データ | **arXiv 共著網**(SNAP ca-HepTh または ca-AstroPh)を Part 4/5/6 で貫く。`figures/data/` に同梱して再現可能に。尾が素直な直線にならないなら、それ自体を Part 8 の伏線として使う |
| 演習 | 1日目末 = vaccination-game.html / 2日目 = ペーパー演習「Data Visualization」を Part 5 直後に一括 / friendship-paradox-game.html は Part 7「消える網」で |
| 2日目の入り | m03 と同じ作法。リキャップなし、パート扉から直接再開 |
| 結び | Coming up in Module 05: assortativity が「誰と誰が繋がるか」を問い始めた → ではその塊(コミュニティ)とは何か |

## ストーリー(四幕)

- **第1幕 Marketville, 1961(物語)** — James Coleman が米国の高校で友人関係を集め(*The Adolescent Society*, 1961)、30年後に Scott Feld がその一校 "Marketville" の女子生徒8人の友人網を見直した。学生が手で数えると、8人中5人が「自分の友人たちの平均」を下回る。同校146人でも 80 対 41。侮辱ではなく、数え方の帰結。
- **第2幕 その物語の数学** — 端点を数える(次数、$\Sigma k = 2M$、握手補題で M01 回収、$p(k)$)→ なぜ起きるか(ハブは多くの名簿に載る)→ 辺をランダムに選ぶ = $q(k)$(先週 m03 で使った偏り)→ $\langle k^2\rangle/\langle k\rangle$ → $\langle k\rangle + \mathrm{Var}(k)/\langle k\rangle$ → Feld の網で検算(2.5 + 0.5 = 3.0)。
- **応用(第2幕の帰結)** — 共著者・引用・SNS でも同じ / 辺を辿って集めたデータは全部歪む(サンプリングバイアス)/ 逆に使えば知人免疫。1日目はここで「ギャップ = 分散。では実際の網の分散はどれほど?」とクリフハンガー。
- **第3幕 一般化(分布を読む)** — fat tail → 線形ヒストグラムの失敗 → log-log → 直線 = べき乗則 → PDF のビン問題 → CCDF → 傾きは $1-\gamma$(積分で導出)→ ハブはどこから来るか(普遍性、Poisson/正則との対比、BA)。
- **第4幕 エッジケースと懐疑(全て問いで)** — 個人には成り立つか / 消える網 / 有向網 / 繋ぎ方 → そして「直線は power law の証明ではない」→ 復習 → M05 予告。

## パート構成(8パート・約78枚)

Lead + 今日の問い + Roadmap(3枚)のあと:

### Part 1: Marketville, 1961(第1幕、約9枚)

1. 扉 → 物語: 1961年 James Coleman が米国の高校で友人関係を収集。1991年 Scott Feld がその一校 "Marketville" を見直した(実名・年号)
2. 8人の網が登場(名前のみ、次数はまだ出さない)。Feld 本人が「名前は仮名」と明記している点も一言
3. 問い: 「この8人、平均で何人の友人がいる?」→ 数える(**c01** の入口)
4. 答え: $\langle k\rangle = 2.5$
5. 問い(単独スライド、答えを一切載せない): 「では **あなたの友人たち** は平均で何人の友人を持つ?」
6. **Your turn**(マイルストーン): 各自1人担当 → その人の友人の友人数の平均を出す
7. 教室の答えを網に書き込むビルド → 8人中5人が自分より上、上回るのは Sue と Alice の2人だけ、Carol はちょうど同じ
8. Feld の結論: 生徒の平均 2.5、友人の平均 3.0(**c05**)。「これは侮辱ではない」
9. 「8人はたまたまでは?」→ 同じ学校146人: 80人が下回り、41人が上回り、25人が同じ

### Part 2: Counting ends(第2幕前半、約9枚)

1. 扉 → 次数の正式な定義。個人にとっては露出、網にとっては中心性の分布(**c01**)
2. 問い: 「全員の次数を足すといくつ?」(Feld 網で、答えを載せない)
3. 答え: $\Sigma k = 2M$ — 辺には端が2つ(**c02**)。Feld 網で 20 = 2×10
4. 帰結: $\langle k\rangle = 2M/N$
5. 問い: 「次数が奇数の人がちょうど3人、という網は作れる?」
6. 答え: 作れない。握手補題(**c03**)+ M01 のオイラー条件が「0個か2個」だった理由の回収
7. 視点を1人から網全体へ: 各次数の人は何割?(**c04** $p(k)$ の定義)
8. Feld 網の $p(k)$ を柱状に置く(2日目の可視化パートへの布石)
9. 問い: 「なぜ友人の方が多くなる?」→ 名簿を並べるビルド: Sue と Alice は4枚の名簿に載り、Betty と Tina は1枚にしか載らない(**c06**)

### Part 3: The exact gap(第2幕後半、約11枚)

1. 扉 → 問い: 直感は分かった。**どれだけ**多いのか、正確に言える?
2. 「友人を1人ランダムに選ぶ」= 辺の端点を1つランダムに選ぶ。2M 本の手が入った袋(m03 の $q(k)$ の絵を再利用)
3. 次数 $k$ のノードは袋の中に $k$ 本の手を持つ → $q(k) = k\,p(k)/\langle k\rangle$(**c06** 続き、m03 からの明示的な回収)
4. その平均: $\langle k\rangle_{\text{friend}} = \sum_k k\,q(k) = \langle k^2\rangle/\langle k\rangle$
5. 分散の定義 $\mathrm{Var}(k) = \langle k^2\rangle - \langle k\rangle^2$ を代入(1行ビルド)
6. 定理: $\langle k\rangle_{\text{friend}} = \langle k\rangle + \mathrm{Var}(k)/\langle k\rangle$(**c07**)
7. 分散は負にならない → **どの網でも成り立つ**。等号は全員同じ次数のときだけ
8. Feld の網で検算: $\langle k^2\rangle = 7.5$、$\mathrm{Var} = 1.25$、ギャップ $= 0.5$、$2.5 + 0.5 = 3.0$ — 手で数えた 60/20 と一致
9. **どちらの平均か**: 辺をランダムに選ぶ(3.0、定理が言っているのはこれ)vs 人をランダムに選んでその人の平均を平均する(2.99)。図で明示。Part 7 への伏線
10. **Your turn**(マイルストーン): 星グラフとリングで $\mathrm{Var}(k)/\langle k\rangle$ を計算し、ギャップを予言してから数え合わせる
11. 締め: ギャップの正体は分散だった

### Part 4: Using the bias(応用、約8枚)

1. 扉 → 問い: 友情だけの話?
2. 共著網: 「あなたの共著者はあなたより共著者が多い」— arXiv 共著網の実測値(**c08**)
3. 桁を上げる: Facebook 7.2億人 — 92.7% が友人の平均を下回り、83.6% が友人の中央値を下回る(Ugander et al. 2011)。Twitter は98%(Hodas et al. 2013)
4. 問い: 「辺を辿って集めたデータからは、何を推定しても歪む?」
5. 答え: 歪む。辺をたどるサンプリングはハブを過剰に、周辺を過少に拾う(**c11**)
6. 問い: 「では、網の地図を一切持たずにハブを見つけられる?」(m03 の狙い撃ち攻撃の回収)
7. 答え: 知人免疫 — ランダムに選ぶ → 友人を1人挙げてもらう → 挙がった人に打つ(**c09**)
8. **ライブデモ: vaccination-game.html**(マイルストーン)+ クリフハンガー「ギャップ = 分散。実際の網の分散は?」

### Part 5: Reading the distribution(第3幕前半、約14枚、2日目開始)

1. 扉 → 実網の $p(k)$ を線形軸のヒストグラムで出す。ほぼ全部が最初の数本に潰れる(**c13**)
2. 問い: この図から何が読める? → 読めない
3. 尾に何がいるのかを明かす: 少数のノードが莫大な次数を持つ(**c12** fat tail)
4. 両軸を対数に(**c14** log-log)— 同じデータ、同じビン、軸だけ変える
5. 見えたもの: おおむね直線
6. 直線 = べき乗則 $p(k) \sim k^{-\gamma}$(**c17**)。$\gamma$ はハブが希になる速さ
7. 問い: ビン幅を変えたら図はどうなる?
8. 答え: 尾のノイズもビン幅次第で形が変わる(**c15**)
9. ビンを使わない量: $\mathrm{CCDF}(k) = P(k' > k)$(**c16**)、生存関数
10. 同じデータの CCDF — 滑らか、ビン選択なし
11. 余談: CDF は尾を潰す(**c27**、1枚)
12. 問い: CCDF の傾きは $\gamma$ そのもの?
13. 導出ビルド: $p(k) = Ck^{-\gamma}$ を $k$ から $\infty$ まで積分 → $P(k) \propto k^{-(\gamma-1)}$ → 対数を取ると傾き $1-\gamma$(**c18**)
14. **Your turn**(マイルストーン): 測った傾きが $-1.3$。$\gamma$ は? → 2.3、1.3 ではない
15. (授業運営)ペーパー演習「Data Visualization」を一括実施

### Part 6: Where hubs come from(第3幕後半、約9枚)

1. 扉 → ハブの定義と、それが持つ辺の割合(**c22**)
2. 普遍性: 生物・技術・社会の網が揃ってべき乗則的(**c25**、Barabási & Albert 1999)
3. 問い: どんな網でもそうなる? → ランダム網ならどうか
4. 答え: Poisson 分布、平均の周りに集中、ハブは実質存在しない(**c19**、m02 の ER 網の回収)
5. さらに狭い極: 格子・リングは全員同じ次数(**c20**、m02 の回収)。この3つを同じ CCDF 軸に重ねる
6. 問い: では実網のハブはどこから来た?
7. BA モデル(**c21**): 成長 — ノードが1つずつ到着し $m$ 本の辺を持ってくる
8. 優先的選択: $\Pi(k_i) = k_i/\sum_j k_j$、金持ちがさらに富む。成長 GIF → $\gamma = 3$ は結果として提示(導出なし)
9. **見分けクイズ**(マイルストーン): 2つの網の図と CCDF を見せ、どちらが優先的選択でどちらが一様接続の成長か。+ 「片方だけでは足りない」(一様接続の成長は指数分布、固定ノード上の優先的選択は全結合)+ M08 予告

### Part 7: Edge cases(第4幕前半、約9枚、全て問い→答えの対)

1. 問い: パラドックスは **あなた個人** にも成り立つ?
2. 答え: 「平均して真」と「あなたにとって真」は別。Feld 網では8人中5人が下回り、2人が上回り、1人が同じ。ハブ自身には逆に成り立たない。平均 vs 中央値(Facebook の 92.7% と 83.6% の差はここ)
3. 問い: パラドックスが **消える** 網は作れる?
4. 答え: $\mathrm{Var}(k) = 0$ のときだけ — リング、完全グラフ、正則格子。**friendship-paradox-game.html で作らせる**(マイルストーン)
5. 問い: 有向網では? フォロワー数とフォロー数
6. 答え: 入次数と出次数で偏りの向きが分かれる。「あなたが見ているアカウントは、あなたより見られている」
7. 問い: 次数分布が同じ2つの網は同じように振る舞う?
8. 答え: 違う。$p(k)$ はハブの数しか言わず、ハブ同士が繋がるかは言わない — assortative / disassortative / neutral(**c23**)
9. その帰結: 社会網は assortative(ハブのコアが持ちこたえる)、技術・生物網は disassortative(周辺がハブにぶら下がる)→ m03 のロバストネスが変わる

### Part 8: A straight line is not a proof + Review(第4幕後半、約6枚)

1. 問い: Part 5 で引いたあの直線。**べき乗則の証明になっている?**
2. 答え: なっていない。Poisson の混合でも log-log 上でほぼ直線が出る図を並べる(**c26**)
3. だから統計的検定が要る。目視ではなく — scale-free 論争は現在進行形(Broido & Clauset 2019 ほか)
4. それでも $p(k)$ の**形**は効く: ロバストネス (M03)、距離 (M02)、伝播速度 — 1つの分布が課程を横断して振る舞いを決める(**c24**)
5. Module 04 review(四幕の一枚振り返り)
6. Coming up in Module 05: assortativity は「誰と誰が繋がるか」を問い始めた。ではその塊 — コミュニティ — とは何か、そして見つけたものが本物だとどう分かるのか

## マイルストーン(ルーブリック S5)

- **P1**: Your turn — Feld 網で1人担当し友人の友人平均を計算、教室で 5 対 2 を再現
- **P2**: 問い — 「奇数次数がちょうど3人の網は作れる?」(握手補題の発見)
- **P3**: Your turn — 星グラフとリングでギャップを予言してから検算
- **P4**: ライブデモ vaccination-game.html
- **P5**: Your turn — 傾き $-1.3$ から $\gamma$ を出す + ペーパー演習「Data Visualization」一括実施
- **P6**: 見分けクイズ — 優先的選択 vs 一様接続の成長
- **P7**: friendship-paradox-game.html でパラドックスが消える網を作る + 各エッジケースが問い
- **P8**: 「この直線を信じますか?」の挙手

## 概念カバレッジ

- P1: c05 / P2: c01, c02, c03, c04, c06 / P3: c06, c07 / P4: c08, c11, c09, c10
- P5: c13, c12, c14, c17, c15, c16, c27, c18 / P6: c22, c25, c19, c20, c21 / P7: c23(+ c05/c07/c20 の敷衍)/ P8: c26, c24
- **全27概念を採用**。extension の c27(CDF vs CCDF)は1枚の余談として収容

## 作業用グラフ: Feld (1991) Figure 1(検証済み)

原典 Feld, Scott L. 1991. "Why Your Friends Have More Friends than You Do." *American Journal of Sociology* 96(6): 1464–1477 の Figure 1 / Table 1。全数値は独立に検算済み。

**辺(10本)**: Betty–Sue, Sue–Alice, Sue–Pam, Sue–Dale, Alice–Jane, Alice–Pam, Alice–Dale, Jane–Dale, Pam–Carol, Carol–Tina

| | Betty | Sue | Alice | Jane | Pam | Dale | Carol | Tina | 計 |
|---|---|---|---|---|---|---|---|---|---|
| 次数 $k$ | 1 | 4 | 4 | 2 | 3 | 3 | 2 | 1 | **20** |
| 友人の友人の総数 | 4 | 11 | 12 | 7 | 10 | 10 | 4 | 2 | **60** |
| その平均 | 4 | 2.75 | 3 | 3.5 | 3.33 | 3.33 | 2 | 2 | |

*(この表は計画のためのもの。デッキでは表は禁止 — 数値は図に直接刷る)*

- $N = 8$, $M = 10$, $\Sigma k = 20 = 2M$, $\langle k\rangle = 2.5$
- $\Sigma k^2 = 60$, $\langle k^2\rangle = 7.5$, $\langle k^2\rangle/\langle k\rangle = 60/20 = 3.0$
- $\mathrm{Var}(k) = 7.5 - 6.25 = 1.25$, ギャップ $= 1.25/2.5 = 0.5$, $2.5 + 0.5 = 3.0$ ✓
- 人単位の平均の平均 $= 23.92/8 = 2.99$(Feld の丸めた値による。厳密には 2.9896)
- 下回る5人 = Betty, Jane, Pam, Dale, Tina / 上回る2人 = Sue, Alice / 同じ = Carol
- **描画**: 原図は Sue–Dale と Alice–Pam が交差しているが、このグラフは平面的($K_5$ から3辺を抜いた核 + 2本のペンダント)。**交差ゼロで描き直す**(F2)
- **二次資料に誤りがある**: "Pam の友人は Carol, Sue, Dale" とする解説が流通しているが誤り(正しくは Carol, Sue, **Alice**)。次数が Feld の Table 1 と合わなくなる。孫引きしないこと

## 検証必須の数値(DECK_SPEC 段階で全て計算・出典確認)

- Feld 網の全数値(上記。生成器で辺リストから再計算し、上の値と一致することをアサート)
- Feld 146人: 80人が下回り / 41人が上回り / 25人が同じ(計146)、平均 2.7 vs 3.4
- Facebook: 92.7%(平均を下回る)/ 83.6%(中央値を下回る)/ 中央値99 / 平均約190 / $\langle k^2\rangle/\langle k\rangle = 635$ — Ugander, Karrer, Backstrom, Marlow 2011, arXiv:1111.4503、7.21億アクティブユーザ・687億辺(2011年5月)
- Twitter: 98% 超 — Hodas, Kooti, Lerman 2013 (ICWSM), arXiv:1304.3480、5.8M ユーザ・193.9M リンク
- arXiv 共著網の $N, M, \langle k\rangle, \langle k^2\rangle/\langle k\rangle$, ギャップ、推定 $\gamma$(データから計算)
- 星グラフ(4ノード): $\langle k\rangle = 1.5$, $\langle k^2\rangle/\langle k\rangle = 2$, ギャップ $0.5$ / リング: ギャップ $0$
- 傾き $-1.3 \Rightarrow \gamma = 2.3$、BA の $\gamma = 3$
- 史実: Coleman, *The Adolescent Society*, Free Press, 1961 / Feld 1991 / Barabási & Albert 1999 / Cohen et al. 2003(知人免疫)/ Broido & Clauset 2019(scale-free 論争)

## 図・アニメ(FIGURE_SPEC の種)

FIGURE_GUIDE 準拠: ノードリンク図は TikZ、データ図は Altair/seaborn(matplotlib 不可)、棒グラフ不可、緑不使用、最終サイズで作図(1単位 = 1スライドピクセル)、`make_figures.py` + `make_animations.py` に集約、全数値をデータから計算してアサート。

1. Feld 網 — 名前のみ / 次数入り / 友人平均入り / 5対2の色分け、の4段ビルド(**交差ゼロ**をアサート)
2. 名簿ビルド: 各人の友人リストを並べ、Sue と Alice が4回、Betty と Tina が1回だけ現れることを可視化(c06)
3. $q(k)$「2M 本の手が入った袋」図(m03 のジオメトリを踏襲し、m03 との連続性を明示)
4. $\langle k\rangle + \mathrm{Var}/\langle k\rangle$ の数式ビルド(1行ずつ)
5. 「辺を選ぶ vs 人を選ぶ」の対比図(3.0 と 2.99 の違い)
6. Marketville 146人の分布(Feld Fig. 2/3 相当を再描画、平均 2.7 と 3.4 の2本の線)
7. 知人免疫の3ステップ図(ランダムに選ぶ → 指名 → 指名された人に打つ)+ ランダム接種との比較曲線
8. 実網の次数分布 4連ビルド: 線形ヒスト → log-log → PDF のビン幅3種 → CCDF(同一データ、同一色)
9. CCDF の傾きから $\gamma$ を読む注釈付き図(傾き $-1.3$ の三角形)
10. CDF が尾を潰す図(1枚、余談用)
11. 普遍性: 生物・技術・社会の3〜4例の CCDF を1枚に
12. Poisson / 正則 / power law の CCDF 重ね描き
13. BA 成長 GIF(優先的選択でハブが育つ)+ 一様接続の成長との並置(静止画は GIF の最終フレームと一致させる)
14. 見分けクイズ用: 2つの網の図と CCDF(答えは次スライド)
15. エッジケース小図: 消える網(リング・完全グラフ)、有向網のフォロー関係、assortative vs disassortative の模式
16. Poisson 混合が log-log 上で直線に見える図(c26 の山場)
17. Module 04 review 図(四幕を一枚に)
18. Coming up in Module 05 teaser 図

## 実装手順(DECK_BUILD_GUIDE 準拠)

1. m01 から scaffold(`network-science.css`、`check_render.py`、`README.md`。deck ファイル名を `m04-node-degree.md` に)
2. `review/DECK_SPEC.md` — 本計画をスライド1枚単位に展開、**全数値を計算して検証**(ルーブリックの non-negotiables を冒頭に再掲)
3. `review/FIGURE_SPEC.md` → `figures/make_figures.py` + `figures/make_animations.py`(アサーション付き、x-height は測定値でアサート、コンテナはデッキのマークアップから読む)
4. デッキ `m04-node-degree.md` 執筆(fragments は `*`、表・コード禁止、問いと答えは別スライド、質問スライドの `note` にも答えを書かない、KaTeX は `figcaption`/`steps-list` で効かない)
5. render → `python3 check_render.py` が exit 0 になるまで
6. `/slide-review` ループ(REVIEW_PLAYBOOK 準拠、Opus がレビュー・Sonnet が修正、毎ラウンド commit)

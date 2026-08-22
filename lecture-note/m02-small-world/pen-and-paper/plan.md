# M02 ペーパー演習の作り直し — 計画

レビュー用のたたき台です。実装はまだしていません。

---

## 1. いまの状態と、目指す状態

### いま

m02 には演習シートが4枚あります。合計 **26ページ**。

| ファイル | ページ | 中身 |
|---|---|---|
| `six-handshakes.tex` | 8 | 距離、平均距離、直径、リング村、近道2本、Milgram |
| `do-your-friends-know-each-other.tex` | 8 | 三角形、クラスタリング2種類、ランダム基準、σ |
| `turning-the-dial.tex` | 8 | Watts-Strogatz、C(p) の減り方、σ が嘘をつく話 |
| `csr.tex` | 2 | CSR というデータ構造 |

問題は26ページという分量だけではありません。

- 空欄（`___`）と表の穴埋めが大量にあり、学生は「考える」より「埋める」作業をしています
- 英語が長く、専門用語（transitivity, coefficient, lattice, index）が説明なしで出てきます
- 同じリング村が3枚のシートで微妙に違う設定（16人・隣2人／20人・隣4人）で出てきて、つながりません

### 目指す状態

m01（`m01-euler_tour/pen-and-paper/`）とまったく同じ形にします。

```
m02-small-world/pen-and-paper/
  exercise.tex       ← 1枚、4ページ、8問
  solutions.tex      ← 解答（問題文も一緒に載せる）
  townkit.tex        ← 図を1か所に置き、上の2つが両方読み込む
  lab.py             ← marimo ノートブック（Part 4 の行き先）
  lab-solutions.py   ← 自動生成
  lecture-hall.css   ← m01 からそのままコピー
  m02lab-qr.png      ← QRコード
```

---

## 2. 何を残し、何を捨てるか

4枚 → 1枚にするので、捨てる判断が計画の中心です。

### 紙に残すもの（これが4ページの中身）

- 距離（何回の握手で届くか）
- 平均と最悪（＝平均距離と直径。名前は授業で付ける）
- 村が大きくなると距離がどう伸びるか
- 近道を2本足すと何が起きるか
- 「友達どうしは友達か」の割合（＝局所クラスタリング）
- 同じ割合を、でたらめに結んだ村と比べる
- Milgram の計算（150人ずつ知っていたら4〜5回で全人類に届く）と、その計算の嘘
- 「短い道がある」と「素人が短い道を見つけられる」は違う、という Milgram の本当の主張

### ラボ（ノートブック）に移すもの

- **σ（スモールワールド指数）とその破綻**。これは今 `turning-the-dial.tex` の Part 4 にあり、紙でやると対数や近似式が要って高校生には重いです。ラボなら**学生自身が書いたコードが σ > 1 を出してしまう**という形で見せられます。こちらの方が効きます。
- **C(p) と L(p) の2本の曲線**。紙では「だいたいの形を描け」としか言えませんが、ラボならスライダーで本物が出ます。

### 完全に捨てるもの

- **CSR（`csr.tex`）**。これは「ネットワークをどうデータとして持つか」の話で、スモールワールドとは別の話題です。m01 のラボがすでに隣接行列を扱っています。
- **クラスタリングの2つの定義（局所平均 vs 全体）の食い違い**。面白いけれど、初回に2つ教えると両方あいまいになります。1つ（局所）だけにします。
- 空欄と穴埋め表のほとんど。

---

## 3. 村の設計（ここが一番重要な決定）

**16人が輪になって座り、全員が「両隣2人ずつ、計4人」と知り合い。友情は32本。**

理由：1つの図で距離も三角形も両方できるからです。いまの4枚は「隣1人ずつ」の村（三角形がゼロ）と「隣2人ずつ」の村（三角形がある）を別々に使っていて、話がつながっていません。

手計算した数字（すべて検算済み）：

| | 近道を足す前 | 1–9 と 5–13 を足した後 |
|---|---|---|
| 友情の数 | 32 | 34（6% 増）|
| 1番の人から全員への握手の合計 | 36 | 27 |
| 平均 | 2.4 | 1.8（**25% 減**）|
| 1番から一番遠い人 | 4回（9番）| 3回（6番と12番）|
| 1番の友達4人のうち、友達どうしの組 | 6組中3組 = 1/2 | 町全体の三角形は16個のまま |

**うれしい性質**：この図は 1番と9番を通る軸で完全に左右対称です（近道を足した後も）。なので学生は**右半分（2〜9番）の8個だけ**数字を書けば済みます。左半分は鏡写し。作業が半分になり、しかも対称性という気づきが1つ増えます。

近道は「足す」（移動ではなく追加）にします。移動だと三角形が2個壊れて話が濁ります。追加なら「三角形は1個も壊れていない、なのに距離は25%縮んだ」ときれいに言えます。本物のモデルは移動する、という注意は1行だけ入れます。

---

## 4. 4ページの中身（8問）

問題文は英語のまま載せます。短い文、日常語だけ、専門用語なしです。

### 1ページ目

**書き出し**（3文）: 1967年、オマハからボストンの見知らぬ人へ手紙を届ける。直接送ってはいけない。下の名前で呼び合う知り合いにしか渡せない。

> **Question 1**: How many hands did the letter pass through? Write your guess, and write why you guessed that.

（最後の Question 8 で同じことを聞き直します。自分の直感が当たったか外れたかを見る仕掛け）

**Part 1: Ringville** ＋ 図①（16人の輪、輪の外側に2〜9番の横だけ小さな四角）

> **Question 2**: Person 1 wants to reach person 9. Draw the chain on the circle. How many handshakes?
> Now write, in the box next to each person, how many handshakes from person 1. The left half is the mirror of the right half, so you only need the boxes that are printed.
> Add all 15 numbers up. Share them out among the 15 people — that is the *average*. What is the largest number you wrote — the *worst case*?
> One of these two numbers you would tell a newspaper. The other you would tell an engineer who has to promise the letter arrives. Which is which, and why?

### 2ページ目

> **Question 3**: The town grows. 1,000 people, still in a circle, still 4 friends each. How many handshakes to the person on the far side? And with 8 billion people? So can a world wired like Ringville deliver the Omaha letter in six steps?

**Part 2: Two shortcuts** ＋ 図②（同じ輪＋1–9 と 5–13 の弦が**すでに描いてある**。書き込み用の箱も同じ）

*（スキルのルール：学生が知りようのないものを「描け」と言わない。近道は印刷して渡す）*

> **Question 4**: Two people went away to college and each kept one friend far from home. Write the new numbers in the boxes. New total, new average, new worst case.

### 3ページ目

> **Question 5**: You added 2 friendships to 32 — about 6% more. Did the average drop by about 6%? What did those two lines actually do? Answer in your own words.

**Part 3: Do your friends know each other?** ＋ 図③（1番と友達4人だけを抜き出した小さい図）

> **Question 6**: Person 1 knows four people. Those four can form six pairs. How many of the six pairs are friends themselves? Write the fraction.
> The town grows to 10,000 people, still 4 friends each. What is the fraction now?
> Now a different town: same 16 people, same 32 friendships, but thrown together at random. Pick any two people — what is the chance they are friends? So how many of person 1's six pairs would be friends? And in a random town of 10,000?

（1/2 のまま vs 4/10000 ≒ 0。これが「高いクラスタリングはただでは手に入らない」の正体）

> **Question 7**: The town had 16 triangles before the shortcuts. How many did the two shortcuts destroy? So what does a shortcut cost the town?

### 4ページ目

> **Question 8**: Back to Omaha. Suppose everyone knows 150 people, and — pretend for a moment — no two of your friends know each other.

小さい表（1〜4握手で何人に届くか）だけは残します。150, 22500, 3.4M, 506M, 76B。

> At how many handshakes do you pass 8 billion? Compare with your guess in Question 1.
> Question 6 says the "pretend" in this calculation is false. Which way does that push the answer?
> Last: you are person 1 in the town with shortcuts, holding a letter for person 12. You cannot see the drawing. You only know your own friends and where each of them sits. Write the chain you would actually produce. Is it the shortest one that exists? So — are "a short chain exists" and "an ordinary person can find one" the same claim?

**Part 4: The lab, on your own** — QRコードの箱（m01 と同じレイアウト）

---

## 5. ラボノートブック（`lab.py`）

ご要望どおり「まず見て動かす → 自分で書く → 自分のコードで動くデモ」の順にします。✍️ マークの学生が書くセルは**3つだけ**（ガイドの推奨は3〜6）。

### 1 · 波が広がるのを見る（準備）

スライダーを動かすと、**紙の村ではない小さい別の村**（7人）で、1番から波が外へ広がります。0歩目、1歩目、2歩目…と色が付き、横に「1 handshake away: {…}」という表が育ちます。

*（ガイドの鉄則：学生が答えを書かされる図をアニメで歩かせない）*

一言：「2歩目で光った人が、2回の握手で届く人。距離とはそれだけのことです。」

### 2 · ✍️ 村を建てる — `ring_edges(n, half)`

32本の友情を手で打たせるのは無理なので、**規則を2行で書かせます**。
チェックは間違いを名指しします：「あなたの村は34本。町は32本です」「1番の人が6人と知り合いになっています。4人のはずです」。
通ったら、学生のコードで村の絵が描かれます。

### 3 · ✍️ 距離 — `distances_from(A, s)`

幅優先探索。これがこのモジュールの本体のアルゴリズムです。
チェックは小さい村で行い（紙の村の答えを画面に出さないため）、通ったら学生の村で実行し、**紙に鉛筆で書いた 36 / 2.4 / 4 と並べて表示**します。合わなければどちらかが間違っている、それを見つけるのが演習です。

### 4 · 組を見る（準備）

スライダーで人を選ぶと、その人の友達が光り、友達どうしの6組が薄く描かれ、実際にある3組だけ濃くなります。「3 of 6」とカウンタが出ます。

### 5 · ✍️ 割合 — `local_clustering(A, i)`

Question 6 でやったことのコード版。学生の村で走らせると全員が 0.5 になります。

### 6 · ダイヤルを回す（デモ／学生のコードで動く）

- スライダー `p` を 0 → 1 に動かすと、村が組み替わっていく絵が変わり、横に L と C が**学生の関数で計算されて**出ます。
- そして全掃引：p を 0.001 から 1 まで対数軸で振って、L(p)/L(0) と C(p)/C(0) の2本の曲線を描きます。**あの有名な図が、自分の書いたコードから出てくる**。
- 「道が短く、かつ三角形が残っている帯」がどれだけ広いか、その場で見えます。

### 7 · 嘘をつく数（デモ／期待どおりか確かめる）

学生の `distances_from` と `local_clustering` を使って、**近道が1本もない素のリング村**について
σ = (C/C_rand) / (L/L_rand) を計算します。答えは **σ > 1**。

「あなたのコードは、近道がゼロの村を『スモールワールドだ』と判定しました。」

さらに人数を増やすと σ は 1 に近づくどころか**大きくなっていく**。ここが「期待どおりか確かめる」の山場です。紙で σ を教えるより、こちらの方がはるかに強く残ります。

### 8 · 早く終わった人へ

「三角形を9割残したまま、道の長さを半分にする p を見つけてください。」

---

## 6. 作業リスト

1. `townkit.tex` — 図①②③の TikZ を1ファイルに（`exercise.tex` と `solutions.tex` が両方読む）
2. `exercise.tex` — m01 の前文をそのままコピー（Charter 書体、14pt、余白は m01 と同じ）
3. `solutions.tex` — 問題文も載せる。図の問題は**図で答える**（数字が入った輪を描く）
4. `lecture-hall.css` を m01 からコピー
5. `lab.py` を書く
6. `tools/build_m01_lab_notebooks.py` をモジュール引数を取れる形に一般化 → `lab-solutions.py` を生成（m01 は壊さない）
7. QRコード生成（`go.skojaku.com/m02lab` を指す）
8. 古い4枚（`six-handshakes` / `do-your-friends-know-each-other` / `turning-the-dial` / `csr`）の .tex を削除
9. `03-exercises.qmd` のリンクを差し替え
10. `curriculum.yml` の coverage パスを直す（いまは `lecture-note/m02/six-handshakes/exercise.pdf` を指していて、実在しません）
11. PDF を1ページずつ**画像にして目で見る**（`pdftoppm`）。ここを飛ばすと図が枠から出ているのに気づきません
12. ラボを `marimo export html --sandbox` で実行して、空欄のまま Traceback ゼロを確認
13. git add / commit / push

**私の手では終わらない作業**：`lab.py` を molab にアップロードするのは Sadamori さんのアカウントが要ります。アップロード後の URL がわかれば、droplet の Caddy に `go.skojaku.com/m02lab` の転送を私が書き足せます（`ssh digitalocean`）。QRコードは短縮URLを指すので、ノートブックを上げ直しても刷り直しは不要です。

---

## 7. 決定事項（2026-08-22 確認済み）

1. **古い4枚の .tex は削除**し、`exercise.tex` + `solutions.tex` の1枚に置き換える。git 履歴には残るので必要なら取り出せる。
2. **σ はラボへ、CSR は削除**。紙のシートは8問のまま。
3. **村は16人・全員が両隣2人ずつ（友情32本）の1つの図**で、距離と三角形の両方をやる。
4. **molab へのアップロードは Sadamori さん**。URL をもらったら、私が droplet の Caddy に `go.skojaku.com/m02lab` の転送を書き足す。

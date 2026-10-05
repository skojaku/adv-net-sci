# M05 アニメーションスライド (Remotion)

Marp デッキ `../m05-clustering.md` の続きを、クリックで段階的に進むアニメーションで見せる 32 枚。
設計は `DECK_SPEC.md`、作り方と確認の手順は `BUILD_NOTES.md`。

## 動かす

```bash
npm install
npm run dev        # ブラウザで開く。f キーで全画面
npm run build      # 型チェックとビルド
```

| 操作 | 動作 |
| --- | --- |
| クリック, →, ↓, Space, Enter | 次の段階 (最後なら次のスライド) |
| ←, ↑, Backspace | 前の段階 (逆再生) |
| f | 全画面 |

## 1 枚を静止画で確認する

```bash
npx remotion still src/remotion-entry.ts S04-resolution-limit out/s04.png --frame=56
```

composition 名は `S<番号>-<id>`、一覧は `src/slides/index.ts`。`out/` はコミットしない。
Remotion Studio (`npm run studio`) では、各 mark のフレームに合わせて停止状態をコマ送りできる。

## データと数字

スライドが読むデータは `scripts/make_data.py` が `src/data/data.ts` に書く (手で編集しない)。

```bash
uv run scripts/make_data.py       # データを作り直す
uv run scripts/verify_numbers.py  # スライドに出る数字を全部計算し直して assert する
```

`scripts/check_metrics.mjs` は `src/lib/metrics.ts` (NMI、ARI など) の値を確かめる。

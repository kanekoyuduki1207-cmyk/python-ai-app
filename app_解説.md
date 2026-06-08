# StreamlitとGemini APIで作るAIライティングツール — コード解説

---

## 全体の構造を掴もう

`app.py` は大きく **3つのパート** で構成されています。

```
① 初期設定（ページ設定・サイドバー）
② 共通部品（result_area関数）
③ 各ツールのUI・処理（if/elif チェーン）
```

---

## ① 初期設定 — アプリの「顔」を作る

```python
st.set_page_config(page_title="AI ライティングツール", page_icon="✍️", layout="wide")
```

Streamlit でいちばん最初に書く「おまじない」です。ブラウザのタブに表示されるタイトルとアイコン、レイアウトをここで決めます。`layout="wide"` にすると画面幅を最大限使えます。

```python
TOOLS = {
    "📝 ブログ記事執筆": "blog",
    "📧 メール返信文生成": "email",
    ...
}
selected = st.sidebar.radio("ツールを選択", list(TOOLS.keys()))
tool = TOOLS[selected]
```

`TOOLS` は **辞書（dict）** で、「画面に表示する名前」と「コード内で使う短いキー」を対応させています。ユーザーがサイドバーで選んだ名前から `tool` というキーを取り出すのがこの3行のポイントです。

---

## ② 共通部品 — result_area 関数

```python
def result_area(result: str):
    st.markdown("### 生成結果")
    st.markdown(result)
    st.download_button("📥 テキストをダウンロード", result, file_name="output.txt", mime="text/plain")
```

全8ツールが共通して使う関数です。やっていることは2つだけ：

1. **生成結果を画面に表示する**（Markdown形式で綺麗に描画）
2. **ダウンロードボタンを表示する**（クリックすると `output.txt` として保存できる）

「同じ処理を8回書かない」ために関数にまとめた典型例です。

---

## ③ 各ツールの処理 — if/elif チェーン

ここが app.py の本体で、8つのツールが `if/elif` でつながっています。

```python
if tool == "blog":
    # ブログ記事の処理
elif tool == "email":
    # メール返信の処理
elif tool == "summary":
    ...
```

サイドバーで選ばれたツールのブロックだけが実行される仕組みです。各ブロックの中身はどれも同じ3ステップになっています。

---

### ツール1つ分の構造（ブログ記事を例に）

```python
# ステップ1: 入力UIを作る
topic = st.text_input("記事のテーマ・タイトル")
tone  = st.selectbox("文体", ["カジュアル", "フォーマル", ...])

# ステップ2: ボタンが押されたらプロンプトを組み立てる
if st.button("記事を生成", disabled=not topic):
    with st.spinner("記事を生成中..."):
        prompt = f"""以下の条件でブログ記事を書いてください。
テーマ: {topic}
文体: {tone}
..."""
        result = generate(prompt)   # Gemini APIに送信

    # ステップ3: 結果を表示する
    result_area(result)
```

| ステップ | Streamlitの部品 | 役割 |
|----------|----------------|------|
| 入力 | `text_input`, `selectbox`, `text_area`, `checkbox` | ユーザーから条件を受け取る |
| 送信 | `st.button` + `st.spinner` | ボタンクリックでAPI呼び出し・処理中表示 |
| 出力 | `result_area()` | 結果表示＋ダウンロード |

---

## Streamlit の動き方（重要）

Streamlit のコードは **ユーザーが何か操作するたびに上から下へ全部実行し直される** という特徴があります。

そのため `st.button` が `True` を返す（＝押された）のは**その1回のタイミングだけ**です。`disabled=not topic` は「テーマが未入力のときはボタンを押せなくする」という使いやすさのための工夫です。

---

## まとめ — このコードが上手い点

```
TOOLS辞書 → サイドバーで選択 → tool変数にキーが入る → 該当のelifブロックが実行される
```

この流れを覚えれば、**新しいツールを追加するのは `TOOLS` に1行追加して `elif` ブロックを1つ書くだけ**です。全ツールが `result_area()` を共有しているので、ダウンロード機能など共通の改善も1か所直すだけで全ツールに反映されます。

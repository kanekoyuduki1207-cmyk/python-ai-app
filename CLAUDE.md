# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## アプリの起動

```bash
streamlit run app.py
```

起動後は http://localhost:8501 でアクセスできる。初回起動時のメール登録プロンプトは `~/.streamlit/credentials.toml` に以下を書いてスキップする：

```toml
[general]
email = ""
```

## 環境

- Python 3.14.5
- Windows 11（パスの区切り文字は `\`）

`.env` ファイルに Gemini API キーを設定する（`.env.example` を参照）：

```
GEMINI_API_KEY=your_api_key_here
```

パッケージインストール時に権限エラーが出る場合は `--user` オプションを使う：

```bash
pip install --user -r requirements.txt
```

## Gemini SDK の注意点

`google-generativeai` は廃止済み。必ず `google-genai` を使う。

```python
from google import genai
client = genai.Client(api_key=api_key)
response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
```

## アーキテクチャ

2ファイル構成：

- **`gemini.py`** — Gemini API の薄いラッパー。`generate(prompt: str) -> str` の1関数のみ公開。
- **`app.py`** — Streamlit UI と全ツールのロジックを1ファイルに集約。サイドバーの `TOOLS` 辞書でツール名とキーを管理し、`if/elif` チェーンで各ツールのUIとプロンプト生成を行う。

共通のUI部品として `result_area(result: str)` があり、生成結果の表示とテキストダウンロードボタンをまとめて担う。全ツールはこれを通じて結果を出力する。

## ツールの追加方法

1. `app.py` の `TOOLS` 辞書に `"📌 表示名": "key"` を追加
2. `elif tool == "key":` ブロックでUI・プロンプトを実装
3. `generate(prompt)` を呼び出し、結果を `result_area(result)` で表示

プロンプトは日本語で書き、`【条件】` のような見出し付き箇条書きで構造化するのが既存ツールのパターン。

import streamlit as st
from gemini import generate

st.set_page_config(page_title="AI ライティングツール", page_icon="✍️", layout="wide")

st.sidebar.title("✍️ AI ライティングツール")

api_key_input = st.sidebar.text_input(
    "Google API キー",
    type="password",
    placeholder="お持ちのGemini APIキーを入力（任意）",
    help="入力しない場合は、サーバー側の .env に設定されたキーを使用します。キーはセッション内でのみ保持され、保存されません。",
)

st.sidebar.markdown("---")

TOOLS = {
    "📝 ブログ記事執筆": "blog",
    "📧 メール返信文生成": "email",
    "📋 文章要約": "summary",
    "🔍 文章校正・改善": "proofread",
    "📱 SNS投稿文生成": "sns",
    "🏷️ タイトル・見出し生成": "title",
    "🔄 トーン変換": "tone",
    "💡 キャッチコピー生成": "catchcopy",
}

selected = st.sidebar.radio("ツールを選択", list(TOOLS.keys()))
tool = TOOLS[selected]

st.sidebar.markdown("---")
st.sidebar.caption("Powered by Gemini API")


def result_area(result: str):
    st.markdown("### 生成結果")
    st.markdown(result)
    st.download_button("📥 テキストをダウンロード", result, file_name="output.txt", mime="text/plain")


# ── ブログ記事執筆 ──────────────────────────────────────────────
if tool == "blog":
    st.title("📝 ブログ記事執筆")
    st.markdown("テーマや条件を入力するとブログ記事を自動生成します。")

    topic = st.text_input("記事のテーマ・タイトル", placeholder="例: 初心者向けPythonの始め方")
    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("文体", ["親しみやすい・カジュアル", "丁寧・フォーマル", "専門的", "エンタメ・面白い"])
        length = st.selectbox("文字数の目安", ["500字程度", "1000字程度", "2000字程度", "3000字程度"])
    with col2:
        target = st.text_input("ターゲット読者", placeholder="例: プログラミング初心者")
        keywords = st.text_input("含めたいキーワード（任意）", placeholder="例: 環境構築, pip, ライブラリ")

    additional = st.text_area("その他の要望（任意）", placeholder="例: 見出しをH2/H3で構成して、最後にまとめを入れてください", height=80)

    if st.button("記事を生成", type="primary", disabled=not topic):
        with st.spinner("記事を生成中..."):
            prompt = f"""あなたはSEOと日本語ライティングの専門家です。以下の条件で、検索上位を狙えるブログ記事を執筆してください。

【基本情報】
- テーマ: {topic}
- 文体: {tone}
- 文字数の目安: {length}
- ターゲット読者: {target if target else "一般読者"}
- メインキーワード: {keywords if keywords else "テーマから自然に設定"}
- その他の要望: {additional if additional else "特になし"}

【SEOの要件】
- タイトル（H1）にメインキーワードを含める
- H2・H3の見出しにも関連キーワードを自然に散りばめる
- 導入文の冒頭100字以内にメインキーワードを入れる
- キーワードは本文全体を通じて自然な頻度で使う（詰め込みすぎない）
- 読者の検索意図（知りたいこと・解決したいこと）に正面から答える構成にする
- 具体例・数字・根拠を入れて信頼性（E-E-A-T）を高める
- 最後にFAQセクション（よくある質問と回答を3つ）を追加する

【構成】
1. 導入（読者の悩みに共感し、記事で解決できることを伝える）
2. 本文（H2見出しで3〜5セクションに分ける）
3. まとめ（要点を箇条書きで整理）
4. FAQ

Markdown形式で出力してください。"""
            result = generate(prompt, api_key=api_key_input.strip() or None)
        result_area(result)


# ── メール返信文生成 ─────────────────────────────────────────────
elif tool == "email":
    st.title("📧 メール返信文生成")
    st.markdown("受信したメールの内容を貼り付けると、返信文を自動生成します。")

    received = st.text_area("受信メールの内容", placeholder="相手からのメール本文をここに貼り付けてください", height=200)
    col1, col2 = st.columns(2)
    with col1:
        reply_tone = st.selectbox("返信の文体", ["丁寧・ビジネス", "カジュアル・フレンドリー", "簡潔・シンプル"])
        intent = st.selectbox("返信の意図", ["承諾・了承", "断り・辞退", "質問・確認", "お礼", "謝罪", "情報提供"])
    with col2:
        sender_name = st.text_input("差出人の名前（任意）", placeholder="例: 田中様")
        my_name = st.text_input("自分の名前（署名用・任意）", placeholder="例: 山田太郎")

    note = st.text_area("追加で伝えたいこと（任意）", placeholder="例: 来週の月曜日以降であれば対応可能です", height=80)

    if st.button("返信文を生成", type="primary", disabled=not received):
        with st.spinner("返信文を生成中..."):
            prompt = f"""以下の受信メールに対する返信文を作成してください。

【受信メール】
{received}

【条件】
- 文体: {reply_tone}
- 返信の意図: {intent}
- 差出人の名前: {sender_name if sender_name else "相手"}
- 署名の名前: {my_name if my_name else "（名前）"}
- 追加で伝えたいこと: {note if note else "特になし"}

件名の提案も含めて、実際に送信できる返信メールの全文を作成してください。"""
            result = generate(prompt, api_key=api_key_input.strip() or None)
        result_area(result)


# ── 文章要約 ────────────────────────────────────────────────────
elif tool == "summary":
    st.title("📋 文章要約")
    st.markdown("長い文章を貼り付けると、指定した形式で要約します。")

    text = st.text_area("要約したい文章", placeholder="ここに文章を貼り付けてください", height=250)
    col1, col2 = st.columns(2)
    with col1:
        summary_length = st.selectbox("要約の長さ", ["3行以内", "100字以内", "200字以内", "箇条書き5点", "箇条書き10点"])
    with col2:
        summary_style = st.selectbox("要約スタイル", ["重要ポイントを抽出", "結論を中心にまとめる", "時系列でまとめる", "Q&A形式"])

    if st.button("要約する", type="primary", disabled=not text):
        with st.spinner("要約中..."):
            prompt = f"""以下の文章を要約してください。

【文章】
{text}

【条件】
- 要約の長さ: {summary_length}
- 要約スタイル: {summary_style}

指定した条件に従って要約してください。"""
            result = generate(prompt, api_key=api_key_input.strip() or None)
        result_area(result)


# ── 文章校正・改善 ───────────────────────────────────────────────
elif tool == "proofread":
    st.title("🔍 文章校正・改善")
    st.markdown("文章を入力すると、誤字脱字・表現の改善・読みやすさの向上を行います。")

    text = st.text_area("校正したい文章", placeholder="ここに文章を貼り付けてください", height=250)
    fix_options = st.multiselect(
        "改善する項目",
        ["誤字・脱字の修正", "文法・表現の改善", "読みやすさの向上", "敬語・丁寧語の統一", "冗長な表現の削除"],
        default=["誤字・脱字の修正", "文法・表現の改善"],
    )

    if st.button("校正する", type="primary", disabled=not text):
        with st.spinner("校正中..."):
            prompt = f"""以下の文章を校正・改善してください。

【文章】
{text}

【改善する項目】
{chr(10).join(f"- {o}" for o in fix_options)}

まず修正点の一覧を箇条書きで示し、その後に改善後の全文を出力してください。"""
            result = generate(prompt, api_key=api_key_input.strip() or None)
        result_area(result)


# ── SNS投稿文生成 ────────────────────────────────────────────────
elif tool == "sns":
    st.title("📱 SNS投稿文生成")
    st.markdown("内容を入力すると、各SNSに最適化した投稿文を生成します。")

    content = st.text_area("投稿したい内容・伝えたいこと", placeholder="例: 新しいカフェに行ってきた。コーヒーが美味しかった。", height=150)
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("プラットフォーム", ["X（Twitter）", "Instagram", "Facebook", "LinkedIn", "Threads"])
        sns_tone = st.selectbox("投稿のトーン", ["カジュアル・フレンドリー", "丁寧・フォーマル", "エンタメ・面白い", "感動・共感", "情報提供・教育的"])
    with col2:
        hashtag = st.checkbox("ハッシュタグを含める", value=True)
        emoji_use = st.checkbox("絵文字を含める", value=True)

    if st.button("投稿文を生成", type="primary", disabled=not content):
        with st.spinner("投稿文を生成中..."):
            prompt = f"""以下の内容をもとに、{platform}向けの投稿文を生成してください。

【伝えたい内容】
{content}

【条件】
- プラットフォーム: {platform}
- トーン: {sns_tone}
- ハッシュタグ: {"含める" if hashtag else "含めない"}
- 絵文字: {"積極的に使う" if emoji_use else "使わない"}

{platform}の文字数制限や特徴に合わせた投稿文を作成してください。複数のバリエーション（3案）を提案してください。"""
            result = generate(prompt, api_key=api_key_input.strip() or None)
        result_area(result)


# ── タイトル・見出し生成 ─────────────────────────────────────────
elif tool == "title":
    st.title("🏷️ タイトル・見出し生成")
    st.markdown("記事の内容や概要を入力すると、魅力的なタイトルや見出しを複数提案します。")

    content = st.text_area("記事の内容・概要", placeholder="例: Pythonを使ったWebスクレイピングの入門記事。BeautifulSoupの使い方を解説する。", height=150)
    col1, col2 = st.columns(2)
    with col1:
        title_type = st.selectbox("生成するもの", ["記事タイトルのみ", "見出し構成（H2/H3）のみ", "タイトル＋見出し構成"])
        count = st.slider("提案数", min_value=3, max_value=10, value=5)
    with col2:
        title_style = st.multiselect(
            "タイトルのスタイル",
            ["数字を使う（例: 5つの方法）", "疑問形", "ハウツー形式", "驚き・インパクト重視", "SEO重視"],
            default=["数字を使う（例: 5つの方法）", "ハウツー形式"],
        )

    if st.button("生成する", type="primary", disabled=not content):
        with st.spinner("生成中..."):
            prompt = f"""以下の内容に基づいて{title_type}を生成してください。

【記事の内容・概要】
{content}

【条件】
- 提案数: {count}案
- スタイル: {", ".join(title_style) if title_style else "制限なし"}

読者がクリックしたくなる魅力的な{title_type}を提案してください。"""
            result = generate(prompt, api_key=api_key_input.strip() or None)
        result_area(result)


# ── トーン変換 ──────────────────────────────────────────────────
elif tool == "tone":
    st.title("🔄 トーン変換")
    st.markdown("文章の雰囲気・文体を変換します。")

    text = st.text_area("変換したい文章", placeholder="ここに文章を貼り付けてください", height=200)
    col1, col2 = st.columns(2)
    with col1:
        from_tone = st.selectbox("現在の文体", ["カジュアル", "フォーマル・ビジネス", "口語・話し言葉", "学術・専門的", "その他"])
    with col2:
        to_tone = st.selectbox("変換後の文体", ["フォーマル・ビジネス", "カジュアル", "丁寧・敬語", "シンプル・平易", "学術・専門的", "親しみやすい"])

    if st.button("変換する", type="primary", disabled=not text):
        with st.spinner("変換中..."):
            prompt = f"""以下の文章のトーン・文体を変換してください。

【元の文章】
{text}

【変換条件】
- 現在の文体: {from_tone}
- 変換後の文体: {to_tone}

内容・意味は変えずに、指定した文体に変換した文章を出力してください。"""
            result = generate(prompt, api_key=api_key_input.strip() or None)
        result_area(result)


# ── キャッチコピー生成 ───────────────────────────────────────────
elif tool == "catchcopy":
    st.title("💡 キャッチコピー生成")
    st.markdown("商品・サービス・ブランドの情報を入力すると、刺さるキャッチコピーを提案します。")

    subject = st.text_input("商品・サービス・ブランド名", placeholder="例: オーガニックコーヒー「森の朝」")
    description = st.text_area("特徴・強み・ターゲット", placeholder="例: 農薬不使用の豆を使用。朝の時間をゆっくり楽しみたい30〜50代向け。", height=120)
    col1, col2 = st.columns(2)
    with col1:
        copy_style = st.multiselect(
            "キャッチコピーのスタイル",
            ["感情に訴える", "ベネフィット訴求", "問題解決型", "ユーモア・遊び心", "高級感・プレミアム", "シンプル・ストレート"],
            default=["感情に訴える", "ベネフィット訴求"],
        )
        copy_count = st.slider("提案数", min_value=5, max_value=15, value=8)
    with col2:
        use_case = st.selectbox("使用用途", ["Web広告", "SNS", "チラシ・印刷物", "商品パッケージ", "動画広告", "汎用"])

    if st.button("キャッチコピーを生成", type="primary", disabled=not subject):
        with st.spinner("生成中..."):
            prompt = f"""以下の情報をもとに、魅力的なキャッチコピーを生成してください。

【対象】
{subject}

【特徴・強み・ターゲット】
{description if description else "特になし"}

【条件】
- スタイル: {", ".join(copy_style) if copy_style else "制限なし"}
- 提案数: {copy_count}案
- 使用用途: {use_case}

短くて記憶に残る、インパクトのあるキャッチコピーを{copy_count}案提案してください。各案に一言コメントも添えてください。"""
            result = generate(prompt, api_key=api_key_input.strip() or None)
        result_area(result)

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def generate(prompt: str, api_key: str | None = None) -> str:
    api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません。サイドバーにAPIキーを入力するか、.env ファイルを確認してください。")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text

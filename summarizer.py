from google import genai
from google.genai import types
import time
import logging
from config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)


def summarize_article(title: str, text: str, lang: str) -> str:
    if not text and not title:
        return "（本文なし）"

    if lang == "ja":
        prompt = f"""以下の記事を3〜4文で要約してください。
思考力・教育・認知科学に関するポイントを中心に、齊藤（思考研究家）が読んで参考になる内容を抽出してください。

タイトル: {title}
本文: {text}

要約（日本語で）:"""
    else:
        prompt = f"""以下の英語記事を日本語で3〜4文に要約してください。
思考力・教育・認知科学に関するポイントを中心に、齊藤（思考研究家）が読んで参考になる内容を抽出してください。

Title: {title}
Content: {text}

要約（日本語で）:"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                http_options=types.HttpOptions(timeout=30),
            ),
        )
        return response.text.strip()
    except Exception as e:
        logger.warning(f"要約失敗: {e}")
        return f"（要約取得失敗: {title[:30]}）"


def summarize_batch(articles: list, max_articles: int = 30) -> list:
    articles = articles[:max_articles]
    results = []
    for i, article in enumerate(articles):
        logger.info(f"要約中 {i+1}/{len(articles)}: {article['title'][:40]}")
        summary = summarize_article(
            article["title"],
            article.get("original_text", ""),
            article.get("original_lang", "en"),
        )
        article["summary_ja"] = summary
        results.append(article)
        time.sleep(0.5)
    return results

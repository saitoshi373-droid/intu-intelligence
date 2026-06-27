import requests
import time
import logging
from config import GROQ_API_KEY

logger = logging.getLogger(__name__)

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json",
}


def summarize_article(title: str, text: str, lang: str) -> str:
    if not title:
        return "（タイトルなし）"
    if not text or len(text.strip()) < 30:
        return f"（本文未取得 — タイトル: {title[:40]}）"

    if lang == "ja":
        prompt = f"""以下の記事を3〜4文で要約してください。
思考力・教育・認知科学に関するポイントを中心に抽出してください。

タイトル: {title}
本文: {text[:800] if text else "（本文なし）"}

要約（日本語で）:"""
    else:
        prompt = f"""以下の英語記事のタイトルと内容を日本語に翻訳・要約してください。
タイトルの日本語訳と、3〜4文の内容要約を出力してください。

形式：
【タイトル訳】〇〇〇
【要約】〇〇〇

Title: {title}
Content: {text[:800] if text else "(no content)"}"""

    for attempt in range(3):
        try:
            res = requests.post(
                GROQ_URL,
                headers=HEADERS,
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 300,
                    "temperature": 0.3,
                },
                timeout=15,
            )
            if res.status_code == 429:
                wait = 10 * (attempt + 1)
                logger.warning(f"429 Rate limit、{wait}秒待機...")
                time.sleep(wait)
                continue
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.warning(f"要約失敗 (attempt {attempt+1}): {e}")
            time.sleep(5)
    return f"（要約失敗: {title[:30]}）"


def summarize_batch(articles: list, max_articles: int = 50) -> list:
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
        time.sleep(2.0)
    return results

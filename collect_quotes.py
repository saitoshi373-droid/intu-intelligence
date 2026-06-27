"""
思考力・学習・教育に関する偉人の名言をGroqで収集してDBに保存
"""
import requests
import time
import logging
import json
from config import GROQ_API_KEY
from database import upsert_articles

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json",
}

THEMES = [
    ("critical thinking", "批判的思考・自分の頭で考える"),
    ("curiosity and questioning", "好奇心・問いを持つ"),
    ("learning and education", "学ぶことの本質・教育の目的"),
    ("knowledge vs wisdom", "知識と知恵の違い"),
    ("imagination and creativity", "創造性・想像力"),
    ("failure and growth", "失敗と成長・試行錯誤"),
    ("reading and thinking", "読書・思索の価値"),
    ("self-improvement and reflection", "自己成長・内省"),
]


def fetch_quotes_for_theme(theme_en: str, theme_ja: str) -> list:
    prompt = f"""List 5 famous quotes about "{theme_en}" from well-known historical figures, philosophers, scientists, or educators.

Output in this exact JSON format:
[
  {{
    "person": "Name in English",
    "person_ja": "Name in Japanese",
    "title": "their role (e.g. physicist, philosopher)",
    "title_ja": "their role in Japanese",
    "quote": "the exact famous quote in English",
    "quote_ja": "Japanese translation of the quote",
    "relevance_ja": "why this relates to thinking ability in one sentence in Japanese"
  }}
]

Only include verified, famous quotes. Output JSON only, no other text."""

    for attempt in range(3):
        try:
            res = requests.post(
                GROQ_URL,
                headers=HEADERS,
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1200,
                    "temperature": 0.2,
                },
                timeout=30,
            )
            if res.status_code == 429:
                logger.warning("429 Rate limit、20秒待機...")
                time.sleep(20)
                continue
            res.raise_for_status()
            content = res.json()["choices"][0]["message"]["content"].strip()
            start = content.find("[")
            end = content.rfind("]") + 1
            if start == -1 or end == 0:
                logger.warning("JSON見つからず")
                return []
            data = json.loads(content[start:end])
            results = []
            seen = set()
            for item in data:
                quote = item.get("quote", "").strip()
                if not quote or quote in seen:
                    continue
                seen.add(quote)
                person = item.get("person_ja") or item.get("person", "")
                title_ja = item.get("title_ja") or item.get("title", "")
                quote_ja = item.get("quote_ja", "")
                relevance = item.get("relevance_ja", "")
                results.append({
                    "title": f"【{person}】{quote[:80]}",
                    "url": f"https://wikiquote.org/wiki/{item.get('person','').replace(' ','_')}#{abs(hash(quote)) % 99999}",
                    "source": f"{person}（{title_ja}）",
                    "category": "偉人・著名人の名言",
                    "published_date": None,
                    "summary_ja": f"👤 {person}（{title_ja}）\n\n📜 原文：{quote}\n\n🇯🇵 日本語訳：{quote_ja}\n\n💡 思考力との関連：{relevance}\n\n🏷️ テーマ：{theme_ja}",
                    "original_lang": "ja",
                })
            return results
        except json.JSONDecodeError as e:
            logger.warning(f"JSONパース失敗: {e}")
            time.sleep(5)
        except Exception as e:
            logger.warning(f"取得失敗: {e}")
            time.sleep(5)
    return []


def main():
    all_articles = []
    seen_quotes = set()

    for theme_en, theme_ja in THEMES:
        logger.info(f"テーマ取得中: {theme_ja}")
        quotes = fetch_quotes_for_theme(theme_en, theme_ja)
        new = [q for q in quotes if q["title"] not in seen_quotes]
        for q in new:
            seen_quotes.add(q["title"])
        logger.info(f"  → {len(new)}件（重複除去後）")
        all_articles.extend(new)
        time.sleep(5.0)

    logger.info(f"合計 {len(all_articles)} 件を保存中...")
    saved = upsert_articles(all_articles)
    logger.info(f"✅ 保存完了: {saved}件")


if __name__ == "__main__":
    main()

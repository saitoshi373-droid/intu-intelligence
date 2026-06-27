"""
偉人の名言をWikiquoteから収集してDBに保存する（一回限りの大量取得）
"""
import requests
import time
import logging
from database import upsert_articles
from summarizer import summarize_article

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

THINKERS = [
    "Socrates", "Aristotle", "Plato", "Confucius",
    "John Dewey", "Jean Piaget", "Lev Vygotsky",
    "Albert Einstein", "Richard Feynman", "Carl Sagan",
    "Benjamin Franklin", "Abraham Lincoln", "Winston Churchill",
    "Nelson Mandela", "Mahatma Gandhi", "Martin Luther King Jr.",
    "Steve Jobs", "Peter Drucker", "Warren Buffett",
    "Friedrich Nietzsche", "Immanuel Kant", "René Descartes",
    "Blaise Pascal", "Leonardo da Vinci", "Isaac Newton",
]

WIKIQUOTE_API = "https://en.wikiquote.org/w/api.php"


def fetch_quotes(person: str) -> list:
    params = {
        "action": "parse",
        "page": person,
        "prop": "wikitext",
        "format": "json",
    }
    try:
        res = requests.get(WIKIQUOTE_API, params=params, timeout=10,
                          headers={"User-Agent": "intu-intelligence/1.0 (saitoshi373@gmail.com)"})
        res.raise_for_status()
        wikitext = res.json().get("parse", {}).get("wikitext", {}).get("*", "")

        import re
        lines = wikitext.split("\n")
        quotes = []
        for line in lines:
            line = line.strip()
            if line.startswith("*") and len(line) > 20:
                clean = re.sub(r"\[\[.*?\]\]|\{\{.*?\}\}|<.*?>|''+", "", line)
                clean = clean.lstrip("* ").strip()
                if len(clean) > 20 and len(clean) < 500:
                    quotes.append(clean)
        return quotes[:20]
    except Exception as e:
        logger.warning(f"{person} 取得失敗: {e}")
        return []


def is_relevant_quote(quote: str) -> bool:
    """思考力・学習・知性・教育に関係する名言かどうかをキーワードで判定"""
    keywords = [
        "think", "thought", "mind", "knowledge", "learn", "education",
        "wisdom", "intelligence", "reason", "understand", "question",
        "curious", "idea", "truth", "logic", "reflect", "study",
        "teach", "discover", "know", "believe", "imagine", "creative",
        "考", "思", "知", "学", "智", "理", "問",
    ]
    lower = quote.lower()
    return any(kw in lower for kw in keywords)


def main():
    all_articles = []
    for person in THINKERS:
        logger.info(f"取得中: {person}")
        quotes = fetch_quotes(person)
        filtered = [q for q in quotes if is_relevant_quote(q)]
        logger.info(f"  → {len(quotes)}件取得 → フィルター後{len(filtered)}件")
        for quote in filtered:
            summary = summarize_article(
                title=f"{person}: {quote[:50]}",
                text=quote,
                lang="en",
            )
            all_articles.append({
                "title": f"【{person}】{quote[:60]}",
                "url": f"https://en.wikiquote.org/wiki/{person.replace(' ', '_')}",
                "source": "Wikiquote",
                "category": "偉人・著名人の名言",
                "published_date": None,
                "summary_ja": summary,
                "original_lang": "en",
            })
            time.sleep(3.0)
        time.sleep(2.0)

    logger.info(f"合計 {len(all_articles)} 件の名言を保存中...")
    saved = upsert_articles(all_articles)
    logger.info(f"✅ 保存完了: {saved}件")


if __name__ == "__main__":
    main()

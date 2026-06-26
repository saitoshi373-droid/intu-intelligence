import feedparser
import requests
import re
from datetime import datetime, timezone
from typing import List, Dict
import time
import logging
from config import RSS_SOURCES, KEYWORDS_FILTER

BROAD_SOURCES = {"Big Think", "The Marginalian", "Brain Pickings / The Marginalian", "Aeon - Education"}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def fetch_feed(source_name: str, url: str, category: str) -> List[Dict]:
    articles = []
    try:
        feed = feedparser.parse(url, request_headers={"User-Agent": "Mozilla/5.0"})
        for entry in feed.entries[:10]:
            pub_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
            else:
                pub_date = datetime.now(timezone.utc)

            summary_raw = ""
            if hasattr(entry, "summary"):
                summary_raw = entry.summary[:500]
            elif hasattr(entry, "description"):
                summary_raw = entry.description[:500]

            summary_raw = re.sub(r"<[^>]+>", "", summary_raw).strip()

            title = entry.get("title", "")
            if source_name in BROAD_SOURCES:
                combined = (title + " " + summary_raw).lower()
                if not any(kw.lower() in combined for kw in KEYWORDS_FILTER):
                    continue

            articles.append({
                "title": title,
                "url": entry.get("link", ""),
                "source": source_name,
                "category": category,
                "published_date": pub_date.isoformat() if pub_date else None,
                "original_text": summary_raw,
                "original_lang": "ja" if _is_japanese(entry.get("title", "")) else "en",
            })
        logger.info(f"✅ {source_name}: {len(articles)}件取得")
    except Exception as e:
        logger.warning(f"❌ {source_name} 取得失敗: {e}")
    return articles


def _is_japanese(text: str) -> bool:
    for ch in text:
        if "　" <= ch <= "鿿" or "＀" <= ch <= "￯":
            return True
    return False


def scrape_all() -> List[Dict]:
    all_articles = []
    for category, sources in RSS_SOURCES.items():
        for source_name, url in sources:
            articles = fetch_feed(source_name, url, category)
            all_articles.extend(articles)
            time.sleep(0.5)
    logger.info(f"📦 合計取得: {len(all_articles)}件")
    return all_articles

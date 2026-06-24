from supabase import create_client, Client
from typing import List, Dict
import logging
from config import SUPABASE_URL, SUPABASE_KEY

logger = logging.getLogger(__name__)

_client: Client = None


def get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


def upsert_articles(articles: List[Dict]) -> int:
    client = get_client()
    saved = 0
    for article in articles:
        try:
            existing = (
                client.table("articles")
                .select("id")
                .eq("url", article["url"])
                .execute()
            )
            if existing.data:
                continue

            client.table("articles").insert({
                "title": article["title"],
                "url": article["url"],
                "source": article["source"],
                "category": article["category"],
                "published_date": article.get("published_date"),
                "summary_ja": article.get("summary_ja", ""),
                "original_lang": article.get("original_lang", "en"),
            }).execute()
            saved += 1
        except Exception as e:
            logger.warning(f"保存失敗: {article.get('title', '')[:40]} — {e}")
    logger.info(f"💾 新規保存: {saved}件")
    return saved


def fetch_articles(category: str = None, keyword: str = None, limit: int = 100) -> List[Dict]:
    client = get_client()
    query = client.table("articles").select("*").order("published_date", desc=True).limit(limit)
    if category and category != "すべて":
        query = query.eq("category", category)
    if keyword:
        query = query.ilike("title", f"%{keyword}%")
    result = query.execute()
    return result.data or []


def fetch_new_articles_this_week() -> List[Dict]:
    from datetime import datetime, timedelta, timezone
    client = get_client()
    week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    result = (
        client.table("articles")
        .select("*")
        .gte("created_at", week_ago)
        .order("category")
        .execute()
    )
    return result.data or []


def fetch_categories() -> List[str]:
    client = get_client()
    result = client.table("articles").select("category").execute()
    categories = sorted(set(row["category"] for row in result.data or []))
    return ["すべて"] + categories

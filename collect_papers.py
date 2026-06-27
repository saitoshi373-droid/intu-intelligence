"""
Semantic ScholarとPubMedから思考力・教育関連論文を収集（一回限りの大量取得）
"""
import requests
import time
import logging
from database import upsert_articles
from summarizer import summarize_article

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

SEARCH_QUERIES = [
    ("思考力・認知科学", "critical thinking education"),
    ("思考力・認知科学", "metacognition learning"),
    ("脳科学・神経科学", "neuroscience learning brain"),
    ("脳科学・神経科学", "cognitive development children"),
    ("心理学・マインドセット", "growth mindset academic achievement"),
    ("心理学・マインドセット", "self-regulated learning"),
    ("海外の教育", "education reform PISA"),
    ("EdTech・教育テクノロジー", "educational technology learning outcomes"),
    ("哲学・論理学", "philosophy education critical reasoning"),
    ("ビジネス×思考力", "problem solving creativity business"),
]

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"


def fetch_papers_semantic(query: str, category: str, limit: int = 20) -> list:
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,abstract,year,authors,url,externalIds",
        "sort": "citationCount",
    }
    try:
        res = requests.get(SEMANTIC_SCHOLAR_API, params=params, timeout=15)
        res.raise_for_status()
        papers = res.json().get("data", [])
        results = []
        for p in papers:
            if not p.get("title") or not p.get("abstract"):
                continue
            authors = ", ".join(a["name"] for a in p.get("authors", [])[:3])
            year = p.get("year", "")
            doi = p.get("externalIds", {}).get("DOI", "")
            url = f"https://doi.org/{doi}" if doi else p.get("url", "")
            if not url:
                continue
            results.append({
                "title": p["title"],
                "url": url,
                "source": f"Semantic Scholar ({authors})",
                "category": category,
                "published_date": f"{year}-01-01" if year else None,
                "original_text": p["abstract"][:800],
                "original_lang": "en",
            })
        return results
    except Exception as e:
        logger.warning(f"Semantic Scholar失敗 ({query}): {e}")
        return []


def main():
    all_articles = []
    for category, query in SEARCH_QUERIES:
        logger.info(f"検索中: {query} [{category}]")
        papers = fetch_papers_semantic(query, category, limit=15)
        logger.info(f"  → {len(papers)}件取得")
        for paper in papers:
            summary = summarize_article(
                title=paper["title"],
                text=paper.get("original_text", ""),
                lang="en",
            )
            paper["summary_ja"] = summary
            all_articles.append(paper)
            time.sleep(2.0)
        time.sleep(2.0)

    logger.info(f"合計 {len(all_articles)} 件を保存中...")
    saved = upsert_articles(all_articles)
    logger.info(f"✅ 保存完了: {saved}件")


if __name__ == "__main__":
    main()

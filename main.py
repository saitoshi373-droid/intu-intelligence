import logging
from scraper import scrape_all
from summarizer import summarize_batch
from database import upsert_articles, fetch_new_articles_this_week
from email_sender import send_weekly_report

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def run():
    logger.info("=== 思考力情報収集システム 週次実行開始 ===")

    logger.info("① RSSフィード収集中...")
    articles = scrape_all()

    if not articles:
        logger.warning("記事が取得できませんでした。終了します。")
        return

    logger.info(f"② Gemini APIで要約生成中（{len(articles)}件）...")
    articles_with_summary = summarize_batch(articles)

    logger.info("③ Supabaseに保存中...")
    saved_count = upsert_articles(articles_with_summary)

    logger.info("④ 今週の新着記事を取得中...")
    new_articles = fetch_new_articles_this_week()

    logger.info(f"⑤ メール送信中（新着{len(new_articles)}件）...")
    send_weekly_report(new_articles)

    logger.info(f"=== 完了: 新規保存 {saved_count}件 ===")


if __name__ == "__main__":
    run()

import streamlit as st
import pandas as pd
from database import fetch_articles, fetch_categories

st.set_page_config(
    page_title="思考力インテリジェンス",
    page_icon="🧠",
    layout="wide",
)

st.markdown("""
<style>
  .article-card {
    background: #f8fafc;
    border-left: 4px solid #2563eb;
    padding: 16px;
    border-radius: 6px;
    margin-bottom: 16px;
  }
  .article-title { font-weight: bold; font-size: 16px; color: #1a1a2e; }
  .article-meta { font-size: 12px; color: #888; margin: 4px 0 8px; }
  .article-summary { font-size: 14px; line-height: 1.8; color: #444; }
  .category-badge {
    display: inline-block;
    background: #dbeafe;
    color: #1d4ed8;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
  }
</style>
""", unsafe_allow_html=True)

st.title("🧠 思考力インテリジェンス")
st.caption("思考力・教育・認知科学に関する世界の最新情報を自動収集")

with st.sidebar:
    st.header("🔍 絞り込み")
    try:
        categories = fetch_categories()
    except Exception:
        categories = ["すべて"]

    selected_category = st.selectbox("カテゴリ", categories)
    keyword = st.text_input("キーワード検索", placeholder="例: メタ認知、クリティカルシンキング")
    limit = st.slider("表示件数", 10, 200, 50)
    st.markdown("---")
    st.caption("毎週月曜日 午前6時（JST）に自動更新")

try:
    articles = fetch_articles(
        category=selected_category if selected_category != "すべて" else None,
        keyword=keyword or None,
        limit=limit,
    )
except Exception as e:
    st.error(f"データ取得エラー: {e}\n\nSupabaseの接続設定を確認してください。")
    articles = []

if not articles:
    st.info("記事が見つかりませんでした。条件を変えて検索してみてください。")
else:
    st.markdown(f"**{len(articles)}件** 表示中")
    st.markdown("---")

    for article in articles:
        pub = article.get("published_date", "")[:10] if article.get("published_date") else "日付不明"
        lang_badge = "🇯🇵" if article.get("original_lang") == "ja" else "🌐"
        cat = article.get("category", "")
        title = article.get("title", "（タイトルなし）")
        url = article.get("url", "#")
        source = article.get("source", "")
        summary = article.get("summary_ja", "（要約なし）")

        st.markdown(f"""
<div class="article-card">
  <div class="article-title">
    {lang_badge} <a href="{url}" target="_blank" style="color:#1a1a2e;text-decoration:none;">{title}</a>
  </div>
  <div class="article-meta">
    <span class="category-badge">{cat}</span>
    &nbsp; {source} ／ {pub}
  </div>
  <div class="article-summary">{summary}</div>
</div>
""", unsafe_allow_html=True)

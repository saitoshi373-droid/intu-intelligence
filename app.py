import streamlit as st
from database import fetch_articles, fetch_categories, toggle_favorite

st.set_page_config(
    page_title="思考力インテリジェンス",
    page_icon="🧠",
    layout="wide",
)

st.markdown("""
<style>
  [data-testid="stSidebar"] { min-width: 220px; max-width: 220px; }
  .cat-header {
    font-size: 13px;
    font-weight: bold;
    color: #888;
    letter-spacing: 0.05em;
    margin: 16px 0 8px;
    text-transform: uppercase;
  }
  .article-card {
    background: #f8fafc;
    border-left: 4px solid #2563eb;
    padding: 16px 20px;
    border-radius: 6px;
    margin-bottom: 14px;
  }
  .article-card.favorite {
    border-left-color: #f59e0b;
    background: #fffbeb;
  }
  .article-title a {
    font-weight: bold;
    font-size: 15px;
    color: #1a1a2e;
    text-decoration: none;
  }
  .article-title a:hover { text-decoration: underline; }
  .article-meta { font-size: 12px; color: #888; margin: 5px 0 8px; }
  .article-summary { font-size: 13px; line-height: 1.8; color: #444; }
  .badge {
    display: inline-block;
    padding: 2px 9px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: bold;
    margin-right: 4px;
  }
  .badge-cat { background: #dbeafe; color: #1d4ed8; }
  .badge-ja  { background: #dcfce7; color: #15803d; }
  .badge-en  { background: #f1f5f9; color: #475569; }
</style>
""", unsafe_allow_html=True)

# ── サイドバー：カテゴリ一覧 ──────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 思考力インテリジェンス")
    st.caption("毎週火曜 6:00 JST 自動更新")
    st.markdown("---")
    st.markdown('<div class="cat-header">カテゴリ</div>', unsafe_allow_html=True)

    FIXED_CATS = [
        "思考力・認知科学", "日本の教育", "海外の教育",
        "脳科学・神経科学", "TQテスト関連", "アイデアクエスト関連",
        "偉人・著名人の名言", "権威・専門家の発言", "ビジネス×思考力",
        "EdTech・教育テクノロジー", "哲学・論理学", "心理学・マインドセット",
        "歴史×教育の変遷", "政府・政策動向", "競合・類似サービス",
        "動画・YouTube", "SNS上の思考力議論",
    ]
    try:
        db_cats = fetch_categories()
        extra = [c for c in db_cats if c not in FIXED_CATS and c not in ("すべて", "⭐ お気に入り")]
    except Exception:
        extra = []

    try:
        all_articles_for_count = fetch_articles(limit=1000)
        count_map = {}
        for a in all_articles_for_count:
            c = a.get("category", "")
            count_map[c] = count_map.get(c, 0) + 1
        total_count = len(all_articles_for_count)
        fav_count = sum(1 for a in all_articles_for_count if a.get("is_favorite"))
    except Exception:
        count_map = {}
        total_count = 0
        fav_count = 0

    all_cats = ["すべて", "⭐ お気に入り"] + FIXED_CATS + extra

    if "selected_cat" not in st.session_state:
        st.session_state.selected_cat = "すべて"

    for cat in all_cats:
        is_selected = st.session_state.selected_cat == cat
        if cat == "すべて":
            badge = f" ({total_count})" if total_count else ""
        elif cat == "⭐ お気に入り":
            badge = f" ({fav_count})" if fav_count else ""
        else:
            n = count_map.get(cat, 0)
            badge = f" ({n})" if n else ""
        label = f"**{cat}{badge}**" if is_selected else f"{cat}{badge}"
        if st.button(label, key=f"cat_{cat}", use_container_width=True):
            st.session_state.selected_cat = cat
            st.rerun()

    st.markdown("---")
    keyword = st.text_input("🔍 キーワード", placeholder="メタ認知、批判的思考…")
    limit = st.slider("表示件数", 10, 200, 50)

# ── メインエリア ──────────────────────────────────────────
selected = st.session_state.selected_cat
favorites_only = selected == "⭐ お気に入り"
category_filter = None if selected in ("すべて", "⭐ お気に入り") else selected

st.markdown(f"### {selected}")

try:
    articles = fetch_articles(
        category=category_filter,
        keyword=keyword or None,
        limit=limit,
        favorites_only=favorites_only,
    )
except Exception as e:
    st.error(f"データ取得エラー: {e}")
    articles = []

if not articles:
    st.info("記事が見つかりませんでした。")
else:
    st.caption(f"{len(articles)} 件")
    for article in articles:
        art_id   = article.get("id")
        title    = article.get("title", "（タイトルなし）")
        url      = article.get("url", "#")
        source   = article.get("source", "")
        category = article.get("category", "")
        pub      = (article.get("published_date") or "")[:10] or "日付不明"
        retrieved = (article.get("retrieved_at") or article.get("created_at") or "")[:10] or "—"
        summary  = article.get("summary_ja", "（要約なし）")
        lang     = article.get("original_lang", "en")
        is_fav   = article.get("is_favorite", False)

        lang_badge = '<span class="badge badge-ja">🇯🇵 日本語</span>' if lang == "ja" else '<span class="badge badge-en">🌐 英語</span>'
        card_class = "article-card favorite" if is_fav else "article-card"

        col_card, col_star = st.columns([12, 1])
        with col_card:
            st.markdown(f"""
<div class="{card_class}">
  <div class="article-title">
    <a href="{url}" target="_blank">{title}</a>
  </div>
  <div class="article-meta">
    <span class="badge badge-cat">{category}</span>
    {lang_badge}
    {source}
    &nbsp;｜&nbsp; 公開: {pub}
    &nbsp;｜&nbsp; 取得: {retrieved}
  </div>
  <div class="article-summary">{summary}</div>
</div>
""", unsafe_allow_html=True)
        with col_star:
            star_label = "⭐" if is_fav else "☆"
            if st.button(star_label, key=f"fav_{art_id}", help="お気に入り"):
                toggle_favorite(art_id, is_fav)
                st.rerun()

"""
思考力・学習・教育に関する偉人の名言をGroqで収集してDBに保存
"""
import requests
import time
import logging
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
    "思考力・批判的思考の重要性",
    "学ぶことの本質・教育の目的",
    "知識と知恵の違い",
    "創造性・想像力の重要性",
    "問いを持つことの価値",
    "失敗と成長・試行錯誤",
    "自分の頭で考えることの重要性",
    "好奇心・探求心の価値",
]


def fetch_quotes_for_theme(theme: str) -> list:
    prompt = f"""テーマ「{theme}」に関する偉人・著名人の名言を5つ教えてください。

以下の形式で出力してください（5件、番号付き）：

1.
人物名：（日本語表記）
肩書き：（例：物理学者、哲学者、教育者など）
原文：（英語または日本語の原文）
日本語訳：（日本語訳、原文が日本語なら同じ）
思考力との関連：（なぜ思考力・教育に重要な言葉か1文で）

2.
...

有名で信頼性の高い名言のみ選んでください。"""

    try:
        res = requests.post(
            GROQ_URL,
            headers=HEADERS,
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1500,
                "temperature": 0.3,
            },
            timeout=30,
        )
        if res.status_code == 429:
            logger.warning("429 Rate limit、20秒待機...")
            time.sleep(20)
            return fetch_quotes_for_theme(theme)
        res.raise_for_status()
        return parse_quotes(res.json()["choices"][0]["message"]["content"], theme)
    except Exception as e:
        logger.warning(f"取得失敗 ({theme}): {e}")
        return []


def parse_quotes(text: str, theme: str) -> list:
    articles = []
    blocks = []
    current = []
    for line in text.split("\n"):
        line = line.strip()
        if line and line[0].isdigit() and line[1:3] in (".\n", ". ", "）", ")"):
            if current:
                blocks.append("\n".join(current))
            current = [line]
        elif line:
            current.append(line)
    if current:
        blocks.append("\n".join(current))

    for block in blocks:
        person = _extract(block, ["人物名：", "人物："])
        title = _extract(block, ["肩書き：", "肩書："])
        original = _extract(block, ["原文："])
        translation = _extract(block, ["日本語訳："])
        relevance = _extract(block, ["思考力との関連：", "関連："])

        if not person or not original:
            continue

        articles.append({
            "title": f"【{person}】{original[:80]}",
            "url": f"https://en.wikiquote.org/wiki/{person.replace(' ', '_').replace('　', '_')}#{hash(original) % 99999}",
            "source": f"Wikiquote（{person}）",
            "category": "偉人・著名人の名言",
            "published_date": None,
            "summary_ja": f"👤 {person}（{title}）\n\n📜 原文：{original}\n\n🇯🇵 日本語訳：{translation}\n\n💡 思考力との関連：{relevance}",
            "original_lang": "ja",
        })
    return articles


def _extract(text: str, keys: list) -> str:
    for key in keys:
        for line in text.split("\n"):
            if key in line:
                return line.split(key, 1)[-1].strip()
    return ""


def main():
    all_articles = []
    for theme in THEMES:
        logger.info(f"テーマ取得中: {theme}")
        quotes = fetch_quotes_for_theme(theme)
        logger.info(f"  → {len(quotes)}件")
        all_articles.extend(quotes)
        time.sleep(5.0)

    logger.info(f"合計 {len(all_articles)} 件を保存中...")
    saved = upsert_articles(all_articles)
    logger.info(f"✅ 保存完了: {saved}件")


if __name__ == "__main__":
    main()

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from typing import List, Dict
import logging
from config import GMAIL_USER, GMAIL_APP_PASSWORD, EMAIL_TO

logger = logging.getLogger(__name__)


def build_email_body(articles: List[Dict]) -> str:
    today = datetime.now().strftime("%Y年%m月%d日")

    by_category: Dict[str, List[Dict]] = {}
    for a in articles:
        by_category.setdefault(a["category"], []).append(a)

    html = f"""
<html><body style="font-family:sans-serif;max-width:700px;margin:auto;color:#333;">
<h2 style="color:#1a1a2e;">📚 思考力インテリジェンス週次レポート</h2>
<p style="color:#666;">{today} 更新 ／ 今週の新着: {len(articles)}件</p>
<hr style="border:1px solid #eee;">
"""

    for category, items in by_category.items():
        html += f'<h3 style="color:#2563eb;margin-top:28px;">▍{category}</h3>'
        for item in items[:5]:
            pub = item.get("published_date", "")[:10] if item.get("published_date") else ""
            html += f"""
<div style="margin-bottom:20px;padding:14px;background:#f8fafc;border-left:3px solid #2563eb;border-radius:4px;">
  <p style="margin:0 0 4px;font-weight:bold;">
    <a href="{item['url']}" style="color:#1a1a2e;text-decoration:none;">{item['title']}</a>
  </p>
  <p style="margin:0 0 6px;font-size:12px;color:#888;">{item['source']} ／ {pub}</p>
  <p style="margin:0;font-size:14px;line-height:1.7;">{item.get('summary_ja','')}</p>
</div>
"""

    html += """
<hr style="border:1px solid #eee;margin-top:32px;">
<p style="font-size:12px;color:#aaa;">
  このメールは思考力情報収集システムから自動送信されています。<br>
  ダッシュボード: <a href="https://your-streamlit-url.streamlit.app">こちら</a>
</p>
</body></html>
"""
    return html


def send_weekly_report(articles: List[Dict]) -> bool:
    if not articles:
        logger.info("新規記事なし。メール送信スキップ。")
        return False

    subject = f"【週次レポート】思考力インテリジェンス {datetime.now().strftime('%Y/%m/%d')} — {len(articles)}件追加"
    body_html = build_email_body(articles)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = EMAIL_TO
    msg.attach(MIMEText(body_html, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, EMAIL_TO, msg.as_string())
        logger.info(f"✉️ メール送信完了 → {EMAIL_TO}")
        return True
    except Exception as e:
        logger.error(f"メール送信失敗: {e}")
        return False

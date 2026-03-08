# integrations.py

import requests
import smtplib
from email.mime.text import MIMEText
from config import SLACK_WEBHOOK, GOOGLE_SHEET_WEBHOOK


def send_to_slack(top_articles):
    if SLACK_WEBHOOK == "":
        return
    text = "*Top AI Content Opportunities*\n"
    for article in top_articles:
        post_link = article.get("Post Link", article.get("link", "No Link"))
        platform = article.get("Platform", "Website")
        title = article.get("Title", "No Title")
        text += f"{title} ({platform})\n{post_link}\n\n"
    requests.post(SLACK_WEBHOOK, json={"text": text})
    
def send_to_google_sheet(article):
    """Send one article to Google Sheet webhook"""
    if not GOOGLE_SHEET_WEBHOOK:
        return

    payload = {
        "title": article.get("Title", ""),
        "platform": article.get("Platform", ""),
        "score": article.get("Intelligence Score", 0),
        "link": article.get("Post Link", "")
    }

    try:
        response = requests.post(GOOGLE_SHEET_WEBHOOK, json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("Google Sheet POST error:", e)
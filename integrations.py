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
    if GOOGLE_SHEET_WEBHOOK == "":
        return
    payload = {
        "title": article["Title"],
        "platform": article["Platform"],
        "score": article["Intelligence Score"],
        "link": article["Post Link"]
    }
    requests.post(GOOGLE_SHEET_WEBHOOK, json=payload)
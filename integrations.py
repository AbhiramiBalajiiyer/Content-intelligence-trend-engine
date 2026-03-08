# integrations.py
import requests
from config import SLACK_WEBHOOK, GOOGLE_SHEET_WEBHOOK

def send_to_slack(top_articles_list):
    if not top_articles_list:  # works for lists
        return

    text = "*Top 5 AI Content Opportunities*\n\n"
    for article in top_articles_list:
        title = article.get("Title", "No Title")
        link = article.get("Post Link", "No Link")
        platform = article.get("Platform", "Website")
        text += f"{title} ({platform})\n{link}\n\n"

    requests.post(SLACK_WEBHOOK, json={"text": text})

def send_to_google_sheet(article):
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
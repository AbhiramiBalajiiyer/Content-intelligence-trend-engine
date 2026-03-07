import feedparser
import requests
import re
from config import ARTICLES_PER_FEED


def clean_html(text):
    return re.sub(r"<[^>]+>", "", text or "")


def fetch_articles(feed_name, feed_url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    articles = []

    try:
        response = requests.get(feed_url, headers=headers, timeout=15)
        response.raise_for_status()

        feed = feedparser.parse(response.text)

    except Exception as e:
        print(f"Feed failed: {feed_name}")
        return []

    if not feed.entries:
        print(f"No entries: {feed_name}")
        return []

    for entry in feed.entries[:ARTICLES_PER_FEED]:

        title = entry.get("title", "")

        summary = (
            entry.get("summary")
            or entry.get("description")
            or ""
        )

        if not summary and getattr(entry, "content", None):
            summary = entry.content[0].value

        summary = clean_html(summary)

        articles.append({
            "creator": feed_name,
            "title": title,
            "link": entry.get("link", ""),
            "summary": summary,
            "published": entry.get("published", "")
        })

    return articles
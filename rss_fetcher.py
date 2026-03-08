import feedparser
import requests
import re
from config import ARTICLES_PER_FEED

def fetch_articles(feed_name, feed_url):
    articles = []
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(feed_url, headers=headers, timeout=15)
        response.raise_for_status()
        feed = feedparser.parse(response.text)

        for entry in feed.entries[:ARTICLES_PER_FEED]:
            summary = ""
            if "summary" in entry:
                summary = entry.summary
            elif "description" in entry:
                summary = entry.description
            elif "content" in entry:
                summary = entry.content[0].value

            summary = re.sub('<.*?>', '', summary)

            articles.append({
                "creator": feed_name,
                "title": entry.get("title", "No Title"),
                "link": entry.get("link", ""),
                "summary": summary[:500],
                "published": entry.get("published", ""),
                "source_url": feed_url
            })

    except Exception as e:
        print(f"Error fetching {feed_name}: {e}")

    return articles
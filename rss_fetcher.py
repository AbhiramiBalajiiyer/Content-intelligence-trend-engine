import feedparser
import re
from config import ARTICLES_PER_FEED


def fetch_articles(feed_name, feed_url):
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries[:ARTICLES_PER_FEED]:
        summary = re.sub('<.*?>', '', entry.get("summary", ""))

        articles.append({
            "creator": feed_name,
            "title": entry.title,
            "link": entry.link,
            "summary": summary,
            "published": entry.get("published", "")
        })

    return articles
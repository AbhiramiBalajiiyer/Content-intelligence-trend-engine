import feedparser
import re
from config import ARTICLES_PER_FEED


def fetch_articles(feed_name, feed_url):

    feed = feedparser.parse(feed_url)

    articles = []

    for entry in feed.entries[:ARTICLES_PER_FEED]:

        # Extract summary safely
        summary = ""

        if "summary" in entry:
            summary = entry.summary
        elif "description" in entry:
            summary = entry.description
        elif "content" in entry:
            summary = entry.content[0].value

        # Remove HTML tags
        summary = re.sub('<.*?>', '', summary)

        articles.append({

            "creator": feed_name,

            "title": entry.get("title", ""),

            "link": entry.get("link", ""),

            "summary": summary,

            "published": entry.get("published", "")

        })

    return articles
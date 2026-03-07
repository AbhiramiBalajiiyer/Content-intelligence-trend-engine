import feedparser
import requests
import re
from config import ARTICLES_PER_FEED


def _parse_feed_via_feedparser(source):
    """Return feedparser-parsed object from a URL or raw content."""
    if isinstance(source, bytes):
        return feedparser.parse(source)
    return feedparser.parse(source)


def _fetch_via_requests(url, headers=None, timeout=10):
    try:
        resp = requests.get(url, headers=headers or {}, timeout=timeout)
        if resp.status_code == 200 and resp.content:
            return resp.content
    except Exception:
        return None
    return None


def fetch_articles(feed_name, feed_url):
    """Fetch articles from the given feed URL with fallbacks for blocked feeds.

    Strategy:
    1. Try direct `feedparser.parse(feed_url)` (fast/common case).
    2. If no entries or non-200, try `requests.get` with a modern User-Agent and parse returned content.
    3. If still empty and the URL references `rsshub.app`, attempt a simple proxy via `r.jina.ai` to fetch the raw content and parse it.
    """
    articles = []
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        )
    }

    # 1) Try direct feedparser
    try:
        feed = _parse_feed_via_feedparser(feed_url)
    except Exception:
        feed = None

    # 2) If no entries, try requests with UA and parse content
    if not feed or not getattr(feed, "entries", None):
        content = _fetch_via_requests(feed_url, headers=headers)
        if content:
            try:
                feed = _parse_feed_via_feedparser(content)
            except Exception:
                feed = None

    # 3) If still empty and URL looks like rsshub (sometimes blocked), try jina.ai http proxy
    if (not feed or not getattr(feed, "entries", None)) and "rsshub.app" in feed_url:
        proxy_url = "https://r.jina.ai/http://" + feed_url.replace("https://", "").replace("http://", "")
        content = _fetch_via_requests(proxy_url, headers=headers)
        if content:
            try:
                feed = _parse_feed_via_feedparser(content)
            except Exception:
                feed = None

    # Fail-safe: if feed is still None, return empty list
    if not feed:
        return []

    entries = list(getattr(feed, "entries", []))[:ARTICLES_PER_FEED]

    for entry in entries:
        summary = re.sub('<.*?>', '', entry.get("summary", ""))

        articles.append({
            "creator": feed_name,
            "title": entry.get("title", "") if hasattr(entry, 'get') else getattr(entry, 'title', ''),
            "link": entry.get("link", "") if hasattr(entry, 'get') else getattr(entry, 'link', ''),
            "summary": summary,
            "published": entry.get("published", "") if hasattr(entry, 'get') else getattr(entry, 'published', '')
        })

    return articles
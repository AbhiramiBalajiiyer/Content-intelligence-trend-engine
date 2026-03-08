
from textblob import TextBlob
from datetime import datetime

# Helper Functions
def detect_platform(source_url):

    if not source_url:
        return "Website"

    url = source_url.lower()

    if "youtube.com" in url:
        return "YouTube"

    elif "bensbites" in url:
        return "Newsletter"

    elif "therundown" in url:
        return "Newsletter"

    elif "futuretools" in url:
        return "Newsletter"

    elif "techcrunch" in url:
        return "Website"

    elif "wired" in url:
        return "Website"

    else:
        return "Website"


def generate_script(title, summary):
    summary = summary if summary else ""
    return f"""{title} is making headlines.

{summary[:200]}...

Why does this matter?

Because this could influence the direction of the industry.

Follow for more insights."""

def calculate_viral_score(title):
    base = len(title) / 10
    sensational = ["major", "first", "reveals", "breaking", "shocking"]
    bonus = sum(2 for w in sensational if w in title.lower())
    return min(10, round(base + bonus))

# Main Analysis Function
def analyze_articles(articles):
    results = []

    for article in articles:
        text = article["title"] + " " + article.get("summary", "")

        # Sentiment
        sentiment_score = TextBlob(text).sentiment.polarity
        if sentiment_score > 0.2:
            sentiment = "Positive"
        elif sentiment_score < -0.2:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        # Simple keyword trend detection
        keywords = ["gpt", "ai", "agent", "automation", "openai", "model", "video", "tools"]
        trend_score = sum(word in text.lower() for word in keywords)

        if trend_score >= 3:
            trend_label = "Emerging Trend"
        elif trend_score == 2:
            trend_label = "Growing"
        else:
            trend_label = "Low"

        # Viral score
        viral_score = calculate_viral_score(article["title"])

        # Intelligence score (normalized)
        intelligence_score = round(viral_score * 0.5 + min(trend_score * 2, 10) * 0.3 + (2 if sentiment=="Negative" else 1)*0.2, 2)

        # Recommended action
        if intelligence_score > 8:
            recommended_action = "Post Immediately"
        elif intelligence_score > 6:
            recommended_action = "Monitor Trend"
        else:
            recommended_action = "Low Priority"

        # Platform
        platform = detect_platform(article.get("source_url", ""))

        # Build result dictionary
        results.append({
            "Creator": article.get("creator", "Unknown"),
            "Title": article["title"],
            "Topic": article["title"],
            "Post Link": article.get("link", ""),
            "Viral Rating": viral_score,
            "Trend Strength": trend_label,
            "Sentiment": sentiment,
            "Platform": platform,
            "Draft Script": generate_script(article["title"], article.get("summary", "")),
            "Intelligence Score": intelligence_score,
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Status": "New",
            "Recommended Action": recommended_action
        })

    # Sort by Intelligence Score descending
    results.sort(key=lambda x: x["Intelligence Score"], reverse=True)

    return results
import re
from collections import Counter
from datetime import datetime


def extract_keywords(text):

    words = re.findall(r"\b[A-Za-z]{4,}\b", text.lower())

    stopwords = {"this", "that", "with", "from", "have", "will", "their", "about"}

    return [w for w in words if w not in stopwords]


def analyze_sentiment(text):

    positive = ["growth", "success", "innovation", "approval", "breakthrough"]

    negative = ["risk", "controversy", "decline", "lawsuit", "problem"]

    score = sum(1 for w in positive if w in text.lower())
    score -= sum(1 for w in negative if w in text.lower())

    if score > 0:
        return "Positive Impact"
    elif score < 0:
        return "Controversial"
    else:
        return "Neutral"


def calculate_viral_score(title):

    base = len(title) / 10

    sensational = ["major", "first", "reveals", "breaking", "shocking"]

    bonus = sum(2 for w in sensational if w in title.lower())

    return min(10, round(base + bonus))


def suggest_platform(score):

    if score >= 8:
        return "LinkedIn + Twitter"
    elif score >= 6:
        return "LinkedIn"
    else:
        return "Instagram Reels"


def generate_script(title, summary):

    summary = summary or ""

    return f"""
{title} is making headlines.

{summary[:200]}...

Why does this matter?

Because this could influence the direction of the industry.

Follow for more insights.
"""


def analyze_articles(all_articles):

    all_keywords = []

    # Collect keywords from all articles
    for article in all_articles:

        text = article["title"] + " " + article.get("summary", "")

        all_keywords.extend(extract_keywords(text))

    keyword_counts = Counter(all_keywords)

    results = []

    # Analyze each article
    for article in all_articles:

        text = article["title"] + " " + article.get("summary", "")

        keywords = extract_keywords(text)

        trend_score = sum(keyword_counts[k] for k in keywords[:5])

        if trend_score > 20:
            trend_label = "Emerging Trend"
        elif trend_score > 10:
            trend_label = "Growing"
        else:
            trend_label = "Low Momentum"

        viral_score = calculate_viral_score(article["title"])

        sentiment = analyze_sentiment(text)

        intelligence_score = round(
            viral_score * 0.5 +
            min(trend_score / 5, 10) * 0.3 +
            (2 if sentiment == "Controversial" else 1) * 0.2,
            2
        )

        results.append({

            "Creator": article.get("creator", "Unknown"),

            "Title": article["title"],

            "Topic": article["title"],

            "Post Link": article.get("link", ""),

            "Viral Rating": viral_score,

            "Trend Strength": trend_label,

            "Sentiment": sentiment,

            "Platform": suggest_platform(viral_score),

            "Draft Script": generate_script(
                article["title"],
                article.get("summary", "")
            ),

            "Intelligence Score": intelligence_score,

            "Date": datetime.now().strftime("%Y-%m-%d"),

            "Status": "New"

        })

    # Sort by intelligence score
    results.sort(
        key=lambda x: x["Intelligence Score"],
        reverse=True
    )

    # Add ranking + action
    for i, item in enumerate(results):

        item["Priority Rank"] = i + 1

        if item["Intelligence Score"] > 8:
            item["Recommended Action"] = "Post Immediately"

        elif item["Intelligence Score"] > 6:
            item["Recommended Action"] = "Schedule This Week"

        else:
            item["Recommended Action"] = "Monitor"

    return results
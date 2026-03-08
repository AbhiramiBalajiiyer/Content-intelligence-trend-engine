# config.py

RSS_FEEDS = {
    # YouTube Channels
    "AI Explained": "https://www.youtube.com/feeds/videos.xml?channel_id=UC8butISFwT-Wl7EV0hUK0BQ",
    "Two Minute Papers": "https://www.youtube.com/feeds/videos.xml?channel_id=UCbfYPyITQ-7l4upoX8nvctg",
    "Matt Wolfe": "https://www.youtube.com/feeds/videos.xml?channel_id=UCiT9RITQ9PW6BhXK0y2jaeg",

    # AI Newsletters
    "Ben's Bites": "https://www.bensbites.co/rss",
    "The Rundown AI": "https://www.therundown.ai/rss",
    "Future Tools": "https://www.futuretools.io/news/rss.xml",

    # Tech News
    "TechCrunch AI": "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "Wired AI": "https://www.wired.com/feed/tag/ai/latest/rss"
}

ARTICLES_PER_FEED = 5  

# Slack Webhook
SLACK_WEBHOOK = "https://hooks.slack.com/services/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"

# Google Sheet webhook
GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/AKfycbzrtWrK-ThSHLLJyLH7P_nFKzMUCPCpFyl2oKWPEdBzcRUR_fi55XG6dD2iNwj8o8bW/exec"
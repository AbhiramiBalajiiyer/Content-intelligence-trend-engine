# app.py
import streamlit as st
import pandas as pd
from config import RSS_FEEDS, ARTICLES_PER_FEED
from rss_fetcher import fetch_articles
from analyzer import analyze_articles
from integrations import send_to_slack, send_to_google_sheet
from datetime import datetime

# ---------------------------
# Streamlit Config
# ---------------------------
st.set_page_config(
    page_title="Content Intelligence & Trend Prioritization Engine",
    layout="wide"
)

st.title("Content Intelligence & Trend Prioritization Engine")
st.write(
    "A multi-source content intelligence system that detects trends, "
    "analyzes sentiment, scores viral potential, and prioritizes high-impact content opportunities."
)

# ---------------------------
# Session State
# ---------------------------
if 'df' not in st.session_state:
    st.session_state['df'] = None

# ---------------------------
# Run Analysis Button
# ---------------------------
if st.button("Run Analysis", key="run_analysis"):
    all_articles = []

    for name, url in RSS_FEEDS.items():
        articles = fetch_articles(name, url)
        # Keep creator name simple
        for a in articles:
            a["creator"] = name
        all_articles.extend(articles)

    # Analyze articles
    results = analyze_articles(all_articles)
    df = pd.DataFrame(results)
    st.session_state['df'] = df
    st.success("Analysis Complete")

# ---------------------------
# Display Data
# ---------------------------
if st.session_state['df'] is not None:
    df = st.session_state['df']

    # ---------------------------
    # Metrics
    # ---------------------------
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Articles", len(df))
    col2.metric("Emerging Trends", len(df[df["Trend Strength"] == "Emerging Trend"]))
    col3.metric("Post Immediately", len(df[df["Recommended Action"] == "Post Immediately"]))
    col4.metric("Average Intelligence Score", round(df["Intelligence Score"].mean(), 2))

    st.divider()

    # ---------------------------
    # Top 5 Table
    # ---------------------------
    st.subheader("Top 5 Content Opportunities")
    top5_df = df.head(5)
    st.dataframe(top5_df, use_container_width=True)

    top5_list = top5_df.to_dict(orient="records")  # Convert to list of dicts for Slack / Sheets

    # Buttons to send Top 5
    colA, colB = st.columns(2)
    with colA:
        if st.button("Send Top 5 to Slack", key="send_slack"):
            if not top5_list:
                st.warning("No articles to send")
            else:
                send_to_slack(top5_list)
                st.success("Top 5 articles sent to Slack!")

    with colB:
        if st.button("Send Top 5 to Google Sheets", key="send_sheets"):
            if not top5_list:
                st.warning("No articles to send")
            else:
                for article in top5_list:
                    send_to_google_sheet(article)
                st.success("Top 5 articles sent to Google Sheets!")

    st.divider()

    # ---------------------------
    # Filters
    # ---------------------------
    st.subheader("Filter Content")
    col1, col2, col3 = st.columns(3)
    creator_options = ["All"] + sorted(df["Creator"].dropna().unique().tolist())
    sentiment_options = ["All"] + sorted(df["Sentiment"].dropna().unique().tolist())
    trend_options = ["All"] + sorted(df["Trend Strength"].dropna().unique().tolist())

    creator_filter = col1.selectbox("Filter by Creator", creator_options, key="creator_filter")
    sentiment_filter = col2.selectbox("Filter by Sentiment", sentiment_options, key="sentiment_filter")
    trend_filter = col3.selectbox("Filter by Trend Strength", trend_options, key="trend_filter")

    filtered_df = df.copy()
    if creator_filter != "All":
        filtered_df = filtered_df.loc[filtered_df["Creator"] == creator_filter]
    if sentiment_filter != "All":
        filtered_df = filtered_df.loc[filtered_df["Sentiment"] == sentiment_filter]
    if trend_filter != "All":
        filtered_df = filtered_df.loc[filtered_df["Trend Strength"] == trend_filter]

    # ---------------------------
    # Ranked Table & Charts
    # ---------------------------
    st.subheader("Ranked Content Opportunities")
    if filtered_df.empty:
        st.warning("No articles match the selected filters.")
    else:
        st.dataframe(filtered_df, use_container_width=True)

    st.subheader("Average Intelligence Score by Creator")
    if not filtered_df.empty:
        creator_scores = filtered_df.groupby("Creator")["Intelligence Score"].mean().sort_values(ascending=False)
        st.bar_chart(creator_scores)

    st.subheader("Platform Distribution")
    if not filtered_df.empty:
        st.bar_chart(filtered_df["Platform"].value_counts())

    # ---------------------------
    # Download CSV
    # ---------------------------
    st.download_button(
        label="Download Analysis as CSV",
        data=filtered_df.to_csv(index=False),
        file_name=f"content_intelligence_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        key="download_csv"
    )

else:
    st.info("Click 'Run Analysis' to fetch articles and enable filters.")
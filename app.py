import streamlit as st
import pandas as pd
from config import RSS_FEEDS
from rss_fetcher import fetch_articles
from analyzer import analyze_articles

st.set_page_config(page_title="Content Intelligence & Trend Prioritization Engine", layout="wide")

st.title("Content Intelligence & Trend Prioritization Engine")

st.write(
    "A multi-source content analysis system that detects trends, scores viral potential, "
    "analyzes sentiment, and prioritizes high-impact publishing opportunities."
)

if st.button("Run Analysis"):

    all_articles = []

    for name, url in RSS_FEEDS.items():
        all_articles.extend(fetch_articles(name, url))

    results = analyze_articles(all_articles)

    df = pd.DataFrame(results)

    st.success("Analysis Complete")

    st.subheader("Ranked Content Opportunities")
    st.dataframe(df)

    st.subheader("Intelligence Score Distribution")
    st.bar_chart(df["Intelligence Score"])
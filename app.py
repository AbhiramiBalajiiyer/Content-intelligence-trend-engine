import streamlit as st
import pandas as pd
import logging
import traceback
from config import RSS_FEEDS
from rss_fetcher import fetch_articles
from analyzer import analyze_articles

logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="Content Intelligence & Trend Prioritization Engine",
    layout="wide"
)

def main():
    st.title("Content Intelligence & Trend Prioritization Engine")

    st.write(
        "A multi-source content intelligence system that detects trends, "
        "analyzes sentiment, scores viral potential, and prioritizes high-impact content opportunities."
    )

    if 'df' not in st.session_state:
        st.session_state['df'] = None

    try:
        if st.button("Run Analysis"):
            all_articles = []

            for name, url in RSS_FEEDS.items():
                all_articles.extend(fetch_articles(name, url))

            results = analyze_articles(all_articles)

            df = pd.DataFrame(results)
            st.session_state['df'] = df

            st.success("Analysis Complete")

        if st.session_state['df'] is not None:
            df = st.session_state['df']

            # Executive Metrics Section
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Articles", len(df))
            col2.metric(
                "Emerging Trends",
                len(df[df["Trend Strength"] == "Emerging Trend"])
            )
            col3.metric(
                "Post Immediately",
                len(df[df["Recommended Action"] == "Post Immediately"])
            )
            col4.metric(
                "Average Intelligence Score",
                round(df["Intelligence Score"].mean(), 2)
            )

            st.divider()

            # Top 5 Section
            st.subheader("Top 5 Content Opportunities")
            top5 = df.head(5)
            st.dataframe(top5, width='stretch')

            st.divider()

            # Filters Section
            st.subheader("Filter Content")
            colA, colB, colC = st.columns(3)

            # normalize values to strings and strip whitespace
            df['Creator'] = df['Creator'].fillna('Unknown').astype(str).str.strip()
            df['Sentiment'] = df['Sentiment'].fillna('Unknown').astype(str).str.strip()
            df['Trend Strength'] = df['Trend Strength'].fillna('Unknown').astype(str).str.strip()

            creator_options = ["All"] + sorted(df["Creator"].unique().tolist())
            sentiment_options = ["All"] + sorted(df["Sentiment"].unique().tolist())
            trend_options = ["All"] + sorted(df["Trend Strength"].unique().tolist())

            creator_filter = colA.selectbox("Filter by Creator", creator_options)
            sentiment_filter = colB.selectbox("Filter by Sentiment", sentiment_options)
            trend_filter = colC.selectbox("Filter by Trend Strength", trend_options)

            filtered_df = df.copy()

            if creator_filter != "All":
                filtered_df = filtered_df[filtered_df["Creator"] == creator_filter]

            if sentiment_filter != "All":
                filtered_df = filtered_df[filtered_df["Sentiment"] == sentiment_filter]

            if trend_filter != "All":
                filtered_df = filtered_df[filtered_df["Trend Strength"] == trend_filter]

            st.divider()

            # Full Ranked Table
            st.subheader("Ranked Content Opportunities")
            st.dataframe(filtered_df, width='stretch')

            st.divider()

            # Chart Section
            st.subheader("Intelligence Score Distribution")
            st.bar_chart(filtered_df["Intelligence Score"])

            st.divider()

            # Download Button
            csv = filtered_df.to_csv(index=False)

            st.download_button(
                label="Download Analysis as CSV",
                data=csv,
                file_name="content_intelligence_analysis.csv",
                mime="text/csv",
            )
        else:
            st.info("Click \"Run Analysis\" to fetch articles and enable filters.")
    except Exception as e:
        tb = traceback.format_exc()
        logging.error('Unhandled exception in app: %s', tb)
        try:
            with open('error.log', 'w') as f:
                f.write(tb)
        except Exception:
            pass
        st.error('An error occurred while starting the app. See error.log for details.')
        st.text(tb)

if __name__ == '__main__':
    main()

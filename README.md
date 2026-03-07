---
title: Content Intelligence & Trend Prioritization Engine
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.32.0"
python_version: "3.10"
app_file: app.py
pinned: false
---

# Content Intelligence & Trend Prioritization Engine (CITPE)

## Overview

Content Intelligence & Trend Prioritization Engine (CITPE) is a multi-source content intelligence system that:

- Aggregates RSS feeds from leading tech publications
- Detects cross-source keyword trends
- Performs lightweight sentiment analysis
- Scores viral potential
- Computes a composite intelligence score
- Prioritizes high-impact content opportunities
- Recommends publishing actions

The system transforms raw news signals into structured, ranked, actionable content ideas.

---

## Architecture

1. RSS ingestion layer  
2. Keyword trend detection engine  
3. Sentiment classifier  
4. Viral scoring logic  
5. Composite intelligence ranking  
6. Streamlit dashboard interface  

---

## How to Run Locally

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

---

## Deployment

This project is configured for deployment on Hugging Face Spaces using the Streamlit SDK.
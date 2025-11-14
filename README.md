# Welcome to the Global News Tracker project!

# Real-Time Global News Aggregator

This project aims to collect, process, and visualize real-time global news data from various online sources. Using a combination of RSS feeds, APIs, and web scraping, the system will identify trending topics, summarize them via an LLM, and display results on an interactive map.

---

## Overview

Features of our fully automated pipeline:
1. Collects recent articles via RSS feeds, News APIs, or web scraping.  
2. Extracts article text using web scraping tools.  
3. Processes and clusters articles with Natural Language Processing (NLP) (e.g., HDBSCAN).  
4. Summarizes content using a Large Language Model (LLM) API.  
5. Stores results in a PostgreSQL database.  
6. Visualizes global news topics on a React-based frontend using Folium.

---

## Data Sources

### RSS Feeds - Fetched from various top News sources across the World
Some example feeds:
- BBC: `http://feeds.bbci.co.uk/news/world/rss.xml`  
- Xinhua: `http://www.xinhuanet.com/english/rss/worldrss.xml`  
- NBC: `https://feeds.nbcnews.com/nbcnews/public/news`  
- The Guardian: `https://www.theguardian.com/world/rss`  
- ABC News: `https://abcnews.go.com/abcnews/internationalheadlines`  
- CBC: `https://www.cbc.ca/webfeed/rss/rss-world`

---

## Web Scraping

- **requests** — Fetch HTML pages  
- **BeautifulSoup / newspaper3k / Selenium** — Parse and extract article content  
- **feedparser** — Read and iterate through RSS feeds  
- **Multithreading** — (Possibly) speed up scraping across multiple sources  

---

## NLP and Data Processing

- **Topic Clustering:** HDBSCAN or similar to group related articles  
- **Summarization:** LLM API for short article summaries  
- **Geolocation:** Identify and store locations mentioned in the articles  

### Database Schema (Tentative)
**Tables:**
- `key_topics`: topic, latitude, longitude, articleCount, createdAt, related article URLs  
- `articles`: title, source, url, content, publishedAt, topic_id (FK)

**Hosting Options:** Neon, [Supabase](https://supabase.com/docs/reference/python/insert), or Ghost host  



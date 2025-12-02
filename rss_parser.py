import feedparser
import time
from datetime import datetime, timedelta, timezone
from langdetect import detect, LangDetectException

def parse_url(url, time_limit, verbose=False):
    recent_articles = []

    try:
        if verbose:
            print(f"\nParsing the url for {url}")
        news_feed = feedparser.parse(url)
    except Exception as e:
        #if verbose:
        print(f"Failed to parse {url} due to {e}")
        return recent_articles

    if news_feed.entries:
        try:
            first_entry = news_feed.entries[0]
            check_text = f"{first_entry.get('title', '')}: {first_entry.get('summary', '')}"
            if len(check_text) < 5 or detect(check_text) != "en":
                print(f"Skipping non-english feed: {url}")
                return []
        except LangDetectException:
            return []


    for entry in news_feed.entries:
        if not hasattr(entry, "published_parsed") or not entry.published_parsed:
            print(f"Ignoring this entry")
            continue

        published_time = datetime.fromtimestamp(
            time.mktime(entry.published_parsed), timezone.utc
        )
    
        if published_time >= time_limit:
            link = entry.get("link", "")

            clean_article = {
                "title": entry.get("title", "No title provided"),
                "published_parsed": published_time,
                "link": link,
                "summary": entry.get("summary", "No summary provided")
            }

            recent_articles.append(clean_article)
            if verbose:
                print(f'Processed the article: "{entry.title}"!')

        else:
            if verbose:
                print(f'Article: "{entry.title}" is too old!')
    return recent_articles 

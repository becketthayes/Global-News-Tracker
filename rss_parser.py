import feedparser
import time
from datetime import datetime, timedelta, timezone
from htmlScraper import fetch_html


def parse_url(url, time_limit, verbose=False):
    recent_articles = []

    try:
        if verbose:
            print(f"\nParsing the url for {url}")
        news_feed = feedparser.parse(url)
    except Exception as e:
        if verbose:
            print(f"Failed to parse {url} due to {e}")
        return recent_articles

    for entry in news_feed.entries:
        if not hasattr(entry, "published_parsed") or not entry.published_parsed:
            print(f"Ignoring this entry")
            continue

        published_time = datetime.fromtimestamp(
            time.mktime(entry.published_parsed), timezone.utc
        )
    
        if published_time >= time_limit:
            if verbose:
                print(f'Processed the article: "{entry.title}"!')
            article_link = entry.get("link", "No link provided")
            html_content = fetch_html(article_link, verbose = verbose)
            clean_article = {
                "title": entry.get("title", "No title provided"),
                "published_parsed": published_time,
                "link": entry.get("link", "No link provided"),
                "summary": entry.get("summary", "No summary provided"),
                "html_content": html_content
            }
            recent_articles.append(clean_article)
        else:
            if verbose:
                print(f'Article: "{entry.title}" is too old!')
    return recent_articles 

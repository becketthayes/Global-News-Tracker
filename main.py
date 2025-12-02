import json
import socket
from pprint import pprint
from datetime import datetime, timedelta, timezone
from rss_parser import parse_url
from opml2rss_parser.opml_to_rss import get_all_rss
from nlp import cluster_articles
import random

socket.setdefaulttimeout(3)

current_time = datetime.now(timezone.utc)
time_limit = current_time - timedelta(hours=12)

opml_feeds = get_all_rss()
urls = []
for country, feeds in opml_feeds.items():
    urls.extend(feeds.values())
print(f"Total amount of urls: {len(urls)}")

dict_articles = dict()
i = 0
for url in urls:
    if i % 10 == 0:
        print(f"Finished processing {i} urls.")
    dict_articles[url] = parse_url(url, time_limit, verbose=False)
    i += 1

count = 0
count_non_empty = 0
for key, value in dict_articles.items():
    count += len(value)
    if value:
        count_non_empty += 1
        print(key)
print(count_non_empty)
print(count)

articles_for_nlp = [article for feeds in dict_articles.values() for article in feeds]

clustered_articles = cluster_articles(articles_for_nlp)

# 2. INSPECT the results
# Group articles by their new 'cluster_id' to see the trends
from collections import defaultdict
trends = defaultdict(list)

for article in clustered_articles:
    c_id = article.get('cluster_id', -1)
    trends[c_id].append(article)

# 3. PRINT the top 5 trends
print("\n--- TOP TRENDS FOUND ---")
# Filter out -1 (noise) and sort by size
sorted_trends = sorted(trends.items(), key=lambda x: len(x[1]), reverse=True)

for cluster_id, articles in sorted_trends:
    if cluster_id == -1: continue # Skip noise
    
    print(f"\nTrend #{cluster_id} ({len(articles)} articles):")
    # Print the first 3 headlines in this trend
    for a in articles[:3]:
        print(f"  - {a['title']}")

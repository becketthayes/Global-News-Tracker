import json
import socket
from pprint import pprint
from datetime import datetime, timedelta, timezone
from rss_parser import parse_url
from opml2rss_parser.opml_to_rss import get_all_rss
from nlp import cluster_articles, get_trend_coordinates
import random
import utils
import concurrent.futures

socket.setdefaulttimeout(5)

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
    if i > 100:
        break

articles_flattened = [article for feeds in dict_articles.values() for article in feeds]
random.shuffle(articles_flattened)
articles_flattened = articles_flattened[:500]

print(f"Start parallel scraping for {len(articles_flattened)} articles!")

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    list(executor.map(utils.scrape_article, articles_flattened))

clustered_articles = cluster_articles(articles_flattened)

# 2. INSPECT the results
# Group articles by their new 'cluster_id' to see the trends
from collections import defaultdict
trends = defaultdict(list)

for article in clustered_articles:
    c_id = article.get('cluster_id', -1)
    trends[c_id].append(article)

trend_locations = get_trend_coordinates(trends)

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

utils.save_trends_to_supabase(trends, trend_locations)

"""
utils.save_articles_to_json(clustered_articles)

import umap
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import hdbscan

def visualize_trends(articles, filename="global_trends_map.png"):
    print("Generating visualization...")

    if not articles:
        print("No articles to visualize.")
        return

    # 1. Prepare Data (Same logic as nlp.py)
    corpus = []
    cluster_ids = []
    
    for a in articles:
        # Use the same text selection logic to ensure the map matches the clusters
        html_data = a.get('html_content')
        if isinstance(html_data, dict) and html_data.get('text') and len(html_data['text']) > 150:
            text = html_data['text']
        else:
            text = a.get('summary', '')
        
        corpus.append(f"{a.get('title', '')} {text}")
        # Important: We use the cluster_ID you already found!
        cluster_ids.append(a.get('cluster_id', -1)) 

    # 2. Vectorize (Text -> Numbers)
    # We need to turn text into math one last time for the plotter
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000, max_df=0.8)
    try:
        tfidf = vectorizer.fit_transform(corpus)
    except ValueError:
        print("Not enough text data to visualize.")
        return

    # 3. The "Reducer" (UMAP)
    # This squashes the 5000-dimensional math down to 2D (x, y) for the graph
    print("Running UMAP reduction (this might take a moment)...")
    reducer = umap.UMAP(n_neighbors=15, n_components=2, metric='cosine', random_state=42)
    embedding = reducer.fit_transform(tfidf)

    # 4. Plotting
    df = pd.DataFrame(embedding, columns=['x', 'y'])
    df['cluster'] = cluster_ids

    plt.figure(figsize=(12, 8))
    
    # Draw "Noise" points in faint gray
    noise_data = df[df['cluster'] == -1]
    plt.scatter(noise_data['x'], noise_data['y'], c='lightgray', s=10, alpha=0.3, label='Noise')
    
    # Draw "Trend" points in color
    clustered_data = df[df['cluster'] != -1]
    if not clustered_data.empty:
        sns.scatterplot(data=clustered_data, x='x', y='y', hue='cluster', palette='tab10', legend='full', s=50)
    
    plt.title('Global News Trends (HDBSCAN Clusters)', fontsize=16)
    plt.xlabel('UMAP Dimension 1')
    plt.ylabel('UMAP Dimension 2')
    
    # Save to file (since you have no screen on GitHub Actions)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to {filename}")

visualize_trends(articles_flattened)
"""
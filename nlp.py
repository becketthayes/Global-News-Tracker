from sklearn.feature_extraction.text import TfidfVectorizer
import hdbscan
import numpy as np

def cluster_articles(articles):
    corpus = [f"{a['title']} {a['summary']}" for a in articles]

    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000, max_df=0.8)
    tfidf = vectorizer.fit_transform(corpus)

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=3,
        metric="euclidean",
        cluster_selection_method="eom"
    )

    labels = clusterer.fit_predict(tfidf.toarray())

    for i, label in enumerate(labels):
        articles[i]["cluster_id"] = int(label)

    num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print(f"Found {num_clusters} trends from {len(articles)} articles.")

    return articles
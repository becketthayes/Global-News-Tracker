from sklearn.feature_extraction.text import TfidfVectorizer
import hdbscan
import numpy as np

import spacy
from collections import Counter
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

# Load spaCy's English NER model
nlp_spacy = spacy.load("en_core_web_sm")

# Initialize geocoder (Nominatim requires a custom user_agent)
geolocator = Nominatim(user_agent="global_news_tracker_app")

def cluster_articles(articles):
    corpus = [f"{a['title']} {a['html_content']['text']}" if a['html_content'] else f"{a['title']} {a['summary']}" for a in articles]

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

def get_trend_coordinates(trends_dict):
    print("Extracting geographic locations")

    trend_coords = {}

    for cluster_id, articles in trends_dict.items():
        if cluster_id == -1:
            continue 
            
        cluster_text = ""
        for a in articles:
            html_data = a.get('html_content')
            if isinstance(html_data, dict) and html_data.get('text'):
                cluster_text += html_data['text'] + " "
            else:
                cluster_text += a.get('summary', '') + " "
        
        doc = nlp_spacy(cluster_text)
        locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

        if not locations:
            print("    No locations found. Defaulting to 0.0, 0.0")
            trend_coords[cluster_id] = {"lat": 0.0, "lng": 0.0, "location_name": "Unknown"}
            continue

        most_common_loc = Counter(locations).most_common(1)[0][0]
        print(f"    Top location found: {most_common_loc}")

        try:
            time.sleep(1)
            location_data = geolocator.geocode(most_common_loc)

            if location_data:
                trend_coords[cluster_id] = {
                    "lat": location_data.latitude,
                    "lng": location_data.longitude,
                    "location_name": most_common_loc
                }
                print(f"    Mapped to: {location_data.latitude}, {location_data.longitude}")

            else:
                print("Geolocator failed")
                trend_coords[cluster_id] = {"lat": 0.0, "lng": 0.0, "location_name": most_common_loc}

        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            print(f"    Geocoding failed for {most_common_loc}: {e}")
            trend_coords[cluster_id] = {"lat": 0.0, "lng": 0.0, "location_name": most_common_loc}
    
    return trend_coords
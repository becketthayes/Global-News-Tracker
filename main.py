import json
import socket
from pprint import pprint
from datetime import datetime, timedelta, timezone
from rss_parser import parse_url

socket.setdefaulttimeout(10)

try:
    with open("feeds.json", "r") as f:
        urls = json.load(f)
except FileNotFoundError:
    print("feeds.json not found!")
    urls = []
except json.JSONDecodeError:
    print("feeds.json is not a valid JSON file.")
    urls = []

print(urls)

current_time = datetime.now(timezone.utc)
time_limit = current_time - timedelta(hours=12)

dict_articles = dict()
for url in urls:
    dict_articles[url] = parse_url(url, time_limit, verbose=False)

# pprint(dict_articles)
import feedparser
from pprint import pprint

url = "http://www.xinhuanet.com/english/rss/worldrss.xml"

news_feed = feedparser.parse(url)

pprint(news_feed.entries[0])
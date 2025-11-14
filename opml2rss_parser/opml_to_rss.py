import requests
from bs4 import BeautifulSoup
from pprint import pprint
from opml_parser import get_countries_with_opml

def parse_opml(url):
    print(f"Fetching OPML: {url}")
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "xml")

    rss_urls = {}

    # loop through all <outline ... xmlUrl="..."> tags in osml dictionary
    for outline in soup.find_all("outline"):
        if outline.has_attr("xmlUrl") and outline.get("type") == "rss":
            feed_name = outline.get("title", "Unknown")
            feed_url = outline["xmlUrl"]
            rss_urls[feed_name] = feed_url

    return rss_urls


countries_dict = get_countries_with_opml()
pprint(countries_dict)

full_rss_index = {}

for country, rss_urls in countries_dict.items():
    opml_url = rss_urls["without_category"]   
    rss_list = parse_opml(opml_url)

    full_rss_index[country] = rss_list

return full_rss_index


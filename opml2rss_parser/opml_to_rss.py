import requests
from bs4 import BeautifulSoup
from pprint import pprint
from opml_parser import get_countries_with_opml

def parse_opml(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "xml")

    rss_urls = {}

    # loop through all <outline ... xmlUrl="..."> tags in osml dictionary
    for outline in soup.find_all("outline"):
        if outline.has_attr("xmlUrl") and outline.get("type") == "rss":
            feed_name = outline.get("title") or outline.get("text") or "Feed Name Unkown"
            feed_url = outline["xmlUrl"]
            rss_urls[feed_name] = feed_url

    return rss_urls

def get_all_rss():
    print("Fetching RSS list for all countries from the OPML")
    countries_dict = get_countries_with_opml()
    # pprint(countries_dict)

    full_rss_index = {}

    for country, rss_urls in countries_dict.items():
        print(f"Fetching OPML: {country}") 
        opml_url = rss_urls["without_category"]  
        rss_list = parse_opml(opml_url)

        full_rss_index[country] = rss_list

    return full_rss_index

def main():
    rss_dict = get_all_rss()
    pprint(rss_dict)

    # Total RSS feeds
    per_country_counts = {country: len(feeds) for country, feeds in rss_dict.items()}
    total_feeds = sum(per_country_counts.values())

    pprint(per_country_counts)
    print("\nTOTAL RSS FEEDS FOUND:", total_feeds)
    

if __name__ == "__main__":
    main()




import requests
from bs4 import BeautifulSoup
from newspaper import Article
import json

def scrape_articles(url):
    # Step 1: fetch page HTML
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Step 2: find article links on the page (simple example)
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/world" in href or "article" in href:
            if href.startswith("http"):
                links.append(href)

    # removing duplicates
    links = list(set(links))

    articles_data = []

    # Step 3: extract real article content with newspaper3k
    for link in links[:5]:  # limit to first 5 for speed
        try:
            article = Article(link)
            article.download()
            article.parse()

            articles_data.append({
                "url": link,
                "title": article.title,
                "authors": article.authors,
                "publish_date": str(article.publish_date),
                "text": article.text[:500] + "..."  # shortened for demo
            })

        except Exception as e:
            print(f"Failed to scrape {link}: {e}")

    # Step 4: save to JSON
    with open("articles_output.json", "w", encoding="utf8") as f:
        json.dump(articles_data, f, indent=4)

    print("Saved articles_output.json")

def scrape_single_url(url):
    article_data = {}

    try:
        article = Article(url)
        article.download()
        article.parse()

        article_data = {
            "url": url,
            "title": article.title,
            "authors": article.authors,
            "publish_date": str(article.publish_date),
            "text": article.text
        }
    except Exception as e:
        print(f"Url {url} failed to scrape due to {e}")

    return article_data
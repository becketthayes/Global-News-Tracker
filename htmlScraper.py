import requests
import time

HEADERS = {
    "User-Agent":  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

def fetch_html(url, verbose=False):
    if verbose:
        print(f"   Scraping HTML from: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status() 
        return response.text
        
    except requests.RequestException as e:
        if verbose:
            print(f"  Failed to scrape {url} : {e}")
        return None

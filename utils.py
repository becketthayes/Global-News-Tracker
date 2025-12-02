import json
from scraper import scrape_single_url

def save_articles_to_json(articles, filename="debug_articles.json"):
    """
    Saves a list of article dictionaries to a JSON file for inspection.
    """
    print(f"Saving {len(articles)} articles to {filename}...")
    
    # Prepare a clean list for JSON dumping
    # We want to make sure we handle cases where 'text' might not exist yet
    # if you haven't run the scraper, or if it failed.
    debug_data = []
    
    for article in articles:
        # Create a copy or a new dict to avoid modifying the original if needed
        # We prioritize the 'text' field if it exists (from newspaper3k)
        # or 'html_content' if you stored it there. 
        # Adjust key names based on your actual dictionary structure!
        
        # Based on your scraper.py, the key is "text" inside the result of scrape_single_url
        # But in rss_parser.py you might be storing the whole result in "html_content"
        # Let's assume the structure from your main.py context where you might have flat dicts
        
        content_text = article.get("text", "") 
        
        # If you are using the structure from rss_parser.py where 
        # 'html_content' is a dictionary RETURNED by scrape_single_url:
        if isinstance(article.get("html_content"), dict):
             content_text = article["html_content"].get("text", "")
        elif isinstance(article.get("html_content"), str):
             content_text = article.get("html_content") # "No HTML content" string

        debug_entry = {
            "title": article.get("title", "No Title"),
            "link": article.get("link", "No Link"),
            "cluster_id": article.get("cluster_id", "N/A"), # If you ran clustering
            "text_preview": content_text[:200] if content_text else "EMPTY/NONE", # First 200 chars
            "full_text": content_text, # The full thing to inspect
            "is_empty": not bool(content_text) or content_text == "No HTML content"
        }
        debug_data.append(debug_entry)

    # Write to file with indentation for readability
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(debug_data, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved to {filename}")
        
        # Quick stat on empty articles
        empty_count = sum(1 for x in debug_data if x["is_empty"])
        print(f"Quick Stat: {empty_count} out of {len(articles)} articles have no text content.")
        
    except Exception as e:
        print(f"Error saving JSON: {e}")

def scrape_article(article):
    link = article.get("link")

    if link:
        html_content = scrape_single_url(link)
    else:
        html_content = {}
    article["html_content"] = html_content

    return article
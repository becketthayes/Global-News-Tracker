import requests
from bs4 import BeautifulSoup
from pprint import pprint

RAW_README_URL = "https://github.com/spians/awesome-RSS-feeds?tab=readme-ov-file"


# Download the README of github with opml for all countries
def fetch_readme():
    print("Fetching README.md html from GitHub...")
    response = requests.get(RAW_README_URL)
    response.raise_for_status()
    return response.text


def get_opml_html(readme):
    print("Fetching OPML table's html from README.md...")
    parser = BeautifulSoup(readme, "html.parser")
    tables = parser.find_all("markdown-accessiblity-table") # grab all tables in readme

    for table in tables:
        thead = table.find("thead")
        if not thead:
            continue

        headers = [th.get_text(strip=True) for th in thead.find_all("th")] # grab the texts from header

        if (
            "Country" in headers and
            "OPML" in headers and
            any("without category" in header for header in headers)
        ):
            return table

    raise ValueError("Could not find OPML table. GitHub may have changed structure.")


def get_opml_table(opml_html):
    print("Parsing OPML table's html into dictionary...")
    countries_rss = {}

    tbody = opml_html.find("tbody")
    country_block = tbody.find_all("tr")

    for row in country_block:
        cols = row.find_all("td")
        if len(cols) != 3:
            continue

        # Column 1: country name text 
        country = cols[0].get_text(strip=True)

        # Column 2: OPML with category
        with_category = cols[1].find("a")["href"]

        # Column 3: OPML without category
        without_category = cols[2].find("a")["href"]

        countries_rss[country] = {
            "with_category": with_category,
            "without_category": without_category
        }

    return countries_rss


def main():
    readme = fetch_readme()
    opml_html = get_opml_html(readme)
    table = get_opml_table(opml_html)

    pprint(table)
    print("\nWith Category vs Without Category:")
    print("• 'With Category' OPML wraps feeds inside extra <outline> tags so RSS readers can import them grouped by category.")
    print("• 'Without Category' OPML contains the same feeds but in a flat structure for readers that do NOT support category groupings.\n")


if __name__ == "__main__":
    main()
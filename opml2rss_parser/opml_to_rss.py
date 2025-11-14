import requests
from bs4 import BeautifulSoup

from opml_parser import get_countries_with_opml

countries_dict = get_countries_with_opml()
print(countries_dict)


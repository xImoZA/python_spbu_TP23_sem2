import re

import requests
from bs4 import BeautifulSoup


def get_links(url_in: str) -> set[str]:
    reqs = requests.get(url_in)
    soup = BeautifulSoup(reqs.text, "html.parser")

    urls = set()
    for link in soup.find_all("a", href=re.compile("^/wiki/[^File:]+")):
        urls.add("https://en.wikipedia.org" + link.get("href"))

    return urls

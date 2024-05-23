import re

import requests
from bs4 import BeautifulSoup


def get_links(url_in: str) -> list[str]:
    reqs = requests.get(url_in)
    soup = BeautifulSoup(reqs.text, "html.parser")

    urls = set()
    for link in soup.find_all("a", href=re.compile("^/wiki/[^File:]+")):
        urls.add("http://en.wikipedia.org" + link.get("href"))

    return list(urls)

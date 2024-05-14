import bs4
import requests


class ModelParser:
    def __init__(self, count: int) -> None:
        self.count: int = count

    async def parse_quotes(self, url: str) -> list[str]:
        quotes = []
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, "html.parser")
        tags = soup.findAll(attrs={"class": "quote__body"})

        for quote in tags:
            string = ""
            for child in quote.children:
                if isinstance(child, bs4.NavigableString):
                    if list(child.split()):
                        string += " ".join(list(child.split())) + "\n"
            if string:
                quotes.append(string)
            if len(quotes) == self.count:
                break
        return quotes

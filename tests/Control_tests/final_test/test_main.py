from src.Control_tests.final_test.get_wiki_links import get_links
from src.Control_tests.final_test.wiki_bfs import get_path, Node


def test_get_links():
    links = get_links("https://en.wikipedia.org/wiki/Axiom_of_choice")
    assert len(links) != 0


def test_get_path():
    start_url = Node("https://en.wikipedia.org/wiki/Axiom_of_choice", None)
    end_url = Node("http://en.wikipedia.org/wiki/Adolf_Hitler", start_url)
    assert get_path(end_url) == ["https://en.wikipedia.org/wiki/Axiom_of_choice", "http://en.wikipedia.org/wiki/Adolf_Hitler"]
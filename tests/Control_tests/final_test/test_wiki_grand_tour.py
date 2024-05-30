from io import StringIO

import pytest
from src.Control_tests.final_test.get_wiki_links import get_links
from src.Control_tests.final_test.main import main
from src.Control_tests.final_test.wiki_bfs import ModelClickTo, Node, get_path


class TestSubFunctions:
    def test_get_links(self) -> None:
        links = get_links("https://en.wikipedia.org/wiki/Axiom_of_choice")
        assert len(links) != 0

    def test_get_path(self) -> None:
        n1 = Node("1", None)
        n2 = Node("2", n1)
        n3 = Node("3", n2)
        assert get_path(n3) == ["1", "2", "3"]


class TestModelClickTo:
    @pytest.mark.parametrize(
        "start,end",
        [
            ("https://en.wikipedia.org/wiki/Struthas", "https://en.wikipedia.org/wiki/History_of_Sparta"),
            ("https://en.wikipedia.org/wiki/History_of_Sparta", "https://en.wikipedia.org/wiki/City-state"),
            ("https://en.wikipedia.org/wiki/Skibidi_Toilet", "https://en.wikipedia.org/wiki/Adolf_Hitler"),
            ("https://en.wikipedia.org/wiki/Toilet_humour", "https://en.wikipedia.org/wiki/Skibidi_Toilet"),
            ("https://en.wikipedia.org/wiki/Cheese", "https://en.wikipedia.org/wiki/Adolf_Hitler"),
        ],
    )
    def test_find_way(self, start, end) -> None:
        model = ModelClickTo()
        path = model.find_way(start, end, 3, True)
        if path:
            assert path[0] == start and path[-1] == end and len(path) >= 2


class TestMain:
    @pytest.mark.parametrize(
        "urls",
        [
            [
                "https://en.wikipedia.org/wiki/Struthas",
                "https://en.wikipedia.org/wiki/History_of_Sparta",
                "https://en.wikipedia.org/wiki/City-state",
            ],
            [
                "https://en.wikipedia.org/wiki/Cheese",
                "https://en.wikipedia.org/wiki/Croatia",
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
            ],
            ["https://en.wikipedia.org/wiki/Skibidi_Toilet", "https://en.wikipedia.org/wiki/Adolf_Hitler"],
            [
                "https://en.wikipedia.org/wiki/Toilet_humour",
                "https://en.wikipedia.org/wiki/Skibidi_Toilet",
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
            ],
        ],
    )
    def test_main(self, monkeypatch, urls) -> None:
        fake_output = StringIO()
        monkeypatch.setattr("sys.stdout", fake_output)
        main(urls, 3, False)
        output = fake_output.getvalue()[20:-1].split(" -> ")
        assert output[0] == urls[0] and output[-1] == urls[-1]
        for link in urls:
            assert link in output

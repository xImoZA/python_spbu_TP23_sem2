import asyncio

import hypothesis.strategies as st
from hypothesis import given, settings

from src.Control_tests.control_test_2.model import *


class TestModelParser:
    @settings(deadline=None)
    @given(st.integers(min_value=1, max_value=25))
    def test_parse_quotes(self, count: int) -> None:
        model = ModelParser(count)
        quotes = model.parse_quotes("https://башорг.рф/")
        assert len(quotes) == count and isinstance(quotes, list) and isinstance(quotes[0], str)

    @settings(deadline=None)
    @given(st.integers(min_value=1, max_value=25))
    def test_get_new(self, count: int) -> None:
        model = ModelParser(count)
        quotes = asyncio.run(model.get_new())
        assert len(quotes) == count and isinstance(quotes, list) and isinstance(quotes[0], str)

    @settings(deadline=None)
    @given(st.integers(min_value=1, max_value=25))
    def test_get_best(self, count: int) -> None:
        model = ModelParser(count)
        quotes = asyncio.run(model.get_best())
        assert len(quotes) == count and isinstance(quotes, list) and isinstance(quotes[0], str)

    @settings(deadline=None)
    @given(st.integers(min_value=1, max_value=25))
    def test_get_random(self, count: int) -> None:
        model = ModelParser(count)
        quotes = asyncio.run(model.get_random())
        assert len(quotes) == count and isinstance(quotes, list) and isinstance(quotes[0], str)

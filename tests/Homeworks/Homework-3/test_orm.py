import json

import hypothesis.strategies as st
import pytest
from hypothesis import given

from src.Homeworks.Homework_3.orm_datacls import *


class TestORM:
    @given(st.floats(), st.integers(), st.floats())
    def test_parse_json(self, speed: float, deg: int, gust: float) -> None:
        data = {"speed": speed, "deg": deg, "gust": gust}
        current_orm = Wind.parse_json(data)
        assert [getattr(current_orm, i) for i in data.keys()] == [speed, deg, gust]

    @given(st.floats(), st.integers(), st.text())
    def test_parse_json_with_subcls_and_list(self, float_arg: float, int_arg: int, str_arg: str) -> None:
        main_weather = {"temp": float_arg, "pressure": int_arg}
        weather = {"id": int_arg, "main": str_arg, "description": str_arg, "icon": str_arg}
        data = {"weather": [weather], "main": main_weather, "visibility": int_arg}
        big_orm = DayWeather.parse_json(data)
        small_orm1 = MainWeather.parse_json(main_weather)
        small_orm2 = Weather.parse_json(weather)
        assert big_orm.weather == [small_orm2] and big_orm.main == small_orm1

    def test_parse_json_errors(self) -> None:
        main = {"temp": 993.0, "pressure": 52}
        with pytest.raises(AttributeError):
            MainWeather.parse_json(main, strict=True)

    @given(st.floats(), st.integers(), st.text())
    def test_dump_json(self, float_arg: float, int_arg: int, str_arg: str) -> None:
        wind = {"speed": float_arg, "deg": int_arg, "gust": float_arg}
        weather = {"id": int_arg, "main": str_arg, "description": str_arg, "icon": str_arg}
        data = {"weather": [weather], "visibility": int_arg, "wind": wind}
        big_orm = DayWeather.parse_json(data)
        new_data = {
            "weather": [weather],
            "main": None,
            "visibility": int_arg,
            "wind": wind,
            "dt_txt": None,
        }
        assert big_orm.dump() == json.dumps(new_data)

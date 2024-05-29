import json
from dataclasses import dataclass

import hypothesis.strategies as st
import pytest
from hypothesis import given

from src.Homeworks.Homework_3.orm import ORM
from src.Homeworks.Homework_3.orm_datacls import DayWeather, MainWeather, Weather, Wind
from src.Homeworks.Homework_3.orm_error import JsonError


@dataclass
class NewDayWeather(ORM):
    main: MainWeather
    main_dict: dict


class TestORM:
    @given(st.floats(), st.integers(), st.floats())
    def test_parse_json(self, speed: float, deg: int, gust: float) -> None:
        data = {"speed": speed, "deg": deg, "gust": gust}
        current_orm = Wind.parse_json(data)
        assert [getattr(current_orm, i) for i in data.keys()] == [speed, deg, gust] and isinstance(current_orm, Wind)

    @given(st.floats(), st.integers(), st.text())
    def test_parse_json_with_subcls_and_list(self, float_arg: float, int_arg: int, str_arg: str) -> None:
        main_weather = {"temp": float_arg, "pressure": int_arg}
        weather = {"id": int_arg, "main": str_arg, "description": str_arg, "icon": str_arg}
        data = {"weather": [weather], "main": main_weather, "visibility": int_arg}
        big_orm = DayWeather.parse_json(data)
        small_orm1 = MainWeather.parse_json(main_weather)
        small_orm2 = Weather.parse_json(weather)

        final_dict2 = list(Weather.__dict__["__annotations__"].keys())
        final_dict2.append("__json__")
        assert (
            isinstance(big_orm, DayWeather)
            and isinstance(big_orm.weather, list)
            and isinstance(big_orm.weather[0], Weather)
            and big_orm.weather[0] == small_orm2
            and list(big_orm.weather[0].__dict__.keys()) == final_dict2
        )

        final_dict1 = list(MainWeather.__dict__["__annotations__"].keys())
        final_dict1.append("__json__")
        assert (
            isinstance(big_orm.main, MainWeather)
            and big_orm.main == small_orm1
            and list(big_orm.main.__dict__.keys()) == final_dict1
        )

    @given(st.floats(min_value=0), st.integers())
    def test_get_subcls_items(self, float_arg: float, int_arg: int) -> None:
        main_weather = {"temp": float_arg, "pressure": int_arg}
        data = {"main": main_weather, "main_dict": main_weather}
        big_orm = NewDayWeather.parse_json(data)
        assert (
            isinstance(big_orm, NewDayWeather)
            and isinstance(big_orm.main, MainWeather)
            and isinstance(big_orm.main_dict, dict)
        )
        assert (
            big_orm.main.temp == main_weather["temp"]
            and big_orm.main.pressure == main_weather["pressure"]
            and big_orm.main_dict == main_weather
        )

    def test_get_errors(self) -> None:
        with pytest.raises(JsonError):
            Wind("", "", "").deg

    def test_parse_json_errors(self) -> None:
        main = {"temp": 993.0, "pressure": 52}
        with pytest.raises(JsonError):
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
        assert big_orm.dump_json() == json.dumps(new_data)

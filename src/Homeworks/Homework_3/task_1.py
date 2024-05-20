from argparse import ArgumentParser
from typing import Any

import matplotlib.pyplot as plt
import requests

from src.Homeworks.Homework_3.exceptions import CityNameError
from src.Homeworks.Homework_3.ORM_dataclasses import *

API_key = "5666f2a81657a6921ab4be376b1577ba"
URL = "https://api.openweathermap.org/data/2.5/"


def get_json(url: str) -> dict[str, Any]:
    data = requests.get(url).json()
    if data.get("cod") == "404":
        raise CityNameError

    return data


def show_plot_figure(indicator: str, date: list[str], ind: list[int | float]) -> None:
    plt.figure(figsize=(10, 20))
    plt.plot(date, ind)

    plt.title(f"{indicator}")
    plt.xticks(rotation=90, fontsize=5, alpha=0.7)
    plt.grid(True)

    plt.show()


def current_weather(city: str, attr: str) -> None:
    json = get_json(f"{URL}weather?q={city}&units=metric&appid={API_key}")
    cur_weather = BigWeather.parse_json(json)
    if attr in ["temp", "feels_like", "pressure", "humidity"]:
        out_str = f"{attr}: {getattr(cur_weather.main, attr)}"
    else:
        if attr == "wind_speed":
            out_str = f"{attr}: {getattr(cur_weather.wind, 'speed')}"
        else:
            out_str = f"{attr}: {getattr(cur_weather.wind, attr)}"

    print(f"Weather in {city} now: {cur_weather.weather[0].description}, {out_str}")


def forecast_weather(city: str, attr: str, count: int) -> None:
    json = get_json(f"{URL}forecast?q={city}&units=metric&appid={API_key}")
    forecast_weather = ForecastWeather.parse_json(json)
    data = []
    date = []
    for weather in forecast_weather.list[: count * 8 + 1]:
        if attr in ["temp", "feels_like", "pressure", "humidity"]:
            data.append(getattr(weather.main, attr))
        else:
            if attr == "wind_speed":
                data.append(getattr(weather.wind, "speed"))
            else:
                data.append(getattr(weather.wind, attr))
        date.append(weather.dt_txt[5:-3])
    show_plot_figure(attr, date, data)


def main(city: str, command: str, ind: str, days: int) -> None:
    if command == "current_weather":
        current_weather(city, ind)
    else:
        forecast_weather(city, ind, days)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("city", type=str, help="City name")
    parser.add_argument("command", type=str, help="Command", choices=["current_weather", "forecast_weather"])
    parser.add_argument(
        "parameter",
        type=str,
        help="Parameter",
        choices=["temp", "feels_like", "pressure", "humidity", "wind_speed", "gust"],
    )
    parser.add_argument("---period", type=int, default=1, help="Days period", choices=[1, 2, 3, 4, 5])
    args = parser.parse_args()

    main(args.city, args.command, args.parameter, args.period)

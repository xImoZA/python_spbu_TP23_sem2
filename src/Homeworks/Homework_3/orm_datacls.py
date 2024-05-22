from dataclasses import dataclass

from src.Homeworks.Homework_3.orm import ORM


@dataclass
class Weather(ORM):
    id: int
    main: str
    description: str
    icon: str


@dataclass
class MainWeather(ORM):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int
    grnd_level: int


@dataclass
class Wind(ORM):
    speed: float
    deg: int
    gust: float


@dataclass
class DayWeather(ORM):
    weather: list[Weather]
    main: MainWeather
    visibility: int
    wind: Wind
    dt_txt: str


@dataclass
class FiveDayWeather(ORM):
    list: list[DayWeather]

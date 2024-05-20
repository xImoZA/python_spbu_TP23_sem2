from dataclasses import dataclass

from src.Homeworks.Homework_3.orm import ORM, ORMMeta


@dataclass
class Weather(ORM, metaclass=ORMMeta):
    id: int
    main: str
    description: str
    icon: str


@dataclass
class MainWeather(ORM, metaclass=ORMMeta):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int
    grnd_level: int


@dataclass
class Wind(ORM, metaclass=ORMMeta):
    speed: float
    deg: int
    gust: float


@dataclass
class Clouds(ORM, metaclass=ORMMeta):
    all: int


@dataclass
class DayWeather(ORM, metaclass=ORMMeta):
    weather: list[Weather]
    main: MainWeather
    visibility: int
    wind: Wind
    clouds: Clouds
    dt_txt: str


@dataclass
class FiveDayWeather(ORM, metaclass=ORMMeta):
    list: list[DayWeather]

class CityNameError(Exception):
    def __init__(self) -> None:
        super().__init__(f"City not found")


class JsonError(Exception):
    def __init__(self) -> None:
        super().__init__()

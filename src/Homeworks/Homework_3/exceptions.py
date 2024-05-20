class CityNameError(Exception):
    def __init__(self) -> None:
        super().__init__(f"City not found")


class DataclassAttributeError(Exception):
    def __init__(self) -> None:
        super().__init__(f"Dataclass does not match json")


class JsonError(Exception):
    def __init__(self) -> None:
        super().__init__()

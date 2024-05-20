class CityNameError(Exception):
    def __init__(self) -> None:
        super().__init__(f"City not found")


class AttributeJsonError(Exception):
    def __init__(self) -> None:
        super().__init__("JSON data is missing")

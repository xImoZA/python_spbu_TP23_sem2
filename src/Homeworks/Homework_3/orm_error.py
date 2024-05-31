class CityNameError(KeyError):
    def __init__(self) -> None:
        super().__init__(f"City not found")


class ORMError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class JsonError(ORMError):
    def __init__(self, message: str) -> None:
        super().__init__(message)

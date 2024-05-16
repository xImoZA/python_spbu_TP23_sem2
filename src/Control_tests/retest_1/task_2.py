import decimal
from typing import Generic, TypeVar

T = TypeVar("T", float, complex, int, decimal.Decimal)


class DifferentDimensionsError(Exception):
    def __init__(self) -> None:
        super().__init__(f"Vectors have different dimensions")


class VectorProductError(Exception):
    def __init__(self) -> None:
        super().__init__(f"The vector product can only be executed with vectors of dimension is 3")


class NotVectorError(Exception):
    def __init__(self) -> None:
        super().__init__(f"The operation can only be performed with elements of the 'Vector' class")


class Vector(Generic[T]):
    def __init__(self, coord: list[T]) -> None:
        self.coord: list[T] = coord

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector):
            return self.coord == other.coord
        raise NotVectorError

    def __bool__(self) -> bool:
        return bool(sum(self.coord))

    def __len__(self) -> int:
        return len(self.coord)

    def __add__(self, other: "Vector") -> "Vector":
        if len(self) == len(other):
            return Vector([self.coord[i] + other.coord[i] for i in range(len(self))])
        else:
            raise DifferentDimensionsError

    def __sub__(self, other: "Vector") -> "Vector":
        if len(self) == len(other):
            return Vector([self.coord[i] - other.coord[i] for i in range(len(self))])
        else:
            raise DifferentDimensionsError

    def __mul__(self, other: "Vector") -> T:
        if len(self) == len(other):
            return sum([self.coord[i] * other.coord[i] for i in range(len(self))])
        else:
            raise DifferentDimensionsError

    @staticmethod
    def vector_product(vector1: "Vector", vector2: "Vector") -> "Vector":
        if len(vector1) != 3 or len(vector2) != 3:
            raise VectorProductError

        return Vector(
            [
                vector1.coord[1] * vector2.coord[2] - vector1.coord[2] * vector2.coord[1],
                vector1.coord[2] * vector2.coord[0] - vector1.coord[0] * vector2.coord[2],
                vector1.coord[0] * vector2.coord[1] - vector1.coord[1] * vector2.coord[0],
            ]
        )

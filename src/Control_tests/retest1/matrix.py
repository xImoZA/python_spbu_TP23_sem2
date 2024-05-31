from typing import Any, Generic, Protocol, TypeVar


class ArithmeticAvailable(Protocol):
    def __eq__(self, other: Any) -> bool:
        pass

    def __add__(self, other: Any) -> Any:
        pass

    def __sub__(self, other: Any) -> Any:
        pass

    def __mul__(self, other: Any) -> Any:
        pass


T = TypeVar("T", bound=ArithmeticAvailable)


class MatrixError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class DifferentDimensionsError(MatrixError):
    def __init__(self) -> None:
        super().__init__(f"Matrix have different dimensions")


class MatrixProductError(MatrixError):
    def __init__(self) -> None:
        super().__init__(
            f"The matrix product can be performed only when the number of columns of the first one coincides with the number of rows of the second one"
        )


class NotMatrixError(Exception):
    def __init__(self) -> None:
        super().__init__(f"The operation can only be performed with elements of the 'Matrix' class")


class Matrix(Generic[T]):
    def __init__(self, matrix: list[list[T]]) -> None:
        self.matrix: list[list[T]] = matrix
        self.row: int = len(self.matrix)
        self.column: int = len(self.matrix[0])

        for row in self.matrix:
            if len(row) != self.column:
                raise MatrixError("The transmitted list is not a matrix")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Matrix):
            return self.matrix == other.matrix
        raise NotMatrixError

    def dimension(self) -> tuple[int, int]:
        return self.row, self.column

    def __add__(self, other: "Matrix") -> "Matrix":
        if self.dimension() != other.dimension():
            raise DifferentDimensionsError
        return Matrix([[self.matrix[i][j] + other.matrix[i][j] for j in range(self.column)] for i in range(self.row)])

    def __sub__(self, other: "Matrix") -> "Matrix":
        if self.dimension() != other.dimension():
            raise DifferentDimensionsError
        return Matrix([[self.matrix[i][j] - other.matrix[i][j] for j in range(self.column)] for i in range(self.row)])

    def __mul__(self, other: "Matrix") -> "Matrix[T]":
        if self.dimension() != other.dimension():
            raise DifferentDimensionsError
        return Matrix([[self.matrix[i][j] * other.matrix[i][j] for j in range(self.column)] for i in range(self.row)])

    def __getitem__(self, item: int) -> list[T]:
        return self.matrix[item]

    def matrix_product(self, matrix2: "Matrix") -> "Matrix":
        if self.column != matrix2.row:
            raise MatrixProductError
        new_matrix = [
            [sum([self.matrix[x][i] * matrix2.matrix[i][y] for i in range(self.column)]) for y in range(matrix2.column)]
            for x in range(self.row)
        ]

        return Matrix(new_matrix)


class IntMatrix(Matrix[int]):
    def is_unit(self) -> bool:
        if self.row != self.column:
            return False

        for i_string in range(self.row):
            row = self.matrix[i_string]
            if sum(row) != 1 or (sum(row) == 1 and row[i_string] != 1):
                return False
        return True

    def zeroing_out(self) -> None:
        self.matrix = [[0] * self.column for _ in range(self.row)]

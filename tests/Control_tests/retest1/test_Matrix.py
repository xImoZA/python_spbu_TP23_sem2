import random

import hypothesis.strategies as st
import numpy as np
import pytest
from hypothesis import given

from src.Control_tests.retest1.matrix import DifferentDimensionsError, IntMatrix, Matrix, MatrixError, NotMatrixError


class TestMatrix:
    @given(st.integers(min_value=5, max_value=10), st.integers(min_value=5, max_value=10))
    def test_init(self, row: int, column: int) -> None:
        matrix = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        del matrix[4][0]
        with pytest.raises(MatrixError):
            Matrix(matrix)

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_eq(self, row: int, column: int) -> None:
        matrix1 = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        matrix2 = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]

        m1 = Matrix(matrix1)
        m2 = Matrix(matrix2)
        assert (m1 == m2) == (matrix1 == matrix2)

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_eq_errors(self, row: int, column: int) -> None:
        matrix = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        with pytest.raises(NotMatrixError):
            Matrix(matrix) == "aboba"

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_dimension(self, row: int, column: int) -> None:
        matrix = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        assert Matrix(matrix).dimension() == (len(matrix), len(matrix[0]))

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_add(self, row: int, column: int) -> None:
        matrix1 = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        matrix2 = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        new_matrix = [[matrix1[i][j] + matrix2[i][j] for j in range(column)] for i in range(row)]

        m1 = Matrix(matrix1)
        m2 = Matrix(matrix2)
        assert m1 + m2 == Matrix(new_matrix)

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_add_errors(self, row: int, column: int) -> None:
        if row != column:
            matrix1 = Matrix([[random.randint(0, 50) for _ in range(column)] for _ in range(row)])
            matrix2 = Matrix([[random.randint(0, 50) for _ in range(row)] for _ in range(column)])

            with pytest.raises(DifferentDimensionsError):
                matrix1 + matrix2

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_sub(self, row: int, column: int) -> None:
        matrix1 = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        matrix2 = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        new_matrix = [[matrix1[i][j] - matrix2[i][j] for j in range(column)] for i in range(row)]

        m1 = Matrix(matrix1)
        m2 = Matrix(matrix2)
        assert m1 - m2 == Matrix(new_matrix)

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_sub_errors(self, row: int, column: int) -> None:
        if row != column:
            matrix1 = Matrix([[random.randint(0, 50) for _ in range(column)] for _ in range(row)])
            matrix2 = Matrix([[random.randint(0, 50) for _ in range(row)] for _ in range(column)])

            with pytest.raises(DifferentDimensionsError):
                matrix1 - matrix2

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_mul(self, row: int, column: int) -> None:
        matrix1 = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        matrix2 = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        new_matrix = [[matrix1[i][j] * matrix2[i][j] for j in range(column)] for i in range(row)]

        m1 = Matrix(matrix1)
        m2 = Matrix(matrix2)
        assert m1 * m2 == Matrix(new_matrix)

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_mul_errors(self, row: int, column: int) -> None:
        if row != column:
            matrix1 = Matrix([[random.randint(0, 50) for _ in range(column)] for _ in range(row)])
            matrix2 = Matrix([[random.randint(0, 50) for _ in range(row)] for _ in range(column)])

            with pytest.raises(DifferentDimensionsError):
                matrix1 * matrix2

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_getitem(self, row: int, column: int) -> None:
        matrix = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        m = Matrix(matrix)
        for i_row in range(len(matrix)):
            for i_column in range(len(matrix[0])):
                assert m[i_row][i_column] == matrix[i_row][i_column]

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_magic_getitem(self, row: int, column: int) -> None:
        matrix = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        m = Matrix(matrix)
        for i_row in range(len(matrix)):
            assert m[i_row] == matrix[i_row]

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_matrix_product(self, row: int, column: int) -> None:
        matrix1 = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        matrix2 = [[random.randint(0, 50) for _ in range(row)] for _ in range(column)]

        m1 = Matrix(matrix1)
        m2 = Matrix(matrix2)

        assert m1.matrix_product(m2).matrix == np.dot(np.array(matrix1), np.array(matrix2)).tolist()


class TestIntMatrix:
    @given(
        st.integers(min_value=1, max_value=10),
        st.integers(min_value=1, max_value=10),
        st.integers(min_value=1, max_value=10),
    )
    def test_is_unit(self, row: int, column: int, n: int) -> None:
        matrix = [[random.randint(0, 50) for _ in range(column)] for _ in range(row)]
        unit = [[0] * n for _ in range(n)]
        for i in range(n):
            unit[i][i] = 1

        assert IntMatrix(matrix).is_unit() is False and IntMatrix(unit).is_unit() is True

    @given(st.integers(min_value=1, max_value=10), st.integers(min_value=1, max_value=10))
    def test_zeroing_out(self, row: int, column: int) -> None:
        matrix = IntMatrix([[random.randint(0, 50) for _ in range(column)] for _ in range(row)])
        zero_matrix = [[0 for _ in range(column)] for _ in range(row)]

        matrix.zeroing_out()
        assert matrix == Matrix(zero_matrix)

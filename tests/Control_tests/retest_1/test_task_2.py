import hypothesis.strategies as st
import pytest
from hypothesis import given

from src.Control_tests.retest_1.task_2 import *


class TestVector:
    @given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
    def test_eq(self, vector1: list[int], vector2: list[int]) -> None:
        test_vector1 = Vector(vector1)
        test_vector2 = Vector(vector2)

        assert test_vector1.__eq__(test_vector1) is True and test_vector2.__eq__(test_vector2) is True

    @given(st.lists(st.integers(), min_size=1))
    def test_errors_eq(self, vector: list[int]) -> None:
        test_vector = Vector(vector)
        with pytest.raises(NotVectorError):
            test_vector.__eq__("aboba")

    @given(st.lists(st.integers(), min_size=1))
    def test_bool(self, vector: list[int]) -> None:
        test_vector = Vector(vector)
        if set(vector) == {0}:
            assert test_vector.__bool__() is False
        else:
            assert test_vector.__bool__() is True

    @given(st.lists(st.integers(), min_size=1))
    def test_len(self, vector: list[int]) -> None:
        test_vector = Vector(vector)
        assert len(test_vector) == len(vector)

    @given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
    def test_add(self, vector1: list[int], vector2: list[int]) -> None:
        test_vector1 = Vector(vector1)
        test_vector2 = Vector(vector2)

        if len(vector1) == len(vector2):
            assert test_vector1 + test_vector2 == Vector([vector1[i] + vector2[i] for i in range(len(vector2))])
        else:
            with pytest.raises(DifferentDimensionsError):
                test_vector1 + test_vector2

    @given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
    def test_sub(self, vector1: list[int], vector2: list[int]) -> None:
        test_vector1 = Vector(vector1)
        test_vector2 = Vector(vector2)

        if len(vector1) == len(vector2):
            assert test_vector1 - test_vector2 == Vector([vector1[i] - vector2[i] for i in range(len(vector2))])
            assert test_vector2 - test_vector1 == Vector([vector2[i] - vector1[i] for i in range(len(vector2))])
        else:
            with pytest.raises(DifferentDimensionsError):
                test_vector1 - test_vector2

    @given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
    def test_mul(self, vector1: list[int], vector2: list[int]) -> None:
        test_vector1 = Vector(vector1)
        test_vector2 = Vector(vector2)

        if len(vector1) == len(vector2):
            assert test_vector1 * test_vector2 == sum([vector1[i] * vector2[i] for i in range(len(vector2))])
        else:
            with pytest.raises(DifferentDimensionsError):
                test_vector1 * test_vector2

    @given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
    def test_vector_product(self, vector1: list[int], vector2: list[int]) -> None:
        test_vector1 = Vector(vector1)
        test_vector2 = Vector(vector2)

        if len(vector1) == len(vector2) == 3:
            assert Vector.vector_product(test_vector1, test_vector2) == Vector(
                [
                    vector1[1] * vector2[2] - vector1[2] * vector2[1],
                    vector1[2] * vector2[0] - vector1[0] * vector2[2],
                    vector1[0] * vector2[1] - vector1[1] * vector2[0],
                ]
            )
        else:
            with pytest.raises(VectorProductError):
                Vector.vector_product(test_vector1, test_vector2)

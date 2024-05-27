import random

import hypothesis.strategies as st
import pytest
from hypothesis import given

from src.Homeworks.Homework_2.PerformedCommandStorage import *


class TestAction:
    @given(st.lists(st.integers(), min_size=1), st.integers())
    def test_AddToStart(self, collection: list[int], value: int) -> None:
        action = AddToStart(value)
        given_collection = collection.copy()

        action.forward_action(collection)
        assert collection == [value] + given_collection

        action.reverse_action(collection)
        assert collection == given_collection

    @given(st.lists(st.integers(), min_size=1))
    def test_DeleteFromStart(self, collection: list[int]) -> None:
        action = DeleteFromStart()
        given_collection = collection.copy()

        action.forward_action(collection)
        assert collection == given_collection[1:]

        action.reverse_action(collection)
        assert collection == given_collection

    @given(st.lists(st.integers(), min_size=1), st.integers())
    def test_AddToEnd(self, collection: list[int], value: int) -> None:
        action = AddToEnd(value)
        given_collection = collection.copy()

        action.forward_action(collection)
        assert collection == given_collection + [value]

        action.reverse_action(collection)
        assert collection == given_collection

    @given(st.lists(st.integers(), min_size=1))
    def test_DeleteFromEnd(self, collection: list[int]) -> None:
        action = DeleteFromEnd()
        given_collection = collection.copy()

        action.forward_action(collection)
        assert collection == given_collection[:-1]

        action.reverse_action(collection)
        assert collection == given_collection

    @given(st.lists(st.integers(), min_size=1), st.integers())
    def test_AdditionValue(self, collection: list[int], value: int) -> None:
        i = random.randint(-len(collection), len(collection) - 1)
        action = AdditionValue(i, value)
        given_collection = collection.copy()

        action.forward_action(collection)
        given_collection[i] += value
        assert collection == given_collection

        action.reverse_action(collection)
        given_collection[i] -= value
        assert collection == given_collection

    @given(st.lists(st.integers(), min_size=1), st.integers())
    def test_SubtractingValue(self, collection: list[int], value: int) -> None:
        i = random.randint(-len(collection), len(collection) - 1)
        action = SubtractingValue(i, value)
        given_collection = collection.copy()

        action.forward_action(collection)
        given_collection[i] -= value
        assert collection == given_collection

        action.reverse_action(collection)
        given_collection[i] += value
        assert collection == given_collection

    @given(st.lists(st.integers(), min_size=1), st.integers())
    def test_InsertValue(self, collection: list[int], value: int) -> None:
        i = random.randint(-len(collection) - 1, len(collection))
        action = InsertValue(i, value)
        given_collection = collection.copy()

        action.forward_action(collection)
        assert collection == given_collection[:i] + [value] + given_collection[i:]

        action.reverse_action(collection)
        assert collection == given_collection

    @given(st.lists(st.integers(), min_size=1))
    def test_DeleteValue(self, collection: list[int]) -> None:
        i = random.randint(-len(collection), len(collection) - 1)
        action = DeleteValue(i)
        given_collection = collection.copy()

        action.forward_action(collection)
        value = given_collection.pop(i)
        assert collection == given_collection

        action.reverse_action(collection)
        if i == -1:
            given_collection.append(value)
        elif i >= 0:
            given_collection.insert(i, value)
        else:
            given_collection.insert(i + 1, value)
        assert collection == given_collection

    @given(st.lists(st.integers(), min_size=2))
    def test_Move(self, collection: list[int]) -> None:
        i = random.randint(-len(collection), len(collection) - 1)
        j = random.randint(-len(collection), len(collection) - 1)
        action = Move(i, j)
        given_collection = collection.copy()

        action.forward_action(collection)
        given_collection[i], given_collection[j] = given_collection[j], given_collection[i]
        assert collection == given_collection

        action.reverse_action(collection)
        given_collection[i], given_collection[j] = given_collection[j], given_collection[i]
        assert collection == given_collection

    @given(st.lists(st.integers(), min_size=1))
    def test_Reverse(self, collection: list[int]) -> None:
        action = Reverse()
        given_collection = collection.copy()

        action.forward_action(collection)
        assert collection == list(reversed(given_collection))

        action.reverse_action(collection)
        assert collection == given_collection

    @given(st.lists(st.integers(), min_size=1))
    def test_Clear(self, collection: list[int]) -> None:
        action = Clear()
        given_collection = collection.copy()

        action.forward_action(collection)
        assert collection == []

        action.reverse_action(collection)
        assert collection == given_collection


class TestActionException:
    def test_DeleteFromStart(self) -> None:
        action = DeleteFromStart()
        with pytest.raises(IndexError):
            action.reverse_action(st.lists(st.integers(), min_size=1).example())
        with pytest.raises(IndexError):
            action.forward_action([])

    def test_DeleteFromEnd(self) -> None:
        action = DeleteFromEnd()
        with pytest.raises(IndexError):
            action.reverse_action(st.lists(st.integers(), min_size=1).example())
        with pytest.raises(IndexError):
            action.forward_action([])

    @given(st.lists(st.integers(), min_size=1), st.integers())
    def test_AdditionValue(self, collection: list[int], value: int) -> None:
        i1 = random.randint(-(10**8), -len(collection) - 1)
        action = AdditionValue(i1, value)
        with pytest.raises(IndexError):
            action.forward_action(collection)

        i2 = random.randint(len(collection), 10**8)
        action = AdditionValue(i2, value)
        with pytest.raises(IndexError):
            action.forward_action(collection)

    @given(st.lists(st.integers(), min_size=1), st.integers())
    def test_SubtractingValue(self, collection: list[int], value: int) -> None:
        i1 = random.randint(-(10**8), -len(collection) - 1)
        action = SubtractingValue(i1, value)
        with pytest.raises(IndexError):
            action.forward_action(collection)

        i2 = random.randint(len(collection), 10**8)
        action = SubtractingValue(i2, value)
        with pytest.raises(IndexError):
            action.forward_action(collection)

    @given(st.lists(st.integers(), min_size=1), st.integers())
    def test_InsertValue(self, collection: list[int], value: int) -> None:
        i1 = random.randint(-(10**8), -len(collection) - 2)
        action = InsertValue(i1, value)
        with pytest.raises(IndexError):
            action.forward_action(collection)

        i2 = random.randint(len(collection) + 1, 10**8)
        action = InsertValue(i2, value)
        with pytest.raises(IndexError):
            action.forward_action(collection)

    @given(st.lists(st.integers(), min_size=1))
    def test_DeleteValue(self, collection: list[int]) -> None:
        i1 = random.randint(-(10**8), -len(collection) - 1)
        action = DeleteValue(i1)
        with pytest.raises(IndexError):
            action.reverse_action(collection)
        with pytest.raises(IndexError):
            action.forward_action(collection)

        i2 = random.randint(len(collection), 10**8)
        action = DeleteValue(i2)
        with pytest.raises(IndexError):
            action.forward_action(collection)

    @given(st.lists(st.integers(), min_size=1))
    def test_Move(self, collection: list[int]) -> None:
        i = random.randint(-(10**8), -len(collection) - 1)
        j = random.randint(len(collection), 10**8)
        action = Move(i, j)
        with pytest.raises(IndexError):
            action.forward_action(collection)

    @given(st.lists(st.integers(), min_size=1))
    def test_Clear(self, collection: list[int]) -> None:
        action = Clear()
        with pytest.raises(IndexError):
            action.reverse_action(collection)


class TestPerformedCommandStorage:
    @pytest.mark.parametrize(
        "collection,action,expected",
        [
            ([1, 1000, 3], SubtractingValue(1, 7), [1, 1000 - 7, 3]),
            ([], AddToStart(52), [52]),
            ([100, 300, 2444], InsertValue(2, 52), [100, 300, 52, 2444]),
        ],
    )
    def test_apply(self, collection: list[int], action: Action, expected: list[int]) -> None:
        storage = PerformedCommandStorage(collection)
        storage.apply(action)
        assert storage.collection == expected
        assert storage.action_list[-1] == action

    @pytest.mark.parametrize(
        "collection,action",
        [([1, 1000, 3], SubtractingValue(1, 7)), ([], AddToStart(52)), ([100, 300, 2444], InsertValue(2, 52))],
    )
    def test_undo(self, collection: list[int], action: Action) -> None:
        initial_state = collection.copy()
        storage = PerformedCommandStorage(collection)
        storage.apply(action)
        storage.undo()
        assert storage.collection == initial_state
        assert action not in storage.action_list

    def test_raise_exception_action_index_error(self) -> None:
        with pytest.raises(IndexError):
            PerformedCommandStorage([]).undo()

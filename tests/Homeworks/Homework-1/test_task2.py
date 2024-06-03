from collections import Counter

import pytest

from src.Homeworks.Homework_1.task2 import *


class TestTreap:
    @staticmethod
    def create_random_items(size: int) -> list[tuple[int, int]]:
        items = []
        for _ in range(size):
            items.append((random.randint(0, 10**8), random.randint(0, 10**8)))
        return items

    @staticmethod
    def create_treap(items: list[tuple[int, int]]) -> Treap:
        treap: Treap[int, int] = Treap()
        for key, value in items:
            treap[key] = value
        return treap

    def test_len(self) -> None:
        for length in range(1, 25):
            treap: Treap[int, int] = Treap()
            for i in range(1, length + 1):
                treap[i] = i
                assert len(treap) == i

    @pytest.mark.parametrize("size", [52, 1000 - 7])
    def test_split_node(self, size: int) -> None:
        items = TestTreap.create_random_items(size)
        treap: Treap[int, int] = TestTreap.create_treap(items)
        key, value = items[random.randint(0, size - 1)]

        node1, node2 = Treap.split_node(treap.root, key)
        if node1:
            assert max(node1.__iter__()) < key
            if node2:
                assert max(node1.__iter__()) < min(node2.__iter__()) == key

    @pytest.mark.parametrize("size", [52, 1000 - 7])
    def test_merge_node(self, size: int) -> None:
        items = sorted(TestTreap.create_random_items(size))
        index = random.randint(1, size - 1)
        items1, items2 = items[:index], items[index:]

        node1 = TestTreap.create_treap(items1).root
        node2 = TestTreap.create_treap(items2).root

        node = Treap.merge_node(node1, node2)
        if node:
            assert Counter(set(key for key, _ in items)) == Counter(node.__iter__())

    @pytest.mark.parametrize("size", [1, 2, 3, 10, 52, 1000 - 7])
    def test_setitem(self, size: int) -> None:
        items = TestTreap.create_random_items(size)
        treap: Treap[int, int] = Treap()
        for i in range(size):
            key, value = items[i]
            treap[key] = value
            assert key in treap and treap[key] == value and len(treap) == i + 1

    @pytest.mark.parametrize("size", [1, 2, 3, 10, 52, 1000 - 7])
    def test_delitem(self, size: int) -> None:
        items = TestTreap.create_random_items(size)
        treap: Treap[int, int] = TestTreap.create_treap(items)
        for i in range(size - 1):
            key, _ = items[i]
            del treap[key]
            assert size - i - 1 == len(treap)
            with pytest.raises(KeyError):
                treap[key]

    @pytest.mark.parametrize("size", [1, 2, 3, 10, 52, 1000 - 7])
    def test_delitem_errors(self, size: int) -> None:
        items = TestTreap.create_random_items(size)
        treap = TestTreap.create_treap(items[:-1])

        with pytest.raises(KeyError):
            del treap[items[-1][0]]

    @pytest.mark.parametrize("size", [1, 2, 3, 10, 52, 1000 - 7])
    def test_getitem(self, size: int) -> None:
        items = TestTreap.create_random_items(size)
        treap = TestTreap.create_treap(items)
        for key, value in items:
            assert treap[key] == value

    @pytest.mark.parametrize("size", [2, 3, 10, 52, 1000 - 7])
    def test_getitem_exception(self, size: int) -> None:
        treap: Treap[int, int] = Treap()
        with pytest.raises(EmptyTreeError):
            treap[1]

        items = TestTreap.create_random_items(size)
        treap: Treap[int, int] = TestTreap.create_treap(items[:-1])

        with pytest.raises(KeyError):
            assert treap[items[-1][0]]

    @pytest.mark.parametrize("size", [1, 2, 3, 10, 52, 1000 - 7])
    def test_iter(self, size: int) -> None:
        items = TestTreap.create_random_items(size)
        treap = TestTreap.create_treap(items)
        assert Counter([key for key, _ in items]) == Counter(list(iter(treap)))

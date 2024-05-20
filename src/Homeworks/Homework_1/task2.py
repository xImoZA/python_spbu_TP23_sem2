import random
from typing import Any, Generic, Iterator, MutableMapping, Optional, Protocol, Tuple, TypeVar


class Comparable(Protocol):
    def __gt__(self, other: Any) -> bool:
        ...

    def __ge__(self, other: Any) -> bool:
        ...


V = TypeVar("V")
K = TypeVar("K", bound=Comparable)


class EmptyTreeError(Exception):
    def __init__(self) -> None:
        super().__init__(f"The Treap is empty")


class Node(Generic[K, V]):
    def __init__(self, key: K, value: V) -> None:
        self.key: K = key
        self.value: V = value
        self.priority: float = random.random()
        self.left: Optional[Node[K, V]] = None
        self.right: Optional[Node[K, V]] = None

    def __iter__(self) -> Iterator[K]:
        if self.left:
            yield from self.left
        yield self.key
        if self.right:
            yield from self.right

    def __getitem__(self, key: K) -> V:
        if self.key < key:
            if self.right:
                return self.right[key]

            raise KeyError(f"The key {key} is not in the Node")

        if self.key > key:
            if self.left:
                return self.left[key]

            raise KeyError(f"The key {key} is not in the Node")

        return self.value

    def __repr__(self) -> str:
        return (
            f"Node(key={self.key}, value={self.value}, priority={self.priority}, left={repr(self.left)}, "
            f"right={repr(self.right)})"
        )

    def __str__(self) -> str:
        return f"[<key={self.key}, value={self.value}>, left={self.left}, right={self.right}]"


class Treap(MutableMapping, Generic[K, V]):
    def __init__(self) -> None:
        self.root: Optional[Node[K, V]] = None
        self.length: int = 0

    def __len__(self) -> int:
        return self.length

    @staticmethod
    def comparison(key1: K, key2: K, key_in_right: bool) -> bool:
        if key_in_right:
            return key1 > key2
        return key1 >= key2

    @staticmethod
    def split_node(
        node: Optional[Node[K, V]], key: K, key_in_left: bool = True
    ) -> Tuple[Optional[Node[K, V]], Optional[Node[K, V]]]:
        if node is None:
            return None, None

        if Treap.comparison(key, node.key, key_in_left):
            node1, node2 = Treap.split_node(node.right, key, key_in_left)
            node.right = node1
            return node, node2

        node1, node2 = Treap.split_node(node.left, key, key_in_left)
        node.left = node2
        return node1, node

    @staticmethod
    def merge_node(left_node: Optional[Node[K, V]], right_node: Optional[Node[K, V]]) -> Optional[Node[K, V]]:
        if left_node is None:
            return right_node

        if right_node is None:
            return left_node

        if left_node.priority > right_node.priority:
            left_node.right = Treap.merge_node(left_node.right, right_node)
            return left_node

        right_node.left = Treap.merge_node(left_node, right_node.left)
        return right_node

    def __setitem__(self, key: K, value: V) -> None:
        if self.root is None:
            self.root = Node(key, value)
            self.length = 1
        else:
            if key in self:
                del self[key]

            node1, node2 = Treap.split_node(self.root, key)
            if node1 and key > node1.key:
                node1 = Treap.merge_node(node1, Node(key, value))
            else:
                node1 = Treap.merge_node(Node(key, value), node1)
            self.root = Treap.merge_node(node1, node2)
            self.length += 1

    def __delitem__(self, key: K) -> None:
        node1, sml_node = Treap.split_node(self.root, key)
        key_node, node2 = Treap.split_node(sml_node, key, key_in_left=False)

        if key_node is None:
            raise KeyError(f"The key {key} is not in the Treap")
        self.root = Treap.merge_node(node1, node2)
        self.length -= 1

    def __getitem__(self, key: K) -> V:
        try:
            if self.root:
                return self.root[key]
            else:
                raise EmptyTreeError
        except KeyError:
            raise KeyError(f"The key {key} is not in the Treap")

    def __iter__(self) -> Iterator[K]:
        if self.root:
            return iter(self.root)
        raise EmptyTreeError

    def __repr__(self) -> str:
        if self.root:
            return (
                f"Treap(length={self.length}, root=Node(key={self.root.key}, value={self.root.value}, priority={self.root.priority}), "
                f"left={repr(self.root.left)}, right={repr(self.root.right)})"
            )

        return f"Treap(length=0, root=None, left=None, right=None)"

    def __str__(self) -> str:
        return str(self.root)

import random
from typing import MutableMapping, TypeVar, Generic, Optional, Iterator, Set

V = TypeVar("V")
K = TypeVar("K")


class Node(Generic[K, V]):
    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.priority: float = random.random()
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None

    def __iter__(self) -> Iterator[K]:
        def iterate(root: Optional[Node], output: Set[K]) -> Set[K]:
            if root is not None:
                output.add(root.key)
                output = iterate(root.left, output)
                output = iterate(root.right, output)

            return output

        return iter(iterate(self, set()))

    def __repr__(self) -> str:
        if self:
            return (
                f"Node(key={self.key}, value={self.value}, priority={self.priority}, left={self.left.__repr__()}, "
                f"right={self.right.__repr__()})"
            )
        return "None"

    def __str__(self) -> str:
        if self:
            return f"[<key={self.key}, value={self.value}>, left={self.left}, right={self.right}]"
        return "None"


class Treap(MutableMapping):
    def __init__(self) -> None:
        self.root: Optional[Node] = None
        self.length: int = 0

    def __len__(self) -> int:
        return self.length

    def __contains__(self, key: K) -> bool:
        try:
            self[key]
            return True
        except KeyError:
            return False

    @staticmethod
    def split_node(node: Node, key: K) -> tuple[Optional["Node"], Optional["Node"]]:
        if node is None:
            return None, None

        if key > node.key:
            node1, node2 = Treap.split_node(node.right, key)
            node.right = node1
            return node, node2

        node1, node2 = Treap.split_node(node.left, key)
        node.left = node2
        return node1, node

    @staticmethod
    def merge_node(left_node: Optional[Node], right_node: Optional[Node]) -> Optional["Node"]:
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
        node1, node2 = Treap.split_node(self.root, key)
        try:
            new_element: Node = self[key]
            new_element.value = value
            del self[key]

        except KeyError:
            new_element = Node(key, value)

        self.root = Treap.merge_node(Treap.merge_node(node1, new_element), node2)
        self.length += 1

    def __delitem__(self, key: K) -> None:
        node1, node2 = Treap.split_node(self.root, key)

        def recursion(node: Optional[Node]) -> Optional[Node]:
            if node and node.left:
                node.left = recursion(node.left)
                return node

            if node and node.key == key:
                return_node = node.right
                del node
                return return_node

            raise KeyError(f"The key {key} is not in the Treap")

        node2 = recursion(node2)

        self.root = Treap.merge_node(node1, node2)
        self.length -= 1

    @staticmethod
    def get_item(root: Optional[Node], key) -> Optional["Node"]:
        if root is not None:
            if root.key < key:
                return Treap.get_item(root.right, key)

            if root.key > key:
                return Treap.get_item(root.left, key)

            return root

        raise KeyError(f"The key {key} is not in the Treap")

    def __getitem__(self, key: K) -> Optional[V]:
        return Treap.get_item(self.root, key).value

    def __iter__(self) -> Iterator[K]:
        return self.root.__iter__()

    def __repr__(self) -> str:
        if self.root:
            return (
                f"Treap(length={self.length}, root=Node(key={self.root.key}, value={self.root.value}, priority={self.root.priority}), "
                f"left={self.root.left.__repr__()}, right={self.root.right.__repr__()})"
            )

        return f"Treap(length=0, root=None, left=None, right=None)"

    def __str__(self) -> str:
        return self.root.__str__()

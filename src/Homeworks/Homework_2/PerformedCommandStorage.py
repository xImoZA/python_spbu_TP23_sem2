import abc
from typing import MutableSequence, Optional

from src.Homeworks.Homework_1.task1 import Registry

REGISTRY = Registry["Action"]()


class Action(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def forward_action(self, user_list: MutableSequence[int]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def reverse_action(self, user_list: MutableSequence[int]) -> None:
        raise NotImplementedError()


class PerformedCommandStorage:
    def __init__(self, user_list: MutableSequence[int]) -> None:
        self.collection: MutableSequence[int] = user_list
        self.action_list: list[Action] = []

    def apply(self, user_action: Action) -> None:
        user_action.forward_action(self.collection)
        self.action_list.append(user_action)

    def undo(self) -> None:
        if len(self.action_list) == 0:
            raise IndexError("Action list is empty")

        last_action: Action = self.action_list.pop()
        last_action.reverse_action(self.collection)


@REGISTRY.register("AddToStart")
class AddToStart(Action):
    def __init__(self, value: int) -> None:
        self.value: int = value

    def forward_action(self, user_list: MutableSequence[int]) -> None:
        user_list.insert(0, self.value)

    def reverse_action(self, user_list: MutableSequence[int]) -> None:
        user_list.pop(0)


@REGISTRY.register("DeleteFromStart")
class DeleteFromStart(Action):
    def __init__(self) -> None:
        self.deleted_object: Optional[int] = None

    def forward_action(self, user_list: MutableSequence[int]) -> None:
        if len(user_list) == 0:
            raise IndexError("Delete from empty collection")

        self.deleted_object = user_list.pop(0)

    def reverse_action(self, user_list: MutableSequence[int]) -> None:
        if self.deleted_object is not None:
            user_list.insert(0, self.deleted_object)
        else:
            raise IndexError("The undo action has not been performed")


@REGISTRY.register("AddToEnd")
class AddToEnd(Action):
    def __init__(self, value: int):
        self.value: int = value

    def forward_action(self, user_list: MutableSequence[int]) -> None:
        user_list.append(self.value)

    def reverse_action(self, user_list: MutableSequence[int]) -> None:
        user_list.pop()


@REGISTRY.register("DeleteFromEnd")
class DeleteFromEnd(Action):
    def __init__(self) -> None:
        self.deleted_object: Optional[int] = None

    def forward_action(self, user_list: MutableSequence[int]) -> None:
        if len(user_list) == 0:
            raise IndexError("Delete from empty collection")

        self.deleted_object = user_list.pop()

    def reverse_action(self, user_list: MutableSequence[int]) -> None:
        if self.deleted_object is not None:
            user_list.append(self.deleted_object)
        else:
            raise IndexError("The undo action has not been performed")


@REGISTRY.register("AdditionValue")
class AdditionValue(Action):
    def __init__(self, i: int, value: int):
        self.i: int = i
        self.value: int = value

    def forward_action(self, user_list: MutableSequence[int]) -> None:
        if self.i >= len(user_list) or self.i < -len(user_list):
            raise IndexError("Addition with non-existent index")

        user_list[self.i] += self.value

    def reverse_action(self, user_list: MutableSequence[int]) -> None:
        user_list[self.i] -= self.value


@REGISTRY.register("SubtractingValue")
class SubtractingValue(Action):
    def __init__(self, i: int, value: int):
        self.i: int = i
        self.value: int = value

    def forward_action(self, user_list: MutableSequence[int]) -> None:
        if self.i >= len(user_list) or self.i < -len(user_list):
            raise IndexError("Subtracting from non-existent index")

        user_list[self.i] -= self.value

    def reverse_action(self, user_list: MutableSequence[int]) -> None:
        user_list[self.i] += self.value


@REGISTRY.register("InsertValue")
class InsertValue(Action):
    def __init__(self, i: int, value: int):
        self.i: int = i
        self.value: int = value

    def forward_action(self, user_list: MutableSequence[int]) -> None:
        if self.i > len(user_list) or self.i < -len(user_list) - 1:
            raise IndexError("Insert to non-existent index")

        user_list.insert(self.i, self.value)

    def reverse_action(self, user_list: MutableSequence[int]) -> None:
        if self.i < 0:
            user_list.pop(self.i - 1)
        else:
            user_list.pop(self.i)


@REGISTRY.register("DeleteValue")
class DeleteValue(Action):
    def __init__(self, i: int):
        self.i: int = i
        self.deleted_value: Optional[int] = None

    def forward_action(self, user_list: MutableSequence[int]) -> None:
        if self.i >= len(user_list) or self.i < -len(user_list):
            raise IndexError("Deleted from non-existent index")

        self.deleted_value = user_list.pop(self.i)

    def reverse_action(self, user_list: MutableSequence[int]) -> None:
        if self.deleted_value is not None:
            if self.i == -1:
                user_list.append(self.deleted_value)
            elif self.i < 0:
                user_list.insert(self.i + 1, self.deleted_value)
            else:
                user_list.insert(self.i, self.deleted_value)
        else:
            raise IndexError("The undo action has not been performed")


@REGISTRY.register("Move")
class Move(Action):
    def __init__(self, i: int, j: int):
        self.i: int = i
        self.j: int = j

    def forward_action(self, user_list: MutableSequence[int]) -> None:
        if (self.i or self.j) >= len(user_list) or (self.i or self.j) < -len(user_list):
            raise IndexError("Move from non-existent index")

        if self.i < 0:
            self.i = len(user_list) + self.i
        if self.j < 0:
            self.j = len(user_list) + self.j

        if self.i != self.j:
            user_list.insert(min(self.i, self.j), user_list.pop(max(self.i, self.j)))
            user_list.insert(max(self.i, self.j), user_list.pop(min(self.i, self.j) + 1))

    def reverse_action(self, user_list: MutableSequence[int]) -> None:
        if self.i != self.j:
            user_list.insert(min(self.i, self.j), user_list.pop(max(self.i, self.j)))
            user_list.insert(max(self.i, self.j), user_list.pop(min(self.i, self.j) + 1))


@REGISTRY.register("Reverse")
class Reverse(Action):
    def forward_action(self, user_list: MutableSequence[int]) -> None:
        user_list.reverse()

    def reverse_action(self, user_list: MutableSequence[int]) -> None:
        user_list.reverse()


@REGISTRY.register("Clear")
class Clear(Action):
    def __init__(self) -> None:
        self.deleted_collection: Optional[MutableSequence[int]] = None

    def forward_action(self, user_list: MutableSequence[int]) -> None:
        self.deleted_collection = type(user_list)()
        self.deleted_collection.extend(user_list)
        user_list.clear()

    def reverse_action(self, user_list: MutableSequence[int]) -> None:
        if self.deleted_collection is not None:
            user_list.extend(self.deleted_collection)
        else:
            raise IndexError("The undo action has not been performed")

import collections
from typing import Callable, Dict, Generic, MutableMapping, Optional, Type, TypeVar

I = TypeVar("I")

USER_TEXT = "Select a collection:\n" "\tCounter\n" "\tOrderedDict\n" "\tDefaultdict\n" "Enter class name: "


class Registry(Generic[I]):
    def __init__(self, default: Optional[Type[I]] = None) -> None:
        self.classes: Dict[str, Type[I]] = dict()
        self.default: Optional[Type[I]] = default

    def register(self, name: str) -> Callable[[Type[I]], Type[I]]:
        def _decorator(cls: Type[I]) -> Type[I]:
            self.classes[name] = cls
            return cls

        if name in self.classes:
            raise ValueError(f"The name {name} has already been registered")
        return _decorator

    def dispatch(self, name: str) -> Type[I]:
        if name in self.classes:
            return self.classes[name]
        elif self.default:
            return self.default

        raise ValueError(f"No class named {name} found")


def main() -> None:
    register = Registry[MutableMapping](default=dict)
    register.register("Counter")(collections.Counter)
    register.register("OrderedDict")(collections.OrderedDict)
    register.register("DefaultDict")(collections.defaultdict)

    user_input = input(USER_TEXT)

    user_class = register.dispatch(user_input)()

    print("Dictionary type:", type(user_class))
    print("Content of dictionary:", user_class)
    print("Add (1, Solo Leveling)")
    user_class[1] = "Solo Leveling"
    print("Content of dictionary:", user_class)
    print("Add (2, Omniscient Reader)")
    user_class[2] = "Omniscient Reader"
    print("Content of dictionary:", user_class)
    print("Delete (1, Solo Leveling)")
    del user_class[1]
    print(f"Content of dictionary", user_class)


if __name__ == "__main__":
    main()

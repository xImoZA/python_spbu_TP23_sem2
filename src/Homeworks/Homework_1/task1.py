from typing import Callable, Generic, Optional, TypeVar

Interface = TypeVar("Interface")


class Registry(Generic[Interface]):
    def __init__(self, default: Optional[Interface] = None) -> None:
        self.registry: dict[str, Interface] = dict()
        self.default: Optional[Interface] = default

    def register(self, name: str) -> Callable:
        def _decorator(cls: Interface) -> Interface:
            self.registry[name] = cls
            return cls

        if name in self.registry:
            raise ValueError(f"The name {name} has already been registered")
        return _decorator

    def dispatch(self, name: str) -> Optional[Interface] | Callable:
        if name in self.registry or self.default:
            return self.registry.get(name, self.default)

        raise ValueError(f"No class named {name} found")

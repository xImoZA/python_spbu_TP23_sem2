import json
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any, Optional, Type, TypeVar, get_args

from src.Homeworks.Homework_3.orm_error import JsonError

T = TypeVar("T", bound="ORM")


class ORMDescriptor(object):
    def __init__(self, key: str) -> None:
        self.key: str = key

    def __get__(self, instance: T, owner: Type[T]) -> Optional[T]:
        if not hasattr(instance, "__json__"):
            raise JsonError("JSON data is missing")

        try:
            value = instance.__dict__[self.key]
        except KeyError:
            raise JsonError(f"The dataclass does not have an attribute <{self.key}>")

        if value:
            return value
        elif value is None and self.key in instance.__json__.keys():
            data = instance.__json__[self.key]

            if isinstance(data, dict):
                setattr(instance, self.key, instance.__annotations__[self.key].parse_json(data))
                return instance.__dict__[self.key]

            if isinstance(data, list) and len(data) != 0 and isinstance(data[0], dict):
                sub_cls = get_args(instance.__annotations__[self.key])[0]
                obj = [sub_cls.parse_json(small_data) for small_data in data]
                setattr(instance, self.key, obj)
                return instance.__dict__[self.key]

            else:
                setattr(instance, self.key, data)
                return instance.__dict__[self.key]
        else:
            return value

    def __set__(self, instance: T, value: Any) -> None:
        instance.__dict__[self.key] = value


@dataclass
class ORM:
    @classmethod
    def parse_json(cls: Type[T], json_dict: dict[str, Any], strict: bool = False) -> T:
        if strict:
            if Counter(json_dict.keys()) != Counter(cls.__annotations__.keys()):
                raise JsonError("Dataclass does not match json")

        for name in cls.__annotations__.keys():
            setattr(cls, name, ORMDescriptor(name))

        arr = [None] * len(cls.__annotations__.keys())
        new_cls = cls(*arr)
        setattr(new_cls, "__json__", json_dict)

        return new_cls

    def dump_json(self) -> str:
        return json.dumps(asdict(self))

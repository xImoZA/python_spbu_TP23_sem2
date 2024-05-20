import json
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any, Type, TypeVar, get_args

from src.Homeworks.Homework_3.orm_error import AttributeJsonError

T = TypeVar("T", bound="ORM")


class Descr(object):
    def __init__(self, key: str) -> None:
        self.key: str = key

    def __get__(self, instance: T, owner: Type[T]) -> T:
        if not hasattr(instance, "json_dict"):
            raise AttributeJsonError

        value = instance.__dict__[self.key]
        if value is None:
            setattr(instance, self.key, instance.json_dict.get(self.key))
            return instance.__dict__[self.key]
        return value

    def __set__(self, instance: T, value: Any) -> None:
        instance.__dict__[self.key] = value


class ORMMeta(type):
    def __new__(cls, name: Any, bases: Any, dct: dict) -> type:
        for field_name, field_type in dct["__annotations__"].items():
            dct[field_name] = None

        return super().__new__(cls, name, bases, dct)


@dataclass
class ORM:
    @classmethod
    def parse_json(cls: Type[T], json_dict: dict[str, Any], strict: bool = False) -> T:
        if strict:
            if Counter(json_dict.keys()) != Counter(cls.__annotations__):
                raise AttributeError("Dataclass does not match json")
        for attr in getattr(cls, "__annotations__"):
            setattr(cls, attr, Descr(attr))

        new_cls = cls()
        setattr(new_cls, "json_dict", json_dict)

        for name, small_data in json_dict.items():
            if isinstance(small_data, dict):
                sub_cls_type = new_cls.__annotations__[name]
                setattr(new_cls, name, sub_cls_type.parse_json(small_data, strict))

            elif isinstance(small_data, list) and isinstance(small_data[0], dict):
                sub_cls_type = get_args(new_cls.__annotations__[name])
                obj = [sub_cls_type[0].parse_json(small_data[i], strict) for i in range(len(small_data))]
                setattr(new_cls, name, obj)

        return new_cls

    def dump(self) -> str:
        return json.dumps(asdict(self))
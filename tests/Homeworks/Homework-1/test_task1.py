from src.Homeworks.Homework_1.task1 import *

from typing import Mapping

import pytest

MAPPING_REGISTRY = Registry[Mapping]()
MAPPING_REGISTRY_WITH_DEFAULT = Registry[Mapping](default=dict)


@MAPPING_REGISTRY.register(name="Solo Leveling")
class SoloLeveling(Mapping):
    def __iter__(self) -> None:
        pass

    def __getitem__(self, item) -> None:
        pass

    def __len__(self) -> None:
        pass


@MAPPING_REGISTRY_WITH_DEFAULT.register(name="Omniscient Reader")
class OmniscientReader(Mapping):
    def __iter__(self) -> None:
        pass

    def __getitem__(self, item) -> None:
        pass

    def __len__(self) -> None:
        pass


@pytest.mark.parametrize(
    "register,name,expected",
    [
        (MAPPING_REGISTRY, "Solo Leveling", SoloLeveling),
        (MAPPING_REGISTRY_WITH_DEFAULT, "Omniscient Reader", OmniscientReader),
    ],
)
def test_register(register, name, expected) -> None:
    assert name in register.registry
    assert isinstance(register.registry[name](), expected)


@pytest.mark.parametrize(
    "register,name,expected",
    [
        (MAPPING_REGISTRY, "Solo Leveling", SoloLeveling),
        (MAPPING_REGISTRY_WITH_DEFAULT, "Omniscient Reader", OmniscientReader),
        (MAPPING_REGISTRY_WITH_DEFAULT, "Mashle", dict),
    ],
)
def test_dispatch(register, name, expected) -> None:
    actual = register.dispatch(name)()
    assert isinstance(actual, expected)


def test_raise_exception_register() -> None:
    with pytest.raises(ValueError):

        @MAPPING_REGISTRY.register("Solo Leveling")
        class BeBeBe(Mapping):
            pass


def test_raise_exception_dispatch() -> None:
    with pytest.raises(ValueError):
        MAPPING_REGISTRY.dispatch("Mashle")

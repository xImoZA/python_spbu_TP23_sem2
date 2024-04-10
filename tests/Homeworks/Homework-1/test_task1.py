import collections
from typing import Mapping

import pytest

from src.Homeworks.Homework_1.task1 import *

registry = Registry[Mapping]()
registry_with_default = Registry[Mapping](default=dict)


@registry.register(name="SoloLeveling")
class SoloLeveling(Mapping):
    pass


@registry_with_default.register(name="OmniscientReader")
class OmniscientReader(Mapping):
    pass


class TestRegistry:
    @pytest.mark.parametrize(
        "name,storage,expected",
        [
            ("SoloLeveling", registry, SoloLeveling),
            ("OmniscientReader", registry_with_default, OmniscientReader),
        ],
    )
    def test_registry(self, name: str, storage: Registry, expected: Mapping) -> None:
        assert name in storage.classes
        assert storage.classes[name] == expected

    @pytest.mark.parametrize(
        "storage,name,expected",
        [
            (registry, "SoloLeveling", SoloLeveling),
            (registry_with_default, "OmniscientReader", OmniscientReader),
            (registry_with_default, "Mashle", dict),
        ],
    )
    def test_dispatch(self, storage: Registry, name: str, expected: Mapping) -> None:
        assert storage.dispatch(name) == expected


class TestRegistryExceptions:
    def test_raise_exception_register(self) -> None:
        with pytest.raises(ValueError):
            registry.register("SoloLeveling")(collections.Counter)

    def test_raise_exception_dispatch(self) -> None:
        with pytest.raises(ValueError):
            registry.dispatch("Mashle")

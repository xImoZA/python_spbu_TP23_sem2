import pytest

from src.Homeworks.Homework_1.task1 import *


class TestRegistry:
    class Cls:
        pass

    registry = Registry[Cls]()
    registry_with_default = Registry[Cls](default=dict)

    class SoloLeveling(Cls):
        pass

    class OmniscientReader(Cls):
        pass

    registry.register("Solo Leveling")(SoloLeveling)
    registry_with_default.register("Omniscient Reader")(OmniscientReader)

    @pytest.mark.parametrize(
        "name,storage,expected",
        [
            ("Solo Leveling", registry, SoloLeveling),
            ("Omniscient Reader", registry_with_default, OmniscientReader),
        ],
    )
    def test_registry(self, name: str, storage: Registry, expected: Cls) -> None:
        assert name in storage.classes
        assert storage.classes[name] == expected

    @pytest.mark.parametrize(
        "storage,name,expected",
        [
            (registry, "Solo Leveling", SoloLeveling),
            (registry_with_default, "Omniscient Reader", OmniscientReader),
            (registry_with_default, "Mashle", dict),
        ],
    )
    def test_dispatch(self, storage: Registry, name: str, expected: Cls) -> None:
        assert storage.dispatch(name) == expected

    def test_raise_exception_register(self) -> None:
        with pytest.raises(ValueError):
            self.registry.register("Solo Leveling")(self.OmniscientReader)

    def test_raise_exception_dispatch(self) -> None:
        with pytest.raises(ValueError):
            self.registry.dispatch("Mashle")

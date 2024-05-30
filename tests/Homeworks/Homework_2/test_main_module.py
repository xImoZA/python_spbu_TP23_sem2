from io import StringIO

import pytest

from src.Homeworks.Homework_2.task1 import *


class TestMainModule:
    @pytest.mark.parametrize(
        "user_actions,expected",
        [
            (
                ["list", "0 1 2 3 4 5", "AddToEnd 1000", "SubtractingValue 6 7", "Show", "Exit"],
                AVAILABLE_COMMANDS + "\n[0, 1, 2, 3, 4, 5, 993]\n",
            ),
            (
                ["list", "1 8 8 17 430 7 9 1", "InsertValue 2 52", "Move 2 5", "Show", "Exit"],
                AVAILABLE_COMMANDS + "\n[1, 8, 430, 8, 17, 52, 7, 9, 1]\n",
            ),
        ],
    )
    def test_main_scenario(self, monkeypatch, user_actions: list[str], expected: str) -> None:
        monkeypatch.setattr("builtins.input", lambda _: user_actions.pop(0))
        fake_output = StringIO()
        monkeypatch.setattr("sys.stdout", fake_output)
        main()
        output = fake_output.getvalue()
        assert output == expected

    @pytest.mark.parametrize(
        "user_actions,expected",
        [
            (["drcfvghbj", "1 2 3"], "Invalid collection type\n"),
            (["list", "fg ghj i p "], "Expected int for storage\n"),
            (["list", "1 2 3", "Undo", "Exit"], AVAILABLE_COMMANDS + "\nAction list is empty\n"),
            (["list", "1 2 3", "aboba", "Exit"], AVAILABLE_COMMANDS + "\nIncorrect action was entered\n"),
            (["list", "1 2 3", "AddToStart  gf", "Exit"], AVAILABLE_COMMANDS + "\nExpected integer for arguments\n"),
            (["list", "1 2 3", "AddToStart  1 2 3", "Exit"], AVAILABLE_COMMANDS + "\nIncorrect number of arguments\n"),
        ],
    )
    def test_main_scenario_error(self, monkeypatch, user_actions: list[str], expected: str) -> None:
        monkeypatch.setattr("builtins.input", lambda _: user_actions.pop(0))
        fake_output = StringIO()
        monkeypatch.setattr("sys.stdout", fake_output)
        main()
        output = fake_output.getvalue()
        assert output == expected

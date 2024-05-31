import hypothesis.strategies as st
import pytest
from hypothesis import given

from src.Homeworks.Homework_6.model import *


class TestTicTacToeModel:
    test_model = TicTacToeModel()

    def test_make_move(self) -> None:
        pl1 = Human("1", "X", [])
        for num_cage in range(9):
            self.test_model.make_move(num_cage, pl1)
            assert len(self.test_model.free_cages) == 9 - num_cage - 1 and self.test_model.cages[
                num_cage
            ].value == Cage(num_cage, pl1.side)
            assert num_cage not in self.test_model.free_cages
            assert num_cage in pl1.positions
        assert self.test_model.session.value.name == "final"

    @pytest.mark.parametrize("pos_list", WIN_POS)
    def test_check_win_true(self, pos_list: list[int]) -> None:
        pl1 = Human("1", "X", pos_list)
        assert self.test_model.check_win(pl1) is True

    @given(st.lists(st.integers(min_value=9)))
    def test_check_win_true(self, pos_list: list[int]) -> None:
        pl1 = Human("1", "X", pos_list)
        assert self.test_model.check_win(pl1) is False


class TestStupidBot:
    bot = StupidBot("Bot", "X", [])
    free_cages = [num for num in range(9)]

    def test_make_move_bot(self) -> None:
        for _ in range(9):
            move = self.bot.make_move(None, self.free_cages)
            assert isinstance(move, int) and move in self.free_cages
            del self.free_cages[self.free_cages.index(move)]

    def test_make_move_bot_error(self) -> None:
        with pytest.raises(TicTacToeException):
            self.bot.make_move(None, [])


class TestSmartBot:
    def test_out_isinstance_int(self) -> None:
        bot = SmartBot("Bot", "X", [])
        free_cages = [num for num in range(9)]
        for _ in range(9):
            move = bot.make_move(None, free_cages)
            assert isinstance(move, int) and move in free_cages
            del free_cages[free_cages.index(move)]

    def test_error(self) -> None:
        bot = SmartBot("Bot", "X", [])
        with pytest.raises(TicTacToeException):
            bot.make_move(None, [])

    @given(st.lists(st.integers(), min_size=1))
    def test_4_is_available(self, free_cages: list[int]) -> None:
        bot = SmartBot("Bot", "X", [])
        if 4 not in free_cages:
            free_cages.append(4)
        assert bot.make_move(None, free_cages) == 4

    @pytest.mark.parametrize("win_pos", WIN_POS)
    def test_get_win_move(self, win_pos: list[int]) -> None:
        move = win_pos[randint(0, 2)]
        near_win_pos = [pos for pos in win_pos if pos != move]

        bot = SmartBot("Bot", "X", near_win_pos)

        assert bot.make_move(None, [move]) == move

    @pytest.mark.parametrize("win_pos", WIN_POS)
    def test_defense(self, win_pos: list[int]) -> None:
        move = win_pos[randint(0, 2)]
        near_win_pos = [pos for pos in win_pos if pos != move]

        bot = SmartBot("Bot", "X", [])

        non_player_pos = list({num for num in range(9)} - set(near_win_pos))
        bot.positions.extend(non_player_pos)

        assert bot.make_move(None, [move]) == move

    @given(st.integers(min_value=1, max_value=100))
    def test_get_diagonal_if_available(self, count: int) -> None:
        bot = SmartBot("Bot", "X", [])
        for _ in range(count):
            assert bot.make_move(None, [num for num in range(9) if num != 4]) in [0, 2, 6, 8]

    @given(st.integers(min_value=1, max_value=100))
    def test_get_not_diagonal(self, count: int) -> None:
        bot = SmartBot("Bot", "X", [])
        for _ in range(count):
            assert bot.make_move(None, [num for num in range(9) if num not in [0, 2, 4, 6, 8]]) in [1, 3, 5, 7]

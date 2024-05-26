import abc
from dataclasses import dataclass
from random import randint
from typing import Callable, Optional

from observer import Observable

WIN_POS = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]


class TicTacToeException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


@dataclass
class Mode:
    name: str
    players: dict


@dataclass
class Cage:
    num: int
    side: str


@dataclass
class Player:
    name: str
    side: str
    positions: list[int]


class Bot(Player, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def make_bot_move(self, free_cages: list[int]) -> Optional[int]:
        raise NotImplementedError


class StupidBot(Bot):
    def make_bot_move(self, free_cages: list[int]) -> int:
        return free_cages[randint(0, len(free_cages) - 1)]


class SmartBot(Bot):
    def make_bot_move(self, free_cages: list[int]) -> int:
        if 4 in free_cages:
            return 4

        player_cages = list(set([i for i in range(9)]) - set(self.positions) - set(free_cages))
        for win_pos in WIN_POS:
            if len(set(win_pos) & set(self.positions)) == 2:
                pos = list(set(win_pos) - set(self.positions))[0]
                if pos in free_cages:
                    return pos

            if len(set(win_pos) & set(player_cages)) == 2:
                pos = list(set(win_pos) - set(player_cages))[0]
                if pos in free_cages:
                    return pos

        free_diagonal_cages = [num_cage for num_cage in free_cages if num_cage % 2 == 0 and num_cage != 4]
        bot_diagonal_cages = [num_cage for num_cage in self.positions if num_cage % 2 == 0 and num_cage != 4]
        if 4 in self.positions:
            if (len(free_diagonal_cages) == 4 and len(bot_diagonal_cages) == 0) or (
                len(free_diagonal_cages) == 2 and len(bot_diagonal_cages) == 1
            ):
                return free_diagonal_cages[randint(0, len(free_diagonal_cages) - 1)]

        if free_diagonal_cages:
            return free_diagonal_cages[randint(0, len(free_diagonal_cages) - 1)]
        if free_cages:
            return free_cages[randint(0, len(free_cages) - 1)]

        raise TicTacToeException("There are no possible moves")


class TicTacToeModel:
    def __init__(self) -> None:
        self.cages: dict[int, Observable[Cage]] = {}
        for i in range(9):
            self.cages[i] = Observable(Cage(i, ""))
        self.free_cages = [i for i in range(9)]

        self.session: Observable = Observable()

    def choose_mod(self, mode: str, data: dict) -> None:
        self.session.value = Mode(mode, data)

    def make_move(self, num_cage: Optional[int], player: Optional[Player]) -> None:
        if num_cage is not None and player:
            if num_cage not in self.cages.keys():
                raise TicTacToeException("Wrong cage number")

            if self.cages[num_cage].value != Cage(num_cage, ""):
                raise TicTacToeException(f"The cage {num_cage} is not available")

            self.cages[num_cage].value = Cage(num_cage, player.side)

            del self.free_cages[self.free_cages.index(num_cage)]
            if len(self.free_cages) == 0:
                self.session.value = Mode("final", {})

            player.positions.append(num_cage)
            if self.check_win(player):
                self.session.value = Mode("final", {"win": player})

    @staticmethod
    def check_win(player: Player) -> bool:
        for pos in WIN_POS:
            if len(set(pos) & set(player.positions)) == 3:
                return True
        return False

    def add_session_listener(self, callback: Callable) -> Callable:
        return self.session.add_callback(callback)

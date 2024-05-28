import abc
from random import randint
from tkinter import Tk, ttk
from typing import Callable, Optional

from src.Homeworks.Homework_6.model import Bot, Mode, Player, SmartBot, StupidBot, TicTacToeException, TicTacToeModel
from src.Homeworks.Homework_6.observer import Observable
from src.Homeworks.Homework_6.view import FieldView, FinalView, MainView, SideView, MultiplayerView


class IViewModel(metaclass=abc.ABCMeta):
    def __init__(self, model: TicTacToeModel):
        self._model = model

    @abc.abstractmethod
    def start(self, root: Tk, data: dict) -> ttk.Frame:
        raise NotImplementedError


class ViewModel:
    def __init__(self, model: TicTacToeModel, root: Tk):
        self._model = model
        self._root = root

        self._viewmodels: dict[str, IViewModel] = {
            "main": MainViewModel(self._model),
            "multiplayer": MultiplayerViewModel(self._model),
            "side": SideViewModel(self._model),
            "field": FieldViewModel(self._model),
            "final": FinalViewModel(self._model),
        }

        self._session_callback_rm = model.add_session_listener(self._session_observer)
        self._current_view: Optional[ttk.Frame] = None

    def _session_observer(self, mode: Mode) -> None:
        if mode.name == "final":
            self.switch("final", mode.players)
        elif mode.name == "multiplayer":
            self.switch("multiplayer", mode.players)
        elif mode.name == "side":
            self.switch("side", mode.players)
        else:
            self.switch("field", mode.players)

    def switch(self, name: str, data: dict) -> None:
        if name not in self._viewmodels:
            raise RuntimeError(f"Unknown view to switch: {name}")

        if self._current_view is not None:
            self._current_view.destroy()

        self._current_view = self._viewmodels[name].start(self._root, data)
        self._current_view.grid(row=0, column=0, sticky="NSEW")

    def start(self) -> None:
        self.switch("main", {})


class MainViewModel(IViewModel):
    def _bind(self, view: MainView) -> None:
        view.yourself_btn.config(command=lambda: self.play_by_self())
        view.easy_btn.config(command=lambda: self.stupid_bot())
        view.hard_btn.config(command=lambda: self.smart_bot())
        view.multiplayer_btn.config(command=lambda : self.multiplayer())

    def play_by_self(self) -> None:
        self._model.choose_mod("play_by_self", {"player1": Player("1", "O", []), "player2": Player("2", "X", [])})

    def stupid_bot(self) -> None:
        self._model.choose_mod("side", {"player1": Player("You", "", []), "player2": StupidBot("Bot", "", [])})

    def smart_bot(self) -> None:
        self._model.choose_mod("side", {"player1": Player("You", "", []), "player2": SmartBot("Bot", "", [])})

    def multiplayer(self) -> None:
        self._model.choose_mod("multiplayer", {})

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        frame = MainView(root)
        self._bind(frame)
        return frame


class MultiplayerViewModel(IViewModel):
    def _bind(self, view: MultiplayerView) -> None:
        view.label.pack()
        view.ip_entry.pack()
        view.enter_btn.pack()

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        frame = MultiplayerView(root)
        self._bind(frame)
        return frame


class SideViewModel(IViewModel):
    def _bind(self, view: SideView, data: dict) -> None:
        view.tic_btn.config(command=lambda: self.choose_side(1, data))
        view.tac_btn.config(command=lambda: self.choose_side(0, data))

    def choose_side(self, tictac: int, data: dict) -> None:
        pl1: Player = data["player1"]
        pl2: Player = data["player2"]

        if tictac == 0:
            pl1.side = "O"
            pl2.side = "X"
        else:
            pl1.side = "X"
            pl2.side = "O"

        new_data = {"player1": pl1, "player2": pl2}
        if isinstance(pl2, StupidBot):
            self._model.choose_mod("stupid_bot", new_data)
        else:
            self._model.choose_mod("smart_bot", new_data)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        frame = SideView(root)
        self._bind(frame, data)
        return frame


class FieldViewModel(IViewModel):
    def _bind(self, view: FieldView, data: dict) -> None:
        pl1: Player = data["player1"]
        pl2: Player = data["player2"]
        self._players: list[Player] = [pl1, pl2]
        self._now_player: Observable[Player] = Observable(self._players[randint(0, 1)])

        if isinstance(self._now_player.value, Player):
            view.header.config(text=f"{self._now_player.value.name} is get move now")

        label_observer_rm = self._now_player.add_callback(
            lambda player: view.header.config(text=f"{player.name} is get move now")
        )
        cages_observer_rm = []
        for i in range(9):
            view.__dict__[f"btn_{i}"].config(command=lambda num_cage=i: self.make_move(num_cage))
            cages_observer_rm.append(
                self._model.cages[i].add_callback(lambda cage: view.__dict__[f"btn_{cage.num}"].config(text=cage.side))
            )

        if isinstance(self._now_player.value, Bot):
            self.make_move(self._now_player.value.make_bot_move(self._model.free_cages))

        def _destroy_wrapper(original_destroy: Callable) -> Callable:
            def destroy() -> None:
                original_destroy()
                label_observer_rm()
                for observer_rm in cages_observer_rm:
                    observer_rm()

            return destroy

        setattr(view, "destroy", _destroy_wrapper(view.destroy))

    def make_move(self, num_cage: Optional[int]) -> None:
        try:
            self._model.make_move(num_cage, self._now_player.value)
            self._now_player.value = (
                self._players[0] if self._now_player.value == self._players[1] else self._players[1]
            )
            if self._now_player and isinstance(self._now_player.value, Bot):
                self.make_move(self._now_player.value.make_bot_move(self._model.free_cages))

        except TicTacToeException:
            pass

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        frame = FieldView(root)
        frame.grid(row=0, column=0, sticky="NSEW")
        self._bind(frame, data)
        return frame


class FinalViewModel(IViewModel):
    def start(self, root: Tk, data: dict) -> ttk.Frame:
        frame = FinalView(root)
        frame.grid(row=0, column=0, sticky="NSEW")
        pl1: Optional[Player] = data.get("win")

        if pl1:
            frame.header.config(text=f"Win {pl1.name}")
        else:
            frame.header.config(text=f"Draw")
        return frame

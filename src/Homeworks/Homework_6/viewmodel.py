import abc
import socket
from random import randint
from threading import Thread
from tkinter import Tk, ttk
from typing import Callable, Optional

from src.Homeworks.Homework_6.model import Human, Mode, Player, SmartBot, StupidBot, TicTacToeException, TicTacToeModel
from src.Homeworks.Homework_6.observer import Observable
from src.Homeworks.Homework_6.view import FieldView, FinalView, MainView, SideView


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
        if not mode:
            self._model.free_cages = [i for i in range(9)]
            self.switch("main", {})
        elif mode.name == "final":
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
        view.multiplayer_btn.config(command=lambda: self.multiplayer())

    def play_by_self(self) -> None:
        self._model.choose_mod("play_by_self", {"player1": Human("1", "O", []), "player2": Human("2", "X", [])})

    def stupid_bot(self) -> None:
        self._model.choose_mod("side", {"player1": Human("You", "", []), "player2": StupidBot("Bot", "", [])})

    def smart_bot(self) -> None:
        self._model.choose_mod("side", {"player1": Human("You", "", []), "player2": SmartBot("Bot", "", [])})
    
    def multiplayer(self) -> None:
        self._model.choose_mod("multiplayer", {"player1": Human("You", "", []), "player2": Human("Opponent", "", [])})

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        frame = MainView(root)
        self._bind(frame)
        return frame


class MultiplayerViewModel(IViewModel):
    def _bind(self, view: MultiplayerView, data: dict) -> None:
        view.label.pack()
        view.ip_entry.pack()
        view.enter_btn.config(command=lambda: get_ip_and_swap_view())

        def get_ip_and_swap_view() -> None:
            data["ip"] = view.ip_entry.get()
            if data["ip"] == "":
                data["ip"] = "127.0.0.1"
            self._model.choose_mod("side", data)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        frame = MultiplayerView(root)
        self._bind(frame, data)
        return frame

      
class SideViewModel(IViewModel):
    def _bind(self, view: SideView, data: dict) -> None:
        view.tic_btn.config(command=lambda: self.choose_side(1, data))
        view.tac_btn.config(command=lambda: self.choose_side(0, data))

    def choose_side(self, tictac: int, data: dict) -> None:
        if tictac == 0:
            data["player1"].side = "O"
            data["player2"].side = "X"
        else:
            data["player1"].side = "X"
            data["player2"].side = "O"

        if isinstance(data["player2"], StupidBot):
            self._model.choose_mod("stupid_bot", data)
        elif isinstance(data["player2"], SmartBot):
            self._model.choose_mod("smart_bot", data)
        else:
            self._model.choose_mod("field", data)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        frame = SideView(root)
        self._bind(frame, data)
        return frame


class FieldViewModel(IViewModel):
    def _bind(self, view: FieldView, data: dict) -> None:
        pl1: Player = data["player1"]
        pl2: Player = data["player2"]
        self._players: list[Player] = [pl1, pl2]
        if pl2.name == "Opponent":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((data.get("ip"), 12345))

            while True:
                self.sock.sendall(bytes(f"? {self.sock.getsockname()[-1]}", encoding="UTF-8"))
                responce = self.sock.recv(1024)
                if responce:
                    if responce.decode() == "you":
                        self._now_player: Observable[Player] = Observable(pl1)
                        break
                    elif responce.decode() == "not you":
                        self._now_player = Observable(pl2)
                        break

            def get_response() -> None:
                while True:
                    data = self.sock.recv(1024)
                    if data:
                        move = int(data.decode().split()[0])
                        self.make_move(move, pl2)

            player_thread = Thread(target=get_response)
            player_thread.start()

        else:
            self._now_player = Observable(self._players[randint(0, 1)])

        if isinstance(self._now_player.value, Player):
            view.header.config(text=f"{self._now_player.value.name} is get move now")

        label_observer_rm = self._now_player.add_callback(
            lambda player: view.header.config(text=f"{player.name} is get move now")
        )
        if self._now_player.value:
            cages_observer_rm = []
            for i in range(9):
                view.__dict__[f"btn_{i}"].config(
                    command=lambda num_cage=i: self.make_move(
                        self._now_player.value.make_move(num_cage, None),
                        self._players[0] if self._players[0].name == "You" else None,
                    )
                )
                cages_observer_rm.append(
                    self._model.cages[i].add_callback(
                        lambda cage: view.__dict__[f"btn_{cage.num}"].config(text=cage.side)
                    )
                )

            if self._now_player.value.name == "Bot":
                self.make_move(self._now_player.value.make_move(None, self._model.free_cages), self._now_player.value)

            setattr(view, "destroy", self._destroy_wrapper(view.destroy, label_observer_rm, *cages_observer_rm))

    def _destroy_wrapper(self, *args: Callable) -> Callable:
        def destroy() -> None:
            for observer_rm in args:
                observer_rm()

        return destroy

    def make_move(self, num_cage: Optional[int], player: Optional[Player]) -> None:
        try:
            if player == self._now_player.value or player is None:
                self._model.make_move(num_cage, self._now_player.value)
                self._now_player.value = (
                    self._players[0] if self._now_player.value == self._players[1] else self._players[1]
                )

                if self._now_player.value.name == "Bot":
                    self.make_move(
                        self._now_player.value.make_move(None, self._model.free_cages), self._now_player.value
                    )
                elif self._now_player.value.name == "Opponent":
                    self.sock.sendall(bytes(f"{num_cage} {self.sock.getsockname()[-1]}", encoding="UTF-8"))

        except TicTacToeException:
            pass

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        frame = FieldView(root)
        frame.grid(row=0, column=0, sticky="NSEW")
        self._bind(frame, data)
        return frame


class FinalViewModel(IViewModel):
    def _bind(self, view: FinalView) -> None:
        view.menu.config(command=self._model.return_menu)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        frame = FinalView(root)
        frame.grid(row=0, column=0, sticky="NSEW")
        pl1: Optional[Player] = data.get("win")

        if pl1:
            frame.header.config(text=f"{pl1.name} win")
        else:
            frame.header.config(text=f"Draw")

        self._bind(frame)
        return frame

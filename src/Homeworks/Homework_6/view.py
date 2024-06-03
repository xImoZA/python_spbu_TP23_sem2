from tkinter import ttk
from typing import Any


class MainView(ttk.Frame):
    GREETINGS = 'Welcome to the "TicTacToe"!'
    CHOOSE_MODE = "Select a mode:"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=60)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        self.header1 = ttk.Label(self, text=self.GREETINGS)
        self.header1.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.header2 = ttk.Label(self, text=self.CHOOSE_MODE)
        self.header2.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        self.yourself_btn = ttk.Button(self, text="By self")
        self.yourself_btn.grid(row=2, column=0, sticky="NSEW")
        self.easy_btn = ttk.Button(self, text="Easy bot mod")
        self.easy_btn.grid(row=2, column=1, sticky="NSEW")
        self.hard_btn = ttk.Button(self, text="Hard bot mod")
        self.hard_btn.grid(row=2, column=2, sticky="NSEW")
        self.multiplayer_btn = ttk.Button(self, text="Multiplayer")
        self.multiplayer_btn.grid(row=2, column=3, sticky="NSEW")


class MultiplayerView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.label = ttk.Label(self, text="Enter ip of server:")
        self.ip_entry = ttk.Entry(self)
        self.enter_btn = ttk.Button(self, text="Enter")
        self.label.pack()
        self.ip_entry.pack()
        self.enter_btn.pack()


class SideView(ttk.Frame):
    CHOOSE_SIDE = "Choose a side:"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=60)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

        self.header = ttk.Label(self, text=self.CHOOSE_SIDE)
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.tic_btn = ttk.Button(self, text="X")
        self.tic_btn.grid(row=1, column=0, sticky="NSEW")
        self.tac_btn = ttk.Button(self, text="O")
        self.tac_btn.grid(row=1, column=1, sticky="NSEW")


class FieldView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i + 1, weight=3)

        self.header = ttk.Label(self)
        self.header.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        for num_btn in range(9):
            self.__dict__[f"btn_{num_btn}"] = ttk.Button(self)
            self.__dict__[f"btn_{num_btn}"].grid(row=num_btn // 3 + 1, column=num_btn % 3, sticky="NSEW")


class FinalView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_columnconfigure(0, weight=10)

        self.header = ttk.Label(self)
        self.header.grid(row=0, column=0)
        self.menu = ttk.Button(self)
        self.menu.grid(row=1, column=0, sticky="NSEW")

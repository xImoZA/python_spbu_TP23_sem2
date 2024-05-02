import asyncio
from tkinter import END, Tk

from model import *
from view import MainView


class ViewModel:
    def __init__(self, model: ModelParser, root: Tk):
        self._model = model
        self._root = root

        self._current_view = MainViewModel(self._model).start(self._root)
        self._current_view.grid(row=0, column=0, sticky="NSEW")


class MainViewModel:
    def __init__(self, model: ModelParser):
        self._model: ModelParser = model
        self.loop = asyncio.get_event_loop()

    def _bind(self, view: MainView) -> None:
        view.best_btn.config(command=lambda: self.loop.create_task(self.handle_best(view)))
        view.new_btn.config(command=lambda: self.loop.create_task(self.handle_new(view)))
        view.random_btn.config(command=lambda: self.loop.create_task(self.handle_random(view)))

    async def handle_best(self, view: MainView) -> None:
        quotes = await self._model.parse_quotes("https://башорг.рф/byrating")
        view.text.config(state="normal")
        view.text.delete("1.0", END)
        view.text.insert(END, ">>>\n" + ">>>\n".join(quotes))
        view.text.config(state="disabled")

    async def handle_new(self, view: MainView) -> None:
        quotes = await self._model.parse_quotes("https://башорг.рф/")
        view.text.config(state="normal")
        view.text.delete("1.0", END)
        view.text.insert(END, ">>>\n" + ">>>\n".join(quotes))
        view.text.config(state="disabled")

    async def handle_random(self, view: MainView) -> None:
        quotes = await self._model.parse_quotes("https://башорг.рф/random")
        view.text.config(state="normal")
        view.text.delete("1.0", END)
        view.text.insert(END, ">>>\n" + ">>>\n".join(quotes))
        view.text.config(state="disabled")

    def start(self, root: Tk) -> MainView:
        frame = MainView(root)
        self._bind(frame)
        return frame

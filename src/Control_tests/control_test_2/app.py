import asyncio
from tkinter import Tk

from model import ModelParser
from viewmodel import ViewModel


class Window:
    APPLICATION_NAME = "QUOTES"
    START_SIZE = 512, 512
    MIN_SIZE = 256, 256

    def __init__(self) -> None:
        self._root = self._setup_root()
        self._model = ModelParser(10)
        self._viewmodel = ViewModel(self._model, self._root)

    def _setup_root(self) -> Tk:
        root = Tk()
        root.geometry("x".join(map(str, self.START_SIZE)))
        root.minsize(*self.MIN_SIZE)
        root.title(self.APPLICATION_NAME)
        return root

    async def show(self) -> None:
        while True:
            self._root.update()
            await asyncio.sleep(0)


class App:
    async def exec(self) -> None:
        await Window().show()


if __name__ == "__main__":
    asyncio.run(App().exec())

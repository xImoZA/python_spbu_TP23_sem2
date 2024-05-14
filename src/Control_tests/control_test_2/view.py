from tkinter import Text, Tk, ttk


class MainView(ttk.Frame):
    GREETINGS = "Welcome. Choose which quotes you want to see:"
    BEST = "BEST"
    NEW = "NEW"
    RANDOM = "RANDOM"

    def __init__(self, root: Tk) -> None:
        super().__init__(root)
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        self.header = ttk.Label(self, text=self.GREETINGS)
        self.header.grid(row=0, column=0, columnspan=3, sticky="NSEW")

        self.best_btn = ttk.Button(self, text=self.BEST)
        self.best_btn.grid(row=1, column=0, sticky="NSEW")
        self.new_btn = ttk.Button(self, text=self.NEW)
        self.new_btn.grid(row=1, column=1, sticky="NSEW")
        self.random_btn = ttk.Button(self, text=self.RANDOM)
        self.random_btn.grid(row=1, column=2, sticky="NSEW")

        self.text = Text(wrap="word", width=60)
        self.text.config(state="disabled")
        self.text.grid(row=2)

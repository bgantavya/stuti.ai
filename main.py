from tkinter import Tk

try:
    from .gui import ChatGUI
    from .bot import BotEngine
except ImportError:
    from gui import ChatGUI
    from bot import BotEngine


class StutiApp:
    def __init__(self) -> None:
        self.root = Tk()
        self.bot = BotEngine()
        self.gui = ChatGUI(self.root, self.bot)

    def run(self) -> None:
        self.root.mainloop()

if __name__ == '__main__':
    app = StutiApp()
    app.run()

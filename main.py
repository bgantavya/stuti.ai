from tkinter import Tk

try:
    from .gui import ChatGUI
    from .bot import BotEngine
except ImportError:
    from gui import ChatGUI
    from bot import BotEngine

if __name__ == '__main__':
    root = Tk()
    bot = BotEngine()
    app = ChatGUI(root, bot)
    root.mainloop()

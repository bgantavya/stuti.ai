from tkinter import Tk
from gui import ChatGUI
from bot import BotEngine
if __name__ == '__main__':
    root = Tk()
    bot = BotEngine()
    app = ChatGUI(root, bot)
    root.mainloop()

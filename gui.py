try:
    from . import configs
except ImportError:
    import configs
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatGUI:
    def __init__(self, root, bot_engine):
        self.root = root
        self.bot = bot_engine
        self.root.title("Stuti AI")
        self.root.configure(bg=configs.BG_COLOR)
        self.buildUI()

    def buildUI(self):
        mainFrame = tk.Frame(self.root, bg=configs.BG_COLOR)
        mainFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        mainFrame.grid_rowconfigure(0, weight=1)
        mainFrame.grid_columnconfigure(0, weight=1)

        self.chatArea = scrolledtext.ScrolledText(
            mainFrame, bg=configs.BG_COLOR, fg=configs.TEXT_COLOR, 
            font=configs.FONT_NORMAL, width=70, height=20, 
            wrap=tk.WORD, relief=tk.FLAT, state=tk.DISABLED
        )
        self.chatArea.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.chatArea.tag_configure("user_label", font=configs.FONT_BOLD, foreground="#87ceeb")
        self.chatArea.tag_configure("bot_label", font=configs.FONT_BOLD, foreground="#98fb98")
        self.chatArea.tag_configure("typing", font=configs.FONT_NORMAL, foreground="#808080")

        self.entry = tk.Entry(
            mainFrame, bg=configs.ENTRY_BG, fg=configs.TEXT_COLOR, 
            font=configs.FONT_NORMAL, relief=tk.FLAT, insertbackground=configs.TEXT_COLOR
        )
        self.entry.grid(row=1, column=0, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.sendMessageEvent)

        self.send_btn = tk.Button(
            mainFrame, text="Send", font=configs.FONT_BOLD, 
            bg=configs.BUTTON_BG, fg=configs.BUTTON_FG,
            command=self.sendMessageEvent, relief=tk.FLAT, 
            activebackground="#005f9e"
        )
        self.send_btn.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
        self.entry.focus_set()

    def addMessage(self, label, label_tag, message):
        self.chatArea.config(state=tk.NORMAL)
        self.chatArea.insert(tk.END, f"{label}: ", (label_tag,))
        self.chatArea.insert(tk.END, f"{message}\n\n")
        self.chatArea.config(state=tk.DISABLED)
        self.chatArea.see(tk.END)

    def sendMessageEvent(self, event=None):
        user_msg = self.entry.get().strip()
        if not user_msg:
            return
        
        self.entry.delete(0, tk.END)
        self.addMessage("You", "user_label", user_msg)
        self.toggle_input_widgets(False)
        self.show_typing_indicator(True)
        
        threading.Thread(target=self.getBotResponse, args=(user_msg,), daemon=True).start()

    def getBotResponse(self, user_msg):
        response_text = self.bot.getResponse(user_msg)
        
        self.root.after(0, self.show_typing_indicator, False)
        self.root.after(0, self.addMessage, "Stuti", "bot_label", response_text)
        self.root.after(0, self.toggle_input_widgets, True)

    def show_typing_indicator(self, show):
        self.chatArea.config(state=tk.NORMAL)
        if show:
            self.chatArea.insert(tk.END, "Stuti is typing...", ("typing",))
        else:
            content = self.chatArea.get("1.0", tk.END)
            if "Stuti is typing..." in content.splitlines()[-1]:
                 self.chatArea.delete("end-1c linestart", "end")
        self.chatArea.config(state=tk.DISABLED)
        self.chatArea.see(tk.END)
        
    def toggle_input_widgets(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.entry.config(state=state)
        self.send_btn.config(state=state)
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
from google import genai
from google.genai import types
#import pyttsx3

# --- API Configuration ---
# It's better practice to handle the API key at the start.
try:
    # Use your actual API key here or set it as an environment variable
   # API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_API_KEY_HERE") 
    #if API_KEY == "YOUR_API_KEY_HERE":
     #   raise ValueError("Please replace 'YOUR_API_KEY_HERE' with your actual Google API key.")
    client = genai.Client(api_key='AIzaSyD2MnVdZQwKvBDGLVHvg-nwMeN1RrTATSU')
except (Exception, ValueError) as e:
    # Show an error in a GUI window instead of just printing to console.
    root = tk.Tk()
    root.withdraw() # Hide the main window
    messagebox.showerror("API Error", f"Failed to initialize AI client: {e}")
    exit()


chat = client.chats.create(
    model="gemini-3-flash-preview", # Using the latest available model
    config=types.GenerateContentConfig(
        # system_instruction=SYSTEM_INSTRUCTION,
        temperature=1.2 # Slightly reduced for more coherent, yet creative responses
    )
)

# --- UI Constants ---
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#d4d4d4"
USER_MSG_BG = "#005f5f"
BOT_MSG_BG = "#2a2a2a"
ENTRY_BG = "#252526"
BUTTON_BG = "#007acc"
BUTTON_FG = "#ffffff"
FONT_NORMAL = ("Segoe UI", 12)
FONT_BOLD = ("Segoe UI", 12, "bold")

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Private Chat - Stuti")
        self.root.configure(bg=BG_COLOR)
        self.build_ui()

    def build_ui(self):

	
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Use ScrolledText for simplicity (combines Text and Scrollbar)
        self.chat_area = scrolledtext.ScrolledText(
            main_frame, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT_NORMAL,
            width=70, height=20, wrap=tk.WORD, relief=tk.FLAT,
            state=tk.DISABLED # Start as read-only
        )
        self.chat_area.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # --- Message Styling Tags ---
        self.chat_area.tag_configure("user_label", font=FONT_BOLD, foreground="#87ceeb")
        self.chat_area.tag_configure("bot_label", font=FONT_BOLD, foreground="#98fb98")
        self.chat_area.tag_configure("typing", font=FONT_NORMAL, foreground="#808080")

        # --- Input Area ---
        self.entry = tk.Entry(
            main_frame, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT_NORMAL,
            relief=tk.FLAT, insertbackground=TEXT_COLOR
        )
        self.entry.grid(row=1, column=0, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.send_message_event)

        self.send_btn = tk.Button(
            main_frame, text="Send", font=FONT_BOLD, bg=BUTTON_BG, fg=BUTTON_FG,
            command=self.send_message_event, relief=tk.FLAT, activebackground="#005f9e"
        )
        self.send_btn.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        self.entry.focus_set()

    def add_message(self, label, label_tag, message):
        """Adds a formatted message to the chat area."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{label}: ", (label_tag,))
        self.chat_area.insert(tk.END, f"{message}\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def send_message_event(self, event=None):
        user_msg = self.entry.get().strip()
        if not user_msg:
            return
        
        threading.Thread(target=self.get_bot_response, args=(user_msg,), daemon=True).start()
        self.entry.delete(0, tk.END)
        self.add_message("You", "user_label", user_msg)
        
        # Disable input and show "typing..." indicator
        self.toggle_input_widgets(False)
        self.show_typing_indicator(True)

        # Run the API call in a separate thread to avoid freezing the GUI

    def get_bot_response(self, user_msg):
        """Handles the API call in a background thread."""
        try:
            response = chat.send_message(user_msg)
            
            # Use root.after to safely update UI from the background thread
            self.root.after(0, self.show_typing_indicator, False) # Hide "typing..."
            self.root.after(0, self.prepare_bot_message_area)
            # res = ""
            # for chunk in response_stream:
            self.root.after(0, self.append_bot_message, response.text)
                # res += chunk.text
            
            # if res:
            #     try:
            #         # 1. Initialize engine inside the thread
            #         tts_engine = pyttsx3.init()
                    
            #         # 2. Set properties (optional, but good practice)
            #         voices = tts_engine.getProperty('voices')
            #         # for voice in voices:
            #         #     if voice.gender == 'female':
            #         tts_engine.setProperty('voice', 'mb-in2')
            #                 # break
            #         tts_engine.setProperty('rate', 120)
                    
            #         # 3. Say the text and wait for it to complete
            #         tts_engine.say(res)
            #         tts_engine.runAndWait()
                    
            #         # 4. Stop the engine to ensure clean shutdown (important!)
            #         tts_engine.stop()
            #     except Exception as e:
            #         print(f"TTS Error: {e}")
            
            # Add final newlines for spacing
            self.root.after(0, self.append_bot_message, "\n\n")

        except Exception as e:
            # Safely show error in the main thread
            self.root.after(0, messagebox.showerror, "Error", f"Failed to get response: {e}")
        finally:
            # Re-enable input widgets once done
            self.root.after(0, self.toggle_input_widgets, True)
    
    def prepare_bot_message_area(self):
        """Prepares the bot's message area."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, "Stuti: ", ("bot_label",))
        self.chat_area.config(state=tk.DISABLED)

    def append_bot_message(self, text):
        """Appends a chunk of the bot's message to the chat area."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, text)
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def show_typing_indicator(self, show):
        """Shows or removes the 'Stuti is typing...' indicator."""
        self.chat_area.config(state=tk.NORMAL)
        if show:
            self.chat_area.insert(tk.END, "Stuti is typing...", ("typing",))
        else:
            content = self.chat_area.get("1.0", tk.END)
            # A simple way to remove the last line if it's the typing indicator
            if "Stuti is typing..." in content.splitlines()[-1]:
                 self.chat_area.delete("end-1c linestart", "end")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
        
    def toggle_input_widgets(self, enabled):
        """Enables or disables the entry and send button."""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.entry.config(state=state)
        self.send_btn.config(state=state)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()


# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('rate', 120)
# # print(voices)
# for index, voice in enumerate(voices):
#     if(voice.name == 'Hindi'):
#         print(f"Voice #{index}:")
#         print(f"  - ID: {voice.id}")
#         print(f"  - Name: {voice.name}")
#         print(f"  - Languages: {voice.languages}")
#         print(f"  - Gender: {voice.gender}")
#         print(f"  - Age: {voice.age}")
#         print("---")
#    engine.setProperty('voice', voice.id)
#    engine.say('The quick brown fox jumped over the lazy dog.')
#    engine.runAndWait()

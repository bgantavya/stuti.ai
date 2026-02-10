import sqlite3
from datetime import datetime

class Memory:
    def __init__(self, db_name="memoryStuti.db"):
        self.db_name = db_name
        self.CreateTable()

    def CreateTable(self):
        """Creates the messages table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fact TEXT,
                    timestamp DATETIME
                )
            ''')
            conn.commit()

    def save_message(self, fact):
        """Saves a fact about user in memory."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO memory (fact, timestamp) VALUES (?, ?)",
                (fact, datetime.now())
            )
            conn.commit()

    def load_history(self, limit=20):
        """Fetches the last N messages to provide context to the AI."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT fact FROM memory ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            history = cursor.fetchall()
            return history[::-1]
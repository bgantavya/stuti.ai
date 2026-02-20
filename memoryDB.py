import os
import sqlite3
from datetime import datetime
from typing import TypeAlias

HistoryRow: TypeAlias = tuple[str, str, str]


class MemoryDB:
    def __init__(self, db_name: str | None = None) -> None:
        if db_name:
            self.db_name = db_name
        else:
            self.db_name = os.path.join(os.path.dirname(__file__), "memoryStuti.db")
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Creates or migrates the messages table."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME NOT NULL
                )
                """
            )

            cursor.execute("PRAGMA table_info(memory)")
            columns = {row[1] for row in cursor.fetchall()}

            if "fact" in columns and "message" not in columns:
                cursor.execute("ALTER TABLE memory RENAME TO memory_old")
                cursor.execute(
                    """
                    CREATE TABLE memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        role TEXT NOT NULL,
                        message TEXT NOT NULL,
                        timestamp DATETIME NOT NULL
                    )
                    """
                )
                cursor.execute(
                    """
                    INSERT INTO memory (role, message, timestamp)
                    SELECT 'user', fact, timestamp FROM memory_old
                    """
                )
                cursor.execute("DROP TABLE memory_old")

            conn.commit()

    def save_message(self, role: str, message: str) -> None:
        """Saves a chat message with role and timestamp."""
        if not message:
            return

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO memory (role, message, timestamp) VALUES (?, ?, ?)",
                (role, message, datetime.now())
            )
            conn.commit()

    def load_history(self, limit: int = 20) -> list[HistoryRow]:
        """Fetches the last N messages for chat context."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT role, message, timestamp
                FROM memory
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,)
            )
            history = cursor.fetchall()
            return history[::-1]


DB = MemoryDB
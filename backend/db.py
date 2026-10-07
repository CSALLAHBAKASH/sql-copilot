from __future__ import annotations

import sqlite3
from typing import Optional


DB_PATH = "history.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            sql TEXT,
            row_count INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def log_query(question: str, sql: Optional[str], row_count: Optional[int]):
    conn = get_connection()
    conn.execute(
        "INSERT INTO query_history (question, sql, row_count) VALUES (?, ?, ?)",
        (question, sql, row_count),
    )
    conn.commit()
    conn.close()
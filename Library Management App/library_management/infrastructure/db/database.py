
import sqlite3
from pathlib import Path
from typing import Iterator

DB_FILE = Path(__file__).resolve().parent / "lbmms.db"
import datetime

def write_log(entity: str, action: str, details: str):
    """Write a log entry with current timestamp into the logs table."""
    conn = get_connection()
    cur = conn.cursor()
    # Make sure logs table exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT,
            timestamp TEXT NOT NULL
        )
    ''')
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    ddl = '''
    CREATE TABLE IF NOT EXISTS members (
        member_id          INTEGER PRIMARY KEY,
        member_name        TEXT NOT NULL,
        member_contact     TEXT NOT NULL,
        member_type        TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS books (
        book_title          TEXT NOT NULL,
        book_author         TEXT NOT NULL,
        book_isbn           INTEGER PRIMARY KEY,
        book_genre          TEXT NOT NULL,
        book_availability   TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    entity TEXT NOT NULL,
    action TEXT NOT NULL,
    details TEXT
);
    '''
    with get_connection() as conn:
        conn.executescript(ddl)

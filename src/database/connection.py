from pathlib import Path
import sqlite3

DATABASE_PATH = Path(__file__).parent / "database.db"


def get_connection() -> sqlite3.Connection:
    """
    Returns a SQLite connection.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    # Access columns by name instead of index
    connection.row_factory = sqlite3.Row

    # Enable foreign keys
    connection.execute("PRAGMA foreign_keys = ON")

    return connection
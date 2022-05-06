import sqlite3
from contextlib import contextmanager


@contextmanager
def conn_context(db_path: str) -> sqlite3.Connection:
    """Контекстный менеджер для sqlite3 соединения.

    Args:
        db_path: str
    Yields:
        sqlite3.Connection
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()

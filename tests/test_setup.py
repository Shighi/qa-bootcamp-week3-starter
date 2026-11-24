"""Checks that your environment is ready for Week 3."""
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "shop.db"


def test_environment_is_ready_python_3_9_or_newer():
    # Needs Python 3.9 or newer, data/shop.db, and its four tables.
    assert sys.version_info >= (3, 9), f"Python 3.9 or newer is needed, you have {sys.version.split()[0]}"
    assert DB_PATH.is_file(), f"Can't find {DB_PATH}"
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        tables = {row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    finally:
        con.close()
    assert {"customers", "products", "orders", "order_items"} <= tables

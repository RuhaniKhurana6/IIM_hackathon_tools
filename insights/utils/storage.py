# insights/utils/storage.py
import sqlite3
from datetime import datetime
from typing import Dict, Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    amount REAL,
    category TEXT,
    merchant TEXT,
    raw_text TEXT,
    source TEXT
);
"""

def init_db(db_path="insights/data/transactions.db"):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    return conn

def insert_transaction(conn, tx: Dict[str, Any]):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (date, amount, category, merchant, raw_text, source) VALUES (?, ?, ?, ?, ?, ?)",
        (tx["date"], tx["amount"], tx.get("category","Uncategorized"), tx.get("merchant","Unknown"), tx.get("raw_text",""), tx.get("source","sms"))
    )
    conn.commit()
    return cur.lastrowid

def query_transactions_month(conn, year:int, month:int):
    # returns list of dicts in that month
    cur = conn.cursor()
    start = f"{year:04d}-{month:02d}-01"
    # compute next month for exclusive end
    if month == 12:
        end = f"{year+1:04d}-01-01"
    else:
        end = f"{year:04d}-{month+1:02d}-01"
    cur.execute("SELECT id, date, amount, category, merchant, raw_text, source FROM transactions WHERE date >= ? AND date < ?", (start, end))
    rows = cur.fetchall()
    cols = ["id","date","amount","category","merchant","raw_text","source"]
    return [dict(zip(cols, r)) for r in rows]

def query_transactions_range(conn, start_date, end_date):
    cur = conn.cursor()
    cur.execute("SELECT id, date, amount, category, merchant, raw_text, source FROM transactions WHERE date >= ? AND date < ?", (start_date, end_date))
    rows = cur.fetchall()
    cols = ["id","date","amount","category","merchant","raw_text","source"]
    return [dict(zip(cols, r)) for r in rows]

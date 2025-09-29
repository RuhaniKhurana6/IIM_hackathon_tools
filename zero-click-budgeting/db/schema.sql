CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT,
  ts DATETIME DEFAULT CURRENT_TIMESTAMP,
  source TEXT,
  merchant TEXT,
  category TEXT,
  amount REAL
);
CREATE TABLE IF NOT EXISTS budgets (
  user_id TEXT PRIMARY KEY,
  monthly_limit REAL,
  config TEXT
);
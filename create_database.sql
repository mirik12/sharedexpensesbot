-- Створення таблиці expenses
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    amount REAL,
    category TEXT,
    description TEXT
);

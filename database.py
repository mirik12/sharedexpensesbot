import sqlite3
from sqlite3 import Connection


class Expense:
    def __init__(self, user_id: int, name: str, amount: float, category: str, description: str):
        self.user_id = user_id
        self.name = name
        self.amount = amount
        self.category = category
        self.description = description


class Database:
    def __init__(self, db_name: str = 'expenses.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            amount REAL,
            category TEXT,
            description TEXT
        );
        """
        self.conn.execute(query)

    def add_expense(self, expense: Expense):
        query = """
        INSERT INTO expenses (user_id, name, amount, category, description) 
        VALUES (?, ?, ?, ?, ?);
        """
        self.conn.execute(query, (expense.user_id, expense.name,
                          expense.amount, expense.category, expense.description))
        self.conn.commit()

    def get_expenses(self, user_id: int):
        query = """
        SELECT * FROM expenses WHERE user_id = ?;
        """
        cursor = self.conn.execute(query, (user_id,))
        return cursor.fetchall()

    def close(self):
        self.conn.close()

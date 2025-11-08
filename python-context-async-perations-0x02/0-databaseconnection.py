#!/usr/bin/env python3
import sqlite3


class DatabaseConnection:
    """Custom class-based context manager for SQLite database connections."""
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection, even if an exception occurs."""
        if self.conn:
            self.conn.close()


# Using the custom context manager
if __name__ == "__main__":
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)

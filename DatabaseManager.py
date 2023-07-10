import sqlite3

class DatabaseManager:
    def __init__(self, dbpath):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()
        return conn, c

    def create_tables_if_not_exists(c):
        c.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                password TEXT,
                understanding INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
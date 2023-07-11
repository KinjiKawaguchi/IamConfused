import sqlite3

class DatabaseManager:
    def __init__(self, dbpath):
        self.conn = sqlite3.connect(dbpath)
        self.c = self.conn.cursor()

    def create_tables_if_not_exists(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                password TEXT,
                understanding INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
        self.conn.commit()

    def update_understanding(self, new_understanding, id_to_update):
        self.c.execute('UPDATE students SET understanding = ? WHERE id = ?', (new_understanding, id_to_update))
        self.conn.commit()


    def get_password(self,id):
        self.c.execute('SELECT password FROM students WHERE id = ?', (id,))
        password = self.c.fetchone()
        return password

    def register_student(self, id, password):
        self.c.execute('INSERT INTO students (id, password, understanding) VALUES (?, ?, NULL)', (id, password))
        self.conn.commit()

    def get_all_student(self):
        self.c.execute('SELECT * FROM students')
        students = self.c.fetchall()
        return students

    def get_student(self, id):
        self.c.execute('SELECT * FROM students WHERE id = ?', (id,))
        student = self.c.fetchone()
        return student

    def delete_student(self, id):
        self.c.execute('DELETE FROM students WHERE id = ?', (id,))
        self.conn.commit()

    def reset(self):
        self.c.execute('DELETE FROM students')
        self.conn.commit()

    def check_table_exists(self, table_name):
        self.c.execute("""
            SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}'
            """.format(table_name.replace('\'', '\'\'')))
        if self.c.fetchone()[0] == 1:
            return True
        return

    def count_student(self):
        self.c.execute('SELECT COUNT(*) FROM students')
        count = self.c.fetchone()[0]
        return count

    def get_understanding_distribution(self):
        understanding = self.c.execute('SELECT understanding, COUNT(*) FROM students WHERE understanding IS NOT NULL GROUP BY understanding')
        understanding = self.c.fetchall()
        return understanding

    def authenticate_admin(self, admin_username, admin_password):
        # Query the admin table
        self.c.execute("SELECT * FROM admin WHERE name = ? AND password = ?", (admin_username, admin_password))

        # Fetch one record
        record = self.c.fetchone()

        # If a record is found, return True, else return False
        if record is not None:
            return True
        else:
            return False

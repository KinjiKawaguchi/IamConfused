import streamlit as st
import sqlite3
from pages import student, teacher

# Connect to SQLite database
conn = sqlite3.connect('confused.db')
c = conn.cursor()

# Create table for students if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        password TEXT,
        understanding INTEGER
    )
''')
conn.commit()

# Authenticate user
id = st.text_input('学籍番号を入力してください')
password = st.text_input('誕生日を入力してください', type='password')
if id and password:
    c.execute('SELECT password FROM students WHERE id = ?', (id,))
    result = c.fetchone()
    if result is None:
        # Register new user
        c.execute('INSERT INTO students (id, password, understanding) VALUES (?, ?, NULL)', (id, password))
        conn.commit()
    elif result[0] != password:
        st.error('誕生日が間違っています')
        id = None  # Clear id to prevent access to pages

# Page routing
if id is not None:
    student.show_page(conn, id)
else:
    teacher.show_page(conn)

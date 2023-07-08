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
id = st.sidebar.text_input('学籍番号を入力してください')
password = st.sidebar.text_input('誕生日を入力してください', type='password')
if id and password:
    c.execute('SELECT password FROM students WHERE id = ?', (id,))
    result = c.fetchone()
    if result is None:
        # Register new user
        c.execute('INSERT INTO students (id, password, understanding) VALUES (?, ?, NULL)', (id, password))
        conn.commit()
    elif result[0] != password:
        st.sidebar.error('誕生日が間違っています')
        id = None  # Clear id to prevent access to pages

# Page routing
page = st.sidebar.selectbox('ページを選択', ['生徒向けページ', '先生向けページ'])

if page == '生徒向けページ' and id is not None:
    student.show_page(conn, id)
elif page == '先生向けページ':
    teacher.show_page(conn)

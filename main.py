import streamlit as st
import sqlite3
from pages import student, teacher

# Connect to SQLite database
conn = sqlite3.connect('confused.db')
c = conn.cursor()

# Create table for confused count if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS confused_count (
        id INTEGER PRIMARY KEY,
        count INTEGER
    )
''')

# Initialize count in database if it doesn't exist
c.execute('''
    INSERT INTO confused_count (id, count)
    SELECT 1, 0
    WHERE NOT EXISTS(SELECT 1 FROM confused_count WHERE id = 1)
''')
conn.commit()

# Page routing
page = st.sidebar.selectbox('ページを選択', ['生徒向けページ', '先生向けページ'])

if page == '生徒向けページ':
    student.show_page(conn)
elif page == '先生向けページ':
    teacher.show_page(conn)

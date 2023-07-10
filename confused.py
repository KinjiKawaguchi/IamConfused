import streamlit as st
import sqlite3
from pages import graph

conn = sqlite3.connect('confused.db')
c = conn.cursor()

# Create table for students if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        password TEXT,
        understanding INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()

id = None
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

understanding = None
if not id == None:
    # Define the options and their corresponding values
    options = [
        ('😭（全く理解できなかった）', 0),
        ('🥺（ほとんど理解できなかった）', 1),
        ('😨（大部分が理解できなかった）', 2),
        ('😰（多少は理解できたがまだ難しい）', 3),
        ('😕（あまり理解できなかった）', 4),
        ('😐（半分くらい理解できた）', 5),
        ('🙂（まあまあ理解できた）', 6),
        ('😊（ほぼ理解できた）', 7),
        ('😃（大部分を理解できた）', 8),
        ('😁（完全に理解できた）', 9)
    ]

    for option, value in options:
        if st.button(option):
            understanding = value
            # Update understanding in database
            c.execute('UPDATE students SET understanding = ? WHERE id = ?', (understanding, id))
            conn.commit()
            #st.write('理解度が更新されました')

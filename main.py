import streamlit as st
import sqlite3
from pages import teacher

class User:
    def __init__(self):
        self.id = None
        self.understanding = 5

# Connect to SQLite database4
user = User()

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


id = st.text_input('学籍番号を入力してください')
password = st.text_input('誕生日を入力してください', type='password')
if id and password:
    c.execute('SELECT password FROM students WHERE id = ?', (id,))
    result = c.fetchone()
    if result is None:
        # Register new user
        c.execute('INSERT INTO students (id, password, understanding) VALUES (?, ?, NULL)', (id, password))
        user.id = id
        conn.commit()
    elif result[0] != password:
        st.error('誕生日が間違っています')
        id = None  # Clear id to prevent access to pages
    else:
        user.id = id

if not user.id == None:
    # Page for students
    understanding = st.radio(
        '理解度を選択してください',
        [('😭（全く理解できなかった）', 0), ('🥺（ほとんど理解できなかった）', 1), ('😨（大部分が理解できなかった）', 2),
         ('😰（多少は理解できたがまだ難しい）', 3), ('😕（あまり理解できなかった）', 4), ('😐（半分くらい理解できた）', 5),
         ('🙂（まあまあ理解できた）', 6), ('😊（ほぼ理解できた）', 7), ('😃（大部分を理解できた）', 8), ('😁（完全に理解できた）', 9)])

    if understanding is None:
        understanding = 5
    # Update understanding in database
    c.execute('UPDATE students SET understanding = ? WHERE id = ?', (understanding, id))
    conn.commit()
    st.write('理解度が更新されました')
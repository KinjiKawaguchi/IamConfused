import streamlit as st
import sqlite3

def show_page(conn):
    c = conn.cursor()

    # Page for students
    username = st.text_input('ユーザー名を入力してください')
    if username:
        if st.button('わからない'):
            # Increment count in database
            c.execute('UPDATE confused_count SET count = count + 1 WHERE id = 1')
            conn.commit()

            # Get updated count from database
            c.execute('SELECT count FROM confused_count WHERE id = 1')
            count = c.fetchone()[0]
            st.write('あなたがわからないと押したら、わからない人の数が1増えました。現在のわからない人の数は {} 人です。'.format(count))

import streamlit as st
import sqlite3

def show_page(conn):
    c = conn.cursor()

    # Page for teacher
    # Get count from database
    c.execute('SELECT count FROM confused_count WHERE id = 1')
    count = c.fetchone()[0]
    st.write('現在のわからない人の数は {} 人です。'.format(count))

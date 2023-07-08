import streamlit as st
import sqlite3


def show_page(conn, id):
    c = conn.cursor()

    # Page for students
    understanding = st.radio(
        '理解度を選択してください',
        [('😭（全く理解できなかった）', 0), ('🥺（ほとんど理解できなかった）', 1), ('😨（大部分が理解できなかった）', 2),
         ('😰（多少は理解できたがまだ難しい）', 3), ('😕（あまり理解できなかった）', 4), ('😐（半分くらい理解できた）', 5),
         ('🙂（まあまあ理解できた）', 6), ('😊（ほぼ理解できた）', 7), ('😃（大部分を理解できた）', 8), ('😁（完全に理解できた）', 9)])

    if understanding is not None:
        # Update understanding in database
        c.execute('UPDATE students SET understanding = ? WHERE id = ?', (understanding, id))
        conn.commit()
        st.write('理解度が更新されました')

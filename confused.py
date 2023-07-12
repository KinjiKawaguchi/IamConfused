import streamlit as st
from DatabaseManager import DatabaseManager

db = DatabaseManager('confused.db')
db.create_tables_if_not_exists()

login = False
id = st.text_input('学籍番号を入力してください')
password = st.text_input('誕生日を入力してください', type='password')
if id and password:
    result = db.get_password(id)
    if result is None:
        # Register new user
        db.register_student(id, password)
        login = True
    elif result[0] != password:
        st.error('誕生日が間違っています')
        id = None  # Clear id to prevent access to pages
        login = False
    elif result[0] == password:
        st.write("ログインに成功しました。")
        login = True
else:
    st.write("学籍番号と誕生日を入力してください。")

understanding = None
if login:
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
            db.update_understanding(id, understanding)
            
import streamlit as st

# データベースマネージャークラスは適切な実装を想定しています
from DatabaseManager import DatabaseManager

db = DatabaseManager('confused.db')
db.create_tables_if_not_exists()

# セッションステートの初期化
if 'login' not in st.session_state:
    st.session_state['login'] = False
if 'wtp' not in st.session_state:
    st.session_state['wtp'] = None
if 'current_offer' not in st.session_state:
    st.session_state['current_offer'] = 2000  # 最初のオファー

id = st.text_input('学籍番号を入力してください')
password = st.text_input('誕生日を入力してください', type='password')

# ログイン処理
if id and password and not st.session_state['login']:
    result = db.get_password(id)
    if result is None:
        db.register_student(id, password)
        st.session_state['login'] = True
    elif result[0] != password:
        st.error('誕生日が間違っています')
    elif result[0] == password:
        st.session_state['login'] = True

# ユーザーがログインしている場合にWTPアンケートを表示
if st.session_state['login']:
    st.write(f"次の商品に対して、あなたが支払う意思がある最大金額は {st.session_state['current_offer']} 円ですか？")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button('はい'):
            # はいと回答した場合、セッションステートのWTPを更新し、次のオファーを設定
            st.session_state['wtp'] = st.session_state['current_offer']
            if st.session_state['current_offer'] < 5000:  # 最大オファーまで繰り返す
                st.session_state['current_offer'] += 1000  # 次のオファー額を増やす
            else:
                st.success(f'あなたの支払い意思価格は {st.session_state['wtp']} 円です。')
                db.register_wtp_response(id, st.session_state['wtp'])  # DBに登録する
    with col2:
        if st.button('いいえ'):
            # いいえと回答した場合、現在のオファーを最終的なWTPとして記録
            if st.session_state['wtp'] is None:  # まだWTPが記録されていない場合
                st.session_state['wtp'] = 0  # WTPを0として記録
            st.success(f'あなたの支払い意思価格は {st.session_state['wtp']} 円です。')
            db.register_wtp_response(id, st.session_state['wtp'])  # DBに登録する
            st.session_state['current_offer'] = 0  # オファーをリセット

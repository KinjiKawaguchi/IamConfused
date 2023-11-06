import streamlit as st
from DatabaseManager import DatabaseManager

# DatabaseManagerの初期化
db = DatabaseManager('wtp.db')
db.create_tables_if_not_exists()

# ユーザー認証のフラグ
login = False

# ユーザーIDとパスワード入力フィールド
id = st.text_input('学籍番号を入力してください')
password = st.text_input('誕生日を入力してください', type='password')

# ログイン処理
if id and password:
    result = db.get_password(id)
    if result is None:
        # 新規ユーザー登録
        db.register_student(id, password)
        login = True
    elif result[0] != password:
        st.error('誕生日が間違っています')
        login = False
    else:
        st.success("ログインに成功しました。")
        login = True

# ログインしていなければ指示を出力
if not login:
    st.warning("学籍番号と誕生日を入力してください。")

# WTP質問フロー
if login:
    # 状態遷移の辞書
    state_transitions = {
        2000: {'払う': 3000, '払えない': 1000},
        3000: {'払える': 4000, '払えない': '終了(2000-3000)'},
        4000: {'払える': '終了(4000-)', '払えない': '終了(3000-4000)'},
        1000: {'払える': '終了(1000-2000)', '払えない': '終了(-1000)'}
    }

    # ユーザーの現在の状態
    current_state = 2000  # 初期状態

    # 状態とボタンを表示
    st.write(f"現在の価格: ¥{current_state}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button('払える'):
            next_state = state_transitions[current_state].get('払える')
    with col2:
        if st.button('払えない'):
            next_state = state_transitions[current_state].get('払えない')

    # 次の状態が終了状態ならばデータベースに記録して結果を表示
    if isinstance(next_state, str) and next_state.startswith('終了'):
        st.success(f"あなたのWTPは {next_state} です。")
        # データベースにWTPを記録するコードをここに書く
        # 例: db.record_wtp(id, current_state, next_state)
    elif next_state:
        # 状態を更新して再度表示
        current_state = next_state
        st.experimental_rerun()

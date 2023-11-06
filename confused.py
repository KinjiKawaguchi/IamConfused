import streamlit as st

# 状態遷移の辞書
transitions = {
    2000: {'払う': 3000, '払えない': 1000},
    3000: {'払う': 4000, '払えない': '終了 (2000-3000)'},
    4000: {'払う': '終了 (4000-)', '払えない': '終了 (3000-4000)'},
    1000: {'払う': '終了 (1000-2000)', '払えない': '終了 (-1000)'}
}

# セッションステートの初期化
if 'current_offer' not in st.session_state:
    st.session_state['current_offer'] = 2000

# ユーザーのレスポンスに応じた処理を行う関数
def handle_response(response):
    if st.session_state['current_offer'] in transitions:
        next_state = transitions[st.session_state['current_offer']][response]
        
        if isinstance(next_state, int):  # まだ終了していない場合
            st.session_state['current_offer'] = next_state
        else:  # 終了する場合
            st.success(next_state)
            st.session_state['current_offer'] = '終了'

# アンケートの質問と応答ボタンを表示
if isinstance(st.session_state['current_offer'], int):
    st.write(f"あなたは {st.session_state['current_offer']} 円を支払う意思がありますか？")

    if st.button('払える'):
        handle_response('払う')
    elif st.button('払えない'):
        handle_response('払えない')
else:
    st.write("アンケートは終了しました。")

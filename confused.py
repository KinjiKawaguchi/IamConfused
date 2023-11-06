import streamlit as st

# セッションステートで現在の金額を追跡します
if 'current_offer' not in st.session_state:
    st.session_state['current_offer'] = 2000  # 初期オファー

# ユーザーが「払える」または「払えない」と答えた場合のロジックを関数にまとめます
def handle_response(response):
    current_offer = st.session_state['current_offer']
    
    # ユーザーの応答に基づいて次の状態に遷移します
    if current_offer == 2000:
        if response == '払う':
            st.session_state['current_offer'] = 3000
        else:  # '払えない'
            st.session_state['current_offer'] = 1000
    
    elif current_offer == 1000:
        if response == '払える':
            st.success('終了 (1000-2000)')
            st.session_state['current_offer'] = '終了'
        else:  # '払えない'
            st.success('終了 (-1000)')
            st.session_state['current_offer'] = '終了'
    
    elif current_offer == 3000:
        if response == '払えない':
            st.success('終了 (2000-3000)')
            st.session_state['current_offer'] = '終了'
        else:  # '払える'
            st.session_state['current_offer'] = 4000
    
    elif current_offer == 4000:
        if response == '払えない':
            st.success('終了 (3000-4000)')
            st.session_state['current_offer'] = '終了'
        else:  # '払える'
            st.success('終了 (4000-)')
            st.session_state['current_offer'] = '終了'

# アンケートの質問と応答ボタンを表示します
if st.session_state['current_offer'] != '終了':
    st.write(f"あなたは {st.session_state['current_offer']} 円を支払う意思がありますか？")
    
    if st.button('払える'):
        handle_response('払う')
    elif st.button('払えない'):
        handle_response('払えない')
else:
    st.write("アンケートは終了しました。")

import streamlit as st

# 初期設定
if 'current_offer' not in st.session_state:
    st.session_state['current_offer'] = 2000

# 終了状態をチェックする関数
def is_ended(offer):
    return isinstance(offer, str) and offer.startswith('終了')

# ユーザーのレスポンスを処理する関数
def update_offer(agree):
    if agree:
        # 払うことに同意した場合
        if st.session_state['current_offer'] == 2000:
            st.session_state['current_offer'] = 3000
        elif st.session_state['current_offer'] == 3000:
            st.session_state['current_offer'] = 4000
        elif st.session_state['current_offer'] == 4000:
            st.session_state['current_offer'] = '終了 (4000以上)'
    else:
        # 払うことに同意しなかった場合
        if st.session_state['current_offer'] == 2000:
            st.session_state['current_offer'] = 1000
        elif st.session_state['current_offer'] == 3000:
            st.session_state['current_offer'] = '終了 (2000-3000)'
        elif st.session_state['current_offer'] == 1000:
            st.session_state['current_offer'] = '終了 (1000以下)'

# メインアプリケーション
def main():
    if is_ended(st.session_state['current_offer']):
        st.write(st.session_state['current_offer'])
    else:
        st.write(f"あなたは {st.session_state['current_offer']} 円を支払う意思がありますか？")

        agree_key = f"agree_{st.session_state['current_offer']}"
        disagree_key = f"disagree_{st.session_state['current_offer']}"

        col1, col2 = st.columns(2)
        with col1:
            if st.button('払える', key=agree_key):
                update_offer(True)
        with col2:
            if st.button('払えない', key=disagree_key):
                update_offer(False)

        # 再描画を避けるために状態の変更後に即時アップデートする
        st.experimental_rerun()

main()

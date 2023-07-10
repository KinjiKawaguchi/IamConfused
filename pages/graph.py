import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from DatabaseManager import DatabaseManager

def showGraph():
    db = DatabaseManager.create_tables_if_not_exists('confused.db')

    db.create_tables_if_not_exists()

    db.check_table_exists('students')


    # studentsテーブルが存在すれば以下のクエリを実行
    if db.check_table_exists('students'):
        if db.count_student() > 0:
            result = db.get_understanding_distribution()

            # Show as a bar chart
            df = pd.DataFrame(results, columns=['Understanding', 'Count'])
            df = df.sort_values('Understanding')
            plt.bar(df['Understanding'], df['Count'], tick_label=df['Understanding'])
            plt.xlabel('Understanding')
            plt.ylabel('Count')
            plt.title('Understanding Distribution')
            st.pyplot(plt.gcf())
            plt.clf()
        else:
            print("No records in the table.")

    # データベース接続を閉じる
    conn.close()


# Run the function once
showGraph()

# And schedule it to run every 10 seconds
'''
state = st.session_state
if "run_id" not in state:
    state.run_id = 0

while True:
    showGraph()
    state.run_id += 1
    time.sleep(10)
'''
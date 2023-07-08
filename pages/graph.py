import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import time


def showGraph():
    conn = sqlite3.connect('confused.db')
    c = conn.cursor()

    # Create table for students if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            password TEXT,
            understanding INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # テーブルが存在するか確認
    def check_table_exists(db_con, table_name):
        db_cur = db_con.cursor()
        db_cur.execute("""
            SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}'
            """.format(table_name.replace('\'', '\'\'')))
        if db_cur.fetchone()[0] == 1:
            return True
        return False

    # studentsテーブルが存在すれば以下のクエリを実行
    if check_table_exists(conn, 'students'):
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM students')
        count = c.fetchone()[0]

        if count > 0:
            c.execute(
                'SELECT understanding, COUNT(*) FROM students WHERE understanding IS NOT NULL GROUP BY understanding')
            results = c.fetchall()

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
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from DatabaseManager import DatabaseManager

def showGraph(slot):
    db = DatabaseManager('confused.db')

    db.create_tables_if_not_exists()

    if db.check_table_exists('students'):
        if db.count_student() > 0:
            results = db.get_understanding_distribution()

            df = pd.DataFrame(results, columns=['Understanding', 'Count'])
            df = df.sort_values('Understanding')
            plt.bar(df['Understanding'], df['Count'], tick_label=df['Understanding'])
            plt.xlabel('Understanding')
            plt.ylabel('Count')
            plt.title('Understanding Distribution')
            slot.pyplot(plt.gcf())  # use the provided slot to show the plot
            plt.clf()
        else:
            print("[graph.py]No records in the table.")

# Create an empty slot
plot_slot = st.empty()

state = st.session_state
if "run_id" not in state:
    state.run_id = 0

# And schedule it to run every 10 seconds
while True:
    showGraph(plot_slot)  # use the same slot every time
    state.run_id += 1
    time.sleep(10)

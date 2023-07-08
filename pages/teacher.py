import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('confused.db')
c = conn.cursor()

# Page for teacher
# Get understanding counts from database
c.execute('SELECT understanding, COUNT(*) FROM students WHERE understanding IS NOT NULL GROUP BY understanding')
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

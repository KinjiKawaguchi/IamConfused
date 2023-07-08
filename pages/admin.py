import streamlit as st
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('confused.db')
c = conn.cursor()

# Fetch all student data
c.execute('SELECT * FROM students')
students = c.fetchall()

# Display all student data
st.write('All student data:')
for student in students:
    st.write(student)

# Allow admin to update understanding of a student
st.write('Update student understanding:')
id_to_update = st.text_input('Enter student ID')
new_understanding = st.number_input('Enter new understanding level', min_value=0, max_value=9)
if st.button('Update understanding'):
    c.execute('UPDATE students SET understanding = ? WHERE id = ?', (new_understanding, id_to_update))
    conn.commit()
    st.write('Understanding updated.')

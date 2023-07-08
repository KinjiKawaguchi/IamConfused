import streamlit as st
import sqlite3
import pandas as pd
from faker import Faker
import random

# Enter password
password = st.text_input("Enter password", type='password')
if password == 'caretaker':
    # Connect to SQLite database
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

    # Fetch all student data
    c.execute('SELECT * FROM students')
    students = c.fetchall()

    # Display all student data in a table
    st.write('All student data:')
    df = pd.DataFrame(students, columns=['ID', 'Password', 'Understanding','CreatedAt'])
    st.dataframe(df)

    # Allow admin to perform CRUD operations
    st.write('CRUD operations:')

    operation = st.selectbox('Choose operation', ['Create', 'Read', 'Update', 'Delete'])

    if operation == 'Create':
        new_id = st.text_input('Enter new ID')
        new_password = st.text_input('Enter new password')
        new_understanding = st.number_input('Enter understanding level', min_value=0, max_value=9)
        if st.button('Create student'):
            c.execute('INSERT INTO students (id, password, understanding) VALUES (?, ?, ?)',
                      (new_id, new_password, new_understanding))
            conn.commit()
            st.write('Student created.')

    elif operation == 'Read':
        id_to_read = st.text_input('Enter ID to read')
        if st.button('Read student'):
            c.execute('SELECT * FROM students WHERE id = ?', (id_to_read,))
            student = c.fetchone()
            st.write(student)

    elif operation == 'Update':
        id_to_update = st.text_input('Enter ID to update')
        new_understanding = st.number_input('Enter new understanding level', min_value=0, max_value=9)
        if st.button('Update student'):
            c.execute('UPDATE students SET understanding = ? WHERE id = ?', (new_understanding, id_to_update))
            conn.commit()
            st.write('Student updated.')

    elif operation == 'Delete':
        id_to_delete = st.text_input('Enter ID to delete')
        if st.button('Delete student'):
            c.execute('DELETE FROM students WHERE id = ?', (id_to_delete,))
            conn.commit()
            st.write('Student deleted.')

    # Allow admin to reset the database
    if st.button('Reset database'):
        c.execute('DELETE FROM students')
        conn.commit()
        st.write('Database reset.')

    # Allow admin to add 100 random students
    if st.button('Add 100 random students'):
        fake = Faker()
        for _ in range(100):
            id = fake.unique.random_number(digits=8)
            password = fake.password(length=8)
            understanding = random.randint(0, 9)
            c.execute('INSERT INTO students (id, password, understanding) VALUES (?, ?, ?)', (id, password, understanding))
        conn.commit()
        st.write('100 random students added.')
else:
    st.write('Please enter your password to access this page.')

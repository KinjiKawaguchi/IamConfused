import hashlib
import streamlit as st
import pandas as pd
from faker import Faker
import random
from DatabaseManager import DatabaseManager

# Enter admin credentials
admin_username = st.text_input("Enter admin username")
admin_password = hashlib.sha256(st.text_input("Enter admin password", type='password').encode()).hexdigest()



# Connect to SQLite database
db = DatabaseManager('confused.db')
db.create_tables_if_not_exists()

# Check if the entered admin credentials are correct
if db.authenticate_admin(admin_username, admin_password):
    # Connect to SQLite database
    db = DatabaseManager('confused.db')
    db.create_tables_if_not_exists()

    # Fetch all student data
    students = db.get_all_student()

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
            db.register_student(new_id, new_password)
            st.write('Student created.')

    elif operation == 'Read':
        id_to_read = st.text_input('Enter ID to read')
        if st.button('Read student'):
            student = db.get_student(id_to_read)
            st.write(student)

    elif operation == 'Update':
        id_to_update = st.text_input('Enter ID to update')
        new_understanding = st.number_input('Enter new understanding level', min_value=0, max_value=9)
        if st.button('Update student'):
            db.update_understanding(id_to_update, new_understanding)
            st.write('Student updated.')

    elif operation == 'Delete':
        id_to_delete = st.text_input('Enter ID to delete')
        if st.button('Delete student'):
            db.delete_student(id_to_delete)
            st.write('Student deleted.')

    # Allow admin to reset the database
    if st.button('Reset database'):
        db.reset()
        st.write('Database reset.')

    # Allow admin to add 100 random students
    if st.button('Add 100 random students'):
        fake = Faker()
        for _ in range(100):
            id = fake.unique.random_number(digits=8)
            password = fake.password(length=8)
            understanding = random.randint(0, 9)
            db.register_student(id, password)
            db.update_understanding(understanding, id)
        st.write('100 random students added.')
else:
    st.write('Please enter your password to access this page.')

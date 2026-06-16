import streamlit as st
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql@123",
        database="crypto_risk_db"
    )

st.title("User Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM User WHERE username=%s AND password_hash=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            st.success("Login successful!")
            st.write(f"Welcome, {username}")
        else:
            st.error("Invalid username or password")

    except Exception as e:
        st.error("Error connecting to database")
        st.write(e)
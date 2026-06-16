import streamlit as st
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql@123",
        database="crypto_risk_db"
    )

st.title("Database Connection Test")

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User")
    data = cursor.fetchall()

    st.success("Database connected successfully!")
    st.write("User table data:")
    st.dataframe(data)

except Exception as e:
    st.error("Database connection failed")
    st.write(e)
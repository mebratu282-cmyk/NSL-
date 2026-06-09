import oracledb
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
def get_connection():
    try:
        connection = oracledb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            service_name=os.getenv("DB_SERVICE_NAME")
        )
        return connection
    except oracledb.DatabaseError as e:
        print(f"Database connection error: {e}")
        return None
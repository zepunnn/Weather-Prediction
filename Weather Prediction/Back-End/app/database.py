import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG ={
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", ""),
    "database": os.getenv("DB_NAME", "bmkg_data"),
}

def get_connection():
    """Membuat koneksi database baru."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print("[DB ERROR]", e)
        return None
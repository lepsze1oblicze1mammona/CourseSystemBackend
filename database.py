import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def get_db_connection():
    conn = sqlite3.connect(db_file)
    return conn

def check_course_exists(course_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM WszystkieKursy WHERE nazwa=?", (course_name,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
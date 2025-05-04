import sqlite3
import os

def get_db_connection():
    conn = sqlite3.connect('/etc/sn/baza.db')
    return conn

def check_course_exists(course_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM WszystkieKursy WHERE nazwa=?", (course_name,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def zmien_termin_zadania(nazwa_kursu, nazwa_zadania, nowy_termin):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    c.execute("UPDATE KursNazwa SET termin_realizacji=? WHERE nazwa=? AND kurs_id=(SELECT id FROM WszystkieKursy WHERE nazwa=?)", (nowy_termin, nazwa_zadania, nazwa_kursu))
    
    conn.commit()
    conn.close()
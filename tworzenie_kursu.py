import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def stworz_kurs(nazwa, wlasciciel_id):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Sprawdź unikalność nazwy
    c.execute("SELECT id FROM WszystkieKursy WHERE nazwa=?", (nazwa,))
    if c.fetchone():
        print("Kurs o tej nazwie już istnieje!")
        return
    
    # Dodaj do bazy
    c.execute("INSERT INTO WszystkieKursy (nazwa, wlasciciel) VALUES (?, ?)", (nazwa, wlasciciel_id))
    kurs_id = c.lastrowid
    
    # Utwórz folder
    sciezka = f"etc/sn/Kursy/{nazwa}"
    os.makedirs(sciezka, exist_ok=True)
    
    conn.commit()
    conn.close()
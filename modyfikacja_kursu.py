import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def zmien_nazwe_kursu(stara_nazwa, nowa_nazwa):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Aktualizuj nazwę w bazie
    c.execute("UPDATE WszystkieKursy SET nazwa=? WHERE nazwa=?", (nowa_nazwa, stara_nazwa))
    
    # Zmień nazwę folderu
    stara_sciezka = f"etc/sn/Kursy/{stara_nazwa}"
    nowa_sciezka = f"etc/sn/Kursy/{nowa_nazwa}"
    os.rename(stara_sciezka, nowa_sciezka)
    
    conn.commit()
    conn.close()
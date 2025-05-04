import sqlite3
import shutil

def usun_zadanie(nazwa_kursu, nazwa_zadania):
    conn = sqlite3.connect('baza.db')
    c = conn.cursor()
    
    # Znajdź ID kursu
    c.execute("SELECT id FROM WszystkieKursy WHERE nazwa=?", (nazwa_kursu,))
    kurs_id = c.fetchone()[0]
    
    # Usuń z bazy
    c.execute("DELETE FROM KursNazwa WHERE nazwa=? AND kurs_id=?", (nazwa_zadania, kurs_id))
    
    # Usuń folder
    sciezka = f"/etc/sn/Kursy/{nazwa_kursu}/Zadania/{nazwa_zadania}"
    shutil.rmtree(sciezka)
    
    conn.commit()
    conn.close()
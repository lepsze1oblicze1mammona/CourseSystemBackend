import sqlite3
import shutil

def usun_kurs(nazwa):
    conn = sqlite3.connect('baza.db')
    c = conn.cursor()
    
    # Usuń z bazy
    c.execute("DELETE FROM WszystkieKursy WHERE nazwa=?", (nazwa,))
    
    # Usuń folder
    sciezka = f"/etc/sn/Kursy/{nazwa}"
    shutil.rmtree(sciezka)
    
    conn.commit()
    conn.close()
import sqlite3
import shutil
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def usun_zadanie(nazwa_kursu, nazwa_zadania):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Znajdź ID kursu
    c.execute("SELECT id FROM WszystkieKursy WHERE nazwa=?", (nazwa_kursu,))
    kurs_id = c.fetchone()[0]
    
    # Usuń z bazy
    c.execute("DELETE FROM KursNazwa WHERE nazwa=? AND kurs_id=?", (nazwa_zadania, kurs_id))
    
    # Usuń folder
    sciezka = f"etc/sn/Kursy/{nazwa_kursu}/Zadania/{nazwa_zadania}"
    shutil.rmtree(sciezka)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    nazwa_kursu = input("Podaj nazwę kursu: ")
    nazwa_zadania = input("Podaj nazwę zadania do usunięcia: ")
    
    # Wywołanie funkcji usuwającej zadanie
    usun_zadanie(nazwa_kursu, nazwa_zadania)
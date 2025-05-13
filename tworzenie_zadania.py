import sqlite3
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def stworz_zadanie(nazwa_kursu, nazwa_zadania, termin):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Znajdź ID kursu
    c.execute("SELECT id FROM WszystkieKursy WHERE nazwa=?", (nazwa_kursu,))
    kurs_id = c.fetchone()
    if not kurs_id:
        print("Kurs nie istnieje!")
        return
    
    # Dodaj zadanie do bazy
    c.execute("INSERT INTO KursNazwa (nazwa, termin_realizacji, kurs_id) VALUES (?, ?, ?)", 
              (nazwa_zadania, termin, kurs_id[0]))
    
    # Utwórz folder zadania
    sciezka = f"etc/sn/Kursy/{nazwa_kursu}/Zadania/{nazwa_zadania}"
    os.makedirs(sciezka, exist_ok=True)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tworzenie nowego zadania")
    parser.add_argument('--nazwa_kursu', required=True, help="Nazwa kursu")
    parser.add_argument('--nazwa_zadania', required=True, help="Nazwa zadania")
    parser.add_argument('--termin', required=True, help="Termin realizacji zadania (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    stworz_zadanie(args.nazwa_kursu, args.nazwa_zadania, args.termin)
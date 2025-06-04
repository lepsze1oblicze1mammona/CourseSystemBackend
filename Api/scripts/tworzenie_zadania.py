import sqlite3
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "baza.db")

def stworz_zadanie(nazwa_kursu, nazwa_zadania, opis, termin):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Znajdź ID kursu po nazwie
    c.execute("SELECT id FROM WszystkieKursy WHERE nazwa=?", (nazwa_kursu,))
    row = c.fetchone()
    if not row:
        print(f"Kurs '{nazwa_kursu}' nie istnieje!")
        conn.close()
        return
    kurs_id = row[0]
    
    # Dodaj zadanie do bazy z opisem
    c.execute("INSERT INTO KursNazwa (nazwa, opis, termin_realizacji, kurs_id) VALUES (?, ?, ?, ?)", 
              (nazwa_zadania, opis, termin, kurs_id))
    
    # Utwórz folder zadania
    sciezka = os.path.join(BASE_DIR, "etc", "sn", "Kursy", nazwa_kursu, "Zadania", nazwa_zadania)
    os.makedirs(sciezka, exist_ok=True)
    
    conn.commit()
    conn.close()
    print(f"Zadanie '{nazwa_zadania}' zostało utworzone w kursie '{nazwa_kursu}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tworzenie nowego zadania")
    parser.add_argument('--nazwa_kursu', required=True, help="Nazwa kursu")
    parser.add_argument('--nazwa_zadania', required=True, help="Nazwa zadania")
    parser.add_argument('--opis', required=True, help="Opis zadania")
    parser.add_argument('--termin', required=True, help="Termin realizacji zadania (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    stworz_zadanie(args.nazwa_kursu, args.nazwa_zadania, args.opis, args.termin)
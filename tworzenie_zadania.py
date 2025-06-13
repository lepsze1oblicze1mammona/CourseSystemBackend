import sqlite3
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def stworz_zadanie(kurs_id, nazwa_zadania, opis, termin):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Sprawdź czy kurs istnieje
    c.execute("SELECT id FROM WszystkieKursy WHERE id=?", (kurs_id,))
    row = c.fetchone()
    if not row:
        print(f"Kurs o id '{kurs_id}' nie istnieje!")
        conn.close()
        return

    # Dodaj zadanie do bazy z opisem
    c.execute("INSERT INTO KursNazwa (nazwa, opis, termin_realizacji, kurs_id) VALUES (?, ?, ?, ?)", 
              (nazwa_zadania, opis, termin, kurs_id))

    # Utwórz folder zadania
    # Pobierz nazwę kursu do ścieżki
    c.execute("SELECT nazwa FROM WszystkieKursy WHERE id=?", (kurs_id,))
    kurs_nazwa = c.fetchone()[0]
    sciezka = os.path.join(BASE_DIR, "etc", "sn", "Kursy", kurs_nazwa, "Zadania", nazwa_zadania)
    os.makedirs(sciezka, exist_ok=True)

    conn.commit()
    conn.close()
    print(f"Zadanie '{nazwa_zadania}' zostało utworzone w kursie o id '{kurs_id}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tworzenie nowego zadania")
    parser.add_argument('--kurs_id', required=True, type=int, help="ID kursu")
    parser.add_argument('--nazwa_zadania', required=True, help="Nazwa zadania")
    parser.add_argument('--opis', required=True, help="Opis zadania")
    parser.add_argument('--termin', required=True, help="Termin realizacji zadania (YYYY-MM-DD)")

    args = parser.parse_args()

    stworz_zadanie(args.kurs_id, args.nazwa_zadania, args.opis, args.termin)
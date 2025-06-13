import sqlite3
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def zmien_termin_zadania(kurs_id, nazwa_zadania, nowy_termin):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Sprawdź czy kurs istnieje
    c.execute("SELECT nazwa FROM WszystkieKursy WHERE id=?", (kurs_id,))
    row = c.fetchone()
    if not row:
        print(f"Kurs o id '{kurs_id}' nie istnieje!")
        conn.close()
        return
    nazwa_kursu = row[0]
    
    # Zmień termin zadania po nazwie i kursie
    c.execute("UPDATE KursNazwa SET termin_realizacji=? WHERE nazwa=? AND kurs_id=?", (nowy_termin, nazwa_zadania, kurs_id))
    
    if c.rowcount == 0:
        print(f"Nie znaleziono zadania '{nazwa_zadania}' w kursie o id '{kurs_id}'.")
    else:
        print(f"Termin zadania '{nazwa_zadania}' w kursie o id '{kurs_id}' został zmieniony na {nowy_termin}.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modyfikacja terminu zadania")
    parser.add_argument('--kurs_id', required=True, type=int, help="ID kursu")
    parser.add_argument('--nazwa_zadania', required=True, help="Nazwa zadania")
    parser.add_argument('--nowy_termin', required=True, help="Nowy termin realizacji (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    zmien_termin_zadania(args.kurs_id, args.nazwa_zadania, args.nowy_termin)
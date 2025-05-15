import sqlite3
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def zmien_termin_zadania(nazwa_kursu, nazwa_zadania, nowy_termin):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Pobierz id kursu po nazwie
    c.execute("SELECT id FROM WszystkieKursy WHERE nazwa=?", (nazwa_kursu,))
    row = c.fetchone()
    if not row:
        print(f"Kurs '{nazwa_kursu}' nie istnieje!")
        conn.close()
        return
    kurs_id = row[0]
    
    # Zmień termin zadania po nazwie i kursie
    c.execute("UPDATE KursNazwa SET termin_realizacji=? WHERE nazwa=? AND kurs_id=?", (nowy_termin, nazwa_zadania, kurs_id))
    
    if c.rowcount == 0:
        print(f"Nie znaleziono zadania '{nazwa_zadania}' w kursie '{nazwa_kursu}'.")
    else:
        print(f"Termin zadania '{nazwa_zadania}' w kursie '{nazwa_kursu}' został zmieniony na {nowy_termin}.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modyfikacja terminu zadania")
    parser.add_argument('--nazwa_kursu', required=True, help="Nazwa kursu")
    parser.add_argument('--nazwa_zadania', required=True, help="Nazwa zadania")
    parser.add_argument('--nowy_termin', required=True, help="Nowy termin realizacji (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    zmien_termin_zadania(args.nazwa_kursu, args.nazwa_zadania, args.nowy_termin)
import sqlite3
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "baza.db")

def zmien_termin_zadania(kurs_id, zadanie_id, nowy_termin):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Sprawdź kurs
    c.execute("SELECT nazwa FROM WszystkieKursy WHERE id=?", (kurs_id,))
    if not c.fetchone():
        print(f"Kurs o id '{kurs_id}' nie istnieje!")
        conn.close()
        return

    # Zmień termin
    c.execute(
        "UPDATE KursNazwa SET termin_realizacji=? WHERE id=? AND kurs_id=?",
        (nowy_termin, zadanie_id, kurs_id)
    )
    if c.rowcount == 0:
        print(f"Nie znaleziono zadania o id '{zadanie_id}' w kursie '{kurs_id}'.")
    else:
        print(f"Termin zadania id={zadanie_id} zmieniony na {nowy_termin}.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modyfikacja terminu zadania")
    parser.add_argument('--kurs_id', required=True, type=int, help="ID kursu")
    parser.add_argument('--zadanie_id', required=True, type=int, help="ID zadania")
    parser.add_argument('--nowy_termin', required=True, help="Nowy termin YYYY-MM-DD")
    args = parser.parse_args()
    zmien_termin_zadania(args.kurs_id, args.zadanie_id, args.nowy_termin)
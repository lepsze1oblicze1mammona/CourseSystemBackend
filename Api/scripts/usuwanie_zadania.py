import sqlite3
import shutil
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "baza.db")

def usun_zadanie(kurs_id, zadanie_id):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Sprawdź kurs
    c.execute("SELECT nazwa FROM WszystkieKursy WHERE id=?", (kurs_id,))
    row = c.fetchone()
    if not row:
        print(f"Kurs o id '{kurs_id}' nie istnieje!")
        conn.close()
        return
    nazwa_kursu = row[0]

    c.execute("SELECT nazwa FROM KursNazwa WHERE id=? AND kurs_id=?", (zadanie_id, kurs_id))
    nazwa_zadania = c.fetchone()[0]

    # Usuń rekord
    c.execute("DELETE FROM KursNazwa WHERE id=? AND kurs_id=?", (zadanie_id, kurs_id))
    if c.rowcount == 0:
        print(f"Zadanie id={zadanie_id} nie istnieje w kursie '{kurs_id}'!")
        conn.close()
        return

    # Usuń folder
    sciezka = os.path.join(
        BASE_DIR, "etc", "sn", "Kursy",
        nazwa_kursu, "Zadania", nazwa_zadania
    )
    if os.path.exists(sciezka):
        shutil.rmtree(sciezka)
        print(f"Folder zadania id={zadanie_id} usunięty.")
    else:
        print(f"Folder zadania id={zadanie_id} nie znaleziony.")

    conn.commit()
    conn.close()
    print(f"Zadanie id={zadanie_id} usunięte z kursu {kurs_id}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usuwanie zadania")
    parser.add_argument('--kurs_id', required=True, type=int, help="ID kursu")
    parser.add_argument('--zadanie_id', required=True, type=int, help="ID zadania")
    args = parser.parse_args()
    usun_zadanie(args.kurs_id, args.zadanie_id)
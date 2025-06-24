# NEW FILE
import sqlite3
import json
import glob
import os
import argparse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "baza.db")

def sprawdz_plik(student_login, kurs_id, zadanie_id):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Pobierz id użytkownika
    c.execute("SELECT id FROM users WHERE email=?", (student_login,))
    user = c.fetchone()
    if not user:
        conn.close()
        return {"result": "Brak studenta", "time_of_check": None}
    user_id = user[0]

    # Pobierz studenta
    c.execute("SELECT id, imie, nazwisko FROM Student WHERE user_id=?", (user_id,))
    student = c.fetchone()
    if not student:
        conn.close()
        return {"result": "Brak studenta", "time_of_check": None}
    student_id, imie, nazwisko = student

    # Pobierz kurs
    c.execute("SELECT nazwa FROM WszystkieKursy WHERE id=?", (kurs_id,))
    kurs = c.fetchone()
    if not kurs:
        conn.close()
        return {"result": "Brak kursu", "time_of_check": None}
    nazwa_kursu = kurs[0]

    # Pobierz zadanie po ID
    c.execute(
        "SELECT nazwa, termin_realizacji FROM KursNazwa WHERE id=? AND kurs_id=?",
        (zadanie_id, kurs_id)
    )
    zad = c.fetchone()
    if not zad:
        conn.close()
        return {"result": "Brak zadania", "time_of_check": None}
    nazwa_zadania, termin = zad


    # Szukaj pliku i jego timestamp
    pattern = os.path.join(
        BASE_DIR, "etc", "sn", "Kursy",
        nazwa_kursu, "Zadania", nazwa_zadania,
        student_login, f"{imie}_{nazwisko}.*"
    )
    matches = glob.glob(pattern)
    if not matches:
        conn.close()
        return {"result": "Brak pliku", "time_of_upload": None}

    filepath = matches[0]
    mtime = os.path.getmtime(filepath)
    ts = datetime.fromtimestamp(mtime).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

       # Sprawdź termin
    if datetime.now() > datetime.strptime(termin, "%Y-%m-%dT%H:%M:%S.%fZ"):
        conn.close()
        return {"result": "Termin przekroczony", "time_of_check": ts}

    conn.close()
    return {"result": "OK", "time_of_upload": ts}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sprawdzanie obecności pliku studenta")
    parser.add_argument('--student_login', required=True, help="Login studenta")
    parser.add_argument('--kurs_id', required=True, type=int, help="ID kursu")
    parser.add_argument('--zadanie_id', required=True, type=int, help="ID zadania")
    args = parser.parse_args()

    out = sprawdz_plik(args.student_login, args.kurs_id, args.zadanie_id)
    print(json.dumps(out, ensure_ascii=False))

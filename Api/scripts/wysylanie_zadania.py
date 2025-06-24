import sqlite3
import shutil
import os
import argparse
from datetime import datetime
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "baza.db")

def wyslij_zadanie(sciezka_pliku, student_login, kurs_id, zadanie_id):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Pobierz user_id
    c.execute("SELECT id FROM users WHERE email=?", (student_login,))
    user = c.fetchone()
    if not user:
        conn.close()
        return None, "Brak studenta"
    user_id = user[0]

    # Pobierz dane studenta
    c.execute("SELECT id, imie, nazwisko FROM Student WHERE user_id=?", (user_id,))
    student = c.fetchone()
    if not student:
        conn.close()
        return None, "Brak studenta"
    student_id, imie, nazwisko = student

    # Sprawdź kurs
    c.execute("SELECT nazwa FROM WszystkieKursy WHERE id=?", (kurs_id,))
    kurs = c.fetchone()
    if not kurs:
        conn.close()
        return None, "Brak kursu"
    nazwa_kursu = kurs[0]

    # Sprawdź zadanie po ID
    c.execute("SELECT 1 FROM KursNazwa WHERE id=? AND kurs_id=?", (zadanie_id, kurs_id))
    if not c.fetchone():
        conn.close()
        return None, "Brak zadania"
    
    c.execute("SELECT nazwa FROM KursNazwa WHERE id=? AND kurs_id=?", (zadanie_id, kurs_id))
    nazwa_zadania = c.fetchone()[0]

    # Sprawdź przynależność studenta do kursu
    c.execute(
        "SELECT 1 FROM uczniowie_kursy WHERE uczen_id=? AND kurs_id=?",
        (student_id, kurs_id)
    )
    if not c.fetchone():
        conn.close()
        return None, "Student nie jest przypisany do kursu"

    # Kopiuj plik i zweryfikuj timestamp
    sciezka_docelowa = os.path.join(
        BASE_DIR, "etc", "sn", "Kursy",
        nazwa_kursu, "Zadania",
        nazwa_zadania, student_login
    )
    os.makedirs(sciezka_docelowa, exist_ok=True)
    ext = os.path.splitext(sciezka_pliku)[1]
    nowa_nazwa = f"{imie}_{nazwisko}{ext}"
    dst = os.path.join(sciezka_docelowa, nowa_nazwa)
    shutil.copy(sciezka_pliku, dst)

    mtime = os.path.getmtime(dst)
    ts = datetime.fromtimestamp(mtime).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    conn.close()
    return dst, ts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wysyłanie zadania przez studenta")
    parser.add_argument('--sciezka_pliku', required=True, help="Ścieżka do pliku do wysłania")
    parser.add_argument('--student_login', required=True, help="Login studenta")
    parser.add_argument('--kurs_id', required=True, type=int, help="ID kursu")
    parser.add_argument('--zadanie_id', required=True, type=int, help="ID zadania")
    args = parser.parse_args()

    dst, result = wyslij_zadanie(
        args.sciezka_pliku,
        args.student_login,
        args.kurs_id,
        args.zadanie_id
    )

    output = {
        "result": result if dst is None else "OK",
        "time_of_upload": None if dst is None else result
    }
    print(json.dumps(output, ensure_ascii=False))
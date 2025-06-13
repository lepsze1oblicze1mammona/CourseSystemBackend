import sqlite3
from datetime import datetime
import glob
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def sprawdz_plik(student_login, kurs_id, nazwa_zadania):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Najpierw pobierz id użytkownika po emailu
    c.execute("SELECT id FROM users WHERE email=?", (student_login,))
    user = c.fetchone()
    if not user:
        print(f"Użytkownik o emailu '{student_login}' nie istnieje!")
        conn.close()
        return "Brak studenta"
    user_id = user[0]

    # Następnie pobierz id, imię i nazwisko studenta po user_id
    c.execute("SELECT id, imie, nazwisko FROM Student WHERE user_id=?", (user_id,))
    student = c.fetchone()
    if not student:
        print(f"Student powiązany z użytkownikiem '{student_login}' nie istnieje!")
        conn.close()
        return "Brak studenta"
    student_id, imie, nazwisko = student

    # Pobierz nazwę kursu po id
    c.execute("SELECT nazwa FROM WszystkieKursy WHERE id=?", (kurs_id,))
    kurs = c.fetchone()
    if not kurs:
        print(f"Kurs o id '{kurs_id}' nie istnieje!")
        conn.close()
        return "Brak kursu"
    nazwa_kursu = kurs[0]

    # Pobierz id zadania po nazwie i kursie
    c.execute("SELECT id, termin_realizacji FROM KursNazwa WHERE nazwa=? AND kurs_id=?", (nazwa_zadania, kurs_id))
    zadanie = c.fetchone()
    if not zadanie:
        print(f"Zadanie '{nazwa_zadania}' nie istnieje w kursie o id '{kurs_id}'!")
        conn.close()
        return "Brak zadania"
    zadanie_id, termin = zadanie

    # Sprawdź, czy termin minął
    if datetime.now() > datetime.strptime(termin, "%Y-%m-%d"):
        conn.close()
        return "Termin przekroczony"

    login = student_login  # email jest loginem

    # Sprawdź obecność pliku w folderze użytkownika
    sciezka = os.path.join(
        BASE_DIR, "etc", "sn", "Kursy", nazwa_kursu, "Zadania", nazwa_zadania, login, f"{imie}_{nazwisko}.*"
    )
    if glob.glob(sciezka):
        wynik = "OK"
    else:
        wynik = "Brak pliku"

    conn.close()
    return wynik

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sprawdzanie obecności pliku studenta")
    parser.add_argument('--student_login', required=True, help="Login studenta")
    parser.add_argument('--kurs_id', required=True, type=int, help="ID kursu")
    parser.add_argument('--nazwa_zadania', required=True, help="Nazwa zadania")

    args = parser.parse_args()

    wynik = sprawdz_plik(args.student_login, args.kurs_id, args.nazwa_zadania)
    print(f"Wynik sprawdzenia: {wynik}")
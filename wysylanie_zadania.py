import sqlite3
import shutil
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def wyslij_zadanie(sciezka_pliku, student_login, kurs_id, nazwa_zadania):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Najpierw pobierz id użytkownika po emailu
    c.execute("SELECT id FROM users WHERE email=?", (student_login,))
    user = c.fetchone()
    if not user:
        print(f"Użytkownik o emailu '{student_login}' nie istnieje!")
        conn.close()
        return
    user_id = user[0]

    # Następnie pobierz id, imię i nazwisko studenta po user_id
    c.execute("SELECT id, imie, nazwisko FROM Student WHERE user_id=?", (user_id,))
    student = c.fetchone()
    if not student:
        print(f"Student powiązany z użytkownikiem '{student_login}' nie istnieje!")
        conn.close()
        return
    student_id, imie, nazwisko = student

    # Sprawdź czy kurs istnieje
    c.execute("SELECT nazwa FROM WszystkieKursy WHERE id=?", (kurs_id,))
    kurs = c.fetchone()
    if not kurs:
        print(f"Kurs o id '{kurs_id}' nie istnieje!")
        conn.close()
        return
    nazwa_kursu = kurs[0]

    # Pobierz id zadania po nazwie i kursie
    c.execute("SELECT id FROM KursNazwa WHERE nazwa=? AND kurs_id=?", (nazwa_zadania, kurs_id))
    zadanie = c.fetchone()
    if not zadanie:
        print(f"Zadanie '{nazwa_zadania}' nie istnieje w kursie o id '{kurs_id}'!")
        conn.close()
        return
    zadanie_id = zadanie[0]

    # Sprawdź, czy student należy do kursu
    c.execute("SELECT 1 FROM uczniowie_kursy WHERE uczen_id=? AND kurs_id=?", (student_id, kurs_id))
    if not c.fetchone():
        print("Student nie jest przypisany do kursu!")
        conn.close()
        return

    # Pobierz login użytkownika (email)
    login = student_login  # email jest loginem

    # Utwórz folder użytkownika w folderze zadania
    sciezka_docelowa = os.path.join(
        BASE_DIR, "etc", "sn", "Kursy", nazwa_kursu, "Zadania", nazwa_zadania, login
    )
    os.makedirs(sciezka_docelowa, exist_ok=True)

    # Skopiuj plik do folderu użytkownika
    rozszerzenie = os.path.splitext(sciezka_pliku)[1]
    nowa_nazwa = f"{imie}_{nazwisko}{rozszerzenie}"
    sciezka_docelowa_pliku = os.path.join(sciezka_docelowa, nowa_nazwa)
    shutil.copy(sciezka_pliku, sciezka_docelowa_pliku)

    print(f"Plik został wysłany do: {sciezka_docelowa_pliku}")
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wysyłanie zadania przez studenta")
    parser.add_argument('--sciezka_pliku', required=True, help="Ścieżka do pliku do wysłania")
    parser.add_argument('--student_login', required=True, help="Login studenta")
    parser.add_argument('--kurs_id', required=True, type=int, help="ID kursu")
    parser.add_argument('--nazwa_zadania', required=True, help="Nazwa zadania")

    args = parser.parse_args()

    wyslij_zadanie(args.sciezka_pliku, args.student_login, args.kurs_id, args.nazwa_zadania)
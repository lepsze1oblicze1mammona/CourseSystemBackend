import sqlite3
import argparse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "baza.db")

def przypisz_uzytkownika(student_login, nazwa_kursu):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Pobierz id użytkownika po emailu
    c.execute("SELECT id FROM users WHERE email=?", (student_login,))
    user = c.fetchone()
    if not user:
        print(f"Użytkownik o emailu '{student_login}' nie istnieje!")
        conn.close()
        return
    user_id = user[0]

    # Pobierz id studenta po user_id
    c.execute("SELECT id FROM Student WHERE user_id=?", (user_id,))
    student = c.fetchone()
    if not student:
        print(f"Student powiązany z użytkownikiem '{student_login}' nie istnieje!")
        conn.close()
        return
    student_id = student[0]

    # Pobierz id kursu po nazwie
    c.execute("SELECT id FROM WszystkieKursy WHERE nazwa=?", (nazwa_kursu,))
    kurs = c.fetchone()
    if not kurs:
        print(f"Kurs '{nazwa_kursu}' nie istnieje!")
        conn.close()
        return
    kurs_id = kurs[0]

    # Sprawdź, czy już przypisany
    c.execute("SELECT 1 FROM uczniowie_kursy WHERE uczen_id=? AND kurs_id=?", (student_id, kurs_id))
    if c.fetchone():
        print(f"Student '{student_login}' już jest przypisany do kursu '{nazwa_kursu}'.")
        conn.close()
        return

    # Przypisz studenta do kursu
    c.execute("INSERT INTO uczniowie_kursy (uczen_id, kurs_id) VALUES (?, ?)", (student_id, kurs_id))
    conn.commit()
    conn.close()
    print(f"Student '{student_login}' został przypisany do kursu '{nazwa_kursu}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Przypisz użytkownika do kursu")
    parser.add_argument('--student_login', required=True, help="Login studenta")
    parser.add_argument('--nazwa_kursu', required=True, help="Nazwa kursu")
    args = parser.parse_args()
    przypisz_uzytkownika(args.student_login, args.nazwa_kursu)
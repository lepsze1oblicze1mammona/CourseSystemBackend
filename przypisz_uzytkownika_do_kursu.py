import sqlite3
import argparse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def przypisz_uzytkownika(student_login, kurs_id):
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

    # Sprawdź czy kurs istnieje
    c.execute("SELECT id FROM WszystkieKursy WHERE id=?", (kurs_id,))
    kurs = c.fetchone()
    if not kurs:
        print(f"Kurs o id '{kurs_id}' nie istnieje!")
        conn.close()
        return

    # Sprawdź, czy już przypisany
    c.execute("SELECT 1 FROM uczniowie_kursy WHERE uczen_id=? AND kurs_id=?", (student_id, kurs_id))
    if c.fetchone():
        print(f"Student '{student_login}' już jest przypisany do kursu o id '{kurs_id}'.")
        conn.close()
        return

    # Przypisz studenta do kursu
    c.execute("INSERT INTO uczniowie_kursy (uczen_id, kurs_id) VALUES (?, ?)", (student_id, kurs_id))
    conn.commit()
    conn.close()
    print(f"Student '{student_login}' został przypisany do kursu o id '{kurs_id}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Przypisz użytkownika do kursu")
    parser.add_argument('--student_login', required=True, help="Login studenta")
    parser.add_argument('--kurs_id', required=True, type=int, help="ID kursu")
    args = parser.parse_args()
    przypisz_uzytkownika(args.student_login, args.kurs_id)
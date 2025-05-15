import sqlite3
import argparse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def usun_uzytkownika(student_login, nazwa_kursu):
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

    # Następnie pobierz id studenta po user_id
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

    # Usuń przypisanie
    c.execute("DELETE FROM uczniowie_kursy WHERE uczen_id=? AND kurs_id=?", (student_id, kurs_id))
    if c.rowcount == 0:
        print(f"Student '{student_login}' nie był przypisany do kursu '{nazwa_kursu}'.")
    else:
        print(f"Student '{student_login}' został usunięty z kursu '{nazwa_kursu}'.")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usuń użytkownika z kursu")
    parser.add_argument('--student_login', required=True, help="Login studenta")
    parser.add_argument('--nazwa_kursu', required=True, help="Nazwa kursu")
    args = parser.parse_args()
    usun_uzytkownika(args.student_login, args.nazwa_kursu)
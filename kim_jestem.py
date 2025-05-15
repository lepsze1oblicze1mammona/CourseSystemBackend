import sqlite3
import argparse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def kim_jestem(login):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Najpierw pobierz id użytkownika po emailu
    c.execute("SELECT id FROM users WHERE email=?", (login,))
    user = c.fetchone()
    if not user:
        print(f"Użytkownik '{login}' nie został znaleziony.")
        conn.close()
        return "nieznany"
    user_id = user[0]

    # Sprawdź w tabeli Student po user_id
    c.execute("SELECT id FROM Student WHERE user_id=?", (user_id,))
    if c.fetchone():
        print(f"Użytkownik '{login}' jest uczniem.")
        conn.close()
        return "uczen"

    # Sprawdź w tabeli users po roli
    c.execute("SELECT role FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    if row:
        role = row[0]
        if role == "teacher":
            print(f"Użytkownik '{login}' jest nauczycielem.")
            conn.close()
            return "nauczyciel"
        else:
            print(f"Użytkownik '{login}' ma rolę: {role}.")
            conn.close()
            return role

    print(f"Użytkownik '{login}' nie został znaleziony.")
    conn.close()
    return "nieznany"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sprawdź kim jest użytkownik po loginie")
    parser.add_argument('--login', required=True, help="Login użytkownika")
    args = parser.parse_args()
    kim_jestem(args.login)
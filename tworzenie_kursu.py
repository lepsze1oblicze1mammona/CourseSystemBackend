import sqlite3
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def stworz_kurs(nazwa, wlasciciel_login):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Sprawdź unikalność nazwy kursu
    c.execute("SELECT id FROM WszystkieKursy WHERE nazwa=?", (nazwa,))
    if c.fetchone():
        print("Kurs o tej nazwie już istnieje!")
        conn.close()
        return

    # Pobierz id nauczyciela po emailu (loginie)
    c.execute("""
        SELECT Nauczyciele.id
        FROM Nauczyciele
        JOIN users ON Nauczyciele.user_id = users.id
        WHERE users.email = ?
    """, (wlasciciel_login,))
    row = c.fetchone()
    if not row:
        print(f"Nauczyciel o loginie '{wlasciciel_login}' nie istnieje!")
        conn.close()
        return
    wlasciciel_id = row[0]

    # Dodaj kurs do bazy
    c.execute("INSERT INTO WszystkieKursy (nazwa, wlasciciel) VALUES (?, ?)", (nazwa, wlasciciel_id))
    kurs_id = c.lastrowid  # Pobierz id nowo utworzonego kursu
    
    # Utwórz folder kursu
    sciezka = os.path.join(BASE_DIR, "etc", "sn", "Kursy", nazwa)
    os.makedirs(sciezka, exist_ok=True)
    
    conn.commit()
    conn.close()
    print(f"Kurs '{nazwa}' został utworzony. ID kursu: {kurs_id}, Właściciel: {wlasciciel_login}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tworzenie nowego kursu")
    parser.add_argument('--nazwa_kursu', required=True, help="Nazwa kursu")
    parser.add_argument('--wlasciciel_login', required=True, help="Login właściciela kursu")
    
    args = parser.parse_args()
    
    stworz_kurs(args.nazwa_kursu, args.wlasciciel_login)


import sqlite3
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def id_to_name_maps():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT id, nazwa FROM WszystkieKursy")
    kursy = {row[0]: row[1] for row in c.fetchall()}
    # Pobierz login nauczyciela z tabeli Nauczyciele + users
    c.execute("SELECT Nauczyciele.id, users.email FROM Nauczyciele JOIN users ON Nauczyciele.user_id = users.id")
    nauczyciele = {row[0]: row[1] for row in c.fetchall()}
    c.execute("SELECT Student.id, users.email FROM Student JOIN users ON Student.user_id = users.id")
    studenci = {row[0]: row[1] for row in c.fetchall()}
    c.execute("SELECT id, email FROM users")
    uzytkownicy = {row[0]: row[1] for row in c.fetchall()}
    conn.close()
    return kursy, studenci, uzytkownicy, nauczyciele

def fetch_table_as_json(table_name, kursy, studenci, uzytkownicy, nauczyciele):
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()
    result = []
    for row in rows:
        row_dict = dict(row)
        if table_name == "uczniowie_kursy":
            if "uczen_id" in row_dict:
                row_dict["student_login"] = studenci.get(row_dict["uczen_id"], row_dict["uczen_id"])
            # Zamiast nazwy kursu, wyświetl id kursu
            if "kurs_id" in row_dict:
                row_dict["kurs_id"] = row_dict["kurs_id"]
        if table_name == "WszystkieKursy":
            if "wlasciciel" in row_dict:
                # Pobierz email nauczyciela po id z tabeli Nauczyciele
                row_dict["wlasciciel_login"] = nauczyciele.get(row_dict["wlasciciel"], row_dict["wlasciciel"])
        if table_name == "KursNazwa":
            if "kurs_id" in row_dict:
                row_dict["kurs_id"] = row_dict["kurs_id"]
        result.append(row_dict)
    conn.close()
    return result

def get_all_tables():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in c.fetchall()]
    conn.close()
    return tables

if __name__ == "__main__":
    kursy, studenci, uzytkownicy, nauczyciele = id_to_name_maps()
    tables = get_all_tables()
    for table in tables:
        print(f"\nTabela: {table}")
        data = fetch_table_as_json(table, kursy, studenci, uzytkownicy, nauczyciele)
        print(json.dumps(data, indent=2, ensure_ascii=False))
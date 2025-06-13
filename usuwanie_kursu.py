import sqlite3
import shutil
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def usun_kurs(kurs_id):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Sprawdź, czy kurs istnieje i pobierz jego nazwę
    c.execute("SELECT nazwa FROM WszystkieKursy WHERE id=?", (kurs_id,))
    row = c.fetchone()
    if not row:
        print(f"Kurs o id '{kurs_id}' nie istnieje!")
        conn.close()
        return
    nazwa_kursu = row[0]

    # Usuń kurs z bazy
    c.execute("DELETE FROM WszystkieKursy WHERE id=?", (kurs_id,))
    
    # Usuń folder kursu
    sciezka = os.path.join(BASE_DIR, "etc", "sn", "Kursy", nazwa_kursu)
    if os.path.exists(sciezka):
        shutil.rmtree(sciezka)
        print(f"Folder kursu '{nazwa_kursu}' został usunięty.")
    else:
        print(f"Folder kursu '{nazwa_kursu}' nie istnieje.")

    conn.commit()
    conn.close()
    print(f"Kurs o id '{kurs_id}' został usunięty z bazy danych.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usuwanie kursu")
    parser.add_argument('--kurs_id', required=True, type=int, help="ID kursu do usunięcia")
    
    args = parser.parse_args()
    
    usun_kurs(args.kurs_id)
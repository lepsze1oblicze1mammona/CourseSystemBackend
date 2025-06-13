import sqlite3
import shutil
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def usun_zadanie(kurs_id, nazwa_zadania):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Sprawdź czy kurs istnieje i pobierz jego nazwę
    c.execute("SELECT nazwa FROM WszystkieKursy WHERE id=?", (kurs_id,))
    row = c.fetchone()
    if not row:
        print(f"Kurs o id '{kurs_id}' nie istnieje!")
        conn.close()
        return
    nazwa_kursu = row[0]
    
    # Usuń zadanie z bazy
    c.execute("DELETE FROM KursNazwa WHERE nazwa=? AND kurs_id=?", (nazwa_zadania, kurs_id))
    if c.rowcount == 0:
        print(f"Zadanie '{nazwa_zadania}' nie istnieje w kursie o id '{kurs_id}'!")
        conn.close()
        return
    
    # Usuń folder zadania
    sciezka = os.path.join(BASE_DIR, "etc", "sn", "Kursy", nazwa_kursu, "Zadania", nazwa_zadania)
    if os.path.exists(sciezka):
        shutil.rmtree(sciezka)
        print(f"Folder zadania '{nazwa_zadania}' został usunięty.")
    else:
        print(f"Folder zadania '{nazwa_zadania}' nie istnieje.")
    
    conn.commit()
    conn.close()
    print(f"Zadanie '{nazwa_zadania}' zostało usunięte z kursu o id '{kurs_id}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usuwanie zadania z kursu")
    parser.add_argument('--kurs_id', required=True, type=int, help="ID kursu")
    parser.add_argument('--nazwa_zadania', required=True, help="Nazwa zadania do usunięcia")
    
    args = parser.parse_args()
    
    usun_zadanie(args.kurs_id, args.nazwa_zadania)
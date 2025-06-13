import sqlite3
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def zmien_nazwe_kursu(kurs_id, nowa_nazwa):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Sprawdź, czy kurs o nowej nazwie już istnieje
    c.execute("SELECT id FROM WszystkieKursy WHERE nazwa=?", (nowa_nazwa,))
    if c.fetchone():
        print(f"Kurs o nazwie '{nowa_nazwa}' już istnieje!")
        conn.close()
        return

    # Pobierz starą nazwę kursu po id
    c.execute("SELECT nazwa FROM WszystkieKursy WHERE id=?", (kurs_id,))
    row = c.fetchone()
    if not row:
        print(f"Nie znaleziono kursu o id '{kurs_id}'.")
        conn.close()
        return
    stara_nazwa = row[0]

    # Aktualizuj nazwę w bazie
    c.execute("UPDATE WszystkieKursy SET nazwa=? WHERE id=?", (nowa_nazwa, kurs_id))
    
    if c.rowcount == 0:
        print(f"Nie znaleziono kursu o id '{kurs_id}'.")
    else:
        print(f"Nazwa kursu została zmieniona z '{stara_nazwa}' na '{nowa_nazwa}'.")

    # Zmień nazwę folderu
    stara_sciezka = os.path.join(BASE_DIR, "etc", "sn", "Kursy", stara_nazwa)
    nowa_sciezka = os.path.join(BASE_DIR, "etc", "sn", "Kursy", nowa_nazwa)
    if os.path.exists(stara_sciezka):
        os.rename(stara_sciezka, nowa_sciezka)
        print(f"Folder kursu został zmieniony na '{nowa_sciezka}'.")
    else:
        print(f"Folder kursu '{stara_sciezka}' nie istnieje.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modyfikacja nazwy kursu")
    parser.add_argument('--kurs_id', required=True, type=int, help="ID kursu")
    parser.add_argument('--nowa_nazwa', required=True, help="Nowa nazwa kursu")
    
    args = parser.parse_args()
    
    zmien_nazwe_kursu(args.kurs_id, args.nowa_nazwa)
import sqlite3
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def zmien_nazwe_kursu(stara_nazwa, nowa_nazwa):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Sprawdź, czy kurs o nowej nazwie już istnieje
    c.execute("SELECT id FROM WszystkieKursy WHERE nazwa=?", (nowa_nazwa,))
    if c.fetchone():
        print(f"Kurs o nazwie '{nowa_nazwa}' już istnieje!")
        conn.close()
        return

    # Aktualizuj nazwę w bazie
    c.execute("UPDATE WszystkieKursy SET nazwa=? WHERE nazwa=?", (nowa_nazwa, stara_nazwa))
    
    if c.rowcount == 0:
        print(f"Nie znaleziono kursu o nazwie '{stara_nazwa}'.")
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
    parser.add_argument('--stara_nazwa', required=True, help="Obecna nazwa kursu")
    parser.add_argument('--nowa_nazwa', required=True, help="Nowa nazwa kursu")
    
    args = parser.parse_args()
    
    zmien_nazwe_kursu(args.stara_nazwa, args.nowa_nazwa)
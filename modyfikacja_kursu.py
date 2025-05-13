import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def zmien_nazwe_kursu(stara_nazwa, nowa_nazwa):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
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
    zmien_nazwe_kursu()

if __name__ == "__main__":
    stara_nazwa = input("Podaj obecną nazwę kursu: ")
    nowa_nazwa = input("Podaj nową nazwę kursu: ")
    
    # Wywołanie funkcji zmieniającej nazwę kursu
    zmien_nazwe_kursu(stara_nazwa, nowa_nazwa)
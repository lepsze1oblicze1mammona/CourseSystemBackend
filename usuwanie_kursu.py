import sqlite3
import shutil
import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def usun_kurs(nazwa):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Usuń z bazy
    c.execute("DELETE FROM WszystkieKursy WHERE nazwa=?", (nazwa,))
    
    # Usuń folder
    sciezka = f"etc/sn/Kursy/{nazwa}"
    shutil.rmtree(sciezka)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usuwanie kursu")
    parser.add_argument('--nazwa', required=True, help="Nazwa kursu do usunięcia")
    
    args = parser.parse_args()
    
    usun_kurs(args.nazwa)
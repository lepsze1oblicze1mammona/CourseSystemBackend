import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def stworz_zadanie(nazwa_kursu, nazwa_zadania, termin):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Znajdź ID kursu
    c.execute("SELECT id FROM WszystkieKursy WHERE nazwa=?", (nazwa_kursu,))
    kurs_id = c.fetchone()
    if not kurs_id:
        print("Kurs nie istnieje!")
        return
    
    # Dodaj zadanie do bazy
    c.execute("INSERT INTO KursNazwa (nazwa, termin_realizacji, kurs_id) VALUES (?, ?, ?)", 
              (nazwa_zadania, termin, kurs_id[0]))
    
    # Utwórz folder zadania
    sciezka = f"etc/sn/Kursy/{nazwa_kursu}/Zadania/{nazwa_zadania}"
    os.makedirs(sciezka, exist_ok=True)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
        nazwa_kursu = input("Podaj nazwę kursu: ")
        nazwa_zadania = input("Podaj nazwę zadania: ")
        termin = input("Podaj termin realizacji (YYYY-MM-DD): ")
    
        stworz_zadanie(nazwa_kursu, nazwa_zadania, termin)
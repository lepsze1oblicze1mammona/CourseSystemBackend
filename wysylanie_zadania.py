import sqlite3
import shutil
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")

def wyslij_zadanie(sciezka_pliku, student_id, kurs_id, zadanie_id):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Pobierz nazwę kursu i zadania
    c.execute("SELECT nazwa FROM WszystkieKursy WHERE id=?", (kurs_id,))
    kurs_nazwa = c.fetchone()[0]
    
    c.execute("SELECT nazwa FROM KursNazwa WHERE id=?", (zadanie_id,))
    zadanie_nazwa = c.fetchone()[0]

    # Sprawdź, czy student należy do kursu
    c.execute("SELECT 1 FROM uczniowie_kursy WHERE uczen_id=? AND kurs_id=?", (student_id, kurs_id))
    if not c.fetchone():
        print("Student nie jest przypisany do kursu!")
        return
    
    # Pobierz dane studenta
    c.execute("SELECT imie, nazwisko FROM Student WHERE id=?", (student_id,))
    imie, nazwisko = c.fetchone()
    
    # Utwórz nazwę pliku
    rozszerzenie = os.path.splitext(sciezka_pliku)[1]
    nowa_nazwa = f"{imie}_{nazwisko}{rozszerzenie}"
    
    # Skopiuj plik do folderu zadania
    sciezka_docelowa = f"etc/sn/Kursy/{kurs_nazwa}/Zadania/{zadanie_nazwa}/{nowa_nazwa}"
    shutil.copy(sciezka_pliku, sciezka_docelowa)
    
    conn.close()

if __name__ == "__main__":
    sciezka_pliku = input("Podaj ścieżkę do pliku: ")
    student_id = int(input("Podaj ID studenta: "))
    kurs_id = int(input("Podaj ID kursu: "))
    zadanie_id = int(input("Podaj ID zadania: "))
    
    wyslij_zadanie(sciezka_pliku, student_id, kurs_id, zadanie_id)
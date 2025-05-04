import sqlite3
import shutil
import os


def wyslij_zadanie(sciezka_pliku, student_id, kurs_id, zadanie_id):
    conn = sqlite3.connect('baza.db')
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
    sciezka_docelowa = f"/etc/sn/Kursy/{kurs_nazwa}/Zadania/{zadanie_nazwa}/{nowa_nazwa}"
    shutil.copy(sciezka_pliku, sciezka_docelowa)
    
    conn.close()
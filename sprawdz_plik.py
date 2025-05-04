import sqlite3
import datetime
import glob


def sprawdz_plik(student_id, zadanie_id):
    conn = sqlite3.connect('baza.db')
    c = conn.cursor()

    # Pobierz nazwę kursu i zadania
    c.execute("SELECT kurs_id FROM KursNazwa WHERE id=?", (zadanie_id,))
    kurs_id = c.fetchone()[0]
    
    c.execute("SELECT nazwa FROM WszystkieKursy WHERE id=?", (kurs_id,))
    kurs_nazwa = c.fetchone()[0]
    
    c.execute("SELECT nazwa FROM KursNazwa WHERE id=?", (zadanie_id,))
    zadanie_nazwa = c.fetchone()[0]
    
    # Pobierz dane studenta i zadania
    c.execute("SELECT imie, nazwisko FROM Student WHERE id=?", (student_id,))
    imie, nazwisko = c.fetchone()
    c.execute("SELECT termin_realizacji FROM KursNazwa WHERE id=?", (zadanie_id,))
    termin = c.fetchone()[0]
    
    # Sprawdź, czy termin minął
    if datetime.now() > termin:
        return "Termin przekroczony"
    
    # Sprawdź obecność pliku
    sciezka = f"/etc/sn/Kursy/{kurs_nazwa}/Zadania/{zadanie_nazwa}/{imie}_{nazwisko}.*"
    if glob.glob(sciezka):
        return "OK"
    else:
        return "Brak pliku"
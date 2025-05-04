import sqlite3

def zmien_termin_zadania(nazwa_kursu, nazwa_zadania, nowy_termin):
    conn = sqlite3.connect('baza.db')
    c = conn.cursor()
    
    c.execute("UPDATE KursNazwa SET termin_realizacji=? WHERE nazwa=? AND kurs_id=(SELECT id FROM WszystkieKursy WHERE nazwa=?)", (nowy_termin, nazwa_zadania, nazwa_kursu))
    
    conn.commit()
    conn.close()
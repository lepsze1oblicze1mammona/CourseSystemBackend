import sqlite3
import bcrypt
import argparse
import os
# import jwt
# import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "etc", "sn", "baza.db")
#SECRET_KEY = "tajny_klucz"

def get_db_connection():
    conn = sqlite3.connect(db_file)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabela użytkownicy
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('student', 'teacher'))
        )
    ''')
    
    # Tabela studenci
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            imie TEXT NOT NULL,
            nazwisko TEXT NOT NULL,
            klasa TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Tabela nauczyciele
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Nauczyciele (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            imie TEXT NOT NULL,
            nazwisko TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Tabela WszystkieKursy
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS WszystkieKursy (
            id INTEGER PRIMARY KEY,
            nazwa TEXT UNIQUE NOT NULL,
            wlasciciel INTEGER NOT NULL,
            FOREIGN KEY (wlasciciel) REFERENCES Nauczyciele(id)
        )
    ''')

    # Tabela KursNazwa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS KursNazwa (
            id INTEGER PRIMARY KEY,
            nazwa TEXT NOT NULL,
            opis TEXT,
            termin_realizacji DATE,
            kurs_id INTEGER NOT NULL,
            FOREIGN KEY (kurs_id) REFERENCES WszystkieKursy(id)
        )
    ''')

    # Tabela Dołączenia
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dolaczenia (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            kurs_id INTEGER NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('pending', 'accepted', 'rejected')),
            FOREIGN KEY (student_id) REFERENCES Student(id),
            FOREIGN KEY (kurs_id) REFERENCES WszystkieKursy(id)
        )
    ''')

     # Tabela uczniowie_kursy
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uczniowie_kursy (
            uczen_id INTEGER,
            kurs_id INTEGER,
            PRIMARY KEY (uczen_id, kurs_id),
            FOREIGN KEY (uczen_id) REFERENCES Student(id),
            FOREIGN KEY (kurs_id) REFERENCES WszystkieKursy(id)
        )
    ''')

    
    conn.commit()
    conn.close()

# Rejestracja
def register(email, password, role, imie, nazwisko, klasa=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Sprawdź czy email istnieje
        cursor.execute("SELECT id FROM users WHERE email=?", (email,))
        if cursor.fetchone():
            print("Email już istnieje!")
            return

        # Hashuj hasło
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Dodaj użytkownika
        cursor.execute(
            "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
            (email, hashed.decode('utf-8'), role)
        )
        user_id = cursor.lastrowid
        
        # Dodaj do odpowiedniej tabeli (Student/Nauczyciele)
        if role == 'student':
            cursor.execute(
                "INSERT INTO Student (user_id, imie, nazwisko, klasa) VALUES (?, ?, ?, ?)",
                (user_id, imie, nazwisko, klasa)
            )
        else:
            cursor.execute(
                "INSERT INTO Nauczyciele (user_id, imie, nazwisko) VALUES (?, ?, ?)",
                (user_id, imie, nazwisko)
            )
        
        conn.commit()
        print("Rejestracja udana!")
        
    except Exception as e:
        print(f"Błąd: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

# Logowanie
def login(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, password_hash, role FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        
        if not user:
            print("Nieprawidłowy email!")
            return
        
        user_id, hashed, role = user
        if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
            # Generowanie tokena JWT
            # payload = {
            #     "user_id": user_id,
            #     "role": role,
            #     "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=2)
            # }
            # token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            # if isinstance(token, bytes):
            #     token = token.decode()
            # print(f"{role} {user_id} {token}")
            print(f'{role} {user_id}')
        else:
            print("Nieprawidłowe hasło!")
            
    except Exception as e:
        print(f"Błąd: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_tables() 
    
    parser = argparse.ArgumentParser(description="System rejestracji i logowania")
    subparsers = parser.add_subparsers(dest='command')
    
    # Rejestracja
    parser_register = subparsers.add_parser('register')
    parser_register.add_argument('--email', required=True)
    parser_register.add_argument('--password', required=True)
    parser_register.add_argument('--role', choices=['student', 'teacher'], required=True)
    parser_register.add_argument('--imie', required=True)
    parser_register.add_argument('--nazwisko', required=True)
    parser_register.add_argument('--klasa')
    
    # Logowanie
    parser_login = subparsers.add_parser('login')
    parser_login.add_argument('--email', required=True)
    parser_login.add_argument('--password', required=True)
    
    args = parser.parse_args()
    
    if args.command == 'register':
        if args.role == 'student' and not args.klasa:
            print("Dla studenta wymagany jest parametr --klasa")
        else:
            register(args.email, args.password, args.role, args.imie, args.nazwisko, args.klasa)
    elif args.command == 'login':
        login(args.email, args.password)
    else:
        parser.print_help()
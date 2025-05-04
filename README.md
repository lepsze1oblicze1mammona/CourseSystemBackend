# CourseSystemBackend
System kursów dla nauczycieli i studentów

PLIKI
/etc/sn/Kursy/Zadania/

SKRYPTY
scripts/  
  │   └── database.py     # Połączenie z bazą, na razie kazdy skrypt osobno łączy się z bazą
  ├── tworzenie_kursu.py  
  ├── tworzenie_zadania.py  
  ├── modyfikacja_kursu.py  
  ├── modyfikacja_zadania.py  
  ├── usuwanie_kursu.py  
  ├── usuwania_zadania.py  
  ├── wysylanie_zadania.py     
  └── sprawdz_plik.py

  INSTRUKCJA SKRYPT 
  1) Tworzenie kurs: 
    python3 tworzenie_kursu.py --nazwa "Programowanie" --wlasciciel_id 1
      [--nazwa: Unikalna nazwa kursu]
      [--wlasciciel_id: ID nauczyciela z tabeli nauczyciel]
  3) Tworzenie zadania:
     python3 tworzenie_zadania.py --kurs "Programowanie" --zadanie "Lab1" --termin "2023-12-31"
      [--kurs: Nazwa istniejącego kursu]
      [--termin: Data w formacie YYYY-MM-DD]
  4) Wysyłanie zadania:
     python3 wyslij_zadanie.py --student_id 5 --kurs_id 1 --zadanie_id 3 --plik rozwiazanie.pdf
      [--student_id: ID studenta z tabeli Student]
      [--plik: Ścieżka do pliku z rozwiązaniem]
  5) Sprawdz plik:
     python3 sprawdz_plik.py --student_id 5 --zadanie_id 3
      [OK – plik istnieje i termin nie minął]
      [Brak pliku – plik nie został przesłany]
      [Termin przekroczony – zadanie nie zostało dostarczone na czas]
  7) Usun kurs:
     python3 usuwanie_kursu.py --kurs_id 1

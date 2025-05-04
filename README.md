# CourseSystemBackend
System kursów dla nauczycieli i studentów

PLIKI
/etc/sn/
  ├── Kursy/                  # Główny folder kursów
  │   ├── [NazwaKursu]/       # Folder kursu (tworzony przez skrypt 1)
  │   │   ├── Zadania/        # Folder z zadaniami (tworzony przez skrypt 2)
  │   │   │   ├── Zadanie1/   # Podfolder dla konkretnego zadania
  │   │   │   └── ...  
  │   │   └── ...  
  └── ...  
SKRYPTY
scripts/  
  ├── utils/              # Wspólne funkcje pomocnicze
  │   ├── __init__.py  
  │   └── database.py     # Połączenie z bazą, zapytania SQL  
  ├── create_course.py  
  ├── create_task.py  
  ├── modify_course.py  
  ├── modify_task.py  
  ├── delete_course.py  
  ├── delete_task.py  
  ├── submit_task.py      # Wysyłanie zadania przez studenta  
  └── check_task.py       # Sprawdzanie obecności pliku 

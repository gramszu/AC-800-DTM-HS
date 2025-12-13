# Instrukcja Obsługi Aplikacji AC800-DTM-HS

## Spis Treści
1. [Wprowadzenie](#wprowadzenie)
2. [Uruchomienie Aplikacji](#uruchomienie-aplikacji)
3. [Interfejs Użytkownika](#interfejs-użytkownika)
4. [Opis Przycisków i Funkcji](#opis-przycisków-i-funkcji)
5. [Konfiguracja Sterownika](#konfiguracja-sterownika)
6. [Zarządzanie Numerami Telefonów](#zarządzanie-numerami-telefonów)
7. [Rozwiązywanie Problemów](#rozwiązywanie-problemów)

---

## Wprowadzenie

Aplikacja **AC800-DTM-HS** służy do konfiguracji sterownika bramy obsługującego do **800 numerów telefonów**. Sterownik wykorzystuje mikrokontroler ATmega1284P i komunikuje się przez port szeregowy (COM).

### Wymagania systemowe:
- System operacyjny: Windows/macOS/Linux
- Port COM (USB-UART) do połączenia ze sterownikiem
- Zainstalowane narzędzie `avrdude` (dołączone w folderze `tools/`)

---

## Uruchomienie Aplikacji

1. **Podłącz sterownik** do komputera przez port USB (konwerter USB-UART)
2. **Uruchom aplikację** `AC800-DTM-HS.py` lub skompilowaną wersję `.exe`
3. **Wybierz właściwy port COM** z listy rozwijanej w sekcji "Port COM"
4. Kliknij **"Odczytaj dane ze sterownika"** aby rozpocząć pracę

---

## Zalecane Procedury Bezpieczeństwa

> **⚠️ WAŻNE: Zawsze pracuj na kopii danych!**

Przed wprowadzeniem jakichkolwiek zmian w konfiguracji sterownika **zdecydowanie zaleca się** wykonanie następującej procedury:

### Bezpieczny Przepływ Pracy:

1. **Odczytaj dane ze sterownika** 
   - Kliknij przycisk "Odczytaj dane ze sterownika"
   - Poczekaj na zakończenie operacji (27 sekund)

2. **Zapisz kopię zapasową do CSV**
   - Kliknij przycisk "Zapisz dane do CSV"
   - Wybierz lokalizację i nazwę pliku (np. `kopia_zapasowa_2025-12-13.csv`)
   - Zapisz plik w bezpiecznym miejscu

3. **Wprowadź zmiany**
   - Dodaj/usuń numery
   - Zmień ustawienia (status, tryb, harmonogram)
   - Zmień kod dostępu

4. **Zapisz zmodyfikowaną listę do CSV**
   - Kliknij ponownie "Zapisz dane do CSV"
   - Zapisz jako nowy plik (np. `nowa_konfiguracja_2025-12-13.csv`)

5. **Wczytaj i zweryfikuj**
   - Kliknij "Odczytaj dane z CSV"
   - Wybierz plik z nową konfiguracją
   - Sprawdź czy wszystko jest poprawne

6. **Wgraj do sterownika**
   - Dopiero teraz kliknij "Wgraj dane do sterownika"
   - Poczekaj na zakończenie operacji (27 sekund)

### Dlaczego ta procedura jest ważna?

✅ **Bezpieczeństwo danych** - masz kopię zapasową na wypadek błędu  
✅ **Możliwość cofnięcia zmian** - możesz wrócić do poprzedniej konfiguracji  
✅ **Weryfikacja przed zapisem** - możesz sprawdzić zmiany przed wgraniem do sterownika  
✅ **Historia zmian** - pliki CSV z datami tworzą historię konfiguracji  

### W razie problemów:

Jeśli coś pójdzie nie tak, możesz zawsze:
1. Kliknij "Odczytaj dane z CSV"
2. Wybierz plik z kopią zapasową
3. Kliknij "Wgraj dane do sterownika"

---

## Interfejs Użytkownika

Aplikacja składa się z następujących sekcji:

### 1. **Pasek Postępu**
- Pokazuje postęp operacji odczytu/zapisu (0-27 sekund)
- Status: "Gotowe" gdy operacja zakończona

### 2. **Port COM**
- Lista rozwijana z dostępnymi portami szeregowymi
- Domyślnie: COM3 (Windows) lub odpowiednik na macOS/Linux
- **Wybierz właściwy port** przed rozpoczęciem pracy

### 3. **Status Sterownika**
Dwa przyciski radiowe:
- ⚪ **Aktywny** - sterownik działa normalnie
- ⚪ **Blokada** - sterownik zablokowany (nie reaguje na połączenia)

### 4. **Tryb Pracy**
Dwa przyciski radiowe:
- ⚪ **Prywatny** - tylko numery z listy mogą otwierać bramę
- ⚪ **Publiczny** - każdy numer może otwierać bramę

### 5. **Tryb Sterowania** (tylko w wersji DTM-HS)
Dwa przyciski radiowe:
- ⚪ **CLIP** - sterowanie przez rozpoznawanie numeru dzwoniącego
- ⚪ **DTMF** - sterowanie przez tony DTMF (kody dostępu)

### 6. **Funkcja Skryba**
Dwa przyciski radiowe:
- ⚪ **Włączona** - zapisuje informacje o połączeniach
- ⚪ **Wyłączona** - nie zapisuje historii

**Limit Skryba:** Pole numeryczne (1-795) - określa ile pozycji na liście jest dostępnych dla zwykłych użytkowników. Pozycje 796-800 są zarezerwowane dla Super Userów.

> **UWAGA:** Włączenie funkcji Skryba automatycznie przełącza tryb pracy na **Publiczny**.

### 7. **Harmonogram (Time Control)**
Checkbox **"Włącz harmonogram"** + pola czasowe:
- **Czas START:** Godzina:Minuta (00-23:00-59)
- **Czas STOP:** Godzina:Minuta (00-23:00-59)

Gdy włączony, brama działa tylko w określonych godzinach.

### 8. **Zmiana Kodu Dostępu**
- Pole tekstowe na 4-cyfrowy kod
- Przycisk **"Zmień"** - zapisuje nowy kod do sterownika

### 9. **Lista Numerów Uprawnionych**
- Pole tekstowe z numerami telefonów (jeden w każdej linii)
- Obsługuje do 800 numerów
- Numery muszą mieć 3-9 cyfr

### 10. **Pole do Dodawania Numeru**
- Pole tekstowe + przycisk **"Dodaj"**
- Dodaje numer do listy

### 11. **Pole do Usuwania Numeru**
- Pole tekstowe + przycisk **"Usuń"**
- Usuwa numer z listy

---

## Opis Przycisków i Funkcji

### 🔵 **Odczytaj dane ze sterownika**
**Co robi:**
- Łączy się ze sterownikiem przez port COM
- Odczytuje całą pamięć EEPROM (4096 bajtów)
- Wyświetla wszystkie zapisane numery telefonów
- Odczytuje ustawienia: status, tryb pracy, funkcję Skryba, harmonogram
- Odczytuje kod dostępu

**Kiedy używać:**
- Na początku pracy z aplikacją
- Po podłączeniu nowego sterownika
- Gdy chcesz sprawdzić aktualną konfigurację

**Czas trwania:** ~27 sekund

**Co się dzieje:**
1. Aplikacja wysyła impuls DTR (reset sterownika)
2. Uruchamia `avrdude` z parametrami odczytu EEPROM
3. Parsuje odczytane dane
4. Wyświetla numery i ustawienia w interfejsie

---

### 🔵 **Wgraj dane do sterownika**
**Co robi:**
- Zapisuje wszystkie numery z listy do pamięci EEPROM sterownika
- Zapisuje wszystkie ustawienia (status, tryb, Skryba, harmonogram)
- Zapisuje kod dostępu
- Przelicza i zapisuje sumę kontrolną

**Kiedy używać:**
- Po dodaniu/usunięciu numerów
- Po zmianie ustawień
- Po zmianie kodu dostępu

**Czas trwania:** ~27 sekund

**Co się dzieje:**
1. Aplikacja przygotowuje dane w formacie EEPROM
2. Numery są zapisywane w formacie Little-Endian (odwrócone bajty)
3. Wysyła impuls DTR (reset)
4. Uruchamia `avrdude` z parametrami zapisu EEPROM
5. Pokazuje okno postępu "Aktualizacja firmware..."

---

### 🔵 **Aktualizacje**
**Co robi:**
- Otwiera stronę internetową producenta: https://www.sonfy.pl
- Pozwala sprawdzić dostępność nowych wersji firmware i aplikacji
- Zapewnia dostęp do najnowszych funkcji i poprawek błędów

**Kiedy używać:**
- Regularnie (zalecane raz na miesiąc)
- Gdy chcesz sprawdzić dostępność nowych funkcji
- Gdy potrzebujesz wsparcia technicznego
- Gdy napotkasz problemy z działaniem sterownika

---

### Procedura Aktualizacji Firmware

> **⚠️ UWAGA:** Przed aktualizacją firmware **ZAWSZE** wykonaj kopię zapasową!

**Krok 1: Sprawdź aktualną wersję**
- Aktualna wersja firmware: **2.0**
- Sprawdź w oknie "Info" (przycisk Info w aplikacji)

**Krok 2: Pobierz nową wersję**
1. Kliknij przycisk **"Aktualizacje"**
2. Przejdź na stronę www.sonfy.pl
3. Znajdź sekcję "Pobieranie" lub "Downloads"
4. Pobierz najnowszą wersję firmware (plik `.hex`)
5. Pobierz najnowszą wersję aplikacji (jeśli dostępna)

**Krok 3: Wykonaj kopię zapasową**
1. Kliknij **"Odczytaj dane ze sterownika"**
2. Kliknij **"Zapisz dane do CSV"**
3. Zapisz plik z datą (np. `backup_przed_aktualizacja_2025-12-13.csv`)

**Krok 4: Wgraj nowy firmware**

> **Uwaga:** Firmware można wgrać na dwa sposoby: przez plik `.hex` (tylko program) lub `.dat` (program + EEPROM).

**Metoda A: Plik .hex (tylko program, zachowuje dane)**
```bash
avrdude -C avrdude.conf -c urclock -p m1284p -b 115200 -P COM3 -U flash:w:nowy_firmware.hex:i
```
- Wgrywa tylko kod programu
- **Zachowuje** wszystkie numery i ustawienia w EEPROM
- Zalecane przy aktualizacji bez zmiany konfiguracji

**Metoda B: Plik .dat (program + EEPROM, kompletna kopia)**
```bash
avrdude -C avrdude.conf -c urclock -p m1284p -b 115200 -P COM3 -U flash:w:firmware.dat:i -U eeprom:w:firmware.dat:i
```
- Wgrywa kod programu **oraz** dane EEPROM
- **Nadpisuje** wszystkie numery i ustawienia
- Przydatne przy przywracaniu pełnej kopii zapasowej sterownika
- Plik `.dat` może zawierać prekonfigurowaną listę numerów

> **⚠️ UWAGA:** Przy użyciu pliku `.dat` wszystkie aktualne dane zostaną zastąpione danymi z pliku!

**Krok 5: Przywróć konfigurację (tylko dla metody A)**
1. Uruchom aplikację
2. Kliknij **"Odczytaj dane z CSV"**
3. Wybierz plik z kopią zapasową
4. Kliknij **"Wgraj dane do sterownika"**

**Krok 6: Weryfikacja**
1. Sprawdź czy wszystkie numery są na liście
2. Sprawdź ustawienia (status, tryb, harmonogram)
3. Przetestuj działanie bramy (wykonaj testowe połączenie)

---

### Aktualizacja Aplikacji

**Dla wersji .exe (Windows):**
1. Pobierz nową wersję z www.sonfy.pl
2. Zamknij starą aplikację
3. Usuń starą wersję (lub zmień nazwę folderu)
4. Rozpakuj nową wersję
5. Uruchom nową aplikację

**Dla wersji .py (Python):**
1. Pobierz nowy plik `AC800-DTM-HS.py`
2. Zastąp stary plik nowym
3. Sprawdź czy folder `tools/` zawiera aktualne pliki `avrdude`

**Zachowanie danych:**
- Pliki CSV z kopiami zapasowymi **nie są usuwane** podczas aktualizacji
- Zaleca się przechowywanie kopii zapasowych w osobnym folderze

---

### Historia Wersji

**Wersja 2.0** (aktualna)
- Obsługa 800 numerów telefonów
- Funkcja Skryba z limitem użytkowników
- Harmonogram czasowy (Time Control)
- Tryb CLIP/DTMF (wersja DTM-HS)
- Ulepszona walidacja numerów
- Eksport/import CSV

**Wcześniejsze wersje:**
- Sprawdź na stronie producenta: www.sonfy.pl

---

### 🔵 **Zapisz dane do CSV**
**Co robi:**
- Eksportuje listę numerów do pliku CSV
- Format: każdy numer w osobnej linii
- Otwiera okno dialogowe wyboru miejsca zapisu

**Kiedy używać:**
- Gdy chcesz zrobić kopię zapasową numerów
- Gdy chcesz edytować numery w Excelu/Calc
- Gdy chcesz przenieść numery do innego sterownika

**Format pliku CSV:**
```
123456789
987654321
555123456
```

---

### 🔵 **Odczytaj dane z CSV**
**Co robi:**
- Importuje listę numerów z pliku CSV
- Zastępuje aktualną listę numerów w aplikacji
- Waliduje numery (3-9 cyfr)

**Kiedy używać:**
- Gdy chcesz przywrócić kopię zapasową
- Gdy chcesz załadować numery przygotowane w innym programie

**UWAGA:** Ta operacja **nie zapisuje** numerów do sterownika automatycznie. Po wczytaniu CSV musisz kliknąć **"Wgraj dane do sterownika"**.

---

### 🔵 **Wyczyść wszystkie numery**
**Co robi:**
- Usuwa wszystkie numery z listy w aplikacji
- Czyści pole tekstowe z numerami

**Kiedy używać:**
- Gdy chcesz zacząć od nowa
- Przed importem nowej listy z CSV

**UWAGA:** Ta operacja **nie czyści** pamięci sterownika automatycznie. Musisz kliknąć **"Wgraj dane do sterownika"** aby zapisać pustą listę.

---

### 🔵 **Aktualizuj listę numerów**
**Co robi:**
- Synchronizuje listę numerów z pola tekstowego
- Usuwa duplikaty
- Waliduje format numerów
- Aktualizuje wyświetlanie

**Kiedy używać:**
- Po ręcznej edycji listy numerów w polu tekstowym
- Gdy chcesz sprawdzić poprawność numerów

---

### 🔵 **Info**
**Co robi:**
- Wyświetla okno z informacjami o aplikacji:
  - Nazwa: Bramster AC800-DTM-HS
  - Wersja firmware: 2.0
  - Autor: Robert Gramsz
  - Strona: www.sonfy.pl

---

### 🔵 **Zmień** (kod dostępu)
**Co robi:**
- Zapisuje nowy 4-cyfrowy kod dostępu do pamięci aplikacji
- Wyświetla komunikat potwierdzenia

**Kiedy używać:**
- Gdy chcesz zmienić kod dostępu do sterownika

**UWAGA:** Kod zostanie zapisany do sterownika dopiero po kliknięciu **"Wgraj dane do sterownika"**.

**Format kodu:** 4 cyfry (np. 1234, 0000, 9999)

---

### 🔵 **Dodaj** (numer)
**Co robi:**
- Dodaje numer z pola tekstowego do listy numerów uprawnionych
- Waliduje numer (3-9 cyfr)
- Wyświetla komunikat błędu jeśli numer nieprawidłowy

**Kiedy używać:**
- Gdy chcesz dodać pojedynczy numer do listy

**Walidacja:**
- Numer musi mieć od 3 do 9 cyfr
- Tylko cyfry (0-9)
- Przykłady poprawnych numerów: 123, 123456789, 600123456

---

### 🔵 **Usuń** (numer)
**Co robi:**
- Usuwa numer z pola tekstowego z listy numerów uprawnionych
- Wyświetla komunikat potwierdzenia

**Kiedy używać:**
- Gdy chcesz usunąć pojedynczy numer z listy

---

## Konfiguracja Sterownika

### Zmiana Statusu Sterownika

1. Kliknij **"Odczytaj dane ze sterownika"**
2. Wybierz:
   - **Aktywny** - sterownik będzie reagował na połączenia
   - **Blokada** - sterownik nie będzie reagował na połączenia
3. Kliknij **"Wgraj dane do sterownika"**

**Zastosowanie:**
- **Aktywny:** Normalna praca
- **Blokada:** Tymczasowe wyłączenie (np. podczas konserwacji)

---

### Zmiana Trybu Pracy

1. Kliknij **"Odczytaj dane ze sterownika"**
2. Wybierz:
   - **Prywatny** - tylko numery z listy mogą otwierać bramę
   - **Publiczny** - każdy numer może otwierać bramę
3. Kliknij **"Wgraj dane do sterownika"**

**Zastosowanie:**
- **Prywatny:** Budynki mieszkalne, firmy (kontrola dostępu)
- **Publiczny:** Parkingi publiczne, miejsca ogólnodostępne

---

### Zmiana Trybu Sterowania (CLIP/DTMF)

**Tylko w wersji AC800-DTM-HS (instalacja/AC800-DTM-HS.py)**

1. Kliknij **"Odczytaj dane ze sterownika"**
2. Wybierz:
   - **CLIP** - sterowanie przez rozpoznawanie numeru dzwoniącego
   - **DTMF** - sterowanie przez tony DTMF (wymagany kod dostępu)
3. Kliknij **"Wgraj dane do sterownika"**

**Różnice:**

| Funkcja | CLIP | DTMF |
|---------|------|------|
| Sposób działania | Rozpoznaje numer dzwoniącego | Wymaga wpisania kodu DTMF |
| Bezpieczeństwo | Średnie | Wysokie |
| Wygoda | Wysoka (jedno połączenie) | Średnia (trzeba wpisać kod) |
| Koszt połączenia | Brak (połączenie odrzucane) | Minimalny (krótkie połączenie) |
| Czas otwarcia | ~3 sekundy | ~5-10 sekund |

---

### Konfiguracja Funkcji Skryba

**Funkcja Skryba** zapisuje informacje o wszystkich połączeniach w pamięci sterownika.

1. Kliknij **"Odczytaj dane ze sterownika"**
2. Wybierz:
   - **Włączona** - zapisuje historię połączeń
   - **Wyłączona** - nie zapisuje historii
3. Ustaw **Limit Skryba** (1-795):
   - Określa ile pozycji jest dostępnych dla zwykłych użytkowników
   - Pozycje 796-800 są zarezerwowane dla Super Userów
4. Kliknij **"Wgraj dane do sterownika"**

**UWAGA:** Włączenie Skryby automatycznie przełącza tryb pracy na **Publiczny**.

**Zastosowanie:**
- Monitoring dostępu
- Kontrola kto i kiedy otwierał bramę
- Analiza ruchu

---

### Konfiguracja Harmonogramu (Time Control)

Harmonogram pozwala ograniczyć działanie bramy do określonych godzin.

1. Kliknij **"Odczytaj dane ze sterownika"**
2. Zaznacz **"Włącz harmonogram"**
3. Ustaw **Czas START** (godzina i minuta)
4. Ustaw **Czas STOP** (godzina i minuta)
5. Kliknij **"Wgraj dane do sterownika"**

**Przykład:**
- START: 08:00
- STOP: 18:00
- **Efekt:** Brama działa tylko od 8:00 do 18:00

**Zastosowanie:**
- Ograniczenie dostępu w godzinach nocnych
- Automatyczne wyłączenie w weekendy (wymaga dodatkowej konfiguracji)
- Oszczędność energii

---

## Zarządzanie Numerami Telefonów

### Dodawanie Numerów

**Metoda 1: Pojedynczo**
1. Wpisz numer w pole "Dodaj numer"
2. Kliknij **"Dodaj"**
3. Powtórz dla kolejnych numerów
4. Kliknij **"Wgraj dane do sterownika"**

**Metoda 2: Masowo (CSV)**
1. Przygotuj plik CSV z numerami (jeden w każdej linii)
2. Kliknij **"Odczytaj dane z CSV"**
3. Wybierz plik
4. Kliknij **"Wgraj dane do sterownika"**

**Metoda 3: Ręczna edycja**
1. Kliknij w pole "Lista numerów uprawnionych"
2. Wpisz/wklej numery (jeden w każdej linii)
3. Kliknij **"Aktualizuj listę numerów"**
4. Kliknij **"Wgraj dane do sterownika"**

---

### Usuwanie Numerów

**Metoda 1: Pojedynczo**
1. Wpisz numer w pole "Usuń numer"
2. Kliknij **"Usuń"**
3. Kliknij **"Wgraj dane do sterownika"**

**Metoda 2: Ręczna edycja**
1. Kliknij w pole "Lista numerów uprawnionych"
2. Usuń numery
3. Kliknij **"Aktualizuj listę numerów"**
4. Kliknij **"Wgraj dane do sterownika"**

**Metoda 3: Wyczyść wszystko**
1. Kliknij **"Wyczyść wszystkie numery"**
2. Kliknij **"Wgraj dane do sterownika"**

---

### Eksport/Import Numerów

**Eksport (kopia zapasowa):**
1. Kliknij **"Odczytaj dane ze sterownika"**
2. Kliknij **"Zapisz dane do CSV"**
3. Wybierz miejsce zapisu
4. Zapisz plik

**Import (przywracanie):**
1. Kliknij **"Odczytaj dane z CSV"**
2. Wybierz plik CSV
3. Kliknij **"Wgraj dane do sterownika"**

---

## Rozwiązywanie Problemów

### Problem: "Nie znaleziono pliku avrdude.exe"
**Rozwiązanie:**
- Sprawdź czy folder `tools/` zawiera plik `avrdude.exe` (Windows) lub `avrdude` (macOS/Linux)
- Pobierz ponownie aplikację z pełnym pakietem

### Problem: "Błąd komunikacji"
**Rozwiązanie:**
1. Sprawdź czy sterownik jest podłączony
2. Sprawdź czy wybrany właściwy port COM
3. Sprawdź czy sterownik ma zasilanie
4. Spróbuj innego portu USB
5. Zrestartuj aplikację

### Problem: "Port COM niedostępny"
**Rozwiązanie:**
1. Zamknij inne programy korzystające z portu (Arduino IDE, PuTTY, itp.)
2. Odłącz i podłącz ponownie kabel USB
3. Sprawdź sterowniki USB-UART w menedżerze urządzeń

### Problem: "Nieprawidłowy numer w polu"
**Rozwiązanie:**
- Numer musi mieć 3-9 cyfr
- Tylko cyfry (bez spacji, kresek, nawiasów)
- Przykład poprawny: `600123456`
- Przykład niepoprawny: `+48 600 123 456`

### Problem: "Pole zawiera niedozwolone znaki"
**Rozwiązanie:**
- Usuń litery, spacje, znaki specjalne
- Zostaw tylko cyfry 0-9

### Problem: Aplikacja się nie uruchamia
**Rozwiązanie:**
1. Sprawdź uprawnienia do pliku
2. Uruchom jako administrator (Windows)
3. Sprawdź logi w pliku `bramster.log`

### Problem: Numery nie są zapisywane
**Rozwiązanie:**
1. Sprawdź czy kliknąłeś **"Wgraj dane do sterownika"** po zmianach
2. Poczekaj na zakończenie operacji (27 sekund)
3. Odczytaj ponownie dane ze sterownika aby zweryfikować

### Problem: Harmonogram nie działa
**Rozwiązanie:**
1. Sprawdź czy checkbox "Włącz harmonogram" jest zaznaczony
2. Sprawdź czy czas START i STOP są poprawne (00-23:00-59)
3. Kliknij **"Wgraj dane do sterownika"**
4. Sprawdź czy sterownik ma poprawny czas (wymaga synchronizacji z siecią GSM)

---

## Parametry Techniczne

### Sterownik
- **Mikrokontroler:** ATmega1284P
- **Pamięć EEPROM:** 4096 bajtów
- **Maksymalna liczba numerów:** 800
- **Długość numeru:** 3-9 cyfr
- **Kod dostępu:** 4 cyfry

### Komunikacja
- **Protokół:** UART (szeregowy)
- **Prędkość:** 115200 baud
- **Programator:** urclock
- **Narzędzie:** avrdude

### Adresy EEPROM
- **Numery telefonów:** 0x0008 - 0x0FA7 (5 bajtów na numer)
- **Kod dostępu:** 0x0001 - 0x0004
- **Status:** 0x0FF7 (4087)
- **Tryb pracy:** 0x0FFE (4094)
- **CLIP/DTMF:** 0x0FFF (4095) - tylko DTM-HS
- **Skryba:** 0x0FF9 (4089)
- **Limit Skryba:** 0x0FF5-0x0FF6 (4085-4086)
- **Harmonogram START:** 0x0FFA-0x0FFB (4090-4091)
- **Harmonogram STOP:** 0x0FFC-0x0FFD (4092-4093)
- **Suma kontrolna:** 0x0000

---

## Podsumowanie Przepływu Pracy

### Typowy scenariusz konfiguracji:

1. **Podłącz sterownik** do komputera
2. **Wybierz port COM**
3. **Odczytaj dane ze sterownika** (27s)
4. **Dodaj/usuń numery** telefonów
5. **Ustaw tryb pracy** (Prywatny/Publiczny)
6. **Ustaw status** (Aktywny/Blokada)
7. **(Opcjonalnie) Włącz Skrybę**
8. **(Opcjonalnie) Skonfiguruj harmonogram**
9. **(Opcjonalnie) Zmień kod dostępu**
10. **Wgraj dane do sterownika** (27s)
11. **Odłącz sterownik**

### Kopia zapasowa:

1. **Odczytaj dane ze sterownika**
2. **Zapisz dane do CSV**
3. Zachowaj plik w bezpiecznym miejscu

### Przywracanie z kopii:

1. **Odczytaj dane z CSV**
2. **Wgraj dane do sterownika**

---

## Kontakt i Wsparcie

**Producent:** Robert Gramsz  
**Strona:** www.sonfy.pl  
**Aplikacja:** Bramster AC800-DTM-HS  
**Wersja firmware:** 2.0

---

*Dokument wygenerowany automatycznie na podstawie kodu źródłowego aplikacji AC800-DTM-HS.py*

# Instrukcja Obsługi Funkcji SKRYBA

## Co to jest Skryba?

**Skryba** to funkcja automatycznego dodawania numerów telefonów do systemu. Gdy jest włączona, każdy nieznany numer, który zadzwoni do urządzenia, zostanie automatycznie dodany do listy autoryzowanych użytkowników.

## Komendy SMS

### Włączenie Skryby
```
ABCD SKRYBA ON
```
Włącza automatyczne dodawanie nowych numerów.

### Wyłączenie Skryby
```
ABCD SKRYBA OFF
```
Wyłącza automatyczne dodawanie nowych numerów.

## Jak Działa Skryba?

### Proces Automatycznego Dodawania

1. **Przychodzące połączenie** - gdy ktoś dzwoni do urządzenia
2. **Sprawdzenie listy** - system sprawdza czy numer jest już zapisany
3. **Automatyczny zapis** - jeśli numer nie istnieje i Skryba jest włączona:
   - Numer jest automatycznie dodawany do pierwszej wolnej pozycji
   - Używane są ostatnie 9 cyfr numeru (format skrócony)
   - Numer jest zapisywany na pozycjach **1-795**

### Ważne: Jak System Zapisuje Numery

**System zapisuje TYLKO ostatnie 9 cyfr (0-9) z numeru telefonu.**

**Znaki pomijane:**
- `+` (prefiks międzynarodowy)
- `#` (kratka)
- `*` (gwiazdka)
- Spacje

**Przykłady:**

| Co przychodzi | Co się zapisuje |
|---------------|-----------------|
| `+48 793557357` | `793557357` (9 cyfr) |
| `48793557357` | `793557357` (ostatnie 9) |
| `+48793557357` | `793557357` (ostatnie 9) |
| `123456789` | `123456789` (9 cyfr) |
| `+000#777777` | `000777777` (tylko cyfry) |

⚠️ **Uwaga:** Jeśli numer ma więcej niż 9 cyfr, system zapisze **tylko ostatnie 9**!


### Ograniczenia

#### Limit Pozycji
- Skryba dodaje numery **tylko do pozycji 1-795**
- Pozycje **795-800 są zarezerwowane dla Super Userów**
- Super Userzy muszą być dodani ręcznie (nie przez Skrybę)

#### Automatyczne Wyłączenie
Gdy liczba zapisanych numerów osiągnie ustawiony limit, Skryba automatycznie się wyłącza.

#### Limit można ustawić przez aplikację EEPROM:
- Domyślny limit: **795 użytkowników**
- Maksymalny limit: **795 użytkowników** (pozycje 796-800 zarezerwowane)

## Tryby Pracy

### Tryb Publiczny (OPEN)
- Skryba działa, ale **wszyscy** mogą otwierać bramę
- Numery są zapisywane dla celów statystycznych

### Tryb Prywatny (CLOSE)
- Skryba działa i **tylko zapisane numery** mogą otwierać bramę
- Nowe numery są automatycznie autoryzowane po pierwszym połączeniu

## Przykłady Użycia

### Scenariusz 1: Budynek Mieszkalny (Tryb Prywatny)
```
ABCD CLOSE          # Ustaw tryb prywatny
ABCD SKRYBA ON      # Włącz Skrybę
```
- Pierwszy mieszkaniec dzwoni → numer zapisany → brama otwarta
- Kolejne połączenia tego numeru → brama otwarta
- Nieznany numer → brama zamknięta, ale numer zapisany
- Po drugim połączeniu nieznany numer → brama otwarta

### Scenariusz 2: Parking Publiczny (Tryb Publiczny)
```
ABCD OPEN           # Ustaw tryb publiczny
ABCD SKRYBA ON      # Włącz Skrybę
```
- Każdy może otworzyć bramę
- System zapisuje wszystkie numery dla statystyk

### Scenariusz 3: Wyłączenie Automatycznego Dodawania
```
ABCD SKRYBA OFF     # Wyłącz Skrybę
ABCD CLOSE          # Tryb prywatny
```
- Tylko wcześniej zapisane numery mogą otwierać bramę
- Nowe numery nie są dodawane automatycznie

## Super Userzy (Pozycje 795-800)

### Czym się różnią Super Userzy?

Super Userzy to specjalne numery na pozycjach **795-800**, które:
- ✅ **Działają zawsze** - nawet gdy system jest zatrzymany (`ABCD STOP`)
- ✅ **Omijają harmonogram** - działają poza godzinami ustawionymi `ABCD TIME`
- ✅ **Nie mogą być nadpisani** - Skryba nie może ich usunąć ani nadpisać
- ✅ **Muszą być dodane ręcznie** - przez aplikację EEPROM lub komendę SMS

### Jak Dodać Super Usera?

Super Userów można dodać tylko ręcznie:
1. Przez aplikację **AC800-DTM-HS.py** (EEPROM Editor)
2. Przez komendę SMS (jeśli zaimplementowana)
3. Zapisując numer bezpośrednio na pozycjach 795-800 w EEPROM

## Sprawdzanie Statusu

### Komenda REPORT (przed zmianą)
```
ABCD REPORT
```
**Odpowiedź zawierała**:
```
*
AC800-TS
Czas: 16:10:00
Sygnal GSM 85%
Uzytkownicy 45/755
Status: Aktywny
Tryb: Publiczny CLIP
Harmonogram: Wylaczony
Skryba: Limit 750          ← TA LINIA ZOSTAŁA USUNIĘTA
www.sonfy.pl
```

### Komenda REPORT (po zmianie)
```
ABCD REPORT
```
**Nowa odpowiedź**:
```
*
AC800-TS
Czas: 16:10:00
Sygnal GSM 85%
Uzytkownicy 45/755
Status: Aktywny
Tryb: Publiczny CLIP
Harmonogram: Wylaczony
www.sonfy.pl
```

> **Uwaga**: Informacja o Skrybie została usunięta z raportu SMS, ale funkcja nadal działa!

## Zarządzanie przez Aplikację

Status Skryby można sprawdzić i zmienić przez aplikację **AC800-DTM-HS.py**:
- Checkbox "Skryba ON/OFF"
- Pole "Limit użytkowników" (1-795)
- Zmiany są zapisywane w EEPROM (adres 4089)

## Rozwiązywanie Problemów

### Skryba nie dodaje numerów
1. Sprawdź czy Skryba jest włączona: `ABCD SKRYBA ON`
2. Sprawdź czy nie osiągnięto limitu (795 użytkowników)
3. Sprawdź czy pozycje 1-795 nie są pełne

### Numer został dodany, ale brama się nie otwiera
1. Sprawdź tryb pracy: `ABCD REPORT`
2. W trybie prywatnym (`CLOSE`) numer musi być zapisany
3. Sprawdź czy nie ma blokady czasowej (`ABCD TIME`)
4. Sprawdź czy system nie jest zatrzymany (`ABCD STOP`)

### Chcę usunąć wszystkie numery
```
ABCD RESET          # Resetuje wszystkie ustawienia (UWAGA!)
```
**Ostrzeżenie**: Ta komenda usuwa WSZYSTKIE numery i ustawienia!

## Podsumowanie

| Funkcja | Komenda | Opis |
|---------|---------|------|
| Włącz Skrybę | `ABCD SKRYBA ON` | Automatyczne dodawanie numerów |
| Wyłącz Skrybę | `ABCD SKRYBA OFF` | Zatrzymaj automatyczne dodawanie |
| Sprawdź status | `ABCD REPORT` | Pokaż status systemu (bez info o Skrybie) |
| Tryb publiczny | `ABCD OPEN` | Wszyscy mogą otwierać |
| Tryb prywatny | `ABCD CLOSE` | Tylko zapisane numery |

---

**Wersja dokumentu**: 1.0  
**Data**: 2025-12-11  
**System**: AC800-DTM-HS

# Instrukcja Obsługi: Super User

## System Kontroli Dostępu AC800-DTM-HS-RC3

---

## Czym jest Super User?

**Super User** to użytkownik z rozszerzonymi uprawnieniami, który może:

✅ **Dzwonić zawsze** - nawet gdy system jest zatrzymany (`ABCD STOP`)  
✅ **Omijać harmonogram** - dzwonić poza godzinami ustawionymi w `ABCD TIME`  
✅ **Mieć gwarantowane miejsce** - pozycje 795-800 są zarezerwowane tylko dla Super Userów

---

## Ważne: Jak System Zapisuje Numery

**System zapisuje TYLKO ostatnie 9 cyfr (0-9) z numeru telefonu.**

**Znaki pomijane:**
- `+` (prefiks międzynarodowy)
- `#` (kratka)
- `*` (gwiazdka)
- Spacje

**Przykłady:**

| Co wpisujesz | Co się zapisuje |
|--------------|-----------------|
| `+48 793557357` | `793557357` (9 cyfr) |
| `48793557357` | `793557357` (ostatnie 9) |
| `+48793557357` | `793557357` (ostatnie 9) |
| `123456789` | `123456789` (9 cyfr) |
| `+000#777777` | `000777777` (tylko cyfry) |

⚠️ **Uwaga:** Jeśli wpiszesz więcej niż 9 cyfr, system zapisze **tylko ostatnie 9**!

---

## Jak Dodać Super Usera?

### Krok 1: Wyślij SMS z kodem dostępu

```
ABCD SUB 793557357
```

**Gdzie:**
- `ABCD` - Twój kod dostępu (4 cyfry)
- `SUB` - komenda dodania Super Usera
- `793557357` - numer telefonu (bez prefiksu +48)

### Krok 2: Otrzymasz potwierdzenie

```
Super User dodany na pozycji 795
```

**Gotowe!** Numer został dodany jako Super User.

---

## Jak Usunąć Super Usera?

### Wyślij SMS:

```
ABCD DEL 793557357
```

**Gdzie:**
- `ABCD` - Twój kod dostępu
- `DEL` - komenda usunięcia
- `793557357` - numer telefonu do usunięcia

**Uwaga:** Komenda DEL nie wysyła potwierdzenia SMS. Aby sprawdzić czy numer został usunięty, wyślij `ABCD REPORT`.

---

## Jak Sprawdzić Status?

### Wyślij SMS:

```
ABCD REPORT
```

### Otrzymasz raport:

```
*
AC800-DTM-TS
Czas: 16:10:00
Sygnal GSM 85%
Uzytkownicy 2/800
Status: Aktywny
Tryb: Publiczny CLIP
Harmonogram: Wylaczony
Skryba: Wylaczona
www.sonfy.pl
```

**"Uzytkownicy 2/800"** - pokazuje ile numerów jest zapisanych (w tym Super Userzy)

---

## Ile Mogę Dodać Super Userów?

**Maksymalnie 6 Super Userów** (pozycje 795-800)

Jeśli spróbujesz dodać 7. Super Usera, otrzymasz:
```
Brak wolnych pozycji Super User (795-800)
```

---

## Przykłady Użycia

### Przykład 1: Właściciel Firmy

**Sytuacja:** Chcesz mieć dostęp do bramy zawsze, nawet gdy:
- System jest zatrzymany na weekend (`ABCD STOP`)
- Poza godzinami pracy (harmonogram 8:00-16:00)

**Rozwiązanie:**
```
ABCD SUB 600123456
```

Teraz możesz dzwonić 24/7, niezależnie od ustawień!

### Przykład 2: Ochrona

**Sytuacja:** Ochrona musi mieć dostęp zawsze, nawet w nocy.

**Rozwiązanie:**
```
ABCD SUB 600234567
```

Ochrona może dzwonić poza harmonogramem czasowym.

### Przykład 3: Usunięcie Pracownika

**Sytuacja:** Pracownik odszedł z firmy, trzeba usunąć jego numer.

**Rozwiązanie:**
```
ABCD DEL 600345678
ABCD REPORT  (sprawdź czy usunięto)
```

---

## Różnice: Super User vs Zwykły Użytkownik

| Funkcja | Zwykły Użytkownik | Super User |
|---------|-------------------|------------|
| Dzwonienie gdy `ABCD STOP` | ❌ Zablokowane | ✅ Działa |
| Dzwonienie poza `ABCD TIME` | ❌ Zablokowane | ✅ Działa |
| Pozycje w systemie | 1-795 | 795-800 |
| Może być nadpisany przez Skrybę | ✅ Tak | ❌ Nie |
| Dodawanie | `ABCD ADD numer` | `ABCD SUB numer` |
| Usuwanie | `ABCD DEL numer` | `ABCD DEL numer` |

---

## Często Zadawane Pytania

### ❓ Czy Super User musi wpisywać kod DTMF?

**Tak**, w trybie DTMF Super User musi:
1. Odebrać połączenie (system odbiera automatycznie)
2. Wcisnąć klawisz **"1"** aby otworzyć bramę

W trybie CLIP brama otwiera się automatycznie.

### ❓ Czy mogę mieć ten sam numer jako zwykły użytkownik i Super User?

**Nie**, każdy numer może być tylko raz w systemie. Jeśli numer jest już dodany jako zwykły użytkownik, komenda `ABCD SUB` zwróci:
```
Numer juz istnieje w systemie
```

Musisz najpierw usunąć numer (`ABCD DEL`), a potem dodać jako Super User (`ABCD SUB`).

### ❓ Co się stanie gdy zapełnię wszystkie 6 miejsc Super User?

Otrzymasz komunikat:
```
Brak wolnych pozycji Super User (795-800)
```

Musisz usunąć któryś istniejący Super User (`ABCD DEL`), żeby dodać nowy.

### ❓ Czy Super User może być usunięty przez Skrybę?

**Nie**, funkcja Skryba (automatyczne dodawanie numerów) działa tylko na pozycjach 1-795. Pozycje 795-800 są chronione i mogą być zarządzane tylko ręcznie przez komendy SMS.

---

## Komendy SMS - Szybkie Przypomnienie

| Komenda | Opis | Przykład |
|---------|------|----------|
| `ABCD SUB numer` | Dodaj Super Usera | `ABCD SUB 600123456` |
| `ABCD DEL numer` | Usuń użytkownika | `ABCD DEL 600123456` |
| `ABCD REPORT` | Sprawdź status | `ABCD REPORT` |
| `ABCD STOP` | Zatrzymaj system | `ABCD STOP` |
| `ABCD START` | Uruchom system | `ABCD START` |
| `ABCD TIME HH:MM HH:MM` | Ustaw harmonogram | `ABCD TIME 08:00 16:00` |
| `ABCD TIME OFF` | Wyłącz harmonogram | `ABCD TIME OFF` |

---

## Wsparcie Techniczne

**Producent:** Robert Gramsz  
**Website:** www.sonfy.pl  
**Wersja Firmware:** AC800-DTM-HS-RC3  
**Data:** 2025-12-11

---

## Bezpieczeństwo

⚠️ **WAŻNE:**
- Nie udostępniaj kodu dostępu ABCD osobom niepowołanym
- Super Userzy mają pełny dostęp - dodawaj tylko zaufane numery
- Regularnie sprawdzaj listę użytkowników (`ABCD REPORT`)
- W razie utraty telefonu Super Usera, natychmiast usuń jego numer (`ABCD DEL`)

---

**Koniec instrukcji**

# Instrukcja Obsługi - Sterownik Bramy AC800-DTM-HS

## Dla Użytkownika

**Wersja:** RC3  
**Data:** 2025-12-11

---

## Podstawowe Informacje

Urządzenie steruje bramą przez **SMS** lub **połączenie telefoniczne**.

**Twój kod dostępu:** `ABCD` (zmień na swój 4-cyfrowy kod)

---

## Lampka LED - Co Oznacza?

Na urządzeniu jest **lampka LED** która pokazuje co się dzieje:

### Jak Działa Lampka?

| Co robi lampka? | Co to znaczy? |
|-----------------|---------------|
| 💡 **Świeci cały czas** | Urządzenie szuka sieci - czeka na połączenie z operatorem |
| ⚫ **Zgaszona** | Wszystko OK - urządzenie działa prawidłowo ✅ |
| ⚡ **Miga szybko co 5 sekund** (3 błyski) | Działa OK - dobry zasięg sieci 📶📶📶 |
| 💫 **Miga wolno co 5 sekund** (2 błyski) | Działa OK - słaby zasięg sieci 📶 |
| ✨ **5 szybkich błysków** | Wysyła SMS - urządzenie coś robi 📨 |
| 💥 **Jedno krótkie mrugnięcie** | Przyszedł SMS lub ktoś dzwoni 📞 |

### ⚠️ Lampka Świeci Cały Czas - Co Robić?

Jeśli lampka **świeci bez przerwy** dłużej niż 2 minuty:

**Sprawdź po kolei:**
1. ✅ Czy karta SIM jest włożona?
2. ✅ Czy karta SIM ma **wyłączony PIN**? (musi być wyłączony!)
3. ✅ Czy w tym miejscu jest zasięg sieci? (sprawdź na telefonie)
4. ✅ Czy antena jest podłączona?

**To normalne:** Po włączeniu urządzenia lampka świeci przez minutę, potem gaśnie. To znaczy że wszystko działa! 👍

---

## Jak Otworzyć Bramę?

### Sposób 1: Zadzwoń
1. Zadzwoń na numer urządzenia
2. Brama otworzy się automatycznie
3. Połączenie zostanie rozłączone

⚠️ **Uwaga:** Komenda `ABCD OPEN` **NIE otwiera bramy** - ona zmienia tryb pracy na "Publiczny"!

---

## Podstawowe Komendy SMS

### Dodaj Numer Telefonu
```
ABCD ADD 793557357
```
**Co robi:** Dodaje numer do listy uprawnionych użytkowników.

**Przykład:**
- Wysyłasz: `ABCD ADD 600123456`
- Efekt: Numer 600123456 może teraz dzwonić i otwierać bramę
- Numer zapisuje się na pierwszej wolnej pozycji (1-795)

---

### Usuń Numer Telefonu
```
ABCD DEL 793557357
```
**Co robi:** Usuwa numer z listy.

**Przykład:**
- Wysyłasz: `ABCD DEL 600123456`
- Efekt: Numer 600123456 nie może już otwierać bramy
- **Uwaga:** Nie dostaniesz SMS z potwierdzeniem

---

### Sprawdź Czy Numer Jest w Systemie
```
ABCD USER 793557357
```
**Co robi:** Sprawdza czy numer jest zapisany w systemie.

**Przykład 1 - Numer istnieje:**
- Wysyłasz: `ABCD USER 600123456`
- Odpowiedź: `600123456: OK`
- Znaczy: Numer jest w systemie ✅

**Przykład 2 - Numer nie istnieje:**
- Wysyłasz: `ABCD USER 600999888`
- Odpowiedź: `600999888: Brak takiego numeru w systemie`
- Znaczy: Numer NIE jest w systemie ❌

---

### Sprawdź Status Systemu
```
ABCD REPORT
```
**Co robi:** Wysyła pełny raport o stanie systemu.

**Przykładowa odpowiedź:**
```
*
AC800-DTM-TS
Czas: 16:10:00
Sygnal GSM 85%
Uzytkownicy 45/800
Status: Aktywny
Tryb: Publiczny CLIP
Harmonogram: 08:00-16:00
Skryba: Wlaczona
www.sonfy.pl
```

**Co oznaczają informacje:**
- **Czas:** Aktualny czas w systemie
- **Sygnał GSM:** Jakość połączenia (im wyższy, tym lepiej)
- **Użytkownicy 45/800:** 45 numerów zapisanych, 755 wolnych miejsc
- **Status:** Aktywny (działa) lub Zablokowany (zatrzymany)
- **Tryb:** Publiczny (wszyscy) lub Prywatny (tylko zapisani)
- **Harmonogram:** Godziny pracy lub Wylaczony
- **Skryba:** Wlaczona (auto-dodawanie) lub Wylaczona

---

## Zatrzymanie i Uruchomienie Systemu

### Zatrzymaj System (np. na weekend)
```
ABCD STOP
```
**Co robi:** Blokuje bramę - nikt nie może wejść (oprócz Super Userów).

**Kiedy użyć:**
- Weekend - zamykasz firmę
- Urlop - nie ma nikogo w biurze
- Awaria - chcesz zablokować dostęp

**Przykład:**
- Piątek 16:00: Wysyłasz `ABCD STOP`
- Efekt: Brama zablokowana do poniedziałku
- Super Userzy (VIP) nadal mogą wchodzić!
- Sprawdź: `ABCD REPORT` → zobaczysz "Status: Zablokowany"

---

### Uruchom System
```
ABCD START
```
**Co robi:** Odblokowuje bramę - system wraca do normalnej pracy.

**Przykład:**
- Poniedziałek 8:00: Wysyłasz `ABCD START`
- Efekt: Brama działa normalnie
- Wszyscy zapisani użytkownicy mogą wchodzić
- Sprawdź: `ABCD REPORT` → zobaczysz "Status: Aktywny"

---

## Harmonogram Czasowy

### Ustaw Godziny Pracy (np. 8:00 - 16:00)
```
ABCD TIME 08:00 16:00
```
**Co robi:** Brama działa tylko w określonych godzinach.

**Przykład:**
- Wysyłasz: `ABCD TIME 08:00 16:00`
- Efekt:
  - **8:00-16:00** → Brama działa normalnie ✅
  - **16:00-8:00** → Brama zablokowana ❌ (oprócz Super Userów)
- Sprawdź: `ABCD REPORT` → zobaczysz "Harmonogram: 08:00-16:00"

**Kiedy użyć:**
- Firma pracuje 8:00-16:00
- Chcesz żeby po godzinach nikt nie wchodził
- Super Userzy (szef, ochrona) mogą wchodzić zawsze

---

### Wyłącz Harmonogram
```
ABCD TIME OFF
```
**Co robi:** Wyłącza ograniczenia czasowe - brama działa 24/7.

**Przykład:**
- Wysyłasz: `ABCD TIME OFF`
- Efekt: Brama działa przez całą dobę
- Sprawdź: `ABCD REPORT` → zobaczysz "Harmonogram: Wylaczony"

---

## Super Userzy (Dostęp VIP)

**Co to jest Super User?**

Super User to numer z **pełnym dostępem** - działa **zawsze**, nawet gdy:
- System jest zatrzymany (`ABCD STOP`)
- Poza godzinami pracy (`ABCD TIME`)

**Dla kogo:**
- Szef firmy - potrzebuje dostępu 24/7
- Ochrona - musi wchodzić w nocy
- Serwis - naprawy poza godzinami

---

### Dodaj Super Usera
```
ABCD SUB 793557357
```
**Co robi:** Dodaje numer jako Super User (VIP) na pozycjach 795-800.

**Przykład:**
- Wysyłasz: `ABCD SUB 600111222`
- Odpowiedź: `Super User dodany na pozycji 795`
- Efekt: Numer 600111222 ma pełny dostęp 24/7
- **Maksymalnie 6 Super Userów** (pozycje 795-800)

**Co się stanie gdy zapełnisz 6 miejsc:**
- Wysyłasz: `ABCD SUB 600777888` (7. Super User)
- Odpowiedź: `Brak wolnych pozycji Super User (795-800)`
- Musisz usunąć któregoś Super Usera żeby dodać nowego

---

### Usuń Super Usera
```
ABCD DEL 793557357
```
**Co robi:** Usuwa Super Usera (tak samo jak zwykłego użytkownika).

**Przykład:**
- Wysyłasz: `ABCD DEL 600111222`
- Efekt: Numer 600111222 nie jest już Super Userem
- **Uwaga:** Nie dostaniesz SMS z potwierdzeniem
- Sprawdź: `ABCD USER 600111222` → zobaczysz "Brak takiego numeru"

---

## Automatyczne Dodawanie (Skryba)

**Co to jest Skryba?**

Skryba automatycznie dodaje nowe numery do systemu. Gdy ktoś zadzwoni pierwszy raz, system go zapamięta.

**Kiedy użyć:**
- Masz wielu pracowników
- Nie chcesz ręcznie dodawać każdego numeru
- Chcesz żeby system sam zarządzał dostępem

---

### Włącz Skrybę
```
ABCD SKRYBA ON
```
**Co robi:** Włącza automatyczne dodawanie numerów.

**Przykład:**
- Wysyłasz: `ABCD SKRYBA ON`
- Sprawdź: `ABCD REPORT` → zobaczysz "Skryba: Wlaczona"

**Co się dzieje:**
1. Nowy pracownik dzwoni pierwszy raz
2. System automatycznie dodaje jego numer (pozycje 1-795)
3. Drugi raz dzwoni → brama się otwiera

**Ważne:**
- Skryba dodaje tylko do pozycji 1-795
- Pozycje 795-800 są zarezerwowane dla Super Userów
- Gdy zapełni się 795 miejsc, Skryba się automatycznie wyłącza

---

### Wyłącz Skrybę
```
ABCD SKRYBA OFF
```
**Co robi:** Wyłącza automatyczne dodawanie.

**Przykład:**
- Wysyłasz: `ABCD SKRYBA OFF`
- Sprawdź: `ABCD REPORT` → zobaczysz "Skryba: Wylaczona"
- Efekt: Nowe numery NIE będą dodawane automatycznie
- Musisz dodawać ręcznie przez `ABCD ADD`

---

## Tryby Pracy (OPEN / CLOSE)

**Co to są tryby pracy?**

System ma dwa tryby:
- **Publiczny (OPEN)** - wszyscy mogą dzwonić i otwierać bramę
- **Prywatny (CLOSE)** - tylko zapisane numery mogą otwierać

---

### Tryb Publiczny - Wszyscy Mogą Dzwonić
```
ABCD OPEN
```
**Co robi:** Zmienia tryb na Publiczny - każdy może otworzyć bramę.

**Przykład:**
- Wysyłasz: `ABCD OPEN`
- Sprawdź: `ABCD REPORT` → zobaczysz "Tryb: Publiczny CLIP"
- Efekt: Każdy kto zadzwoni otworzy bramę (nie tylko zapisani)

**Kiedy użyć:**
- Parking publiczny - wszyscy mogą wjeżdżać
- Dzień otwarty - chcesz żeby każdy mógł wejść
- Tymczasowo - np. dostawa, goście

⚠️ **Ważne:** `ABCD OPEN` **nie otwiera bramy** - tylko zmienia tryb!

---

### Tryb Prywatny - Tylko Zapisane Numery
```
ABCD CLOSE
```
**Co robi:** Zmienia tryb na Prywatny - tylko zapisane numery mogą otwierać.

**Przykład:**
- Wysyłasz: `ABCD CLOSE`
- Sprawdź: `ABCD REPORT` → zobaczysz "Tryb: Prywatny CLIP"
- Efekt: Tylko numery z listy (ADD lub Skryba) mogą otwierać bramę

**Kiedy użyć:**
- Firma - tylko pracownicy mogą wchodzić
- Budynek mieszkalny - tylko mieszkańcy
- Bezpieczeństwo - kontrola dostępu

---

## Ważne Informacje

### Jak System Zapisuje Numery?

System zapisuje **tylko ostatnie 9 cyfr** numeru telefonu.

**Przykłady:**
- Wpisujesz: `+48 793557357` → Zapisuje: `793557357`
- Wpisujesz: `48793557357` → Zapisuje: `793557357` (ostatnie 9)
- Wpisujesz: `+000#777777` → Zapisuje: `000777777` (tylko cyfry)

**Znaki pomijane:** `+`, `#`, `*`, spacje

### Limit Użytkowników

- **Zwykli użytkownicy:** 1-795 (795 miejsc)
- **Super Userzy:** 795-800 (6 miejsc)
- **Razem:** 800 numerów

---

## Szybka Ściągawka - Wszystkie Komendy

| Co chcesz zrobić | Komenda | Opis |
|------------------|---------|------|
| **Zarządzanie Numerami** |
| Dodać numer | `ABCD ADD 793557357` | Dodaje zwykłego użytkownika |
| Usunąć numer | `ABCD DEL 793557357` | Usuwa użytkownika |
| Sprawdzić numer | `ABCD USER 793557357` | Sprawdza czy numer jest w systemie |
| Dodać VIP (Super User) | `ABCD SUB 793557357` | Dodaje Super Usera (pozycje 795-800) |
| **System** |
| Sprawdzić status | `ABCD REPORT` | Pełny raport systemu |
| Zatrzymać system | `ABCD STOP` | Blokuje bramę (oprócz Super Userów) |
| Uruchomić system | `ABCD START` | Odblokowuje bramę |
| Zmienić kod dostępu | `ABCD CODE C3D4` | Zmienia kod z ABCD na C3D4 |
| Reset fabryczny | `ABCD XXXX` | ⚠️ Usuwa WSZYSTKO! |
| **Harmonogram** |
| Ustawić godziny pracy | `ABCD TIME 08:00 16:00` | Brama działa tylko 8:00-16:00 |
| Wyłączyć harmonogram | `ABCD TIME OFF` | Brama działa 24/7 |
| Ustawić czas | `ABCD SET 16:30:00` | Ustawia czas w systemie |
| Sprawdzić czas | `ABCD SET` | Pokazuje aktualny czas |
| **Tryby Pracy** |
| Tryb publiczny | `ABCD OPEN` | Wszyscy mogą dzwonić |
| Tryb prywatny | `ABCD CLOSE` | Tylko zapisane numery |
| Tryb CLIP | `ABCD OPEN CLIP` | Publiczny + automatyczne otwarcie |
| Tryb DTMF | `ABCD OPEN DTMF` | Publiczny + klawisz "1" |
| **Skryba (Auto-dodawanie)** |
| Włączyć Skrybę | `ABCD SKRYBA ON` | Automatyczne dodawanie numerów |
| Wyłączyć Skrybę | `ABCD SKRYBA OFF` | Zatrzymaj auto-dodawanie |
| **Debug** |
| Tryb debug | `ABCD DEBUG ON/OFF` | Włącz/wyłącz tryb debugowania |

---

## Praktyczne Scenariusze Użycia

### Scenariusz 1: Dodanie Nowego Pracownika

**Sytuacja:** Jan Kowalski zaczyna pracę, potrzebujesz dodać jego numer.

**Krok po kroku:**

1. **Wyślij SMS:**
   ```
   ABCD ADD 600123456
   ```

2. **Sprawdź czy dodano:**
   ```
   ABCD USER 600123456
   ```
   Odpowiedź: `600123456: OK`

3. **Sprawdź ile masz użytkowników:**
   ```
   ABCD REPORT
   ```
   Zobaczysz: `Uzytkownicy 45/800` (zwiększyło się o 1)

**Gotowe!** Jan może teraz dzwonić i otwierać bramę.

---

### Scenariusz 2: Usunięcie Pracownika

**Sytuacja:** Anna Nowak odeszła z firmy, trzeba usunąć jej numer.

**Krok po kroku:**

1. **Usuń numer:**
   ```
   ABCD DEL 600987654
   ```
   (Brak odpowiedzi SMS - to normalne)

2. **Sprawdź czy usunięto:**
   ```
   ABCD USER 600987654
   ```
   Odpowiedź: `600987654: Brak takiego numeru w systemie`

3. **Potwierdź w raporcie:**
   ```
   ABCD REPORT
   ```
   Zobaczysz: `Uzytkownicy 44/800` (zmniejszyło się o 1)

**Gotowe!** Anna nie może już otwierać bramy.

---

### Scenariusz 3: Weekend - Zatrzymanie Systemu

**Sytuacja:** Piątek 16:00, zamykasz firmę na weekend. Chcesz żeby nikt nie mógł wejść.

**Krok po kroku:**

1. **Piątek 16:00 - Zatrzymaj system:**
   ```
   ABCD STOP
   ```

2. **Sprawdź status:**
   ```
   ABCD REPORT
   ```
   Zobaczysz: `Status: Zablokowany`

3. **Poniedziałek 8:00 - Uruchom system:**
   ```
   ABCD START
   ```

4. **Sprawdź status:**
   ```
   ABCD REPORT
   ```
   Zobaczysz: `Status: Aktywny`

**Uwaga:** Super Userzy (VIP) mogą wchodzić nawet gdy system jest zatrzymany!

---

### Scenariusz 4: Godziny Pracy 8:00-16:00

**Sytuacja:** Chcesz żeby brama działała tylko w godzinach pracy.

**Krok po kroku:**

1. **Ustaw godziny:**
   ```
   ABCD TIME 08:00 16:00
   ```

2. **Sprawdź w raporcie:**
   ```
   ABCD REPORT
   ```
   Zobaczysz: `Harmonogram: 08:00-16:00`

**Co się dzieje:**
- **8:00-16:00** → Brama działa normalnie
- **16:00-8:00** → Brama zablokowana (oprócz Super Userów)

**Wyłączenie harmonogramu:**
```
ABCD TIME OFF
```

---

### Scenariusz 5: Dodanie Szefa jako Super User (VIP)

**Sytuacja:** Dyrektor potrzebuje dostępu 24/7, nawet gdy system jest zatrzymany.

**Krok po kroku:**

1. **Dodaj jako Super User:**
   ```
   ABCD SUB 600111222
   ```
   Odpowiedź: `Super User dodany na pozycji 795`

2. **Sprawdź:**
   ```
   ABCD USER 600111222
   ```
   Odpowiedź: `600111222: OK`

**Korzyści:**
- ✅ Działa gdy system zatrzymany (`ABCD STOP`)
- ✅ Działa poza godzinami pracy (`ABCD TIME`)
- ✅ Gwarantowane miejsce (nie usunie Skryba)

---

### Scenariusz 6: Automatyczne Dodawanie Nowych Numerów

**Sytuacja:** Masz wielu pracowników, chcesz żeby system sam dodawał nowe numery.

**Krok po kroku:**

1. **Włącz Skrybę:**
   ```
   ABCD SKRYBA ON
   ```

2. **Sprawdź w raporcie:**
   ```
   ABCD REPORT
   ```
   Zobaczysz: `Skryba: Wlaczona`

**Co się dzieje:**
- Nowy pracownik dzwoni pierwszy raz → System automatycznie dodaje numer
- Drugi raz dzwoni → Brama się otwiera

**Wyłączenie:**
```
ABCD SKRYBA OFF
```

---

## Zmiana Kodu Dostępu

### Zmień Kod z ABCD na Nowy (np. C3D4)
```
ABCD CODE C3D4
```
**Co robi:** Zmienia kod dostępu z ABCD na nowy (np. C3D4).

**Przykład:**
- Stary kod: `ABCD`
- Wysyłasz: `ABCD CODE C3D4`
- Nowy kod: `C3D4`

**Od teraz używaj nowego kodu:**
```
C3D4 REPORT
C3D4 ADD 600123456
C3D4 STOP
C3D4 SUB 600777888
```

**Kiedy zmienić kod:**
- Ktoś poznał Twój kod
- Bezpieczeństwo - zmiana co miesiąc
- Nowy administrator

⚠️ **BARDZO WAŻNE:** 
- Zapamiętaj nowy kod! 
- Zapisz go w bezpiecznym miejscu
- Jeśli zapomnisz, musisz zresetować urządzenie (`ABCD XXXX`)
- Reset usuwa WSZYSTKIE numery i ustawienia!

---

### Scenariusz 7: Sprawdzenie Kto Jest w Systemie

**Sytuacja:** Chcesz sprawdzić czy konkretny numer jest dodany.

**Przykłady:**

```
ABCD USER 600123456
```
Odpowiedź: `600123456: OK` ✅ (jest w systemie)

```
ABCD USER 600999888
```
Odpowiedź: `600999888: Brak takiego numeru w systemie` ❌ (nie ma)

---

### Scenariusz 8: Pełny Raport Systemu

**Komenda:**
```
ABCD REPORT
```

**Przykładowa odpowiedź:**
```
*
AC800-DTM-TS
Czas: 16:10:00
Sygnal GSM 85%
Uzytkownicy 45/800
Status: Aktywny
Tryb: Publiczny CLIP
Harmonogram: 08:00-16:00
Skryba: Wlaczona
www.sonfy.pl
```

**Co oznaczają informacje:**
- **Czas:** Aktualny czas w systemie
- **Sygnał GSM:** Jakość połączenia (im wyższy, tym lepiej)
- **Użytkownicy 45/800:** 45 numerów zapisanych, 755 wolnych miejsc
- **Status:** Aktywny (działa) lub Zablokowany (STOP)
- **Tryb:** Publiczny CLIP (wszyscy mogą dzwonić)
- **Harmonogram:** Godziny pracy lub Wylaczony
- **Skryba:** Wlaczona (auto-dodawanie) lub Wylaczona

---

## Rozwiązywanie Problemów

### Brama się nie otwiera
1. Sprawdź czy numer jest dodany: `ABCD USER 793557357`
2. Sprawdź status: `ABCD REPORT`
3. Sprawdź czy system nie jest zatrzymany (Status: Zablokowany)
4. Sprawdź czy jesteś w godzinach pracy (jeśli ustawione)

### Zapomniałem kodu dostępu
Skontaktuj się z administratorem systemu.

### Chcę usunąć wszystkie numery
```
ABCD XXXX          # Resetuje wszystkie ustawienia (UWAGA!)
```
**Ostrzeżenie**: Ta komenda usuwa WSZYSTKIE numery i ustawienia!

---

## Wsparcie

**Producent:** Robert Gramsz  
**Website:** www.sonfy.pl  
**System:** AC800-DTM-HS-RC3

---

**Koniec instrukcji**

# Instrukcja Obsługi - Sterownik Bramy AC800-DTM-HS

## Dla Użytkownika

**Wersja:** RC3  
**Data:** 2025-12-11

---

## Podstawowe Informacje

Urządzenie steruje bramą przez **SMS** lub **połączenie telefoniczne**.

**ℹ️ Ważne - Jak działa urządzenie:**

Sterownik **nie otwiera bramy bezpośrednio**. Zamiast tego aktywuje **przekaźnik** (wyjście elektryczne), który steruje automatyką bramy. Przekaźnik działa jak przycisk - zamyka obwód elektryczny na 2 sekundy, co powoduje otwarcie bramy przez Twoją automatykę bramową.

💡 **W całej instrukcji:** Gdy piszemy "otwiera bramę" lub "steruje bramą", oznacza to aktywację przekaźnika, który steruje automatyką bramy.

---

**🔑 Co to jest kod dostępu?**

Kod dostępu (domyślnie `ABCD`) to **4-cyfrowy kod zabezpieczający**, który musisz wpisać na początku każdej komendy SMS. Dzięki temu tylko Ty możesz zarządzać systemem.

**Przykład:**
```
ABCD REPORT        # ABCD to Twój kod dostępu
ABCD ADD 600123456 # Każda komenda zaczyna się od kodu
```

**Ważne:** Możesz zmienić kod na własny (np. `1234`, `C3D4`) komendą `ABCD CODE nowy_kod`. Zobacz sekcję "Zmiana Kodu Dostępu" poniżej.

**Twój kod dostępu:** `ABCD` (zmień na swój 4-cyfrowy kod)

---

## Lampki LED - Co Oznaczają?

Na urządzeniu są **dwie lampki LED** które pokazują co się dzieje:

- **LED GSM** 📡 - pokazuje status modemu GSM (połączenie z siecią)
- **LED SYS** 💡 - pokazuje pracę systemu (odbiór/wysyłanie SMS, funkcje)

---

### 📡 LED GSM - Status Modemu

**Co pokazuje:** Połączenie z siecią GSM

| Co robi lampka? | Co to znaczy? |
|-----------------|---------------|
| 💡 **Świeci cały czas** | Modem szuka sieci - czeka na połączenie z operatorem |
| ⚫ **Zgaszona** | Modem zalogowany w sieci - wszystko OK ✅ |
| ⚡ **Miga szybko co 5 sekund** (3 błyski) | Zalogowany - dobry zasięg sieci 📶📶📶 |
| 💫 **Miga wolno co 5 sekund** (2 błyski) | Zalogowany - słaby zasięg sieci 📶 |

### ⚠️ LED GSM Świeci Cały Czas - Co Robić?

Jeśli lampka **świeci bez przerwy** dłużej niż 2 minuty:

**Sprawdź po kolei:**
1. ✅ Czy karta SIM jest włożona?
2. ✅ Czy karta SIM ma **wyłączony PIN**? (musi być wyłączony!)
3. ✅ Czy w tym miejscu jest zasięg sieci? (sprawdź na telefonie)
4. ✅ Czy antena jest podłączona?

**To normalne:** Po włączeniu urządzenia lampka świeci przez minutę, potem gaśnie. To znaczy że wszystko działa! 👍

---

### 💡 LED SYS - Diagnostyka Systemu

**Co pokazuje:** Pracę systemu (odbiór/wysyłanie SMS, aktywne funkcje)

| Co robi lampka? | Co to znaczy? |
|-----------------|---------------|
| ✨ **5 szybkich błysków** | Wysyła SMS - urządzenie coś robi 📨 |
| 💥 **Jedno krótkie mrugnięcie** | Przyszedł SMS lub ktoś dzwoni 📞 |
| ⚫ **Zgaszona** | Brak aktywności - tryb czuwania |

---

## Jak Otworzyć Bramę?

### Sposób 1: Zadzwoń
1. Zadzwoń na numer urządzenia
2. Brama otworzy się automatycznie
3. Połączenie zostanie rozłączone

⚠️ **Uwaga:** Komenda `ABCD OPEN` **NIE otwiera bramy** - ona zmienia tryb pracy na "Publiczny"!

---

## Jak Działa Sterowanie Bramą Przez Telefon?

### 🔐 Sterowanie CLIP - Zadzwoń i Wjedź

**Dostępne w:** Trybie Prywatnym i Publicznym

Sterownik rozpoznaje uprawnione numery dzwoniące na kartę SIM urządzenia. Po rozpoznaniu numeru z listy uprawnionych, system natychmiastowo **aktywuje przekaźnik na 2 sekundy**, otwierając Twoją bramę.

**Jak to działa krok po kroku:**

1. **Dzwonisz** na numer karty SIM w sterowniku
2. **System rozpoznaje** Twój numer telefonu (CLIP)
3. **Sprawdza** czy jesteś na liście uprawnionych
4. **Aktywuje przekaźnik** na 2 sekundy → brama się otwiera
5. **Rozłącza połączenie** automatycznie

**💰 Całkowicie Bezkosztowe!**

Połączenie jest automatycznie rozłączane po aktywacji, co oznacza, że sterowanie jest całkowicie **bez kosztowe** dla użytkownika. Nie płacisz za połączenie!

**Jak aktywować użytkownika:**

- **Tryb Prywatny:** Dodaj numer do listy pamięci urządzenia (`ABCD ADD numer`)
- **Tryb Publiczny:** Każdy numer może otwierać bramę, nawet taki którego nie dodano

**Przykład:**

```
ABCD ADD 600123456    # Dodaj numer do systemu
```

Teraz numer 600123456 może dzwonić i otwierać bramę bezpłatnie!

---

### 🕵️ Tryb Anonimowy - Prywatność i Szybkość

**Dostępne w:** Tylko w Trybie Prywatnym

Cenisz sobie prywatność? Włącz Tryb Anonimowy. Zamiast pełnego numeru telefonu, możesz wprowadzić do systemu **od czterech do sześciu ostatnich cyfr** numeru uprawnionego.

**Korzyści:**

✅ **Pełna anonimowość** w pamięci sterownika  
✅ **Bezpłatne sterowanie** - tak samo jak w trybie CLIP  
✅ **Szybkie działanie** - natychmiastowa aktywacja bramy

**Przykład:**

Zamiast dodawać pełny numer `600123456`, możesz dodać tylko:
- `123456` (6 ostatnich cyfr)
- `23456` (5 ostatnich cyfr)
- `3456` (4 ostatnie cyfry)

```
ABCD ADD 3456    # Dodaj tylko ostatnie 4 cyfry
```

Teraz każdy numer kończący się na `3456` może otwierać bramę (np. 600123456, 501233456, itp.)

**⚠️ Uwaga:** Tryb Anonimowy działa **tylko w trybie Prywatnym** (`ABCD CLOSE`). W trybie Publicznym nie ma znaczenia, bo każdy może dzwonić.

---

### ⏰ Harmonogram Czasowy - Kontrola Godzin Dostępu

**Dostępne w:** Trybie Prywatnym i Publicznym

Uruchomienie harmonogramu pozwala na otwieranie bramy tylko w określonych godzinach.

**Jak to działa:**

1. **Ustawiasz godziny** pracy (np. 8:00 - 16:00)
2. **W tych godzinach** brama działa normalnie
3. **Poza godzinami** brama jest zablokowana (oprócz Super Userów)

**Przykład:**

```
ABCD TIME 08:00 16:00    # Brama działa tylko 8:00-16:00
```

**Co się dzieje:**

| Godzina | Zwykły Użytkownik | Super User (VIP) |
|---------|-------------------|------------------|
| **8:00-16:00** | ✅ Może dzwonić | ✅ Może dzwonić |
| **16:00-8:00** | ❌ Zablokowany | ✅ Może dzwonić |

**Wyłączenie harmonogramu:**

```
ABCD TIME OFF    # Brama działa 24/7
```

**Kiedy użyć:**

- Firma pracuje tylko w określonych godzinach
- Parking otwarty tylko w dzień
- Budynek mieszkalny - cisza nocna

**Przykład zastosowania:**

Masz firmę która pracuje 8:00-16:00. Chcesz żeby:
- Pracownicy mogli wchodzić tylko w godzinach pracy
- Szef (Super User) mógł wchodzić zawsze, nawet w nocy

**Rozwiązanie:**

```
ABCD TIME 08:00 16:00    # Ustaw godziny pracy
ABCD SUB 600111222       # Dodaj szefa jako Super User
```

Teraz:
- Pracownicy mogą dzwonić tylko 8:00-16:00
- Szef może dzwonić 24/7

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

## Tryby Sterowania: CLIP vs DTMF

System obsługuje dwa sposoby sterowania bramą przez telefon:

### 🔐 Tryb CLIP (Domyślny) - Automatyczne Rozpoznawanie

**Jak działa:**
1. Dzwonisz na numer urządzenia
2. System rozpoznaje Twój numer (CLIP)
3. Brama otwiera się **automatycznie**
4. Połączenie się rozłącza

**Zalety:**
- ✅ Szybkie - natychmiastowe otwarcie
- ✅ Wygodne - nie musisz nic wciskać
- ✅ Bezkosztowe - połączenie się rozłącza

**Komenda:**
```
ABCD OPEN CLIP    # Tryb publiczny z CLIP
ABCD CLOSE        # Tryb prywatny (domyślnie CLIP)
```

---

### 📞 Tryb DTMF - Sterowanie Tonami

**Jak działa:**
1. Dzwonisz na numer urządzenia
2. System **odbiera połączenie**
3. Wciskasz klawisz **"1"** na telefonie
4. Brama się otwiera
5. Masz **30 sekund** na wciśnięcie klawisza
6. Po 30 sekundach połączenie się rozłącza

**Zalety:**
- ✅ Działa gdy operator blokuje CLIP
- ✅ Możliwość wielokrotnego otwarcia w jednym połączeniu
- ✅ Kontrola - Ty decydujesz kiedy otworzyć

**Wady:**
- ❌ Płatne - operator może naliczyć opłatę za połączenie
- ❌ Wolniejsze - musisz wcisnąć klawisz

**Komenda:**
```
ABCD OPEN DTMF    # Tryb publiczny z DTMF
```

**Przykład użycia:**
```
1. Wysyłasz SMS: ABCD OPEN DTMF
2. Dzwonisz na numer urządzenia
3. System odbiera (słyszysz sygnał)
4. Wciskasz klawisz "1"
5. Brama się otwiera
6. Możesz wcisnąć "1" ponownie (np. za 10 sekund)
7. Po 30 sekundach połączenie się rozłącza
```

---

### 🤔 Który Tryb Wybrać?

| Sytuacja | Zalecany Tryb |
|----------|---------------|
| Normalnie użytkowanie | **CLIP** - szybkie i bezkosztowe |
| Operator blokuje CLIP | **DTMF** - zawsze działa |
| Potrzebujesz otworzyć kilka razy | **DTMF** - możesz wciskać "1" wielokrotnie |
| Chcesz zaoszczędzić | **CLIP** - połączenie się rozłącza |

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
| **Auto-Sync Czasu** |
| Ustawić numer karty SIM | `ABCD MYNUM 600123456` | Zapisuje numer do auto-sync czasu |
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

## Automatyczna Synchronizacja Czasu (MYNUM)

### Co to jest MYNUM?

MYNUM to numer karty SIM zainstalowanej w sterowniku. System używa go do **automatycznej synchronizacji czasu** po restarcie urządzenia.

**Dlaczego to ważne?**

Po restarcie procesora (np. awaria zasilania), modem GSM może mieć nieprawidłowy czas (00:00:xx). System automatycznie wykrywa to i synchronizuje czas wysyłając SMS do siebie.

---

### Jak Ustawić Numer Karty SIM?

#### Metoda 1: Przez SMS

```
ABCD MYNUM 600123456
```

**Przykłady:**
```
ABCD MYNUM 123456789    → Zapisze: 123456789
ABCD MYNUM +48600123456 → Zapisze: 600123456 (pomija +48)
ABCD MYNUM 600 123 456  → Zapisze: 600123456 (pomija spacje)
```

**Odpowiedź sterownika:**
```
MYNUM zapisany
```

> **📝 Uwaga:** Numer może mieć od 3 do 9 cyfr. Znaki specjalne (+, #, *, spacje) są automatycznie pomijane.

---

### Jak Działa Auto-Sync?

Jeśli sterownik wykryje nieprawidłowy czas po restarcie (00:00:xx), automatycznie:

1. ⏱️ Czeka 25 sekund po zalogowaniu do sieci
2. 🔍 Sprawdza czas w module GSM
3. 📱 Jeśli czas to 00:00:xx - wysyła SMS do siebie (MYNUM)
4. ⏰ Synchronizuje czas z otrzymanego SMS-a

> **✅ Zaleta:** Nie musisz ręcznie ustawiać czasu po każdym restarcie!

---

### Sprawdzanie Zapisanego Numeru

Wyślij SMS:
```
ABCD REPORT
```

W odpowiedzi zobaczysz:
```
Moj nr: 600123456
```

Lub jeśli nie ustawiono:
```
Moj nr: ----
```

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

## Instalacja i Pierwsze Uruchomienie

### 📱 Krok 1: Przygotowanie Karty SIM

**Co potrzebujesz:**
- Karta SIM z aktywnym abonamentem lub doładowaniem
- Telefon do konfiguracji karty SIM

**Wyłączenie kodu PIN:**

1. Włóż kartę SIM do telefonu
2. Wejdź w ustawienia telefonu
3. Znajdź "Bezpieczeństwo" → "Blokada karty SIM"
4. **Wyłącz kod PIN** (bardzo ważne!)
5. Sprawdź czy karta ma zasięg i może odbierać połączenia

⚠️ **WAŻNE:** Karta SIM **MUSI** mieć wyłączony kod PIN, inaczej urządzenie nie zadziała!

---

### 🔧 Krok 2: Instalacja Karty SIM w Urządzeniu

1. **Wyłącz zasilanie** urządzenia
2. Otwórz obudowę (jeśli wymagane)
3. **Włóż kartę SIM** do gniazda (złącza skierowane zgodnie z oznaczeniem)
4. Sprawdź czy karta jest dobrze osadzona
5. Zamknij obudowę

---

### ⚡ Krok 3: Podłączenie do Automatyki Bramy

**Schemat podłączenia:**

```
Sterownik AC800-DTM-HS:
┌─────────────────────┐
│  [+12V] [GND]       │  ← Zasilanie 12V DC
│                     │
│  [NO] [COM] [NC]    │  ← Przekaźnik
└─────────────────────┘
         │
         └─→ Podłącz do automatyki bramy
             (tak jak przycisk otwierania)
```

**Podłączenie przekaźnika:**
- **NO** (Normally Open) - zestyk normalnie otwarty
- **COM** (Common) - wspólny
- **NC** (Normally Closed) - zestyk normalnie zamknięty

**Typowe podłączenie:**
1. Znajdź w automatyce bramy wejście "PRZYCISK" lub "OPEN"
2. Podłącz **COM** i **NO** do tego wejścia
3. Przekaźnik zadziała jak przycisk - zamknie obwód na 2 sekundy

⚠️ **Uwaga:** Jeśli nie jesteś pewien, skonsultuj się z elektrykiem lub producentem automatyki!

---

### 🚀 Krok 4: Pierwsze Uruchomienie

1. **Podłącz zasilanie** (12V DC)
2. **LED GSM zaświeci się** - urządzenie szuka sieci
3. Poczekaj **1-2 minuty**
4. **LED GSM zgaśnie** - urządzenie zalogowane w sieci ✅

**Jeśli LED GSM świeci dłużej niż 2 minuty:**
- Sprawdź czy karta SIM ma wyłączony PIN
- Sprawdź czy w tym miejscu jest zasięg sieci
- Sprawdź czy antena jest podłączona

---

### ✅ Krok 5: Test Działania

**Test 1: Sprawdź status**
```
Wyślij SMS: ABCD REPORT
```
Powinieneś otrzymać raport z informacjami o systemie.

**Test 2: Dodaj swój numer**
```
Wyślij SMS: ABCD ADD 600123456
```
(Wpisz swój numer telefonu)

**Test 3: Otwórz bramę**
```
Zadzwoń na numer karty SIM w urządzeniu
```
Brama powinna się otworzyć, połączenie rozłączy się automatycznie.

**Jeśli wszystko działa - gratulacje! 🎉**

---

## Specyfikacja Techniczna

### Parametry Elektryczne

| Parametr | Wartość |
|----------|---------|
| **Zasilanie** | 12V DC |
| **Pobór prądu** | ~200mA (w spoczynku), ~500mA (podczas połączenia) |
| **Przekaźnik** | 1x NO/NC, max 10A / 250V AC |
| **Czas aktywacji przekaźnika** | 2 sekundy |

### Parametry GSM

| Parametr | Wartość |
|----------|---------|
| **Moduł GSM** | SIM900 |
| **Pasma** | 850/900/1800/1900 MHz (2G) |
| **Karta SIM** | Standard SIM (Mini-SIM) |
| **Antena** | Zewnętrzna, złącze SMA |

### Parametry Środowiskowe

| Parametr | Wartość |
|----------|---------|
| **Temperatura pracy** | -10°C do +50°C |
| **Wilgotność** | 10% - 90% (bez kondensacji) |
| **Stopień ochrony** | IP20 (do montażu wewnętrznego) |

### Pamięć i Limity

| Parametr | Wartość |
|----------|---------|
| **Maksymalna liczba użytkowników** | 800 numerów |
| **Zwykli użytkownicy** | 795 pozycji (1-795) |
| **Super Userzy** | 6 pozycji (795-800) |
| **Długość numeru** | 9 cyfr (ostatnie cyfry) |
| **Kod dostępu** | 4 znaki (cyfry lub litery) |

---

## Bezpieczeństwo i Dobre Praktyki

### 🔒 Zabezpieczenie Kodu Dostępu

**Zmiana kodu dostępu:**
```
ABCD CODE C3D4    # Zmień ABCD na C3D4
```

**Jak często zmieniać kod:**
- ✅ Co 3-6 miesięcy (dla bezpieczeństwa)
- ✅ Gdy podejrzewasz, że ktoś poznał kod
- ✅ Gdy zmienia się administrator systemu
- ✅ Po zwolnieniu pracownika, który znał kod

**Dobre praktyki:**
- 📝 Zapisz kod w bezpiecznym miejscu (sejf, menedżer haseł)
- 🚫 Nie udostępniaj kodu osobom niepowołanym
- 🔄 Używaj różnych kodów dla różnych urządzeń
- ✅ Wybieraj kody trudne do odgadnięcia (nie `1234`, `0000`)

---

### 📱 Co Zrobić Gdy Zgubisz Telefon?

**Natychmiast:**

1. **Usuń numer z systemu:**
   ```
   ABCD DEL 600123456    # Twój zgubiony numer
   ```

2. **Sprawdź czy usunięto:**
   ```
   ABCD USER 600123456
   ```
   Odpowiedź: "Brak takiego numeru w systemie" ✅

3. **Dodaj nowy numer:**
   ```
   ABCD ADD 600999888    # Twój nowy numer
   ```

**Jeśli byłeś Super Userem:**
```
ABCD SUB 600999888    # Dodaj nowy numer jako Super User
```

---

### 💾 Backup Listy Numerów

**Jak zrobić backup:**

1. **Wyślij komendę REPORT:**
   ```
   ABCD REPORT
   ```
   Zobaczysz ile numerów jest w systemie.

2. **Zapisz ważne numery:**
   - Sprawdź każdy numer komendą `ABCD USER numer`
   - Zapisz listę w bezpiecznym miejscu (plik, notatnik)

3. **Regularnie aktualizuj backup:**
   - Co miesiąc lub po każdej większej zmianie
   - Przechowuj w bezpiecznym miejscu

**W razie awarii:**
- Możesz szybko przywrócić wszystkie numery
- Wyślij komendy `ABCD ADD` dla każdego numeru z listy

---

### 🛡️ Zabezpieczenie Fizyczne

**Montaż urządzenia:**
- 🔒 Zamontuj w zamkniętej szafce lub obudowie
- 🚫 Nie montuj w miejscach dostępnych dla osób niepowołanych
- 🌡️ Unikaj miejsc narażonych na wysoką temperaturę
- 💧 Chroń przed wilgocią i wodą

**Zabezpieczenie karty SIM:**
- 🔐 Używaj karty z kodem PUK zapisanym w bezpiecznym miejscu
- 📞 Regularnie sprawdzaj saldo/abonament
- 🚨 Monitoruj nietypową aktywność (dziwne SMS, połączenia)

---

## Rozwiązywanie Problemów (FAQ)

### ❌ Brama się nie otwiera

**Krok po kroku diagnoza:**

1. **Sprawdź czy numer jest dodany:**
   ```
   ABCD USER 600123456
   ```
   - Jeśli "Brak takiego numeru" → Dodaj numer: `ABCD ADD 600123456`

2. **Sprawdź status systemu:**
   ```
   ABCD REPORT
   ```
   - Jeśli "Status: Zablokowany" → Uruchom: `ABCD START`
   - Jeśli "Harmonogram: 08:00-16:00" → Sprawdź czy jesteś w godzinach pracy

3. **Sprawdź tryb:**
   - Jeśli "Tryb: Prywatny" → Tylko zapisane numery mogą otwierać
   - Jeśli "Tryb: Publiczny DTMF" → Musisz wcisnąć klawisz "1"

4. **Sprawdź przekaźnik:**
   - Czy słyszysz kliknięcie przekaźnika?
   - Sprawdź podłączenie do automatyki bramy
   - Sprawdź czy automatyka bramy działa (przycisk manualny)

---

### 📱 SMS nie dochodzą / nie wysyłają się

**Problem: Nie otrzymujesz odpowiedzi na SMS**

1. **Sprawdź czy karta SIM ma saldo/abonament:**
   - Zadzwoń na numer karty SIM
   - Jeśli nie odbiera → problem z kartą SIM

2. **Sprawdź LED GSM:**
   - Świeci cały czas → Brak połączenia z siecią
   - Zgaszona lub miga → Połączenie OK

3. **Sprawdź kod dostępu:**
   - Upewnij się że używasz prawidłowego kodu (np. `ABCD`)
   - Sprawdź czy nie zmieniłeś kodu wcześniej

4. **Sprawdź format komendy:**
   ```
   ABCD REPORT        # Prawidłowo ✅
   abcd report        # Nieprawidłowo ❌ (małe litery)
   ABCD  REPORT       # Nieprawidłowo ❌ (podwójna spacja)
   ```

**Problem: SMS wysyłają się z opóźnieniem**

- To normalne - operator może opóźniać SMS
- Poczekaj 1-2 minuty
- Sprawdź czy LED SYS miga (5 błysków = wysyła SMS)

---

### 📡 Problemy z zasięgiem GSM

**LED GSM świeci cały czas (brak sieci):**

1. **Sprawdź kartę SIM:**
   - Czy ma wyłączony PIN?
   - Czy ma aktywny abonament/doładowanie?
   - Włóż kartę do telefonu i sprawdź czy działa

2. **Sprawdź antenę:**
   - Czy jest podłączona?
   - Czy nie jest uszkodzona?
   - Spróbuj innej anteny

3. **Sprawdź zasięg:**
   - Sprawdź na telefonie czy jest zasięg w tym miejscu
   - Rozważ zewnętrzną antenę GSM
   - Zmień operatora (inna karta SIM)

**LED GSM miga wolno (słaby zasięg):**

- Rozważ zewnętrzną antenę GSM
- Przenieś urządzenie w inne miejsce
- Sprawdź czy w pobliżu nie ma urządzeń zakłócających

---

### 🔄 Urządzenie się resetuje

**Problem: Urządzenie restartuje się co ~30 sekund**

**Możliwe przyczyny:**

1. **Watchdog (pies stróżujący):**
   - System wykrył zawieszenie i zrestartował urządzenie
   - To mechanizm bezpieczeństwa

2. **Problem z zasilaniem:**
   - Sprawdź napięcie zasilania (powinno być 12V DC)
   - Sprawdź czy zasilacz ma wystarczającą moc (min. 1A)
   - Sprawdź przewody zasilające

3. **Problem z kartą SIM:**
   - Sprawdź czy karta ma wyłączony PIN
   - Sprawdź czy karta jest dobrze osadzona

**Rozwiązanie:**
- Wyłącz zasilanie na 10 sekund
- Włącz ponownie
- Sprawdź LED GSM - powinien zgasnąć po 1-2 minutach
- Jeśli problem się powtarza → skontaktuj się z serwisem

---

### 🚪 Brama otwiera się sama (bez dzwonienia)

**Możliwe przyczyny:**

1. **Przekaźnik zwarty:**
   - Sprawdź podłączenie przekaźnika
   - Sprawdź czy przewody nie są zwarte

2. **Automatyka bramy:**
   - Problem może być w automatyce, nie w sterowniku
   - Odłącz sterownik i sprawdź czy problem znika

3. **Zakłócenia:**
   - Sprawdź czy w pobliżu nie ma urządzeń zakłócających
   - Sprawdź ekranowanie przewodów

---

### 🔑 Zapomniałem kodu dostępu

**Rozwiązanie 1: Reset fabryczny**
```
ABCD XXXX    # Jeśli pamiętasz stary kod
```
⚠️ **Uwaga:** To usuwa WSZYSTKIE numery i ustawienia!

**Rozwiązanie 2: Kontakt z producentem**
- Skontaktuj się z administratorem systemu
- Producent może pomóc w odzyskaniu dostępu

**Zapobieganie:**
- Zapisz kod w bezpiecznym miejscu
- Regularnie sprawdzaj czy pamiętasz kod
- Nie zmieniaj kodu bez zapisania nowego

---

### 🔧 Przekaźnik nie działa

**Diagnoza:**

1. **Sprawdź czy słyszysz kliknięcie:**
   - Zadzwoń na urządzenie
   - Słuchaj czy przekaźnik klika
   - Jeśli klika → problem w podłączeniu do automatyki
   - Jeśli nie klika → problem w sterowniku

2. **Sprawdź podłączenie:**
   - Sprawdź przewody COM i NO
   - Sprawdź czy są dobrze dokręcone
   - Sprawdź czy nie są uszkodzone

3. **Sprawdź automatykę:**
   - Sprawdź czy automatyka działa z przyciskiem manualnym
   - Sprawdź dokumentację automatyki

---

### 💡 LED SYS nie świeci / nie miga

**To normalne!**

LED SYS świeci tylko gdy:
- Wysyła SMS (5 błysków)
- Odbiera SMS lub połączenie (1 mrugnięcie)

Większość czasu LED SYS jest **zgaszona** (tryb czuwania).

---

## Konserwacja i Serwis

### 🔍 Regularna Konserwacja

**Co miesiąc:**
- ✅ Sprawdź czy urządzenie działa (wyślij `ABCD REPORT`)
- ✅ Sprawdź saldo/abonament karty SIM
- ✅ Sprawdź czy LED GSM gaśnie (połączenie z siecią OK)
- ✅ Przetestuj otwarcie bramy (zadzwoń)

**Co 3 miesiące:**
- ✅ Sprawdź podłączenia elektryczne (dokręć śruby)
- ✅ Sprawdź czy urządzenie nie jest zapylone
- ✅ Sprawdź antenę GSM
- ✅ Zrób backup listy numerów

**Co 6 miesięcy:**
- ✅ Zmień kod dostępu (dla bezpieczeństwa)
- ✅ Sprawdź czy wszystkie numery są aktualne
- ✅ Usuń nieaktywne numery

---

### 🔄 Wymiana Karty SIM

**Kiedy wymieniać:**
- Karta SIM jest uszkodzona
- Chcesz zmienić operatora
- Karta wygasła (przedpłacona)

**Jak wymienić:**

1. **Wyłącz zasilanie**
2. Wyjmij starą kartę SIM
3. **Przygotuj nową kartę:**
   - Wyłącz kod PIN
   - Sprawdź czy ma saldo/abonament
   - Zapisz nowy numer telefonu
4. Włóż nową kartę SIM
5. Włącz zasilanie
6. Poczekaj 1-2 minuty (LED GSM powinien zgasnąć)
7. Przetestuj: `ABCD REPORT`

---

### 📞 Kontakt Serwisowy

**Kiedy kontaktować się z serwisem:**
- Urządzenie nie działa po resecie
- Przekaźnik nie klika
- LED GSM świeci cały czas (mimo prawidłowej karty SIM)
- Urządzenie się resetuje ciągle
- Fizyczne uszkodzenie urządzenia

**Dane kontaktowe:**
- **Producent:** Robert Gramsz
- **Website:** www.sonfy.pl
- **Email:** (podaj jeśli dostępny)

**Przed kontaktem przygotuj:**
- Model urządzenia: AC800-DTM-HS-RC3
- Opis problemu
- Co już próbowałeś zrobić
- Wynik komendy `ABCD REPORT` (jeśli działa)

---

## Przykłady Zastosowań

### 🏢 Parking Firmowy

**Scenariusz:**
- Firma z 50 pracownikami
- Parking otwarty 6:00-18:00
- Dyrektor potrzebuje dostępu 24/7

**Konfiguracja:**
```
ABCD TIME 06:00 18:00      # Godziny pracy
ABCD SUB 600111222         # Dyrektor jako Super User
ABCD SKRYBA ON             # Automatyczne dodawanie pracowników
ABCD CLOSE                 # Tryb prywatny
```

**Efekt:**
- Pracownicy mogą wjeżdżać 6:00-18:00
- Dyrektor może wjeżdżać zawsze
- Nowi pracownicy są automatycznie dodawani

---

### 🏘️ Budynek Mieszkalny

**Scenariusz:**
- Blok z 20 mieszkaniami
- Dostęp tylko dla mieszkańców
- Brak godzin ograniczających

**Konfiguracja:**
```
ABCD CLOSE                 # Tryb prywatny
ABCD TIME OFF              # Brak ograniczeń czasowych
ABCD SKRYBA OFF            # Ręczne dodawanie mieszkańców
```

**Dodawanie mieszkańców:**
```
ABCD ADD 600123456         # Mieszkaniec 1
ABCD ADD 600234567         # Mieszkaniec 2
...
```

---

### 🏠 Garaż Prywatny

**Scenariusz:**
- Dom jednorodzinny
- Tylko właściciel i rodzina
- Dostęp 24/7

**Konfiguracja:**
```
ABCD CLOSE                 # Tryb prywatny
ABCD TIME OFF              # Brak ograniczeń
ABCD ADD 600111222         # Właściciel
ABCD ADD 600222333         # Żona
ABCD ADD 600333444         # Syn
```

---

### 🚧 Brama Wjazdowa - Budowa

**Scenariusz:**
- Plac budowy
- Różne firmy wjeżdżają
- Tymczasowy dostęp publiczny

**Konfiguracja:**
```
ABCD OPEN                  # Tryb publiczny - wszyscy mogą wjeżdżać
ABCD TIME 07:00 17:00      # Tylko w godzinach pracy
```

**Po zakończeniu budowy:**
```
ABCD CLOSE                 # Zmień na tryb prywatny
ABCD TIME OFF              # Wyłącz ograniczenia czasowe
```

---

### 🅿️ Parking Publiczny z Opłatami

**Scenariusz:**
- Parking płatny
- Abonenci mają bezpłatny wjazd
- Inni płacą przy wjeździe

**Konfiguracja:**
```
ABCD OPEN DTMF             # Tryb publiczny z DTMF
ABCD TIME OFF              # Dostęp 24/7
```

**Jak działa:**
- Abonenci: dodani do listy, automatyczne otwarcie (CLIP)
- Inni: dzwonią, wciskają "1", płacą przy wjeździe

```
ABCD ADD 600111222         # Abonent 1
ABCD ADD 600222333         # Abonent 2
```

---

## Wsparcie

**Producent:** Robert Gramsz  
**Website:** www.sonfy.pl  
**System:** AC800-DTM-HS-RC3

---

**Koniec instrukcji**

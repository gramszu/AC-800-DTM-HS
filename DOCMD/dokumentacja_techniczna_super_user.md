# Dokumentacja Techniczna: Funkcja Super User

## Wersja: AC800-DTM-HS-RC3
**Data:** 2025-12-11  
**Autor:** Robert Gramsz

---

## 1. Przegląd Funkcjonalności

Funkcja **Super User** pozwala na rezerwację pozycji 795-800 (6 miejsc) dla użytkowników z rozszerzonymi uprawnieniami. Super Userzy mogą:

- Omijać blokadę systemu (`ABCD STOP`)
- Omijać blokadę czasową (`ABCD TIME`)
- Działać w trybie CLIP (automatyczne otwarcie) i DTMF (odbieranie + klawisz "1")

---

## 2. Implementacja Krok po Kroku

### 2.1. Rezerwacja Pozycji w EEPROM

**Plik:** `main.c`

**Zmienne globalne:**
```c
uint skryba_limit = 795; // Limit użytkowników dla Skryby (795 max, pozycje 796-800 dla Super Userów)
```

**Pozycje:**
- Zwykli użytkownicy: 1-795 (indeksy C: 0-794)
- Super Userzy: 795-800 (indeksy C: 794-799)

### 2.2. Funkcja Sprawdzania Super Usera

**Plik:** `main.c` (około linii 260-270)

```c
// Funkcja pomocnicza: sprawdza czy numer jest Super Userem (pozycje 794-799)
uchar czy_numer_jest_super_userem(const uchar *numer_telefonu) {
  uchar bufor_lokalny[LICZBA_BAJTOW_NUMERU_TELEFONU_W_EEPROM];
  
  // Konwertuj numer do formatu EEPROM
  konwertuj_telefon_na_blok_eeprom(
      numer_telefonu,
      numer_telefonu + strlen((char *)numer_telefonu),
      bufor_lokalny);
  
  // Sprawdź pozycje 794-799 (user-facing 795-800)
  for (uint nr_uzyt = 794; nr_uzyt < MAX_LICZBA_NUMEROW_TELEFONOW_BRAMA; ++nr_uzyt) {
    if (porownaj_numer_telefonu_blok(
            bufor_lokalny,
            (void *)EEPROM_NUMER_TELEFONU_BRAMA(nr_uzyt))) {
      return TRUE;
    }
  }
  return FALSE;
}
```

### 2.3. Omijanie Blokad w Funkcji Sprawdzania Połączeń

**Plik:** `main.c` (funkcja `sprawdz_przychodzaca_rozmowe`)

**Przed sprawdzeniem blokad dodaj:**
```c
// Sprawdź czy dzwoniący jest Super Userem
uchar jest_super_user = czy_numer_jest_super_userem(numer_telefonu_ktory_dzwoni);

// Super Userzy omijają blokady systemu i czasowe
if (blokada_systemu && !jest_super_user) {
  return FALSE; // Ignoruj rozmowy gdy system zablokowany
}

if (blokada_sterowania_czasowa && !jest_super_user) {
  return FALSE; // Ignoruj rozmowy gdy blokada czasowa
}
```

### 2.4. Ograniczenie Skryby do Pozycji 1-795

**Plik:** `main.c` (handler `KOMENDA_KOLEJKI_DODAJ_UZYTKOWNIKA_BRAMA`)

```c
// Skryba: dodawaj tylko do pozycji 0-794 (user-facing 1-795)
// Pozycje 795-800 (indeksy 794-799) są zarezerwowane dla Super Userów
uint max_pozycja = (skryba_limit < 795) ? skryba_limit : 795;
for (uint nr_uzyt_clip = 0; nr_uzyt_clip < max_pozycja; ++nr_uzyt_clip) {
  if (not czy_aktywny_numer_telefonu_brama(nr_uzyt_clip)) {
    // Dodaj numer
    zapisz_znaki_w_eeprom_bez_kopiowania(
        EEPROM_NUMER_TELEFONU_BRAMA(nr_uzyt_clip),
        LICZBA_BAJTOW_NUMERU_TELEFONU_W_EEPROM);
    dodano = TRUE;
    break;
  }
}
```

### 2.5. Komenda SMS: ABCD SUB

#### 2.5.1. Dodanie Komendy do Parsera

**Plik:** `interpretacjaSMS.c`

**Aktualizacja liczby instrukcji:**
```c
#define LICZBA_INSTRUKCJI_SMS 17 // Zwiększone do 17
```

**Dodanie do tablicy instrukcji:**
```c
static const uchar instrukcja_sms[][MAX_LICZBA_ZNAKOW_INSTRUKCJI_SMS] PROGMEM = {
    // ... inne komendy ...
    "\x03"
    "SUB", // SUB numer (dodaj do pozycji 795-800)
};
```

**Dodanie do enum:**
```c
enum {
  INSTRUKCJA_CODE,
  INSTRUKCJA_ADD,
  // ... inne instrukcje ...
  INSTRUKCJA_STOP,
  INSTRUKCJA_SUB,  // NOWA INSTRUKCJA
};
```

**Rozszerzenie zakresu parsowania:**
```c
switch (
    interpretuj_instrukcje_sms(&sms, INSTRUKCJA_CODE, INSTRUKCJA_SUB + 1)) {
    // WAŻNE: INSTRUKCJA_SUB + 1, nie INSTRUKCJA_STOP + 1!
```

**Handler komendy SUB:**
```c
case INSTRUKCJA_SUB: {
  if (not pobierz_numer_telefonu(&sms, &numer_telefonu_do_ktorego_dzwonic[0], 14))
    return INTERPRETACJA_SMS_BLEDNE_DANE;
  dodaj_komende(KOMENDA_KOLEJKI_DODAJ_SUPER_USERA);
  return INTERPRETACJA_SMS_POPRAWNY;
}
```

#### 2.5.2. Dodanie Komendy do Kolejki

**Plik:** `enumkomendy.h`

```c
enum komenda_typ {
  // ... inne komendy ...
  KOMENDA_KOLEJKI_DODAJ_SUPER_USERA,
  // ...
};
```

#### 2.5.3. Handler Komendy w Głównej Pętli

**Plik:** `main.c` (główna pętla `main()`)

**WAŻNE: Użyj lokalnego bufora aby uniknąć korupcji przez `czy_numer_istnieje`!**

```c
case KOMENDA_KOLEJKI_DODAJ_SUPER_USERA: {
  JESLI_EEPROM_ZAJETY_WYKONAJ_POZNIEJ();

  // Use a LOCAL buffer to avoid corruption by czy_numer_istnieje
  uchar bufor_super[LICZBA_BAJTOW_NUMERU_TELEFONU_W_EEPROM];

  // Convert number to EEPROM format FIRST, before duplicate check
  konwertuj_telefon_na_blok_eeprom(
      &numer_telefonu_do_ktorego_dzwonic[0],
      &numer_telefonu_do_ktorego_dzwonic[strlen(
          (char *)numer_telefonu_do_ktorego_dzwonic)],
      bufor_super);

  // Check for duplicates
  if (czy_numer_istnieje(numer_telefonu_do_ktorego_dzwonic)) {
    strcpy((char *)numer_telefonu_wysylanego_smsa,
           (char *)numer_telefonu_odebranego_smsa);
    strcpy_P((char *)tekst_wysylanego_smsa,
             PSTR("Numer juz istnieje w systemie"));
    dodaj_komende(KOMENDA_KOLEJKI_WYSLIJ_SMSA_TEXT);
    return TRUE;
  }

  // Copy our safe buffer to bufor_eeprom for writing
  memcpy(bufor_eeprom, bufor_super, LICZBA_BAJTOW_NUMERU_TELEFONU_W_EEPROM);

  // Szukaj pierwszej wolnej pozycji w zakresie 794-799 (user-facing 795-800)
  uchar dodano = FALSE;
  uint pozycja_dodana = 0;
  for (uint nr_uzyt = 794; nr_uzyt < MAX_LICZBA_NUMEROW_TELEFONOW_BRAMA;
       ++nr_uzyt) {
    if (not czy_aktywny_numer_telefonu_brama(nr_uzyt)) {
      zapisz_znaki_w_eeprom_bez_kopiowania(
          EEPROM_NUMER_TELEFONU_BRAMA(nr_uzyt),
          LICZBA_BAJTOW_NUMERU_TELEFONU_W_EEPROM);
      dodano = TRUE;
      pozycja_dodana = nr_uzyt + 1; // User-facing (1-indexed)
      break;
    }
  }

  // Wyslij odpowiedz
  strcpy((char *)numer_telefonu_wysylanego_smsa,
         (char *)numer_telefonu_odebranego_smsa);
  if (dodano) {
    sprintf((char *)tekst_wysylanego_smsa, "Super User dodany na pozycji %u",
            pozycja_dodana);
  } else {
    strcpy_P((char *)tekst_wysylanego_smsa,
             PSTR("Brak wolnych pozycji Super User (795-800)"));
  }
  dodaj_komende(KOMENDA_KOLEJKI_WYSLIJ_SMSA_TEXT);

  return TRUE;
}
```

---

## 3. Aktualizacja Python GUI

**Plik:** `instalacja/AC800-DTM-HS.py`

**Zmień domyślny limit Skryby:**
```python
self.skryba_limit_var = tk.IntVar(value=795)  # Zmienione z 800 na 795
```

**Aktualizuj walidację:**
```python
def validate_skryba_limit(self, new_value: str) -> bool:
    """Walidacja dla limitu Skryba (1-795)."""
    if new_value == "":
        return True
    if not new_value.isdigit():
        return False
    val = int(new_value)
    return 1 <= val <= 795  # Zmienione z 800 na 795
```

**Aktualizuj odczyt z EEPROM:**
```python
if limit_l == 0xFF and limit_h == 0xFF:
    # Nie ustawiono - domyślnie 795 (pozycje 796-800 dla Super Userów)
    self.skryba_limit_var.set(795)
else:
    limit_value = limit_l | (limit_h << 8)
    # Walidacja zakresu (max 795, pozycje 796-800 dla Super Userów)
    if 1 <= limit_value <= 795:
        self.skryba_limit_var.set(limit_value)
    else:
        self.skryba_limit_var.set(795)
```

---

## 4. Raport SMS (Opcjonalnie)

**Plik:** `main.c` (funkcja `generuj_raport_stanu_urzadzenia`)

**Dodaj status Skryby (bez limitu):**
```c
// Skryba status (ON/OFF) - bez wyświetlania limitu
if (skryba_wlaczona) {
  strcpy_P((char *)sms, PSTR("Skryba: Wlaczona"));
} else {
  strcpy_P((char *)sms, PSTR("Skryba: Wylaczona"));
}
sms += strlen((char *)sms);
*sms++ = '\n';
```

---

## 5. Najczęstsze Błędy i Rozwiązania

### Problem 1: Komenda SUB nie działa
**Przyczyna:** Zakres parsowania nie obejmuje INSTRUKCJA_SUB  
**Rozwiązanie:** Zmień `INSTRUKCJA_STOP + 1` na `INSTRUKCJA_SUB + 1` w `interpretuj_wiadomosc_sms`

### Problem 2: Numer nie jest dodawany (brak SMS)
**Przyczyna:** `czy_numer_istnieje()` korumpuje `bufor_eeprom`  
**Rozwiązanie:** Użyj lokalnego bufora `bufor_super[]` przed sprawdzeniem duplikatów

### Problem 3: Skryba nadpisuje Super Userów
**Przyczyna:** `skryba_limit` ustawiony na 800  
**Rozwiązanie:** Zmień na 795 i ogranicz pętlę Skryby do `max_pozycja = 795`

### Problem 4: Super User nie omija blokad
**Przyczyna:** Brak sprawdzenia `jest_super_user` przed blokami  
**Rozwiązanie:** Dodaj `&& !jest_super_user` do warunków blokad

---

## 6. Testowanie

### Test 1: Dodawanie Super Usera
```
ABCD SUB 793557357
```
Oczekiwana odpowiedź: `Super User dodany na pozycji 795`

### Test 2: Sprawdzenie duplikatu
```
ABCD SUB 793557357  (ponownie)
```
Oczekiwana odpowiedź: `Numer juz istnieje w systemie`

### Test 3: Omijanie STOP
```
ABCD STOP
ABCD REPORT  (sprawdź status: Zablokowany)
```
Zadzwoń z numeru Super Usera → powinno otworzyć bramę  
Zadzwoń z numeru zwykłego → nie powinno otworzyć

### Test 4: Omijanie TIME
```
ABCD TIME 08:00 16:00
```
Zadzwoń z numeru Super Usera poza godzinami → powinno otworzyć  
Zadzwoń z numeru zwykłego poza godzinami → nie powinno otworzyć

### Test 5: Usuwanie Super Usera
```
ABCD DEL 793557357
ABCD REPORT  (sprawdź czy liczba użytkowników się zmniejszyła)
```

---

## 7. Pliki Zmodyfikowane

- `main.c` - główna logika, funkcje, handlery
- `interpretacjaSMS.c` - parsowanie komendy SUB
- `enumkomendy.h` - definicja KOMENDA_KOLEJKI_DODAJ_SUPER_USERA
- `instalacja/AC800-DTM-HS.py` - GUI, limit Skryby
- `Makefile` - nazwa projektu AC800-DTM-HS-RC3

---

## 8. Rozmiar Firmware

**Przed:** 25506 bajtów  
**Po:** 25946 bajtów  
**Wzrost:** +440 bajtów (funkcja Super User + komenda SUB + raport Skryba)

---

## 9. Kompatybilność Wsteczna

- ✅ Wszystkie istniejące komendy działają bez zmian
- ✅ Numery na pozycjach 1-795 działają normalnie
- ✅ Skryba działa poprawnie (ograniczona do 1-795)
- ✅ Python GUI kompatybilny z nowym firmware

---

## 10. Licencja i Kontakt

**Autor:** Robert Gramsz  
**Projekt:** AC800-DTM-HS  
**Wersja:** RC3  
**Data:** 2025-12-11  
**Website:** www.sonfy.pl

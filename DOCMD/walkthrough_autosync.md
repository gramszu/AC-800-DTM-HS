# Automatyczna Synchronizacja Czasu Po Restarcie

## Przegląd

Zaimplementowano mechanizm automatycznej synchronizacji czasu, który rozwiązuje problem utraty czasu po restarcie urządzenia (np. po zaniku zasilania).

## Jak To Działa

### 1. Ustawienie Własnego Numeru

Użytkownik musi najpierw ustawić swój numer telefonu przez komendę SMS:

```
ABCD MYNUM 123456789
```

**Odpowiedź:**
```
Numer zapisany: 123456789
```

**Sprawdzenie zapisanego numeru:**

Wyślij komendę `ABCD REPORT` aby zobaczyć zapisany numer:

```
*
AC800-DTM-TS
Czas: 09:50:39
GSM: 87%
Uzyt: 5/795
Status: Aktywny
Tryb: Publiczny CLIP
Harm: Wylaczony
Skryba: Wylaczona
Moj nr: 123456789
www.sonfy.pl
```

Jeśli numer nie został zapisany, raport pokaże:
```
Moj nr: ----
```

**Limit długości:** Raport mieści się w limicie 159 znaków SMS (maksymalnie 157 znaków z pełnym 9-cyfrowym numerem).

**Ważne:**
- Numer musi mieć 3-9 cyfr
- Numer jest zapisywany w EEPROM (adres 4040)
- Można również ustawić numer przez aplikację GUI Python

### 2. Wykrywanie Nieprawidłowego Czasu

Po restarcie urządzenia, system sprawdza czy czas jest nieprawidłowy (`00:00:xx`):

```c
if (rtc_czas[0] == '0' && rtc_czas[1] == '0' && 
    rtc_czas[3] == '0' && rtc_czas[4] == '0')
```

Jeśli czas jest nieprawidłowy **i** mamy zapisany numer własny:
- Ustawia flagę `autosync_czas_aktywny = TRUE`

### 3. Automatyczne Wysyłanie SMS

Gdy urządzenie zaloguje się do sieci GSM, automatycznie wysyła SMS do siebie:

**Treść SMS:** `"Synchronizacja Czasu"`

**Fallback:** Jeśli SMS nie może zostać wysłany (np. brak numeru), system normalnie pracuje i czeka na dowolny przychodzący SMS.

### 4. Synchronizacja Czasu

Gdy urządzenie odbierze SMS (własny lub dowolny inny):
- Odczytuje timestamp z SMS-a (z sieci GSM)
- Aktualizuje RTC w module SIM900
- Aktualizuje zmienną `rtc_czas`
- Wyłącza auto-sync: `autosync_czas_aktywny = FALSE`

---

## Zmiany W Kodzie

### Nowe Pliki/Sekcje

#### [`adresyeeprom.h`](file:///Users/gramsz/Desktop/AC-800-DTM-HARMO/uc/adresyeeprom.h#L59-L60)

```c
// Numer własny urządzenia (dla auto-sync czasu)
#define ADRES_EEPROM_MOJE_NUMER_START 4040 // 10 bajtów na numer
```

#### [`main.c`](file:///Users/gramsz/Desktop/AC-800-DTM-HARMO/uc/main.c#L122-L124) - Zmienne Globalne

```c
// Auto-sync czasu po restarcie
uchar autosync_czas_aktywny = FALSE;
uchar moj_numer_telefonu[MAX_LICZBA_ZNAKOW_TELEFON + 1];
```

#### [`main.c`](file:///Users/gramsz/Desktop/AC-800-DTM-HARMO/uc/main.c#L1832-L1847) - Inicjalizacja

```c
// Auto-sync czasu: Odczytaj numer własny z EEPROM
eeprom_read_block(moj_numer_telefonu, (const void *)ADRES_EEPROM_MOJE_NUMER_START, 
                  MAX_LICZBA_ZNAKOW_TELEFON + 1);
moj_numer_telefonu[MAX_LICZBA_ZNAKOW_TELEFON] = 0;

// Sprawdź czy czas jest nieprawidłowy (00:00:xx) i czy mamy zapisany numer
if (rtc_czas[0] == '0' && rtc_czas[1] == '0' && 
    rtc_czas[3] == '0' && rtc_czas[4] == '0' &&
    moj_numer_telefonu[0] != 0xFF && moj_numer_telefonu[0] != 0) {
  autosync_czas_aktywny = TRUE;
}
```

#### [`main.c`](file:///Users/gramsz/Desktop/AC-800-DTM-HARMO/uc/main.c#L1514-L1539) - Wysyłanie SMS

```c
// Auto-sync czasu: Wyślij SMS do siebie jeśli aktywny i zalogowany w sieci
static uchar autosync_sms_wyslany = FALSE;
if (autosync_czas_aktywny && !autosync_sms_wyslany && modul_zalogowany_w_sieci) {
  if (moj_numer_telefonu[0] != 0xFF && moj_numer_telefonu[0] != 0 && 
      !flaga_wysylanie_smsa) {
    // Wyślij SMS do siebie
    strcpy((char *)numer_telefonu_wysylanego_smsa, (char *)moj_numer_telefonu);
    strcpy_P((char *)tekst_wysylanego_smsa, PSTR("Synchronizacja Czasu"));
    dodaj_komende(KOMENDA_KOLEJKI_WYSLIJ_SMSA_TEXT);
    autosync_sms_wyslany = TRUE;
  } else {
    // Brak numeru - czekamy na przychodzący SMS
    autosync_sms_wyslany = TRUE;
  }
}
```

#### [`main.c`](file:///Users/gramsz/Desktop/AC-800-DTM-HARMO/uc/main.c#L430-L433) - Wyłączanie Auto-Sync

```c
// Auto-sync: Wyłącz po pierwszej synchronizacji czasu
if (autosync_czas_aktywny) {
  autosync_czas_aktywny = FALSE;
}
```

#### [`interpretacjaSMS.c`](file:///Users/gramsz/Desktop/AC-800-DTM-HARMO/uc/interpretacjaSMS.c#L535-L564) - Komenda MYNUM

```c
case INSTRUKCJA_MYNUM: {
  // MYNUM 123456789 - zapisz własny numer telefonu
  uchar temp_numer[MAX_LICZBA_ZNAKOW_TELEFON + 1];
  if (not pobierz_numer_telefonu(&sms, temp_numer, MAX_LICZBA_ZNAKOW_TELEFON + 1))
    return INTERPRETACJA_SMS_BLEDNE_DANE;
  
  // Walidacja: numer musi mieć 3-9 cyfr
  uchar len = strlen((char *)temp_numer);
  if (len < 3 || len > 9)
    return INTERPRETACJA_SMS_BLEDNE_DANE;
  
  // Zapisz do EEPROM i RAM
  zapisz_znaki_w_eeprom(temp_numer, ADRES_EEPROM_MOJE_NUMER_START, len + 1);
  strcpy((char *)moj_numer_telefonu, (char *)temp_numer);
  
  // Wyślij potwierdzenie
  strcpy((char *)numer_telefonu_wysylanego_smsa, (char *)numer_telefonu_odebranego_smsa);
  strcpy_P((char *)tekst_wysylanego_smsa, PSTR("Numer zapisany: "));
  strcat((char *)tekst_wysylanego_smsa, (char *)temp_numer);
  dodaj_komende(KOMENDA_KOLEJKI_WYSLIJ_SMSA_TEXT);
  
  return INTERPRETACJA_SMS_POPRAWNY;
}
```

---

## Scenariusze Użycia

### Scenariusz 1: Pierwsze Uruchomienie

1. Użytkownik wysyła: `ABCD MYNUM 600123456`
2. Urządzenie odpowiada: `Numer zapisany: 600123456`
3. Numer jest zapisany w EEPROM

### Scenariusz 2: Restart Z Utratą Czasu

1. Urządzenie restartuje się (zanik zasilania)
2. RTC pokazuje `00:00:00`
3. System wykrywa nieprawidłowy czas
4. Ustawia `autosync_czas_aktywny = TRUE`
5. Czeka na zalogowanie do sieci GSM
6. Wysyła SMS do siebie: `"Synchronizacja Czasu"`
7. Odbiera własny SMS z timestampem (np. `09:50:39`)
8. Synchronizuje czas z timestampu
9. Wyłącza auto-sync
10. System działa normalnie

### Scenariusz 3: Brak Zapisanego Numeru

1. Urządzenie restartuje się
2. RTC pokazuje `00:00:00`
3. System wykrywa brak zapisanego numeru
4. **Nie** wysyła SMS do siebie
5. Czeka na dowolny przychodzący SMS
6. Synchronizuje czas z pierwszego SMS-a
7. System działa normalnie

---

## Testy

### Test Kompilacji

```bash
cd uc && make clean && make
```

**Wynik:** ✅ Kompilacja zakończona sukcesem

**Rozmiar firmware:**
- `.text`: 26418 bajtów (kod programu)
- `.data`: 224 bajty
- `.bss`: 1606 bajtów (zmienne)

### Testy Manualne (Do Wykonania)

1. **Test komendy MYNUM:**
   - Wyślij: `ABCD MYNUM 600123456`
   - Sprawdź odpowiedź: `Numer zapisany: 600123456`

2. **Test auto-sync:**
   - Zresetuj urządzenie (odłącz zasilanie)
   - Poczekaj na zalogowanie do sieci
   - Sprawdź czy urządzenie wysłało SMS do siebie
   - Wyślij `ABCD SET` aby sprawdzić czy czas został zsynchronizowany

3. **Test fallback:**
   - Wyczyść numer własny (ustaw na `0xFF` w EEPROM)
   - Zresetuj urządzenie
   - Wyślij dowolny SMS (np. `ABCD REPORT`)
   - Sprawdź czy czas został zsynchronizowany

---

## Podsumowanie

- Testy manualne na urządzeniu
- Dokumentacja użytkownika w `instrukcja_obslugi_aplikacji.md`

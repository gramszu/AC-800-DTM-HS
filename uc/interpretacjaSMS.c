#ifndef INCLUDE

#include "interpretacjaSMS.h"
#include "ctype.h"
#include "komendy.h"
#include <avr/io.h>
#include <avr/pgmspace.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "adresyeeprom.h" // Ensure this is included for address definitions
#include "konfiguracja_eeprom.h"
#include "wewy.h"
#include "zapiseeprom.h"

extern uchar skryba_wlaczona; // Declared in main.c
extern uint skryba_limit;     // Declared in main.c
extern uchar tryb_clip;       // Declared in main.c

uchar nr_usunietego_uzytkownika_z_smsa;

#endif

#define przeskocz_biale_znaki(BUF)                                             \
  while (isspace(*BUF))                                                        \
  ++BUF

uchar sprawdz_kod(const uchar **buf_sms) {
  przeskocz_biale_znaki(*buf_sms);
  if ((*buf_sms)[0] == kod_modulu[0] && (*buf_sms)[1] == kod_modulu[1] &&
      (*buf_sms)[2] == kod_modulu[2] && (*buf_sms)[3] == kod_modulu[3]) {
    *buf_sms += LICZBA_BAJTOW_KODU_DOSTEPU;
    return TRUE;
  } else
    return FALSE;
}

uchar sprawdz_reset_ustawien(const uchar *buf) {
  static const char res_ust[] PROGMEM =
      INSTRUKCJA_SMS_RESET_WSZYSTKICH_USTAWIEN;
  return memcmp_R(buf, res_ust) == 0;
}

#define LICZBA_INSTRUKCJI_SMS 17 // Increased to 17
#define MAX_LICZBA_ZNAKOW_INSTRUKCJI_SMS 8
// uwaga: wana jest kolejno oraz usytuowanie pomidzy nimi
static const uchar
    instrukcja_sms[LICZBA_INSTRUKCJI_SMS]
                  [MAX_LICZBA_ZNAKOW_INSTRUKCJI_SMS] PROGMEM = {
                      // przed kad instrukcj musi by kod, litery
                      // mog by due lub mae
                      "\x04"
                      "CODE", // CODE EFGH (zmiana kodu dostpu)
                      "\x03"
                      "ADD", //
                      "\x03"
                      "DEL", //
                      "\x04"
                      "XXXX", // RESET
                      "\x06"
                      "REPORT", // REPORT
                      "\x04"
                      "USER", // USER
                      "\x04"
                      "OPEN", // OPEN
                      "\x05"
                      "CLOSE", // CLOSE
                      "\x04"
                      "CLIP", // CLIP (sub-command)
                      "\x04"
                      "DTMF", // DTMF (sub-command)
                      "\x03"
                      "SET", // SET HH:MM:SS
                      "\x04"
                      "TIME", // TIME HH:MM HH:MM lub TIME OFF
                      "\x06"
                      "SKRYBA", // SKRYBA ON/OFF
                      "\x05"
                      "DEBUG", // DEBUG (diagnostyka SKRYBA)
                      "\x05"
                      "START", // START (odblokuj)
                      "\x04"
                      "STOP", // STOP (zablokuj)
                      "\x03"
                      "SUB", // SUB numer (dodaj do pozycji 795-800)
};

enum {
  INSTRUKCJA_CODE, // code EFGH [K]
  INSTRUKCJA_ADD,
  INSTRUKCJA_DEL,
  INSTRUKCJA_RESET,
  INSTRUKCJA_REPORT, // report
  INSTRUKCJA_USER, // user +48505691117 E C B R [K] // user del +48505691117 [K]
  INSTRUKCJA_OPEN,
  INSTRUKCJA_CLOSE,
  INSTRUKCJA_CLIP,
  INSTRUKCJA_DTMF,
  INSTRUKCJA_SET,
  INSTRUKCJA_TIME,
  INSTRUKCJA_SKRYBA,
  INSTRUKCJA_DEBUG,
  INSTRUKCJA_START,
  INSTRUKCJA_STOP,
  INSTRUKCJA_SUB,
};

uchar interpretuj_instrukcje_sms(const uchar **buf_sms, const uchar start,
                                 const uchar end) {
  przeskocz_biale_znaki(*buf_sms);
  uchar i;
  for (i = start; i < end; ++i) {
    const void *p =
        &instrukcja_sms[0][0] + i * MAX_LICZBA_ZNAKOW_INSTRUKCJI_SMS;
    const uchar l = pgm_read_byte(p);
    if (memcmp_P(*buf_sms, p + 1, l) == 0) {
      *buf_sms += l;
      return i;
    }
  }
  return i;
}

uchar pobierz_long(const uchar **buf_sms, long *wartosc) {
  const uchar *buf_sms_pom = *buf_sms;
  *wartosc = strtol(*buf_sms, (char **)buf_sms, 10);
  return *buf_sms != buf_sms_pom;
}

uchar pomin_znak(const uchar **buf_sms, const uchar wartosc) {
  przeskocz_biale_znaki(*buf_sms);
  if (**buf_sms == toupper(wartosc)) {
    ++*buf_sms;
    return TRUE;
  } else
    return FALSE;
}

uchar czy_jest_znak(const uchar **buf_sms, const uchar wartosc) {
  przeskocz_biale_znaki(*buf_sms);
  const uchar *buf_sms_pom = *buf_sms;
  const uchar w = toupper(wartosc);
  uchar ch;
  while ((ch = *buf_sms_pom++) != '\0' && ch != w)
    ;
  if (ch == w) {
    *buf_sms = buf_sms_pom;
    return TRUE;
  } else
    return FALSE;
}

void pobierz_wyraz(const uchar **buf_sms, uchar *buf, uchar max_liczba_znakow) {
  przeskocz_biale_znaki(*buf_sms);
  while (max_liczba_znakow-- && !isspace(**buf_sms) &&
         (*buf = **buf_sms) != '\0') {
    buf++;
    (*buf_sms)++;
  }
  *buf = '\0';
}

uchar pobierz_numer_telefonu(const uchar **buf_sms, uchar *buf_telefon,
                             const uchar rozmiar_bufora) {
  przeskocz_biale_znaki(*buf_sms);
  const uchar *tel = *buf_sms;
  uchar *buf = buf_telefon;
  uchar l = 0;
  while (konwersja_znaku_telefonu(*tel) != ZNAK_NUMERU_TELEFONU_NIEZNANY &&
         ++l < rozmiar_bufora)
    *buf++ = *tel++;
  *buf = '\0';
  if (buf_telefon[0] != '\0') {
    *buf_sms = tel;
    return TRUE;
  } else
    return FALSE;
}

uchar interpretuj_wiadomosc_sms(const uchar *sms) {
  memcpy(bufor_eeprom, sms, MAX_BUFOR_EEPROM);
  const uchar *sms_pom = sms;
  if (!sprawdz_kod(&sms)) {
    if (sprawdz_reset_ustawien(sms))
      return INTERPRETACJA_SMS_RESET_WSZYSTKICH_USTAWIEN;
    return INTERPRETACJA_SMS_BRAK_KODU;
  }
  { // mona wstawi ten kod do kolejki i w nastpnym kroku interpretowa
    for (uchar *ptr = (uchar *)sms; *ptr != '\0'; ++ptr)
      *ptr = toupper(*ptr);
  }

  switch (
      interpretuj_instrukcje_sms(&sms, INSTRUKCJA_CODE, INSTRUKCJA_SUB + 1)) {
  case INSTRUKCJA_CODE: {
    przeskocz_biale_znaki(sms);
    for (uchar i = 0; i < LICZBA_BAJTOW_KODU_DOSTEPU; ++i) {
      const uchar znak = bufor_eeprom[(sms - sms_pom) + i];
      if (not((znak >= 'A' && znak <= 'Z') || (znak >= '0' && znak <= '9')))
        return INTERPRETACJA_SMS_BLEDNE_DANE;
    }
    memcpy(kod_modulu, bufor_eeprom + (sms - sms_pom),
           LICZBA_BAJTOW_KODU_DOSTEPU);
    zapisz_znaki_w_eeprom(bufor_eeprom + (sms - sms_pom),
                          (uint)ADRES_EEPROM_KOD_DOSTEPU,
                          LICZBA_BAJTOW_KODU_DOSTEPU);
    return INTERPRETACJA_SMS_POPRAWNY;
  }
  case INSTRUKCJA_REPORT: {
    return INTERPRETACJA_SMS_RAPORT;
  }
  case INSTRUKCJA_USER: {
    // Komenda USER ma działać wyłącznie z podanym numerem.
    // Przykład: USER +48505691117 E C B R [K]
    if (pobierz_numer_telefonu(&sms, &numer_telefonu_do_ktorego_dzwonic[0], 14))
      return INTERPRETACJA_SMS_USER;

    // Brak numeru po "USER" – wyślij informację z instrukcją użycia,
    // zamiast pełnej listy użytkowników.
    return INTERPRETACJA_SMS_USER_BEZ_NUMERU;
  }
  case INSTRUKCJA_ADD: {
    if (not pobierz_numer_telefonu(&sms, &numer_telefonu_do_ktorego_dzwonic[0],
                                   14))
      return INTERPRETACJA_SMS_BLEDNE_DANE;
    dodaj_komende(KOMENDA_KOLEJKI_DODAJ_UZYTKOWNIKA_BRAMA);
    return INTERPRETACJA_SMS_POPRAWNY;
  }
  case INSTRUKCJA_DEL: {
    if (not pobierz_numer_telefonu(&sms, &numer_telefonu_do_ktorego_dzwonic[0],
                                   14))
      return INTERPRETACJA_SMS_BLEDNE_DANE;
    dodaj_komende(KOMENDA_KOLEJKI_USUN_UZYTKOWNIKA_BRAMA);
    return INTERPRETACJA_SMS_POPRAWNY;
  }
  case INSTRUKCJA_RESET: {
    return INTERPRETACJA_SMS_RESET_WSZYSTKICH_USTAWIEN;
  }
  case INSTRUKCJA_OPEN: {
    const uchar podtryb =
        interpretuj_instrukcje_sms(&sms, INSTRUKCJA_CLIP, INSTRUKCJA_DTMF + 1);
    if (podtryb == INSTRUKCJA_CLIP) {
      tryb_pracy = 1; // Publiczny
      zapisz_znak_w_eeprom(1, ADRES_EEPROM_TRYB_PRACY);

      tryb_clip = TRUE;
      zapisz_znak_w_eeprom(1, ADRES_EEPROM_TRYB_CLIP_DTMF);
      return INTERPRETACJA_SMS_POPRAWNY;
    } else if (podtryb == INSTRUKCJA_DTMF) {
      tryb_pracy = 1; // Publiczny
      zapisz_znak_w_eeprom(1, ADRES_EEPROM_TRYB_PRACY);

      tryb_clip = FALSE; // DTMF
      zapisz_znak_w_eeprom(0, ADRES_EEPROM_TRYB_CLIP_DTMF);
      return INTERPRETACJA_SMS_POPRAWNY;
    } else {
      // Domyślne zachowanie (stare OPEN): Tylko tryb publiczny, nie zmieniaj
      // sub-trybu (chyba ze wymusimy CLIP?) Dla kompatybilnosci wstecznej OPEN
      // = OPEN CLIP Lub zostawiamy stary sub-tryb? AC200 wymusza CLIP przy
      // samym OPEN? Nie, AC200 zwraca BLEDNE_DANE jesli brak podtrybu! Ale my
      // chcemy kompatybilnosc. Zrobmy tak: OPEN bez parametru = OPEN (zachowaj
      // obecny podtryb) + Publiczny

      // Jednak w AC200 kod:
      // if ( podtryb == INSTRUKCJA_CLIP ) ...
      // else if ( podtryb == INSTRUKCJA_DTMF ) ...
      // else return INTERPRETACJA_SMS_BLEDNE_DANE;

      // Decyzja: Zachowujemy kompatybilnosc wsteczna.
      // Jesli brak parametru -> tylko zmien tryb_pracy na 1.
      tryb_pracy = 1; // Publiczny
      zapisz_znak_w_eeprom(1, ADRES_EEPROM_TRYB_PRACY);
      return INTERPRETACJA_SMS_POPRAWNY;
    }
  }
  case INSTRUKCJA_CLOSE: {
    const uchar podtryb =
        interpretuj_instrukcje_sms(&sms, INSTRUKCJA_CLIP, INSTRUKCJA_DTMF + 1);
    if (podtryb == INSTRUKCJA_CLIP) {
      tryb_pracy = 0; // Prywatny
      zapisz_znak_w_eeprom(0, ADRES_EEPROM_TRYB_PRACY);

      tryb_clip = TRUE;
      zapisz_znak_w_eeprom(1, ADRES_EEPROM_TRYB_CLIP_DTMF);
      return INTERPRETACJA_SMS_POPRAWNY;
    } else if (podtryb == INSTRUKCJA_DTMF) {
      tryb_pracy = 0; // Prywatny
      zapisz_znak_w_eeprom(0, ADRES_EEPROM_TRYB_PRACY);

      tryb_clip = FALSE; // DTMF
      zapisz_znak_w_eeprom(0, ADRES_EEPROM_TRYB_CLIP_DTMF);
      return INTERPRETACJA_SMS_POPRAWNY;
    } else {
      // Kompatybilnosc wsteczna: CLOSE bez parametru
      tryb_pracy = 0; // Prywatny
      zapisz_znak_w_eeprom(0, ADRES_EEPROM_TRYB_PRACY);

      // Jeśli SKRYBA była włączona, wyłącz ją automatycznie
      if (skryba_wlaczona) {
        zapisz_znak_w_eeprom(0, ADRES_EEPROM_SKRYBA);
        skryba_wlaczona = FALSE;
      }
      return INTERPRETACJA_SMS_POPRAWNY;
    }
  }
  case INSTRUKCJA_SET: {
    long h, m, s;

    // Sprawdź czy są parametry (próba parsowania)
    uchar ma_parametry = pobierz_long(&sms, &h) && pomin_znak(&sms, ':') &&
                         pobierz_long(&sms, &m) && pomin_znak(&sms, ':') &&
                         pobierz_long(&sms, &s);

    if (!ma_parametry) {
      // ABCD SET bez parametrów - zwróć aktualny czas (bez sync z SMS)
      // Blokujemy sync czasu, aby odczytać aktualny RTC przed aktualizacją
      extern uchar sms_pomijaj_aktualizacje_czasu;
      sms_pomijaj_aktualizacje_czasu = TRUE;

      // Wyślij raport z aktualnym czasem
      extern char rtc_czas[12];
      uchar *sms_out = tekst_wysylanego_smsa;
      strcpy_P((char *)sms_out, PSTR("Time: "));
      sms_out += strlen((char *)sms_out);
      strcpy((char *)sms_out, rtc_czas);

      // Ustaw numer telefonu odbiorcy
      extern uchar numer_telefonu_wysylanego_smsa[];
      extern uchar numer_telefonu_odebranego_smsa[];
      strcpy((char *)numer_telefonu_wysylanego_smsa,
             (char *)numer_telefonu_odebranego_smsa);

      // Dodaj komendę wysłania SMS
      dodaj_komende(KOMENDA_KOLEJKI_WYSLIJ_SMSA_TEXT);

      return INTERPRETACJA_SMS_POPRAWNY;
    }

    // ABCD SET HH:MM:SS - ustaw czas
    if (h < 0 || h > 23 || m < 0 || m > 59 || s < 0 || s > 59)
      return INTERPRETACJA_SMS_BLEDNE_DANE;

    // Format: AT+CCLK="yy/MM/dd,hh:mm:ss+zz"
    // Używamy fikcyjnej daty 24/01/01
    sprintf(bufor_ustaw_czas, "+CCLK=\"24/01/01,%02d:%02d:%02d+04\"", (int)h,
            (int)m, (int)s);
    dodaj_komende(KOMENDA_KOLEJKI_USTAW_ZEGAR_SIM900);

    // Wyłącz aktualizację czasu z timestampu SMS dla tej komendy
    extern uchar sms_pomijaj_aktualizacje_czasu;
    sms_pomijaj_aktualizacje_czasu = TRUE;

    return INTERPRETACJA_SMS_POPRAWNY;
  }
  case INSTRUKCJA_TIME: {
    // Sprawdzenie czy to komenda OFF
    przeskocz_biale_znaki(sms);
    if (strncasecmp_P(sms, PSTR("OFF"), 3) == 0) {
      // Zapisz wartosci wylaczajace (np. 0xFF)
      zapisz_znak_w_eeprom(0xFF, ADRES_EEPROM_CZAS_START_H);
      zapisz_znak_w_eeprom(0xFF, ADRES_EEPROM_CZAS_START_M);
      zapisz_znak_w_eeprom(0xFF, ADRES_EEPROM_CZAS_STOP_H);
      zapisz_znak_w_eeprom(0xFF, ADRES_EEPROM_CZAS_STOP_M);

      // Aktualizuj zmienne w RAM
      czas_start_h = 0xFF;
      czas_start_m = 0xFF;
      czas_stop_h = 0xFF;
      czas_stop_m = 0xFF;
      blokada_sterowania_czasowa = FALSE;

      return INTERPRETACJA_SMS_POPRAWNY;
    }

    long sh, sm, eh, em;
    // Pobierz HH:MM (start)
    if (!pobierz_long(&sms, &sh) || !pomin_znak(&sms, ':') ||
        !pobierz_long(&sms, &sm))
      return INTERPRETACJA_SMS_BLEDNE_DANE;

    // Pobierz separator (spacja lub inny bialy znak juz pominiety przez
    // pobierz_long/pomin_znak, ale tu moze byc #) Uzytkownik podal przyklad:
    // HH:MM #HH:MM Sprawdzmy czy jest opcjonalny separator np '#'
    if (czy_jest_znak(&sms, '#')) { /* ok, pominelismy */
    }

    // Pobierz HH:MM (stop)
    if (!pobierz_long(&sms, &eh) || !pomin_znak(&sms, ':') ||
        !pobierz_long(&sms, &em))
      return INTERPRETACJA_SMS_BLEDNE_DANE;

    if (sh < 0 || sh > 23 || sm < 0 || sm > 59 || eh < 0 || eh > 23 || em < 0 ||
        em > 59)
      return INTERPRETACJA_SMS_BLEDNE_DANE;

    // Zapis do EEPROM
    zapisz_znak_w_eeprom((uchar)sh, ADRES_EEPROM_CZAS_START_H);
    zapisz_znak_w_eeprom((uchar)sm, ADRES_EEPROM_CZAS_START_M);
    zapisz_znak_w_eeprom((uchar)eh, ADRES_EEPROM_CZAS_STOP_H);
    zapisz_znak_w_eeprom((uchar)em, ADRES_EEPROM_CZAS_STOP_M);

    // Aktualizuj zmienne w RAM
    czas_start_h = (uchar)sh;
    czas_start_m = (uchar)sm;
    czas_stop_h = (uchar)eh;
    czas_stop_m = (uchar)em;

    return INTERPRETACJA_SMS_POPRAWNY;
  }
  case INSTRUKCJA_SKRYBA: {
    przeskocz_biale_znaki(sms);
    if (strncasecmp_P(sms, PSTR("ON"), 2) == 0) {
      sms += 2; // Przeskocz "ON"

      // Sprawdz czy jest opcjonalny parametr (liczba)
      long limit_value = 800; // Domyslny
      przeskocz_biale_znaki(sms);
      if (*sms >= '0' && *sms <= '9') {
        // Jest liczba - sprobuj ja odczytac
        if (pobierz_long(&sms, &limit_value)) {
          // Walidacja zakresu
          if (limit_value < 1 ||
              limit_value > MAX_LICZBA_NUMEROW_TELEFONOW_BRAMA) {
            return INTERPRETACJA_SMS_BLEDNE_DANE;
          }
        } else {
          return INTERPRETACJA_SMS_BLEDNE_DANE;
        }
      }

      // Sprawdz czy jest miejsce na liscie
      uchar jest_miejsce = FALSE;
      for (uint i = 0; i < MAX_LICZBA_NUMEROW_TELEFONOW_BRAMA; ++i) {
        if (!czy_aktywny_numer_telefonu_brama(i)) {
          jest_miejsce = TRUE;
          break;
        }
      }

      if (!jest_miejsce) {
        // Brak miejsca - nie wlaczaj Skryby
        return INTERPRETACJA_SMS_BLEDNE_DANE;
      }

      // Zapisz obecny tryb przed włączeniem SKRYBA
      uchar obecny_tryb =
          eeprom_read_byte((const uint8_t *)ADRES_EEPROM_TRYB_PRACY);
      zapisz_znak_w_eeprom(obecny_tryb, ADRES_EEPROM_SKRYBA_TRYB_BACKUP);

      // Zapisz limit do EEPROM (2 bajty)
      zapisz_znak_w_eeprom((uchar)(limit_value & 0xFF),
                           ADRES_EEPROM_SKRYBA_LIMIT_L);
      zapisz_znak_w_eeprom((uchar)((limit_value >> 8) & 0xFF),
                           ADRES_EEPROM_SKRYBA_LIMIT_H);
      skryba_limit = (uint)limit_value; // Aktualizuj RAM

      // Włącz SKRYBA
      zapisz_znak_w_eeprom(1, ADRES_EEPROM_SKRYBA);
      skryba_wlaczona = TRUE; // Aktualizuj RAM natychmiast

      // Automatycznie ustaw OPEN CLIP (tryb publiczny = 1)
      tryb_pracy = 1; // Aktualizuj RAM
      zapisz_znak_w_eeprom(1, ADRES_EEPROM_TRYB_PRACY);

      return INTERPRETACJA_SMS_POPRAWNY;
    } else if (strncasecmp_P(sms, PSTR("OFF"), 3) == 0) {
      // Wyłącz SKRYBA
      zapisz_znak_w_eeprom(0, ADRES_EEPROM_SKRYBA);
      skryba_wlaczona = FALSE; // Aktualizuj RAM natychmiast

      // Przywróć poprzedni tryb
      uchar poprzedni_tryb =
          eeprom_read_byte((const uint8_t *)ADRES_EEPROM_SKRYBA_TRYB_BACKUP);
      if (poprzedni_tryb != 0xFF) {  // Jeśli był zapisany
        tryb_pracy = poprzedni_tryb; // Aktualizuj RAM
        zapisz_znak_w_eeprom(poprzedni_tryb, ADRES_EEPROM_TRYB_PRACY);
      }

      return INTERPRETACJA_SMS_POPRAWNY;
    }
    return INTERPRETACJA_SMS_BLEDNE_DANE;
  }
  case INSTRUKCJA_DEBUG: {
    return INTERPRETACJA_SMS_DEBUG;
  }
  case INSTRUKCJA_START: {
    blokada_systemu = FALSE;
    zapisz_znak_w_eeprom(0, ADRES_EEPROM_BLOKADA_SYSTEMU);
    return INTERPRETACJA_SMS_POPRAWNY;
  }
  case INSTRUKCJA_STOP: {
    blokada_systemu = TRUE;
    zapisz_znak_w_eeprom(1, ADRES_EEPROM_BLOKADA_SYSTEMU);
    return INTERPRETACJA_SMS_POPRAWNY;
  }
  case INSTRUKCJA_SUB: {
    if (not pobierz_numer_telefonu(&sms, &numer_telefonu_do_ktorego_dzwonic[0],
                                   14))
      return INTERPRETACJA_SMS_BLEDNE_DANE;
    dodaj_komende(KOMENDA_KOLEJKI_DODAJ_SUPER_USERA);
    return INTERPRETACJA_SMS_POPRAWNY;
  }
  }
  return INTERPRETACJA_SMS_ZLY_FORMAT;
}

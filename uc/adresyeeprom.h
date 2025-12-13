
#include "narzedzia.h"

#define ADRES_EEPROM_KOD_DOSTEPU 1
#define LICZBA_BAJTOW_KODU_DOSTEPU 4

#define EEPROM_USTAWIENIE_STANOW_WYJSC                                         \
  (ADRES_EEPROM_KOD_DOSTEPU + LICZBA_BAJTOW_KODU_DOSTEPU)

#define EEPROM_USTAWIENIE_WYJSCIA (EEPROM_USTAWIENIE_STANOW_WYJSC + 1)

#define MAX_LICZBA_ZNAKOW_TELEFON 16
#define LICZBA_BAJTOW_NUMERU_TELEFONU_W_EEPROM 5 // byo 5

#define EEPROM_NUMER_TELEFONU_BRAMA_0 (EEPROM_USTAWIENIE_WYJSCIA + 2)
#define EEPROM_NUMER_TELEFONU_BRAMA(NR)                                        \
  (EEPROM_NUMER_TELEFONU_BRAMA_0 +                                             \
   (NR) * LICZBA_BAJTOW_NUMERU_TELEFONU_W_EEPROM)
#define MAX_LICZBA_NUMEROW_TELEFONOW_BRAMA 800
#define MAX_LICZBA_NUMEROW_TELEFONOW_BRAMA_USER 255

#define ADRES_EEPROM_TRYB_PRACY 4094
#define ADRES_EEPROM_TRYB_CLIP_DTMF 4095 // 0=DTMF, 1=CLIP

// Adres dla funkcji SKRYBA
#define ADRES_EEPROM_SKRYBA 4089
#define ADRES_EEPROM_SKRYBA_TRYB_BACKUP                                        \
  4088 // Backup poprzedniego trybu (OPEN/CLOSE CLIP/DTMF)
#define ADRES_EEPROM_SKRYBA_LIMIT_H 4086 // High byte limitu uzytkownikow
#define ADRES_EEPROM_SKRYBA_LIMIT_L 4085 // Low byte limitu uzytkownikow
#define ADRES_EEPROM_BLOKADA_SYSTEMU                                           \
  4087 // Status blokady (0=Aktywny, 1=Zablokowany)

// Adresy dla funkcji TIME
#define ADRES_EEPROM_CZAS_START_H 4090
#define ADRES_EEPROM_CZAS_START_M 4091
#define ADRES_EEPROM_CZAS_STOP_H 4092
#define ADRES_EEPROM_CZAS_STOP_M 4093

// Debug SKRYBA (tymczasowe)
#define ADRES_EEPROM_DEBUG_SKRYBA_1 4080 // CLIP otrzymany
#define ADRES_EEPROM_DEBUG_SKRYBA_2 4081 // skryba_wlaczona
#define ADRES_EEPROM_DEBUG_SKRYBA_3 4082 // !znaleziono
#define ADRES_EEPROM_DEBUG_SKRYBA_4 4083 // komenda dodana
#define ADRES_EEPROM_DEBUG_SKRYBA_5 4084 // komenda wykonana

// Debug USER
#define ADRES_EEPROM_DEBUG_USER_1 4070 // Komenda USER otrzymana
#define ADRES_EEPROM_DEBUG_USER_2 4071 // flaga_wysylanie_smsa
#define ADRES_EEPROM_DEBUG_USER_3 4072 // licznik_report_user
#define ADRES_EEPROM_DEBUG_USER_4 4073 // liczba_sms_w_kolejce
#define ADRES_EEPROM_DEBUG_USER_5 4074 // liczba_wszystkich_komend
#define ADRES_EEPROM_DEBUG_USER_6 4075 // znaleziono (0/1)
#define ADRES_EEPROM_DEBUG_USER_7 4076 // dodano_komende_wyslij (0/1)

#define EEPROM_DEBUG_START 4050
#define EEPROM_DEBUG_LICZNIK_RESETOW 4060

// Numer własny urządzenia (dla auto-sync czasu)
#define ADRES_EEPROM_MOJE_NUMER_START 4040 // 10 bajtów na numer (max 9 cyfr + null)

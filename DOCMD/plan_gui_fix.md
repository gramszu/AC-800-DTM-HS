# Implementacja opcji CLIP/DTMF w GUI i weryfikacja komend SMS

## Opis Problemu

Interfejs GUI (`AC800-DTM-HS.py`) **nie posiada kontrolki** do ustawiania trybu sterowania **CLIP/DTMF** (adres EEPROM 4095). Obecna sekcja "Funkcja Skryba" to osobna funkcjonalność (adres 4089) i nie kontroluje trybu CLIP/DTMF.

### Stan obecny:
| Element | Adres EEPROM | W GUI? | W C? |
|---------|--------------|--------|------|
| Status (Aktywny/Blokada) | 4087 | ✅ | ✅ |
| Tryb pracy (Prywatny/Publiczny) | 4094 | ✅ | ✅ |
| **Tryb sterowania (CLIP/DTMF)** | **4095** | ❌ BRAK | ✅ |
| Funkcja Skryba (ON/OFF) | 4089 | ✅ | ✅ |
| Harmonogram (TIME) | 4090-4093 | ✅ | ✅ |

---

## Proponowane Zmiany

### [Komponent 1: Python GUI]

#### [MODIFY] [AC800-DTM-HS.py](file:///Users/gramsz/Desktop/AC-800-DTM-HARMO/uc/AC800-DTM-HS.py)

1. **Dodać adres EEPROM w konfiguracji:**
   ```python
   "ADDR_CLIP_DTMF": 4095,  # 0=DTMF, 1=CLIP
   ```

2. **Dodać zmienną dla trybu CLIP/DTMF:**
   ```python
   self.clip_dtmf_var = tk.IntVar(value=1)  # 0=DTMF, 1=CLIP (domyślnie CLIP)
   ```

3. **Poprawić etykiety - rozdzielić Skryba od CLIP/DTMF:**
   ```python
   "control_mode": "Tryb sterowania",  # Nowa sekcja
   "control_clip": "CLIP",
   "control_dtmf": "DTMF",
   "skryba_mode": "Funkcja Skryba",
   "skryba_on": "Włączona",
   "skryba_off": "Wyłączona",
   ```

4. **Dodać nową sekcję GUI dla trybu CLIP/DTMF:**
   - RadioButton "CLIP" (value=1)
   - RadioButton "DTMF" (value=0)

5. **Poprawić istniejącą sekcję Skryba:**
   - Zmienić etykiety na "Włączona"/"Wyłączona"
   - Usunąć pomieszanie z CLIP/DTMF

6. **Dodać odczyt/zapis trybu CLIP/DTMF w funkcjach:**
   - `read_status_and_mode_from_eeprom()` - odczyt z adresu 4095
   - `write_status_and_mode_to_eeprom()` - zapis do adresu 4095

7. **Dodać obsługę CSV dla trybu CLIP/DTMF**

---

### [Komponent 2: Kod C - weryfikacja]

Komendy SMS działają poprawnie – weryfikacja kodu:

#### [interpretacjaSMS.c](file:///Users/gramsz/Desktop/AC-800-DTM-HARMO/uc/interpretacjaSMS.c)
- ✅ `ABCD OPEN CLIP` - ustawia `tryb_clip=TRUE`, zapisuje 1 do adresu 4095
- ✅ `ABCD OPEN DTMF` - ustawia `tryb_clip=FALSE`, zapisuje 0 do adresu 4095
- ✅ `ABCD CLOSE CLIP` - ustawia `tryb_clip=TRUE`, zapisuje 1 do adresu 4095
- ✅ `ABCD CLOSE DTMF` - ustawia `tryb_clip=FALSE`, zapisuje 0 do adresu 4095
- ✅ `ABCD OPEN` (bez parametru) - tylko zmienia tryb na Publiczny, bez zmiany CLIP/DTMF
- ✅ `ABCD CLOSE` (bez parametru) - tylko zmienia tryb na Prywatny

#### [main.c](file:///Users/gramsz/Desktop/AC-800-DTM-HARMO/uc/main.c)
- ✅ Raport SMS (`ABCD REPORT`) wyświetla " CLIP" lub " DTMF" (linie 237-242)
- ✅ Inicjalizacja `tryb_clip` z EEPROM (linie 1770-1776)
- ✅ Logika `sprawdz_przychodzaca_rozmowe()` poprawnie sprawdza `tryb_clip`

> [!IMPORTANT]
> Kod C nie wymaga zmian - tylko GUI Python.

---

## Plan Weryfikacji

### Automatyczne testy
1. Kompilacja GUI Python (brak błędów składniowych)
2. Kompilacja firmware C (brak błędów)

### Testy manualne
1. Odczyt EEPROM ze sterownika - sprawdzenie czy GUI poprawnie wyświetla tryb CLIP/DTMF
2. Zapis EEPROM - sprawdzenie czy zmiana trybu w GUI zapisuje się poprawnie
3. Testy SMS:
   - `ABCD REPORT` - powinien zwrócić aktualny tryb CLIP lub DTMF
   - `ABCD OPEN CLIP` / `ABCD OPEN DTMF` - zmiana trybu
   - `ABCD CLOSE CLIP` / `ABCD CLOSE DTMF` - zmiana trybu

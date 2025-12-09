#!/bin/bash

# Jeśli skrypt nie ma uprawnień roota (potrzebne do dostępu do AVRISP2 na macOS),
# spróbuj uruchomić go ponownie przez sudo – unikamy pętli dzięki znacznikowi.
if [ "$EUID" -ne 0 ] && [ -z "$UPLOAD_SH_ROOT" ]; then
    echo "Brak uprawnień do urządzenia USB – proszę o hasło administratora..."
    UPLOAD_SH_ROOT=1 exec sudo -E UPLOAD_SH_ROOT=1 "$0" "$@"
fi

# Skrypt do wgrywania flash, EEPROM, bootloadera i fuse bits do ATmega328PB przez AVRISP2

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

MCU="atmega1284p"
PROGRAMMER="avrisp2"
FLASH_BASENAME="AC800-DTM-HS.hex"
FLASH_FILE="${FLASH_FILE:-$SCRIPT_DIR/$FLASH_BASENAME}"

if [ ! -f "$FLASH_FILE" ]; then
    ALT_FLASH=$(find "$SCRIPT_DIR" "$SCRIPT_DIR/.." -maxdepth 2 -name "$FLASH_BASENAME" 2>/dev/null | head -n 1)
    if [ -n "$ALT_FLASH" ]; then
        FLASH_FILE="$ALT_FLASH"
    fi
fi

EEPROM_FILE="${EEPROM_FILE:-$SCRIPT_DIR/default_eeprom.hex}"
BOOTLOADER_FILE="${BOOTLOADER_FILE:-$SCRIPT_DIR/urboot-1284p.hex}"

echo "=========================================="
echo "Wgrywanie do ATmega1284p przez AVRISP2"
echo "=========================================="
echo ""

# Sprawdz czy pliki istnieja
if [ ! -f "$FLASH_FILE" ]; then
    echo "BŁĄD: Nie znaleziono pliku $FLASH_FILE"
    exit 1
fi

if [ ! -f "$BOOTLOADER_FILE" ]; then
    echo "BŁĄD: Nie znaleziono pliku bootloadera $BOOTLOADER_FILE"
    exit 1
fi

# Sprawdz czy EEPROM istnieje (opcjonalny)
if [ ! -f "$EEPROM_FILE" ]; then
    echo "UWAGA: Nie znaleziono pliku $EEPROM_FILE - wgrywam bez EEPROM"
    EEPROM_OPTION=""
else
    EEPROM_OPTION="-U eeprom:w:$EEPROM_FILE:i"
fi

echo "Wgrywanie:"
echo "  1. Flash programu: $FLASH_FILE"
if [ -n "$EEPROM_OPTION" ]; then
    echo "  2. EEPROM: $EEPROM_FILE"
fi
echo "  3. Bootloader: $BOOTLOADER_FILE"
echo "  4. Fuse bits (lfuse=0xFD, hfuse=0xDE, efuse=0xF5)"
echo "  5. Lock bits (0x0C)"
echo ""

# Wgraj wszystko w jednej komendzie (jak w Pythonie)
# Kolejność: flash programu, EEPROM, bootloader, fuse bits, lock bits
avrdude -c $PROGRAMMER -p $MCU -B 5 -e -D -v \
    -U flash:w:$FLASH_FILE:i \
    $EEPROM_OPTION \
    -U flash:w:$BOOTLOADER_FILE:i \
    -U lfuse:w:0xFD:m \
    -U hfuse:w:0xDE:m \
    -U efuse:w:0xF5:m \
    -U lock:w:0x0C:m -v

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Wgrywanie zakończone pomyślnie!"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "✗ Błąd podczas wgrywania!"
    echo "=========================================="
    exit 1
fi


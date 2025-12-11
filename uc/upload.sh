#!/bin/bash

# Jeśli skrypt nie ma uprawnień roota (potrzebne do dostępu do AVRISP2 na macOS),
# spróbuj uruchomić go ponownie przez sudo – unikamy pętli dzięki znacznikowi.
if [ "$EUID" -ne 0 ] && [ -z "$UPLOAD_SH_ROOT" ]; then
    echo "Brak uprawnień do urządzenia USB – proszę o hasło administratora..."
    UPLOAD_SH_ROOT=1 exec sudo -E UPLOAD_SH_ROOT=1 "$0" "$@"
fi

# Skrypt do wgrywania flash, EEPROM, bootloadera i fuse bits do ATmega1284P przez AVRISP2

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

MCU="atmega1284p"
PROGRAMMER="avrisp2"
FLASH_BASENAME="AC800-DTM-HS-RC3.hex"
FLASH_FILE="${FLASH_FILE:-$SCRIPT_DIR/$FLASH_BASENAME}"
EEPROM_FILE="$SCRIPT_DIR/default_eeprom.hex"

BOOTLOADER_FILE="${BOOTLOADER_FILE:-$SCRIPT_DIR/urboot-1284p.hex}"

echo "=========================================="
echo "Operacje na ATmega1284P przez AVRISP2"
echo "=========================================="
echo ""

echo "=========================================="
echo "Kompilacja projektu..."
make
if [ $? -ne 0 ]; then
    echo "BŁĄD: Kompilacja nie powiodła się!"
    exit 1
fi
echo "=========================================="

# KROK: Wgrywanie nowego softu + ustalonego EEPROM
echo "Wgrywanie:"
echo "   - Flash programu: $FLASH_FILE"
echo "   - EEPROM (stały plik): $EEPROM_FILE"
echo "   - Bootloader: $BOOTLOADER_FILE"
echo "   - Fuse bits (lfuse=0xFD, hfuse=0xDA, efuse=0xF5)"
echo "   - Lock bits (0x3C)"

# Sprawdz czy pliki istnieja
if [ ! -f "$FLASH_FILE" ]; then
    echo "BŁĄD: Nie znaleziono pliku $FLASH_FILE"
    exit 1
fi

if [ ! -f "$BOOTLOADER_FILE" ]; then
    echo "BŁĄD: Nie znaleziono pliku bootloadera $BOOTLOADER_FILE"
    exit 1
fi

if [ ! -f "$EEPROM_FILE" ]; then
    echo "BŁĄD: Nie znaleziono pliku EEPROM $EEPROM_FILE"
    exit 1
fi

# Wgraj wszystko w jednej komendzie
avrdude -c $PROGRAMMER -p $MCU -B 5 -e -D -v \
    -U flash:w:$FLASH_FILE:i \
    -U eeprom:w:$EEPROM_FILE:i \
    -U flash:w:$BOOTLOADER_FILE:i \
    -U lfuse:w:0xFD:m \
    -U hfuse:w:0xDE:m \
    -U efuse:w:0xF5:m \
    -U lock:w:0x0c:m -v

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Operacja zakończona pomyślnie!"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "✗ Błąd podczas wgrywania!"
    echo "=========================================="
    exit 1
fi

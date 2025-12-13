import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import subprocess
import os
import string
import webbrowser
import csv
import threading
import time
import sys
import logging
import ctypes
from queue import Queue
from typing import Optional, Tuple, Dict, List
import serial.tools.list_ports
import serial
import shutil

# Configure logging
logging.basicConfig(
    filename="bramster.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ===== FUNKCJA OBSŁUGI ŚCIEŻEK DLA PYINSTALLER =====
def resource_path(relative_path: str) -> str:
    """Zwraca absolutną ścieżkę do pliku w pakiecie PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    full_path = os.path.join(base_path, relative_path)
    logging.info(f"Resolved path for {relative_path}: {full_path}")
    return full_path


# ===== KONFIGURACJA PROGRAMU =====
class AppConfig:
    def __init__(self):
        # Ustawienia techniczne dla ATmega1284 (800 numerów) - JEDYNA KONFIGURACJA
        self.CONFIG_M1284 = {
            "MCU": "m1284p",
            "EEPROM_SIZE": 4096,
            "NUM_ENTRIES": 800,
            "RANGE_START": 0x08,
            "DESCRIPTION": "Bramster AC800-TS",
            # Adresy specyficzne dla M1284
            "ADDR_SKRYBA": 4089,
            "ADDR_SKRYBA_LIMIT_L": 4085,
            "ADDR_SKRYBA_LIMIT_H": 4086,
            "ADDR_TIME_START_H": 4090,
            "ADDR_TIME_START_M": 4091,
            "ADDR_TIME_STOP_H": 4092,
            "ADDR_TIME_STOP_M": 4093,
            "ADDR_MODE": 4094,
            "ADDR_STATUS": 4087,
            "ADDR_MYNUM": 4040,  # Własny numer telefonu (10 bajtów)
            "ADDR_CLIP_DTMF": 4095,  # 0=DTMF, 1=CLIP
        }

        # Aktywna konfiguracja - tylko M1284
        self.ACTIVE_CONFIG = self.CONFIG_M1284

        self.PROGRAMMER = "urclock"
        self.BAUDRATE = "115200"
        self.PORT = "COM3"

        # Dynamicznie ustawiane wartości
        self.MCU = self.ACTIVE_CONFIG["MCU"]
        self.EEPROM_SIZE = self.ACTIVE_CONFIG["EEPROM_SIZE"]
        self.EEPROM_FILE = resource_path("tools/eeprom_dump.bin")
        self.FLASH_FILE = resource_path("tools/firmware_temp.hex")

        # Ścieżki do lokalnych plików avrdude
        self.AVRDUDE_PATH = resource_path("tools/avrdude.exe" if os.name == "nt" else "tools/avrdude")
        self.AVRDUDE_CONF = resource_path("tools/avrdude.conf")

        # Ustawienia interfejsu
        self.WINDOW_TITLE = "AC800 DTM-TS"
        self.WINDOW_SIZE = "605x950" # Zwiekszone dla Time Control
        self.WEBSITE_URL = "https://www.sonfy.pl"

        # Teksty przycisków
        self.BUTTONS = {
            "read_chip": "Odczytaj dane ze sterownika",
            "write_chip": "Wgraj dane do sterownika",
            "buy_now": "Aktualizacje",
            "save_csv": "Zapisz dane do CSV",
            "read_csv": "Odczytaj dane z CSV",
            "clear_all": "Wyczyść wszystkie numery",
            "sync_numbers": "Aktualizuj listę numerów",
            "about": "Info",
            "apply": "Zmień",
            "add": "Dodaj",
            "remove": "Usuń",
        }

        # Etykiety i nagłówki
        self.LABELS = {
            "access_code": "Zmiana kodu dostępu",
            "numbers_list": "Lista numerów uprawnionych",
            "ready": "Gotowe",
            "com_port": "Port COM",
            "processor_select": "Wybór sterownika",
            "status_control": "Status sterownika",
            "mode_control": "Tryb pracy",
            "status_active": "Aktywny",
            "status_blocked": "Blokada",
            "mode_private": "Prywatny",
            "mode_public": "Publiczny",
            "clip_dtmf_mode": "Tryb sterowania",  # Nowa sekcja CLIP/DTMF
            "clip_mode": "CLIP",
            "dtmf_mode": "DTMF",
            "control_mode": "Funkcja Skryba",
            "control_clip": "Włączona",
            "control_dtmf": "Wyłączona",
            "time_control": "Harmonogram",
        }

        # Komunikaty
        self.MESSAGES = {
            "start_info": "Aby zacząć, podłącz sterownik.\nKliknij odczytaj dane ze sterownika",
            "number_cleared": "Numer usunięty",
            "update_success": "Zaktualizowano dane z listy numerów",
            "access_code_updated": "Zaktualizowano kod dostępu",
            "file_saved": "Zapisano listę numerów do pliku",
            "file_loaded": "Odczytano listę numerów z pliku",
            "chip_read": "Odczytano listę numerów ze sterownika",
            "chip_written": "Wgrano listę numerów do sterownika",
            "csv_saved": "Zapisano listę numerów do CSV",
            "csv_loaded": "Odczytano listę numerów z pliku",
            "all_cleared": "Wszystkie numery usunięto z bufora",
            "status_updated": "Zaktualizowano status sterownika",
            "mode_updated": "Zaktualizowano tryb pracy",
            "error": "Błąd",
            "info": "Info",
            "no_data": "Brak danych",
            "permission_error": "Brak uprawnień do pliku.",
            "avrdude_missing": "Nie znaleziono pliku avrdude.exe w folderu tools/.",
            "avrdude_invalid": "Plik avrdude.exe nie jest prawidłową aplikacją Win32.",
            "invalid_hex": "Nieprawidłowy numer w polu.",
            "invalid_chars": "Pole zawiera niedozwolone znaki",
            "file_error": "Błąd podczas operacji na pliku",
            "process_error": "Błąd podczas przetwarzania",
            "communication_error": "Błąd komunikacji."
        }

        # Inicjalizacja adresów z domyślnej konfiguracji
        self.update_addresses()

        self.ABOUT_INFO = """
AC800 DTM-TS
firmware 2.0

Autor: Robert Gramsz
www.sonfy.pl
"""

    def update_addresses(self):
        """Aktualizuje adresy EEPROM na podstawie aktywnej konfiguracji."""
        self.EEPROM_ADDR_SKRYBA = self.ACTIVE_CONFIG["ADDR_SKRYBA"]
        self.EEPROM_ADDR_SKRYBA_LIMIT_L = self.ACTIVE_CONFIG["ADDR_SKRYBA_LIMIT_L"]
        self.EEPROM_ADDR_SKRYBA_LIMIT_H = self.ACTIVE_CONFIG["ADDR_SKRYBA_LIMIT_H"]
        self.EEPROM_ADDR_STATUS = self.ACTIVE_CONFIG["ADDR_STATUS"]
        self.EEPROM_ADDR_MODE = self.ACTIVE_CONFIG["ADDR_MODE"]
        self.EEPROM_ADDR_TIME_START_H = self.ACTIVE_CONFIG["ADDR_TIME_START_H"]
        self.EEPROM_ADDR_TIME_START_M = self.ACTIVE_CONFIG["ADDR_TIME_START_M"]
        self.EEPROM_ADDR_TIME_STOP_H = self.ACTIVE_CONFIG["ADDR_TIME_STOP_H"]
        self.EEPROM_ADDR_TIME_STOP_M = self.ACTIVE_CONFIG["ADDR_TIME_STOP_M"]
        self.EEPROM_ADDR_MYNUM = self.ACTIVE_CONFIG["ADDR_MYNUM"]
        self.EEPROM_ADDR_CLIP_DTMF = self.ACTIVE_CONFIG["ADDR_CLIP_DTMF"]



# ===== KLASA PROGRESS MANAGER =====
class ProgressManager:
    def __init__(self, root: tk.Tk, config: AppConfig):
        self.root = root
        self.config = config
        self.progress_running = False
        self.start_time = 0
        self.max_duration = 27

        self.frame = ttk.Frame(root)
        self.frame.pack(fill='x', padx=10, pady=5)

        self.progress_bar = ttk.Progressbar(
            self.frame,
            orient='horizontal',
            mode='determinate',
            maximum=self.max_duration,
            length=490
        )
        self.progress_bar.pack(side='left')

        self.label = ttk.Label(self.frame, text=self.config.LABELS["ready"], width=10)
        self.label.pack(side='left', padx=10)

    def start(self) -> None:
        if not self.progress_running:
            self.progress_running = True
            self.start_time = time.time()
            self.progress_bar['value'] = 0
            self.label.config(text=f"0/{self.max_duration}s")
            self._update()

    def _update(self) -> None:
        if self.progress_running:
            elapsed = min(int(time.time() - self.start_time), self.max_duration)
            self.progress_bar['value'] = elapsed
            self.label.config(text=f"{elapsed}/{self.max_duration}s")
            if elapsed < self.max_duration:
                self.root.after(1000, self._update)
            else:
                self.stop()

    def stop(self) -> None:
        if self.progress_running:
            self.progress_running = False
            self.progress_bar['value'] = 0
            self.label.config(text=self.config.LABELS["ready"])


# ===== POST-FLASH PROGRESS MANAGER =====
class PostFlashProgressManager:
    def __init__(self, master: tk.Tk, duration_sec: int = 27):
        self.master = master
        self.duration_sec = duration_sec
        self.start_time = 0.0
        self.top: Optional[tk.Toplevel] = None
        self.progress_bar: Optional[ttk.Progressbar] = None
        self.label: Optional[ttk.Label] = None
        self.running = False
        self.update_interval = 1000

    def start(self) -> None:
        if self.running:
            return

        self.running = True
        self.start_time = time.time()

        self.top = tk.Toplevel(self.master)
        self.top.title("Aktualizacja firmware...")
        self.top.geometry("320x100")
        self.top.transient(self.master)
        self.top.grab_set()
        self.top.resizable(False, False)
        self.top.protocol("WM_DELETE_WINDOW", lambda: None)

        frame = ttk.Frame(self.top, padding="10")
        frame.pack(fill='both', expand=True)

        self.label = ttk.Label(frame, text=f"Trwa reset sterownika: {self.duration_sec}s")
        self.label.pack(pady=(5, 5))

        self.progress_bar = ttk.Progressbar(
            frame,
            orient='horizontal',
            mode='determinate',
            maximum=self.duration_sec,
            length=280
        )
        self.progress_bar.pack(padx=5, fill='x')

        self.top.update_idletasks()
        width = self.top.winfo_width()
        height = self.top.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.top.geometry(f'+{x}+{y}')

        self._update()

    def _update(self) -> None:
        if self.running and self.top:
            elapsed = int(time.time() - self.start_time)
            remaining = max(0, self.duration_sec - elapsed)

            self.progress_bar['value'] = self.duration_sec - remaining

            if remaining > 0:
                self.label.config(text=f"Aktualizacja... Pozostało: {remaining}s")
                self.top.after(self.update_interval, self._update)
            else:
                self.stop()

    def stop(self) -> None:
        if self.running and self.top:
            self.running = False
            try:
                self.top.grab_release()
                self.top.destroy()
            except tk.TclError:
                pass
            self.top = None


# ===== GŁÓWNA KLASA APLIKACJI =====
class BramsterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.config = AppConfig()
        self.result_queue = Queue()
        self.hex_configs: List[Dict] = []
        self.about_logo: Optional[tk.PhotoImage] = None
        self.icon_photo: Optional[tk.PhotoImage] = None
        self.ascii_var = tk.StringVar()
        self.mynum_var = tk.StringVar()  # Własny numer telefonu dla auto-sync
        self.com_port_var = tk.StringVar(value=self.config.PORT)

        # Zmienne dla statusu, trybu i sterowania (zgodne z C)
        self.status_var = tk.IntVar(value=0)  # 0 = Aktywny, 1 = Blokada
        self.mode_var = tk.IntVar(value=1)    # 0 = Prywatny, 1 = Publiczny
        self.clip_dtmf_var = tk.IntVar(value=1)  # 0 = DTMF, 1 = CLIP (domyślnie CLIP)
        self.skryba_var = tk.IntVar(value=0)  # 0 = Wylaczona, 1 = Wlaczona
        self._skryba_trace_enabled = True  # Flaga do blokowania trace podczas odczytu EEPROM
        self.skryba_var.trace_add("write", self.on_skryba_change)
        self.backup_mode = None  # Do przywracania trybu po wyłączeniu Skryby
        self.backup_clip_dtmf = None  # Do przywracania trybu CLIP/DTMF
        self.skryba_limit_var = tk.IntVar(value=800)  # Limit użytkowników dla Skryby (1-800)

        # Zmienne dla Time Control
        self.time_enabled_var = tk.IntVar(value=0)  # 0 = Wyłączony, 1 = Włączony
        self.time_start_h_var = tk.StringVar(value="00")
        self.time_start_m_var = tk.StringVar(value="00")
        self.time_stop_h_var = tk.StringVar(value="00")
        self.time_stop_m_var = tk.StringVar(value="00")



        # Elementy UI
        self.text_area: Optional[scrolledtext.ScrolledText] = None
        self.numbers_text: Optional[scrolledtext.ScrolledText] = None
        self.progress_manager: Optional[ProgressManager] = None
        self.entry_ascii: Optional[tk.Entry] = None
        self.com_port_combobox: Optional[ttk.Combobox] = None

        # Kontrolki status/tryb/sterowanie
        self.check_status_active: Optional[tk.Radiobutton] = None
        self.check_status_blocked: Optional[tk.Radiobutton] = None
        self.check_mode_private: Optional[tk.Radiobutton] = None
        self.check_mode_public: Optional[tk.Radiobutton] = None
        self.check_skryba_on: Optional[tk.Radiobutton] = None
        self.check_skryba_off: Optional[tk.Radiobutton] = None
        
        # Kontrolki Time Control
        self.spin_start_h: Optional[tk.Spinbox] = None
        self.spin_start_m: Optional[tk.Spinbox] = None
        self.spin_stop_h: Optional[tk.Spinbox] = None
        self.spin_stop_m: Optional[tk.Spinbox] = None

        if not self.check_system_requirements():
            root.after(100, root.destroy)
            return

        self.setup_ui()
        self.generate_hex_configs()
        self.clear_hex_data()
        self.root.after(100, self.show_result)

    def validate_number_input(self, text: str) -> bool:
        """Waliduje wprowadzane numery - od 3 do 9 cyfr."""
        if not (3 <= len(text) <= 9):
            return False
        if not text.isdigit():
            return False
        return True

    def on_skryba_change(self, *args) -> None:
        """Automatycznie zarządza trybem pracy przy zmianie Skryby."""
        # Blokuj działanie podczas odczytu z EEPROM
        if not getattr(self, '_skryba_trace_enabled', True):
            return
            
        val = self.skryba_var.get()
        if val == 1:
            # Włączanie Skryby: Zapisz obecne tryby i wymuś Aktywny + CLIP + Publiczny
            self.backup_mode = self.mode_var.get()
            self.backup_clip_dtmf = self.clip_dtmf_var.get()
            self.backup_status = self.status_var.get()
            # Wymuś status Aktywny
            if self.status_var.get() != 0:
                self.status_var.set(0)
            # Wymuś tryb Publiczny
            if self.mode_var.get() != 1:
                self.mode_var.set(1)
            # Wymuś tryb CLIP
            if self.clip_dtmf_var.get() != 1:
                self.clip_dtmf_var.set(1)
            
            # Disable controls
            try:
                self.check_status_active.config(state="disabled")
                self.check_status_blocked.config(state="disabled")
                self.check_mode_private.config(state="disabled")
                self.check_mode_public.config(state="disabled")
                self.check_clip.config(state="disabled")
                self.check_dtmf.config(state="disabled")
            except AttributeError:
                pass # Kontrolki mogą jeszcze nie istnieć przy inicjalizacji
            
        elif val == 0:
            # Enable controls first
            try:
                self.check_status_active.config(state="normal")
                self.check_status_blocked.config(state="normal")
                self.check_mode_private.config(state="normal")
                self.check_mode_public.config(state="normal")
                self.check_clip.config(state="normal")
                self.check_dtmf.config(state="normal")
            except AttributeError:
                pass

            # Wyłączanie Skryby: Przywróć poprzednie tryby (jeśli były zapisane)
            if self.backup_mode is not None:
                self.mode_var.set(self.backup_mode)
                self.backup_mode = None
            if self.backup_clip_dtmf is not None:
                self.clip_dtmf_var.set(self.backup_clip_dtmf)
                self.backup_clip_dtmf = None
            if getattr(self, 'backup_status', None) is not None:
                self.status_var.set(self.backup_status)
                self.backup_status = None

    def validate_hour(self, new_value: str) -> bool:
        """Walidacja dla pola godziny (0-23)."""
        if new_value == "":
            return True
        if not new_value.isdigit():
            return False
        return 0 <= int(new_value) <= 23

    def validate_minute(self, new_value: str) -> bool:
        """Walidacja dla pola minuty (0-59)."""
        if new_value == "":
            return True
        if not new_value.isdigit():
            return False
        return 0 <= int(new_value) <= 59

    def validate_mynum_input(self, new_value: str) -> bool:
        """Walidacja dla numeru karty SIM - tylko cyfry 0-9, maksymalnie 9 znaków."""
        if new_value == "":
            return True
        if not new_value.isdigit():
            return False
        return len(new_value) <= 9

    def generate_hex_configs(self) -> None:
        """Generuje dynamiczną konfigurację dla aktywnej liczby numerów."""
        self.hex_configs = []
        current_config = self.config.ACTIVE_CONFIG
        start_address = current_config["RANGE_START"]
        entry_size = 5
        num_entries = current_config["NUM_ENTRIES"]

        for i in range(num_entries):
            current_start = start_address + i * entry_size
            current_end = current_start + entry_size - 1

            if current_end >= current_config["EEPROM_SIZE"]:
                break

            self.hex_configs.append({
                "RANGE_START": current_start,
                "RANGE_END": current_end,
                "SKIP_F": True,
                "NO_SPACES": True,
                "NAME": f"Numer {i + 1}"
            })
        logging.info(f"Generated {len(self.hex_configs)} HEX configs for {current_config['MCU']}")



    def get_available_com_ports(self) -> List[str]:
        """Zwraca listę dostępnych portów COM."""
        try:
            ports = [port.device for port in serial.tools.list_ports.comports()]
            if not ports:
                ports = [f"COM{i}" for i in range(1, 11)]
        except Exception as e:
            logging.error(f"Error listing COM ports: {str(e)}")
            ports = [f"COM{i}" for i in range(1, 11)]
        return ports

    def update_com_port(self) -> None:
        """Aktualizuje wybrany port COM w konfiguracji."""
        selected_port = self.com_port_var.get()
        if selected_port:
            self.config.PORT = selected_port
            logging.info(f"COM port updated to: {self.config.PORT}")

    def pulse_dtr(self) -> None:
        """Wysyła impuls 0.2 sekundy na pin DTR."""
        try:
            with serial.Serial(self.config.PORT, baudrate=9600, timeout=1) as ser:
                ser.dtr = True
                time.sleep(0.2)
                ser.dtr = False
            logging.info(f"DTR pulse sent on port {self.config.PORT}")
        except Exception as e:
            logging.error(f"Error sending DTR pulse: {str(e)}")

    def get_status_text(self, status_var_value: int) -> str:
        return self.config.LABELS["status_active"] if status_var_value == 0 else self.config.LABELS["status_blocked"]

    def get_mode_text(self, mode_var_value: int) -> str:
        return self.config.LABELS["mode_private"] if mode_var_value == 0 else self.config.LABELS["mode_public"]

    def get_skryba_text(self, skryba_var_value: int) -> str:
        return self.config.LABELS["control_clip"] if skryba_var_value == 1 else self.config.LABELS["control_dtmf"]

    def read_status_and_mode_from_eeprom(self, data: bytes) -> None:
        """Odczytuje status, tryb pracy, Skryba i Time Control z EEPROM i aktualizuje GUI."""
        # Wyłącz trace aby nie wywoływać automatycznego ustawiania CLIP/Publiczny przy odczycie
        self._skryba_trace_enabled = False
        
        # Skryba (M1284: 1=ON, 0=OFF)
        if self.config.EEPROM_ADDR_SKRYBA and len(data) > self.config.EEPROM_ADDR_SKRYBA:
            skryba_byte = data[self.config.EEPROM_ADDR_SKRYBA]
            self.skryba_var.set(1 if skryba_byte == 0x01 else 0)
        
        # Włącz trace z powrotem
        self._skryba_trace_enabled = True
        
        # Skryba Limit (2 bajty: L i H)
        if (self.config.EEPROM_ADDR_SKRYBA_LIMIT_L and 
            len(data) > self.config.EEPROM_ADDR_SKRYBA_LIMIT_H):
            limit_l = data[self.config.EEPROM_ADDR_SKRYBA_LIMIT_L]
            limit_h = data[self.config.EEPROM_ADDR_SKRYBA_LIMIT_H]
            if limit_l == 0xFF and limit_h == 0xFF:
                # Nie ustawiono - domyślnie 800
                self.skryba_limit_var.set(800)
            else:
                limit_value = limit_l | (limit_h << 8)
                # Walidacja zakresu
                if 1 <= limit_value <= 800:
                    self.skryba_limit_var.set(limit_value)
                else:
                    self.skryba_limit_var.set(800)

        # Status
        if self.config.EEPROM_ADDR_STATUS and len(data) > self.config.EEPROM_ADDR_STATUS:
            status_byte = data[self.config.EEPROM_ADDR_STATUS]
            # 0x01 = Blocked, 0x00 or 0xFF = Active
            self.status_var.set(1 if status_byte == 0x01 else 0)

        # Mode
        if self.config.EEPROM_ADDR_MODE and len(data) > self.config.EEPROM_ADDR_MODE:
            mode_byte = data[self.config.EEPROM_ADDR_MODE]
            # W C M1284P: 0=Prywatny, 1=Publiczny.
            # W starym Pythonie: 0=Prywatny, 1=Publiczny (set(0 if mode_byte == 0x00 else 1))
            self.mode_var.set(0 if mode_byte == 0x00 else 1)

        # CLIP/DTMF (0=DTMF, 1=CLIP)
        if self.config.EEPROM_ADDR_CLIP_DTMF and len(data) > self.config.EEPROM_ADDR_CLIP_DTMF:
            clip_byte = data[self.config.EEPROM_ADDR_CLIP_DTMF]
            # 0x01 = CLIP, 0x00 = DTMF, 0xFF = domyślnie CLIP
            self.clip_dtmf_var.set(1 if clip_byte != 0x00 else 0)

        # Time Control (tylko jesli zdefiniowane)
        if self.config.EEPROM_ADDR_TIME_START_H:
            # Sprawdź czy harmonogram jest włączony (czas_start_h != 0xFF)
            if len(data) > self.config.EEPROM_ADDR_TIME_START_H:
                start_h_byte = data[self.config.EEPROM_ADDR_TIME_START_H]
                if start_h_byte == 0xFF:
                    # Harmonogram wyłączony
                    self.time_enabled_var.set(0)
                    self.time_start_h_var.set("")
                    self.time_start_m_var.set("")
                    self.time_stop_h_var.set("")
                    self.time_stop_m_var.set("")
                else:
                    # Harmonogram włączony - odczytaj wartości
                    self.time_enabled_var.set(1)
                    self.time_start_h_var.set(f"{start_h_byte:02d}")
                    
                    if len(data) > self.config.EEPROM_ADDR_TIME_START_M:
                        self.time_start_m_var.set(f"{data[self.config.EEPROM_ADDR_TIME_START_M]:02d}")
                    if len(data) > self.config.EEPROM_ADDR_TIME_STOP_H:
                        self.time_stop_h_var.set(f"{data[self.config.EEPROM_ADDR_TIME_STOP_H]:02d}")
                    if len(data) > self.config.EEPROM_ADDR_TIME_STOP_M:
                        self.time_stop_m_var.set(f"{data[self.config.EEPROM_ADDR_TIME_STOP_M]:02d}")

        # MYNUM (własny numer telefonu)
        if self.config.EEPROM_ADDR_MYNUM and len(data) > self.config.EEPROM_ADDR_MYNUM + 9:
            # Odczytaj 10 bajtów (maksymalnie 9 cyfr + null terminator)
            mynum_bytes = data[self.config.EEPROM_ADDR_MYNUM:self.config.EEPROM_ADDR_MYNUM + 10]
            # Konwertuj na string, zatrzymaj się na 0x00 lub 0xFF
            mynum_str = ""
            for b in mynum_bytes:
                if b == 0x00 or b == 0xFF:
                    break
                if 48 <= b <= 57:  # ASCII cyfry 0-9
                    mynum_str += chr(b)
            self.mynum_var.set(mynum_str)

        logging.info(
            f"Read from EEPROM - Status: {self.status_var.get()}, "
            f"Mode: {self.mode_var.get()}, Skryba: {self.skryba_var.get()}, "
            f"CLIP/DTMF: {self.clip_dtmf_var.get()}"
        )

    def write_status_and_mode_to_eeprom(self, data: bytearray) -> None:
        """Zapisuje status, tryb pracy, Skryba i Time Control do EEPROM."""
        # Skryba (M1284: 1=ON, 0=OFF)
        if self.config.EEPROM_ADDR_SKRYBA:
            val = 0x01 if self.skryba_var.get() == 1 else 0x00
            data[self.config.EEPROM_ADDR_SKRYBA] = val
        
        # Skryba Limit (2 bajty: L i H)
        if self.config.EEPROM_ADDR_SKRYBA_LIMIT_L:
            limit_value = self.skryba_limit_var.get()
            data[self.config.EEPROM_ADDR_SKRYBA_LIMIT_L] = limit_value & 0xFF
            data[self.config.EEPROM_ADDR_SKRYBA_LIMIT_H] = (limit_value >> 8) & 0xFF

        # Status (0=Aktywny, 1=Blokada -> 0x00/0x01)
        if self.config.EEPROM_ADDR_STATUS:
            data[self.config.EEPROM_ADDR_STATUS] = 0x00 if self.status_var.get() == 0 else 0x01

        # Mode (M1284: 0=Prywatny, 1=Publiczny)
        if self.config.EEPROM_ADDR_MODE:
            val = 0x01 if self.mode_var.get() == 1 else 0x00
            data[self.config.EEPROM_ADDR_MODE] = val

        # CLIP/DTMF (0=DTMF, 1=CLIP)
        if self.config.EEPROM_ADDR_CLIP_DTMF:
            val = 0x01 if self.clip_dtmf_var.get() == 1 else 0x00
            data[self.config.EEPROM_ADDR_CLIP_DTMF] = val

        # Time Control
        if self.config.EEPROM_ADDR_TIME_START_H:
            if self.time_enabled_var.get() == 0:
                # Harmonogram wyłączony - zapisz 0xFF
                data[self.config.EEPROM_ADDR_TIME_START_H] = 0xFF
                data[self.config.EEPROM_ADDR_TIME_START_M] = 0xFF
                data[self.config.EEPROM_ADDR_TIME_STOP_H] = 0xFF
                data[self.config.EEPROM_ADDR_TIME_STOP_M] = 0xFF
            else:
                # Harmonogram włączony - zapisz wartości
                try:
                    data[self.config.EEPROM_ADDR_TIME_START_H] = int(self.time_start_h_var.get())
                    data[self.config.EEPROM_ADDR_TIME_START_M] = int(self.time_start_m_var.get())
                    data[self.config.EEPROM_ADDR_TIME_STOP_H] = int(self.time_stop_h_var.get())
                    data[self.config.EEPROM_ADDR_TIME_STOP_M] = int(self.time_stop_m_var.get())
                except ValueError:
                    logging.error("Invalid time values")

        # MYNUM (własny numer telefonu)
        if self.config.EEPROM_ADDR_MYNUM:
            mynum_str = self.mynum_var.get().strip()
            # Walidacja: tylko cyfry, 3-9 znaków
            if mynum_str and mynum_str.isdigit() and 3 <= len(mynum_str) <= 9:
                # Zapisz numer jako ASCII
                for i, char in enumerate(mynum_str):
                    data[self.config.EEPROM_ADDR_MYNUM + i] = ord(char)
                # Dodaj null terminator
                if len(mynum_str) < 10:
                    data[self.config.EEPROM_ADDR_MYNUM + len(mynum_str)] = 0x00
            else:
                # Wyczyść (ustaw na 0xFF)
                for i in range(10):
                    data[self.config.EEPROM_ADDR_MYNUM + i] = 0xFF

        logging.info(
            f"Write to EEPROM - Status: {self.status_var.get()}, "
            f"Mode: {self.mode_var.get()}, Skryba: {self.skryba_var.get()}, "
            f"CLIP/DTMF: {self.clip_dtmf_var.get()}"
        )

    def check_system_requirements(self) -> bool:
        """Sprawdza wymagania systemowe."""
        logging.info("Checking system requirements")
        try:
            test_file = resource_path("permission_test.tmp")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            logging.info("File permission test passed")
        except Exception as e:
            logging.error(f"File error during test: {str(e)}")
            messagebox.showerror(
                self.config.MESSAGES["error"],
                f"{self.config.MESSAGES['file_error']}: {str(e)}"
            )
            return False

        try:
            avrdude_path = self.config.AVRDUDE_PATH
            if not os.path.isfile(avrdude_path):
                logging.error(f"avrdude not found at: {avrdude_path}")
                messagebox.showerror(
                    self.config.MESSAGES["error"],
                    self.config.MESSAGES["avrdude_missing"]
                )
                return False

            logging.info(f"Attempting to run avrdude at: {avrdude_path}")
            result = subprocess.run(
                [avrdude_path, "-?"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=0x08000000 if os.name == "nt" else 0
            )
            logging.info(f"avrdude test output: {result.stdout}\n{result.stderr}")
        except Exception as e:
            logging.error(f"Unexpected error during check: {str(e)}")
            messagebox.showerror(
                self.config.MESSAGES["error"],
                f"Błąd podczas sprawdzania: {str(e)}"
            )
            return False

        return True

    def cleanup_temp_files(self) -> None:
        """Usuwa tymczasowe pliki."""
        for file_path in [self.config.EEPROM_FILE, self.config.FLASH_FILE]:
            if os.path.exists(file_path):
                try:
                    if os.name != 'nt':
                        os.chmod(file_path, 0o777)
                    os.remove(file_path)
                    logging.info(f"Removed temporary file: {file_path}")
                except Exception as e:
                    logging.error(f"Error removing temporary file {file_path}: {str(e)}")

    def run_avrdude(self, command_args: List[str]) -> Tuple[bool, str]:
        """Uruchamia avrdude z podanymi argumentami."""
        try:
            avrdude_path = self.config.AVRDUDE_PATH
            avrdude_conf = self.config.AVRDUDE_CONF

            if not os.path.isfile(avrdude_path):
                logging.error("avrdude not found during run")
                return False, self.config.MESSAGES["avrdude_missing"]

            if not os.path.isfile(avrdude_conf):
                logging.error("avrdude.conf not found during run")
                return False, "Nie znaleziono pliku avrdude.conf w folderze tools/."

            command_args_base = [
                avrdude_path,
                "-C", avrdude_conf,
                "-c", self.config.PROGRAMMER,
                "-p", self.config.MCU,
                "-b", self.config.BAUDRATE,
                "-P", self.config.PORT,
                "-B", "50"
            ]

            args_to_append = []
            for i, arg in enumerate(command_args):
                if arg == "-U" or arg == "-x":
                    args_to_append = command_args[i:]
                    break

            final_command_args = command_args_base + args_to_append

            kwargs = {}
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                kwargs = {'startupinfo': startupinfo}

            logging.info(f"Running avrdude command: {' '.join(final_command_args)}")
            result = subprocess.run(
                final_command_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
                **kwargs
            )

            full_output = result.stdout + "\n" + result.stderr
            logging.info(f"avrdude output: {full_output}")

            if result.returncode != 0:
                logging.error(f"avrdude failed with return code {result.returncode}: {full_output}")
                return False, self.config.MESSAGES["communication_error"]

            logging.info("avrdude command executed successfully")
            return True, result.stdout
        except Exception as e:
            logging.error(f"Unexpected error during avrdude run: {str(e)}")
            return False, f"{self.config.MESSAGES['process_error']}: {str(e)}"

    def format_hex_view(self, data_bytes: bytes) -> str:
        """Formatuje dane HEX do czytelnego widoku."""
        lines = []
        for addr in range(0, len(data_bytes), 16):
            chunk = data_bytes[addr:addr + 16]
            hex_chunk = " ".join(f"{b:02X}" for b in chunk)
            lines.append(f"{addr:04X}: {hex_chunk}")
        return "\n".join(lines)

    def format_hex_from_eeprom_for_display(self, data_bytes: bytes, config: Dict) -> str:
        """Formatuje odczytane dane EEPROM do czytelnego widoku GUI."""
        start = config["RANGE_START"]
        end = config["RANGE_END"]

        if len(data_bytes) <= end:
            return self.config.MESSAGES["no_data"]

        chunk = data_bytes[start:end + 1]
        hex_str = ''.join(f"{b:02X}" for b in chunk)
        hex_str = hex_str[::-1]

        if config["SKIP_F"]:
            hex_str = hex_str.replace('F', '')

        if config["NO_SPACES"]:
            return hex_str.lower()

        if len(hex_str) % 2 != 0:
            hex_str += 'F'

        return ' '.join([hex_str[i:i + 2] for i in range(0, len(hex_str), 2)]).lower()

    def format_hex_from_gui_for_eeprom(self, text_value: str, config: Dict) -> bytes:
        """Formatuje numer z GUI do postaci odwróconej (Little-Endian) do zapisu w EEPROM."""
        hex_value = text_value.replace(" ", "").strip().upper()
        if not all(c in "0123456789ABCDEF" for c in hex_value):
            raise ValueError(self.config.MESSAGES["invalid_hex"])

        if config["SKIP_F"]:
            hex_value = hex_value.replace('F', '')

        reversed_hex = hex_value[::-1]

        if len(reversed_hex) % 2 != 0:
            reversed_hex = reversed_hex + 'F'

        try:
            bytes_data = bytes.fromhex(reversed_hex)
        except ValueError:
            raise ValueError(self.config.MESSAGES["invalid_hex"])

        return bytes_data

    def parse_hex_view(self, text: str) -> bytes:
        """Parsuje tekst HEX do postaci binarnej."""
        data = []
        for line in text.strip().splitlines():
            if not line.strip():
                continue
            parts = line.split(":", 1)
            if len(parts) < 2:
                tokens = line.strip().split()
            else:
                tokens = parts[1].strip().split()
            for tok in tokens:
                if len(tok) == 0:
                    continue
                if len(tok) == 2 and all(c in "0123456789ABCDEFabcdef" for c in tok):
                    try:
                        data.append(int(tok, 16))
                    except ValueError:
                        continue
        return bytes(data)

    @staticmethod
    def compute_checksum_twos_complement(data_without_checksum: bytes) -> int:
        """Oblicza sumę kontrolną metodą uzupełnienia do dwóch."""
        s = sum(data_without_checksum) & 0xFF
        return (-s) & 0xFF

    def recalc_and_apply_checksum(self, data: bytearray) -> None:
        """Przelicza i aplikuje sumę kontrolną na adresie 0."""
        if len(data) == 0:
            return
        if len(data) == 1:
            data[0] = self.compute_checksum_twos_complement(b"")
            return
        chk = self.compute_checksum_twos_complement(bytes(data[1:]))
        data[0] = chk

    @staticmethod
    def bytes_to_ascii_preview(bs: bytes) -> str:
        """Konwertuje bajty na czytelny tekst ASCII."""
        out = []
        for b in bs:
            ch = chr(b)
            if ch in string.printable and ch not in "\t\r\x0b\x0c":
                out.append(ch)
            else:
                out.append('.')
        return ''.join(out)

    def apply_ascii_to_data(self, data: bytearray, ascii_text: str) -> None:
        """Aplikuje tekst ASCII do danych (adresy 0x01 - 0x04)."""
        if len(data) < 5:
            return
        chars = list(ascii_text[:4])
        while len(chars) < 4:
            chars.append('\x00')
        for i, ch in enumerate(chars):
            data[0x01 + i] = ord(ch)

    def update_numbers_text(self, data: bytes) -> None:
        """Aktualizuje tekst z numerami na podstawie danych."""
        lines = []
        for config in self.hex_configs:
            hex_content = self.format_hex_from_eeprom_for_display(data, config)
            lines.append(f"{config['NAME']}; {hex_content}")
        self.numbers_text.delete(1.0, tk.END)
        self.numbers_text.insert(tk.END, "\n".join(lines))

    def update_ascii_field_from_data(self, data: bytes) -> None:
        """Aktualizuje pole ASCII na podstawie danych."""
        if len(data) >= 5:
            ascii_text = self.bytes_to_ascii_preview(data[0x01:0x05])
            self.ascii_var.set(ascii_text)
        else:
            self.ascii_var.set("")

    def clear_hex_data(self) -> None:
        """Czyści dane HEX w GUI."""
        data = bytearray([0xFF] * self.config.EEPROM_SIZE)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.format_hex_view(data))
        self.update_ascii_field_from_data(data)
        self.update_numbers_text(data)
        self.status_var.set(0)
        self.mode_var.set(1)
        self.clip_dtmf_var.set(1)  # Domyślnie CLIP
        self.skryba_var.set(0)  # Domyślnie wyłączona

    def sync_from_numbers_list(self) -> bool:
        """Synchronizuje dane z listy numerów. Zwraca True jeśli sukces, False jeśli błąd."""
        try:
            data = bytearray(self.parse_hex_view(self.text_area.get(1.0, tk.END)))
            lines = self.numbers_text.get(1.0, tk.END).strip().splitlines()
            name_to_config = {c['NAME']: c for c in self.hex_configs}

            for line in lines:
                if ':' not in line:
                    continue
                name, value = line.split(':', 1)
                name = name.strip()
                value = value.strip().replace(" ", "")

                if not value:
                    continue

                if not self.validate_number_input(value):
                    messagebox.showerror(
                        self.config.MESSAGES["error"],
                        f"Nieprawidłowy numer w pozycji {name}!\nNumer musi mieć od 3 do 9 cyfr (0-9)."
                    )
                    return False

                if name not in name_to_config:
                    continue
                config = name_to_config[name]

                try:
                    bytes_data = self.format_hex_from_gui_for_eeprom(value, config)
                except ValueError as e:
                    messagebox.showerror(self.config.MESSAGES["error"], str(e))
                    return False

                start = config["RANGE_START"]
                end = config["RANGE_END"]
                required_length = end - start + 1
                if len(bytes_data) > required_length:
                    bytes_data = bytes_data[:required_length]
                elif len(bytes_data) < required_length:
                    bytes_data = bytes_data + bytes([0xFF] * (required_length - len(bytes_data)))
                data[start:start + len(bytes_data)] = bytes_data

            self.recalc_and_apply_checksum(data)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, self.format_hex_view(data))
            return True
        except Exception as e:
            logging.error(f"Error in sync_from_numbers_list: {str(e)}")
            messagebox.showerror(
                self.config.MESSAGES["error"],
                f"{self.config.MESSAGES['process_error']}: {e}"
            )
            return False

    def sync_ascii_into_textarea(self) -> bool:
        """Synchronizuje tekst ASCII do obszaru tekstowego. Zwraca True jeśli sukces."""
        try:
            data = bytearray(self.parse_hex_view(self.text_area.get(1.0, tk.END)))
            ascii_text = self.ascii_var.get().strip()
            if len(ascii_text) != 4:
                messagebox.showerror(
                    self.config.MESSAGES["error"],
                    "Kod dostępu musi mieć dokładnie 4 znaki!"
                )
                return False

            if not all(c in string.printable for c in ascii_text):
                messagebox.showerror(
                    self.config.MESSAGES["error"],
                    self.config.MESSAGES["invalid_chars"]
                )
                return False
            self.apply_ascii_to_data(data, ascii_text)
            self.recalc_and_apply_checksum(data)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, self.format_hex_view(data))
            self.update_ascii_field_from_data(data)
            self.update_numbers_text(data)
            return True
        except Exception as e:
            logging.error(f"Error in sync_ascii_into_textarea: {str(e)}")
            messagebox.showerror(
                self.config.MESSAGES["error"],
                f"{self.config.MESSAGES['process_error']}: {e}"
            )
            return False

    def show_about(self) -> None:
        """Wyświetla okno 'O programie'."""
        about_window = tk.Toplevel(self.root)
        about_window.title("O programie")
        about_window.geometry("250x250")

        tk.Label(
            about_window,
            text=self.config.ABOUT_INFO,
            justify=tk.CENTER
        ).pack(padx=10, pady=10, expand=True)

        try:
            #logo_path = resource_path("graphics/logo.png")
           # self.about_logo = tk.PhotoImage(file=logo_path)
            tk.Label(
                about_window,
                image=self.about_logo
            ).pack(pady=(0, 20))
        except Exception as e:
            logging.error(f"Error loading logo: {str(e)}")

        tk.Button(
            about_window,
            text="OK",
            command=about_window.destroy
        ).pack(pady=10)

    def flash_firmware(self) -> None:
        """Otwiera okno wyboru pliku .dat i flashuje firmware."""
        self.update_com_port()

        hex_path = filedialog.askopenfilename(filetypes=[
            ("Pliki Firmware (DAT)", "*.dat"),
            ("Wszystkie pliki", "*.*")
        ])
        if not hex_path:
            return

        # 1. Pobierz aktualne dane konfiguracyjne z GUI (snapshot przed wątkiem)
        try:
            # Synchronizacja ASCII
            if not self.sync_ascii_into_textarea():
                return
                
            # Synchronizacja listy numerów
            if not self.sync_from_numbers_list():
                return
                
            current_data = bytearray(self.parse_hex_view(self.text_area.get(1.0, tk.END)))
            
            # Aktualizacja statusów w buforze
            self.write_status_and_mode_to_eeprom(current_data)
            
            # Zabezpieczenie danych (OUT=0, długość)
            if len(current_data) >= 8:
                current_data[5] = 0x00
                current_data[6] = 0x00
                current_data[7] = 0x00
                
            if len(current_data) == self.config.EEPROM_SIZE:
                # Zapisz "backup" do pliku tymczasowego (ten sam plik co przy normalnym zapisie)
                try:
                    with open(self.config.EEPROM_FILE, "wb") as f:
                        f.write(current_data)
                    logging.info("Configuration backed up to temporary file before flash.")
                except Exception as e:
                    logging.error(f"Failed to backup configuration: {e}")
                    # Nie przerywamy, bo użytkownik chce wgrać firmware, ale warto zalogować
            
        except Exception as e:
            logging.error(f"Error preparing configuration backup: {e}")
            if not messagebox.askyesno("Ostrzeżenie", "Nie udało się przygotować kopii zapasowej ustawień.\nCzy mimo to kontynuować aktualizację firmware?"):
                return

        def worker():
            try:
                self.pulse_dtr()
                self.progress_manager.start()

                try:
                    shutil.copy(hex_path, self.config.FLASH_FILE)
                except Exception as e:
                    logging.error(f"Error copying DAT file: {str(e)}")
                    self.result_queue.put((False, f"Błąd kopiowania pliku: {e}", None))
                    return

                command_args = [
                    self.config.AVRDUDE_PATH,
                    "-C", self.config.AVRDUDE_CONF,
                    "-c", self.config.PROGRAMMER,
                    "-p", self.config.MCU,
                    "-b", self.config.BAUDRATE,
                    "-P", self.config.PORT,
                    "-x", "delay=100",
                    "-x", "strict",
                    "-U", f"flash:w:{self.config.FLASH_FILE}:i"
                ]

                success, output = self.run_avrdude(command_args)

                if success:
                    post_flash_progress = PostFlashProgressManager(self.root, duration_sec=27)
                    self.root.after(0, post_flash_progress.start)
                    self.root.update_idletasks()
                    time.sleep(27)

                    if post_flash_progress.running:
                        self.root.after(0, post_flash_progress.stop)

                    message = "Aktualizacja firmware zakończona pomyślnie!"
                else:
                    message = f"Błąd aktualizacji oprogramowania ({self.config.MCU}):\n{output}"

                self.result_queue.put((success, message, None))

            except Exception as e:
                logging.error(f"Error in flash_firmware: {str(e)}")
                self.result_queue.put((False, f"Błąd procesu aktualizacji: {e}", None))
            finally:
                self.progress_manager.stop()
                if os.path.exists(self.config.FLASH_FILE):
                    os.remove(self.config.FLASH_FILE)

        threading.Thread(target=worker, daemon=True).start()

    def odczyt_eeprom(self) -> None:
        """Odczytuje dane z EEPROM."""
        self.update_com_port()

        def worker():
            try:
                self.pulse_dtr()
                self.progress_manager.start()
                self.cleanup_temp_files()

                command_args = [
                    self.config.AVRDUDE_PATH,
                    "-C", self.config.AVRDUDE_CONF,
                    "-c", self.config.PROGRAMMER,
                    "-p", self.config.MCU,
                    "-b", self.config.BAUDRATE,
                    "-P", self.config.PORT,
                    "-x", "delay=100",
                    "-x", "strict",
                    "-U", f"eeprom:r:{self.config.EEPROM_FILE}:r"
                ]

                success, output = self.run_avrdude(command_args)

                if not success:
                    self.result_queue.put((False, output, None))
                    return

                try:
                    if not os.path.exists(self.config.EEPROM_FILE):
                        logging.error(f"EEPROM file not found: {self.config.EEPROM_FILE}")
                        self.result_queue.put((False, self.config.MESSAGES["file_error"], None))
                        return

                    with open(self.config.EEPROM_FILE, "rb") as f:
                        data = bytearray(f.read(self.config.EEPROM_SIZE))

                    if len(data) != self.config.EEPROM_SIZE:
                        logging.error(
                            f"Invalid EEPROM data length: {len(data)} (Expected: {self.config.EEPROM_SIZE})"
                        )
                        self.result_queue.put((False, "Nieprawidłowa długość danych", None))
                        return

                    self.result_queue.put((True, self.config.MESSAGES["chip_read"], {'data': data}))
                except Exception as e:
                    logging.error(f"Error reading EEPROM file: {str(e)}")
                    self.result_queue.put((False, f"{self.config.MESSAGES['file_error']}: {e}", None))
                finally:
                    self.cleanup_temp_files()
            except Exception as e:
                logging.error(f"Error in odczyt_eeprom: {str(e)}")
                self.result_queue.put((False, f"{self.config.MESSAGES['process_error']}: {e}", None))
            finally:
                self.progress_manager.stop()

        threading.Thread(target=worker, daemon=True).start()

    def zapis_eeprom(self) -> None:
        """Zapisuje dane do EEPROM."""
        # Okno dialogowe z potwierdzeniem
        if not messagebox.askokcancel(
            "Potwierdzenie zapisu",
            "Zapisane zostaną dane widoczne w aplikacji.\n"
            "(Uprzednio wprowadzone ręcznie i wczytane z CSV)\n\n"
            "Upewnij się, że wszystkie ustawienia są poprawne.\n\n"
            "Czy kontynuować zapis do sterownika?"
        ):
            return
        
        self.update_com_port()

        # 1. Walidacja i synchronizacja danych (w wątku głównym)
        if not self.sync_from_numbers_list():
            return  # Błąd walidacji, przerywamy (pasek nie startuje)
        
        if not self.sync_ascii_into_textarea():
            return  # Błąd walidacji ASCII, przerywamy

        # Walidacja Harmonogramu
        if self.time_enabled_var.get() == 1:
            try:
                sh = int(self.time_start_h_var.get())
                sm = int(self.time_start_m_var.get())
                eh = int(self.time_stop_h_var.get())
                em = int(self.time_stop_m_var.get())
                
                if not (0 <= sh <= 23 and 0 <= sm <= 59 and 0 <= eh <= 23 and 0 <= em <= 59):
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    self.config.MESSAGES["error"],
                    "Nieprawidłowe godziny harmonogramu!\nUzupełnij wszystkie pola (HH:MM) lub odznacz 'Aktywuj harmonogram'."
                )
                return

        # Pobierz dane w wątku głównym (bezpiecznie dla Tkinter)
        try:
            current_data = bytearray(self.parse_hex_view(self.text_area.get(1.0, tk.END)))
        except Exception as e:
            logging.error(f"Error reading data from GUI: {e}")
            messagebox.showerror("Błąd", "Nie udało się pobrać danych z interfejsu.")
            return

        def worker(data_to_write):
            try:
                self.pulse_dtr()
                self.progress_manager.start()

                # 3. Zapisz status/tryb/CLIP-DTMF/Time do bufora
                self.write_status_and_mode_to_eeprom(data_to_write)

                # 4. Zaktualizuj GUI ?? Nie możemy z wątku.
                # Ale dane są już zaktualizowane w data_to_write.
                # Możemy użyć schedule_update_gui jeśli byśmy chcieli,
                # ale tutaj ważniejszy jest zapis do pliku.
                
                # 5. Używamy danych przekazanych do workera
                data = data_to_write

                # Zabezpieczenie: OUT zawsze wyłączone (5–7 = 0)
                if len(data) >= 8:
                    data[5] = 0x00
                    data[6] = 0x00
                    data[7] = 0x00

                if len(data) != self.config.EEPROM_SIZE:
                    logging.error(
                        f"Invalid data length for EEPROM write: {len(data)} (Expected: {self.config.EEPROM_SIZE})"
                    )
                    self.result_queue.put((False, "Nieprawidłowa długość danych", None))
                    return

                try:
                    with open(self.config.EEPROM_FILE, "wb") as f:
                        f.write(data)
                except PermissionError:
                    logging.error("Permission error writing EEPROM file")
                    self.result_queue.put((False, self.config.MESSAGES["permission_error"], None))
                    return

                command_args = [
                    self.config.AVRDUDE_PATH,
                    "-C", self.config.AVRDUDE_CONF,
                    "-c", self.config.PROGRAMMER,
                    "-p", self.config.MCU,
                    "-b", self.config.BAUDRATE,
                    "-P", self.config.PORT,
                    "-x", "delay=100",
                    "-x", "strict",
                    "-U", f"eeprom:w:{self.config.EEPROM_FILE}:r"
                ]

                success, output = self.run_avrdude(command_args)
                
                # Przekazujemy zaktualizowane dane z powrotem do głównego wątku, aby odświeżyć GUI
                self.result_queue.put((True, self.config.MESSAGES["chip_written"] if success else output, {'data': data}))

            except Exception as e:
                logging.error(f"Error in zapis_eeprom: {str(e)}")
                self.result_queue.put((False, f"{self.config.MESSAGES['process_error']}: {e}", None))
            finally:
                self.progress_manager.stop()
                self.cleanup_temp_files()

        threading.Thread(target=worker, args=(current_data,), daemon=True).start()

    def odczyt_z_csv(self) -> None:
        """Odczytuje dane z pliku CSV (kod, status, tryb, skryba, czas + numery)."""
        file_path = filedialog.askopenfilename(filetypes=[("Pliki CSV", "*.csv")])
        if not file_path:
            return

        def worker():
            self.progress_manager.start()
            try:
                data = bytearray(self.parse_hex_view(self.text_area.get(1.0, tk.END)))
                if len(data) < self.config.EEPROM_SIZE:
                    data = bytearray([0xFF] * self.config.EEPROM_SIZE)

                csv_data: Dict[str, str] = {}
                kod_dostepu_text: Optional[str] = None
                status_text: Optional[str] = None
                mode_text: Optional[str] = None
                clip_dtmf_text: Optional[str] = None
                skryba_text: Optional[str] = None
                time_text: Optional[str] = None

                with open(file_path, "r", encoding="utf-8") as f:
                    # Czytamy nagłówki (pierwsze kilka linii)
                    # Format: Klucz, Wartość
                    # Moze byc rozna kolejnosc, wiec czytamy do pustej linii lub naglowka "Pozycja"
                    
                    # Proste podejscie: czytamy linie po kolei
                    line = f.readline()
                    while line and not line.startswith("Pozycja;"):
                        if ";" in line:
                            key, val = line.strip().split(";", 1)
                            if key == "Kod dostępu":
                                kod_dostepu_text = val
                            elif key == "Status":
                                status_text = val
                            elif key == "Tryb":
                                mode_text = val
                            elif key == "Tryb sterowania":
                                clip_dtmf_text = val
                            elif key == "Funkcja Skryba":
                                skryba_text = val
                            elif key == "Kontrola Czasu":
                                time_text = val
                        line = f.readline()
                    
                    # Teraz powinnismy byc przy naglowku tabeli
                    if not line.startswith("Pozycja;"):
                         # Jesli nie znalezlismy naglowka, szukamy dalej
                         line = f.readline()
                         while line and not line.startswith("Pozycja;"):
                             line = f.readline()

                    if line and line.startswith("Pozycja;"):
                        reader = csv.reader(f, delimiter=';')
                        for row in reader:
                            if len(row) >= 2:
                                csv_data[row[0]] = row[1]
                    else:
                        # Fallback dla starych plikow bez naglowkow
                        f.seek(0)
                        reader = csv.DictReader(f, delimiter=';')
                        # Walidacja nagłówków dla DictReader
                        if not reader.fieldnames or "Pozycja" not in reader.fieldnames or "Numer" not in reader.fieldnames:
                             self.result_queue.put((False, "Nieprawidłowy format pliku CSV.\nWymagane kolumny: 'Pozycja', 'Numer'.", None))
                             return

                        for row in reader:
                            if "Pozycja" in row and "Numer" in row:
                                csv_data[row["Pozycja"]] = row["Numer"]

                if kod_dostepu_text:
                    self.ascii_var.set(kod_dostepu_text)
                    self.apply_ascii_to_data(data, kod_dostepu_text)

                if status_text:
                    if status_text == self.config.LABELS["status_active"]:
                        self.status_var.set(0)
                    elif status_text == self.config.LABELS["status_blocked"]:
                        self.status_var.set(1)

                if mode_text:
                    if mode_text == self.config.LABELS["mode_private"]:
                        self.mode_var.set(0)
                    elif mode_text == self.config.LABELS["mode_public"]:
                        self.mode_var.set(1)

                if clip_dtmf_text:
                    if clip_dtmf_text == "CLIP":
                        self.clip_dtmf_var.set(1)
                    elif clip_dtmf_text == "DTMF":
                        self.clip_dtmf_var.set(0)

                if skryba_text:
                    # Kompatybilnosc: Wlaczona -> 1, Wylaczona -> 0
                    if skryba_text == self.config.LABELS["control_clip"] or skryba_text == "Włączona":
                        self.skryba_var.set(1)
                    elif skryba_text == self.config.LABELS["control_dtmf"] or skryba_text == "Wyłączona":
                        self.skryba_var.set(0)
                
                if time_text:
                    # Format: HH:MM - HH:MM lub "Wylaczony"
                    if time_text == "Wylaczony":
                        self.time_enabled_var.set(0)
                        self.time_start_h_var.set("00")
                        self.time_start_m_var.set("00")
                        self.time_stop_h_var.set("00")
                        self.time_stop_m_var.set("00")
                    else:
                        try:
                            start, stop = time_text.split("-")
                            start_h, start_m = start.strip().split(":")
                            stop_h, stop_m = stop.strip().split(":")
                            self.time_enabled_var.set(1)
                            self.time_start_h_var.set(start_h)
                            self.time_start_m_var.set(start_m)
                            self.time_stop_h_var.set(stop_h)
                            self.time_stop_m_var.set(stop_m)
                        except ValueError:
                            logging.error(f"Error parsing time from CSV: {time_text}")

                self.write_status_and_mode_to_eeprom(data)

                lines_out: List[str] = []
                for config in self.hex_configs:
                    name = config["NAME"]
                    value = csv_data.get(name, "")
                    if value == "Brak danych":
                        value = ""

                    if value:
                        clean = value.replace(" ", "").strip()
                        if not self.validate_number_input(clean):
                            self.result_queue.put(
                                (
                                    False,
                                    f"Nieprawidłowy numer w pozycji {name}!\nNumer musi mieć od 3 do 9 cyfr (0-9).",
                                    None,
                                )
                            )
                            return

                        hex_value = clean.upper()
                        if not all(c in "0123456789ABCDEF" for c in hex_value):
                            continue
                        if config["SKIP_F"]:
                            hex_value = hex_value.replace("F", "")
                        reversed_hex = hex_value[::-1]
                        if len(reversed_hex) % 2 != 0:
                            reversed_hex = reversed_hex + "F"
                        try:
                            bytes_data = bytes.fromhex(reversed_hex)
                        except ValueError:
                            continue
                        start = config["RANGE_START"]
                        end = config["RANGE_END"]
                        required_length = end - start + 1
                        if len(bytes_data) > required_length:
                            bytes_data = bytes_data[:required_length]
                        elif len(bytes_data) < required_length:
                            bytes_data = bytes_data + bytes([0xFF] * (required_length - len(bytes_data)))
                        data[start:start + len(bytes_data)] = bytes_data
                        lines_out.append(f"{name}; {clean}")
                    else:
                        start = config["RANGE_START"]
                        end = config["RANGE_END"]
                        for addr in range(start, end + 1):
                            if addr < len(data):
                                data[addr] = 0xFF
                        lines_out.append(f"{name}; ")

                # Bezpieczny stan wyjścia OUT
                if len(data) >= 8:
                    data[5] = 0x00
                    data[6] = 0x00
                    data[7] = 0x00

                self.recalc_and_apply_checksum(data)
                self.result_queue.put(
                    (True, self.config.MESSAGES["csv_loaded"], {"data": data, "text": "\n".join(lines_out)})
                )
            except Exception as e:
                logging.error(f"Error in odczyt_z_csv: {str(e)}")
                self.result_queue.put((False, f"{self.config.MESSAGES['file_error']}: {e}", None))
            finally:
                self.progress_manager.stop()

        threading.Thread(target=worker, daemon=True).start()

    def zapis_do_csv(self) -> None:
        """Zapisuje dane do pliku CSV (kod, status, tryb, sterowanie + numery)."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Pliki CSV", "*.csv")]
        )
        if not file_path:
            return

        def worker():
            self.progress_manager.start()
            try:
                lines = self.numbers_text.get(1.0, tk.END).strip().splitlines()
                name_to_value: Dict[str, str] = {}
                for line in lines:
                    if ';' in line:
                        name, value = line.split(';', 1)
                        name = name.strip()
                        value = value.strip()
                        name_to_value[name] = value if value else "Brak danych"

                with open(file_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f, delimiter=';')

                    kod_dostepu_text = self.ascii_var.get()
                    status_text = self.get_status_text(self.status_var.get())
                    mode_text = self.get_mode_text(self.mode_var.get())
                    clip_dtmf_text = "CLIP" if self.clip_dtmf_var.get() == 1 else "DTMF"
                    skryba_text = self.get_skryba_text(self.skryba_var.get())
                    
                    # Format czasu: HH:MM - HH:MM lub "Wylaczony"
                    if self.time_enabled_var.get() == 0:
                        time_text = "Wylaczony"
                    else:
                        time_text = f"{self.time_start_h_var.get()}:{self.time_start_m_var.get()} - {self.time_stop_h_var.get()}:{self.time_stop_m_var.get()}"

                    writer.writerow(["Kod dostępu", kod_dostepu_text])
                    writer.writerow(["Status", status_text])
                    writer.writerow(["Tryb", mode_text])
                    writer.writerow(["Tryb sterowania", clip_dtmf_text])
                    writer.writerow(["Funkcja Skryba", skryba_text])
                    writer.writerow(["Kontrola Czasu", time_text])
                    writer.writerow([])
                    writer.writerow(["Pozycja", "Numer"])

                    for config in self.hex_configs:
                        value = name_to_value.get(config["NAME"], "Brak danych")
                        writer.writerow([config["NAME"], value])

                self.result_queue.put((True, self.config.MESSAGES["csv_saved"], None))
            except Exception as e:
                logging.error(f"Error in zapis_do_csv: {str(e)}")
                self.result_queue.put((False, f"{self.config.MESSAGES['file_error']}: {e}", None))
            finally:
                self.progress_manager.stop()

        threading.Thread(target=worker, daemon=True).start()

    def clear_all_numbers(self) -> None:
        """Czyści wszystkie numery (nie rusza kodu, statusu, trybu, CLIP/DTMF)."""

        def worker():
            self.progress_manager.start()
            try:
                current_data = self.text_area.get(1.0, tk.END)
                data = bytearray(self.parse_hex_view(current_data))

                if len(data) < self.config.EEPROM_SIZE:
                    data = bytearray([0xFF] * self.config.EEPROM_SIZE)

                for config in self.hex_configs:
                    start = config["RANGE_START"]
                    end = config["RANGE_END"]
                    if end < len(data):
                        for i in range(start, end + 1):
                            data[i] = 0xFF

                self.recalc_and_apply_checksum(data)
                self.result_queue.put((True, self.config.MESSAGES["all_cleared"], {"data": data}))
            except Exception as e:
                logging.error(f"Error in clear_all_numbers: {str(e)}")
                self.result_queue.put((False, f"{self.config.MESSAGES['process_error']}: {e}", None))
            finally:
                self.progress_manager.stop()

        threading.Thread(target=worker, daemon=True).start()

    def show_result(self) -> None:
        """Wyświetla wyniki operacji z kolejki."""
        while not self.result_queue.empty():
            success, message, update_data = self.result_queue.get()

            hidden_messages = [
                self.config.MESSAGES["access_code_updated"],
                self.config.MESSAGES["update_success"],
                self.config.MESSAGES["chip_written"],
                self.config.MESSAGES["csv_saved"],
                self.config.MESSAGES["file_saved"],
                self.config.MESSAGES["chip_read"],
                self.config.MESSAGES["csv_loaded"],
                self.config.MESSAGES["all_cleared"],
                self.config.MESSAGES["status_updated"],
                self.config.MESSAGES["mode_updated"],
            ]

            should_show_message = message not in hidden_messages

            if success:
                if update_data:
                    if "data" in update_data:
                        data = update_data["data"]
                        self.text_area.delete(1.0, tk.END)
                        self.text_area.insert(tk.END, self.format_hex_view(data))
                        self.update_ascii_field_from_data(data)
                        self.update_numbers_text(data)
                        self.read_status_and_mode_from_eeprom(data)
                    if "text" in update_data:
                        self.numbers_text.delete(1.0, tk.END)
                        self.numbers_text.insert(tk.END, update_data["text"])

                if should_show_message:
                    messagebox.showinfo(self.config.MESSAGES["info"], message)
            else:
                messagebox.showerror(self.config.MESSAGES["error"], message)

        self.root.after(100, self.show_result)

    def setup_ui(self) -> None:
        """Konfiguruje interfejs użytkownika."""
        self.root.title(self.config.WINDOW_TITLE)
        self.root.geometry(self.config.WINDOW_SIZE)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Ustawienie domyślnej czcionki dla całej aplikacji
        default_font = ("TkDefaultFont", 10)
        self.root.option_add("*Font", default_font)

        try:
            icon_path = resource_path("graphics/logo.png")
            if os.path.exists(icon_path):
                self.icon_photo = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, self.icon_photo)
        except Exception as e:
            logging.error(f"Error setting icon: {str(e)}")

        self.progress_manager = ProgressManager(self.root, self.config)

        frame_config = tk.Frame(self.root)
        frame_config.pack(fill="x", padx=10, pady=8)

        frame_com_port = tk.LabelFrame(frame_config, text=self.config.LABELS["com_port"])
        frame_com_port.pack(side="left", padx=(0, 5), expand=True, fill="x")

        com_ports = self.get_available_com_ports()
        self.com_port_combobox = ttk.Combobox(
            frame_com_port,
            textvariable=self.com_port_var,
            values=com_ports,
            width=10,
            state="readonly"
        )
        self.com_port_combobox.pack(padx=8, pady=8, fill="x", expand=True)

        if self.config.PORT in com_ports:
            self.com_port_combobox.set(self.config.PORT)
        else:
            self.com_port_combobox.set(com_ports[0] if com_ports else "COM3")

        # Processor selection removed - only AC800 supported

        # --- Układ 2x2 dla kontrolek ---
        frame_controls = tk.Frame(self.root)
        frame_controls.pack(fill="x", padx=10, pady=8)
        
        # Konfiguracja kolumn i wierszy - uniform zapewnia identyczny rozmiar
        frame_controls.columnconfigure(0, weight=1, uniform="controls")
        frame_controls.columnconfigure(1, weight=1, uniform="controls")
        frame_controls.rowconfigure(0, weight=1, uniform="rows")
        frame_controls.rowconfigure(1, weight=1, uniform="rows")

        # Wiersz 1, Kolumna 1: Status sterownika
        self.frame_status = tk.LabelFrame(frame_controls, text=self.config.LABELS["status_control"])
        self.frame_status.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky="nsew")

        self.check_status_active = tk.Radiobutton(
            self.frame_status,
            text=self.config.LABELS["status_active"],
            variable=self.status_var,
            value=0
        )
        self.check_status_active.pack(side="left", padx=8, pady=8)

        self.check_status_blocked = tk.Radiobutton(
            self.frame_status,
            text=self.config.LABELS["status_blocked"],
            variable=self.status_var,
            value=1
        )
        self.check_status_blocked.pack(side="left", padx=8, pady=8)

        # Wiersz 1, Kolumna 2: Tryb pracy
        self.frame_mode = tk.LabelFrame(frame_controls, text=self.config.LABELS["mode_control"])
        self.frame_mode.grid(row=0, column=1, padx=(5, 0), pady=(0, 5), sticky="nsew")

        self.check_mode_private = tk.Radiobutton(
            self.frame_mode,
            text=self.config.LABELS["mode_private"],
            variable=self.mode_var,
            value=0
        )
        self.check_mode_private.pack(side="left", padx=8, pady=8)

        self.check_mode_public = tk.Radiobutton(
            self.frame_mode,
            text=self.config.LABELS["mode_public"],
            variable=self.mode_var,
            value=1
        )
        self.check_mode_public.pack(side="left", padx=8, pady=8)

        # Wiersz 2, Kolumna 1: Tryb sterowania CLIP/DTMF
        self.frame_clip_dtmf = tk.LabelFrame(frame_controls, text=self.config.LABELS["clip_dtmf_mode"])
        self.frame_clip_dtmf.grid(row=1, column=0, padx=(0, 5), pady=(5, 0), sticky="nsew")

        self.check_clip = tk.Radiobutton(
            self.frame_clip_dtmf,
            text=self.config.LABELS["clip_mode"],
            variable=self.clip_dtmf_var,
            value=1
        )
        self.check_clip.pack(side="left", padx=8, pady=8)

        self.check_dtmf = tk.Radiobutton(
            self.frame_clip_dtmf,
            text=self.config.LABELS["dtmf_mode"],
            variable=self.clip_dtmf_var,
            value=0
        )
        self.check_dtmf.pack(side="left", padx=8, pady=8)

        # Wiersz 2, Kolumna 2: Funkcja Skryba
        self.frame_clip = tk.LabelFrame(frame_controls, text=self.config.LABELS["control_mode"])
        self.frame_clip.grid(row=1, column=1, padx=(5, 0), pady=(5, 0), sticky="nsew")

        self.check_skryba_on = tk.Radiobutton(
            self.frame_clip,
            text=self.config.LABELS["control_clip"],
            variable=self.skryba_var,
            value=1
        )
        self.check_skryba_on.pack(side="left", padx=8, pady=8)

        self.check_skryba_off = tk.Radiobutton(
            self.frame_clip,
            text=self.config.LABELS["control_dtmf"],
            variable=self.skryba_var,
            value=0
        )
        self.check_skryba_off.pack(side="left", padx=8, pady=8)

        # --- Time Control Frame ---
        # Zapisujemy referencje, aby móc ukrywać/pokazywać
        self.frame_time = tk.LabelFrame(self.root, text=self.config.LABELS["time_control"])
        self.frame_time.pack(fill="x", padx=10, pady=8)
         
        
        # Checkbox aktywacji harmonogramu
        self.check_time_enabled = tk.Checkbutton(
            self.frame_time,
            text="Aktywuj harmonogram",
            variable=self.time_enabled_var
        )
        self.check_time_enabled.pack(side="left", padx=8, pady=8)
        
        # Rejestracja funkcji walidacji
        vcmd_hour = (self.root.register(self.validate_hour), '%P')
        vcmd_minute = (self.root.register(self.validate_minute), '%P')

        tk.Label(self.frame_time, text="Start:").pack(side="left", padx=5)
        self.spin_start_h = tk.Spinbox(
            self.frame_time, from_=0, to=23, width=3,
            textvariable=self.time_start_h_var, format="%02.0f",
            validate="key", validatecommand=vcmd_hour
        )
        self.spin_start_h.pack(side="left")
        tk.Label(self.frame_time, text=":").pack(side="left")
        self.spin_start_m = tk.Spinbox(
            self.frame_time, from_=0, to=59, width=3,
            textvariable=self.time_start_m_var, format="%02.0f",
            validate="key", validatecommand=vcmd_minute
        )
        self.spin_start_m.pack(side="left")

        tk.Label(self.frame_time, text="  Stop:").pack(side="left", padx=5)
        self.spin_stop_h = tk.Spinbox(
            self.frame_time, from_=0, to=23, width=3,
            textvariable=self.time_stop_h_var, format="%02.0f",
            validate="key", validatecommand=vcmd_hour
        )
        self.spin_stop_h.pack(side="left")
        tk.Label(self.frame_time, text=":").pack(side="left")
        self.spin_stop_m = tk.Spinbox(
            self.frame_time, from_=0, to=59, width=3,
            textvariable=self.time_stop_m_var, format="%02.0f",
            validate="key", validatecommand=vcmd_minute
        )
        self.spin_stop_m.pack(side="left")
        # --------------------------

        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(fill="x", pady=5)
        
        # Konfiguracja kolumn i wierszy - uniform zapewnia identyczny rozmiar
        frame_buttons.columnconfigure(0, weight=1, uniform="btns")
        frame_buttons.columnconfigure(1, weight=1, uniform="btns")
        frame_buttons.columnconfigure(2, weight=1, uniform="btns")
        frame_buttons.rowconfigure(0, weight=1, uniform="btnrows")
        frame_buttons.rowconfigure(1, weight=1, uniform="btnrows")
        frame_buttons.rowconfigure(3, weight=1, uniform="btnrows")

        btn_font = ("TkDefaultFont", 10)
        
        self.btn_read_chip = tk.Button(
            frame_buttons,
            text=self.config.BUTTONS["read_chip"],
            command=self.odczyt_eeprom,
            width=30,
            height=2,
            font=btn_font
        )
        self.btn_write_chip = tk.Button(
            frame_buttons,
            text=self.config.BUTTONS["write_chip"],
            command=self.zapis_eeprom,
            width=30,
            height=2,
            font=btn_font
        )
        self.btn_buy_now = tk.Button(
            frame_buttons,
            text=self.config.BUTTONS["buy_now"],
            command=self.flash_firmware,
            width=15,
            height=2,
            font=btn_font
        )
        self.btn_save_csv = tk.Button(
            frame_buttons,
            text=self.config.BUTTONS["save_csv"],
            command=self.zapis_do_csv,
            width=30,
            height=2,
            font=btn_font
        )
        self.btn_read_csv = tk.Button(
            frame_buttons,
            text=self.config.BUTTONS["read_csv"],
            command=self.odczyt_z_csv,
            width=30,
            height=2,
            font=btn_font
        )

        self.btn_about = tk.Button(
            frame_buttons,
            text=self.config.BUTTONS["about"],
            command=self.show_about,
            width=15,
            height=2,
            font=btn_font
        )

        self.btn_read_chip.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.btn_write_chip.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.btn_buy_now.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.btn_about.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        self.btn_save_csv.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.btn_read_csv.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Przyciski clear_all i sync_numbers usunięte na żądanie użytkownika.


        # Kontener dla ramek obok siebie
        container_frames = tk.Frame(self.root)
        container_frames.pack(fill="x", padx=10, pady=8)

        # Ramka kodu dostępu (po lewej)
        frame_ascii = tk.LabelFrame(container_frames, text=self.config.LABELS["access_code"])
        frame_ascii.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.entry_ascii = tk.Entry(
            frame_ascii,
            textvariable=self.ascii_var,
            width=20
        )
        self.entry_ascii.grid(row=0, column=0, padx=8, pady=8)

        self.entry_ascii.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
        frame_ascii.columnconfigure(0, weight=1)

        # Ramka numeru karty SIM (po prawej)
        frame_mynum = tk.LabelFrame(container_frames, text="Numer karty SIM w sterowniku")
        frame_mynum.pack(side="left", fill="both", expand=True, padx=(5, 0))

        # Walidacja: tylko cyfry 0-9
        vcmd_mynum = (self.root.register(self.validate_mynum_input), '%P')
        self.entry_mynum = tk.Entry(
            frame_mynum,
            textvariable=self.mynum_var,
            width=20,
            validate='key',
            validatecommand=vcmd_mynum
        )
        self.entry_mynum.grid(row=0, column=0, padx=8, pady=8)

        label_hex = tk.Label(
            self.root,
            text=self.config.LABELS["numbers_list"],
            font=("Arial", 10, "bold")
        )
        label_hex.pack(pady=(10, 0))

        self.numbers_text = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.NONE,
            width=60,
            height=30,
            font=("Courier New", 12)
        )
        self.numbers_text.pack(pady=5, padx=10, fill="both", expand=True)

        self.text_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=110,
            height=15,
            font=("Courier New", 10)
        )
        self.text_area.pack(pady=10, padx=10, fill="both", expand=True)




    def on_close(self) -> None:
        """Zamyka aplikację i czyści zasoby."""
        self.cleanup_temp_files()
        self.root.destroy()


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = BramsterApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Krytyczny błąd aplikacji: {e}")
        logging.critical(f"Critical application error: {e}")
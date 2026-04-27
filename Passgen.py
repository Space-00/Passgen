#!/usr/bin/env python
import sys
import csv
import datetime
import math
import random
import re
import string

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QTabWidget, QStackedWidget, QLabel, QLineEdit, QTextEdit, QSpinBox,
    QComboBox, QCheckBox, QPushButton, QProgressBar, QTableWidget,
    QTableWidgetItem, QFileDialog, QMessageBox, QDialog, QGroupBox,
    QStatusBar
)

# ----------------------------------------------------------------------
# Embedded word list for passphrase generation (200+ common words)
# ----------------------------------------------------------------------
WORD_LIST = [
    "apple", "banana", "carrot", "dog", "elephant", "frog", "grape", "house",
    "igloo", "jungle", "kite", "lemon", "mango", "ninja", "octopus", "panda",
    "queen", "rabbit", "sun", "tree", "umbrella", "violet", "water", "xylophone",
    "yacht", "zebra", "airplane", "balloon", "candle", "diamond", "eagle", "flower",
    "guitar", "honey", "island", "jacket", "kangaroo", "ladder", "mountain", "notebook",
    "ocean", "penguin", "quilt", "rainbow", "star", "tiger", "unicorn", "volcano",
    "window", "xray", "yogurt", "zipper", "anchor", "bridge", "castle", "dragon",
    "engine", "forest", "garden", "hammer", "ice", "jewel", "key", "lighthouse",
    "moon", "needle", "owl", "pillow", "quiver", "river", "stone", "tower",
    "village", "wheel", "box", "yarn", "zero", "angel", "bubble", "camera",
    "desert", "echo", "feather", "glass", "helmet", "insect", "jigsaw", "knot",
    "lantern", "magnet", "nest", "orange", "puzzle", "rocket", "saddle", "tent",
    "vase", "whistle", "xenon", "yawn", "zinc", "acorn", "badge", "cabin",
    "daisy", "ember", "flame", "geode", "harbor", "iron", "jade", "kelp",
    "lily", "maple", "noodle", "olive", "pearl", "quill", "reed", "silk",
    "thorn", "velvet", "wheat", "ivy", "jasmine", "oak", "pine", "rose",
    "snow", "tulip", "willow", "clover", "fern", "grass", "hyacinth", "iris",
    "juniper", "lavender", "moss", "nettle", "orchid", "poppy", "quartz", "ruby",
    "sapphire", "topaz", "amber", "coral", "crystal", "emerald", "granite", "marble",
    "opal", "sand", "slate", "wood", "brick", "clay", "dust", "earth",
    "fire", "water", "air", "shadow", "light", "thunder", "frost", "mist",
    "rain", "storm", "wind", "cloud", "sunrise", "sunset", "twilight", "dawn",
    "dusk", "midnight", "noon", "evening", "winter", "spring", "summer", "autumn",
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december"
]

# ----------------------------------------------------------------------
# Common passwords list (used by the Analyzer)
# ----------------------------------------------------------------------
COMMON_PASSWORDS = [
    "password", "123456", "12345678", "1234", "qwerty", "12345", "dragon",
    "pussy", "baseball", "football", "letmein", "monkey", "696969", "abc123",
    "mustang", "michael", "shadow", "master", "jennifer", "111111", "2000",
    "jordan", "superman", "harley", "1234567", "hunter", "fuckme", "fuckyou",
    "trustno1", "ranger", "buster", "thomas", "tigger", "robert", "soccer",
    "batman", "test", "pass", "killer", "hockey", "george", "charlie",
    "andrew", "michelle", "love", "sunshine", "jessica", "pepper", "daniel",
    "access", "123456789", "654321", "joshua", "maggie", "starwars", "silver",
    "william", "dallas", "yankees", "123123", "ashley", "666666", "hello",
    "amanda", "orange", "biteme", "freedom", "computer", "sexy", "thunder",
    "nicole", "ginger", "heather", "hammer", "summer", "corvette", "taylor",
    "fucker", "austin", "1111", "merlin", "matthew", "121212", "golfer",
    "cheese", "princess", "martin", "chelsea", "patrick", "richard", "diamond",
    "yellow", "bigdog", "secret", "asdfgh", "sparky", "cowboy", "camaro",
    "anthony", "matrix", "iloveyou", "bailey", "1234567890", "einstein",
    "redsox", "boomer", "mickey", "cowboys", "edward", "johnson", "alexis",
    "broncos", "fireman", "happy", "lakers", "morgan", "liverpool", "samantha",
    "chicago", "steelers", "arsenal", "london", "paris", "messi", "ronaldo",
    "stella", "boston", "newyork", "losangeles", "tokyo", "sydney", "berlin",
    "rome", "madrid", "munich", "moscow", "beijing", "shanghai", "seoul",
    "india", "china", "japan", "brazil", "canada", "australia", "germany",
    "france", "italy", "spain", "portugal", "netherlands", "sweden", "norway",
    "finland", "denmark", "poland", "russia", "turkey", "greece", "egypt"
]


# ======================================================================
# Main Window
# ======================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Passgen")
        self.setMinimumSize(820, 640)
        self.history_data = []  # list of dicts: timestamp, passwords, type

        self.initUI()
        self.applyDarkTheme()
        self.setupStatusBar()

    # ---------- UI Setup ----------
    def initUI(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.generator_tab = self.create_generator_tab()
        self.analyzer_tab = self.create_analyzer_tab()
        self.history_tab = self.create_history_tab()
        self.settings_tab = self.create_settings_tab()

        self.tabs.addTab(self.generator_tab, "Generator")
        self.tabs.addTab(self.analyzer_tab, "Analyzer")
        self.tabs.addTab(self.history_tab, "History")
        self.tabs.addTab(self.settings_tab, "Settings")

        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def applyDarkTheme(self):
        dark = """
        QMainWindow {
            background-color: #2b2b2b;
        }
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
            font-family: "Segoe UI", Arial;
            font-size: 13px;
        }
        QTabWidget::pane {
            border: 1px solid #555;
            background-color: #2b2b2b;
        }
        QTabBar::tab {
            background-color: #3c3c3c;
            color: #ffffff;
            padding: 8px 15px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #555;
        }
        QLabel {
            color: #ffffff;
        }
        QLineEdit, QTextEdit, QSpinBox, QComboBox {
            background-color: #3c3c3c;
            border: 1px solid #555;
            color: #ffffff;
            padding: 4px;
        }
        QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
            border: 1px solid #1e90ff;
        }
        QPushButton {
            background-color: #0d6efd;
            color: white;
            border: none;
            padding: 8px 14px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1a79ff;
        }
        QPushButton:pressed {
            background-color: #0a58ca;
        }
        QProgressBar {
            border: 1px solid #555;
            border-radius: 5px;
            text-align: center;
            background-color: #3c3c3c;
            color: white;
        }
        QProgressBar::chunk {
            background-color: #0d6efd;
            border-radius: 5px;
        }
        QTableWidget {
            background-color: #3c3c3c;
            alternate-background-color: #2e2e2e;
            gridline-color: #555;
            color: #ffffff;
        }
        QHeaderView::section {
            background-color: #444;
            padding: 4px;
            border: 1px solid #555;
        }
        QScrollBar:vertical {
            background-color: #2b2b2b;
            width: 12px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background-color: #555;
            border-radius: 6px;
            min-height: 20px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QStatusBar {
            background-color: #1e1e1e;
            color: #aaaaaa;
        }
        QCheckBox {
            spacing: 8px;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        QSpinBox, QComboBox {
            min-height: 24px;
        }
        QGroupBox {
            border: 1px solid #555;
            border-radius: 5px;
            margin-top: 12px;
            padding-top: 20px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
            color: #ccc;
        }
        """
        self.setStyleSheet(dark)

    def setupStatusBar(self):
        self.status_label = QLabel(
            'Created by <a href="https://github.com/Space-00">Space-00</a>'
        )
        self.status_label.setOpenExternalLinks(True)
        self.statusBar().addPermanentWidget(self.status_label)
        self.statusBar().showMessage("Ready")

    # ---------- Generator Tab ----------
    def create_generator_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Mode selection
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Mode:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Random Characters", "Pronounceable", "Passphrase"])
        self.mode_combo.currentIndexChanged.connect(self.switch_generator_mode)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)

        # Stacked options
        self.generator_stack = QStackedWidget()
        self.char_page = self.create_char_page()
        self.pronounce_page = self.create_pronounce_page()
        self.passphrase_page = self.create_passphrase_page()
        self.generator_stack.addWidget(self.char_page)
        self.generator_stack.addWidget(self.pronounce_page)
        self.generator_stack.addWidget(self.passphrase_page)
        layout.addWidget(self.generator_stack)

        # Common controls: number of passwords + generate + auto-copy
        common_layout = QHBoxLayout()
        common_layout.addWidget(QLabel("Number:"))
        self.num_passwords_spin = QSpinBox()
        self.num_passwords_spin.setRange(1, 100)
        self.num_passwords_spin.setValue(1)
        common_layout.addWidget(self.num_passwords_spin)

        self.auto_copy_check = QCheckBox("Auto-copy first password")
        common_layout.addWidget(self.auto_copy_check)

        common_layout.addStretch()
        self.generate_btn = QPushButton("Generate Password(s)")
        self.generate_btn.clicked.connect(self.generate_passwords)
        common_layout.addWidget(self.generate_btn)
        layout.addLayout(common_layout)

        # Primary password output
        out_layout = QHBoxLayout()
        self.primary_pass_edit = QLineEdit()
        self.primary_pass_edit.setReadOnly(True)
        self.primary_pass_edit.setPlaceholderText("Generated password will appear here")
        copy_primary_btn = QPushButton("Copy")
        copy_primary_btn.clicked.connect(
            lambda: self.copy_to_clipboard(self.primary_pass_edit.text())
        )
        out_layout.addWidget(self.primary_pass_edit)
        out_layout.addWidget(copy_primary_btn)
        layout.addLayout(out_layout)

        # Strength display
        strength_layout = QHBoxLayout()
        self.strength_label = QLabel("Strength: N/A")
        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setValue(0)
        self.strength_bar.setTextVisible(True)
        strength_layout.addWidget(self.strength_label)
        strength_layout.addWidget(self.strength_bar)
        layout.addLayout(strength_layout)

        # All generated passwords
        self.all_passwords_edit = QTextEdit()
        self.all_passwords_edit.setReadOnly(True)
        self.all_passwords_edit.setPlaceholderText(
            "All generated passwords will appear here (for multiple)"
        )
        layout.addWidget(self.all_passwords_edit)

        # Action buttons for all
        all_btn_layout = QHBoxLayout()
        copy_all_btn = QPushButton("Copy All")
        copy_all_btn.clicked.connect(
            lambda: self.copy_to_clipboard(self.all_passwords_edit.toPlainText())
        )
        export_btn = QPushButton("Export to File")
        export_btn.clicked.connect(self.export_passwords)
        all_btn_layout.addWidget(copy_all_btn)
        all_btn_layout.addWidget(export_btn)
        all_btn_layout.addStretch()
        layout.addLayout(all_btn_layout)

        return tab

    def create_char_page(self):
        page = QWidget()
        layout = QFormLayout(page)

        self.char_length_spin = QSpinBox()
        self.char_length_spin.setRange(1, 128)
        self.char_length_spin.setValue(16)
        layout.addRow("Length:", self.char_length_spin)

        self.upper_check = QCheckBox("Uppercase (A-Z)")
        self.upper_check.setChecked(True)
        self.lower_check = QCheckBox("Lowercase (a-z)")
        self.lower_check.setChecked(True)
        self.digit_check = QCheckBox("Digits (0-9)")
        self.digit_check.setChecked(True)
        self.symbol_check = QCheckBox("Symbols")
        self.symbol_check.setChecked(True)

        layout.addRow(self.upper_check)
        layout.addRow(self.lower_check)
        layout.addRow(self.digit_check)
        layout.addRow(self.symbol_check)

        sym_layout = QHBoxLayout()
        sym_layout.addWidget(QLabel("Custom symbols:"))
        self.symbols_edit = QLineEdit("!@#$%^&*")
        self.symbols_edit.setEnabled(self.symbol_check.isChecked())
        self.symbol_check.toggled.connect(self.symbols_edit.setEnabled)
        sym_layout.addWidget(self.symbols_edit)
        layout.addRow(sym_layout)

        self.exclude_similar_check = QCheckBox(
            "Exclude similar characters (i, l, 1, L, o, 0, O)"
        )
        layout.addRow(self.exclude_similar_check)

        self.require_one_check = QCheckBox("Require at least one from each selected type")
        self.require_one_check.setChecked(True)
        layout.addRow(self.require_one_check)

        self.custom_chars_check = QCheckBox("Use custom characters only")
        self.custom_chars_edit = QLineEdit()
        self.custom_chars_edit.setPlaceholderText("Enter allowed characters")
        self.custom_chars_edit.setEnabled(False)
        self.custom_chars_check.toggled.connect(self.custom_chars_edit.setEnabled)
        layout.addRow(self.custom_chars_check, self.custom_chars_edit)

        return page

    def create_pronounce_page(self):
        page = QWidget()
        layout = QFormLayout(page)

        self.pron_length_spin = QSpinBox()
        self.pron_length_spin.setRange(4, 64)
        self.pron_length_spin.setValue(12)
        layout.addRow("Length:", self.pron_length_spin)

        self.pron_case_combo = QComboBox()
        self.pron_case_combo.addItems(["lowercase", "UPPERCASE", "Mixed Case"])
        layout.addRow("Case:", self.pron_case_combo)

        self.pron_add_digit_check = QCheckBox("Add a random digit at end")
        self.pron_add_symbol_check = QCheckBox("Add a random symbol at end")
        layout.addRow(self.pron_add_digit_check)
        layout.addRow(self.pron_add_symbol_check)

        return page

    def create_passphrase_page(self):
        page = QWidget()
        layout = QFormLayout(page)

        self.pass_num_words_spin = QSpinBox()
        self.pass_num_words_spin.setRange(3, 10)
        self.pass_num_words_spin.setValue(4)
        layout.addRow("Number of words:", self.pass_num_words_spin)

        self.pass_separator_combo = QComboBox()
        self.pass_separator_combo.setEditable(True)
        self.pass_separator_combo.addItems([" ", "-", "_", ".", ","])
        self.pass_separator_combo.setCurrentText("-")
        layout.addRow("Separator:", self.pass_separator_combo)

        self.pass_capitalize_check = QCheckBox("Capitalize each word")
        self.pass_add_digit_check = QCheckBox("Append a random digit")
        self.pass_add_symbol_check = QCheckBox("Append a random symbol")
        layout.addRow(self.pass_capitalize_check)
        layout.addRow(self.pass_add_digit_check)
        layout.addRow(self.pass_add_symbol_check)

        self.wordlist_count_label = QLabel(f"Wordlist size: {len(WORD_LIST)} words")
        layout.addRow(self.wordlist_count_label)

        return page

    def switch_generator_mode(self, index):
        self.generator_stack.setCurrentIndex(index)

    # ---------- Generation Logic ----------
    def generate_passwords(self):
        mode = self.mode_combo.currentIndex()  # 0: char, 1: pronounce, 2: passphrase
        count = self.num_passwords_spin.value()
        passwords = []
        try:
            if mode == 0:
                passwords = self._generate_char_passwords(count)
            elif mode == 1:
                passwords = self._generate_pronounce_passwords(count)
            else:
                passwords = self._generate_passphrase_passwords(count)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        if not passwords:
            return

        self.primary_pass_edit.setText(passwords[0])
        if len(passwords) > 1:
            self.all_passwords_edit.setPlainText("\n".join(passwords))
        else:
            self.all_passwords_edit.clear()

        # Update strength for the first password
        self._update_strength_display(passwords[0])

        # History
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        type_str = ["Random", "Pronounceable", "Passphrase"][mode]
        self.history_data.append({
            "timestamp": timestamp,
            "passwords": passwords.copy(),
            "type": type_str
        })
        self.refresh_history_table()

        # Auto-copy
        if self.auto_copy_check.isChecked():
            self.copy_to_clipboard(passwords[0])

    def _generate_char_passwords(self, count):
        if self.custom_chars_check.isChecked():
            pool = self.custom_chars_edit.text()
            if not pool:
                raise ValueError("Custom characters field is empty")
            require_one = False
        else:
            upper = string.ascii_uppercase if self.upper_check.isChecked() else ""
            lower = string.ascii_lowercase if self.lower_check.isChecked() else ""
            digits = string.digits if self.digit_check.isChecked() else ""
            symbols = self.symbols_edit.text() if self.symbol_check.isChecked() else ""
            pool = upper + lower + digits + symbols
            if not pool:
                raise ValueError("No character types selected")
            require_one = (
                self.require_one_check.isChecked() and
                (self.upper_check.isChecked() or self.lower_check.isChecked() or
                 self.digit_check.isChecked() or self.symbol_check.isChecked())
            )
            if self.exclude_similar_check.isChecked():
                similar = "il1Lo0O"
                pool = ''.join(c for c in pool if c not in similar)
                if not pool:
                    raise ValueError("All characters excluded by similarity filter")

        length = self.char_length_spin.value()
        passwords = []
        for _ in range(count):
            if require_one:
                must_have = []
                if self.upper_check.isChecked():
                    must_have.append(random.choice(string.ascii_uppercase))
                if self.lower_check.isChecked():
                    must_have.append(random.choice(string.ascii_lowercase))
                if self.digit_check.isChecked():
                    must_have.append(random.choice(string.digits))
                if self.symbol_check.isChecked():
                    syms = self.symbols_edit.text()
                    if syms:
                        must_have.append(random.choice(syms))
                remaining = length - len(must_have)
                if remaining < 0:
                    raise ValueError("Length too short for required character types")
                pwd_chars = [random.choice(pool) for _ in range(remaining)]
                for ch in must_have:
                    pos = random.randint(0, len(pwd_chars))
                    pwd_chars.insert(pos, ch)
                password = ''.join(pwd_chars)
            else:
                password = ''.join(random.choices(pool, k=length))
            passwords.append(password)
        return passwords

    def _generate_pronounce_passwords(self, count):
        length = self.pron_length_spin.value()
        case_mode = self.pron_case_combo.currentText()
        add_digit = self.pron_add_digit_check.isChecked()
        add_symbol = self.pron_add_symbol_check.isChecked()
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        passwords = []
        for _ in range(count):
            start_with_consonant = random.choice([True, False])
            chars = []
            for i in range(length):
                if (i % 2 == 0) == start_with_consonant:
                    chars.append(random.choice(consonants))
                else:
                    chars.append(random.choice(vowels))
            pwd = ''.join(chars)
            if case_mode == "lowercase":
                pwd = pwd.lower()
            elif case_mode == "UPPERCASE":
                pwd = pwd.upper()
            else:  # Mixed Case
                pwd = ''.join(
                    c.upper() if random.random() > 0.5 else c.lower() for c in pwd
                )
            if add_digit:
                pwd += random.choice(string.digits)
            if add_symbol:
                pwd += random.choice("!@#$%^&*")
            passwords.append(pwd)
        return passwords

    def _generate_passphrase_passwords(self, count):
        num_words = self.pass_num_words_spin.value()
        separator = self.pass_separator_combo.currentText()
        capitalize = self.pass_capitalize_check.isChecked()
        add_digit = self.pass_add_digit_check.isChecked()
        add_symbol = self.pass_add_symbol_check.isChecked()
        passwords = []
        for _ in range(count):
            chosen = random.choices(WORD_LIST, k=num_words)
            if capitalize:
                chosen = [w.capitalize() for w in chosen]
            pwd = separator.join(chosen)
            if add_digit:
                pwd += random.choice(string.digits)
            if add_symbol:
                pwd += random.choice("!@#$%^&*")
            passwords.append(pwd)
        return passwords

    def _update_strength_display(self, password):
        entropy = self._calculate_entropy(password)
        score = min(int(entropy * 100 / 128), 100)
        self.strength_bar.setValue(score)
        if score < 40:
            color = "#ff4d4d"
        elif score < 70:
            color = "#ffaa00"
        else:
            color = "#4caf50"
        self.strength_bar.setStyleSheet(
            f"QProgressBar::chunk {{ background-color: {color}; }}"
        )
        online_seconds = (2 ** entropy) / 100
        self.strength_label.setText(
            f"Entropy: {entropy:.1f} bits | Crack time (100/s): "
            f"{self._format_crack_time(online_seconds)}"
        )

    def _calculate_entropy(self, password):
        mode = self.mode_combo.currentIndex()
        if mode == 0:  # Random Characters
            if self.custom_chars_check.isChecked():
                pool_len = len(self.custom_chars_edit.text()) or 1
                return len(password) * math.log2(pool_len)
            pool = ""
            if self.upper_check.isChecked():
                pool += string.ascii_uppercase
            if self.lower_check.isChecked():
                pool += string.ascii_lowercase
            if self.digit_check.isChecked():
                pool += string.digits
            if self.symbol_check.isChecked():
                pool += self.symbols_edit.text()
            if self.exclude_similar_check.isChecked():
                similar = "il1Lo0O"
                pool = ''.join(c for c in pool if c not in similar)
            if not pool:
                return 0
            return len(password) * math.log2(len(pool))
        elif mode == 1:  # Pronounceable (approximation)
            case_factor = 2 if self.pron_case_combo.currentText() == "Mixed Case" else 1
            return len(password) * math.log2(26 * case_factor)
        else:  # Passphrase
            num = self.pass_num_words_spin.value()
            wl_size = len(WORD_LIST)
            ent = num * math.log2(wl_size)
            if self.pass_add_digit_check.isChecked():
                ent += math.log2(10)
            if self.pass_add_symbol_check.isChecked():
                ent += math.log2(10)  # assume 10 symbols
            return ent

    @staticmethod
    def _format_crack_time(seconds):
        if seconds < 1:
            return "instantly"
        elif seconds < 60:
            return f"{seconds:.1f} sec"
        elif seconds < 3600:
            return f"{seconds / 60:.1f} min"
        elif seconds < 86400:
            return f"{seconds / 3600:.1f} h"
        elif seconds < 31536000:
            return f"{seconds / 86400:.1f} days"
        else:
            return f"{seconds / 31536000:.1f} years"

    # ---------- Utility ----------
    def copy_to_clipboard(self, text):
        if text:
            QApplication.clipboard().setText(text)
            self.statusBar().showMessage("Copied to clipboard!", 2000)

    def export_passwords(self):
        text = self.all_passwords_edit.toPlainText()
        if not text:
            QMessageBox.warning(self, "No passwords", "No passwords to export.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Passwords", "", "Text files (*.txt);;All files (*)"
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
                self.statusBar().showMessage(f"Exported to {path}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save: {e}")

    # ---------- Analyzer Tab ----------
    def create_analyzer_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        input_layout = QHBoxLayout()
        self.analyze_line_edit = QLineEdit()
        self.analyze_line_edit.setPlaceholderText("Enter password to analyze...")
        self.analyze_line_edit.textChanged.connect(
            lambda: QTimer.singleShot(400, self.analyze_password)
        )
        paste_btn = QPushButton("Paste")
        paste_btn.clicked.connect(
            lambda: self.analyze_line_edit.setText(QApplication.clipboard().text())
        )
        input_layout.addWidget(self.analyze_line_edit)
        input_layout.addWidget(paste_btn)
        layout.addLayout(input_layout)

        self.analyze_group = QGroupBox("Strength Analysis")
        analyze_layout = QVBoxLayout(self.analyze_group)

        self.analyze_entropy_label = QLabel("Entropy: -")
        self.analyze_bar = QProgressBar()
        self.analyze_bar.setRange(0, 100)
        self.analyze_bar.setTextVisible(True)
        self.analyze_crack_label = QLabel("Crack time: -")
        self.analyze_common_label = QLabel("")
        self.analyze_common_label.setStyleSheet("color: red;")

        analyze_layout.addWidget(self.analyze_entropy_label)
        analyze_layout.addWidget(self.analyze_bar)
        analyze_layout.addWidget(self.analyze_crack_label)
        analyze_layout.addWidget(self.analyze_common_label)

        layout.addWidget(self.analyze_group)
        layout.addStretch()
        return tab

    def analyze_password(self):
        pwd = self.analyze_line_edit.text()
        if not pwd:
            self.analyze_entropy_label.setText("Entropy: -")
            self.analyze_crack_label.setText("Crack time: -")
            self.analyze_common_label.setText("")
            self.analyze_bar.setValue(0)
            return

        if pwd.lower() in (cp.lower() for cp in COMMON_PASSWORDS):
            self.analyze_common_label.setText("⚠ This password is in the common passwords list!")
        else:
            self.analyze_common_label.setText("")

        has_lower = any(c.islower() for c in pwd)
        has_upper = any(c.isupper() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_symbol = any(c in string.punctuation for c in pwd)
        pool_size = 0
        if has_lower: pool_size += 26
        if has_upper: pool_size += 26
        if has_digit: pool_size += 10
        if has_symbol: pool_size += len(string.punctuation)
        if pool_size == 0:
            pool_size = 1
        entropy = len(pwd) * math.log2(pool_size)

        # Penalty for common patterns
        penalty = 0
        sequences = [
            "abcdef", "bcdefg", "cdefgh", "defghi", "efghij", "fghijk",
            "ghijkl", "hijklm", "ijklmn", "jklmno", "klmnop", "lmnopq",
            "mnopqr", "nopqrs", "opqrst", "pqrstu", "qrstuv", "rstuvw",
            "stuvwx", "tuvwxy", "uvwxyz", "012345", "123456", "234567",
            "345678", "456789", "567890", "987654", "876543", "765432",
            "654321", "543210", "qwerty", "asdfgh", "zxcvbn"
        ]
        low = pwd.lower()
        for seq in sequences:
            if seq in low:
                penalty = max(penalty, 20)
                break
        if re.search(r'(.)\1{3,}', pwd):
            penalty = max(penalty, 20)

        entropy = max(0, entropy - penalty)
        score = min(int(entropy * 100 / 128), 100)
        self.analyze_bar.setValue(score)
        color = "#ff4d4d" if score < 40 else ("#ffaa00" if score < 70 else "#4caf50")
        self.analyze_bar.setStyleSheet(
            f"QProgressBar::chunk {{ background-color: {color}; }}"
        )
        self.analyze_entropy_label.setText(f"Entropy: {entropy:.1f} bits")

        online = (2 ** entropy) / 100
        slow = (2 ** entropy) / 1e4
        fast = (2 ** entropy) / 1e9
        self.analyze_crack_label.setText(
            f"Online (100/s): {self._format_crack_time(online)}\n"
            f"Offline slow (10^4/s): {self._format_crack_time(slow)}\n"
            f"Offline fast (10^9/s): {self._format_crack_time(fast)}"
        )

    # ---------- History Tab ----------
    def create_history_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(
            ["Timestamp", "Password", "Type", "Copy"]
        )
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.history_table)

        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear History")
        clear_btn.clicked.connect(self.clear_history)
        export_csv_btn = QPushButton("Export History (CSV)")
        export_csv_btn.clicked.connect(self.export_history_csv)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(export_csv_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        return tab

    def refresh_history_table(self):
        table = self.history_table
        table.setRowCount(0)
        for entry in self.history_data:
            for pwd in entry["passwords"]:
                row = table.rowCount()
                table.insertRow(row)
                table.setItem(row, 0, QTableWidgetItem(entry["timestamp"]))
                table.setItem(row, 1, QTableWidgetItem(pwd))
                table.setItem(row, 2, QTableWidgetItem(entry["type"]))
                copy_btn = QPushButton("Copy")
                copy_btn.clicked.connect(
                    lambda checked, p=pwd: self.copy_to_clipboard(p)
                )
                table.setCellWidget(row, 3, copy_btn)
        table.resizeColumnsToContents()

    def clear_history(self):
        self.history_data.clear()
        self.refresh_history_table()
        self.statusBar().showMessage("History cleared", 3000)

    def export_history_csv(self):
        if not self.history_data:
            QMessageBox.warning(self, "No data", "No history to export.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export History", "", "CSV files (*.csv);;All files (*)"
        )
        if path:
            try:
                with open(path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Timestamp", "Password", "Type"])
                    for entry in self.history_data:
                        for pwd in entry["passwords"]:
                            writer.writerow([entry["timestamp"], pwd, entry["type"]])
                self.statusBar().showMessage(f"History exported to {path}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export: {e}")

    # ---------- Settings Tab ----------
    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        group = QGroupBox("Custom Wordlist")
        wl_layout = QVBoxLayout(group)
        self.load_wordlist_btn = QPushButton("Load Wordlist from File")
        self.load_wordlist_btn.clicked.connect(self.load_custom_wordlist)
        self.wordlist_info_label = QLabel("Default wordlist loaded.")
        wl_layout.addWidget(self.load_wordlist_btn)
        wl_layout.addWidget(self.wordlist_info_label)
        layout.addWidget(group)
        layout.addStretch()
        return tab

    def load_custom_wordlist(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Wordlist File", "", "Text files (*.txt);;All files (*)"
        )
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    words = [line.strip() for line in f if line.strip()]
                if len(words) < 10:
                    QMessageBox.warning(
                        self, "Too few words", "Wordlist must have at least 10 words."
                    )
                    return
                global WORD_LIST
                WORD_LIST = words
                self.wordlist_info_label.setText(
                    f"Custom wordlist loaded: {len(words)} words."
                )
                self.wordlist_count_label.setText(f"Wordlist size: {len(WORD_LIST)} words")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load: {e}")

    # ---------- About Dialog ----------
    def show_about(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("About Passgen")
        layout = QVBoxLayout(dlg)
        label = QLabel(
            '<h2>Passgen</h2>'
            '<p>The Insane Password Generator</p>'
            '<p>Version 1.0</p>'
            '<p>Created by <a href="https://github.com/Space-00">Space-00</a></p>'
        )
        label.setOpenExternalLinks(True)
        layout.addWidget(label)
        btn = QPushButton("Close")
        btn.clicked.connect(dlg.accept)
        layout.addWidget(btn)
        dlg.exec()


# ======================================================================
# Entry point
# ======================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

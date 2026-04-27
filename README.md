# Passgen - The Insane Password Generator

Passgen is a feature‑rich, dark‑themed password generator for desktop, written in Python and PyQt6.  
It creates strong, random passwords like those recommended by Google, and includes an advanced strength analyzer, history, export, and custom wordlists.

Created by [Space‑00](https://github.com/Space-00).

![Screenshot](url)

## Features

- Three generation modes  
  - *Random Characters* – fully customizable character sets, exclude similar characters, require at least one from each type.  
  - *Pronounceable* – alternates consonants and vowels, with case and digit/symbol options.  
  - *Passphrase* – using a built‑in 200+ word list (custom wordlist support via Settings tab), customizable separator, capitalisation, and extra digits/symbols.

- Strength Meter  
  Entropy calculation and visual progress bar with colour‑coded feedback.  
  Estimated crack times for online (100 guesses/s), offline slow (10⁴/s), and offline fast (10⁹/s) attacks.

- Password Analyzer  
  Paste or type any password to instantly see its entropy score, crack‑time projections, and a warning if it appears in a list of common passwords. Detects keyboard walks and repeated characters.

- Auto‑copy & Batch Generation  
  Generate up to 100 passwords at once. The primary password is displayed prominently, and all results can be copied or exported to a text file.

- History Tab  
  Every generated password is saved with a timestamp and generation type. Entries can be copied individually and the whole history exported as a CSV file.

- Custom Wordlist  
  Load any .txt file (one word per line) from the Settings tab to use your own vocabulary for passphrases.

- Dark Theme  
  The entire UI uses a carefully styled dark colour scheme, reducing eye strain and looking great.

- Credits  
  The status bar permanently shows “Created by Space‑00” with a clickable link to the creator’s GitHub profile.

## Installation

### Prerequisites
- Python 3.7 or higher
- PyQt6

### 1. Clone the repository
git clone https://github.com/Space-00/passgen.git
cd passgen

2. Install dependencies

pip install PyQt6
No other packages are required. The app uses only Python’s standard library and PyQt6.

3. Run the application

python passgen.py
(If you saved the script as passgen.py)

Usage

1. Generate a password
      Choose a mode from the dropdown, adjust the options (length, character sets, separators, etc.), set the number of passwords, and click Generate Password(s).
      The first password appears in the main field, and all generated passwords are listed below.
2. Analyze a password
      Switch to the Analyzer tab, paste or type any password, and the strength, entropy, crack times, and common‑password warning update instantly.
3. History
      The History tab records every password you generate. Click the Copy button next to an entry to copy it, or use Export History (CSV) to save everything.
4. Custom wordlist
      Go to Settings, click Load Wordlist from File, and choose a .txt file with at least 10 words. The passphrase generator will then use those words.
5. Export
      In the Generator tab, click Export to File to save all currently generated passwords as a .txt file.

Building a Standalone Executable

You can package Passgen into a single executable using PyInstaller:

pip install pyinstaller
pyinstaller --onefile --windowed passgen.py
The executable will be inside the dist folder.

Contributing

Pull requests are welcome. If you find a bug or have a feature idea, please open an issue first to discuss what you would like to change.

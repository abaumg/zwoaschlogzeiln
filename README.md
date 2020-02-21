# ZwoaSchlogzeiln
## Installation
- Code herunterladen: `git clone https://github.com/abaumg/zwoaschlogzeiln`
- Python-Module laden: `pip3 install -r requirements.txt`
- deutsches SpaCy-Sprachmodell laden: `python3 -m spacy download de`
- Konfigurationsdatei kopieren: `cp zwoaschlogzeiln.ini.example zwoaschlogzeiln.ini`
- Twitter-Zugangsdaten konfigurieren
- Feeds konfigurieren: im Abschnitt `[sources]` eine Zeile pro Feed eintragen: `feedname=feedurl` (feedname ist frei wählbar)
- eventuelle feedspezifische Anpassungen programmieren:
  - `cp feedspezifika.py.example feedspezifika.py`
  - Funktion muss gleich heißen wie `feedname=` in `zwoaschlogzeiln.ini`

# ZwoaSchlogzeiln
## Installation
- Code herunterladen: `git clone https://github.com/abaumg/zwoaschlogzeiln`
- Python-Module laden: `pip3 install -r requirements.txt`
- deutsches SpaCy-Sprachmodell laden: `python3 -m spacy download de`
- Konfigurationsdatei kopieren: `cp zwoaschlogzeiln.ini.example zwoaschlogzeiln.ini`
- Twitter-Zugangsdaten konfigurieren
- Feeds konfigurieren: im Abschnitt `[sources]` eine Zeile pro Feed eintragen: `feedname=feedurl` (feedname ist frei wählbar)
- eventuelle feedspezifische Anpassungen programmieren, wobei `xxx` identisch sein muss mit`feedname=` in `zwoaschlogzeiln.ini`:
  - `cp feedspezifika.py.example feedspezifika.py`
  - Funktion zur Manipulation des gesamten Feeds: `filter_items_xxx`
  - Funktion zur Manipulation eines einzelnen Feedeintrags: `filter_content_xxx`

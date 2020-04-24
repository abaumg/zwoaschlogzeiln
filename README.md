# ZwoaSchlogzeiln
## Installation
- Code herunterladen: `git clone https://github.com/abaumg/zwoaschlogzeiln`
- Python-Module laden: `pip3 install -r requirements.txt`
- deutsches SpaCy-Sprachmodell laden: `python3 -m spacy download de`
- Konfigurationsdatei kopieren: `cp zwoaschlogzeiln.ini.example zwoaschlogzeiln.ini`
- Twitter-Zugangsdaten konfigurieren
- Feeds konfigurieren: im Abschnitt `[sources]` eine Zeile pro Feed eintragen: `feedname=feedurl` (feedname ist frei wählbar)
- eventuelle feedspezifische Anpassungen programmieren, wobei `xxx` identisch sein muss mit`feedname=` in `zwoaschlogzeiln.ini`:
-  `cp feedspezifika.py.example feedspezifika.py`
- Funktion zur Manipulation des gesamten Feeds: `filter_items_xxx`
- Funktion zur Manipulation eines einzelnen Feedeintrags: `filter_content_xxx`
  
 
## Beispiel für Anpassungen:
Die Nachrichtenseite nachrichten.it bietet keinen RSS-Feed an und steht somit als Quelle für ZwoaSchlogzeilen nicht zur Verfügung. Allerdings gibt es ein proprietäres JSON-File, das die Nachrichten enthält. Mit einem Filter `filter_content_nachrichtenit` kann das JSON-File ganz einfach ausgelesen und in einen RSS-Feed umgewandelt werden:

    import json
    import rfeed
    
    def filter_items_nachrichtenit(entry):
        """ Nur Nachrichten aus den Kategorien Lokal und National berücksichtigen """
        if entry.author in ('Lokal', 'National'):
            return entry
        return None
    
    def filter_content_nachrichtenit(content):
        """ Proprietäres JSON-File zu RSS konvertieren """
        itemlist = []
        for item in json.loads(content):
            itemlist.append(
                rfeed.Item(
                    title = item.get('titel'),
                    link = item.get('plink'),
                    description = item.get('text'),
                    guid = rfeed.Guid(item.get('uid')),
                    author = item.get('verortung'),
                )
            )
  
    feed = rfeed.Feed(
        title = 'nachrichten.it',
        items = itemlist,
        link = 'http://www.suedtirolnews.it',
        description = 'Bogus',
    )
  
    return feed.rss()
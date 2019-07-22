import feedparser
import spacy
from random import choice


class ZwoaSchlogzeiln():
    def cleanup(self, titel):
        chars = ['„', '“', '”']
        for char in chars:
            titel = titel.replace(char, '')
        return titel


    def __init__(self):
        # Feeds laden
        stol = feedparser.parse('https://www.stol.it/rss/feed/AlleRessorts')
        tz = feedparser.parse('https://www.tageszeitung.it/feed')
        snews = feedparser.parse('https://www.suedtirolnews.it/nachrichten/suedtirol-lokal/feed')
        ut24 = feedparser.parse('https://www.unsertirol24.com/category/suedtirol/feed/')

        # SpaCy initialisieren
        self.nlp = spacy.load('de')

        # Globale Variablen
        self.titel = []
        self.kurzetitel = []
        self.subj = []

        # Feeds parsen
        # Stol
        for entry in stol.entries:
            if '/Lokal/' in entry.link: # nur lokale News
                if entry['title'].count(' ') > 1:
                    self.titel.append(self.cleanup(entry['title']))
                else:
                    self.kurzetitel.append(self.cleanup(entry['title']))
        
        # Tageszeitung
        for entry in tz.entries:
            if entry['title'].count(' ') > 1:
                self.titel.append(self.cleanup(entry['title']))
            else:
                self.kurzetitel.append(self.cleanup(entry['title']))

        # Südtirolnews
        for entry in snews.entries:
            if entry['title'].count(' ') > 1:
                self.titel.append(self.cleanup(entry['title']))
            else:
                self.kurzetitel.append(self.cleanup(entry['title']))

        # UnserTirol24
        for entry in ut24.entries:
            if entry['title'].count(' ') > 1:
                self.titel.append(self.cleanup(entry['title']))
            else:
                self.kurzetitel.append(self.cleanup(entry['title']))

        # Sämtliche Titel durch SpaCy jagen und eine Liste aller Nomen und Eigennamen erstellen
        for titel in (self.titel + self.kurzetitel):	# für den Korpus sind die kurzen Titel gut genug
            titel = self.nlp(titel)
            tsubj = [str(k) for k in titel if k.pos_ in ('PROPN', 'NOUN')]
            self.subj = self.subj + tsubj


    def schlagzeile_generieren(self):
        # Zufällige Schlagzeile wählen und nochmals durch SpaCy jagen
        satz = choice(self.titel)
        satz = self.nlp(satz)

        # Von der ausgewählten Schlagzeile ebenfalls alle Nomen und Eigennamen extrahieren
        satzsubj = [str(k) for k in satz if k.pos_ in ('PROPN', 'NOUN')]
        
        # Alle Wörter in eine neue Liste kopieren
        satzneu = []
        satzneu = ' '.join([str(k) for k in satz])
        
        # Zufällig einen Nomen/Eigennamen auswählen, der ersetzt werden soll
        wortalt = choice(satzsubj)
        
        # Ausgewähltes Wort aus der Wortliste streichen
        self.subj.remove(wortalt)

        # Zufällig einen Nomen/Eigennamen auswählen aus der Liste aller Nomen/Eigennamen...
        wortneu = choice(self.subj)

        # ... und ersetzen
        satzneu = satzneu.replace(str(wortalt), str(wortneu))

        # Punktuation bereinigen
        satzneu = satzneu.replace(' : ', ': ')
        satzneu = satzneu.replace(' . ', '. ')
        satzneu = satzneu.replace(' ?', '?')
        satzneu = satzneu.replace(' .', '.')
        satzneu = satzneu.replace(' !', '!')

        # Fertig!
        return satzneu
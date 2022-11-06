import feedparser
import os
import requests
import spacy
from random import choice
from configparser import ConfigParser

try:
    from feedspezifika import *
except ImportError:
    pass


class ZwoaSchlogzeiln:
    def cleanup(self, titel):
        chars = ["„", "“", "”"]
        for char in chars:
            titel = titel.replace(char, "")
        return titel

    def ist_unbedenklich(self, titel):
        stopwords = [
            "tragisch",
            "tod",
            "tot",
            "tödlich",
            "stirbt",
            "gestorben",
            "unglück",
            "opfer",
            "trauer",
        ]
        for stopword in stopwords:
            if stopword.strip().lower() in titel.lower():
                return False
        return True

    def __init__(self):
        self.titel = []
        self.kurzetitel = []
        self.subj = []

        cfg = ConfigParser()
        cfg.read(os.path.join(os.path.dirname(__file__), "zwoaschlogzeiln.ini"))

        # Konfigurierte Sources parsen
        for name, url in cfg.items("sources"):

            resp = requests.get(url)
            content = resp.content
            try:
                content = globals()["filter_content_" + name](content)
            except KeyError:
                pass

            feed = feedparser.parse(content)

            # Feedspezifische Filter anwenden, d.h. feedspezifika.<feedname>() aufrufen (sofern existent)
            for entry in feed.entries:
                try:
                    entry = globals()["filter_items_" + name](entry)
                except KeyError:
                    # entry unverändert lassen
                    pass
                if (
                    entry
                ):  # Weitermachen, falls der Entry noch existiert und nicht weggefiltert (=auf None gesetzt) wurde
                    if self.ist_unbedenklich(entry["title"]) is True:
                        if entry["title"].count(" ") > 1:
                            self.titel.append(self.cleanup(entry["title"]))
                        else:
                            self.kurzetitel.append(self.cleanup(entry["title"]))

        # SpaCy initialisieren
        self.nlp = spacy.load("de_core_news_sm")

        # Sämtliche Titel durch SpaCy jagen und eine Liste aller Nomen und Eigennamen erstellen
        for titel in (
            self.titel + self.kurzetitel
        ):  # für den Korpus sind die kurzen Titel gut genug
            titel = self.nlp(titel)
            tsubj = [str(k) for k in titel if k.pos_ in ("PROPN", "NOUN")]
            self.subj = self.subj + tsubj

    def schlagzeile_generieren(self):
        # Zufällige Schlagzeile wählen und nochmals durch SpaCy jagen
        satz = choice(self.titel)
        satz = self.nlp(satz)

        # Von der ausgewählten Schlagzeile ebenfalls alle Nomen und Eigennamen extrahieren
        satzsubj = [str(k) for k in satz if k.pos_ in ("PROPN", "NOUN")]

        # Alle Wörter in eine neue Liste kopieren
        satzneu = []
        satzneu = " ".join([str(k) for k in satz])

        # Zufällig einen Nomen/Eigennamen auswählen, der ersetzt werden soll
        wortalt = choice(satzsubj)

        # Ausgewähltes Wort aus der Wortliste streichen
        self.subj.remove(wortalt)

        # Zufällig einen Nomen/Eigennamen auswählen aus der Liste aller Nomen/Eigennamen...
        wortneu = choice(self.subj)

        # ... und ersetzen
        satzneu = satzneu.replace(str(wortalt), str(wortneu))

        # Punktuation bereinigen
        satzneu = satzneu.replace(" : ", ": ")
        satzneu = satzneu.replace(" . ", ". ")
        satzneu = satzneu.replace(" , ", ", ")
        satzneu = satzneu.replace(" ?", "?")
        satzneu = satzneu.replace(" .", ".")
        satzneu = satzneu.replace(" !", "!")

        # Fertig!
        return satzneu

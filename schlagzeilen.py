import feedparser
import spacy
from random import choice


def cleanup(titel):
    chars = ['„', '“', '”']
    for char in chars:
        titel = titel.replace(char, '')
    return titel


# Init
stol = feedparser.parse('https://www.stol.it/rss/feed/AlleRessorts')
tz = feedparser.parse('https://www.tageszeitung.it/feed')
snews = feedparser.parse('https://www.suedtirolnews.it/nachrichten/suedtirol-lokal/feed')
ut24 = feedparser.parse('https://www.unsertirol24.com/category/suedtirol/feed/')
titel = []
kurzetitel = []
subj = []
propn = []
noun = []

nlp = spacy.load('de')


# Feeds holen
for entry in stol.entries:
    if '/Lokal/' in entry.link:
        if entry['title'].count(' ') > 1:
            titel.append(cleanup(entry['title']))
        else:
            kurzetitel.append(cleanup(entry['title']))
for entry in tz.entries:
    if entry['title'].count(' ') > 1:
        titel.append(cleanup(entry['title']))
    else:
        kurzetitel.append(cleanup(entry['title']))
for entry in snews.entries:
    if entry['title'].count(' ') > 1:
        titel.append(cleanup(entry['title']))
    else:
        kurzetitel.append(cleanup(entry['title']))
for entry in ut24.entries:
    if entry['title'].count(' ') > 1:
        titel.append(cleanup(entry['title']))
    else:
        kurzetitel.append(cleanup(entry['title']))


for t in (titel + kurzetitel):	# für den Korpus sind die kurzen Titel
    t = nlp(t)
    tsubj = [str(k) for k in t if k.pos_ in ('PROPN', 'NOUN')]
    tpropn = [k for k in t if k.tag_ in ('NE')]	# Eigennamen
    tnoun = [k for k in t if k.tag_ in ('NN')]	# gewöhnliche Nouns
    propn = propn + tpropn
    noun = noun + tnoun
    subj = subj + tsubj

satzneu = []
satz = choice(titel)
satz = nlp(satz)

satzsubj = [str(k) for k in satz if k.pos_ in ('PROPN', 'NOUN')]
satzneu = ' '.join([str(k) for k in satz])
wortalt = choice(satzsubj)
subj.remove(wortalt)
wortneu = choice(subj)
satzneu = satzneu.replace(str(wortalt), str(wortneu))

# Endreinigung
satzneu = satzneu.replace(' : ', ': ')
satzneu = satzneu.replace(' . ', '. ')

# Ausgabe
print(satz)
print(wortalt, wortneu)
print(satzneu)


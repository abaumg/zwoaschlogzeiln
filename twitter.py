import os
from twython import Twython
from schlagzeilen import ZwoaSchlogzeiln

try:
    CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
    OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']
except KeyError:
    quit('Twitter-Zugangsdaten sind fehlerhaft')

# Twitter-Login durchführen
twitterclient = Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# Schlagzeile generieren
tweettext = ZwoaSchlogzeiln().schlagzeile_generieren()

print(tweettext)
if tweettext:
    # twittern!
    twitterclient.update_status(status=tweettext)
import os
from twython import Twython
from schlagzeilen import ZwoaSchlogzeiln
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('zwoaschlogzeiln.ini')

# Twitter-Login durchführen
twitterclient = Twython(
    cfg.get('twitter', 'consumer_key'),
    cfg.get('twitter', 'consumer_secret'),
    cfg.get('twitter', 'oauth_token'),
    cfg.get('twitter', 'oauth_token_secret')
    )

# Schlagzeile generieren
tweettext = ZwoaSchlogzeiln().schlagzeile_generieren()

if tweettext:
    # twittern!
    twitterclient.update_status(status=tweettext)
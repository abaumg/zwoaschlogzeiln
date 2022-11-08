import os
from twython import Twython
from mastodon import Mastodon
from schlagzeilen import ZwoaSchlogzeiln
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read(os.path.join(os.path.dirname(__file__), "zwoaschlogzeiln.ini"))

# Twitter-Login durchführen
twitterclient = Twython(
    cfg.get("twitter", "consumer_key"),
    cfg.get("twitter", "consumer_secret"),
    cfg.get("twitter", "oauth_token"),
    cfg.get("twitter", "oauth_token_secret"),
)

# Mastodon
mastodon = Mastodon(
    access_token=cfg.get("mastodon", "access_token"),
    api_base_url=cfg.get("mastodon", "instance_url"),
)

ZS = ZwoaSchlogzeiln()

# Schlagzeile generieren
tweettext = ZS.schlagzeile_generieren()

if tweettext:
    # twittern!
    twitterclient.update_status(status=tweettext)
    mastodon.status_post(
        status=tweettext,
        visibility="unlisted",
    )

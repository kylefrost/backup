import tweepy
from keys import server_keys

def Tweet(tweet):
    auth = tweepy.OAuthHandler(server_keys['consumer_key'], server_keys['consumer_secret'])
    auth.secure = True
    auth.set_access_token(server_keys['access_token'], server_keys['access_token_secret'])

    api = tweepy.API(auth)

    api.update_status(status=tweet)

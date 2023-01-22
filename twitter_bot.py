import requests
from requests_oauthlib import OAuth1
import os


consumer_key = '..' #os.environ.get("CONSUMER_KEY")
consumer_secret = '..' #os.environ.get("CONSUMER_SECRET")
access_token = '..' # os.environ.get("ACCESS_TOKEN")
access_token_secret = '..' #os.environ.get("ACCESS_TOKEN_SECRET")

def random_fact():
    fact = requests.get("https://catfact.ninja/fact?max_length=280").json()
    return fact["fact"]


def format_twit(fact):
    return {"text": "{}".format(fact)}


def connect_to_oauth(consumer_key, consumer_secret, acccess_token, access_token_secret):
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(consumer_key, consumer_secret, acccess_token, access_token_secret)
    return url, auth


def twit_payload(text, twit_url):
    fact = text + '\n\n' + twit_url
    payload = format_twit(fact)
    url, auth = connect_to_oauth(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    request = requests.post(
        auth=auth, url=url, json=payload, headers={"Content-Type": "application/json"}
    )

if __name__ == '__main__':
    twit_payload('¡El Al Nassr de Ronaldo tiene un nuevo arquero y hasta el Inter le tenía el ojo puesto!', 'https://www.cancha24.com/2023/01/al-nassr-de-ronaldo-tiene-un-nuevo.html')